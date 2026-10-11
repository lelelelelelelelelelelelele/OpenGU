# EXP-079：252格缓存性能 Gate

运行版本：`39da4a58a2bdaa4ba61daec03860274236bf8d45`。3个数据集 × 12个选点条件 × 7种方法，训练seed42，删除比例0.1。仅分析本gate，不代表2520格正式矩阵完成。

| 观察 | 首轮 e79g4c | 热轮 e79g4w |
|---|---:|---:|
| 完整作业秒数 | 941.0 | 278.0 |
| 排队秒数 | 32.0 | 52.0 |
| 完成格数 | 252 | 252 |
| score | hit=252 | hit=252 |
| selection | hit=252 | hit=252 |
| method | hit=252 | hit=252 |
| selector_checkpoint | hit=168, not_applicable=84 | hit=168, not_applicable=84 |
| method_checkpoint | hit=216, not_applicable=36 | hit=216, not_applicable=36 |
| evaluation | miss=245, hit=7 | hit=252 |
| post_unlearning_utility_and_retrain_gap | miss=210, hit=6 | hit=216 |
| post_unlearning_flip_hop | miss=210, hit=6 | hit=216 |

完整作业时间取 Core receipt started_at→finished_at，包含进程初始化、导出和终态页面生成；排队、回传分别处理，不算作计算。首轮保留既有Evaluation缓存，仅计算缺失指标。热轮相对首轮耗时比为 3.38 倍。

历史同范围 e79g1 在1802秒处因1800秒上限终止，未完成。本次可说明累计优化后的实际表现；历史未完成、缓存状态及代码不同，不能把时间比解释为AAGU-094单项净加速或精确A/B。

两轮252/252 Output引用与Evaluation来源一致，252份metrics.json、252份selection.json逐字节一致。每轮505份产物经正常自动回传和SHA核验，项目接受252格；科研接受仍未请求。

## 逐项计时

下表为方法条目的current_access wall总和及基础/配对评价访问时间总和；后者可能包含在方法wall内，不能再次相加推算整轮时间。Selector时间由同组选点共享，不按七种方法重复累加。完整逐格计时见CSV。

