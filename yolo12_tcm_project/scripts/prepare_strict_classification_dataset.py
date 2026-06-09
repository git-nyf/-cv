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


@dataclass
class SkippedImage:
    split: str
    class_name: str
    source: str
    reason: str


def default_source() -> Path:
    return project_root().parent / "data"


def class_dirs(root: Path, split: str) -> dict[str, Path]:
    split_root = root / split
    if not split_root.exists():
        return {}
    return {p.name: p for p in sorted(split_root.iterdir(), key=lambda item: item.name) if p.is_dir()}


def image_files(root: Path) -> list[Path]:
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
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        elif image.mode == "L":
            image = image.convert("RGB")
        else:
            image = image.copy()
    return image, fmt


def prepare(source: Path, output: Path, overwrite: bool, quality: int) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    if not source.exists():
        raise FileNotFoundError(f"source dataset not found: {source}")
    if output.exists() and overwrite:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    train_dirs = class_dirs(source, "train")
    val_dirs = class_dirs(source, "val")
    keep_classes = sorted(set(train_dirs) & set(val_dirs))
    dropped_train = sorted(set(train_dirs) - set(val_dirs))
    dropped_val = sorted(set(val_dirs) - set(train_dirs))

    processed: list[ProcessedImage] = []
    skipped: list[SkippedImage] = []
    distribution: dict[str, Counter[str]] = {"train": Counter(), "val": Counter()}
    action_counts: Counter[str] = Counter()
    source_formats: Counter[str] = Counter()

    for split, dirs in (("train", train_dirs), ("val", val_dirs)):
        for class_name in keep_classes:
            source_dir = dirs[class_name]
            target_dir = output / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            for source_image in image_files(source_dir):
                try:
                    image, source_format = load_rgb(source_image)
                except Exception as exc:
                    skipped.append(SkippedImage(split, class_name, str(source_image), str(exc)))
                    continue

                source_formats[source_format] += 1
                target_image = unique_target(target_dir / f"{source_image.stem}.jpg")
                action = "copy_jpeg" if source_format in {"jpeg", "mpo"} else "convert_to_jpeg"
                image.save(target_image, format="JPEG", quality=quality, optimize=True)
                processed.append(ProcessedImage(split, class_name, str(source_image), str(target_image), action, source_format))
                distribution[split][class_name] += 1
                action_counts[action] += 1

    report = {
        "source": str(source),
        "output": str(output),
        "quality": quality,
        "summary": {
            "classes": len(keep_classes),
            "train_images": sum(distribution["train"].values()),
            "val_images": sum(distribution["val"].values()),
            "total_images": len(processed),
            "skipped_images": len(skipped),
            "dropped_train_only_classes": dropped_train,
            "dropped_val_only_classes": dropped_val,
            "actions": dict(sorted(action_counts.items())),
            "source_formats": dict(sorted(source_formats.items())),
        },
        "classes": keep_classes,
        "distribution": {split: dict(counter) for split, counter in distribution.items()},
        "skipped": [asdict(item) for item in skipped],
        "samples": [asdict(item) for item in processed[:20]],
    }
    (output / "strict_classification_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output / "strict_classification_report.md")
    return report


def write_markdown(report: dict[str, Any], output: Path) -> None:
    lines = [
        "# 严格分类数据集报告",
        "",
        f"- 来源: `{report['source']}`",
        f"- 输出: `{report['output']}`",
        f"- JPEG 质量: {report['quality']}",
        "",
        "## 总览",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 类别", ""])
    for idx, name in enumerate(report["classes"]):
        lines.append(f"- {idx}: {name}")
    lines.extend(["", "## 跳过文件", ""])
    if report["skipped"]:
        for item in report["skipped"]:
            lines.append(f"- `{item['source']}`: {item['reason']}")
    else:
        lines.append("- 无")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a strict classification dataset with JPEG-only readable images.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--output", default="data/classification_strict_jpeg")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--quality", type=int, default=95)
    args = parser.parse_args()

    report = prepare(Path(args.source), resolve_project_path(args.output), args.overwrite, args.quality)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
