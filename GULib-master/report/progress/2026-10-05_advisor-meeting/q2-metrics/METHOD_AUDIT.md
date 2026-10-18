# GraphRevoker 方法审计：当前 70.68% 对应哪个实现？

2026-10-19 · EXP-079/e79r5 · 原论文、上游 OpenGU、当前 adapter、精确 checkpoint 对照

**结论：当前实验没有运行原论文完整的 GraphRevoker。最明确的问题是当前 adapter 将聚合器固定为 GPA + optimal，缺少论文的特征投影、逐节点注意力和对比/重构聚合模块。70.68% 是这个配置版本的真实输出，不是原方法已经合理复现的证据。** 冻结分区与子模型、替换聚合头的预先固定对照只提高到 72.93%，不能宣称全部精度差距已经归因，或修复后一定达到八十多。

## 1. 原论文和执行链在哪里不一致

论文 §4.2 定义特征投影、节点相关注意力及分类、对比、重构联合训练；附录 A.1 给出聚合 AdamW lr=0.01、decay=1e-5，并采用 20 shard、100 个子模型训练 epoch。论文为 inductive、70/20/10 划分，当前为 transductive、70/10/20；不能直接用论文表中精度作为本实验必须达到的阈值。[原论文](https://arxiv.org/html/2403.07353v1#S4.SS2)

| 核查对象 | 当前真正执行的行为 | 判断及证据 |
| --- | --- | --- |
| 聚合器入口 | YAML 设置 `optimal`；`validate_graphrevoker` 拒绝 `contrastive` | 明确缺少完整方法模块，不是只有图例名称不同。[配置](../../../../experiments/configs/unlearning/graphrevoker.yaml)、[adapter](../../../../experiments/modular_graphrevoker.py) |
| 聚合输入与容量 | 每个 shard 的类别 log-probability；十个全局标量权重，与节点无关 | 不是特征投影与逐节点注意力。[ShardEnsemble.forward](../../../../experiments/modular_shards.py) |
| 聚合训练目标 | `cross_entropy(softmax(weighted_logp), labels) + norm(weights)`；Adam lr=.001、20 epochs | 当前运行没有对比与重构项；不是“contrastive 已实现但辅助项权重较小”。[OptimalAggregator](../../../../unlearning/unlearning_methods/GraphRevoker/lib_aggregator/optimal_aggregator.py) |
| 已有 contrastive 代码 | 仓库存在 ContraAggr / ContrastiveAggregator，但当前 adapter 完全未调用 | 此三个类的 AST 与固定上游 OpenGU commit 一致；代码存在不等于实验使用。[上游固定版本](https://github.com/bwfan-bit/OpenGU/blob/475e045a65fd8176dabd8fd66be69669d5509bf7/GULib-master/unlearning/unlearning_methods/GraphRevoker/lib_aggregator/contra_aggregator_v2.py) |
| 子模型训练 | Adam、lr=.05、weight_decay=.0001、3000 epochs；用最终权重，无验证集选 checkpoint | 与当前 checkpoint 元数据一致；不是论文完整设置。lr/.05 和 decay/.0001 来自 OpenGU GCN 配置，不能无来源地称为原作者参数。[训练](../../../../experiments/c_target_v1/core.py)、[GCN 配置](../../../../model/properties/GCN.yaml) |
| 子模型结构 | 两个 GCNConv：输入→64→7；没有独立 MLP 分类头；`return_feature` 为第一个卷积的 64 维输出 | 原论文描述两层消息传递加 MLP；当前是 OpenGU GCN 适配，不能称为结构逐项一致。[GCNNet](../../../../model/base_gnn/gcn.py) |
| 分区输入 | 独立训练完整分类器，使用训练节点的 log-softmax 输出 | 与本地旧 OpenGU NodeEmbedding 语义相近；不能把它描述成论文已明确要求的原始特征输入。 |
| 分区目标与后处理 | Ncut + .001×正熵 + .001×eff_norm；argmax 后按容量上限重新分配 | 主体来自 OpenGU。eff_norm 采用节点比例平方与边比例乘积的立方根，不是论文时间目标的原式；该差异不是当前报告新改出的。 |
| 聚合训练/推断图 | 聚合训练在 1000 个采样训练节点的诱导图上提特征；最终推断按各 shard 的过滤图计算 | 当前 optimal 和上游 contrastive 数据准备都采用这种不同上下文；只能登记协议差异，不能直接断言它导致本次掉点。 |

方法缩减可追溯到本地 adapter 引入提交 `6c6703b4`，它从一开始就只支持 `gpa / optimal`；这不是画图或回传时才产生的错误。尚未核验到原作者独立发布的代码仓库，本轮的源码对照对象明确是 **OpenGU 上游实现**，不能冒称作者官方实现。上游固定 commit 为 `475e045a65fd8176dabd8fd66be69669d5509bf7`，URL、文件哈希、类级 AST 比较见 [来源清单](method_upstream_sources.json)。

## 2. 用相同 checkpoint 检验聚合替换，不重训 shard

问题：保留当前分区和十个 shard 的全部权重，只更换聚合头，是否足以消除低 before？

设计在执行前固定：Cora 的全部十 seed；每个 seed 从原训练 mask 中随机抽 1000 节点，诊断 seed=9000+原训练 seed；20 epochs、AdamW lr=.01、decay=1e-5、batch512、投影128/注意力16。使用上游一致的 ContraAggr 和负采样代码，按排序后的真实节点索引绑定 shard id。两臂使用相同样本、初始聚合头、批次顺序与 mask，分别是分类损失和分类+1e-4×对比+1e-4×重构；保留代码中 mask 的 19 次有放回抽样。测试与验证结果只在固定最后一轮读取，不用于选参数或 epoch。

| 聚合方式 | 十 seed 测试精度均值 % |
| --- | ---: |
| 原 checkpoint 的 optimal 聚合 | 70.683 |
| 注意力聚合头，仅分类训练 | 72.878 |
| 注意力聚合头，分类+对比+重构 | 72.934 |

完整聚合头相对当前 baseline 的配对平均差为 **2.251 pp**，点态 95% t 区间 **[-1.334, 5.836] pp**；7/10 seed 提高，3/10 下降。区间跨零，不能称为已验证的稳定改善。两个新聚合头的均值接近，也不支持把这批低精度主要归因于漏掉两个辅助损失。

这控制住了分区、子模型、数据和评估节点，但“旧 optimal → 新聚合头”同时改变结构、损失、优化器及学习率，属于**整个聚合模块的替换对照**，不能把全部差值归给注意力或某一损失。新头复用当前 OpenGU GCN 特征；并未恢复原论文的模型结构、分区或完整训练协议，因此也不是完整 GraphRevoker 复现。只有两臂之间的比较进一步控制了聚合结构与优化设置。

| seed | baseline | attention_ce | attention_full | delta |
| --- | --- | --- | --- | --- |
| 42 | 75.461 | 77.491 | 78.044 | 2.583 |
| 212 | 66.790 | 69.373 | 70.111 | 3.321 |
| 2024 | 73.432 | 71.218 | 72.140 | -1.292 |
| 0 | 70.111 | 73.985 | 72.509 | 2.399 |
| 1 | 61.993 | 69.742 | 70.480 | 8.487 |
| 2 | 75.830 | 74.908 | 74.354 | -1.476 |
| 3 | 74.908 | 69.557 | 69.373 | -5.535 |
| 4 | 73.432 | 74.723 | 73.801 | 0.369 |
| 5 | 59.963 | 72.325 | 71.956 | 11.993 |
| 6 | 74.908 | 75.461 | 76.568 | 1.661 |

## 3. 训练到底有没有拟合上

对相同十个初始 checkpoint 作额外只读前向，统计每个 shard 在**自己参与训练的节点**上的结果，以及固定完整 test mask 上的结果。所有 shard 等权汇总；这些 100 个 shard 不是 100 次独立运行。

| 检查 | 准确率均值 % |
| --- | ---: |
| 分区前完整 encoder：完整测试集 | 89.889 |
| 每个 shard：自己的训练节点 | 99.403 |
| 每个 shard：完整测试集 | 46.854 |
| 当前 shard ensemble：完整测试集 | 70.683 |

完整 encoder 表现正常，shard 也已高度拟合自己的监督样本。因此不能用“模型没有训练”“before 只是未初始化模型”或“shard 没学会训练样本”解释 70.68%。单 shard 对完整测试集的准确率低不自动构成 bug：分工后的模型可以互补；本轮也没有把缺类当作精度下降的因果证据。这些终态 checkpoint 无法告诉我们 100、500 或 1000 epoch 的精度轨迹，不能把 3000 epochs 直接判成过拟合原因。

## 4. 正熵方向：代码行为可证，原作者意图仍有歧义

原论文文字希望保留标签多样性，但式(3)/(7)写正熵并放入最小化目标，文字和公式方向冲突。OpenGU 与当前 LabelEntropyLoss 类的 AST 一致：都计算正熵并最小化。因此我之前称“GPA 本来就要让类别集中”不严谨——只能确认**当前代码**会这样优化，不能替作者确定意图。[论文 §4.1](https://arxiv.org/html/2403.07353v1#S4.SS1)

用实际 LabelEntropyLoss 做最小反例：四节点、两类别、两 shard，均匀混合分区损失为 0.693147，按类别分离约 0.00006604。最小化会更偏好后者；这是目标方向的数值核验，不是 Cora 精度下降的归因实验。不能悄悄翻转符号再沿用旧结果身份。[探针](entropy_direction_probe.py)

## 5. 对当前论文和后续修复的影响

- 图中这批 GraphRevoker 应标明为 **GPA + optimal 的当前配置版本**，不能作为原论文完整方法的优劣证据。原预测数值保留，不用新聚合头结果替换正式 before。
- 最小完整修复不是把 YAML 从 optimal 改成 contrastive：当前验证器拒绝它，输出/恢复路径也只保存和恢复标量权重，必须接入聚合头训练、状态保存、before/after、重训及恢复一致性。
- 分区正熵方向、模型结构和训练协议应单独形成明确选择与受控对照；一次只改一个层面，才能判断剩余精度差距来自哪里。本轮没有改正式 adapter、配置或运行队列。
- 科学受影响对象应按实际 adapter 与参数身份核定，不把全部历史“GraphRevoker”一概判成同一问题；其他方法不因本次审计自动失效。当前审计精确绑定的是 EXP-079/e79r5 的 Cora 十个初始 ensemble。

**审计回答：原方法没有完整实现到当前执行链中；这点已确认。为什么恰好是 70.68%，目前没有能解释全部差距的单一因果结论。冻结 shard 的替换实验反而说明，单独补聚合头不足以宣称问题已解决。**

## 证据与执行边界

CPU 两线程，20 个内存聚合拟合，零 shard/encoder 重训；没有创建或改写远端模型、Cache 或正式结果。聚合对照耗时 46.2s。最初一次校验在训练前因 Python 3.13/3.10 AST 表示差异停止，改用换行归一化源码哈希后通过；失败日志保留，没有调参或择优重跑。当前远端 SHA：`a217daf5c67b485afed63c393b5e8bb23820b237`；原输出执行 SHA：`e02b5fa40ebce66fb45e57ea23b8d6c8d7856685`。

[聚合对照 JSON](aggregation_audit.json) · [训练拟合 JSON](training_audit.json) · [逐 seed CSV](method_audit_paired.csv) · [聚合诊断脚本](audit_aggregation_remote.py) · [训练前向脚本](audit_training_remote.py) · [原 before 核验](BEFORE_AUDIT.html) · [返回叙事图](STORIES.html)。
