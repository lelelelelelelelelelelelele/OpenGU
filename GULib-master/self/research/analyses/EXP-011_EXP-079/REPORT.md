# 两张主表的新结果：先看原值，再看请求响应

2026-10-23 · EXP-011/e11r1 与 EXP-079/e79r6 · 新损失 / shard_epochs=300 · 分析已生成，等待科学验收

**你选的这张 PubMed 原始准确率图已用 e79r6 重做。主要观察保留：R-point 和 D-full 在两种分片方法上都低于 Random；不同 GU 的响应方向与幅度仍然不同。** 这组规律不能外推为每个数据集上的普遍攻击：CiteSeer 的 GraphEraser 在这两类请求下反而高于 Random。

本轮共重建 **32 组图，每组提供 PNG、PDF、SVG（96 个图文件）**：两张表的三数据集原始准确率、CE、分类 AUC；Random 配对差值、GU–Retrain 差值与预测分歧；新旧分片协议对照；079 十 seed 的跨选点模型响应与敏感性分析。

## 重点图：PubMed，四种请求与同请求 Retrain

![EXP-079 e79r6 PubMed 原始准确率](e79r6_pubmed_accuracy.png)

[PNG](e79r6_pubmed_accuracy.png) · [PDF](e79r6_pubmed_accuracy.pdf) · [SVG](e79r6_pubmed_accuracy.svg)

这张图适合放在分析的前面，因为它直接回答三个问题：模型本身表现怎样、换请求之后改变多少、与同请求 Retrain 相差多少。实心圆为 GU，空心菱形为同请求 Retrain，虚线为该 GU 自己的 Before 均值。横轴是独立请求条件，不是连续删除过程。

PubMed 原始准确率均值（%）：

| method | Random | Degree | R-point | D-full |
| --- | --- | --- | --- | --- |
| Retrain | 88.528 | 88.578 | 86.496 | 86.917 |
| GNNDelete | 86.346 | 87.122 | 86.869 | 86.803 |
| GIF / IDEA | 88.579 | 88.522 | 87.939 | 87.647 |
| MEGU | 87.052 | 86.775 | 86.940 | 86.935 |
| GraphEraser | 87.051 | 87.107 | 86.083 | 86.476 |
| GraphRevoker | 86.429 | 86.410 | 85.114 | 85.614 |

GraphEraser 从 Random 的 87.051% 降至 R-point 的 86.083%、D-full 的 86.476%；GraphRevoker 从 86.429% 降至 85.114%、85.614%。GIF/IDEA 也呈下降，GNNDelete 的 R-point 则高于 Random。**因此要保留完整方法面板，不能把方向不同的响应压成一个统一排名。**

## Q1 / Q2：下降是否超出同 seed 的 Random 波动

以下是 Selected − Random 的准确率变化，负值表示准确率降低。先在训练 seed 内平均 Random 重复，再逐 seed 配对相减；区间为点态 95% t 区间，未做全表多重比较校正。

| 数据集 | 方法 | 请求 | 准确率相对 Random（pp，95% CI） |
| --- | --- | --- | --- |
| PubMed | GraphEraser | R-point | -0.969 [-1.236, -0.701] |
| PubMed | GraphEraser | D-full | -0.576 [-0.729, -0.423] |
| PubMed | GraphRevoker | R-point | -1.315 [-1.728, -0.902] |
| PubMed | GraphRevoker | D-full | -0.816 [-1.244, -0.387] |
| Cora | GraphEraser | R-point | -0.406 [-1.343, +0.531] |
| Cora | GraphEraser | D-full | -0.443 [-0.904, +0.018] |
| Cora | GraphRevoker | R-point | +0.658 [-1.363, +2.679] |
| Cora | GraphRevoker | D-full | +0.178 [-0.731, +1.088] |
| CiteSeer | GraphEraser | R-point | +0.756 [+0.212, +1.300] |
| CiteSeer | GraphEraser | D-full | +0.591 [+0.238, +0.943] |
| CiteSeer | GraphRevoker | R-point | -0.140 [-1.437, +1.157] |
| CiteSeer | GraphRevoker | D-full | -0.095 [-0.597, +0.407] |

**PubMed 的四项分片对照区间均低于零；CiteSeer 的 GraphEraser 两项均高于零；Cora 两种分片方法的 R-point / D-full 区间均跨零。** 这支持有条件的请求响应，不支持普遍伤害。区间跨零也不是等效或“没有影响”的证明。

准确率只是效用的一面。完整图册同时给出测试 CE 与分类 macro OvR AUC，后者不是隐私攻击 AUC。GU–Retrain 预测分歧是同请求的预测差异，不能单独证明遗忘成功或失败。

## EXP-011：把 IM 和 PageRank 补回同一视图

![EXP-011 e11r1 PubMed 八类请求](e11r1_pubmed_accuracy.png)

[PNG](e11r1_pubmed_accuracy.png) · [PDF](e11r1_pubmed_accuracy.pdf) · [SVG](e11r1_pubmed_accuracy.svg)

011 展示八类请求，覆盖 R-point、D-full、Degree、PageRank、三种 IM/RR 预算及 Random。PubMed 下 GraphEraser / R-point 相对 Random 为 **-1.258 [-2.101, -0.416] pp**；GraphRevoker / R-point 为 **-1.896 [-2.472, -1.319] pp**。三种 IM 在两种分片方法上的这些 PubMed 区间均跨零，而 GNNDelete 的 IM 响应明显不同，具体量级见[011 图册](EXP011_REPORT.html)。

