# strict 数据集分类训练报告

更新时间：2026-06-07  
项目目录：`D:\AAA中药cv\yolo12_tcm_project`

## 结论

已基于严格清洗后的 `classification_strict_jpeg` 数据集完成 YOLOv12n 分类任务 5 epoch CPU 训练，并完成独立验证。该轮实验比上一轮 `classification_clean` 1 epoch 冒烟训练更接近可复现实验：数据格式统一为 JPEG，GIF 伪 JPG 和损坏图片已剔除，验证集 0 errors / 0 warnings。

当前结果可作为“真实分类数据链路已跑通并产生阶段性指标”的交付记录；但它仍不是目标检测实验，因为原始数据没有真实 bbox 标注，不能据此汇报检测 mAP 或定位能力。

## 数据集

- 来源：`D:\AAA中药cv\data`
- strict 输出：`D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg`
- 类别数：92
- 训练图像：7826
- 验证图像：1741
- 总图像：9567
- 跳过问题图：28
- 转换为 JPEG：122
- 直接复制 JPEG：9445
- 被排除类别：`大腹皮`，原因是只有验证样本、没有训练样本

类别一致性审计：

- `reports/class_consistency_audit.md`
- `reports/class_consistency_audit.json`
- 原始数据 93 类，train 92 类，val 93 类；strict 实验 92 类
- `大腹皮` 只在 val 出现，原始 train 为 0、原始 val 为 19，未纳入 strict 训练
- 状态：`needs_class_completion`，需补充 `大腹皮` 训练样本后重建 strict 数据集，才能恢复完整 93 类实验

93 类补齐实验：

- `reports/classification_93class_training_report.md`
- `data/classification_strict_jpeg_93class` 输出 93 类，7841 train / 1745 val，9586 张图像复审 0 errors / 0 warnings
- `大腹皮` 由 19 张原始 val-only 样本确定性拆为 15 train / 4 val
- 1 epoch CPU 冒烟训练输出 `runs/train/strict_93class_yolo12n_cls_cpu_smoke`，Top-1 0.0665，Top-5 0.2086
- 该实验用于证明 93 类覆盖链路可运行，不替代当前 92 类 strict 5 epoch 基准

可复现实验 Manifest：

- `reports/repro_manifest.md`
- `reports/repro_manifest.json`
- 覆盖环境版本、训练配置、Top-1/Top-5 指标、类别一致性摘要、重复/泄漏审计、泄漏人工复核包、检测标注准备包、标注样本 contact sheet、CPU benchmark、复现命令和关键产物 SHA256
- 用途：提交时追溯当前 strict 分类阶段结果由哪些命令、配置、权重和报告产物生成

检测 bbox 标注准备包：

- `reports/detection_annotation_package_report.md`
- `reports/detection_annotation_package_report.json`
- `reports/detection_annotation_package_validation.md`
- `reports/detection_annotation_package_validation.json`
- `reports/detection_annotation_contact_sheet.md`
- `reports/detection_annotation_contact_sheet.json`
- `reports/figures/detection_annotation_contact_sheet.png`
- `data/detection_annotation_package`
- 来源为 `data/classification_strict_jpeg_93class`
- 覆盖 93 类，每类抽样 3 张，合计 279 张待人工标注图片
- `classes.txt`、`data_template.yaml`、`annotation_manifest.csv/json` 和 `ANNOTATION_GUIDE.md` 已生成
- 标注样本 contact sheet 覆盖 93 类、279 张图片，用于人工 bbox 标注前快速复核类别、抽样图和预期标签文件
- `labels/` 仍为空，已完成标签文件为 0；该准备包不可直接训练检测模型，也不能据此汇报检测 mAP、Precision 或 Recall
- pending 校验结果：图片 279/279，缺失标签 279，errors 0，warnings 0；人工标注完成后需运行 `scripts\validate_detection_annotation_package.py --require-complete` 严格验收

重复与泄漏审计：

