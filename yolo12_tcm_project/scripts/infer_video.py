from __future__ import annotations

import argparse

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Run YOLOv12 video/camera inference.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--source", default="0", help="Video path, stream URL, or camera index")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--device", default="")
    parser.add_argument("--output", default="runs/predict")
    args = parser.parse_args()

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    source = int(args.source) if args.source.isdigit() else str(resolve_project_path(args.source))
    kwargs = {
        "source": source,
        "imgsz": args.imgsz,
        "conf": args.conf,
        "project": str(resolve_project_path(args.output)),
        "name": "video",
        "save": True,
        "show": False,
        "exist_ok": True,
    }
    if args.device:
        kwargs["device"] = args.device
    model.predict(**kwargs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

