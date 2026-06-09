from __future__ import annotations

import argparse
import json
from pathlib import Path

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate YOLOv12 model.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", default="data/splits/data.yaml")
    parser.add_argument("--split", choices=["val", "test"], default="test")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="")
    parser.add_argument("--output", default="reports/evaluation_metrics.json")
    args = parser.parse_args()

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    kwargs = {"data": str(resolve_project_path(args.data)), "split": args.split, "imgsz": args.imgsz}
    if args.device:
        kwargs["device"] = args.device
    metrics = model.val(**kwargs)
    summary = {
        "precision": getattr(metrics.box, "mp", None),
        "recall": getattr(metrics.box, "mr", None),
        "map50": getattr(metrics.box, "map50", None),
        "map50_95": getattr(metrics.box, "map", None),
        "fitness": getattr(metrics, "fitness", None),
    }
    out = resolve_project_path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

