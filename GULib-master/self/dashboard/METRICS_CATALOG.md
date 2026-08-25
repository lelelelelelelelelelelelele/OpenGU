# Metrics Catalog

> Last updated: 2026-07-16 (rev: explicit small/large dataset policy for optional update-detection AUC)
> Source of definitions: `self/plan_flow_v2_delta.md` §3 (formal) + `report/paper/overleaf/sec/3_method.tex` (paper-canonical)
> 实测状态字段每次重跑后更新
> Field semantics: read `self/dashboard/METRIC_FIELD_SEMANTICS.md` before using any `*_before` value.

> **2026-05-07 paper rename + decomposition update**: the symbol formerly written `\Delta F_{\mathrm{arch}}` was renamed to `\Delta F_{\mathrm{noise}}` (= drop at k=5). The paper now uses the three-term decomposition `drop_total = ΔF_noise + ΔF_volume(r) + ΔF_attack(S)`, where `ΔF_volume(r)=ΔF_rand(r)-ΔF_noise`. See §"三项分解 / 三种 baseline" below.

---

## v2 最小指标集（论文 abstract 承诺的 6 个 + 2 secondary）

### 1. F1-drop family — four named quantities, three decomposition terms ⭐

The paper reports the F1-drop signal through four named quantities, each derived from the same primitive `drop = F1_before − F1_after`. `ΔF_rand(r)` is the budget-matched random baseline used to derive the two decomposition terms `ΔF_volume` and `ΔF_attack`:

```
drop_total(S) = ΔF_noise + ΔF_volume(r) + ΔF_attack(S)
```

| Quantity | 公式 | 数据源 | Paper 出现处 |
|---|---|---|---|
| **ΔF_noise** | $F_1^{\text{before}} - F_1^{\text{k=5 random}}$ | `results/baseline/k5_random/{Method}/cora/{Bk}/baseline_averaged_k5.json::f1_after` (5 seeds avg) | Master scorecard col 1; FIG-2 bar height; §3 method def; §5.4 prose; abstract `k=5 noise floor` |
| **ΔF_rand(r)** | $F_1^{\text{before}} - F_1^{\text{r·N random}}$ | `_phase_b_aggregate.csv::f1_drop` (`strategy=='random'` row) | §3 method def; §5.4 散文 (e.g.\ GNNDelete +10-13% at r=5%) |
| **ΔF_volume(r)** | $\Delta F_{\text{rand}}(r)-\Delta F_{\text{noise}}$ | derived from k=5 baseline + random@r row | §3 method def; §5.4 Shard/GNNDelete volume interpretation |
| **ΔF_attack (paired)** | $\mathrm{drop}_{\text{strat}} - \mathrm{drop}_{\text{random@r}}$ same-seed | inline pivot: strategy-row − random-row in CSV | Master scorecard 5 attack columns; FIG-3 / FIG-4b axes; FIG-5 y-axis; abstract effect numbers |

- **实现**：`attack/attack_eval.py::evaluate_f1_drop()` (line 42) for absolute drop; paired ΔF_attack and ΔF_rand both computed inline by `scripts/plot_neurips_figures.py` and the master-scorecard-generation pivot (no standalone Python class for paired)
- **存储现状**：raw `f1_after` per (method, strategy, seed) lives in `attack.json::results.<strategy>.f1_after`. `f1_before` in attack.json is method `poison_f1` and is `None` on node tasks — **don't use for baseline**; reconstruct from `f1_after + f1_drop` of the random row when needed.
- **Decomposition tightness**: `drop_strat = ΔF_noise + ΔF_volume(r) + ΔF_attack` exactly by construction, with `ΔF_volume(r)=ΔF_rand(r)-ΔF_noise` and `ΔF_attack=drop_strat-ΔF_rand(r)`.
- **Bug/口径状态**：field-name history in `METRIC_FIELD_SEMANTICS.md`; the 2026-05-07 paper rename `ΔF_arch → ΔF_noise` does NOT touch CSV fields or code.

### 2. Update-Detection AUC ⚠️ (legacy field: `mia_auc`)

