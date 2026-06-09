# 模型卡片

## 模型名称

YOLOv12-TCM Baseline

## 基础模型

- YOLOv12n：首选基线，适合快速闭环。
- YOLOv12s：在显存和时间允许时进行对照。

## 任务

中药饮片目标检测：输出边界框、类别和置信度。

## 训练输入

- 输入尺寸：默认 640，可对小目标尝试 768/960。
- 数据格式：YOLO detection。
- 划分：7:2:1。

## 评估指标

- Precision
- Recall
- mAP@50
- mAP@50-95
- per-class AP
- 混淆矩阵
- 单图延迟
- FPS
- 模型大小
- 参数量/FLOPs

## 参考改进方向

GhostC2f、DySnakeC2f、SimSPPF、CA 来自 YOLOv8-TCM 文献，不能直接视作 YOLOv12 的天然模块。建议作为二阶段实验：

1. 完成 YOLOv12n/s 基线。
2. 做输入尺寸、学习率、batch、阈值和增强策略调优。
3. 评估是否有必要迁移轻量化或注意力模块。
4. 若迁移，必须做消融实验和稳定性记录。

