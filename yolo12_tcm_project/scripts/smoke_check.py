from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> tuple[Path, object]:
    target = ROOT / path
    return target, json.loads(target.read_text(encoding="utf-8"))


def check_exists(path: str) -> dict:
    target = ROOT / path
    return {"name": f"exists:{path}", "passed": target.exists(), "detail": str(target)}


def check_file_size(path: str, min_bytes: int) -> dict:
    target = ROOT / path
    size = target.stat().st_size if target.exists() else 0
    return {
        "name": f"file_size:{path}",
        "passed": size >= min_bytes,
        "detail": f"bytes={size}, min={min_bytes}",
    }


def check_python_deps() -> list[dict]:
    deps = ["PIL", "yaml", "fastapi", "uvicorn", "ultralytics", "torch", "pytest", "docx", "playwright"]
    return [
        {
            "name": f"python_dep:{dep}",
            "passed": importlib.util.find_spec(dep) is not None,
            "detail": "installed" if importlib.util.find_spec(dep) is not None else "missing",
        }
        for dep in deps
    ]


def check_pptx(path: str) -> dict:
    target = ROOT / path
    if not target.exists():
        return {"name": f"pptx:{path}", "passed": False, "detail": "missing"}
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    with zipfile.ZipFile(target) as z:
        slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        text = []
        for slide in slides:
            root = ET.fromstring(z.read(slide))
            text.extend((t.text or "") for t in root.findall(".//a:t", ns))
    joined = "\n".join(text)
    required = [
        "YOLOv12",
        "GhostC2f",
        "CHDPL-Net",
        "DGS-YOLOv8",
        "误判分析",
        "人工复核",
        "类别一致性",
        "大腹皮",
        "可复现实验",
        "Manifest",
        "93 类补齐",
        "检测标注准备包",
        "重复/泄漏",
        "跨类别复核",
        "跨类别决策表",
    ]
    ok = len(slides) >= 8 and not any(x in joined.lower() for x in ["lorem", "ipsum", "placeholder", "xxxx"]) and all(x in joined for x in required)
    return {"name": f"pptx:{path}", "passed": ok, "detail": f"slides={len(slides)}, required_refs={all(x in joined for x in required)}"}


def check_docx_text(path: str, required: list[str]) -> dict:
    target = ROOT / path
    if not target.exists():
        return {"name": f"docx_text:{path}", "passed": False, "detail": "missing"}
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(target) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    joined = "".join((node.text or "") for node in root.findall(".//w:t", ns))
    missing = [item for item in required if item not in joined]
    return {"name": f"docx_text:{path}", "passed": not missing, "detail": f"missing={missing}"}


def check_json_summary(path: str, expected: dict) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {}) if isinstance(payload, dict) else {}
        mismatches = {key: {"expected": value, "actual": summary.get(key)} for key, value in expected.items() if summary.get(key) != value}
        return {
            "name": f"json_summary:{path}",
            "passed": not mismatches,
            "detail": f"summary={summary}, mismatches={mismatches}",
        }
    except Exception as exc:
        return {"name": f"json_summary:{path}", "passed": False, "detail": repr(exc)}


def check_strict_metrics(path: str) -> dict:
    expected = {
        "top1": 0.17690981924533844,
        "top5": 0.4956921339035034,
        "fitness": 0.33630097657442093,
    }
    try:
        _, payload = read_json(path)
        mismatches = {
            key: {"expected": value, "actual": payload.get(key)}
            for key, value in expected.items()
            if abs(float(payload.get(key, -1)) - value) > 1e-9
        }
        return {
            "name": f"strict_metrics:{path}",
            "passed": not mismatches,
            "detail": f"metrics={payload}, mismatches={mismatches}",
        }
    except Exception as exc:
        return {"name": f"strict_metrics:{path}", "passed": False, "detail": repr(exc)}


def check_93class_metrics(path: str) -> dict:
    expected = {
        "top1": 0.06647564470767975,
        "top5": 0.20859599113464355,
        "fitness": 0.13753581792116165,
    }
    try:
        _, payload = read_json(path)
        mismatches = {
            key: {"expected": value, "actual": payload.get(key)}
            for key, value in expected.items()
            if abs(float(payload.get(key, -1)) - value) > 1e-9
        }
        return {
            "name": f"93class_metrics:{path}",
            "passed": not mismatches,
            "detail": f"metrics={payload}, mismatches={mismatches}",
        }
    except Exception as exc:
        return {"name": f"93class_metrics:{path}", "passed": False, "detail": repr(exc)}


def check_93class_completion(path: str) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        distribution = payload.get("distribution", {})
        class_strategies = payload.get("class_strategies", [])
        dafu = next((item for item in class_strategies if item.get("class_name") == "大腹皮"), {})
        expected = {
            "status": "complete",
            "raw_classes": 93,
            "output_classes": 93,
            "train_images": 7841,
            "val_images": 1745,
            "total_images": 9586,
            "skipped_images": 28,
            "excluded_classes": [],
            "rebalanced_classes": ["大腹皮"],
            "val_only_rebalanced_classes": ["大腹皮"],
            "train_only_rebalanced_classes": [],
        }
        mismatches = {key: {"expected": value, "actual": summary.get(key)} for key, value in expected.items() if summary.get(key) != value}
        ok = (
            not mismatches
            and dafu.get("strategy") == "rebalance_val_only"
            and dafu.get("raw_train") == 0
            and dafu.get("raw_val") == 19
            and dafu.get("assigned_train") == 15
            and dafu.get("assigned_val") == 4
            and distribution.get("train", {}).get("大腹皮") == 15
            and distribution.get("val", {}).get("大腹皮") == 4
            and "补齐实验" in payload.get("boundary_note", "")
        )
        return {
            "name": f"93class_completion:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "mismatches": mismatches,
                "dafu": dafu,
                "distribution": {
                    "train": distribution.get("train", {}).get("大腹皮"),
                    "val": distribution.get("val", {}).get("大腹皮"),
                },
            },
        }
    except Exception as exc:
        return {"name": f"93class_completion:{path}", "passed": False, "detail": repr(exc)}


def check_strict_benchmark(path: str) -> dict:
    try:
        _, payload = read_json(path)
        ok = (
            payload.get("images") == 20
            and payload.get("device") == "cpu"
            and payload.get("imgsz") == 224
            and float(payload.get("latency_ms_mean", 0)) > 0
            and float(payload.get("fps_mean", 0)) > 0
        )
        detail = {
            "images": payload.get("images"),
            "device": payload.get("device"),
            "imgsz": payload.get("imgsz"),
            "latency_ms_mean": payload.get("latency_ms_mean"),
            "fps_mean": payload.get("fps_mean"),
        }
        return {"name": f"strict_benchmark:{path}", "passed": ok, "detail": detail}
    except Exception as exc:
        return {"name": f"strict_benchmark:{path}", "passed": False, "detail": repr(exc)}


def check_sample_prediction(path: str) -> dict:
    try:
        _, payload = read_json(path)
        results = payload.get("results", [])
        first = results[0] if results else {}
        predictions = first.get("predictions", [])
        ok = payload.get("topk") == 5 and first.get("expected_class") == "丝瓜络" and len(predictions) == 5
        detail = {
            "topk": payload.get("topk"),
            "expected_class": first.get("expected_class"),
            "top1_class_name": first.get("top1_class_name"),
            "predictions": len(predictions),
        }
        return {"name": f"sample_prediction:{path}", "passed": ok, "detail": detail}
    except Exception as exc:
        return {"name": f"sample_prediction:{path}", "passed": False, "detail": repr(exc)}


def check_error_analysis(path: str) -> dict:
    expected_top1 = 0.17690982194141297
    expected_top5 = 0.4956921309592188
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        ok = (
            summary.get("images") == 1741
            and summary.get("classes") == 92
            and summary.get("top1_correct") == 308
            and summary.get("top5_correct") == 863
            and abs(float(summary.get("top1_accuracy", -1)) - expected_top1) < 1e-9
            and abs(float(summary.get("top5_accuracy", -1)) - expected_top5) < 1e-9
            and len(payload.get("worst_classes", [])) > 0
            and len(payload.get("best_classes", [])) > 0
            and len(payload.get("confusion_pairs", [])) > 0
        )
        detail = {
            "summary": summary,
            "worst_first": (payload.get("worst_classes") or [{}])[0].get("class_name"),
            "best_first": (payload.get("best_classes") or [{}])[0].get("class_name"),
            "confusion_first": (payload.get("confusion_pairs") or [{}])[0],
        }
        return {"name": f"error_analysis:{path}", "passed": ok, "detail": detail}
    except Exception as exc:
        return {"name": f"error_analysis:{path}", "passed": False, "detail": repr(exc)}


