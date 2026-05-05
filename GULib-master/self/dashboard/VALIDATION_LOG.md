# Validation Log

> Last updated: 2026-05-06
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

### V-2026-05-04-01: §3.5 IDEA/MEGU 立场承诺为 B（mechanism-incomparable）

**Decision**：默认承诺"B 不可比"作为论文叙事，而非"A 真鲁棒"

**Reasons**：
- A 等于承认攻击对 IDEA/MEGU 失败，立场被动
- B 把 0 effect 转成 mechanism finding（"该类方法的设计天然免疫当前 selector 信号"），立场主动且有 future-work 钩子
- A 不被否认，作为 supplementary audit；若 Phase B 时间允许，跑 IDEA/MEGU 专属 selector（直接扰动 x_unlearn 或 gradient-objective-aware）作 sanity

**FIG-4b 处置**：保留 5 行，IDEA/MEGU 行加阴影/标注，caption 明确

**详见**：`thesis_transition_memo.md §3.5`

---

### V-2026-05-04-02: §3.4 attack-as-importance-proxy 反驳证据已就位

**问题**：referee 必问"informed selector 是不是只是 importance proxy"

**已存数据可反驳**（无需新实验）：

| 反驳点 | 数据 |
|--------|------|
| 跨 family selector 排序翻转 | GIF: TracIn>>IM；GNNDelete: IM>>TracIn |
| PageRank ≠ IM ≠ TracIn 效果差 | GNNDelete: 10.83 vs 12.32 vs 8.46 (Rel_F1_Drop, MG-0) |
| Jaccard 异 | PageRank=1.0 / IM=0.13 / TracIn=0.42 |
| family-specific 免疫 | IDEA/MEGU 对所有 selector ~0 |

**Paper 操作**：单列一节"Are informed selectors just importance proxies?"，依次列证据

**详见**：`thesis_transition_memo.md §3.4` 预先反驳证据段

---

### V-2026-05-04-03: §5.3.2 arxiv 可行性闸增加 metrics 验证清单

**问题**：可行性闸只验证"跑通"是不够的，arxiv 是修复 MIA bug + 加 hop-decay 后**新代码第一次大图运行**，必须验证所有 metric 产出合理值

**12 项检查清单**详见 `thesis_transition_memo.md §5.3.2.1`，关键项：
- mia_auc 不为 0.000 且 ∈ [0.3, 0.9]（验证 MIA fix 在 arxiv 上生效）
- hop_decay 含完整 keys 且 1-hop ≥ 2-hop ≥ 3-hop（验证 hop-decay 实现且符合预期单调性）
- selection_time (IM_v4) < 30 min（验证 candidate_fraction + numba 在大图上有效）

**操作时机**：每个 family 的 1-seed random 跑完即对照清单，全 pass 才进主矩阵

---

### V-2026-05-04-04: Phase A.1–A.5 patch 应用 + sanity test 全部通过

**Setting**：cora/GCN/r=0.05/seed=42，--no_cache 强制刷新

**A.1 MEGU MIA fix**（`unlearning/unlearning_methods/MEGU/megu.py:140`）
- 取消注释并加 `unlearn_task=='node' and downstream_task=='node'` 守卫
- sanity：`Average AUC Score: 0.3701`（pre-fix 0.0）✅

**A.2 IDEA MIA — dashboard 误判**：实测 IDEA 的 mia_auc 始终非零
- 审 10 个 IDEA result JSON × 4 strategy × N seed → 40 条 mia_auc 值，全部 ∈ {0.4, 0.6}，**zero=0 nonzero=40 nan=0**
- 机制：`idea.py:54-169` 整段 `run_exp` 注释，但 fall-through 到 `pipeline/IF_based_pipeline.py::run_exp:142` 的 `self.mia_attack()`，IDEA 又在 `idea.py:508` 重写了 `mia_attack`（功能完整）
- **决定**：dashboard §3.1 + V-2026-05-03-05 关于 IDEA 的指控撤销（其它两条 MEGU/GraphEraser 仍成立）
- **MEGU + GraphEraser → IDEA 列表受污染**：意味着 paper 不能再用 V-2026-05-03-05 的 "MEGU/IDEA/GraphEraser 整列 0 → 不可比" 框架，而应改为 "MEGU/GraphEraser 0 是 bug，IDEA 0.55 是真低敏感"

