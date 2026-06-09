# 基于 YOLOv12 的中草药饮片智能识别与分类系统测试报告

## 1. 测试结论

截至当前交付，项目已完成从工程环境、数据处理、YOLOv12 训练/调参/评估/推理、FastAPI 后端、Vue3 前端、模型导出、接口验证到概要设计 PPT 的完整工程闭环。当前本机 `.venv` 已安装并验证 `torch 2.12.0+cpu`、`ultralytics 8.4.60`、`fastapi 0.136.3`、`playwright 1.60.0` 等核心依赖，增强工程自检已扩展到覆盖 93 类补齐实验、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包和标注样本 contact sheet，单元测试 16/16 项通过。

已使用合成 demo YOLO 数据集完成最小训练闭环：数据生成、数据校验、train/val/test 划分、YOLOv12n CPU 1 epoch 训练、测试集评估、图片推理、ONNX 导出、后端 API 调用和前端 Playwright 渲染 QA 均已跑通。该 demo 数据只用于证明项目流程和代码可运行，不代表真实中药饮片识别效果。

用户补充的真实中药饮片数据当前是分类目录，不含真实 bbox 标注。项目已完成 strict JPEG 分类数据集清洗与 YOLOv12n 分类 5 epoch CPU 训练，独立验证 Top-1 为 0.1769、Top-5 为 0.4957，并补充了类别一致性审计、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、可复现实验 Manifest、每类表现、最高/最低类别、高频混淆对和人工复核 contact sheet。重复审计发现 strict 与 93 类补齐数据均存在 34 组 train/val exact duplicate 和 52 组跨类别 exact duplicate；本轮已生成覆盖全部 34 组的泄漏人工复核包，并构建 strict 与 93 类两个候选泄漏清理集，均只移除 val 侧泄漏副本，train/val 泄漏归零；剩余 34 组跨类别 exact duplicate 已单独生成复核包、对照图、可填写决策表、执行前 dry-run 清理计划报告和非破坏性执行脚本，仍需人工确认真实类别。类别审计显示原始数据 93 类、strict 基准实验 92 类；本轮新增 93 类补齐实验，将 `大腹皮` 19 张原始 val-only 样本确定性重划为 15 train / 4 val，并完成 1 epoch CPU 冒烟训练，Top-1 为 0.0665、Top-5 为 0.2086。同时已生成检测 bbox 标注准备包、279 张样本总览 contact sheet 并完成 pending 状态校验，覆盖 93 类、279 张待标注图片，但 `labels/` 仍为空。该结果可作为真实分类数据阶段性指标；检测 Precision、Recall、mAP、bbox 定位能力仍需在补充真实检测标注后实测。报告不复用参考文献指标，也不将 demo 合成数据指标当作项目真实性能。

## 2. 测试环境

| 项目 | 当前状态 |
|---|---|
| 操作系统 | Windows，本地工作区 |
| 项目路径 | `D:\AAA中药cv\yolo12_tcm_project` |
| Python 环境 | `.venv\Scripts\python.exe` |
| Python 版本 | 3.13.7 |
| PyTorch | `torch 2.12.0+cpu`，当前为 CPU-only |
| Ultralytics | `8.4.60` |
| 后端框架 | `fastapi 0.136.3` + `uvicorn` |
| 前端框架 | Vue3 + Vite |
| GPU | 当前本机未检测到 CUDA；正式训练建议使用 NVIDIA GPU |
| 真实数据集 | 已接入分类数据 `data\classification_strict_jpeg`；已准备 `data\detection_annotation_package`；真实检测 bbox 标签仍缺失 |

## 3. 功能测试矩阵

