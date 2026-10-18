# Before 来源核验：单 shard，还是完整 ensemble？

2026-10-18 · EXP-079/e79r5 · 只读核验，未训练或修改缓存

**结论：当前图中的 Cora before 来自完整初始 ensemble，未复现“最后一个 shard 被当成 before”的问题。GraphRevoker 的低起点是真实保存在这一批 checkpoint 中的表现，但原因和配置代表性尚未核实。** 不能把“数值可复算”扩大成“实现和实验配置已经合理”。

## 1. 本轮实际核验了什么

1. 按 run.json 的精确 Output 身份读取两种分片方法、三数据集、十 seed 的 60 个 D-full/GCN 条件，核对 Output 文件哈希与绑定 Dataset/Split，直接从保存的 logits_before 和测试标签计算准确率。60 个结果均与回传 metrics.json 一致。
2. 按 Output 内的 ensemble_state_hash 查找对应初始 checkpoint，核对 method、training、parameters 和 data identity，没有用当前默认参数重新训练。
3. 对 Cora 的 20 个初始 checkpoint 核验文件及 state 哈希，加载全部十个 shard、assignment 和聚合 weights，在 CPU 上重新前向。20 组 ensemble 的测试预测均与保存的 before 完全一致（每组 542 个测试节点，类别预测不一致数均为 0）。CPU/GPU 浮点输出最大绝对差为 7.62939e-06，未改变测试 argmax。
4. 同时分别计算每个 shard 的结果，以及使用相同 shard、改为均匀权重的聚合诊断。后者仅用于排查，不替换正式指标、不重训、不写回 Cache。

CiteSeer/PubMed 的 40 组只核对保存预测和初始 checkpoint 身份，未独立前向重算。完整原始证据在 [before_audit.json](before_audit.json)，只读脚本为 [audit_before_remote.py](audit_before_remote.py)。

## 2. 图里的数值与单 shard 数值有明显区别

![Cora：单 shard、保存 before、重算 ensemble 与均匀聚合](before_checkpoint_audit.png)

橙色空心圆是保存的 before，绿色加号是从初始 checkpoint 重算的完整 ensemble；两者重合。灰点是各单 shard，蓝横线是均匀权重诊断。

| 数据集 | 方法 | 十 seed before 均值 | 最低 seed | 最高 seed |
| --- | --- | --- | --- | --- |
| CiteSeer | GraphEraser | 75.195 | 74.024 | 76.426 |
| CiteSeer | GraphRevoker | 72.162 | 68.468 | 74.474 |
| Cora | GraphEraser | 85.775 | 84.502 | 86.716 |
| Cora | GraphRevoker | 70.683 | 59.963 | 75.830 |
| PubMed | GraphEraser | 87.325 | 87.044 | 87.551 |
| PubMed | GraphRevoker | 86.600 | 85.700 | 86.917 |

例如 Cora / seed 42：GraphEraser 的十个 shard 为 70.11%–75.46%，完整 ensemble 为 86.72%；GraphRevoker 的单 shard 为 36.16%–72.88%，完整 ensemble 为 75.46%。这两项 before 都不是最后一个 shard 的值。

## 3. 为什么仍需要检查 GraphRevoker 的初始质量

GraphRevoker 的 Cora before 均值为 70.68%，seed 范围 59.96%–75.83%；GraphEraser 为 85.78%。对同一批 shard 使用均匀权重，GraphRevoker 的均值为 68.03%，没有简单恢复到八十多。这只能排除“换成均匀权重就能普遍修复”的简单解释，不能证明聚合实现无误。

已绑定的配置为十 shard、GCN 2 层/64 隐藏维度、3000 epochs、lr=0.05、weight_decay=0.0001；GraphEraser 使用 lpa_base，GraphRevoker 使用 gpa，后者 gpa_epochs=10；两者当前聚合均为 optimal。应进一步审查分区的节点和类别分布、分区训练充分性、shard 训练与聚合图是否符合 intended protocol，以及与原方法实验设置的差异。上述差异不等同于已确认的 bug，本轮没有改参数或启动重跑。

因此图 1 只能说：**在当前配置和 checkpoint 下，GraphRevoker 的初始 ensemble 性能较低，gap 解释必须考虑这个起点。** 暂不把它写成 GraphRevoker 的固有性质，更不据此宣称它天然不如其他 GU。

## 4. 与历史单 shard 误取问题的关系