**A.3 GraphEraser MIA fix**（`pipeline/Shard_based_pipeline.py:177`）
- 取消注释 `self.attack_unlearning()` 并加 `unlearn_task=='node' and downstream_task=='node'` 守卫
- sanity：`Average AUC Score: 0.6040`（pre-fix 0.0），MIA Progress 100% × 2（member + nonmember）✅
- 同步影响 GUIDE / GraphRevoker（两者也有 `attack_unlearning` 实现，未来跑这俩 family 时自动生效）

**A.4 IM_v4 fixed MC seed**（`attack/attack_strategies/im_strategy.py:140-148`）
- 改读 `args['im_selector_seed']`（默认 2024），不再 fallback 到 `random_seed`/`seed`
- 微测：cora，args_a={seed:42,...} vs args_b={seed:1337,...}，IMV4Strategy.select_nodes(k=20) 返回**完全相同**的节点列表（identical=True，Jaccard=1.0）
- **缓存影响**：旧的 `results/selection_cache/im_v4/` 按 GU seed 分桶 5 份非决定性数据，Phase B 重跑前需清空（或保留作历史快照）

**A.5 Hop-distance Collateral Decay**（`attack/attack_eval.py::evaluate_collateral_damage`）
- 新增 `unlearn_nodes` + `max_hop` 可选参数；新增内部 `_bfs_hop_distance` 用 deque BFS（O(V+E)）
- 返回字典加 `hop_decay` 子 dict，含 `1_hop_flip_rate / 1_hop_count ... gt3_hop_flip_rate / gt3_hop_count`
- 同步更新 `eval_collateral.py:407` 传入 `unlearn_nodes=selected_nodes`
- 18 个 attack_eval 单元测试全部通过（向后兼容，未传 unlearn_nodes 时不输出 hop_decay）
- 端到端 sanity（cora，dummy model，3 个 unlearn 节点）：
  ```
  1_hop_count=6   1_hop_flip_rate=1.00
  2_hop_count=25  2_hop_flip_rate=0.84
  3_hop_count=145 3_hop_flip_rate=0.80
  gt3_hop_count=2529 gt3_hop_flip_rate=0.83
  sum=2705 = retain_count ✓
  ```

**Verification commands**（可重复）：
```bash
# A.4 micro-test
H:/conda_package/envs/gnn/python.exe -c "from attack.attack_strategies.im_v4_strategy import IMV4Strategy; ..."

# A.1/A.3 end-to-end
H:/conda_package/envs/gnn/python.exe demo_attack.py --dataset_name cora --base_model GCN \
  --unlearning_methods {MEGU,GraphEraser} --strategies random --unlearn_ratio 0.05 \
  --seed 42 --no_cache --num_epochs 100 --batch_size 64

# Unit tests
H:/conda_package/envs/gnn/python.exe -m pytest tests/test_attack_eval.py -x -q
```

**下一步（Phase B 启动前）**：
1. 清 `results/cache/` + `results/selection_cache/im_v4/` 中 mia_auc=0 / 旧 IM 抖动条目
2. 决定 GPU 渠道（本地 / 租）
3. 跑 cora/GCN/seed=42 单 cell × 6 strategy 作 Phase B 第一闸（验证 5 family × 6 strategy 全部产出 mia_auc ∈ [0.3,0.9]）

---

### V-2026-05-04-05: eval_collateral.py 加 `--save_predictions` 实现 metric 解耦缓存

**Decision**：Phase B 全量重跑时启用 `--save_predictions`，让 forward-only metric 未来可离线重算

