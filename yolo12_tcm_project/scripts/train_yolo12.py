from __future__ import annotations

import argparse

from yolo_common import load_yaml, normalize_train_args, require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Train YOLOv12 baseline.")
    parser.add_argument("--config", default="configs/train_baseline.yaml")
    parser.add_argument("--model", default="", help="Override model, e.g. yolo12n.pt or yolo12n.yaml")
    parser.add_argument("--data", default="", help="Override data yaml")
    parser.add_argument("--epochs", type=int, default=0)
    parser.add_argument("--device", default="")
    parser.add_argument("--batch", type=int, default=0)
    parser.add_argument("--imgsz", type=int, default=0)
    parser.add_argument("--name", default="")
    parser.add_argument("--project", default="")
    args = parser.parse_args()

    config = load_yaml(args.config)
    if args.model:
        config["model"] = args.model
    if args.data:
        config["data"] = args.data
    if args.epochs:
        config["epochs"] = args.epochs
    if args.device:
        config["device"] = args.device
    if args.batch:
        config["batch"] = args.batch
    if args.imgsz:
        config["imgsz"] = args.imgsz
    if args.name:
        config["name"] = args.name
    if args.project:
        config["project"] = args.project

    model_name = config.pop("model", "yolo12n.pt")
    YOLO = require_ultralytics()
    model = YOLO(model_name)
    train_args = normalize_train_args(config)
    print("Training args:", train_args)
    model.train(**train_args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