| 模块 | 测试项 | 状态 | 说明 |
|---|---|---|---|
| 环境搭建 | 虚拟环境、依赖安装、脚本可导入 | 通过 | `scripts/smoke_check.py` |
| 数据生成 | 生成 demo YOLO 数据 | 通过 | `scripts/create_demo_dataset.py` |
| 数据校验 | 图片损坏、标签缺失、bbox 越界、重复图片 | 通过 | demo 数据 0 errors / 0 warnings |
| 数据划分 | 7:2:1 train/val/test | 通过 | demo 数据划分为 13 / 4 / 1 |
| 真实分类数据清洗 | 统一 JPEG、跳过 GIF/损坏图、排除无训练样本类别 | 通过 | 92 类，7826 train / 1741 val，0 errors / 0 warnings |
| 类别一致性审计 | 原始 93 类与 strict 92 类差异、缺训练样本类别、跳过图分布 | 通过 | `reports/class_consistency_audit.md`，`大腹皮` 只在 val 出现，训练样本为 0 |
| 重复/泄漏审计 | exact duplicate、train/val 泄漏、跨类别重复 | 待人工复核 | strict 与 93 类补齐数据均发现 train/val 泄漏组 34、跨类别重复组 52 |
| 泄漏人工复核包 | 34 组 train/val exact duplicate 的 JSON、Markdown 和对照图 | 通过 | `reports/classification_leakage_review_package.md/json`，18 组同时跨类别 |
| 候选泄漏清理集 | 基于复核包移除 val 侧泄漏副本并复审 | 通过 | strict 9533 张、93 类 9552 张，train/val 泄漏组均为 0，跨类别重复组均为 34 |
| 跨类别复核包 | 34 组跨类别 exact duplicate 的 JSON、Markdown 和对照图 | 待人工复核 | `reports/classification_cross_class_review_package.md/json`，`manual_decision` 等待填写 |
| 跨类别决策表 | 34 组跨类别标签冲突的 JSON/CSV/Markdown 填写表 | 待人工填写 | `reports/classification_cross_class_decision_table.md/json/csv`，34/34 组为 `pending`，校验错误 0 |
| 跨类别清理计划校验 | 人工决策 CSV 的执行前 dry-run 报告和操作预览 CSV | 待人工决策 | `reports/classification_cross_class_cleanup_plan.md/json/csv`，当前 `waiting_for_manual_decisions`，计划操作 0 |
| 跨类别清理执行入口 | 校验通过后的非破坏性执行脚本 | 待人工决策 | `scripts/apply_classification_cross_class_cleanup_plan.py`，当前计划未就绪时会阻断，只写新输出目录 |
| 93 类补齐实验 | `大腹皮` val-only 样本确定性重划、93 类数据复审、1 epoch 训练和独立验证 | 通过 | `reports/classification_93class_training_report.md`，Top-1 0.0665，Top-5 0.2086 |
| 检测标注准备包 | 93 类抽样、标注指南、`classes.txt`、manifest、空 `labels/` 目录 | 通过 | `reports/detection_annotation_package_report.md`，279 张待人工标注图片，`labels/` 仍为空 |
| 检测标注包校验 | 待标注包结构、manifest、图片哈希、缺失标签统计、YOLO 标签严格验收入口 | 通过 | `reports/detection_annotation_package_validation.md`，当前 `pending_bbox_annotation`，缺失标签 279，errors 0 |
| 检测标注样本总览 | 每类 3 张待标注样本索引与 contact sheet PNG | 通过 | `reports/detection_annotation_contact_sheet.md/json`，样本 279、类别 93 |
| 可复现实验 Manifest | 环境版本、复现命令、关键指标、实验边界和产物 SHA256 | 通过 | `reports/repro_manifest.md/json`，包含泄漏复核包、跨类别复核包、检测标注准备包和 contact sheet 关键产物 |
| 真实分类训练 | YOLOv12n 分类 CPU 5 epoch | 通过 | `runs/train/strict_classify_yolo12n_cls_cpu_5e` |
| 真实分类误判分析 | 每类 Top-1/Top-5、高频混淆对、典型误判样例 | 通过 | `reports/strict_classification_error_analysis.md` |
| 真实分类人工复核 | 高频混淆和低表现类别 contact sheet | 通过 | `reports/strict_classification_review_samples.md`、`reports/figures/strict_confusion_contact_sheet.png`、`reports/figures/strict_worst_class_contact_sheet.png` |
| 真实分类推理 | strict 权重 Top-k 单图推理 | 通过 | `scripts/infer_image_cls.py`，输出 `reports/strict_classification_sample_prediction.json` |
| 真实分类 benchmark | strict 权重 CPU 延迟测试 | 通过 | 20 张样本 mean 9.76 ms/image，约 102.51 FPS |
| 基线训练 | YOLOv12n CPU 1 epoch | 通过 | `runs/train/demo_yolo12n_smoke` |
| 参数调优 | 模型规模、imgsz、batch、lr 配置 | 通过 | `scripts/tune_yolo12.py` 支持 dry-run/正式运行 |
| 模型评估 | Precision、Recall、mAP | 通过 demo 流程 | demo 指标为 0，仅说明合成数据短训未形成可用精度 |
| 图片推理 | 保存结果图和 JSON | 通过 | `scripts/infer_image.py`、`scripts/infer_image_cls.py` |
| 后端接口 | health、models、detect/image、classify/image | 通过 | 后端 QA 4/4 |
| 前端页面 | 分类上传、目标检测页签、摄像头页签、训练页签、桌面/移动端渲染 | 通过 | 前端 QA 6/6，相关 console error 0 |
| 模型导出 | ONNX | 通过 | strict 分类 `best.onnx` 已生成 |
| 测试报告 | Markdown + DOCX | 通过 | `reports/test_report.md`、`reports/test_report.docx` |
| 概要设计 PPT | 10 页概要设计汇报 | 通过 | `reports/overview_design.pptx` |
| 提交前清单 | 交付物、复现命令、验证结果和边界说明 | 通过 | `reports/submission_checklist.md` |

