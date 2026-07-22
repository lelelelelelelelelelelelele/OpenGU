---
title: IM 成熟算法可用性、Score 形态与 Degree 超越实验计划
created: 2026-07-23
updated: 2026-07-23
type: supplementary-experiment-plan
status: pre-registered-awaiting-approval
tags: [influence-maximization, reverse-reachable, score-artifact, degree-baseline, scalability]
aliases: [IM成熟算法实验, IM Score实验, IM与Degree实验]
---

# IM 成熟算法可用性、Score 形态与 Degree 超越实验计划

> [!IMPORTANT]
> **状态：待审批，尚未执行。** 本页只完成研究问题、方法输出合同、实验矩阵、资源预算与停止条件的预注册。用户批准前，不实现算法 adapter，不运行 selector benchmark，也不启动 GU cell。

关联页面：

- [[20_IF目标层级对比实验计划]]：可复用的“reference / proxy / downstream outcome”文档结构；
- [[21_C目标TracIn与GIF近似有效性实验计划]]：selection fidelity 与真实集合效果分开验收的范例；
- [[12_近似策略重合度实验]]：当前 IM/IF proxy-validity 总入口；
- [现代 IM 算法调研](../../reports/im_modern_algorithms_SURVEY_REPORT.md)：算法保证、纠偏文献与 OpenGU 适配背景；
- [历史大图 IM materializer 验收](../../docs/cache_v2_im_selection_materializer_ACCEPTANCE_REPORT.md)：ogbn-arxiv cold `13,583.91 s` 的时间锚点；
- [小图 17-output 实测](../../reports/small_graph_selection_BENCHMARK_REPORT.md)：IF 线小图 cold/warm 工程参照。

## 0. 先给计划结论

本轮不研究“再发明一个 IM 算法”，而是把成熟算法当作受测系统，回答四件事：

1. **时间：** 在 Cora/CiteSeer/PubMed 与 ogbn-arxiv 上，cold、warm、peak RSS、RR 规模分别是多少？
2. **保证：** 返回的是论文级近似保证、运行中 certificate、有限样本置信区间，还是只有经验结果？
3. **Score：** 方法返回完整静态 score、预算相关 score、逐轮动态 marginal，还是只有最终 selection？
4. **Degree：** 方法是否在独立 IC spread 上稳定超过 degree；若超过，该优势是否传递到 approximate-GU retrain gap？

首轮只保留两条主线：

- **Set-level 主线：** corrected IMM、OPIM-C；
- **Full-score 主线：** RR-SNI、RR-Shapley、RR-$k$-semivalue。

`degree` 是主竞争基线，`random` 是负控制；current Batch-CELF 与 strict CELF 只在小图用于解释历史实现。SSA/D-SSA、SUBSIM/HIST、SKIM、TipTop、深度/RL IM 不进入首轮主矩阵。

> [!WARNING]
> Degree 是一次结构统计，预期始终比 RR/IM 更快。因此“超过 degree”不定义成同时赢得 wall-clock，而定义成：**在预注册时间与内存预算内，独立 spread 或 GU retrain gap 稳定高于 degree。**

## 1. 三种真值必须分开

### 1.1 理论/实现有效性

检查算法是否满足它声称的前提与输出合同：

- corrected IMM 是否使用独立最终 RR batch；
- OPIM-C 是否使用独立 $\mathcal R_1/\mathcal R_2$ 并输出 per-budget lower/upper certificate；
- candidate ground set 是否严格为 canonical train candidates；
- RR roots 是否仍从完整评估节点域采样；
- directed arcs 与 IC Bernoulli edge semantics 是否与当前图合同一致。

这回答“实现是否属于所标注的成熟算法”，不回答它是否比 degree 强。

### 1.2 Selection objective outcome

独立评估：

$$
\sigma(S)=\mathbb E[|\operatorname{Reach}_{\mathrm{IC}}(S)|].
$$

主比较为：

$$
\Delta_{\mathrm{degree}}(M)
=
\sigma(S_M)-\sigma(S_{\mathrm{degree}}).
$$

所有方法必须使用与 selector 内部 RR/MC 完全独立的 common-random evaluator。低 Jaccard 只说明选点不同；只有 $\Delta_{\mathrm{degree}}>0$ 才说明在 IM 目标上超过 degree。

### 1.3 GU downstream outcome

只有通过 spread gate 的方法才进入 GU canary。主指标为：

