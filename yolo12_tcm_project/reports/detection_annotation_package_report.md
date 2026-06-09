# 检测 bbox 标注准备包报告

- 来源数据: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class`
- 输出目录: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package`

## 总览

- 状态: `pending_bbox_annotation`
- 类别数: 93
- 待标注图片: 279
- 预期标签文件: 279
- 已完成标签文件: 0
- 每类样本数: min 3 / max 3
- 来源划分: {'train': 186, 'val': 93}

## 关键文件

- 标注说明: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\ANNOTATION_GUIDE.md`
- 类别文件: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\classes.txt`
- 数据模板: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\data_template.yaml`
- CSV manifest: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\annotation_manifest.csv`
- JSON manifest: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\annotation_manifest.json`

## 抽样说明

- 每类最多 3 张，优先选择 train 2 张和 val 1 张。
- 本抽样用于标注启动和检测链路建设，后续正式训练可扩大到全量图片。

## 边界说明

- 当前没有真实 bbox 标签，不能训练检测模型或汇报检测指标。
- 标注完成后需运行 YOLO 标签校验、划分数据集、训练检测模型并重新生成评估报告。