def check_class_consistency(path: str) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        expected = {
            "status": "needs_class_completion",
            "raw_classes": 93,
            "raw_train_classes": 92,
            "raw_val_classes": 93,
            "strict_classes": 92,
            "classes_missing_from_strict": ["大腹皮"],
            "extra_classes_in_strict": [],
            "train_only_classes": [],
            "val_only_classes": ["大腹皮"],
            "zero_train_classes": ["大腹皮"],
            "zero_val_classes": [],
            "raw_train_images": 7847,
            "raw_val_images": 1767,
            "raw_total_images": 9614,
            "strict_train_images": 7826,
            "strict_val_images": 1741,
            "strict_total_images": 9567,
            "strict_verified_images": 9567,
            "strict_errors": 0,
            "strict_warnings": 0,
            "skipped_images": 28,
            "converted_to_jpeg": 122,
            "copied_jpeg": 9445,
        }
        mismatches = {key: {"expected": value, "actual": summary.get(key)} for key, value in expected.items() if summary.get(key) != value}
        skipped = payload.get("skipped_by_class", {})
        per_class = payload.get("per_class", [])
        dafu = next((item for item in per_class if item.get("class_name") == "大腹皮"), {})
        ok = (
            not mismatches
            and dafu.get("raw_train") == 0
            and dafu.get("raw_val") == 19
            and dafu.get("included_in_strict") is False
            and len(skipped) >= 20
            and "冬虫夏草" in skipped
            and len(payload.get("recommended_actions", [])) >= 2
        )
        detail = {
            "summary": summary,
            "mismatches": mismatches,
            "dafu": dafu,
            "skipped_classes": len(skipped),
        }
        return {"name": f"class_consistency:{path}", "passed": ok, "detail": detail}
    except Exception as exc:
        return {"name": f"class_consistency:{path}", "passed": False, "detail": repr(exc)}


def check_detection_annotation_package(report_path: str) -> dict:
    try:
        _, report = read_json(report_path)
        summary = report.get("summary", {})
        package_root = ROOT / "data" / "detection_annotation_package"
        images_dir = package_root / "images"
        labels_dir = package_root / "labels"
        classes_file = package_root / "classes.txt"
        manifest_json = package_root / "annotation_manifest.json"
        data_template = package_root / "data_template.yaml"
        guide = package_root / "ANNOTATION_GUIDE.md"
        labels_readme = labels_dir / "README.md"

        classes = classes_file.read_text(encoding="utf-8").splitlines() if classes_file.exists() else []
        images = sorted(images_dir.glob("*.jpg")) if images_dir.exists() else []
        label_txts = sorted(labels_dir.glob("*.txt")) if labels_dir.exists() else []
        manifest = json.loads(manifest_json.read_text(encoding="utf-8")) if manifest_json.exists() else {}
        per_class_counts = manifest.get("per_class_counts", {})
        manifest_samples = manifest.get("samples", [])
        template_text = data_template.read_text(encoding="utf-8") if data_template.exists() else ""
        guide_text = guide.read_text(encoding="utf-8") if guide.exists() else ""

        ok = (
            summary.get("status") == "pending_bbox_annotation"
            and summary.get("classes") == 93
            and summary.get("images") == 279
            and summary.get("labels_expected") == 279
            and summary.get("labels_completed") == 0
            and summary.get("min_samples_per_class") == 3
            and summary.get("max_samples_per_class") == 3
            and summary.get("source_split_counts") == {"train": 186, "val": 93}
            and len(classes) == 93
            and "大腹皮" in classes
            and len(images) == 279
            and len(label_txts) == 0
            and labels_readme.exists()
            and len(per_class_counts) == 93
            and all(count == 3 for count in per_class_counts.values())
            and len(manifest_samples) == 279
            and "当前 labels/ 为空" in template_text
            and "尚未包含真实 bbox" in guide_text
        )
        return {
            "name": f"detection_annotation_package:{report_path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "classes_file_lines": len(classes),
                "images": len(images),
                "label_txts": len(label_txts),
                "manifest_samples": len(manifest_samples),
                "per_class_counts": len(per_class_counts),
            },
        }
    except Exception as exc:
        return {"name": f"detection_annotation_package:{report_path}", "passed": False, "detail": repr(exc)}


def check_detection_annotation_validation(path: str) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        issues = payload.get("issues", [])
        ok = (
            summary.get("status") == "pending_bbox_annotation"
            and summary.get("require_complete") is False
            and summary.get("classes") == 93
            and summary.get("manifest_classes") == 93
            and summary.get("images_expected") == 279
            and summary.get("images_present") == 279
            and summary.get("missing_images") == 0
            and summary.get("labels_expected") == 279
            and summary.get("labels_completed") == 0
            and summary.get("labels_missing") == 279
            and summary.get("labels_empty") == 0
            and summary.get("orphan_labels") == 0
            and summary.get("boxes") == 0
            and summary.get("classes_with_boxes") == 0
            and summary.get("errors") == 0
            and summary.get("warnings") == 0
            and len(issues) == 0
            and "pending_bbox_annotation" in payload.get("boundary_note", "")
        )
        return {"name": f"detection_annotation_validation:{path}", "passed": ok, "detail": summary}
    except Exception as exc:
        return {"name": f"detection_annotation_validation:{path}", "passed": False, "detail": repr(exc)}


def check_detection_annotation_contact_sheet(path: str) -> dict:
    try:
        target, payload = read_json(path)
        summary = payload.get("summary", {})
        samples = payload.get("samples", [])
        figure = Path(payload.get("figure", ""))
        figure_path = figure if figure.is_absolute() else ROOT / figure
        markdown_path = target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""

        with Image.open(figure_path) as image:
            width, height = image.size

        class_counts: dict[int, int] = {}
        image_paths_ok = True
        label_paths_ok = True
        source_split_counts = {"train": 0, "val": 0}
        for sample in samples:
            class_index = int(sample.get("class_index", -1))
            class_counts[class_index] = class_counts.get(class_index, 0) + 1
            image_paths_ok = image_paths_ok and Path(sample.get("package_image", "")).exists()
            label_path = Path(sample.get("yolo_label", ""))
            label_paths_ok = label_paths_ok and label_path.parent.name == "labels" and label_path.suffix == ".txt"
            split = sample.get("source_split")
            if split in source_split_counts:
                source_split_counts[split] += 1

        ok = (
            target.name == "detection_annotation_contact_sheet.json"
            and summary.get("samples") == 279
            and summary.get("classes") == 93
            and summary.get("labels_expected") == 279
            and summary.get("labels_completed") == 0
            and summary.get("annotation_status") == "pending_bbox_annotation"
            and len(samples) == 279
            and len(class_counts) == 93
            and all(count == 3 for count in class_counts.values())
            and source_split_counts == {"train": 186, "val": 93}
            and image_paths_ok
            and label_paths_ok
            and figure_path.exists()
            and figure_path.stat().st_size > 1_000_000
            and width >= 1200
            and height >= 6000
            and "样本总数: 279" in markdown_text
            and "类别数: 93" in markdown_text
            and "不是检测训练数据" in markdown_text
        )
        return {
            "name": f"detection_annotation_contact_sheet:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "samples": len(samples),
                "classes": len(class_counts),
                "source_split_counts": source_split_counts,
                "figure": str(figure_path),
                "figure_size": [width, height],
                "figure_bytes": figure_path.stat().st_size if figure_path.exists() else 0,
                "markdown": str(markdown_path),
                "image_paths_ok": image_paths_ok,
                "label_paths_ok": label_paths_ok,
            },
        }
    except Exception as exc:
        return {"name": f"detection_annotation_contact_sheet:{path}", "passed": False, "detail": repr(exc)}


def check_duplicate_audit(path: str, expected: dict) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        groups = payload.get("duplicate_groups", [])
        mismatches = {key: {"expected": value, "actual": summary.get(key)} for key, value in expected.items() if summary.get(key) != value}
        ok = (
            not mismatches
            and summary.get("status") == "needs_leakage_review"
            and summary.get("train_val_leak_hashes") == 34
            and summary.get("cross_class_duplicate_hashes") == 52
            and len(groups) == summary.get("reported_groups")
            and any(group.get("train_val_leak") for group in groups)
            and "SHA256 完全重复" in payload.get("boundary_note", "")
            and len(payload.get("recommended_actions", [])) >= 3
        )
        return {
            "name": f"duplicate_audit:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "mismatches": mismatches,
                "first_group": groups[0] if groups else {},
            },
        }
    except Exception as exc:
        return {"name": f"duplicate_audit:{path}", "passed": False, "detail": repr(exc)}


