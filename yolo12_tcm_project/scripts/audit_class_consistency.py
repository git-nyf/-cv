from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from path_utils import IMAGE_EXTS, project_root, resolve_project_path


def default_source() -> Path:
    return project_root().parent / "data"


def class_dirs(root: Path, split: str) -> dict[str, Path]:
    split_root = root / split
    if not split_root.exists():
        return {}
    return {p.name: p for p in sorted(split_root.iterdir(), key=lambda item: item.name) if p.is_dir()}


def count_images(class_dir: Path) -> int:
    return sum(1 for p in class_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def split_distribution(source: Path, split: str) -> dict[str, int]:
    return {name: count_images(path) for name, path in class_dirs(source, split).items()}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def skipped_by_class(strict_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in strict_report.get("skipped", []):
        class_name = item.get("class_name", "")
        reason = item.get("reason", "unknown")
        bucket = grouped.setdefault(class_name, {"total": 0, "reasons": Counter(), "samples": []})
        bucket["total"] += 1
        bucket["reasons"][reason] += 1
        if len(bucket["samples"]) < 5:
            bucket["samples"].append(item.get("source", ""))
    return {
        name: {
            "total": value["total"],
            "reasons": dict(sorted(value["reasons"].items())),
            "samples": value["samples"],
        }
        for name, value in sorted(grouped.items())
    }


def build_report(source: Path, strict_report_path: Path, strict_inspection_path: Path | None) -> dict[str, Any]:
    source = source.resolve()
    strict_report = load_json(strict_report_path)
    strict_inspection = load_json(strict_inspection_path) if strict_inspection_path and strict_inspection_path.exists() else {}

    raw_train = split_distribution(source, "train")
    raw_val = split_distribution(source, "val")
    raw_train_classes = set(raw_train)
    raw_val_classes = set(raw_val)
    raw_classes = raw_train_classes | raw_val_classes

    strict_classes = set(strict_report.get("classes", []))
    strict_distribution = strict_report.get("distribution", {})
    strict_train = strict_distribution.get("train", {})
    strict_val = strict_distribution.get("val", {})
    strict_summary = strict_report.get("summary", {})
    inspection_summary = strict_inspection.get("summary", {})

    missing_from_strict = sorted(raw_classes - strict_classes)
    extra_in_strict = sorted(strict_classes - raw_classes)
    train_only = sorted(raw_train_classes - raw_val_classes)
    val_only = sorted(raw_val_classes - raw_train_classes)
    zero_train = sorted(name for name in raw_classes if raw_train.get(name, 0) == 0)
    zero_val = sorted(name for name in raw_classes if raw_val.get(name, 0) == 0)

    skipped_grouped = skipped_by_class(strict_report)
    per_class: list[dict[str, Any]] = []
    for class_name in sorted(raw_classes):
        raw_train_count = raw_train.get(class_name, 0)
        raw_val_count = raw_val.get(class_name, 0)
        strict_train_count = strict_train.get(class_name, 0)
        strict_val_count = strict_val.get(class_name, 0)
        skipped = skipped_grouped.get(class_name, {"total": 0, "reasons": {}, "samples": []})
        per_class.append(
            {
                "class_name": class_name,
                "raw_train": raw_train_count,
                "raw_val": raw_val_count,
                "strict_train": strict_train_count,
                "strict_val": strict_val_count,
                "included_in_strict": class_name in strict_classes,
                "skipped_images": skipped["total"],
                "skip_reasons": skipped["reasons"],
            }
        )

    status = "needs_class_completion" if missing_from_strict or extra_in_strict or zero_train else "consistent"
    recommended_actions: list[str] = []
    if zero_train:
        recommended_actions.append(f"为 {', '.join(zero_train)} 补充训练样本后重建 strict 数据集，恢复完整 {len(raw_classes)} 类实验。")
    if skipped_grouped:
        recommended_actions.append("保留 strict JPEG 清洗策略：跳过 GIF 伪 JPG 和损坏图，统一可读 PNG/JPEG 为 JPEG。")
    recommended_actions.append("若课程要求检测指标，补充真实 YOLO bbox 标注；当前类别审计只证明分类数据一致性。")

    report = {
        "source": str(source),
        "strict_report": str(strict_report_path.resolve()),
        "strict_inspection": str(strict_inspection_path.resolve()) if strict_inspection_path and strict_inspection_path.exists() else None,
        "summary": {
            "status": status,
            "raw_classes": len(raw_classes),
            "raw_train_classes": len(raw_train_classes),
            "raw_val_classes": len(raw_val_classes),
            "strict_classes": len(strict_classes),
            "classes_missing_from_strict": missing_from_strict,
            "extra_classes_in_strict": extra_in_strict,
            "train_only_classes": train_only,
            "val_only_classes": val_only,
            "zero_train_classes": zero_train,
            "zero_val_classes": zero_val,
            "raw_train_images": sum(raw_train.values()),
            "raw_val_images": sum(raw_val.values()),
            "raw_total_images": sum(raw_train.values()) + sum(raw_val.values()),
            "strict_train_images": strict_summary.get("train_images"),
            "strict_val_images": strict_summary.get("val_images"),
            "strict_total_images": strict_summary.get("total_images"),
            "strict_verified_images": inspection_summary.get("verified_images"),
            "strict_errors": inspection_summary.get("errors"),
            "strict_warnings": inspection_summary.get("warnings"),
            "skipped_images": strict_summary.get("skipped_images"),
            "converted_to_jpeg": strict_summary.get("actions", {}).get("convert_to_jpeg", 0),
            "copied_jpeg": strict_summary.get("actions", {}).get("copy_jpeg", 0),
        },
        "raw_distribution": {
            "train": dict(sorted(raw_train.items())),
            "val": dict(sorted(raw_val.items())),
        },
        "strict_distribution": {
            "train": dict(sorted(strict_train.items())),
            "val": dict(sorted(strict_val.items())),
        },
        "skipped_by_class": skipped_grouped,
        "per_class": per_class,
        "recommended_actions": recommended_actions,
    }
    return report


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 类别一致性审计报告",
        "",
        f"- 原始数据: `{report['source']}`",
        f"- strict 清洗报告: `{report['strict_report']}`",
        f"- strict 复审报告: `{report.get('strict_inspection') or '未提供'}`",
        "",
        "## 总览",
        "",
        f"- 状态: `{summary['status']}`",
        f"- 原始类别: {summary['raw_classes']}；train 类别: {summary['raw_train_classes']}；val 类别: {summary['raw_val_classes']}",
        f"- strict 类别: {summary['strict_classes']}",
        f"- 原始图片: train {summary['raw_train_images']} / val {summary['raw_val_images']} / total {summary['raw_total_images']}",
        f"- strict 图片: train {summary['strict_train_images']} / val {summary['strict_val_images']} / total {summary['strict_total_images']}",
        f"- strict 可读复审: verified {summary['strict_verified_images']}，errors {summary['strict_errors']}，warnings {summary['strict_warnings']}",
        f"- 跳过图片: {summary['skipped_images']}；转换 JPEG: {summary['converted_to_jpeg']}；直接 JPEG: {summary['copied_jpeg']}",
        "",
        "## 类别差异",
        "",
    ]
    for key, label in [
        ("classes_missing_from_strict", "未纳入 strict 的原始类别"),
        ("extra_classes_in_strict", "strict 额外类别"),
        ("train_only_classes", "只在 train 出现"),
        ("val_only_classes", "只在 val 出现"),
        ("zero_train_classes", "训练样本为 0 的类别"),
        ("zero_val_classes", "验证样本为 0 的类别"),
    ]:
        values = summary[key]
        lines.append(f"- {label}: {', '.join(values) if values else '无'}")

    lines.extend(["", "## 跳过图片分布", ""])
    if report["skipped_by_class"]:
        lines.append("| 类别 | 跳过数 | 原因 |")
        lines.append("|---|---:|---|")
        for class_name, item in report["skipped_by_class"].items():
            reasons = "; ".join(f"{reason}: {count}" for reason, count in item["reasons"].items())
            lines.append(f"| {class_name} | {item['total']} | {reasons} |")
    else:
        lines.append("- 无")

    lines.extend(["", "## 关键类别明细", "", "| 类别 | raw train | raw val | strict train | strict val | 纳入 strict | 跳过图 |"])
    lines.append("|---|---:|---:|---:|---:|---|---:|")
    key_rows = [
        row
        for row in report["per_class"]
        if (not row["included_in_strict"]) or row["skipped_images"] or row["raw_train"] == 0 or row["raw_val"] == 0
    ]
    for row in key_rows:
        lines.append(
            f"| {row['class_name']} | {row['raw_train']} | {row['raw_val']} | {row['strict_train']} | "
            f"{row['strict_val']} | {'是' if row['included_in_strict'] else '否'} | {row['skipped_images']} |"
        )

    lines.extend(["", "## 建议处理", ""])
    for item in report["recommended_actions"]:
        lines.append(f"- {item}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit class consistency between raw classification data and strict JPEG dataset.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--strict-report", default="data/classification_strict_jpeg/strict_classification_report.json")
    parser.add_argument("--strict-inspection", default="reports/strict_classification_dataset_inspection.json")
    parser.add_argument("--output", default="reports/class_consistency_audit.json")
    parser.add_argument("--markdown", default="reports/class_consistency_audit.md")
    args = parser.parse_args()

    report = build_report(
        source=Path(args.source),
        strict_report_path=resolve_project_path(args.strict_report),
        strict_inspection_path=resolve_project_path(args.strict_inspection),
    )
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown = resolve_project_path(args.markdown)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, markdown)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
