# Experiment Dashboard

> Last updated: 2026-05-04
> See rules: `CLAUDE.md`
> NeurIPS deadline: 3 days from now (~2026-05-07)

---

## 1. Phase Progress

### 4-Day NeurIPS Push

```
[x] Phase 0  FIG-4b 5-seed 稳定性诊断 — 2026-05-03 完成（结论见 §3.2 / §3.3，根因已定位为 Phase A.4）
[x] Phase A  代码修复（必须在重跑之前完成）— 2026-05-04 完成 + sanity test pass
    [x] A.1  MEGU MIA bug         — megu.py:140 已取消注释（sanity AUC=0.3701）
    [x] A.2  IDEA MIA bug         — 误判，无需改动（V-2026-05-04-04 验证 ~0.55 非零）
    [x] A.3  GraphEraser MIA bug  — Shard_based_pipeline.py:177 已修（sanity AUC=0.6040）
    [x] A.4  IM fixed MC seed     — im_selector_seed=2024 默认，跨 GU seed Jaccard=1.0
    [x] A.5  Hop-distance Collateral Decay  — evaluate_collateral_damage 已扩展（4 桶 1/2/3/>3）
[x] (额外) v4 摘帽 + path/runner refactor — 2026-05-04（V-2026-05-04-06）
    - registry: `im_v4`→`im`、`hybrid_v4`→`hybrid` — 当时只是 dispatcher 层重命名
    - **2026-05-05 完成代码合并**：`im_v4_strategy.py` / `hybrid_v4_strategy.py` 文件删除，batch-CELF + `im_batch_size`（兼容 legacy `im_v4_batch_size`）合并进 `im_strategy.py::_compute_im_celf_numba`；`IMV4Strategy` / `HybridV4Strategy` 退化成 `attack_strategies/__init__.py` 的别名
    - 新路径：`results/runs/{cell}/{method}_{strategy}/seed{N}/{4 files}`
    - 新 runner：`experiments/run.py` + 4 yaml configs（见 experiments/configs/README.md）
[ ] Phase B  全量重跑（服务器侧，2026-05-05+）
    [ ] B.0  服务器 env + sanity（`experiments/configs/sanity_one_cell.yaml --force`，~20s）
    [ ] B.1  arxiv 可行性闸（`phase_b_arxiv_feasibility.yaml`，5 cells / ~1.5h，验 11 项 metric 闸 §5.3.2.1）
    [ ] B.2  arxiv 主矩阵（`phase_b_arxiv.yaml`，36 cells / ~12 GPU-h）
    [ ] B.3  cora/GCN 全矩阵（`phase_b_cora_gcn.yaml`，150 cells / ~75 min）
    [ ] B.4  cora/GAT 全矩阵（`phase_b_cora_gat.yaml`，150 cells / ~90 min）
[ ] Phase C  分析 + paper writing
    [ ] C.1  重画 FIG-4b（含 error bar + Jaccard 注释，新数据 Jaccard 应 = 1.0）
    [ ] C.2  生成 hop-decay 衰减曲线图（按 family 分线，对照 GCN num_layers）
    [ ] C.3  写 §method 含 B1/B2 选择讨论 + Shard Protection Effect 解读
    [ ] C.4  写 §limitation 含 MEGU/IDEA mechanism-incomparable framing
    [ ] C.5  abstract refresh：跑完后用真实数字替换 abstract.md 的 interim 数（见 report/paper/review/abstract_review_2026-05-04.md）
```

> **服务器侧执行入口**：`experiments/configs/README.md` 末尾的 checklist。所有 Phase B 任务都通过 `python experiments/run.py <yaml>` 启动。

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

每个 (method, dataset, model) cell 应包含 6 个 strategy：random / degree / pagerank / tracin / **im** / **hybrid**

