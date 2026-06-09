from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from path_utils import IMAGE_EXTS, project_root, resolve_project_path


@dataclass
class CopiedImage:
    split: str
    class_name: str
    source: str
    target: str


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


def prepare(source: Path, output: Path, overwrite: bool, copy_mode: str) -> dict[str, Any]:
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

    copied: list[CopiedImage] = []
    distribution: dict[str, Counter[str]] = {"train": Counter(), "val": Counter()}
    for split, dirs in (("train", train_dirs), ("val", val_dirs)):
        for class_name in keep_classes:
            source_dir = dirs[class_name]
            target_dir = output / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            for source_image in image_files(source_dir):
                rel = source_image.relative_to(source_dir)
                target_image = unique_target(target_dir / rel.name)
                if copy_mode == "hardlink":
                    try:
                        target_image.hardlink_to(source_image)
                    except OSError:
                        shutil.copy2(source_image, target_image)
                else:
                    shutil.copy2(source_image, target_image)
                copied.append(CopiedImage(split, class_name, str(source_image), str(target_image)))
                distribution[split][class_name] += 1

    report = {
        "source": str(source),
        "output": str(output),
        "copy_mode": copy_mode,
        "summary": {
            "classes": len(keep_classes),
            "train_images": sum(distribution["train"].values()),
            "val_images": sum(distribution["val"].values()),
            "total_images": len(copied),
            "dropped_train_only_classes": dropped_train,
            "dropped_val_only_classes": dropped_val,
        },
        "classes": keep_classes,
        "distribution": {split: dict(counter) for split, counter in distribution.items()},
        "samples": [asdict(item) for item in copied[:20]],
    }
    (output / "classification_clean_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output / "classification_clean_report.md")
    return report


def write_markdown(report: dict[str, Any], output: Path) -> None:
    lines = [
        "# 清洗后分类数据集报告",
        "",
        f"- 来源: `{report['source']}`",
        f"- 输出: `{report['output']}`",
        f"- 复制模式: `{report['copy_mode']}`",
        "",
        "## 总览",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 类别", ""])
    for idx, name in enumerate(report["classes"]):
        lines.append(f"- {idx}: {name}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a clean classification dataset with matching train/val class folders.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--output", default="data/classification_clean")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--copy-mode", choices=["copy", "hardlink"], default="copy")
    args = parser.parse_args()

    report = prepare(Path(args.source), resolve_project_path(args.output), args.overwrite, args.copy_mode)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
