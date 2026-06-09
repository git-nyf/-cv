# YOLOv12 中药饮片识别项目执行计划

更新时间：2026-06-07

## 长期目标

在 `D:\AAA中药cv` 中，从当前完整数据分类 1 epoch 部分训练状态出发，持续推进 YOLOv12 中药饮片识别项目：清理数据质量问题，补齐/处理类别不一致，完成可复现实验训练与评估，更新报告/PPT/工程文档，并在每轮可执行范围内继续推进，直到项目交付物达到可提交状态。

## 当前权威状态

- 项目目录：`D:\AAA中药cv\yolo12_tcm_project`
- 原始数据目录：`D:\AAA中药cv\data`
- 原始数据是分类目录结构：`train/<类别>/*.jpg`、`val/<类别>/*.jpg`，未发现真实 bbox 标注源。
- strict 5 epoch 分类基准：92 类，`runs/train/strict_classify_yolo12n_cls_cpu_5e`，Top-1 0.1769，Top-5 0.4957。
- 93 类补齐冒烟实验：`data/classification_strict_jpeg_93class`，`大腹皮` 从 19 张 val-only 样本确定性重划为 15 train / 4 val；1 epoch CPU 训练 Top-1 0.0665，Top-5 0.2086。
- 重复/泄漏审计：strict 与 93 类补齐数据均发现 546 组 exact duplicate，其中 34 组 train/val exact duplicate、52 组跨类别 exact duplicate；状态为 `needs_leakage_review`。
- 泄漏人工复核包：`reports/classification_leakage_review_package.md/json` 与 `reports/figures/classification_train_val_leakage_contact_sheet.png`，覆盖全部 34 / 34 组 train/val exact duplicate，涉及 69 条记录；其中同类别泄漏 16 组、跨类别泄漏 18 组，`manual_decision` 等待人工填写。该包不自动删图或重划。
- 检测 bbox 人工标注准备包：`data/detection_annotation_package`，覆盖 93 类、279 张待标注图片；`labels/` 仍为空，当前不能训练检测模型或汇报检测指标。
- 检测标注样本总览：`reports/detection_annotation_contact_sheet.md/json` 与 `reports/figures/detection_annotation_contact_sheet.png`，覆盖 93 类、279 张样本，用于人工 bbox 标注前复核。
- 候选泄漏清理集：
  - strict：`data/classification_strict_jpeg_leakage_clean_candidate`，92 类，7826 train / 1707 val，总计 9533 张；已移除 34 张 val 侧 train/val exact duplicate，train/val 泄漏组 0，跨类别 exact duplicate 34 组。
  - 93 类：`data/classification_strict_jpeg_93class_leakage_clean_candidate`，93 类，7841 train / 1711 val，总计 9552 张；train/val 泄漏组 0，跨类别 exact duplicate 34 组。
  - 边界：候选集只移除 val 侧泄漏副本，不自动修改 train 图像或裁决跨类别标签。
- 跨类别 exact duplicate 复核包：`reports/classification_cross_class_review_package.md/json` 与 `reports/figures/classification_cross_class_contact_sheet.png`，覆盖候选清理集剩余 34 / 34 组跨类别 exact duplicate，涉及 68 条记录，train/val 泄漏组 0；`manual_decision` 等待人工填写。该包不自动删除、移动、重命名或重标图片。
- 跨类别标签冲突决策表：`reports/classification_cross_class_decision_table.md/json/csv`，状态 `ready_for_manual_decision`，34 / 34 组为 `pending`，校验错误 0；CSV 是人工填写真实类别、处理动作和复核说明的入口，不自动修改数据集。
- 跨类别清理计划与执行入口：`reports/classification_cross_class_cleanup_plan.md/json/csv` 当前状态 `waiting_for_manual_decisions`，待决策 34 / 34，计划操作 0；`scripts/generate_classification_cross_class_cleanup_plan.py` 和 `scripts/apply_classification_cross_class_cleanup_plan.py` 已存在，执行脚本会在计划未就绪时阻断，且真正执行时只写入新的输出目录。
- 可复现实验 Manifest：`reports/repro_manifest.md/json`，记录 92 个关键产物 SHA256 和 31 条复现命令。
- 增强工程自检：`reports/smoke_check.json/md`，157/157 通过；包含 `cleanup_execution_blocked:pending_cross_class_plan`，验证 pending 清理计划会阻断执行且不产生输出目录或执行报告。

## 阶段状态

