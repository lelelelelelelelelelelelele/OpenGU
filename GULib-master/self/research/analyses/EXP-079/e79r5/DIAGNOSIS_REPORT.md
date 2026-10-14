# EXP-079：迁移规律偏窄的诊断与改进优先级

2026-10-14 · e79r5 · 完整十 seed · 本轮只读分析，无新增 GPU 实验

## 判断

**主要问题是正例覆盖窄、GCN 参照攻击经常不成立，以及攻击目标与 GU 评价之间存在距离。没有在本次核查中确认一个足以解释全体现象的实现错误。** Cora / GNNDelete / gt_full / GIN 的相对 Random 增益为 9.46 pp，不能称绝对效应很小；但不能把这一格的效果推广到其他数据集或 GU。SGC 在 PubMed 上也有正例，因此不是“只有 Cora 能攻击”，而是当前没有统一的迁移规律。

## 1. 已确认：迁移的起点经常没有攻击增益

对 GNNDelete 的六个 dataset×selector 条件，GCN 只有 **1/6** 的点态配对区间明确高于 Random，**0/6** 明确高于 Degree。区间跨零不证明无效，也不构成等效；这里的计数仅作描述，不能当成独立试验成功率。

其他 GU 的参照情况如下；小效应也会被计入，不是实用效果阈值。GIF/IDEA 的响应重合，不能当作独立复现。

| GU | 条件数 | 高于Random的点态区间 | 高于Degree的点态区间 |
| --- | --- | --- | --- |
| GIF | 6 | 3 | 4 |
| GNNDelete | 6 | 1 | 0 |
| GraphEraser | 6 | 2 | 2 |
| GraphRevoker | 6 | 3 | 2 |
| IDEA | 6 | 3 | 4 |
| MEGU | 6 | 1 | 1 |

**改进顺序：先验证 direct 选点的预测能力，再评价它的迁移。** 对 GCN 没有明确正向增益的条件，讨论 surrogate 是否产生新增益，不解释“保留比例”，也不归类为有效攻击的迁移失败。不能只增加 seed 来修复这一逻辑。

## 2. 已确认：攻击目标与最终指标没有直接对齐

当前 selector 的目标是原训练模型在 validation_mask 上的平均交叉熵，Hessian 使用训练集平均交叉熵。gt_full / r_point 没有将具体 GU 更新算子或 GU−Retrain 差距放入目标。最终主图却评价 GU 后的测试集 F1。因此，当前更接近“把模型影响选点作为 GU 压力测试”，并不天然保证最大化某个 GU 的失败。

数据也显示同一个选点请求可以有不同作用：下表中 U 是原模型到 GU 的 F1 下降；G 是 Retrain F1−GU F1；Retrain_loss 是原模型到 Retrain 的 F1 下降，满足 U=G+Retrain_loss。单位 pp。

| dataset | source | U_mean | G_mean | Retrain_loss_mean | U_vs_random_mean | G_vs_random_mean |
| --- | --- | --- | --- | --- | --- | --- |
| CiteSeer | GAT | 0.330 | 0.616 | -0.285 | 0.501 | 0.896 |
| CiteSeer | GCN | -0.195 | -0.601 | 0.405 | -0.025 | -0.320 |
| CiteSeer | GIN | -0.015 | -0.616 | 0.601 | 0.155 | -0.335 |
| CiteSeer | SGC | -0.150 | -0.495 | 0.345 | 0.020 | -0.215 |
| Cora | GAT | 17.177 | 16.716 | 0.461 | 4.262 | 3.807 |
| Cora | GCN | 20.424 | 19.705 | 0.720 | 7.509 | 6.796 |
| Cora | GIN | 22.380 | 21.716 | 0.664 | 9.465 | 8.807 |
| Cora | SGC | 15.332 | 14.797 | 0.535 | 2.417 | 1.888 |
| PubMed | GAT | 2.226 | 0.119 | 2.107 | -0.020 | -2.062 |
| PubMed | GCN | 1.790 | 0.114 | 1.676 | -0.456 | -2.067 |
| PubMed | GIN | 1.590 | 0.920 | 0.669 | -0.657 | -1.261 |
| PubMed | SGC | 8.030 | 8.233 | -0.203 | 5.783 | 6.051 |

Cora / gt_full / GIN 的 GU 损失为 22.38 pp，而 Retrain 损失仅 0.66 pp；PubMed / gt_full / SGC 的 GU 损失为 8.03 pp，而 Retrain_loss 为 −0.20 pp。这两项首先是 GU 与重训的差异，不像单纯删掉重要训练数据导致所有模型共同下降。相对 Random 的额外 G 分别为 8.81、6.05 pp。它们支持进一步研究 GU 响应，但尚未识别产生该响应的机制。

