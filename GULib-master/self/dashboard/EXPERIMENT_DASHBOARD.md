# Experiment Dashboard

> Last updated: 2026-05-07 (§3.3 衍生事实 + IM cross-cell cache 行为 + arxiv k 选择 tradeoff + master scorecard / k=5 dual-baseline)
> See rules: `CLAUDE.md`
> NeurIPS deadline: today (~2026-05-07)

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
    [ ] B.2-T1  arxiv 主矩阵 seed=42（`phase_b_arxiv_T1_seed42.yaml`，12 cells / ~6-8h，**必跑**）
    [ ] B.2-T2  arxiv 主矩阵 seed=212（`phase_b_arxiv_T2_seed212.yaml`，12 cells / ~7-8h，条件跑）
    [ ] B.2-T3  arxiv 主矩阵 seed=722（`phase_b_arxiv_T3_seed722.yaml`，12 cells / ~7-8h，条件跑）
        # 2026-05-06: 原 phase_b_arxiv.yaml 单 yaml ~21-24h 压 deadline 太紧；拆三段 deadline 到了 kill，已完成 cell 受 fingerprint 保护
        # 注：tier split 不省时间——ScoreCache IF key 含 seed (`tracin_strategy.py:136-149`)，每 tier 独立 ~7-8h
    [ ] B.3  cora/GCN 全矩阵（`phase_b_cora_gcn.yaml`，180 cells / ~90 min；旧 5 method 完成时只补 GraphRevoker）
    [ ] B.4  cora/GAT 全矩阵（`phase_b_cora_gat.yaml`，180 cells / ~110 min）
[x] Phase C  分析 + paper writing（2026-05-07 完成主体）
    [x] C.1  paper 5 figure 重画完毕（FIG-1/2/3/4a/4b 全部从 _phase_b_aggregate.csv 重生成）
    [x] C.2  hop-decay 数字进 master scorecard Hop₁ 列；曲线图作为 supplementary
    [x] C.3  §5 含 Shard Protection 解读 + §5.2 alignment subsection
    [x] C.4  abstract / §5 / appendix 共 57 个 \interim{} 全部填实数（V-2026-05-07-02）
    [x] C.5  §5 master scorecard `Table~\ref{tab:benchmark}`：12 行（6 method × 2 backbone）× 6 metric (ΔF_arch, Best attack, Sig/5, Gap, Hop₁, AUC) + Verdict
    [ ] C.5b 加 "Noise (k=5)" 列到 master scorecard——需先补 4 个缺数据 cell（GraphRevoker × {GCN,GAT}, IDEA/MEGU × GCN）
        Generator: `experiments/baseline_k5/fill_missing_cora.py`（idempotent，~15 min on 4090）
        缺因：k=5 batch 在 2026-05-05 GraphRevoker dispatcher fix 之前生成；IDEA/MEGU 当时只跑 GAT
    [ ] C.6  *(低优先级 / 提交后)* surrogate transferability sanity — cora/GCN/GNNDelete/TracIn，shadow=独立训的 GCN（5 seed），单 cell ~2h 4090。验证 §3.1 access spectrum 的 L2-direct → L2-surrogate 上界论述；若 transferability ≥60% 则把 §6.3 L4 升级为"surrogate 攻击力 ≈ direct × 0.X"
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

## 3. 关键已知问题（截至 2026-05-06）

### 3.1 ✅ MIA AUC = 0.000 bug（Phase A.1-A.3）— 已修复

> Note (2026-05-07): paper-side metric 现命名为 **update-detection AUC**（首次出现可写 "posterior-shift deletion-membership audit"，详见 `METRICS_CATALOG §2`）。本节标题与 code field `mia_auc` / log 中 "MIA AUC" / sanity-check 命令保留 legacy 命名以便溯源。

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

**衍生事实（2026-05-07，`fix/im-celf-shared-cache` 落地后）**：
IM full-CELF 在 arxiv 上**每 (dataset, IM hyperparams) 配置只需实算一次**。
新增的 `results/score_cache/im_celf/` cache key 不含 `unlearning_methods` 也不含 GU 训练 seed（仅依赖 graph_fingerprint + IM hyperparams + `im_selector_seed`，后者默认 2024 固定）。所以：