- **协议（posterior-shift deletion-membership audit）**：
  - **positives**：被请求 unlearn 的节点（deleted set）
  - **negatives**：held-out test 节点
  - **score**：unlearn 前 vs unlearn 后模型 posterior 输出的 L2 距离
  - **metric**：上述 score 的 ROC-AUC
- **scope note**：这**不是**标准的 Shokri/Olatunji shadow-model membership inference attack。它直接审计"一次 unlearning 更新是否暴露了被删除集合"，更贴合 deletion-selection / graph-unlearning threat model。详见 `self/paper_todo.md` §Decision。Paper 主术语：**update-detection AUC**；首次出现可写 "a posterior-shift deletion-membership audit"。
- **实现**：`attack/attack_eval.py::evaluate_mia_auc()` (line 72)；运行期 `attack.json::mia_auc` 由 `attack/pipeline_adapter.py` 从各方法的 `average_auc` 取值（GIF/GNNDelete/MEGU/IDEA 单模 forward；GraphEraser/GraphRevoker 走 shard ensemble），function 与字段名出于向后兼容**保留 legacy 命名**。统一开关为 `defaults.run_update_detection_auc`。
- **数据集策略（2026-07-16）**：这是 secondary metric。Cora/Citeseer 等小图 YAML 显式 `true`；ogbn-arxiv 等大图 YAML 显式 `false`。策略由 YAML 指定，不按 dataset 名称硬编码；无该字段的旧配置默认 `true`。
- **存储**：JSON 每个 strategy 保留 `mia_auc` 字段。启用时为有限数；关闭时必须为 `null`，同时 `_meta.json::metric_policy.update_detection_auc.status = disabled_by_config`。`null` 表示“按配置未运行”，不是 0，也不是实验失败。
- **完成门**：`scripts/gate_runs.py` 仅在开关开启时要求 `0.001 < mia_auc < 0.999`；关闭时要求 `null`。因此大数据集可以在没有该 secondary metric 的情况下形成完整 cell。
- **Cache 边界**：开关不进入 Score/Selection identity；当前完整 run fingerprint 包含它，防止开/关结果目录混用。V2.3 接入后 AUC 属于可选、versioned EvaluationArtifact，不应迫使上游 Score/Selection/Prediction 重算。
- **覆盖**（Phase B post-fix 实测，Cora 主矩阵，5 seeds × 6 strategies 平均）：
  - GraphEraser: GCN 0.72 / GAT 0.55 ✅
  - GraphRevoker: GCN 0.81 / GAT 0.79 ✅（最高 update-detection 信号）
  - GIF: GCN 0.65 / GAT 0.40 ✅
  - IDEA: GCN 0.51 / GAT 0.44 ✅（near-random）
  - GNNDelete: GCN 0.67 / GAT 0.62 ✅
  - MEGU: GCN 0.50 / GAT 0.57 ✅（near-random）
- **paper 用法**：master scorecard "AUC" 列；§5.5 update-detection 子节 + tab:mia 表已被 master scorecard 吸收；secondary metric。**避免**写"GraphEraser 比单模方法更/不更隐私"这种跨 family 校准比较——本指标实现成本不同，跨 family 不可直接比较。
- **bug 历史**：见 `EXPERIMENT_DASHBOARD.md §3.1`（历史标题保留 "MIA AUC = 0.000 bug"，已修）。

### 3. Selection Time ✅ (utility / not paper-promised, kept for tracking)

- **核心量**：策略选点耗时（秒）
- **实现**：`attack/attack_manager.py` 计时 wrapper
- **存储**：CSV `selection_time` 字段
- **覆盖**：完整
- **bug 状态**：无
- **注意**：im / im_v4 用旧版纯 Python BFS vs 新版 numba，时间不可比；report 时只用 v4 数据
- **paper 用法**：未在主表 / 主图出现；可作 §A 的"compute resources"附注（IM ~3 min/cell, TracIn ~85 min/cell on arxiv）

### 4. Approximation Gap (Retrain Gap) ✅

