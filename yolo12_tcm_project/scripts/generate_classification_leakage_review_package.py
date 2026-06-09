from __future__ import annotations

import argparse
import json
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from path_utils import resolve_project_path


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in [Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf"), Path("C:/Windows/Fonts/simsun.ttc")]:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        return ImageOps.contain(image.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    width: int,
    line_height: int,
) -> None:
    x, y = xy
    for line in textwrap.wrap(text, width=width, break_long_words=True, replace_whitespace=False) or [""]:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def image_size(path: Path) -> list[int] | None:
    try:
        with Image.open(path) as image:
            return [int(image.width), int(image.height)]
    except Exception:
        return None


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    path = Path(record["path"])
    return {
        "split": record.get("split", ""),
        "class_name": record.get("class_name", ""),
        "filename": record.get("filename", path.name),
        "relative_path": record.get("relative_path", ""),
        "path": str(path),
        "exists": path.exists(),
        "bytes": record.get("bytes", path.stat().st_size if path.exists() else None),
        "image_size": image_size(path) if path.exists() else None,
    }


def suggested_action(group: dict[str, Any]) -> str:
    if group.get("cross_class"):
        return "先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。"
    return "确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。"


def build_review_groups(audit: dict[str, Any]) -> list[dict[str, Any]]:
    leak_groups = [group for group in audit.get("duplicate_groups", []) if group.get("train_val_leak")]
    groups: list[dict[str, Any]] = []
    for index, group in enumerate(leak_groups, start=1):
        records = [normalize_record(record) for record in group.get("records", [])]
        split_counts = Counter(record["split"] for record in records)
        groups.append(
            {
                "group_id": f"leak_{index:03d}",
                "sha256": group.get("sha256", ""),
                "sha256_short": str(group.get("sha256", ""))[:16],
                "record_count": len(records),
                "train_records": int(split_counts.get("train", 0)),
                "val_records": int(split_counts.get("val", 0)),
                "classes": sorted({record["class_name"] for record in records}),
                "cross_class": bool(group.get("cross_class")),
                "risk_level": "high_label_and_split_leak" if group.get("cross_class") else "split_leak",
                "suggested_action": suggested_action(group),
                "manual_decision": "",
                "records": records,
            }
        )
    return groups


def build_payload(source_audit: Path, reference_audit: Path | None, figure: Path) -> dict[str, Any]:
    source_payload = read_json(source_audit)
    groups = build_review_groups(source_payload)
    split_counts = Counter(record["split"] for group in groups for record in group["records"])
    class_counts = Counter(class_name for group in groups for class_name in group["classes"])
    reference_summary: dict[str, Any] = {}
    shared_leak_hashes = None
    if reference_audit and reference_audit.exists():
        reference_payload = read_json(reference_audit)
        reference_summary = reference_payload.get("summary", {})
        reference_hashes = {group.get("sha256") for group in reference_payload.get("duplicate_groups", []) if group.get("train_val_leak")}
        source_hashes = {group["sha256"] for group in groups}
        shared_leak_hashes = len(source_hashes & reference_hashes)

    expected_leaks = int(source_payload.get("summary", {}).get("train_val_leak_hashes", 0))
    status = "complete_review_package" if expected_leaks == len(groups) else "incomplete_review_package"
    summary = {
        "status": status,
        "source_audit_status": source_payload.get("summary", {}).get("status"),
        "source_total_images": source_payload.get("summary", {}).get("total_images"),
        "leakage_groups": len(groups),
        "expected_leakage_groups": expected_leaks,
        "leakage_records": sum(group["record_count"] for group in groups),
        "train_records": int(split_counts.get("train", 0)),
        "val_records": int(split_counts.get("val", 0)),
        "same_class_leakage_groups": sum(1 for group in groups if not group["cross_class"]),
        "cross_class_leakage_groups": sum(1 for group in groups if group["cross_class"]),
        "classes_involved": len(class_counts),
        "shared_with_reference_leak_hashes": shared_leak_hashes,
        "figure": str(figure),
    }
    return {
        "source_audit": str(source_audit),
        "reference_audit": str(reference_audit) if reference_audit else None,
        "summary": summary,
        "reference_summary": reference_summary,
        "groups": groups,
        "boundary_note": "该复核包只整理 train/val 字节级 exact duplicate 风险，不自动删除、移动或重划任何图片。",
        "review_instructions": [
            "优先处理 risk_level 为 high_label_and_split_leak 的组，因为它同时涉及验证泄漏和跨类别标签冲突。",
            "人工确认图片内容和类别目录后，再决定删除副本、移动样本或重建无泄漏划分。",
            "完成处理后必须重新运行 duplicate audit、训练和独立验证，旧指标不能作为无泄漏基准。",
        ],
    }


def record_caption(record: dict[str, Any]) -> str:
    return f"{record['split']} | {record['class_name']}\n{record['filename']}\n{record['relative_path']}"


