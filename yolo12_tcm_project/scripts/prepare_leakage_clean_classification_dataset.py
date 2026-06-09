from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from path_utils import IMAGE_EXTS, resolve_project_path


def normalize_relative_path(value: str) -> str:
    return str(Path(value.replace("\\", "/")))


def load_review_package(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def val_leak_relative_paths(review_package: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for group in review_package.get("groups", []):
        for record in group.get("records", []):
            if record.get("split") == "val":
                paths.add(normalize_relative_path(str(record.get("relative_path", ""))))
    return paths


def iter_classification_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for split in ("train", "val", "test"):
        split_root = source / split
        if not split_root.exists():
            continue
        for path in split_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                files.append(path)
    return sorted(files, key=lambda item: str(item.relative_to(source)))


def count_split_class(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for record in records:
        counts.setdefault(record["split"], Counter())[record["class_name"]] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def build_record(path: Path, root: Path) -> dict[str, Any]:
    relative = path.relative_to(root)
    split = relative.parts[0] if len(relative.parts) >= 1 else ""
    class_name = relative.parts[1] if len(relative.parts) >= 2 else ""
    return {
        "path": str(path),
        "relative_path": str(relative),
        "split": split,
        "class_name": class_name,
        "filename": path.name,
        "bytes": path.stat().st_size,
    }


def prepare_dataset(source: Path, output: Path, review_package: Path, overwrite: bool = False) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    review_package = review_package.resolve()
    package = load_review_package(review_package)
    remove_relative_paths = val_leak_relative_paths(package)

    if output.exists():
        if not overwrite:
            raise FileExistsError(f"Output already exists: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    source_files = iter_classification_files(source)
    copied_records: list[dict[str, Any]] = []
    removed_records: list[dict[str, Any]] = []
    for source_file in source_files:
        relative = source_file.relative_to(source)
        normalized = normalize_relative_path(str(relative))
        source_record = build_record(source_file, source)
        if normalized in remove_relative_paths:
            removed_records.append(source_record)
            continue
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
        copied_records.append(build_record(target, output))

    missing_requested_removals = sorted(
        path for path in remove_relative_paths if not (source / Path(path)).exists()
    )
    output_classes = sorted({record["class_name"] for record in copied_records})
    source_records = [build_record(path, source) for path in source_files]
    split_totals = Counter(record["split"] for record in copied_records)
    source_split_totals = Counter(record["split"] for record in source_records)
    removed_split_totals = Counter(record["split"] for record in removed_records)

    expected_groups = int(package.get("summary", {}).get("leakage_groups", len(remove_relative_paths)))
    status = "leakage_val_duplicates_removed" if len(removed_records) == len(remove_relative_paths) else "incomplete_removal"
    return {
        "source": str(source),
        "output": str(output),
        "review_package": str(review_package),
        "summary": {
            "status": status,
            "strategy": "copy_all_except_val_exact_duplicates_from_review_package",
            "source_images": len(source_records),
            "output_images": len(copied_records),
            "removed_images": len(removed_records),
            "requested_val_removals": len(remove_relative_paths),
            "missing_requested_removals": len(missing_requested_removals),
            "leakage_groups_from_review": expected_groups,
            "classes": len(output_classes),
            "source_split_counts": dict(sorted(source_split_totals.items())),
            "output_split_counts": dict(sorted(split_totals.items())),
            "removed_split_counts": dict(sorted(removed_split_totals.items())),
        },
        "split_distribution": count_split_class(copied_records),
        "removed_records": removed_records,
        "missing_requested_removals": missing_requested_removals,
        "boundary_note": (
            "本候选数据集只移除人工复核包中列出的 val 侧字节级 train/val 重复副本；"
            "不自动修改 train 图像、不自动裁决跨类别标签，也不替代人工类别复核。"
        ),
        "recommended_next_steps": [
            "对输出数据集重新运行 exact duplicate 审计，确认 train/val 泄漏组归零。",
            "基于该候选数据集重新训练与独立验证，指标不得与旧泄漏数据集直接等价比较。",
            "跨类别 exact duplicate 仍需结合 contact sheet 和原始图像人工确认真实类别。",
        ],
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 分类数据 train/val 泄漏候选清理报告",
        "",
        f"- 源数据集: `{report['source']}`",
        f"- 输出数据集: `{report['output']}`",
        f"- 复核包: `{report['review_package']}`",
        f"- 状态: `{summary['status']}`",
        f"- 策略: `{summary['strategy']}`",
        f"- 源图片: {summary['source_images']}",
        f"- 输出图片: {summary['output_images']}",
        f"- 移除图片: {summary['removed_images']} / 请求移除 {summary['requested_val_removals']}",
        f"- 类别数: {summary['classes']}",
        f"- 源划分: {summary['source_split_counts']}",
        f"- 输出划分: {summary['output_split_counts']}",
        f"- 移除划分: {summary['removed_split_counts']}",
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
    lines.extend(["", "## 已移除 val 副本", "", "| split | class | filename | relative_path | bytes |", "|---|---|---|---|---:|"])
    for record in report["removed_records"]:
        lines.append(
            f"| {record['split']} | {record['class_name']} | {record['filename']} | `{record['relative_path']}` | {record['bytes']} |"
        )
    if not report["removed_records"]:
        lines.append("| - | - | - | - | 0 |")
    if report["missing_requested_removals"]:
        lines.extend(["", "## 未找到的请求移除路径", ""])
        for path in report["missing_requested_removals"]:
            lines.append(f"- `{path}`")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a classification dataset candidate with reviewed val-side train/val exact duplicates removed.")
    parser.add_argument("--source", required=True, help="Classification dataset root.")
    parser.add_argument("--review-package", default="reports/classification_leakage_review_package.json")
    parser.add_argument("--output", required=True, help="Output dataset root.")
    parser.add_argument("--report", required=True, help="JSON report path.")
    parser.add_argument("--markdown", required=True, help="Markdown report path.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    report = prepare_dataset(
        source=resolve_project_path(args.source),
        output=resolve_project_path(args.output),
        review_package=resolve_project_path(args.review_package),
        overwrite=args.overwrite,
    )
    output = resolve_project_path(args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, resolve_project_path(args.markdown))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0 if report["summary"]["status"] == "leakage_val_duplicates_removed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
