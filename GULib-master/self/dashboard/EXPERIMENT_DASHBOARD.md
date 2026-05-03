# Experiment Dashboard

> Last updated: 2026-05-03
> See rules: `CLAUDE.md`
> NeurIPS deadline: 4 days from now (~2026-05-07)

---

## 1. Phase Progress

### 4-Day NeurIPS Push

```
[ ] Phase 0  FIG-4b 5-seed 稳定性确认（partial — see §3 below）
[ ] Phase A  代码修复（必须在重跑之前完成）
    [ ] A.1  MEGU MIA bug         — megu.py:140 取消注释
    [ ] A.2  IDEA MIA bug         — idea.py:107 取消注释 + 验证 attack 块
    [ ] A.3  GraphEraser MIA bug  — Shard_based_pipeline.py:177 取消注释
    [ ] A.4  IM_v4 fixed MC seed  — 解耦 selector RNG 与 GU training seed
    [ ] A.5  Hop-distance Collateral Decay  — 扩展 evaluate_collateral_damage
[ ] Phase B  全量重跑（租 GPU）
    [ ] B.1  cora/GCN MG-0 重跑（5 seed × 5 family × 6 strategy）
    [ ] B.2  cora/GAT MG-3 重跑
    [ ] B.3  arxiv 主矩阵（参考 thesis_transition_memo §5.3）
    [ ] B.4  B2 sanity 单点（GNNDelete×TracIn ref-model）
[ ] Phase C  分析 + paper writing
    [ ] C.1  重画 FIG-4b（含 error bar + Jaccard 注释）
    [ ] C.2  生成 hop-decay 衰减曲线图
    [ ] C.3  写 §method 含 B1/B2 选择讨论
    [ ] C.4  写 §limitation 含 MEGU/IDEA mechanism-incomparable framing
```

---

## 2. Coverage Matrix（手写快照，2026-05-03）

> 待 `scripts/dashboard/refresh.py` 建好后改为自动生成。当前数据来源：`results/evaluation/stats/final_paper_stats.csv` + `results/experiments/`

### 2.1 已有数据（method × dataset × model × ratio × N_seeds）

| Method | cora/GCN/0.05 | cora/GAT/0.05 | citeseer/GCN/0.05 | 其他 |
|--------|:-:|:-:|:-:|:-|
| GIF | ✓ N=5 | ✓ N=5 | ✓ N=5 | + GIN, ratio sweep 0.05/0.1/0.2 |
| GNNDelete | ✓ N=5 | ✓ N=5 | ✓ N=5 | — |
| GraphEraser | ✓ N=5 | ✓ N=5 | ✓ N=5 | — |
| IDEA | ❌ | ✓ N=5 | ✓ N=5 | — |
| MEGU | ❌ | ✓ N=5 | ✓ N=5 | — |
| GUKD / Projector / UTU / CEU / SGU / D2DGN / ScaleGUN / GraphRevoker | ❌ 全空 | ❌ | ❌ | — |
| arxiv（任何 method） | ❌ 全空 | — | — | 计划 Phase B.3 |

### 2.2 Strategy 覆盖（横向）

每个 (method, dataset, model) cell 应包含 6 个 strategy：random / degree / pagerank / tracin / im_v4 / hybrid_v4

抽查 cora/GCN/0.05/N=5：
- GIF：6/6 ✓
- GNNDelete：6/6 ✓
- GraphEraser：6/6 ✓

注：旧版 `im` / `hybrid`（非 v4）只在部分 cell 存在，N=2-7 不等，**不进 paper**，仅历史保留。

---

## 3. 关键已知问题（截至 2026-05-03）

### 3.1 ⚠️ MIA AUC = 0.000 bug（Phase A.1-A.3）

| Family | 注释位置 | 状态 |
|--------|---------|------|
| MEGU | `unlearning/unlearning_methods/MEGU/megu.py:140` | 待修 |
| IDEA | `unlearning/unlearning_methods/IDEA/idea.py:107`（含 line 88-114 的 attack 块）| 待修 |
| GraphEraser（影响所有 shard-based）| `pipeline/Shard_based_pipeline.py:177` | 待修 |

