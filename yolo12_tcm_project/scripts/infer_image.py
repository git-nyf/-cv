from __future__ import annotations

import argparse
import json
from pathlib import Path

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def result_to_dict(result) -> dict:
    boxes = []
    names = result.names or {}
    if result.boxes is not None:
        for box in result.boxes:
            cls = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            xyxy = [float(v) for v in box.xyxy[0].tolist()]
            boxes.append({"class_id": cls, "class_name": names.get(cls, str(cls)), "confidence": conf, "bbox_xyxy": xyxy})
    return {"image": str(result.path), "detections": boxes}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run YOLOv12 image inference.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--device", default="")
    parser.add_argument("--output", default="runs/predict")
    args = parser.parse_args()

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    kwargs = {
        "source": str(resolve_project_path(args.source)),
        "imgsz": args.imgsz,
        "conf": args.conf,
        "iou": args.iou,
        "project": str(resolve_project_path(args.output)),
        "name": "image",
        "save": True,
        "exist_ok": True,
    }
    if args.device:
        kwargs["device"] = args.device
    results = model.predict(**kwargs)
    payload = [result_to_dict(r) for r in results]
    out = resolve_project_path(args.output) / "image" / "predictions.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

