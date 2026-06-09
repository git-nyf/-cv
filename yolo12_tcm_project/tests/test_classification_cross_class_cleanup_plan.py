from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_classification_cross_class_cleanup_plan import build_cleanup_plan


def write_table(tmp_path: Path, decisions: list[dict]) -> Path:
    table = {
        "schema_version": 1,
        "summary": {"status": "ready_for_manual_decision"},
        "decisions": decisions,
    }
    path = tmp_path / "decision_table.json"
    path.write_text(json.dumps(table, ensure_ascii=False), encoding="utf-8")
    return path


def base_decision(**updates) -> dict:
    decision = {
        "group_id": "cross_class_001",
        "sha256": "abc123",
        "sha256_short": "abc123",
        "risk_level": "label_conflict",
        "record_count": 2,
        "splits": {"train": 2},
        "classes": ["类A", "类B"],
        "record_relative_paths": [
            str(Path("train") / "类A" / "same.jpg"),
            str(Path("train") / "类B" / "same.jpg"),
        ],
        "record_summary": [
            {
                "split": "train",
                "class_name": "类A",
                "relative_path": str(Path("train") / "类A" / "same.jpg"),
                "path": "",
                "exists": True,
            },
            {
                "split": "train",
                "class_name": "类B",
                "relative_path": str(Path("train") / "类B" / "same.jpg"),
                "path": "",
                "exists": True,
            },
        ],
        "suggested_action": "人工核对图片真实类别。",
        "decision_status": "pending",
        "chosen_class": "",
        "action": "",
        "remove_relative_paths": [],
        "move_to_class": "",
        "reviewer": "",
        "reviewed_at": "",
        "decision_note": "",
    }
    decision.update(updates)
    return decision


def test_pending_table_waits_for_manual_decisions(tmp_path: Path):
    table_path = write_table(tmp_path, [base_decision()])

    plan = build_cleanup_plan(table_path)

    assert plan["summary"]["status"] == "waiting_for_manual_decisions"
    assert plan["summary"]["pending_decisions"] == 1
    assert plan["summary"]["decided_groups"] == 0
    assert plan["summary"]["planned_operations"] == 0
    assert plan["validation_errors"] == []


def test_decided_keep_chosen_class_creates_remove_operation(tmp_path: Path):
    remove_path = str(Path("train") / "类B" / "same.jpg")
    table_path = write_table(
        tmp_path,
        [
            base_decision(
                decision_status="decided",
                chosen_class="类A",
                action="keep_chosen_class_remove_others",
                remove_relative_paths=[remove_path],
                reviewer="tester",
                reviewed_at="2026-06-07",
                decision_note="类A 目录为真实类别。",
            )
        ],
    )

    plan = build_cleanup_plan(table_path)

    assert plan["summary"]["status"] == "ready_for_cleanup_execution"
    assert plan["summary"]["planned_operations"] == 1
    assert plan["summary"]["planned_remove_operations"] == 1
    assert plan["operations"][0]["operation"] == "remove"
    assert plan["operations"][0]["relative_path"] == remove_path
    assert plan["operations"][0]["reason"] == "cross_class_exact_duplicate_not_chosen"


def test_decided_rows_require_metadata_and_valid_remove_paths(tmp_path: Path):
    table_path = write_table(
        tmp_path,
        [
            base_decision(
                decision_status="decided",
                chosen_class="类A",
                action="keep_chosen_class_remove_others",
                remove_relative_paths=[str(Path("train") / "类A" / "same.jpg")],
            )
        ],
    )

    plan = build_cleanup_plan(table_path)

    assert plan["summary"]["status"] == "invalid_cleanup_plan"
    assert plan["summary"]["validation_errors"] >= 3
    assert any("reviewer" in error for error in plan["validation_errors"])
    assert any("reviewed_at" in error for error in plan["validation_errors"])
    assert any("decision_note" in error for error in plan["validation_errors"])
    assert any("must not remove chosen_class" in error for error in plan["validation_errors"])
