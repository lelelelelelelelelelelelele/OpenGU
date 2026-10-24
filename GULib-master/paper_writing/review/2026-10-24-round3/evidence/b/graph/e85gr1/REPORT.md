# e85gr1 同权重两图与后处理诊断

仅采用已accepted且delivery/handoff/job/SHA/可信索引一致的 e85gr1；36个GU–Ret对，180组三端点、7200个真值格通过独立整数重建。

逐seed端点、真值、两图变化、请求组成分别输出CSV；MEGU另给四端点后处理效应。原图accuracy及D复现旧084/080；CE按冻结容差复核，未放宽阈值。O=G≠R拆为Ret纠错、Ret损失和双方均错。

A完整范围仅R-point与D-full的20对；B完整范围保留三个seed、两预算和两个基线。门槛gate只做局部技术核验，不能代替全范围。完整结果给逐seed请求差和B的5%→33%差中差；共享Ret、固定Selection及节点不能当作独立样本。

该报告只分析已返回协议统计，不把请求组成解释成因果控制；Ret轨迹和核心贡献复审仍须独立完成。Original-before CE absent in old084/080; checked against trusted first layer only. Raw per-logit relative tolerance cannot be independently recomputed from lightweight result files; exact frozen policy and recorded replay checks are retained. Three of six MEGU endpoint pair counts reconstruct from triangle joints; remaining pairs and cross-graph counts checked by integer bounds and metric inequalities only, no node-level predictions returned. Composition is observational, not a causal adjustment. No Ret training-quality conclusion or writing-gate decision.

