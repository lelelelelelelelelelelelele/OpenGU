# 当前有效参数、配置变体与缓存影响

核对基线：`8383e30239398c5268965e088afdfba7abc74ca9`；2026-09-04 源码/配置审查。下表是该基线的可追溯快照，不是另一份可执行参数权威。修改实验仍须改相应配置/实现并重新核验；“可比较”表示设计变量，不表示当前正式入口已接受或获准执行。

## 1. Dataset/Split

本表列的是解析后的有效值，不要求用户在每份 YAML 中重复填写所有 OpenGU 默认值。人工小表只列必填输入与覆盖值；方法注册/实际消费者提供其余默认值，运行记录保存完整值与来源。固定公式属于方法实现，只有需要比较且实现支持的设置才作为调参项。

来源：[formal YAML](../../experiments/configs/syncmate_target_direct_formal_v2.yaml)，[`load_config`](../../experiments/target_direct_v1/syncmate_stage.py)，[split contract](../../experiments/target_direct_v1/__init__.py)。

| 字段 | 当前 formal-v2 值 | 可改/待定项 | 正确身份影响 |
|---|---|---|---|
| dataset | Cora、CiteSeer、PubMed | 新数据集需新的已注册实例及资产 | 数据的真实消费者 |
| split 方法 | 持久化 OpenGU processed pair；profile 由合同派生 | 不接受 PyG public split 替代当前 split | Split/候选/训练/评分/GU |
| train/val/test ratio | 0.7 / 0.1 / 0.2 | 合法比例可另建资产，不覆盖原资产 | 同上 |
| split_seed | 2024 | 与模型 seed 分开 | 同上 |
| processed_profile | planetoid_70_10_20_seed2024 | 从规范化比例和 split seed 派生，不手填互相冲突值 | 实际 split 哈希仍需核验 |
| materialize_on_miss | formal recipe 声明 true | 是已注册数据准备边界，不是纯配置读取的写权限 | 不作为 GU 参数 |
| 数据/划分内容 hash | 来自真实资产，非 YAML 猜出 | 本次未观察正式远端值 | 缺失时不能执行/接纳 |

由当前配置推导，Cora 候选数 1895，1% K=18、5% K=94；CiteSeer 2328→23/116；PubMed 13801→138/690。它们是计划推导值，运行还须与实际 train mask 数量一致，不把这些常数写回 split 资产。

## 2. Selector 公共字段与模型

来源：[runner 参数与 Recipe 组装](../../experiments/target_direct_v1/run_selection.py)，[GCN 属性](../../model/properties/GCN.yaml)，[GCN 模型](../../model/base_gnn/gcn.py)，[基础训练](../../task/GNNDeleteTrainer.py)。

| 字段 | 当前有效值/来源 | 可比较的配置或待定项 | 正确身份影响 |
|---|---|---|---|
| candidate | train_mask 中节点，实际有序 ID hash | 候选规则变化必须显式定义 | 相应 Score/Selection |
| ratio | 0.01、0.05 | 可写不同 Selector 表；其他比例不是当前 formal 白名单 | Selection；预算无关 Score 可复用 |
| budget denominator / rounding | train_candidate_count / floor_with_minimum_one | 改规则是语义变化 | 最终节点与下游 |
| ranking / tie-break | score 降序，node ID 升序 | 改方向/同分规则需新配置 | Selection；不必改未消费该规则的原始分数 |
| selector model | OpenGU.GCNNet，2 层，hidden 64 | SGC 与 GCN 可分别建表；当前 formal 只允许两层 GCN | 模型型 selector；degree/random 不依赖它 |
| dropout | 0.5，模型 forward 的有效值 | 不能只写 YAML 就声称已改变 forward | 训练/模型型评分 |
| training epochs | 100，formal YAML → runner → num_epochs | 如 100/200 为不同训练配置；200 非本次批准 | checkpoint 及消费者 |
| training optimizer | Adam，GNNDeleteTrainer.train_node_fullbatch | 可支持范围由实现声明 | checkpoint 及消费者 |
| training lr | 0.005，model/properties/GCN.yaml | 如 0.005/0.01；不是 GU 学习率 | checkpoint 及消费者 |
| training weight_decay | 0.000001，同上 | 如另一个非负值；需实际进入优化器 | checkpoint 及消费者 |
| training scheduler | none，当前基础训练循环 | 非空调度器属于实现能力变化，不是任意 YAML 承诺 | checkpoint、快照权重及消费者 |
| model seed | 42、212、2024 | 小表拥有 seed；大表组合实例 | 对应模型/评分，不重切 split |
| random ranking seed | model/experiment seed + 100003 | 42 对应 100045；未来独立字段需显式传值 | random，不应影响 degree |
| numeric identity | data.x.dtype、实际 device、CUDA version 写入现有 Recipe | 本次不推测正式运行环境；未来按真实计算依赖归属 | 当前整包依赖；026 收敛边界 |