| 阶段 | 状态 | 证据 |
|---|---|---|
| 工程与上下文整理 | complete | `README.md`、`docs/README.md`、根目录计划文档 |
| 原始数据审计 | complete | 原始数据 93 类、9614 张图；无真实 bbox 标注 |
| strict JPEG 数据清洗 | complete | `data/classification_strict_jpeg`，92 类、9567 张图，0 errors / 0 warnings |
| strict 可复现实验训练与评估 | complete | `runs/train/strict_classify_yolo12n_cls_cpu_5e`，Top-1 0.1769，Top-5 0.4957 |
| 推理、benchmark、ONNX、应用联调 | complete | Top-k 推理、CPU benchmark、`best.onnx`、后端 QA 4/4、前端 QA 6/6 |
| 每类误判分析和人工复核样例 | complete | `reports/strict_classification_error_analysis.*`、`strict_classification_review_samples.*` |
| 类别一致性审计 | complete | `reports/class_consistency_audit.*`，`大腹皮` 缺训练样本 |
| 93 类补齐冒烟实验 | complete | `reports/classification_93class_training_report.md` |
| 重复/泄漏审计 | complete | `reports/strict_classification_duplicate_audit.*`、`reports/classification_93class_duplicate_audit.*`，均为 `needs_leakage_review` |
| 泄漏人工复核包 | complete | `reports/classification_leakage_review_package.*`、`reports/figures/classification_train_val_leakage_contact_sheet.png`，覆盖 34/34 组 train/val 泄漏 |
| 候选泄漏清理集 | complete | `data/classification_strict_jpeg_leakage_clean_candidate`、`data/classification_strict_jpeg_93class_leakage_clean_candidate`；train/val 泄漏组 0，跨类别重复组 34 |
| 跨类别复核包 | complete | `reports/classification_cross_class_review_package.*`、`reports/figures/classification_cross_class_contact_sheet.png`，覆盖 34/34 组跨类别 exact duplicate |
| 跨类别决策表 | complete | `reports/classification_cross_class_decision_table.*`，34/34 组 pending，校验错误 0，不自动改图 |
| 跨类别清理计划与执行入口 | blocked | `reports/classification_cross_class_cleanup_plan.*` 状态 `waiting_for_manual_decisions`；执行入口 `scripts/apply_classification_cross_class_cleanup_plan.py` 已存在，但需人工 CSV 决策完成后才可执行 |
| 检测标注准备包 | complete | `data/detection_annotation_package`、`reports/detection_annotation_package_report.*` |
| 检测标注包 pending 校验 | complete | `reports/detection_annotation_package_validation.*`，图片 279/279，缺失标签 279，errors 0 |
| 检测标注样本 contact sheet | complete | `reports/detection_annotation_contact_sheet.*`、PNG 1258x11055 |
| 报告、PPT、清单和 manifest 同步 | complete | `test_report.md/docx`、`overview_design.pptx`、`submission_checklist.md`、`repro_manifest.*` |
| 后续正式提升 | pending | 需要 GPU/更长轮次、`大腹皮` 独立补样、真实 bbox 标注 |

## 最新验证命令

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe -m compileall scripts backend tests -q
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe scripts\audit_classification_duplicates.py --source data\classification_strict_jpeg --output reports\strict_classification_duplicate_audit.json --markdown reports\strict_classification_duplicate_audit.md --max-groups 80
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
.\.venv\Scripts\python.exe scripts\generate_detection_annotation_contact_sheet.py --manifest data\detection_annotation_package\annotation_manifest.json --output reports\detection_annotation_contact_sheet.json --figure reports\figures\detection_annotation_contact_sheet.png
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

当前结果：

- Python 编译：通过。
- 单元测试：10/10 通过。
- 增强工程自检：157/157 通过。
- Manifest：92 个关键产物、31 条复现命令。
- 重复/泄漏审计：strict 与 93 类补齐数据均为 `needs_leakage_review`；train/val exact duplicate 34 组，跨类别 exact duplicate 52 组。
- 泄漏人工复核包：`complete_review_package`，覆盖 34/34 组 train/val 泄漏，69 条记录；同类别 16 组，跨类别 18 组。
- 候选泄漏清理集：strict 9533 张、93 类 9552 张；两者 train/val exact duplicate 均为 0 组，跨类别 exact duplicate 均为 34 组。
- 跨类别复核包：`complete_review_package`，覆盖 34/34 组跨类别 exact duplicate，68 条记录，train/val 泄漏组 0，PNG 尺寸 874x7942。
- 跨类别决策表：`ready_for_manual_decision`，34/34 组 pending，校验错误 0，CSV/JSON/Markdown 已纳入 Manifest 与 smoke。
- 跨类别清理计划：`waiting_for_manual_decisions`，待决策 34/34，计划操作 0，清理执行入口已存在但因人工 CSV 未填写而阻断。
- Contact sheet：279 样本、93 类、`labels_completed=0`，PNG 存在且尺寸为 1258x11055。

## 下一步优先级

1. 若有 GPU，运行 `configs/train_cls_strict_gpu_100e.yaml` 做 strict 100 epoch 正式训练。
2. 若只能 CPU，运行 `configs/train_cls_strict_cpu_30e.yaml` 做延长训练。
3. 为 `大腹皮` 补充独立训练样本，运行更严格的 93 类长轮次实验。
4. 先填写 `classification_cross_class_decision_table.csv` 的 34 组人工决策；随后重新生成 `classification_cross_class_cleanup_plan.*`，只有状态变为 `ready_for_cleanup_execution` 且校验错误为 0 时，才运行清理执行入口并重建数据集。
5. 若课程最终要求目标检测，基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注；标注完成后运行 `scripts\validate_detection_annotation_package.py --require-complete`，再训练与评估检测模型。
6. 基于 `strict_classification_review_samples.md` 与 `detection_annotation_contact_sheet.md` 补充人工复核结论、补样优先级和答辩材料。
