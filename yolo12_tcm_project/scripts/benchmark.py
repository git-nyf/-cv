from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

import psutil

from path_utils import iter_images, resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark YOLOv12 inference latency.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--images", default="data/splits/images/test")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--output", default="runs/benchmarks/latency.json")
    args = parser.parse_args()

    image_paths = sorted(iter_images(resolve_project_path(args.images)))
    if not image_paths:
        raise SystemExit(f"No images found: {resolve_project_path(args.images)}")
    samples = image_paths[: max(1, min(len(image_paths), args.iterations))]

    YOLO = require_ultralytics()
    model = YOLO(str(resolve_project_path(args.model)))
    for image in samples[: args.warmup]:
        model.predict(source=str(image), imgsz=args.imgsz, device=args.device, verbose=False)

    process = psutil.Process()
    latencies = []
    rss_before = process.memory_info().rss
    for image in samples:
        start = time.perf_counter()
        model.predict(source=str(image), imgsz=args.imgsz, device=args.device, verbose=False)
        latencies.append((time.perf_counter() - start) * 1000)
    rss_after = process.memory_info().rss

    report = {
        "model": args.model,
        "device": args.device,
        "imgsz": args.imgsz,
        "images": len(samples),
        "latency_ms_mean": statistics.mean(latencies),
        "latency_ms_median": statistics.median(latencies),
        "latency_ms_min": min(latencies),
        "latency_ms_max": max(latencies),
        "fps_mean": 1000.0 / statistics.mean(latencies) if latencies else None,
        "rss_delta_mb": (rss_after - rss_before) / 1024 / 1024,
    }
    out = resolve_project_path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