| 轮次 | 数据集 | 方法 | 格数 | 方法访问wall秒 | 基础Evaluation秒 | 配对评价访问秒 |
|---|---|---|---:|---:|---:|---:|
| e79g4c | Cora | GNNDelete | 12 | 11.172 | 4.433 | 23.044 |
| e79g4c | Cora | GIF | 12 | 10.783 | 4.592 | 25.155 |
| e79g4c | Cora | IDEA | 12 | 11.231 | 4.143 | 29.798 |
| e79g4c | Cora | MEGU | 12 | 10.952 | 4.337 | 31.233 |
| e79g4c | Cora | GraphEraser | 12 | 11.725 | 5.146 | 31.223 |
| e79g4c | Cora | GraphRevoker | 12 | 14.164 | 7.792 | 31.034 |
| e79g4c | Cora | Retrain | 12 | 11.425 | 4.555 | 0.000 |
| e79g4c | CiteSeer | GNNDelete | 12 | 15.543 | 8.269 | 21.027 |
| e79g4c | CiteSeer | GIF | 12 | 15.074 | 8.170 | 21.432 |
| e79g4c | CiteSeer | IDEA | 12 | 15.721 | 8.032 | 22.007 |
| e79g4c | CiteSeer | MEGU | 12 | 15.773 | 8.229 | 22.208 |
| e79g4c | CiteSeer | GraphEraser | 12 | 20.390 | 12.893 | 24.733 |
| e79g4c | CiteSeer | GraphRevoker | 12 | 29.179 | 19.988 | 23.063 |
| e79g4c | CiteSeer | Retrain | 12 | 27.926 | 17.729 | 0.000 |
| e79g4c | PubMed | GNNDelete | 12 | 12.503 | 5.167 | 36.868 |
| e79g4c | PubMed | GIF | 12 | 11.412 | 4.901 | 26.178 |
| e79g4c | PubMed | IDEA | 12 | 11.985 | 5.235 | 26.477 |
| e79g4c | PubMed | MEGU | 12 | 12.345 | 5.583 | 26.649 |
| e79g4c | PubMed | GraphEraser | 12 | 13.639 | 7.141 | 31.136 |
| e79g4c | PubMed | GraphRevoker | 12 | 12.456 | 5.675 | 33.736 |
| e79g4c | PubMed | Retrain | 12 | 13.171 | 5.494 | 0.000 |
| e79g4w | Cora | GNNDelete | 12 | 10.673 | 7.733 | 3.894 |
| e79g4w | Cora | GIF | 12 | 8.429 | 6.411 | 4.189 |
| e79g4w | Cora | IDEA | 12 | 2.036 | 1.383 | 3.910 |
| e79g4w | Cora | MEGU | 12 | 2.991 | 2.288 | 3.794 |
| e79g4w | Cora | GraphEraser | 12 | 2.170 | 1.490 | 3.854 |
| e79g4w | Cora | GraphRevoker | 12 | 2.201 | 1.571 | 3.929 |
| e79g4w | Cora | Retrain | 12 | 2.343 | 1.487 | 0.000 |
| e79g4w | CiteSeer | GNNDelete | 12 | 2.208 | 1.412 | 3.796 |
| e79g4w | CiteSeer | GIF | 12 | 2.053 | 1.437 | 3.931 |
| e79g4w | CiteSeer | IDEA | 12 | 1.850 | 1.238 | 3.881 |
| e79g4w | CiteSeer | MEGU | 12 | 2.026 | 1.376 | 3.901 |
| e79g4w | CiteSeer | GraphEraser | 12 | 2.156 | 1.481 | 3.974 |
| e79g4w | CiteSeer | GraphRevoker | 12 | 1.993 | 1.387 | 3.909 |
| e79g4w | CiteSeer | Retrain | 12 | 2.321 | 1.465 | 0.000 |
| e79g4w | PubMed | GNNDelete | 12 | 2.437 | 1.623 | 4.599 |
| e79g4w | PubMed | GIF | 12 | 2.307 | 1.566 | 4.508 |
| e79g4w | PubMed | IDEA | 12 | 2.353 | 1.628 | 4.739 |
| e79g4w | PubMed | MEGU | 12 | 2.318 | 1.543 | 5.575 |
| e79g4w | PubMed | GraphEraser | 12 | 2.505 | 1.738 | 5.739 |
| e79g4w | PubMed | GraphRevoker | 12 | 2.554 | 1.750 | 5.661 |
| e79g4w | PubMed | Retrain | 12 | 2.950 | 1.583 | 0.000 |

## 证据

- [e79g4c逐格CSV](e79g4c.items.csv)、[摘要](e79g4c.summary.json)；[本地结果](../../../../../results/runs/gpu4090/exp079-cache-speed-gate/e79g4c/run.json)；[delivery](../../../../../.syncmate/deliveries/exp079-20261012-e79g4c.json)。
- [e79g4w逐格CSV](e79g4w.items.csv)、[摘要](e79g4w.summary.json)；[本地结果](../../../../../results/runs/gpu4090/exp079-cache-speed-gate/e79g4w/run.json)；[delivery](../../../../../.syncmate/deliveries/exp079-20261012-e79g4w.json)。


## 性能瓶颈调查

[诊断报告](PERFORMANCE_DIAGNOSIS.html)及[可编辑源](PERFORMANCE_DIAGNOSIS.md)：真实只读HIT单请求59次SQL执行，底层SQLite执行/取数占样本90.6%；三类真实指标的隔离冷写入样本中SQLite执行/取数/提交占70.2%–74.4%。待优化方向是减少重复查询、写连接/schema重复准备及同Output跨评价重复加载，未将小样本换算为承诺加速倍数。
