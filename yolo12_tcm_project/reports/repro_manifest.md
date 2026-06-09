# 可复现实验 Manifest

- 生成时间: 2026-06-09T15:01:22
- 项目目录: `D:\AAA中药cv\yolo12_tcm_project`

## 环境

- Python: 3.13.7
- Python executable: `D:\AAA中药cv\yolo12_tcm_project\.venv\Scripts\python.exe`
- Platform: Windows-11-10.0.26200-SP0

| 包 | 版本 |
|---|---|
| torch | 2.6.0+cu124 |
| ultralytics | 8.4.60 |
| fastapi | 0.136.3 |
| uvicorn | 0.49.0 |
| playwright | 1.60.0 |
| pillow | 12.2.0 |
| PyYAML | 6.0.3 |
| python-docx | 1.2.0 |
| pytest | 9.0.3 |

## 数据与类别边界

- strict 数据集: 92 类，train 7826 / val 1741 / total 9567，verified 9567，errors 0，warnings 0
- strict 重复/泄漏审计: 状态 `needs_leakage_review`，重复 SHA256 组 546，train/val 泄漏组 34，跨类别重复组 52
- 泄漏人工复核包: 状态 `complete_review_package`，覆盖 34 / 34 组 train/val 泄漏，涉及记录 69，跨类别泄漏组 18，对照图 `classification_train_val_leakage_contact_sheet.png`
- strict 候选泄漏清理集: 状态 `leakage_val_duplicates_removed`，移除 val 副本 34 张，输出 train 7826 / val 1707 / total 9533，train/val 泄漏组 0，跨类别重复组 34
- 跨类别 exact duplicate 复核包: 状态 `complete_review_package`，覆盖 34 / 34 组，涉及记录 68，train/val 泄漏组 0，对照图 `classification_cross_class_contact_sheet.png`
- 跨类别标签冲突决策表: 状态 `ready_for_manual_decision`，待决策 34 / 34 组，已决策 0 组，校验错误 0
- 跨类别清理计划校验: 状态 `waiting_for_manual_decisions`，待决策 34 / 34 组，计划操作 0，校验错误 0
- 类别一致性: 原始 93 类，strict 92 类，状态 `needs_class_completion`
- 未纳入 strict 类别: 大腹皮
- zero-train 类别: 大腹皮
- 93 类补齐实验: 输出 93 类，train 7841 / val 1745 / total 9586，verified 9586，errors 0，warnings 0
- 93 类补齐重划类别: 大腹皮；大腹皮 15 train / 4 val
- 93 类重复/泄漏审计: 状态 `needs_leakage_review`，重复 SHA256 组 546，train/val 泄漏组 34，跨类别重复组 52
- 93 类候选泄漏清理集: 状态 `leakage_val_duplicates_removed`，移除 val 副本 34 张，输出 train 7841 / val 1711 / total 9552，train/val 泄漏组 0，跨类别重复组 34
- 检测标注准备包: 状态 `pending_bbox_annotation`，覆盖 93 类，待标注图片 279 张，预期标签 279 个，已完成标签 0 个
- 标注抽样: 每类 3 张，来源 train 186 / val 93；当前 labels/ 为空，不可直接训练检测模型
- 标注包校验: 状态 `pending_bbox_annotation`，图片 279 / 279，缺失标签 279，errors 0，warnings 0

## 训练与评估摘要

- 训练配置: `configs/train_cls_strict_cpu_5e.yaml`
- 模型: `yolo12n-cls.yaml`，epochs 5，imgsz 224，batch 16，device `cpu`
- Top-1: 0.17690981924533844
- Top-5: 0.4956921339035034
- Fitness: 0.33630097657442093
- benchmark: 20 张，mean 9.75544999964768 ms/image，FPS 102.50680389281018
- smoke check: 161 / 161 通过，failed 0

## 93 类补齐实验摘要

