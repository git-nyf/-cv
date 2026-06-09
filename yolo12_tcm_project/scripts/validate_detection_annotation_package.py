from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from path_utils import resolve_project_path


@dataclass
class PackageIssue:
    level: str
    file: str
    message: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_classes(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_yolo_label(path: Path, class_count: int, expected_class: int, issues: list[PackageIssue]) -> int:
    boxes = 0
    seen: set[str] = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line in seen:
            issues.append(PackageIssue("warning", str(path), f"重复标注行: line {lineno}"))
        seen.add(line)
        parts = line.split()
        if len(parts) != 5:
            issues.append(PackageIssue("error", str(path), f"YOLO 标注应为 5 个字段: line {lineno}"))
            continue
        try:
            cls = int(float(parts[0]))
            x, y, w, h = map(float, parts[1:])
        except ValueError:
            issues.append(PackageIssue("error", str(path), f"标注无法解析为数字: line {lineno}"))
            continue
        if cls < 0 or cls >= class_count:
            issues.append(PackageIssue("error", str(path), f"类别编号越界: line {lineno}, class={cls}"))
        if cls != expected_class:
            issues.append(PackageIssue("error", str(path), f"类别编号与 manifest 不一致: line {lineno}, expected={expected_class}, actual={cls}"))
        if not all(0.0 <= value <= 1.0 for value in (x, y, w, h)):
            issues.append(PackageIssue("error", str(path), f"bbox 未归一化到 0~1: line {lineno}"))
        if w <= 0 or h <= 0:
            issues.append(PackageIssue("error", str(path), f"bbox 宽高必须为正: line {lineno}"))
        if x - w / 2 < 0 or x + w / 2 > 1 or y - h / 2 < 0 or y + h / 2 > 1:
            issues.append(PackageIssue("warning", str(path), f"bbox 超出图片边界: line {lineno}"))
        boxes += 1
    return boxes


def validate_package(package_dir: Path, require_complete: bool = False) -> dict[str, Any]:
    package_dir = package_dir.resolve()
    images_dir = package_dir / "images"
    labels_dir = package_dir / "labels"
    classes_file = package_dir / "classes.txt"
    manifest_file = package_dir / "annotation_manifest.json"
    issues: list[PackageIssue] = []

    for required in [images_dir, labels_dir, classes_file, manifest_file]:
        if not required.exists():
            issues.append(PackageIssue("error", str(required), "必要路径不存在"))

    classes = load_classes(classes_file)
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8")) if manifest_file.exists() else {}
    except json.JSONDecodeError as exc:
        manifest = {}
        issues.append(PackageIssue("error", str(manifest_file), f"manifest JSON 无法解析: {exc}"))

    manifest_classes = manifest.get("classes", []) if isinstance(manifest.get("classes", []), list) else []
    if classes and manifest_classes and classes != manifest_classes:
        issues.append(PackageIssue("error", str(classes_file), "classes.txt 与 annotation_manifest.json 的类别顺序不一致"))

    samples = manifest.get("samples", []) if isinstance(manifest.get("samples", []), list) else []
    image_files = sorted(images_dir.glob("*.jpg")) if images_dir.exists() else []
    image_by_name = {path.name: path for path in image_files}
    expected_images = {Path(sample.get("package_image", "")).name for sample in samples}
    missing_images: list[str] = []
    missing_labels: list[str] = []
    completed_labels = 0
    empty_labels = 0
    boxes = 0
    boxes_by_class: Counter[int] = Counter()

    for sample in samples:
        image_name = Path(sample.get("package_image", "")).name
        image_path = image_by_name.get(image_name)
        label_path = Path(sample.get("yolo_label", ""))
        if not label_path.is_absolute():
            label_path = package_dir / label_path
        expected_class = int(sample.get("class_index", -1))
        if image_path is None:
            missing_images.append(image_name)
            issues.append(PackageIssue("error", str(package_dir / "images" / image_name), "manifest 图片不存在"))
            continue
        try:
            with Image.open(image_path) as image:
                width, height = image.size
            if int(sample.get("width", -1)) != width or int(sample.get("height", -1)) != height:
                issues.append(PackageIssue("error", str(image_path), f"图片尺寸与 manifest 不一致: manifest={sample.get('width')}x{sample.get('height')}, actual={width}x{height}"))
        except Exception as exc:
            issues.append(PackageIssue("error", str(image_path), f"图片无法读取: {exc}"))
            continue
        expected_hash = sample.get("sha256")
        if expected_hash and sha256_file(image_path) != expected_hash:
            issues.append(PackageIssue("error", str(image_path), "图片 SHA256 与 manifest 不一致"))

        if not label_path.exists():
            missing_labels.append(str(label_path))
            if require_complete:
                issues.append(PackageIssue("error", str(label_path), "缺少对应 YOLO 标签文件"))
            continue

        completed_labels += 1
        current_boxes = parse_yolo_label(label_path, len(classes), expected_class, issues)
        if current_boxes == 0:
            empty_labels += 1
            level = "error" if require_complete else "warning"
            issues.append(PackageIssue(level, str(label_path), "标签文件为空"))
        boxes += current_boxes
        boxes_by_class[expected_class] += current_boxes

    extra_images = sorted(set(image_by_name) - expected_images)
    for image_name in extra_images:
        issues.append(PackageIssue("warning", str(images_dir / image_name), "images/ 中存在 manifest 外图片"))

    orphan_labels: list[str] = []
    if labels_dir.exists():
        for label in sorted(labels_dir.glob("*.txt")):
            expected_image = label.with_suffix(".jpg").name
            if expected_image not in image_by_name:
                orphan_labels.append(str(label))
                issues.append(PackageIssue("warning", str(label), "labels/ 中存在没有对应图片的标签文件"))

    status = "complete" if completed_labels == len(samples) and not missing_labels and not any(issue.level == "error" for issue in issues) else "pending_bbox_annotation"
    if require_complete and status != "complete":
        status = "incomplete_or_invalid"

    return {
        "summary": {
            "status": status,
            "require_complete": require_complete,
            "classes": len(classes),
            "manifest_classes": len(manifest_classes),
            "images_expected": len(samples),
            "images_present": len(image_files),
            "missing_images": len(missing_images),
            "labels_expected": len(samples),
            "labels_completed": completed_labels,
            "labels_missing": len(missing_labels),
            "labels_empty": empty_labels,
            "orphan_labels": len(orphan_labels),
            "boxes": boxes,
            "classes_with_boxes": len(boxes_by_class),
            "errors": sum(1 for issue in issues if issue.level == "error"),
            "warnings": sum(1 for issue in issues if issue.level == "warning"),
        },
        "package_dir": str(package_dir),
        "classes": {idx: name for idx, name in enumerate(classes)},
        "boxes_by_class": dict(sorted(boxes_by_class.items())),
        "missing_label_examples": missing_labels[:20],
        "issues": [asdict(issue) for issue in issues],
        "boundary_note": "pending_bbox_annotation 表示标注准备包结构有效但 labels/ 尚未补齐；只有 require_complete=true 且 status=complete 后才可进入检测训练。",
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 检测标注准备包校验报告",
        "",
        f"- 包目录: `{report['package_dir']}`",
        f"- 状态: `{summary['status']}`",
        f"- 严格完成模式: {summary['require_complete']}",
        "",
        "## 总览",
        "",
        f"- 类别数: {summary['classes']}",
        f"- manifest 图片数: {summary['images_expected']}",
        f"- 实际图片数: {summary['images_present']}",
        f"- 预期标签: {summary['labels_expected']}",
        f"- 已完成标签: {summary['labels_completed']}",
        f"- 缺失标签: {summary['labels_missing']}",
        f"- 空标签: {summary['labels_empty']}",
        f"- 有效 bbox 数: {summary['boxes']}",
        f"- 含 bbox 类别数: {summary['classes_with_boxes']}",
        f"- errors / warnings: {summary['errors']} / {summary['warnings']}",
        "",
        "## 当前结论",
        "",
    ]
    if summary["status"] == "complete":
        lines.append("- 标注文件已补齐且通过基础 YOLO 格式校验，可进入后续划分、训练和评估。")
    elif summary["status"] == "pending_bbox_annotation":
        lines.append("- 当前仍是待人工标注状态；结构和 manifest 可用于标注启动，但不能直接训练检测模型。")
    else:
        lines.append("- 当前未达到完整检测标注验收要求，需要先修复 errors 或补齐缺失标签。")
    lines.extend(
        [
            "",
            "## 缺失标签示例",
            "",
        ]
    )
    if report["missing_label_examples"]:
        for item in report["missing_label_examples"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- 无")
    lines.extend(["", "## 问题列表", ""])
    if report["issues"]:
        for issue in report["issues"][:200]:
            lines.append(f"- [{issue['level']}] `{issue['file']}`: {issue['message']}")
    else:
        lines.append("- 未发现结构或已有标签格式问题")
    lines.extend(["", "## 边界说明", "", f"- {report['boundary_note']}"])
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the manual YOLO bbox annotation package.")
    parser.add_argument("--package", default="data/detection_annotation_package", help="Annotation package directory")
    parser.add_argument("--require-complete", action="store_true", help="Fail when any expected label is missing or empty")
    parser.add_argument("--output", default="reports/detection_annotation_package_validation.json")
    parser.add_argument("--markdown", default="reports/detection_annotation_package_validation.md")
    args = parser.parse_args()

    report = validate_package(resolve_project_path(args.package), require_complete=args.require_complete)
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
