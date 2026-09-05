# AAGU-015 · Selector 配置、输出与复用覆盖

当前验收按用户明确的三项关注组织：配置与指标正确；主阶段为纯 Selector；产出分数排名，并通过小测试确认未来 GU 可以命中已有结果。完整实验、真实输入绑定及独立 Retrain 不作为本次完成条件。

## 配置与指标

已由实际 parser 检查 18 份 Stage S 大表：Cora/CiteSeer/PubMed × 三个训练 seed × 两种预算，每表 17 个 Selector，总计 306 cell。全部为 stage=selector，无 Unlearning 配置及 GU Evaluation 引用。449 份源/生成 YAML 在本次验证前后逐文件哈希相同。

Dataset/Split 为持久化 70/10/20、split seed 2024；候选为 train_mask，validation-conditioned 方法的目标为 validation_mask。训练 seed 与 split seed 分开，预算以实际训练候选数为分母。真实 manifest 尚未绑定属于正式运行准备，不是读取能力缺失。

Selector 评价使用 Spearman、Kendall、common fraction、Jaccard 和计算/读取时间，比较的是候选分数向量、排序及 top-K 集合。Q1–Q4 的比较对象与控制见 [方案](EXPERIMENT_PLAN.md)。现有 [pair_metrics](../../../experiments/c_target_v1/core.py) 已在小测试中实际消费 40 组输出，并通过已知同序/逆序向量核对。Stage S 不引用 F1 或 retrain-gap；这些属于未来 GU 评价。

## 真实分数与排名产物 — PASS

[CPU 软件回执](evidence/selector-reuse-check.json) 使用 20 节点、14 个训练候选的小图运行全部 17 个 Selector。每个方法得到 14 个有限分数、覆盖候选空间的完整排序及 top-K Selection。排序与 score 降序/node ID 升序规则一致；读取真实 Selection Artifact 后，选点与排名前 K 个节点相同。

[分数排名 CSV](evidence/selector-score-rank-example.csv) 有 238 行，字段为 selector、node_id、score、rank、selected。它是可复核的软件验证样例，不是 Cora/CiteSeer/PubMed 的研究结果。正式产物应同样保留完整 candidate IDs、scores、ranking 和精确身份。

## 后续 Unlearning 复用 — PASS

- Selector warm：禁止 Score / Selection producer 后，17 个方法的 Score 与 Selection 全部 HIT；分数、排名和 Artifact 引用与首次相同。
- 已有 Selection→GU：取同一 p_point Selection，禁止整个 Selector 调用，再执行真实 GNNDelete 和 GIF。两种 GU 首次 MISS、再次 HIT；已有 checkpoint 也命中，未重算 Selector。
- 保留 Selector 引用的后续组合：同一 p_point selector_ref 加上两个 GU，Score、Selection 与 GU 均 HIT；可以复用前一阶段的输出。
- 错误身份：修改 Selection content_hash 后，消费者在 GU 和结果文件写入前拒绝。

本次实际验证的是节点删除、现有 GNNDelete/GIF 消费者以及相同数据/配置/模型条件。未验证的所有未来模型、GU 或跨设备物理缓存不据此宣称支持。

## 与这次验收分开的事项

独立 Retrain / Metrics 只读复用此前没有被代码实现，现由主项目 AAGU-028 承接。普通 modular 的 retrain-gap case 仍不在本次测试范围；已有 target-direct 固定 GNNDelete 路径不能代表所有未来组合。Stage U 文件保留未来设计，不把本次测试降成一次完整 Stage U 评价。

SM-005 曾观察到 GU 结果冷/热读取的 f1_drop 舍入差异。本次小图虽然输出相等，也不能推翻该已复现缺陷；它属于结果数值复用修复，不影响本次观察到的 Selector 分数/排名精确 HIT。测试不替代该修复的验收。

正式数据绑定、GPU 设备/job、成本和完整研究结果属于运行准备及获批后执行，不能称为 026 的漏实现或 015 未交付。纯 Selector 主阶段允许为模型型方法准备 checkpoint；不要求阶段本身执行 GU。

## 证据与复核

- [可重跑 CPU 验证器](evidence/verify_selector_reuse.py)：从实际 Selector 小表构造缩小的隔离测试实例，用原生产消费者执行；不修改生产实现或正式配置。
- [本次回执](evidence/selector-reuse-check.json)：fixture/覆盖值、代码与验证器身份、每方法 HIT、GU 复用和历史目录保护。
- [Selector 指标样例](evidence/selector-comparisons-example.json)：40 组 Q1–Q4 小图输出；不作科学效果结论。
- [已有定义展开](evidence/definition-summary.json)、[306 个 S cell](evidence/stage-s-cells.csv)：配置事实；其中 execution_ready=false 描述正式输入准备，不代表材料未完成。
- [此前入口核对快照](evidence/capability-audit.json)：保留当时 27 个 WorkItem 与源码的历史事实；Retrain 的当前登记更新以主项目 AAGU-028 为准。