用户指出的历史问题与既有审计记忆一致：旧 Step0 曾将最后一个 shard 的约 71.03% 当成 before，记忆中的完整聚合 before 约 84.69%。这是历史审计记录，本轮没有重新打开那次原始日志，不将其当成当前配置的正确替代值。当前 e79r5 的明确身份、保存预测及 Cora checkpoint 重算是本轮判断依据。

## 5. 全部 Cora 逐 seed 核验结果

| 方法 | seed | 保存的 before | 重算 ensemble | 单 shard 最低 | 单 shard 最高 | 最后一个 shard | 均匀聚合诊断 | 测试预测不一致数 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GraphEraser | 42 | 86.716 | 86.716 | 70.111 | 75.461 | 74.354 | 86.716 | 0 |
| GraphRevoker | 42 | 75.461 | 75.461 | 36.162 | 72.878 | 56.089 | 71.033 | 0 |
| GraphEraser | 212 | 86.531 | 86.531 | 67.343 | 73.985 | 72.140 | 86.347 | 0 |
| GraphRevoker | 212 | 66.790 | 66.790 | 15.867 | 70.664 | 39.668 | 65.314 | 0 |
| GraphEraser | 2024 | 84.502 | 84.502 | 66.236 | 73.985 | 73.985 | 84.317 | 0 |
| GraphRevoker | 2024 | 73.432 | 73.432 | 16.605 | 61.993 | 61.993 | 69.373 | 0 |
| GraphEraser | 0 | 86.531 | 86.531 | 68.266 | 78.782 | 74.723 | 86.531 | 0 |
| GraphRevoker | 0 | 70.111 | 70.111 | 30.996 | 63.653 | 63.653 | 68.266 | 0 |
| GraphEraser | 1 | 84.502 | 84.502 | 68.266 | 74.539 | 73.063 | 84.317 | 0 |
| GraphRevoker | 1 | 61.993 | 61.993 | 23.801 | 63.100 | 43.727 | 55.535 | 0 |
| GraphEraser | 2 | 85.609 | 85.609 | 69.373 | 76.568 | 71.956 | 85.609 | 0 |
| GraphRevoker | 2 | 75.830 | 75.830 | 17.712 | 72.325 | 59.041 | 69.557 | 0 |
| GraphEraser | 3 | 84.686 | 84.686 | 66.605 | 74.723 | 66.605 | 84.686 | 0 |
| GraphRevoker | 3 | 74.908 | 74.908 | 17.343 | 62.546 | 59.225 | 75.646 | 0 |
| GraphEraser | 4 | 86.716 | 86.716 | 69.557 | 76.199 | 76.199 | 86.716 | 0 |
| GraphRevoker | 4 | 73.432 | 73.432 | 15.867 | 75.092 | 52.952 | 71.771 | 0 |
| GraphEraser | 5 | 86.162 | 86.162 | 69.742 | 74.723 | 73.616 | 85.609 | 0 |
| GraphRevoker | 5 | 59.963 | 59.963 | 15.867 | 63.469 | 43.911 | 61.255 | 0 |
| GraphEraser | 6 | 85.793 | 85.793 | 69.926 | 76.937 | 72.878 | 85.240 | 0 |
| GraphRevoker | 6 | 74.908 | 74.908 | 36.162 | 61.624 | 52.952 | 72.509 | 0 |

## 复现与影响范围

原运行 SHA：`e02b5fa40ebce66fb45e57ea23b8d6c8d7856685`。核验时远端 SHA：`5bfd9765fa0bedf17b252765e22142b209f06bef`。用于重算的 ShardEnsemble、GCNNet、create_model，以及原始 before 生成/utility 函数已与原运行版本作 AST 对照，均相同；Output 自己的生成 producer 和初始 checkpoint 身份另在 JSON 中逐项保留，不能用当前 checkout SHA 冒充最初生成版本。

本次只读 SQLite、Output、绑定数据和初始 checkpoint；不修改缓存、训练参数、远端源码或科学接受状态。新增 CPU 重算而非 GPU 训练。已回传的 before 数值无需替换；论文图注需明确“当前配置的初始 ensemble”，并保留初始质量待审阅的限制。

[逐 seed CSV](before_audit_cora.csv) · [汇总 CSV](before_audit_summary.csv) · [矢量图](before_checkpoint_audit.pdf) · [渲染脚本](render_before_audit.py) · [返回三张叙事图](STORIES.html)。