- **核心量**：`perf_retrain − perf_unlearn`（近似遗忘相对精确 retrain 的额外损失；正值 = unlearn 后 F1 比 retrain 低，表示 over-forgetting / approximation drift）
- **实现**：`attack/attack_eval.py::evaluate_retrain_gap()` (line 95)
- **存储**：Phase B canonical 路径 `results/runs/{cell}/{method}_{strategy}/seed{N}/collateral.json::results[0].gap`；旧路径 `results/collateral/...` 已 untrack（2026-05-05）
- **覆盖**（Cora post-Phase-B 实测，attack strategies 平均）：
  - GraphEraser: GCN $+1.8\%$ / GAT $+1.8\%$ ✅
  - GraphRevoker: GCN $-0.4\%$ / GAT $-1.2\%$ ✅
  - GIF$^{\ddagger}$: GCN $-0.4\%$ / GAT $-0.6\%$ — IF-family pre-fix lower bound
  - IDEA$^{\ddagger}$: GCN $-0.4\%$ / GAT $-0.5\%$ — 同
  - GNNDelete: GCN $+11.0\%$ / GAT $+11.8\%$ ✅ — **唯一 outlier**
  - MEGU: GCN $-0.0\%$ / GAT $+0.2\%$ ✅
- **证据状态**：GIF/IDEA 的现有 collateral 仍是 IF-family pre-fix（`perf_unlearn` ≈ `perf_before`，所以旧 `gap` 实际是 `perf_retrain − perf_before`，不能当作修复后 gap）。代码已修复，受影响 evidence 等待重跑；Master scorecard 继续用 `^{\ddagger}` 标注。
- **paper 用法**：master scorecard "Gap" 列；§5.4 GNNDelete approx-error 论据（"order of magnitude larger than every other method"）
- **三模型框架**：(model_before, model_unlearned, model_retrained) 同时持有，定义 `drop_retrain + gap = drop_total`
- **before 口径注意**：`perf_before` 是当前 method 的 `train_only` before；对 GraphEraser/GraphRevoker 可能是 SISA/shard before，不一定是 vanilla `canonical_f1_before`

### 5. Prediction Shift ✅

- **核心量**：retain set 上 model_unlearned vs model_retrained 的预测差异
- **子指标**：
  - `mean_pred_shift` — 保留节点 posterior $\ell_2$ 偏移均值
  - `max_pred_shift` — 保留节点最大偏移
  - `fraction_flipped` — unlearn 与 retrain 类别不一致比例
- **实现**：`attack/attack_eval.py::evaluate_collateral_damage()` (line 132)
- **存储**：CSV `mean_pred_shift` / `max_pred_shift` / `fraction_flipped`；同时存于 `collateral.json::results[0]`
- **覆盖**：Cora 12 cell 完整；GIF/IDEA bug-affected (lower bound)
- **paper 用法**：abstract 承诺 6 metric 之一；**主表 / 主图当前未单独可视化**（hop-decay #6 是其按距离切片的版本，更有 GNN-specific 卖点）；§A appendix 散文写一句平均偏移幅度
- **关键设计**：对比 unlearn vs retrain（不是 before vs after），隔离近似误差

### 6. Hop-distance Collateral Decay ✅ (formerly v3 #8.3, promoted 2026-05-04)

- **核心量**：按距离 unlearn 节点的 BFS-hop 分组，分别报告 retain set 上的 fraction_flipped
- **公式**：
  ```
  对 hop ∈ {1, 2, 3, >3}:
      nodes_at_hop = BFS(unlearn_nodes, hop) ∩ retain_mask
      flip_rate_at_hop = fraction_flipped(model_unlearned, model_retrained, nodes_at_hop)
  ```
