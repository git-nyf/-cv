# YOLOv12 中药饮片识别项目发现记录

更新时间：2026-06-07

## 数据发现

- 原始真实数据路径：`D:\AAA中药cv\data`
- 原始数据结构：`train/<类别名>/*.jpg`、`val/<类别名>/*.jpg`
- 原始数据规模：93 类，train 7847 张，val 1767 张，总计 9614 张。
- 未发现可用于真实目标检测训练的 `.txt`、`.xml`、`.json`、`.csv` bbox 标注源。
- 图像内容审计发现 GIF 伪 JPG、损坏图、扩展名与实际内容不一致等问题；strict 数据已跳过问题图并统一可读图片格式。

## 类别一致性发现

- 审计脚本：`yolo12_tcm_project/scripts/audit_class_consistency.py`
- 审计输出：`reports/class_consistency_audit.md/json`
- 原始数据 93 类；原始 train 92 类、val 93 类。
- strict 基准数据 92 类。
- `大腹皮` 只在原始 val 出现，原始 train / val 为 0 / 19，因此未纳入 strict 5 epoch 基准。
- 当前 strict 5 epoch 基准边界是可信的 92 类分类实验；若要形成严格 93 类正式基准，仍建议补充 `大腹皮` 独立训练样本。

## strict 分类实验发现

- strict 数据路径：`data/classification_strict_jpeg`
- strict 数据规模：92 类，train 7826 张，val 1741 张，总计 9567 张。
- 数据复审：9567 张图可读，0 errors，0 warnings。
- 训练输出：`runs/train/strict_classify_yolo12n_cls_cpu_5e`
- 当前环境：Python 3.13.7，Ultralytics 8.4.60，PyTorch 2.12.0+cpu，CUDA 不可用。
- 独立验证指标：
  - Top-1 Accuracy：0.1769098192
  - Top-5 Accuracy：0.4956921339
  - Fitness：0.3363009766
- 该结果是分类指标，不是检测 Precision、Recall 或 mAP。

## 每类误判与人工复核发现

- 分析脚本：`scripts/analyze_classification_errors.py`
- 分析输出：`reports/strict_classification_error_analysis.md/json`
- 覆盖 strict 验证集 1741 张图、92 类。
- Top-1 正确 308 张；Top-5 正确 863 张。
- 高频混淆包括 `九香虫 -> 木丁香`、`合欢皮 -> 川牛膝`、`柏子仁 -> 芥子`、`荜澄茄 -> 木丁香`。
- 人工复核输出：`reports/strict_classification_review_samples.md/json` 与 `reports/figures/strict_confusion_contact_sheet.png`、`reports/figures/strict_worst_class_contact_sheet.png`。

## 93 类补齐实验发现

- 脚本：`scripts/prepare_completed_classification_dataset.py`
- 数据输出：`data/classification_strict_jpeg_93class`
- 报告输出：`reports/classification_93class_completion_report.*`、`reports/classification_93class_dataset_inspection.*`、`reports/classification_93class_training_report.md`
- 数据规模：93 类，train 7841 张，val 1745 张，总计 9586 张；0 errors，0 warnings。
- `大腹皮` 处理：19 张原始 val-only 样本按确定性顺序拆为 15 train / 4 val，策略为 `rebalance_val_only`。
- 训练输出：`runs/train/strict_93class_yolo12n_cls_cpu_smoke`
- 独立验证指标：Top-1 0.0664756447，Top-5 0.2085959911，Fitness 0.1375358179。
- 边界：该实验是 1 epoch CPU 冒烟训练，只证明 93 类覆盖链路可运行，不替代 92 类 strict 5 epoch 基准。

## 重复与泄漏审计发现

- 审计脚本：`scripts/audit_classification_duplicates.py`
- 测试：`tests/test_classification_duplicate_audit.py`
- strict 审计输出：`reports/strict_classification_duplicate_audit.md/json`
- 93 类补齐审计输出：`reports/classification_93class_duplicate_audit.md/json`
- strict 92 类审计结果：
  - 状态：`needs_leakage_review`
  - 总图片：9567
  - 唯一 SHA256：9014
  - 重复 SHA256 组：546
  - 重复图片数：1099，额外重复图：553
  - train/val 泄漏组：34
  - 跨类别重复组：52
- 93 类补齐审计结果：
  - 状态：`needs_leakage_review`
  - 总图片：9586
  - 唯一 SHA256：9033
  - 重复 SHA256 组：546
  - 重复图片数：1099，额外重复图：553
  - train/val 泄漏组：34
  - 跨类别重复组：52
- 结论：重复风险来自原始样本集合而非 93 类补齐脚本新增；当前 strict 与 93 类补齐指标都需要带数据泄漏风险边界解读。
- 处理边界：该审计只检查文件字节级 SHA256 完全重复；不包含近似重复、裁剪相似或感知哈希判断。不能自动删图，必须人工复核后删除或重划。

## 分类 train/val 泄漏人工复核包发现