- B.2 全矩阵 6 method × 3 GU seed × IM strategy = **18 cell 共享 1 份 cache**
- B.2 全矩阵 6 method × 3 GU seed × Hybrid strategy 的 IM 分支同样命中（Hybrid 用 `compute_initial_marginal_gains` 已经跨方法共享，新 cache 进一步覆盖 full CELF）
- IM 不依赖 GNN 模型，**整条 select_nodes 路径 0 GPU 操作** → 可在 CPU-only 实例（autodl 32 核 ~¥0.5-1/h）跑出 cache 后传到 GPU 实例
- `_estimate_spread_numba_parallel`（numba.prange + per-round buffer）在 32 核 CPU 上 ~25-30× 加速；arxiv k=6773 串行预估 2-4h，并行 ~5-10 min

**等价性测试**：`scripts/test_im_celf_cache_equivalence.py` 在 cora 上 4 项验证 PASS（serial vs parallel bit-identical、cache MISS→SAVE→HIT 闭环、改 method+GU seed 仍命中同一 key）。

**paper §method 措辞建议**：
> "IM seed selection is computed once per (dataset, IM hyperparams) configuration and reused across unlearning methods and GU training seeds. This is methodologically clean because CELF only depends on graph topology and IM hyperparams (propagation probability, MC rounds, candidate pruning fraction); it has no dependence on the unlearning algorithm or its training seed. We fix `im_selector_seed=2024` to decouple from GU seeds (Sec A.4)."

### 3.3.1 arxiv unlearn_ratio 取值 tradeoff（pending decision，2026-05-07）

| 项 | 5%（当前 yaml）| **1%（候选）** | 0.5% |
|---|---|---|---|
| k（arxiv train=135K）| 6,773 | **1,355** | 677 |
| CELF 轮数（batch=5）| 1,355 | 271 | 135 |
| 单核 numba 估时 | 2-4 h | **10-15 min** | ~3 min |
| 32-core prange 估时 | 5-10 min | **~30 s** | <10 s |
| CELF lazy upper-bound 有效性 | 弱（k 大 → submod gap 小 → heap top 反复 stale → 退化成 plain greedy）| **强（标准 CELF 工作区间）** | 强 |
| 真实 deletion budget 量级 | 半个 retrain，不真实 | **千级 bulk deletion，符合 GDPR/CCPA 量级** | 单数百，常见 |
| IM 文献 benchmark k 范围 | 异常值（>>200）| 落在常见范围（10-2K）| 落在常见范围 |
| 跨 strategy 区分度 | 差（k 大 → random 也能让模型崩）| **好** | 好 |
| **batch_size hack 是否必要** | 必要（否则 1355 轮 × 严格 validate 太慢） | **不必要 → 可回 batch=1 classic CELF** | 不必要 |

**诚实 caveat（用户 2026-05-07 提的）**：
> "对于 IM 的 score 没有区别"。换句话说，5% → 1% 是**纯粹的 budget 缩减**，不是"更聪明的 IM"。每个候选节点的 marginal-gain 序列没变，只是截断点变早。**这只是工程加速 + threat-model 对齐，不是算法改进**。paper 里不应该 claim "我们提出的更好的 IM 变体"——而是 "我们在 arxiv 上选择更现实的 budget 量级"。

**如果决定切 1%**，对应改动是**最小化的**：
1. yaml 三处：`phase_b_arxiv_T1/T2/T3_seed*.yaml` + `phase_b_arxiv_tracin_smoke.yaml` + `phase_b_arxiv_feasibility.yaml` 把 `ratio: 0.05` → `ratio: 0.01`
2. yaml 同时把 `im_batch_size: 5` → `im_batch_size: 1`（回 classic CELF，无 approximation 包袱）
3. paper §method 加一句 cross-dataset ratio 解释（不是问题，是设计选择）
4. cora 全部不动（cora 5% = 7 nodes，CELF 飞快）

**衍生收益**：
- IM CPU prewarm 时间：~30 s（32 核）vs 5-10 min @ 5%
- T1 总耗：~9-10 h vs ~10-11 h @ 5%
- paper 方法学不再需要 "approximate batch-CELF" caveat

