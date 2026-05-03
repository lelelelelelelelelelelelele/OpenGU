# Validation Log

> Last updated: 2026-05-03
> **Append-only**——禁止删改历史条目。错的条目不删，新条目标 SUPERSEDES + 解释
> 用途：固化今天讨论 / 实测验证 / sanity check 的实证证据，避免 4 天 deadline 期间反复发现同一件事

---

## 2026-05-03 Session

### V-2026-05-03-01: FIG-4b 数据源混合

**Finding**：FIG-4b heatmap 的 5 行**不来自同一个 (dataset, model)**。GIF/GNNDelete/GraphEraser 取自 mg0_completion (cora/GCN)，IDEA/MEGU 取自 mg3_gat (cora/GAT)。

**Source**：`scripts/evaluation/generate_figures.py:33-37` (FIG4_JSON_PATTERNS dict)

**Implication**：当前 FIG-4b 是不严谨混合图。Phase B 重跑后必须把 IDEA/MEGU 补到 cora/GCN，或在论文中明确标注配置不同。

---

### V-2026-05-03-02: GNNDelete 5-seed paired effect 全行不显著

**Setting**：cora/GCN/r=0.05/N=5，paired effect = strategy_drop − random_drop（同 seed 内配对，FIG-4b 口径）

**Result**：

| Cell | mean | std | 95% CI | p (>0) |
|------|------|-----|--------|--------|
| GNNDelete × TracIn | +3.84 | 5.05 | [-0.59, +8.26] | 0.082 |
| GNNDelete × IM_v4 | +6.75 | 8.56 | [-0.75, +14.25] | 0.076 |
| GNNDelete × Hybrid_v4 | +3.36 | 7.58 | [-3.29, +10.00] | 0.189 |

**Implication**：N=5 不足以支撑"GNNDelete 显著 vulnerable"主张。+6.8 头条数字 95% CI **跨过 0**。

**Verification command**：
```bash
H:/conda_package/envs/gnn/python.exe -c "
import json, glob, numpy as np
from scipy.stats import ttest_rel
files = sorted(glob.glob('results/experiments/mg0_completion/phase_a/*/GNNDelete_cora_GCN_r0.05_s*.json'))
diffs, sv, rv = [], [], []
for f in files:
    d = json.load(open(f))
    r = d.get('results', {})
    diffs.append((r['im_v4']['f1_drop'] - r['random']['f1_drop'])*100)
    sv.append(r['im_v4']['f1_drop']); rv.append(r['random']['f1_drop'])
print('mean=%.2f, std=%.2f, p=%.4f' % (np.mean(diffs), np.std(diffs, ddof=1), ttest_rel(sv, rv, alternative='greater').pvalue))
"
```

---

### V-2026-05-03-03: IM_v4 跨 seed Jaccard = 0.13

**Setting**：cora/GCN/r=0.05/N=5，比较 5 个 seed 选出的 top-135 节点的 pairwise Jaccard

**Result**：

| Strategy | mean Jaccard | 解读 |
|----------|:-:|------|
| random | 0.023 | sanity ✓ |
| **im_v4** | **0.129** | **MC 抖，节点 87% 跨 seed 不重叠** |
| tracin | 0.415 | model-coupled drift |
| hybrid_v4 (GNNDelete) | 0.646 | 较稳 |
| hybrid_v4 (GIF) | 0.319 | 高漂移 |
| hybrid_v4 (GraphEraser) | 0.295 | 高漂移 |
| pagerank / degree | 1.000 | 完美稳定 |

**Implication**：IM_v4 的 +6.8 effect 部分来自 "MC 偶然踩中 lucky set"。Phase A.4 通过 fixed MC seed 解耦，预期 Jaccard → 1.0。

**注意**：IM_v4 Jaccard 不依赖 family（5 个 family 都是 0.129），因为 IM 选点只用图结构 + MC，不用 model。TracIn (0.415 across all families) 同理——它依赖 pre-unlearn 模型，pre-unlearn model 在不同 GU 方法下相同。

---

### V-2026-05-03-04: GNNDelete × IM_v4 单 seed 复盘

