from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime
from importlib import metadata
from pathlib import Path
from typing import Any

from path_utils import project_root, resolve_project_path


ROOT = project_root()


def load_json(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    if not path.exists():
        return {}
    try:
        import yaml

        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        result: dict[str, Any] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if ":" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
        return result


def package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_entry(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    entry: dict[str, Any] = {
        "path": relative_path,
        "exists": path.exists(),
    }
    if path.exists() and path.is_file():
        entry.update(
            {
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            }
        )
    return entry


def build_manifest() -> dict[str, Any]:
    dataset = load_json("reports/strict_classification_dataset_inspection.json")
    class_audit = load_json("reports/class_consistency_audit.json")
    completed_93 = load_json("reports/classification_93class_completion_report.json")
    completed_93_inspection = load_json("reports/classification_93class_dataset_inspection.json")
    strict_duplicate_audit = load_json("reports/strict_classification_duplicate_audit.json")
    leakage_review = load_json("reports/classification_leakage_review_package.json")
    leakage_clean = load_json("reports/classification_leakage_clean_candidate_report.json")
    leakage_clean_inspection = load_json("reports/classification_leakage_clean_candidate_inspection.json")
    leakage_clean_duplicate_audit = load_json("reports/classification_leakage_clean_candidate_duplicate_audit.json")
    cross_class_review = load_json("reports/classification_cross_class_review_package.json")
    cross_class_decision_table = load_json("reports/classification_cross_class_decision_table.json")
    cross_class_cleanup_plan = load_json("reports/classification_cross_class_cleanup_plan.json")
    completed_93_duplicate_audit = load_json("reports/classification_93class_duplicate_audit.json")
    completed_93_leakage_clean = load_json("reports/classification_93class_leakage_clean_candidate_report.json")
    completed_93_leakage_clean_inspection = load_json("reports/classification_93class_leakage_clean_candidate_inspection.json")
    completed_93_leakage_clean_duplicate_audit = load_json("reports/classification_93class_leakage_clean_candidate_duplicate_audit.json")
    metrics = load_json("reports/strict_classification_evaluation_metrics.json")
    completed_93_metrics = load_json("reports/classification_93class_evaluation_metrics.json")
    detection_annotation_package = load_json("reports/detection_annotation_package_report.json")
    detection_annotation_validation = load_json("reports/detection_annotation_package_validation.json")
    detection_contact_sheet = load_json("reports/detection_annotation_contact_sheet.json")
    error_analysis = load_json("reports/strict_classification_error_analysis.json")
    review_samples = load_json("reports/strict_classification_review_samples.json")
    benchmark = load_json("runs/benchmarks/strict_classification_latency_20.json")
    backend_qa = load_json("reports/backend_qa.json")
    frontend_qa = load_json("reports/frontend_qa.json")
    smoke = load_json("reports/smoke_check.json")

    training_config_path = "configs/train_cls_strict_cpu_5e.yaml"
    training_config = load_yaml(training_config_path)
    completed_93_config_path = "configs/train_cls_93class_smoke.yaml"
    completed_93_config = load_yaml(completed_93_config_path)
    package_names = [
        "torch",
        "ultralytics",
        "fastapi",
        "uvicorn",
        "playwright",
        "pillow",
        "PyYAML",
        "python-docx",
        "pytest",
    ]

    artifacts = [
        "configs/train_cls_strict_cpu_5e.yaml",
        "configs/train_cls_93class_smoke.yaml",
        "configs/train_cls_strict_cpu_30e.yaml",
        "configs/train_cls_strict_gpu_100e.yaml",
        "data/classification_strict_jpeg/strict_classification_report.json",
        "data/classification_strict_jpeg_93class/classification_93class_completion_report.json",
        "data/classification_strict_jpeg_93class/classification_93class_completion_report.md",
        "data/detection_annotation_package/ANNOTATION_GUIDE.md",
        "data/detection_annotation_package/annotation_manifest.csv",
        "data/detection_annotation_package/annotation_manifest.json",
        "data/detection_annotation_package/annotation_summary.md",
        "data/detection_annotation_package/classes.txt",
        "data/detection_annotation_package/data_template.yaml",
        "data/detection_annotation_package/labels/README.md",
        "scripts/validate_detection_annotation_package.py",
        "scripts/generate_detection_annotation_contact_sheet.py",
        "scripts/audit_classification_duplicates.py",
        "scripts/generate_classification_leakage_review_package.py",
        "scripts/prepare_leakage_clean_classification_dataset.py",
        "scripts/generate_classification_cross_class_review_package.py",
        "scripts/generate_classification_cross_class_decision_table.py",
        "scripts/generate_classification_cross_class_decision_review_html.py",
        "scripts/generate_classification_cross_class_cleanup_plan.py",
        "scripts/apply_classification_cross_class_cleanup_plan.py",
        "reports/strict_classification_dataset_inspection.json",
        "reports/strict_classification_duplicate_audit.json",
        "reports/strict_classification_duplicate_audit.md",
        "reports/classification_leakage_review_package.json",
        "reports/classification_leakage_review_package.md",
        "reports/classification_leakage_clean_candidate_report.json",
        "reports/classification_leakage_clean_candidate_report.md",
        "reports/classification_leakage_clean_candidate_inspection.json",
        "reports/classification_leakage_clean_candidate_inspection.md",
        "reports/classification_leakage_clean_candidate_duplicate_audit.json",
        "reports/classification_leakage_clean_candidate_duplicate_audit.md",
        "reports/classification_cross_class_review_package.json",
        "reports/classification_cross_class_review_package.md",
        "reports/classification_cross_class_decision_table.json",
        "reports/classification_cross_class_decision_table.csv",
        "reports/classification_cross_class_decision_table.md",
        "reports/classification_cross_class_decision_review.html",
        "reports/classification_cross_class_cleanup_plan.json",
        "reports/classification_cross_class_cleanup_plan.csv",
        "reports/classification_cross_class_cleanup_plan.md",
        "reports/class_consistency_audit.json",
        "reports/class_consistency_audit.md",
        "reports/classification_93class_completion_report.json",
        "reports/classification_93class_completion_report.md",
        "reports/classification_93class_dataset_inspection.json",
        "reports/classification_93class_dataset_inspection.md",
        "reports/classification_93class_duplicate_audit.json",
        "reports/classification_93class_duplicate_audit.md",
        "reports/classification_93class_leakage_clean_candidate_report.json",
        "reports/classification_93class_leakage_clean_candidate_report.md",
        "reports/classification_93class_leakage_clean_candidate_inspection.json",
        "reports/classification_93class_leakage_clean_candidate_inspection.md",
        "reports/classification_93class_leakage_clean_candidate_duplicate_audit.json",
        "reports/classification_93class_leakage_clean_candidate_duplicate_audit.md",
        "reports/classification_93class_training_report.md",
        "reports/classification_93class_evaluation_metrics.json",
        "reports/detection_annotation_package_report.json",
        "reports/detection_annotation_package_report.md",
        "reports/detection_annotation_package_validation.json",
        "reports/detection_annotation_package_validation.md",
        "reports/detection_annotation_contact_sheet.json",
        "reports/detection_annotation_contact_sheet.md",
        "reports/strict_classification_evaluation_metrics.json",
        "reports/strict_classification_error_analysis.json",
        "reports/strict_classification_error_analysis.md",
        "reports/strict_classification_review_samples.json",
        "reports/strict_classification_review_samples.md",
        "reports/strict_classification_sample_prediction.json",
        "runs/benchmarks/strict_classification_latency_20.json",
        "reports/backend_qa.json",
        "reports/frontend_qa.json",
        "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt",
        "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/last.pt",
        "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx",
        "runs/train/strict_93class_yolo12n_cls_cpu_smoke/results.csv",
        "runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt",
        "runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/last.pt",
        "reports/test_report.md",
        "reports/test_report.docx",
        "reports/strict_classification_training_report.md",
        "reports/submission_checklist.md",
        "reports/overview_design.pptx",
        "reports/figures/strict_confusion_contact_sheet.png",
        "reports/figures/strict_worst_class_contact_sheet.png",
        "reports/figures/classification_train_val_leakage_contact_sheet.png",
        "reports/figures/classification_cross_class_contact_sheet.png",
        "reports/figures/detection_annotation_contact_sheet.png",
        "README.md",
        "docs/README.md",
        "scripts/prepare_detection_annotation_package.py",
    ]

    repro_commands = [
        r".\.venv\Scripts\python.exe scripts\prepare_strict_classification_dataset.py --source ..\data --output data\classification_strict_jpeg --overwrite",
        r".\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg --verify-images --output reports\strict_classification_dataset_inspection.json",
        r".\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg --output reports\strict_classification_duplicate_audit.json --markdown reports\strict_classification_duplicate_audit.md --max-groups 80",
        r".\.venv\Scripts\python.exe scripts\audit_class_consistency.py --source ..\data --output reports\class_consistency_audit.json --markdown reports\class_consistency_audit.md",
        r".\.venv\Scripts\python.exe scripts\prepare_completed_classification_dataset.py --source ..\data --output data\classification_strict_jpeg_93class --overwrite --report reports\classification_93class_completion_report.json --markdown reports\classification_93class_completion_report.md",
        r".\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class --verify-images --output reports\classification_93class_dataset_inspection.json --markdown reports\classification_93class_dataset_inspection.md",
        r".\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class --output reports\classification_93class_duplicate_audit.json --markdown reports\classification_93class_duplicate_audit.md --max-groups 80",
        r".\.venv\Scripts\python.exe scripts\generate_classification_leakage_review_package.py --audit reports\strict_classification_duplicate_audit.json --reference-audit reports\classification_93class_duplicate_audit.json --output reports\classification_leakage_review_package.json --figure reports\figures\classification_train_val_leakage_contact_sheet.png",
        r".\.venv\Scripts\python.exe scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_leakage_clean_candidate --report reports\classification_leakage_clean_candidate_report.json --markdown reports\classification_leakage_clean_candidate_report.md --overwrite",
        r".\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_leakage_clean_candidate --verify-images --output reports\classification_leakage_clean_candidate_inspection.json --markdown reports\classification_leakage_clean_candidate_inspection.md",
        r".\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_leakage_clean_candidate --output reports\classification_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_leakage_clean_candidate_duplicate_audit.md --max-groups 80",
        r".\.venv\Scripts\python.exe scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg_93class --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_93class_leakage_clean_candidate --report reports\classification_93class_leakage_clean_candidate_report.json --markdown reports\classification_93class_leakage_clean_candidate_report.md --overwrite",
        r".\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --verify-images --output reports\classification_93class_leakage_clean_candidate_inspection.json --markdown reports\classification_93class_leakage_clean_candidate_inspection.md",
        r".\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --output reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_93class_leakage_clean_candidate_duplicate_audit.md --max-groups 80",
        r".\.venv\Scripts\python.exe scripts\generate_classification_cross_class_review_package.py --audit reports\classification_leakage_clean_candidate_duplicate_audit.json --reference-audit reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --output reports\classification_cross_class_review_package.json --figure reports\figures\classification_cross_class_contact_sheet.png",
        r".\.venv\Scripts\python.exe scripts\generate_classification_cross_class_decision_table.py --review-package reports\classification_cross_class_review_package.json --output reports\classification_cross_class_decision_table.json --csv reports\classification_cross_class_decision_table.csv --markdown reports\classification_cross_class_decision_table.md",
        r".\.venv\Scripts\python.exe scripts\generate_classification_cross_class_decision_review_html.py --review-package reports\classification_cross_class_review_package.json --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_decision_review.html",
        r".\.venv\Scripts\python.exe scripts\generate_classification_cross_class_cleanup_plan.py --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_cleanup_plan.json --operations-csv reports\classification_cross_class_cleanup_plan.csv --markdown reports\classification_cross_class_cleanup_plan.md",
        r".\.venv\Scripts\python.exe scripts\prepare_detection_annotation_package.py --source data\classification_strict_jpeg_93class --output data\detection_annotation_package --overwrite --samples-per-class 3 --train-per-class 2 --val-per-class 1 --report reports\detection_annotation_package_report.json --markdown reports\detection_annotation_package_report.md",
        r".\.venv\Scripts\python.exe scripts\generate_detection_annotation_contact_sheet.py --manifest data\detection_annotation_package\annotation_manifest.json --output reports\detection_annotation_contact_sheet.json --figure reports\figures\detection_annotation_contact_sheet.png",
        r".\.venv\Scripts\python.exe scripts\validate_detection_annotation_package.py --package data\detection_annotation_package --output reports\detection_annotation_package_validation.json --markdown reports\detection_annotation_package_validation.md",
        r".\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_93class_smoke.yaml",
        r".\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py --model runs\train\strict_93class_yolo12n_cls_cpu_smoke\weights\best.pt --data data\classification_strict_jpeg_93class --imgsz 224 --device cpu --output reports\classification_93class_evaluation_metrics.json",
        r".\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_5e.yaml",
        r".\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg --imgsz 224 --device cpu --output reports\strict_classification_evaluation_metrics.json",
        r".\.venv\Scripts\python.exe scripts\analyze_classification_errors.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg\val --imgsz 224 --device cpu --output reports\strict_classification_error_analysis.json",
        r".\.venv\Scripts\python.exe scripts\generate_error_review_contact_sheet.py --analysis reports\strict_classification_error_analysis.json --output reports\strict_classification_review_samples.json",
        r".\.venv\Scripts\python.exe scripts\infer_image_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --source data\classification_strict_jpeg\val\丝瓜络\Sigualuo117.jpg --imgsz 224 --device cpu --topk 5 --output reports\strict_classification_sample_prediction.json",
        r".\.venv\Scripts\python.exe scripts\benchmark_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --images data\classification_strict_jpeg\val --imgsz 224 --device cpu --warmup 3 --iterations 20 --output runs\benchmarks\strict_classification_latency_20.json",
        r".\.venv\Scripts\python.exe scripts\export_model.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --format onnx --imgsz 224 --simplify",
        r".\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md",
        r".\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json",
    ]

    review_figures = review_samples.get("figures", {}) if isinstance(review_samples, dict) else {}
    return {
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(ROOT),
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": {name: package_version(name) for name in package_names},
        },
        "dataset": {
            "strict_summary": dataset.get("summary", {}),
            "strict_duplicate_audit_summary": strict_duplicate_audit.get("summary", {}),
            "classification_leakage_review_summary": leakage_review.get("summary", {}),
            "classification_leakage_clean_candidate_summary": leakage_clean.get("summary", {}),
            "classification_leakage_clean_candidate_inspection_summary": leakage_clean_inspection.get("summary", {}),
            "classification_leakage_clean_candidate_duplicate_audit_summary": leakage_clean_duplicate_audit.get("summary", {}),
            "classification_cross_class_review_summary": cross_class_review.get("summary", {}),
            "classification_cross_class_decision_table_summary": cross_class_decision_table.get("summary", {}),
            "classification_cross_class_cleanup_plan_summary": cross_class_cleanup_plan.get("summary", {}),
            "class_consistency_summary": class_audit.get("summary", {}),
            "completed_93class_summary": completed_93.get("summary", {}),
            "completed_93class_inspection_summary": completed_93_inspection.get("summary", {}),
            "completed_93class_duplicate_audit_summary": completed_93_duplicate_audit.get("summary", {}),
            "completed_93class_leakage_clean_candidate_summary": completed_93_leakage_clean.get("summary", {}),
            "completed_93class_leakage_clean_candidate_inspection_summary": completed_93_leakage_clean_inspection.get("summary", {}),
            "completed_93class_leakage_clean_candidate_duplicate_audit_summary": completed_93_leakage_clean_duplicate_audit.get("summary", {}),
            "detection_annotation_package_summary": detection_annotation_package.get("summary", {}),
            "detection_annotation_validation_summary": detection_annotation_validation.get("summary", {}),
            "detection_annotation_contact_sheet_summary": detection_contact_sheet.get("summary", {}),
        },
        "training": {
            "config_path": training_config_path,
            "config": training_config,
            "weights_dir": "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights",
            "note": "CPU 5 epoch strict 分类阶段实验；不是目标检测训练。",
            "completed_93class": {
                "config_path": completed_93_config_path,
                "config": completed_93_config,
                "weights_dir": "runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights",
                "note": "CPU 1 epoch 93 类补齐覆盖实验；大腹皮由原始 val-only 样本确定性重划 train/val。",
            },
        },
        "evaluation": {
            "metrics": metrics,
            "completed_93class_metrics": completed_93_metrics,
            "error_analysis_summary": error_analysis.get("summary", {}),
            "review_samples": {
                "confusion_samples": len(review_samples.get("confusion_samples", [])) if review_samples else 0,
                "worst_class_samples": len(review_samples.get("worst_class_samples", [])) if review_samples else 0,
                "figures": review_figures,
            },
            "benchmark": benchmark,
            "backend_qa": backend_qa.get("summary", {}),
            "frontend_qa": frontend_qa.get("summary", {}),
            "smoke_check": smoke.get("summary", {}),
        },
        "reproduction_commands": repro_commands,
        "artifacts": [artifact_entry(path) for path in artifacts],
        "boundaries": [
            "当前真实实验是分类任务，只能汇报 Top-1 / Top-5、每类误判分析、推理延迟和工程 QA。",
            "原始数据不含真实 bbox 标注，不能汇报检测 Precision、Recall、mAP 或定位能力。",
            "strict 5 epoch 基准保持 92 类原始 train/val 交集；93 类补齐实验仅用于证明大腹皮已可进入训练链路。",
            "93 类补齐实验将大腹皮 19 张原始 val-only 样本按确定性顺序拆为 15 train / 4 val，不应与原始 92 类 strict 指标直接等价比较。",
            "检测标注准备包只包含待人工标注图片、类别顺序和 manifest；当前校验报告为 pending_bbox_annotation，labels/ 仍为空，不能据此训练检测模型或汇报检测指标。",
            "重复与泄漏审计只检查文件字节级 SHA256 完全重复；已发现 train/val exact duplicate 和跨类别 exact duplicate，需人工复核后再删除或重划。",
            "classification_leakage_review_package 是删除或重划前的人工复核包，只提供复核清单和对照图，不改变数据集。",
            "leakage_clean_candidate 数据集只移除 val 侧 train/val exact duplicate 副本，不自动裁决跨类别标签；重新训练前仍需单独审计和报告新指标。",
            "classification_cross_class_review_package 只提供跨类别 exact duplicate 人工复核清单和对照图，不自动删除、移动、重命名或重标图片。",
            "classification_cross_class_decision_table 是跨类别标签冲突的人工决策输入表，当前默认 pending，不自动执行任何数据修改。",
            "classification_cross_class_decision_review.html 是本地静态复核页，只辅助人工查看图片和复制决策字段，不写回 CSV，也不自动裁决类别。",
            "classification_cross_class_cleanup_plan 是人工决策 CSV 的执行前校验报告；只在校验通过时生成可审计操作清单，本身不修改数据集。",
            "apply_classification_cross_class_cleanup_plan 是人工决策和计划校验通过后的非破坏性执行入口；当前计划未就绪时会阻断，真正执行也只写入新的输出目录。",
        ],
    }


def write_markdown(manifest: dict[str, Any], output: Path) -> None:
    env = manifest["environment"]
    dataset = manifest["dataset"]
    evaluation = manifest["evaluation"]
    training = manifest["training"]
    strict = dataset["strict_summary"]
    strict_duplicates = dataset.get("strict_duplicate_audit_summary", {})
    leakage_review = dataset.get("classification_leakage_review_summary", {})
    leakage_clean = dataset.get("classification_leakage_clean_candidate_summary", {})
    leakage_clean_inspection = dataset.get("classification_leakage_clean_candidate_inspection_summary", {})
    leakage_clean_duplicates = dataset.get("classification_leakage_clean_candidate_duplicate_audit_summary", {})
    cross_class_review = dataset.get("classification_cross_class_review_summary", {})
    cross_class_decision = dataset.get("classification_cross_class_decision_table_summary", {})
    cross_class_cleanup = dataset.get("classification_cross_class_cleanup_plan_summary", {})
    class_summary = dataset["class_consistency_summary"]
    completed_93 = dataset.get("completed_93class_summary", {})
    completed_93_inspection = dataset.get("completed_93class_inspection_summary", {})
    completed_93_duplicates = dataset.get("completed_93class_duplicate_audit_summary", {})
    completed_93_leakage_clean = dataset.get("completed_93class_leakage_clean_candidate_summary", {})
    completed_93_leakage_clean_inspection = dataset.get("completed_93class_leakage_clean_candidate_inspection_summary", {})
    completed_93_leakage_clean_duplicates = dataset.get("completed_93class_leakage_clean_candidate_duplicate_audit_summary", {})
    detection_annotation = dataset.get("detection_annotation_package_summary", {})
    detection_validation = dataset.get("detection_annotation_validation_summary", {})
    metrics = evaluation["metrics"]
    completed_93_metrics = evaluation.get("completed_93class_metrics", {})
    benchmark = evaluation["benchmark"]
    smoke = evaluation["smoke_check"]

    lines = [
        "# 可复现实验 Manifest",
        "",
        f"- 生成时间: {manifest['generated_at']}",
        f"- 项目目录: `{manifest['project_root']}`",
        "",
        "## 环境",
        "",
        f"- Python: {env['python_version']}",
        f"- Python executable: `{env['python_executable']}`",
        f"- Platform: {env['platform']}",
        "",
        "| 包 | 版本 |",
        "|---|---|",
    ]
    for name, version in env["packages"].items():
        lines.append(f"| {name} | {version or '未安装'} |")

    lines.extend(
        [
            "",
            "## 数据与类别边界",
            "",
            f"- strict 数据集: {strict.get('classes')} 类，train {strict.get('train_images')} / val {strict.get('val_images')} / total {strict.get('total_images')}，verified {strict.get('verified_images')}，errors {strict.get('errors')}，warnings {strict.get('warnings')}",
            f"- strict 重复/泄漏审计: 状态 `{strict_duplicates.get('status')}`，重复 SHA256 组 {strict_duplicates.get('duplicate_hashes')}，train/val 泄漏组 {strict_duplicates.get('train_val_leak_hashes')}，跨类别重复组 {strict_duplicates.get('cross_class_duplicate_hashes')}",
            f"- 泄漏人工复核包: 状态 `{leakage_review.get('status')}`，覆盖 {leakage_review.get('leakage_groups')} / {leakage_review.get('expected_leakage_groups')} 组 train/val 泄漏，涉及记录 {leakage_review.get('leakage_records')}，跨类别泄漏组 {leakage_review.get('cross_class_leakage_groups')}，对照图 `classification_train_val_leakage_contact_sheet.png`",
            f"- strict 候选泄漏清理集: 状态 `{leakage_clean.get('status')}`，移除 val 副本 {leakage_clean.get('removed_images')} 张，输出 train {leakage_clean_inspection.get('train_images')} / val {leakage_clean_inspection.get('val_images')} / total {leakage_clean_inspection.get('total_images')}，train/val 泄漏组 {leakage_clean_duplicates.get('train_val_leak_hashes')}，跨类别重复组 {leakage_clean_duplicates.get('cross_class_duplicate_hashes')}",
            f"- 跨类别 exact duplicate 复核包: 状态 `{cross_class_review.get('status')}`，覆盖 {cross_class_review.get('cross_class_groups')} / {cross_class_review.get('expected_cross_class_groups')} 组，涉及记录 {cross_class_review.get('cross_class_records')}，train/val 泄漏组 {cross_class_review.get('train_val_leak_groups')}，对照图 `classification_cross_class_contact_sheet.png`",
            f"- 跨类别标签冲突决策表: 状态 `{cross_class_decision.get('status')}`，待决策 {cross_class_decision.get('pending_decisions')} / {cross_class_decision.get('groups')} 组，已决策 {cross_class_decision.get('decided_groups')} 组，校验错误 {cross_class_decision.get('validation_errors')}",
            f"- 跨类别清理计划校验: 状态 `{cross_class_cleanup.get('status')}`，待决策 {cross_class_cleanup.get('pending_decisions')} / {cross_class_cleanup.get('groups')} 组，计划操作 {cross_class_cleanup.get('planned_operations')}，校验错误 {cross_class_cleanup.get('validation_errors')}",
            f"- 类别一致性: 原始 {class_summary.get('raw_classes')} 类，strict {class_summary.get('strict_classes')} 类，状态 `{class_summary.get('status')}`",
            f"- 未纳入 strict 类别: {', '.join(class_summary.get('classes_missing_from_strict', [])) or '无'}",
            f"- zero-train 类别: {', '.join(class_summary.get('zero_train_classes', [])) or '无'}",
            f"- 93 类补齐实验: 输出 {completed_93.get('output_classes')} 类，train {completed_93.get('train_images')} / val {completed_93.get('val_images')} / total {completed_93.get('total_images')}，verified {completed_93_inspection.get('verified_images')}，errors {completed_93_inspection.get('errors')}，warnings {completed_93_inspection.get('warnings')}",
            f"- 93 类补齐重划类别: {', '.join(completed_93.get('rebalanced_classes', [])) or '无'}；大腹皮 15 train / 4 val",
            f"- 93 类重复/泄漏审计: 状态 `{completed_93_duplicates.get('status')}`，重复 SHA256 组 {completed_93_duplicates.get('duplicate_hashes')}，train/val 泄漏组 {completed_93_duplicates.get('train_val_leak_hashes')}，跨类别重复组 {completed_93_duplicates.get('cross_class_duplicate_hashes')}",
            f"- 93 类候选泄漏清理集: 状态 `{completed_93_leakage_clean.get('status')}`，移除 val 副本 {completed_93_leakage_clean.get('removed_images')} 张，输出 train {completed_93_leakage_clean_inspection.get('train_images')} / val {completed_93_leakage_clean_inspection.get('val_images')} / total {completed_93_leakage_clean_inspection.get('total_images')}，train/val 泄漏组 {completed_93_leakage_clean_duplicates.get('train_val_leak_hashes')}，跨类别重复组 {completed_93_leakage_clean_duplicates.get('cross_class_duplicate_hashes')}",
            f"- 检测标注准备包: 状态 `{detection_annotation.get('status')}`，覆盖 {detection_annotation.get('classes')} 类，待标注图片 {detection_annotation.get('images')} 张，预期标签 {detection_annotation.get('labels_expected')} 个，已完成标签 {detection_annotation.get('labels_completed')} 个",
            f"- 标注抽样: 每类 {detection_annotation.get('samples_per_class')} 张，来源 train {detection_annotation.get('source_split_counts', {}).get('train')} / val {detection_annotation.get('source_split_counts', {}).get('val')}；当前 labels/ 为空，不可直接训练检测模型",
            f"- 标注包校验: 状态 `{detection_validation.get('status')}`，图片 {detection_validation.get('images_present')} / {detection_validation.get('images_expected')}，缺失标签 {detection_validation.get('labels_missing')}，errors {detection_validation.get('errors')}，warnings {detection_validation.get('warnings')}",
            "",
            "## 训练与评估摘要",
            "",
            f"- 训练配置: `{training['config_path']}`",
            f"- 模型: `{training['config'].get('model')}`，epochs {training['config'].get('epochs')}，imgsz {training['config'].get('imgsz')}，batch {training['config'].get('batch')}，device `{training['config'].get('device')}`",
            f"- Top-1: {metrics.get('top1')}",
            f"- Top-5: {metrics.get('top5')}",
            f"- Fitness: {metrics.get('fitness')}",
            f"- benchmark: {benchmark.get('images')} 张，mean {benchmark.get('latency_ms_mean')} ms/image，FPS {benchmark.get('fps_mean')}",
            f"- smoke check: {smoke.get('passed')} / {smoke.get('total')} 通过，failed {smoke.get('failed')}",
            "",
            "## 93 类补齐实验摘要",
            "",
            f"- 训练配置: `{training['completed_93class']['config_path']}`",
            f"- 模型: `{training['completed_93class']['config'].get('model')}`，epochs {training['completed_93class']['config'].get('epochs')}，imgsz {training['completed_93class']['config'].get('imgsz')}，batch {training['completed_93class']['config'].get('batch')}，device `{training['completed_93class']['config'].get('device')}`",
            f"- Top-1: {completed_93_metrics.get('top1')}",
            f"- Top-5: {completed_93_metrics.get('top5')}",
            f"- Fitness: {completed_93_metrics.get('fitness')}",
            f"- 边界: 该 1 epoch 结果证明 93 类覆盖链路可运行，不替代 92 类 strict 5 epoch 基准。",
            "",
            "## 复现命令",
            "",
            "```powershell",
            "cd D:\\AAA中药cv\\yolo12_tcm_project",
        ]
    )
    lines.extend(manifest["reproduction_commands"])
    lines.extend(["```", "", "## 关键产物哈希", "", "| 路径 | bytes | SHA256 |", "|---|---:|---|"])
    for item in manifest["artifacts"]:
        if item.get("exists"):
            lines.append(f"| `{item['path']}` | {item.get('bytes', '')} | `{item.get('sha256', '')}` |")
        else:
            lines.append(f"| `{item['path']}` | missing | missing |")

    lines.extend(["", "## 边界说明", ""])
    for item in manifest["boundaries"]:
        lines.append(f"- {item}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a reproducibility manifest for the strict classification experiment.")
    parser.add_argument("--output", default="reports/repro_manifest.json")
    parser.add_argument("--markdown", default="reports/repro_manifest.md")
    args = parser.parse_args()

    manifest = build_manifest()
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown = resolve_project_path(args.markdown)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(manifest, markdown)
    print(json.dumps({"artifacts": len(manifest["artifacts"]), "commands": len(manifest["reproduction_commands"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
