from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from path_utils import IMAGE_EXTS, project_root, resolve_project_path


@dataclass
class AnnotationSample:
    image_id: str
    class_index: int
    class_name: str
    source_split: str
    source_path: str
    package_image: str
    yolo_label: str
    width: int
    height: int
    sha256: str
    annotation_status: str = "pending"


def default_source() -> Path:
    root = project_root()
    completed_93 = root / "data" / "classification_strict_jpeg_93class"
    if completed_93.exists():
        return completed_93
    return root / "data" / "classification_strict_jpeg"


def class_dirs(source: Path, split: str) -> dict[str, Path]:
    split_root = source / split
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        image.load()
        return image.size


def choose_samples(
    train_images: list[Path],
    val_images: list[Path],
    samples_per_class: int,
    train_per_class: int,
    val_per_class: int,
) -> list[tuple[str, Path]]:
    selected: list[tuple[str, Path]] = []
    selected.extend(("train", path) for path in train_images[:train_per_class])
    selected.extend(("val", path) for path in val_images[:val_per_class])
    seen = {path for _, path in selected}
    remainder = [("train", path) for path in train_images[train_per_class:]] + [("val", path) for path in val_images[val_per_class:]]
    for split, path in sorted(remainder, key=lambda item: str(item[1])):
        if len(selected) >= samples_per_class:
            break
        if path not in seen:
            selected.append((split, path))
            seen.add(path)
    return selected[:samples_per_class]


def write_classes(classes: list[str], output: Path) -> None:
    (output / "classes.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")


def write_data_template(classes: list[str], output: Path) -> None:
    lines = [
        "# 标注完成后再复制为正式 data.yaml；当前 labels/ 为空，不可直接训练。",
        "path: .",
        "train: images",
        "val: images",
        "names:",
    ]
    for idx, name in enumerate(classes):
        lines.append(f"  {idx}: {name}")
    (output / "data_template.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(samples: list[AnnotationSample], output: Path) -> None:
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(samples[0]).keys()) if samples else [])
        writer.writeheader()
        for sample in samples:
            writer.writerow(asdict(sample))


