# strict 分类人工复核样例清单

- 来源分析: `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_error_analysis.json`
- 高频混淆样例图: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\strict_confusion_contact_sheet.png`
- 低表现类别样例图: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\strict_worst_class_contact_sheet.png`

## 复核目的

这些样例用于人工检查目录混入、外观相似、拍摄条件差异、标注命名不一致等数据质量问题。该材料不代表新模型性能，只为后续补样和清洗排序。

## 高频混淆复核样例

| 真实类别 | 预测类别 | 置信度 | Top-5 含真实类别 | 图片 |
|---|---|---:|---|---|
| 九香虫 | 木丁香 | 0.3284 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\九香虫\Jiuxiangchong1.jpg` |
| 九香虫 | 木丁香 | 0.0989 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\九香虫\Jiuxiangchong105.jpg` |
| 九香虫 | 木丁香 | 0.2835 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\九香虫\Jiuxiangchong25.jpg` |
| 合欢皮 | 川牛膝 | 0.0981 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\合欢皮\HehuanpiHehuanpi10.jpg` |
| 合欢皮 | 川牛膝 | 0.0696 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\合欢皮\HehuanpiHehuanpi11.jpg` |
| 合欢皮 | 川牛膝 | 0.0627 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\合欢皮\HehuanpiHehuanpi12.jpg` |
| 柏子仁 | 芥子 | 0.1074 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\柏子仁\BaizirenBaizirenBaiziren1.jpg` |
| 柏子仁 | 芥子 | 0.4252 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\柏子仁\BaizirenBaizirenBaiziren10.jpg` |
| 柏子仁 | 芥子 | 0.3969 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\柏子仁\BaizirenBaizirenBaiziren11.jpg` |
| 荜澄茄 | 木丁香 | 0.4029 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\荜澄茄\BichengqieBichengqieBichengqie1.jpg` |
| 荜澄茄 | 木丁香 | 0.0941 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\荜澄茄\BichengqieBichengqieBichengqie10.jpg` |
| 荜澄茄 | 木丁香 | 0.2158 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\荜澄茄\BichengqieBichengqieBichengqie11.jpg` |
| 山茱萸 | 枸杞子 | 0.4462 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\山茱萸\Shanzhuyu114.jpg` |
| 山茱萸 | 枸杞子 | 0.8209 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\山茱萸\Shanzhuyu19.jpg` |
| 山茱萸 | 枸杞子 | 0.7281 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\山茱萸\Shanzhuyu4.jpg` |
| 浙贝母 | 白芷 | 0.3853 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\浙贝母\ZhebeimuZhebeimuZhebeimuIMG_20200722_171210.jpg` |
| 浙贝母 | 白芷 | 0.3738 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\浙贝母\ZhebeimuZhebeimuZhebeimuIMG_20200722_171210_1.jpg` |
| 浙贝母 | 白芷 | 0.2927 | 是 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\浙贝母\ZhebeimuZhebeimuZhebeimuIMG_20200722_171211.jpg` |

## 低表现类别复核样例

| 真实类别 | 预测类别 | 置信度 | Top-5 含真实类别 | 图片 |
|---|---|---:|---|---|
| 地龙 | 白芷 | 0.3254 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\地龙\DilongDilong1.jpg` |
| 地龙 | 木丁香 | 0.2178 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\地龙\DilongDilong10.jpg` |
| 地龙 | 川牛膝 | 0.0476 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\地龙\DilongDilong11.jpg` |
| 安息香 | 干姜 | 0.1182 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\安息香\AnxixiangAnxixiangAnxixiang1.jpg` |
| 安息香 | 肉豆蔻 | 0.0760 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\安息香\AnxixiangAnxixiangAnxixiang10.jpg` |
| 安息香 | 土荆皮 | 0.0530 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\安息香\AnxixiangAnxixiangAnxixiang11.jpg` |
| 瓦楞子 | 湖北贝母 | 0.1424 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\瓦楞子\Walengzi114.jpg` |
| 瓦楞子 | 干姜 | 0.1113 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\瓦楞子\Walengzi119.jpg` |
| 瓦楞子 | 川牛膝 | 0.0775 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\瓦楞子\Walengzi21.jpg` |
| 北沙参 | 谷芽 | 0.1619 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\北沙参\BeishashenBeishashenBeishashen1.jpg` |
| 北沙参 | 黄芩 | 0.0444 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\北沙参\BeishashenBeishashenBeishashen10.jpg` |
| 北沙参 | 川牛膝 | 0.0901 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\北沙参\BeishashenBeishashenBeishashen11.jpg` |
| 全蝎 | 芥子 | 0.1320 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\全蝎\Quanxie13.jpg` |
| 全蝎 | 川牛膝 | 0.0602 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\全蝎\Quanxie17.jpg` |
| 全蝎 | 干姜 | 0.0533 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\全蝎\Quanxie26.jpg` |
| 白芍 | 干姜 | 0.0643 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\白芍\BaishaoBaishaoBaishaoBaishao_106.jpg` |
| 白芍 | 肉豆蔻 | 0.1414 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\白芍\BaishaoBaishaoBaishaoBaishao_109.jpg` |
| 白芍 | 薏苡仁 | 0.3776 | 否 | `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\白芍\BaishaoBaishaoBaishaoBaishao_110.jpg` |

## 建议处理

- 优先人工打开 contact sheet 中高频混淆对，判断是否存在目录混入或类别外观高度重叠。
- 对 Top-1 为 0 且 Top-5 也低的类别，优先补充训练样本或检查验证样本来源。
- 若两类长期互相混淆且人工也难区分，应在报告中明确相似类别风险，必要时设计合并/细分标签对照实验。
- 若课程要求目标检测，本材料只能作为分类数据清洗依据，仍需真实 bbox 标注。
