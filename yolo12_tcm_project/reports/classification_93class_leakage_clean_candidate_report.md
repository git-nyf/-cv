# 分类数据 train/val 泄漏候选清理报告

- 源数据集: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class`
- 输出数据集: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class_leakage_clean_candidate`
- 复核包: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_leakage_review_package.json`
- 状态: `leakage_val_duplicates_removed`
- 策略: `copy_all_except_val_exact_duplicates_from_review_package`
- 源图片: 9586
- 输出图片: 9552
- 移除图片: 34 / 请求移除 34
- 类别数: 93
- 源划分: {'train': 7841, 'val': 1745}
- 输出划分: {'train': 7841, 'val': 1711}
- 移除划分: {'val': 34}

## 边界说明

本候选数据集只移除人工复核包中列出的 val 侧字节级 train/val 重复副本；不自动修改 train 图像、不自动裁决跨类别标签，也不替代人工类别复核。

## 建议后续动作

- 对输出数据集重新运行 exact duplicate 审计，确认 train/val 泄漏组归零。
- 基于该候选数据集重新训练与独立验证，指标不得与旧泄漏数据集直接等价比较。
- 跨类别 exact duplicate 仍需结合 contact sheet 和原始图像人工确认真实类别。

## 已移除 val 副本

| split | class | filename | relative_path | bytes |
|---|---|---|---|---:|
| val | 山奈 | Shannai80.jpg | `val\山奈\Shannai80.jpg` | 48761 |
| val | 山奈 | Shannai83.jpg | `val\山奈\Shannai83.jpg` | 40317 |
| val | 川牛膝 | ChuanniuxiChuanniuxi13.jpg | `val\川牛膝\ChuanniuxiChuanniuxi13.jpg` | 51994 |
| val | 湖北贝母 | Hubeibeimu17.jpg | `val\湖北贝母\Hubeibeimu17.jpg` | 39583 |
| val | 湖北贝母 | Hubeibeimu47.jpg | `val\湖北贝母\Hubeibeimu47.jpg` | 33779 |
| val | 瓦楞子 | Walengzi119.jpg | `val\瓦楞子\Walengzi119.jpg` | 64754 |
| val | 石榴皮 | Shiliupi53.jpg | `val\石榴皮\Shiliupi53.jpg` | 43881 |
| val | 稻芽 | DaoyaDaoya17.jpg | `val\稻芽\DaoyaDaoya17.jpg` | 78261 |
| val | 稻芽 | DaoyaDaoya18.jpg | `val\稻芽\DaoyaDaoya18.jpg` | 79537 |
| val | 稻芽 | DaoyaDaoya19.jpg | `val\稻芽\DaoyaDaoya19.jpg` | 19668 |
| val | 稻芽 | DaoyaDaoya20.jpg | `val\稻芽\DaoyaDaoya20.jpg` | 49445 |
| val | 竹茹 | Zhuru89.jpg | `val\竹茹\Zhuru89.jpg` | 28218 |
| val | 芦根 | Lugen5.jpg | `val\芦根\Lugen5.jpg` | 63942 |
| val | 苍术 | CangzhuCangzhuCangzhuCangzhu_59.jpg | `val\苍术\CangzhuCangzhuCangzhuCangzhu_59.jpg` | 36098 |
| val | 苏木 | Sumu39.jpg | `val\苏木\Sumu39.jpg` | 42403 |
| val | 荆芥穗 | Jingjiesui46.jpg | `val\荆芥穗\Jingjiesui46.jpg` | 27658 |
| val | 荆芥穗 | Jingjiesui71.jpg | `val\荆芥穗\Jingjiesui71.jpg` | 56215 |
| val | 荆芥穗 | Jingjiesui75.jpg | `val\荆芥穗\Jingjiesui75.jpg` | 47594 |
| val | 荔枝核 | Lizhihe79.jpg | `val\荔枝核\Lizhihe79.jpg` | 51359 |
| val | 荔枝核 | Lizhihe94.jpg | `val\荔枝核\Lizhihe94.jpg` | 12320 |
| val | 荜澄茄 | BichengqieBichengqieBichengqie11.jpg | `val\荜澄茄\BichengqieBichengqieBichengqie11.jpg` | 51117 |
| val | 荜澄茄 | BichengqieBichengqieBichengqie13.jpg | `val\荜澄茄\BichengqieBichengqieBichengqie13.jpg` | 90902 |
| val | 谷芽 | GuyaGuya2.jpg | `val\谷芽\GuyaGuya2.jpg` | 51581 |
| val | 谷芽 | GuyaGuya20.jpg | `val\谷芽\GuyaGuya20.jpg` | 57107 |
| val | 谷芽 | GuyaGuya7.jpg | `val\谷芽\GuyaGuya7.jpg` | 82698 |
| val | 谷芽 | GuyaGuya9.jpg | `val\谷芽\GuyaGuya9.jpg` | 57387 |
| val | 路路通 | Lulutong17.jpg | `val\路路通\Lulutong17.jpg` | 42052 |
| val | 路路通 | Lulutong33.jpg | `val\路路通\Lulutong33.jpg` | 54046 |
| val | 路路通 | Lulutong46.jpg | `val\路路通\Lulutong46.jpg` | 69551 |
| val | 路路通 | Lulutong60.jpg | `val\路路通\Lulutong60.jpg` | 46621 |
| val | 路路通 | Lulutong61.jpg | `val\路路通\Lulutong61.jpg` | 57669 |
| val | 郁金 | Yujin87.jpg | `val\郁金\Yujin87.jpg` | 59441 |
| val | 金果榄 | Jinguolan91.jpg | `val\金果榄\Jinguolan91.jpg` | 39514 |
| val | 麦冬 | Maidong114.jpg | `val\麦冬\Maidong114.jpg` | 49949 |
