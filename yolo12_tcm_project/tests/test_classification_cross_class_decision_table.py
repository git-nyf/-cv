from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_classification_cross_class_decision_table import build_table


def make_review_package(tmp_path: Path) -> Path:
    review = {
        "summary": {"status": "complete_review_package"},
        "groups": [
            {
                "group_id": "cross_class_001",
                "sha256": "abc123",
                "sha256_short": "abc123",
                "risk_level": "label_conflict",
                "suggested_action": "人工核对图片真实类别。",
                "records": [
                    {
                        "split": "train",
                        "class_name": "类A",
                        "relative_path": "train\\类A\\same.jpg",
                        "path": str(tmp_path / "train" / "类A" / "same.jpg"),
                        "exists": True,
                    },
                    {
                        "split": "train",
                        "class_name": "类B",
                        "relative_path": "train\\类B\\same.jpg",
                        "path": str(tmp_path / "train" / "类B" / "same.jpg"),
                        "exists": True,
                    },
                ],
            }
        ],
    }
    path = tmp_path / "review.json"
    path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    return path


def test_build_table_creates_pending_decisions(tmp_path: Path):
    table = build_table(make_review_package(tmp_path))
    summary = table["summary"]
    decision = table["decisions"][0]

    assert summary["status"] == "ready_for_manual_decision"
    assert summary["groups"] == 1
    assert summary["records"] == 2
    assert summary["pending_decisions"] == 1
    assert summary["validation_errors"] == 0
    assert decision["group_id"] == "cross_class_001"
    assert decision["classes"] == ["类A", "类B"]
    assert decision["record_relative_paths"] == [
        str(Path("train") / "类A" / "same.jpg"),
        str(Path("train") / "类B" / "same.jpg"),
    ]
    assert decision["decision_status"] == "pending"
    assert decision["chosen_class"] == ""
    assert decision["action"] == ""


def test_build_table_preserves_existing_manual_fields(tmp_path: Path):
    review_path = make_review_package(tmp_path)
    existing = {
        "decisions": [
            {
                "group_id": "cross_class_001",
                "decision_status": "decided",
                "chosen_class": "类A",
                "action": "keep_chosen_class_remove_others",
                "remove_relative_paths": [str(Path("train") / "类B" / "same.jpg")],
                "reviewer": "tester",
                "reviewed_at": "2026-06-07",
                "decision_note": "类A is correct.",
            }
        ]
    }
    existing_path = tmp_path / "existing.json"
    existing_path.write_text(json.dumps(existing, ensure_ascii=False), encoding="utf-8")

    table = build_table(review_path, existing_path)
    decision = table["decisions"][0]

    assert table["summary"]["status"] == "ready_for_manual_decision"
    assert table["summary"]["pending_decisions"] == 0
    assert table["summary"]["decided_groups"] == 1
    assert decision["decision_status"] == "decided"
    assert decision["chosen_class"] == "类A"
    assert decision["action"] == "keep_chosen_class_remove_others"
    assert decision["remove_relative_paths"] == [str(Path("train") / "类B" / "same.jpg")]
    assert decision["reviewer"] == "tester"
    assert decision["decision_note"] == "类A is correct."
