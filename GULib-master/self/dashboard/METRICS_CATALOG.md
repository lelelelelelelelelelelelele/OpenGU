# Metrics Catalog

> Last updated: 2026-05-07 (rev: ΔF_arch dual-baseline section added)
> Source of definitions: `self/plan_flow_v2_delta.md` §3
> 实测状态字段每次重跑后更新
> Field semantics: read `self/dashboard/METRIC_FIELD_SEMANTICS.md` before using any `*_before` value.

---

## v2 最小指标集（6 类，论文必须全部覆盖）

### 1. F1 Drop ⚠️

- **核心量（设计口径）**：`canonical_f1_before - f1_after`（绝对，0–1 范围）
- **派生**：`Rel_F1_Drop`（相对 k=5 random baseline，详见下方"两个 Rel 指标的差别"）
- **实现**：`attack/attack_eval.py::evaluate_f1_drop()` (line 42)
- **存储现状**：`attack.json` 的 `f1_before` 来自 method `poison_f1`，node task 下常为 `None`；不要把它当统一 baseline
- **Phase B 主用法**：用 `relative_f1_drop = baseline_f1_after(k=5 random) - attack_f1_after`，不依赖 `f1_before`
- **bug/口径状态**：字段名有历史歧义；详见 `METRIC_FIELD_SEMANTICS.md`

### 2. Update-Detection AUC ⚠️ (legacy field: `mia_auc`)

- **协议（posterior-shift deletion-membership audit）**：
  - **positives**：被请求 unlearn 的节点（deleted set）
  - **negatives**：held-out test 节点
  - **score**：unlearn 前 vs unlearn 后模型 posterior 输出的 L2 距离
  - **metric**：上述 score 的 ROC-AUC
- **scope note**：这**不是**标准的 Shokri/Olatunji shadow-model membership inference attack。它直接审计"一次 unlearning 更新是否暴露了被删除集合"，更贴合 deletion-selection / graph-unlearning threat model。详见 `self/paper_todo.md` §Decision。Paper 主术语：**update-detection AUC**；首次出现可写 "a posterior-shift deletion-membership audit"。
- **实现**：`attack/attack_eval.py::evaluate_mia_auc()` (line 72)；运行期 `attack.json::mia_auc` 由 `attack/pipeline_adapter.py` 从各方法的 `average_auc` 取值（GIF/GNNDelete/MEGU/IDEA 单模 forward；GraphEraser/GraphRevoker 走 shard ensemble），function 与字段名出于向后兼容**保留 legacy 命名**。
- **存储**：JSON 每个 strategy 的 `mia_auc` 字段（field name unchanged）
- **覆盖**（数值为历史 pre-Phase-B 数据，下次 Phase B 重跑后刷新）：
  - GIF: 0.585–0.640 ✅
  - GNNDelete: 0.409–0.543 ⚠（≈ 0.5，update-detection 信号弱）
  - **GraphEraser: 0.000 ❌ bug**（已修，见 §3.1）
  - IDEA: 0.308–0.509 ⚠（update-detection 信号弱）
  - **MEGU: 0.000 ❌ bug**（已修，见 §3.1）
- **bug 位置**：见 `EXPERIMENT_DASHBOARD.md §3.1`（历史标题保留 "MIA AUC = 0.000 bug"）
- **paper 用法**：secondary metric，appendix。详见 thesis_transition_memo §3.5 framing。**避免**写"GraphEraser 比单模方法更/不更隐私"这种跨 family 校准比较——本指标实现成本不同，跨 family 不可直接比较。

### 3. Selection Time ✅

- **核心量**：策略选点耗时（秒）
- **实现**：`attack/attack_manager.py` 计时 wrapper
- **存储**：JSON 每个 strategy 的 `selection_time`
- **覆盖**：完整
- **bug 状态**：无
- **注意**：im / im_v4 用旧版纯 Python BFS vs 新版 numba，时间不可比；report 时只用 v4 数据

### 4. Approximation Gap (Retrain Gap) ✅

- **核心量**：`Perf_retrain - Perf_unlearn`（近似遗忘的额外损失）
- **实现**：`attack/attack_eval.py::evaluate_retrain_gap()` (line 95)
- **存储**：`results/collateral/{Method}/{Dataset}/{Model}/collateral_*.json` 内 `gap` / `gap_pct` 字段；CSV `Retrain_Gap_Abs_Mean`
- **覆盖**：mg0/mg1/mg2/mg3 的 cell 完整；arxiv 待 Phase B
- **bug 状态**：无
- **三模型框架**：(model_before, model_unlearned, model_retrained) 同时持有，定义 Drop_retrain + Gap = Total
- **before 口径注意**：`perf_before` 是当前 method 的 `train_only` before；对 GraphEraser/GraphRevoker 可能是 SISA/shard before，不一定是 vanilla `canonical_f1_before`

### 5. Collateral Damage ✅

- **核心量**：retain set 上 model_unlearned vs model_retrained 的预测差异
- **子指标**：
  - `mean_pred_shift` — 保留节点 L_inf 偏移均值
  - `max_pred_shift` — 保留节点最大偏移
  - `fraction_flipped` — unlearn 与 retrain 类别不一致比例
- **实现**：`attack/attack_eval.py::evaluate_collateral_damage()` (line 132)
- **存储**：与 #4 同 JSON
- **覆盖**：mg0/mg1/mg2/mg3 cell 完整
- **bug 状态**：无
- **关键设计**：对比 unlearn vs retrain（不是 before vs after），隔离近似误差