## 4. Demo 数据链路验证

该验证使用 `scripts/create_demo_dataset.py` 生成几何图形合成数据，仅用于工程链路自检，不代表中药饮片真实实验。

| 项目 | 结果 |
|---|---:|
| 图片数 | 18 |
| 类别数 | 3 |
| 数据校验 errors | 0 |
| 数据校验 warnings | 0 |
| train/val/test | 13 / 4 / 1 |

报告文件：`reports/demo_dataset_validation.md`、`reports/demo_dataset_validation.json`。

## 5. Demo 训练、评估与导出

| 项目 | 结果 |
|---|---|
| 模型 | YOLOv12n |
| 训练设备 | CPU |
| 输入尺寸 | 320 |
| batch | 2 |
| epoch | 1 |
| 训练输出 | `runs/train/demo_yolo12n_smoke` |
| 权重 | `best.pt`、`last.pt` |
| ONNX | `runs/train/demo_yolo12n_smoke/weights/best.onnx` |

Demo 测试集评估结果如下。由于 demo 数据为合成几何图形，且只进行 CPU 1 epoch 短训，指标为 0 只说明最小训练流程未产生可泛化检测能力，不能作为真实中药饮片项目性能。

| 指标 | Demo 结果 | 备注 |
|---|---:|---|
| Precision | 0.0 | 工程验证，不代表真实数据 |
| Recall | 0.0 | 工程验证，不代表真实数据 |
| mAP@50 | 0.0 | 工程验证，不代表真实数据 |
| mAP@50-95 | 0.0 | 工程验证，不代表真实数据 |
| fitness | 0.0 | 工程验证，不代表真实数据 |

## 6. 真实分类数据实验

原始 `D:\AAA中药cv\data` 是 `train/<类别名>/*.jpg`、`val/<类别名>/*.jpg` 形式的分类数据集，未发现 `.txt`、`.xml`、`.json`、`.csv` 等真实 bbox 标注源。因此本阶段采用分类路线作为可信实验，不把分类目录伪装为真实检测数据。

strict 数据集处理结果：

| 项目 | 结果 |
|---|---:|
| 数据路径 | `data/classification_strict_jpeg` |
| 类别数 | 92 |
| train 图像 | 7826 |
| val 图像 | 1741 |
| 总图像 | 9567 |
| 跳过 GIF/损坏图 | 28 |
| 转换为 JPEG | 122 |
| 图片复审 errors / warnings | 0 / 0 |

类别一致性审计：

| 项目 | 结果 |
|---|---:|
| 审计输出 | `reports/class_consistency_audit.md/json` |
| 原始类别 | 93 |
| 原始 train / val 类别 | 92 / 93 |
| strict 类别 | 92 |
| 未纳入 strict 类别 | `大腹皮` |
| `大腹皮` 原始 train / val | 0 / 19 |
| 审计状态 | `needs_class_completion` |

可复现实验 Manifest：

