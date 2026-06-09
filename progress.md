# YOLOv12 中药饮片识别项目进度记录

## 2026-06-07 已完成的主要工作

- 建立并维护长期目标：持续推进 YOLOv12 中药饮片识别项目，直到数据、训练、评估、报告、PPT 和工程交付物达到可提交状态。
- 审计原始真实数据，确认当前数据是分类目录，不含真实 bbox 标注。
- 清洗 strict JPEG 分类数据集：保留 92 类、9567 张可读图片，跳过 GIF 伪 JPG 和损坏图，排除缺少训练样本的 `大腹皮`。
- 完成 YOLOv12n 分类 5 epoch CPU 训练与独立验证：Top-1 0.1769，Top-5 0.4957。
- 完成 strict 分类 Top-k 推理、CPU benchmark、ONNX 导出、后端分类接口和前端分类入口联调。
- 完成 strict 验证集每类表现与误判分析，生成高频混淆和低表现类别人工复核 contact sheet。
- 完成类别一致性审计，明确原始 93 类与 strict 92 类边界。
- 完成 93 类补齐冒烟实验：`大腹皮` 15 train / 4 val，1 epoch CPU 训练 Top-1 0.0665，Top-5 0.2086。
- 生成检测 bbox 人工标注准备包，覆盖 93 类、279 张待标注图片；`labels/` 仍为空。
- 完成检测标注准备包 pending 校验：图片 279/279，缺失标签 279，errors 0，warnings 0。

## 本轮新增进展：检测标注样本 contact sheet 纳入交付链

- 核对当前工作树，确认根目录不是 Git 仓库，`rg` 在当前环境被拒绝执行，因此改用 PowerShell 原生命令核对项目状态。
- 确认已有 `reports/detection_annotation_contact_sheet.md/json` 和 `reports/figures/detection_annotation_contact_sheet.png`，但生成时间晚于旧 manifest 和 smoke check，尚未纳入正式交付链。
- 增强 `scripts/generate_repro_manifest.py`：
  - 将 `scripts/generate_detection_annotation_contact_sheet.py` 纳入关键产物哈希。
  - 将 `reports/detection_annotation_contact_sheet.md/json` 和 `reports/figures/detection_annotation_contact_sheet.png` 纳入关键产物哈希。
  - 增加 contact sheet 复现命令。
  - 增加 `detection_annotation_contact_sheet_summary` 摘要字段。
- 增强 `scripts/smoke_check.py`：
  - 新增 `check_detection_annotation_contact_sheet` 结构化校验。
  - 校验样本 279、类别 93、每类 3 张、来源 train 186 / val 93。
  - 校验 expected label 路径、package image 路径、Markdown 索引、PNG 存在、PNG 尺寸和文件大小。
  - Manifest 校验升级为 57 个关键产物、19 条复现命令。
- 重新生成 contact sheet：
  - JSON/Markdown：`reports/detection_annotation_contact_sheet.*`
  - PNG：`reports/figures/detection_annotation_contact_sheet.png`
  - 摘要：279 样本、93 类、预期标签 279、已完成标签 0、状态 `pending_bbox_annotation`
- 同步工程文档：
  - `README.md`
  - `docs/README.md`
  - `reports/test_report.md`
  - `reports/submission_checklist.md`
  - `reports/strict_classification_training_report.md`
- 同步生成脚本并重新生成：
  - `scripts/generate_test_report_docx.py`
  - `scripts/generate_overview_ppt.js`
  - `reports/test_report.docx`
  - `reports/overview_design.pptx`
  - `reports/repro_manifest.md/json`
- 重写根目录 `task_plan.md`、`findings.md`、`progress.md` 为 UTF-8 中文交接版，修复先前乱码问题。

## 本轮新增进展：分类数据 exact duplicate 与 train/val 泄漏审计

- 新增 `scripts/audit_classification_duplicates.py`，对分类数据集进行文件字节级 SHA256 exact duplicate 审计。
- 新增 `tests/test_classification_duplicate_audit.py`，覆盖 train/val 泄漏与跨类别重复场景。
- 生成 strict 审计报告：
  - `reports/strict_classification_duplicate_audit.json`
  - `reports/strict_classification_duplicate_audit.md`
- 生成 93 类补齐审计报告：
  - `reports/classification_93class_duplicate_audit.json`
  - `reports/classification_93class_duplicate_audit.md`
