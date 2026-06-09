from __future__ import annotations

import argparse
import json
import textwrap
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


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: str, width: int, line_height: int) -> None:
    x, y = xy
    for line in textwrap.wrap(text, width=width, break_long_words=True, replace_whitespace=False) or [""]:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height


def sample_caption(sample: dict[str, Any]) -> str:
    return (
        f"{sample['class_index']:03d} {sample['class_name']} [{sample['source_split']}]\n"
        f"{Path(sample['package_image']).name}\n"
        f"label: {Path(sample['yolo_label']).name}"
    )


def make_sheet(samples: list[dict[str, Any]], output: Path, title: str, columns: int, thumb_size: tuple[int, int]) -> None:
    font_title = load_font(30)
    font_body = load_font(14)
    margin = 24
    gap = 14
    header_h = 70
    label_h = 74
    cell_w = thumb_size[0]
    cell_h = thumb_size[1] + label_h
    rows = max(1, (len(samples) + columns - 1) // columns)
    width = margin * 2 + columns * cell_w + (columns - 1) * gap
    height = margin * 2 + header_h + rows * cell_h + (rows - 1) * gap
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, margin), title, font=font_title, fill="#1F4E79")
    draw.text((margin, margin + 40), "每类 3 张：train 2 + val 1；仅用于人工 bbox 标注前复核，labels/ 当前为空。", font=font_body, fill="#667085")

    for index, sample in enumerate(samples):
        row, col = divmod(index, columns)
        x = margin + col * (cell_w + gap)
        y = margin + header_h + row * (cell_h + gap)
        image_path = Path(sample["package_image"])
        try:
            thumb = fit_image(image_path, thumb_size)
            canvas.paste(thumb, (x + (thumb_size[0] - thumb.width) // 2, y + (thumb_size[1] - thumb.height) // 2))
        except Exception:
            draw.rectangle([x, y, x + thumb_size[0], y + thumb_size[1]], outline="#B42318", width=2)
            draw.text((x + 8, y + 8), "image load failed", font=font_body, fill="#B42318")
        draw.rectangle([x, y, x + thumb_size[0], y + thumb_size[1]], outline="#D0D7DE", width=1)
        draw_wrapped(draw, (x, y + thumb_size[1] + 6), sample_caption(sample), font_body, "#344054", 34, 17)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# 检测标注样本 contact sheet 索引",
        "",
        f"- 来源 manifest: `{payload['manifest']}`",
        f"- 样本总数: {payload['summary']['samples']}",
        f"- 类别数: {payload['summary']['classes']}",
        f"- contact sheet: `{payload['figure']}`",
        f"- 当前标签状态: `{payload['summary']['annotation_status']}`，已完成标签 {payload['summary']['labels_completed']} / {payload['summary']['labels_expected']}",
        "",
        "## 用途",
        "",
        "该图用于人工 bbox 标注前快速复核类别、抽样图片和预期标签文件。它不是检测训练数据，也不提供检测指标。",
        "",
        "## 标注前检查",
        "",
        "- 确认每类 3 张图片与类别名匹配。",
        "- 标注工具必须使用 `classes.txt` 的 93 类顺序。",
        "- 标注输出必须写入 `labels/`，文件名与图片同名、扩展名为 `.txt`。",
        "- 标注完成后运行 `scripts\\validate_detection_annotation_package.py --require-complete`。",
        "",
        "## 样本索引",
        "",
        "| class_index | class_name | split | image | expected_label |",
        "|---:|---|---|---|---|",
    ]
    for sample in payload["samples"]:
        lines.append(
            f"| {sample['class_index']} | {sample['class_name']} | {sample['source_split']} | `{Path(sample['package_image']).name}` | `{Path(sample['yolo_label']).name}` |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a contact sheet for manual detection annotation package review.")
    parser.add_argument("--manifest", default="data/detection_annotation_package/annotation_manifest.json")
    parser.add_argument("--output", default="reports/detection_annotation_contact_sheet.json")
    parser.add_argument("--figure", default="reports/figures/detection_annotation_contact_sheet.png")
    parser.add_argument("--columns", type=int, default=6)
    args = parser.parse_args()

    manifest_path = resolve_project_path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    samples = manifest.get("samples", [])
    figure = resolve_project_path(args.figure)
    make_sheet(samples, figure, "检测 bbox 待标注样本总览", args.columns, (190, 145))
    payload = {
        "manifest": str(manifest_path),
        "figure": str(figure),
        "summary": {
            "samples": len(samples),
            "classes": len(manifest.get("classes", [])),
            "labels_expected": manifest.get("summary", {}).get("labels_expected", len(samples)),
            "labels_completed": manifest.get("summary", {}).get("labels_completed", 0),
            "annotation_status": manifest.get("summary", {}).get("status", "pending_bbox_annotation"),
        },
        "samples": samples,
    }
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, output.with_suffix(".md"))
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
