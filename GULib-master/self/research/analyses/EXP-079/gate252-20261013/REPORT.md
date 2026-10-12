# EXP-079：seed2024 的252点冷热 Gate 对比

两轮完成、回传及项目核验通过。冷轮 **790秒**，热轮 **91秒**；分别对比历史941秒和278秒。未重跑前测。

| 轮次 | 历史 seed42 | 本轮 seed2024 | 减少 | 耗时降低 | 历史/本轮 |
|---|---:|---:|---:|---:|---:|
| 冷轮 | 941s | 790s | 151s | 16.0% | 1.19× |
| 热轮 | 278s | 91s | 187s | 67.3% | 3.05× |

## 范围与计时

本轮执行版本：`35f7df936e2858cf13ff2a80dda395a18dfc396c`；历史执行版本：`39da4a58a2bdaa4ba61daec03860274236bf8d45`。Cora、CiteSeer、PubMed各12种选点条件×七种方法，各84点，共252点；训练seed2024、删除比例0.1。配置及方法参数保持原矩阵口径。

完整作业耗时由原Core receipt的started_at至finished_at计算，包含进程初始化、计算、导出和终态投影，排队与回传不计入。每轮1800秒为超时边界；全MISS串行估时22728秒是历史工程预算，不是缓存命中速度预测。

冷轮排队11秒，热轮排队8秒。回传独立耗时未单独确认，保留未记录。

## 缓存与正确性

| 层 | 冷轮 e79g7c | 热轮 e79g7w |
|---|---:|---:|
| score | hit=252 | hit=252 |
| selection | hit=252 | hit=252 |
| method | hit=252 | hit=252 |
| selector_checkpoint | hit=168, not_applicable=84 | hit=168, not_applicable=84 |
| method_checkpoint | hit=216, not_applicable=36 | hit=216, not_applicable=36 |
| evaluation | miss=252 | hit=252 |
| post_unlearning_utility_and_retrain_gap | miss=216 | hit=216 |
| post_unlearning_flip_hop | miss=216 | hit=216 |

冷轮684个Evaluation请求全部MISS并计算保存；热轮684个请求全部HIT。两轮Score/Selection/Output适用请求全部HIT，三层producer均未调用。表中Score/Selection按cell展示重复记录；独立选点请求为36组，不能把252展示次数称为252个独立Selection。

252/252条件、Output及缓存来源引用一致；252份metrics.json和252份selection.json逐字节一致。每轮505份结果产物经正常回传、SHA-256核验及可信索引，项目结果检查接受252格。这里的“接受”是机器结果检查，未代替人的科研结论接受。

## 可比性与结论边界

该结果用于评估095交付后的实际工程表现。历史冷轮已有19个Evaluation HIT、665个MISS；本轮为684个MISS，并且训练seed不同。没有追加前测或重复运行来隔离机器负载与冷启动波动，所以不能把耗时比当成严格同seed受控实验或每次运行的保证。

本次只完成指定252点的两轮性能验证，不代表2520点完整多seed矩阵完成，也不自动提交全表。

## 方法访问分项

下表只汇总各方法条目的排他阶段计时，覆盖Output查询及基础Evaluation；不包括全部配对Evaluation、Selector、共享准备、导出或终态投影，不能当作整轮分解。

| 阶段 | 历史冷轮 | 本轮冷轮 | 历史热轮 | 本轮热轮 |
|---|---:|---:|---:|---:|
| output_query | 150.554s | 179.797s | 18.728s | 10.303s |
| evaluation_query_validation | 7.587s | 8.449s | 42.481s | 3.410s |
| evaluation_inputs | 69.537s | 32.947s | 0.000s | 0.000s |
| metric_formula | 2.702s | 2.739s | 0.000s | 0.000s |
| evaluation_write_validation | 76.563s | 61.578s | 0.000s | 0.000s |
| output_access | 1.585s | 1.352s | 1.624s | 0.435s |

## 数据集访问计时

方法访问wall包含其基础Evaluation；配对评价另外列出。这里只是单元累计访问时间，不是数据集或整轮作业起止时间。

| 轮次 | 数据集 | 点数 | 方法访问wall总和 | 配对评价访问总和 |
|---|---|---:|---:|---:|
| e79g7c | Cora | 84 | 88.678s | 106.985s |
| e79g7c | CiteSeer | 84 | 79.441s | 139.413s |
| e79g7c | PubMed | 84 | 119.784s | 115.148s |
| e79g7w | Cora | 84 | 5.061s | 1.464s |
| e79g7w | CiteSeer | 84 | 4.606s | 1.447s |
| e79g7w | PubMed | 84 | 5.497s | 1.958s |

## AutoReport 终态核对

两轮原始事件均已出现唯一run completed，全部started与completed配对，无failed或悬空条目。按独立事件计数，每轮Selection36 HIT、Output252 HIT；Evaluation冷轮684 MISS、热轮684 HIT。输入核对条目与实际指标计算分开计数。

| 阶段 | 冷轮已完成条目耗时累计 | 热轮已完成条目耗时累计 |
|---|---:|---:|
| output_query | 179.797s | 10.303s |
| evaluation_inputs | 63.813s | 0.000s |
| evaluation_query_validation | 40.722s | 8.274s |
| evaluation_write_validation | 358.872s | 0.000s |
| metric_formula | 3.738s | 0.000s |

此表涵盖基础与配对指标的已完成条目，包含范围比上方方法条目表更广；仍不含条目之外的全部共享准备、审计写入、导出和进程开销。两表不得相加。

AutoReport执行器wall：冷轮775.170s，热轮83.210s；其中审计追加记录累计分别74.743s、29.363s。执行器wall不包含全部进程导入及结束投影，不替代首页的Runner完整作业时间。

## 证据

- [机器可读对比](comparison.json)；[历史252点报告](../gate252-20261012/REPORT.md)。
- [本轮配置](../../../../../experiments/configs/exp079/cache_speed_gate_s2024.yaml)；[提交前逐点只读检查](../../../../../.syncmate/exp079-gate84-20261013/seed2024-252-check.json)。
- e79g7c：[摘要](e79g7c.summary.json)、[逐点CSV](e79g7c.items.csv)、[AutoReport摘要](e79g7c.audit-summary.json)、[原始事件快照](../../../../../.syncmate/exp079-gate252-20261013/e79g7c.audit-snapshot.json)、[run.json](../../../../../results/runs/gpu4090/exp079-cache-speed-gate/e79g7c/run.json)、[正式回传核验](../../../../../.syncmate/deliveries/exp079-20261013-e79g7c.json)。
- e79g7w：[摘要](e79g7w.summary.json)、[逐点CSV](e79g7w.items.csv)、[AutoReport摘要](e79g7w.audit-summary.json)、[原始事件快照](../../../../../.syncmate/exp079-gate252-20261013/e79g7w.audit-snapshot.json)、[run.json](../../../../../results/runs/gpu4090/exp079-cache-speed-gate/e79g7w/run.json)、[正式回传核验](../../../../../.syncmate/deliveries/exp079-20261013-e79g7w.json)。
