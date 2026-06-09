from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_classification_duplicates import audit


def test_audit_detects_train_val_and_cross_class_duplicates(tmp_path: Path):
    source = tmp_path / "data"
    train_a = source / "train" / "类A"
    val_a = source / "val" / "类A"
    train_b = source / "train" / "类B"
    val_b = source / "val" / "类B"
    for path in [train_a, val_a, train_b, val_b]:
        path.mkdir(parents=True)

    base = train_a / "base.jpg"
    Image.new("RGB", (32, 32), "white").save(base)
    shutil.copyfile(base, val_a / "same_in_val.jpg")
    shutil.copyfile(base, train_b / "same_in_other_class.jpg")
    Image.new("RGB", (32, 32), "black").save(val_b / "unique.jpg")

    report = audit(source)
    summary = report["summary"]

    assert summary["total_images"] == 4
    assert summary["unique_hashes"] == 2
    assert summary["duplicate_hashes"] == 1
    assert summary["duplicate_images"] == 3
    assert summary["duplicate_extra_images"] == 2
    assert summary["train_val_leak_hashes"] == 1
    assert summary["cross_class_duplicate_hashes"] == 1
    assert summary["status"] == "needs_leakage_review"