- **实现**：`attack/attack_eval.py::evaluate_collateral_damage()`，4 桶 hop 用 PyG `k_hop_subgraph`；扩展 commit `evaluate_hop_decay` (Phase A.5)
- **存储**：CSV `hop_1_flip_rate` / `hop_1_count` / `hop_2_flip_rate` / `hop_2_count` / `hop_3_*` / `hop_gt3_*`；同时存于 `collateral.json::results[0].hop_decay`
- **覆盖**（Cora/GCN, attack strategies 平均，h=1 flip rate）：
  - GIF$^{\ddagger}$: 2.9% (RF-localized)
  - IDEA$^{\ddagger}$: 2.9%（与 GIF bit-identical：IF-family pre-fix bug）
  - GNNDelete: 35.5% (扩散，h=2 18%, h=3 4.5%)
  - MEGU: 2.7% (RF-localized)
  - GraphEraser: 29.0% (各桶都高 — shard rebalance)
  - GraphRevoker: 29.9%（同）
- **bug 状态**：GIF/IDEA `hop_*_flip_rate` bug-affected（IF-family pre-fix `model_unlearned` ≈ `model_before`，flip 计算成"原 vs retrain"而非"unlearn vs retrain"）。Master scorecard 早期版有 Hop₁ 列，**当前已去掉**避免误导
- **paper 用法**：abstract 承诺 6 metric 之一；§A.4 appendix 散文（GIF/IDEA 集中 1-hop / GNNDelete 扩散 / Partition 各桶都高）；当前**未单独画 figure**（FIG-A.X candidate）
- **关键设计**：GNN-specific locality metric — 衰减形状本身就是 receptive-field signature 的证据；与方法的 mask network / Hessian conditioning / shard 等机制有强解释力
- **新生成 cell 必带**：`evaluate_collateral_damage()` 已是 Phase B canonical 调用，不需手动开启

### 7. Selection-degree Alignment ✅ (pivot 引入 2026-05-07)

- **核心量**：每个 (method, strategy, backbone, seed) tuple 上，**被选中节点的平均 degree** $\bar{d}$ 与同 tuple 的 paired ΔF^attack 的相关性
- **公式**：
  ```
  对每个 attack tuple t = (method, strategy, backbone, seed):
      d̄_t = mean(degree(v) for v in selected_nodes[t])
      Δ_t = paired_F1_attack[t]
  Pearson r = corr(d̄, Δ) over n=300 non-random tuples
  ```
- **实现**：inline pivot in `scripts/plot_neurips_figures.py::collect_alignment_tuples()` 扫 `results/runs/4090/cora_*_r0.05/*/seed*/attack.json` 读 `selected_nodes`，跟 CSV 配对算
- **存储**：未单独存 CSV；在 figure 生成时实时 inline 算
- **覆盖**（Cora 12 method×backbone cells, 5 strategies × 5 seeds = n=300 non-random tuples）：
  - **全局相关性**：Pearson $r{=}0.239$ ($p{=}2.8\times 10^{-5}$), Spearman $\rho{=}0.341$ ($p{=}1.4\times 10^{-9}$)
  - **strategy mean** $\bar{d}$ → paired effect 单调：Degree 18.69/+2.04% > PageRank 18.49/+1.54% > IM 13.09/+0.88% > Hybrid 6.47/+0.42% > **TracIn 3.94/+0.02% ≈ Random 3.88**（graph mean 3.90）
  - **cell-level**：11/12 cells 正相关；4 cells $r{>}0.9, p{<}.05$（GIF/GCN 0.97 / GNNDelete/GCN 0.99 / MEGU/GCN 0.94 / IDEA/GAT 0.97）
  - **唯一负相关 cell**：GraphRevoker$\times$GAT $r{=}-0.78$，恰好是唯一 TracIn-significant paired cell ($+3.58\%, p{=}.018$)；alignment 假设的内部反例
- **paper 用法**：§5.2 "Structural Alignment Predicts Attack Success" 子节；FIG-5_Alignment.pdf 双 panel；G "Objective Misalignment Hypothesis" 段落 + future work 锚点
- **status**：post-hoc analysis；不影响主决策路径，但是把"为什么 TracIn 不如 Degree"这个 puzzle 关上了

### 8. Paired t-test Significance ✅