**已排查一个替代解释：不是只因 F1 粗糙才看不见 CiteSeer 的一致效果。** 从全部原始 metrics.json 补取交叉熵与分类 AUC；下面 CE_gain=攻击后 CE−Random 后 CE，AUC_drop=Random AUC−攻击后 AUC，正值才表示更坏。多数 CiteSeer 条件 CE_gain 为负，AUC_drop 全部为负；现有数据没有支持“换个指标就有统一攻击增益”。这些补充指标是事后诊断，不替换既有主指标。

| selector | source | U_vs_random_mean | CE_gain_mean | AUC_drop_mean |
| --- | --- | --- | --- | --- |
| gt_full | GAT | 0.501 | -0.038 | -0.003 |
| gt_full | GCN | -0.025 | -0.048 | -0.006 |
| gt_full | GIN | 0.155 | -0.036 | -0.003 |
| gt_full | SGC | 0.020 | 0.006 | -0.000 |
| r_point | GAT | 0.140 | -0.058 | -0.007 |
| r_point | GCN | 0.185 | -0.057 | -0.009 |
| r_point | GIN | -0.160 | -0.078 | -0.010 |
| r_point | SGC | -0.415 | 0.012 | -0.000 |

改进：区分“损害重训模型”的数据影响目标与“使 GU 偏离重训”的 GU 特定目标。先检查选点评分对小规模真实删除效果的排序预测；只有确认前者与研究目标不符，才考虑设计 GU-aware 选点，不在当前结果上直接换目标后宣布原方法成功。

## 3. 高优先级数值疑点：20 步 LiSSA 与 last_layer 的含义

已核对执行 SHA 对应实现：默认 parameter_scope=last_layer、iterations=20、scale=25、damp=0.01、affected_hops=2。更新式为 v_next=b+(1−damp)v−Hv/scale，最后除以 scale。若收敛，它对应 (H+scale×damp×I) 的逆作用，所以当前有效附加阻尼是 **0.25I**，不能把 damp=0.01 直接解释为 Hessian 上的 0.01I。

20 步是否足够取决于曲率，不能仅凭有限值判定。可手算的标量示例：假定 b 完全位于 Hessian 特征值 0、1、5 的方向，20 次更新后，对阻尼系统的相对残差分别约为 **0.810、0.341、0.007**。这是更新式的数学诊断，**不是本次 GNN 的实测谱或残差**；当前真实残差 NOT OBSERVED。

last_layer 在不同架构中也不是同样的近似范围：SGC 是单个 SGConv，选到的是其全部可训练线性参数；GCN 只包含最后一层；GIN 的最终卷积包含内部 MLP。因此架构差异与曲率近似范围存在混合。不能从 SGC 更稳定直接推出线性模型普遍更适合攻击。

优先改进：复用原 checkpoint，记录阻尼系统相对残差、梯度范数、训练/验证损失；比较 20 步与收敛参考的 score 排序及 top-k 变化。按谱/残差决定是否改 scale、damp、迭代数。增加 all_trainable 对照时固定其他条件，并报告计算代价；不以更大 F1 损伤作为求解器正确性的判据。

