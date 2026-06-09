from __future__ import annotations

import argparse

from path_utils import resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Export YOLOv12 model.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--format", default="onnx", choices=["onnx", "engine", "openvino", "torchscript"])
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--half", action="store_true")
    parser.add_argument("--dynamic", action="store_true")
    parser.add_argument("--simplify", action="store_true")
    args = parser.parse_args()

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    exported = model.export(format=args.format, imgsz=args.imgsz, half=args.half, dynamic=args.dynamic, simplify=args.simplify)
    print(exported)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

