# 基于 YOLOv12 的中药饮片智能识别与分类系统 PPT 详细大纲

本版大纲按概要设计检查要求重排为“一个点一页”。建议共 7 页，适配 5 分钟汇报；每页只讲一个主题，避免把分类已完成内容和检测待完成内容混在一起。

## 汇报总边界

- 当前可信成果：已完成环境搭建、YOLOv12 分类基础模型跑通、真实中药饮片分类数据清洗、训练评估、Top-k 推理、FastAPI 后端和 Vue3 前端联调。
- 当前主线任务：中药饮片图像分类识别。
- 当前检测任务状态：只完成 bbox 标注准备包，覆盖 93 类、279 张待标注图片；`labels/` 仍为空，不能汇报检测 mAP、Precision、Recall。

## 第 1 页：概要设计基本要求

页面标题：本阶段已完成环境搭建并跑通 YOLOv12 基础分类模型

对应要求：完成搭建环境、跑通公开代码或基础模型。

页面内容：

- 项目环境：Windows 本地工程，Python 虚拟环境，核心依赖包含 PyTorch、Ultralytics、FastAPI、Vue3。
- 算法框架：以 YOLOv12 为主线，当前跑通 `yolo12n-cls.yaml` 分类基础模型。
- 工程目录：`yolo12_tcm_project/` 已包含 `backend/`、`frontend/`、`configs/`、`scripts/`、`reports/`、`runs/`。
- 已跑通链路：数据清洗 -> 分类训练 -> 独立验证 -> 单图 Top-k 推理 -> 后端 API -> 前端展示。
- 关键产物：`runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`。

建议画面：

- 左侧放“环境/代码/模型/系统”四个状态块。
- 右侧放工程链路图：数据集 -> YOLOv12n-cls -> 评估报告 -> FastAPI -> Vue3。

讲述重点：

- 本页先回答老师最基本的检查点：环境不是停留在配置，基础模型已经训练并能被系统调用。
- 不要在本页展开模型结构或实验指标，留给后面页面。

## 第 2 页：系统目标

页面标题：系统目标是构建可复现的中药饮片智能分类识别闭环

对应要求：系统目标。

页面内容：

- 识别目标：对中药饮片图片输出类别、Top-k 候选和置信度。
- 数据目标：将原始图片清洗为可训练、可验证、可复审的 strict JPEG 数据集。
- 模型目标：基于 YOLOv12n-cls 完成训练、验证、推理和权重保存。
- 系统目标：通过 FastAPI + Vue3 提供图片上传、模型选择和识别结果展示。
- 阶段边界：当前汇报分类识别成果；检测任务需等待 bbox 标注完成后再训练和评估。

关键数字：

- strict 分类数据集：92 类，7826 张训练图，1741 张验证图，总计 9567 张。
- 当前最佳分类结果：Top-1 Accuracy 0.6295，Top-5 Accuracy 0.8621。
- 检测准备包：93 类、279 张待标注图片，尚未形成检测训练数据。

建议画面：

- 用一个“四目标闭环”图：数据目标、模型目标、系统目标、复现目标。
- 页脚放红色或灰色边界提示：当前不汇报检测指标。

讲述重点：

- 强调项目目标不是单纯跑模型，而是做出从数据到前端演示的闭环。
- 明确分类和检测的阶段差异，避免老师追问检测指标时被动。

## 第 3 页：功能概述

页面标题：系统功能由前端交互、后端接口和训练评估脚本共同支撑

对应要求：功能概述。

页面内容：

- 前端功能：Vue3 识别工作台，包含“分类识别、目标检测、摄像头、训练入口”四个页签。
- 当前可演示功能：上传图片后调用分类接口，返回 Top-k 类别、置信度、结果图和 JSON。
- 模型管理功能：通过 `/models` 查询本地 `.pt` 权重，前端可选择推理模型。
- 后端接口：FastAPI 提供 `/health`、`/models`、`/classify/image`、`/detect/image`、`/train/start`。
- 工程验证：后端 QA 4/4 通过，前端 Playwright QA 6/6 通过。

