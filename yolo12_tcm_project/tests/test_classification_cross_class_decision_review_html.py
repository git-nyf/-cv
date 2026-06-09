from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_classification_cross_class_decision_review_html import build_html


def test_build_html_contains_images_fields_and_copy_controls(tmp_path: Path):
    image_a = tmp_path / "data" / "train" / "类A" / "same.jpg"
    image_b = tmp_path / "data" / "train" / "类B" / "same.jpg"
    image_a.parent.mkdir(parents=True, exist_ok=True)
    image_b.parent.mkdir(parents=True, exist_ok=True)
    image_a.write_bytes(b"a")
    image_b.write_bytes(b"a")
    review = {
        "summary": {"status": "complete_review_package"},
        "groups": [
            {
                "group_id": "cross_class_001",
                "sha256_short": "abc123",
                "record_count": 2,
                "classes": ["类A", "类B"],
                "records": [
                    {
                        "split": "train",
                        "class_name": "类A",
                        "filename": "same.jpg",
                        "relative_path": "train\\类A\\same.jpg",
                        "path": str(image_a),
                        "exists": True,
                        "bytes": 1,
                    },
                    {
                        "split": "train",
                        "class_name": "类B",
                        "filename": "same.jpg",
                        "relative_path": "train\\类B\\same.jpg",
                        "path": str(image_b),
                        "exists": True,
                        "bytes": 1,
                    },
                ],
            }
        ],
    }
    table = {
        "decisions": [
            {
                "group_id": "cross_class_001",
                "decision_status": "pending",
                "chosen_class": "",
                "action": "",
                "remove_relative_paths": [],
                "move_to_class": "",
                "reviewer": "",
                "reviewed_at": "",
                "decision_note": "",
            }
        ]
    }
    review_path = tmp_path / "review.json"
    table_path = tmp_path / "table.json"
    output = tmp_path / "reports" / "review.html"
    review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    table_path.write_text(json.dumps(table, ensure_ascii=False), encoding="utf-8")

    html = build_html(review_path, table_path, None, output)

    assert "跨类别标签冲突人工决策复核页" in html
    assert "cross_class_001" in html
    assert "train/类A/same.jpg" in html
    assert "train/类B/same.jpg" in html
    assert 'data-field="decision_status"' in html
    assert 'data-field="chosen_class"' in html
    assert 'data-copy-row' in html
    assert 'data-copy-remove' in html
    assert "只辅助人工填写，不自动修改 CSV 或数据集" in html