- 生成脚本：`scripts/generate_classification_leakage_review_package.py`
- 测试：`tests/test_classification_leakage_review_package.py`
- 复核包输出：
  - `reports/classification_leakage_review_package.json`
  - `reports/classification_leakage_review_package.md`
  - `reports/figures/classification_train_val_leakage_contact_sheet.png`
- 复核包状态：`complete_review_package`
- 覆盖 train/val 泄漏组：34 / 34。
- 涉及文件记录：69，train 35 / val 34。
- 同类别泄漏组：16。
- 跨类别泄漏组：18。
- 涉及类别数：27。
- 与 93 类补齐审计共享泄漏哈希：34。
- Markdown 保留 `manual_decision` 空栏，用于人工确认后填写删除、移动、重划或保留决策。
- PNG 对照图尺寸：1112x7942，文件大小约 2.5 MB；每行展示一组泄漏的风险级别、SHA256 短码、类别和 train/val 图片对照。
- 边界：复核包只整理 train/val 字节级 exact duplicate 风险，不自动删除、移动或重划任何图片。
- 后续动作：人工填完 `manual_decision` 后，再重建无泄漏数据集，重新运行 duplicate audit、训练和独立验证。

## 分类候选泄漏清理集发现

- 新增脚本：`scripts/prepare_leakage_clean_classification_dataset.py`
- 新增测试：`tests/test_prepare_leakage_clean_classification_dataset.py`
- 清理策略：从分类数据集中复制全部非泄漏图片，只移除 `reports/classification_leakage_review_package.json` 中列出的 val 侧 train/val exact duplicate 副本；不自动修改 train 图像，不自动裁决跨类别标签。
- strict 候选清理输出：
  - 数据集：`data/classification_strict_jpeg_leakage_clean_candidate`
  - 报告：`reports/classification_leakage_clean_candidate_report.md/json`
  - 复审：`reports/classification_leakage_clean_candidate_inspection.md/json`
  - 重复审计：`reports/classification_leakage_clean_candidate_duplicate_audit.md/json`
  - 规模：92 类，7826 train / 1707 val，总计 9533 张；已移除 34 张 val 侧泄漏副本；图片复审 0 errors / 0 warnings。
  - 审计结果：train/val 泄漏组 0，跨类别 exact duplicate 34 组，状态仍为 `needs_leakage_review`。
- 93 类候选清理输出：
  - 数据集：`data/classification_strict_jpeg_93class_leakage_clean_candidate`
  - 报告：`reports/classification_93class_leakage_clean_candidate_report.md/json`
  - 复审：`reports/classification_93class_leakage_clean_candidate_inspection.md/json`
  - 重复审计：`reports/classification_93class_leakage_clean_candidate_duplicate_audit.md/json`
  - 规模：93 类，7841 train / 1711 val，总计 9552 张；已移除 34 张 val 侧泄漏副本；图片复审 0 errors / 0 warnings。
  - 审计结果：train/val 泄漏组 0，跨类别 exact duplicate 34 组，状态仍为 `needs_leakage_review`。
- 结论：本轮已把 train/val 字节级泄漏从候选训练/验证划分中移除；剩余风险从“验证集泄漏”收敛为“跨类别重复标签复核”，后续正式重训练前应优先人工裁决这 34 组跨类别 exact duplicate。

## 检测标注准备包发现

- 准备脚本：`scripts/prepare_detection_annotation_package.py`
- 输出目录：`data/detection_annotation_package`
- 报告输出：`reports/detection_annotation_package_report.md/json`
- 关键文件：
  - `images/`
  - `labels/README.md`
  - `classes.txt`
  - `data_template.yaml`
  - `annotation_manifest.csv`
  - `annotation_manifest.json`
  - `ANNOTATION_GUIDE.md`
- 准备包状态：`pending_bbox_annotation`
- 覆盖 93 类，待标注图片 279 张，每类 3 张，来源 train 186 / val 93。
- 预期标签 279 个，已完成标签 0 个；`labels/` 当前只包含 README，不含真实 `.txt` 标签。
- 该准备包是人工绘制真实 YOLO bbox 的启动材料，不是已完成检测数据集。

## 检测标注包校验发现

- 校验脚本：`scripts/validate_detection_annotation_package.py`
- 测试：`tests/test_detection_annotation_package_validation.py`
- 校验输出：`reports/detection_annotation_package_validation.md/json`
- 当前 pending 校验结果：
  - 状态：`pending_bbox_annotation`
  - 图片：279 / 279
  - 类别：93
  - 预期标签：279
  - 已完成标签：0
  - 缺失标签：279
  - 有效 bbox：0
  - errors / warnings：0 / 0
- 默认模式允许待标注状态；人工标注完成后必须使用 `--require-complete` 严格验收。

## 检测标注样本 contact sheet 发现

- 生成脚本：`scripts/generate_detection_annotation_contact_sheet.py`
- 输出索引：`reports/detection_annotation_contact_sheet.md/json`
- 输出图片：`reports/figures/detection_annotation_contact_sheet.png`
- 覆盖 93 类、279 张样本，每类 3 张。
- 当前标签状态：`pending_bbox_annotation`，已完成标签 0 / 279。
- PNG 尺寸：1258x11055，文件大小约 13.2 MB。
- 用途：人工 bbox 标注前快速复核类别、抽样图片和预期标签文件；不是检测训练数据，也不提供检测指标。

