# Table02 v2：加入 GIF / IDEA 后的结果分析

2026-09-30。问题：结构化删除请求能否比随机请求造成更多效用损害，以及这种变化是否伴随相对同请求 Retrain 的偏离？

本次采用 exp011-t2 / 0925-v1 的全部 1449 格，执行 SHA 为 `1f5cfec08494ef1a78eda16bd3f69428ac47b0bd`。三个数据集、三个训练 seed、10% 删除预算、六种 GU 加 Retrain；1242 条 GU–Retrain 配对逐条核对完整输出引用、Selection ID、数据集及训练 seed。2898 个逐格文件再次按运行 manifest 校验通过。无排除格。207 个条件使用 81 个不同 Selection Artifact，不是 207 次独立选点抽样。

证据：[可信运行](../../../../results/runs/gpu4090/exp011-t2/0925-v1/run.json)、[汇总CSV](table02-v2-summary.csv)、[全部方法表](table02-v2-tables.md)、[审计](table02-v2-audit.json)、[复算脚本](analyze_table02_v2.py)。正式配置为 [table02_v2.yaml](../../../../experiments/configs/aagu011/table02_v2.yaml)。历史报告中的数值不替代本次重新汇总结果。

## 指标与汇总口径

- after F1：当前 utility 实现为测试节点 argmax 分类准确率（单标签 micro-F1 等价），不是 macro-F1。
- 效用损失：before−after，正值表示损害。
- 相对 Random：同数据集、方法、训练 seed 下，after 减去十个 Random 选集的 after 均值；负值表示结构化请求损害更大。各 selector 内先平均选点重复，再对三个训练 seed 等权平均。
- 本报告 signed gap = GU−Retrain；原始 metrics 中的 `gap` 是 Retrain−GU，报告已反号。正值表示 GU 测试效用高于 Retrain，不等于更正确地遗忘。
- Flip 是 GU 与同请求 Retrain 的预测分歧，不是相对原模型的翻转。保留测试节点上的分歧衡量行为差异，不等于精度下降或隐私泄露。
- 训练 SD 是三个训练 seed 的选点均值之间的样本标准差，不是置信区间。三个训练 seed 和同一图上复用的选集不足以支撑广泛显著性宣称。

## GIF / IDEA：效用损害较小，具有数据集和策略依赖

两方法 207/207 配对条件的 after F1 完全相同，所以下表共同展示。完整输出 content hash 均不同，不能据此断言模型、logits 或算法相同；也不能把两列相同 F1 当作两份独立机制证据。部分其他指标不同。后续若要解释两方法机制差异，需要专门核对更新量与预测概率，本表不作该推断。

| 数据集 | Random after % | R-point 相对Random / pp | D-full 相对Random / pp | RR-16384 相对Random / pp | RR-65536 相对Random / pp |
|---|---:|---:|---:|---:|---:|
| Cora | 90.117 | −0.203 | −0.510 | +0.207 | +0.187 |
| CiteSeer | 74.595 | +0.430 | +0.430 | −0.003 | +0.147 |
| PubMed | 88.458 | −0.680 | −0.942 | −0.001 | −0.023 |

PubMed 的 D-full 是新增方法中最清楚的描述性效用损害：before 88.480%，after 87.517%，下降 0.963 pp，相对 Random 低 0.942 pp。Cora 的 D-full 相对 Random 低 0.510 pp；CiteSeer 的 R-point/D-full 反而比 Random 高 0.430 pp。因此不能写成 IF 选点对 GIF/IDEA 在所有数据集有效。

RR 三个规模对 GIF/IDEA 没有表现出强效用攻击：Cora 为 +0.125 至 +0.207 pp；CiteSeer 为 −0.003 至 +0.147 pp；PubMed 为 −0.006、−0.001、−0.023 pp。增加 RR 数量不能直接解释成更强下游效用损害。

## 效用接近不意味着接近 Retrain

| GIF / IDEA 数据集 | Random Flip % | R-point Flip % | R-point GU−Retrain / pp | D-full GU−Retrain / pp |
|---|---:|---:|---:|---:|
| Cora | 2.491 | 6.396 | +1.169 | −0.185 |
| CiteSeer | 4.665 | 7.407 | +0.100 | +0.200 |
| PubMed | 2.121 | 4.048 | +1.665 | +1.031 |

R-point 在三个数据集的预测分歧均高于 Random，即使 CiteSeer 的 F1 还提高了。PubMed 的 R-point 和 D-full 虽使 GU 效用下降，GU 仍高于同请求 Retrain：删除请求也损害了精确重训模型，不能把 GU 的全部下降归因于近似遗忘失效。应并列报告效用、signed gap 和预测分歧。

## 放回六种 GU 的完整表

以下每项是在七种非 Random 策略中取最小的相对 Random 均值，仅用于描述响应范围，存在事后选最优，不能当作预先指定策略的无偏攻击效果。

| 方法 | Cora 最小差值 / pp | CiteSeer 最小差值 / pp | PubMed 最小差值 / pp |
|---|---|---|---|
| GIF / IDEA | D-full −0.510 | Degree −0.020 | D-full −0.942 |
| GNNDelete | D-full −6.070 | RR-16384 −1.166 | RR-65536 −3.093 |
| MEGU | RR-4096 −0.125 | D-full −0.220 | Degree −0.262 |
| GraphEraser | RR-4096 −0.629 | RR-4096 −0.194 | R-point −1.171 |
| GraphRevoker | R-point −3.850 | D-full −0.345 | R-point −1.210 |

本表支持“不同方法对相同选点策略的响应具有异质性”：GNNDelete 的额外损害幅度明显大于新增 GIF/IDEA，但不能据此建立普遍方法排序。GIF/IDEA 显式使用 H64；各方法训练模型和分片聚合机制不应被假设相同，绝对 after F1 排名尤其不能直接作为算法优劣结论。分片方法的 GU−Retrain 差异还包含模型与聚合差异。

## 论文使用与下一步

主表可采用本次完整六 GU 的描述性结果，同时展示相对 Random 的效用变化；预测分歧与 signed gap 放入配套诊断表，强调效用保持与重训一致性是不同问题。新增方法提供了攻击边界：在当前预算与参数下，GIF/IDEA 没有出现普遍的大幅效用崩塌，但部分结构化请求增加了与 Retrain 的行为差异。

优先后续分析是解释 GIF/IDEA 相同 F1 的来源，核对其更新幅度、概率差异与数值参数；在此之前不将其表述为两种机制的独立鲁棒性验证。本次不启动新实验。科学决定保持待用户确认；回传通过与本报告提交不代表科学接受。
