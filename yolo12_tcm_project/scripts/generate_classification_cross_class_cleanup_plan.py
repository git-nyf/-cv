from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from generate_classification_cross_class_decision_table import (
    ALLOWED_ACTIONS,
    ALLOWED_DECISION_STATUS,
    MANUAL_FIELDS,
    normalize_path,
    validate_decision,
)
from path_utils import resolve_project_path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_semicolon(value: str) -> list[str]:
    return [normalize_path(item.strip()) for item in value.split(";") if item.strip()]


def load_csv_manual_fields(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    overrides: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            group_id = str(row.get("group_id", "")).strip()
            if not group_id:
                continue
            item: dict[str, Any] = {}
            for key in MANUAL_FIELDS:
                value = str(row.get(key, "")).strip()
                if key == "remove_relative_paths":
                    item[key] = split_semicolon(value)
                else:
                    item[key] = value
            overrides[group_id] = item
    return overrides


def merge_csv_overrides(decisions: list[dict[str, Any]], overrides: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for decision in decisions:
        item = dict(decision)
        override = overrides.get(str(item.get("group_id")))
        if override:
            for key in MANUAL_FIELDS:
                item[key] = override.get(key, item.get(key, [] if key == "remove_relative_paths" else ""))
        if isinstance(item.get("remove_relative_paths"), str):
            item["remove_relative_paths"] = split_semicolon(item["remove_relative_paths"])
        else:
            item["remove_relative_paths"] = [
                normalize_path(str(path)) for path in item.get("remove_relative_paths", [])
            ]
        merged.append(item)
    return merged


def record_by_path(decision: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        normalize_path(str(record.get("relative_path", ""))): record
        for record in decision.get("record_summary", [])
    }


def require_decided_metadata(decision: dict[str, Any]) -> list[str]:
    group_id = decision.get("group_id", "<missing>")
    errors: list[str] = []
    if decision.get("decision_status") != "decided":
        return errors
    if not str(decision.get("reviewer", "")).strip():
        errors.append(f"{group_id}: decided rows must set reviewer")
    if not str(decision.get("reviewed_at", "")).strip():
        errors.append(f"{group_id}: decided rows must set reviewed_at")
    if not str(decision.get("decision_note", "")).strip():
        errors.append(f"{group_id}: decided rows must set decision_note")
    return errors


def validate_action_semantics(decision: dict[str, Any]) -> list[str]:
    group_id = decision.get("group_id", "<missing>")
    status = decision.get("decision_status")
    action = decision.get("action", "")
    chosen_class = decision.get("chosen_class", "")
    remove_paths = {normalize_path(str(path)) for path in decision.get("remove_relative_paths", [])}
    records = record_by_path(decision)
    classes = set(decision.get("classes", []))
    errors: list[str] = []

    if status != "decided":
        if action:
            errors.append(f"{group_id}: non-decided rows must not set action")
        return errors

    if action == "keep_chosen_class_remove_others":
        if chosen_class not in classes:
            errors.append(f"{group_id}: chosen_class must be one of classes")
        non_chosen = {
            path for path, record in records.items() if record.get("class_name") != chosen_class
        }
        chosen_paths = {
            path for path, record in records.items() if record.get("class_name") == chosen_class
        }
        if not remove_paths:
            errors.append(f"{group_id}: keep_chosen_class_remove_others must set remove_relative_paths")
        missing_non_chosen = sorted(non_chosen - remove_paths)
        if missing_non_chosen:
            errors.append(f"{group_id}: remove_relative_paths must include all non-chosen records: {missing_non_chosen}")
        chosen_removed = sorted(chosen_paths & remove_paths)
        if chosen_removed:
            errors.append(f"{group_id}: remove_relative_paths must not remove chosen_class records: {chosen_removed}")
    elif action == "move_all_to_chosen_class":
        move_to_class = decision.get("move_to_class") or chosen_class
        if move_to_class not in classes:
            errors.append(f"{group_id}: move_all_to_chosen_class requires chosen_class or move_to_class in classes")
        if remove_paths:
            errors.append(f"{group_id}: move_all_to_chosen_class must not set remove_relative_paths")
    elif action == "keep_all_as_is":
        if remove_paths:
            errors.append(f"{group_id}: keep_all_as_is must not set remove_relative_paths")
    elif action == "remove_all_uncertain":
        if chosen_class:
            errors.append(f"{group_id}: remove_all_uncertain should leave chosen_class empty")
        if remove_paths:
            errors.append(f"{group_id}: remove_all_uncertain removes all records; leave remove_relative_paths empty")
    elif action == "needs_expert_review":
        if remove_paths:
            errors.append(f"{group_id}: needs_expert_review must not set remove_relative_paths")

    return errors


def target_for_move(path: str, target_class: str) -> str:
    parts = Path(path).parts
    if len(parts) < 3:
        return path
    split = parts[0]
    filename = parts[-1]
    return str(Path(split) / target_class / filename)


def operations_for_decision(decision: dict[str, Any]) -> list[dict[str, Any]]:
    if decision.get("decision_status") != "decided":
        return []
    action = decision.get("action", "")
    records = record_by_path(decision)
    operations: list[dict[str, Any]] = []
    if action == "keep_chosen_class_remove_others":
        for path in decision.get("remove_relative_paths", []):
            record = records.get(normalize_path(str(path)), {})
            operations.append(
                {
                    "operation": "remove",
                    "group_id": decision.get("group_id"),
                    "relative_path": normalize_path(str(path)),
                    "class_name": record.get("class_name", ""),
                    "reason": "cross_class_exact_duplicate_not_chosen",
                }
            )
    elif action == "move_all_to_chosen_class":
        target_class = decision.get("move_to_class") or decision.get("chosen_class", "")
        for path, record in records.items():
            if record.get("class_name") == target_class:
                continue
            operations.append(
                {
                    "operation": "move",
                    "group_id": decision.get("group_id"),
                    "source_relative_path": path,
                    "target_relative_path": target_for_move(path, target_class),
                    "source_class": record.get("class_name", ""),
                    "target_class": target_class,
                    "reason": "cross_class_exact_duplicate_relabel",
                }
            )
    elif action == "remove_all_uncertain":
        for path, record in records.items():
            operations.append(
                {
                    "operation": "remove",
                    "group_id": decision.get("group_id"),
                    "relative_path": path,
                    "class_name": record.get("class_name", ""),
                    "reason": "uncertain_cross_class_exact_duplicate",
                }
            )
    return operations


def build_cleanup_plan(decision_table: Path, decision_csv: Path | None = None) -> dict[str, Any]:
    payload = read_json(decision_table)
    decisions = payload.get("decisions", [])
    decisions = merge_csv_overrides(decisions, load_csv_manual_fields(decision_csv))

    validation_errors: list[str] = []
    operations: list[dict[str, Any]] = []
    no_op_groups: list[str] = []
    for decision in decisions:
        validation_errors.extend(validate_decision(decision))
        validation_errors.extend(require_decided_metadata(decision))
        validation_errors.extend(validate_action_semantics(decision))
        operations.extend(operations_for_decision(decision))
        if decision.get("decision_status") == "decided" and decision.get("action") == "keep_all_as_is":
            no_op_groups.append(str(decision.get("group_id")))

    status_counts = Counter(decision.get("decision_status", "pending") for decision in decisions)
    action_counts = Counter(decision.get("action") or "unset" for decision in decisions)
    operation_counts = Counter(operation.get("operation") for operation in operations)

    if validation_errors:
        status = "invalid_cleanup_plan"
    elif status_counts.get("decided", 0) == 0:
        status = "waiting_for_manual_decisions"
    elif status_counts.get("pending", 0) or status_counts.get("needs_expert_review", 0) or status_counts.get("defer", 0):
        status = "partial_cleanup_plan"
    else:
        status = "ready_for_cleanup_execution"

    return {
        "schema_version": 1,
        "source_decision_table": str(decision_table),
        "source_decision_csv": str(decision_csv) if decision_csv else "",
        "summary": {
            "status": status,
            "groups": len(decisions),
            "records": sum(int(decision.get("record_count", 0)) for decision in decisions),
            "pending_decisions": int(status_counts.get("pending", 0)),
            "decided_groups": int(status_counts.get("decided", 0)),
            "needs_expert_review_groups": int(status_counts.get("needs_expert_review", 0)),
            "deferred_groups": int(status_counts.get("defer", 0)),
            "validation_errors": len(validation_errors),
            "planned_operations": len(operations),
            "planned_remove_operations": int(operation_counts.get("remove", 0)),
            "planned_move_operations": int(operation_counts.get("move", 0)),
            "keep_all_as_is_groups": len(no_op_groups),
        },
        "action_counts": dict(sorted(action_counts.items())),
        "operations": operations,
        "no_op_groups": no_op_groups,
        "validation_errors": validation_errors,
        "boundary_note": (
            "本报告只把人工决策转换为可审计清理计划；不会删除、移动、重命名、重标或复制任何图片。"
        ),
        "recommended_next_steps": [
            "人工填写所有 pending 决策后重新生成本清理计划。",
            "仅当 status 为 ready_for_cleanup_execution 且 validation_errors 为 0 时，才可进入真实数据清理执行脚本。",
            "执行清理后必须重新运行 classification inspection、duplicate audit、训练和独立评估。",
        ],
    }


def write_operations_csv(plan: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "operation",
        "group_id",
        "relative_path",
        "source_relative_path",
        "target_relative_path",
        "class_name",
        "source_class",
        "target_class",
        "reason",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for operation in plan.get("operations", []):
            writer.writerow({key: operation.get(key, "") for key in fieldnames})


def write_markdown(plan: dict[str, Any], output: Path, operations_csv: Path) -> None:
    summary = plan["summary"]
    lines = [
        "# 分类跨类别标签冲突清理计划校验报告",
        "",
        f"- 决策表: `{plan['source_decision_table']}`",
        f"- 决策 CSV: `{plan['source_decision_csv'] or '未提供'}`",
        f"- 状态: `{summary['status']}`",
        f"- 待决策组: {summary['pending_decisions']} / {summary['groups']}",
        f"- 已决策组: {summary['decided_groups']}",
        f"- 需专家复核组: {summary['needs_expert_review_groups']}",
        f"- 延后处理组: {summary['deferred_groups']}",
        f"- 校验错误: {summary['validation_errors']}",
        f"- 计划操作: {summary['planned_operations']}，remove {summary['planned_remove_operations']}，move {summary['planned_move_operations']}",
        f"- 操作 CSV: `{operations_csv}`",
        "",
        "## 边界说明",
        "",
        plan["boundary_note"],
        "",
        "## 建议后续动作",
        "",
    ]
    for item in plan["recommended_next_steps"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 操作预览", "", "| operation | group_id | source | target | reason |", "|---|---|---|---|---|"])
    if plan["operations"]:
        for operation in plan["operations"]:
            source = operation.get("relative_path") or operation.get("source_relative_path", "")
            target = operation.get("target_relative_path", "")
            lines.append(
                f"| {operation.get('operation', '')} | {operation.get('group_id', '')} | `{source}` | `{target}` | {operation.get('reason', '')} |"
            )
    else:
        lines.append("| - | - | - | - | 当前没有可执行操作 |")
    if plan["validation_errors"]:
        lines.extend(["", "## 校验错误", ""])
        for error in plan["validation_errors"]:
            lines.append(f"- {error}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a dry-run cleanup plan from cross-class decision table data.")
    parser.add_argument("--decision-table", default="reports/classification_cross_class_decision_table.json")
    parser.add_argument("--decision-csv", default="", help="Optional manually edited CSV that overrides JSON manual fields.")
    parser.add_argument("--output", default="reports/classification_cross_class_cleanup_plan.json")
    parser.add_argument("--operations-csv", default="reports/classification_cross_class_cleanup_plan.csv")
    parser.add_argument("--markdown", default="reports/classification_cross_class_cleanup_plan.md")
    args = parser.parse_args()

    decision_table = resolve_project_path(args.decision_table)
    decision_csv = resolve_project_path(args.decision_csv) if args.decision_csv else None
    output = resolve_project_path(args.output)
    operations_csv = resolve_project_path(args.operations_csv)
    markdown = resolve_project_path(args.markdown)

    plan = build_cleanup_plan(decision_table, decision_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    write_operations_csv(plan, operations_csv)
    write_markdown(plan, markdown, operations_csv)
    print(json.dumps(plan["summary"], ensure_ascii=False, indent=2))
    return 0 if not plan["validation_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