注意：`run_selection.py` 有 `getattr(model_config, 'lr', 0.01)` 与 decay=5e-4 后备值，但 GCN 实际加载 properties，当前有效值是 0.005/1e-6。仅抄代码中的后备数字会填错参数表。

## 3. IF、数值近似和轨迹

来源：[runner 的 `build_parser` 和评分调用](../../experiments/target_direct_v1/run_selection.py)、[scoring](../../experiments/target_direct_v1/scoring.py)、[core](../../experiments/c_target_v1/core.py)。这些值由现有 stage 没有覆盖的 CLI 默认值进入计算，不是在 YAML 中显式固定的字段。

| 字段 | 当前有效值 | 意义及可比较项 | 正确身份影响 |
|---|---|---|---|
| parameter_scope | last_layer | 最后一层中 requires_grad 参数；另有 all_trainable 代码选项，formal GU 仍拒绝非 last_layer | 实际使用梯度/IF/TracIn 的方法；不是 degree/random 参数 |
| target set / loss | validation_mask 真标签；CE mean | 最终科学目标由 015 决定；不能用 test 标签替换 | 使用目标梯度的方法 |
| Hessian training set/loss | 全 train 候选，CE mean | 改 reduction 或集合是语义变化 | IHVP 消费者 |
| LiSSA iterations | 20 | 逆 Hessian 向量积的递推次数；可比较 20/40 等正整数 | r_point、gt_simple、gt_full、B-Hutch |
| LiSSA scale | 25.0 | 递推缩放，正数；不同值属于求解配置 | 同上 |
| LiSSA damp | 0.01 | 递推阻尼，当前校验 0≤damp<1 | 同上 |
| Hutch probes | 32 | 随机 ±1 探针数；32/64 是同算法两份配置 | 仅 B-Hutch 及其真实下游 |
| Hutch seed | 1729 | 控制探针，不是模型训练 seed | 仅 B-Hutch |
| affected_hops | 2 | 候选及无向邻域；源标签只取受影响 train 子集 | 图源评分，不是 point/degree 必填项 |
| intervention / graph source | 移除候选关联边；grad1 为原图受影响训练集 CE sum，grad2 为删边后邻居训练集 CE sum | 不包含验证/测试源标签，不逐候选精确重训练 | 图源评分 |
| saved checkpoint epochs | [1,10,25,50,75,100] | 基础训练后保存的精确权重 | 轨迹实际消费者 |
| cp3 indices / epochs | [0,3,5] / [1,50,100] | first/middle/final；不是 [1,25,100] | 相应 TracIn 变体 |
| cp_all | 6 个 checkpoint | 与 cp3 同一训练，可复用快照 | 相应 TracIn 变体 |
| checkpoint weights | preceding_optimizer_update_lr | 当前每份为基础训练学习率；必须保存实际权重值 | TracIn，不是所有 GU 必需 |