def check_classification_leakage_review_package(path: str) -> dict:
    try:
        target, payload = read_json(path)
        summary = payload.get("summary", {})
        groups = payload.get("groups", [])
        figure = Path(summary.get("figure", ""))
        figure_path = figure if figure.is_absolute() else ROOT / figure
        markdown_path = target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""

        with Image.open(figure_path) as image:
            width, height = image.size

        records = [record for group in groups for record in group.get("records", [])]
        record_paths_ok = all(Path(record.get("path", "")).exists() for record in records)
        group_ids_ok = [group.get("group_id") for group in groups] == [f"leak_{index:03d}" for index in range(1, 35)]
        manual_decision_ok = all(group.get("manual_decision") == "" for group in groups)
        risk_levels = {group.get("risk_level") for group in groups}
        ok = (
            target.name == "classification_leakage_review_package.json"
            and summary.get("status") == "complete_review_package"
            and summary.get("source_audit_status") == "needs_leakage_review"
            and summary.get("leakage_groups") == 34
            and summary.get("expected_leakage_groups") == 34
            and summary.get("leakage_records") == 69
            and summary.get("train_records") == 35
            and summary.get("val_records") == 34
            and summary.get("same_class_leakage_groups") == 16
            and summary.get("cross_class_leakage_groups") == 18
            and summary.get("classes_involved") == 27
            and summary.get("shared_with_reference_leak_hashes") == 34
            and len(groups) == 34
            and len(records) == 69
            and group_ids_ok
            and manual_decision_ok
            and risk_levels == {"high_label_and_split_leak", "split_leak"}
            and record_paths_ok
            and figure_path.exists()
            and figure_path.stat().st_size > 1_000_000
            and width >= 1000
            and height >= 7000
            and "train/val 泄漏组: 34 / 34" in markdown_text
            and "manual_decision" in markdown_text
            and "不自动删除、移动或重划任何图片" in markdown_text
        )
        return {
            "name": f"classification_leakage_review_package:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "groups": len(groups),
                "records": len(records),
                "risk_levels": sorted(risk_levels),
                "record_paths_ok": record_paths_ok,
                "group_ids_ok": group_ids_ok,
                "manual_decision_ok": manual_decision_ok,
                "figure": str(figure_path),
                "figure_size": [width, height],
                "figure_bytes": figure_path.stat().st_size if figure_path.exists() else 0,
                "markdown": str(markdown_path),
            },
        }
    except Exception as exc:
        return {"name": f"classification_leakage_review_package:{path}", "passed": False, "detail": repr(exc)}


def check_leakage_clean_candidate(report_path: str, inspection_path: str, duplicate_path: str, expected: dict) -> dict:
    try:
        report_target, report = read_json(report_path)
        _, inspection = read_json(inspection_path)
        _, duplicates = read_json(duplicate_path)
        report_summary = report.get("summary", {})
        inspection_summary = inspection.get("summary", {})
        duplicate_summary = duplicates.get("summary", {})
        markdown_path = report_target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
        output_path = Path(report.get("output", ""))
        output_exists = output_path.exists()
        removed_records = report.get("removed_records", [])
        removed_paths_absent = all(not (output_path / record.get("relative_path", "")).exists() for record in removed_records)
        mismatches = {
            "report": {
                key: {"expected": value, "actual": report_summary.get(key)}
                for key, value in expected.get("report", {}).items()
                if report_summary.get(key) != value
            },
            "inspection": {
                key: {"expected": value, "actual": inspection_summary.get(key)}
                for key, value in expected.get("inspection", {}).items()
                if inspection_summary.get(key) != value
            },
            "duplicate": {
                key: {"expected": value, "actual": duplicate_summary.get(key)}
                for key, value in expected.get("duplicate", {}).items()
                if duplicate_summary.get(key) != value
            },
        }
        ok = (
            output_exists
            and removed_paths_absent
            and not mismatches["report"]
            and not mismatches["inspection"]
            and not mismatches["duplicate"]
            and len(removed_records) == expected.get("removed_records")
            and "本候选数据集只移除人工复核包中列出的 val 侧" in report.get("boundary_note", "")
            and "不自动裁决跨类别标签" in report.get("boundary_note", "")
            and "已移除 val 副本" in markdown_text
        )
        return {
            "name": f"leakage_clean_candidate:{report_path}",
            "passed": ok,
            "detail": {
                "report": report_summary,
                "inspection": inspection_summary,
                "duplicate": duplicate_summary,
                "mismatches": mismatches,
                "output": str(output_path),
                "output_exists": output_exists,
                "removed_records": len(removed_records),
                "removed_paths_absent": removed_paths_absent,
                "markdown": str(markdown_path),
            },
        }
    except Exception as exc:
        return {"name": f"leakage_clean_candidate:{report_path}", "passed": False, "detail": repr(exc)}


def check_cross_class_review_package(path: str) -> dict:
    try:
        target, payload = read_json(path)
        summary = payload.get("summary", {})
        groups = payload.get("groups", [])
        figure = Path(summary.get("figure", ""))
        figure_path = figure if figure.is_absolute() else ROOT / figure
        markdown_path = target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
        with Image.open(figure_path) as image:
            width, height = image.size
        records = [record for group in groups for record in group.get("records", [])]
        record_paths_ok = all(Path(record.get("path", "")).exists() for record in records)
        manual_decision_ok = all(group.get("manual_decision") == "" for group in groups)
        group_ids_ok = [group.get("group_id") for group in groups] == [f"cross_class_{index:03d}" for index in range(1, 35)]
        risk_levels = {group.get("risk_level") for group in groups}
        ok = (
            summary.get("status") == "complete_review_package"
            and summary.get("source_audit_status") == "needs_leakage_review"
            and summary.get("cross_class_groups") == 34
            and summary.get("expected_cross_class_groups") == 34
            and summary.get("cross_class_records") == 68
            and summary.get("train_records") == 62
            and summary.get("val_records") == 6
            and summary.get("cross_split_groups") == 0
            and summary.get("train_val_leak_groups") == 0
            and summary.get("classes_involved") == 22
            and summary.get("shared_with_reference_cross_class_hashes") == 34
            and len(groups) == 34
            and len(records) == 68
            and group_ids_ok
            and manual_decision_ok
            and risk_levels == {"label_conflict"}
            and record_paths_ok
            and figure_path.exists()
            and figure_path.stat().st_size > 1_000_000
            and width >= 800
            and height >= 7000
            and "跨类别重复组: 34 / 34" in markdown_text
            and "manual_decision" in markdown_text
            and "不自动删除、移动、重命名或重标任何图片" in payload.get("boundary_note", "")
        )
        return {
            "name": f"cross_class_review_package:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "groups": len(groups),
                "records": len(records),
                "risk_levels": sorted(risk_levels),
                "record_paths_ok": record_paths_ok,
                "group_ids_ok": group_ids_ok,
                "manual_decision_ok": manual_decision_ok,
                "figure": str(figure_path),
                "figure_size": [width, height],
                "figure_bytes": figure_path.stat().st_size if figure_path.exists() else 0,
                "markdown": str(markdown_path),
            },
        }
    except Exception as exc:
        return {"name": f"cross_class_review_package:{path}", "passed": False, "detail": repr(exc)}


