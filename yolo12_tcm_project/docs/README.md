# 基于 YOLOv12 的中草药饮片智能识别与分类系统

本工程面向课程项目交付，围绕“数据集准备 -> YOLOv12 训练 -> 模型评估 -> 在线推理 -> 结果展示”的闭环搭建。

## 当前状态

- 已完成工程骨架、数据集校验/划分脚本、YOLOv12 训练/调参/评估/推理脚本。
- 已完成 FastAPI 后端和 Vue3 前端工作台。
- 已完成测试报告模板和概要设计 PPT 生成脚本。
- 已接入真实中药饮片分类数据，完成 strict JPEG 清洗、YOLOv12n 分类 5 epoch CPU 训练和独立验证。
- 已新增 93 类补齐实验数据集和 YOLOv12n 分类 1 epoch CPU 冒烟训练，`大腹皮` 已由 val-only 样本重划进入 train/val。
- 已新增 exact duplicate / train-val 泄漏审计，发现 strict 与 93 类补齐数据均有 34 组 train/val exact duplicate、52 组跨类别 exact duplicate；已生成覆盖全部 34 组泄漏的人工复核包，并构建两个候选泄漏清理集，均已移除 val 侧泄漏副本、train/val 泄漏归零；剩余 34 组跨类别 exact duplicate 已生成 `classification_cross_class_review_package` 复核包、对照图、`classification_cross_class_decision_table` 人工决策表、`classification_cross_class_cleanup_plan` 执行前校验报告和 `apply_classification_cross_class_cleanup_plan.py` 非破坏性执行入口，需人工确认真实类别。
- 已生成检测 bbox 人工标注准备包、标注样本总览 contact sheet，并完成 pending 状态校验，覆盖 93 类、279 张待标注图片；`labels/` 仍为空，不可直接训练检测模型。
- 已补齐 strict 分类权重的 Top-k 推理脚本、CPU benchmark、每类误判分析、人工复核 contact sheet、ONNX 导出、后端分类接口和前端分类识别入口。
- 原始数据尚未包含真实 bbox 标注，因此检测 mAP、Precision、Recall 仍必须在补充真实检测标注后生成。

## 环境搭建

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\scripts\setup_env.ps1
.\.venv\Scripts\Activate.ps1
```

如需手动安装，Windows 上优先使用 `py -3`，避免系统 `python.exe` 指向 WindowsApps 占位入口：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 数据准备

标准 YOLO 数据集应包含：

```text
data/yolo/
  images/
  labels/
  classes.txt 或 data.yaml