> 2026-05-04 起 `im_v4` / `hybrid_v4` 已**摘帽**为 `im` / `hybrid`（v4 batch-CELF + decoupled MC seed 是 canonical 实现）。下面"已有数据"的 cell 是 pre-2026-05-04 跑出来的，文件里 keys 仍是 `im_v4` / `hybrid_v4`——**Phase B 重跑后新数据全部用新 keys**，old + new 数据物理隔离（老在 `results/experiments/`，新在 `results/runs/`），不会混。

抽查 cora/GCN/0.05/N=5（pre-Phase-B 旧数据）：
- GIF：6/6 ✓
- GNNDelete：6/6 ✓
- GraphEraser：6/6 ✓

---

## 3. 关键已知问题（截至 2026-05-04）

### 3.1 ✅ MIA AUC = 0.000 bug（Phase A.1-A.3）— 已修复

| Family | 位置 | 状态（2026-05-04） |
|--------|------|--------|
| MEGU | `unlearning/unlearning_methods/MEGU/megu.py:140` | ✅ 已取消注释，sanity AUC=0.3701 |
| IDEA | `unlearning/unlearning_methods/IDEA/idea.py` | ✅ 误判：实测 mia_auc≈0.55 非零（V-2026-05-04-04） |
| GraphEraser（影响所有 shard-based）| `pipeline/Shard_based_pipeline.py:177` | ✅ 已修，sanity AUC=0.6040 |

GIF / GNNDelete 的 MIA 一直正常。**Phase B 重跑前需清理 results/cache + results/selection_cache 中受 bug 污染的旧条目**（cli: `--no_cache` 一次性强制刷新），否则会取到 mia_auc=0 的 stale 缓存。

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

### 3.3 ✅ IM_v4 selector 跨 seed Jaccard = 0.13 — A.4 已修复

cora/GCN/r=0.05 上 IM_v4 在 5 个 seed 选出的 top-135 节点之间平均只有 ~17 个节点重合。**+6.8 effect 部分由"selector 自己抖"贡献，不是纯 surface variance**。

**修复（2026-05-04, A.4）**：`attack/attack_strategies/im_strategy.py` 改读 `args['im_selector_seed']`（默认 2024），不再 fallback 到 `random_seed`/`seed`。微测验证：seed=42 vs seed=1337 的 IM_v4 选出节点集 **完全相同**（Jaccard=1.0）。Phase B 重跑前需清空 `results/selection_cache/im_v4/`（旧条目按 GU seed 分桶，5 份非决定性数据）。

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

### 已完成 ✅
1. **2026-05-03**：dashboard 目录骨架 + cache CLAUDE.md
2. **2026-05-04 上午**：Phase A.1–A.5 patch + 本地 sanity 全 pass（V-2026-05-04-04）
3. **2026-05-04 下午**：predictions.npz 缓存 + round-trip 验证（V-2026-05-04-05）
4. **2026-05-04 晚**：path/runner refactor + v4 摘帽（V-2026-05-04-06）
5. **2026-05-04 晚**：abstract 重写为 ECCV interim 版（report/paper/sections/abstract.md，review 笔记 review/abstract_review_2026-05-04.md）

### 服务器侧（按顺序执行）
1. **B.0** `git pull` → conda env → `python experiments/run.py experiments/configs/sanity_one_cell.yaml --force` —— 验证 env，~20s
2. **B.1** `python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml` —— 5 family × random × 1 seed，对照 §5.3.2.1 的 11 项闸门
3. **B.2** B.1 全 pass → `python experiments/run.py experiments/configs/phase_b_arxiv.yaml` —— 36 cells / ~12 GPU-h
4. **B.3 / B.4** 并行（如有第二张卡）：cora/GCN + cora/GAT 全矩阵
5. **Phase C** 数据回流 → 分析 + 出图 + paper（见 §1 Phase C 列表）

### 关键数据交付节点（NeurIPS 2026-05-07）
- 主 figure: FIG-4b 重画后入 paper §4
- hop-decay 衰减曲线: §4 第二张图，按 family 分线
- abstract refresh: 用真实数字替换 interim 数（abstract.md §status 已标 interim）

