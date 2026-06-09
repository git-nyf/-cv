from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from path_utils import iter_images, resolve_project_path
from yolo_common import require_ultralytics


def tensor_item(value: Any) -> float:
    if hasattr(value, "item"):
        return float(value.item())
    return float(value)


def batched(items: list[Path], size: int) -> Iterable[list[Path]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def prediction_names(result: Any, topk: int) -> list[str]:
    names = result.names or {}
    probs = result.probs
    if probs is None:
        return []
    return [str(names.get(int(class_id), class_id)) for class_id in probs.top5[:topk]]


def prediction_confidences(result: Any, topk: int) -> list[float]:
    probs = result.probs
    if probs is None:
        return []
    return [tensor_item(value) for value in probs.top5conf[:topk]]


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    data_dir = resolve_project_path(args.data)
    image_paths = sorted(iter_images(data_dir))
    if args.limit > 0:
        image_paths = image_paths[: args.limit]
    if not image_paths:
        raise SystemExit(f"No images found: {data_dir}")

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))

    per_class: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "total": 0,
            "top1_correct": 0,
            "top5_correct": 0,
            "top1_predictions": Counter(),
        }
    )
    confusion_pairs: Counter[tuple[str, str]] = Counter()
    confusion_examples: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    class_error_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    examples: list[dict[str, Any]] = []
    top1_correct = 0
    top5_correct = 0

    topk = max(1, args.topk)
    for chunk in batched(image_paths, max(1, args.batch)):
        results = model.predict(
            source=[str(path) for path in chunk],
            imgsz=args.imgsz,
            device=args.device,
            verbose=False,
        )
        for source_path, result in zip(chunk, results):
            image = source_path
            expected = image.parent.name
            names = prediction_names(result, topk)
            confidences = prediction_confidences(result, topk)
            predicted = names[0] if names else ""
            confidence = confidences[0] if confidences else 0.0
            is_top1 = predicted == expected
            is_top5 = expected in names

            stats = per_class[expected]
            stats["total"] += 1
            stats["top1_correct"] += int(is_top1)
            stats["top5_correct"] += int(is_top5)
            if predicted:
                stats["top1_predictions"][predicted] += 1

            top1_correct += int(is_top1)
            top5_correct += int(is_top5)
            if not is_top1 and predicted:
                confusion_pairs[(expected, predicted)] += 1
                example = {
                    "image": str(image),
                    "expected_class": expected,
                    "predicted_class": predicted,
                    "top1_confidence": confidence,
                    "top5_predictions": [
                        {"class_name": name, "confidence": confidences[index]}
                        for index, name in enumerate(names)
                    ],
                    "top5_contains_expected": is_top5,
                }
                pair_key = (expected, predicted)
                if len(confusion_examples[pair_key]) < args.max_examples_per_confusion:
                    confusion_examples[pair_key].append(example)
                if len(class_error_examples[expected]) < args.max_examples_per_class:
                    class_error_examples[expected].append(example)
                if len(examples) < args.max_examples:
                    examples.append(example)

    class_rows = []
    for class_name, stats in per_class.items():
        total = stats["total"]
        top1 = stats["top1_correct"]
        top5_count = stats["top5_correct"]
        pred_counter: Counter = stats["top1_predictions"]
        class_rows.append(
            {
                "class_name": class_name,
                "total": total,
                "top1_correct": top1,
                "top5_correct": top5_count,
                "top1_accuracy": top1 / total if total else 0.0,
                "top5_accuracy": top5_count / total if total else 0.0,
                "most_predicted": [
                    {"class_name": name, "count": count}
                    for name, count in pred_counter.most_common(args.max_predictions_per_class)
                ],
            }
        )

    class_rows.sort(key=lambda row: (row["top1_accuracy"], row["top5_accuracy"], -row["total"], row["class_name"]))
    confusion_rows = [
        {"expected_class": expected, "predicted_class": predicted, "count": count}
        for (expected, predicted), count in confusion_pairs.most_common(args.max_confusions)
    ]
    total_images = len(image_paths)
    return {
        "model": str(resolve_project_path(args.model)),
        "data": str(data_dir),
        "imgsz": args.imgsz,
        "device": args.device,
        "topk": topk,
        "summary": {
            "images": total_images,
            "classes": len(per_class),
            "top1_correct": top1_correct,
            "top5_correct": top5_correct,
            "top1_accuracy": top1_correct / total_images,
            "top5_accuracy": top5_correct / total_images,
        },
        "worst_classes": class_rows[: args.max_classes],
        "best_classes": sorted(
            class_rows,
            key=lambda row: (-row["top1_accuracy"], -row["top5_accuracy"], -row["total"], row["class_name"]),
        )[: args.max_classes],
        "confusion_pairs": confusion_rows,
        "misclassification_examples": examples,
        "review_samples": {
            "confusion_pairs": [
                {
                    **item,
                    "examples": confusion_examples[(item["expected_class"], item["predicted_class"])],
                }
                for item in confusion_rows
            ],
            "worst_classes": [
                {
                    "class_name": row["class_name"],
                    "top1_accuracy": row["top1_accuracy"],
                    "top5_accuracy": row["top5_accuracy"],
                    "examples": class_error_examples[row["class_name"]],
                }
                for row in class_rows[: args.max_classes]
            ],
        },
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# strict 分类误判与每类表现分析",
        "",
        f"- 模型: `{report['model']}`",
        f"- 数据: `{report['data']}`",
        f"- 图像数: {summary['images']}",
        f"- 类别数: {summary['classes']}",
        f"- Top-1 Accuracy: {summary['top1_accuracy']:.10f}",
        f"- Top-5 Accuracy: {summary['top5_accuracy']:.10f}",
        "",
        "## Top-1 最低类别",
        "",
        "| 类别 | 样本数 | Top-1 | Top-5 | 最常预测为 |",
        "|---|---:|---:|---:|---|",
    ]
    for row in report["worst_classes"]:
        most_predicted = "，".join(f"{item['class_name']}({item['count']})" for item in row["most_predicted"][:3])
        lines.append(
            f"| {row['class_name']} | {row['total']} | {row['top1_accuracy']:.4f} | {row['top5_accuracy']:.4f} | {most_predicted} |"
        )

    lines.extend(
        [
            "",
            "## Top-1 最高类别",
            "",
            "| 类别 | 样本数 | Top-1 | Top-5 | 最常预测为 |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in report["best_classes"]:
        most_predicted = "，".join(f"{item['class_name']}({item['count']})" for item in row["most_predicted"][:3])
        lines.append(
            f"| {row['class_name']} | {row['total']} | {row['top1_accuracy']:.4f} | {row['top5_accuracy']:.4f} | {most_predicted} |"
        )

    lines.extend(
        [
            "",
            "## 高频混淆对",
            "",
            "| 真实类别 | 预测类别 | 次数 |",
            "|---|---|---:|",
        ]
    )
    for item in report["confusion_pairs"]:
        lines.append(f"| {item['expected_class']} | {item['predicted_class']} | {item['count']} |")

    lines.extend(
        [
            "",
            "## 典型误判样例",
            "",
            "| 图片 | 真实类别 | Top-1 | 置信度 | Top-5 含真实类别 |",
            "|---|---|---|---:|---|",
        ]
    )
    for item in report["misclassification_examples"]:
        contains = "是" if item["top5_contains_expected"] else "否"
        lines.append(
            f"| `{item['image']}` | {item['expected_class']} | {item['predicted_class']} | {item['top1_confidence']:.4f} | {contains} |"
        )

    lines.extend(
        [
            "",
            "## 解读",
            "",
            "- 该分析基于 strict 验证集逐图推理，适合解释当前 5 epoch CPU 短训模型的分类误差。",
            "- 若某类 Top-1 低但 Top-5 较高，说明模型已把真实类别排进候选但排序能力不足，后续可通过更长训练、预训练权重和相似类增强改善。",
            "- 若某类长期被同一类别吸收，需要优先检查两类图像是否存在外观相似、目录混入、拍摄条件差异或标注命名不一致。",
            "- 该分析仍是分类评估，不能替代目标检测 mAP 或 bbox 定位误差分析。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze YOLOv12 classification per-class errors.")
    parser.add_argument("--model", default="runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt")
    parser.add_argument("--data", default="data/classification_strict_jpeg/val")
    parser.add_argument("--imgsz", type=int, default=224)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--topk", type=int, default=5)
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--limit", type=int, default=0, help="Optional image limit for quick checks; 0 means all images.")
    parser.add_argument("--max-classes", type=int, default=15)
    parser.add_argument("--max-confusions", type=int, default=20)
    parser.add_argument("--max-examples", type=int, default=20)
    parser.add_argument("--max-examples-per-confusion", type=int, default=4)
    parser.add_argument("--max-examples-per-class", type=int, default=4)
    parser.add_argument("--max-predictions-per-class", type=int, default=5)
    parser.add_argument("--output", default="reports/strict_classification_error_analysis.json")
    args = parser.parse_args()

    report = analyze(args)
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, output.with_suffix(".md"))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