**Rationale**：
- 当前架构不持久化 model（state_dict 跨代码版本不可复用），新 metric 必须重跑整条 train+unlearn+retrain 链
- 但 6 个 v2 metric + 8.4 Budget Efficiency 全部基于 forward predictions（softmax / argmax / 距离），不依赖 model gradients
- 保存 `logits_{before, unlearned, retrained}` + `labels` + `train/test_mask` + `retain_mask` + `selected_nodes` 即可在离线脚本中复算所有现有 + 多数预期未来 metric
- 相对存 model：(a) 大小小一个量级（cora 0.2MB/strategy vs ~3MB/state_dict），(b) 跨 PyTorch 版本无依赖，(c) 与代码改动解耦

**实现**（`eval_collateral.py`）：
- CLI `--save_predictions`（默认关，opt-in）
- 落盘：`results/collateral/{Method}/{Dataset}/{Model}/predictions_{timestamp}.npz`
- npz keys：`_meta__y / _meta__train_mask / _meta__test_mask / _meta__num_nodes` + 每个 strategy `{s}__logits_{before,unlearned,retrained} / {s}__retain_mask / {s}__selected_nodes`

**Round-trip 验证**（cora/GCN/GIF/random/seed=42）：

| 指标 | offline 重算 | JSON 内 | 匹配 |
|------|-------------|---------|------|
| gap | -0.0018 | -0.0018 | ✓ |
| 1-hop count/flip_rate | 348 / 0.0172 | 348 / 0.0172 | ✓ |
| 2-hop count/flip_rate | 895 / 0.0078 | 895 / 0.0078 | ✓ |
| 3-hop count/flip_rate | 461 / 0.0065 | 461 / 0.0065 | ✓ |

bit-identical。1-hop > 2-hop > 3-hop 单调衰减（GIF retain-set 对预测的扰动确实随 hop 距离衰减，与 §8.3 hop-decay 假说一致）。

**预期容量**（Phase B 全跑）：
- cora 单 cell（6 strategy）≈ 1.2MB
- arxiv 单 cell（6 strategy）≈ 90MB（169K nodes × 40 classes × float32 × 6 strategy × 3 model × compress 0.5）
- 全 Phase B：cora/GCN + cora/GAT + arxiv ≈ 50 cell × 6 strategy → cora 部分 ~60MB + arxiv 部分 ~5GB ≈ 5GB

**离线重算示例**（用于未来加 metric）：
```python
bundle = np.load('predictions_*.npz')
y = bundle['_meta__y']; tm = bundle['_meta__test_mask']
for s in [...]:
    lb = bundle[f'{s}__logits_before']; lu = bundle[f'{s}__logits_unlearned']
    f1_drop = f1(y[tm], lb.argmax(1)[tm]) - f1(y[tm], lu.argmax(1)[tm])
```

---

### V-2026-05-04-06: Path / runner refactor + v4 摘帽

**Decision**：用户 2026-05-04 反馈现有 `results/experiments/{mgN}/phase_a/` 命名按 milestone 而非内容、`im_v4` 帽子已无意义、bash 脚本 + CLI 重复。**不迁老数据，新跑用新 runner**——服务器侧从 yaml 配置启动。

**新路径方案** (`results/runs/`)：
```
results/runs/
  cora_GCN_r0.05/                       # cell = (dataset, model, ratio) 三元组
    GIF_random/                          # leaf = (method, strategy) 二元组（method+strategy 间用 _ 分）
      seed42/
        attack.json                      # L3 metric（demo_attack）
        collateral.json                  # L3 metric（eval_collateral）
        predictions.npz                  # L2 logits bundle（含 selected_nodes/retain_mask 完整快照）
        _meta.json                       # audit：config snapshot + git_sha + hostname + timestamp
```

3 层深度（cell / leaf / seed），叶子内 4 个文件。glob 模式见 `experiments/configs/README.md`。

