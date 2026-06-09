# 分类数据重复与泄漏审计报告

- 数据路径: `D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg_93class_leakage_clean_candidate`
- 状态: `needs_leakage_review`
- 总图片: 9552
- 唯一 SHA256: 9033
- 重复 SHA256 组: 513
- 重复图片数: 1032，额外重复图: 519
- 跨划分重复组: 0
- train/val 泄漏组: 0
- 跨类别重复组: 34

## 边界说明

该审计只检查文件字节级 SHA256 完全重复；不包含近似重复、裁剪相似或感知哈希判断。

## 建议动作

- 优先人工复核 train/val exact duplicate，避免验证集泄漏导致指标偏乐观。
- 若同一 SHA256 跨类别出现，优先检查目录标签是否混入或类别命名是否冲突。
- 确认后再删除或重划样本；不要仅凭本报告自动删图。

## 重复组样例

| SHA256 | count | splits | classes | train/val leak | paths |
|---|---:|---|---|---|---|
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
| `07f890b4cbffdc5b...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi26(1).jpg`<br>`train\枸杞子\GouqiziGouqizi26.jpg` |
| `0849f07eaec13030...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang59(1).jpg`<br>`train\干姜\GanjiangGanjiang59.jpg` |
| `085f02a22eaeb716...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi101(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi101.jpg` |
| `08b49e5bb737058a...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang33(1).jpg`<br>`train\干姜\GanjiangGanjiang33.jpg` |
| `09c967d6a5f45a6d...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175142(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinIMG_20200724_175142.jpg` |
| `0ab308f5ab7ad7be...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang91(1).jpg`<br>`train\木丁香\Mudingxiang91.jpg` |
| `0ad408b809eff210...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi32(1).jpg`<br>`train\枸杞子\GouqiziGouqizi32.jpg` |
| `0b237545408eee65...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang32(1).jpg`<br>`train\干姜\GanjiangGanjiang32.jpg` |
| `0b4317d15e80bce4...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_25(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_25.jpg` |
| `0b4b6261b11f5900...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang73(1).jpg`<br>`train\干姜\GanjiangGanjiang73.jpg` |
| `0bcd65c45943f069...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang65(1).jpg`<br>`train\木丁香\Mudingxiang65.jpg` |
| `0caead1efd8419cc...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang93(1).jpg`<br>`train\干姜\GanjiangGanjiang93.jpg` |
| `0d23aadd287635ee...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi69(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi69.jpg` |
| `0ed9188dc6d63df2...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi58(1).jpg`<br>`train\枸杞子\GouqiziGouqizi58.jpg` |
| `0f0edcbe57fd8737...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang103(1).jpg`<br>`train\木丁香\Mudingxiang103.jpg` |
| `0f2d4beb81879430...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi70(1).jpg`<br>`train\枸杞子\GouqiziGouqizi70.jpg` |
| `0f701d11a00bd36d...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang26(1).jpg`<br>`train\木丁香\Mudingxiang26.jpg` |
| `0fc6950ac9bc14e8...` | 2 | train | 谷精草 | False | `train\谷精草\GujingcaoGujingcao88.jpg`<br>`train\谷精草\GujingcaoGujingcao91.jpg` |
| `103559645f6a9774...` | 2 | train | 黄芩 | False | `train\黄芩\HuangqinHuangqinHuangqinHuangqin_21(1).jpg`<br>`train\黄芩\HuangqinHuangqinHuangqinHuangqin_21.jpg` |
| `10386264d4984bfa...` | 2 | train | 枸杞子 | False | `train\枸杞子\GouqiziGouqizi113(1).jpg`<br>`train\枸杞子\GouqiziGouqizi113.jpg` |
| `10d1d6d245d3630d...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi88(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi88.jpg` |
| `10f3eb7d7c6f3710...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang93(1).jpg`<br>`train\木丁香\Mudingxiang93.jpg` |
| `11b6c87e2d53307a...` | 2 | train | 荔枝核 | False | `train\荔枝核\Lizhihe59.jpg`<br>`train\荔枝核\Lizhihe73.jpg` |
| `12618b8efcb26622...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi72(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi72.jpg` |
| `128fa8b5e0622a66...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang25(1).jpg`<br>`train\干姜\GanjiangGanjiang25.jpg` |
| `1310d76f4f2ec738...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang50(1).jpg`<br>`train\木丁香\Mudingxiang50.jpg` |
| `1316aeaab8a375f0...` | 2 | train | 土荆皮 | False | `train\土荆皮\Tujingpi87.jpg`<br>`train\土荆皮\Tujingpi90.jpg` |
| `1498b08777aef5fa...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi49(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi49.jpg` |
| `152982e078ccb28b...` | 2 | train | 人参 | False | `train\人参\Renshen54.jpg`<br>`train\人参\Renshen97.jpg` |
| `159ecfd8522604a8...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang47(1).jpg`<br>`train\干姜\GanjiangGanjiang47.jpg` |
| `165a11da19114d73...` | 2 | train | 川牛膝 | False | `train\川牛膝\ChuanniuxiChuanniuxi47(1).jpg`<br>`train\川牛膝\ChuanniuxiChuanniuxi47.jpg` |
| `16ff1c80fc053059...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang67(1).jpg`<br>`train\干姜\GanjiangGanjiang67.jpg` |
| `17278cf488072890...` | 2 | train | 干姜 | False | `train\干姜\GanjiangGanjiang85(1).jpg`<br>`train\干姜\GanjiangGanjiang85.jpg` |
| `174b921ea60b7349...` | 2 | train | 木丁香 | False | `train\木丁香\Mudingxiang6(1).jpg`<br>`train\木丁香\Mudingxiang6.jpg` |
