# IM selector seed 大表实例

这些表是 AAGU-040 软件验证实例，未注册为正式科研矩阵或 SyncMate recipe。

`matrix: cartesian_product` 保持普通大表合同。独立轴写在顶层，与 `seeds`、`budget_ratios` 并列；不引入任意参数矩阵或第二套嵌套语法。

```yaml
matrix: cartesian_product
seeds: [42, 212, 2024]           # 模型训练 seed
im_selector_seeds: [11, 22, 33] # 仅 IM 的 Monte Carlo / RR 采样 seed
budget_ratios: [0.1]
```

| 实例 | IM 条件 | Degree / Random / R-point | 总效果条件 |
|---|---:|---:|---:|
| single_seed.yaml | 1 × 3 = 3 | 各3 | 12 |
| multi_seed.yaml | 3 × 3 = 9 | 各3 | 18 |
| candidates.yaml | RR：3 × 3 = 9 | Degree / Random / R-point / GT-full 各3 | 21 |

在同一图、候选集、K、算法和其他参数下，多值实例仅需3份 IM Selection。训练seed=42消费11/22/33三份选集，212和2024复用这三份。不同selector seed可以偶然得到相同节点集合；判据是身份隔离，不是强迫节点不同。

优先级为大表 `im_selector_seeds` > IM小表 `parameters.im_selector_seed` > ImParameters默认2024。省略大表轴只消费有效小表seed，不跟随训练seed。轴必须是非空、无重复的非负整数列表，拒绝布尔、字符串和浮点。没有IM时声明该轴也拒绝。Random继续使用自己的抽样参数，图和split完全由dataset小表持有。

本入口运行现有MC/Batch-CELF与固定RR最大覆盖贪心，按实际K生产选集。K或selector seed改变形成不同身份；不从大K选集截断复用，不计算全候选静态排名。Numba后端支持Batch-CELF；Python经典CELF仅允许batch size=1，后端变更会隔离身份。

## 算法小表与选型结论

| 小表 | 实际实现 | 用途 |
|---|---|---|
| [im_rr_greedy.yaml](../selectors/im_rr_greedy.yaml) | `method: im_rr_greedy`，RR=4096 | 固定样本覆盖贪心 |
| [im_celf.yaml](../selectors/im_celf.yaml) | `method: im`，batch=1，MC=100 | Monte Carlo 传播估计与 CELF 贪心 |

实验表通过 selector_refs 明确引用算法小表，可以单独运行其中一种，也可以同时比较。底层 method: im 表示 MC-CELF，method: im_rr_greedy 表示 RR，不按主次地位改变算法含义。

选型结论：后续 IM 组优先采用 RR，因为共享采样后只需覆盖更新，符合预期的大图计算方式。因此本目录示例显式引用 im_rr_greedy.yaml；这是实验配置选择，不是对 CELF 的禁用或软件约束，也不是 RR 实测更优的结论。

RR读取图的有向边（重复边去重）、全部节点作为均匀采样root、train_mask作为可选节点；静态IC传播概率由propagation_prob指定。它复用im_score_benchmark的真实采样与覆盖实现，返回K个节点。rr_count、传播概率、selector seed、数据/图/候选集、split、K和实现指纹均进入身份；训练seed不进入。改变rr_count会重新选点，普通入口未单独缓存RR样本。

4096是可修改的固定采样预算，不是IMM/OPIM-C的自适应精度证书。MC=100与RR=4096也不是等计算量。现有MC每次边际估计使用采样，不应把确定性子模贪心的严格保证直接套到它的噪声估计上。RR-SNI/Shapley的静态单点排名与本次集合覆盖目标不同，未在此入口冒充为IM集合选择。

IM 小表可与 IF 小表并列引用，分别运行各自的选择方法；这不是 Hybrid 融合。大表 IM 轴覆盖各 IM 算法的采样 seed，IF 参数保持独立。现有 HybridStrategy 的静态分数融合语义未改变。

### 采样预算与第二阶段

第一阶段集中生成 rr_count 个 RR 样本；第二阶段仅做覆盖计数、倒排索引和堆更新，不重新模拟传播。覆盖总数也按新增样本数累加，不再每轮扫描全部样本。样本和索引保留在内存中，大图仍需评估其大小。

当前固定样本 RR 没有 Lambda 精度参数。调节采样预算应修改 parameters.rr_count（正整数）；4096 保持为起始值。未来可以人工设置如 8192、16384，配合独立评估判断精度与开销，本次未生成或执行任何采样预算实验。更多样本通常降低估计噪声，但不保证每次选集或下游效果单调变好。propagation_prob 改变传播模型，im_selector_seed 改变采样随机性，两者都不是精度旋钮；Hybrid 的融合权重也与 rr_count 无关。

本轮仅允许合成小图单元验证与 YAML 无写入解析，不启动真实数据、训练、遗忘或 SSH 实验；因此没有大图耗时、内存或科研效果结论。

可复现的轻量候选评估：`python -m experiments.im_candidate_probe --output <不存在的JSON路径>`。它只生成三张80节点CPU小图，K=5、40个候选、3个selector seed，以固定16384个独立RR样本评估传播覆盖，并记录耗时和选集Jaccard。MC在该probe中使用serial Numba，warmup单列；公共小表的parallel_mc仍可独立选择。JSON包含图边、候选集、全部选集与每seed估计，不构成正式GU科研数据。

IM常规结果返回实际节点、K、Selection引用及recipe/content哈希、两条seed和selector seed来源。HIT与MISS同样返回这些内容。Score状态为not_applicable。当前Selection Store未保留K步收益，因此包含IM的表拒绝 `return_scores: true`，不会为回传重新计算收益或全排名。需要评分的其他selector可使用单独的普通表。

无写入检查：

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu040/multi_seed.yaml --dry_run
```

这只是解析/展开，正式运行仍须已批准的配置、设备和完整证据链。多训练seed反复消费同一IM选集，不构成多份独立选集样本。
