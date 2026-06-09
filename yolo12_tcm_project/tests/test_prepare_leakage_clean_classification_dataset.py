from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from prepare_leakage_clean_classification_dataset import prepare_dataset


def write_image(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 32), color).save(path)


def test_prepare_dataset_removes_only_reviewed_val_duplicates(tmp_path: Path):
    source = tmp_path / "source"
    train_a = source / "train" / "类A"
    val_a = source / "val" / "类A"
    train_b = source / "train" / "类B"
    val_b = source / "val" / "类B"
    for path in [train_a, val_a, train_b, val_b]:
        path.mkdir(parents=True)

    leak_train = train_a / "leak_train.jpg"
    leak_val = val_b / "leak_val.jpg"
    write_image(leak_train, "white")
    shutil.copyfile(leak_train, leak_val)
    write_image(train_b / "train_only_a.jpg", "black")
    shutil.copyfile(train_b / "train_only_a.jpg", train_b / "train_only_b.jpg")
    write_image(val_a / "unique_val.jpg", "blue")

    review_package = {
        "summary": {"leakage_groups": 1},
        "groups": [
            {
                "records": [
                    {
                        "split": "train",
                        "relative_path": str(leak_train.relative_to(source)),
                    },
                    {
                        "split": "val",
                        "relative_path": str(leak_val.relative_to(source)),
                    },
                ]
            }
        ],
    }
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(review_package, ensure_ascii=False), encoding="utf-8")

    output = tmp_path / "clean"
    report = prepare_dataset(source, output, review_path, overwrite=True)
    summary = report["summary"]

    assert summary["status"] == "leakage_val_duplicates_removed"
    assert summary["source_images"] == 5
    assert summary["output_images"] == 4
    assert summary["removed_images"] == 1
    assert summary["requested_val_removals"] == 1
    assert summary["output_split_counts"] == {"train": 3, "val": 1}
    assert (output / "train" / "类A" / "leak_train.jpg").exists()
    assert not (output / "val" / "类B" / "leak_val.jpg").exists()
    assert (output / "train" / "类B" / "train_only_a.jpg").exists()
    assert (output / "train" / "类B" / "train_only_b.jpg").exists()
    assert report["removed_records"][0]["relative_path"] == str(Path("val") / "类B" / "leak_val.jpg")
    assert "不自动修改 train 图像" in report["boundary_note"]
