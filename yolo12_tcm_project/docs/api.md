# API 文档

## GET /health

返回服务状态。

## GET /models

扫描项目目录下 `.pt` 权重文件。

响应字段：

- `name`
- `path`
- `size_mb`
- `modified_time`

## POST /detect/image

表单字段：

- `file`：图片文件
- `model`：可选，权重文件名或路径
- `imgsz`：默认 640
- `conf`：默认 0.25
- `iou`：默认 0.7

响应：

- `model`
- `saved_image`
- `detections`
- `elapsed_ms`

## POST /detect/video

当前为占位接口。课程演示版使用前端摄像头截帧上传；生产方案可扩展 WebSocket 视频帧流。

## POST /train/start

启动后台训练进程。

请求：

```json
{
  "config": "configs/train_baseline.yaml",
  "model": "yolo12n.pt",
  "epochs": 20,
  "device": "0"
}
```

## GET /metrics

返回指标生成状态。真实指标由 `scripts/evaluate_yolo12.py` 和 `scripts/benchmark.py` 生成。