**v4 摘帽**：
- `attack/attack_manager.py::BUILTIN_STRATEGIES`：删 `"im": IMStrategy`、`"hybrid": HybridStrategy`、`"im_v4": IMV4Strategy`、`"hybrid_v4": HybridV4Strategy`，新建 `"im": IMV4Strategy` + `"hybrid": HybridV4Strategy`（v4 版变成 canonical 实现）
- `REUSABLE_SELECTION_STRATEGIES`：去掉 `"im_v4"`，留 `{"random", "pagerank", "im"}`
- `_strategy_params_for_cache`：合并 im / im_v4 分支，统一报 `im_batch_size`
- 默认 `--strategies`：demo_attack 改为 `random,degree,pagerank,tracin,im,hybrid`，eval_collateral 同
- 测试 `tests/test_im_hybrid.py` 36/36 通过；新增 `test_im_resolves_to_v4_implementation` / `test_v4_alias_no_longer_registered`
- 老 cache + 老 JSON 里的 `im_v4` / `hybrid_v4` keys：服务器全新跑，物理隔离

**GCN 参数化**（解决 arxiv f1>0.55 闸门）：
- `parameter_parser.py` 加 `--gcn_num_layers`（默认 2）、`--gcn_hidden`（默认 64）
- `model/base_gnn/gcn.py` 改读 args；`forward` / `forward_once` / `forward_once_unlearn` 全部循环化兼容多层
- arxiv yaml `model_overrides.GCN: {gcn_num_layers: 3, gcn_hidden: 256}`，OGB benchmark 配置
- cora/citeseer 默认 2/64 与 pre-patch bit-identical 验证：sanity GIF/random/seed=42 跑出 f1=0.88，与 2026-05-04 早期 sanity 相同 ✅

**eval_collateral.py 加 `--output_dir`**：runner 模式下 collateral.json + predictions.npz 写到指定目录、无 timestamp 后缀；老的 `results/collateral/{Method}/{ds}/{model}/collateral_{ts}.json` 路径在 `--output_dir` 不传时保持不动。

**experiments/run.py runner**：~200 行 subprocess 调度
- 读 yaml → 展开 method × strategy × seed 三重循环
- 每 cell 串接 demo_attack（写 attack.json）+ eval_collateral --save_predictions --output_dir（写 collateral.json + predictions.npz）+ runner 自己写 _meta.json
- skip-if-exists：4 文件齐全则跳过；`--force` 强制重跑；`--dry_run` 列出会跑什么；`--limit N` 调试用
- UTF-8 yaml load（Windows GBK 默认会挂中文注释）

**Sanity test**（cora/GCN/GIF/random/seed=42，单 cell）：
```
=== Loaded sanity_one_cell.yaml ===
  cell: cora_GCN_r0.05
  total cells: 1
  model_overrides: {'gcn_num_layers': 2, 'gcn_hidden': 64}
[run] demo_attack GIF/random/seed42 → results\runs\cora_GCN_r0.05\GIF_random\seed42
[run] eval_collateral GIF/random/seed42
=== Summary === completed: 1, elapsed: 18.3s
```

文件落地：
- `_meta.json`：config_name, git_sha=353fccb..., hostname=LELE-MSI ✅
- `attack.json`：12.5KB，含 selected_nodes ✅
- `collateral.json`：含 gap=-0.0018 + hop_decay 4 桶 keys ✅
- `predictions.npz`：210KB，含 logits_{before,unlearned,retrained} + masks + selected_nodes ✅

**三个 yaml 配置 dry-run 通过**：
- `phase_b_cora_gcn.yaml`：5 method × 6 strategy × 5 seed = 150 cells
- `phase_b_cora_gat.yaml`：同 150 cells
- `phase_b_arxiv.yaml`：3 method × 4 strategy × 3 seed = 36 cells（OGB 3/256 GCN 配置）
- `phase_b_arxiv_feasibility.yaml`：5 method × random × 1 seed = 5 cells（先跑这个闸）

