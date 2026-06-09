# 93 类补齐实验训练报告

更新时间：2026-06-07  
项目目录：`D:\AAA中药cv\yolo12_tcm_project`

## 结论

本轮已新增并跑通 93 类补齐实验链路：在保持原 92 类 strict 基准不变的前提下，单独生成 `classification_strict_jpeg_93class` 数据集，将原始数据中只出现在验证集的 `大腹皮` 19 张样本按确定性顺序拆为 15 张 train、4 张 val，并完成 YOLOv12n 分类 CPU 1 epoch 冒烟训练与独立验证。

独立验证摘要：Top-1 0.0665，Top-5 0.2086，Fitness 0.1375。

该实验解决的是“完整 93 类能否进入训练/评估链路”的类别覆盖问题，不替代 `classification_strict_jpeg` 的 92 类 5 epoch strict 基准，也不应直接与原始 92 类 strict 指标等价比较。

## 数据集

生成命令：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\prepare_completed_classification_dataset.py `
  --source ..\data `
  --output data\classification_strict_jpeg_93class `
  --overwrite `
  --report reports\classification_93class_completion_report.json `
  --markdown reports\classification_93class_completion_report.md
```

复审命令：

```powershell
.\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py `
  --source data\classification_strict_jpeg_93class `
  --verify-images `
  --output reports\classification_93class_dataset_inspection.json `
  --markdown reports\classification_93class_dataset_inspection.md
```

| 项目 | 结果 |
|---|---:|
| 原始类别 | 93 |
| 输出类别 | 93 |
| train 图像 | 7841 |
| val 图像 | 1745 |
| 总图像 | 9586 |
| 跳过 GIF/损坏图 | 28 |
| 转换为 JPEG | 122 |
| 直接 JPEG | 9464 |
| verified images | 9586 |
| errors / warnings | 0 / 0 |

`大腹皮` 处理策略：

| 类别 | 原始 train | 原始 val | 输出 train | 输出 val | 策略 |
|---|---:|---:|---:|---:|---|
| 大腹皮 | 0 | 19 | 15 | 4 | `rebalance_val_only` |

## 训练配置

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_93class_smoke.yaml
```

关键参数：

- 模型：`yolo12n-cls.yaml`
- 数据：`data/classification_strict_jpeg_93class`
- epoch：1
- imgsz：224
- batch：16
- optimizer：AdamW
- lr0：0.001
- device：CPU
- seed：42
- pretrained：false

训练输出：

- `runs/train/strict_93class_yolo12n_cls_cpu_smoke`
- `runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt`
- `runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/last.pt`

训练日志：

| epoch | train/loss | val/loss | Top-1 | Top-5 | 用时 |
|---:|---:|---:|---:|---:|---:|
| 1 | 4.40445 | 4.22270 | 0.06648 | 0.20860 | 200.041 s |

## 独立验证

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py `
  --model runs\train\strict_93class_yolo12n_cls_cpu_smoke\weights\best.pt `
  --data data\classification_strict_jpeg_93class `
  --imgsz 224 `
  --device cpu `
  --output reports\classification_93class_evaluation_metrics.json
```

| 指标 | 数值 |
|---|---:|
| Top-1 Accuracy | 0.0664756447 |
| Top-5 Accuracy | 0.2085959911 |
| Fitness | 0.1375358179 |

## 边界说明

- 该实验为 93 类覆盖链路验证，训练轮次只有 1 epoch，指标只能证明流程可运行。
- `大腹皮` 由原始 val-only 样本重划得到 train/val，不是新增采集样本。
- 92 类 strict 5 epoch 结果仍是当前较强分类基准：Top-1 0.1769、Top-5 0.4957。
- 当前真实数据仍不含 bbox 标注，不能据此汇报检测 Precision、Recall、mAP 或定位能力。