- `reports/strict_classification_duplicate_audit.md`
- `reports/strict_classification_duplicate_audit.json`
- `reports/classification_leakage_review_package.md`
- `reports/classification_leakage_review_package.json`
- `reports/figures/classification_train_val_leakage_contact_sheet.png`
- `reports/classification_cross_class_review_package.md`
- `reports/classification_cross_class_review_package.json`
- `reports/figures/classification_cross_class_contact_sheet.png`
- `reports/classification_cross_class_decision_table.md`
- `reports/classification_cross_class_decision_table.json`
- `reports/classification_cross_class_decision_table.csv`
- `reports/classification_cross_class_cleanup_plan.md`
- `reports/classification_cross_class_cleanup_plan.json`
- `reports/classification_cross_class_cleanup_plan.csv`
- `scripts/apply_classification_cross_class_cleanup_plan.py`
- `reports/classification_93class_duplicate_audit.md`
- `reports/classification_93class_duplicate_audit.json`
- strict 92 类数据：状态 `needs_leakage_review`，重复 SHA256 组 546，train/val 泄漏组 34，跨类别重复组 52
- 93 类补齐数据：状态 `needs_leakage_review`，重复 SHA256 组 546，train/val 泄漏组 34，跨类别重复组 52
- 泄漏人工复核包：状态 `complete_review_package`，覆盖 34 / 34 组 train/val 泄漏，涉及 69 条文件记录；同类别泄漏 16 组、跨类别泄漏 18 组，`manual_decision` 等待人工填写
- strict 候选泄漏清理集：`data/classification_strict_jpeg_leakage_clean_candidate`，92 类，7826 train / 1707 val，总计 9533 张；移除 34 张 val 侧泄漏副本后，train/val 泄漏组为 0，跨类别重复组仍为 34
- 93 类候选泄漏清理集：`data/classification_strict_jpeg_93class_leakage_clean_candidate`，93 类，7841 train / 1711 val，总计 9552 张；train/val 泄漏组为 0，跨类别重复组仍为 34
- 跨类别复核包：`classification_cross_class_review_package` 覆盖候选清理集剩余 34 / 34 组跨类别 exact duplicate，涉及 68 条文件记录，train/val 泄漏组 0，配套 `classification_cross_class_contact_sheet.png` 用于逐组确认真实类别
- 跨类别决策表：`classification_cross_class_decision_table.md/json/csv` 将 34 组标签冲突整理为可填写输入，状态 `ready_for_manual_decision`，34 / 34 组为 `pending`，校验错误 0；CSV 用于填写 `decision_status`、真实类别、处理动作、复核人和说明
- 跨类别清理计划校验：`classification_cross_class_cleanup_plan.md/json/csv` 将人工决策 CSV 转换为执行前 dry-run 报告，当前状态 `waiting_for_manual_decisions`，计划操作 0、校验错误 0；只有人工填完 CSV 且状态变为 `ready_for_cleanup_execution` 后，才可进入真实清理执行
- 跨类别清理执行入口：`apply_classification_cross_class_cleanup_plan.py` 只接受校验通过的计划；当前真实计划未就绪时会阻断，真正执行也只复制到新的输出数据集目录，不删除或覆盖源候选集
- 边界：该审计只检查文件字节级 SHA256 完全重复；不包含近似重复、裁剪相似或感知哈希判断
- 处理建议：候选集只移除 val 侧泄漏副本，不自动修改 train 图像或裁决跨类别标签；重新训练前应先填写跨类别决策表或复核包的 `manual_decision`，重新生成清理计划校验报告，再用执行脚本写入新的候选输出目录并复审

复审结果：

- `reports/strict_classification_dataset_inspection.md`
- `reports/strict_classification_dataset_inspection.json`
- 9567 张图片均可读，0 errors，0 warnings

## 训练环境

- Python：3.13.7
- Ultralytics：8.4.60
- PyTorch：2.12.0+cpu
- CUDA：不可用
- 设备：CPU

