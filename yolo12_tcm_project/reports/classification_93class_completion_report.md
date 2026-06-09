# 93 类补齐分类数据集报告

- 来源: `D:\AAA中药cv\data`
- 输出: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class`
- JPEG 质量: 95
- 单侧类别验证比例: 0.2

## 总览

- 状态: `complete`
- 原始类别: 93；输出类别: 93
- 图片: train 7841 / val 1745 / total 9586
- 跳过图片: 28
- 重划类别: 大腹皮
- val-only 重划类别: 大腹皮
- train-only 重划类别: 无
- 排除类别: 无
- 操作统计: {'convert_to_jpeg': 122, 'copy_jpeg': 9464}
- 内容格式: {'jpeg': 9464, 'png': 122}

## 划分策略

| 类别 | 策略 | raw train | raw val | assigned train | assigned val |
|---|---|---:|---:|---:|---:|
| 大腹皮 | rebalance_val_only | 0 | 19 | 15 | 4 |

## 跳过文件

- [train/冬虫夏草/preserve_raw_split] `D:\AAA中药cv\data\train\冬虫夏草\DongchongxiacaoDongchongxiacao92.jpg`: unsupported content format: gif
- [val/北沙参/preserve_raw_split] `D:\AAA中药cv\data\val\北沙参\BeishashenBeishashenBeishashen19.jpg`: unsupported content format: gif
- [train/木丁香/preserve_raw_split] `D:\AAA中药cv\data\train\木丁香\Mudingxiang36(1).jpg`: unsupported content format: gif
- [train/木丁香/preserve_raw_split] `D:\AAA中药cv\data\train\木丁香\Mudingxiang36.jpg`: unsupported content format: gif
- [train/枸杞子/preserve_raw_split] `D:\AAA中药cv\data\train\枸杞子\GouqiziGouqizi103(1).jpg`: unsupported content format: gif
- [train/枸杞子/preserve_raw_split] `D:\AAA中药cv\data\train\枸杞子\GouqiziGouqizi103.jpg`: unsupported content format: gif
- [train/枸杞子/preserve_raw_split] `D:\AAA中药cv\data\train\枸杞子\GouqiziGouqizi53(1).jpg`: unsupported content format: gif
- [train/枸杞子/preserve_raw_split] `D:\AAA中药cv\data\train\枸杞子\GouqiziGouqizi53.jpg`: unsupported content format: gif
- [val/桑寄生/preserve_raw_split] `D:\AAA中药cv\data\val\桑寄生\SangjishengSangjishengSangjishengIMG_20200724_180506.jpg`: broken data stream when reading image file
- [train/浙贝母/preserve_raw_split] `D:\AAA中药cv\data\train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_103.jpg`: unsupported content format: gif
- [val/淡豆豉/preserve_raw_split] `D:\AAA中药cv\data\val\淡豆豉\DandouchiDandouchi20.jpg`: unsupported content format: gif
- [train/湖北贝母/preserve_raw_split] `D:\AAA中药cv\data\train\湖北贝母\Hubeibeimu18.jpg`: unsupported content format: gif
- [train/灵芝/preserve_raw_split] `D:\AAA中药cv\data\train\灵芝\Lingzhi84.jpg`: unsupported content format: gif
- [train/甘松/preserve_raw_split] `D:\AAA中药cv\data\train\甘松\GansongGansong95.jpg`: unsupported content format: gif
- [train/甘草/preserve_raw_split] `D:\AAA中药cv\data\train\甘草\GancaoGancaoGancaoGancao_32.jpg`: unsupported content format: gif
- [val/白前/preserve_raw_split] `D:\AAA中药cv\data\val\白前\BaiqianBaiqianBaiqian10.jpg`: unsupported content format: gif
- [train/白芍/preserve_raw_split] `D:\AAA中药cv\data\train\白芍\BaishaoBaishaoBaishaoIMG_20200724_180221.jpg`: broken data stream when reading image file
- [train/白芍/preserve_raw_split] `D:\AAA中药cv\data\train\白芍\BaishaoBaishaoBaishaoIMG_20200724_180244.jpg`: broken data stream when reading image file
- [val/羌活/preserve_raw_split] `D:\AAA中药cv\data\val\羌活\QianghuoQianghuoQianghuoQianghuo_10.jpg`: unsupported content format: gif
- [train/肉豆蔻/preserve_raw_split] `D:\AAA中药cv\data\train\肉豆蔻\Roudoukou86.jpg`: unsupported content format: gif
- [train/芦根/preserve_raw_split] `D:\AAA中药cv\data\train\芦根\Lugen106.jpg`: unsupported content format: gif
- [train/荆芥穗/preserve_raw_split] `D:\AAA中药cv\data\train\荆芥穗\Jingjiesui26.jpg`: unsupported content format: gif
- [train/荔枝核/preserve_raw_split] `D:\AAA中药cv\data\train\荔枝核\Lizhihe104.jpg`: unsupported content format: gif
- [train/荜拨/preserve_raw_split] `D:\AAA中药cv\data\train\荜拨\BiboBiboBibo25.jpg`: unsupported content format: gif
- [train/莲子/preserve_raw_split] `D:\AAA中药cv\data\train\莲子\Lianzi15.jpg`: unsupported content format: gif
- [val/金钱白花蛇/preserve_raw_split] `D:\AAA中药cv\data\val\金钱白花蛇\Jinqianbaihuashe114.jpg`: unsupported content format: gif
- [train/黄芪/preserve_raw_split] `D:\AAA中药cv\data\train\黄芪\HuangqiHuangqi66.jpg`: unsupported content format: gif
- [val/龙眼肉/preserve_raw_split] `D:\AAA中药cv\data\val\龙眼肉\Longyanrou80.jpg`: unsupported content format: gif

## 边界说明

- 该数据集用于 93 类覆盖补齐实验。原始 train/val 均存在的类别保留原始划分；仅单侧存在的类别按确定性顺序重划 train/val，因此其结果不应与原始 92 类 strict 基准直接等价比较。
