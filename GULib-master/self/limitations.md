# Limitations 与 scaling 观察 — 实验过程发现的硬约束

> 这里只记录**实测**遇到的 scaling / methodology 限制，不写没验证的猜想。
> 用于：paper §5 limitations、advisor meeting、reviewer rebuttal、未来 follow-up。

更新规则：
- 每条 limitation 至少要有 **evidence**（log 片段、commit hash、metric 数字）
- **decision** 字段标明 `OPEN` / `RESOLVED` / `ACCEPTED`（接受为 paper 限制）
- 涉及代码位置写文件:行号

---

## L1. GraphEraser × ogbn-arxiv: LPA partition 慢但可行（早停救场）

**Status**: `ACCEPTED-MITIGATED` — terminate_delta 提前终止避免最坏情况
**Discovered**: 2026-05-05 跑 B.1 第一个 GraphEraser cell 时
**Severity**: 中 — 单 cell ~20 min，B.2 总耗 ~4h，可接受
**Updated**: 2026-05-05 实测 partition 实际早停在 1-2 iter

### Evidence

实测 LPA `iteration` 间隔（ogbn-arxiv, 135K 训练节点, num_shards=10, partition_method=lpa_base）：

```
16:22:22  iteration 0       (LPA partition 开始)
16:32:04  iteration 1       —— 10 min / iter（最坏情况估计）
≤ 16:38:34  partition 完成 + shard model 训完 + unlearning 走完
            （即 partition 实际只跑 1-2 iter 就早停）
```

**早停机制**：`constrained_lpa_base.py:131-132`：
```python
if delta <= self.terminate_delta:    # default 0, see parameter_parser.py:137
    break
```
节点稳定后立即退出，不会跑满 `max_iteration=30`。

**实际单 cell 耗时**（empirical）：
- LPA partition: ~10 min（1-2 iter）
- shard model train: <1 min
- unlearning: ~40 s
- MIA: ~6 min
- **总计 ~20 min/cell**

B.2 GraphEraser × {random,tracin,im,hybrid} × 3 seed = 12 cell × 20 min = **~4 h**，可接受。

### Root cause

`unlearning/unlearning_methods/GraphEraser/partition/constrained_lpa_base.py:139-157`
`_determine_desire_move()`:

```python
for i in range(self.num_nodes):           # 135K 次 Python for 循环
    neighbor_community = self.node_community[self.adj[i]]
    unique_community, unique_count = np.unique(neighbor_community, return_counts=True)
    for community in unique_community:    # 内层
        ...
```

是纯 Python for 循环 + `np.unique`，单 iter O(N × avg_degree) 没 vectorize。原 GraphEraser
论文 (BLP, Ugander et al. 2013) 的实现假设 N ~ 10⁴ 量级，arxiv 的 N ~ 10⁵ 慢 10×。

加上 `cvxpy` 解 LP（`num_communities²` 维），每 iter 还要算一次。

### Available alternatives (in source, dispatched via --partition_method)

| 选项 | 速度（estimated）| 是否在 GraphEraser 原论文 | 备注 |
|---|---|---|---|
| `lpa_base` (current) | 5h | ✅ 论文方法 | 不可行 |
| `sage_km_base` | ~1 min | ✅ 论文给的另一选项 (SAGE encoder + sklearn KMeans) | **首选** |
| `metis` | ~10s | ❌ METIS 是另一族算法 | 需 paper 注一句"substitute for scaling" |
| `random` | <1s | partial | partition 质量未保证 |
| `gpa` / `graph_km` | 未测 | partial | 不熟悉 |

`sage_km_base` 在 cora 上跑过、速度正常（具体测试 TBD）。

### Methodology defense (if pivot to sage_km_base)

> "On ogbn-arxiv we use the SAGE-KMeans partition variant of GraphEraser
> (Chen et al. 2022, §4.2) instead of the LPA variant, as the reference
> LPA implementation has an O(N) Python loop per iteration that is
> intractable at the arxiv scale (N=135K). SAGE-KMeans is one of two
> partition methods proposed in the original paper; we use it for parity
> with the cora/citeseer LPA results."

### Decision

`ACCEPT lpa_base`. 实测早停后 ~20min/cell，B.2 4h 总耗在预算内。
无需切换 partition method、无需 paper 加 limitation。

如果未来 arxiv 上 cell 超过 1h（partition 没早停），再考虑 fallback 到 `sage_km_base`。

---

## L2. TracIn × ogbn-arxiv: G-matrix 显存不足 24GB

**Status**: `RESOLVED-VIA-HARDWARE` — 决定通过升级 GPU 解决，而非改算法
**Discovered**: 2026-05-05 commit `6b7285b` 之后 code review 推算
**Severity**: 中 — 不影响 cora，只在 arxiv 卡 24GB GPU 上 OOM

### Evidence