- 审计发现：
  - strict 92 类：重复 SHA256 组 546，train/val exact duplicate 34 组，跨类别 exact duplicate 52 组，状态 `needs_leakage_review`
  - 93 类补齐：重复 SHA256 组 546，train/val exact duplicate 34 组，跨类别 exact duplicate 52 组，状态 `needs_leakage_review`
- 处理边界：本轮未自动删图或重划，只把风险定位、纳入报告与自检；后续必须人工复核后再重建无泄漏数据集。
- 同步 `generate_repro_manifest.py`、`smoke_check.py`、README、docs、测试报告、提交清单、strict 训练报告、Word/PPT 生成脚本。
- 重新生成 `reports/test_report.docx`、`reports/overview_design.pptx`、`reports/repro_manifest.md/json`。

## 本轮新增进展：34 组 train/val 泄漏人工复核包纳入交付链

- 新增 `scripts/generate_classification_leakage_review_package.py`：
  - 从 `reports/strict_classification_duplicate_audit.json` 中抽取全部 train/val exact duplicate 组。
  - 与 `reports/classification_93class_duplicate_audit.json` 对比共享泄漏哈希。
  - 输出 JSON、Markdown 和 PNG 对照图，不删除、移动或重划任何图片。
- 新增 `tests/test_classification_leakage_review_package.py`，覆盖只抽取 train/val 泄漏、跨类别风险分级、`manual_decision` 空栏和参考审计交集统计。
- 生成泄漏人工复核包：
  - `reports/classification_leakage_review_package.json`
  - `reports/classification_leakage_review_package.md`
  - `reports/figures/classification_train_val_leakage_contact_sheet.png`
- 复核包摘要：
  - 状态：`complete_review_package`
  - 覆盖 train/val 泄漏组：34 / 34
  - 涉及文件记录：69，train 35 / val 34
  - 同类别泄漏组：16
  - 跨类别泄漏组：18
  - 与 93 类补齐审计共享泄漏哈希：34
- 视觉检查：PNG 尺寸 1112x7942，约 2.5 MB；每行可见风险说明、类别、SHA256 短码和 train/val 图片对照。
- 同步 `scripts/generate_repro_manifest.py`：
  - 纳入 `classification_leakage_review_summary`。
  - 纳入生成脚本、JSON、Markdown、PNG 的 SHA256。
  - 复现命令从 21 条增至 22 条。
- 同步 `scripts/smoke_check.py`：
  - 新增 `check_classification_leakage_review_package`。
  - 校验 34 组、69 条记录、16/18 同类/跨类泄漏、PNG 尺寸和 Markdown 关键字段。
  - 自检总数升至 115 项。
- 同步正式交付物：
  - `README.md`
  - `docs/README.md`
  - `reports/test_report.md`
  - `reports/test_report.docx`
  - `reports/overview_design.pptx`
  - `reports/submission_checklist.md`
  - `reports/strict_classification_training_report.md`
  - `reports/repro_manifest.md/json`

## 当时验证结果：泄漏复核包阶段

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe -m compileall scripts backend tests -q
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe scripts\generate_classification_leakage_review_package.py --audit reports\strict_classification_duplicate_audit.json --reference-audit reports\classification_93class_duplicate_audit.json --output reports\classification_leakage_review_package.json --figure reports\figures\classification_train_val_leakage_contact_sheet.png
.\.venv\Scripts\python.exe scripts\generate_detection_annotation_contact_sheet.py --manifest data\detection_annotation_package\annotation_manifest.json --output reports\detection_annotation_contact_sheet.json --figure reports\figures\detection_annotation_contact_sheet.png
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

验证结论：

- Python 编译：通过。
- 单元测试：6/6 通过。
- 增强工程自检：115/115 通过。
- Manifest：66 个关键产物、22 条复现命令。
- Contact sheet：279 样本、93 类、`labels_completed=0`，PNG 尺寸 1258x11055，约 13.2 MB。
- 重复/泄漏审计：strict 与 93 类补齐数据均为 `needs_leakage_review`；train/val exact duplicate 34 组，跨类别 exact duplicate 52 组。
- 泄漏人工复核包：`complete_review_package`，34/34 组 train/val 泄漏，69 条记录，PNG 尺寸 1112x7942。
- 文档关键字抽查：README、docs、测试报告、提交清单、strict 训练报告、Manifest 均包含 `classification_leakage_review_package`、`detection_annotation_contact_sheet`、`重复/泄漏审计`、`115 / 115`、`66 个`、`22 条` 等当时事实。

