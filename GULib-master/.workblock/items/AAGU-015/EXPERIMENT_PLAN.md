# AAGU-015 · 当前阶段实验方案与配置映射

本文件是 AAGU-015 的本轮验收材料：把已经讨论的两阶段研究问题对应到实际 YAML、比较设计和指标输入。理论背景与历史研究记录仍由 [OpenGU DocMap](E:/project/OpenGU-DocMap/10_实验矩阵/20_IF目标层级对比实验计划.md) 拥有；本文件不沿用其中旧实验的结果、public split、固定小 K、18 方法或训练超参数作为本轮证据。

本轮交付实验方案、对应配置及能力覆盖检查。范围是当前 Stage S / Stage U，不是所有未来实验；配置检查通过也不表示运行准备或科研验证通过。具体实现边界见 [能力覆盖说明](CAPABILITY_COVERAGE.md)，本次决定见 [报告](REPORT.md)。

## 1. 两阶段问题与依赖

Stage S 比较 Selector 的评分、排序、选集与成本，不运行 GU。先固定这一阶段的配置、分析规则和 Selection 身份，再进入 Stage U。

Stage U 对同一个 Selection 分别执行 GNNDelete、GIF，并与同删除请求的完整重训练参照比较。研究问题是：Selector 的选择差异是否对应效用和遗忘近似误差的差异。Stage U 指标不回流调整本轮 Selector；若据此改方法或参数，应形成后续研究轮次。

Retrain 在研究设计中是执行删除请求得到参照模型的操作。Metrics 消费模型输出；它不应为了每个指标重新训练。当前代码尚未把 Retrain 注册为独立 Unlearning 小表方法，这一能力缺口在本方案中显式保留，不伪造可执行的 `method: Retrain` 配置。

## 2. 固定条件与实际配置

配置入口：[Stage S](../../../experiments/configs/aagu015/stage_s.yaml)、[Stage U](../../../experiments/configs/aagu015/stage_u.yaml)、[生成与检查命令](../../../experiments/configs/aagu015/README.md)。方法小表声明选择与覆盖值，未填写的默认值由方法所有者展开；[有效参数与配置哈希](evidence/definition-summary.json) 是本次检查快照。

| 轴 | 本轮定义 | 比较时保持一致的条件 |
|---|---|---|
| 数据集 | Cora、CiteSeer、PubMed | 持久化图、预处理、节点编号及实际文件身份 |
| 划分 | train/val/test = 70/10/20；split seed 2024 | 模型 seed、Selector 和 GU 改变均不得重新切分 |
| 候选 / 目标 | 候选是 train_mask；validation-conditioned 方法的目标为 val_mask | test 不参与 Selector 的目标或参数选择 |
| 模型 | GCN 两层、hidden 64、dropout 0.5 | 同一比较单元使用相同模型与实际 checkpoint |
| 训练 | seeds 42、212、2024；100 epochs；Adam；lr 0.005；weight decay 0.000001；无 scheduler | Selector 与 GU 的训练配置分别展开，配置相同不直接证明 checkpoint 相同 |
| 参数范围 | last_layer | 不混入 all_trainable 历史结果 |
| 预算 | 训练候选数的 1% / 5%；K=max(1,floor(N_train×ratio)) | 同预算、同候选池比较；节点总数不是分母 |
| 排名 | score 降序；相同 score 按 node ID 升序 | 保留原始有限分数及完整候选顺序 |
| LiSSA / Hutchinson | iterations 20、scale 25、damp 0.01；B 使用 32 probes / seed 1729 | 只对消费这些参数的方法生效 |
| checkpoint 视图 | CP3=[1,50,100]；CP6=[1,10,25,50,75,100] | 按真实 global_step 取值；保留对应 update_lr |
| 控制 | degree、random；random seed 104245 | random 不随训练 seed 产生三次独立抽样，不将重复观察当独立样本 |
| GU | GNNDelete：lr 0.01、50 epochs、alpha 0.5、mse_mean/both_layerwise；GIF：iteration 100、scale 1e9、damp 0、GIF_method=GIF | 同 Selection 下只改变声明的 GU 配置，不能重新选点 |

| 数据集 | 节点数预期 | train 候选数预期 | 1% K | 5% K |
|---|---:|---:|---:|---:|
| Cora | 2708 | 1895 | 18 | 94 |
| CiteSeer | 3327 | 2328 | 23 | 116 |
| PubMed | 19717 | 13801 | 138 | 690 |

