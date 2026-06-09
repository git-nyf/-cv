from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_classification_duplicates import audit
from generate_classification_cross_class_review_package import build_payload


def test_build_payload_extracts_cross_class_duplicates(tmp_path: Path):
    source = tmp_path / "data"
    train_a = source / "train" / "类A"
    train_b = source / "train" / "类B"
    val_a = source / "val" / "类A"
    for path in [train_a, train_b, val_a]:
        path.mkdir(parents=True)

    cross_class = train_a / "same_a.jpg"
    Image.new("RGB", (32, 32), "white").save(cross_class)
    shutil.copyfile(cross_class, train_b / "same_b.jpg")

    train_val_same_class = train_a / "leak_train.jpg"
    Image.new("RGB", (32, 32), "black").save(train_val_same_class)
    shutil.copyfile(train_val_same_class, val_a / "leak_val.jpg")

    audit_path = tmp_path / "audit.json"
    audit_report = audit(source, max_groups=10)
    audit_path.write_text(json.dumps(audit_report, ensure_ascii=False), encoding="utf-8")

    payload = build_payload(audit_path, audit_path, tmp_path / "figure.png")
    summary = payload["summary"]
    groups = payload["groups"]

    assert summary["status"] == "complete_review_package"
    assert summary["cross_class_groups"] == 1
    assert summary["expected_cross_class_groups"] == 1
    assert summary["cross_class_records"] == 2
    assert summary["train_records"] == 2
    assert summary["val_records"] == 0
    assert summary["train_val_leak_groups"] == 0
    assert summary["shared_with_reference_cross_class_hashes"] == 1
    assert len(groups) == 1
    assert groups[0]["group_id"] == "cross_class_001"
    assert groups[0]["risk_level"] == "label_conflict"
    assert groups[0]["manual_decision"] == ""
    assert groups[0]["classes"] == ["类A", "类B"]
    assert {record["split"] for record in groups[0]["records"]} == {"train"}
