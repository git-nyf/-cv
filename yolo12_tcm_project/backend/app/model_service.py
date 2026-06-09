from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile

from .config import Settings


def list_models(settings: Settings) -> list[dict[str, Any]]:
    candidates = sorted(settings.project_root.rglob("*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    models = []
    for path in candidates:
        try:
            stat = path.stat()
        except OSError:
            continue
        models.append(
            {
                "name": path.name,
                "path": str(path),
                "size_mb": round(stat.st_size / 1024 / 1024, 3),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            }
        )
    return models


def resolve_model(settings: Settings, model_name: str | None) -> Path:
    if model_name:
        candidate = Path(model_name)
        if candidate.is_absolute() and candidate.exists():
            return candidate
        for model in list_models(settings):
            if model["name"] == model_name or model["path"] == model_name:
                return Path(model["path"])
        project_candidate = settings.project_root / model_name
        if project_candidate.exists():
            return project_candidate
    if settings.default_model:
        default = Path(settings.default_model)
        if not default.is_absolute():
            default = settings.project_root / default
        if default.exists():
            return default
    models = list_models(settings)
    if models:
        return Path(models[0]["path"])
    raise HTTPException(status_code=404, detail="未找到 .pt 权重文件。请先训练模型或把 best.pt 放入 runs/train。")


def require_yolo():
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"当前环境未安装或无法导入 ultralytics: {exc}") from exc
    return YOLO


async def save_upload(file: UploadFile, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    target = output_dir / f"upload_{int(time.time() * 1000)}{suffix}"
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")
    target.write_bytes(content)
    return target


def detect_image(settings: Settings, image_path: Path, model_name: str | None, imgsz: int, conf: float, iou: float) -> dict[str, Any]:
    YOLO = require_yolo()
    model_path = resolve_model(settings, model_name)
    model = YOLO(str(model_path))
    run_name = f"api_{int(time.time() * 1000)}"
    start = time.perf_counter()
    results = model.predict(
        source=str(image_path),
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        project=str(settings.prediction_dir),
        name=run_name,
        save=True,
        exist_ok=True,
        verbose=False,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    detections = []
    saved_image = None
    if results:
        result = results[0]
        names = result.names or {}
        if result.save_dir:
            candidates = list(Path(result.save_dir).glob(Path(image_path).name))
            if candidates:
                saved_image = str(candidates[0])
        if result.boxes is not None:
            for box in result.boxes:
                cls = int(box.cls[0].item())
                detections.append(
                    {
                        "class_id": cls,
                        "class_name": str(names.get(cls, cls)),
                        "confidence": float(box.conf[0].item()),
                        "bbox_xyxy": [float(v) for v in box.xyxy[0].tolist()],
                    }
                )
    payload = {"model": str(model_path), "saved_image": saved_image, "detections": detections, "elapsed_ms": elapsed_ms}
    (settings.prediction_dir / run_name / "result.json").parent.mkdir(parents=True, exist_ok=True)
    (settings.prediction_dir / run_name / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def classify_image(settings: Settings, image_path: Path, model_name: str | None, imgsz: int, topk: int) -> dict[str, Any]:
    YOLO = require_yolo()
    model_path = resolve_model(settings, model_name)
    model = YOLO(str(model_path))
    run_name = f"api_cls_{int(time.time() * 1000)}"
    start = time.perf_counter()
    results = model.predict(
        source=str(image_path),
        imgsz=imgsz,
        project=str(settings.prediction_dir),
        name=run_name,
        save=True,
        exist_ok=True,
        verbose=False,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    saved_image = None
    predictions: list[dict[str, Any]] = []
    top1_class_id = None
    top1_class_name = None
    top1_confidence = None
    if results:
        result = results[0]
        names = result.names or {}
        if result.save_dir:
            candidates = list(Path(result.save_dir).glob(Path(image_path).name))
            if candidates:
                saved_image = str(candidates[0])
        probs = result.probs
        if probs is not None:
            top1_class_id = int(probs.top1)
            top1_class_name = str(names.get(top1_class_id, top1_class_id))
            top1_confidence = float(probs.top1conf.item())
            limit = max(1, min(topk, len(probs.top5)))
            for index, class_id in enumerate(probs.top5[:limit]):
                cls = int(class_id)
                predictions.append(
                    {
                        "class_id": cls,
                        "class_name": str(names.get(cls, cls)),
                        "confidence": float(probs.top5conf[index].item()),
                    }
                )
    payload = {
        "model": str(model_path),
        "saved_image": saved_image,
        "predictions": predictions,
        "top1_class_id": top1_class_id,
        "top1_class_name": top1_class_name,
        "top1_confidence": top1_confidence,
        "elapsed_ms": elapsed_ms,
    }
    (settings.prediction_dir / run_name / "result.json").parent.mkdir(parents=True, exist_ok=True)
    (settings.prediction_dir / run_name / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def start_training(settings: Settings, config: str, model: str | None, epochs: int | None, device: str | None) -> dict[str, Any]:
    script = settings.project_root / "scripts" / "train_yolo12.py"
    cmd = [sys.executable, str(script), "--config", config]
    if model:
        cmd += ["--model", model]
    if epochs:
        cmd += ["--epochs", str(epochs)]
    if device:
        cmd += ["--device", device]
    log_dir = settings.project_root / "runs" / "train"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"api_train_{int(time.time())}.log"
    with log_file.open("w", encoding="utf-8") as log:
        subprocess.Popen(cmd, cwd=settings.project_root, stdout=log, stderr=subprocess.STDOUT)
    return {"accepted": True, "command": cmd, "message": f"训练任务已启动，日志: {log_file}"}