“数值近似”不是新增科研模块：目标仍是原来的 IF 量，只是采用有限次 LiSSA 递推、有限 Hutch 随机探针计算近似。它会影响数值和排序，因而属于使用它的 selector 配置。有限值检查通过不等于近似足够准确；误差/收敛判据和最终采用哪个范围仍须由具体实验决定。

### `iterations: 20` 的具体含义

当前 `inverse_hessian_vectors` 在固定 checkpoint 的模型上，对每一个右端向量 v 做 20 次 Hessian-vector product 递推。它不是训练 20 个 epoch、选取 20 个节点或做 20 次实验，也不在这些步骤中更新模型参数。目标是近似逆 Hessian 对向量的作用，而非显式构造并求逆整个矩阵。

源码递推为 `h0 = v`，重复 `h_next = v + (1 - damp) * h - Hh / scale`，最后返回 `h / scale`。若该递推收敛，其阻尼对应求解 `(H + scale*damp*I)^(-1) v`；当前 scale=25、damp=0.01 时移位量为 0.25，不能把 damp=0.01 直接描述为给 H 加 0.01I。固定 20 次是计算预算，不是已达到精度阈值的证明；40 次通常增加开销，也不保证未收敛或不稳定问题自动改善。

在 B-Hutch 中，probes=32 是 32 个随机右端向量，每个向量再各递推 20 次，因此该探针分支执行 32×20=640 次 HVP 递推；这不包括当前整包 runner 另外计算目标 IHVP 等工作。20 与 32 不是同一个参数。

### 17 种评分应各自消费什么

下表来自实际评分表达式，是拆键时的依赖依据；当前实现仍把它们装入同一 ScoreBundle。共同训练/图可共享，但每种方法只应声明自己需要的依赖。

| 方法 | 数值实际依赖（除候选/数据/基础模型外） |
|---|---|
| degree | 原图出度；不需要基础模型、标签梯度或轨迹 |
| random | 候选序列和随机 seed；不需要基础模型/图梯度 |
| a_grad_norm | 最终候选梯度范数、参数范围 |
| b_param_hutch | 最终候选梯度、训练 Hessian、LiSSA、Hutch probes/seed、参数范围；不消费 validation 目标梯度 |
| legacy | 最终候选梯度与候选梯度之和的负内积；不消费 validation 目标 |
| p_point | 最终候选梯度与 validation 目标梯度 |
| r_point | 最终候选梯度与 validation 目标 IHVP（LiSSA） |
| p_simple / p_graph | 图源梯度/差分、validation 目标梯度、affected_hops |
| gt_simple / gt_full | 图源梯度/差分、validation 目标 IHVP、affected_hops、LiSSA |
| tracin_cp_point_3 / _6 | 指定快照的 point 内积与对应 update_lr 权重；不消费 LiSSA/Hutch |
| tracin_cp_simple_3 / _6 | 指定快照的 simple 图源内积、hops、权重；不消费 LiSSA/Hutch |
| tracin_cp_graph_3 / _6 | 指定快照的 graph 差分内积、hops、权重；不消费 LiSSA/Hutch |

实际统一实现目前会计算多于单方法所需的中间量；这不等于所有中间配置都是该方法的语义输入。通用 `tracin` 也不能仅凭名字视为上述 checkpoint TracIn 的同一实现。

## 4. Unlearning 独立参数

来源：[通用 parser](../../parameter_parser.py)、[GU config builder](../../experiments/target_direct_v1/build_gu_config.py)、[GNNDelete](../../unlearning/unlearning_methods/GNNDelete/gnndelete.py)、[GNNDeleteTrainer](../../task/GNNDeleteTrainer.py)。