**不切的话**：3 个 fix 已经让 5% 在 deadline 内可行（IM 1 次 2-4h × 18 cell 摊销 + parallel 32 核砍到 5-10 min），**工程上 5% 不再是阻塞**，但 lazy-greedy 退化的方法学包袱还在。

**决策状态**：等用户确认。决定后改动只在 yaml 层（3-5 个文件），不动代码。

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

### 3.6 ✅ Phase B 污染 bug 集（RESOLVED 2026-05-06，commits `66a90f8` + `13f1e89` + `ddb7109` + 第 9 条 pending commit）

5 条第一轮 + 3 条二次 audit + 1 条 B.1 arxiv 实跑发现 = 9 条 attack pipeline 正确性问题，都在 `fix/blocker-1-train-before-select` branch 上修完。**Phase B 既有所有 attack.json/collateral.json 数据全部判定为不可信**，用户已清盘 `results/runs/` + 三个 cache 目录，下一次 B.0 sanity 是第一次干净数据。详见 V-2026-05-06-01 / V-2026-05-06-02 / V-2026-05-06-03。

| Bug | 影响 | 状态 |
|---|---|---|
| **demo_attack 剥离 sys.argv 后 config.py 烘出默认 cora/0.1 路径** — `_inject_unlearn_nodes` 写到正确 (arxiv/0.05) 路径，但 SGU/GIF/GNNDelete/GUIDE/CGU/IDEA 通过 `from config import unlearning_path` 读到错误 (cora/0.1) 路径，可能静默 unlearn 来自旧 cora 文件的节点 ID | ✅ demo_attack.py 把 shared args 回注 sys.argv；pipeline_adapter 加 `assert path == config.unlearning_path + run_id` 兜底 |
| **Random/Degree/PageRank baseline 不限 train_mask** — `data.num_nodes` 全图 topk，TracIn/IM/Hybrid 只取 train。Baselines 不是 budget-matched random，"TracIn beats random" 比较污染 | ✅ `BaseStrategy.candidate_nodes` helper（train_mask → train_indices → arange fallback）三策略全用 |
| **TracIn / Hybrid 在 random-init 模型上算梯度** — `AttackPipeline._setup` 只构造 model_zoo（随机初始化），训练在 `method.run_exp()` 里发生，时序晚于 `strategy.select_nodes`。pre-fix 的 IF 分数实际是结构-特征-范数代理，不是训练影响力 | ✅ `BaseStrategy.requires_trained_model` 标志位；`AttackPipeline._ensure_base_model_trained()` 用 `train_only=True` 训完 + state_dict snapshot；`run_with_strategy` hook 在 select_nodes 前调用；ScoreCache 和 SelectionCache 都加 `cache_schema: "v2"` 自动作废旧 entry |
| **eval_collateral.py 缺 seed_everything** — retrain 不可复现；`predictions.npz::logits_retrained` 同 seed 跑两次得到不同 logits | ✅ 加 `_seed_everything(seed_value)` 在 args sync 之后调 |
| **demo_attack 没同步 `proportion_unlearned_nodes`** — 默认 0.1 vs `unlearn_ratio` 0.05，导致 GIF_logger_name / df_size 计算 / cache key 在 demo_attack 与 eval_collateral 之间不一致 | ✅ 在 args dict 和 sys.argv 注入两处都同步 |
| **SelectionCache 对 Hybrid/TracIn 漏 hyperparam** — `_strategy_params_for_cache` 对它俩 fallthrough 到 `{}`，`fingerprint = sha256("{}")` 常数；两次 hybrid 实验只差 alpha/candidate_fraction/fusion_method/loss_type 时 cache key 完全相同，第二次 HIT 拿到第一次的 selected_nodes，`strategy.select_nodes` 根本不执行 | ✅ ddb7109：加 tracin/hybrid 分支返回完整 hyperparam dict |
| **ResultCache CACHE_KEY_FIELDS 漏架构/loss 系数** — 缺 gcn_num_layers/gcn_hidden（arxiv 3/256 vs cora 2/64 同 base_model 时碰撞）、alpha（GNNDelete/CGU loss 系数直接进 f1_after）、hybrid_alpha | ✅ ddb7109：加 4 个字段 |
| **跨 strategy 训练状态污染** — `compare_strategies` 内所有 strategy 共享 `model_zoo.model`；第 1 个 strategy 跑完后是 post-unlearn 状态，第 2 个 strategy 的 `train_original_model` 在污染权重上 fine-tune；cell 内 strategy 顺序影响 f1_after | ✅ ddb7109：`_setup` snapshot random_init state_dict；新增 `_restore_random_init`；hook 在 `_ensure_base_model_trained` 训练前 + `_run_unlearning_with_selected_nodes::method.run_exp()` 前 |
| **失败 unlearning 结果写入 ResultCache 污染下次 hit + cache-skip 引发 detection chain 失效** — `pipeline_adapter.run_with_selected_nodes` except 块 swallow 异常后伪造 `f1_before=None, f1_after=0.0` 但无 failure flag；`attack_manager` 无脑 `cache.save`；下次 run 立即 cache hit 返回坏结果，unlearning 根本没重跑（B.1 arxiv GNNDelete 实测：cache key `f29ac5e85baed066` 存了 `f1_drop=NA`）。**关键陷阱 1**：不能用 `f1_before is None` 当 failure 指标，正常 GraphEraser 路径也会 `f1_before=None`。**关键陷阱 2**：单纯阻止失败 cache 写会破坏既有 detection chain——eval_collateral 原本靠 cache hit 拿 selected_nodes 后重跑 run_exp 复现 crash → rc≠0 → run.py 报 failed_collateral，cache 没了反而 SKIP 走过场写假 _meta.json | ✅ 多层防御：(1) pipeline_adapter except 块 `failed=True/failure_reason=...`；(2) AttackResult 加 `failed`+`failure_reason` 字段（带 default 兼容旧 JSON），`to_dict` 序列化进 attack.json；(3) attack_manager 失败时 skip cache.save 但仍构造 AttackResult；(4) demo_attack 末尾扫 `comparison.results`，发现 `failed=True` → `sys.exit(1)`；(5) eval_collateral runner mode (`_output_dir`) 下 cache miss → `sys.exit(1)` 兜底。**三层 cache 在 unlearning 失败时**：ScoreCache + SelectionCache 保留（昂贵 selection 不白做），ResultCache skip（避免污染）。已有脏 entry 需手动 rm |

