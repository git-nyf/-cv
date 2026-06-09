from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from path_utils import IMAGE_EXTS, resolve_project_path


@dataclass
class ConvertedImage:
    split: str
    class_name: str
    class_id: int
    source: str
    image: str
    label: str


def iter_class_images(split_dir: Path) -> list[tuple[str, Path]]:
    items: list[tuple[str, Path]] = []
    if not split_dir.exists():
        return items
    for class_dir in sorted([p for p in split_dir.iterdir() if p.is_dir()], key=lambda p: p.name):
        for image in sorted(class_dir.rglob("*")):
            if image.is_file() and image.suffix.lower() in IMAGE_EXTS:
                items.append((class_dir.name, image))
    return items


def unique_destination(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    idx = 1
    while True:
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def write_data_yaml(output_root: Path, names: list[str]) -> None:
    data = {
        "path": output_root.as_posix(),
        "train": "images/train",
        "val": "images/val",
        "nc": len(names),
        "names": names,
    }
    (output_root / "data.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (output_root / "classes.txt").write_text("\n".join(names) + "\n", encoding="utf-8")


def write_markdown(report: dict, output: Path) -> None:
    lines = [
        "# 分类目录转 YOLO 整图框报告",
        "",
        "## 结论",
        "",
        "该转换为临时方案：每张图生成一个覆盖全图的 YOLO bbox，用于验证检测训练链路；不等价于真实目标检测标注。",
        "",
        "## 概览",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 类别映射", ""])
    for name, idx in report["class_to_id"].items():
        lines.append(f"- {idx}: {name}")
    lines.extend(["", "## 划分统计", ""])
    for split, dist in report["split_distribution"].items():
        lines.append(f"### {split}")
        for name, count in dist.items():
            lines.append(f"- {name}: {count}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def convert(source_root: Path, output_root: Path, overwrite: bool) -> dict:
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    if not source_root.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_root}")
    if output_root.exists() and overwrite:
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    split_items = {split: iter_class_images(source_root / split) for split in ("train", "val")}
    class_names = sorted({class_name for items in split_items.values() for class_name, _ in items})
    if not class_names:
        raise ValueError(f"No class folders with images found under {source_root}/train or {source_root}/val")
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    converted: list[ConvertedImage] = []
    split_distribution: dict[str, Counter[str]] = {"train": Counter(), "val": Counter()}
    for split, items in split_items.items():
        for class_name, source_image in items:
            class_id = class_to_id[class_name]
            rel_dir = Path(split) / class_name
            image_dir = output_root / "images" / rel_dir
            label_dir = output_root / "labels" / rel_dir
            image_dir.mkdir(parents=True, exist_ok=True)
            label_dir.mkdir(parents=True, exist_ok=True)

            dest_image = unique_destination(image_dir / source_image.name)
            shutil.copy2(source_image, dest_image)
            dest_label = label_dir / dest_image.with_suffix(".txt").name
            dest_label.write_text(f"{class_id} 0.5 0.5 1.0 1.0\n", encoding="utf-8")
            converted.append(
                ConvertedImage(
                    split=split,
                    class_name=class_name,
                    class_id=class_id,
                    source=str(source_image),
                    image=str(dest_image),
                    label=str(dest_label),
                )
            )
            split_distribution[split][class_name] += 1

    write_data_yaml(output_root, class_names)
    report = {
        "source_root": str(source_root),
        "output_root": str(output_root),
        "summary": {
            "images": len(converted),
            "classes": len(class_names),
            "train_images": sum(split_distribution["train"].values()),
            "val_images": sum(split_distribution["val"].values()),
            "label_policy": "full_image_bbox",
        },
        "class_to_id": class_to_id,
        "split_distribution": {split: dict(counter) for split, counter in split_distribution.items()},
        "samples": [asdict(item) for item in converted[:20]],
    }
    (output_root / "conversion_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output_root / "conversion_report.md")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert classification folders to temporary YOLO full-image boxes.")
    parser.add_argument("--source", default=r"D:\AAA中药cv\data", help="Source root with train/val class folders.")
    parser.add_argument("--output", default="data/partial_fullbox_yolo", help="Output YOLO detection dataset root.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source = Path(args.source)
    output = resolve_project_path(args.output)
    report = convert(source, output, args.overwrite)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
