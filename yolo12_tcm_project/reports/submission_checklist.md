# 提交前检查清单

更新时间：2026-06-07  
项目目录：`D:\AAA中药cv\yolo12_tcm_project`

## 交付物状态

| 交付物 | 路径 | 状态 | 说明 |
|---|---|---|---|
| 项目 README | `README.md` | 已更新 | 包含 strict 分类实验、类别一致性审计、93 类补齐、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、标注样本 contact sheet、标注包校验、可复现实验 Manifest、推理、benchmark、ONNX 和应用联调入口 |
| 工程说明 | `docs/README.md` | 已更新 | 说明当前数据为分类目录，检测 bbox 准备包和样本总览已生成并通过 pending 校验但真实标签仍缺失，`大腹皮` 需补独立训练样本，候选清理集剩余跨类别冲突已形成复核包、决策表、执行前校验报告和非破坏性执行入口 |
| 测试报告 Markdown | `reports/test_report.md` | 已更新 | 包含 strict 分类指标、类别一致性审计、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、标注样本 contact sheet、标注包校验、可复现实验 Manifest、误判分析、人工复核样例、接口 QA、前端 QA、benchmark |
| 测试报告 Word | `reports/test_report.docx` | 已生成 | 已校验包含 `/classify/image`、ONNX、benchmark、Top-k、类别一致性、泄漏人工复核包、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、标注包校验、可复现实验、误判分析、人工复核 |
| 概要设计 PPT | `reports/overview_design.pptx` | 已生成 | 10 页，已校验包含 strict 分类、类别一致性、泄漏人工复核包、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、可复现实验 Manifest、误判分析、人工复核与 bbox 边界说明 |
| strict 训练报告 | `reports/strict_classification_training_report.md` | 已更新 | 包含 5 epoch 训练、类别一致性审计、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、独立验证、每类误判分析、人工复核 contact sheet、推理、benchmark、ONNX、应用联调 |
| 93 类补齐训练报告 | `reports/classification_93class_training_report.md` | 已生成 | 包含 `大腹皮` 15/4 重划、93 类数据复审、1 epoch 训练和独立验证 |
| 检测标注准备包报告 | `reports/detection_annotation_package_report.md` | 已生成 | 覆盖 93 类、279 张待人工标注图片；`labels/` 仍为空，不可直接训练检测模型 |
| 检测标注包校验报告 | `reports/detection_annotation_package_validation.md` | 已生成 | 当前 `pending_bbox_annotation`，图片 279/279，缺失标签 279，errors 0，warnings 0；标注完成后用 `--require-complete` 严格验收 |
| 检测标注样本总览 | `reports/detection_annotation_contact_sheet.md` | 已生成 | 索引 93 类、279 张待标注图片；配套 PNG 为 `reports/figures/detection_annotation_contact_sheet.png` |
| 重复/泄漏审计报告 | `reports/strict_classification_duplicate_audit.md` | 已生成 | strict 数据发现 train/val 泄漏组 34、跨类别重复组 52，需人工复核 |
| 泄漏人工复核包 | `reports/classification_leakage_review_package.md` | 已生成 | 覆盖 34 / 34 组 train/val exact duplicate；配套 PNG 为 `reports/figures/classification_train_val_leakage_contact_sheet.png`，`manual_decision` 等待人工填写 |
| 跨类别复核包 | `reports/classification_cross_class_review_package.md` | 已生成 | 覆盖候选清理集剩余 34 / 34 组跨类别 exact duplicate；配套 PNG 为 `reports/figures/classification_cross_class_contact_sheet.png`，不自动删图或重标 |
| 跨类别决策表 | `reports/classification_cross_class_decision_table.md` | 已生成 | JSON/CSV/Markdown 三种格式，34 / 34 组为 `pending`、校验错误 0；用于人工填写真实类别和处理动作，不自动改动数据 |
| 跨类别清理计划校验 | `reports/classification_cross_class_cleanup_plan.md` | 已生成 | 当前 `waiting_for_manual_decisions`，计划操作 0、校验错误 0；人工填完决策 CSV 后先重新生成该报告，不自动改动数据 |
| 跨类别清理执行入口 | `scripts/apply_classification_cross_class_cleanup_plan.py` | 已生成 | 只接受 `ready_for_cleanup_execution` 且校验错误为 0 的计划；当前真实计划未就绪时会阻断，只写新输出目录 |
| 类别一致性审计 | `reports/class_consistency_audit.md` | 已生成 | 原始 93 类、strict 92 类；`大腹皮` 只在 val 出现，训练样本为 0 |
| 可复现实验 Manifest | `reports/repro_manifest.md` | 已生成 | 记录环境版本、复现命令、关键指标、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包边界、contact sheet 和关键产物 SHA256 |
| 前端截图 | `reports/figures/frontend_classify_result.png` | 已生成 | 分类上传 Top-k 结果截图 |