### 6. Gap 统计显著性 ✅ 部分

- **核心量**：多 seed Gap 的 t-test p-value + 95% CI
- **实现**：`attack/attack_eval.py::compute_gap_statistics()`
- **存储**：CSV `P_Value`, `Rel_F1_Drop_Std`；CI 字段需检查是否生成
- **覆盖**：N≥5 cell 有 p-value
- **当前问题**：GNNDelete 整行 p > 0.05（详见 EXPERIMENT_DASHBOARD §3.2）
- **维护**：每次 N_seeds 变化都要重算

---

## 三种 baseline / 两条独立分解（v2.1，2026-05-07 起 paper 实采）

> 历史上最常被混淆的一点。Phase B 起 paper 同时报两条**互不重叠**的分解，分别回答不同问题。

### Baseline 选择表

| Baseline | 公式（drop = $F_1^{\text{before}}{-}F_1^{\text{after}}$） | 出处 / 字段 | 含义 |
|---|---|---|---|
| **k=5 noise floor** | $F_1^{\text{before}} - F_1^{\text{k=5 random}}$ | `results/baseline/k5_random/{Method}/{ds}/{bk}/baseline_averaged_k5.json::f1_after` | 删 5 个节点（≈ 0.18% on Cora）下方法的 intrinsic 架构成本；几乎无 volume 效应 |
| **r=budget random** | $F_1^{\text{before}} - F_1^{\text{r·N random}}$ | `_phase_b_aggregate.csv::f1_drop`（strategy='random' 行）| 攻击 budget 下随机基线；包含 architecture + volume |
| **paired vs random** | $\text{drop}_{\text{strat}} - \text{drop}_{\text{r=budget random}}$ | `(strategy 行) − (random 行)` 同 seed 配对，inline pivot | "informed selector 比 random 多杀多少" — 减去 k 增大的混淆，paired-$t$ 主用 |

### 两条互不重叠的分解（two complementary 2-term decompositions）

```
分解 A（攻击是否超出 random）：
    drop_strat = drop_random_budget + ΔF^attack_paired
                 ────────────────────  ────────────────
                 architectural@budget   attack-vs-random@budget   ← paired-t 用这个
```

```
分解 B（架构 vs volume）：
    drop_random_budget = drop_at_k=5 + ΔF_volume
                         ─────────────  ────────────
                         intrinsic       budget contribution      ← Shard Protection / collapse-mode 故事用这个
```

→ **总不是"三项分解"**。每条独立的 2-term decomposition 都成立；master scorecard `Table~\ref{tab:benchmark}` 同时用上 k=5（Noise 列）和 r=budget（ΔF_arch 列），分别支撑分解 B 的两端。

### 三 family 在分解 B 下的特征模式（实测 Cora，r=0.05）

| Family | $k=5$ noise | $r=5\%$ random | 模式 |
|---|---|---|---|
| Learning（GNNDelete）| ${\sim}0$ | $+10\%{-}13\%$ | **collapse 全部来自 volume**，架构本身没成本 |
| Partition（GraphEraser）| $-10\%{-}{-}12\%$ | $-6\%{-}{-}9\%$ | **Shard Protection 在 k=5 就启动**，volume 反而稍微攻坚 |
| IF / Mild Learning（GIF/IDEA/MEGU）| ${\sim}0$ | $+2\%{-}5\%$ | 架构和 volume 都小，attack 信号在 paired ΔF^attack 列 |

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

### 8.3 [计划实现，Phase A.5] Hop-distance Collateral Decay

- **核心量**：按距离 unlearn 节点的 hop 分组，分别报告 fraction_flipped
- **公式**：
  ```
  对 hop ∈ {1, 2, 3, >3}:
      nodes_at_hop = BFS(unlearn_nodes, hop) ∩ retain_mask
      collateral_at_hop = fraction_flipped(model_unlearned, model_retrained, nodes_at_hop)
  ```
- **实现位置**：扩展 `evaluate_collateral_damage()`，~30 行 PyG `k_hop_subgraph`
- **paper 价值**：高（GNN-specific，文献空白，可视化冲击，机制锚）
- **耦合性**：必须在训练 pipeline 内嵌入计算（model 不持久化），但已有 collateral evaluation 调用点已在 unlearn + retrain 同时持有时，扩展成本 0
- **0 训练成本 piggyback**：所有 Phase B 重跑直接收集
- **预期可视化**：衰减曲线图，按 family 分线，与 GCN 层数（receptive field = L-hop）对照

### 8.4 [机会主义] Budget Efficiency

- **核心量**：`F1_drop / k`（边际损害） + `MinBudget(τ)`（达到 τ% F1 drop 所需最小 k）
- **判断**：ratio_sensitivity 实验已有数据，几乎免费
- **决定**：appendix 单图，不主推

### 8.5 [跳过] Stealthiness

- **判断**：本 paper 主线不涉及 detection；out of scope

---

## 维护规则

- 实测覆盖每次重跑后更新 §1-6 的"覆盖"字段
- 新增 bug → §对应指标的 bug 状态字段 + EXPERIMENT_DASHBOARD §3
- 修复 bug → 把状态从 ❌/⚠ 改为 ✅，同时在 VALIDATION_LOG 新增条目
- v3 候选若决定实现 → 移到 v2 列表 + 同步 plan_flow_v2_delta.md
