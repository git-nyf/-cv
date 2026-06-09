# 分类跨类别标签冲突清理计划校验报告

- 决策表: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_table.json`
- 决策 CSV: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_table.csv`
- 状态: `waiting_for_manual_decisions`
- 待决策组: 34 / 34
- 已决策组: 0
- 需专家复核组: 0
- 延后处理组: 0
- 校验错误: 0
- 计划操作: 0，remove 0，move 0
- 操作 CSV: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_cleanup_plan.csv`

## 边界说明

本报告只把人工决策转换为可审计清理计划；不会删除、移动、重命名、重标或复制任何图片。

## 建议后续动作

- 人工填写所有 pending 决策后重新生成本清理计划。
- 仅当 status 为 ready_for_cleanup_execution 且 validation_errors 为 0 时，才可进入真实数据清理执行脚本。
- 执行清理后必须重新运行 classification inspection、duplicate audit、训练和独立评估。

## 操作预览

| operation | group_id | source | target | reason |
|---|---|---|---|---|
| - | - | - | - | 当前没有可执行操作 |
