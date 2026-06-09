# YOLOv12 部分训练记录

## 结论

`D:\AAA中药cv\data` 当前可以用于“部分训练”，但它不是标准 YOLO 检测数据集。该目录按类别文件夹组织图片，没有发现 bbox 标注文件，因此不能直接作为真实目标检测训练数据。

本次采用临时整图框方案：每张图片生成一个覆盖全图的 YOLO bbox，用于验证 YOLOv12 检测训练链路。该结果只能作为工程流程验证，不能作为真实中药饮片检测精度。

## 原始数据状态

| 项目 | 结果 |
|---|---:|
| 原始路径 | `D:\AAA中药cv\data` |
| 图片总数 | 200 |
| 实际类别数 | 2 |
| train | 162 |
| val | 38 |
| 实际类别 | `丝瓜络`、`九香虫` |
| bbox 标注 | 未发现 |

原始 `data.yaml` 声明了 100 类，但当前目录里实际只提供了 `丝瓜络` 和 `九香虫` 两类图片。

## 转换数据

| 项目 | 路径 / 结果 |
|---|---|
| 转换脚本 | `scripts/classification_to_fullbox_yolo.py` |
| 输出数据集 | `data/partial_fullbox_yolo` |
| 类别映射 | `0: 丝瓜络`, `1: 九香虫` |
| 标签策略 | 每图 1 个全图 bbox：`class_id 0.5 0.5 1.0 1.0` |
| 转换报告 | `data/partial_fullbox_yolo/conversion_report.md` |

## 数据校验

| 划分 | 图片数 | errors | warnings | 说明 |
|---|---:|---:|---:|---|
| train | 162 | 0 | 2 | 发现 2 组重复图片 |
| val | 38 | 0 | 0 | 校验通过 |

校验报告：

- `reports/partial_fullbox_train_validation.md`
- `reports/partial_fullbox_val_validation.md`

## 训练配置

| 项目 | 配置 |
|---|---|
| 配置文件 | `configs/train_partial_fullbox.yaml` |
| 模型 | YOLOv12n |
| 初始化方式 | `yolo12n.yaml`，`pretrained: false` |
| 设备 | CPU |
| epochs | 1 |
| batch | 4 |
| imgsz | 320 |
| optimizer | AdamW |
| lr0 | 0.001 |

训练输出目录：`runs/train/partial_fullbox_yolo12n_cpu`

## 训练结果

| 项目 | 结果 |
|---|---:|
| train/box_loss | 2.98295 |
| train/cls_loss | 3.34300 |
| train/dfl_loss | 3.85355 |
| val/box_loss | 3.14378 |
| val/cls_loss | 3.80928 |
| val/dfl_loss | 3.99247 |
| Precision | 0.00422 |
| Recall | 1.00000 |
| mAP@50 | 0.01822 |
| mAP@50-95 | 0.00284 |

权重文件：

- `runs/train/partial_fullbox_yolo12n_cpu/weights/best.pt`
- `runs/train/partial_fullbox_yolo12n_cpu/weights/last.pt`

训练生成图表：

- `runs/train/partial_fullbox_yolo12n_cpu/results.png`
- `runs/train/partial_fullbox_yolo12n_cpu/confusion_matrix.png`
- `runs/train/partial_fullbox_yolo12n_cpu/BoxPR_curve.png`

## 独立验证与推理

独立验证输出：`reports/partial_fullbox_evaluation_metrics.json`

| 指标 | 结果 |
|---|---:|
| Precision | 0.004441 |
| Recall | 1.000000 |
| mAP@50 | 0.017395 |
| mAP@50-95 | 0.002704 |

单图推理输出：

- `runs/predict/partial_fullbox_image/image/predictions.json`
- `runs/predict/partial_fullbox_image/image/Sigualuo117.jpg`

本次推理使用 `conf=0.01` 只是为了检查模型是否输出检测框；结果中大量检测置信度约为 0.011，不能作为可用识别结果。

## CPU benchmark

| 项目 | 结果 |
|---|---:|
| 测试图片数 | 20 |
| imgsz | 320 |
| 平均延迟 | 28.67 ms |
| 中位延迟 | 26.77 ms |
| 最小延迟 | 18.57 ms |
| 最大延迟 | 43.53 ms |
| FPS 估计 | 34.87 |
| RAM 增量 | 21.21 MB |

Benchmark 文件：`runs/benchmarks/partial_fullbox_latency.json`

## 限制

1. 当前数据没有真实 bbox，整图框标签不等价于真实检测标注。
2. 当前只包含 `丝瓜络`、`九香虫` 两类，不是原始 `data.yaml` 声明的 100 类完整数据。
3. 本次只跑 CPU 1 epoch，指标很低，不能写成正式模型性能。
4. 若要得到可用于汇报的真实检测指标，需要补充真实 YOLO bbox 标注，或明确项目阶段改为分类任务。