def write_guide(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 中药饮片检测 bbox 标注准备包",
        "",
        f"- 来源数据: `{report['source']}`",
        f"- 输出目录: `{report['output']}`",
        f"- 待标注图片: {summary['images']}",
        f"- 覆盖类别: {summary['classes']}",
        f"- 每类抽样: {summary['samples_per_class']} 张，默认 train {summary['train_per_class']} + val {summary['val_per_class']}",
        "",
        "## 目录说明",
        "",
        "- `images/`: 待人工标注图片。",
        "- `labels/`: YOLO `.txt` 标签输出目录；当前为空，标注完成后每张图应有同名 `.txt`。",
        "- `classes.txt`: 类别顺序，标注工具中必须保持该顺序。",
        "- `data_template.yaml`: 标注完成后的 YOLO 数据配置模板；当前不可直接用于训练。",
        "- `annotation_manifest.csv/json`: 每张图的来源、类别、尺寸、SHA256 和预期标签文件。",
        "",
        "## 标注规则",
        "",
        "- 只标注图中主要中药饮片目标，不标注背景、容器、手、标签纸、水印或文字。",
        "- bbox 应尽量贴合可见药材区域；如果同图中有多个明显分离的同类主体，应分别标注。",
        "- 若图像是散落饮片且个体边界不可稳定分离，可框选主要可见药材团簇的最小外接矩形。",
        "- 类别必须使用 `classes.txt` 中的 class index；不要按拼音、文件名或标注工具默认顺序重新排序。",
        "- 质量不清、遮挡严重或类别疑似错误的图片，应在 manifest 中保留备注并提交复核，不要强行标注。",
        "",
        "## LabelImg 建议流程",
        "",
        "```powershell",
        "labelImg images classes.txt",
        "```",
        "",
        "1. 将保存格式设为 YOLO。",
        "2. 将输出目录设为 `labels/`。",
        "3. 每张图片保存同名 `.txt` 标签文件。",
        "4. 完成后运行项目的数据校验脚本，再划分 train/val/test 并训练检测模型。",
        "",
        "## 当前边界",
        "",
        "- 本包只是人工标注准备包，尚未包含真实 bbox。",
        "- 不应把空 `labels/` 目录用于训练，也不应据此汇报检测 mAP、Precision 或 Recall。",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 检测 bbox 标注准备包报告",
        "",
        f"- 来源数据: `{report['source']}`",
        f"- 输出目录: `{report['output']}`",
        "",
        "## 总览",
        "",
        f"- 状态: `{summary['status']}`",
        f"- 类别数: {summary['classes']}",
        f"- 待标注图片: {summary['images']}",
        f"- 预期标签文件: {summary['labels_expected']}",
        f"- 已完成标签文件: {summary['labels_completed']}",
        f"- 每类样本数: min {summary['min_samples_per_class']} / max {summary['max_samples_per_class']}",
        f"- 来源划分: {summary['source_split_counts']}",
        "",
        "## 关键文件",
        "",
        f"- 标注说明: `{report['guide']}`",
        f"- 类别文件: `{report['classes_file']}`",
        f"- 数据模板: `{report['data_template']}`",
        f"- CSV manifest: `{report['manifest_csv']}`",
        f"- JSON manifest: `{report['manifest_json']}`",
        "",
        "## 抽样说明",
        "",
        f"- 每类最多 {summary['samples_per_class']} 张，优先选择 train {summary['train_per_class']} 张和 val {summary['val_per_class']} 张。",
        "- 本抽样用于标注启动和检测链路建设，后续正式训练可扩大到全量图片。",
        "",
        "## 边界说明",
        "",
        "- 当前没有真实 bbox 标签，不能训练检测模型或汇报检测指标。",
        "- 标注完成后需运行 YOLO 标签校验、划分数据集、训练检测模型并重新生成评估报告。",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_package(
    source: Path,
    output: Path,
    overwrite: bool,
    samples_per_class: int,
    train_per_class: int,
    val_per_class: int,
) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    if not source.exists():
        raise FileNotFoundError(f"source dataset not found: {source}")
    if output.exists() and overwrite:
        shutil.rmtree(output)
    images_dir = output / "images"
    labels_dir = output / "labels"
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    (labels_dir / "README.md").write_text(
        "# YOLO 标签输出目录\n\n当前目录应由人工标注工具生成 `.txt` 标签文件；空目录不可用于训练。\n",
        encoding="utf-8",
    )

    train_dirs = class_dirs(source, "train")
    val_dirs = class_dirs(source, "val")
    classes = sorted(set(train_dirs) | set(val_dirs))
    samples: list[AnnotationSample] = []
    per_class_counts: Counter[str] = Counter()
    split_counts: Counter[str] = Counter()

    for class_index, class_name in enumerate(classes):
        selected = choose_samples(
            train_images=image_files(train_dirs.get(class_name)),
            val_images=image_files(val_dirs.get(class_name)),
            samples_per_class=samples_per_class,
            train_per_class=train_per_class,
            val_per_class=val_per_class,
        )
        if len(selected) < samples_per_class:
            raise ValueError(f"class {class_name} has only {len(selected)} available images")
        for local_index, (source_split, source_image) in enumerate(selected, start=1):
            image_id = f"{class_index:03d}_{source_split}_{local_index:02d}_{source_image.stem}"
            target_image = images_dir / f"{image_id}.jpg"
            shutil.copy2(source_image, target_image)
            width, height = image_size(target_image)
            sample = AnnotationSample(
                image_id=image_id,
                class_index=class_index,
                class_name=class_name,
                source_split=source_split,
                source_path=str(source_image),
                package_image=str(target_image),
                yolo_label=str(labels_dir / f"{image_id}.txt"),
                width=width,
                height=height,
                sha256=sha256_file(target_image),
            )
            samples.append(sample)
            per_class_counts[class_name] += 1
            split_counts[source_split] += 1

    write_classes(classes, output)
    write_data_template(classes, output)
    manifest_csv = output / "annotation_manifest.csv"
    manifest_json = output / "annotation_manifest.json"
    write_csv(samples, manifest_csv)
    completed_labels = [Path(sample.yolo_label) for sample in samples if Path(sample.yolo_label).exists()]

    report = {
        "source": str(source),
        "output": str(output),
        "guide": str(output / "ANNOTATION_GUIDE.md"),
        "classes_file": str(output / "classes.txt"),
        "data_template": str(output / "data_template.yaml"),
        "manifest_csv": str(manifest_csv),
        "manifest_json": str(manifest_json),
        "summary": {
            "status": "pending_bbox_annotation",
            "classes": len(classes),
            "images": len(samples),
            "samples_per_class": samples_per_class,
            "train_per_class": train_per_class,
            "val_per_class": val_per_class,
            "labels_expected": len(samples),
            "labels_completed": len(completed_labels),
            "min_samples_per_class": min(per_class_counts.values()) if per_class_counts else 0,
            "max_samples_per_class": max(per_class_counts.values()) if per_class_counts else 0,
            "source_split_counts": dict(sorted(split_counts.items())),
        },
        "classes": classes,
        "per_class_counts": dict(sorted(per_class_counts.items())),
        "samples": [asdict(sample) for sample in samples],
        "boundary_note": "当前产物仅为真实 bbox 人工标注准备包，不含可训练检测标签。",
    }
    manifest_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_guide(report, output / "ANNOTATION_GUIDE.md")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a deterministic image package for manual YOLO bbox annotation.")
    parser.add_argument("--source", default=str(default_source()))
    parser.add_argument("--output", default="data/detection_annotation_package")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--samples-per-class", type=int, default=3)
    parser.add_argument("--train-per-class", type=int, default=2)
    parser.add_argument("--val-per-class", type=int, default=1)
    parser.add_argument("--report", default="reports/detection_annotation_package_report.json")
    parser.add_argument("--markdown", default="reports/detection_annotation_package_report.md")
    args = parser.parse_args()

    report = build_package(
        source=resolve_project_path(args.source),
        output=resolve_project_path(args.output),
        overwrite=args.overwrite,
        samples_per_class=args.samples_per_class,
        train_per_class=args.train_per_class,
        val_per_class=args.val_per_class,
    )
    report_path = resolve_project_path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, resolve_project_path(args.markdown))
    write_markdown(report, resolve_project_path(args.output) / "annotation_summary.md")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
