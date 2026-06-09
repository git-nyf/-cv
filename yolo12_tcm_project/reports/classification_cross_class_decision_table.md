# 分类跨类别标签冲突决策表

- 来源复核包: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_review_package.json`
- 状态: `ready_for_manual_decision`
- 待决策组: 34 / 34
- 已决策组: 0
- 需专家复核组: 0
- 延后处理组: 0
- 校验错误: 0
- CSV 填写表: `D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_table.csv`

## 边界说明

本决策表只把跨类别 exact duplicate 复核结果整理为可填写输入；默认不自动删除、移动、重命名、重标或复制任何图片。

## 填写字段

| 字段 | 说明 |
|---|---|
| decision_status | pending / decided / needs_expert_review / defer |
| chosen_class | 确认后的真实类别；涉及保留或移动到某一类别时必填 |
| action | keep_chosen_class_remove_others / move_all_to_chosen_class / keep_all_as_is / remove_all_uncertain / needs_expert_review |
| remove_relative_paths | 需要移除的相对路径，多个路径用分号分隔 |
| move_to_class | 需要统一移动到的类别；没有移动动作时留空 |
| reviewer / reviewed_at / decision_note | 复核人、日期和证据说明 |

## 决策清单

| group_id | classes | records | paths | decision_status | action | chosen_class | note |
|---|---|---:|---|---|---|---|---|
| cross_class_001 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya30.jpg`<br>`train\谷芽\GuyaGuya48.jpg` | pending |  |  |  |
| cross_class_002 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya60.jpg`<br>`train\谷芽\GuyaGuya77.jpg` | pending |  |  |  |
| cross_class_003 | 稻芽、谷芽 | 2 | `val\稻芽\DaoyaDaoya16.jpg`<br>`val\谷芽\GuyaGuya15.jpg` | pending |  |  |  |
| cross_class_004 | 橘核、龙眼肉 | 2 | `train\橘核\Juhe99.jpg`<br>`train\龙眼肉\Longyanrou105.jpg` | pending |  |  |  |
| cross_class_005 | 橘核、荔枝核 | 2 | `train\橘核\Juhe62.jpg`<br>`train\荔枝核\Lizhihe99.jpg` | pending |  |  |  |
| cross_class_006 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya42.jpg`<br>`train\谷芽\GuyaGuya45.jpg` | pending |  |  |  |
| cross_class_007 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya31.jpg`<br>`train\谷芽\GuyaGuya50.jpg` | pending |  |  |  |
| cross_class_008 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya96.jpg`<br>`train\谷芽\GuyaGuya90.jpg` | pending |  |  |  |
| cross_class_009 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya51.jpg`<br>`train\谷芽\GuyaGuya70.jpg` | pending |  |  |  |
| cross_class_010 | 肉豆蔻、草豆蔻 | 2 | `train\肉豆蔻\Roudoukou34.jpg`<br>`train\草豆蔻\CaodoukouCaodoukouCaodoukou43.jpg` | pending |  |  |  |
| cross_class_011 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen46.jpg`<br>`train\芦根\Lugen52.jpg` | pending |  |  |  |
| cross_class_012 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen114.jpg`<br>`train\芦根\Lugen41.jpg` | pending |  |  |  |
| cross_class_013 | 甘草、黄芪 | 2 | `val\甘草\GancaoGancaoGancaoGancao_11.jpg`<br>`val\黄芪\HuangqiHuangqi1.jpg` | pending |  |  |  |
| cross_class_014 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya23.jpg`<br>`train\谷芽\GuyaGuya106.jpg` | pending |  |  |  |
| cross_class_015 | 芥子、莱菔子 | 2 | `train\芥子\Jiezi23.jpg`<br>`train\莱菔子\Laifuzi18.jpg` | pending |  |  |  |
| cross_class_016 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya44.jpg`<br>`train\谷芽\GuyaGuya43.jpg` | pending |  |  |  |
| cross_class_017 | 五加皮、藁本 | 2 | `train\五加皮\WujiapiWujiapiWujiapiWujiapi_106.jpg`<br>`train\藁本\GaobenGaobenGaobenGaoben_90.jpg` | pending |  |  |  |
| cross_class_018 | 浙贝母、湖北贝母 | 2 | `train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_21.jpg`<br>`train\湖北贝母\Hubeibeimu100.jpg` | pending |  |  |  |
| cross_class_019 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen95.jpg`<br>`train\芦根\Lugen63.jpg` | pending |  |  |  |
| cross_class_020 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya50.jpg`<br>`train\谷芽\GuyaGuya104.jpg` | pending |  |  |  |
| cross_class_021 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya57.jpg`<br>`train\谷芽\GuyaGuya60.jpg` | pending |  |  |  |
| cross_class_022 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya52.jpg`<br>`train\谷芽\GuyaGuya53.jpg` | pending |  |  |  |
| cross_class_023 | 稻芽、谷芽 | 2 | `val\稻芽\DaoyaDaoya14.jpg`<br>`val\谷芽\GuyaGuya19.jpg` | pending |  |  |  |
| cross_class_024 | 瓦楞子、自然铜 | 2 | `train\瓦楞子\Walengzi14.jpg`<br>`train\自然铜\Zirantong87.jpg` | pending |  |  |  |
| cross_class_025 | 橘核、苍术 | 2 | `train\橘核\Juhe74.jpg`<br>`train\苍术\CangzhuCangzhuCangzhuCangzhu_6.jpg` | pending |  |  |  |
| cross_class_026 | 橘核、荔枝核 | 2 | `train\橘核\Juhe60.jpg`<br>`train\荔枝核\Lizhihe113.jpg` | pending |  |  |  |
| cross_class_027 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen101.jpg`<br>`train\芦根\Lugen47.jpg` | pending |  |  |  |
| cross_class_028 | 橘核、荔枝核 | 2 | `train\橘核\Juhe97.jpg`<br>`train\荔枝核\Lizhihe119.jpg` | pending |  |  |  |
| cross_class_029 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya38.jpg`<br>`train\谷芽\GuyaGuya58.jpg` | pending |  |  |  |
| cross_class_030 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen62.jpg`<br>`train\芦根\Lugen95.jpg` | pending |  |  |  |
| cross_class_031 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya102.jpg`<br>`train\谷芽\GuyaGuya107.jpg` | pending |  |  |  |
| cross_class_032 | 白茅根、芦根 | 2 | `train\白茅根\BaimaogenBaimaogenBaimaogen89.jpg`<br>`train\芦根\Lugen97.jpg` | pending |  |  |  |
| cross_class_033 | 稻芽、谷芽 | 2 | `train\稻芽\DaoyaDaoya85.jpg`<br>`train\谷芽\GuyaGuya38.jpg` | pending |  |  |  |
| cross_class_034 | 北沙参、麦冬 | 2 | `train\北沙参\BeishashenBeishashenBeishashen64.jpg`<br>`train\麦冬\Maidong112.jpg` | pending |  |  |  |