```

检查数据：

```powershell
python scripts\validate_yolo_dataset.py --images data/yolo/images --labels data/yolo/labels --data-yaml configs/data.yaml
```

划分数据：

```powershell
python scripts\split_yolo_dataset.py --images data/yolo/images --labels data/yolo/labels --output data/splits --overwrite
```

如果只有分类目录，可临时转换为整图框检测格式：

```powershell
python scripts\download_or_prepare_dataset.py --source data/raw/classification_dataset --mode classification --output data/yolo --overwrite
```

注意：整图框只能跑通流程，不等价于真实检测标注。

## 真实分类数据实验

用户补充的 `D:\AAA中药cv\data` 是分类目录结构：

```text
data/
  train/<类别名>/*.jpg
  val/<类别名>/*.jpg
```

当前未发现可用于真实目标检测训练的 `.txt`、`.xml`、`.json`、`.csv` bbox 标注文件，因此本阶段采用分类路线作为可信实验。

strict 数据集清洗、检查、训练和评估：

```powershell
python scripts\prepare_strict_classification_dataset.py --source ..\data --output data\classification_strict_jpeg --overwrite
python scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg --verify-images --output reports\strict_classification_dataset_inspection.json
python scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg --output reports\strict_classification_duplicate_audit.json --markdown reports\strict_classification_duplicate_audit.md --max-groups 80
python scripts\audit_class_consistency.py --source ..\data --output reports\class_consistency_audit.json --markdown reports\class_consistency_audit.md
python scripts\prepare_completed_classification_dataset.py --source ..\data --output data\classification_strict_jpeg_93class --overwrite --report reports\classification_93class_completion_report.json --markdown reports\classification_93class_completion_report.md
python scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class --verify-images --output reports\classification_93class_dataset_inspection.json --markdown reports\classification_93class_dataset_inspection.md
python scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class --output reports\classification_93class_duplicate_audit.json --markdown reports\classification_93class_duplicate_audit.md --max-groups 80
python scripts\generate_classification_leakage_review_package.py --audit reports\strict_classification_duplicate_audit.json --reference-audit reports\classification_93class_duplicate_audit.json --output reports\classification_leakage_review_package.json --figure reports\figures\classification_train_val_leakage_contact_sheet.png
python scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_leakage_clean_candidate --report reports\classification_leakage_clean_candidate_report.json --markdown reports\classification_leakage_clean_candidate_report.md --overwrite
python scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_leakage_clean_candidate --verify-images --output reports\classification_leakage_clean_candidate_inspection.json --markdown reports\classification_leakage_clean_candidate_inspection.md
python scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_leakage_clean_candidate --output reports\classification_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_leakage_clean_candidate_duplicate_audit.md --max-groups 80
python scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg_93class --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_93class_leakage_clean_candidate --report reports\classification_93class_leakage_clean_candidate_report.json --markdown reports\classification_93class_leakage_clean_candidate_report.md --overwrite
python scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --verify-images --output reports\classification_93class_leakage_clean_candidate_inspection.json --markdown reports\classification_93class_leakage_clean_candidate_inspection.md
python scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --output reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_93class_leakage_clean_candidate_duplicate_audit.md --max-groups 80
python scripts\generate_classification_cross_class_review_package.py --audit reports\classification_leakage_clean_candidate_duplicate_audit.json --reference-audit reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --output reports\classification_cross_class_review_package.json --figure reports\figures\classification_cross_class_contact_sheet.png
python scripts\generate_classification_cross_class_decision_table.py --review-package reports\classification_cross_class_review_package.json --output reports\classification_cross_class_decision_table.json --csv reports\classification_cross_class_decision_table.csv --markdown reports\classification_cross_class_decision_table.md
python scripts\generate_classification_cross_class_cleanup_plan.py --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_cleanup_plan.json --operations-csv reports\classification_cross_class_cleanup_plan.csv --markdown reports\classification_cross_class_cleanup_plan.md
# 仅当 cleanup plan 状态为 ready_for_cleanup_execution 且校验错误为 0 时运行：
# python scripts\apply_classification_cross_class_cleanup_plan.py --source data\classification_strict_jpeg_leakage_clean_candidate --cleanup-plan reports\classification_cross_class_cleanup_plan.json --output data\classification_strict_jpeg_cross_class_clean_candidate --report reports\classification_cross_class_cleanup_execution_report.json --markdown reports\classification_cross_class_cleanup_execution_report.md
python scripts\prepare_detection_annotation_package.py --source data\classification_strict_jpeg_93class --output data\detection_annotation_package --overwrite --samples-per-class 3 --train-per-class 2 --val-per-class 1 --report reports\detection_annotation_package_report.json --markdown reports\detection_annotation_package_report.md
python scripts\generate_detection_annotation_contact_sheet.py --manifest data\detection_annotation_package\annotation_manifest.json --output reports\detection_annotation_contact_sheet.json --figure reports\figures\detection_annotation_contact_sheet.png
python scripts\validate_detection_annotation_package.py --package data\detection_annotation_package --output reports\detection_annotation_package_validation.json --markdown reports\detection_annotation_package_validation.md
python scripts\train_yolo12_cls.py --config configs\train_cls_93class_smoke.yaml
python scripts\evaluate_yolo12_cls.py --model runs\train\strict_93class_yolo12n_cls_cpu_smoke\weights\best.pt --data data\classification_strict_jpeg_93class --imgsz 224 --device cpu --output reports\classification_93class_evaluation_metrics.json
python scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_5e.yaml
python scripts\evaluate_yolo12_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg --imgsz 224 --device cpu --output reports\strict_classification_evaluation_metrics.json
python scripts\analyze_classification_errors.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg\val --imgsz 224 --device cpu --output reports\strict_classification_error_analysis.json
python scripts\generate_error_review_contact_sheet.py --analysis reports\strict_classification_error_analysis.json --output reports\strict_classification_review_samples.json
python scripts\infer_image_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --source data\classification_strict_jpeg\val\丝瓜络\Sigualuo117.jpg --imgsz 224 --device cpu --topk 5 --output reports\strict_classification_sample_prediction.json
python scripts\benchmark_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --images data\classification_strict_jpeg\val --imgsz 224 --device cpu --warmup 3 --iterations 20 --output runs\benchmarks\strict_classification_latency_20.json
python scripts\export_model.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --format onnx --imgsz 224 --simplify
python scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
```

阶段性结果：

- strict 数据集：92 类，7826 train / 1741 val，9567 张图片全部可读。
- strict 重复/泄漏审计：`reports/strict_classification_duplicate_audit.md`，发现 546 组 exact duplicate，其中 train/val 泄漏组 34、跨类别重复组 52。
- 泄漏人工复核包：`reports/classification_leakage_review_package.md/json`，对照图 `reports/figures/classification_train_val_leakage_contact_sheet.png`；覆盖 34/34 组 train/val 泄漏、69 条记录，其中 18 组同时跨类别。
- strict 候选泄漏清理集：`data/classification_strict_jpeg_leakage_clean_candidate`，92 类，7826 train / 1707 val，总计 9533 张；已移除 34 张 val 侧泄漏副本，train/val 泄漏组 0、跨类别重复组 34。
- 跨类别复核包：`reports/classification_cross_class_review_package.md/json`，对照图 `reports/figures/classification_cross_class_contact_sheet.png`；覆盖候选清理集剩余 34/34 组跨类别 exact duplicate、68 条记录，train/val 泄漏组 0，`manual_decision` 等待人工填写。
- 跨类别决策表：`reports/classification_cross_class_decision_table.md/json/csv`，状态 `ready_for_manual_decision`，34/34 组为 `pending`，校验错误 0；用于人工填写 `decision_status`、真实类别、处理动作和复核说明，不自动修改图片。
- 跨类别清理计划校验：`reports/classification_cross_class_cleanup_plan.md/json/csv`，状态 `waiting_for_manual_decisions`，计划操作 0、校验错误 0；人工填完 CSV 后先重新生成该报告，只有 `ready_for_cleanup_execution` 才进入真实清理执行。
- 跨类别清理执行入口：`scripts/apply_classification_cross_class_cleanup_plan.py` 只接受校验通过的计划；执行时复制到新的输出数据集目录，不删除或覆盖源候选集。
- 类别一致性审计：原始数据 93 类，strict 实验 92 类；`大腹皮` 只在 val 出现、训练样本为 0，需补样后恢复 93 类实验。
- 93 类补齐实验：输出 93 类，7841 train / 1745 val；`大腹皮` 由 19 张 val-only 原始样本拆为 15 train / 4 val；1 epoch CPU 冒烟训练 Top-1 0.0665、Top-5 0.2086。
- 93 类补齐重复/泄漏审计：`reports/classification_93class_duplicate_audit.md`，同样为 34 组 train/val 泄漏、52 组跨类别重复。
- 93 类候选泄漏清理集：`data/classification_strict_jpeg_93class_leakage_clean_candidate`，93 类，7841 train / 1711 val，总计 9552 张；train/val 泄漏组 0、跨类别重复组 34。
- 检测 bbox 标注准备包：`data/detection_annotation_package`，覆盖 93 类、279 张待人工标注图片；`classes.txt`、`annotation_manifest.csv/json`、`data_template.yaml` 和 `ANNOTATION_GUIDE.md` 已生成，`labels/` 仍为空。
- 检测标注样本总览：`reports/detection_annotation_contact_sheet.md/json` 与 `reports/figures/detection_annotation_contact_sheet.png`，覆盖 93 类、279 张样本，用于标注前复核。
- 检测标注包校验：`reports/detection_annotation_package_validation.md`，当前状态 `pending_bbox_annotation`，图片 279/279，缺失标签 279，errors 0，warnings 0；人工标注完成后可加 `--require-complete` 做严格验收。
- 已跳过 28 张 GIF 伪 JPG 或损坏图片，122 张 PNG 内容统一转换为 JPEG。
- 训练输出：`runs/train/strict_classify_yolo12n_cls_cpu_5e`。
- 独立验证：Top-1 0.1769，Top-5 0.4957，Fitness 0.3363。
- 每类误判分析：`reports/strict_classification_error_analysis.md`，覆盖最低/最高类别、高频混淆对和典型误判样例。
- 人工复核样例：`reports/strict_classification_review_samples.md`，配套高频混淆和低表现类别 contact sheet 图片。
- 单样例推理：`reports/strict_classification_sample_prediction.json`。
- CPU benchmark：20 张样本 mean 9.76 ms/image，约 102.51 FPS。
- ONNX：`runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx`。
- 报告：`reports/strict_classification_training_report.md`。
- 类别审计：`reports/class_consistency_audit.md`。
- 可复现实验 Manifest：`reports/repro_manifest.md`，包含环境版本、复现命令、关键指标、跨类别决策表、跨类别清理计划校验、清理执行入口和关键产物 SHA256。
- 检测标注准备包报告：`reports/detection_annotation_package_report.md`。
- 检测标注准备包校验：`reports/detection_annotation_package_validation.md`。
- 检测标注样本总览：`reports/detection_annotation_contact_sheet.md`。
- 93 类补齐报告：`reports/classification_93class_training_report.md`。
- 提交前清单：`reports/submission_checklist.md`。

后续正式训练配置：

```powershell
python scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_30e.yaml
python scripts\train_yolo12_cls.py --config configs\train_cls_strict_gpu_100e.yaml
```

## Demo 链路自检

没有真实数据时，可生成几何图形 demo 数据集验证数据脚本：

```powershell
python scripts\create_demo_dataset.py --output data/demo_yolo --overwrite
python scripts\validate_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt
python scripts\split_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output data/demo_splits --overwrite
```

该 demo 只验证链路，不能用于中药饮片精度汇报。

## 训练

基线训练：

```powershell
python scripts\train_yolo12.py --config configs/train_baseline.yaml
```

调参 dry-run：

```powershell
python scripts\tune_yolo12.py --config configs/train_tune.yaml --dry-run
```

正式调参：

```powershell
python scripts\tune_yolo12.py --config configs/train_tune.yaml
```

## 评估与推理

```powershell
python scripts\evaluate_yolo12.py --model runs/train/yolo12n_baseline/weights/best.pt --data data/splits/data.yaml --split test
python scripts\infer_image.py --model runs/train/yolo12n_baseline/weights/best.pt --source data/samples/demo.jpg
python scripts\benchmark.py --model runs/train/yolo12n_baseline/weights/best.pt --images data/splits/images/test --device cpu
python scripts\export_model.py --model runs/train/yolo12n_baseline/weights/best.pt --format onnx --simplify
```

## 后端

```powershell
.\scripts\start_backend.ps1
```

API:

- `GET /health`
- `GET /models`
- `POST /detect/image`
- `POST /classify/image`
- `POST /detect/video`
- `POST /train/start`
- `GET /metrics`

## 前端

```powershell
.\scripts\start_frontend.ps1
```

访问 `http://127.0.0.1:5173`。

## 报告与 PPT

生成概要设计 PPT：

```powershell
npm install pptxgenjs
node scripts\generate_overview_ppt.js
```

测试报告位于 `reports/test_report.md`。真实训练完成后，应把 `reports/evaluation_metrics.json`、`runs/benchmarks/latency.json`、训练曲线和混淆矩阵补入报告。