def check_cross_class_decision_table(path: str) -> dict:
    try:
        target, payload = read_json(path)
        summary = payload.get("summary", {})
        decisions = payload.get("decisions", [])
        csv_path = target.with_suffix(".csv")
        markdown_path = target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
        statuses = {decision.get("decision_status") for decision in decisions}
        group_ids_ok = [decision.get("group_id") for decision in decisions] == [f"cross_class_{index:03d}" for index in range(1, 35)]
        manual_fields = set(payload.get("manual_fields", []))
        required_manual = {
            "decision_status",
            "chosen_class",
            "action",
            "remove_relative_paths",
            "move_to_class",
            "reviewer",
            "reviewed_at",
            "decision_note",
        }
        record_paths_ok = all(len(decision.get("record_relative_paths", [])) == 2 for decision in decisions)
        allowed_actions_ok = "keep_chosen_class_remove_others" in payload.get("allowed_actions", [])
        csv_header = csv_path.read_text(encoding="utf-8-sig").splitlines()[0] if csv_path.exists() else ""
        ok = (
            payload.get("schema_version") == 1
            and summary.get("status") == "ready_for_manual_decision"
            and summary.get("source_review_status") == "complete_review_package"
            and summary.get("groups") == 34
            and summary.get("records") == 68
            and summary.get("pending_decisions") == 34
            and summary.get("decided_groups") == 0
            and summary.get("needs_expert_review_groups") == 0
            and summary.get("deferred_groups") == 0
            and summary.get("validation_errors") == 0
            and len(decisions) == 34
            and statuses == {"pending"}
            and group_ids_ok
            and record_paths_ok
            and required_manual.issubset(manual_fields)
            and allowed_actions_ok
            and csv_path.exists()
            and csv_path.stat().st_size > 5_000
            and "decision_status" in csv_header
            and "remove_relative_paths" in csv_header
            and markdown_path.exists()
            and "待决策组: 34 / 34" in markdown_text
            and "不自动删除、移动、重命名、重标或复制任何图片" in payload.get("boundary_note", "")
        )
        return {
            "name": f"cross_class_decision_table:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "decisions": len(decisions),
                "statuses": sorted(statuses),
                "group_ids_ok": group_ids_ok,
                "record_paths_ok": record_paths_ok,
                "csv": str(csv_path),
                "markdown": str(markdown_path),
            },
        }
    except Exception as exc:
        return {"name": f"cross_class_decision_table:{path}", "passed": False, "detail": repr(exc)}


def check_cross_class_decision_review_html(path: str) -> dict:
    target = ROOT / path
    try:
        text = target.read_text(encoding="utf-8")
        group_cards = text.count('<article class="group-card"')
        image_refs = text.count("<img ")
        ok = (
            target.exists()
            and target.stat().st_size > 100_000
            and group_cards == 34
            and image_refs == 68
            and "cross_class_001" in text
            and "cross_class_034" in text
            and 'data-field="decision_status"' in text
            and 'data-field="chosen_class"' in text
            and 'data-copy-row' in text
            and 'data-copy-remove' in text
            and "只辅助人工填写，不自动修改 CSV 或数据集" in text
            and "data/classification_strict_jpeg_leakage_clean_candidate/" in text
        )
        return {
            "name": f"cross_class_decision_review_html:{path}",
            "passed": ok,
            "detail": {
                "bytes": target.stat().st_size if target.exists() else 0,
                "group_cards": group_cards,
                "image_refs": image_refs,
            },
        }
    except Exception as exc:
        return {"name": f"cross_class_decision_review_html:{path}", "passed": False, "detail": repr(exc)}


def check_cross_class_cleanup_plan(path: str) -> dict:
    try:
        target, payload = read_json(path)
        summary = payload.get("summary", {})
        operations = payload.get("operations", [])
        operations_csv = target.with_suffix(".csv")
        markdown_path = target.with_suffix(".md")
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
        csv_header = operations_csv.read_text(encoding="utf-8-sig").splitlines()[0] if operations_csv.exists() else ""
        ok = (
            payload.get("schema_version") == 1
            and summary.get("status") == "waiting_for_manual_decisions"
            and summary.get("groups") == 34
            and summary.get("records") == 68
            and summary.get("pending_decisions") == 34
            and summary.get("decided_groups") == 0
            and summary.get("needs_expert_review_groups") == 0
            and summary.get("deferred_groups") == 0
            and summary.get("validation_errors") == 0
            and summary.get("planned_operations") == 0
            and summary.get("planned_remove_operations") == 0
            and summary.get("planned_move_operations") == 0
            and summary.get("keep_all_as_is_groups") == 0
            and payload.get("action_counts") == {"unset": 34}
            and operations == []
            and payload.get("validation_errors") == []
            and operations_csv.exists()
            and "operation" in csv_header
            and "target_relative_path" in csv_header
            and markdown_path.exists()
            and "状态: `waiting_for_manual_decisions`" in markdown_text
            and "待决策组: 34 / 34" in markdown_text
            and "当前没有可执行操作" in markdown_text
            and "不会删除、移动、重命名、重标或复制任何图片" in payload.get("boundary_note", "")
            and any("ready_for_cleanup_execution" in step for step in payload.get("recommended_next_steps", []))
        )
        return {
            "name": f"cross_class_cleanup_plan:{path}",
            "passed": ok,
            "detail": {
                "summary": summary,
                "operations": len(operations),
                "operations_csv": str(operations_csv),
                "markdown": str(markdown_path),
            },
        }
    except Exception as exc:
        return {"name": f"cross_class_cleanup_plan:{path}", "passed": False, "detail": repr(exc)}