TracIn `_compute_tracin_scores` 把每个候选节点的梯度堆成 `[N_cand, num_params]` 矩阵：
```
G_size = 90,941 × 109,096 × 4 bytes = 39.7 GB
```
4090 (24GB) 必 OOM；A100 80GB / A6000 48GB 可容。

详见 `attack/attack_strategies/tracin_strategy.py:_compute_tracin_scores`（commit `6b7285b`
之后 forward-once 优化保留了 G matrix 的内存模式，没改）。

### Mitigations 评估

| 方案 | 单 cell 时长 | 显存 | 方法论代价 |
|---|---|---|---|
| 直接租 A100 80GB | ~150 min | 40 GB | 0（推荐） |
| 候选集随机子采样 10% | ~10 min | 4 GB | paper 注脚说明 |
| 2-pass exact (无 G matrix) | ~300 min | <1 GB | 0 但慢 |

### Decision

升级 GPU。配套 commit `af1c8ba` 提供 `prewarm_selection_cache.py`，把 selection 阶段
（贵卡需求）和 GU+retrain+MIA（4090 够）拆到两台机器跑，总成本 ~$20 vs 单 A100 全程 ~$42。

详见 `SERVER_RUNBOOK.md §B.1.5`。

---

## L3. IM × ogbn-arxiv: 默认参数下 CELF step-1 不可行 (RESOLVED)

**Status**: `RESOLVED` — yaml 默认参数已修复
**Discovered**: 2026-05-05 早上跑 B.1 时卡 10h
**Severity**: 高（已解）

### Evidence

默认 `mc_rounds=100, candidate_fraction=1.0` 下，CELF step 1 = 90K candidates × 100 MC = **9M
次 BFS** 在 169K 节点图上。10h+ 没出第一个候选 spread。

### Resolution

`experiments/configs/phase_b_arxiv.yaml` 默认带：
```yaml
extra_args:
  - --candidate_fraction
  - "0.1"
  - --mc_rounds
  - "50"
```
top-degree 10% 剪枝（IM 文献标准做法，IC spread ~ degree） + MC 减半 → 单 cell ~3 min。

Commit `6b7285b` 同步把 feasibility yaml 也加上同套参数。

### Methodology defense

CELF + degree-based candidate pruning 是 IM 文献标准做法（Goyal et al. 2011, "CELF++"）。
no defense needed beyond a footnote.

---

## L4. 选择策略与 GU 方法解耦：B.1 误把 selection 测试塞进 GU 稳定性测试 (RESOLVED)

**Status**: `RESOLVED` — yaml 回滚 + 独立探针脚本
**Discovered**: 2026-05-05 commit `81733b2` 之后立即识别
**Severity**: 低 — 设计错误，没产出错误数据

### Evidence

Commit `81733b2` 把 B.1 从 5 cell（5 method × random）扩成 15 cell（5 × 3 strategy）。
但 SelectionCache 是 cross-method 共享的——同 (seed, strategy, k) 跨 5 method 复用同一份
selection。所以 tracin × 5 method 里有 4 cell 重复劳动（selection cache hit，GU 部分各
跑一次）。

### Resolution

Commit `6b7285b` 回滚 B.1 到 random-only。新增 `scripts/feasibility_selection_only.py`
独立测策略可行性（不带 GU）。Runbook §B.1.5 说明分层。

---

## L5. MIA 阶段 CPU-bound，GPU 闲置

**Status**: `ACCEPTED` — 设计层面无法 deadline 内优化
**Discovered**: 2026-05-05 跑 B.1 GraphEraser 时观察 CPU 1000% / GPU ~0%
**Severity**: 低 — 不影响正确性，只影响硬件选型

### Evidence

`attack/Attack_methods/GraphEraser_MIA.py:447-462` 的 MIA 循环每个 iter (~3.6s)：
1. 磁盘 I/O：load community + 10 个 shard model 权重
2. CPU：repartition shard data per unlearned target
3. GPU：每 shard 一次小 forward（毫秒级）

实测 cora/arxiv 上 GPU 利用率 < 5%，CPU 跑满 1000% (10 核)。

### Implications

- **租 GPU 实例时优先看 CPU 核数 + RAM**，不是只看 GPU 显存
- B.1.5 分卡工作流中，MIA 在 4090 stage 完成；只要 4090 实例 CPU ≥ 8 核就够
- 36-cell B.2 总 MIA 耗时 ~3.6h，包在 ~11h Stage 2 预算内

### 不修复的理由

修复路径已知（cache shard model loads + parallelize across unlearned_indices），
但是 OpenGU 原代码的 attack 实现，改动会动到 paper baseline。NeurIPS 后做 follow-up。

---

## L6. Hybrid 的 IM 分支没有 submodular diversity

