from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.main import app

MODEL = ROOT / "runs" / "train" / "demo_yolo12n_smoke" / "weights" / "best.pt"
IMAGE = ROOT / "data" / "demo_splits" / "images" / "test" / "demo_003.jpg"
CLS_MODEL = ROOT / "runs" / "train" / "strict_classify_yolo12n_cls_cpu_5e" / "weights" / "best.pt"
CLS_IMAGE = ROOT / "data" / "classification_strict_jpeg" / "val" / "丝瓜络" / "Sigualuo117.jpg"


def main() -> int:
    client = TestClient(app)
    checks: list[dict] = []

    health = client.get("/health")
    checks.append({"name": "GET /health", "passed": health.status_code == 200 and health.json().get("status") == "ok", "detail": health.json()})

    models = client.get("/models")
    model_payload = models.json()
    checks.append(
        {
            "name": "GET /models",
            "passed": models.status_code == 200 and any(item["path"].endswith("best.pt") for item in model_payload),
            "detail": {"status_code": models.status_code, "count": len(model_payload)},
        }
    )

    if MODEL.exists() and IMAGE.exists():
        with IMAGE.open("rb") as f:
            detect = client.post(
                "/detect/image",
                data={"model": str(MODEL), "imgsz": "320", "conf": "0.05", "iou": "0.7"},
                files={"file": ("demo_003.jpg", f, "image/jpeg")},
            )
        payload = detect.json()
        checks.append(
            {
                "name": "POST /detect/image",
                "passed": detect.status_code == 200 and "detections" in payload and "elapsed_ms" in payload,
                "detail": {
                    "status_code": detect.status_code,
                    "detections": len(payload.get("detections", [])),
                    "elapsed_ms": payload.get("elapsed_ms"),
                    "saved_image": payload.get("saved_image"),
                },
            }
        )
    else:
        checks.append({"name": "POST /detect/image", "passed": False, "detail": "demo model or image missing"})

    if CLS_MODEL.exists() and CLS_IMAGE.exists():
        with CLS_IMAGE.open("rb") as f:
            classify = client.post(
                "/classify/image",
                data={"model": str(CLS_MODEL), "imgsz": "224", "topk": "5"},
                files={"file": ("Sigualuo117.jpg", f, "image/jpeg")},
            )
        payload = classify.json()
        checks.append(
            {
                "name": "POST /classify/image",
                "passed": classify.status_code == 200 and "predictions" in payload and "elapsed_ms" in payload,
                "detail": {
                    "status_code": classify.status_code,
                    "predictions": len(payload.get("predictions", [])),
                    "top1_class_name": payload.get("top1_class_name"),
                    "elapsed_ms": payload.get("elapsed_ms"),
                    "saved_image": payload.get("saved_image"),
                },
            }
        )
    else:
        checks.append({"name": "POST /classify/image", "passed": False, "detail": "strict classification model or image missing"})

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "checks": checks,
        "summary": {
            "total": len(checks),
            "passed": sum(1 for item in checks if item["passed"]),
            "failed": sum(1 for item in checks if not item["passed"]),
        },
    }
    out = ROOT / "reports" / "backend_qa.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 后端 API QA 报告",
        "",
        f"- 时间: {report['timestamp']}",
        f"- 总检查项: {report['summary']['total']}",
        f"- 通过: {report['summary']['passed']}",
        f"- 失败: {report['summary']['failed']}",
        "",
        "| 检查项 | 状态 | 说明 |",
        "|---|---|---|",
    ]
    for item in checks:
        lines.append(f"| `{item['name']}` | {'通过' if item['passed'] else '未通过'} | `{json.dumps(item['detail'], ensure_ascii=False)}` |")
    (ROOT / "reports" / "backend_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