| 项目 | 结果 |
|---|---:|
| Manifest 输出 | `reports/repro_manifest.md/json` |
| 关键产物哈希 | 92 个 |
| 复现命令 | 31 条 |
| 记录内容 | 环境版本、训练配置、类别审计摘要、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、标注样本 contact sheet、Top-1/Top-5、benchmark、工程自检、报告与权重 SHA256 |

重复/泄漏审计：

| 项目 | strict 92 类 | 93 类补齐 |
|---|---:|---:|
| 审计报告 | `reports/strict_classification_duplicate_audit.md` | `reports/classification_93class_duplicate_audit.md` |
| 状态 | `needs_leakage_review` | `needs_leakage_review` |
| 重复 SHA256 组 | 546 | 546 |
| train/val 泄漏组 | 34 | 34 |
| 跨类别重复组 | 52 | 52 |
| 处理边界 | 人工复核后再删除或重划 | 人工复核后再删除或重划 |

泄漏人工复核包：

| 项目 | 结果 |
|---|---:|
| 复核包 | `reports/classification_leakage_review_package.md/json` |
| 对照图 | `reports/figures/classification_train_val_leakage_contact_sheet.png` |
| 覆盖 train/val 泄漏组 | 34 / 34 |
| 涉及文件记录 | 69，train 35 / val 34 |
| 同类别 / 跨类别泄漏组 | 16 / 18 |
| 与 93 类补齐审计共享泄漏哈希 | 34 |
| 人工决策栏 | `manual_decision` 留空，等待人工确认后填写 |

候选泄漏清理集：

| 项目 | strict 92 类候选集 | 93 类候选集 |
|---|---:|---:|
| 数据路径 | `data/classification_strict_jpeg_leakage_clean_candidate` | `data/classification_strict_jpeg_93class_leakage_clean_candidate` |
| train / val / total | 7826 / 1707 / 9533 | 7841 / 1711 / 9552 |
| 已移除 val 侧泄漏副本 | 34 | 34 |
| 图片复审 errors / warnings | 0 / 0 | 0 / 0 |
| train/val 泄漏组 | 0 | 0 |
| 跨类别重复组 | 34 | 34 |
| 状态 | `needs_leakage_review` | `needs_leakage_review` |

该候选集只删除复核包中列出的 val 侧字节级重复副本，不自动修改 train 图像，也不裁决跨类别标签；重新训练前仍需用新的审计报告解释剩余跨类别重复。

跨类别复核包：

| 项目 | 结果 |
|---|---:|
| 复核包 | `reports/classification_cross_class_review_package.md/json` |
| 对照图 | `reports/figures/classification_cross_class_contact_sheet.png` |
| 覆盖跨类别重复组 | 34 / 34 |
| 涉及文件记录 | 68，train 62 / val 6 |
| train/val 泄漏组 | 0 |
| 涉及类别数 | 22 |
| 与 93 类候选集共享跨类别哈希 | 34 |
| 人工决策栏 | `manual_decision` 留空，等待人工确认真实类别后填写 |

该复核包只整理候选清理集剩余的字节级 exact duplicate 标签冲突；不自动删除、移动、重命名或重标图片。正式重训前应先确认每组图片真实类别，并把处理决策写回复核记录或后续清理报告。

跨类别决策表：

| 项目 | 结果 |
|---|---:|
| 决策表 | `reports/classification_cross_class_decision_table.md/json/csv` |
| 状态 | `ready_for_manual_decision` |
| 待决策组 | 34 / 34 |
| 已决策组 | 0 |
| 校验错误 | 0 |
| 填写入口 | `classification_cross_class_decision_table.csv` |

该决策表把复核包中的 `manual_decision` 空栏标准化为 `decision_status`、`chosen_class`、`action`、`remove_relative_paths`、`reviewer`、`reviewed_at` 和 `decision_note` 等字段；它只收集人工决策，不自动删除、移动、重命名、重标或复制图片。

跨类别清理计划校验：

| 项目 | 结果 |
|---|---:|
| 清理计划 | `reports/classification_cross_class_cleanup_plan.md/json/csv` |
| 状态 | `waiting_for_manual_decisions` |
| 待决策组 | 34 / 34 |
| 计划操作 | 0 |
| 校验错误 | 0 |
| 操作预览 | `classification_cross_class_cleanup_plan.csv` |

