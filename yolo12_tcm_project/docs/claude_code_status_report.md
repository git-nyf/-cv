# Claude Code 项目状态汇报

生成日期：2026-06-09

## 1. 当前项目进行到哪里

当前项目主线已经跑通到“中药饮片图像分类识别系统”的可演示阶段：

- 数据侧：已构建 `data/classification_strict_jpeg` 严格分类数据集，共 92 类、9567 张图片，其中 train 7826 张、val 1741 张。
- 模型侧：已完成 GPU 100 epoch 分类训练，当前最佳权重为 `runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`。
- 服务侧：FastAPI 后端已实现健康检查、模型列表、图片分类、图片检测占位接口、训练启动接口等。
- 前端侧：Vue + Vite 前端已实现图片上传、模型选择、分类/检测模式切换、Top-k 分类结果展示。
- 文档侧：已补充使用说明、VSCode 任务、Claude 接手说明、概要设计大纲和汇报 PPT。

需要强调：当前可信成果是“分类识别”，不是完整目标检测。检测部分只完成了 bbox 人工标注准备包，真实 bbox 标签仍未完成。

## 2. 当前效果怎么样

当前最佳分类模型：

- 权重：`runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`
- 模型：`yolo12n-cls.yaml`
- 数据：`data/classification_strict_jpeg`
- 训练：GPU 100 epoch，`pretrained: true`
- Top-1 Accuracy：0.6295，约 62.95%
- Top-5 Accuracy：0.8621，约 86.21%
- Fitness：0.7458

对比旧的 CPU 5 epoch 基线：

- 旧 Top-1：约 17.69%
- 旧 Top-5：约 49.57%
- 新 Top-1：约 62.95%
- 新 Top-5：约 86.21%

训练曲线大致表现：

- `train/loss` 从 4.4210 降到 0.9949。
- `val/loss` 从 5.4679 降到约 1.5190，后期有小幅波动。
- Top-1 / Top-5 持续提升，100 epoch 后趋于稳定。

结论：训练已经明显有效，Top-5 可用性较好，但 Top-1 仍只有约 63%，细粒度中药饮片相似类别仍会误判。下一步应先做数据质量清理，再考虑换 `yolo12s-cls`、提升 `imgsz` 到 320/384、做难样本增强。

## 3. 前端代码在哪里

前端目录：

`frontend`

核心文件：

- `frontend/src/App.vue`
  - 主页面和主要交互逻辑。
  - 包含分类/检测模式切换、模型列表加载、图片上传、请求后端接口、状态提示等。
  - 分类请求调用 `/classify/image`。
  - 检测请求调用 `/detect/image`，但检测模型训练尚未完成，不能把检测结果当作最终成果。

- `frontend/src/components/ResultPanel.vue`
  - 结果展示组件。
  - 分类模式展示 Top-k 预测类别和置信度。
  - 检测模式展示检测框数量、类别、置信度、bbox 信息。

- `frontend/src/main.js`
  - Vue 应用入口。

- `frontend/src/styles.css`
  - 全局页面样式。

前端启动方式：

- VSCode 可运行任务：`启动前端页面`
- 默认访问地址：`http://127.0.0.1:5173`

## 4. 后端代码在哪里

后端目录：

`backend/app`

核心文件：

- `backend/app/main.py`
  - FastAPI 入口。
  - 定义主要 API：
    - `GET /health`
    - `GET /models`
    - `POST /classify/image`
    - `POST /detect/image`
    - `POST /detect/video`
    - `POST /train/start`
    - `GET /metrics`
    - `GET /files`

- `backend/app/model_service.py`
  - 模型服务核心逻辑。
  - 负责查找 `.pt` 权重、加载 Ultralytics YOLO、图片保存、分类推理、检测推理、训练子进程启动。
  - `/models` 默认按权重修改时间倒序列出模型，因此新训练的 GPU 100e `best.pt` 会优先出现。

- `backend/app/schemas.py`
  - API 请求和响应数据结构。

- `backend/app/config.py`
  - 项目路径、默认模型、预测输出目录等配置。

后端启动方式：

- VSCode 可运行任务：`启动后端 API`
- 默认访问地址：`http://127.0.0.1:8000`
- API 文档：`http://127.0.0.1:8000/docs`

## 5. 核心训练在哪里

核心训练配置：

`configs/train_cls_strict_gpu_100e.yaml`

当前关键超参数：

- `model: yolo12n-cls.yaml`
- `data: data/classification_strict_jpeg`
- `epochs: 100`
- `batch: 64`
- `imgsz: 224`
- `optimizer: AdamW`
- `lr0: 0.001`
- `weight_decay: 0.0005`
- `patience: 20`
- `device: 0`
- `seed: 42`
- `pretrained: true`

训练脚本：

`scripts/train_yolo12_cls.py`

评估脚本：

`scripts/evaluate_yolo12_cls.py`

训练产物：

- 权重：`runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`
- 末轮权重：`runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/last.pt`
- 训练曲线 CSV：`runs/train/strict_classify_yolo12n_cls_gpu_100e/results.csv`
- 训练曲线图：`runs/train/strict_classify_yolo12n_cls_gpu_100e/results.png`
- 混淆矩阵：`runs/train/strict_classify_yolo12n_cls_gpu_100e/confusion_matrix.png`
- 评估 JSON：`reports/strict_classification_gpu_100e_evaluation_metrics.json`

VSCode 训练任务：

- `训练分类模型 GPU 100e`
- `评估 GPU 100e 分类模型`

## 6. 目前不要误判的边界

1. 当前不是完整检测系统。
   - `data/detection_annotation_package` 只是 bbox 人工标注准备包。
   - 状态是 `pending_bbox_annotation`。
   - 93 类、279 张待标注图。
   - `labels_completed: 0`。
   - 不要汇报检测 mAP、检测 Precision、检测 Recall。

2. 数据质量还有人工决策未完成。
   - 跨类别 exact duplicate 共 34 组。
   - 清理计划状态：`waiting_for_manual_decisions`。
   - 决策表：`reports/classification_cross_class_decision_table.csv`
   - 复核页面：`reports/classification_cross_class_decision_review.html`
   - 当前不能自动删除或移动这些图片。

3. 93 类补齐实验不是主基准。
   - 当前主基准是 92 类 strict 分类数据集。
   - 93 类更多用于补齐链路和检测标注准备，不替代当前 92 类 strict 结果。

## 7. 建议 Claude Code 下一步做什么

优先级 1：做数据质量人工决策闭环。

- 打开 `reports/classification_cross_class_decision_review.html`。
- 填写 `reports/classification_cross_class_decision_table.csv`。
- 重新生成 cleanup plan。
- 只有状态变成 `ready_for_cleanup_execution` 且 validation errors 为 0 时，才执行清理。

优先级 2：基于干净数据重训分类模型。

- 继续使用 GPU。
- 先复现当前 `yolo12n-cls` 100e 结果。
- 再尝试 `yolo12s-cls`。
- 再尝试 `imgsz: 320` 或 `384`。

优先级 3：检测任务必须先完成 bbox 标注。

- 完成 `data/detection_annotation_package` 内 279 张样本标注。
- 运行 `scripts/validate_detection_annotation_package.py --require-complete`。
- 校验通过后再训练检测模型。

## 8. 一句话总结

项目已经完成“92 类中药饮片分类识别”的前后端闭环和 GPU 100 epoch 模型训练，当前 Top-1 约 62.95%、Top-5 约 86.21%；下一阶段重点不是继续包装页面，而是先清理 34 组跨类别重复数据，再提升分类精度，最后补齐 bbox 标注后再做真实目标检测。