$$
\Delta RG(M)
=
RG(S_M)-RG(S_{\mathrm{degree}}),
$$

其中 $RG$ 为 approximate unlearning 相对 exact retrain 的 absolute retrain gap。它回答“IM spread 优势是否真的转化为更强的 GU 攻击”，不能由 spread、Jaccard 或 certificate 代替。

## 2. 为什么 IM 不能只有一种 Score

对已经选择的集合 $S$，节点 $v$ 的 IM 价值是条件边际：

$$
\Delta(v\mid S)=\sigma(S\cup\{v\})-\sigma(S).
$$

因为该值随 $S$ 改变，一般不存在一个与 budget/context 无关的静态向量，使其 top-$k$ 精确等于 set-level IM。当前 Hybrid 使用的 Stage 1：

$$
s_{\mathrm{SNI}}(v)=\sigma(\{v\})
$$

已经是完整候选 score，但只表示节点孤立传播能力，不包含种子之间的覆盖重叠。

本轮不把这些语义混成一个 `im_score`，而是显式测试三种静态分数和一种动态输出。

### 2.1 RR-SNI：孤立影响分数

对 $\theta$ 个 RR sets：

$$
\hat s_{\mathrm{SNI}}(v)
=
\frac{n}{\theta}
\sum_{R}\mathbf 1[v\in R].
$$

- 输出：每个 eligible candidate 一个静态 score；
- budget：无关，可切任意 top-$k$ 前缀；
- 保证：估计 singleton spread；没有 top-$k$ IM approximation guarantee；
- 角色：当前 Stage 1 的 RR 加速等价物。

### 2.2 RR-Shapley：全 coalition 平均贡献

对候选集 $C$，本项目使用候选受限推导：

$$
\hat s_{\mathrm{Sh},C}(v)
=
\frac{n}{\theta}
\sum_{R:v\in R}
\frac{1}{|R\cap C|}.
$$

- 输出：每个 eligible candidate 一个静态 attribution score；
- budget：无关；
- 保证：估计 Shapley centrality；没有 top-$k$ IM approximation guarantee；
- 角色：检验“平均群体贡献”能否比 singleton/degree 更好地处理重叠。

