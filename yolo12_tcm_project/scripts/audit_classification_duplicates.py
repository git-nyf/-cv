from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from path_utils import IMAGE_EXTS, resolve_project_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_classification_images(source: Path) -> list[Path]:
    paths: list[Path] = []
    for split in ("train", "val", "test"):
        split_root = source / split
        if not split_root.exists():
            continue
        for class_dir in sorted((p for p in split_root.iterdir() if p.is_dir()), key=lambda p: p.name):
            paths.extend(
                sorted(
                    (p for p in class_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS),
                    key=lambda p: str(p),
                )
            )
    return paths


def image_record(path: Path, source: Path) -> dict[str, Any]:
    relative = path.relative_to(source)
    split = relative.parts[0] if len(relative.parts) >= 1 else ""
    class_name = relative.parts[1] if len(relative.parts) >= 2 else ""
    return {
        "path": str(path),
        "relative_path": str(relative),
        "split": split,
        "class_name": class_name,
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def group_entry(digest: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    splits = sorted({item["split"] for item in records})
    classes = sorted({item["class_name"] for item in records})
    return {
        "sha256": digest,
        "count": len(records),
        "splits": splits,
        "classes": classes,
        "cross_split": len(splits) > 1,
        "cross_class": len(classes) > 1,
        "train_val_leak": "train" in splits and "val" in splits,
        "records": records,
    }


def audit(source: Path, max_groups: int = 50) -> dict[str, Any]:
    source = source.resolve()
    records = [image_record(path, source) for path in iter_classification_images(source)]
    by_hash: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_hash.setdefault(record["sha256"], []).append(record)

    duplicate_groups = [group_entry(digest, items) for digest, items in by_hash.items() if len(items) > 1]
    duplicate_groups.sort(
        key=lambda item: (
            not item["train_val_leak"],
            not item["cross_class"],
            -int(item["count"]),
            item["sha256"],
        )
    )
    train_val_leaks = [item for item in duplicate_groups if item["train_val_leak"]]
    cross_class = [item for item in duplicate_groups if item["cross_class"]]
    cross_split = [item for item in duplicate_groups if item["cross_split"]]

    if train_val_leaks or cross_class:
        status = "needs_leakage_review"
    elif duplicate_groups:
        status = "duplicates_found"
    else:
        status = "clean_exact_hash"

    split_counts: dict[str, int] = {}
    class_counts: dict[str, int] = {}
    for record in records:
        split_counts[record["split"]] = split_counts.get(record["split"], 0) + 1
        class_counts[record["class_name"]] = class_counts.get(record["class_name"], 0) + 1

    return {
        "source": str(source),
        "summary": {
            "status": status,
            "total_images": len(records),
            "unique_hashes": len(by_hash),
            "duplicate_hashes": len(duplicate_groups),
            "duplicate_images": sum(int(item["count"]) for item in duplicate_groups),
            "duplicate_extra_images": sum(int(item["count"]) - 1 for item in duplicate_groups),
            "cross_split_duplicate_hashes": len(cross_split),
            "train_val_leak_hashes": len(train_val_leaks),
            "cross_class_duplicate_hashes": len(cross_class),
            "classes": len(class_counts),
            "splits": split_counts,
            "reported_groups": min(len(duplicate_groups), max_groups),
        },
        "duplicate_groups": duplicate_groups[:max_groups],
        "boundary_note": "该审计只检查文件字节级 SHA256 完全重复；不包含近似重复、裁剪相似或感知哈希判断。",
        "recommended_actions": [
            "优先人工复核 train/val exact duplicate，避免验证集泄漏导致指标偏乐观。",
            "若同一 SHA256 跨类别出现，优先检查目录标签是否混入或类别命名是否冲突。",
            "确认后再删除或重划样本；不要仅凭本报告自动删图。",
        ],
    }


def write_markdown(report: dict[str, Any], output: Path) -> None:
    summary = report["summary"]
    lines = [
        "# 分类数据重复与泄漏审计报告",
        "",
        f"- 数据路径: `{report['source']}`",
        f"- 状态: `{summary['status']}`",
        f"- 总图片: {summary['total_images']}",
        f"- 唯一 SHA256: {summary['unique_hashes']}",
        f"- 重复 SHA256 组: {summary['duplicate_hashes']}",
        f"- 重复图片数: {summary['duplicate_images']}，额外重复图: {summary['duplicate_extra_images']}",
        f"- 跨划分重复组: {summary['cross_split_duplicate_hashes']}",
        f"- train/val 泄漏组: {summary['train_val_leak_hashes']}",
        f"- 跨类别重复组: {summary['cross_class_duplicate_hashes']}",
        "",
        "## 边界说明",
        "",
        report["boundary_note"],
        "",
        "## 建议动作",
        "",
    ]
    for item in report["recommended_actions"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 重复组样例",
            "",
            "| SHA256 | count | splits | classes | train/val leak | paths |",
            "|---|---:|---|---|---|---|",
        ]
    )
    if report["duplicate_groups"]:
        for group in report["duplicate_groups"]:
            paths = "<br>".join(f"`{item['relative_path']}`" for item in group["records"])
            lines.append(
                f"| `{group['sha256'][:16]}...` | {group['count']} | {', '.join(group['splits'])} | {', '.join(group['classes'])} | {group['train_val_leak']} | {paths} |"
            )
    else:
        lines.append("| 无 | 0 | - | - | False | - |")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit exact duplicate images and train/val leakage in a classification dataset.")
    parser.add_argument("--source", required=True, help="Classification dataset root with train/class and val/class directories.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--max-groups", type=int, default=50)
    args = parser.parse_args()

    report = audit(resolve_project_path(args.source), max_groups=args.max_groups)
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown = resolve_project_path(args.markdown)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, markdown)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