该校验报告把人工决策 CSV 转换为执行前 dry-run 计划；当前所有组仍为 `pending`，因此不会产生删除或移动操作。人工填完 CSV 后应先重新生成该报告，只有状态为 `ready_for_cleanup_execution` 且校验错误为 0 时，才可进入真实数据清理执行。

跨类别清理执行入口：

| 项目 | 结果 |
|---|---:|
| 执行脚本 | `scripts/apply_classification_cross_class_cleanup_plan.py` |
| 当前状态 | 真实计划未就绪时阻断执行 |
| 写入边界 | 只复制到新的输出数据集目录，不删除或覆盖源候选集 |

该脚本用于人工决策全部完成并通过清理计划校验之后。当前 `classification_cross_class_cleanup_plan.json` 仍为 `waiting_for_manual_decisions`，因此脚本会返回 `cleanup_execution_blocked`，不会生成清理输出目录或执行报告。

93 类补齐实验：

| 项目 | 结果 |
|---|---:|
| 数据路径 | `data/classification_strict_jpeg_93class` |
| 输出类别 | 93 |
| train 图像 | 7841 |
| val 图像 | 1745 |
| 总图像 | 9586 |
| `大腹皮` train / val | 15 / 4 |
| 数据复审 errors / warnings | 0 / 0 |
| 训练输出 | `runs/train/strict_93class_yolo12n_cls_cpu_smoke` |
| 独立验证 Top-1 | 0.0664756447 |
| 独立验证 Top-5 | 0.2085959911 |
| Fitness | 0.1375358179 |

该 93 类补齐实验用于证明完整类别覆盖链路已跑通；由于 `大腹皮` 来自原始 val-only 样本重划，且训练只有 1 epoch，不能替代 92 类 strict 5 epoch 基准指标。

检测标注准备包：

| 项目 | 结果 |
|---|---:|
| 输出目录 | `data/detection_annotation_package` |
| 覆盖类别 | 93 |
| 待标注图片 | 279 |
| 每类抽样 | 3 张，train 2 + val 1 |
| 预期标签 / 已完成标签 | 279 / 0 |
| 来源划分 | train 186 / val 93 |
| 样本总览 contact sheet | `reports/detection_annotation_contact_sheet.md` + `reports/figures/detection_annotation_contact_sheet.png` |
| 状态 | `pending_bbox_annotation` |

该准备包用于后续人工绘制真实 YOLO bbox：`images/` 放待标注图片，`classes.txt` 固定 93 类顺序，`annotation_manifest.csv/json` 记录来源和预期标签文件；`detection_annotation_contact_sheet` 用于标注前复核每类 3 张样本。`labels/` 仍为空，因此不可直接训练检测模型，也不能据此汇报检测指标。

检测标注包校验：

| 项目 | 结果 |
|---|---:|
| 校验报告 | `reports/detection_annotation_package_validation.md/json` |
| 状态 | `pending_bbox_annotation` |
| 图片 | 279 / 279 |
| 缺失标签 | 279 |
| 有效 bbox | 0 |
| errors / warnings | 0 / 0 |

当前校验证明待标注包结构、图片和 manifest 一致；人工标注完成后应使用同一脚本增加 `--require-complete`，确认 279 个 `.txt` 标签全部存在、类别编号与 manifest 一致、bbox 归一化合法后，再进入检测训练。

训练与验证结果：

| 项目 | 结果 |
|---|---:|
| 模型 | `yolo12n-cls.yaml` |
| 训练设备 | CPU |
| epoch | 5 |
| batch | 16 |
| imgsz | 224 |
| 训练输出 | `runs/train/strict_classify_yolo12n_cls_cpu_5e` |
| 独立验证 Top-1 | 0.1769098192 |
| 独立验证 Top-5 | 0.4956921339 |
| Fitness | 0.3363009766 |

推理、导出与应用联调结果：

| 项目 | 结果 |
|---|---:|
| 单样例 Top-k 推理 | `reports/strict_classification_sample_prediction.json` |
| 样例 Top-1 | 干姜，置信度 0.0926 |
| strict CPU benchmark | 20 张样本，mean 9.76 ms/image，约 102.51 FPS |
| benchmark 输出 | `runs/benchmarks/strict_classification_latency_20.json` |
| ONNX 导出 | `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx` |
| 后端分类接口 | `POST /classify/image`，后端 QA 4/4 |
| 前端分类入口 | 默认分类识别，上传 strict 验证图后返回 Top-k，前端 QA 6/6 |