**Status**: `ACCEPTED` — paper §5 limitation candidate，NeurIPS 后再修
**Discovered**: 2026-05-05 review hybrid_strategy.py + cora top-3 比对
**Severity**: 中 — alpha-sweep 在 IM 端的有效性受限，但不影响整体方法学

### Evidence

`attack/attack_strategies/hybrid_strategy.py:55` 用 `compute_initial_marginal_gains`
拿 N 维 σ({v}) 做 IM 那一支的分数，然后跟 IF 加权一次性 topk：

```python
im_scores = self.im.compute_initial_marginal_gains(...)  # σ({v}) for each v
fused = α * normalize(if_scores) + (1-α) * normalize(im_scores)
_, topk_indices = torch.topk(fused, k)   # ← 没有 step 2+ 的 marginal 重估
```

**与 IM strategy 对比**：IM strategy (`compute_im_celf`) 用 σ({v}) 初始化堆，
然后做 CELF lazy step 2+ 的 marginal 重估，submodularity 保住。Hybrid 把
σ({v}) 当最终评分用，submodularity 丢了。

**实证（cora SGC，r=0.05，top-3）**：

| strategy | top-3 selected |
|---|---|
| degree | [1358, 306, 1701] |
| im (with CELF) | [1358, 306, 1072] |
| pagerank | [1358, 1701, 1986] |

- IM (with CELF) vs degree: top-2 完全一致（σ({v}) 跟 degree 高相关）
- 但 IM Gap = -5.57% vs degree Gap = -4.49% on r=0.05 → 有差，IM 不完全等价 degree
- Hybrid 在 α=0 corner 的输出会更靠近 σ({v}) topk（不是 CELF 完整选择），
  退化向 degree-like 的方向比 IM strategy 更严重

### Implications

- Hybrid alpha sweep 在 IM 端的有效"diversity"被压制
- 已知修法两条，**都不完美**：
  - **(A) hop-decay 近似**：选完 v 把 r-hop 邻居 IM 分打折扣。便宜但启发式
    （`decay∈{0.3,0.5,0.7}` × `hop∈{1,2}` 是新超参；衰减常数无原则依据）
  - **(B) K'-superset CELF**：先跑真 CELF 选 5k diverse pool，
    pool 内按 fused 分重排选 k。理论干净但 α=1 corner 不再恢复纯 TracIn
- 严格 CELF（每步重跑 MC 算 σ(S∪{v})-σ(S)）在 arxiv k=200 上 10+ 小时，不可行

### 不修的理由（NeurIPS 时间窗）

1. 改了会动 hybrid 输出分布，所有 hybrid cell 要重跑（B.2 / B.3 至少 +6 小时）
2. (A) hop-decay 的衰减系数没有理论依据，引入超参反而更难辩护
3. (B) 破坏 α=1 corner 的可解释性
4. 当前 hybrid 已经有 "IF + topology prior" 的可解释性，paper 立得住
5. (A)/(B) 的系统对比可作为 future work 章节的 follow-up

### Talking points (advisor / reviewer)

- "Hybrid's IM branch uses single-node spread σ({v}) as a per-candidate score
  for fusion with IF. This loses submodularity — the topology score
  effectively reduces to a degree-correlated prior at the top-k."
- "We acknowledge a CELF-aware fusion variant (greedy with submodular discount)
  could improve diversity, but the standard CELF inner loop is incompatible
  with our per-candidate fusion budget, and known approximations
  (hop-decay, K'-superset rerank) introduce hyperparameters or break α=1
  recovery. We leave a principled fix to future work."

---

## 待观察 / 推测但未实测

下列是怀疑但尚未实测，**不要直接写进 paper**：

- **MEGU / IDEA × arxiv**：二阶梯度可能在 Hessian-vector product 阶段慢，估计 10-30 min/cell，未验证
- **GNNDelete × arxiv**：mask network 训练步数可能要调，未验证
- **Update-detection audit（legacy 措辞 "MIA shadow models"）在 arxiv 上的耗时**：估计每 shadow ~30s，未直接测过；本工程实测的隐私 metric 为 update-detection AUC（非标准 shadow-model MIA），shadow-model 升级路径属 future work
- **collateral retrain 收敛性**：arxiv 200 epoch 是否够 retrain f1 达到 base train f1，待 B.1 数据出来确认

---

## 给 advisor / reviewer 的一行 talking points

- "我们在 4090 上无法跑 GraphEraser-LPA 的 arxiv，因为参考实现是 Python loop O(N)；改用同论文的 SAGE-KMeans 变体（如确认）"
- "TracIn 在 arxiv 上需要 ≥40GB GPU 显存（G matrix），在 A100 80GB 上跑"
- "IM 用了 CELF 标准的 degree pruning（top 10%），mc_rounds=50，符合文献"
- "selection 与 GU pipeline 解耦，selection cache 跨 method 共享降低成本"