建议画面：

- 放三层架构图：Vue3 前端 -> FastAPI 后端 -> YOLOv12/本地文件系统。
- 右侧放接口表：

| 接口 | 当前状态 | 用途 |
|---|---|---|
| `GET /health` | 已通过 | 服务健康检查 |
| `GET /models` | 已通过 | 查询权重 |
| `POST /classify/image` | 已通过 | 分类 Top-k 推理 |
| `POST /detect/image` | 预留接口 | 待真实检测权重 |
| `POST /train/start` | 已实现入口 | 启动训练任务 |

讲述重点：

- 当前主展示功能是图片分类识别。
- 目标检测和摄像头入口已经预留，但不能说成真实检测功能已完成。

## 第 4 页：基础模型结构

页面标题：基础模型采用 YOLOv12n-cls 进行 92 类中药饮片分类

对应要求：基础模型结构。

页面内容：

- 模型名称：YOLOv12n-cls。
- 模型配置：`yolo12n-cls.yaml`。
- 输入尺寸：224 x 224。
- 输出形式：92 类概率分布，前端展示 Top-k 分类结果。
- 结构理解：Backbone 提取纹理、颜色、边缘和形态特征；Classification Head 输出类别概率。
- 训练策略：GPU 优化实验使用 AdamW、batch 64、`pretrained: true`、device 0。

建议画面：

- 用简化结构图表示：输入图片 -> Backbone 特征提取 -> 分类头 -> Top-k 类别。
- 右侧列训练参数表：

| 参数 | 配置 |
|---|---|
| model | `yolo12n-cls.yaml` |
| data | `data/classification_strict_jpeg` |
| imgsz | 224 |
| batch | 64 |
| optimizer | AdamW |
| pretrained | true |
| device | GPU `0` |

讲述重点：

- 中药饮片是细粒度图像分类任务，难点在纹理相似、颜色接近、形态破碎。
- 本阶段先采用轻量级分类模型验证路线，后续再考虑更大模型或检测模型。

## 第 5 页：核心算法设计

页面标题：核心算法流程从数据清洗开始，最终服务于 Top-k 推理展示

对应要求：核心算法设计。

页面内容：

1. 原始数据读取：从 `D:\AAA中药cv\data` 读取中药饮片分类目录。
2. strict JPEG 清洗：剔除损坏图和异常格式，统一为可训练图片。
3. 类别一致性审计：发现原始数据 93 类，strict 基线纳入 92 类；`大腹皮` 原始训练样本为 0。
4. 重复与泄漏审计：检查 exact duplicate、train/val 泄漏和跨类别重复。
5. YOLOv12n-cls 训练：生成 `best.pt`、`last.pt`、`results.csv`、`results.png`。
6. 独立验证与推理：输出 Top-1、Top-5、Fitness 和单图 Top-k JSON。
7. 服务化接入：FastAPI 封装推理接口，Vue3 前端展示识别结果。

建议画面：

- 横向流程图：数据 -> 清洗 -> 审计 -> 训练 -> 评估 -> API -> 前端。
- 每个节点下面放一个关键路径：
  - 数据集：`data/classification_strict_jpeg`
  - 训练配置：`configs/train_cls_strict_gpu_100e.yaml`
  - 指标：`reports/strict_classification_gpu_100e_evaluation_metrics.json`
  - 前端 QA：`reports/frontend_qa.md`

讲述重点：

- 数据质量控制是本项目的核心算法前置环节。
- 本阶段算法输出是分类概率和 Top-k，不是检测框。

## 第 6 页：基于基础模型已完成的实验与训练结果

页面标题：GPU 100 epoch 训练使 Top-1 提升至 0.6295，Top-5 提升至 0.8621

对应要求：基于基础模型已完成的实验或模型训练基础结果，包含验证集/测试集 Loss 曲线、准确率曲线等。

页面内容：

