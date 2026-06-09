# 基于 YOLOv12 的中草药饮片智能识别与分类系统

这是课程项目工程入口。完整说明见 [docs/README.md](docs/README.md)。

## 快速开始

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\scripts\setup_env.ps1
.\.venv\Scripts\Activate.ps1
```

启动后端：

```powershell
.\scripts\start_backend.ps1
```

启动前端：

```powershell
.\scripts\start_frontend.ps1
```

## 主要交付物

- `scripts/`：数据检查、划分、训练、调参、评估、推理、导出、性能测试脚本。
- `scripts/create_demo_dataset.py`：生成仅用于链路自检的微型 YOLO demo 数据集。
- `scripts/infer_image_cls.py`、`scripts/benchmark_cls.py`、`scripts/analyze_classification_errors.py`、`scripts/generate_error_review_contact_sheet.py`、`scripts/audit_class_consistency.py`、`scripts/audit_classification_duplicates.py`、`scripts/generate_classification_leakage_review_package.py`、`scripts/prepare_leakage_clean_classification_dataset.py`、`scripts/generate_classification_cross_class_review_package.py`、`scripts/generate_classification_cross_class_decision_table.py`、`scripts/generate_classification_cross_class_cleanup_plan.py`、`scripts/apply_classification_cross_class_cleanup_plan.py`、`scripts/prepare_completed_classification_dataset.py`、`scripts/prepare_detection_annotation_package.py`、`scripts/generate_detection_annotation_contact_sheet.py`、`scripts/validate_detection_annotation_package.py`、`scripts/generate_repro_manifest.py`：strict 分类权重的 Top-k 推理、CPU 延迟测试、每类误判分析、人工复核 contact sheet、类别一致性审计、exact duplicate / train-val 泄漏审计、34 组泄漏人工复核包、候选泄漏清理数据集、34 组跨类别 exact duplicate 复核包、跨类别标签冲突人工决策表、跨类别清理计划校验、跨类别清理非破坏性执行入口、93 类补齐数据集、检测标注准备包、标注样本总览、标注包校验和可复现实验 manifest 脚本。
- `data/classification_strict_jpeg/`：由用户补充的真实分类数据清洗得到的 strict JPEG 数据集。
- `data/classification_strict_jpeg_leakage_clean_candidate/`：基于泄漏复核包仅移除 34 张 val 侧 train/val exact duplicate 副本的 strict 候选清理集；train/val 泄漏归零，但仍有 34 组跨类别 exact duplicate 待人工复核。
- `data/classification_strict_jpeg_93class/`：93 类补齐实验数据集，`大腹皮` 由原始 val-only 样本确定性重划为 15 train / 4 val。
- `data/classification_strict_jpeg_93class_leakage_clean_candidate/`：93 类补齐数据的候选泄漏清理集，同样仅移除 val 侧泄漏副本。
- `data/detection_annotation_package/`：检测 bbox 人工标注准备包，覆盖 93 类、279 张待标注图片；`labels/` 仍为空，不可直接训练检测模型。
- `backend/`：FastAPI 推理服务，包含 `/detect/image` 检测接口与 `/classify/image` 分类接口。
- `frontend/`：Vue3 识别工作台，默认提供分类识别入口，保留目标检测入口。
- `configs/`：YOLOv12 数据和训练配置。
- `reports/test_report.md`：测试报告。
- `reports/strict_classification_training_report.md`：strict 分类数据 5 epoch 训练报告。
- `reports/classification_93class_training_report.md`：93 类补齐实验 1 epoch 训练报告。
- `reports/detection_annotation_package_report.md`：检测 bbox 标注准备包报告，固定类别顺序、抽样 manifest 和空标签边界。
- `reports/detection_annotation_package_validation.md`：检测标注准备包校验报告，当前为 `pending_bbox_annotation`，用于后续人工标注完成后的严格验收。
- `reports/detection_annotation_contact_sheet.md`：检测标注样本总览索引；配套 PNG 位于 `reports/figures/detection_annotation_contact_sheet.png`，覆盖 93 类、279 张待标注样本。
- `reports/class_consistency_audit.md`：原始 93 类与 strict 92 类的类别一致性审计报告。
- `reports/strict_classification_duplicate_audit.md`、`reports/classification_93class_duplicate_audit.md`：分类数据 exact duplicate 与 train/val 泄漏审计报告。
- `reports/classification_leakage_review_package.md`：34 组 train/val exact duplicate 人工复核包；配套对照图位于 `reports/figures/classification_train_val_leakage_contact_sheet.png`。
- `reports/classification_leakage_clean_candidate_report.md`、`reports/classification_93class_leakage_clean_candidate_report.md`：候选泄漏清理报告；证明 val 侧泄漏副本已移除，但跨类别重复仍需人工复核。
- `reports/classification_cross_class_review_package.md`：候选清理集剩余 34 组跨类别 exact duplicate 人工复核包；配套对照图位于 `reports/figures/classification_cross_class_contact_sheet.png`。
- `reports/classification_cross_class_decision_table.md`、`reports/classification_cross_class_decision_table.csv`、`reports/classification_cross_class_decision_table.json`：跨类别标签冲突人工决策表，当前 34 / 34 组仍为 `pending`，用于人工填写真实类别、处理动作和复核说明。
- `reports/classification_cross_class_cleanup_plan.md`、`reports/classification_cross_class_cleanup_plan.csv`、`reports/classification_cross_class_cleanup_plan.json`：跨类别清理计划校验报告，当前状态 `waiting_for_manual_decisions`，用于人工填完决策 CSV 后做执行前 dry-run 校验；不修改数据集。
- `scripts/apply_classification_cross_class_cleanup_plan.py`：跨类别清理执行入口，只接受 `ready_for_cleanup_execution` 且校验错误为 0 的计划；执行时只写入新的输出目录，不删除或覆盖源数据集。
- `reports/repro_manifest.md`：可复现实验 Manifest，汇总环境版本、复现命令、关键指标和产物 SHA256。
- `reports/strict_classification_error_analysis.md`：strict 验证集每类表现、Top-1/Top-5 和高频混淆对分析。
- `reports/strict_classification_review_samples.md`：高频混淆与低表现类别人工复核样例清单，配套 contact sheet 图片位于 `reports/figures/`。
- `reports/submission_checklist.md`：提交前检查清单。
- `reports/overview_design.pptx`：概要设计汇报 PPT。

## 当前限制

当前工程已接入真实中药饮片分类数据，并完成 strict JPEG 数据清洗与 YOLOv12n 分类 5 epoch CPU 训练，独立验证 Top-1 为 0.1769、Top-5 为 0.4957。类别一致性审计显示原始数据为 93 类，strict 基准实验为 92 类；本轮已新增 93 类补齐实验，将 `大腹皮` 原始 val-only 样本确定性重划为 15 train / 4 val，并完成 1 epoch CPU 冒烟训练，Top-1 为 0.0665、Top-5 为 0.2086。当前已生成覆盖全部 34 组 train/val exact duplicate 的人工复核包，并基于该复核包构建 strict 与 93 类两个候选泄漏清理集：均只移除 val 侧泄漏副本，train/val 泄漏归零；剩余 34 组跨类别 exact duplicate 已单独生成复核包、对照图、可填写决策表、执行前校验报告和非破坏性执行入口；当前所有组仍需人工确认真实类别后再删除、移动、重标或保留。检测 bbox 标注准备包覆盖 93 类、279 张待人工标注图片，但 `labels/` 仍为空。原始数据不包含真实 bbox 标注，因此仍不能汇报检测 mAP、Precision、Recall 或定位能力；这些指标必须在补充真实 YOLO 检测标注并完成训练后生成。

## 真实分类实验

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\prepare_strict_classification_dataset.py --source ..\data --output data\classification_strict_jpeg --overwrite
.\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg --verify-images --output reports\strict_classification_dataset_inspection.json
.\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg --output reports\strict_classification_duplicate_audit.json --markdown reports\strict_classification_duplicate_audit.md --max-groups 80
.\.venv\Scripts\python.exe scripts\audit_class_consistency.py --source ..\data --output reports\class_consistency_audit.json --markdown reports\class_consistency_audit.md
.\.venv\Scripts\python.exe scripts\prepare_completed_classification_dataset.py --source ..\data --output data\classification_strict_jpeg_93class --overwrite --report reports\classification_93class_completion_report.json --markdown reports\classification_93class_completion_report.md
.\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class --verify-images --output reports\classification_93class_dataset_inspection.json --markdown reports\classification_93class_dataset_inspection.md
.\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class --output reports\classification_93class_duplicate_audit.json --markdown reports\classification_93class_duplicate_audit.md --max-groups 80
.\.venv\Scripts\python.exe scripts\generate_classification_leakage_review_package.py --audit reports\strict_classification_duplicate_audit.json --reference-audit reports\classification_93class_duplicate_audit.json --output reports\classification_leakage_review_package.json --figure reports\figures\classification_train_val_leakage_contact_sheet.png
.\.venv\Scripts\python.exe scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_leakage_clean_candidate --report reports\classification_leakage_clean_candidate_report.json --markdown reports\classification_leakage_clean_candidate_report.md --overwrite
.\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_leakage_clean_candidate --verify-images --output reports\classification_leakage_clean_candidate_inspection.json --markdown reports\classification_leakage_clean_candidate_inspection.md
.\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_leakage_clean_candidate --output reports\classification_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_leakage_clean_candidate_duplicate_audit.md --max-groups 80
.\.venv\Scripts\python.exe scripts\prepare_leakage_clean_classification_dataset.py --source data\classification_strict_jpeg_93class --review-package reports\classification_leakage_review_package.json --output data\classification_strict_jpeg_93class_leakage_clean_candidate --report reports\classification_93class_leakage_clean_candidate_report.json --markdown reports\classification_93class_leakage_clean_candidate_report.md --overwrite
.\.venv\Scripts\python.exe scripts\inspect_classification_dataset.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --verify-images --output reports\classification_93class_leakage_clean_candidate_inspection.json --markdown reports\classification_93class_leakage_clean_candidate_inspection.md
.\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg_93class_leakage_clean_candidate --output reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --markdown reports\classification_93class_leakage_clean_candidate_duplicate_audit.md --max-groups 80
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_review_package.py --audit reports\classification_leakage_clean_candidate_duplicate_audit.json --reference-audit reports\classification_93class_leakage_clean_candidate_duplicate_audit.json --output reports\classification_cross_class_review_package.json --figure reports\figures\classification_cross_class_contact_sheet.png
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_decision_table.py --review-package reports\classification_cross_class_review_package.json --output reports\classification_cross_class_decision_table.json --csv reports\classification_cross_class_decision_table.csv --markdown reports\classification_cross_class_decision_table.md
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_cleanup_plan.py --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_cleanup_plan.json --operations-csv reports\classification_cross_class_cleanup_plan.csv --markdown reports\classification_cross_class_cleanup_plan.md
# 仅当 cleanup plan 状态为 ready_for_cleanup_execution 且校验错误为 0 时运行：
# .\.venv\Scripts\python.exe scripts\apply_classification_cross_class_cleanup_plan.py --source data\classification_strict_jpeg_leakage_clean_candidate --cleanup-plan reports\classification_cross_class_cleanup_plan.json --output data\classification_strict_jpeg_cross_class_clean_candidate --report reports\classification_cross_class_cleanup_execution_report.json --markdown reports\classification_cross_class_cleanup_execution_report.md
.\.venv\Scripts\python.exe scripts\prepare_detection_annotation_package.py --source data\classification_strict_jpeg_93class --output data\detection_annotation_package --overwrite --samples-per-class 3 --train-per-class 2 --val-per-class 1 --report reports\detection_annotation_package_report.json --markdown reports\detection_annotation_package_report.md
.\.venv\Scripts\python.exe scripts\generate_detection_annotation_contact_sheet.py --manifest data\detection_annotation_package\annotation_manifest.json --output reports\detection_annotation_contact_sheet.json --figure reports\figures\detection_annotation_contact_sheet.png
.\.venv\Scripts\python.exe scripts\validate_detection_annotation_package.py --package data\detection_annotation_package --output reports\detection_annotation_package_validation.json --markdown reports\detection_annotation_package_validation.md
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_93class_smoke.yaml
.\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py --model runs\train\strict_93class_yolo12n_cls_cpu_smoke\weights\best.pt --data data\classification_strict_jpeg_93class --imgsz 224 --device cpu --output reports\classification_93class_evaluation_metrics.json
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_5e.yaml
.\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg --imgsz 224 --device cpu --output reports\strict_classification_evaluation_metrics.json
.\.venv\Scripts\python.exe scripts\analyze_classification_errors.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --data data\classification_strict_jpeg\val --imgsz 224 --device cpu --output reports\strict_classification_error_analysis.json
.\.venv\Scripts\python.exe scripts\generate_error_review_contact_sheet.py --analysis reports\strict_classification_error_analysis.json --output reports\strict_classification_review_samples.json
.\.venv\Scripts\python.exe scripts\infer_image_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --source data\classification_strict_jpeg\val\丝瓜络\Sigualuo117.jpg --imgsz 224 --device cpu --topk 5 --output reports\strict_classification_sample_prediction.json
.\.venv\Scripts\python.exe scripts\benchmark_cls.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --images data\classification_strict_jpeg\val --imgsz 224 --device cpu --warmup 3 --iterations 20 --output runs\benchmarks\strict_classification_latency_20.json
.\.venv\Scripts\python.exe scripts\export_model.py --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt --format onnx --imgsz 224 --simplify
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
```