**附带修复**：
- HybridStrategy 之前绕过 `compute_im_celf` 直接调 `compute_initial_marginal_gains`，不应用 `candidate_fraction` pruning → 改为对 IF/IM 共享候选集统一 prune
- `--alpha` 字段同时是 GNNDelete/CGU loss alpha 和 Hybrid fusion ω → 加 `--hybrid_alpha`，向后兼容 fallback 到 `alpha`

**对既有数据的影响**：
- 所有 `results/runs/**/attack.json` 中 TracIn/Hybrid cell：测的是 random-init 代理，**叙事不能写"IF-guided"**，需重跑
- 所有 `results/runs/**/attack.json` 中 random/degree/pagerank cell：选点跨 train_mask，预算未匹配，需重跑
- 所有 `results/runs/**/collateral.json` 的 retrain_gap：单次有效但跨 seed 不可复现
- IM-only / k=5 noise floor / 旧 `results/baseline/k5_random/`：**不受影响**

**重跑策略**：B.0 sanity → 用 v2 binary 重跑全 B.1（cora 6 method × 6 strategy × 5 seed ≈ 180 cell, ~1.5h cora 4090；arxiv 子集后做）。

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
3. **B.2-T1** B.1 全 pass → `python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml` —— 12 cells / ~7-8h（必跑，arxiv 列 n=1 骨架）
3a. **B.2-T2 / T3** deadline 富余则串：T2 (`phase_b_arxiv_T2_seed212.yaml`) → T3 (`phase_b_arxiv_T3_seed722.yaml`)，各 ~7-8h（不复用 T1 的 IF cache，per-seed 全价）。一键串见 SERVER_RUNBOOK §3.4.4 / §A.3
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
> Note (2026-05-07): "MIA AUC" 是 legacy 名，paper 现称 **update-detection AUC**（详见 `METRICS_CATALOG §2`）；historical bug 名保留以匹配旧 log/JSON。

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
