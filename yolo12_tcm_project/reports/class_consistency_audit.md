# 类别一致性审计报告

- 原始数据: `D:\AAA中药cv\data`
- strict 清洗报告: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\strict_classification_report.json`
- strict 复审报告: `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_dataset_inspection.json`

## 总览

- 状态: `needs_class_completion`
- 原始类别: 93；train 类别: 92；val 类别: 93
- strict 类别: 92
- 原始图片: train 7847 / val 1767 / total 9614
- strict 图片: train 7826 / val 1741 / total 9567
- strict 可读复审: verified 9567，errors 0，warnings 0
- 跳过图片: 28；转换 JPEG: 122；直接 JPEG: 9445

## 类别差异

- 未纳入 strict 的原始类别: 大腹皮
- strict 额外类别: 无
- 只在 train 出现: 无
- 只在 val 出现: 大腹皮
- 训练样本为 0 的类别: 大腹皮
- 验证样本为 0 的类别: 无

## 跳过图片分布

| 类别 | 跳过数 | 原因 |
|---|---:|---|
| 冬虫夏草 | 1 | unsupported content format: gif: 1 |
| 北沙参 | 1 | unsupported content format: gif: 1 |
| 木丁香 | 2 | unsupported content format: gif: 2 |
| 枸杞子 | 4 | unsupported content format: gif: 4 |
| 桑寄生 | 1 | broken data stream when reading image file: 1 |
| 浙贝母 | 1 | unsupported content format: gif: 1 |
| 淡豆豉 | 1 | unsupported content format: gif: 1 |
| 湖北贝母 | 1 | unsupported content format: gif: 1 |
| 灵芝 | 1 | unsupported content format: gif: 1 |
| 甘松 | 1 | unsupported content format: gif: 1 |
| 甘草 | 1 | unsupported content format: gif: 1 |
| 白前 | 1 | unsupported content format: gif: 1 |
| 白芍 | 2 | broken data stream when reading image file: 2 |
| 羌活 | 1 | unsupported content format: gif: 1 |
| 肉豆蔻 | 1 | unsupported content format: gif: 1 |
| 芦根 | 1 | unsupported content format: gif: 1 |
| 荆芥穗 | 1 | unsupported content format: gif: 1 |
| 荔枝核 | 1 | unsupported content format: gif: 1 |
| 荜拨 | 1 | unsupported content format: gif: 1 |
| 莲子 | 1 | unsupported content format: gif: 1 |
| 金钱白花蛇 | 1 | unsupported content format: gif: 1 |
| 黄芪 | 1 | unsupported content format: gif: 1 |
| 龙眼肉 | 1 | unsupported content format: gif: 1 |

## 关键类别明细

| 类别 | raw train | raw val | strict train | strict val | 纳入 strict | 跳过图 |
|---|---:|---:|---:|---:|---|---:|
| 冬虫夏草 | 84 | 19 | 83 | 19 | 是 | 1 |
| 北沙参 | 80 | 19 | 80 | 18 | 是 | 1 |
| 大腹皮 | 0 | 19 | 0 | 0 | 否 | 0 |
| 木丁香 | 176 | 19 | 174 | 19 | 是 | 2 |
| 枸杞子 | 154 | 19 | 150 | 19 | 是 | 4 |
| 桑寄生 | 80 | 19 | 80 | 18 | 是 | 1 |
| 浙贝母 | 80 | 19 | 79 | 19 | 是 | 1 |
| 淡豆豉 | 80 | 19 | 80 | 18 | 是 | 1 |
| 湖北贝母 | 89 | 19 | 88 | 19 | 是 | 1 |
| 灵芝 | 80 | 19 | 79 | 19 | 是 | 1 |
| 甘松 | 80 | 19 | 79 | 19 | 是 | 1 |
| 甘草 | 80 | 19 | 79 | 19 | 是 | 1 |
| 白前 | 80 | 19 | 80 | 18 | 是 | 1 |
| 白芍 | 80 | 19 | 78 | 19 | 是 | 2 |
| 羌活 | 80 | 19 | 80 | 18 | 是 | 1 |
| 肉豆蔻 | 83 | 19 | 82 | 19 | 是 | 1 |
| 芦根 | 80 | 19 | 79 | 19 | 是 | 1 |
| 荆芥穗 | 80 | 19 | 79 | 19 | 是 | 1 |
| 荔枝核 | 79 | 19 | 78 | 19 | 是 | 1 |
| 荜拨 | 80 | 19 | 79 | 19 | 是 | 1 |
| 莲子 | 80 | 19 | 79 | 19 | 是 | 1 |
| 金钱白花蛇 | 80 | 19 | 80 | 18 | 是 | 1 |
| 黄芪 | 86 | 19 | 85 | 19 | 是 | 1 |
| 龙眼肉 | 74 | 19 | 74 | 18 | 是 | 1 |

## 建议处理

- 为 大腹皮 补充训练样本后重建 strict 数据集，恢复完整 93 类实验。
- 保留 strict JPEG 清洗策略：跳过 GIF 伪 JPG 和损坏图，统一可读 PNG/JPEG 为 JPEG。
- 若课程要求检测指标，补充真实 YOLO bbox 标注；当前类别审计只证明分类数据一致性。
