from __future__ import annotations

import argparse
import itertools

from yolo_common import load_yaml, normalize_train_args, require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Run controlled YOLOv12 tuning grid.")
    parser.add_argument("--config", default="configs/train_tune.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_yaml(args.config)
    models = config.pop("models", ["yolo12n.pt"])
    imgsz_values = config.pop("imgsz", [640])
    batch_values = config.pop("batch", [16])
    lr_values = config.pop("lr0", [0.001])
    max_runs = int(config.pop("max_runs", 999))
    base_name = config.pop("base_name", "yolo12_tune")

    combos = list(itertools.product(models, imgsz_values, batch_values, lr_values))[:max_runs]
    if args.dry_run:
        for i, combo in enumerate(combos, 1):
            print(i, combo)
        return 0

    YOLO = require_ultralytics()
    for i, (model_name, imgsz, batch, lr0) in enumerate(combos, 1):
        run_args = dict(config)
        run_args.update({"imgsz": imgsz, "batch": batch, "lr0": lr0, "name": f"{base_name}_{i:02d}_{model_name.replace('.', '_')}_img{imgsz}_b{batch}_lr{lr0}"})
        print(f"=== Tuning run {i}/{len(combos)}: {run_args['name']} ===")
        model = YOLO(model_name)
        model.train(**normalize_train_args(run_args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