- CPU 基线实验：CPU 训练 5 epoch，`pretrained: false`，Top-1 0.1769，Top-5 0.4957。
- GPU 优化实验：GPU 训练约 100 epoch，`pretrained: true`，Top-1 0.6295，Top-5 0.8621。
- 曲线结果：`results.csv/results.png` 显示 train/loss 整体下降，Top-1、Top-5 持续上升并在后期趋稳。
- 第 100 epoch 指标点：train/loss 0.99491，val/loss 1.51897，Top-1 0.62895，Top-5 0.86215。
- 结论：GPU 训练、充分 epoch 和预训练迁移显著提升分类识别能力。

建议画面：

- 左侧放训练曲线图：`runs/train/strict_classify_yolo12n_cls_gpu_100e/results.png`。
- 右侧放实验对比表：

| 实验 | 设备/轮次 | 预训练 | Top-1 | Top-5 |
|---|---|---:|---:|---:|
| CPU 基线 | CPU / 5 epoch | false | 0.1769 | 0.4957 |
| GPU 优化 | GPU / 100 epoch | true | 0.6295 | 0.8621 |

讲述重点：

- 这一页集中回答“已完成实验”和“训练基础结果”。
- 如果老师问测试集，需要说明当前项目材料中可靠指标主要来自验证集/独立验证；后续会补充严格测试集评估。

## 第 7 页：准备做的改进点与后续实验计划

页面标题：后续将按数据清理、模型升级和检测扩展三条线推进

对应要求：准备做的改进点/准备做什么实验，本阶段不要求已实现。

页面内容：

- 数据清理实验：人工处理 34 组跨类别重复图片，填写决策表，生成清理计划后重建数据集。
- 重训练实验：基于清理后的候选数据集重新训练 YOLOv12n-cls，对比 Top-1、Top-5、混淆矩阵变化。
- 模型升级实验：尝试 `yolo12s-cls`，对比输入尺寸 320/384、batch、学习率和增强策略。
- 难样本增强实验：针对高频混淆类别补充样本，重点提升相似饮片识别能力。
- 检测扩展实验：完成 93 类 279 张 bbox 标注，校验 YOLO 标签后训练检测模型，再汇报 mAP、Precision、Recall。
- 系统完善：补充真实部署压测，完善摄像头连续识别和训练任务状态展示。

建议画面：

- 用三阶段路线图：
  - 阶段一：数据质量治理
  - 阶段二：分类精度提升
  - 阶段三：目标检测落地
- 页脚放最后边界：检测指标必须等真实 bbox 标注和检测训练完成后再汇报。

讲述重点：

- 后续计划不是简单增加模型，而是先解决数据质量，再提升模型，最后扩展检测。
- 这页可作为结尾页停留，方便回答问题。

## 可直接使用的素材路径

- 概要设计要求：`概要设计.pptx`
- 当前修正版 PPT：`基于YOLOv12的中药饮片智能识别与分类系统_修正版.pptx`
- 项目 README：`yolo12_tcm_project/README.md`
- GPU 指标：`yolo12_tcm_project/reports/strict_classification_gpu_100e_evaluation_metrics.json`
- GPU 曲线：`yolo12_tcm_project/runs/train/strict_classify_yolo12n_cls_gpu_100e/results.png`
- GPU 权重：`yolo12_tcm_project/runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`
- CPU 基线报告：`yolo12_tcm_project/reports/strict_classification_training_report.md`
- 检测标注准备包：`yolo12_tcm_project/reports/detection_annotation_package_report.md`
- 后端 QA：`yolo12_tcm_project/reports/backend_qa.md`
- 前端 QA：`yolo12_tcm_project/reports/frontend_qa.md`

## 不应写进 PPT 的表述

- 不要写“已完成目标检测模型训练”。
- 不要写“检测 mAP 已达到某数值”。
- 不要把 `/detect/image` 预留接口等同于真实检测能力。
- 不要把 93 类 1 epoch 冒烟训练结果当作主结果。
- 不要把单张样例预测错误解释为系统不可用；应说明它反映当前 Top-1 仍有提升空间。
