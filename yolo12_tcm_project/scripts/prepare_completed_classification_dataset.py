from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from path_utils import IMAGE_EXTS, project_root, resolve_project_path


SUPPORTED_FORMATS = {"jpeg", "mpo", "png", "bmp", "webp", "tiff"}


@dataclass
class ProcessedImage:
    split: str
    class_name: str
    source: str
    target: str
    action: str
    source_format: str
    strategy: str


@dataclass
class SkippedImage:
    split: str
    class_name: str
    source: str
    reason: str
    strategy: str


def default_source() -> Path:
    return project_root().parent / "data"


def class_dirs(root: Path, split: str) -> dict[str, Path]:
    split_root = root / split
    if not split_root.exists():
        return {}
    return {p.name: p for p in sorted(split_root.iterdir(), key=lambda item: item.name) if p.is_dir()}


def image_files(root: Path | None) -> list[Path]:
    if root is None or not root.exists():
        return []
    return sorted(
        [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda item: str(item),
    )


def unique_target(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 1
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def load_rgb(source: Path) -> tuple[Image.Image, str]:
    with Image.open(source) as image:
        fmt = (image.format or "").lower()
        image = ImageOps.exif_transpose(image)
        image.load()
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(f"unsupported content format: {fmt or 'unknown'}")
        if image.mode != "RGB":
            image = image.convert("RGB")
        else:
            image = image.copy()
    return image, fmt


def split_single_side_images(
    images: list[Path],
    val_ratio: float,
    min_train: int,
    min_val: int,
) -> tuple[list[Path], list[Path]]:
    if len(images) < min_train + min_val:
        raise ValueError(
            f"not enough images for completed split: images={len(images)}, "
            f"min_train={min_train}, min_val={min_val}"
        )
    val_count = max(min_val, round(len(images) * val_ratio))
    val_count = min(val_count, len(images) - min_train)
    if val_count < min_val:
        raise ValueError(
            f"unable to reserve validation images: images={len(images)}, "
            f"val_count={val_count}, min_val={min_val}"
        )
    train_count = len(images) - val_count
    return images[:train_count], images[train_count:]


def build_assignments(
    class_name: str,
    train_images: list[Path],
    val_images: list[Path],
    val_ratio: float,
    min_train: int,
    min_val: int,
) -> tuple[list[tuple[str, Path, str]], dict[str, Any]]:
    if train_images and val_images:
        return (
            [("train", path, "preserve_raw_split") for path in train_images]
            + [("val", path, "preserve_raw_split") for path in val_images],
            {
                "class_name": class_name,
                "strategy": "preserve_raw_split",
                "raw_train": len(train_images),
                "raw_val": len(val_images),
                "assigned_train": len(train_images),
                "assigned_val": len(val_images),
            },
        )

    combined = sorted(train_images + val_images, key=lambda item: str(item))
    train_assigned, val_assigned = split_single_side_images(combined, val_ratio, min_train, min_val)
    source_side = "train_only" if train_images else "val_only"
    strategy = f"rebalance_{source_side}"
    return (
        [("train", path, strategy) for path in train_assigned] + [("val", path, strategy) for path in val_assigned],
        {
            "class_name": class_name,
            "strategy": strategy,
            "raw_train": len(train_images),
            "raw_val": len(val_images),
            "assigned_train": len(train_assigned),
            "assigned_val": len(val_assigned),
        },
    )


def prepare(
    source: Path,
    output: Path,
    overwrite: bool,
    quality: int,
    val_ratio: float,
    min_train: int,
    min_val: int,
) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    if not source.exists():
        raise FileNotFoundError(f"source dataset not found: {source}")
    if output.exists() and overwrite:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    train_dirs = class_dirs(source, "train")
    val_dirs = class_dirs(source, "val")
    all_classes = sorted(set(train_dirs) | set(val_dirs))

    processed: list[ProcessedImage] = []
    skipped: list[SkippedImage] = []
    distribution: dict[str, Counter[str]] = {"train": Counter(), "val": Counter()}
    action_counts: Counter[str] = Counter()
    strategy_counts: Counter[str] = Counter()
    source_formats: Counter[str] = Counter()
    class_strategies: list[dict[str, Any]] = []
    excluded_classes: list[dict[str, Any]] = []

    for class_name in all_classes:
        train_images = image_files(train_dirs.get(class_name))
        val_images = image_files(val_dirs.get(class_name))
        try:
            assignments, strategy_info = build_assignments(class_name, train_images, val_images, val_ratio, min_train, min_val)
        except Exception as exc:
            excluded_classes.append(
                {
                    "class_name": class_name,
                    "raw_train": len(train_images),
                    "raw_val": len(val_images),
                    "reason": str(exc),
                }
            )
            continue

        class_strategies.append(strategy_info)
        strategy_counts[strategy_info["strategy"]] += 1

        for split, source_image, strategy in assignments:
            target_dir = output / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            try:
                image, source_format = load_rgb(source_image)
            except Exception as exc:
                skipped.append(SkippedImage(split, class_name, str(source_image), str(exc), strategy))
                continue

            source_formats[source_format] += 1
            target_image = unique_target(target_dir / f"{source_image.stem}.jpg")
            action = "copy_jpeg" if source_format in {"jpeg", "mpo"} else "convert_to_jpeg"
            image.save(target_image, format="JPEG", quality=quality, optimize=True)
            processed.append(
                ProcessedImage(split, class_name, str(source_image), str(target_image), action, source_format, strategy)
            )
            distribution[split][class_name] += 1
            action_counts[action] += 1

    output_classes = sorted(set(distribution["train"]) & set(distribution["val"]))
    rebalanced_classes = sorted(item["class_name"] for item in class_strategies if item["strategy"] != "preserve_raw_split")
    val_only_rebalanced = sorted(item["class_name"] for item in class_strategies if item["strategy"] == "rebalance_val_only")
    train_only_rebalanced = sorted(item["class_name"] for item in class_strategies if item["strategy"] == "rebalance_train_only")

    status = "complete" if len(output_classes) == len(all_classes) and not excluded_classes else "partial"
    report = {
        "source": str(source),
        "output": str(output),
        "quality": quality,
        "val_ratio": val_ratio,
        "min_train": min_train,
        "min_val": min_val,
        "summary": {
            "status": status,
            "raw_classes": len(all_classes),
            "output_classes": len(output_classes),
            "train_images": sum(distribution["train"].values()),
            "val_images": sum(distribution["val"].values()),
            "total_images": len(processed),
            "skipped_images": len(skipped),
            "excluded_classes": [item["class_name"] for item in excluded_classes],
            "rebalanced_classes": rebalanced_classes,
            "val_only_rebalanced_classes": val_only_rebalanced,
            "train_only_rebalanced_classes": train_only_rebalanced,
            "actions": dict(sorted(action_counts.items())),
            "source_formats": dict(sorted(source_formats.items())),
            "strategy_counts": dict(sorted(strategy_counts.items())),
        },
        "classes": output_classes,
        "distribution": {split: dict(counter) for split, counter in distribution.items()},
        "class_strategies": class_strategies,
        "excluded_classes": excluded_classes,
        "skipped": [asdict(item) for item in skipped],
        "samples": [asdict(item) for item in processed[:20]],
        "boundary_note": (
            "该数据集用于 93 类覆盖补齐实验。原始 train/val 均存在的类别保留原始划分；"
            "仅单侧存在的类别按确定性顺序重划 train/val，因此其结果不应与原始 92 类 strict 基准直接等价比较。"
        ),
    }
    return report


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 93 类补齐分类数据集报告",
        "",
        f"- 来源: `{report['source']}`",
        f"- 输出: `{report['output']}`",
        f"- JPEG 质量: {report['quality']}",
        f"- 单侧类别验证比例: {report['val_ratio']}",
        "",
        "## 总览",
        "",
        f"- 状态: `{summary['status']}`",
        f"- 原始类别: {summary['raw_classes']}；输出类别: {summary['output_classes']}",
        f"- 图片: train {summary['train_images']} / val {summary['val_images']} / total {summary['total_images']}",
        f"- 跳过图片: {summary['skipped_images']}",
        f"- 重划类别: {', '.join(summary['rebalanced_classes']) if summary['rebalanced_classes'] else '无'}",
        f"- val-only 重划类别: {', '.join(summary['val_only_rebalanced_classes']) if summary['val_only_rebalanced_classes'] else '无'}",
        f"- train-only 重划类别: {', '.join(summary['train_only_rebalanced_classes']) if summary['train_only_rebalanced_classes'] else '无'}",
        f"- 排除类别: {', '.join(summary['excluded_classes']) if summary['excluded_classes'] else '无'}",
        f"- 操作统计: {summary['actions']}",
        f"- 内容格式: {summary['source_formats']}",
        "",
        "## 划分策略",
        "",
        "| 类别 | 策略 | raw train | raw val | assigned train | assigned val |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for item in report["class_strategies"]:
        if item["strategy"] != "preserve_raw_split":
            lines.append(
                f"| {item['class_name']} | {item['strategy']} | {item['raw_train']} | {item['raw_val']} | "
                f"{item['assigned_train']} | {item['assigned_val']} |"
            )
    if not summary["rebalanced_classes"]:
        lines.append("| 无 | preserve_raw_split | 0 | 0 | 0 | 0 |")

    lines.extend(["", "## 跳过文件", ""])
    if report["skipped"]:
        for item in report["skipped"]:
            lines.append(f"- [{item['split']}/{item['class_name']}/{item['strategy']}] `{item['source']}`: {item['reason']}")
    else:
        lines.append("- 无")

    lines.extend(["", "## 边界说明", "", f"- {report['boundary_note']}"])
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report_files(report: dict[str, Any], json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, markdown_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a strict JPEG classification dataset that completes val-only/train-only classes.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--output", default="data/classification_strict_jpeg_93class")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--quality", type=int, default=95)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--min-train", type=int, default=1)
    parser.add_argument("--min-val", type=int, default=1)
    parser.add_argument("--report", default="reports/classification_93class_completion_report.json")
    parser.add_argument("--markdown", default="reports/classification_93class_completion_report.md")
    args = parser.parse_args()

    report = prepare(
        source=Path(args.source),
        output=resolve_project_path(args.output),
        overwrite=args.overwrite,
        quality=args.quality,
        val_ratio=args.val_ratio,
        min_train=args.min_train,
        min_val=args.min_val,
    )

    dataset_report = resolve_project_path(args.output) / "classification_93class_completion_report.json"
    dataset_markdown = dataset_report.with_suffix(".md")
    write_report_files(report, dataset_report, dataset_markdown)
    write_report_files(report, resolve_project_path(args.report), resolve_project_path(args.markdown))

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0 if report["summary"]["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
