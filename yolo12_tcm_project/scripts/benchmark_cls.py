from __future__ import annotations

import argparse
import json
import statistics
import time

import psutil

from path_utils import iter_images, resolve_project_path
from yolo_common import require_ultralytics


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark YOLOv12 classification inference latency.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--images", default="data/classification_strict_jpeg/val")
    parser.add_argument("--imgsz", type=int, default=224)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--output", default="runs/benchmarks/strict_classification_latency.json")
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
    correct_top1 = 0
    correct_top5 = 0
    for image in samples:
        start = time.perf_counter()
        results = model.predict(source=str(image), imgsz=args.imgsz, device=args.device, verbose=False)
        latencies.append((time.perf_counter() - start) * 1000)
        if results and results[0].probs is not None:
            names = results[0].names or {}
            expected = image.parent.name
            top1_name = str(names.get(int(results[0].probs.top1), results[0].probs.top1))
            top5_names = [str(names.get(int(class_id), class_id)) for class_id in results[0].probs.top5]
            correct_top1 += int(top1_name == expected)
            correct_top5 += int(expected in top5_names)
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
        "sample_top1_accuracy": correct_top1 / len(samples),
        "sample_top5_accuracy": correct_top5 / len(samples),
    }
    output = resolve_project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
