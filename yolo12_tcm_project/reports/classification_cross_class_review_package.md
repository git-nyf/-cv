# 分类跨类别 exact duplicate 人工复核包

- 来源审计: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_leakage_clean_candidate_duplicate_audit.json`
- 状态: `complete_review_package`
- 跨类别重复组: 34 / 34
- 涉及文件记录: 68，train 62 / val 6
- 跨划分组: 0
- train/val 泄漏组: 0
- 涉及类别数: 22
- 与参考审计共享跨类别哈希: 34
- 复核对照图: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\classification_cross_class_contact_sheet.png`

## 边界说明

该复核包只整理跨类别字节级 exact duplicate 标签冲突；不自动删除、移动、重命名或重标任何图片。

## 复核建议

- 逐组查看同 SHA256 图片在不同类别目录中的标注，确认真实药材类别。
- 若只有一个类别正确，后续应只保留正确类别样本或把错误副本移动到正确类别；若无法确认，应标记为需要专家复核。
- 完成处理后必须重新运行 duplicate audit、候选数据集检查、训练和独立验证，旧指标不能作为最终无标签冲突基准。

## 复核清单

| group_id | risk_level | records | splits | classes | paths | suggested_action | manual_decision |
|---|---|---:|---|---|---|---|---|
| cross_class_001 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya30.jpg`<br>`train\谷芽\GuyaGuya48.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_002 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya60.jpg`<br>`train\谷芽\GuyaGuya77.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_003 | label_conflict | 2 | {'val': 2} | 稻芽、谷芽 | `val\稻芽\DaoyaDaoya16.jpg`<br>`val\谷芽\GuyaGuya15.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_004 | label_conflict | 2 | {'train': 2} | 橘核、龙眼肉 | `train\橘核\Juhe99.jpg`<br>`train\龙眼肉\Longyanrou105.jpg` | 人工核对图片真实类别；若 橘核、龙眼肉 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_005 | label_conflict | 2 | {'train': 2} | 橘核、荔枝核 | `train\橘核\Juhe62.jpg`<br>`train\荔枝核\Lizhihe99.jpg` | 人工核对图片真实类别；若 橘核、荔枝核 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_006 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya42.jpg`<br>`train\谷芽\GuyaGuya45.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_007 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya31.jpg`<br>`train\谷芽\GuyaGuya50.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_008 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya96.jpg`<br>`train\谷芽\GuyaGuya90.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_009 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya51.jpg`<br>`train\谷芽\GuyaGuya70.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_010 | label_conflict | 2 | {'train': 2} | 肉豆蔻、草豆蔻 | `train\肉豆蔻\Roudoukou34.jpg`<br>`train\草豆蔻\CaodoukouCaodoukouCaodoukou43.jpg` | 人工核对图片真实类别；若 肉豆蔻、草豆蔻 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_011 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen46.jpg`<br>`train\芦根\Lugen52.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_012 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen114.jpg`<br>`train\芦根\Lugen41.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_013 | label_conflict | 2 | {'val': 2} | 甘草、黄芪 | `val\甘草\GancaoGancaoGancaoGancao_11.jpg`<br>`val\黄芪\HuangqiHuangqi1.jpg` | 人工核对图片真实类别；若 甘草、黄芪 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_014 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya23.jpg`<br>`train\谷芽\GuyaGuya106.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_015 | label_conflict | 2 | {'train': 2} | 芥子、莱菔子 | `train\芥子\Jiezi23.jpg`<br>`train\莱菔子\Laifuzi18.jpg` | 人工核对图片真实类别；若 芥子、莱菔子 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_016 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya44.jpg`<br>`train\谷芽\GuyaGuya43.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_017 | label_conflict | 2 | {'train': 2} | 五加皮、藁本 | `train\五加皮\WujiapiWujiapiWujiapiWujiapi_106.jpg`<br>`train\藁本\GaobenGaobenGaobenGaoben_90.jpg` | 人工核对图片真实类别；若 五加皮、藁本 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_018 | label_conflict | 2 | {'train': 2} | 浙贝母、湖北贝母 | `train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_21.jpg`<br>`train\湖北贝母\Hubeibeimu100.jpg` | 人工核对图片真实类别；若 浙贝母、湖北贝母 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_019 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen95.jpg`<br>`train\芦根\Lugen63.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_020 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya50.jpg`<br>`train\谷芽\GuyaGuya104.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_021 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya57.jpg`<br>`train\谷芽\GuyaGuya60.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_022 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya52.jpg`<br>`train\谷芽\GuyaGuya53.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_023 | label_conflict | 2 | {'val': 2} | 稻芽、谷芽 | `val\稻芽\DaoyaDaoya14.jpg`<br>`val\谷芽\GuyaGuya19.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_024 | label_conflict | 2 | {'train': 2} | 瓦楞子、自然铜 | `train\瓦楞子\Walengzi14.jpg`<br>`train\自然铜\Zirantong87.jpg` | 人工核对图片真实类别；若 瓦楞子、自然铜 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_025 | label_conflict | 2 | {'train': 2} | 橘核、苍术 | `train\橘核\Juhe74.jpg`<br>`train\苍术\CangzhuCangzhuCangzhuCangzhu_6.jpg` | 人工核对图片真实类别；若 橘核、苍术 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_026 | label_conflict | 2 | {'train': 2} | 橘核、荔枝核 | `train\橘核\Juhe60.jpg`<br>`train\荔枝核\Lizhihe113.jpg` | 人工核对图片真实类别；若 橘核、荔枝核 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_027 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen101.jpg`<br>`train\芦根\Lugen47.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_028 | label_conflict | 2 | {'train': 2} | 橘核、荔枝核 | `train\橘核\Juhe97.jpg`<br>`train\荔枝核\Lizhihe119.jpg` | 人工核对图片真实类别；若 橘核、荔枝核 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_029 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya38.jpg`<br>`train\谷芽\GuyaGuya58.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_030 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen62.jpg`<br>`train\芦根\Lugen95.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_031 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya102.jpg`<br>`train\谷芽\GuyaGuya107.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_032 | label_conflict | 2 | {'train': 2} | 白茅根、芦根 | `train\白茅根\BaimaogenBaimaogenBaimaogen89.jpg`<br>`train\芦根\Lugen97.jpg` | 人工核对图片真实类别；若 白茅根、芦根 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_033 | label_conflict | 2 | {'train': 2} | 稻芽、谷芽 | `train\稻芽\DaoyaDaoya85.jpg`<br>`train\谷芽\GuyaGuya38.jpg` | 人工核对图片真实类别；若 稻芽、谷芽 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
| cross_class_034 | label_conflict | 2 | {'train': 2} | 北沙参、麦冬 | `train\北沙参\BeishashenBeishashenBeishashen64.jpg`<br>`train\麦冬\Maidong112.jpg` | 人工核对图片真实类别；若 北沙参、麦冬 中只有一个正确目录，保留正确类别样本并移除或重标其他副本。 |  |
