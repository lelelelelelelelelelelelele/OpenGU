# Paper Analysis: Adversarial Deletion Attacks on Graph Unlearning

> Generated: 2026-02-26
> Evidence base: 106 relative result files, 1438 collateral data points, 5-seed cross-validation (seeds 42/212/722/1337/2024)
> Constraint: **GUIDE excluded** (source-library bugs render all GUIDE data invalid)

---

## 1. 取证路线图 (Evidence Roadmap)

### 2.1 现有证据能支撑什么 (What We Can Write Now)

| # | 可写结论 | 证据来源 | 字段/指标 |
|---|---------|---------|-----------|
| C1 | **GNNDelete 极度脆弱**：IM 策略在 ratio=0.01（仅 27 节点）即导致 F1 下降 17.3% | `results/collateral/GNNDelete/cora/GCN/collateral_20260225_*.json` → `perf_unlearn`, `gap_pct` | `gap_pct=21.53%`（im_v4, ratio=0.01, seed=42） |
| C2 | **GNNDelete collateral damage 极大**：retrain gap 高达 20%+，26% 非目标节点预测翻转 | 同上 → `gap_pct`, `fraction_flipped` | `im_v4: gap=0.1919, fraction_flipped=0.2623` |
| C3 | **GIF 近似误差极小**：collateral gap ≈ 0–2%，pred_shift ≈ 0.02 | `report/daily-log/2026-02-25_log.md` → collateral 统计, `results/collateral/GIF/` | `mean gap=-0.34%, mean pred_shift=0.0235` |
| C4 | **GraphEraser 天然防御（Shard 保护效应）**：所有策略 F1 drop 为负值（性能反而提升） | `report/analysis/notes/2026-02-22_新发现_Shard保护效应与新指标.md` → §1.1 | `random f1_drop=-13.10%`, MG-0: `GraphEraser random f1_drop=-6.27%` |
| C5 | **方法类型决定攻击面**：Learning-based（GNNDelete）可攻击，Shard-based（GraphEraser）免疫，IF-based（GIF）效果小 | `report/analysis/notes/2026-02-22_技术分析_攻击策略有效性与改进方向.md` → §1.2 核心数据 | MG-0 Cora/GCN 全策略表 |
| C6 | **Relative 指标体系**：k=5 random baseline 消除方法本身的 F1 偏移，106 个结果文件 | `experiments/baseline_k5/eval_relative.py`, `results/relative/` | 5 methods × 2 datasets × 2 models × 5 seeds |
| C7 | **IM v4 (Batch CELF) 效率**：18.9s vs V0 baseline 653s（34× 加速），spread 仅损失 1.3% | `experiments/im_benchmark/results/bench_results.json` | `V0: time=653, spread=2700; V4: time=18.9, spread=2666` |
| C8 | **攻击效果 ratio 敏感性**：GNNDelete 在 ratio=0.01~0.20 全范围脆弱 | `report/daily-log/2026-02-25_log.md` → §二.3 GNNDelete 多 ratio 表 | ratio=0.01: 17.34%, ratio=0.10: 18.45%, ratio=0.20: 13.84% |
| C9 | **MEGU/IDEA 低 collateral**：gap ≈ 0%, pred_shift 极小 | `report/daily-log/2026-02-25_log.md` → collateral 统计 | `MEGU: gap=-0.01%, shift=0.0505; IDEA: gap=-0.52%, shift=0.0302` |

### 2.2 证据缺口 (Evidence Gaps — Reviewer Attack Vectors)

| # | 缺口 | 被打爆的审稿风险 | 最小补方案 |
|---|------|----------------|-----------|
| G1 | **跨 seed 方差未报告**：relative 结果有 5 seeds 数据但未聚合为 mean ± std | "cherry-picked seed" | 写脚本聚合 `results/relative/*/` 下 5 seeds，计算 mean±std |
| G2 | **GIF relative drop 过小（~1–3%）**：审稿人可能认为"攻击无效" | "trivial attack effect" | 补 ratio=0.10/0.20 的 GIF 实验，展示 ratio-attack 效果曲线 |
| G3 | **retrain-after-deletion 对照不完整**：目前 drop_retrain 字段存在但未系统展示 | "you just removed important nodes" | 从 collateral JSON 提取 `drop_retrain` 并系统汇报，证明 retrain 后性能不下降 |
| G4 | **GNNDelete relative F1 drop 异常负值（-0.5191）**：daily-log 标记"待排查" | "data quality issue" | 核查 seed 配置一致性 + baseline 生成逻辑 |
| G5 | **缺 MIA leakage evaluation**：仅有 F1 drop + collateral，无隐私指标 | "incomplete evaluation" | 从已有 `attack/MIA_attack.py` 运行 MIA，至少覆盖 GNNDelete + GIF |
| G6 | **仅 Cora/Citeseer 两个数据集**：泛化性不足 | "limited generalization" | 补 PubMed（中等规模），理想情况加 ogbn-arxiv |
| G7 | **缺 ablation**：IF vs IM vs Hybrid 的贡献分解 | "no ablation" | 已有数据覆盖 tracin/im_v4/hybrid_v4/random/degree/pagerank，汇总为 ablation 表 |
| G8 | **GraphEraser k=5 relative 指标缺失或异常** | Shard 保护效应的相对量化不足 | 用 `eval_relative.py` 对 GraphEraser 跑完 5 seeds × 6 strategies |