相关文献仅用于支持诊断动机：Koh & Liang 的 IF 工作讨论梯度/Hessian近似；Basu 等指出架构与正则化会影响 IF 准确性。它们不证明本实验已经发生相同失效。[Koh & Liang, 2017](https://proceedings.mlr.press/v70/koh17a/koh17a.pdf)；[Basu et al., ICLR 2021](https://arxiv.org/abs/2006.14651)。

## 4. 已确认：训练删边，但评估使用原图

本轮 deletion 契约为：排除选中节点的监督标签、训练图移除关联边、保留孤立特征行，**evaluation_graph=original**。当前指标衡量删除训练后的模型回到原图上的表现；它不等同于在 retained graph 上的部署性能。GU 与 Retrain 使用相同评估契约，所以这不是已确认的配对错误，但会影响图结构删除的解释。

改进：把 original 与 retained 的评估作为明确的敏感性对照，固定相同删除集和评估节点。不要悄悄改默认值覆盖已有结果。若需要执行，保存为独立评估，不并入本轮十 seed。还应检查固定两跳影响集合是否覆盖各架构的真实扰动范围；当前无法从回传内容证明完整性。

## 5. 已确认：静态单点排序一次取 10%，没有建模集合交互

当前先对原始图上的每个候选评分，再取降序前缀；不随已选节点重算。删除量为 Cora [189]、CiteSeer [232]、PubMed [1380] 个训练节点。10% 是候选训练池比例，不是仅删几个节点；单点局部影响能否预测这个批量扰动，当前未验证。

潜在问题包括重复覆盖相同邻域、类别集中，以及多个删除节点的影响相互抵消或放大。本轮未加载图数据，且回传未包含评分向量，不能把这些猜测写成事实。

改进：先对固定排序做小预算与 10% 的删除效果校准，再判断是否值得采用分批重评分或邻域去冗余。不能仅依据某种改法在已看过的测试集上更好，就选择并报告它；诊断与最终确认的 split 应分开。

## 6. 复现、SGC 稳定性与当前排除的疑点

- 本轮重新核对 run.json 及 5040 个 metrics/selection 文件哈希；2520 格请求的选点数正确、无重复节点，未发现漏格或结果错配迹象。
- 检查的 9 个实现/配置文件与执行 SHA 一致，不用后来的实现解释旧结果。SGC 的构造器在本路径明确使用标准 SGConv 分支，并未误走 GNNDelete 的两层 Linear 特殊分支。
- SGC 在 Cora/PubMed 两种 selector 下跨十 seed 选集完全相同，CiteSeer 也近乎相同。这可能符合线性模型训练收敛后的稳定性，也可能来自分数排序特性；没有模型参数/分数证据，不能宣布缓存碰撞或训练失败。10 个目标训练重复仍存在，但不是十份不同 SGC 请求。
- GIF 与 IDEA 的 F1 完全一致，补查交叉熵最大差仅约 1.01e−8；配置中两者使用几乎相同的求解参数，IDEA 噪声为零。这应作为该配置下近乎重复的响应解释，不当作两份独立防御证据。
- 所有十 seed 使用同一个 seed2024 数据划分，仍未覆盖 split 不确定性。继续加同 split 的 seed 主要缩小训练波动，不扩大数据划分适用范围。

## 下一步：先诊断，再决定是否开发更强 selector

| 优先级 | 操作 | 要回答的问题 | 当前状态 |
| --- | --- | --- | --- |
| P0 | 回传/读取原 Score 与 checkpoint 诊断；记录训练/验证性能、IHVP残差 | 是数值近似不稳，还是评分本身不预测删除效果？ | 本地未回传，NOT OBSERVED |
| P0 | 固定已有 checkpoint、选集、评估节点，比较 original/retained 评估口径 | 当前规律是否依赖评估图？ | NOT OBSERVED |
| P1 | 以稳定数值参考，校准单点/小批量预测与真实删除结果，再比较10% | 静态单点 top-k 是否在大预算下失准？ | NOT OBSERVED |
| P1 | 先检查 GCN 相对 Random、Degree 的优势，再检验 surrogate | 有没有一个可迁移的有效攻击起点？ | 本轮可直接判断，见前表 |
| P2 | 若目标错位得到证实，再研究 GU-aware 目标或集合交互处理 | 是否需要改变方法，而非仅调数值参数？ | 研究提案，未实施 |
| 确认 | 冻结方法后使用未参与诊断的 split 验证，保持完整对照 | 改进能否泛化？ | 未开展 |

**当前建议：暂时将“跨架构迁移”保留为局部结果，不再强化成核心普遍规律。优先排查数值校准与评估口径，再决定攻击目标是否需要调整。** Cora 与 PubMed/SGC 的 GU−Retrain 分离现象值得继续研究，但不能据此补写因果机制。

## 证据与复现

- [全部条件的新增指标与配对区间](diagnostic_metric_checks.csv) · [GCN参照覆盖](diagnostic_direct_coverage.csv) · [核验记录](diagnosis_verification.json)
- [分析脚本](diagnose.py) · [原完整分析](REPORT.html) · [当前展示图解](OVERVIEW_REPORT.html)
- [IF默认与目标](../../../../../experiments/target_direct_v1/methods.py) · [数值更新实现](../../../../../experiments/c_target_v1/core.py) · [删除与评估契约](../../../../../experiments/node_deletion.py)
- 从仓库根运行：`python -B -X utf8 self/research/analyses/EXP-079/e79r5/diagnose.py`。输入固定于 `e02b5fa40ebce66fb45e57ea23b8d6c8d7856685` 对应 e79r5；新的 GPU 实验数为 0。科学接受状态不变。
