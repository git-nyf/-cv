from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from path_utils import IMAGE_EXTS, resolve_project_path


READY_STATUS = "ready_for_cleanup_execution"
SUCCESS_STATUS = "cleanup_dataset_written"
VALID_SPLITS = {"train", "val", "test"}


def normalize_relative_path(value: str) -> str:
    return str(Path(str(value).strip().replace("\\", "/")))


def safe_relative_path(value: str) -> str:
    path = Path(str(value).strip().replace("\\", "/"))
    if path.is_absolute():
        raise ValueError(f"path must be relative: {value}")
    if not path.parts:
        raise ValueError("path must not be empty")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"path must not contain traversal segments: {value}")
    if path.parts[0] not in VALID_SPLITS:
        raise ValueError(f"path must start with train, val, or test: {value}")
    return str(path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_classification_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for split in ("train", "val", "test"):
        split_root = source / split
        if not split_root.exists():
            continue
        for path in split_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                files.append(path)
    return sorted(files, key=lambda item: normalize_relative_path(str(item.relative_to(source))))


def build_record(path: Path, root: Path) -> dict[str, Any]:
    relative = path.relative_to(root)
    return {
        "path": str(path),
        "relative_path": normalize_relative_path(str(relative)),
        "split": relative.parts[0] if len(relative.parts) >= 1 else "",
        "class_name": relative.parts[1] if len(relative.parts) >= 2 else "",
        "filename": path.name,
        "bytes": path.stat().st_size,
    }


def files_match(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    return left.read_bytes() == right.read_bytes()


def path_relation_blocked(source: Path, output: Path) -> bool:
    if source == output:
        return True
    return output.is_relative_to(source) or source.is_relative_to(output)


def validate_ready_plan(plan: dict[str, Any]) -> list[str]:
    summary = plan.get("summary", {})
    errors: list[str] = []
    if plan.get("schema_version") != 1:
        errors.append("cleanup plan schema_version must be 1")
    if summary.get("status") != READY_STATUS:
        errors.append(f"cleanup plan status must be {READY_STATUS}, got {summary.get('status')!r}")
    if int(summary.get("validation_errors", 0)) != 0:
        errors.append("cleanup plan summary validation_errors must be 0")
    if plan.get("validation_errors"):
        errors.append("cleanup plan validation_errors must be empty")
    if int(summary.get("planned_operations", len(plan.get("operations", [])))) != len(plan.get("operations", [])):
        errors.append("cleanup plan planned_operations does not match operations length")
    return errors


def build_operation_indexes(plan: dict[str, Any]) -> tuple[set[str], dict[str, str], list[str]]:
    remove_paths: set[str] = set()
    move_targets: dict[str, str] = {}
    errors: list[str] = []
    seen_sources: set[str] = set()

    for index, operation in enumerate(plan.get("operations", []), start=1):
        kind = operation.get("operation")
        try:
            if kind == "remove":
                source_path = safe_relative_path(str(operation.get("relative_path", "")))
                if source_path in seen_sources:
                    errors.append(f"operation {index}: duplicate source operation for {source_path}")
                seen_sources.add(source_path)
                remove_paths.add(source_path)
            elif kind == "move":
                source_path = safe_relative_path(str(operation.get("source_relative_path", "")))
                target_path = safe_relative_path(str(operation.get("target_relative_path", "")))
                if source_path in seen_sources:
                    errors.append(f"operation {index}: duplicate source operation for {source_path}")
                seen_sources.add(source_path)
                move_targets[source_path] = target_path
            else:
                errors.append(f"operation {index}: unsupported operation {kind!r}")
        except ValueError as exc:
            errors.append(f"operation {index}: {exc}")

    overlap = sorted(remove_paths & set(move_targets))
    if overlap:
        errors.append(f"paths cannot be both removed and moved: {overlap}")
    return remove_paths, move_targets, errors


def count_split_class(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for record in records:
        counts.setdefault(record["split"], Counter())[record["class_name"]] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def apply_cleanup_plan(source: Path, output: Path, plan_path: Path, overwrite: bool = False) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    plan_path = plan_path.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source dataset does not exist: {source}")
    if path_relation_blocked(source, output):
        raise ValueError("Output must be a separate directory outside the source dataset tree.")

    plan = load_json(plan_path)
    remove_paths, move_targets, operation_errors = build_operation_indexes(plan)
    validation_errors = validate_ready_plan(plan) + operation_errors
    if validation_errors:
        raise ValueError("Cleanup plan is not executable: " + "; ".join(validation_errors[:8]))

    source_files = iter_classification_files(source)
    source_by_relative = {normalize_relative_path(str(path.relative_to(source))): path for path in source_files}
    operation_sources = remove_paths | set(move_targets)
    missing_sources = sorted(path for path in operation_sources if path not in source_by_relative)
    if missing_sources:
        raise FileNotFoundError(f"Operation source files are missing from dataset: {missing_sources}")

    assignments: dict[str, list[tuple[Path, str, bool]]] = defaultdict(list)
    removed_records: list[dict[str, Any]] = []
    for source_file in source_files:
        source_relative = normalize_relative_path(str(source_file.relative_to(source)))
        if source_relative in remove_paths:
            removed_records.append(build_record(source_file, source))
            continue
        target_relative = move_targets.get(source_relative, source_relative)
        assignments[target_relative].append((source_file, source_relative, source_relative in move_targets))

    target_conflicts: list[dict[str, Any]] = []
    for target_relative, items in assignments.items():
        first = items[0][0]
        for other, other_relative, _ in items[1:]:
            if not files_match(first, other):
                target_conflicts.append(
                    {
                        "target_relative_path": target_relative,
                        "source_relative_path": other_relative,
                        "first_source": normalize_relative_path(str(first.relative_to(source))),
                    }
                )
    if target_conflicts:
        raise ValueError(f"Move target conflicts with different bytes: {target_conflicts[:5]}")

    if output.exists():
        if not overwrite:
            raise FileExistsError(f"Output already exists: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    copied_records: list[dict[str, Any]] = []
    moved_records: list[dict[str, Any]] = []
    merged_records: list[dict[str, Any]] = []
    for target_relative, items in sorted(assignments.items()):
        source_file, source_relative, is_move = items[0]
        target_file = output / Path(target_relative)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        target_record = build_record(target_file, output)
        if is_move:
            moved_records.append(
                {
                    "source": build_record(source_file, source),
                    "target": target_record,
                }
            )
        else:
            copied_records.append(target_record)

        for merged_file, merged_relative, merged_is_move in items[1:]:
            merged_records.append(
                {
                    "source": build_record(merged_file, source),
                    "target_relative_path": target_relative,
                    "operation": "move" if merged_is_move else "dedupe_target_collision",
                    "source_relative_path": merged_relative,
                }
            )

    output_files = iter_classification_files(output)
    output_records = [build_record(path, output) for path in output_files]
    plan_summary = plan.get("summary", {})
    operation_counts = Counter(operation.get("operation") for operation in plan.get("operations", []))
    source_split_totals = Counter(build_record(path, source)["split"] for path in source_files)
    output_split_totals = Counter(record["split"] for record in output_records)

    return {
        "schema_version": 1,
        "source": str(source),
        "output": str(output),
        "cleanup_plan": str(plan_path),
        "summary": {
            "status": SUCCESS_STATUS,
            "plan_status": plan_summary.get("status"),
            "source_images": len(source_files),
            "output_images": len(output_records),
            "requested_operations": len(plan.get("operations", [])),
            "requested_remove_operations": int(operation_counts.get("remove", 0)),
            "requested_move_operations": int(operation_counts.get("move", 0)),
            "removed_images": len(removed_records),
            "moved_images": len(moved_records),
            "merged_move_targets": sum(1 for record in merged_records if record.get("operation") == "move"),
            "unchanged_copied_images": len(copied_records),
            "missing_operation_sources": 0,
            "target_conflicts": 0,
            "source_split_counts": dict(sorted(source_split_totals.items())),
            "output_split_counts": dict(sorted(output_split_totals.items())),
        },
        "split_distribution": count_split_class(output_records),
        "removed_records": removed_records,
        "moved_records": moved_records,
        "merged_records": merged_records,
        "boundary_note": (
            "本脚本只把清理计划应用到新的输出目录；不会删除、移动、重命名或覆盖源数据集中的任何图片。"
        ),
        "recommended_next_steps": [
            "对输出数据集重新运行 classification inspection 和 duplicate audit。",
            "基于输出数据集重新训练与独立验证，报告新指标时标明清理计划和执行报告路径。",
        ],
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 分类跨类别标签冲突清理执行报告",
        "",
        f"- 源数据集: `{report['source']}`",
        f"- 输出数据集: `{report['output']}`",
        f"- 清理计划: `{report['cleanup_plan']}`",
        f"- 状态: `{summary['status']}`",
        f"- 源图片: {summary['source_images']}",
        f"- 输出图片: {summary['output_images']}",
        f"- 请求操作: {summary['requested_operations']}，remove {summary['requested_remove_operations']}，move {summary['requested_move_operations']}",
        f"- 实际移除: {summary['removed_images']}",
        f"- 实际移动复制: {summary['moved_images']}",
        f"- exact duplicate 移动合并: {summary['merged_move_targets']}",
        "",
        "## 边界说明",
        "",
        report["boundary_note"],
        "",
        "## 建议后续动作",
        "",
    ]
    for item in report["recommended_next_steps"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 移除记录", "", "| split | class | relative_path | bytes |", "|---|---|---|---:|"])
    for record in report["removed_records"]:
        lines.append(f"| {record['split']} | {record['class_name']} | `{record['relative_path']}` | {record['bytes']} |")
    if not report["removed_records"]:
        lines.append("| - | - | - | 0 |")
    lines.extend(["", "## 移动记录", "", "| source | target | bytes |", "|---|---|---:|"])
    for record in report["moved_records"]:
        source = record["source"]
        target = record["target"]
        lines.append(f"| `{source['relative_path']}` | `{target['relative_path']}` | {source['bytes']} |")
    for record in report["merged_records"]:
        source = record["source"]
        lines.append(f"| `{source['relative_path']}` | `{record['target_relative_path']}` | {source['bytes']} |")
    if not report["moved_records"] and not report["merged_records"]:
        lines.append("| - | - | 0 |")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a validated cross-class cleanup plan into a new dataset directory.")
    parser.add_argument("--source", default="data/classification_strict_jpeg_leakage_clean_candidate")
    parser.add_argument("--cleanup-plan", default="reports/classification_cross_class_cleanup_plan.json")
    parser.add_argument("--output", default="data/classification_strict_jpeg_cross_class_clean_candidate")
    parser.add_argument("--report", default="reports/classification_cross_class_cleanup_execution_report.json")
    parser.add_argument("--markdown", default="reports/classification_cross_class_cleanup_execution_report.md")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        report = apply_cleanup_plan(
            source=resolve_project_path(args.source),
            output=resolve_project_path(args.output),
            plan_path=resolve_project_path(args.cleanup_plan),
            overwrite=args.overwrite,
        )
    except Exception as exc:
        print(json.dumps({"status": "cleanup_execution_blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    report_path = resolve_project_path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, resolve_project_path(args.markdown))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