**011 只有三个训练 seed。** Random 的十次选点、IM 的三次选点先在每个训练 seed 内平均；误差线使用 n=3，而不是把 30 次 Random 或 9 次 IM 当作独立训练 seed。固定 split 下的训练 seed 区间不覆盖重新划分数据带来的不确定性。011 和 079 的公共条件有重叠，不合并成 13 个独立训练 seed，也不累计为独立科学样本。

## Q3：跨选点模型的响应模式重新计算

复用此前审阅的 response_pattern.py 统计函数，但输入仅来自当前 e79r6；没有复用旧报告结论。GIF/IDEA 在推断几何中只计一个坐标，同时保留六方法敏感性版本。

| 数据集 | GU 维度 | 跨来源模式 margin（pp²） | 95%下限 | 95%上限 |
| --- | --- | --- | --- | --- |
| Cora | dedup5 | 10.108 | 5.086 | 15.129 |
| Cora | drop_GNNDelete | 0.064 | -0.235 | 0.363 |
| CiteSeer | dedup5 | 0.009 | -0.044 | 0.061 |
| CiteSeer | drop_GNNDelete | 0.010 | -0.034 | 0.053 |
| PubMed | dedup5 | 0.057 | -0.173 | 0.287 |
| PubMed | drop_GNNDelete | 0.086 | 0.061 | 0.111 |

这里的正 margin 表示“不同策略、不同选点模型之间的距离”大于“同策略、不同选点模型之间的距离”；单位是 pp²，区间是十个训练 seed 的近似 jackknife 区间。

**Cora 的模式区分仍主要由 GNNDelete 驱动：保留五个独立 GU 坐标时区间为正，去掉 GNNDelete 后跨零。CiteSeer 不支持稳定的整体区分；PubMed 五坐标整体区间也跨零。** PubMed 去掉 GNNDelete 后的正区间属于敏感性结果，不能事后挑选它来宣布全方法普遍迁移。跨来源、逐方法的对照与 Holm 校正结果均保留在 CSV 中。

![EXP-079 e79r6 跨来源响应模式敏感性](response_margin_sensitivity_10seeds.png)

[PNG](response_margin_sensitivity_10seeds.png) · [PDF](response_margin_sensitivity_10seeds.pdf) · [SVG](response_margin_sensitivity_10seeds.svg)

## 和旧图相比，真正变化在哪里

已按数据集、训练 seed、请求与 Selection 身份逐格对齐新旧结果。**非分片方法及 Retrain 的 Output 身份、准确率、CE、AUC、Before、重训差值与分歧值均保持一致（数值容差 1e-8）。** 新变化集中于两个分片方法；下表只列 079 的新−旧原始准确率均值变化。

| 数据集 | 方法 | Random 新−旧（pp） | R-point 新−旧（pp） | D-full 新−旧（pp） |
| --- | --- | --- | --- | --- |
| PubMed | GraphEraser | -0.115 | -0.094 | -0.150 |
| PubMed | GraphRevoker | -0.081 | 0.056 | -0.084 |
| Cora | GraphEraser | -0.351 | -0.258 | -0.498 |
| Cora | GraphRevoker | 7.749 | 10.517 | 10.830 |
| CiteSeer | GraphEraser | -0.050 | 0.000 | 0.360 |
| CiteSeer | GraphRevoker | 1.251 | 0.721 | 0.586 |

这次同时改变了损失实现和 shard_epochs；此对照是协议变化前后的描述，不能归因成“只把轮数减至300就导致某个准确率变化”。旧 Result、旧分析图和原有科学决定保持原样。新图的 Before 也读取新 run，未沿用旧分片 Before。

GraphRevoker 仍是本项目 YAML 声明的 GPA + optimal 实现，本轮没有把它变成论文完整对比聚合实现。它保留独立纵轴，前五个面板共享纵轴；跨面板量级比较要读刻度或 CSV。GIF 与 IDEA 的准确率坐标相同，CE 最大差约 1.01e-8、分类 AUC 最大差约 0.00071 pp，合并面板不等于算法等价。误差线是均值区间，不能直接当作稳定性或方差比较。

## 完整图册与复算入口

- [EXP-011 全部图与数据说明](EXP011_REPORT.html) · [MD](EXP011_REPORT.md)
- [EXP-079 全部图与响应分析](EXP079_REPORT.html) · [MD](EXP079_REPORT.md)
- [逐 cell 数据](cells.csv) · [按训练 seed 汇总](seed_values.csv) · [均值、SD 与区间](summary.csv)
- [逐 seed Random 配对差值](paired_seed_values.csv) · [配对区间](paired_vs_random.csv)
- [新旧逐格对照](old_new_matched_cells.csv) · [新旧配对差值](protocol_change_paired.csv)
- [输入与身份核验](input_audit.json) · [生成器](rebuild.py) · [报告生成器](report.py) · [图册验证](validation.json)

## 证据范围与状态

当前输入为 011 的 1,449 格 / 1,242 个 GU–Retrain 配对，以及 079 的 2,520 格 / 2,160 个配对。重新核对两次可信 delivery、项目检查、可信索引、全部 7,940 个当前文件的 SHA-256；对历史参照另外核对 7,940 个文件及配对身份。图中没有使用未回传的模型或本地重新运行结果。

执行 SHA：`bab1781e182254e0b02cbeb1de138d58f7f1cd50`。图册生成与科学接受分开：本轮完成可复算的描述性分析，尚未把它写成用户已经接受的新论文结论。

复现：用带 numpy、pandas、scipy、matplotlib、markdown-it-py 的 Python 先运行 `rebuild.py`，再运行 `report.py`。全流程只读本地可信结果，不启动 GPU、不修改远端缓存。
