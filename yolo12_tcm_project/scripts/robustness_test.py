from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

from path_utils import iter_images, resolve_project_path


def augment(image: Image.Image, kind: str) -> Image.Image:
    if kind == "brightness_low":
        return ImageEnhance.Brightness(image).enhance(0.55)
    if kind == "brightness_high":
        return ImageEnhance.Brightness(image).enhance(1.45)
    if kind == "contrast_low":
        return ImageEnhance.Contrast(image).enhance(0.65)
    if kind == "rotate_15":
        return image.rotate(15, expand=True, fillcolor=(255, 255, 255))
    if kind == "blur":
        return image.filter(ImageFilter.GaussianBlur(radius=2))
    if kind == "occlusion":
        img = image.copy()
        w, h = img.size
        from PIL import ImageDraw

        draw = ImageDraw.Draw(img)
        draw.rectangle([w * 0.35, h * 0.35, w * 0.65, h * 0.65], fill=(128, 128, 128))
        return img
    return image.copy()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate robustness test image variants.")
    parser.add_argument("--images", default="data/splits/images/test")
    parser.add_argument("--output", default="runs/benchmarks/robustness_inputs")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    source = resolve_project_path(args.images)
    output = resolve_project_path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    kinds = ["brightness_low", "brightness_high", "contrast_low", "rotate_15", "blur", "occlusion"]
    manifest = []
    for image_path in sorted(iter_images(source))[: args.limit]:
        with Image.open(image_path) as im:
            im = im.convert("RGB")
            for kind in kinds:
                aug = augment(im, kind)
                target = output / kind / image_path.name
                target.parent.mkdir(parents=True, exist_ok=True)
                aug.save(target)
                manifest.append({"source": str(image_path), "variant": kind, "output": str(target)})
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(manifest)} robustness images: {manifest_path}")
    print("Next: run infer_image.py/evaluate_yolo12.py on these variants and compare metrics with the clean test set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

