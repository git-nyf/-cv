from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_yolo_dataset import validate


def test_validate_tiny_yolo_dataset(tmp_path: Path):
    images = tmp_path / "images"
    labels = tmp_path / "labels"
    images.mkdir()
    labels.mkdir()
    Image.new("RGB", (64, 64), "white").save(images / "a.jpg")
    (labels / "a.txt").write_text("0 0.5 0.5 0.4 0.4\n", encoding="utf-8")

    report = validate(images, labels, None, None)

    assert report["summary"]["images"] == 1
    assert report["summary"]["errors"] == 0
    assert report["box_distribution"][0] == 1