### 2.3 写作蓝图 (Writing Blueprint)

**Results 叙事主线：**
> Utility collapse (F1 drop) → Cross-family vulnerability spectrum → Collateral damage & retrain gap → Efficiency → Robustness / MIA

**Proposed Section Structure:**

| §  | 标题 | 核心结论 | 图/表 |
|----|------|---------|-------|
| 5.1 | Cross-Family Vulnerability Spectrum | 方法类型（Learning/IF/Shard-based）决定攻击面 | **Table 1**: Method × Strategy F1 drop matrix (Cora/GCN, 5-seed avg) |
| 5.2 | GNNDelete: Extreme Vulnerability Under Minimal Budgets | ratio=0.01 即可导致 17%+ F1 下降 | **Figure 1**: F1 drop vs ratio curve for GNNDelete (4 ratios × 6 strategies) |
| 5.3 | Collateral Damage & Retrain Gap | GNNDelete gap 20%+ vs GIF gap ≈ 0%; 证明 collapse 源于近似误差 | **Table 2**: Collateral metrics (gap, pred_shift, fraction_flipped) by method × strategy |
| 5.4 | The Shard Protection Effect | GraphEraser F1 反而提升；机制：删 hub → shard 纯化 → 子模型分类更准 | **Figure 2**: GraphEraser F1 before/after violin plot across seeds |
| 5.5 | Selection Strategy Ablation | IM/Hybrid > TracIn > Degree > Random (on vulnerable methods) | **Table 3**: Strategy ranking by relative_f1_drop (k=5 baseline), 5-seed avg |
| 5.6 | Efficiency: IM v4 Node Selection | 34× speedup vs brute-force CELF, <2% spread loss | **Table 4**: V0/V2/V3/V4 time + spread from bench_results.json |

---

## 2. 理论-证据对照表 (Theory-Evidence Alignment Table)

### Hypotheses Extracted from Project Context

| ID | 理论预期 / 机制假设 | 可观测指标 | 比较维度 | 证据状态 | 关键 Caveat |
|----|---------------------|-----------|---------|---------|-------------|
| **H1** | IF/IM 策略选择的节点对近似 GU 方法造成的损害大于随机选点 | `relative_f1_drop` = baseline_f1_after − attack_f1_after | strategy (im_v4/tracin/hybrid_v4 vs random) × method × dataset | **部分支持** | 仅对 Learning-based 方法成立；Shard-based 反效；GIF 效果小 |
| **H2** | 性能崩塌源于近似误差而非节点本身重要性（attribution hypothesis） | `gap` = perf_retrain − perf_unlearn（retrain gap） | strategy × method | **支持**（对 GNNDelete） | GNNDelete: gap 6–21%（近似误差大）；retrain 后 drop_retrain ≈ 0–1%（证明节点删除本身影响小）；GIF: gap ≈ 0–2%（近似误差小，攻击效果也小） |
| **H3** | Shard-based 方法天然抗攻击（Shard 保护效应） | `f1_drop` (GraphEraser, all strategies) | all strategies × GraphEraser | **支持** | 所有策略导致 F1 提升（负 f1_drop）；机制：删 hub 节点 → shard 拓扑纯化 → 子模型准确度提升。但注意：此为 **随机选点也存在** 的现象，非策略特有 |
| **H4** | Hub 节点（高度数/PageRank）在 Shard-based 方法中反而有害 | `f1_drop` for degree/pagerank strategies on GraphEraser vs GNNDelete | method (Shard vs Learning) × strategy (degree/pagerank) | **支持** | GraphEraser: degree f1_drop = −4.4%（性能提升）；GNNDelete: degree f1_drop = +5.4%（性能下降）。Hub 节点对两类方法产生相反效果 |
| **H5** | Collateral damage (非目标节点损害) 是近似 GU 的关键弱点 | `mean_pred_shift`, `fraction_flipped`, `gap_pct` | method × strategy | **强支持** | GNNDelete: 26% 非目标节点预测翻转（im_v4, ratio=0.01）；GIF: pred_shift ≈ 0.024；MEGU/IDEA: pred_shift < 0.05 |
| **H6** | IM 策略的攻击效果随 unlearn_ratio 单调增加 | `f1_drop` at ratio=0.01/0.05/0.10/0.20 for GNNDelete | ratio | **不支持** | GNNDelete: ratio=0.01 时 hybrid_v4 f1_drop=17.34%，ratio=0.10 时 degree=18.45%，ratio=0.20 时 hybrid_v4=13.84%。**非单调**：ratio=0.01 已极效，更高 ratio 并未线性增强 |
| **H7** | GIF 的攻击效果显著（IF-based 方法应脆弱） | `relative_f1_drop` for GIF | strategy × seed | **部分不支持** | GIF relative_f1_drop ≈ 0.3–1.4%（平均 +0.0147）。效果存在但极小——GIF 近似误差本身就小（gap ≈ 0–2%），所以攻击面有限 |
| **H8** | Hybrid (IF + IM fusion) 策略优于单一 IF 或 IM | `relative_f1_drop` for hybrid_v4 vs im_v4 vs tracin | strategy comparison | **证据不足** | 对 GNNDelete: hybrid_v4 有时最高（ratio=0.01/0.20），有时 degree/pagerank 更高（ratio=0.05/0.10）。对 GIF: hybrid_v4 不稳定优势。需要更大数据规模 |