## 训练配置

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\train_yolo12_cls.py --config configs\train_cls_strict_cpu_5e.yaml
```

关键参数：

- 模型：`yolo12n-cls.yaml`
- 数据：`data/classification_strict_jpeg`
- epoch：5
- imgsz：224
- batch：16
- optimizer：AdamW
- lr0：0.001
- seed：42
- pretrained：false
- workers：0

说明：本机没有可用的 `yolo12n-cls.pt` 预训练分类权重，因此本轮仍使用 YOLOv12n 分类结构从头训练。该限制会显著压低短轮次准确率。

## 训练结果

训练输出目录：

`D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_cpu_5e`

权重文件：

- `D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt`
- `D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\last.pt`

训练日志：

| epoch | train/loss | val/loss | Top-1 | Top-5 | 累计用时 |
|---:|---:|---:|---:|---:|---:|
| 1 | 4.39647 | 4.23136 | 0.05859 | 0.19989 | 189.554 s |
| 2 | 4.11596 | 3.89991 | 0.06893 | 0.26479 | 355.940 s |
| 3 | 3.93608 | 3.58389 | 0.11143 | 0.35210 | 519.144 s |
| 4 | 3.74722 | 3.39533 | 0.14819 | 0.42389 | 676.917 s |
| 5 | 3.60868 | 3.21768 | 0.17634 | 0.49569 | 875.946 s |

## 独立验证

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\evaluate_yolo12_cls.py `
  --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt `
  --data data\classification_strict_jpeg `
  --imgsz 224 `
  --device cpu `
  --output reports\strict_classification_evaluation_metrics.json
```

| 指标 | 数值 |
|---|---:|
| Top-1 Accuracy | 0.1769098192 |
| Top-5 Accuracy | 0.4956921339 |
| Fitness | 0.3363009766 |
| 推理耗时 | 约 3.3 ms/image，CPU |

验证输出：

- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_evaluation_metrics.json`
- `D:\AAA中药cv\yolo12_tcm_project\runs\classify\val-2`

## 推理、导出与应用联调

分类单图推理：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\infer_image_cls.py `
  --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt `
  --source data\classification_strict_jpeg\val\丝瓜络\Sigualuo117.jpg `
  --imgsz 224 `
  --device cpu `
  --topk 5 `
  --output reports\strict_classification_sample_prediction.json
```

样例输出中，验证图真实目录为 `丝瓜络`，模型 Top-1 预测为 `干姜`，置信度 0.0926。该样例用于证明分类推理接口与 JSON 输出可运行；单样例预测错误也符合当前 5 epoch 短训准确率仍偏低的事实。

分类 CPU benchmark：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\benchmark_cls.py `
  --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt `
  --images data\classification_strict_jpeg\val `
  --imgsz 224 `
  --device cpu `
  --warmup 3 `
  --iterations 20 `
  --output runs\benchmarks\strict_classification_latency_20.json
```

| 指标 | 数值 |
|---|---:|
| 样本数 | 20 |
| 平均延迟 | 9.75545 ms/image |
| 中位延迟 | 9.24755 ms/image |
| FPS 估计 | 102.5068 |
| 样本 Top-1 | 0.0000 |
| 样本 Top-5 | 0.1500 |

ONNX 导出：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\export_model.py `
  --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt `
  --format onnx `
  --imgsz 224 `
  --simplify
```

已生成：

- `D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.onnx`

应用联调：

- 后端新增并验证 `POST /classify/image`，返回 Top-k 分类结果；`scripts/backend_qa.py` 为 4/4 通过。
- 前端默认进入“分类识别”，保留“目标检测”页签；`scripts/frontend_qa.py` 为 6/6 通过，相关 console error 为 0。
- 前端分类结果截图：`D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_classify_result.png`
- 提交前清单：`D:\AAA中药cv\yolo12_tcm_project\reports\submission_checklist.md`

## 每类表现与误判分析

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\analyze_classification_errors.py `
  --model runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt `
  --data data\classification_strict_jpeg\val `
  --imgsz 224 `
  --device cpu `
  --output reports\strict_classification_error_analysis.json
```

分析输出：

- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_error_analysis.json`
- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_error_analysis.md`

| 项目 | 数值 |
|---|---:|
| 验证图像 | 1741 |
| 类别数 | 92 |
| Top-1 正确 | 308 |
| Top-5 正确 | 863 |
| Top-1 Accuracy | 0.1769098219 |
| Top-5 Accuracy | 0.4956921310 |

Top-1 最高类别包括 `枸杞子`、`莲子心`，均为 1.0000；`鸡冠花` 为 0.9474，`白矾` 为 0.8421。Top-1 最低类别包括 `地龙`、`安息香`、`瓦楞子`、`北沙参`，当前 5 epoch 权重下为 0.0000。

高频混淆对包括：

| 真实类别 | 预测类别 | 次数 |
|---|---|---:|
| 九香虫 | 木丁香 | 12 |
| 合欢皮 | 川牛膝 | 12 |
| 柏子仁 | 芥子 | 12 |
| 荜澄茄 | 木丁香 | 12 |
| 山茱萸 | 枸杞子 | 11 |