GIF / GNNDelete 的 MIA 正常（继承 IF_based / Learning_based pipeline 调用未被注释）。详见 `VALIDATION_LOG.md` 2026-05-03 条目。

### 3.2 ⚠️ FIG-4b 在 GNNDelete 上的统计稳定性问题

cora/GCN/r=0.05/N=5 的 paired effect size：

| Cell | mean | std | 95% CI | p (>0) |
|------|------|-----|--------|--------|
| GNNDelete × IM_v4 | **+6.75** | **8.56** | **[-0.75, +14.25]** | **0.076** ❌ 不显著 |
| GNNDelete × Hybrid_v4 | +3.36 | 7.58 | [-3.29, +10.00] | 0.189 ❌ |
| GNNDelete × TracIn | +3.84 | 5.05 | [-0.59, +8.26] | 0.082 ❌ |
| GIF × TracIn | +4.17 | 0.76 | [+3.51, +4.83] | 0.0001 ✅ |
| GraphEraser × IM_v4 | +3.17 | 2.95 | [+0.59, +5.75] | 0.037 ✅ |

**GNNDelete 整行 p > 0.05**——不能在当前 5 seed 下 claim "GNNDelete 显著 vulnerable"。详见 VALIDATION_LOG。

### 3.3 ⚠️ IM_v4 selector 跨 seed Jaccard = 0.13

cora/GCN/r=0.05 上 IM_v4 在 5 个 seed 选出的 top-135 节点之间平均只有 ~17 个节点重合。**+6.8 effect 部分由"selector 自己抖"贡献，不是纯 surface variance**。Phase A.4 通过 fixed MC seed 解耦。

| Strategy | Jaccard | 解读 |
|----------|---------|------|
| random | 0.023 | sanity ✓ |
| im_v4 | **0.129** | **病态——MC 抖** |
| tracin | 0.415 | model-coupled，正常 |
| hybrid_v4 (GNNDelete) | 0.646 | 较稳 |
| pagerank | 1.000 | 纯结构 |
| degree | 1.000 | 纯结构 |

### 3.4 ⚠️ FIG-4b 数据源混合

`scripts/evaluation/generate_figures.py:33-37` 显示：
- GIF/GNNDelete/GraphEraser 来自 mg0_completion (cora/**GCN**)
- IDEA/MEGU 来自 mg3_gat (cora/**GAT**)

**5 行不在同一个 (dataset, model) 设置上**。Phase B.1 和 B.2 重跑后，应在 cora/GCN 上补 IDEA/MEGU。

### 3.5 IDEA / MEGU 整行 effect 接近 0

可能解释 A：真鲁棒；B：mechanism-incomparable（特征保留 / 梯度型独立）。详见 thesis_transition_memo §3.5。

---

## 4. 不在 4 天窗口内（已显式 out-of-scope）

- 新 backbone（GAT 之外不增加）
- Physics 数据集（feature 维度 8,415，TracIn G 矩阵 44GB）
- 新 selector 设计（Lane B 留 future work）
- 重命名 hash-named cache 文件（用 _index.json 替代，等 scripts 层）
- v3 候选指标 8.2 / 8.4 / 8.5（详见 METRICS_CATALOG）

---

## 5. 当前 TODO 优先级（高 → 低）

1. **今天**：建完本目录所有文件 + cache CLAUDE.md（进行中）
2. **今晚**：写 Phase A.1-A.5 的 patch（不应用，等审查）
3. **明天**：审 patch + 应用 + 本地 sanity test（cora/GCN 单 seed × 单 strategy 跑通）
4. **第 2 天**：租 GPU + Phase B 全量重跑
5. **第 3 天**：分析 + Phase C.1-C.2 出图
6. **第 4 天**：写 paper + 收尾

---

## 6. 何时更新本文件

- 每完成一个 checkbox：勾选 + 更新 Last updated 日期
- 每发现新的 bug / 数据问题：加到 §3
- 每改变 4 天计划：更新 §1 + §5
