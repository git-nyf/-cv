# Claude Code 项目接手说明

本文件是给 Claude Code 的项目级上下文。请优先按这里的事实、边界和命令接手，不要凭文件名或项目标题推断当前已经完成了目标检测训练。这个项目有一点绕：标题是 YOLOv12 中药饮片识别，但当前可信实验主体是“分类”，检测部分只完成了 bbox 人工标注准备包。

## 1. 基本定位

- 工作区根目录：`D:\AAA中药cv`
- 主工程目录：`D:\AAA中药cv\yolo12_tcm_project`
- 原始数据目录：`D:\AAA中药cv\data`
- 默认交流语言：简体中文
- 当前日期基线：2026-06-09
- 这个目录不是 git 仓库；`D:\AAA中药cv` 和 `D:\AAA中药cv\yolo12_tcm_project` 下都没有 `.git`
- 如果 `rg.exe` 被系统拒绝执行，请用 PowerShell 原生命令，例如 `Get-ChildItem`、`Select-String`

项目目标是课程交付：围绕“数据准备 -> YOLOv12 训练 -> 评估 -> 在线推理 -> 前端展示 -> 报告/PPT/可复现清单”构建中药饮片识别系统。工程、脚本、前后端、报告和可复现实验产物已经达到可提交状态。

## 2. 当前最高可信状态

最后一次完整自检已经通过：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall scripts backend tests -q
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

最终结果：

- `pytest`: 17/17 passed
- `compileall`: passed
- `smoke_check`: 161/161 passed
- `reports/repro_manifest.json`: 94 个产物、32 条复现命令
- Manifest 内嵌 smoke 摘要：`total=161, passed=161, failed=0`

GPU 100 epoch 训练已完成（2026-06-09）：

- 模型：YOLOv12n-cls, pretrained ImageNet, 100 epoch, batch 64, GPU RTX 4060
- 权重：`runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`
- Top-1: 62.95% | Top-5: 86.21% | Fitness: 0.7458
- 相比 CPU 5 epoch 旧基线（Top-1 17.69%）提升显著
- 提升方向：数据清理 → yolo12s-cls → imgsz 320/384 → 难样本增强

权威入口文件：

- `D:\AAA中药cv\yolo12_tcm_project\reports\repro_manifest.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\smoke_check.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_training_report.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_gpu_100e_evaluation_metrics.json`
- `D:\AAA中药cv\yolo12_tcm_project\reports\submission_checklist.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\overview_design.pptx`
- `D:\AAA中药cv\yolo12_tcm_project\reports\test_report.docx`
- `D:\AAA中药cv\yolo12_tcm_project\docs\claude_code_status_report.md`

## 3. 最重要的边界

当前真实数据是分类目录结构：

```text
D:\AAA中药cv\data
  train\<类别>\*.jpg
  val\<类别>\*.jpg
```

目前没有可用于真实目标检测训练的 bbox 标注源。没有可靠 `.txt`、`.xml`、`.json`、`.csv` bbox 标签。因此：

- 可以汇报分类 Top-1、Top-5、每类误判分析、推理延迟、前后端 QA、ONNX 导出。
- 不要把分类 Top-1/Top-5 说成检测 Precision、Recall、mAP。
- 不要宣称已经完成真实目标检测模型训练。
- 只有完成人工 YOLO bbox 标注并通过严格校验后，才能训练检测模型并汇报检测指标。

检测部分当前只是准备包：

- `data/detection_annotation_package`
- 覆盖 93 类、279 张待人工标注图片
- `labels/` 仍为空
- `reports/detection_annotation_package_validation.json` 状态为 `pending_bbox_annotation`
- 当前校验摘要：图片 279/279，缺失标签 279，errors 0，warnings 0

人工标注完成后再运行：

```powershell
.\.venv\Scripts\python.exe scripts\validate_detection_annotation_package.py --package data\detection_annotation_package --require-complete --output reports\detection_annotation_package_validation.json --markdown reports\detection_annotation_package_validation.md
```

## 4. 数据集与实验事实

### strict 分类基准（当前最佳）

目录：`data/classification_strict_jpeg`

摘要：

- 类别数：92
- train：7826
- val：1741
- total：9567
- verified：9567
- errors：0
- warnings：0

训练产物（GPU 100 epoch — 当前最佳）：

- `runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/best.pt`
- `runs/train/strict_classify_yolo12n_cls_gpu_100e/weights/last.pt`
- `runs/train/strict_classify_yolo12n_cls_gpu_100e/results.csv`
- `runs/train/strict_classify_yolo12n_cls_gpu_100e/results.png`
- `runs/train/strict_classify_yolo12n_cls_gpu_100e/confusion_matrix.png`
- 评估报告：`reports/strict_classification_gpu_100e_evaluation_metrics.json`

GPU 100 epoch 评估：

- Top-1：0.6295（约 62.95%）
- Top-5：0.8621（约 86.21%）
- Fitness：0.7458
- train/loss：4.42 → 0.99
- val/loss：5.47 → 1.52

历史基线（CPU 5 epoch — 已被超越）：