阶段性结果：

- strict 数据集：92 类，7826 train / 1741 val，0 errors / 0 warnings。
- strict 重复/泄漏审计：状态 `needs_leakage_review`，发现 546 组 exact duplicate，其中 34 组 train/val exact duplicate、52 组跨类别 exact duplicate；需人工复核后再删除或重划。
- 泄漏人工复核包：`reports/classification_leakage_review_package.md/json` 和 `reports/figures/classification_train_val_leakage_contact_sheet.png`，覆盖全部 34 组 train/val exact duplicate，涉及 69 条文件记录，其中 18 组同时跨类别；`manual_decision` 留空等待人工填写。
- strict 候选泄漏清理集：`data/classification_strict_jpeg_leakage_clean_candidate`，92 类，7826 train / 1707 val，总计 9533 张；已移除 34 张 val 侧泄漏副本，duplicate audit 显示 train/val 泄漏组 0、跨类别重复组 34。
- 跨类别复核包：`reports/classification_cross_class_review_package.md/json` 和 `reports/figures/classification_cross_class_contact_sheet.png`，覆盖候选清理集剩余 34 / 34 组跨类别 exact duplicate，涉及 68 条文件记录，train/val 泄漏组 0；`manual_decision` 留空等待人工填写。
- 跨类别决策表：`reports/classification_cross_class_decision_table.md/json/csv`，状态 `ready_for_manual_decision`，34 / 34 组仍为 `pending`，校验错误 0；该表只作为人工填写入口，不自动修改图片或数据集。
- 跨类别清理计划校验：`reports/classification_cross_class_cleanup_plan.md/json/csv`，状态 `waiting_for_manual_decisions`，当前计划操作 0、校验错误 0；人工填完决策 CSV 后先重新生成该报告，只有状态为 `ready_for_cleanup_execution` 才进入真实清理执行。
- 跨类别清理执行入口：`scripts/apply_classification_cross_class_cleanup_plan.py`，当前真实计划未就绪时会阻断；人工决策全部通过后可把清理结果复制到新的输出数据集目录，不修改源候选集。
- 类别一致性：原始数据 93 类，strict 实验 92 类；`大腹皮` 只在 val 出现、训练样本为 0，需补样后恢复 93 类实验。
- 93 类补齐实验：`data/classification_strict_jpeg_93class`，93 类，7841 train / 1745 val，`大腹皮` 为 15 train / 4 val；1 epoch CPU 冒烟训练 Top-1 0.0665，Top-5 0.2086。
- 93 类补齐重复/泄漏审计：同样发现 34 组 train/val exact duplicate、52 组跨类别 exact duplicate，说明该风险来自原始样本集合而非补齐脚本新增。
- 93 类候选泄漏清理集：`data/classification_strict_jpeg_93class_leakage_clean_candidate`，93 类，7841 train / 1711 val，总计 9552 张；train/val 泄漏组 0、跨类别重复组 34。
- 检测标注准备包：`data/detection_annotation_package`，93 类、279 张待标注图片，`classes.txt` 和 `annotation_manifest.csv/json` 已生成；`labels/` 仍为空，不可直接训练检测模型。
- 检测标注样本总览：`reports/detection_annotation_contact_sheet.md/json` 和 `reports/figures/detection_annotation_contact_sheet.png`，用于人工 bbox 标注前复核 93 类、279 张抽样图片。
- 检测标注包校验：`reports/detection_annotation_package_validation.md`，当前 `pending_bbox_annotation`，图片 279/279，缺失标签 279，errors 0，warnings 0；人工标注完成后可加 `--require-complete` 做严格验收。
- 训练输出：`runs/train/strict_classify_yolo12n_cls_cpu_5e`。
- 独立验证：Top-1 0.1769，Top-5 0.4957，Fitness 0.3363。
- 每类误判分析：1741 张验证图、92 类，Top-1 正确 308 张，Top-5 正确 863 张；高频混淆包括 `九香虫 -> 木丁香`、`合欢皮 -> 川牛膝`、`柏子仁 -> 芥子`。
- 人工复核样例：高频混淆 18 张、低表现类别 18 张，输出 `reports/strict_classification_review_samples.md`、`reports/figures/strict_confusion_contact_sheet.png`、`reports/figures/strict_worst_class_contact_sheet.png`。
- CPU 分类 benchmark：20 张样本 mean 9.76 ms/image，约 102.51 FPS。
- 导出权重：`runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx`。
- 应用联调：后端 QA 4/4，前端 Playwright QA 6/6，分类上传 Top-k 展示通过。
- 详细报告：`reports/strict_classification_training_report.md`。
- 类别审计：`reports/class_consistency_audit.md`。
- 可复现实验 Manifest：`reports/repro_manifest.md`，包含环境版本、复现命令、跨类别复核包、跨类别决策表、跨类别清理计划校验、清理执行入口、关键产物 SHA256 和实验边界。
- 93 类补齐报告：`reports/classification_93class_training_report.md`，说明该实验只证明 93 类覆盖链路可运行，不替代 92 类 strict 5 epoch 基准。
- 提交前清单：`reports/submission_checklist.md`。

后续正式训练配置：

```powershell
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_30e.yaml
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_gpu_100e.yaml
```

## Demo 链路自检

```powershell
python scripts\create_demo_dataset.py --output data/demo_yolo --overwrite
python scripts\validate_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt
python scripts\split_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output data/demo_splits --overwrite
```

该 demo 只验证工程链路，不是中药饮片真实实验数据。

也可以直接运行：

```powershell
.\scripts\run_demo_pipeline.ps1
```