## 数据与模型

| 项目 | 路径 | 状态 | 说明 |
|---|---|---|---|
| strict JPEG 数据集 | `data/classification_strict_jpeg` | 已生成 | 92 类，7826 train / 1741 val，0 errors / 0 warnings |
| 类别一致性审计 | `reports/class_consistency_audit.json` | 已生成 | 原始 93 类，strict 92 类；`大腹皮` 需补训练样本 |
| strict 重复/泄漏审计 | `reports/strict_classification_duplicate_audit.json` | 已生成 | 状态 `needs_leakage_review`，train/val 泄漏组 34，跨类别重复组 52 |
| 泄漏人工复核包 | `reports/classification_leakage_review_package.json` | 已生成 | 状态 `complete_review_package`，34/34 组泄漏、69 条记录；同类别 16 组，跨类别 18 组 |
| strict 候选泄漏清理集 | `data/classification_strict_jpeg_leakage_clean_candidate` | 已生成 | 92 类，7826 train / 1707 val，总计 9533 张；train/val 泄漏组 0，跨类别重复组 34 |
| 跨类别复核包 | `reports/classification_cross_class_review_package.json` | 已生成 | 状态 `complete_review_package`，覆盖 34/34 组跨类别 exact duplicate、68 条记录；train/val 泄漏组 0 |
| 跨类别决策表 | `reports/classification_cross_class_decision_table.json` | 已生成 | 状态 `ready_for_manual_decision`，pending 34/34，decided 0，校验错误 0；CSV 填写表同步生成 |
| 跨类别清理计划校验 | `reports/classification_cross_class_cleanup_plan.json` | 已生成 | 状态 `waiting_for_manual_decisions`，pending 34/34，计划操作 0，校验错误 0；只做 dry-run 校验 |
| 93 类补齐数据集 | `data/classification_strict_jpeg_93class` | 已生成 | 93 类，7841 train / 1745 val，`大腹皮` 15 train / 4 val，0 errors / 0 warnings |
| 93 类重复/泄漏审计 | `reports/classification_93class_duplicate_audit.json` | 已生成 | 状态 `needs_leakage_review`，train/val 泄漏组 34，跨类别重复组 52 |
| 93 类候选泄漏清理集 | `data/classification_strict_jpeg_93class_leakage_clean_candidate` | 已生成 | 93 类，7841 train / 1711 val，总计 9552 张；train/val 泄漏组 0，跨类别重复组 34 |
| 93 类补齐权重 | `runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt` | 已生成 | YOLOv12n 分类，CPU 1 epoch 冒烟训练 |
| 93 类补齐指标 | `reports/classification_93class_evaluation_metrics.json` | 已生成 | Top-1 0.0665，Top-5 0.2086，Fitness 0.1375 |
| 检测标注准备包 | `data/detection_annotation_package` | 已生成 | 93 类，279 张待标注图，`classes.txt` 和 `annotation_manifest.csv/json` 已生成；`labels/` 仍为空 |
| 检测标注包校验 | `reports/detection_annotation_package_validation.json` | 已生成 | pending 校验通过，0 errors / 0 warnings；当前缺失标签 279 属于待标注状态 |
| 检测标注样本总览 | `reports/detection_annotation_contact_sheet.json` | 已生成 | 样本 279、类别 93、每类 3 张；PNG 已生成并纳入自检和 Manifest |
| 可复现实验 Manifest | `reports/repro_manifest.json` | 已生成 | 包含关键产物哈希、复现命令、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口和检测标注准备包边界 |
| strict 训练权重 | `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt` | 已生成 | YOLOv12n 分类，CPU 5 epoch |
| strict ONNX | `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx` | 已导出 | imgsz=224，输出维度 92 |
| strict 评估指标 | `reports/strict_classification_evaluation_metrics.json` | 已生成 | Top-1 0.1769，Top-5 0.4957，Fitness 0.3363 |
| strict 误判分析 | `reports/strict_classification_error_analysis.md` | 已生成 | 1741 张验证图，92 类；Top-1 正确 308 张，Top-5 正确 863 张，含高频混淆对 |
| strict 人工复核样例 | `reports/strict_classification_review_samples.md` | 已生成 | 高频混淆 18 张、低表现类别 18 张，配套两张 contact sheet |
| strict 样例推理 | `reports/strict_classification_sample_prediction.json` | 已生成 | Top-k JSON 输出可追溯 |
| strict 延迟测试 | `runs/benchmarks/strict_classification_latency_20.json` | 已生成 | 20 张样本 mean 9.76 ms/image，约 102.51 FPS |

