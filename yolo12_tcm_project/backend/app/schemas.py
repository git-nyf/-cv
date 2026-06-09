from __future__ import annotations

from pydantic import BaseModel, Field


class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox_xyxy: list[float] = Field(min_length=4, max_length=4)


class ImageDetectResponse(BaseModel):
    model: str
    saved_image: str | None
    detections: list[Detection]
    elapsed_ms: float


class ClassificationPrediction(BaseModel):
    class_id: int
    class_name: str
    confidence: float


class ImageClassifyResponse(BaseModel):
    model: str
    saved_image: str | None
    predictions: list[ClassificationPrediction]
    top1_class_id: int | None
    top1_class_name: str | None
    top1_confidence: float | None
    elapsed_ms: float


class ModelInfo(BaseModel):
    name: str
    path: str
    size_mb: float
    modified_time: str


class TrainRequest(BaseModel):
    config: str = "configs/train_baseline.yaml"
    model: str | None = None
    epochs: int | None = None
    device: str | None = None


class TrainResponse(BaseModel):
    accepted: bool
    command: list[str]
    message: str