- 训练配置: `configs/train_cls_93class_smoke.yaml`
- 模型: `yolo12n-cls.yaml`，epochs 1，imgsz 224，batch 16，device `cpu`
- Top-1: 0.06647564470767975
- Top-5: 0.20859599113464355
- Fitness: 0.13753581792116165
- 边界: 该 1 epoch 结果证明 93 类覆盖链路可运行，不替代 92 类 strict 5 epoch 基准。

## 复现命令

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
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_decision_review_html.py --review-package reports\classification_cross_class_review_package.json --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_decision_review.html
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
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

## 关键产物哈希

| 路径 | bytes | SHA256 |
|---|---:|---|
| `configs/train_cls_strict_cpu_5e.yaml` | 301 | `0e0f6d19447fcf9c168c5017af825668dbb087d55a72cf9acd9651941ea488a4` |
| `configs/train_cls_93class_smoke.yaml` | 311 | `0be5f2e046dd8e343d245dc2ff432a1143af37bcdb6f852ad723d8b617552be7` |
| `configs/train_cls_strict_cpu_30e.yaml` | 303 | `62a369037deae11a61c0e6abd0aa38971b3c8e7d52aa27d9146b9e199b83a152` |
| `configs/train_cls_strict_gpu_100e.yaml` | 303 | `1e452d8c0f22aaab7ff6fda5910391960ddbd78b8ea85cf4a8f4f297420944f9` |
| `data/classification_strict_jpeg/strict_classification_report.json` | 19027 | `84fdcd6a9ac74a9730f09ff4d5fcdd1164a6fd722fe525954a93d01230d31729` |
| `data/classification_strict_jpeg_93class/classification_93class_completion_report.json` | 39505 | `68160981c7c01c21b9664b40bae65a44f56fc274474bf73de743c2e1ce6d2328` |
| `data/classification_strict_jpeg_93class/classification_93class_completion_report.md` | 4832 | `1879491febf22d0d11759459364b3c080b7a3fb7bb02fbe661de1e5eac4be9af` |
| `data/detection_annotation_package/ANNOTATION_GUIDE.md` | 1895 | `e3f00540a11bca3b973f783f67c7fe7562953368ac6f860fe4436238766cccd9` |
| `data/detection_annotation_package/annotation_manifest.csv` | 129443 | `77ee10bbf2163f2e231f3c11fa1ce3d7c41b839f3b2912356b44ed601e7b46e4` |
| `data/detection_annotation_package/annotation_manifest.json` | 214667 | `8a4a187fd1770ecf13f823fb6d9872ae0acf68bf5c6738b4df93cfe1be7d4c9f` |
| `data/detection_annotation_package/annotation_summary.md` | 1408 | `e8fec620bfc7f6c3031c30aff78843a4563bccfbd32d85e88a91ed1d1fdb2075` |
| `data/detection_annotation_package/classes.txt` | 909 | `e76fec830f76735df00a41065e9b67b098764d0e9c0ad911ae5d260c850537aa` |
| `data/detection_annotation_package/data_template.yaml` | 1597 | `dc85a482a66ab419c385691929fbd5d7162950ffafd6461ef7f7922bfdd1215b` |
| `data/detection_annotation_package/labels/README.md` | 126 | `c1bc28b6098fd5adbaca0a3e5ec831f8608ff9586e2bb38fc1bdafa3e6444663` |
| `scripts/validate_detection_annotation_package.py` | 11888 | `365a2d75d4a968167b7f530bf26c3e53115fc286f50eea154ccc0f411bf771a8` |
| `scripts/generate_detection_annotation_contact_sheet.py` | 6535 | `6f4b885ea9a18409da2cbfccbdaf6c41ac6e36b36f69e1306fcd2ce71232ea9d` |
| `scripts/audit_classification_duplicates.py` | 7445 | `e1d43414e8423ac2f0cdbc82abe9537c4b6f53a10ae415f23b667fa72cdcdc56` |
| `scripts/generate_classification_leakage_review_package.py` | 12575 | `20576651d0f908c926dae88555f6e116a22a24568360a876ec24d4cff46f7bf1` |
| `scripts/prepare_leakage_clean_classification_dataset.py` | 8948 | `ff31e0d1b35e669da21f41553246e4c278830fa59cf15c2d8899d9dde0498f19` |
| `scripts/generate_classification_cross_class_review_package.py` | 12554 | `e6dffe412200291795913948857ed0ab067dec8506b079b791b400a1a6e9bf4b` |
| `scripts/generate_classification_cross_class_decision_table.py` | 11853 | `9472e4167e6cc4b2aa3eafe95a96a6421dceb6b7139104ff5fb7d91d86eb7615` |
| `scripts/generate_classification_cross_class_decision_review_html.py` | 18893 | `e2013b3d4564c1a89c27ec1b054e9de00e7a8a44be7a72719fdff1df4932101d` |
| `scripts/generate_classification_cross_class_cleanup_plan.py` | 15479 | `e4576515998900fe562ce291758585853efd3e2f21e3b814948d93da03fb670b` |
| `scripts/apply_classification_cross_class_cleanup_plan.py` | 14993 | `d2a8555bc637389d4f4cfbdb33dd95b7bb693ea308b618e044ae1684c3b3785b` |
| `reports/strict_classification_dataset_inspection.json` | 6149 | `84a0ffb1c6120400cb279a4aecd576426dc379b6c1dde6223e029939836b9f5b` |
| `reports/strict_classification_duplicate_audit.json` | 103852 | `db2159b578600538cc9d94e462231ff35e32891400c9cefd6460a6a0deb95322` |
| `reports/strict_classification_duplicate_audit.md` | 12680 | `ec06b9078443248189b6952714d8e95c2ca373367cdff908f403283c478f5d0b` |
| `reports/classification_leakage_review_package.json` | 53315 | `6e275e1ac49745c461d890225b4b6875a5a17b49962f9cf91dd5d0bdb746afe4` |
| `reports/classification_leakage_review_package.md` | 9748 | `a49265537a79cccaf015c9cef0df16f9215b8208838bfa15f472b6d51b3813ed` |
| `reports/classification_leakage_clean_candidate_report.json` | 16406 | `93423f86c8abf9de9a652d8490928dc7236562665bde59e2931f9669ded68c0d` |
| `reports/classification_leakage_clean_candidate_report.md` | 4090 | `86be4f1bcee4390b7de1521a423848de0c3d872fa695798a5984b9060e41e938` |
| `reports/classification_leakage_clean_candidate_inspection.json` | 6173 | `c87a4f30bb6cff9885881e76dfbf40a83cef737272dba457413c49f4eb3a4487` |
| `reports/classification_leakage_clean_candidate_inspection.md` | 3295 | `cc0f4134e42f8f6e07cd4b3810869618aa4f71360023a7aa8aeaa0618b5a7eb5` |
| `reports/classification_leakage_clean_candidate_duplicate_audit.json` | 107970 | `fccc88bd7a96789c0d38fbe5e97d1f9e50ffca096bd59dc37da353de9e7b1934` |
| `reports/classification_leakage_clean_candidate_duplicate_audit.md` | 12826 | `54a4489c9b1a026fe754d181b20faa350bef070810aa8a89490296ae217606db` |
| `reports/classification_cross_class_review_package.json` | 56973 | `b0e9cc40d73082cbeab3338fb8c61e3f8c25cdcbf4092a82fe5d96d6d29b396a` |
| `reports/classification_cross_class_review_package.md` | 11413 | `57ae8ba1ed5f5fe1615f66ececa4546cc3506e56c31424c4263b5ce7b20ab033` |
| `reports/classification_cross_class_decision_table.json` | 55659 | `9ba28b3a0bb3d8008894343c177ce33958d5e2f7ca08516bff504122fa1c770e` |
| `reports/classification_cross_class_decision_table.csv` | 10633 | `2e1e13816ee8c64780bc0786cc9c0c53a07815f0f3d466e379b2df4d18862bf8` |
| `reports/classification_cross_class_decision_table.md` | 6030 | `1d4075b688ea75a02e3a39f7b9e7ad9bf78e21b9c0dc07ffcc3813a16da0cfd8` |
| `reports/classification_cross_class_decision_review.html` | 163474 | `b18f99e590b96866b3b8bd75dccce9ece2fa83c9200e23a0d80ee98685c9f45b` |
| `reports/classification_cross_class_cleanup_plan.json` | 1289 | `e86b1b9801b05f90e0303def47198630ccdf49f410a161f4883206bbc0065b84` |
| `reports/classification_cross_class_cleanup_plan.csv` | 123 | `af7c4e96b4901b62bb3fd3f2f4351dd89e23b6a3e84c171942fa7d9e5e78b95f` |
| `reports/classification_cross_class_cleanup_plan.md` | 1190 | `a7a6f5b8c65dbfa1759b4f2026a4a0c18e2d6a2f3bf9b9c578c8eaf23fb7878c` |
| `reports/class_consistency_audit.json` | 38828 | `36a3cc46ce19e7045714d3bafdf9578a3845161f087f5811f567c148ae179fcf` |
| `reports/class_consistency_audit.md` | 3820 | `59147b8feb22a0e5c952aead884b0de6a5bd5a16d9dc0ae19bd498190f8bc71b` |
| `reports/classification_93class_completion_report.json` | 39505 | `68160981c7c01c21b9664b40bae65a44f56fc274474bf73de743c2e1ce6d2328` |
| `reports/classification_93class_completion_report.md` | 4832 | `1879491febf22d0d11759459364b3c080b7a3fb7bb02fbe661de1e5eac4be9af` |
| `reports/classification_93class_dataset_inspection.json` | 6222 | `4798d43b3e44708998b104ad4ebbc553494d93cdf3698773d8dc1f27cb3e9216` |
| `reports/classification_93class_dataset_inspection.md` | 3312 | `7fcbbff805fe4edc0539e4d21fec7a88130c2042e410e3a4710673593cb97d1b` |
| `reports/classification_93class_duplicate_audit.json` | 105196 | `e933819eaa2ab6ede34b5501da6cba1d6e3db9ea968e4673a0c9b43491119378` |
| `reports/classification_93class_duplicate_audit.md` | 12688 | `2d786c7b5bce600fb95d1b0aa32e02204945325dc034dc79d991868cf18153ae` |
| `reports/classification_93class_leakage_clean_candidate_report.json` | 16741 | `815b51ad11c117086a73ebe5722af52adb016086d1a4310ee167b0c6af3e1cfb` |
| `reports/classification_93class_leakage_clean_candidate_report.md` | 4106 | `baf0b1cb052b4973a54a31a727bf1fc4bc4b63ba5e3dacd60449a49e937eb3eb` |
| `reports/classification_93class_leakage_clean_candidate_inspection.json` | 6246 | `773a90aa0b3530c18f68e9d8a0d43442b1170bf69e7953f526895233e73ca998` |
| `reports/classification_93class_leakage_clean_candidate_inspection.md` | 3336 | `7c63ddc24e941638942ce09b899493953ffe86d811131709fe547d2c07544295` |
| `reports/classification_93class_leakage_clean_candidate_duplicate_audit.json` | 109306 | `f75ce3a1541f23e58f87fb40534097e855e5e054b223d6386c72d57935b80e32` |
| `reports/classification_93class_leakage_clean_candidate_duplicate_audit.md` | 12834 | `4e9c386fad95e2a0bf8e0bc2f23168a483c45a782839e4a74f5c7168c62ebdc6` |
| `reports/classification_93class_training_report.md` | 3635 | `1ba41da897777ac1f008fa416b278eac39c0be9554ed3a06fbe329fca432f619` |
| `reports/classification_93class_evaluation_metrics.json` | 102 | `35c1437c94415bca08357eb715f57b842b0f8eb02a9bd24c86a1a2d4e9528427` |
| `reports/detection_annotation_package_report.json` | 214667 | `8a4a187fd1770ecf13f823fb6d9872ae0acf68bf5c6738b4df93cfe1be7d4c9f` |
| `reports/detection_annotation_package_report.md` | 1408 | `e8fec620bfc7f6c3031c30aff78843a4563bccfbd32d85e88a91ed1d1fdb2075` |
| `reports/detection_annotation_package_validation.json` | 5407 | `1ed6d963c4e8b8dc893d65c70f341a2552940d3d96eeb4445f041a0365972736` |
| `reports/detection_annotation_package_validation.md` | 3140 | `4a42b01df37f35351a3c133e632c0fe9156fe0bd448a9b5a4f216911dca7dc49` |
| `reports/detection_annotation_contact_sheet.json` | 210372 | `ee4e87311330032b52337964e933d4fd86469793d92b1957c74007261d639deb` |
| `reports/detection_annotation_contact_sheet.md` | 30357 | `f3ea359ddc6d1dd8ae2f70f86c072a33bfb957d5d3b8b0f477077389aaaadafd` |
| `reports/strict_classification_evaluation_metrics.json` | 101 | `83f4d61e6f019ca89eb1c3661ebe638261313ce90ceb37e828c90cb8452d2952` |
| `reports/strict_classification_error_analysis.json` | 188719 | `8b5d9bb07103bbac2656c5911845827aab302c845020b26cea24681f48f986e4` |
| `reports/strict_classification_error_analysis.md` | 6953 | `e2a4a03a616acbbf0db7483f8f1b8e9d07df3c50927e37c4759ca6e476d7be58` |
| `reports/strict_classification_review_samples.json` | 33522 | `ba219d79ca0db435aa1eac0c9c18b9be13afe72e755cacfbfe03ff4425539792` |
| `reports/strict_classification_review_samples.md` | 6802 | `c55c57f664ed50544deffb6dde0b5c4a4545a7d6c7603b6ef3bb7debfbeb4496` |
| `reports/strict_classification_sample_prediction.json` | 1286 | `de47fb2d288ed6cfe1f1df991f1f4101daa0f8a738edc216795388c0eca8f38d` |
| `runs/benchmarks/strict_classification_latency_20.json` | 432 | `c4a9f1ce37f974096633997accdaaac36839e56edf3ddcbb9e4d2f097a515397` |
| `reports/backend_qa.json` | 1141 | `d68609ffc014deb4b701130d4246c6a2f95423d1c2987ad5151bc5135f9a7b91` |
| `reports/frontend_qa.json` | 2910 | `0b3e66ae12653314de5b62c7bc73bd6f11165b17da13311ce03dd91bba326baf` |
| `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.pt` | 3873085 | `bfa3307e6fcd53897b4cbcf981c616bf242eb1bdadd0f278dd3188a377e0b514` |
| `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/last.pt` | 3873085 | `bfa3307e6fcd53897b4cbcf981c616bf242eb1bdadd0f278dd3188a377e0b514` |
| `runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx` | 7410316 | `54b59063690688a344d9f4668e019b5b375be74391442708008bb7b4ffb8ecf5` |
| `runs/train/strict_93class_yolo12n_cls_cpu_smoke/results.csv` | 172 | `b7407a62d6000f25606b26003d0aef81ed362d2a3409b8efcc4e0c0969e3274b` |
| `runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/best.pt` | 3875389 | `5fa052ed074ad619438cc88565a4ff6435bebedce642e756a161019ce7a0860d` |
| `runs/train/strict_93class_yolo12n_cls_cpu_smoke/weights/last.pt` | 3875389 | `5fa052ed074ad619438cc88565a4ff6435bebedce642e756a161019ce7a0860d` |
| `reports/test_report.md` | 26273 | `093cf04937a1ff5059206493f8436d2d6dac45f8ee572f1540ce06b17e857822` |
| `reports/test_report.docx` | 3009722 | `340b4a969171f6e6eec77f5f5a0a482da95274ac1f316adb30197af6e068af5e` |
| `reports/strict_classification_training_report.md` | 16862 | `ec5d2f1f2588bfa0ea7eb8984bc53105c77f7259e4a08a4ba1e78e0272ddf716` |
| `reports/submission_checklist.md` | 20417 | `3c765fc226517bc6b44151002805da84edd358b173e186d6e51d36a3c031320a` |
| `reports/overview_design.pptx` | 303916 | `35078399d33d3bdacfcc4502fd017cf69fc0e3c3fe4cf093cc004666f62c9eff` |
| `reports/figures/strict_confusion_contact_sheet.png` | 1450407 | `5e9f800002f9fdfa5811f59850b05be36a424372c77e165754caef8fedb3a1a0` |
| `reports/figures/strict_worst_class_contact_sheet.png` | 1516732 | `259b2add3c54aaafba4054cdb7a1992cc3fa6ff97d74c5335330e824532872c5` |
| `reports/figures/classification_train_val_leakage_contact_sheet.png` | 2518389 | `1c33b8fa4da07b6881734c92b7ccffe38975dc7b002b740842299099e2a98c97` |
| `reports/figures/classification_cross_class_contact_sheet.png` | 2415251 | `0d05c7bed87fbbfacf29822e8dbf807a17e3a99a52ec035376268b39cca17030` |
| `reports/figures/detection_annotation_contact_sheet.png` | 13246218 | `e83042cd8d1fc22d8129e0dcfcc58d2b0bf82725a91f2c8ea5cc3421bb62a574` |
| `README.md` | 21818 | `f69a7f0ae0159695e3d6c8e6c54e3dcfcfb989632c5050578ca489fed15c8dd9` |
| `docs/README.md` | 18319 | `15f5eea63e710ab6f85713d58ea2f733417cdc011466bba2e8ffb1e1d60627b8` |
| `scripts/prepare_detection_annotation_package.py` | 13582 | `2e7559ea214c404ee1371a76e8389ef24c52f2fa03e6a411f0f8f7a1f6cd1138` |

