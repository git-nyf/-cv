from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from path_utils import resolve_project_path


CLASSES = {
    0: ("demo_round_piece", (66, 135, 245)),
    1: ("demo_long_piece", (35, 150, 90)),
    2: ("demo_slice_piece", (190, 120, 45)),
}


def yolo_box(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> tuple[float, float, float, float]:
    xc = ((x1 + x2) / 2) / w
    yc = ((y1 + y2) / 2) / h
    bw = (x2 - x1) / w
    bh = (y2 - y1) / h
    return xc, yc, bw, bh


def create_image(path: Path, label_path: Path, index: int, size: int = 640) -> None:
    rng = random.Random(index)
    image = Image.new("RGB", (size, size), (248, 249, 246))
    draw = ImageDraw.Draw(image)
    labels: list[str] = []

    for class_id in sorted(CLASSES):
        name, color = CLASSES[class_id]
        cx = rng.randint(120, size - 120)
        cy = rng.randint(120, size - 120)
        if class_id == 0:
            r = rng.randint(38, 62)
            box = (cx - r, cy - r, cx + r, cy + r)
            draw.ellipse(box, fill=color, outline=(40, 55, 70), width=3)
        elif class_id == 1:
            length = rng.randint(130, 190)
            thickness = rng.randint(24, 36)
            box = (cx - length // 2, cy - thickness // 2, cx + length // 2, cy + thickness // 2)
            draw.rounded_rectangle(box, radius=16, fill=color, outline=(40, 55, 70), width=3)
        else:
            ww = rng.randint(90, 130)
            hh = rng.randint(50, 78)
            box = (cx - ww // 2, cy - hh // 2, cx + ww // 2, cy + hh // 2)
            draw.rectangle(box, fill=color, outline=(40, 55, 70), width=3)
        xc, yc, bw, bh = yolo_box(*box, size, size)
        labels.append(f"{class_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

    image.save(path)
    label_path.write_text("\n".join(labels) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a tiny synthetic YOLO dataset for pipeline smoke tests.")
    parser.add_argument("--output", default="data/demo_yolo")
    parser.add_argument("--count", type=int, default=18)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    output = resolve_project_path(args.output)
    if output.exists() and args.overwrite:
        shutil.rmtree(output)
    images = output / "images"
    labels = output / "labels"
    images.mkdir(parents=True, exist_ok=True)
    labels.mkdir(parents=True, exist_ok=True)

    for idx in range(args.count):
        create_image(images / f"demo_{idx:03d}.jpg", labels / f"demo_{idx:03d}.txt", idx)

    names = [CLASSES[i][0] for i in sorted(CLASSES)]
    (output / "classes.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    (output / "DEMO_DATASET_NOTICE.md").write_text(
        "# Demo 数据集说明\n\n"
        "该数据集由脚本绘制几何形状生成，仅用于验证 YOLO 数据校验、划分、前后端和训练命令链路。"
        "它不是中药饮片真实数据，不能用于项目精度汇报或替代正式训练数据。\n",
        encoding="utf-8",
    )
    (output / "manifest.json").write_text(
        json.dumps({"classes": names, "images": args.count, "purpose": "pipeline smoke test only"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Created demo YOLO dataset: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

