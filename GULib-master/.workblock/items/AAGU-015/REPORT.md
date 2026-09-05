# AAGU-015 · Selector 配置、分数排名与复用验证

## Human Result

### 实际增量

已把本轮验收聚焦为纯 Selector 实验：配置与指标正确，输出完整分数排名，并用一个隔离 CPU 小测试确认未来 Unlearning 能复用这些结果。原有 449 份 YAML 保持不变；Q1–Q4 共享 Stage S 计算，Stage U 保留未来设计。

### 核心观察

- **PASS · 配置与指标**：18 份 Stage S 大表均为纯 Selector，覆盖三个数据集、17 个方法、三训练 seed、两预算。候选来自 train_mask；需要验证目标的方法使用 validation_mask。Selector 指标为 Spearman/Kendall、common fraction/Jaccard 和成本；没有 GU 或 F1/retrain-gap 引用。
- **PASS · 分数与排名**：20 节点 CPU 小图有 14 个候选；17 个方法各输出 14 个有限分数及完整排名，共 238 行。top-K 与持久化 Selection 一致，完整分数/排名已提供 CSV 示例。
- **PASS · Selector 缓存**：再次运行时禁止 Score/Selection producer，17 个方法均 HIT；分数、排名和 Artifact 引用逐项相同。
- **PASS · 未来 GU 复用**：同一 p_point Selection 交给真实 GNNDelete/GIF，禁用 Selector 调用；两种 GU 首次 MISS、再次 HIT，checkpoint 也命中。保留相同 selector_ref 的组合计划同样全部 HIT。错误 Selection 哈希在 GU 前被拒绝。

### 当前决定

> 当前验收决定：`接受`

Agent 建议接受 015 当前范围：Selector 方案、实际配置、分数排名输出及未来 GU 复用小测试。由用户明确接受或返工；本次不要求跑正式矩阵，也不以独立 Retrain / 完整重训练评价的实现作为验收条件。

## 实验配置与 Selector 指标

- Dataset：Cora、CiteSeer、PubMed；持久化 train/val/test=70/10/20；split seed 2024。真实 manifest 尚未绑定属于未来运行准备。
- 候选与目标：train_mask 为候选；需要验证目标的 Selector 使用 val_mask，test 不参与选点目标或调参。
- 模型：模型型方法使用 GCN 两层、hidden=64、dropout=0.5；训练 100 epochs，Adam，lr=0.005，weight decay=0.000001；seeds=42/212/2024。degree/random 不需要模型。
- 预算与排序：训练候选的 1%/5%，K=max(1,floor(N_train×ratio))；score 降序、同分按 node ID 升序。
- Selector 数值条件：last_layer；LiSSA 20/25/0.01，B-Hutch 32 probes；CP3=[1,50,100]，CP6=[1,10,25,50,75,100]。random seed 固定为 104245，不能将跨训练 seed 的相同抽样当独立样本。
- 指标输入：Spearman/Kendall 使用按候选 ID 对齐的原始分数，common fraction/Jaccard 使用同候选同 K 的 top-K 集合；无定义的相关性保留为空。成本区分模型准备、计算和读取。

## Q1–Q4

- Q1：省略 Hessian 后是否仍选到相似节点？比较 A/B 及各 source 的 Hessian-free proxy 与 IF/GIF 参考。
- Q2：point/simple/graph source 改变带来什么差异？分别在相同 Hessian 处理下作组内比较。
- Q3：参数变化与验证目标是否选择相同节点？比较 A/B 与 IF/GIF 参考，附 degree/random/legacy 控制。
- Q4：final、CP3、CP6 有何差异？同时报告轨迹变化及对同 source final 参考的一致性。

## 最终输出

- Score：candidate IDs、逐候选 scores、完整 ranking，以及数据/模型/方法与 Artifact 身份。
- Selection：按预算派生的 selected_nodes，引用同一 Score，并保留 recipe/content hash；后续 GU 直接使用这份 Selection。
- 本次样例：17×14=238 行 selector/node_id/score/rank/selected；40 组 Q1–Q4 指标输出验证分析接口，不作为方法优劣的研究结论。

## 未来 Unlearning 如何复用

- Score/Selection 冷运行：17 个方法全部 MISS 并实际计算；热运行全部 HIT，明确禁止 producer 调用。
- 后续只引用已有 Selection：p_point→GNNDelete 和 p_point→GIF 均无需 Selector；两种 GU 第一次 MISS，第二次 HIT。
- 后续仍引用同一个 Selector：p_point 的 Score、Selection 与两个 GU 均 HIT，不重复选点。
- 复用条件：真实 Dataset/Split、候选、模型/训练/checkpoint、Selector 参数、删除请求和相关实现身份匹配。只换实验名称不会强迫重算；改变真实依赖不能假定 HIT。

## 分数排名样例

以下仅为 CPU 小图 p_point 的前六名。

```csv
selector,node_id,score,rank,selected
p_point,11,0.05307590961456299,1,True
p_point,13,0.05153393745422363,2,False
p_point,9,0.050595883280038834,3,False
p_point,3,0.050047557801008224,4,False
p_point,1,0.04927053302526474,5,False
p_point,5,0.047859370708465576,6,False
```

## 验证范围

小测试使用 20 节点、14/2/4 三个 mask，hidden=4、训练 6 epochs、CP steps=1–6、LiSSA 2 次、Hutchinson 2 probes、GU 各 2 次迭代。全部运行于独立 CPU 测试目录；正式 YAML 与受保护的既有数据/缓存/结果保持不变。它证明本次接口和复用能力，不是三个真实数据集的全矩阵运行。独立 Retrain 与完整 GU Metrics 由 AAGU-028 承接；此前 GU 冷/热指标舍入缺陷不因这次小图通过而被判定修复。

配置 parser/dry-run 再次检查 18 份 S / 306 份未来 U 计划；449 份 YAML 哈希不变。新增真实消费者测试由回执中的 consumer_source_head、consumer_hashes 和 verifier_sha256 标识；分数排名与 Q1–Q4 示例由该测试生成。未修改生产算法、方法分发、缓存实现或正式实验配置。报告与方案文件发生变化，原配置回归只在实际差异不能改变其结论时复用。

HTML 首屏已在 1440×1100 桌面与 600×1800 窄屏渲染查看，标题、配置与决定区可读，无可见重叠或横向截断；完整页面证据保留在本次 Verify。

## 证据入口

- [Q1–Q4 实验设计总表](EXPERIMENT_PLAN.md)
- [Stage S 配置源表](../../../experiments/configs/aagu015/stage_s.yaml)
- [18 张具体计划与生成命令](../../../experiments/configs/aagu015/README.md)
- [306 个 Selector 配置单元](evidence/stage-s-cells.csv)
- [238 行分数排名样例](evidence/selector-score-rank-example.csv)
- [Q1–Q4 指标输出样例](evidence/selector-comparisons-example.json)
- [真实 HIT / producer / 身份验证回执](evidence/selector-reuse-check.json)
- [可重跑 CPU 验证器](evidence/verify_selector_reuse.py)
- [能力与本次验证范围](CAPABILITY_COVERAGE.md)
- [WorkItem](WORKITEM.md)
