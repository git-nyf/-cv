# 分类 train/val 泄漏人工复核包

- 来源审计: `D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_duplicate_audit.json`
- 状态: `complete_review_package`
- train/val 泄漏组: 34 / 34
- 涉及文件记录: 69，train 35 / val 34
- 同类别泄漏组: 16
- 跨类别泄漏组: 18
- 涉及类别数: 27
- 复核对照图: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\classification_train_val_leakage_contact_sheet.png`

## 边界说明

该复核包只整理 train/val 字节级 exact duplicate 风险，不自动删除、移动或重划任何图片。

## 复核建议

- 优先处理 risk_level 为 high_label_and_split_leak 的组，因为它同时涉及验证泄漏和跨类别标签冲突。
- 人工确认图片内容和类别目录后，再决定删除副本、移动样本或重建无泄漏划分。
- 完成处理后必须重新运行 duplicate audit、训练和独立验证，旧指标不能作为无泄漏基准。

## 复核清单

| group_id | risk_level | records | classes | train paths | val paths | suggested_action | manual_decision |
|---|---|---:|---|---|---|---|---|
| leak_001 | high_label_and_split_leak | 3 | 苍术、黄芩 | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_60(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_60.jpg` | `val\苍术\CangzhuCangzhuCangzhuCangzhu_59.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_002 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\谷芽\GuyaGuya54.jpg` | `val\稻芽\DaoyaDaoya19.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_003 | high_label_and_split_leak | 2 | 湖北贝母、白前 | `train\白前\BaiqianBaiqianBaiqian110.jpg` | `val\湖北贝母\Hubeibeimu17.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_004 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\谷芽\GuyaGuya49.jpg` | `val\稻芽\DaoyaDaoya20.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_005 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya54.jpg` | `val\谷芽\GuyaGuya2.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_006 | high_label_and_split_leak | 2 | 川木香、瓦楞子 | `train\川木香\ChuanmuxiangChuanmuxiang108.jpg` | `val\瓦楞子\Walengzi119.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_007 | high_label_and_split_leak | 2 | 合欢皮、川牛膝 | `train\合欢皮\HehuanpiHehuanpi48.jpg` | `val\川牛膝\ChuanniuxiChuanniuxi13.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_008 | high_label_and_split_leak | 2 | 白前、金果榄 | `train\白前\BaiqianBaiqianBaiqian92.jpg` | `val\金果榄\Jinguolan91.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_009 | high_label_and_split_leak | 2 | 石榴皮、肉豆蔻 | `train\肉豆蔻\Roudoukou100.jpg` | `val\石榴皮\Shiliupi53.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_010 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\谷芽\GuyaGuya47.jpg` | `val\稻芽\DaoyaDaoya17.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_011 | high_label_and_split_leak | 2 | 北沙参、麦冬 | `train\北沙参\BeishashenBeishashenBeishashen72.jpg` | `val\麦冬\Maidong114.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_012 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\谷芽\GuyaGuya46.jpg` | `val\稻芽\DaoyaDaoya18.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_013 | high_label_and_split_leak | 2 | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen64.jpg` | `val\芦根\Lugen5.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_014 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya29.jpg` | `val\谷芽\GuyaGuya20.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_015 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya68.jpg` | `val\谷芽\GuyaGuya7.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_016 | high_label_and_split_leak | 2 | 浙贝母、湖北贝母 | `train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_48.jpg` | `val\湖北贝母\Hubeibeimu47.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_017 | high_label_and_split_leak | 2 | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya100.jpg` | `val\谷芽\GuyaGuya9.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_018 | high_label_and_split_leak | 2 | 秦皮、苏木 | `train\秦皮\Qinpi37.jpg` | `val\苏木\Sumu39.jpg` | 先核对类别目录标签；确认真实类别后只保留正确类别样本，并从验证集移除同字节训练副本。 |  |
| leak_019 | split_leak | 2 | 荔枝核 | `train\荔枝核\Lizhihe54.jpg` | `val\荔枝核\Lizhihe79.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_020 | split_leak | 2 | 路路通 | `train\路路通\Lulutong98.jpg` | `val\路路通\Lulutong60.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_021 | split_leak | 2 | 山奈 | `train\山奈\Shannai92.jpg` | `val\山奈\Shannai80.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_022 | split_leak | 2 | 路路通 | `train\路路通\Lulutong18.jpg` | `val\路路通\Lulutong46.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_023 | split_leak | 2 | 荜澄茄 | `train\荜澄茄\BichengqieBichengqieBichengqie30.jpg` | `val\荜澄茄\BichengqieBichengqieBichengqie11.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_024 | split_leak | 2 | 郁金 | `train\郁金\Yujin90.jpg` | `val\郁金\Yujin87.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_025 | split_leak | 2 | 荆芥穗 | `train\荆芥穗\Jingjiesui69.jpg` | `val\荆芥穗\Jingjiesui46.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_026 | split_leak | 2 | 路路通 | `train\路路通\Lulutong49.jpg` | `val\路路通\Lulutong61.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_027 | split_leak | 2 | 荜澄茄 | `train\荜澄茄\BichengqieBichengqieBichengqie44.jpg` | `val\荜澄茄\BichengqieBichengqieBichengqie13.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_028 | split_leak | 2 | 荆芥穗 | `train\荆芥穗\Jingjiesui47.jpg` | `val\荆芥穗\Jingjiesui71.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_029 | split_leak | 2 | 荔枝核 | `train\荔枝核\Lizhihe76.jpg` | `val\荔枝核\Lizhihe94.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_030 | split_leak | 2 | 荆芥穗 | `train\荆芥穗\Jingjiesui56.jpg` | `val\荆芥穗\Jingjiesui75.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_031 | split_leak | 2 | 山奈 | `train\山奈\Shannai90.jpg` | `val\山奈\Shannai83.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_032 | split_leak | 2 | 竹茹 | `train\竹茹\Zhuru90.jpg` | `val\竹茹\Zhuru89.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_033 | split_leak | 2 | 路路通 | `train\路路通\Lulutong8.jpg` | `val\路路通\Lulutong33.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
| leak_034 | split_leak | 2 | 路路通 | `train\路路通\Lulutong31.jpg` | `val\路路通\Lulutong17.jpg` | 确认同一药材图片跨 train/val 后，保留一侧并重划另一侧，优先保证验证集独立。 |  |
