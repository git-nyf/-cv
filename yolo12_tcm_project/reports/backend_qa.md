# 后端 API QA 报告

- 时间: 2026-06-07T01:32:43
- 总检查项: 4
- 通过: 4
- 失败: 0

| 检查项 | 状态 | 说明 |
|---|---|---|
| `GET /health` | 通过 | `{"status": "ok", "service": "yolo12-tcm-api"}` |
| `GET /models` | 通过 | `{"status_code": 200, "count": 10}` |
| `POST /detect/image` | 通过 | `{"status_code": 200, "detections": 0, "elapsed_ms": 106.45319999821368, "saved_image": "D:\\AAA中药cv\\yolo12_tcm_project\\runs\\predict\\api\\api_1780767163228\\upload_1780767160210.jpg"}` |
| `POST /classify/image` | 通过 | `{"status_code": 200, "predictions": 5, "top1_class_name": "干姜", "elapsed_ms": 41.379499998583924, "saved_image": "D:\\AAA中药cv\\yolo12_tcm_project\\runs\\predict\\api\\api_cls_1780767163360\\upload_1780767163340.jpg"}` |