| 字段 | 当前 formal-v2 GNNDelete 节点 lane | 可比较项/注意 | 正确身份影响 |
|---|---|---|---|
| GU method | GNNDelete | GIF/GraphEraser 等属于另一 GU 表；formal-v2 当前不接受自由切换 | GU，不反向影响 Selector |
| target model / checkpoint | GCN 2×64，消费精确目标 checkpoint | 与 Selector 分别声明，不相同则不共享 | GU 训练/遗忘 |
| target training | Adam；100 epochs；lr=0.005；decay=1e-6 | 共享 checkpoint 时省去重复基础训练，不省略身份检查 | checkpoint 消费者 |
| unlearn_lr | 0.01 | 可比较 0.01/0.02；优化 deletion1/2 参数 | GU；现有通用 trained-selector 键有反向污染，交 026 |
| unlearning_epochs | 50，parser 默认；节点删除循环读取它 | 与基础训练 num_epochs=100 不同 | GU |
| alpha | 0.5 | GNNDelete randomness/locality loss 配比，不是 Hybrid selector 的 alpha | GU |
| loss_fct | mse_mean | 更换损失需明确支持与定义 | GU |
| loss_type | both_layerwise | 当前两层分别建立 Adam；可选类型必须核验消费者支持 | GU |
| deletion optimizer | Adam，每层 deletion 参数；当前默认 weight_decay=0 | 不从 GCN 基础训练 decay 推导 | GU |
| save_predictions / run_collateral / run_update_detection_auc | true / true / true，build_gu_config | 评价与产物保存属于各自消费者，不反向改变选点 | 评价/结果产物 |
| no_cache | 生成的 target-direct GU YAML 为 true | 当前 lane 行为事实；不是新合同要关闭正常缓存的建议，026 保持正常默认缓存 | 执行策略，不可当数值参数 |

## 5. 通用方法的其他真实例子

[AttackManager](../../attack/attack_manager.py) 现在为不同策略取自己的字段：IM 有 propagation_prob=0.1、mc_rounds=100、candidate_fraction=1.0、batch_size=5；PageRank alpha 默认 0.85；Hybrid 有融合方式和自身 alpha。这些应分别注册在所属 selector 配置中，不成为所有方法的公共参数包。SGC 的 [properties](../../model/properties/SGC.yaml) 为 lr=0.05、decay=1e-6，说明换模型时不能原封继承 GCN 训练值。

现有通用 trained-selector 把 `target_parameters`（只排除 unlearning_methods）放进 training，又引用广泛的结果 producer 指纹。因此 GU 学习率或无关源码可能误改变 Selection 键；target-direct 则把 17 个评分共同绑定 Hessian/trajectory。这两处是 026 的实现问题，本表不把它们描述为已解决。

## 6. 还需要科研负责人决定什么

- 015：IF 最终研究目标、last_layer/all_trainable 的主次、graph/point 源定义如何比较。
- 每轮实验：是否比较 solver 精度、采样数、模型、预算或 GU 超参数；先明确问题与误差/接纳准则，再列具体配置实例。
- 026：依合同实现方法级字段校验和真实 HIT/MISS，验证独立模型组合与现有 Selection 直接消费。
- 正式执行：绑定真实数据/划分/checkpoint/Selection 身份及设备 gate；本次不凭计划值捏造资产或批准 306-cell 矩阵。

### 待定义问题：不同 backbone 是否给出相近的节点排序？

用户提出比较 SGC、GCN、GAT 提取的节点相关性。可先做 selector-only：固定已划分数据、候选节点、Selector 算法/目标、预算与数值求解设置，比较不同 backbone 的节点得分排序和 top-K 选集。建议同时观察全候选排序相关性与 top-K 重叠率，并有同 backbone 多 seed 的对照，避免把训练随机性误判为 backbone 差异；原始分数尺度未必可直接比较。

这里把“节点相关性”暂解释为不同模型得到的选点评分/排序一致性，不是节点表示相似度矩阵。两者需要不同实验定义，正式运行前须确认。换 backbone 时各模型实际训练参数/预算也须明确，不能假设复制同一学习率就是公平比较。该问题本轮仅记录，不新增实验 Block、不运行 GPU、不宣称 SGC/GAT 已被当前 formal-v2 入口支持。
