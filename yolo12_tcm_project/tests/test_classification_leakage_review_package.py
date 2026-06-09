from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_classification_duplicates import audit
from generate_classification_leakage_review_package import build_payload


def test_build_payload_extracts_only_train_val_leaks(tmp_path: Path):
    source = tmp_path / "data"
    train_a = source / "train" / "类A"
    val_a = source / "val" / "类A"
    train_b = source / "train" / "类B"
    val_b = source / "val" / "类B"
    for path in [train_a, val_a, train_b, val_b]:
        path.mkdir(parents=True)

    leak = train_a / "leak.jpg"
    Image.new("RGB", (32, 32), "white").save(leak)
    shutil.copyfile(leak, val_b / "leak_val_cross_class.jpg")

    train_only = train_b / "train_only_1.jpg"
    Image.new("RGB", (32, 32), "black").save(train_only)
    shutil.copyfile(train_only, train_b / "train_only_2.jpg")

    audit_path = tmp_path / "audit.json"
    audit_report = audit(source, max_groups=10)
    audit_path.write_text(json.dumps(audit_report, ensure_ascii=False), encoding="utf-8")

    payload = build_payload(audit_path, audit_path, tmp_path / "figure.png")
    summary = payload["summary"]
    groups = payload["groups"]

    assert summary["status"] == "complete_review_package"
    assert summary["leakage_groups"] == 1
    assert summary["expected_leakage_groups"] == 1
    assert summary["leakage_records"] == 2
    assert summary["train_records"] == 1
    assert summary["val_records"] == 1
    assert summary["cross_class_leakage_groups"] == 1
    assert summary["same_class_leakage_groups"] == 0
    assert summary["shared_with_reference_leak_hashes"] == 1
    assert groups[0]["risk_level"] == "high_label_and_split_leak"
    assert groups[0]["manual_decision"] == ""
    assert {record["split"] for record in groups[0]["records"]} == {"train", "val"}