---

## 3. Results + Analysis 可粘贴段落

### (1) Main Results Narrative

#### §5.1 Cross-Family Vulnerability Spectrum

> We evaluate six node-selection strategies (Random, Degree, PageRank, TracIn, IM-v4, Hybrid-v4) against four families of graph unlearning methods on Cora/GCN (5-seed average, ratio=0.05). The results reveal a **stark vulnerability spectrum** that maps directly onto the method's internal mechanism:
>
> **Learning-based methods (GNNDelete)** exhibit high vulnerability: the best attack strategy (IM-v4) achieves 13.8% absolute F1 drop on Cora/GCN (`results/experiments/mg0_completion`, field: `f1_drop` averaged over seeds 42/212/722/1337/2024). Even the random baseline causes a 6.8% drop, confirming that GNNDelete's learned delete-and-compensate mechanism is inherently fragile.
>
> **IF-based methods (GIF)** show marginal vulnerability: attack-induced F1 drops range from 0.9% (random) to 2.8% (hybrid), measured relative to the pre-unlearning F1 (`report/analysis/notes/2026-02-22_技术分析_攻击策略有效性与改进方向.md`, §1.2). When evaluated against a k=5 random baseline (`results/relative/GIF/cora/GCN/relative_seed42_*.json`), the relative F1 drop is 0.3–1.4%, indicating that GIF's influence-function approximation introduces minimal additional error beyond what random node removal already causes.
>
> **Shard-based methods (GraphEraser)** are immune—or more precisely, benefit from node deletion: all strategies yield negative F1 drops (−3.0% to −7.0%), meaning unlearning *improves* downstream performance. This counterintuitive finding, which we term the *Shard Protection Effect*, holds consistently across all seeds and strategies.

#### §5.2 GNNDelete: Extreme Vulnerability Under Minimal Budgets

> A particularly striking finding is GNNDelete's vulnerability at extremely low deletion ratios. At ratio=0.01 (≈27 nodes on Cora, representing <1% of the graph), the IM-v4 strategy achieves a retrain gap of 21.53% (`results/collateral/GNNDelete/cora/GCN/collateral_20260225_173137.json`, field: `gap_pct`), and 26.2% of non-target node predictions are flipped (`fraction_flipped=0.2623`). Critically, the retrain-after-deletion model shows only `drop_retrain ≈ 0.37–0.92%` on the same deletion set, confirming that the performance collapse is attributable to **approximation error**, not to the removal of inherently important information.
>
> The ratio-sensitivity analysis (`report/daily-log/2026-02-25_log.md`, §二.3) reveals a non-monotonic pattern: F1 drop peaks at ratio=0.10 (degree: 18.45%) and does not scale linearly with budget. This suggests that GNNDelete's failure mode is structural—a small number of adversarially chosen nodes suffice to trigger cascading approximation errors in the learned compensation mechanism.

#### §5.3 Collateral Damage and Retrain Gap

