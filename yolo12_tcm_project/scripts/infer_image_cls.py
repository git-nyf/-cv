from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def tensor_item(value: Any) -> float:
    if hasattr(value, "item"):
        return float(value.item())
    return float(value)


def result_to_dict(result, topk: int) -> dict[str, Any]:
    names = result.names or {}
    probs = result.probs
    if probs is None:
        return {"image": str(result.path), "expected_class": Path(result.path).parent.name, "predictions": []}

    class_ids = list(probs.top5[:topk])
    confidences = probs.top5conf[:topk]
    predictions = [
        {
            "class_id": int(class_id),
            "class_name": str(names.get(int(class_id), class_id)),
            "confidence": tensor_item(confidences[index]),
        }
        for index, class_id in enumerate(class_ids)
    ]
    return {
        "image": str(result.path),
        "expected_class": Path(result.path).parent.name,
        "top1_class_id": int(probs.top1),
        "top1_class_name": str(names.get(int(probs.top1), probs.top1)),
        "top1_confidence": tensor_item(probs.top1conf),
        "predictions": predictions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run YOLOv12 classification image inference.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--source", required=True, help="Image file or directory.")
    parser.add_argument("--imgsz", type=int, default=224)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--topk", type=int, default=5)
    parser.add_argument("--save-images", action="store_true", help="Also save Ultralytics rendered prediction images.")
    parser.add_argument("--project", default="runs/predict_cls")
    parser.add_argument("--name", default="image")
    parser.add_argument("--output", default="runs/predict_cls/image/predictions.json")
    args = parser.parse_args()

    if args.topk < 1:
        raise SystemExit("--topk must be >= 1")

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    results = model.predict(
        source=str(resolve_project_path(args.source)),
        imgsz=args.imgsz,
        device=args.device,
        project=str(resolve_project_path(args.project)),
        name=args.name,
        save=args.save_images,
        exist_ok=True,
        verbose=False,
    )

    payload = {
        "model": str(resolve_project_path(args.model)),
        "source": str(resolve_project_path(args.source)),
        "imgsz": args.imgsz,
        "device": args.device,
        "topk": args.topk,
        "results": [result_to_dict(result, args.topk) for result in results],
    }
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
