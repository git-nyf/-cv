# 检测标注准备包校验报告

- 包目录: `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package`
- 状态: `pending_bbox_annotation`
- 严格完成模式: False

## 总览

- 类别数: 93
- manifest 图片数: 279
- 实际图片数: 279
- 预期标签: 279
- 已完成标签: 0
- 缺失标签: 279
- 空标签: 0
- 有效 bbox 数: 0
- 含 bbox 类别数: 0
- errors / warnings: 0 / 0

## 当前结论

- 当前仍是待人工标注状态；结构和 manifest 可用于标注启动，但不能直接训练检测模型。

## 缺失标签示例

- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\000_train_01_Sigualuo0.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\000_train_02_Sigualuo1.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\000_val_03_Sigualuo117.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\001_train_01_Jiuxiangchong10.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\001_train_02_Jiuxiangchong100.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\001_val_03_Jiuxiangchong1.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\002_train_01_WujiapiWujiapiWujiapiIMG_20200722_165948.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\002_train_02_WujiapiWujiapiWujiapiIMG_20200722_165951.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\002_val_03_WujiapiWujiapiWujiapiIMG_20200722_170020.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\003_train_01_Renshen10.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\003_train_02_Renshen100.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\003_val_03_Renshen108.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\004_train_01_Jiangcan0.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\004_train_02_Jiangcan1.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\004_val_03_Jiangcan108.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\005_train_01_Quanxie0.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\005_train_02_Quanxie1.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\005_val_03_Quanxie13.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\006_train_01_DongchongxiacaoDongchongxiacao101.txt`
- `D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package\labels\006_train_02_DongchongxiacaoDongchongxiacao103.txt`

## 问题列表

- 未发现结构或已有标签格式问题

## 边界说明

- pending_bbox_annotation 表示标注准备包结构有效但 labels/ 尚未补齐；只有 require_complete=true 且 status=complete 后才可进入检测训练。
