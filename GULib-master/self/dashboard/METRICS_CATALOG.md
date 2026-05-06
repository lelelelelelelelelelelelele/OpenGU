# Metrics Catalog

> Last updated: 2026-05-06
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

### 2. MIA AUC ⚠️

- **核心量**：confidence-based ROC-AUC（max softmax）
- **实现**：`attack/attack_eval.py::evaluate_mia_auc()` (line 72)
- **存储**：JSON 每个 strategy 的 `mia_auc` 字段
- **覆盖**：
  - GIF: 0.585–0.640 ✅
  - GNNDelete: 0.409–0.543 ⚠（≈ 0.5，攻击信号弱）
  - **GraphEraser: 0.000 ❌ bug**
  - IDEA: 0.308–0.509 ⚠（攻击信号弱）
  - **MEGU: 0.000 ❌ bug**
- **bug 位置**：见 `EXPERIMENT_DASHBOARD.md §3.1`
- **paper 用法**：secondary metric，appendix。详见 thesis_transition_memo §3.5 framing

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

## "两个 Rel 指标"的关键区分

> 这是历史上最常被混淆的一点，记入此处避免再次踩坑

| 指标 | 公式 | 出处 | 含义 |
|------|------|------|------|
| **`Rel_F1_Drop_Mean`**（CSV 主列）| `baseline_f1_after(k=5 random) − attack_f1_after` | `experiments/baseline_k5/eval_relative.py:447` | "比只删 5 个随机节点的 baseline 多掉多少 F1" — 包含 k 增大本身的代价 |
| **FIG-4b effect**（heatmap 数字）| `mean_seeds(strategy_drop − random_drop)`（同一 k 配对）| `scripts/evaluation/generate_figures.py:185` | "在同样 k 下，比 random 多杀多少" — 减去 k 增大的混淆 |

两者对同一 cell 数值差异可达 9-10 percentage points。**论文 main result 用 FIG-4b effect**，因为它回答的是"informed selector 比 random 强多少"这个 referee 真正会问的问题。

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