上表是配置预期。运行前必须从持久化 mask 读取实际 count/hash；当前三份 Dataset YAML 的 manifest 和哈希仍为空，不由此推断远端数据不存在，也不自动下载、重切或绑定。SM-005 已有 Cora 输入与运行证据，其是否可用于某个 015 单元取决于实际输入与计算身份的一致性。

## 3. Stage S：17 个 Selector 的比较设计

记 g_v 为候选训练节点的梯度，g_E 为验证目标的平均梯度；point/simple/graph 分别使用 point、grad1、grad1−grad2 source。这里的 H⁻¹ 表示当前数值求解器的近似作用，不宣称显式精确逆矩阵。

| 组 | 配置方法 | 本轮作用 |
|---|---|---|
| 控制 | degree、random | 拓扑及随机选择参照 |
| 参数变化 | a_grad_norm、b_param_hutch | 梯度范数与曲率修正后的参数变化范数估计；不含验证目标 |
| IF/GIF 参考 | r_point、gt_simple、gt_full | point/simple/graph source 与 H⁻¹g_E 的投影 |
| Hessian-free | p_point、p_simple、p_graph | 对应 source 与 g_E 的直接投影 |
| checkpoint 累积 | tracin_cp_point_3、tracin_cp_point_6、tracin_cp_simple_3、tracin_cp_simple_6、tracin_cp_graph_3、tracin_cp_graph_6 | 同 source 的 3/6 checkpoint 加权累积；simple/graph 是本项目定义的扩展 |
| 历史方向控制 | legacy | 当前部署的训练方向交叉梯度定义；只作负向/历史对照 |

方法定义以 [methods.py](../../../experiments/target_direct_v1/methods.py) 的当前实现为准。D-full (`gt_full`) 是本轮 GIF 定义下的操作性参考；与它一致不等于数学正确、精确重训练一致或攻击效果更强。

| 问题 | 主要比较 | 输出与解释 |
|---|---|---|
| Q1：省略 Hessian 后选择有多一致？ | a_grad_norm ↔ b_param_hutch；p_point ↔ r_point；p_simple ↔ gt_simple；p_graph ↔ gt_full | 全候选 Spearman/Kendall；同 K 的 common fraction/Jaccard。A/B 比较是参数变化估计的一致性，不与 validation-conditioned 目标混称同一量 |
| Q2：source 改变会改变哪些选择？ | r_point、gt_simple、gt_full 组内成对比较；p_point、p_simple、p_graph 组内成对比较 | 固定 Hessian 处理和 checkpoint，比 point/simple/graph；不能把 source 与求解器同时改变后归因给一个因素 |
| Q3：参数变化和验证目标是否选到相同节点？ | A/B 分别与 r_point、gt_simple、gt_full 比较；附 degree/random/legacy 控制 | 报告选集差异及目标定义差异；方向性效果留给 Stage U，不用 score 数值跨量纲比较大小 |
| Q4：final 与 checkpoint 累积有什么差异？ | 每种 source 的 final proxy、CP3、CP6 三者成对比较；分别对同 source 的 final IF/GIF 参考报告一致性 | 区分“跨 checkpoint 改变”与“对参考的一致性”；CP6 更好是待检验命题，不是默认结论 |

完整 17×17 成对摘要可作为补充查阅；主报告按上述问题组织，避免从大量比较中事后挑选最好的一对。每对必须共享 dataset/split/candidate、模型 seed、预算和适用的 checkpoint 条件。

### 排名、选集与成本口径

- Spearman/Kendall：对齐同一候选节点顺序后，比较原始 score 向量。常量向量或指标无定义时记为缺失并说明原因；不能用零或一填补。稳定排序的 tie-break 不等于原始 score 没有并列值。
- common fraction = |S_a∩S_b|/K；Jaccard = |S_a∩S_b|/|S_a∪S_b|。只有候选空间和 K 一致时作对应比较。
- 每个数据集分别展示三个训练 seed 的值与描述性均值/离散程度；三 seed 不自动构成显著性结论。degree/random 的共享结果标明复用。
- 计时分开记录模型/checkpoint 准备、共享中间计算、cold score compute、warm access、Selection materialization 和总墙钟时长。未观测的部分为空；方法总时长不能重复累加共享准备。
- 对照 cold/warm 必须同时核对 Recipe/Artifact、依赖及 producer 标记，不用快慢推断 HIT。不为制造 cold 条件清空既有 Store。

## 4. Stage U：固定 Selection、GU 与 Metrics

