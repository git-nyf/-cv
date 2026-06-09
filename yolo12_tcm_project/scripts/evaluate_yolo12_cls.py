from __future__ import annotations

import argparse
import json

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate YOLOv12 classification model.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", default="../data")
    parser.add_argument("--imgsz", type=int, default=224)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--output", default="reports/classification_evaluation_metrics.json")
    args = parser.parse_args()

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    metrics = model.val(data=str(resolve_project_path(args.data)), imgsz=args.imgsz, device=args.device)
    summary = {
        "top1": getattr(metrics, "top1", None),
        "top5": getattr(metrics, "top5", None),
        "fitness": getattr(metrics, "fitness", None),
    }
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