这些误判说明当前短训模型已对少数外观特征鲜明类别形成有效区分，但大量外观相近类别仍被吸收到少数高频预测类别中。后续应优先对 Top-1 为 0 或高频混淆类别做人工复核、补样、增强和更长轮次训练。

## 人工复核样例与 contact sheet

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\generate_error_review_contact_sheet.py `
  --analysis reports\strict_classification_error_analysis.json `
  --output reports\strict_classification_review_samples.json
```

已生成：

- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_review_samples.json`
- `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_review_samples.md`
- `D:\AAA中药cv\yolo12_tcm_project\reports\figures\strict_confusion_contact_sheet.png`
- `D:\AAA中药cv\yolo12_tcm_project\reports\figures\strict_worst_class_contact_sheet.png`

| 复核材料 | 数量 | 用途 |
|---|---:|---|
| 高频混淆样例 | 18 | 检查 `九香虫 -> 木丁香`、`合欢皮 -> 川牛膝` 等高频混淆是否存在目录混入或外观高度相似 |
| 低表现类别样例 | 18 | 检查 `地龙`、`安息香`、`瓦楞子`、`北沙参` 等低表现类是否需要补样或复核验证样本来源 |

该 contact sheet 是数据质量复核材料，不代表新模型性能。正式提交时可用它说明下一轮数据清洗、补样和相似类别人工复核的依据。

## 指标解释

Top-1 约 17.69%，Top-5 约 49.57%。相比 1 epoch 冒烟训练的 Top-1 约 4.77%、Top-5 约 19.59%，该轮训练有明显提升，说明清洗后的分类数据和训练链路有效。

该结果仍不能作为最终模型性能，主要原因是：

- 92 类分类任务类别多，部分中药饮片外观相似。
- 只训练 5 epoch，训练预算仍偏小。
- CPU-only 环境限制了训练轮次和调参空间。
- 使用 `yolo12n-cls.yaml` 从头训练，没有加载分类预训练权重。
- `大腹皮` 在 92 类 strict 基准中因缺少训练样本被排除；当前已有 93 类补齐冒烟实验，但正式 93 类基准仍建议补充独立训练样本。
- exact duplicate 审计发现 34 组 train/val 泄漏和 52 组跨类别重复；已生成 `classification_leakage_review_package` 覆盖全部 34 组泄漏，并生成 `classification_cross_class_review_package` 覆盖候选清理集剩余 34 组跨类别标签冲突，当前分类指标需带数据泄漏与标签冲突风险说明，清洗前不应视作最终无泄漏基准。
- 检测 bbox 标注准备包已经生成，但 `labels/` 仍为空，真实检测指标仍需人工标注完成后重新训练和评估。
- 检测标注包当前仅通过 pending 状态校验，不能替代 `--require-complete` 严格验收。

## 后续建议

- 在可用 NVIDIA GPU 环境中使用 `configs/train_cls_strict_gpu_100e.yaml` 进行 100 epoch strict 正式训练。
- 若只能使用 CPU，可使用 `configs/train_cls_strict_cpu_30e.yaml` 做 30 epoch strict 延长训练。
- 优先获取 YOLOv12 分类预训练权重，或使用兼容分类预训练模型做迁移学习对照。
- 为 `大腹皮` 补充独立训练样本，运行完整 93 类长轮次分类实验。
- 使用 `classification_leakage_review_package.md`、`classification_train_val_leakage_contact_sheet.png`、`classification_cross_class_review_package.md` 和 `classification_cross_class_contact_sheet.png` 逐组复核 train/val 泄漏与跨类别标签冲突，确认后重建清理数据集并重新评估。
- 基于 `data/detection_annotation_package` 完成人工 bbox 标注，并保持 `classes.txt` 的 93 类顺序不变。
- 标注完成后运行 `scripts\validate_detection_annotation_package.py --require-complete`，通过后再进行检测数据划分、训练和评估。
- 基于 `strict_classification_review_samples.md`、`detection_annotation_contact_sheet.md` 和 contact sheet 补充相似类别人工复核结论、标注样本复核结论和补样优先级。
- 若最终汇报必须是“检测”，需要补充真实 bbox 标注；当前分类实验不能转换为真实检测 mAP。
