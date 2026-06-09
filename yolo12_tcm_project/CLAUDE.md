# Claude Code 项目入口说明

完整接手手册在：

```text
D:\AAA中药cv\CLAUDE.md
```

如果你从 `D:\AAA中药cv\yolo12_tcm_project` 启动，请先读上面的根目录手册。这里保留最关键的行动边界：

- 当前可信主线是 YOLOv12 中药饮片“分类”工程，不是已经完成真实 bbox 检测训练。
- 原始数据是 `D:\AAA中药cv\data\train\<类别>\*.jpg` 和 `D:\AAA中药cv\data\val\<类别>\*.jpg` 分类目录。
- 目前没有真实 bbox 标注；`data/detection_annotation_package/labels/` 仍为空，检测包状态是 `pending_bbox_annotation`。
- 不要报告检测 mAP、Precision、Recall，除非人工 YOLO bbox 标注完成并通过 `validate_detection_annotation_package.py --require-complete`。
- strict 分类基准：92 类，9567 张图，CPU 5 epoch，Top-1 0.1769，Top-5 0.4957。
- 93 类补齐实验：`大腹皮` 从 val-only 19 张确定性重划为 15 train / 4 val，CPU 1 epoch 只证明链路可跑。
- 跨类别 exact duplicate 仍有 34 组待人工决策。不要自动填写 `reports/classification_cross_class_decision_table.csv`。
- 当前 `reports/classification_cross_class_cleanup_plan.json` 是 `waiting_for_manual_decisions`，计划操作 0，不允许执行真实清理。
- 清理脚本必须只在 cleanup plan 为 `ready_for_cleanup_execution` 且 `validation_errors=0` 后运行，并且只写新输出目录。
- 最后一次完整验证：`pytest` 17/17，`smoke_check` 161/161，Manifest 94 个产物、32 条复现命令。

常用自检：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\generate_repro_manifest.py --output reports\repro_manifest.json --markdown reports\repro_manifest.md
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```