## 当时待办：泄漏复核包阶段

- 若有 GPU，运行 `configs/train_cls_strict_gpu_100e.yaml` 做 strict 100 epoch 正式训练。
- 若只能 CPU，运行 `configs/train_cls_strict_cpu_30e.yaml` 做 strict 30 epoch 延长训练。
- 为 `大腹皮` 补充独立训练样本并运行 93 类正式长轮次实验。
- 使用 `reports/classification_leakage_review_package.md` 与 `reports/figures/classification_train_val_leakage_contact_sheet.png` 逐组复核 34 组 train/val 泄漏，填写 `manual_decision` 后重建无泄漏数据集并重新训练/评估。
- 若最终必须交付目标检测指标，基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注，运行 `scripts\validate_detection_annotation_package.py --require-complete` 通过后重新划分、训练和评估。
- 基于 `strict_classification_review_samples.md` 与 `detection_annotation_contact_sheet.md` 补充人工复核结论、补样优先级和最终答辩材料。

## 本轮新增进展：候选泄漏清理集纳入交付链

- 新增 `scripts/prepare_leakage_clean_classification_dataset.py`：
  - 输入分类数据集和 `classification_leakage_review_package.json`。
  - 只移除复核包中列出的 val 侧 train/val exact duplicate 副本。
  - 不自动修改 train 图像、不自动裁决跨类别标签、不替代人工类别复核。
- 新增 `tests/test_prepare_leakage_clean_classification_dataset.py`，覆盖只删除 val 泄漏副本、保留 train 副本和 train-only 重复的核心行为。
- 生成 strict 候选清理集：
  - `data/classification_strict_jpeg_leakage_clean_candidate`
  - `reports/classification_leakage_clean_candidate_report.md/json`
  - `reports/classification_leakage_clean_candidate_inspection.md/json`
  - `reports/classification_leakage_clean_candidate_duplicate_audit.md/json`
  - 结果：92 类，7826 train / 1707 val，总计 9533 张；移除 34 张 val 侧泄漏副本；图片复审 0 errors / 0 warnings；train/val 泄漏组 0，跨类别重复组 34。
- 生成 93 类候选清理集：
  - `data/classification_strict_jpeg_93class_leakage_clean_candidate`
  - `reports/classification_93class_leakage_clean_candidate_report.md/json`
  - `reports/classification_93class_leakage_clean_candidate_inspection.md/json`
  - `reports/classification_93class_leakage_clean_candidate_duplicate_audit.md/json`
  - 结果：93 类，7841 train / 1711 val，总计 9552 张；移除 34 张 val 侧泄漏副本；图片复审 0 errors / 0 warnings；train/val 泄漏组 0，跨类别重复组 34。
- 同步可复现链路：
  - `scripts/generate_repro_manifest.py` 纳入候选清理脚本、报告、inspection、duplicate audit 和 6 条复现命令。
  - `scripts/smoke_check.py` 新增候选清理结构化校验，校验输出规模、移除数量、train/val 泄漏归零、跨类别重复仍为 34、报告边界说明和 Manifest 产物。
  - Manifest 升级为 79 个关键产物、28 条复现命令。
  - Smoke check 升级为 132/132 通过。
- 同步正式交付物：
  - `README.md`
  - `docs/README.md`
  - `reports/test_report.md`
  - `reports/test_report.docx`
  - `reports/overview_design.pptx`
  - `reports/submission_checklist.md`
  - `reports/strict_classification_training_report.md`
  - `reports/repro_manifest.md/json`
- 当时验证：
  - `.\.venv\Scripts\python.exe -m compileall scripts backend tests -q` 通过。
  - `.\.venv\Scripts\python.exe -m pytest tests -q`：7/7 通过。
  - `.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json`：132/132 通过。

## 当时待办：候选清理集阶段