- Top-1：0.1769（约 17.69%）
- Top-5：0.4957（约 49.57%）
- 权重：`runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt`
- ONNX：`runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx`

### 93 类补齐实验

原始数据有 93 类，但 strict 基准只保留 92 类。缺失类是 `大腹皮`，因为原始数据中它只在 val 出现，没有 train 样本。

补齐实验目录：`data/classification_strict_jpeg_93class`

摘要：

- 类别数：93
- train：7841
- val：1745
- total：9586
- `大腹皮` 由 19 张原始 val-only 样本确定性重划为 15 train / 4 val

训练：

- `runs/train/strict_93class_yolo12n_cls_cpu_smoke`
- CPU 1 epoch 冒烟训练
- Top-1：0.06647564470767975
- Top-5：0.20859599113464355
- Fitness：0.13753581792116165

这只证明 93 类链路可运行，不替代 92 类 strict 5 epoch 基准。

## 5. 重复、泄漏和人工决策状态

项目已经做了 SHA256 exact duplicate 审计。请注意这些都是字节级完全重复，不代表视觉近似重复。

strict 和 93 类数据均发现：

- exact duplicate hash：546 组
- train/val exact duplicate：34 组
- 跨类别 exact duplicate：52 组
- 状态：`needs_leakage_review`

已生成 train/val 泄漏人工复核包：

- `reports/classification_leakage_review_package.json`
- `reports/classification_leakage_review_package.md`
- `reports/figures/classification_train_val_leakage_contact_sheet.png`

基于该复核包已经生成候选泄漏清理集，只移除了 val 侧 train/val exact duplicate 副本：

- strict 候选集：`data/classification_strict_jpeg_leakage_clean_candidate`
  - 92 类，7826 train / 1707 val，总计 9533
  - train/val 泄漏组：0
  - 跨类别 exact duplicate：34 组
- 93 类候选集：`data/classification_strict_jpeg_93class_leakage_clean_candidate`
  - 93 类，7841 train / 1711 val，总计 9552
  - train/val 泄漏组：0
  - 跨类别 exact duplicate：34 组

候选集只清理了 split 泄漏，不自动裁决跨类别标签。

### 跨类别 exact duplicate

当前剩余 34 组跨类别 exact duplicate，需要人工判断真实类别。相关产物：

- `reports/classification_cross_class_review_package.json`
- `reports/classification_cross_class_review_package.md`
- `reports/figures/classification_cross_class_contact_sheet.png`
- `reports/classification_cross_class_decision_table.json`
- `reports/classification_cross_class_decision_table.csv`
- `reports/classification_cross_class_decision_table.md`
- `reports/classification_cross_class_decision_review.html`
- `reports/classification_cross_class_cleanup_plan.json`
- `reports/classification_cross_class_cleanup_plan.csv`
- `reports/classification_cross_class_cleanup_plan.md`

当前决策表状态：

- `status=ready_for_manual_decision`
- groups：34
- records：68
- pending_decisions：34
- decided_groups：0
- validation_errors：0

当前清理计划状态：

- `status=waiting_for_manual_decisions`
- pending_decisions：34
- planned_operations：0
- validation_errors：0

绝对不要自动填这些人工决策字段。必须由懂药材/懂数据的人确认真实类别后填写 `classification_cross_class_decision_table.csv`。

辅助人工查看页面：

```text
D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_review.html
```

它只是本地静态复核页，辅助看图片和复制字段，不写回 CSV，不自动裁决。

## 6. 跨类别清理的正确流程

只有人工填完 `reports/classification_cross_class_decision_table.csv` 后，才允许重新生成清理计划：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_cleanup_plan.py --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_cleanup_plan.json --operations-csv reports\classification_cross_class_cleanup_plan.csv --markdown reports\classification_cross_class_cleanup_plan.md
```

只有当清理计划满足：

- `status=ready_for_cleanup_execution`
- `validation_errors=0`

才允许执行非破坏性清理：

```powershell
.\.venv\Scripts\python.exe scripts\apply_classification_cross_class_cleanup_plan.py --source data\classification_strict_jpeg_leakage_clean_candidate --cleanup-plan reports\classification_cross_class_cleanup_plan.json --output data\classification_strict_jpeg_cross_class_clean_candidate --report reports\classification_cross_class_cleanup_execution_report.json --markdown reports\classification_cross_class_cleanup_execution_report.md
```

执行脚本只写入新的输出目录，不应删除或覆盖源候选数据集。当前计划未就绪时，执行入口会阻断，这是有意设计。

## 7. 工程结构

主目录：`D:\AAA中药cv\yolo12_tcm_project`

- `scripts/`：数据检查、清洗、重复审计、人工复核包、训练、评估、推理、导出、自检脚本
- `configs/`：YOLOv12 分类/检测训练配置
- `backend/`：FastAPI 服务
- `frontend/`：Vue3 工作台
- `data/`：项目内生成数据集和标注准备包
- `reports/`：所有报告、manifest、复核包、PPT、docx、contact sheet
- `runs/`：训练、benchmark、日志产物
- `tests/`：单元测试

主要后端接口：

- `GET /health`
- `GET /models`
- `POST /detect/image`
- `POST /classify/image`
- `POST /detect/video`
- `POST /train/start`
- `GET /metrics`

前端默认提供分类识别入口，同时保留检测入口。分类链路是当前可信主线。

## 8. 常用命令

环境：

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

运行单测：

```powershell
.\.venv\Scripts\python.exe -m pytest
```

运行完整自检：

```powershell
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