- **核心量**：每个 (method, strategy) cell 上对 5-seed paired diff $(\mathrm{drop}_{\mathrm{strat}} - \mathrm{drop}_{\mathrm{rand}})$ 做 one-sided t-test，$H_1: \mu > 0$
- **公式**：`scipy.stats.ttest_rel(strat_drop, rand_drop)`，one-sided $p$ = $p_{\text{two-sided}}/2$ if $t > 0$ else $1 - p_{\text{two-sided}}/2$
- **实现**：inline in `scripts/plot_neurips_figures.py::fig4_heatmaps()` and master-scorecard pivot
- **存储**：不存 CSV；每次报表时 inline 算
- **paper 用法**：master scorecard 形状标记 ▲ ($p{<}.001$) / ◆ ($p{<}.01$) / $\bullet$ ($p{<}.05$)；FIG-4a heatmap 显示 $-\log_{10}(p)$
- **N=5 警告**：power 有限（CI ~ ±10% on noisy cells like GNNDelete IM），所以"未显著"不等于"无 effect"；master scorecard 里加粗 best attack 单元格、即使 sig 缺失也保留 mean 值
- **替换历史**：原 §6 "Gap 统计显著性"（对 retrain gap 做 t-test）已弃用，paper paired-t 全部用在 ΔF_attack 而非 gap

---

## 三项分解 / 三种 baseline（v2.2，2026-05-07 起 paper 实采）

> 历史上最常被混淆的一点。当前 paper 把同一条 F1 response curve 拆成 `noise + volume + attack` 三项；`ΔF_rand(r)` 是中间基线，不是单独的攻击效果。
> 2026-05-07 起所有 baseline 的 paper-canonical 名是 ΔF_noise / ΔF_volume / ΔF_attack（旧版 ΔF_arch / Rel_F1_Drop 退役）。

### Baseline 选择表

| Baseline | 名字 | 公式 | 出处 / 字段 | 含义 |
|---|---|---|---|---|
| k=5 noise floor | $\Delta F_{\mathrm{noise}}$ | $F_1^{\text{before}} - F_1^{\text{k=5 random}}$ | `results/baseline/k5_random/{Method}/{ds}/{bk}/baseline_averaged_k5.json::f1_after` | 删 5 个节点（≈ 0.18% on Cora）下方法的 intrinsic 架构成本；几乎无 volume 效应 |
| r=budget random | $\Delta F_{\mathrm{rand}}(r)$ | $F_1^{\text{before}} - F_1^{\text{r·N random}}$ | `_phase_b_aggregate.csv::f1_drop`（`strategy=='random'` 行）| 攻击 budget 下随机基线；包含 architecture + volume |
| paired vs random | $\Delta F^{\mathrm{attack}}(S)$ | $\mathrm{drop}_{\mathrm{strat}} - \mathrm{drop}_{\mathrm{random@r}}$ | `(strategy 行) − (random 行)` 同 seed 配对，inline pivot | "informed selector 比 random 多杀多少" — paired-$t$ 主用 |

### 三项分解

```
drop_strat = ΔF_noise + ΔF_volume(r) + ΔF_attack
             ─────────   ─────────────   ───────────
             k=5 floor    random budget   selector excess vs random@r
```

Only `ΔF_attack` is attack-specific. `ΔF_noise` and `ΔF_volume` are random-deletion diagnostics that separate intrinsic near-zero-volume response from budget-induced random deletion. Master scorecard `Table~\ref{tab:benchmark}` 显式列 ΔF_noise（一列）+ ΔF_attack（5 strategy 列）；ΔF_volume 在 §5.4 散文解释中使用。

### 三 family 在三项分解下的特征模式（实测 Cora，r=0.05）

| Family | $\Delta F_{\mathrm{noise}}$ ($k{=}5$) | $\Delta F_{\mathrm{rand}}(r{=}5\%)$ | 模式 |
|---|---|---|---|
| Partition（GraphEraser）| $-10\%$ to $-12\%$ | $-6\%$ to $-9\%$ | **Shard Protection 在 k=5 就启动**，volume 反而稍微攻坚 |
| Partition（GraphRevoker）| **$-19\%$ / $-17\%$** | $-14\%$ / $-15\%$ | 同上但更夸张 |
| Learning（GNNDelete）| ${\sim}0$ | $+10\%$ to $+13\%$ | **collapse 全部来自 volume**，架构本身没成本 |
| IF / Mild Learning（GIF/IDEA/MEGU）| $-2\%$ to $+2\%$ | $+2\%$ to $+5\%$ | 架构和 volume 都小，attack 信号在 paired $\Delta F^{\mathrm{attack}}$ 列 |

