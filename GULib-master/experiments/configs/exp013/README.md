# EXP-013 · 不同 surrogate → 固定 GCN

[实验 YAML](surrogate_to_gcn.yaml) · [SyncMate Recipe](../../../scripts/syncmate/recipes/opengu-exp013-surrogate-to-gcn-v2.yaml)

本表只改变选点模型：GCN 是 direct 参照，SGC/GAT/GIN 是 surrogate。每个模型使用同样的 r_point、gt_full 参数语义；六种 GU 均采用 GCN backbone，其中 GraphEraser/GraphRevoker 是分片集成；Retrain 为全图 GCN。Random/Degree 只作为共同效果基线，不产生 surrogate 版本。所有可执行参数由 YAML 和小表拥有。

GCN direct 与四种单模型 GU 的 model/training 配置一致，普通模型准备过程使用同一缓存身份；CPU 真实执行验证了 state hash 相等。Surrogate 不读取 victim 权重/梯度/预测来选点。双方共享图、训练划分与指定 validation labels；这属于明确共享数据假设下的 query-free 灰盒迁移。

## 一张表如何展开

3 dataset × 3 训练 seed × (4 backbone × 2 selector + Degree + 3 Random 抽样) × (6 GU + Retrain) = 756 个逻辑输出条件。三个 Random 抽样 seed 与训练 seed 独立；先在训练 seed 内聚合 Random。训练 seed 不进入 GIF/IDEA Profile 匹配，现有参数跨 seed 共用，不新增按 seed 校准要求。

GIF/IDEA 通过 `parameter_profile_ref` 消费现有 GCN H64 映射；不是把这些参数用于 SGC/GAT/GIN。后者仅训练来选点。源模型之间共用算法参数，不混入 all_trainable/hops3 等另一套消融配置。

## 消费路径

1. `experiments/run.py experiments/configs/exp013/surrogate_to_gcn.yaml --dry_run` 检查展开与有效参数。
2. 审阅已生成的 Recipe，再通过 `scripts/syncmate/recipe.py preview opengu-exp013-surrogate-to-gcn-v2 --node gpu4090` 查看提交绑定。Recipe 不是一次已提交运行；候选尚需用户接受、落主线和按既有流程同步。
3. 执行时每个 source 的模型/评分/Selection 都按精确身份查缓存；同一选集被各 GCN GU 消费，并产生同请求 Retrain。现有评价器计算基础指标、utility、retrain-gap 与 Flip/Hop。
4. 执行端目录由 Recipe 的 outputs.root 确定；可信回传通常在 `results/runs/gpu4090/exp013-surrogate-to-gcn/<run_id>/`。以该 job 的 handoff/receipt 为实际定位，不从目录存在推断完成。
5. 分析消费可信回传的 `run.json` 与每个 cell 的 `metrics.json`、`selection.json`。调用现有 `experiments.modular_artifacts.read_run(run_path, expected_sha256)` 校验文件；期望哈希取可信回传记录，不能自行计算一个哈希冒充可信来源。
6. 用 `conditions.selector_ref` 对照执行版本的 YAML 小表确定 source backbone，不能只按 `conditions.selector` 分组，否则四个同名算法会混在一起。`conditions.model` 是 GCN victim，不能误作 source。

配对键：dataset/split 实例、GU 方法及实例、训练 seed、预算、selector 算法。对同一键取 surrogate 与 GCN direct；Random 先对抽样 seed 求均值。不同 selector/方法的行不作独立训练重复。完整表保持缺失/失败可见，不因结果差删行。已有输出是否能复用只由精确缓存身份决定。

GraphEraser/GraphRevoker 已纳入相同选集矩阵。分片集成与全图 GCN 参照之间的差异留在结果分析时单列解释，不能把全图 GCN 参照标作 ensemble-direct；不为加入方法新增配置轴。

## 已有指标如何用于结果图

`metrics.json` 的 rows 里：

| 量 | 来源 | 含义 |
|---|---|---|
| Utility 损失 U | utility.f1_before − utility.f1_after | 固定 GCN victim 的总性能下降 |
| Retrain-gap G | post_unlearning_utility_and_retrain_gap.gap | 同请求 Retrain F1 − GU F1，保持符号，不取绝对值 |
| Flip/Hop | post_unlearning_flip_hop | 同请求 GU/Retrain 预测差异的补充定位 |
| Selection overlap | selection.json 的 selected_nodes | 可在分析中算 Jaccard，辅助解释；不等价于攻击效果 |

指标均按原始定义保存；图中 F1 差值乘100可表示百分点。Utility 下降包含删除本身的影响，不能单独当作近似遗忘误差。Gap 为负或接近零也保留，不只挑有利方向。

## 建议的图（待真实结果，不预造点）

先做同一种版式的两张图：一张 U，一张 G；当前不预先指定哪张进入论文主图。

**原始效果图**：按 dataset × GU 分面；横轴 source backbone（GCN direct、SGC、GAT、GIN），纵轴 U 或 G。r_point/gt_full 用不同颜色，每种显示三个训练 seed 的原始点与均值；Random、Degree 用基准标记/水平参考，Random 已在各训练 seed 内聚合。它直接显示“灰盒是否仍有攻击效果”及 direct 是否本身有效。

**配对差距图**：同样分面，纵轴列 surrogate × selector，横轴 Δ = surrogate − GCN direct（百分点），零线表示与 direct 相同。画三个配对 seed 的点及均值，正负方向按 U/G 的定义解释。它直接显示“离白盒有多远”，不依赖不稳定的比值。

两张原始图和两张配对图在分析时统一产生，再按解释力选择主文重点，其余保留在完整报告/附录。若两指标给出不同结论，明确区分 utility transfer 与 GU-gap transfer，而不是概括为统一的白盒效果。

不用接近零的 direct 效果作分母来主张“100%迁移”。当前没有人为设定等效容差，因此只能描述观察到的差距；三个 seed 未见显著差异不证明统计等效。可以在看结果前另定实际可接受差距，但不在 YAML 中加入虚构 evaluation 字段。

## “是否可行”的两层输入

- 工程可行：配置/Recipe、CPU 集成、正式 gate、可信回传分别报告；dry-run PASS 只回答配置展开能否通过。
- 科学可行：在所测试的共享数据灰盒条件下，surrogate 是否超过简单基线、与 direct 相差多少、哪些 dataset/GU/selector 支持迁移。科学判断依据上面的原始值和配对差值；不把运行成功直接写作“灰盒获得白盒效果”。

仅验证多个 source→GCN，不推断双向对称或对所有 victim backbone 泛化。不要求 surrogate 必须扩大 retrain-gap 才承认其他攻击效果的迁移。

## 当前执行边界

Recipe 的 21600 秒是现有框架允许的6小时超时上限，不是完整矩阵耗时估计。正式 GPU 启动前必须根据实际作业成本冻结 Work Plan 的 cache-miss serial 估时；若超过单任务上限，按既有能力另行规划提交，不能声称本 Recipe 保证整表在6小时内完成。

此交付不启动 GPU、不同步 SSH、不产生科研结论。GAT/GIN 仅开放 selector 入口，GU 端继续拒绝这些未适配架构。
