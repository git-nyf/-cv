from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_classification_cross_class_cleanup_plan import apply_cleanup_plan


def write_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_plan(tmp_path: Path, status: str, operations: list[dict]) -> Path:
    plan = {
        "schema_version": 1,
        "summary": {
            "status": status,
            "validation_errors": 0,
            "planned_operations": len(operations),
            "planned_remove_operations": sum(1 for item in operations if item["operation"] == "remove"),
            "planned_move_operations": sum(1 for item in operations if item["operation"] == "move"),
        },
        "operations": operations,
        "validation_errors": [],
    }
    path = tmp_path / "cleanup_plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return path


def test_blocks_pending_cleanup_plan_without_writing_output(tmp_path: Path):
    source = tmp_path / "source"
    output = tmp_path / "output"
    write_file(source / "train" / "class_a" / "same.jpg", b"same")
    plan_path = write_plan(tmp_path, "waiting_for_manual_decisions", [])

    with pytest.raises(ValueError, match="ready_for_cleanup_execution"):
        apply_cleanup_plan(source, output, plan_path)

    assert not output.exists()


def test_applies_ready_plan_to_new_dataset_without_mutating_source(tmp_path: Path):
    source = tmp_path / "source"
    output = tmp_path / "output"
    keep_path = source / "train" / "class_a" / "same.jpg"
    move_path = source / "train" / "class_b" / "same.jpg"
    remove_path = source / "val" / "class_c" / "drop.jpg"
    untouched_path = source / "val" / "class_a" / "keep.jpg"
    write_file(keep_path, b"duplicate-bytes")
    write_file(move_path, b"duplicate-bytes")
    write_file(remove_path, b"remove-me")
    write_file(untouched_path, b"keep-me")
    plan_path = write_plan(
        tmp_path,
        "ready_for_cleanup_execution",
        [
            {
                "operation": "move",
                "group_id": "cross_class_001",
                "source_relative_path": str(Path("train") / "class_b" / "same.jpg"),
                "target_relative_path": str(Path("train") / "class_a" / "same.jpg"),
            },
            {
                "operation": "remove",
                "group_id": "cross_class_002",
                "relative_path": str(Path("val") / "class_c" / "drop.jpg"),
            },
        ],
    )

    report = apply_cleanup_plan(source, output, plan_path)

    assert report["summary"]["status"] == "cleanup_dataset_written"
    assert report["summary"]["source_images"] == 4
    assert report["summary"]["output_images"] == 2
    assert report["summary"]["removed_images"] == 1
    assert report["summary"]["merged_move_targets"] == 1
    assert (output / "train" / "class_a" / "same.jpg").read_bytes() == b"duplicate-bytes"
    assert (output / "val" / "class_a" / "keep.jpg").read_bytes() == b"keep-me"
    assert not (output / "train" / "class_b" / "same.jpg").exists()
    assert not (output / "val" / "class_c" / "drop.jpg").exists()
    assert keep_path.exists()
    assert move_path.exists()
    assert remove_path.exists()
    assert untouched_path.exists()


def test_rejects_output_inside_source_tree(tmp_path: Path):
    source = tmp_path / "source"
    write_file(source / "train" / "class_a" / "same.jpg", b"same")
    plan_path = write_plan(tmp_path, "ready_for_cleanup_execution", [])

    with pytest.raises(ValueError, match="outside the source dataset tree"):
        apply_cleanup_plan(source, source / "nested_output", plan_path)