每类表现与误判分析：

| 项目 | 结果 |
|---|---:|
| 分析输出 | `reports/strict_classification_error_analysis.md/json` |
| 分析图像 | 1741 |
| 分析类别 | 92 |
| Top-1 正确 | 308 / 1741 |
| Top-5 正确 | 863 / 1741 |
| Top-1 最高类别 | `枸杞子`、`莲子心`，均为 1.0000 |
| Top-1 最低类别 | `地龙`、`安息香`、`瓦楞子`、`北沙参` 等为 0.0000 |
| 高频混淆 | `九香虫 -> 木丁香`、`合欢皮 -> 川牛膝`、`柏子仁 -> 芥子`、`荜澄茄 -> 木丁香`，均为 12 次 |

人工复核样例：

| 项目 | 结果 |
|---|---:|
| 复核清单 | `reports/strict_classification_review_samples.md/json` |
| 高频混淆样例 | 18 张 |
| 低表现类别样例 | 18 张 |
| 高频混淆 contact sheet | `reports/figures/strict_confusion_contact_sheet.png` |
| 低表现类别 contact sheet | `reports/figures/strict_worst_class_contact_sheet.png` |

相关文件：`reports/strict_classification_training_report.md`、`reports/strict_classification_evaluation_metrics.json`、`reports/strict_classification_dataset_inspection.md`、`reports/class_consistency_audit.md`、`reports/repro_manifest.md`、`reports/strict_classification_error_analysis.md`、`reports/strict_classification_review_samples.md`。

该结果说明真实分类数据训练链路已跑通，并且 5 epoch 相比 1 epoch 冒烟训练有明显提升；但它仍不是检测 mAP，不能证明模型具备药材区域定位能力。

## 7. 性能与接口测试

| 测试项 | 结果 | 说明 |
|---|---:|---|
| 工程自检 | 以 `reports/smoke_check.json` 为准 | 覆盖 strict 数据集汇总、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、93 类补齐实验、检测标注准备包、标注样本 contact sheet、标注包校验、类别一致性审计、可复现实验 Manifest、Top-1/Top-5 指标、误判分析、人工复核 contact sheet、ONNX 文件、benchmark、Top-k 样例、QA 汇总、Word/PPT 和报告关键字段校验 |
| 单元测试 | 8 / 8 通过 | `pytest tests -q` |
| 前端构建 | 通过 | `npm run build` |
| 前端 Playwright QA | 6 / 6 通过 | 桌面端、移动端、分类上传、目标检测页签、摄像头页签、训练页签 |
| 相关 console error | 0 | Vite 调试日志不计为错误 |
| 后端 API QA | 4 / 4 通过 | `/health`、`/models`、`/detect/image`、`/classify/image` |
| API 图片识别耗时 | 75.08 ms | demo 权重、本机 CPU、单次请求 |
| API 分类识别耗时 | 42.88 ms | strict 分类权重、本机 CPU、单次请求 |
| CPU 单图 benchmark | 27.07 ms | demo 权重、imgsz=320、1 张图 |
| CPU 单图 FPS 估计 | 36.94 FPS | demo benchmark 粗略估计，不代表生产吞吐 |
| strict 分类 CPU benchmark | 9.76 ms | 20 张验证样本、imgsz=224、本机 CPU |
| strict 分类 FPS 估计 | 102.51 FPS | 小样本延迟测试，用于工程参考 |

截图文件：`reports/figures/frontend_desktop.png`、`reports/figures/frontend_classify_result.png`、`reports/figures/frontend_mobile.png`。

## 8. 真实检测准确性指标状态

| 指标 | 当前结果 | 备注 |
|---|---:|---|
| Precision | 待真实数据实测 | 正式训练完成后生成 |
| Recall | 待真实数据实测 | 正式训练完成后生成 |
| mAP@50 | 待真实数据实测 | 正式训练完成后生成 |
| mAP@50-95 | 待真实数据实测 | 正式训练完成后生成 |
| per-class AP | 待真实数据实测 | 正式训练完成后生成 |
| 混淆矩阵 | 待真实数据实测 | Ultralytics val 输出 |
| PR / F1 曲线 | 待真实数据实测 | Ultralytics val 输出 |