def check_pending_cleanup_execution_blocked() -> dict:
    output = ROOT / "data" / "_smoke_blocked_cleanup_output"
    report = ROOT / "reports" / "_smoke_blocked_cleanup_execution_report.json"
    markdown = ROOT / "reports" / "_smoke_blocked_cleanup_execution_report.md"

    def remove_if_inside_root(path: Path) -> None:
        target = path.resolve()
        if target == ROOT or not target.is_relative_to(ROOT):
            raise ValueError(f"refusing to clean path outside project root: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    try:
        for target in (output, report, markdown):
            remove_if_inside_root(target)

        proc = subprocess.run(
            [
                sys.executable,
                "scripts/apply_classification_cross_class_cleanup_plan.py",
                "--source",
                "data/classification_strict_jpeg_leakage_clean_candidate",
                "--cleanup-plan",
                "reports/classification_cross_class_cleanup_plan.json",
                "--output",
                str(output.relative_to(ROOT)),
                "--report",
                str(report.relative_to(ROOT)),
                "--markdown",
                str(markdown.relative_to(ROOT)),
            ],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=120,
        )
        combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        ok = (
            proc.returncode != 0
            and "cleanup_execution_blocked" in combined
            and "ready_for_cleanup_execution" in combined
            and not output.exists()
            and not report.exists()
            and not markdown.exists()
        )
        return {
            "name": "cleanup_execution_blocked:pending_cross_class_plan",
            "passed": ok,
            "detail": {
                "returncode": proc.returncode,
                "output_exists": output.exists(),
                "report_exists": report.exists(),
                "markdown_exists": markdown.exists(),
                "message": combined[-1000:],
            },
        }
    except Exception as exc:
        return {"name": "cleanup_execution_blocked:pending_cross_class_plan", "passed": False, "detail": repr(exc)}
    finally:
        for target in (output, report, markdown):
            remove_if_inside_root(target)


def check_repro_manifest(path: str) -> dict:
    try:
        target, payload = read_json(path)
        artifacts = payload.get("artifacts", [])
        artifact_by_path = {item.get("path"): item for item in artifacts}
        required_artifacts = [
            "configs/train_cls_strict_cpu_5e.yaml",
            "configs/train_cls_93class_smoke.yaml",
            "scripts/prepare_detection_annotation_package.py",
            "scripts/audit_classification_duplicates.py",
            "scripts/generate_classification_leakage_review_package.py",
            "scripts/prepare_leakage_clean_classification_dataset.py",
            "scripts/generate_classification_cross_class_review_package.py",
            "scripts/generate_classification_cross_class_decision_table.py",
            "scripts/generate_classification_cross_class_decision_review_html.py",
            "scripts/generate_classification_cross_class_cleanup_plan.py",
            "scripts/apply_classification_cross_class_cleanup_plan.py",
            "reports/class_consistency_audit.json",
            "reports/strict_classification_duplicate_audit.json",
            "reports/strict_classification_duplicate_audit.md",
            "reports/classification_leakage_review_package.json",
            "reports/classification_leakage_review_package.md",
            "reports/figures/classification_train_val_leakage_contact_sheet.png",
            "reports/classification_leakage_clean_candidate_report.json",
            "reports/classification_leakage_clean_candidate_report.md",
            "reports/classification_leakage_clean_candidate_inspection.json",
            "reports/classification_leakage_clean_candidate_duplicate_audit.json",
            "reports/classification_cross_class_review_package.json",
            "reports/classification_cross_class_review_package.md",
            "reports/figures/classification_cross_class_contact_sheet.png",
            "reports/classification_cross_class_decision_table.json",
            "reports/classification_cross_class_decision_table.csv",
            "reports/classification_cross_class_decision_table.md",
            "reports/classification_cross_class_decision_review.html",
            "reports/classification_cross_class_cleanup_plan.json",
            "reports/classification_cross_class_cleanup_plan.csv",
            "reports/classification_cross_class_cleanup_plan.md",
            "reports/classification_93class_completion_report.json",
            "reports/classification_93class_dataset_inspection.json",
            "reports/classification_93class_duplicate_audit.json",
            "reports/classification_93class_duplicate_audit.md",
            "reports/classification_93class_leakage_clean_candidate_report.json",
            "reports/classification_93class_leakage_clean_candidate_report.md",
            "reports/classification_93class_leakage_clean_candidate_inspection.json",
            "reports/classification_93class_leakage_clean_candidate_duplicate_audit.json",
            "reports/classification_93class_evaluation_metrics.json",
            "reports/detection_annotation_package_report.json",
            "reports/detection_annotation_package_report.md",
            "reports/detection_annotation_package_validation.json",
            "reports/detection_annotation_package_validation.md",
            "reports/detection_annotation_contact_sheet.json",
            "reports/detection_annotation_contact_sheet.md",
            "reports/figures/detection_annotation_contact_sheet.png",
            "data/detection_annotation_package/ANNOTATION_GUIDE.md",
            "data/detection_annotation_package/classes.txt",
            "data/detection_annotation_package/data_template.yaml",
            "data/detection_annotation_package/annotation_manifest.json",
            "data/detection_annotation_package/annotation_manifest.csv",
            "data/detection_annotation_package/labels/README.md",
            "reports/strict_classification_evaluation_metrics.json",
            "reports/strict_classification_error_analysis.json",
            "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt",
            "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx",
            "runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt",
            "reports/test_report.docx",
            "reports/overview_design.pptx",
        ]
        missing_artifacts = [item for item in required_artifacts if item not in artifact_by_path or not artifact_by_path[item].get("exists")]
        sha_missing = [item for item in required_artifacts if not artifact_by_path.get(item, {}).get("sha256")]

        dataset = payload.get("dataset", {})
        strict = dataset.get("strict_summary", {})
        strict_duplicates = dataset.get("strict_duplicate_audit_summary", {})
        leakage_review = dataset.get("classification_leakage_review_summary", {})
        leakage_clean = dataset.get("classification_leakage_clean_candidate_summary", {})
        leakage_clean_inspection = dataset.get("classification_leakage_clean_candidate_inspection_summary", {})
        leakage_clean_duplicates = dataset.get("classification_leakage_clean_candidate_duplicate_audit_summary", {})
        cross_class_review = dataset.get("classification_cross_class_review_summary", {})
        cross_class_decision = dataset.get("classification_cross_class_decision_table_summary", {})
        cross_class_cleanup = dataset.get("classification_cross_class_cleanup_plan_summary", {})
        class_summary = dataset.get("class_consistency_summary", {})
        completed_93 = dataset.get("completed_93class_summary", {})
        completed_93_duplicates = dataset.get("completed_93class_duplicate_audit_summary", {})
        completed_93_leakage_clean = dataset.get("completed_93class_leakage_clean_candidate_summary", {})
        completed_93_leakage_clean_inspection = dataset.get("completed_93class_leakage_clean_candidate_inspection_summary", {})
        completed_93_leakage_clean_duplicates = dataset.get("completed_93class_leakage_clean_candidate_duplicate_audit_summary", {})
        detection_annotation = dataset.get("detection_annotation_package_summary", {})
        detection_validation = dataset.get("detection_annotation_validation_summary", {})
        detection_contact_sheet = dataset.get("detection_annotation_contact_sheet_summary", {})
        evaluation = payload.get("evaluation", {})
        metrics = evaluation.get("metrics", {})
        metrics_93 = evaluation.get("completed_93class_metrics", {})
        benchmark = evaluation.get("benchmark", {})
        smoke = evaluation.get("smoke_check", {})
        packages = payload.get("environment", {}).get("packages", {})

        ok = (
            payload.get("schema_version") == 1
            and len(artifacts) >= 87
            and len(payload.get("reproduction_commands", [])) == 32
            and strict.get("classes") == 92
            and strict.get("total_images") == 9567
            and strict_duplicates.get("status") == "needs_leakage_review"
            and strict_duplicates.get("duplicate_hashes") == 546
            and strict_duplicates.get("train_val_leak_hashes") == 34
            and strict_duplicates.get("cross_class_duplicate_hashes") == 52
            and leakage_review.get("status") == "complete_review_package"
            and leakage_review.get("leakage_groups") == 34
            and leakage_review.get("leakage_records") == 69
            and leakage_review.get("same_class_leakage_groups") == 16
            and leakage_review.get("cross_class_leakage_groups") == 18
            and leakage_review.get("shared_with_reference_leak_hashes") == 34
            and leakage_clean.get("status") == "leakage_val_duplicates_removed"
            and leakage_clean.get("removed_images") == 34
            and leakage_clean_inspection.get("classes") == 92
            and leakage_clean_inspection.get("train_images") == 7826
            and leakage_clean_inspection.get("val_images") == 1707
            and leakage_clean_inspection.get("total_images") == 9533
            and leakage_clean_duplicates.get("train_val_leak_hashes") == 0
            and leakage_clean_duplicates.get("cross_class_duplicate_hashes") == 34
            and cross_class_review.get("status") == "complete_review_package"
            and cross_class_review.get("source_audit_status") == "needs_leakage_review"
            and cross_class_review.get("source_total_images") == 9533
            and cross_class_review.get("cross_class_groups") == 34
            and cross_class_review.get("expected_cross_class_groups") == 34
            and cross_class_review.get("cross_class_records") == 68
            and cross_class_review.get("train_records") == 62
            and cross_class_review.get("val_records") == 6
            and cross_class_review.get("cross_split_groups") == 0
            and cross_class_review.get("train_val_leak_groups") == 0
            and cross_class_review.get("classes_involved") == 22
            and cross_class_review.get("shared_with_reference_cross_class_hashes") == 34
            and cross_class_decision.get("status") == "ready_for_manual_decision"
            and cross_class_decision.get("source_review_status") == "complete_review_package"
            and cross_class_decision.get("groups") == 34
            and cross_class_decision.get("records") == 68
            and cross_class_decision.get("pending_decisions") == 34
            and cross_class_decision.get("decided_groups") == 0
            and cross_class_decision.get("validation_errors") == 0
            and cross_class_cleanup.get("status") == "waiting_for_manual_decisions"
            and cross_class_cleanup.get("groups") == 34
            and cross_class_cleanup.get("records") == 68
            and cross_class_cleanup.get("pending_decisions") == 34
            and cross_class_cleanup.get("decided_groups") == 0
            and cross_class_cleanup.get("validation_errors") == 0
            and cross_class_cleanup.get("planned_operations") == 0
            and cross_class_cleanup.get("planned_remove_operations") == 0
            and cross_class_cleanup.get("planned_move_operations") == 0
            and class_summary.get("raw_classes") == 93
            and class_summary.get("strict_classes") == 92
            and class_summary.get("zero_train_classes") == ["大腹皮"]
            and completed_93.get("output_classes") == 93
            and completed_93.get("rebalanced_classes") == ["大腹皮"]
            and completed_93.get("train_images") == 7841
            and completed_93.get("val_images") == 1745
            and completed_93_duplicates.get("status") == "needs_leakage_review"
            and completed_93_duplicates.get("duplicate_hashes") == 546
            and completed_93_duplicates.get("train_val_leak_hashes") == 34
            and completed_93_duplicates.get("cross_class_duplicate_hashes") == 52
            and completed_93_leakage_clean.get("status") == "leakage_val_duplicates_removed"
            and completed_93_leakage_clean.get("removed_images") == 34
            and completed_93_leakage_clean_inspection.get("classes") == 93
            and completed_93_leakage_clean_inspection.get("train_images") == 7841
            and completed_93_leakage_clean_inspection.get("val_images") == 1711
            and completed_93_leakage_clean_inspection.get("total_images") == 9552
            and completed_93_leakage_clean_duplicates.get("train_val_leak_hashes") == 0
            and completed_93_leakage_clean_duplicates.get("cross_class_duplicate_hashes") == 34
            and detection_annotation.get("status") == "pending_bbox_annotation"
            and detection_annotation.get("classes") == 93
            and detection_annotation.get("images") == 279
            and detection_annotation.get("labels_expected") == 279
            and detection_annotation.get("labels_completed") == 0
            and detection_validation.get("status") == "pending_bbox_annotation"
            and detection_validation.get("images_expected") == 279
            and detection_validation.get("images_present") == 279
            and detection_validation.get("labels_missing") == 279
            and detection_validation.get("errors") == 0
            and detection_contact_sheet.get("samples") == 279
            and detection_contact_sheet.get("classes") == 93
            and detection_contact_sheet.get("labels_completed") == 0
            and detection_contact_sheet.get("annotation_status") == "pending_bbox_annotation"
            and abs(float(metrics.get("top1", -1)) - 0.17690981924533844) < 1e-9
            and abs(float(metrics.get("top5", -1)) - 0.4956921339035034) < 1e-9
            and abs(float(metrics_93.get("top1", -1)) - 0.06647564470767975) < 1e-9
            and abs(float(metrics_93.get("top5", -1)) - 0.20859599113464355) < 1e-9
            and benchmark.get("images") == 20
            and int(smoke.get("total", 0)) >= 77
            and packages.get("torch") is not None
            and not missing_artifacts
            and not sha_missing
        )
        detail = {
            "target": str(target),
            "artifacts": len(artifacts),
            "commands": len(payload.get("reproduction_commands", [])),
            "missing_artifacts": missing_artifacts,
            "sha_missing": sha_missing,
            "dataset": strict,
            "strict_duplicates": strict_duplicates,
            "leakage_review": leakage_review,
            "leakage_clean": leakage_clean,
            "leakage_clean_inspection": leakage_clean_inspection,
            "leakage_clean_duplicates": leakage_clean_duplicates,
            "cross_class_review": cross_class_review,
            "cross_class_decision": cross_class_decision,
            "cross_class_cleanup": cross_class_cleanup,
            "class_summary": class_summary,
            "completed_93": completed_93,
            "completed_93_duplicates": completed_93_duplicates,
            "completed_93_leakage_clean": completed_93_leakage_clean,
            "completed_93_leakage_clean_inspection": completed_93_leakage_clean_inspection,
            "completed_93_leakage_clean_duplicates": completed_93_leakage_clean_duplicates,
            "detection_annotation": detection_annotation,
            "detection_validation": detection_validation,
            "detection_contact_sheet": detection_contact_sheet,
            "smoke": smoke,
        }
        return {"name": f"repro_manifest:{path}", "passed": ok, "detail": detail}
    except Exception as exc:
        return {"name": f"repro_manifest:{path}", "passed": False, "detail": repr(exc)}


def check_review_samples(path: str) -> dict:
    try:
        target, payload = read_json(path)
        confusion = payload.get("confusion_samples", [])
        worst = payload.get("worst_class_samples", [])
        figures = payload.get("figures", {})
        figure_details = []
        figures_ok = True
        for value in figures.values():
            figure = Path(value)
            figure_path = figure if figure.is_absolute() else ROOT / figure
            if not figure_path.exists():
                figures_ok = False
                figure_details.append({"path": str(figure_path), "exists": False})
                continue
            with Image.open(figure_path) as image:
                width, height = image.size
            size_ok = width >= 800 and height >= 1200 and figure_path.stat().st_size > 100_000
            figures_ok = figures_ok and size_ok
            figure_details.append({"path": str(figure_path), "size": [width, height], "bytes": figure_path.stat().st_size})

        sample_paths_ok = all(Path(sample.get("image", "")).exists() for sample in confusion[:3] + worst[:3])
        ok = (
            target.name == "strict_classification_review_samples.json"
            and len(confusion) == 18
            and len(worst) == 18
            and sample_paths_ok
            and figures_ok
        )
        return {
            "name": f"review_samples:{path}",
            "passed": ok,
            "detail": {
                "confusion_samples": len(confusion),
                "worst_class_samples": len(worst),
                "figures": figure_details,
            },
        }
    except Exception as exc:
        return {"name": f"review_samples:{path}", "passed": False, "detail": repr(exc)}


def check_qa_report(path: str, total_key: str, passed_key: str, expected_total: int) -> dict:
    try:
        _, payload = read_json(path)
        summary = payload.get("summary", {})
        passed = summary.get(total_key) == expected_total and summary.get(passed_key) == expected_total
        if "relevant_console_errors" in summary:
            passed = passed and summary.get("relevant_console_errors") == 0
        return {"name": f"qa_report:{path}", "passed": passed, "detail": summary}
    except Exception as exc:
        return {"name": f"qa_report:{path}", "passed": False, "detail": repr(exc)}


def check_text_contains(path: str, required: list[str]) -> dict:
    target = ROOT / path
    try:
        text = target.read_text(encoding="utf-8")
        missing = [item for item in required if item not in text]
        return {
            "name": f"text_contains:{path}",
            "passed": not missing,
            "detail": f"missing={missing}",
        }
    except Exception as exc:
        return {"name": f"text_contains:{path}", "passed": False, "detail": repr(exc)}


def run_command(name: str, command: list[str], cwd: Path) -> dict:
    try:
        proc = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=120)
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        return {"name": name, "passed": proc.returncode == 0, "detail": output[-1500:]}
    except Exception as exc:
        return {"name": name, "passed": False, "detail": repr(exc)}


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# 工程自检报告",
        "",
        f"- 时间: {report['timestamp']}",
        f"- Python: {report['python']}",
        f"- 总检查项: {report['summary']['total']}",
        f"- 通过: {report['summary']['passed']}",
        f"- 失败: {report['summary']['failed']}",
        "",
        "## 检查明细",
        "",
        "| 检查项 | 状态 | 说明 |",
        "|---|---|---|",
    ]
    for item in report["checks"]:
        status = "通过" if item["passed"] else "未通过"
        detail = str(item["detail"]).replace("\n", "<br>")
        lines.append(f"| `{item['name']}` | {status} | {detail} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run project smoke checks.")
    parser.add_argument("--output", default="reports/smoke_check.json")
    args = parser.parse_args()

    checks = [
        check_exists("README.md"),
        check_exists("requirements.txt"),
        check_exists("configs/train_baseline.yaml"),
        check_exists("scripts/train_yolo12.py"),
        check_exists("backend/app/main.py"),
        check_exists("frontend/src/App.vue"),
        check_exists("reports/test_report.md"),
        check_exists("reports/overview_design.pptx"),
        check_exists("reports/submission_checklist.md"),
        check_exists("reports/strict_classification_training_report.md"),
        check_exists("reports/strict_classification_evaluation_metrics.json"),
        check_exists("scripts/prepare_completed_classification_dataset.py"),
        check_exists("scripts/prepare_detection_annotation_package.py"),
        check_exists("scripts/validate_detection_annotation_package.py"),
        check_exists("scripts/generate_detection_annotation_contact_sheet.py"),
        check_exists("configs/train_cls_93class_smoke.yaml"),
        check_exists("reports/classification_93class_completion_report.json"),
        check_exists("reports/classification_93class_completion_report.md"),
        check_exists("reports/classification_93class_dataset_inspection.json"),
        check_exists("reports/classification_93class_dataset_inspection.md"),
        check_exists("reports/classification_93class_training_report.md"),
        check_exists("reports/classification_93class_evaluation_metrics.json"),
        check_exists("reports/detection_annotation_package_report.json"),
        check_exists("reports/detection_annotation_package_report.md"),
        check_exists("reports/detection_annotation_package_validation.json"),
        check_exists("reports/detection_annotation_package_validation.md"),
        check_exists("reports/detection_annotation_contact_sheet.json"),
        check_exists("reports/detection_annotation_contact_sheet.md"),
        check_exists("data/detection_annotation_package/ANNOTATION_GUIDE.md"),
        check_exists("data/detection_annotation_package/annotation_manifest.csv"),
        check_exists("data/detection_annotation_package/annotation_manifest.json"),
        check_exists("data/detection_annotation_package/annotation_summary.md"),
        check_exists("data/detection_annotation_package/classes.txt"),
        check_exists("data/detection_annotation_package/data_template.yaml"),
        check_exists("data/detection_annotation_package/labels/README.md"),
        check_exists("scripts/infer_image_cls.py"),
        check_exists("scripts/benchmark_cls.py"),
        check_exists("scripts/analyze_classification_errors.py"),
        check_exists("scripts/generate_error_review_contact_sheet.py"),
        check_exists("scripts/audit_class_consistency.py"),
        check_exists("scripts/audit_classification_duplicates.py"),
        check_exists("scripts/generate_classification_leakage_review_package.py"),
        check_exists("scripts/prepare_leakage_clean_classification_dataset.py"),
        check_exists("scripts/generate_classification_cross_class_review_package.py"),
        check_exists("scripts/generate_classification_cross_class_decision_table.py"),
        check_exists("scripts/generate_classification_cross_class_decision_review_html.py"),
        check_exists("scripts/generate_classification_cross_class_cleanup_plan.py"),
        check_exists("scripts/apply_classification_cross_class_cleanup_plan.py"),
        check_exists("scripts/generate_repro_manifest.py"),
        check_exists("reports/class_consistency_audit.json"),
        check_exists("reports/class_consistency_audit.md"),
        check_exists("reports/strict_classification_duplicate_audit.json"),
        check_exists("reports/strict_classification_duplicate_audit.md"),
        check_exists("reports/classification_leakage_review_package.json"),
        check_exists("reports/classification_leakage_review_package.md"),
        check_exists("reports/classification_leakage_clean_candidate_report.json"),
        check_exists("reports/classification_leakage_clean_candidate_report.md"),
        check_exists("reports/classification_leakage_clean_candidate_inspection.json"),
        check_exists("reports/classification_leakage_clean_candidate_inspection.md"),
        check_exists("reports/classification_leakage_clean_candidate_duplicate_audit.json"),
        check_exists("reports/classification_leakage_clean_candidate_duplicate_audit.md"),
        check_exists("reports/classification_cross_class_review_package.json"),
        check_exists("reports/classification_cross_class_review_package.md"),
        check_exists("reports/classification_cross_class_decision_table.json"),
        check_exists("reports/classification_cross_class_decision_table.csv"),
        check_exists("reports/classification_cross_class_decision_table.md"),
        check_exists("reports/classification_cross_class_decision_review.html"),
        check_exists("reports/classification_cross_class_cleanup_plan.json"),
        check_exists("reports/classification_cross_class_cleanup_plan.csv"),
        check_exists("reports/classification_cross_class_cleanup_plan.md"),
        check_exists("reports/classification_93class_duplicate_audit.json"),
        check_exists("reports/classification_93class_duplicate_audit.md"),
        check_exists("reports/classification_93class_leakage_clean_candidate_report.json"),
        check_exists("reports/classification_93class_leakage_clean_candidate_report.md"),
        check_exists("reports/classification_93class_leakage_clean_candidate_inspection.json"),
        check_exists("reports/classification_93class_leakage_clean_candidate_inspection.md"),
        check_exists("reports/classification_93class_leakage_clean_candidate_duplicate_audit.json"),
        check_exists("reports/classification_93class_leakage_clean_candidate_duplicate_audit.md"),
        check_exists("reports/repro_manifest.json"),
        check_exists("reports/repro_manifest.md"),
        check_exists("reports/strict_classification_error_analysis.json"),
        check_exists("reports/strict_classification_error_analysis.md"),
        check_exists("reports/strict_classification_review_samples.json"),
        check_exists("reports/strict_classification_review_samples.md"),
        check_exists("reports/figures/strict_confusion_contact_sheet.png"),
        check_exists("reports/figures/strict_worst_class_contact_sheet.png"),
        check_exists("reports/figures/classification_train_val_leakage_contact_sheet.png"),
        check_exists("reports/figures/classification_cross_class_contact_sheet.png"),
        check_exists("reports/figures/detection_annotation_contact_sheet.png"),
        check_exists("configs/train_cls_strict_cpu_30e.yaml"),
        check_exists("configs/train_cls_strict_gpu_100e.yaml"),
        check_exists("runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt"),
        check_exists("runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx"),
        check_exists("runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt"),
        check_file_size("runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt", 1_000_000),
        check_file_size("runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx", 1_000_000),
        check_file_size("runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt", 1_000_000),
        check_json_summary(
            "reports/strict_classification_dataset_inspection.json",
            {
                "classes": 92,
                "train_images": 7826,
                "val_images": 1741,
                "total_images": 9567,
                "verified_images": 9567,
                "errors": 0,
                "warnings": 0,
            },
        ),
        check_json_summary(
            "reports/classification_93class_dataset_inspection.json",
            {
                "classes": 93,
                "train_images": 7841,
                "val_images": 1745,
                "total_images": 9586,
                "verified_images": 9586,
                "errors": 0,
                "warnings": 0,
            },
        ),
        check_duplicate_audit(
            "reports/strict_classification_duplicate_audit.json",
            {
                "status": "needs_leakage_review",
                "total_images": 9567,
                "unique_hashes": 9014,
                "duplicate_hashes": 546,
                "duplicate_images": 1099,
                "duplicate_extra_images": 553,
                "cross_split_duplicate_hashes": 34,
                "train_val_leak_hashes": 34,
                "cross_class_duplicate_hashes": 52,
                "classes": 92,
                "reported_groups": 80,
            },
        ),
        check_duplicate_audit(
            "reports/classification_93class_duplicate_audit.json",
            {
                "status": "needs_leakage_review",
                "total_images": 9586,
                "unique_hashes": 9033,
                "duplicate_hashes": 546,
                "duplicate_images": 1099,
                "duplicate_extra_images": 553,
                "cross_split_duplicate_hashes": 34,
                "train_val_leak_hashes": 34,
                "cross_class_duplicate_hashes": 52,
                "classes": 93,
                "reported_groups": 80,
            },
        ),
        check_classification_leakage_review_package("reports/classification_leakage_review_package.json"),
        check_leakage_clean_candidate(
            "reports/classification_leakage_clean_candidate_report.json",
            "reports/classification_leakage_clean_candidate_inspection.json",
            "reports/classification_leakage_clean_candidate_duplicate_audit.json",
            {
                "removed_records": 34,
                "report": {
                    "status": "leakage_val_duplicates_removed",
                    "source_images": 9567,
                    "output_images": 9533,
                    "removed_images": 34,
                    "requested_val_removals": 34,
                    "missing_requested_removals": 0,
                    "leakage_groups_from_review": 34,
                    "classes": 92,
                },
                "inspection": {
                    "classes": 92,
                    "train_images": 7826,
                    "val_images": 1707,
                    "total_images": 9533,
                    "verified_images": 9533,
                    "errors": 0,
                    "warnings": 0,
                },
                "duplicate": {
                    "status": "needs_leakage_review",
                    "total_images": 9533,
                    "train_val_leak_hashes": 0,
                    "cross_class_duplicate_hashes": 34,
                    "classes": 92,
                },
            },
        ),
        check_leakage_clean_candidate(
            "reports/classification_93class_leakage_clean_candidate_report.json",
            "reports/classification_93class_leakage_clean_candidate_inspection.json",
            "reports/classification_93class_leakage_clean_candidate_duplicate_audit.json",
            {
                "removed_records": 34,
                "report": {
                    "status": "leakage_val_duplicates_removed",
                    "source_images": 9586,
                    "output_images": 9552,
                    "removed_images": 34,
                    "requested_val_removals": 34,
                    "missing_requested_removals": 0,
                    "leakage_groups_from_review": 34,
                    "classes": 93,
                },
                "inspection": {
                    "classes": 93,
                    "train_images": 7841,
                    "val_images": 1711,
                    "total_images": 9552,
                    "verified_images": 9552,
                    "errors": 0,
                    "warnings": 0,
                },
                "duplicate": {
                    "status": "needs_leakage_review",
                    "total_images": 9552,
                    "train_val_leak_hashes": 0,
                    "cross_class_duplicate_hashes": 34,
                    "classes": 93,
                },
            },
        ),
        check_cross_class_review_package("reports/classification_cross_class_review_package.json"),
        check_cross_class_decision_table("reports/classification_cross_class_decision_table.json"),
        check_cross_class_decision_review_html("reports/classification_cross_class_decision_review.html"),
        check_cross_class_cleanup_plan("reports/classification_cross_class_cleanup_plan.json"),
        check_pending_cleanup_execution_blocked(),
        check_strict_metrics("reports/strict_classification_evaluation_metrics.json"),
        check_93class_metrics("reports/classification_93class_evaluation_metrics.json"),
        check_error_analysis("reports/strict_classification_error_analysis.json"),
        check_class_consistency("reports/class_consistency_audit.json"),
        check_93class_completion("reports/classification_93class_completion_report.json"),
        check_detection_annotation_package("reports/detection_annotation_package_report.json"),
        check_detection_annotation_validation("reports/detection_annotation_package_validation.json"),
        check_detection_annotation_contact_sheet("reports/detection_annotation_contact_sheet.json"),
        check_repro_manifest("reports/repro_manifest.json"),
        check_review_samples("reports/strict_classification_review_samples.json"),
        check_strict_benchmark("runs/benchmarks/strict_classification_latency_20.json"),
        check_sample_prediction("reports/strict_classification_sample_prediction.json"),
        check_qa_report("reports/backend_qa.json", "total", "passed", 4),
        check_qa_report("reports/frontend_qa.json", "checks_total", "checks_passed", 6),
        check_text_contains(
            "reports/strict_classification_training_report.md",
            ["Top-1 Accuracy", "Top-5 Accuracy", "ONNX", "/classify/image", "真实 bbox 标注", "高频混淆对", "检测 bbox 标注准备包", "`labels/` 仍为空", "重复与泄漏审计", "train/val 泄漏组 34", "候选泄漏清理集", "train/val 泄漏组为 0", "classification_leakage_review_package", "classification_cross_class_review_package", "classification_cross_class_cleanup_plan"],
        ),
        check_text_contains(
            "reports/submission_checklist.md",
            ["strict JPEG 数据集", "best.onnx", "Top-1 0.1769", "误判分析", "93 类补齐", "候选泄漏清理集", "train/val 泄漏组 0", "检测标注准备包", "`labels/` 仍为空", "不能把分类 Top-1/Top-5 当作检测", "重复/泄漏审计", "classification_leakage_review_package", "classification_cross_class_review_package", "classification_cross_class_cleanup_plan"],
        ),
        check_text_contains(
            "reports/detection_annotation_package_report.md",
            ["检测 bbox 标注准备包报告", "类别数: 93", "待标注图片: 279", "已完成标签文件: 0", "当前没有真实 bbox 标签"],
        ),
        check_text_contains(
            "reports/detection_annotation_package_validation.md",
            ["检测标注准备包校验报告", "状态: `pending_bbox_annotation`", "缺失标签: 279", "errors / warnings: 0 / 0", "不能直接训练检测模型"],
        ),
        check_text_contains(
            "reports/detection_annotation_contact_sheet.md",
            ["检测标注样本 contact sheet 索引", "样本总数: 279", "类别数: 93", "不是检测训练数据", "validate_detection_annotation_package.py --require-complete"],
        ),
        check_text_contains(
            "reports/strict_classification_error_analysis.md",
            ["Top-1 最低类别", "Top-1 最高类别", "高频混淆对", "典型误判样例"],
        ),
        check_text_contains(
            "reports/strict_classification_review_samples.md",
            ["高频混淆复核样例", "低表现类别复核样例", "contact sheet", "建议处理"],
        ),
        check_text_contains(
            "reports/class_consistency_audit.md",
            ["原始类别: 93", "strict 类别: 92", "大腹皮", "训练样本为 0", "needs_class_completion"],
        ),
        check_text_contains(
            "reports/strict_classification_duplicate_audit.md",
            ["分类数据重复与泄漏审计报告", "状态: `needs_leakage_review`", "train/val 泄漏组: 34", "跨类别重复组: 52", "不要仅凭本报告自动删图"],
        ),
        check_text_contains(
            "reports/classification_leakage_review_package.md",
            ["分类 train/val 泄漏人工复核包", "train/val 泄漏组: 34 / 34", "跨类别泄漏组: 18", "manual_decision", "不自动删除、移动或重划任何图片"],
        ),
        check_text_contains(
            "reports/classification_leakage_clean_candidate_report.md",
            ["分类数据 train/val 泄漏候选清理报告", "移除图片: 34 / 请求移除 34", "train", "val", "不自动修改 train 图像", "不自动裁决跨类别标签"],
        ),
        check_text_contains(
            "reports/classification_cross_class_review_package.md",
            ["分类跨类别 exact duplicate 人工复核包", "跨类别重复组: 34 / 34", "涉及文件记录: 68", "train/val 泄漏组: 0", "manual_decision", "不自动删除、移动、重命名或重标任何图片"],
        ),
        check_text_contains(
            "reports/classification_cross_class_decision_table.md",
            ["分类跨类别标签冲突决策表", "状态: `ready_for_manual_decision`", "待决策组: 34 / 34", "校验错误: 0", "decision_status", "remove_relative_paths", "不自动删除、移动、重命名、重标或复制任何图片"],
        ),
        check_text_contains(
            "reports/classification_cross_class_decision_review.html",
            ["跨类别标签冲突人工决策复核页", "cross_class_001", "cross_class_034", "data-copy-row", "只辅助人工填写，不自动修改 CSV 或数据集"],
        ),
        check_text_contains(
            "reports/classification_cross_class_cleanup_plan.md",
            ["分类跨类别标签冲突清理计划校验报告", "状态: `waiting_for_manual_decisions`", "待决策组: 34 / 34", "计划操作: 0", "当前没有可执行操作", "不会删除、移动、重命名、重标或复制任何图片"],
        ),
        check_text_contains(
            "reports/classification_93class_leakage_clean_candidate_report.md",
            ["分类数据 train/val 泄漏候选清理报告", "移除图片: 34 / 请求移除 34", "train", "val", "不自动修改 train 图像", "不自动裁决跨类别标签"],
        ),
        check_text_contains(
            "reports/classification_93class_duplicate_audit.md",
            ["分类数据重复与泄漏审计报告", "状态: `needs_leakage_review`", "train/val 泄漏组: 34", "跨类别重复组: 52", "不要仅凭本报告自动删图"],
        ),
        check_text_contains(
            "reports/classification_93class_completion_report.md",
            ["93 类补齐分类数据集报告", "输出类别: 93", "大腹皮", "15", "4", "rebalance_val_only"],
        ),
        check_text_contains(
            "reports/classification_93class_training_report.md",
            ["93 类补齐实验", "classification_strict_jpeg_93class", "Top-1 0.0665", "Top-5 0.2086", "大腹皮"],
        ),
        check_text_contains(
            "reports/repro_manifest.md",
            ["可复现实验 Manifest", "关键产物哈希", "Top-1", "Top-5", "大腹皮", "SHA256", "93 类补齐", "候选泄漏清理集", "train/val 泄漏组 0", "检测标注准备包", "detection_annotation_contact_sheet", "classification_leakage_review_package", "classification_cross_class_review_package", "classification_cross_class_decision_table", "classification_cross_class_cleanup_plan", "跨类别清理计划校验", "strict 重复/泄漏审计", "labels/ 为空"],
        ),
        check_text_contains(
            "README.md",
            ["跨类别决策表", "classification_cross_class_decision_table", "ready_for_manual_decision", "跨类别清理计划校验", "classification_cross_class_cleanup_plan", "不自动修改图片或数据集"],
        ),
        check_text_contains(
            "docs/README.md",
            ["跨类别决策表", "classification_cross_class_decision_table", "34/34 组为 `pending`", "跨类别清理计划校验", "classification_cross_class_cleanup_plan", "不自动修改图片"],
        ),
        check_text_contains(
            "reports/test_report.md",
            ["跨类别决策表", "classification_cross_class_decision_table", "34 / 34", "只收集人工决策", "跨类别清理计划校验", "classification_cross_class_cleanup_plan", "ready_for_cleanup_execution"],
        ),
        check_text_contains(
            "reports/submission_checklist.md",
            ["跨类别决策表", "classification_cross_class_decision_table", "CSV 填写表", "pending 34/34", "跨类别清理计划校验", "classification_cross_class_cleanup_plan"],
        ),
        check_text_contains(
            "reports/strict_classification_training_report.md",
            ["跨类别决策表", "classification_cross_class_decision_table", "ready_for_manual_decision", "CSV 用于填写", "跨类别清理计划校验", "classification_cross_class_cleanup_plan"],
        ),
        check_docx_text("reports/test_report.docx", ["误判分析", "人工复核", "类别一致性", "重复/泄漏审计", "泄漏人工复核包", "跨类别复核包", "跨类别决策表", "跨类别清理计划校验", "候选泄漏清理集", "train/val 泄漏归零", "大腹皮", "可复现实验", "93 类补齐实验", "检测标注准备包", "labels/ 仍为空"]),
        check_pptx("reports/overview_design.pptx"),
    ]
    checks.extend(check_python_deps())
    checks.append(run_command("python_compile", [sys.executable, "-m", "compileall", "scripts", "backend", "tests", "-q"], ROOT))
    checks.append(run_command("frontend_build", ["npm.cmd", "run", "build"], ROOT / "frontend"))

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python": sys.executable,
        "checks": checks,
    }
    report["summary"] = {
        "total": len(checks),
        "passed": sum(1 for c in checks if c["passed"]),
        "failed": sum(1 for c in checks if not c["passed"]),
    }

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output.with_suffix(".md"))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    # Missing training dependencies are expected before environment setup, so this is informational.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