原始 SNI/Shapley 区分见 [Chen and Teng](https://arxiv.org/abs/1602.03780)；RR 形式见 [Influence-based Group Shapley](https://arxiv.org/abs/2003.07966)。这里的 $R\cap C$ 适配是项目推导，必须先过 exact-tiny gate。

### 2.3 RR-$k$-semivalue：预算相关平均贡献

固定删除预算 $k$：

$$
s_k(v)
=
\mathbb E_{\substack{T\subseteq C\setminus\{v\}\\|T|=k-1}}
[\Delta(v\mid T)].
$$

对应 RR closed form：

$$
\hat s_k(v)
=
\frac{n}{\theta}
\sum_{R:v\in R}
\frac{
\binom{|C|-|R\cap C|}{k-1}
}{
\binom{|C|-1}{k-1}
}.
$$

- 输出：每个 candidate 一个静态 full score；
- budget：相关，$k$ 必须进入 Score Recipe；
- $k=1$：退化为 RR-SNI；
- 保证：估计固定 coalition-size 下的平均 marginal；没有已知 top-$k$ IM approximation guarantee；
- 角色：最有希望兼容 IF 式 score fusion，同时比 Stage 1 更考虑 budget 与重叠。

Semivalue 的 coalition-size weighting 见 [Szczepański et al.](https://doi.org/10.1609/aaai.v29i1.9215)。上述 RR 公式是项目推导，不预先声称新算法贡献。

### 2.4 RR residual marginal：动态全量分数

对当前未覆盖 RR sets：

$$
s_t(v)=
|\{R:v\in R,\ R\cap S_t=\emptyset\}|.
$$

IMM/OPIM-C 的 maximum-coverage greedy 可在每一步维护所有剩余 candidate 的 residual score。它是最忠实的 set-level 信号，但输出是 context-indexed trace，而不是一个可直接与 IF 后处理相加的静态向量。

正式输出建议保存：

- selected node order；
- 每个已选节点的 accepted residual gain；
- RR count、total incidences、covered count trajectory；
- 可选 top-$L$ per-step trace；
- 不保存不可扩展的 dense $|C|\times k$ 矩阵。

## 3. 方法与输出合同

| 方法 | 首轮位置 | 主要输出 | Full static score | Budget 相关 | 理论/证书状态 |
|---|---|---|---:|---:|---|
| `random` | 小图控制 | selection | 否 | 是 | 无 |
| `degree` | 全部主基线 | full score + ranking | 是 | 否 | 无 IM 保证 |
| `im_batch_celf_current` | 小图 legacy | selection + selected marginals | 否 | 是 | 不继承经典 greedy 保证 |
| `im_celf_strict` | 小图 operational reference | selection + selected marginals | 否 | 是 | 精确 oracle 下有 $1-1/e$；当前有限 MC 无 certificate |
| `im_imm_corrected` | 小图/大图 | selection + residual trace | 否 | 是 | $(1-1/e-\epsilon)$ high-probability；必须使用修正版 |
| `im_opimc` | 小图/大图主方法 | selection + lower/upper certificate | 否 | 是 | anytime / per-budget certificate |
| `im_rr_sni` | 小图/大图 score | full score + ranking | 是 | 否 | singleton estimation only |
| `im_rr_shapley` | 小图/大图 score | full score + ranking | 是 | 否 | Shapley estimation only |
| `im_rr_ksemivalue` | 小图/大图 score | full score + ranking | 是 | 是 | 项目推导；无 IM top-$k$ 保证 |

IMM 的证明纠偏见 [Chen 2018](https://arxiv.org/abs/1808.09363)；OPIM-C 的论文入口见 [Tang et al., SIGMOD 2018](https://doi.org/10.1145/3183713.3183749)。经典 IC 子模性与 degree heuristic 对比见 [Kempe–Kleinberg–Tardos](https://theoryofcomputing.org/articles/v011a004/)。

## 4. 统一数据与扩散合同

| 维度 | 固定口径 |
|---|---|
| Diffusion | static Independent Cascade |
| Primary propagation probability | $p=0.1$，每条 directed arc 独立 Bernoulli |
| Candidate ground set | canonical `train_mask/train_indices` |
| RR root domain | 全评估节点域，不限制到 train candidates |
| Directed graph | 保留 $(u,v)$ 与 $(v,u)$；不重新无向化或合并反向边 |
| Candidate pruning | 主矩阵 `candidate_fraction=1.0`，禁止 degree 预剪枝 |
| Selector seeds | 42、212、2024 |
| Tie-break | score/gain 降序，node ID 升序 |
| Primary theory params | $\epsilon=0.1$、$\delta=0.01$；算法原生参数同时记录 |
| Evaluator | 与 selector 独立的 common RR/live-edge samples |
| Cache | exact-only，graph/candidate/diffusion/algorithm/source/seed/params 全入 Recipe |

禁止 degree 预剪枝是本轮关键约束。若先只保留 top-degree 10% candidates，新方法即使输出不同集合，也无法回答它是否能从完整候选域中真正超过 degree。

## 5. Phase T：exact-tiny 语义 Gate

### 5.1 固定 fixture

使用 6 类 directed graphs，每图 $n\le10$、directed arcs $m\le14$：

1. star/hub；
2. 两个高度重叠的 hubs；
3. directed chain；
4. two-community bridge；
5. asymmetric reverse-reachability；
6. 相同 singleton spread、不同 pairwise redundancy。

每图测试 $p\in\{0.1,0.2\}$、$k\in\{1,2,3\}$，共 36 个 graph-probability-budget contexts。

### 5.2 Exact reference

- 枚举所有 live-edge worlds；
- 枚举所有 $|S|=k$ candidate subsets；
- 得到 exact singleton spread、exact Shapley、exact $k$-semivalue、exact greedy 与 exact OPT；
- RR 估计使用独立种子，逐项检查误差和 candidate-restricted 公式。

### 5.3 必过 Gate

| Gate | 通过条件 |
|---|---|
| Directed semantics | 手算 reachability fixtures 全部一致 |
| SNI | RR estimate CI 覆盖 exact value；误差随样本增长下降 |
| Shapley | efficiency / symmetry / null-player sanity 通过；candidate-restricted 公式与枚举一致 |
| $k$-semivalue | $k=1$ 等于 SNI；固定 $k$ 与 coalition enumeration 一致 |
| IMM/OPIM selection | 所选集合 independent exact spread 不低于预注册理论/经验门 |
| Certificate | OPIM-C lower $\le$ exact spread，reported upper 不低于 exact restricted OPT |
| Determinism | 同 recipe bitwise stable；换 selector seed 形成新 identity |

任何公式/证书 gate 失败，停止后续矩阵并修复；失败结果只作诊断。

## 6. Phase S：三数据集小图主矩阵

### 6.1 配置

| 轴 | 值 |
|---|---|
| Datasets | Cora、CiteSeer、PubMed public Planetoid |
| Candidates | public `train_mask`：140 / 120 / 60 |
| Selector seeds | 42、212、2024 |
| Budgets | $k=3,7,14$ |
| Methods | 9 个，见 §3 |
| Contexts | $3\times3\times3=27$ |
| Method-budget result rows | $27\times9=243$ |

每个 graph/seed 只生成一次共享 RR score bundle，供 SNI/Shapley 使用；$k$-semivalue 从同一 RR bundle 按三个 budget 派生。IMM、OPIM-C 保持各自正式抽样与 certificate 语义，不为了省时间强制共享不允许共享的随机样本。

### 6.2 小图输出

- cold graph load / RR generation / score reduction / selection / write 分段时间；
- warm exact read 与 producer-call sentinel；
- peak RSS；
- RR count、total incidences、mean/max RR size；
- complete score/ranking（适用方法）；
- selection、accepted marginal trace、certificate（适用方法）；
- independent spread、paired difference/ratio vs degree；
- degree–score Spearman/Kendall、Jaccard@k，仅作解释指标。

### 6.3 小图时间 Gate

| 项目 | Gate |
|---|---|
| 共享 RR score bundle cold | 每 cell $\le30$ s |
| 单个派生 score/selection | $\le5$ s，不含共享 RR generation |
| corrected IMM / OPIM-C cold | 每 method-budget $\le30$ s |
| warm exact read | 每 cell $\le1$ s |
| Peak RSS | $\le4$ GiB |

IF 线现有 17-output cold mean/max 为 `6.80/9.16 s`，只作工程参照，不作为 IM pass/fail 的直接数值来源。

## 7. Phase L：ogbn-arxiv 大图 Gate

### 7.1 配置

| 轴 | 值 |
|---|---|
| Dataset | canonical OpenGU ogbn-arxiv processed graph/split |
| Candidates | 运行时从 canonical processed train candidates 解析并记录数量/指纹 |
| Selector seeds | 42、212、2024 |
| Budgets | $0.1\%,0.5\%,1.0\%\times |C|$，向下取整且至少 1 |
| Methods | degree、corrected IMM、OPIM-C、RR-SNI、RR-Shapley、RR-$k$-semivalue |
| Result rows | $3\times3\times6=54$ |
| Candidate pruning | 禁止；`candidate_fraction=1.0` |

current CELF 不重新进入 54 行大图矩阵。已接受的历史 materializer 在 degree-pruned 10%、50 MC 下 cold `13,583.91 s`，作为 legacy time anchor；其 selected set 不能与新 full-candidate 方法作公平 quality 对比。

### 7.2 大图时间与资源 Gate

| 项目 | Gate |
|---|---|
| corrected IMM / OPIM-C cold | 每 method-budget $\le600$ s |
| 共享 full-score RR bundle cold | 每 graph-seed $\le600$ s |
| 三个 score reducer 总计 | $\le60$ s，不含 RR generation |
| Warm end-to-end | $\le6$ s |
| Peak RSS | $\le16$ GiB |
| 相对历史 CELF | 至少 $20\times$ cold speedup，或以更紧 certificate 提供明确补偿 |

首个 seed42、$k=0.1\%|C|$ 是注册 canary。任一主方法超过 600 s、RSS 超过 16 GiB、RR incidences 超过可用磁盘/内存预算，立即停止该方法扩展并记录原因，不静默改成 degree-pruned candidates。

### 7.3 运行环境

- 正式时间必须固定 CPU 型号、物理/逻辑核数、RAM、线程数与编译选项；
- in-repo 语义主矩阵使用单进程、固定线程数；
- 若增加 PNNL Ripples 多核外部对照，单独报告为 systems lane，不与 Python wall-clock 混表；
- 数据必须在运行前存在于 active checkout canonical path，timed run 不下载、不预处理；
- formal run 只能来自 accepted `main` 的 clean SSH active checkout，并记录 full SHA。

## 8. 独立 Spread Evaluator

### 8.1 Common-random paired evaluation

对同一 dataset/seed/budget 的全部方法，使用同一批、与 selector 独立的 RR/live-edge samples。每个 evaluator sample 对方法 $M$ 与 degree 形成 paired observation：

$$
d_i=
\mathbf 1[S_M\cap R_i\ne\emptyset]
-
\mathbf 1[S_{\mathrm{degree}}\cap R_i\ne\emptyset].
$$

按顺序增加独立 evaluator samples，直到：

- paired 95% CI half-width $\le0.5$ 个百分点；或
- 达到预注册上限 2,000,000 RR sets。

不得用 selector 自己的 RR sets 评估同一方法，也不得用 OPIM-C 自报 certificate 代替跨方法独立比较。

### 8.2 Degree 超越 Gate

#### 小图 promotion

某方法进入大图 quality shortlist，需满足：

1. 至少 2/3 datasets 的 mean spread ratio vs degree $\ge1.02$；
2. 对应 paired 95% CI lower bound $>0$；
3. 剩余 dataset 不低于 degree 超过 1%；
4. 满足 §6.3 时间/RSS gate。

#### 大图 promotion

某方法成为 GU canary candidate，需满足：

1. ogbn-arxiv 至少 2/3 budgets 的 spread ratio vs degree $\ge1.02$；
2. paired 95% CI lower bound $>0$；
3. 无 budget 低于 degree 超过 1%；
4. 满足 §7.2 时间/RSS gate。

若没有方法通过，结论应诚实写成“成熟 IM 在本扩散合同下未形成对 degree 的稳定优势”，不通过调整 $p$、candidate pruning 或只挑 winner cell 追求正结果。

## 9. Phase G：条件式 GU Canary

只有通过小图或大图 spread promotion 的最佳 **一个 set-level 方法** 与最佳 **一个 static-score 方法** 可以进入本阶段；若同一方法包揽两类，只保留一个 winner。

### 9.1 首轮 canary

| 轴 | 值 |
|---|---|
| Datasets | Cora、CiteSeer |
| Backbone | GCN |
| GU methods | GIF、GNNDelete |
| Selectors | random、degree、最多 1 个 IM winner |
| GU seeds | 42、212、2024 |
| Budget | canonical OpenGU train-candidate ratio 5% |
| Cells | $2\times2\times3\times3=36$ |

若 static-score 与 set-level 各有独立 winner，先分别与 degree 做 selection/spread 对照；GU 阶段最多加入两个 winner，此时 cells 上限为 48，必须在运行前再次确认。

### 9.2 扩展 Gate

只有 winner 相对 degree 的 paired absolute retrain-gap gain：

$$
\overline{\Delta RG}\ge0.01
$$

且至少在一个 dataset–GU block 三个 seeds 同方向，才扩到 canonical 5 seeds。否则停止，不铺 arxiv GU 或更多方法。

最终“超过 degree 的攻击方法”需要：

- 5-seed paired mean $\Delta RG>0$；
- paired 95% bootstrap CI lower bound $>0$；
- absolute gain 至少 1 个百分点，或 relative gain 至少 10%；
- 不以 raw F1 单一指标替代 retrain gap。

## 10. Artifact 与 Cache 合同

### 10.1 RR bundle

RR hypergraph 不是 per-node score。MVP 可以使用实验专属、typed RR bundle：

```text
graph_fingerprint
candidate_set_hash
root_domain_hash
diffusion_model / p
rr_seed / prng_version
rr_count / total_incidences
rr_offsets + rr_candidate_ids
content_hash
producer_version
```

在架构 gate 通过前，不把它伪装成正式 Cache V2 ScoreArtifact。

### 10.2 Score Artifact

适用于 RR-SNI、RR-Shapley、RR-$k$-semivalue：

```text
ordered candidate IDs
finite full score vector
stable full ranking
score_semantics
budget_context (only k-semivalue)
source_rr_bundle_id
compute_seconds
recipe / content / producer provenance
```

`im_rr_ksemivalue` 的 $k$ 必须进入 Score Recipe；SNI/Shapley 的 $k$ 不进入 Score identity。

### 10.3 Selection Artifact

适用于所有方法：

```text
selected_nodes_ordered
ordered/set hashes
k
source_score_artifact_id or source_rr_bundle_id
accepted marginal trace
certificate payload (IMM/OPIM-C where applicable)
runtime / memory / provenance
```

OPIM-C 的 max-$k$ prefix 不能共享一个 certificate 冒充所有较小 budget 的保证；每个正式 $k$ 必须有独立 certificate record。

## 11. 实现与测试顺序

审批后另开 implementation branch，不在当前文档分支直接开发：

```text
experiments/im_score_benchmark/
  rr_core.py
  score_reducers.py
  selectors.py
  exact_tiny.py
  run_planetoid.py
  run_arxiv.py
  evaluate_spread.py
  aggregate.py
  render_report.py
  tests/
```

顺序：

1. directed RR sampler + inverted index；
2. SNI/Shapley/$k$-semivalue reducers；
3. maximum-coverage greedy trace；
4. corrected IMM；
5. OPIM-C independent dual-sample certificate；
6. exact-tiny tests；
7. small non-formal smoke；
8. 接受实现线到 `main`；
9. clean SSH `main` 上跑 formal Phase S/L；
10. spread gate 通过后再提交/执行 Phase G。

formal 矩阵中若发现代码缺陷，停止矩阵；从 pinned main 建 fix branch，修复/验收/合回 main 后，以新 SHA 和新 artifact identity 重启 gate。

## 12. 预计资源

| 阶段 | 预计开发/运行 | 主要风险 |
|---|---|---|
| RR core + score reducers | 1–2 天 | directed/candidate semantics |
| corrected IMM + OPIM-C | 2–4 天 | sample-size/certificate 复现 |
| exact-tiny gate | 0.5–1 天 | exact enumeration 成本 |
| 三数据集 Phase S | 0.5–1 CPU 日 | strict/current CELF 长尾 |
| ogbn-arxiv Phase L | 0.5–1 CPU 日 | RR incidences / RSS |
| GU canary | 视服务器，36 cells | GPU 与 retrain 成本 |
| 聚合与双格式结果报告 | 0.5–1 天 | 证据/口径漂移 |

首轮不需要本地 GPU；selector 主线为 CPU/RAM workload。GU canary 仍按项目规则走 AutoDL GPU。

## 13. 审批项

本页建议分两次授权：

### 审批 A：实现与 selector 验证

授权范围：

- 建 implementation branch；
- 实现 RR core、3 个 score、corrected IMM、OPIM-C；
- 跑 exact-tiny、Phase S 与注册的 ogbn-arxiv canary/Phase L；
- 不运行任何 approximate-GU cell。

### 审批 B：条件式 GU canary

只有审批 A 结果出现通过 §8.2 的 winner 后，再带具体 winner、预计 cells 与 GPU 预算单独报备。本页的 Phase G 是预注册模板，不等于已授权执行。

## 14. 已覆盖与未覆盖

### 计划覆盖

- small/large cold 与 warm 时间；
- peak RSS 与 RR hypergraph 规模；
- mature set-level algorithm guarantee/certificate；
- 三种 full-score 语义；
- independent spread vs degree；
- 条件式 GU retrain-gap vs degree；
- Cache V2 identity 与 fail-closed provenance。

### 首轮不覆盖

- fair/robust/adaptive/competitive IM；
- LT 或 learned diffusion probability；
- SUBSIM/HIST/SKIM 系统优化；
- GPU/CUDA RR generator；
- GAT/GIN 或更多 GU families；
- 将 $k$-semivalue/联合 IF 融合作为论文新算法 claim。

## 15. 解释规则

| 观察 | 可以说 | 不能说 |
|---|---|---|
| IM 与 degree Jaccard 很低 | 两者选择不同集合 | IM 超过 degree |
| Independent spread 高于 degree | 在固定 IC 合同下 IM 目标更好 | GU 攻击一定更强 |
| OPIM-C certificate 通过 | 该 budget 的实现输出满足已审计证书合同 | 所有 prefix/所有 diffusion 设置都有同一保证 |
| Shapley/$k$-semivalue score 有效 | full-score 接口可用，且有明确贡献语义 | top-$k$ score 等价于 set-level IM |
| 大图 20× 加速 | 相对历史 full pipeline cold anchor 显著改进 | 比 degree 更快 |
| GU retrain gap 高于 degree | 在该 dataset/GU/seed 合同下攻击更强 | 所有 GU 方法或 backbone 普遍成立 |
| 没有方法通过 degree gate | 在本合同下未找到稳定胜者 | IM 理论无效或所有传播模型都不如 degree |

## 16. 一句话记忆

> 本轮不评“哪个 IM 算法更新”，而评“成熟 IM 是否在可接受时间内给出可审计的 selection/score，并在独立 spread、随后在 GU retrain gap 上真正超过 degree”；不同 score 语义和 set-level certificate 必须分开验收。
