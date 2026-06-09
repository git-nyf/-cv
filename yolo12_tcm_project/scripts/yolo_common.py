from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import yaml

from path_utils import resolve_project_path


def require_ultralytics():
    if importlib.util.find_spec("ultralytics") is None:
        raise SystemExit(
            "未安装 ultralytics。请先运行: pip install -r requirements.txt\n"
            "注意：YOLOv12 支持依赖当前 Ultralytics 版本，若官方接口变化，请参照 docs/environment.md 调整。"
        )
    from ultralytics import YOLO

    return YOLO


def load_yaml(path: str | Path) -> dict[str, Any]:
    target = resolve_project_path(path)
    return yaml.safe_load(target.read_text(encoding="utf-8")) or {}


def normalize_train_args(config: dict[str, Any]) -> dict[str, Any]:
    args = dict(config)
    for key in ("data", "project"):
        if key in args:
            args[key] = str(resolve_project_path(args[key]))
    return args

