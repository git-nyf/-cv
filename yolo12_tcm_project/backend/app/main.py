from __future__ import annotations

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import get_settings
from .model_service import classify_image, detect_image, list_models, save_upload, start_training
from .schemas import ImageClassifyResponse, ImageDetectResponse, ModelInfo, TrainRequest, TrainResponse

app = FastAPI(title="YOLOv12 TCM Detection API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yolo12-tcm-api"}


@app.get("/models", response_model=list[ModelInfo])
def models() -> list[dict]:
    return list_models(get_settings())


@app.post("/detect/image", response_model=ImageDetectResponse)
async def detect_uploaded_image(
    file: UploadFile = File(...),
    model: str | None = Form(default=None),
    imgsz: int = Form(default=640),
    conf: float = Form(default=0.25),
    iou: float = Form(default=0.7),
) -> dict:
    settings = get_settings()
    image_path = await save_upload(file, settings.prediction_dir / "uploads")
    return detect_image(settings, image_path, model, imgsz, conf, iou)


@app.post("/classify/image", response_model=ImageClassifyResponse)
async def classify_uploaded_image(
    file: UploadFile = File(...),
    model: str | None = Form(default=None),
    imgsz: int = Form(default=224),
    topk: int = Form(default=5),
) -> dict:
    settings = get_settings()
    image_path = await save_upload(file, settings.prediction_dir / "uploads")
    return classify_image(settings, image_path, model, imgsz, topk)


@app.post("/detect/video")
def detect_video_placeholder() -> dict[str, str]:
    return {
        "status": "planned",
        "message": "摄像头实时识别由前端 getUserMedia 逐帧上传或本地 infer_video.py 完成；生产部署可扩展为 WebSocket 帧流。",
    }


@app.post("/train/start", response_model=TrainResponse)
def train(req: TrainRequest) -> dict:
    settings = get_settings()
    return start_training(settings, req.config, req.model, req.epochs, req.device)


@app.get("/metrics")
def metrics() -> dict[str, str]:
    return {
        "status": "pending",
        "message": "训练完成后运行 scripts/evaluate_yolo12.py 和 scripts/benchmark.py 生成真实指标。",
    }


@app.get("/files")
def get_file(path: str):
    return FileResponse(path)
