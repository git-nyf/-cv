from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, UnidentifiedImageError

from path_utils import IMAGE_EXTS, iter_images, resolve_project_path


@dataclass
class DatasetIssue:
    level: str
    file: str
    message: str


def sha1_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def load_names(data_yaml: Path | None, classes_file: Path | None) -> dict[int, str]:
    if classes_file and classes_file.exists():
        lines = [x.strip() for x in classes_file.read_text(encoding="utf-8").splitlines() if x.strip()]
        return {i: name for i, name in enumerate(lines)}
    if data_yaml and data_yaml.exists():
        data = yaml.safe_load(data_yaml.read_text(encoding="utf-8")) or {}
        names = data.get("names", {})
        if isinstance(names, list):
            return {i: str(name) for i, name in enumerate(names)}
        if isinstance(names, dict):
            return {int(k): str(v) for k, v in names.items()}
    return {}


def expected_label_path(image_path: Path, images_root: Path, labels_root: Path) -> Path:
    rel = image_path.relative_to(images_root)
    return labels_root / rel.with_suffix(".txt")


def parse_label_file(path: Path, class_count: int | None, issues: list[DatasetIssue]) -> list[tuple[int, float, float, float, float]]:
    boxes: list[tuple[int, float, float, float, float]] = []
    seen: set[str] = set()
    if not path.exists():
        return boxes
    for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line in seen:
            issues.append(DatasetIssue("warning", str(path), f"重复标注行: line {lineno}"))
        seen.add(line)
        parts = line.split()
        if len(parts) < 5:
            issues.append(DatasetIssue("error", str(path), f"YOLO 标注字段不足: line {lineno}"))
            continue
        try:
            cls = int(float(parts[0]))
            x, y, w, h = map(float, parts[1:5])
        except ValueError:
            issues.append(DatasetIssue("error", str(path), f"标注无法解析为数字: line {lineno}"))
            continue
        if cls < 0 or (class_count is not None and cls >= class_count):
            issues.append(DatasetIssue("error", str(path), f"类别编号越界: line {lineno}, class={cls}"))
        if not all(0.0 <= v <= 1.0 for v in (x, y, w, h)):
            issues.append(DatasetIssue("error", str(path), f"bbox 未归一化到 0~1: line {lineno}"))
        if w <= 0 or h <= 0:
            issues.append(DatasetIssue("error", str(path), f"bbox 宽高必须为正: line {lineno}"))
        if x - w / 2 < 0 or x + w / 2 > 1 or y - h / 2 < 0 or y + h / 2 > 1:
            issues.append(DatasetIssue("warning", str(path), f"bbox 超出图片边界: line {lineno}"))
        boxes.append((cls, x, y, w, h))
    return boxes


def validate(images_root: Path, labels_root: Path, data_yaml: Path | None, classes_file: Path | None) -> dict[str, Any]:
    issues: list[DatasetIssue] = []
    names = load_names(data_yaml, classes_file)
    class_count = len(names) if names else None
    images = sorted(iter_images(images_root))
    class_counter: Counter[int] = Counter()
    image_counter: Counter[int] = Counter()
    empty_labels = 0
    hashes: defaultdict[str, list[str]] = defaultdict(list)

    if not images_root.exists():
        issues.append(DatasetIssue("error", str(images_root), "图片目录不存在"))
    if not labels_root.exists():
        issues.append(DatasetIssue("error", str(labels_root), "标签目录不存在"))

    for image_path in images:
        try:
            with Image.open(image_path) as im:
                im.verify()
        except (UnidentifiedImageError, OSError) as exc:
            issues.append(DatasetIssue("error", str(image_path), f"图片损坏或无法读取: {exc}"))
            continue
        hashes[sha1_file(image_path)].append(str(image_path))
        label_path = expected_label_path(image_path, images_root, labels_root)
        if not label_path.exists():
            issues.append(DatasetIssue("error", str(label_path), "图片缺少对应标签文件"))
            continue
        boxes = parse_label_file(label_path, class_count, issues)
        if not boxes:
            empty_labels += 1
            issues.append(DatasetIssue("warning", str(label_path), "空标签文件"))
        classes_in_image = set()
        for cls, *_ in boxes:
            class_counter[cls] += 1
            classes_in_image.add(cls)
        for cls in classes_in_image:
            image_counter[cls] += 1

    for digest, files in hashes.items():
        if len(files) > 1:
            issues.append(DatasetIssue("warning", files[0], f"发现重复图片 SHA1={digest}: " + "; ".join(files)))

    orphan_labels = []
    if labels_root.exists():
        for label in labels_root.rglob("*.txt"):
            rel = label.relative_to(labels_root).with_suffix("")
            has_image = any((images_root / rel).with_suffix(ext).exists() for ext in IMAGE_EXTS)
            if not has_image:
                orphan_labels.append(str(label))
                issues.append(DatasetIssue("warning", str(label), "标签文件没有对应图片"))

    return {
        "summary": {
            "images": len(images),
            "classes_declared": class_count,
            "labels_empty": empty_labels,
            "orphan_labels": len(orphan_labels),
            "errors": sum(1 for i in issues if i.level == "error"),
            "warnings": sum(1 for i in issues if i.level == "warning"),
        },
        "classes": names,
        "box_distribution": dict(sorted(class_counter.items())),
        "image_distribution": dict(sorted(image_counter.items())),
        "issues": [asdict(i) for i in issues],
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    lines = [
        "# YOLO 数据集检查报告",
        "",
        "## 总览",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 类别框数量"])
    if report["box_distribution"]:
        for cls, count in report["box_distribution"].items():
            name = report["classes"].get(int(cls), f"class_{cls}") if report["classes"] else f"class_{cls}"
            lines.append(f"- {cls} {name}: {count}")
    else:
        lines.append("- 未发现有效标注框")
    lines.extend(["", "## 问题列表"])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"- [{issue['level']}] `{issue['file']}`: {issue['message']}")
    else:
        lines.append("- 未发现问题")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a YOLO detection dataset.")
    parser.add_argument("--images", default="data/yolo/images", help="Images root")
    parser.add_argument("--labels", default="data/yolo/labels", help="Labels root")
    parser.add_argument("--data-yaml", default="configs/data.yaml", help="YOLO data.yaml")
    parser.add_argument("--classes", default="", help="Optional classes.txt")
    parser.add_argument("--output", default="reports/dataset_validation.json", help="JSON report path")
    parser.add_argument("--markdown", default="reports/dataset_validation.md", help="Markdown report path")
    args = parser.parse_args()

    images = resolve_project_path(args.images)
    labels = resolve_project_path(args.labels)
    data_yaml = resolve_project_path(args.data_yaml) if args.data_yaml else None
    classes = resolve_project_path(args.classes) if args.classes else None
    report = validate(images, labels, data_yaml, classes)
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md = resolve_project_path(args.markdown)
    md.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, md)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