def make_contact_sheet(groups: list[dict[str, Any]], output: Path, title: str) -> None:
    font_title = load_font(30)
    font_subtitle = load_font(15)
    font_group = load_font(16)
    font_body = load_font(13)
    margin = 24
    gap = 12
    header_h = 86
    row_h = 218
    group_w = 320
    cell_w = 236
    thumb_size = (184, 128)
    columns = max((len(group["records"]) for group in groups), default=2)
    width = margin * 2 + group_w + gap + columns * cell_w + (columns - 1) * gap
    height = margin * 2 + header_h + len(groups) * row_h + max(0, len(groups) - 1) * gap
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, margin), title, font=font_title, fill="#1F4E79")
    draw.text((margin, margin + 42), "每行是一组 train/val exact duplicate；红色为同时跨类别，复核后再删除或重划。", font=font_subtitle, fill="#667085")

    for index, group in enumerate(groups):
        y = margin + header_h + index * (row_h + gap)
        bg = "#F8FAFC" if index % 2 == 0 else "#FFFFFF"
        risk_color = "#B42318" if group["cross_class"] else "#B7791F"
        draw.rectangle([margin, y, width - margin, y + row_h], fill=bg, outline="#D0D7DE", width=1)
        draw.rectangle([margin, y, margin + 8, y + row_h], fill=risk_color)
        group_text = (
            f"{group['group_id']}  {group['risk_level']}\n"
            f"sha256: {group['sha256_short']}...\n"
            f"records: {group['record_count']}  train/val: {group['train_records']}/{group['val_records']}\n"
            f"classes: {'、'.join(group['classes'])}"
        )
        draw_wrapped(draw, (margin + 18, y + 16), group_text, font_group, "#1F2933", 28, 22)
        draw_wrapped(draw, (margin + 18, y + 122), group["suggested_action"], font_body, "#475467", 30, 18)

        for col, record in enumerate(group["records"]):
            x = margin + group_w + gap + col * (cell_w + gap)
            border = "#2E75B6" if record["split"] == "train" else "#B7791F"
            image_path = Path(record["path"])
            image_y = y + 14
            try:
                thumb = fit_image(image_path, thumb_size)
                canvas.paste(thumb, (x + (thumb_size[0] - thumb.width) // 2, image_y + (thumb_size[1] - thumb.height) // 2))
            except Exception:
                draw.rectangle([x, image_y, x + thumb_size[0], image_y + thumb_size[1]], outline="#B42318", width=2)
                draw.text((x + 8, image_y + 8), "image load failed", font=font_body, fill="#B42318")
            draw.rectangle([x, image_y, x + thumb_size[0], image_y + thumb_size[1]], outline=border, width=3)
            draw_wrapped(draw, (x, image_y + thumb_size[1] + 8), record_caption(record), font_body, "#344054", 32, 17)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# 分类 train/val 泄漏人工复核包",
        "",
        f"- 来源审计: `{payload['source_audit']}`",
        f"- 状态: `{summary['status']}`",
        f"- train/val 泄漏组: {summary['leakage_groups']} / {summary['expected_leakage_groups']}",
        f"- 涉及文件记录: {summary['leakage_records']}，train {summary['train_records']} / val {summary['val_records']}",
        f"- 同类别泄漏组: {summary['same_class_leakage_groups']}",
        f"- 跨类别泄漏组: {summary['cross_class_leakage_groups']}",
        f"- 涉及类别数: {summary['classes_involved']}",
        f"- 复核对照图: `{summary['figure']}`",
        "",
        "## 边界说明",
        "",
        payload["boundary_note"],
        "",
        "## 复核建议",
        "",
    ]
    for item in payload["review_instructions"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 复核清单",
            "",
            "| group_id | risk_level | records | classes | train paths | val paths | suggested_action | manual_decision |",
            "|---|---|---:|---|---|---|---|---|",
        ]
    )
    for group in payload["groups"]:
        train_paths = "<br>".join(f"`{record['relative_path']}`" for record in group["records"] if record["split"] == "train") or "-"
        val_paths = "<br>".join(f"`{record['relative_path']}`" for record in group["records"] if record["split"] == "val") or "-"
        lines.append(
            f"| {group['group_id']} | {group['risk_level']} | {group['record_count']} | {'、'.join(group['classes'])} | {train_paths} | {val_paths} | {group['suggested_action']} |  |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a manual review package for classification train/val exact duplicate leakage.")
    parser.add_argument("--audit", default="reports/strict_classification_duplicate_audit.json")
    parser.add_argument("--reference-audit", default="reports/classification_93class_duplicate_audit.json")
    parser.add_argument("--output", default="reports/classification_leakage_review_package.json")
    parser.add_argument("--figure", default="reports/figures/classification_train_val_leakage_contact_sheet.png")
    args = parser.parse_args()

    audit = resolve_project_path(args.audit)
    reference_audit = resolve_project_path(args.reference_audit) if args.reference_audit else None
    output = resolve_project_path(args.output)
    figure = resolve_project_path(args.figure)

    payload = build_payload(audit, reference_audit, figure)
    make_contact_sheet(payload["groups"], figure, "分类 train/val 泄漏人工复核总览")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, output.with_suffix(".md"))
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
