from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from path_utils import resolve_project_path


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        image = image.convert("RGB")
        return ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: str, width: int, line_height: int) -> int:
    lines: list[str] = []
    for paragraph in text.splitlines():
        if not paragraph:
            lines.append("")
            continue
        wrapped = textwrap.wrap(paragraph, width=width, break_long_words=True, replace_whitespace=False)
        lines.extend(wrapped or [paragraph])
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def sample_label(sample: dict[str, Any]) -> str:
    confidence = float(sample.get("top1_confidence", 0.0))
    top5 = "Y" if sample.get("top5_contains_expected") else "N"
    image_name = Path(sample.get("image", "")).name
    return (
        f"{sample.get('expected_class', '')} -> {sample.get('predicted_class', '')}\n"
        f"conf={confidence:.3f}, top5={top5}\n"
        f"{image_name}"
    )


def flatten_confusion_samples(report: dict[str, Any], max_pairs: int, samples_per_group: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair in report.get("review_samples", {}).get("confusion_pairs", [])[:max_pairs]:
        for sample in pair.get("examples", [])[:samples_per_group]:
            rows.append({**sample, "group": f"{pair['expected_class']} -> {pair['predicted_class']} ({pair['count']})"})
    return rows


def flatten_worst_class_samples(report: dict[str, Any], max_classes: int, samples_per_group: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for class_row in report.get("review_samples", {}).get("worst_classes", [])[:max_classes]:
        group = f"{class_row['class_name']} top1={class_row['top1_accuracy']:.2f}, top5={class_row['top5_accuracy']:.2f}"
        for sample in class_row.get("examples", [])[:samples_per_group]:
            rows.append({**sample, "group": group})
    return rows


def make_contact_sheet(
    samples: list[dict[str, Any]],
    title: str,
    output: Path,
    columns: int,
    thumb_size: tuple[int, int],
) -> None:
    font_title = load_font(28)
    font_group = load_font(18)
    font_body = load_font(15)
    margin = 24
    gap = 16
    label_height = 82
    header_height = 62
    cell_w = thumb_size[0]
    cell_h = thumb_size[1] + label_height
    rows = max(1, (len(samples) + columns - 1) // columns)
    width = margin * 2 + columns * cell_w + (columns - 1) * gap
    height = margin * 2 + header_height + rows * cell_h + (rows - 1) * gap

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, margin), title, font=font_title, fill="#1F4E79")

    for index, sample in enumerate(samples):
        row, col = divmod(index, columns)
        x = margin + col * (cell_w + gap)
        y = margin + header_height + row * (cell_h + gap)
        image_path = Path(sample["image"])
        try:
            thumb = fit_image(image_path, thumb_size)
            image_x = x + (thumb_size[0] - thumb.width) // 2
            image_y = y + (thumb_size[1] - thumb.height) // 2
            canvas.paste(thumb, (image_x, image_y))
        except Exception:
            draw.rectangle([x, y, x + thumb_size[0], y + thumb_size[1]], outline="#B42318", width=2)
            draw.text((x + 8, y + 8), "image load failed", font=font_body, fill="#B42318")
        draw.rectangle([x, y, x + thumb_size[0], y + thumb_size[1]], outline="#D0D7DE", width=1)
        draw_wrapped(draw, (x, y + thumb_size[1] + 6), sample.get("group", ""), font_group, "#1F2933", 24, 20)
        draw_wrapped(draw, (x, y + thumb_size[1] + 28), sample_label(sample), font_body, "#344054", 32, 17)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# strict 分类人工复核样例清单",
        "",
        f"- 来源分析: `{payload['source_analysis']}`",
        f"- 高频混淆样例图: `{payload['figures']['confusion_contact_sheet']}`",
        f"- 低表现类别样例图: `{payload['figures']['worst_class_contact_sheet']}`",
        "",
        "## 复核目的",
        "",
        "这些样例用于人工检查目录混入、外观相似、拍摄条件差异、标注命名不一致等数据质量问题。该材料不代表新模型性能，只为后续补样和清洗排序。",
        "",
        "## 高频混淆复核样例",
        "",
        "| 真实类别 | 预测类别 | 置信度 | Top-5 含真实类别 | 图片 |",
        "|---|---|---:|---|---|",
    ]
    for sample in payload["confusion_samples"]:
        contains = "是" if sample["top5_contains_expected"] else "否"
        lines.append(
            f"| {sample['expected_class']} | {sample['predicted_class']} | {sample['top1_confidence']:.4f} | {contains} | `{sample['image']}` |"
        )

    lines.extend(
        [
            "",
            "## 低表现类别复核样例",
            "",
            "| 真实类别 | 预测类别 | 置信度 | Top-5 含真实类别 | 图片 |",
            "|---|---|---:|---|---|",
        ]
    )
    for sample in payload["worst_class_samples"]:
        contains = "是" if sample["top5_contains_expected"] else "否"
        lines.append(
            f"| {sample['expected_class']} | {sample['predicted_class']} | {sample['top1_confidence']:.4f} | {contains} | `{sample['image']}` |"
        )

    lines.extend(
        [
            "",
            "## 建议处理",
            "",
            "- 优先人工打开 contact sheet 中高频混淆对，判断是否存在目录混入或类别外观高度重叠。",
            "- 对 Top-1 为 0 且 Top-5 也低的类别，优先补充训练样本或检查验证样本来源。",
            "- 若两类长期互相混淆且人工也难区分，应在报告中明确相似类别风险，必要时设计合并/细分标签对照实验。",
            "- 若课程要求目标检测，本材料只能作为分类数据清洗依据，仍需真实 bbox 标注。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate review samples and contact sheets from classification error analysis.")
    parser.add_argument("--analysis", default="reports/strict_classification_error_analysis.json")
    parser.add_argument("--output", default="reports/strict_classification_review_samples.json")
    parser.add_argument("--max-confusion-pairs", type=int, default=6)
    parser.add_argument("--max-worst-classes", type=int, default=6)
    parser.add_argument("--samples-per-group", type=int, default=3)
    parser.add_argument("--columns", type=int, default=3)
    args = parser.parse_args()

    analysis_path = resolve_project_path(args.analysis)
    report = json.loads(analysis_path.read_text(encoding="utf-8"))
    confusion_samples = flatten_confusion_samples(report, args.max_confusion_pairs, args.samples_per_group)
    worst_class_samples = flatten_worst_class_samples(report, args.max_worst_classes, args.samples_per_group)

    confusion_sheet = resolve_project_path("reports/figures/strict_confusion_contact_sheet.png")
    worst_sheet = resolve_project_path("reports/figures/strict_worst_class_contact_sheet.png")
    make_contact_sheet(confusion_samples, "strict 分类高频混淆人工复核样例", confusion_sheet, args.columns, (260, 190))
    make_contact_sheet(worst_class_samples, "strict 分类低表现类别人工复核样例", worst_sheet, args.columns, (260, 190))

    payload = {
        "source_analysis": str(analysis_path),
        "figures": {
            "confusion_contact_sheet": str(confusion_sheet),
            "worst_class_contact_sheet": str(worst_sheet),
        },
        "confusion_samples": confusion_samples,
        "worst_class_samples": worst_class_samples,
    }
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, output.with_suffix(".md"))
    print(json.dumps({"confusion_samples": len(confusion_samples), "worst_class_samples": len(worst_class_samples)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