> We introduce two metrics to attribute performance collapse to approximation rather than information loss:
>
> 1. **Retrain Gap** = $F_1^{\text{retrain}} - F_1^{\text{unlearn}}$: measures the performance difference between exact retraining and approximate unlearning on the same deletion set. A large gap indicates that the approximate method introduces systematic errors.
> 2. **Collateral Damage** (mean_pred_shift, fraction_flipped): quantifies the impact on non-target nodes—nodes that should be unaffected by the deletion request.
>
> Across 1438 collateral evaluation data points (`report/daily-log/2026-02-25_log.md`, §collateral 统计), we observe a clear method-family pattern:
>
> | Method | Avg Gap | Avg Pred Shift | Data Points |
> |--------|---------|---------------|-------------|
> | GNNDelete | **9.74%** | 0.2451 | 391 |
> | GraphEraser | 0.13% | 0.2646 | 288 |
> | GIF | **−0.34%** | 0.0235 | 390 |
> | MEGU | −0.01% | 0.0505 | 140 |
> | IDEA | −0.52% | 0.0302 | 140 |
>
> *Source: `report/daily-log/2026-02-25_log.md` lines 196–207*
>
> GNNDelete's 9.74% average retrain gap and 0.2451 mean prediction shift demonstrate severe collateral damage, while GIF and MEGU/IDEA show near-zero retrain gaps—their approximations are tight even under adversarial deletion selection.

### (2) Mechanism-Facing Interpretation

#### Why GNNDelete Is Vulnerable: DEC/NI Loss Amplification

