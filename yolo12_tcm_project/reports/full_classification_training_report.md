# 完整数据集分类训练报告

更新时间：2026-06-07  
项目目录：`D:\AAA中药cv\yolo12_tcm_project`

## 结论

当前 `D:\AAA中药cv\data` 是分类数据集，不是带真实 bbox 的 YOLO 目标检测数据集。目录中未发现 `.txt`、`.xml`、`.json`、`.csv` 等可用于生成真实目标框的标注文件，因此不能自动补出真实 YOLO bbox 标注。

本轮按第二方案执行：使用完整数据来源进行 YOLOv12 图像分类训练。训练已在 CPU 环境完成 1 epoch 冒烟/部分训练，验证了完整数据处理、训练、验证、权重保存和指标导出链路。

## 数据审计

- 原始数据路径：`D:\AAA中药cv\data`
- 原始图片数：9614
- 原始结构：`train/<类别名>/*.jpg`、`val/<类别名>/*.jpg`
- bbox 标注文件：未发现
- 初步图片可读性检查：9614 张均可被 Pillow `verify()` 读取
- 类别一致性问题：`大腹皮` 只出现在 `val`，没有训练样本

清洗后的分类训练数据：

- 路径：`D:\AAA中药cv\yolo12_tcm_project\data\classification_clean`
- 类别数：92
- 训练图像：7847
- 验证图像：1748
- 总图像：9595
- 排除类别：`大腹皮`，原因是仅有验证集样本，没有训练集样本

详细文件：

- `D:\AAA中药cv\yolo12_tcm_project\reports\full_classification_dataset_inspection.md`
- `D:\AAA中药cv\yolo12_tcm_project\data\classification_clean\classification_clean_report.md`

## 图片内容审计

严格内容扫描发现 150 个图片内容问题：

- `extension_content_mismatch`: 122 张，主要是 `.jpg` 扩展名但实际内容为 PNG。此类通常仍可被 PIL/Ultralytics 读取。
- `unsupported_content_format`: 25 张，主要是 `.jpg` 扩展名但实际内容为 GIF。Ultralytics 验证阶段会忽略其中不支持的图。
- `load_failed`: 3 张，图片流损坏。
- 按划分统计：train 126 张，val 24 张。

详细文件：

- `D:\AAA中药cv\yolo12_tcm_project\reports\full_classification_image_content_audit.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\full_classification_image_content_audit.json`

## 训练环境

- Python：3.13.7
- Ultralytics：8.4.60
- PyTorch：2.12.0+cpu
- CUDA：不可用
- 设备：CPU，Intel Core i9-13980HX

## 训练配置

训练脚本：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_smoke.yaml
```

关键配置：

- 模型：`yolo12n-cls.yaml`
- 数据：`data/classification_clean`
- 训练轮次：1 epoch
- 输入尺寸：224
- batch：16
- 优化器：AdamW
- 学习率：0.001
- 设备：CPU
- 预训练：false

说明：本机没有 `yolo12n-cls.pt` 预训练分类权重，自动加载也未成功，因此本轮使用 YOLOv12n 分类结构从头训练。该结果用于证明流程可运行，不代表正式最终准确率。

## 训练结果

训练输出目录：

`D:\AAA中药cv\yolo12_tcm_project\runs\train\full_classify_yolo12n_cls_cpu_smoke`

权重文件：

- `D:\AAA中药cv\yolo12_tcm_project\runs\train\full_classify_yolo12n_cls_cpu_smoke\weights\best.pt`
- `D:\AAA中药cv\yolo12_tcm_project\runs\train\full_classify_yolo12n_cls_cpu_smoke\weights\last.pt`

训练阶段指标：

| epoch | train/loss | val/loss | Top-1 | Top-5 | 用时 |
|---:|---:|---:|---:|---:|---:|
| 1 | 4.40644 | 4.33965 | 0.04767 | 0.19586 | 178.337 s |

独立验证指标：

| 指标 | 数值 |
|---|---:|
| Top-1 Accuracy | 0.0476737507 |
| Top-5 Accuracy | 0.1958644390 |
| Fitness | 0.1217690948 |
| 推理耗时 | 约 2.5 ms/image，CPU |

验证输出：

- `D:\AAA中药cv\yolo12_tcm_project\reports\full_classification_evaluation_metrics.json`
- `D:\AAA中药cv\yolo12_tcm_project\runs\classify\val`

## 指标解释

Top-1 约 4.77%、Top-5 约 19.59%。这个结果偏低是预期现象，原因包括：

- 92 类任务类别多。
- 仅训练 1 epoch。
- 使用 CPU，训练预算很小。
- 使用 `yolo12n-cls.yaml` 从头训练，没有加载 YOLOv12 分类预训练权重。
- 数据中存在若干扩展名与真实内容不一致、GIF 伪装为 JPG、损坏图片等质量问题。

因此，本轮指标只能作为“完整数据训练链路已跑通”的阶段性记录，不能作为最终模型性能。

## 后续正式训练建议

分类路线：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_full_gpu.yaml
```

若没有 GPU，可先使用：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_full_cpu.yaml
```

正式训练前建议：

- 修复或删除 `reports/full_classification_image_content_audit.md` 中列出的 GIF 伪 JPG 和损坏图片。
- 为 `大腹皮` 补充训练样本，或从验证集移除该类别。
- 优先获取或训练 YOLOv12 分类预训练权重，再进行微调。
- 正式训练至少 30-100 epoch，并输出混淆矩阵、Top-1/Top-5、每类准确率、推理延迟和模型大小。

检测路线：

- 若课程最终必须展示目标检测能力，需要使用 LabelImg、CVAT、Label Studio 或 Roboflow 人工/半自动标注 bbox，并导出 YOLO `.txt` 标签。
- 不能把当前分类目录直接声称为真实目标检测标注。
- 若使用整图框 YOLO 数据，只能标注为弱标注流程演示，不能作为真实定位能力证明。
