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
| candidates.yaml | 两种IM各9 | Degree / Random / R-point / GT-full 各3 | 30 |

在同一图、候选集、K、算法和其他参数下，多值实例仅需3份 IM Selection。训练seed=42消费11/22/33三份选集，212和2024复用这三份。不同selector seed可以偶然得到相同节点集合；判据是身份隔离，不是强迫节点不同。

优先级为大表 `im_selector_seeds` > IM小表 `parameters.im_selector_seed` > ImParameters默认2024。省略大表轴只消费有效小表seed，不跟随训练seed。轴必须是非空、无重复的非负整数列表，拒绝布尔、字符串和浮点。没有IM时声明该轴也拒绝。Random继续使用自己的抽样参数，图和split完全由dataset小表持有。

本入口运行现有MC/Batch-CELF与固定RR最大覆盖贪心，按实际K生产选集。K或selector seed改变形成不同身份；不从大K选集截断复用，不计算全候选静态排名。Numba后端支持Batch-CELF；Python经典CELF仅允许batch size=1，后端变更会隔离身份。

## 两个候选与公共小表

| 小表 | 实际实现 | 用途 |
|---|---|---|
| [im_celf.yaml](../selectors/im_celf.yaml) | `method: im`，batch=1，MC=100 | 首轮参考候选；逐步更新边际收益，避免batch一次取多个节点的近似 |
| [im_rr_greedy.yaml](../selectors/im_rr_greedy.yaml) | `method: im_rr_greedy`，RR=4096 | 对照候选；一次固定RR采样，再按尚未覆盖的样本逐点贪心 |
| [im.yaml](../selectors/im.yaml) | 原有 `method: im`，batch=5 | 既有Batch-CELF参数实例，不计作第三个独立候选算法 |

RR读取图的有向边（重复边去重）、全部节点作为均匀采样root、train_mask作为可选节点；静态IC传播概率由propagation_prob指定。它复用im_score_benchmark的真实采样与覆盖实现，返回K个节点。rr_count、传播概率、selector seed、数据/图/候选集、split、K和实现指纹均进入身份；训练seed不进入。改变rr_count会重新选点，普通入口未单独缓存RR样本。

4096是可修改的固定采样预算，不是IMM/OPIM-C的自适应精度证书。MC=100与RR=4096也不是等计算量。现有MC每次边际估计使用采样，不应把确定性子模贪心的严格保证直接套到它的噪声估计上。RR-SNI/Shapley的静态单点排名与本次集合覆盖目标不同，未在此入口冒充为IM集合选择。

两个IM小表可与IF小表同时引用；大表IM轴分别覆盖它们的采样seed，其他算法参数仍各自独立。缺少大表轴时，各小表seed分别生效。此轮建议先保留MC-CELF和RR贪心作配对比较，再用正式GU效果决定是否扩充；传播覆盖不能替代删除损害。

可复现的轻量候选评估：`python -m experiments.im_candidate_probe --output <不存在的JSON路径>`。它只生成三张80节点CPU小图，K=5、40个候选、3个selector seed，以固定16384个独立RR样本评估传播覆盖，并记录耗时和选集Jaccard。MC在该probe中使用serial Numba，warmup单列；公共小表的parallel_mc仍可独立选择。JSON包含图边、候选集、全部选集与每seed估计，不构成正式GU科研数据。

IM常规结果返回实际节点、K、Selection引用及recipe/content哈希、两条seed和selector seed来源。HIT与MISS同样返回这些内容。Score状态为not_applicable。当前Selection Store未保留K步收益，因此包含IM的表拒绝 `return_scores: true`，不会为回传重新计算收益或全排名。需要评分的其他selector可使用单独的普通表。

无写入检查：

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu040/multi_seed.yaml --dry_run
```

这只是解析/展开，正式运行仍须已批准的配置、设备和完整证据链。多训练seed反复消费同一IM选集，不构成多份独立选集样本。