**Setting**：cora/GCN/r=0.05，5 seed 的逐个 IM_v4 vs random 对比

| seed | random f1_drop% | im_v4 f1_drop% | IM − random |
|------|:-:|:-:|:-:|
| 722 | 7.01 | 6.09 | **−0.92**（random 反而更狠）|
| 1337 | 12.92 | 19.74 | +6.82 |
| 2024 | 7.01 | 27.12 | **+20.11**（顶起均值）|
| 42 | 8.67 | 16.97 | +8.30 |
| 212 | 11.62 | 11.07 | **−0.55**（random 反而更狠）|

**Implication**：5 个 seed 里有 2 个 IM 输给 random。+6.8 几乎全部由 seed 2024 的 +20 顶起。

---

### V-2026-05-03-05: MIA AUC = 0.000 是代码 bug 不是机制现象

**Finding**：MEGU / IDEA / GraphEraser 在所有 seed × strategy 上 mia_auc = 0.000（不是 NaN，是字面 0.0）

**Root cause**：三处 MIA 调用被注释掉，导致 `self.average_auc = np.zeros(num_runs)` 永远停在初始值

| Family | 注释位置 |
|--------|---------|
| MEGU | `unlearning/unlearning_methods/MEGU/megu.py:140` |
| IDEA | `unlearning/unlearning_methods/IDEA/idea.py:107`（含 line 88-114 attack 块整体注释）|
| GraphEraser（影响所有 shard-based）| `pipeline/Shard_based_pipeline.py:177` |

**Verification command**：
```bash
grep -rn "average_auc\|mia_attack" unlearning/unlearning_methods/{MEGU,IDEA,GraphEraser}/ pipeline/Shard_based_pipeline.py | head
```

**与历史 GUIDE 0.000 bug 同模式**：调用注释 + 初始值 0 + 输出未做 sanity check。

**Fix plan**：Phase A.1–A.3 取消注释 + sanity test 验证输出 ∈ [0, 1] 且非 NaN。

---

### V-2026-05-03-06: GIF × TracIn 是当前最稳的 cell（基线锚点）

**Setting**：cora/GCN/r=0.05/N=5

**Result**：mean = +4.17, std = 0.76, 95% CI = [+3.51, +4.83], p = 0.0001 ✅

**Implication**：可作为"5 seed + paired diff 在干净配置下的 std 上界"参考。其他 cell 若 std ≫ 0.76，要么是 selector 抖（如 IM_v4 0.13 Jaccard 那一档），要么是 surface 真不平滑（如 GNNDelete）。

---

### V-2026-05-03-07: B1 vs B2 决策

**Decision**：选 B1（fix selector-internal RNG，保留 selector-model 耦合）+ 1 个 B2 sanity 锚点

**B1 操作**：IM_v4 fixed MC seed → Jaccard = 1.0；TracIn 保持 model-aware（设计如此）

**B2 锚点**：单 cell 实验 GNNDelete × TracIn × cora/GCN × r=0.05，用 reference model M_ref 的 TracIn 选点固定后应用到 5 个 GU_seed → 测 effect 分布对比 B1

**Rationale**：完整 B2 需重跑 TracIn 全部 cell，为了保留 TracIn 设计语义（model-aware），不值。但纯文字讨论 referee 不接受，单点数据足够防御。

**Placement**：B2 数据 + B1/B2 选择讨论放 paper appendix，不进 main text。

---

### V-2026-05-03-08: 选定 Lane A，Lane B 留 future work

**Decision**：NeurIPS 提交版本聚焦 Lane A（diagnosis-oriented，机制解释为主）

**Rationale**：4 天窗口内，Phase 0 + Phase 1 (re-aggregation) + Phase 2 (arxiv 扩展) + Phase 3 (MEGU/IDEA framing) 已经充实。Lane B (selector refinement) 在没有 mechanism 证据先行的情况下容易退化为 heuristic stacking。

**例外**：若 Phase B 中 H4 (Conditional Shard Protection) 出现强支持，可加 appendix-level proof of concept。

---

## 2026-05-04 Session

（待今天后续添加）
