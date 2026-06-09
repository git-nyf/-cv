from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image

from path_utils import IMAGE_EXTS, resolve_project_path


def convert_classification_to_detection(source: Path, output: Path, overwrite: bool) -> None:
    if output.exists() and overwrite:
        shutil.rmtree(output)
    images_out = output / "images"
    labels_out = output / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    classes = sorted([p for p in source.iterdir() if p.is_dir()])
    if not classes:
        raise SystemExit(f"分类目录为空或不存在类别子目录: {source}")
    class_names = [p.name for p in classes]
    (output / "classes.txt").write_text("\n".join(class_names) + "\n", encoding="utf-8")

    count = 0
    for class_id, class_dir in enumerate(classes):
        for image in class_dir.rglob("*"):
            if not image.is_file() or image.suffix.lower() not in IMAGE_EXTS:
                continue
            rel_name = f"{class_id:03d}_{image.stem}{image.suffix.lower()}"
            dst_image = images_out / rel_name
            dst_label = labels_out / f"{Path(rel_name).stem}.txt"
            try:
                with Image.open(image) as im:
                    im.verify()
            except Exception as exc:
                print(f"Skip broken image: {image} ({exc})")
                continue
            shutil.copy2(image, dst_image)
            # Temporary whole-image box. This is not equivalent to real detection annotation.
            dst_label.write_text(f"{class_id} 0.5 0.5 1.0 1.0\n", encoding="utf-8")
            count += 1

    note = output / "WHOLE_IMAGE_BOX_WARNING.md"
    note.write_text(
        "# 整图框临时标注说明\n\n"
        "该目录由分类数据集自动转换而来，每张图片被写入一个覆盖整图的 YOLO bbox。"
        "这只能用于快速跑通训练流程，不等价于真实目标检测标注；正式实验应使用人工或半自动标注的饮片边界框。\n",
        encoding="utf-8",
    )
    print(f"Converted {count} images into temporary YOLO detection format.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare dataset for YOLOv12 TCM project.")
    parser.add_argument("--source", required=True, help="Source dataset root")
    parser.add_argument("--output", default="data/yolo", help="Output YOLO root")
    parser.add_argument("--mode", choices=["yolo", "classification"], default="yolo")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source = resolve_project_path(args.source)
    output = resolve_project_path(args.output)
    if args.mode == "classification":
        convert_classification_to_detection(source, output, args.overwrite)
        return 0

    if output.exists() and args.overwrite:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    for name in ("images", "labels", "data.yaml", "classes.txt"):
        candidate = source / name
        if candidate.exists():
            target = output / name
            if candidate.is_dir():
                shutil.copytree(candidate, target, dirs_exist_ok=True)
            else:
                shutil.copy2(candidate, target)
    print(f"Copied YOLO dataset assets from {source} to {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