**下一步（服务器侧）**：见 `experiments/configs/README.md` 服务器 checklist。git push 后 ssh server → conda env → `python experiments/run.py ...`。

---
<!--
  DRAFT — to be appended to VALIDATION_LOG.md once r=0.05 + r=0.10 matrices complete.
  Numbers in `<TBD>` placeholders will be filled by aggregate_graphrevoker_sanity.py output.
-->

## 2026-05-05 Session

### V-2026-05-05-01: V4 strategy classes merged into V1 (代码合并完成)

**Setting**: 2026-05-04 V-...-06 only renamed the registry (`im_v4`→`im`, `hybrid_v4`→`hybrid`); the V4 implementations stayed in separate files (`im_v4_strategy.py`, `hybrid_v4_strategy.py`) inheriting from V1.

**Action (commit `028eb08`)**:
- Merged `IMV4Strategy._compute_im_celf_v4_numba` (batch-CELF) into `IMStrategy._compute_im_celf_numba` as the canonical numba path.
- Added `self.im_batch_size` to `IMStrategy.__init__`; legacy `im_v4_batch_size` kwarg still accepted for backward compat.
- Deleted `im_v4_strategy.py`, `hybrid_v4_strategy.py`.
- `IMV4Strategy = IMStrategy` and `HybridV4Strategy = HybridStrategy` aliases retained in `attack/attack_strategies/__init__.py` so old imports still resolve.
- `attack/attack_manager.py::BUILTIN_STRATEGIES` now maps `"im"` → `IMStrategy`, `"hybrid"` → `HybridStrategy` directly.

