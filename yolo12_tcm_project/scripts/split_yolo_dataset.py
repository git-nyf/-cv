from __future__ import annotations

import argparse
import random
import shutil
from collections import defaultdict
from pathlib import Path

import yaml

from path_utils import IMAGE_EXTS, iter_images, resolve_project_path


def read_primary_classes(label_path: Path) -> set[int]:
    classes: set[int] = set()
    if not label_path.exists():
        return classes
    for line in label_path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split()
        if len(parts) >= 5:
            try:
                classes.add(int(float(parts[0])))
            except ValueError:
                pass
    return classes


def split_items(items: list[Path], ratios: tuple[float, float, float], seed: int) -> dict[str, list[Path]]:
    rng = random.Random(seed)
    shuffled = items[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(round(n * ratios[0]))
    n_val = int(round(n * ratios[1]))
    if n_train + n_val > n:
        n_val = max(0, n - n_train)
    return {
        "train": shuffled[:n_train],
        "val": shuffled[n_train : n_train + n_val],
        "test": shuffled[n_train + n_val :],
    }


def stratified_split(images: list[Path], images_root: Path, labels_root: Path, ratios: tuple[float, float, float], seed: int) -> dict[str, list[Path]]:
    by_class: defaultdict[int, list[Path]] = defaultdict(list)
    no_label: list[Path] = []
    assigned: set[Path] = set()

    for image in images:
        rel = image.relative_to(images_root)
        label = labels_root / rel.with_suffix(".txt")
        classes = read_primary_classes(label)
        if not classes:
            no_label.append(image)
            continue
        # Use the rarest class later by sorting class buckets, reducing minority-class loss.
        primary = min(classes)
        by_class[primary].append(image)

    splits = {"train": [], "val": [], "test": []}
    for cls in sorted(by_class, key=lambda c: len(by_class[c])):
        bucket = [p for p in by_class[cls] if p not in assigned]
        partial = split_items(bucket, ratios, seed + cls)
        for name, paths in partial.items():
            splits[name].extend(paths)
            assigned.update(paths)

    if no_label:
        partial = split_items(no_label, ratios, seed + 999)
        for name, paths in partial.items():
            splits[name].extend(paths)

    return splits


def copy_pair(image: Path, images_root: Path, labels_root: Path, output: Path, split: str) -> None:
    rel = image.relative_to(images_root)
    image_out = output / "images" / split / rel
    label_in = labels_root / rel.with_suffix(".txt")
    label_out = output / "labels" / split / rel.with_suffix(".txt")
    image_out.parent.mkdir(parents=True, exist_ok=True)
    label_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image, image_out)
    if label_in.exists():
        shutil.copy2(label_in, label_out)
    else:
        label_out.write_text("", encoding="utf-8")


def load_names(source_yaml: Path | None, classes_file: Path | None) -> dict[int, str]:
    if classes_file and classes_file.exists():
        return {i: line.strip() for i, line in enumerate(classes_file.read_text(encoding="utf-8").splitlines()) if line.strip()}
    if source_yaml and source_yaml.exists():
        data = yaml.safe_load(source_yaml.read_text(encoding="utf-8")) or {}
        names = data.get("names")
        if isinstance(names, list):
            return {i: str(v) for i, v in enumerate(names)}
        if isinstance(names, dict):
            return {int(k): str(v) for k, v in names.items()}
    return {0: "class_0"}


def write_data_yaml(output: Path, names: dict[int, str]) -> None:
    data = {
        "path": str(output.resolve()).replace("\\", "/"),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {int(k): v for k, v in sorted(names.items())},
    }
    target = output / "data.yaml"
    target.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Split YOLO dataset into train/val/test.")
    parser.add_argument("--images", default="data/yolo/images")
    parser.add_argument("--labels", default="data/yolo/labels")
    parser.add_argument("--output", default="data/splits")
    parser.add_argument("--data-yaml", default="configs/data.yaml")
    parser.add_argument("--classes", default="")
    parser.add_argument("--ratios", nargs=3, type=float, default=[0.7, 0.2, 0.1])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    ratios = tuple(args.ratios)
    if abs(sum(ratios) - 1.0) > 1e-6:
        raise SystemExit("--ratios must sum to 1.0")

    images_root = resolve_project_path(args.images)
    labels_root = resolve_project_path(args.labels)
    output = resolve_project_path(args.output)
    if output.exists() and args.overwrite:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    images = sorted(iter_images(images_root))
    if not images:
        raise SystemExit(f"No images found under {images_root}")

    splits = stratified_split(images, images_root, labels_root, ratios, args.seed)
    for split, split_images in splits.items():
        for image in split_images:
            copy_pair(image, images_root, labels_root, output, split)

    names = load_names(resolve_project_path(args.data_yaml) if args.data_yaml else None, resolve_project_path(args.classes) if args.classes else None)
    write_data_yaml(output, names)
    print("Split summary:")
    for split, split_images in splits.items():
        print(f"  {split}: {len(split_images)} images")
    print(f"Data config: {output / 'data.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