### v2.1 之前的"两个 Rel 指标"（保留 audit trail）

下面这两个早期定义已经被上面的三 baseline 设计取代。代码字段保留向后兼容：

| 历史指标 | 公式 | 出处 | 当前状态 |
|---|---|---|---|
| `Rel_F1_Drop_Mean`（CSV 主列）| `baseline_f1_after(k=5 random) − attack_f1_after` | `experiments/baseline_k5/eval_relative.py:447` | **Phase B paper 不再用**——它把 architecture+volume+attack 全混在一起 |
| FIG-4b effect | `mean_seeds(strategy_drop − random_drop)` | `scripts/evaluation/generate_figures.py:185` | 等价于"paired vs random"（上表第三行）；**Phase B 仍用**，只是表头改 paired ΔF^attack |

---

## v3 候选指标（仅记录，部分计划实现）

### 8.1 [跳过] Forgotten Node Accuracy

- **意义**：defender 视角的 efficacy 指标
- **判断**：对 utility-degradation red-team paper 价值低（详见 2026-05-03 讨论）
- **决定**：appendix 也不报；不实现

### 8.3 [PROMOTED to v2 §6 (2026-05-04)] Hop-distance Collateral Decay

已实现并写入 Phase B canonical pipeline，详见 v2 §6。这条留作 audit trail。

### 8.4 [机会主义] Budget Efficiency

- **核心量**：`F1_drop / k`（边际损害） + `MinBudget(τ)`（达到 τ% F1 drop 所需最小 k）
- **判断**：ratio_sensitivity 实验已有数据，几乎免费
- **决定**：appendix 单图，不主推

### 8.5 [跳过] Stealthiness

- **判断**：本 paper 主线不涉及 detection；out of scope

---

## Paper 视觉化映射（master scorecard + 6 figure 各自用哪些 metric）

| Visual | 用到的 metric | 数据 cell | 主张 |
|---|---|---|---|
| Master scorecard `tab:benchmark` | #1 ΔF_noise + #1 ΔF_attack (5 cols) + #4 Gap + #2 AUC + #8 paired-t (▲◆●) + Verdict | Cora GCN+GAT 全 12 cell | 全景 |
| FIG-1_Generalization | #1 ΔF_attack(IM) × ΔF_attack(TracIn) | Cora GCN + GAT 双 panel | fingerprint 跨 backbone 一致 |
| FIG-2_Scaling | #1 ΔF_noise (k=5) | Cora GCN+GAT 并列 bar | partition 在 k=5 已全负 → architectural Shard Protection |
| FIG-3_Spectrum | #1 ΔF_attack(IM) × ΔF_attack(TracIn) + 1σ ellipse | Cora GCN | 主 fingerprint 图 |
| FIG-4a_Significance | #8 paired-t $-\log_{10}(p)$ heatmap | Cora GCN, 6×5 | 显著 cell 分布 |
| FIG-4b_Effect | #1 ΔF_attack mean heatmap | Cora GCN, 6×5 | effect 大小 |
| FIG-5_Alignment | #7 selection-degree alignment | Cora GCN+GAT, n=300 tuples | mean degree 单调预测 effect |

→ #3 Selection Time, #5 Prediction Shift, #6 Hop-decay：未在主表/主图单独可视化，仅 §A appendix 散文。

---

## 维护规则

- 实测覆盖每次重跑后更新 §1-6 的"覆盖"字段
- 新增 bug → §对应指标的 bug 状态字段 + EXPERIMENT_DASHBOARD §3
- 修复 bug → 把状态从 ❌/⚠ 改为 ✅，同时在 VALIDATION_LOG 新增条目
- v3 候选若决定实现 → 移到 v2 列表 + 同步 plan_flow_v2_delta.md