- 基于候选清理集复核剩余 34 组跨类别 exact duplicate，记录真实类别处理决策后再做正式重训练与评估。
- 若有 GPU，运行 `configs/train_cls_strict_gpu_100e.yaml` 做 strict 100 epoch 正式训练；若只能 CPU，运行 `configs/train_cls_strict_cpu_30e.yaml` 做 strict 30 epoch 延长训练。
- 为 `大腹皮` 补充独立训练样本并运行 93 类正式长轮次实验。
- 若最终必须交付目标检测指标，基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注，运行 `scripts\validate_detection_annotation_package.py --require-complete` 通过后重新划分、训练和评估。
- 基于 `strict_classification_review_samples.md` 与 `detection_annotation_contact_sheet.md` 补充人工复核结论、补样优先级和最终答辩材料。

## 本轮新增进展：跨类别 exact duplicate 复核包纳入交付链

- 确认 `reports/classification_cross_class_review_package.md/json` 与 `reports/figures/classification_cross_class_contact_sheet.png` 已生成，但旧 manifest、smoke 和正式文档未完整约束该产物。
- 增强 `scripts/smoke_check.py`：
  - 新增并实际调用 `check_cross_class_review_package`。
  - 校验 34/34 组跨类别 exact duplicate、68 条记录、train 62 / val 6、train/val 泄漏组 0、22 个涉及类别、`manual_decision` 空栏、PNG 尺寸和 Markdown 边界说明。
  - Manifest 校验同步断言 `classification_cross_class_review_summary`、脚本/JSON/Markdown/PNG 产物和 29 条复现命令。
- 同步 `scripts/generate_repro_manifest.py` 的现有跨类别复核摘要，重新生成 `reports/repro_manifest.md/json`，结果为 83 个关键产物、29 条复现命令。
- 同步正式交付物：
  - `README.md`
  - `docs/README.md`
  - `reports/test_report.md`
  - `reports/test_report.docx`
  - `reports/overview_design.pptx`
  - `reports/submission_checklist.md`
  - `reports/strict_classification_training_report.md`
  - `reports/repro_manifest.md/json`
  - `reports/smoke_check.md/json`
- 当时验证：
  - `.\.venv\Scripts\python.exe -m compileall scripts backend tests -q` 通过。
  - `.\.venv\Scripts\python.exe -m pytest tests -q`：8/8 通过。
  - `.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json`：138/138 通过。

## 当时待办：跨类别复核包阶段

- 基于 `reports/classification_cross_class_review_package.md` 和 `reports/figures/classification_cross_class_contact_sheet.png` 逐组复核剩余 34 组跨类别 exact duplicate，填写 `manual_decision`，记录真实类别处理决策后再做正式重训练与评估。
- 若有 GPU，运行 `configs/train_cls_strict_gpu_100e.yaml` 做 strict 100 epoch 正式训练；若只能 CPU，运行 `configs/train_cls_strict_cpu_30e.yaml` 做 strict 30 epoch 延长训练。
- 为 `大腹皮` 补充独立训练样本并运行 93 类正式长轮次实验。
- 若最终必须交付目标检测指标，基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注，运行 `scripts\validate_detection_annotation_package.py --require-complete` 通过后重新划分、训练和评估。
- 基于 `strict_classification_review_samples.md` 与 `detection_annotation_contact_sheet.md` 补充人工复核结论、补样优先级和最终答辩材料。

## 本轮新增进展：跨类别标签冲突决策表纳入交付链

- 复核 `reports/classification_cross_class_decision_table.md/json/csv`，确认来源为 `classification_cross_class_review_package.json`，状态为 `ready_for_manual_decision`。
- 决策表摘要：
  - 覆盖 34 / 34 组跨类别 exact duplicate。
  - 涉及 68 条文件记录。
  - pending / decided / expert / defer = 34 / 0 / 0 / 0。
  - 校验错误 0。
  - CSV 字段覆盖 `decision_status`、`chosen_class`、`action`、`remove_relative_paths`、`move_to_class`、`reviewer`、`reviewed_at`、`decision_note`。
- 同步工程与报告：
  - `README.md`
  - `docs/README.md`
  - `reports/test_report.md`
  - `reports/test_report.docx`
  - `reports/overview_design.pptx`
  - `reports/submission_checklist.md`
  - `reports/strict_classification_training_report.md`
  - `reports/repro_manifest.md/json`
  - `reports/smoke_check.md/json`