**Verification**:
- `pytest tests/test_im_hybrid.py` → 36 passed
- `pytest tests/test_strategy_goldens.py` → 10 passed (golden behavior preserved — IMStrategy was already routed to V4 batch-CELF via the registry, so merging file content doesn't change observable output)
- `experiments/run.py sanity_one_cell.yaml --force` → completed: 1, elapsed 18.3s

**Implication**: `flow.md:10` "已被替代" warning is now factually accurate. The HybridStrategy → `compute_initial_marginal_gains` (NOT `compute_im_celf`) call path is documented in `flow.md:36-44`; per-node fusion fundamentally cannot use CELF's (k, k) output.

---

### V-2026-05-05-02: GraphRevoker dispatcher un-aliased + class bugs fixed

**Finding**: `unlearning_manager.py:40` was `"GraphRevoker": grapheraser` since the original 2026-02 commit. Every experiment with `--unlearning_methods GraphRevoker` actually exercised the GraphEraser implementation. **All historical "GraphRevoker" data** in `results/cache/`, `log/GraphRevoker/`, `results/evaluation/step0/method_compatibility.json:262-287`, etc. were GraphEraser results mislabeled.

**Source**: `experiments/configs/SANITY_GRAPHREVOKER.md:9, 102` (the user's own runbook flagged this; the alias was never flipped before today).

**Action (commits `6045e47`, `e3bbd54`, `0e8071a`)**:
1. Un-aliased dispatcher: line 40 → `"GraphRevoker": graphrevoker`.
2. Fixed `graphrevoker.gen_train_graph` AttributeError on `self.test_indices` (idempotent `train_test_split()` guard).
3. Fixed `graphrevoker.generate_shard_data` AttributeError on `self.datafull` (initialize from `self.data`).
4. yaml `extra_args: ["--partition_method", "gpa"]` (GraphRevoker only supports `random` / `gpa`; default `lpa_base` raises "Unsupported partition method").
5. `OptimalAggregator.generate_train_data` now sets `target_model.data = train_data` (not just `data_full`); `GraphRevokerTrainer._inference` reads `self.data`, not `self.data_full` like NodeClassifier — that asymmetry made the bug latent until now.
6. `GraphRevokerTrainer.prepare_data` replaces `self.data` wholesale (was only updating `edge_index`, leaving stale `x`).
7. `graphrevoker.attack_unlearning` calling-signature fix.
8. `OptimalAggregator._generate_train_data` defensive `np.clip` for `node2com[selected_indices]` (length mismatch after run_retrain).

**Verification (sanity, cora/GCN/r=0.05/random/seed=42)**:
- `f1_after = 0.7804` (runbook target [0.78, 0.88]) ✅
- `mia_auc = 0.833` (runbook: finite > 0) ✅
- `gap = +5.17%` (collateral)
- 4 artifacts written: attack.json, collateral.json, predictions.npz, _meta.json
- elapsed: 124s for sanity, ~12 min for the 6-strategy matrix

**r=0.05 full matrix (6 strategies × seed=42, 6/6 completed in 765s)**:

| strategy | F1_unlearn | F1_retrain | Gap | Gap% | MIA |
|----------|-----------:|-----------:|----:|-----:|----:|
| random   | 0.5812 | 0.5683 | -0.0129 | -2.27%  | 0.849 |
| degree   | 0.6144 | 0.5775 | -0.0369 | -6.39%  | 0.847 |
| pagerank | 0.5978 | 0.6328 | +0.0351 | +5.54%  | 0.834 |
| tracin   | 0.5812 | 0.6089 | +0.0277 | +4.55%  | 0.849 |
| im       | 0.5775 | 0.6162 | +0.0387 | +6.29%  | 0.847 |
| hybrid   | 0.5904 | 0.5941 | +0.0037 | +0.62%  | 0.837 |

**r=0.10 full matrix (6 strategies × seed=42, 6/6 completed in 803s)**:

| strategy | F1_unlearn | F1_retrain | Gap | Gap% | MIA |
|----------|-----------:|-----------:|----:|-----:|----:|
| random   | 0.6476 | 0.6089 | -0.0387 | -6.36%  | 0.749 |
| degree   | 0.6125 | 0.5849 | -0.0277 | -4.73%  | 0.607 |
| pagerank | 0.6273 | 0.5849 | -0.0424 | -7.26%  | 0.621 |
| tracin   | 0.5646 | 0.5498 | -0.0148 | -2.68%  | 0.808 |
| im       | 0.6070 | 0.6181 | +0.0111 | +1.79%  | 0.754 |
| **hybrid** | **0.4926** | **0.5683** | **+0.0756** | **+13.31%** | **0.849** |

**Interpretation**:

- **Hybrid is uniquely effective at r=0.10**: Gap +13.31%, MIA 0.849 — massively beats every other strategy (next is im +1.79%, then four negative-Gap strategies). The +19.67% absolute Gap difference vs random (-6.36%) is the biggest paired effect we've seen on a shard-based method.
- **Shard protection visible at r=0.10**: random/degree/pagerank/tracin all have **negative Gap** — meaning F1_unlearn > F1_retrain, i.e. GraphRevoker's shard isolation preserved more performance than retraining-from-scratch. Hybrid is the only strategy that breaks through.
- **MIA inversely tracks shard protection**: when Gap is negative (shard wins), MIA drops to 0.61–0.81; when Gap is positive (attack works), MIA stays at the 0.85 ceiling. Confirms that "attack succeeded" and "MIA is sensitive" co-occur.
- **r=0.05 is too small to separate**: all gaps within ±6%, MIA all within 0.83–0.85. Use r=0.10 as the report budget for this method.

**Implication**: GraphRevoker is now usable as the 6th method for Phase B. Adding to `phase_b_cora_gcn.yaml` / `phase_b_cora_gat.yaml` is unblocked (per SANITY_GRAPHREVOKER.md Step 5). Pre-2026-05-05 GraphRevoker data must be treated as GraphEraser; do not cite.

**Memory entry**: `project_graphrevoker_dispatcher_history.md` — for future sessions reading old paper claims that mention "GraphRevoker", check the date; pre-2026-05-05 invalidates the GraphRevoker label.

---

## 2026-05-06 Session

### V-2026-05-06-01: Phase B attack pipeline 5-bug correctness audit (RESOLVED)

**Background**：在审 codex 写的 `fix/phase-b-blockers` 时连续发现 5 条 attack pipeline 正确性问题，全部影响 Phase B 既有 attack.json / collateral.json 的可信度。同会话内修完，分两个 commit：`66a90f8`（codex 4 条）+ `13f1e89`（我补的 train-before-select + Hybrid 修复）。

**Bug list & evidence chain**：

1. **`config.unlearning_path` 路径错位**（最致命）
   - **Trigger**：`demo_attack.py:43` `parse_known_args` 之后 `sys.argv = [argv[0]] + remaining_args`，把 `--dataset_name --base_model --unlearning_methods --unlearn_ratio --proportion_unlearned_nodes --num_epochs --batch_size --random_seed` 都剥光
   - **Cascade**：`from attack import AttackManager` → `attack/pipeline_adapter.py:34 from config import unlearning_path` → `config.py:2 args = parameter_parser()` 此时 sys.argv 已空 → 烘出默认 `cora/0.1/transductive/imbalanced` 路径
   - **Read 路径**：SGU/IDEA/GUIDE/GST/CGU/ScaleGUN/GUKD/GraphEraser_MIA/GUIDE_MIA + `utils/dataset_utils.py:12` 都 `from config import unlearning_path`，import 时拿到上面那个错误 string
   - **Write 路径**：`AttackPipeline._inject_unlearn_nodes:201` 自己用 `self.args` 拼路径，写到正确 (arxiv/0.05) 路径
   - **结果**：方法读不到 inject 的文件，可能 fallback 到磁盘上残留的 `unlearning_nodes_0.1_cora_*.txt`（来自旧 cora 实验），静默 unlearn 来自不同 dataset 的节点 ID
   - **Fix**：`demo_attack.py:48-60` 把 shared args 回注 sys.argv；`pipeline_adapter.py:201` 加 `assert path == config.unlearning_path + run_id`

2. **Random/Degree/PageRank 不限 train_mask**
   - `random_strategy.py:17 torch.randperm(data.num_nodes)`、degree/pagerank 同样 `torch.topk(scores, k)` 在全图
   - cora train ~140/2708 ≈ 5%，所以 ≥94% 概率选到 val/test
   - **Fix**：`BaseStrategy.candidate_nodes` helper（train_mask → train_indices → arange fallback），三策略全部走它；测试 fixture 加 `assert_subset_of_train_mask: true` 校验

3. **TracIn / Hybrid 在 random-init 模型上算梯度**
   - **Trigger**：`AttackPipeline._setup:120` 只 `model_zoo(args, data)`（构造，权重随机），训练在 `method.run_exp()` 里发生
   - **Order**：`pipeline_adapter.run_with_strategy:229` `strategy.select_nodes(data, self.model, k)` ← 用 random-init；`run_with_selected_nodes` 里才 `method.run_exp()` 训练
   - **Math**：random-init 下 `out[i] = A·X·W_random` 强烈依赖度数 + 邻域特征，gradient 退化为 structural-feature-norm 代理
   - **Implication**：所有 Phase B TracIn/Hybrid 数字看似工作（F1 drop / collateral 都动），实际测的是结构启发，不是 IF；论文不能 claim "IF-guided"
   - **Fix**：`BaseStrategy.requires_trained_model` 标志位；`AttackPipeline._ensure_base_model_trained()` 用 `args["train_only"]=True` 跑 `method.run_exp()` 训练 + state_dict snapshot 跨 strategy 复用；`run_with_strategy` hook
   - **Cache schema bump**：`tracin_strategy._build_cache_config` 和 `attack_manager._build_selection_config` 都加 `cache_schema: "v2"`，旧 random-init 时代缓存自动作废

4. **eval_collateral.py 缺 seed**
   - `eval_collateral.py:287 main()` 全文没有 `seed_everything / random.seed / np.random.seed / torch.manual_seed`
   - retrain 不可复现：`predictions.npz::logits_retrained` 同 seed 跑两次得到不同 logits
   - **Fix**：加 `_seed_everything(seed_value)` 在 `args['proportion_unlearned_nodes']` sync 之后调

5. **demo_attack 没同步 `proportion_unlearned_nodes`**
   - parameter_parser 默认 0.1 vs `unlearn_ratio` 0.05；`config.py:45 GIF_logger_name` 用 `proportion_unlearned_nodes`，cache key、df_size 计算、log 路径全错
   - eval_collateral.py 已经在 line 304 同步，demo_attack 没有
   - **Fix**：args dict 和 sys.argv 注入两处都同步

**附带 fix**（不是同源 bug 但顺手处理）：
- `HybridStrategy.select_nodes` 之前绕过 `compute_im_celf` 直接调 `compute_initial_marginal_gains`，**不应用 `candidate_fraction` pruning** → 改为对 IF/IM 共享候选集统一 prune（`hybrid_strategy.py:54-65`）
- `--alpha` 字段同时是 GNNDelete/CGU loss alpha 和 Hybrid fusion ω → A.3 alpha sweep 不能直接用这个字段；新加 `--hybrid_alpha`，向后兼容 fallback 到 `alpha`（`parameter_parser.py:99-103`、`hybrid_strategy.py:35-39`）

**端到端验证**（cora/GCN/GIF/random+tracin/seed=42，cli `H:/conda_package/envs/gnn/python.exe demo_attack.py ...`）：
```
Training base model for selection (requires_trained_model strategy)...
Epoch: 030 | F1 Score: 0.8838 | Loss: 0.2661
Base model trained (F1=0.8838); state_dict snapshot taken.
[ScoreCache] MISS if  key=9e1f5b8... — computing TracIn scores...   ← v2 schema 触发新 key
Strategy selected nodes: [1017, 1924, 1065, 1274, ...]
Injected 108 nodes to unlearn at ./data/unlearning_task/transductive/imbalanced/unlearning_nodes_0.05_cora_0.txt
                                                                                ↑ assert 通过：path 与 config.unlearning_path 一致
F1 after unlearning: 0.8875
Average AUC Score: 0.5718                                                       ← MIA 非零
```

**测试**：`pytest tests/ --ignore=tests/test_report_figure_refresh.py` → **185 passed**（FIG-2 测试需要磁盘上 Phase B 数据，pre-existing fail，与本次改动无关）。

**对 Phase B 数据的影响**：
| 数据类型 | 状态 |
|---|---|
| `results/runs/**/attack.json` (TracIn / Hybrid cells) | ❌ 测的是 random-init 代理 |
| `results/runs/**/attack.json` (Random / Degree / PageRank cells) | ❌ 跨 train_mask，预算未匹配 |
| `results/runs/**/attack.json` (IM cells) | ✅ 不依赖模型，候选集本就限 train_mask |
| `results/runs/**/collateral.json::retrain_gap` | ⚠️ 单次有效但跨 seed 不可复现 |
| `results/runs/**/predictions.npz::logits_before/unlearned` | ✅ 来自 ResultCache，非 retrain，不受 seed bug 影响 |
| `results/runs/**/predictions.npz::logits_retrained` | ⚠️ 不可复现 |
| `results/baseline/k5_random/**` | ✅ 不受影响 |
| `results/score_cache/`、`results/selection_cache/` | ✅ 现在只剩 v2 entry（旧 entry 在 2026-05-05 untrack 时一并删除） |

**重跑计划**：见 EXPERIMENT_DASHBOARD §3.6 + §5。B.0 sanity 验 v2 binary，再依次 B.1 → B.2 → B.3 / B.4。

**Branch**: `fix/blocker-1-train-before-select`，commits `66a90f8` + `13f1e89`，145 行 attack/ + 49 行 demo_attack + 21 行 eval_collateral + 4 行 parameter_parser，diff `git diff main..HEAD --stat`。

---

