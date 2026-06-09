from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    project_root: Path = Path(__file__).resolve().parents[2]
    weights_dir: Path = Path(__file__).resolve().parents[2] / "runs" / "train"
    prediction_dir: Path = Path(__file__).resolve().parents[2] / "runs" / "predict" / "api"
    default_model: str = ""
    default_imgsz: int = 640
    default_conf: float = 0.25
    default_iou: float = 0.7


@lru_cache
def get_settings() -> Settings:
    return Settings()

