# 分类数据重复与泄漏审计报告

- 数据路径: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class`
- 状态: `needs_leakage_review`
- 总图片: 9586
- 唯一 SHA256: 9033
- 重复 SHA256 组: 546
- 重复图片数: 1099，额外重复图: 553
- 跨划分重复组: 34
- train/val 泄漏组: 34
- 跨类别重复组: 52

## 边界说明

该审计只检查文件字节级 SHA256 完全重复；不包含近似重复、裁剪相似或感知哈希判断。

## 建议动作

- 优先人工复核 train/val exact duplicate，避免验证集泄漏导致指标偏乐观。
- 若同一 SHA256 跨类别出现，优先检查目录标签是否混入或类别命名是否冲突。
- 确认后再删除或重划样本；不要仅凭本报告自动删图。

## 重复组样例

| SHA256 | count | splits | classes | train/val leak | paths |
|---|---:|---|---|---|---|
| `e8ec1480e293cc8e...` | 3 | train, val | 苍术, 黄芩 | True | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_60(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_60.jpg`<br>`val\苍术\CangzhuCangzhuCangzhuCangzhu_59.jpg` |
| `0163d12c17a4be39...` | 2 | train, val | 稻芽, 谷芽 | True | `train\谷芽\GuyaGuya54.jpg`<br>`val\稻芽\DaoyaDaoya19.jpg` |
| `0b4c4ca0209b329e...` | 2 | train, val | 湖北贝母, 白前 | True | `train\白前\BaiqianBaiqianBaiqian110.jpg`<br>`val\湖北贝母\Hubeibeimu17.jpg` |
| `2ca364e9c60a46cd...` | 2 | train, val | 稻芽, 谷芽 | True | `train\谷芽\GuyaGuya49.jpg`<br>`val\稻芽\DaoyaDaoya20.jpg` |
| `34855067dee8b1f1...` | 2 | train, val | 稻芽, 谷芽 | True | `train\稻芽\DaoyaDaoya54.jpg`<br>`val\谷芽\GuyaGuya2.jpg` |
| `384cc040bd976038...` | 2 | train, val | 川木香, 瓦楞子 | True | `train\川木香\ChuanmuxiangChuanmuxiang108.jpg`<br>`val\瓦楞子\Walengzi119.jpg` |
| `448aa866aff27437...` | 2 | train, val | 合欢皮, 川牛膝 | True | `train\合欢皮\HehuanpiHehuanpi48.jpg`<br>`val\川牛膝\ChuanniuxiChuanniuxi13.jpg` |
| `455bc1c3ba114097...` | 2 | train, val | 白前, 金果榄 | True | `train\白前\BaiqianBaiqianBaiqian92.jpg`<br>`val\金果榄\Jinguolan91.jpg` |
| `4f73e09710638667...` | 2 | train, val | 石榴皮, 肉豆蔻 | True | `train\肉豆蔻\Roudoukou100.jpg`<br>`val\石榴皮\Shiliupi53.jpg` |
| `56f83639e5355641...` | 2 | train, val | 稻芽, 谷芽 | True | `train\谷芽\GuyaGuya47.jpg`<br>`val\稻芽\DaoyaDaoya17.jpg` |
| `7c569f8c12cbd590...` | 2 | train, val | 北沙参, 麦冬 | True | `train\北沙参\BeishashenBeishashenBeishashen72.jpg`<br>`val\麦冬\Maidong114.jpg` |
| `953b2ccdf7e305a4...` | 2 | train, val | 稻芽, 谷芽 | True | `train\谷芽\GuyaGuya46.jpg`<br>`val\稻芽\DaoyaDaoya18.jpg` |
| `d2f746a1b0f43ba2...` | 2 | train, val | 白茅根, 芦根 | True | `train\白茅根\BaimaogenBaimaogenBaimaogen64.jpg`<br>`val\芦根\Lugen5.jpg` |
| `da6c0882f1f93f72...` | 2 | train, val | 稻芽, 谷芽 | True | `train\稻芽\DaoyaDaoya29.jpg`<br>`val\谷芽\GuyaGuya20.jpg` |
| `e1082018a3bf412b...` | 2 | train, val | 稻芽, 谷芽 | True | `train\稻芽\DaoyaDaoya68.jpg`<br>`val\谷芽\GuyaGuya7.jpg` |
| `ed0a2e918604c317...` | 2 | train, val | 浙贝母, 湖北贝母 | True | `train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_48.jpg`<br>`val\湖北贝母\Hubeibeimu47.jpg` |
| `f4bc220bcef2256f...` | 2 | train, val | 稻芽, 谷芽 | True | `train\稻芽\DaoyaDaoya100.jpg`<br>`val\谷芽\GuyaGuya9.jpg` |
| `f7350e26b0baa70e...` | 2 | train, val | 秦皮, 苏木 | True | `train\秦皮\Qinpi37.jpg`<br>`val\苏木\Sumu39.jpg` |
| `1396eeb2cb69a8dd...` | 2 | train, val | 荔枝核 | True | `train\荔枝核\Lizhihe54.jpg`<br>`val\荔枝核\Lizhihe79.jpg` |
| `15603309f94d6a33...` | 2 | train, val | 路路通 | True | `train\路路通\Lulutong98.jpg`<br>`val\路路通\Lulutong60.jpg` |
| `1e0164df7cd5761e...` | 2 | train, val | 山奈 | True | `train\山奈\Shannai92.jpg`<br>`val\山奈\Shannai80.jpg` |
| `33c44f205ca4aafc...` | 2 | train, val | 路路通 | True | `train\路路通\Lulutong18.jpg`<br>`val\路路通\Lulutong46.jpg` |
| `369578c5d404dac3...` | 2 | train, val | 荜澄茄 | True | `train\荜澄茄\BichengqieBichengqieBichengqie30.jpg`<br>`val\荜澄茄\BichengqieBichengqieBichengqie11.jpg` |
| `618b3a0d2ccd8824...` | 2 | train, val | 郁金 | True | `train\郁金\Yujin90.jpg`<br>`val\郁金\Yujin87.jpg` |
| `6f76698390d98dc8...` | 2 | train, val | 荆芥穗 | True | `train\荆芥穗\Jingjiesui69.jpg`<br>`val\荆芥穗\Jingjiesui46.jpg` |
| `9cf1bf4c6199a7c4...` | 2 | train, val | 路路通 | True | `train\路路通\Lulutong49.jpg`<br>`val\路路通\Lulutong61.jpg` |
| `a13cd0d63fc8cba3...` | 2 | train, val | 荜澄茄 | True | `train\荜澄茄\BichengqieBichengqieBichengqie44.jpg`<br>`val\荜澄茄\BichengqieBichengqieBichengqie13.jpg` |
| `a99d290c965369a0...` | 2 | train, val | 荆芥穗 | True | `train\荆芥穗\Jingjiesui47.jpg`<br>`val\荆芥穗\Jingjiesui71.jpg` |
| `b6d425252946bc62...` | 2 | train, val | 荔枝核 | True | `train\荔枝核\Lizhihe76.jpg`<br>`val\荔枝核\Lizhihe94.jpg` |
| `b811579185394416...` | 2 | train, val | 荆芥穗 | True | `train\荆芥穗\Jingjiesui56.jpg`<br>`val\荆芥穗\Jingjiesui75.jpg` |
| `bae41b29013c845b...` | 2 | train, val | 山奈 | True | `train\山奈\Shannai90.jpg`<br>`val\山奈\Shannai83.jpg` |
| `c1b236887a280387...` | 2 | train, val | 竹茹 | True | `train\竹茹\Zhuru90.jpg`<br>`val\竹茹\Zhuru89.jpg` |
| `cf7ff97dd8bd43db...` | 2 | train, val | 路路通 | True | `train\路路通\Lulutong8.jpg`<br>`val\路路通\Lulutong33.jpg` |
| `e87d8a96f1e66d74...` | 2 | train, val | 路路通 | True | `train\路路通\Lulutong31.jpg`<br>`val\路路通\Lulutong17.jpg` |
| `07ae9fdf7ba9735c...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya30.jpg`<br>`train\谷芽\GuyaGuya48.jpg` |
| `12db6b5de76c47d5...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya60.jpg`<br>`train\谷芽\GuyaGuya77.jpg` |
| `2141200648876bb4...` | 2 | val | 稻芽, 谷芽 | False | `val\稻芽\DaoyaDaoya16.jpg`<br>`val\谷芽\GuyaGuya15.jpg` |
| `2587a11d3a2dda00...` | 2 | train | 橘核, 龙眼肉 | False | `train\橘核\Juhe99.jpg`<br>`train\龙眼肉\Longyanrou105.jpg` |
| `25acee6cbf3714be...` | 2 | train | 橘核, 荔枝核 | False | `train\橘核\Juhe62.jpg`<br>`train\荔枝核\Lizhihe99.jpg` |
| `299859d75e631846...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya42.jpg`<br>`train\谷芽\GuyaGuya45.jpg` |
| `342186e6c5550841...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya31.jpg`<br>`train\谷芽\GuyaGuya50.jpg` |
| `3429570c51f28958...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya96.jpg`<br>`train\谷芽\GuyaGuya90.jpg` |
| `3f273e9266fdd9c4...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya51.jpg`<br>`train\谷芽\GuyaGuya70.jpg` |
| `4e0ce76118116468...` | 2 | train | 肉豆蔻, 草豆蔻 | False | `train\肉豆蔻\Roudoukou34.jpg`<br>`train\草豆蔻\CaodoukouCaodoukouCaodoukou43.jpg` |
| `53c1f2f48157b601...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen46.jpg`<br>`train\芦根\Lugen52.jpg` |
| `574acedba57fc9b9...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen114.jpg`<br>`train\芦根\Lugen41.jpg` |
| `5761ab58f7e9690d...` | 2 | val | 甘草, 黄芪 | False | `val\甘草\GancaoGancaoGancaoGancao_11.jpg`<br>`val\黄芪\HuangqiHuangqi1.jpg` |
| `5ff229f40ca3aa6c...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya23.jpg`<br>`train\谷芽\GuyaGuya106.jpg` |
| `68e5cce2ae832fa6...` | 2 | train | 芥子, 莱菔子 | False | `train\芥子\Jiezi23.jpg`<br>`train\莱菔子\Laifuzi18.jpg` |
| `6ad9e95745b9f0ea...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya44.jpg`<br>`train\谷芽\GuyaGuya43.jpg` |
| `8060ab98f2c791b8...` | 2 | train | 五加皮, 藁本 | False | `train\五加皮\WujiapiWujiapiWujiapiWujiapi_106.jpg`<br>`train\藁本\GaobenGaobenGaobenGaoben_90.jpg` |
| `821079cee422b6cb...` | 2 | train | 浙贝母, 湖北贝母 | False | `train\浙贝母\ZhebeimuZhebeimuZhebeimuZhebeimu_21.jpg`<br>`train\湖北贝母\Hubeibeimu100.jpg` |
| `86d5dbcb033a4eb4...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen95.jpg`<br>`train\芦根\Lugen63.jpg` |
| `87a1c53dbae6f5ce...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya50.jpg`<br>`train\谷芽\GuyaGuya104.jpg` |
| `8fbe1d8732f52265...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya57.jpg`<br>`train\谷芽\GuyaGuya60.jpg` |
| `9d55250b1e50086f...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya52.jpg`<br>`train\谷芽\GuyaGuya53.jpg` |
| `a2c8e9e199984ec1...` | 2 | val | 稻芽, 谷芽 | False | `val\稻芽\DaoyaDaoya14.jpg`<br>`val\谷芽\GuyaGuya19.jpg` |
| `b5e70e43a91efb70...` | 2 | train | 瓦楞子, 自然铜 | False | `train\瓦楞子\Walengzi14.jpg`<br>`train\自然铜\Zirantong87.jpg` |
| `b639fb7ce6f299f3...` | 2 | train | 橘核, 苍术 | False | `train\橘核\Juhe74.jpg`<br>`train\苍术\CangzhuCangzhuCangzhuCangzhu_6.jpg` |
| `bd6759cb266cd873...` | 2 | train | 橘核, 荔枝核 | False | `train\橘核\Juhe60.jpg`<br>`train\荔枝核\Lizhihe113.jpg` |
| `d522a63b5a4d1648...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen101.jpg`<br>`train\芦根\Lugen47.jpg` |
| `d6c8bd74882ff5af...` | 2 | train | 橘核, 荔枝核 | False | `train\橘核\Juhe97.jpg`<br>`train\荔枝核\Lizhihe119.jpg` |
| `e40dad2fb61f4e48...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya38.jpg`<br>`train\谷芽\GuyaGuya58.jpg` |
| `edabc03375fca683...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen62.jpg`<br>`train\芦根\Lugen95.jpg` |
| `f1c41162e031474c...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya102.jpg`<br>`train\谷芽\GuyaGuya107.jpg` |
| `f4cdc9c1d5fc653b...` | 2 | train | 白茅根, 芦根 | False | `train\白茅根\BaimaogenBaimaogenBaimaogen89.jpg`<br>`train\芦根\Lugen97.jpg` |
| `f599e26535367aae...` | 2 | train | 稻芽, 谷芽 | False | `train\稻芽\DaoyaDaoya85.jpg`<br>`train\谷芽\GuyaGuya38.jpg` |
| `fe1923297ff9424c...` | 2 | train | 北沙参, 麦冬 | False | `train\北沙参\BeishashenBeishashenBeishashen64.jpg`<br>`train\麦冬\Maidong112.jpg` |
| `183c03aedc0ef784...` | 4 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi71(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi71.jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi90(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi90.jpg` |
| `2a39f4788a5a19f7...` | 4 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi75(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi75.jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi92(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi92.jpg` |
| `7590b226e186cf82...` | 4 | train | 干姜 | False | `train\干姜\GanjiangGanjiang29(1).jpg`<br>`train\干姜\GanjiangGanjiang29.jpg`<br>`train\干姜\GanjiangGanjiang30(1).jpg`<br>`train\干姜\GanjiangGanjiang30.jpg` |
| `00ffbe1e2c06eff7...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang115(1).jpg`<br>`train\木丁香\Mudingxiang115.jpg` |
| `0131b101161829cc...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi91(1).jpg`<br>`train\枸杞子\GouqiziGouqizi91.jpg` |
| `0143d3ce5b65c2c3...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175118(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175118.jpg` |
| `01cfd428eb4984c3...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang64(1).jpg`<br>`train\干姜\GanjiangGanjiang64.jpg` |
| `0250279abddd873d...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175138(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175138.jpg` |
| `03596ad5b9dafee4...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_15(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_15.jpg` |
| `058a229cd3164f02...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang107(1).jpg`<br>`train\木丁香\Mudingxiang107.jpg` |
| `06251bd094740a3f...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang37(1).jpg`<br>`train\木丁香\Mudingxiang37.jpg` |
| `075d0ae01b7d55d3...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_69(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_69.jpg` |