## 可复现命令

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

正式训练建议：

```powershell
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_30e.yaml
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_gpu_100e.yaml
```

## 验证结果

| 检查 | 状态 | 命令/报告 |
|---|---|---|
| Python 编译 | 通过 | `python -m compileall scripts backend tests -q` |
| 单元测试 | 通过 | `python -m pytest tests -q`，16/16 |
| 前端构建 | 通过 | `npm run build --prefix frontend` |
| 后端 QA | 通过 | `reports/backend_qa.md`，4/4 |
| 前端 QA | 通过 | `reports/frontend_qa.md`，6/6，相关 console error 0 |
| 工程自检 | 通过 | `reports/smoke_check.md`，157/157；覆盖 strict 数据集汇总、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、pending 清理计划执行阻断验证、跨类别清理执行入口、93 类补齐实验、检测标注准备包、标注样本 contact sheet、标注包校验、类别一致性审计、可复现实验 Manifest、Top-1/Top-5 指标、误判分析、人工复核 contact sheet、ONNX 文件、benchmark、Top-k 样例、QA 汇总、Word/PPT 和报告关键字段校验 |

## 明确边界

- 当前真实数据是分类目录，不含真实 bbox 标注。
- 原始数据为 93 类，当前 strict 5 epoch 基准为 92 类；93 类补齐实验已将 `大腹皮` 15/4 重划并跑通 1 epoch，但正式 93 类基准仍建议补充独立训练样本。
- strict 与 93 类补齐数据的候选清理集已移除 34 张 val 侧 train/val exact duplicate，train/val 泄漏组为 0；剩余 34 组跨类别 exact duplicate 已生成复核包、决策表、清理计划校验报告和非破坏性执行入口，重新训练前需人工复核真实类别并记录处理决策。
- 检测标注准备包已覆盖 93 类、279 张待标注图，但 `labels/` 仍为空；它是人工标注启动材料，不是已完成检测数据集。
- 检测标注样本总览 contact sheet 已覆盖 279 张样本，仅用于标注前复核，不是检测训练输入。
- 检测标注包当前只通过 pending 状态校验；必须在 `--require-complete` 严格验收通过后才可进入检测训练。
- strict 分类结果可汇报 Top-1、Top-5、每类误判分析、人工复核样例、推理延迟、ONNX 导出和应用联调。
- 不能把分类 Top-1/Top-5 当作检测 Precision、Recall 或 mAP。
- 若最终必须汇报目标检测，需要补充真实 YOLO bbox 标注后重新训练和评估。