分类阶段已有阶段性指标：strict 数据集 Top-1 0.1769、Top-5 0.4957，并已补充每类误判分析、人工复核 contact sheet、泄漏人工复核包、候选泄漏清理集和跨类别复核包。候选泄漏清理集已将 train/val exact duplicate 归零；剩余 34 组跨类别 exact duplicate 已生成复核包，因此重新训练和指标解释仍需带类别复核边界；检测标注准备包已覆盖 93 类、279 张待标注图，并生成样本总览 contact sheet；pending 校验为 errors 0 / warnings 0，但 `labels/` 仍为空；检测阶段的 Precision、Recall、mAP 仍需真实 bbox 标注完成后生成。
类别覆盖方面，当前 strict 5 epoch 基准覆盖 92 类；93 类补齐实验已让 `大腹皮` 进入训练/验证链路，但仍需新增采集或标注训练样本后才能形成更严格的 93 类正式基准。

## 9. 鲁棒性测试方案

`scripts/robustness_test.py` 可生成以下扰动样本：

- 低光照
- 高光照
- 低对比度
- 旋转 15 度
- 高斯模糊
- 中心遮挡

正式测试方法：在干净测试集和扰动测试集上分别运行推理/评估，对比 Precision、Recall、mAP 和误检案例。该项需在真实测试集接入后执行。

## 10. 风险与限制

1. 若公开数据只有分类标签，没有边界框，必须补充检测标注；整图框转换只能跑通流程，不能作为高质量检测标注。
2. YOLOv12 属于注意力中心研究模型，可能存在训练不稳定、显存占用高、CPU 推理慢等问题。
3. 参考文献中的 GhostC2f、DySnakeC2f、SimSPPF、CA 属于 YOLOv8-TCM 改进，不应未经消融直接迁移到 YOLOv12。
4. 文献结果不能直接作为本项目结果；本项目指标必须来自当前数据集和当前权重。
5. 当前 demo 训练用于验证工程链路，不能替代正式实验。
6. 当前 strict 训练是分类任务，只能汇报 Top-1/Top-5，不能替代检测任务的 mAP。
7. `大腹皮` 已通过补齐实验进入 1 epoch 训练链路，但其 train/val 来自原始 val-only 样本重划，正式 93 类基准仍建议补充独立训练样本。
8. 检测标注准备包和样本总览 contact sheet 只是人工标注启动材料，`labels/` 仍为空，不能作为已完成检测数据集。
9. 重复/泄漏审计只检查文件字节级 SHA256 完全重复；当前已生成候选泄漏清理集并移除 val 侧 train/val exact duplicate，剩余 34 组跨类别 exact duplicate 已生成跨类别复核包，需人工确认真实类别后再决定删除、移动、重标或保留。

## 11. 后续补测清单

- 若最终要求目标检测，补充真实 YOLO bbox 标注数据集。
- 优先使用 `data/detection_annotation_package` 完成人工 bbox 标注，保持 `classes.txt` 的 93 类顺序不变。
- 运行数据校验和划分。
- 在 GPU 环境完成 strict 分类 30-100 epoch 正式训练。
- CPU 正式配置：`configs/train_cls_strict_cpu_30e.yaml`。
- GPU 正式配置：`configs/train_cls_strict_gpu_100e.yaml`。
- 为 `大腹皮` 补充独立训练样本后运行 93 类正式长轮次实验。
- 完成 YOLOv12s 或关键调参对照。
- 生成真实检测评估指标、训练曲线和混淆矩阵。
- 运行 CPU/GPU benchmark。
- 基于 `data/classification_strict_jpeg_leakage_clean_candidate` 或 `data/classification_strict_jpeg_93class_leakage_clean_candidate` 重新训练前，先使用 `classification_cross_class_review_package.md` 和 contact sheet 复核剩余 34 组跨类别 exact duplicate，并记录处理决策。
- 基于 `strict_classification_review_samples.md`、`detection_annotation_contact_sheet.md` 和 contact sheet 继续补充人工复核结论、标注复核结论、补样优先级和最终答辩材料。
- 将真实实验结果同步更新到 `reports/test_report.md`、`reports/test_report.docx` 和 `reports/overview_design.pptx`。