## 工程自检发现

- 自检脚本：`scripts/smoke_check.py`
- 最新结果：157/157 通过。
- 覆盖范围包括 strict 数据集、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别 exact duplicate 复核包、跨类别标签冲突决策表、跨类别清理计划、pending 清理计划执行阻断验证、清理执行入口、93 类补齐、检测标注准备包、检测标注样本 contact sheet、标注包校验、类别审计、可复现实验 Manifest、Top-1/Top-5、误判分析、人工复核样例、ONNX、benchmark、QA、Word/PPT 和报告关键字段。
- Manifest：`reports/repro_manifest.md/json`，92 个关键产物 SHA256，31 条复现命令。

## 分类跨类别 exact duplicate 复核包发现

- 生成脚本：`scripts/generate_classification_cross_class_review_package.py`
- 测试：`tests/test_classification_cross_class_review_package.py`
- 复核包输出：
  - `reports/classification_cross_class_review_package.json`
  - `reports/classification_cross_class_review_package.md`
  - `reports/figures/classification_cross_class_contact_sheet.png`
- 复核包状态：`complete_review_package`
- 覆盖跨类别重复组：34 / 34。
- 涉及文件记录：68，train 62 / val 6。
- train/val 泄漏组：0。
- 涉及类别数：22。
- 与 93 类候选清理集共享跨类别哈希：34。
- PNG 对照图尺寸：874x7942，文件大小约 2.4 MB。
- 边界：复核包只整理候选泄漏清理集剩余的字节级 exact duplicate 标签冲突；不自动删除、移动、重命名或重标图片。
- 后续动作：人工填写 `manual_decision`，确认每组图片真实类别后再删除、移动、重标或保留，并重建清理数据集、重新训练和评估。

## 分类跨类别标签冲突决策表发现

- 生成脚本：`scripts/generate_classification_cross_class_decision_table.py`
- 测试：`tests/test_classification_cross_class_decision_table.py`
- 决策表输出：
  - `reports/classification_cross_class_decision_table.json`
  - `reports/classification_cross_class_decision_table.csv`
  - `reports/classification_cross_class_decision_table.md`
- 决策表状态：`ready_for_manual_decision`
- 覆盖冲突组：34 / 34。
- 涉及文件记录：68。
- pending / decided / expert / defer：34 / 0 / 0 / 0。
- 校验错误：0。
- CSV 字段覆盖 `decision_status`、`chosen_class`、`action`、`remove_relative_paths`、`move_to_class`、`reviewer`、`reviewed_at` 和 `decision_note`。
- 边界：决策表只把复核包中的空 `manual_decision` 标准化为人工填写输入；不自动删除、移动、重命名、重标或复制图片。
- 交付同步：README、docs、测试报告 Markdown/Word、概要设计 PPT、提交清单、strict 训练报告、Manifest 和 smoke check 均已纳入该决策表。

## 分类跨类别清理计划与执行入口发现

- 计划生成脚本：`scripts/generate_classification_cross_class_cleanup_plan.py`
- 清理执行脚本：`scripts/apply_classification_cross_class_cleanup_plan.py`
- 清理计划输出：
  - `reports/classification_cross_class_cleanup_plan.json`
  - `reports/classification_cross_class_cleanup_plan.csv`
  - `reports/classification_cross_class_cleanup_plan.md`
- 当前计划状态：`waiting_for_manual_decisions`
- 待决策组：34 / 34。
- 已决策组：0；需专家复核组：0；延后处理组：0。
- 校验错误：0。
- 计划操作：0，remove 0，move 0。
- 当前阻断：`classification_cross_class_decision_table.csv` 仍全是 `pending`，缺少人工填写的真实类别、动作、复核人和说明。
- 边界：计划生成只把人工决策转换为可审计操作清单；执行入口已存在，但在计划未达到 `ready_for_cleanup_execution` 时应阻断，真实执行也只写入新的输出目录，不直接改原候选数据集。

## 风险边界

- 当前真实实验是分类任务，不是目标检测任务。
- 不能汇报真实检测 mAP、Precision、Recall 或 bbox 定位能力，除非补充真实 bbox 标注并重新训练评估。
- 检测标注准备包和 contact sheet 只证明人工标注启动材料已准备，不证明检测数据集已完成。
- 93 类补齐实验中的 `大腹皮` 来自原始 val-only 样本重划，正式 93 类基准仍建议补充独立训练样本。
- 当前候选清理集已移除 train/val exact duplicate，但仍有 34 组跨类别 exact duplicate；清理执行入口已准备好，当前阻断是人工决策 CSV 未填写，候选集重新训练前仍需先完成 34 组人工裁决并生成可执行清理计划。
- 若要提升准确率，需要 GPU、更长 epoch、预训练权重或迁移学习对照。