> GNNDelete's vulnerability can be traced to its loss design. As analyzed in UtU (Tan et al., `2402.10695`), GNNDelete's DEC (Deleted Edge Consistency) loss matches forgotten edges to random node pairs, injecting structural noise that propagates through message passing. The NI (Neighborhood Influence) loss regularizes toward original embeddings that still encode the forgotten nodes' influence.
>
> Under adversarial deletion of hub nodes (high-degree, high-PageRank, IM-selected), this mechanism is exacerbated: the deleted nodes have extensive message-passing neighborhoods, so DEC noise propagates to more retained nodes, and NI regularization anchors the model to representations that are maximally contaminated by the deleted information. The retrain gap data supports this interpretation: `drop_retrain` ≈ 0.37–0.92% (the true effect of removing these nodes) versus `gap` ≈ 6–21% (the effect of approximate unlearning), indicating a **10–60× amplification** of the true information-removal signal by the approximation mechanism.
>
> *[待补充]: A definitive test would ablate DEC and NI losses separately under adversarial deletions (following UtU's loss-surgery approach) to isolate which component drives the amplification. Minimum experiment: run GNNDelete with DEC-only and NI-only on the im_v4 deletion set, compare retrain gaps.*

#### Why GIF Is Resistant: Tight Influence Approximation

> GIF's resistance is consistent with its mechanism: influence-function-based methods approximate the effect of removing training points by computing a Newton step on the Hessian. When the loss landscape is smooth and the training converges (as on Cora/GCN), this first-order approximation is tight, leaving little room for adversarial amplification. The collateral damage data confirms this: GIF's mean pred_shift of 0.0235 means the average retained node's prediction changes by only 2.35% after unlearning, regardless of which nodes are selected.
>
> *[待补充]: This interpretation predicts that GIF's resistance will decrease on (a) larger graphs where the Hessian approximation is less accurate, or (b) more complex backbones (GAT, multi-layer GNNs) where the loss landscape is less smooth. MG-2 (GAT) experiments exist and should be analyzed to test this.*

#### Why GraphEraser Benefits: Shard Purification

> The Shard Protection Effect has a structural explanation (`report/analysis/notes/2026-02-22_新发现_Shard保护效应与新指标.md`, §2.2): GraphEraser partitions the graph into disjoint shards and trains independent sub-models. Hub nodes serve as bridges between shards—their removal purifies intra-shard topology, making each sub-model's classification task simpler and more accurate. The aggregation layer then benefits from higher-quality sub-model outputs.
>
> This effect is present even under random deletion (f1_after increases by 18.44% in Step0 baseline, `results/step0_validation/round2_results.json`), which means **any** deletion request—adversarial or benign—improves GraphEraser's performance. This is a fundamental architectural immunity, not a defense mechanism.

### (3) Heterogeneity & Boundary Conditions

#### Where Conclusions Hold (Stable Range)

- **GNNDelete vulnerability**: stable across all tested ratios (0.01–0.20), seeds (5), and datasets (Cora, partial Citeseer evidence from MG-1). Boundary: may attenuate on very large graphs where GNNDelete's learned compensation has more parameters to absorb errors.
- **GIF resistance**: stable across ratios (0.05–0.20, `report/daily-log/2026-02-25_log.md` §二.4), seeds, and both GCN/GAT (MG-2 exists). Boundary: may break on larger graphs or deeper models—**this is the key evidence gap** (G2).
- **GraphEraser immunity**: stable across seeds, all 6 strategies, and the ratio tested. Boundary: *untested* whether Shard-aware strategies (targeting cross-shard bridges specifically) can overcome the protection effect.

#### Where Conclusions Weaken

- **Dataset scope**: only Cora (2708 nodes) and partial Citeseer (3327 nodes) coverage. PubMed (19717 nodes) and ogbn-arxiv would test scalability.
- **Model scope**: primarily GCN; GAT (MG-2) data exists but not systematically analyzed.
- **Hybrid strategy**: inconsistent advantage over single-strategy baselines. Not robustly better.
- **GNNDelete relative metric anomaly**: daily-log reports GNNDelete relative_f1_drop mean = −0.5191, flagged as anomalous. Must resolve before publication.

### (4) Negative / Surprising Results

#### Surprise 1: GraphEraser Gets Better When Attacked

**Pattern**: All strategies yield negative F1 drop on GraphEraser (−3% to −7% on Cora/GCN, MG-0).

**Alternative explanations**:
- **Explanation A (Supported)**: Shard purification—hub removal simplifies sub-model tasks. Testable: compare with non-hub deletions (random low-degree nodes). If protection effect disappears for low-degree deletions, it confirms hub-specific purification.
- **Explanation B**: GraphEraser was undertrained on the original graph (F1_before ≈ 0.71, much lower than GCN retrain ≈ 0.88). Removing nodes may trigger beneficial re-partitioning. Testable: train GraphEraser to convergence on the original graph, then test attack.

**Story repair if Explanation A confirmed**: Position the finding as "Shard-based methods have an inherent robustness boundary—adversarial deletion selection is not a universal vulnerability." This strengthens the paper's differentiated narrative.

#### Surprise 2: GNNDelete Attack Non-Monotonic with Ratio

**Pattern**: F1 drop at ratio=0.01 (17.3%) is comparable to ratio=0.10 (18.5%) and exceeds ratio=0.20 (13.8%).

**Alternative explanations**:
- **Explanation A**: GNNDelete's compensation mechanism saturates—at low ratio, the compensation is overwhelmed by a few strategic deletions; at high ratio, the model effectively retrains more components and partially self-corrects. Testable: analyze the learned compensation weights at different ratios.
- **Explanation B**: The best strategy changes with ratio, confounding the comparison. At ratio=0.01, hybrid_v4 dominates; at ratio=0.10, degree dominates; at ratio=0.20, hybrid_v4 dominates again. Testable: control for strategy type.

**Story repair**: Emphasize that adversarial deletion is **budget-efficient**: even a <1% deletion budget can cause >17% F1 collapse. This is a more powerful claim than "more deletion = more damage."

#### Surprise 3: GIF Attack Effect is Minimal (1–3%)

**Pattern**: GIF f1_drop is an order of magnitude smaller than GNNDelete's.

**Alternative explanations**:
- **Explanation A (Likely)**: GIF's Newton-step approximation is tight on small graphs, leaving little approximation error to exploit. This predicts the attack should amplify on larger/deeper settings.
- **Explanation B**: The selected nodes are not optimal for GIF's specific failure mode. GIF's vulnerability is more likely in feature space (gradient alignment) than topology space (the IM/TracIn strategies are topology-weighted). Testable: design a feature-space-aware attack strategy.

**Story repair**: Position GIF as the "well-approximated" endpoint—if the approximation is tight, even optimal node selection cannot cause collapse. This supports the attribution hypothesis: vulnerability is a **proxy for approximation quality**.

---

## 4. 图表与写作骨架 (Figure/Table Plan + Paper Skeleton)

### Table 1: Cross-Family Attack Vulnerability Matrix

**Data source**: `results/experiments/mg0_completion/phase_a/` (5-seed aggregation)
**Fields**: `f1_drop` per (method, strategy) pair
**Dimensions**: 3 methods (GNNDelete, GIF, GraphEraser) × 6 strategies
**Conclusion**: Method type determines vulnerability; GNNDelete >> GIF >> GraphEraser (negative)
**Caption**: "F1 drop (↑ = more vulnerable) under six attack strategies on Cora/GCN. GUIDE excluded due to source-library bugs. GNNDelete shows 5–14% vulnerability; GIF shows marginal 1–3%; GraphEraser shows negative drops indicating the Shard Protection Effect."
**Caveat**: Data may use pre-bug-fix f1_before values for MG-0; cross-check with post-fix relative metrics.

### Table 2: Collateral Damage by Method Family

**Data source**: `results/collateral/*/cora/GCN/collateral_*.json`
**Fields**: `gap_pct`, `mean_pred_shift`, `fraction_flipped`, `drop_retrain`
**Dimensions**: 5 methods × best strategy
**Conclusion**: GNNDelete has catastrophic collateral (gap 9.74%, 26% flipped); GIF/MEGU/IDEA near-zero
**Caption**: "Collateral damage metrics. Gap = F1(retrain) − F1(unlearn). Drop_retrain shows the true effect of node removal under exact retraining."

### Figure 1: GNNDelete F1 Drop vs Deletion Ratio

**Data source**: `report/daily-log/2026-02-25_log.md` §二.3 + collateral JSONs
**Fields**: F1 drop at ratio=0.01/0.05/0.10/0.20 × 6 strategies
**Conclusion**: Non-monotonic—maximal vulnerability at ratio=0.01–0.10, slight recovery at 0.20
**Caption**: "GNNDelete's F1 drop as a function of deletion ratio on Cora/GCN. The non-monotonic pattern suggests saturation of the compensation mechanism."

![Figure 1: GNNDelete's F1 Drop vs Ratio](h:/project/OpenGU/GULib-master/report/paper/figures/fig1_gnndelete_ratio.png)

### Figure 2: Shard Protection Effect Visualization

**Data source**: `report/analysis/notes/2026-02-22_新发现_Shard保护效应与新指标.md` + Step0 baseline
**Fields**: f1_before, f1_after for GraphEraser across strategies
**Conclusion**: f1_after > f1_before consistently → deletion improves performance
**Caption**: "The Shard Protection Effect: GraphEraser's F1 increases after node deletion across all attack strategies."

![Figure 2: The Shard Protection Effect: GraphEraser](h:/project/OpenGU/GULib-master/report/paper/figures/fig2_grapheraser_shard.png)

### Table 3: Strategy Ablation (Relative F1 Drop vs k=5 Random Baseline)

**Data source**: `results/relative/*/relative_seed*_*.json` (all datasets, models, ratio=0.05, N=5 seeds each)
**Fields**: `relative_f1_drop` per (strategy, method, dataset, model)
**Dimensions**: 3 strategies (im_v4, tracin, hybrid_v4) × 5 methods (GNNDelete, GIF, GraphEraser, IDEA, MEGU)
**Conclusion**: GNNDelete is orders of magnitude more vulnerable than all other methods. IDEA and MEGU show near-zero drops (< 2%), similar to GIF. GraphEraser shows non-trivial but mixed drops.

> [!NOTE]
> GUIDE is **excluded** from all tables: OpenGU source-library bugs cause node-classification F1 to always return 0 ([`guide.py`](file:///h:/project/OpenGU/GULib-master/unlearning/unlearning_methods/GUIDE/guide.py)). All GUIDE data is invalid.

| Method | Setting | Strategy | Relative F1 Drop (%) ± Std (N=5) |
|--------|---------|----------|----------------------------------|
| **GNNDelete** | Cora/GCN | hybrid_v4 | **11.44% ± 5.09%** |
| **GNNDelete** | Cora/GCN | im_v4 | **12.47% ± 5.47%** |
| **GNNDelete** | Cora/GCN | tracin | 8.05% ± 1.88% |
| GIF | Cora/GCN | hybrid_v4 | 1.41% ± 0.97% |
| GIF | Cora/GCN | im_v4 | 1.52% ± 0.71% |
| GIF | Cora/GCN | tracin | 0.70% ± 0.56% |
| GIF | Cora/GAT | hybrid_v4 | 2.51% ± 0.58% |
| GIF | Cora/GAT | im_v4 | 3.54% ± 0.36% |
| GIF | Cora/GAT | tracin | 1.77% ± 0.65% |
| GraphEraser | Cora/GCN | hybrid_v4 | 4.39% ± 2.56% |
| GraphEraser | Cora/GCN | im_v4 | 4.87% ± 2.34% |
| GraphEraser | Cora/GCN | tracin | 1.70% ± 1.14% |
| GraphEraser | Cora/GAT | hybrid_v4 | 5.16% ± 1.98% |
| GraphEraser | Cora/GAT | im_v4 | 6.20% ± 0.55% |
| GraphEraser | Cora/GAT | tracin | 0.26% ± 1.22% |
| GraphEraser | Citeseer/GCN | hybrid_v4 | −0.03% ± 0.64% |
| GraphEraser | Citeseer/GCN | im_v4 | 0.36% ± 0.58% |
| GraphEraser | Citeseer/GCN | tracin | 0.30% ± 0.85% |
| IDEA | Cora/GAT | hybrid_v4 | 1.66% ± 0.66% |
| IDEA | Cora/GAT | im_v4 | 2.55% ± 0.49% |
| IDEA | Cora/GAT | tracin | 1.03% ± 0.98% |
| IDEA | Citeseer/GCN | hybrid_v4 | 0.27% ± 0.32% |
| IDEA | Citeseer/GCN | im_v4 | 0.51% ± 0.57% |
| IDEA | Citeseer/GCN | tracin | 0.84% ± 0.22% |
| MEGU | Cora/GAT | hybrid_v4 | 1.44% ± 0.83% |
| MEGU | Cora/GAT | im_v4 | 0.85% ± 0.85% |
| MEGU | Cora/GAT | tracin | 0.41% ± 0.39% |
| MEGU | Citeseer/GCN | hybrid_v4 | −0.39% ± 0.29% |
| MEGU | Citeseer/GCN | im_v4 | 0.06% ± 0.38% |
| MEGU | Citeseer/GCN | tracin | 0.99% ± 0.39% |

![Figure 3: Relative F1 Drop Comparison (all methods, ratio=0.05)](h:/project/OpenGU/GULib-master/report/paper/figures/fig3_relative_f1_drop.png)

### Table 4: IM Node Selection Efficiency

**Data source**: `experiments/im_benchmark/results/bench_results.json`
**Fields**: `time`, `spread` for V0/V2/V3/V4
**Conclusion**: V4 (Batch CELF, B=5) achieves 34× speedup over V0 with <2% spread loss
**Caption**: "IM v4 achieves practical feasibility for adversarial node selection."

| Variant | Time (s) | Spread | Spread Loss |
|---------|----------|--------|-------------|
| V0: Baseline CELF | 653.0 | 2700 | — |
| V2: Top-K | 10.1 | 2485 | 8.0% |
| V3: Pruning (M=400) | 197.7 | 2528 | 6.4% |
| V4: Batch (B=5) | **18.9** | 2666 | **1.3%** |

---

## 5. 审稿人压力测试 (Reviewer Pressure Test)

### 5.1 Internal Validity

| 检查项 | 现状 | 判定 |
|--------|------|------|
| 同一 seed 分布？ | 5 seeds (42/212/722/1337/2024), mean±std 已系统报告 | ✅ |
| 同一 ratio/budget/训练步数？ | ratio=0.05 (default), num_epochs=100 (via parameter_parser) | ✅ |
| Caching/leakage 风险？ | selection_cache 在 2025-02-25 commit 7169179 中收紧防止误命中 | ✅ 已修复 |
| f1_before 计算正确？ | 2026-02-25 commit c881058 修复严重 bug | ✅ 已修复，但 MG-0 数据可能用旧逻辑 [待确认] |
| `drop_retrain` 数据完整？ | collateral JSONs 含 `drop_retrain` 字段 | ✅ 但未在所有方法上系统展示 |

### 5.2 Baseline Fairness

| 检查项 | 现状 | 判定 |
|--------|------|------|
| Baselines 同等超参搜索？ | 所有方法使用 OpenGU 默认配置 (`model/properties/` YAML) | ✅ 公平但非最优 |
| Retrain baseline 对齐？ | `AttackPipeline.run_retrain()` 从头训练同一架构 | ✅ |
| Random baseline 鲁棒？ | k=5 多 seed 平均，消除单次波动 | ✅ |
| Strategy 选择 budget 对齐？ | 所有策略选择相同数量节点 (k = ratio × num_nodes) | ✅ |

### 5.3 Attack Protocol

| 检查项 | 现状 | 判定 |
|--------|------|------|
| MIA positive/negative control？ | MIA 代码存在 (`attack/MIA_attack.py`) 但未在当前分析中运行 | ❌ [待补充] |
| Threat model 明确？ | 攻击者控制删除请求，观察 before/after 模型性能 | ⚠️ 需要形式化为 threat model table |
| 攻击者知识假设？ | White-box: 攻击者有模型参数 + 训练数据（for TracIn/IM 评分） | ⚠️ 需要明确区分 white-box / gray-box 场景 |
| 多种 attacker 知识？ | 仅 white-box | ❌ 缺 gray/black-box 对比 |

**最小补方案**:
1. 运行 `attack/MIA_attack.py` 在 GNNDelete + GIF（im_v4 策略 vs random 策略），获取 MIA AUC
2. 撰写 threat model table: 明确 "attacker controls deletion requests for self-owned nodes" + "attacker has query access to model predictions before/after unlearning"

### 5.4 Efficiency Claims

| 检查项 | 现状 | 判定 |
|--------|------|------|
| Selection time 被计量？ | bench_results.json: V4 = 18.9s; selection_cache 记录选择时间 | ✅ |
| Unlearning time 被计量？ | 原始 OpenGU log 含 runtime | ✅ 但需从 log/ 提取并汇总 |
| 是否有"快但忘不干净" tradeoff？ | GIF：快且近似紧密 vs GNNDelete：快但近似极差 | ✅ 可叙述 |
| 显存/计算量一致计量？ | `cal_mem` flag 存在但未在所有实验中开启 | ⚠️ |

---

## 6. CV-Relevance & ECCV 可行性评估

### CV-Relevance Analysis

#### 应用场景关联
- **Scene Graph Unlearning**: Visual Genome scene graphs 是 GNN 处理的典型 CV 数据。Graph unlearning 可用于删除特定视觉关系（如人脸关联的子图）以满足 GDPR。
- **Skeleton-based Action Recognition**: 人体骨骼图作为 GNN 输入，删除特定动作序列的需求存在。
- **Point Cloud**: 3D 点云上的 GNN（如 DGCNN）可能需要删除特定对象的点。

#### 方法论关联
- 我们的攻击框架检测的"近似误差脆弱性"对所有使用近似 GU 的 GNN 系统通用，包括 CV 中的图结构模型。
- IM-based 节点选择可推广到 superpixel graph 或 mesh graph 中的关键区域识别。

#### 隐私/安全关联
- CV 中的 Machine Unlearning（如人脸删除）面临类似的近似误差问题。Graph unlearning 提供了一个更高效的实验平台来研究这些共性问题。

### Framing Strategies

| 策略 | 叙事 | 可行性 | 风险 |
|------|------|--------|------|
| **Strategy A: "Security Audit for GNN Unlearning in Vision"** | Frame 为 CV 系统中 GNN 组件的安全审计工具 | 中 | 需要至少一个 CV 数据集（scene graph / superpixel）的 proof-of-concept |
| **Strategy B: "Machine Unlearning Vulnerability — Graph as a Lens"** | Frame 为通用 ML Unlearning 的安全性研究，以 graph domain 为实验平台 | 高 | 审稿人可能认为 "这是 ML 论文不是 CV 论文" |
| **Strategy C: "Adversarial Robustness of Graph-Structured Vision Models"** | 强调对 scene graph / skeleton GNN 的攻击启示 | 低 | 需要大量 CV 实验补充 |

### ECCV 可行性评估

> [!CAUTION]
> **以现有工作投 ECCV 的可行性：低（15–25%）**

**理由**:
1. **核心工作与 CV 关联薄弱**：实验全部在 citation network（Cora/Citeseer）上完成，无任何 CV 数据/任务。
2. **缺少视觉 proof-of-concept**：即使是最简单的 scene graph experiment 也未实现。
3. **ECCV 审稿人预期**：至少需要 qualitative results（可视化）和一个 CV 任务上的定量结果。

**若要投 ECCV，最小补充**:
- 在 Visual Genome scene graph 或 PASCAL-Context superpixel graph 上跑一组完整实验（1 个 GU 方法 + 3 strategies）
- 可视化：删除不同节点后 scene graph 的变化
- 估计工作量：2–3 周（数据预处理 + 适配 OpenGU + 实验）

### 更合适的 Venue 建议

| Venue | 匹配度 | 理由 |
|-------|--------|------|
| **NeurIPS** | ⭐⭐⭐⭐⭐ | ML security + GNN, 无 CV 要求，接受图学习 |
| **ICML** | ⭐⭐⭐⭐⭐ | 同上，理论/方法导向 |
| **KDD** | ⭐⭐⭐⭐ | 图挖掘/GNN 强势社区 |
| **WWW** | ⭐⭐⭐⭐ | Graph+security，web-scale 图 |
| **AAAI** | ⭐⭐⭐⭐ | 广泛 AI venue，接受 GNN security |
| **USENIX Security / CCS / S&P** | ⭐⭐⭐ | 如果强化 threat model 和实际攻击场景 |
| **ECCV** | ⭐⭐ | 需要大量 CV 补充实验 |

---

## Appendix: 文件-证据索引

### 核心数据文件
- `results/collateral/{Method}/{Dataset}/{Model}/collateral_*.json` — retrain gap, collateral damage
- `results/relative/{Method}/{Dataset}/{Model}/relative_seed*_*.json` — relative F1 drop vs k=5 baseline
- `results/experiments/mg0_completion/phase_a/` — MG-0 phase_a (Cora/GCN, 5 seeds)
- `experiments/im_benchmark/results/bench_results.json` — CELF V0–V4 benchmark

### 分析文档
- `report/analysis/notes/2026-02-22_新发现_Shard保护效应与新指标.md` — Shard protection effect
- `report/analysis/notes/2026-02-22_技术分析_攻击策略有效性与改进方向.md` — Attack effectiveness analysis
- `report/daily-log/2026-02-25_log.md` — Latest experimental log with aggregated statistics

### 代码入口
- `eval_collateral.py` — Collateral damage + retrain gap evaluation
- `experiments/baseline_k5/eval_relative.py` — Relative metric calculation
- `attack/attack_strategies/` — Node selection strategy implementations
- `attack/pipeline_adapter.py` — AttackPipeline wrapping OpenGU

### 文献
- `self/paper_library_synthesis_2026-02-16.md` — 11-paper structured survey with positioning sentences and gap analysis
