# EXP-067 CiteSeer H64 Validate

H64固定参数多请求Validate完成：21/21格，115/115产物校验通过；3个Random请求的GIF/IDEA数值稳定性均通过。H16暂缓；不代表完整双宽度范围或最终科学验收。

执行版本：`88e46cc66f95ae25e13c3eb40ea3f685f75cc6c4`；run：`aagu067-citeseer-h64-validation-104246-104248-v1`。

范围：固定checkpoint及参数，10% train-mask删除，Random请求104246/104247/104248；T100为生产设置，T200/400用于一致性检查。每个请求配对一次3000轮Retrain。GIF/IDEA各9格禁用缓存，3格Retrain均为cache miss。

| 请求 | GIF F1 | IDEA F1 | Retrain F1 | GIF−Retrain |
| --- | ---: | ---: | ---: | ---: |
| 104246 | 0.746246 | 0.746246 | 0.747748 | -0.001502 |
| 104247 | 0.743243 | 0.743243 | 0.747748 | -0.004505 |
| 104248 | 0.744745 | 0.744745 | 0.738739 | +0.006006 |

以上为描述性效用差异，不是预测/参数空间的完整retrain-gap，也不证明其他选择器、预算或宽度同样稳定。原始结果未重跑；Windows长路径回传失败后，针对同一job重新收集并验证成功。初始controller阻塞记录保留，最新delivery记录可信回传。

复核入口：[分析数据](validation-h64-20260924.json)；[分析脚本](../validation-20260924/analyze.py)。数值阈值及逐请求检查明细在分析数据中。
