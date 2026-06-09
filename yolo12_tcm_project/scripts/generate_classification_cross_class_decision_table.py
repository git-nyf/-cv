from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from path_utils import resolve_project_path


ALLOWED_DECISION_STATUS = ["pending", "decided", "needs_expert_review", "defer"]
ALLOWED_ACTIONS = [
    "",
    "keep_chosen_class_remove_others",
    "move_all_to_chosen_class",
    "keep_all_as_is",
    "remove_all_uncertain",
    "needs_expert_review",
]
MANUAL_FIELDS = [
    "decision_status",
    "chosen_class",
    "action",
    "remove_relative_paths",
    "move_to_class",
    "reviewer",
    "reviewed_at",
    "decision_note",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_path(value: str) -> str:
    return str(Path(value.replace("\\", "/")))


def load_existing_decisions(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    payload = read_json(path)
    decisions = payload.get("decisions", []) if isinstance(payload, dict) else []
    return {str(item.get("group_id")): item for item in decisions if item.get("group_id")}


def default_manual_fields() -> dict[str, Any]:
    return {
        "decision_status": "pending",
        "chosen_class": "",
        "action": "",
        "remove_relative_paths": [],
        "move_to_class": "",
        "reviewer": "",
        "reviewed_at": "",
        "decision_note": "",
    }


def merge_manual_fields(decision: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    merged = {**decision, **default_manual_fields()}
    if not existing:
        return merged
    for key in MANUAL_FIELDS:
        if key in existing:
            merged[key] = existing[key]
    if isinstance(merged.get("remove_relative_paths"), str):
        merged["remove_relative_paths"] = [
            normalize_path(item.strip())
            for item in merged["remove_relative_paths"].split(";")
            if item.strip()
        ]
    else:
        merged["remove_relative_paths"] = [
            normalize_path(str(item)) for item in merged.get("remove_relative_paths", [])
        ]
    return merged


def build_decision(group: dict[str, Any]) -> dict[str, Any]:
    records = group.get("records", [])
    record_paths = [normalize_path(str(record.get("relative_path", ""))) for record in records]
    split_counts = Counter(record.get("split", "") for record in records)
    class_counts = Counter(record.get("class_name", "") for record in records)
    return {
        "group_id": group.get("group_id", ""),
        "sha256": group.get("sha256", ""),
        "sha256_short": group.get("sha256_short", str(group.get("sha256", ""))[:16]),
        "risk_level": group.get("risk_level", ""),
        "record_count": len(records),
        "splits": dict(sorted(split_counts.items())),
        "classes": sorted(class_name for class_name in class_counts if class_name),
        "record_relative_paths": record_paths,
        "record_summary": [
            {
                "split": record.get("split", ""),
                "class_name": record.get("class_name", ""),
                "relative_path": normalize_path(str(record.get("relative_path", ""))),
                "path": record.get("path", ""),
                "exists": bool(record.get("exists")),
            }
            for record in records
        ],
        "suggested_action": group.get("suggested_action", ""),
    }


def validate_decision(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    group_id = decision.get("group_id", "<missing>")
    classes = set(decision.get("classes", []))
    record_paths = set(decision.get("record_relative_paths", []))
    status = decision.get("decision_status")
    action = decision.get("action")
    chosen_class = decision.get("chosen_class", "")
    move_to_class = decision.get("move_to_class", "")
    remove_paths = set(decision.get("remove_relative_paths", []))

    if status not in ALLOWED_DECISION_STATUS:
        errors.append(f"{group_id}: invalid decision_status={status!r}")
    if action not in ALLOWED_ACTIONS:
        errors.append(f"{group_id}: invalid action={action!r}")
    if status == "decided" and not action:
        errors.append(f"{group_id}: decided rows must set action")
    if action in {"keep_chosen_class_remove_others", "move_all_to_chosen_class"} and chosen_class not in classes:
        errors.append(f"{group_id}: chosen_class must be one of classes for action={action}")
    if move_to_class and move_to_class not in classes:
        errors.append(f"{group_id}: move_to_class must be one of classes")
    unknown_remove_paths = sorted(remove_paths - record_paths)
    if unknown_remove_paths:
        errors.append(f"{group_id}: remove_relative_paths not in group records: {unknown_remove_paths}")
    return errors


def build_table(review_package: Path, existing_table: Path | None = None) -> dict[str, Any]:
    package = read_json(review_package)
    existing_by_group = load_existing_decisions(existing_table)
    decisions = [
        merge_manual_fields(build_decision(group), existing_by_group.get(str(group.get("group_id"))))
        for group in package.get("groups", [])
    ]
    validation_errors = [error for decision in decisions for error in validate_decision(decision)]
    status_counts = Counter(decision.get("decision_status", "pending") for decision in decisions)
    summary = {
        "status": "ready_for_manual_decision" if not validation_errors else "invalid_decision_table",
        "source_review_status": package.get("summary", {}).get("status"),
        "groups": len(decisions),
        "records": sum(int(decision.get("record_count", 0)) for decision in decisions),
        "pending_decisions": int(status_counts.get("pending", 0)),
        "decided_groups": int(status_counts.get("decided", 0)),
        "needs_expert_review_groups": int(status_counts.get("needs_expert_review", 0)),
        "deferred_groups": int(status_counts.get("defer", 0)),
        "validation_errors": len(validation_errors),
    }
    return {
        "schema_version": 1,
        "source_review_package": str(review_package),
        "summary": summary,
        "allowed_decision_status": ALLOWED_DECISION_STATUS,
        "allowed_actions": ALLOWED_ACTIONS,
        "manual_fields": MANUAL_FIELDS,
        "decisions": decisions,
        "validation_errors": validation_errors,
        "boundary_note": (
            "本决策表只把跨类别 exact duplicate 复核结果整理为可填写输入；"
            "默认不自动删除、移动、重命名、重标或复制任何图片。"
        ),
        "usage_note": (
            "人工填写 decision_status、chosen_class、action、remove_relative_paths、reviewer、reviewed_at 和 decision_note 后，"
            "应先重新运行本脚本合并并校验，再由后续清理脚本消费。"
        ),
    }


def write_csv(table: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "group_id",
        "sha256_short",
        "risk_level",
        "record_count",
        "splits",
        "classes",
        "record_relative_paths",
        "suggested_action",
        *MANUAL_FIELDS,
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for decision in table["decisions"]:
            row = {key: decision.get(key, "") for key in fieldnames}
            row["splits"] = json.dumps(decision.get("splits", {}), ensure_ascii=False)
            row["classes"] = ";".join(decision.get("classes", []))
            row["record_relative_paths"] = ";".join(decision.get("record_relative_paths", []))
            row["remove_relative_paths"] = ";".join(decision.get("remove_relative_paths", []))
            writer.writerow(row)


def write_markdown(table: dict[str, Any], output: Path, csv_path: Path) -> None:
    summary = table["summary"]
    lines = [
        "# 分类跨类别标签冲突决策表",
        "",
        f"- 来源复核包: `{table['source_review_package']}`",
        f"- 状态: `{summary['status']}`",
        f"- 待决策组: {summary['pending_decisions']} / {summary['groups']}",
        f"- 已决策组: {summary['decided_groups']}",
        f"- 需专家复核组: {summary['needs_expert_review_groups']}",
        f"- 延后处理组: {summary['deferred_groups']}",
        f"- 校验错误: {summary['validation_errors']}",
        f"- CSV 填写表: `{csv_path}`",
        "",
        "## 边界说明",
        "",
        table["boundary_note"],
        "",
        "## 填写字段",
        "",
        "| 字段 | 说明 |",
        "|---|---|",
        "| decision_status | pending / decided / needs_expert_review / defer |",
        "| chosen_class | 确认后的真实类别；涉及保留或移动到某一类别时必填 |",
        "| action | keep_chosen_class_remove_others / move_all_to_chosen_class / keep_all_as_is / remove_all_uncertain / needs_expert_review |",
        "| remove_relative_paths | 需要移除的相对路径，多个路径用分号分隔 |",
        "| move_to_class | 需要统一移动到的类别；没有移动动作时留空 |",
        "| reviewer / reviewed_at / decision_note | 复核人、日期和证据说明 |",
        "",
        "## 决策清单",
        "",
        "| group_id | classes | records | paths | decision_status | action | chosen_class | note |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for decision in table["decisions"]:
        paths = "<br>".join(f"`{path}`" for path in decision.get("record_relative_paths", []))
        note = str(decision.get("decision_note", ""))
        lines.append(
            f"| {decision['group_id']} | {'、'.join(decision.get('classes', []))} | {decision['record_count']} | {paths} | {decision.get('decision_status', '')} | {decision.get('action', '')} | {decision.get('chosen_class', '')} | {note} |"
        )
    if table["validation_errors"]:
        lines.extend(["", "## 校验错误", ""])
        for error in table["validation_errors"]:
            lines.append(f"- {error}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a fillable decision table for cross-class exact duplicate conflicts.")
    parser.add_argument("--review-package", default="reports/classification_cross_class_review_package.json")
    parser.add_argument("--existing-table", default="", help="Existing JSON decision table to preserve manual fields.")
    parser.add_argument("--output", default="reports/classification_cross_class_decision_table.json")
    parser.add_argument("--csv", default="reports/classification_cross_class_decision_table.csv")
    parser.add_argument("--markdown", default="reports/classification_cross_class_decision_table.md")
    args = parser.parse_args()

    review_package = resolve_project_path(args.review_package)
    existing_table = resolve_project_path(args.existing_table) if args.existing_table else None
    output = resolve_project_path(args.output)
    csv_path = resolve_project_path(args.csv)
    markdown_path = resolve_project_path(args.markdown)
    table = build_table(review_package, existing_table)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(table, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(table, csv_path)
    write_markdown(table, markdown_path, csv_path)
    print(json.dumps(table["summary"], ensure_ascii=False, indent=2))
    return 0 if not table["validation_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