刷新可复现 Manifest：

```powershell
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
```

strict 30 epoch CPU 延长训练配置：

```powershell
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_30e.yaml
```

strict 100 epoch GPU 正式训练配置：

```powershell
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_gpu_100e.yaml
```

## 9. 关键脚本说明

分类数据与审计：

- `scripts/prepare_strict_classification_dataset.py`：从原始分类目录生成 strict JPEG 数据集
- `scripts/inspect_classification_dataset.py`：检查分类数据集类别、图片数量、可读性
- `scripts/audit_class_consistency.py`：审计原始 93 类与 strict 92 类的一致性
- `scripts/prepare_completed_classification_dataset.py`：构建 93 类补齐数据集
- `scripts/audit_classification_duplicates.py`：SHA256 exact duplicate / train-val 泄漏 / 跨类别重复审计

泄漏与跨类别复核：

- `scripts/generate_classification_leakage_review_package.py`：生成 train/val 泄漏人工复核包
- `scripts/prepare_leakage_clean_classification_dataset.py`：移除 val 侧 train/val exact duplicate 副本，生成候选清理集
- `scripts/generate_classification_cross_class_review_package.py`：生成跨类别 exact duplicate 复核包
- `scripts/generate_classification_cross_class_decision_table.py`：生成可人工填写的决策表
- `scripts/generate_classification_cross_class_decision_review_html.py`：生成本地静态复核页
- `scripts/generate_classification_cross_class_cleanup_plan.py`：基于人工 CSV 做执行前校验
- `scripts/apply_classification_cross_class_cleanup_plan.py`：清理计划通过后的非破坏性执行入口

训练、评估、推理：

- `scripts/train_yolo12_cls.py`：YOLO 分类训练
- `scripts/evaluate_yolo12_cls.py`：分类指标评估
- `scripts/infer_image_cls.py`：分类 Top-k 推理
- `scripts/benchmark_cls.py`：分类 CPU 延迟测试
- `scripts/analyze_classification_errors.py`：误判分析
- `scripts/generate_error_review_contact_sheet.py`：误判 contact sheet
- `scripts/export_model.py`：导出 ONNX 等格式

检测标注准备：

- `scripts/prepare_detection_annotation_package.py`：抽样生成 bbox 人工标注准备包
- `scripts/generate_detection_annotation_contact_sheet.py`：生成标注样本总览图
- `scripts/validate_detection_annotation_package.py`：校验标注包；当前 pending，人工标注后加 `--require-complete`

交付自检：

- `scripts/generate_repro_manifest.py`：记录环境、命令、指标、产物 SHA256
- `scripts/smoke_check.py`：最终工程自检，当前 161/161 通过

## 10. 不要做的事

- 不要自动填写跨类别决策 CSV。
- 不要自动删除、移动、重命名、重标或覆盖任何源图片。
- 不要把 `data/detection_annotation_package/labels/` 为空的准备包拿去训练检测模型。
- 不要报告检测 mAP、Precision、Recall，除非真实 bbox 标注完成并训练/评估了检测模型。
- 不要把 93 类 1 epoch 冒烟结果当作正式模型效果。
- 不要把候选泄漏清理集当作最终人工确认后的干净数据集；它仍有 34 组跨类别 exact duplicate 待人工决策。
- 不要在没有重新跑 `smoke_check.py` 的情况下声称交付状态仍然完全一致。

## 11. 后续优先级

1. 如果用户要继续提升分类效果：优先运行 GPU 100 epoch 或 CPU 30 epoch strict 分类训练，然后重新评估、导出、刷新报告和 Manifest。
2. 如果用户要清理数据质量：先人工填写 `classification_cross_class_decision_table.csv` 的 34 组跨类别决策，再生成 cleanup plan，校验通过后才执行非破坏性清理。
3. 如果用户要做真实目标检测：基于 `data/detection_annotation_package` 完成人工 YOLO bbox 标注，通过 `--require-complete` 校验后，再训练检测模型。
4. 如果用户要答辩/提交：优先使用 `reports/strict_classification_training_report.md`、`reports/test_report.docx`、`reports/overview_design.pptx`、`reports/submission_checklist.md` 和 `reports/repro_manifest.md`。

## 12. 一句话接手判断

这个项目现在是一个完整可提交的“YOLOv12 中药饮片分类识别工程”，并带有检测标注准备能力；分类实验、前后端、报告、PPT、复现清单和自检已经闭环。真正还需要人类判断的是 34 组跨类别 exact duplicate 的真实类别，以及如果课程要求检测指标，则必须补真实 bbox 标注。