Stage U 的 [实际生成示例](../../../experiments/configs/aagu015/generated/stage_u/cora-seed42-r0.01-degree.yaml) 只有 `selection_input`，没有 `selector_refs`。它声明 GNNDelete/GIF 与 `post_unlearning_utility_and_retrain_gap`；当前既有 modular 消费者会拒绝该评价 case，因此这是一份已解析、但尚不具备完整执行支持的计划。

| 比较 | 固定条件 | 需要的产物 |
|---|---|---|
| 不同 Selector 对同一 GU | dataset/split、训练 seed、预算、GU 设置 | 各 Selection 身份、before/GU/retrain 输出及对应指标 |
| GNNDelete ↔ GIF | 同一个 Selection Artifact；相同基准训练条件 | 两个独立 GU 输出；共享重训练参照必须验证删除语义、训练与模型身份相同 |
| GU ↔ 完整 Retrain | 同一个删除请求及删除后的数据语义 | model_before、model_unlearned、model_retrained 或可追溯的预测产物 |
| degree/random 控制 | 同 dataset、seed、预算和 GU | 配对指标差异；不能混入历史 public-split 或另一 checkpoint |

节点请求包含的训练监督删除、边/特征处理及评估图必须逐入口声明一致。本轮不把“只从 train_mask 移除节点”和“同时删除关联边”默认为相同协议。现有辅助 `run_retrain()` 与历史 DocMap 实验之间存在这项需核对的语义差别，运行前必须解决，设计验收时明确列为缺口。

| 指标 / 诊断 | 定义或所需输入 | 当前配置覆盖 |
|---|---|---|
| 测试效用 | 同 test_mask 上的 micro-F1；本轮单标签分类下对应 accuracy | retrain-gap case 声明 perf_before、perf_unlearn、perf_retrain |
| 删除本身的效用影响 | drop_retrain = perf_before − perf_retrain | 已在 case 声明；不等于近似遗忘误差 |
| 遗忘近似差距 | gap = perf_retrain − perf_unlearn；gap_pct = 100×gap/perf_retrain | 已在 case 声明；现有代码在分母为零时返回 0，分析中应标明零分母，不能据此判“无差距” |
| 删除目标与保留训练节点 | 在 selected_nodes / train_mask\selected_nodes 上比较相同模型的损失、预测或效用；报告集合大小 | 设计要求；当前独立 Evaluation case 没有相应完整字段注册 |
| collateral / 预测变化 | GU 与重训练输出在指定 retain_mask 上比较；保存 mask、labels、logits 与图身份 | 通用评估代码已有原语；当前 015 modular 入口未统一接入 |

Metrics 只能消费已明确身份的结果/预测。不存在的字段保持缺失，不能降为 utility-only 后宣布 Stage U 全覆盖。相同重训练输出的复用依赖实际删除集合、删除语义、模型和训练身份；实验 ID 或 Selector 名称相同都不是充分条件。

## 5. 展开、证据与阶段推进

本轮已有 25 份源 YAML、424 份生成 YAML，共 449 份：18 张 S 计划展开 306 个 Selector cell，306 张 U 计划展开 612 个 GU cell。612 不包含独立 Retrain 方法 cell；配对参照也不能按这个数字推断训练次数。条件依赖为 9 个训练准备组、141 个 Score 组、282 个 Selection 组，实际共享仍以身份核验为准。

本轮验收看方案、配置和能力覆盖表是否一致。后续执行按已批准范围依次完成：真实输入/Selection 绑定与入口支持检查 → 最小运行验证 → S 输出与分析 → 冻结 Selection → U 及参照输出 → Metrics 与收集审阅。前序失败时不推进；接受本方案不等于批准这些作业或全矩阵。

SM-005 是远程工具工作链验证，可以复用其符合身份条件的运行机制证据。015 的方案不把 job ID、GPU、Store 路径等操作字段写入科研 YAML，也不重复建设或验收 SyncMate。

## 6. 本轮交付检查

- Q1–Q4 均有具体比较对象、控制变量、输出及解释边界。
- 17 个 Selector、两种 GU、三个数据集、seed 和预算均对应现存 YAML；展开数与逐 cell CSV 对应。
- 每项输出映射到现有入口或明确的能力缺口；运行支持不因配置可解析而被夸大。
- Retrain 独立方法、Metrics 只读复用、删除语义和扩展评价字段的缺口明确留在能力表；未新增占位方法或自动建立实现 Block。
- 无本轮科研结果、实测速度或方向性结论；历史数字不作为本方案结果。