| method | graph | triangle | selector | ratio | n | gu_accuracy_mean | retrain_accuracy_mean | gu_retrain_disagreement_mean | ret_only_corrects_mean | ret_only_harms_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GIF | original | published | degree | 0.050000 | 3 | 0.745245 | 0.751752 | 0.031532 | 10 | 6.333333 |
| GIF | original | published | degree | 0.330000 | 3 | 0.745245 | 0.755255 | 0.081081 | 23.333333 | 18.666667 |
| GIF | original | published | r_point | 0.050000 | 3 | 0.748749 | 0.752753 | 0.046046 | 12.666667 | 10 |
| GIF | original | published | r_point | 0.330000 | 3 | 0.743744 | 0.647147 | 0.246246 | 34.666667 | 102.333333 |
| GIF | original | published | random | 0.050000 | 3 | 0.745245 | 0.747748 | 0.040541 | 11.666667 | 10 |
| GIF | original | published | random | 0.330000 | 3 | 0.746747 | 0.731732 | 0.100100 | 20.333333 | 30 |
| GIF | original | raw | degree | 0.050000 | 3 | 0.745245 | 0.751752 | 0.031532 | 10 | 6.333333 |
| GIF | original | raw | degree | 0.330000 | 3 | 0.745245 | 0.755255 | 0.081081 | 23.333333 | 18.666667 |
| GIF | original | raw | r_point | 0.050000 | 3 | 0.748749 | 0.752753 | 0.046046 | 12.666667 | 10 |
| GIF | original | raw | r_point | 0.330000 | 3 | 0.743744 | 0.647147 | 0.246246 | 34.666667 | 102.333333 |
| GIF | original | raw | random | 0.050000 | 3 | 0.745245 | 0.747748 | 0.040541 | 11.666667 | 10 |
| GIF | original | raw | random | 0.330000 | 3 | 0.746747 | 0.731732 | 0.100100 | 20.333333 | 30 |
| GIF | retained | published | degree | 0.050000 | 3 | 0.730230 | 0.736236 | 0.044044 | 13.666667 | 10 |
| GIF | retained | published | degree | 0.330000 | 3 | 0.722222 | 0.723223 | 0.100100 | 25 | 24.333333 |
| GIF | retained | published | r_point | 0.050000 | 3 | 0.752252 | 0.753754 | 0.036537 | 10.333333 | 8 |
| GIF | retained | published | r_point | 0.330000 | 3 | 0.738238 | 0.650651 | 0.192693 | 24 | 84 |
| GIF | retained | published | random | 0.050000 | 3 | 0.743243 | 0.745746 | 0.034535 | 9.666667 | 8 |
| GIF | retained | published | random | 0.330000 | 3 | 0.739239 | 0.713213 | 0.092593 | 16 | 33 |
| GIF | retained | raw | degree | 0.050000 | 3 | 0.730230 | 0.736236 | 0.044044 | 13.666667 | 10 |
| GIF | retained | raw | degree | 0.330000 | 3 | 0.722222 | 0.723223 | 0.100100 | 25 | 24.333333 |
| GIF | retained | raw | r_point | 0.050000 | 3 | 0.752252 | 0.753754 | 0.036537 | 10.333333 | 8 |
| GIF | retained | raw | r_point | 0.330000 | 3 | 0.738238 | 0.650651 | 0.192693 | 24 | 84 |
| GIF | retained | raw | random | 0.050000 | 3 | 0.743243 | 0.745746 | 0.034535 | 9.666667 | 8 |
| GIF | retained | raw | random | 0.330000 | 3 | 0.739239 | 0.713213 | 0.092593 | 16 | 33 |
| MEGU | original | matched_cs | degree | 0.050000 | 3 | 0.743744 | 0.751752 | 0.053053 | 10.333333 | 8.666667 |
| MEGU | original | matched_cs | degree | 0.330000 | 3 | 0.747247 | 0.755255 | 0.078078 | 20.333333 | 17.333333 |
| MEGU | original | matched_cs | r_point | 0.050000 | 3 | 0.742242 | 0.752753 | 0.062062 | 13.666667 | 10 |
| MEGU | original | matched_cs | r_point | 0.330000 | 3 | 0.742743 | 0.647147 | 0.249249 | 34 | 99 |
| MEGU | original | matched_cs | random | 0.050000 | 3 | 0.738238 | 0.747748 | 0.064064 | 12.666667 | 12.333333 |
| MEGU | original | matched_cs | random | 0.330000 | 3 | 0.736236 | 0.731732 | 0.101101 | 17.333333 | 25.333333 |
| MEGU | original | published | degree | 0.050000 | 3 | 0.743744 | 0.751752 | 0.053053 | 6.666667 | 5.666667 |
| MEGU | original | published | degree | 0.330000 | 3 | 0.747247 | 0.755255 | 0.078078 | 17.666667 | 15.666667 |
| MEGU | original | published | r_point | 0.050000 | 3 | 0.742242 | 0.752753 | 0.062062 | 9.333333 | 7.333333 |
| MEGU | original | published | r_point | 0.330000 | 3 | 0.742743 | 0.647147 | 0.249249 | 33.666667 | 98.333333 |
| MEGU | original | published | random | 0.050000 | 3 | 0.738238 | 0.747748 | 0.064064 | 9.666667 | 7.333333 |
| MEGU | original | published | random | 0.330000 | 3 | 0.736236 | 0.731732 | 0.101101 | 15 | 23.333333 |
| MEGU | original | raw | degree | 0.050000 | 3 | 0.739740 | 0.751752 | 0.067067 | 7.333333 | 5.666667 |
| MEGU | original | raw | degree | 0.330000 | 3 | 0.738739 | 0.755255 | 0.098599 | 18.666667 | 16.666667 |
| MEGU | original | raw | r_point | 0.050000 | 3 | 0.737738 | 0.752753 | 0.073073 | 11.333333 | 7 |
| MEGU | original | raw | r_point | 0.330000 | 3 | 0.740741 | 0.647147 | 0.277277 | 39.666667 | 106 |
| MEGU | original | raw | random | 0.050000 | 3 | 0.739740 | 0.747748 | 0.073574 | 10.333333 | 8.666667 |
| MEGU | original | raw | random | 0.330000 | 3 | 0.746747 | 0.731732 | 0.108609 | 17.666667 | 27.666667 |
| MEGU | retained | matched_cs | degree | 0.050000 | 3 | 0.728228 | 0.736236 | 0.062563 | 14 | 11 |
| MEGU | retained | matched_cs | degree | 0.330000 | 3 | 0.710711 | 0.723223 | 0.093093 | 21 | 16.333333 |
| MEGU | retained | matched_cs | r_point | 0.050000 | 3 | 0.739239 | 0.753754 | 0.059059 | 13 | 9.333333 |
| MEGU | retained | matched_cs | r_point | 0.330000 | 3 | 0.741742 | 0.650651 | 0.225726 | 29.333333 | 91 |
| MEGU | retained | matched_cs | random | 0.050000 | 3 | 0.738238 | 0.745746 | 0.061562 | 11.333333 | 12.333333 |
| MEGU | retained | matched_cs | random | 0.330000 | 3 | 0.727728 | 0.713213 | 0.107107 | 14.666667 | 29.666667 |
| MEGU | retained | published | degree | 0.050000 | 3 | 0.728228 | 0.736236 | 0.062563 | 9.333333 | 7.666667 |
| MEGU | retained | published | degree | 0.330000 | 3 | 0.710711 | 0.723223 | 0.093093 | 16.333333 | 14 |
| MEGU | retained | published | r_point | 0.050000 | 3 | 0.739239 | 0.753754 | 0.059059 | 7.333333 | 4.333333 |
| MEGU | retained | published | r_point | 0.330000 | 3 | 0.741742 | 0.650651 | 0.225726 | 23.333333 | 84 |
| MEGU | retained | published | random | 0.050000 | 3 | 0.738238 | 0.745746 | 0.061562 | 7.333333 | 7 |
| MEGU | retained | published | random | 0.330000 | 3 | 0.727728 | 0.713213 | 0.107107 | 12 | 24.666667 |
| MEGU | retained | raw | degree | 0.050000 | 3 | 0.727728 | 0.736236 | 0.074074 | 9 | 9 |
| MEGU | retained | raw | degree | 0.330000 | 3 | 0.717718 | 0.723223 | 0.108108 | 18 | 18.666667 |
| MEGU | retained | raw | r_point | 0.050000 | 3 | 0.739740 | 0.753754 | 0.065065 | 8.333333 | 4 |
| MEGU | retained | raw | r_point | 0.330000 | 3 | 0.741742 | 0.650651 | 0.233734 | 25.333333 | 88.666667 |
| MEGU | retained | raw | random | 0.050000 | 3 | 0.738739 | 0.745746 | 0.068569 | 8 | 6.666667 |
| MEGU | retained | raw | random | 0.330000 | 3 | 0.737237 | 0.713213 | 0.102102 | 12.333333 | 27.666667 |
