# strict 分类误判与每类表现分析

- 模型: `D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_cpu_5e\weights\best.pt`
- 数据: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val`
- 图像数: 1741
- 类别数: 92
- Top-1 Accuracy: 0.1769098219
- Top-5 Accuracy: 0.4956921310

## Top-1 最低类别

| 类别 | 样本数 | Top-1 | Top-5 | 最常预测为 |
|---|---:|---:|---:|---|
| 地龙 | 19 | 0.0000 | 0.0000 | 木丁香(5)，路路通(4)，川牛膝(3) |
| 安息香 | 19 | 0.0000 | 0.0000 | 干姜(3)，肉豆蔻(3)，木丁香(3) |
| 瓦楞子 | 19 | 0.0000 | 0.0000 | 干姜(5)，川牛膝(3)，甘松(3) |
| 北沙参 | 18 | 0.0000 | 0.0000 | 薏苡仁(6)，川牛膝(4)，谷芽(2) |
| 全蝎 | 19 | 0.0000 | 0.0526 | 川牛膝(3)，甘松(3)，芥子(2) |
| 白芍 | 19 | 0.0000 | 0.0526 | 苍术(5)，干姜(3)，木丁香(2) |
| 草豆蔻 | 19 | 0.0000 | 0.0526 | 干姜(5)，川牛膝(4)，肉豆蔻(3) |
| 白前 | 18 | 0.0000 | 0.0556 | 芥子(6)，谷芽(3)，莱菔子(3) |
| 丝瓜络 | 19 | 0.0000 | 0.1053 | 干姜(8)，川牛膝(3)，湖北贝母(1) |
| 五加皮 | 19 | 0.0000 | 0.1053 | 细辛(4)，川牛膝(3)，肉豆蔻(3) |
| 秦皮 | 19 | 0.0000 | 0.1053 | 川牛膝(6)，木丁香(4)，甘松(2) |
| 自然铜 | 19 | 0.0000 | 0.1053 | 木丁香(6)，莱菔子(2)，芥子(1) |
| 芦根 | 19 | 0.0000 | 0.1053 | 川牛膝(5)，干姜(4)，谷芽(2) |
| 蜂房 | 19 | 0.0000 | 0.1053 | 甘松(4)，芥子(3)，路路通(3) |
| 防风 | 19 | 0.0000 | 0.1053 | 白芷(8)，芥子(2)，甘松(2) |

## Top-1 最高类别

| 类别 | 样本数 | Top-1 | Top-5 | 最常预测为 |
|---|---:|---:|---:|---|
| 枸杞子 | 19 | 1.0000 | 1.0000 | 枸杞子(19) |
| 莲子心 | 19 | 1.0000 | 1.0000 | 莲子心(19) |
| 鸡冠花 | 19 | 0.9474 | 1.0000 | 鸡冠花(18)，白矾(1) |
| 白矾 | 19 | 0.8421 | 1.0000 | 白矾(16)，白芷(2)，木丁香(1) |
| 芥子 | 19 | 0.7895 | 1.0000 | 芥子(15)，谷芽(2)，莱菔子(1) |
| 酸枣仁 | 19 | 0.7368 | 1.0000 | 酸枣仁(14)，枸杞子(5) |
| 番泻叶 | 19 | 0.7368 | 0.8947 | 番泻叶(14)，莲子心(2)，荆芥穗(1) |
| 干姜 | 19 | 0.7368 | 0.8421 | 干姜(14)，麦冬(1)，白芷(1) |
| 木丁香 | 19 | 0.7368 | 0.8421 | 木丁香(14)，路路通(2)，肉豆蔻(1) |
| 苏木 | 19 | 0.7368 | 0.8421 | 苏木(14)，鸡内金(1)，苍术(1) |
| 薏苡仁 | 19 | 0.6842 | 0.7895 | 薏苡仁(13)，干姜(2)，谷芽(2) |
| 黄柏 | 19 | 0.6316 | 0.6316 | 黄柏(12)，芥子(4)，土荆皮(1) |
| 细辛 | 19 | 0.5263 | 0.9474 | 细辛(10)，芥子(3)，莱菔子(3) |
| 路路通 | 19 | 0.4737 | 0.8421 | 路路通(9)，木丁香(3)，莱菔子(3) |
| 荔枝核 | 19 | 0.4737 | 0.7368 | 荔枝核(9)，酸枣仁(3)，木丁香(2) |

## 高频混淆对

| 真实类别 | 预测类别 | 次数 |
|---|---|---:|
| 九香虫 | 木丁香 | 12 |
| 合欢皮 | 川牛膝 | 12 |
| 柏子仁 | 芥子 | 12 |
| 荜澄茄 | 木丁香 | 12 |
| 山茱萸 | 枸杞子 | 11 |
| 浙贝母 | 白芷 | 11 |
| 莲子 | 薏苡仁 | 11 |
| 谷芽 | 芥子 | 11 |
| 山慈菇 | 川牛膝 | 10 |
| 桂枝 | 细辛 | 10 |
| 槟榔 | 细辛 | 10 |
| 荜拨 | 木丁香 | 10 |
| 山奈 | 干姜 | 9 |
| 稻芽 | 芥子 | 9 |
| 肉豆蔻 | 干姜 | 9 |
| 丝瓜络 | 干姜 | 8 |
| 川木香 | 川牛膝 | 8 |
| 桑螵蛸 | 木丁香 | 8 |
| 橘核 | 薏苡仁 | 8 |
| 羌活 | 白芷 | 8 |

## 典型误判样例

| 图片 | 真实类别 | Top-1 | 置信度 | Top-5 含真实类别 |
|---|---|---|---:|---|
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo117.jpg` | 丝瓜络 | 干姜 | 0.0926 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo15.jpg` | 丝瓜络 | 干姜 | 0.1149 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo16.jpg` | 丝瓜络 | 干姜 | 0.1363 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo18.jpg` | 丝瓜络 | 湖北贝母 | 0.1044 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo21.jpg` | 丝瓜络 | 干姜 | 0.1885 | 是 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo25.jpg` | 丝瓜络 | 干姜 | 0.1564 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo29.jpg` | 丝瓜络 | 干姜 | 0.2551 | 是 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo30.jpg` | 丝瓜络 | 芥子 | 0.1734 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo41.jpg` | 丝瓜络 | 川牛膝 | 0.1025 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo61.jpg` | 丝瓜络 | 干姜 | 0.0927 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo67.jpg` | 丝瓜络 | 川牛膝 | 0.0394 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo70.jpg` | 丝瓜络 | 谷芽 | 0.0938 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo74.jpg` | 丝瓜络 | 干姜 | 0.2121 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo8.jpg` | 丝瓜络 | 川牛膝 | 0.0972 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo80.jpg` | 丝瓜络 | 莱菔子 | 0.0622 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo82.jpg` | 丝瓜络 | 川楝子 | 0.0752 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo87.jpg` | 丝瓜络 | 番泻叶 | 0.1318 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo90.jpg` | 丝瓜络 | 太子参 | 0.1234 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\丝瓜络\Sigualuo92.jpg` | 丝瓜络 | 白矾 | 0.0941 | 否 |
| `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\九香虫\Jiuxiangchong1.jpg` | 九香虫 | 木丁香 | 0.3284 | 是 |

## 解读

- 该分析基于 strict 验证集逐图推理，适合解释当前 5 epoch CPU 短训模型的分类误差。
- 若某类 Top-1 低但 Top-5 较高，说明模型已把真实类别排进候选但排序能力不足，后续可通过更长训练、预训练权重和相似类增强改善。
- 若某类长期被同一类别吸收，需要优先检查两类图像是否存在外观相似、目录混入、拍摄条件差异或标注命名不一致。
- 该分析仍是分类评估，不能替代目标检测 mAP 或 bbox 定位误差分析。