### 不在 4 天窗口的（确认 out-of-scope）
- 见 §4：vision-graph 实验（PASCAL-VOC/Kinetics/ShapeNet）、新 backbone、新 selector 设计、Physics 数据集

---

## 6. 何时更新本文件

- 每完成一个 checkbox：勾选 + 更新 Last updated 日期
- 每发现新的 bug / 数据问题：加到 §3
- 每改变 4 天计划：更新 §1 + §5

---

## 7. Historical Appendix — `results/experiments/` 子目录对应表

> 迁入日期：2026-05-05（原文件 `results/experiments/CLAUDE.md` 在 1300+ 文件 untrack 时一并删除，但 mapping 表本身保留参考价值）。
> 数据本身因 bug（MIA AUC=0、IM Jaccard=0.13）已不可信于 paper 引用；本表仅供历史溯源。

### 7.1 子目录对应表（pre-Phase-B 命名）

| 子目录 | 实验内容 | 数据集 | 模型 | 备注 |
|--------|---------|-------|------|------|
| `mg0_completion/` | 稳定性实验（同 dataset/model 多 seed） | cora | GCN | N=5 seeds, ratio=0.05, 5 family，FIG-4b 数据源（前 3 行）|
| `mg1_citeseer/` | 跨数据集 | citeseer | GCN | 仅 GIF/GNNDelete/GraphEraser |
| `mg2_gat/` | 跨 backbone（GCN → GAT）| cora | GAT | 仅 GIF（部分）|
| `mg3_citeseer/` | 跨 dataset 扩展（含 IDEA/MEGU）| citeseer | GCN | IDEA/MEGU/GIF/GNNDelete/GraphEraser |
| `mg3_gat/` | 跨 backbone 扩展（含 IDEA/MEGU）| cora | GAT | FIG-4b 数据源（后 2 行）|
| `p2_ext_gif_GCN/` | GIF 在 GCN 上的 ratio 敏感性 | citeseer | GCN | 仅 GIF |
| `p2_ext_gif_GAT/` | 同上 GAT | citeseer | GAT | 仅 GIF |
| `p2_ext_gif_GIN/` | 同上 GIN | citeseer | GIN | 仅 GIF |
| `im_v4_compare/` | IM_v4 vs 旧 IM 性能对比 | — | — | 方法学 ablation |
| `im_v4_probe/` | IM_v4 算法内部 probe | — | — | debug 用 |
| `ratio_sensitivity/` | ratio sweep | citeseer | GCN/GAT/GIN | 仅 GIF，ratio={0.05, 0.1, 0.2} |
| `_archive/` | 归档（旧批次）| — | — | 只读 |
| `_tmp_timeout_test/` | 临时调试输出 | — | — | 可删 |

### 7.2 路径模板

```
results/experiments/<group>/phase_a/<YYYYMMDD_HHMMSS>_seed<seed>/<Method>_<dataset>_<model>_r<ratio>_s<seed>.json
```

### 7.3 已知 bug 影响（这些数据为何不可直接用于 paper）

- 所有 `mg0/mg1/mg3` 的 IDEA/MEGU/GraphEraser 文件中的 `mia_auc` 字段为 0.000（代码 bug，已在 Phase A 修复）
- 所有 IM/Hybrid 类 strategy 跨 GU seed Jaccard ≈ 0.13（IM Monte-Carlo seed 未独立，已在 Phase A.4 修复）
- 详细 bug 定位与修复说明：§3.1 / §3.3

### 7.4 Phase B 命名替代（新规则）

旧 `results/experiments/<group>/...` 的批次概念被废弃。Phase B 起一律用 cell-leaf 三层路径：

```
results/runs/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{N}/{attack,collateral,predictions,_meta}
```

详见 `experiments/configs/README.md`。