## 边界说明

- 当前真实实验是分类任务，只能汇报 Top-1 / Top-5、每类误判分析、推理延迟和工程 QA。
- 原始数据不含真实 bbox 标注，不能汇报检测 Precision、Recall、mAP 或定位能力。
- strict 5 epoch 基准保持 92 类原始 train/val 交集；93 类补齐实验仅用于证明大腹皮已可进入训练链路。
- 93 类补齐实验将大腹皮 19 张原始 val-only 样本按确定性顺序拆为 15 train / 4 val，不应与原始 92 类 strict 指标直接等价比较。
- 检测标注准备包只包含待人工标注图片、类别顺序和 manifest；当前校验报告为 pending_bbox_annotation，labels/ 仍为空，不能据此训练检测模型或汇报检测指标。
- 重复与泄漏审计只检查文件字节级 SHA256 完全重复；已发现 train/val exact duplicate 和跨类别 exact duplicate，需人工复核后再删除或重划。
- classification_leakage_review_package 是删除或重划前的人工复核包，只提供复核清单和对照图，不改变数据集。
- leakage_clean_candidate 数据集只移除 val 侧 train/val exact duplicate 副本，不自动裁决跨类别标签；重新训练前仍需单独审计和报告新指标。
- classification_cross_class_review_package 只提供跨类别 exact duplicate 人工复核清单和对照图，不自动删除、移动、重命名或重标图片。
- classification_cross_class_decision_table 是跨类别标签冲突的人工决策输入表，当前默认 pending，不自动执行任何数据修改。
- classification_cross_class_decision_review.html 是本地静态复核页，只辅助人工查看图片和复制决策字段，不写回 CSV，也不自动裁决类别。
- classification_cross_class_cleanup_plan 是人工决策 CSV 的执行前校验报告；只在校验通过时生成可审计操作清单，本身不修改数据集。
- apply_classification_cross_class_cleanup_plan 是人工决策和计划校验通过后的非破坏性执行入口；当前计划未就绪时会阻断，真正执行也只写入新的输出目录。
