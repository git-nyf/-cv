from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from path_utils import IMAGE_EXTS, project_root, resolve_project_path


@dataclass
class ImageIssue:
    level: str
    file: str
    message: str


def default_source() -> Path:
    return project_root().parent / "data"


def iter_split_classes(source: Path, split: str) -> list[Path]:
    split_root = source / split
    if not split_root.exists():
        return []
    return sorted([p for p in split_root.iterdir() if p.is_dir()], key=lambda p: p.name)


def count_images(class_dir: Path) -> list[Path]:
    return sorted(
        [p for p in class_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda p: str(p),
    )


def inspect(source: Path, verify_images: bool = False, max_verify: int = 0) -> dict[str, Any]:
    source = source.resolve()
    issues: list[ImageIssue] = []
    split_distribution: dict[str, dict[str, int]] = {}
    split_totals: dict[str, int] = {}
    all_classes: dict[str, set[str]] = defaultdict(set)

    for split in ("train", "val", "test"):
        split_root = source / split
        if not split_root.exists():
            if split != "test":
                issues.append(ImageIssue("error", str(split_root), f"缺少 {split} 目录"))
            continue
        dist: dict[str, int] = {}
        for class_dir in iter_split_classes(source, split):
            images = count_images(class_dir)
            dist[class_dir.name] = len(images)
            all_classes[split].add(class_dir.name)
        split_distribution[split] = dict(sorted(dist.items()))
        split_totals[split] = sum(dist.values())

    if "train" in all_classes and "val" in all_classes:
        train_only = sorted(all_classes["train"] - all_classes["val"])
        val_only = sorted(all_classes["val"] - all_classes["train"])
        for name in train_only:
            issues.append(ImageIssue("warning", str(source / "train" / name), "该类别只出现在 train 中"))
        for name in val_only:
            issues.append(ImageIssue("warning", str(source / "val" / name), "该类别只出现在 val 中"))

    verified = 0
    if verify_images:
        candidates: list[Path] = []
        for split in ("train", "val", "test"):
            for class_dir in iter_split_classes(source, split):
                candidates.extend(count_images(class_dir))
        if max_verify > 0:
            candidates = candidates[:max_verify]
        for image_path in candidates:
            try:
                with Image.open(image_path) as im:
                    im.verify()
                verified += 1
            except (UnidentifiedImageError, OSError) as exc:
                issues.append(ImageIssue("error", str(image_path), f"图片损坏或无法读取: {exc}"))

    class_union = sorted(set().union(*all_classes.values())) if all_classes else []
    return {
        "source": str(source),
        "summary": {
            "classes": len(class_union),
            "train_images": split_totals.get("train", 0),
            "val_images": split_totals.get("val", 0),
            "test_images": split_totals.get("test", 0),
            "total_images": sum(split_totals.values()),
            "verified_images": verified,
            "errors": sum(1 for item in issues if item.level == "error"),
            "warnings": sum(1 for item in issues if item.level == "warning"),
        },
        "classes": class_union,
        "split_distribution": split_distribution,
        "issues": [asdict(item) for item in issues],
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    lines = [
        "# 分类数据集检查报告",
        "",
        f"- 数据路径: `{report['source']}`",
        "",
        "## 总览",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 划分统计", ""])
    for split, dist in report["split_distribution"].items():
        lines.append(f"### {split}")
        for name, count in dist.items():
            lines.append(f"- {name}: {count}")
        lines.append("")
    lines.extend(["## 问题列表", ""])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"- [{issue['level']}] `{issue['file']}`: {issue['message']}")
    else:
        lines.append("- 未发现问题")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a classification dataset arranged as train/class/*.jpg and val/class/*.jpg.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--data", dest="source", help=argparse.SUPPRESS)
    parser.add_argument("--verify-images", action="store_true")
    parser.add_argument("--max-verify", type=int, default=0, help="0 means verify all images when --verify-images is set.")
    parser.add_argument("--output", default="reports/classification_dataset_inspection.json")
    parser.add_argument("--markdown", default="reports/classification_dataset_inspection.md")
    args = parser.parse_args()

    source = Path(args.source)
    report = inspect(source, verify_images=args.verify_images, max_verify=args.max_verify)
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown = resolve_project_path(args.markdown)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, markdown)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
