from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_detection_annotation_package import validate_package


def make_package(root: Path, with_label: bool) -> Path:
    package = root / "package"
    images = package / "images"
    labels = package / "labels"
    images.mkdir(parents=True)
    labels.mkdir()
    image = images / "000_train_01_sample.jpg"
    Image.new("RGB", (80, 60), "white").save(image)
    import hashlib

    digest = hashlib.sha256(image.read_bytes()).hexdigest()
    manifest = {
        "classes": ["样本类"],
        "samples": [
            {
                "image_id": "000_train_01_sample",
                "class_index": 0,
                "class_name": "样本类",
                "source_split": "train",
                "source_path": str(image),
                "package_image": str(image),
                "yolo_label": str(labels / "000_train_01_sample.txt"),
                "width": 80,
                "height": 60,
                "sha256": digest,
                "annotation_status": "pending",
            }
        ],
    }
    (package / "classes.txt").write_text("样本类\n", encoding="utf-8")
    (package / "annotation_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    if with_label:
        (labels / "000_train_01_sample.txt").write_text("0 0.5 0.5 0.4 0.4\n", encoding="utf-8")
    return package


def test_validate_pending_annotation_package(tmp_path: Path):
    report = validate_package(make_package(tmp_path, with_label=False))

    assert report["summary"]["status"] == "pending_bbox_annotation"
    assert report["summary"]["labels_completed"] == 0
    assert report["summary"]["labels_missing"] == 1
    assert report["summary"]["errors"] == 0


def test_validate_complete_annotation_package(tmp_path: Path):
    report = validate_package(make_package(tmp_path, with_label=True), require_complete=True)

    assert report["summary"]["status"] == "complete"
    assert report["summary"]["labels_completed"] == 1
    assert report["summary"]["labels_missing"] == 0
    assert report["summary"]["boxes"] == 1
    assert report["summary"]["errors"] == 0