- 增强 `scripts/generate_test_report_docx.py`、`scripts/generate_overview_ppt.js` 和 `scripts/smoke_check.py`，要求 Word/PPT/Markdown 都包含跨类别决策表口径。
- 当时验证：
  - `.\.venv\Scripts\python.exe -m compileall scripts backend tests -q` 通过。
  - `.\.venv\Scripts\python.exe -m pytest tests -q`：10/10 通过。
  - 当时 smoke check 和 Manifest 已通过；该阶段快照已被下方“pending 清理计划执行阻断纳入自检”阶段更新，最新口径以 157/157 自检、92 个关键产物和 31 条复现命令为准。

## 本轮新增进展：跨类别清理计划与执行入口已完成，等待人工 CSV

- 新增并核对清理计划生成脚本：`scripts/generate_classification_cross_class_cleanup_plan.py`。
- 新增并核对清理执行入口：`scripts/apply_classification_cross_class_cleanup_plan.py`。
- 生成清理计划产物：
  - `reports/classification_cross_class_cleanup_plan.json`
  - `reports/classification_cross_class_cleanup_plan.csv`
  - `reports/classification_cross_class_cleanup_plan.md`
- 当前清理计划摘要：
  - 状态：`waiting_for_manual_decisions`。
  - 决策来源：`reports/classification_cross_class_decision_table.json` 和 `reports/classification_cross_class_decision_table.csv`。
  - 待决策组：34 / 34。
  - 已决策组：0。
  - 校验错误：0。
  - 计划操作：0，remove 0，move 0。
- 当前阻断点：人工决策 CSV 仍为 34 条 `pending`，尚未填写真实类别、处理动作、复核人和说明。
- 执行边界：执行入口已存在，但必须等清理计划状态变为 `ready_for_cleanup_execution` 且校验错误为 0 后才能运行；真实执行也只写入新的输出目录，不直接改原候选数据集。
- 最新验证：
  - `.\.venv\Scripts\python.exe -m compileall scripts backend tests -q` 通过。
  - `.\.venv\Scripts\python.exe -m pytest tests -q`：10/10 通过。
  - `.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md`：92 个关键产物、31 条复现命令。
  - 当时 smoke check 已通过；该旧快照不再作为当前计数，最新口径以下方新增阻断验证后的 157/157 自检为准。

## 本轮新增进展：pending 清理计划执行阻断纳入自检

- 增强 `scripts/smoke_check.py`，新增 `cleanup_execution_blocked:pending_cross_class_plan` 检查。
- 检查行为：调用 `scripts/apply_classification_cross_class_cleanup_plan.py`，使用当前 `reports/classification_cross_class_cleanup_plan.json` 和临时输出目录 `data/_smoke_blocked_cleanup_output`。
- 预期结果：当前计划状态为 `waiting_for_manual_decisions`，执行入口必须返回 `cleanup_execution_blocked`，错误信息包含 `ready_for_cleanup_execution`，且不生成输出目录、JSON 执行报告或 Markdown 执行报告。
- 安全边界：临时输出目录和临时报告路径均限制在项目根目录内，检查前后都会清理，不修改候选清理数据集。
- 最新验证：
  - `.\.venv\Scripts\python.exe -m compileall scripts backend tests -q` 通过。
  - `.\.venv\Scripts\python.exe -m pytest tests -q`：16/16 通过。
  - `.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json`：157/157 通过。
  - `.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md`：92 个关键产物、31 条复现命令。

## 更新后的当前待办

- 基于 `reports/classification_cross_class_decision_table.csv` 和 `reports/figures/classification_cross_class_contact_sheet.png` 逐组复核剩余 34 组跨类别 exact duplicate，填写真实类别、处理动作、复核人和说明。
- 人工决策完成后重新生成 `reports/classification_cross_class_cleanup_plan.*`；只有状态为 `ready_for_cleanup_execution` 且校验错误为 0 时，才运行 `scripts/apply_classification_cross_class_cleanup_plan.py` 重建清理数据集，然后重新审计、重新训练并报告新指标。
- 若有 GPU，运行 `configs/train_cls_strict_gpu_100e.yaml` 做 strict 100 epoch 正式训练；若只能 CPU，运行 `configs/train_cls_strict_cpu_30e.yaml` 做 strict 30 epoch 延长训练。
- 为 `大腹皮` 补充独立训练样本并运行 93 类正式长轮次实验。
- 若最终必须交付目标检测指标，基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注，运行 `scripts\validate_detection_annotation_package.py --require-complete` 通过后重新划分、训练和评估。
