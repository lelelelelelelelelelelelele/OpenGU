# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GULib is a research framework built on top of **OpenGU** (Open Graph Unlearning) for studying adversarial attacks on Graph Neural Network (GNN) unlearning methods. It evaluates how approximate unlearning algorithms can be exploited by strategically selecting nodes/edges for forced unlearning that cause performance collapse.

The framework integrates 16 GU algorithms, 37 datasets, and 13+ GNN backbones via PyTorch Geometric.

## ⚡ Start Here: Live Dashboard

**Single source of truth for current experiment state, bugs, and findings:** `self/dashboard/`

| File | Read when |
|------|-----------|
| `self/dashboard/EXPERIMENT_DASHBOARD.md` | Beginning every session — phase progress, coverage matrix, known issues, TODO |
| `self/dashboard/METRICS_CATALOG.md` | Working with metrics (F1, MIA, Retrain Gap, Collateral, Hop-decay) |
| `self/dashboard/METRIC_FIELD_SEMANTICS.md` | Before using `f1_before`, `perf_before`, or `logits_before` |
| `self/dashboard/VALIDATION_LOG.md` | Need empirical evidence for a claim (append-only) |
| `self/dashboard/CLAUDE.md` | First time entering the folder — rules & maintenance |

**NEVER duplicate dashboard content into other docs.** Always link to the path. This avoids drift.

**Cache directories also have CLAUDE.md** — read before touching:
- `results/cache/CLAUDE.md` — hash-named ResultCache, do NOT rename
- `results/selection_cache/CLAUDE.md` — hash-named SelectionCache, cross-method shared
- `results/experiments/CLAUDE.md` — MG-0/1/2/3/p2/im_v4 子目录的真正含义对应表

## Running Experiments

```bash
# Basic experiment (from GULib-master directory)
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Memory profiling mode
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GIF --cal_mem True

# Key arguments (see parameter_parser.py for all 300+ options):
#   --dataset_name: cora, citeseer, pubmed, CS, Physics, flickr, Photo, Computers, ogbn-arxiv, ...
#   --base_model: GCN, GAT, GIN, SAGE, SGC, S2GC, SIGN, Cheb, APPNP, GCN2, GATv2, TAG, LightGCN, ...
#   --unlearning_methods: GraphEraser, GIF, GNNDelete, CEU, CGU, SGU, GST, Projector, MEGU, UTU, GUKD, D2DGN, IDEA, ScaleGUN, GraphRevoker
#   --unlearn_task: node, edge, feature
#   --downstream_task: node, edge
#   --is_transductive: True/False
#   --is_balanced: True/False
# Phase B canonical runner (yaml-driven; supersedes the legacy run_mg*.sh scripts removed 2026-05-06)
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
H:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/cora_GCN_r0.05    # pass/fail check
```

No formal test suite exists. Validation is experiment-driven; results are logged to `log/{method}/{dataset}/{model}/`.

## Architecture

### Execution Flow

`main.py` → `parameter_parser()` → `original_dataset.load_data()` → `process_data()` → `model_zoo()` → `UnlearningManager.get_method()` → `method.run_exp()`

### Key Routing Patterns

**UnlearningManager** (`unlearning_manager.py`): Maps `--unlearning_methods` string to the corresponding method class via `method_map` dict. Each method class implements `run_exp()` and `run_exp_mem()`.

**model_zoo** (`model/model_zoo.py`): Factory that instantiates the GNN backbone from `--base_model`. Special-cases CEU and Projector models. Loads hyperparameters from YAML files in `model/properties/`.

**Trainer routing** (`task/__init__.py`): Maps `args["unlearn_trainer"]` to task-specific trainer classes (GUIDETrainer, GIFTrainer, etc.) via `trainer_mapping` dict and `get_trainer()`.

### Pipeline Hierarchy

Three abstract pipeline base classes in `pipeline/`:
- **Shard_based_pipeline**: For partition-then-aggregate methods (GraphEraser, GraphRevoker)
- **IF_based_pipeline**: For influence-function-based methods (GIF, GST)
- **Shard_based_pipeline**: For graph-partitioning methods (GraphEraser, GUIDE, GraphRevoker)
- **Learning_based_pipeline**: For learned unlearning strategies

Each unlearning method in `unlearning/unlearning_methods/{Method}/` inherits from one of these pipelines.

### Configuration

`config.py` dynamically constructs all data/model/log paths from parsed arguments. It is imported at module level and runs `parameter_parser()` on import — this means CLI args must be present whenever config.py is loaded.

### Data Flow

1. Raw datasets auto-download via PyTorch Geometric to `data/raw/`
2. `dataset/original_dataset.py` loads and returns `(data, dataset)` objects
3. `utils/dataset_utils.py::process_data()` handles train/test splitting (transductive/inductive, balanced/imbalanced) and caches splits to `data/processed/`
4. Unlearning target nodes/edges are stored under `data/unlearning_task/{transductive|inductive}/{balanced|imbalanced}/`
5. Method-specific processed data goes to `data/{MethodName}/`

### Attack Framework

`attack/` contains Membership Inference Attack (MIA) implementations:
- `MIA_attack.py`: Shadow model training and attack model infrastructure
- `Attack_methods/`: Method-specific attack classes (GraphEraser_MIA, GUIDE_MIA, GNNDelete_MIA, CEU_MIA)

## Dependencies

Core stack: PyTorch + PyTorch Geometric 2.6.1 + torch_scatter + torch_sparse. See `../requirements.txt` for pinned versions. Additional: ogb, deeprobust, cvxpy, scikit-learn.

### Environment

Use the **conda `gnn` environment** for all Python operations.

**In Claude Code's Bash tool, always use the full Python path** — `conda activate` does NOT work in non-interactive shells (git bash does not source conda's init script):

```bash
# CORRECT: use full path directly
H:/conda_package/envs/gnn/python.exe main.py ...
H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py
H:/conda_package/envs/gnn/python.exe demo_attack.py ...

# WRONG: conda not available in non-interactive bash
conda activate gnn && python main.py  # ❌ conda: command not found
```

The `gnn` environment contains all required dependencies (PyTorch, PyG, pytest, etc.).

## Important Notes

- **Never use `--no_cache`** unless explicitly testing cache behavior itself. This flag disables both result cache AND selection cache, causing IM strategy to re-run for ~500s each time instead of using cached selections (sub-second).
- `config.py` executes `parameter_parser()` at import time, so importing it outside of a CLI context (e.g., in a notebook) will fail or use defaults
- ScaleGUN is currently commented out in `unlearning_manager.py`
- GraphRevoker reuses the `grapheraser` class in the method map
- Seed is hardcoded to 2024 in `main.py::seed_everything()`
- Logs are timestamped and organized at `log/{method}/{dataset}/{model}/`
- Bug 修复后数据刷新：Phase B 没有"修补"流程，重跑 `experiments/run.py <yaml>` 即可（旧的 HOWTO_REPAIR_CORRUPTED_RESULTS.md 描述的是 pre-Phase-B 流程，已删除 2026-05-06）

### ⚠ Active Bugs / Status (2026-05-05)

Detailed: `self/dashboard/EXPERIMENT_DASHBOARD.md §3` + `self/limitations.md` (paper §5 candidates).

- **arxiv collateral retrain OOM on 24GB GPU**: peak memory ~22 GB, 4090 边缘 OOM。3/5 B.1 cell（GIF/GNNDelete/IDEA random）缺 collateral.json，待 H800 80GB 上 5 min 补完。详见 `self/limitations.md` 隐含在 L2.
- **TracIn G-matrix on arxiv = ~68 GB**: 必须 ≥80GB GPU（H800/A100 80GB）。L2 in `self/limitations.md`. Forward-once optimization (commit `6b7285b`) keeps memory the same, only halves time.
- **IM CELF default params on arxiv = intractable**: yaml 默认未带 `candidate_fraction=0.1, mc_rounds=50` 时 step-1 要 9M MC BFS，10h+ 不出结果。修复后 ~3 min。L3 in limitations.md.
- **GraphEraser LPA partition on arxiv slow but feasible**: 10 min/iter，但 `terminate_delta=0` 早停在 1-2 iter ≈ 10 min total。L1 (downgraded to ACCEPTED).
- **MIA CPU-bound**: GraphEraser MIA 6 min × 2 rounds (positive + negative samples) per cell。GPU 这段 idle。L5.

Resolved (2026-05-05):
- IM_v4 selector instability — fixed, `im_selector_seed=2024` 固定，`attack_manager.py:_build_selection_config` 锚到 selector seed 而非训练 seed (commit `af1c8ba`)。
- B.1 yaml 误把 selection 测试塞进 GU 稳定性测试 — 回滚到 random-only (commit `6b7285b`)。L4.
- MIA AUC = 0.000 修复（earlier commits）— 现在 GIF/GNNDelete/MEGU/IDEA/GraphEraser 都返非零 AUC。

### Phase B 工具集（2026-05-05 添加）

| 脚本 | 用途 |
|---|---|
| `scripts/feasibility_selection_only.py` | 探针：`--candidate_subset_size N` 限流测内存/时间；ScoreCache 强制关闭，避免污染正式 TracIn/Hybrid cache |
| `scripts/prewarm_selection_cache.py` | 批量算 selection 写 cache；TracIn/Hybrid 必须用 GIF/GNNDelete canonical selector path，shard/SISA method 会 fail fast |
| `scripts/gate_runs.py` | 自动 pass/fail 判 yaml 矩阵：4 文件 + mia_auc + f1 范围 |
| `scripts/diag_b1.sh` | 一键看 cell 输出列表 + log 错误尾（不在 git，需 cat 创建） |
| `scripts/redo_collateral.sh` | 补 OOM 失败的 collateral cell（不在 git，需 cat 创建） |
| `experiments/run.py` | 主 runner：吃 yaml，展开 (method,strategy,seed) 矩阵跑 demo_attack + eval_collateral |
| `SERVER_RUNBOOK.md` | 双机执行手册（4090 cora + H800 arxiv） |
| `self/attack_flow.md` | 一个 cell 时序拆解 + CPU/GPU 占用图 |
| `self/limitations.md` | paper §5 candidates：实测瓶颈 + decision status |

## Project Context (Attack Research)

This project is developing **adversarial attacks on GNN unlearning**. The core idea: strategically select nodes for forced unlearning to cause performance collapse in approximate unlearning algorithms. See `self/` directory for detailed context:

- **`self/dashboard/`**: live state — start here every session
- **`self/limitations.md`**: 实测瓶颈 + paper §5 candidates（2026-05-05 新增，每条带 evidence + decision status）
- **`self/attack_flow.md`**: 一个 cell 时序图 + CPU/GPU 占用（2026-05-05 新增，调试卡死位置必看）
- `self/thesis_transition_memo.md`: thesis 战略层 + 4-day NeurIPS execution plan
- `self/PROJECT_MASTER_CONTEXT.md`: Research background, hypothesis, methodology (frozen background)
- `self/plan_flow_v2_delta.md`: 方法学/指标设计原典
- `self/宏观plan.md`: Experiment plan, code modules to build, priority ordering
- `self/flow.md`: Function-level design, input/output specs, test cases

### Attack Module Structure

```
attack/attack_strategies/       # Node selection strategies
  base_strategy.py              # ABC: select_nodes(data, model, k) -> Tensor
  random_strategy.py            # Baseline
  degree_strategy.py            # Baseline
  pagerank_strategy.py          # Baseline
  tracin_strategy.py            # Core: pseudo-IF
  im_strategy.py                # Core: Influence Maximization (CELF)
  hybrid_strategy.py            # Core: IF-IM fusion
attack/attack_manager.py        # Strategy dispatcher
attack/attack_eval.py           # F1 drop, MIA AUC, retrain gap, collateral damage
attack/pipeline_adapter.py      # AttackPipeline: wraps OpenGU pipelines for attack use
                                #   - _inject_unlearn_nodes(): write node files
                                #   - run_retrain(): exact retrain-from-scratch
                                #   - _get_trained_model(): extract model from pipeline
attack/result_cache.py          # ResultCache: disk-backed caching of pipeline results
attack/selection_cache.py       # SelectionCache: strategy-agnostic node selection caching
attack/attack_result.py         # AttackResult dataclass for structured results
eval_collateral.py              # CLI script: runs retrain gap + collateral damage eval
                                #   Usage: python eval_collateral.py --method GNNDelete --strategy tracin
experiments/baseline_k5/eval_relative.py # CLI script: compute metrics relative to random baseline
```

The three pipeline base classes (`Shard_based_pipeline`, `IF_based_pipeline`, `Learning_based_pipeline`) support a `train_only` flag (`args["train_only"] = True`) that skips the unlearning phase and returns only the trained model — used by `AttackPipeline.run_retrain()` for exact retrain-from-scratch.

### Result Storage Convention

**Phase B onwards (canonical layout, 2026-05-04+)**: every cell writes to
```
results/runs/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{N}/
  attack.json           # F1 drop, MIA AUC, selected_nodes (L3)
  collateral.json       # retrain gap, prediction shift, hop-decay (L3)
  predictions.npz       # logits_{before, unlearned, retrained} (L2)
  _meta.json            # config + git_sha + timestamp (audit)
```
Driven by `experiments/run.py <yaml>`; configs in `experiments/configs/`.
See `experiments/configs/README.md` for the 3-layer artifact decoupling.

**Two distinct baselines — do not confuse**:

| Baseline | Where | Generated by | What it measures |
|----------|-------|-------------|------------------|
| **k=5 noise floor** | `results/baseline/k5_random/{method}/{dataset}/{model}/baseline_seed*_k5.json` | `experiments/baseline_k5/generate_baseline.py` (`--baseline_k 5`) | F1 shift from deleting **5 random nodes** — i.e., the inherent jiggle the unlearning method introduces with negligible deletion. **Not a budget-matched baseline.** |
| **Budget-matched random** (Phase B) | `results/runs/{cell}/{method}_random/seed*/attack.json` | `experiments/run.py` (random is one strategy in the matrix) | F1 drop from deleting **r·\|V_train\| random nodes** at the same budget as the attack. Used for **paired** effect = Δ vs same-seed random. |

These are **complementary, not redundant**. Phase B's random can power
paired t-tests for "did the attack beat random at the same budget?"; k=5
is the method-level noise floor used as a reference line in figures or to
subtract a method's intrinsic shift before comparing across families.
`results/baseline/` is retained even after the 2026-05-05 untrack pass.

**Other persistent paths**:
- `results/evaluation/stats/`: paper-input CSV (`final_paper_stats.csv`, generated by `scripts/evaluation/final_data_aggregator.py`)
- `results/paper_figures/`: 5 figure PDFs/PNGs for paper
- `results/_journal/auto_report.md`: append-only research journal
- `results/cache/`, `results/selection_cache/`: hash-named caches (per-dir CLAUDE.md; only the .md is tracked)

**Untracked since 2026-05-05** (~1300 files of pre-Phase-B bug-polluted data; `.gitignore`'d, Phase B regenerates clean): `results/relative/`, `results/experiments/`, `results/collateral/`, `results/step0_validation/`, `results/runs/` (only output dir, ignored), `results/_deprecated_tracin_bug/`. Historical mapping table preserved at `self/dashboard/EXPERIMENT_DASHBOARD.md §7`.

### Document Workflow

Research journal: `results/_journal/auto_report.md` (append-only, governed by `RULES.md` v2)
- Experiment entries: auto-appended by `scripts.evaluation.reporting.writer` after each run
- Decision entries: manually appended when making strategic choices (see RULES.md v2)
- Session separators: added at start of each Claude Code session

Daily summaries: `report/daily-log/YYYY-MM-DD_log.md` (generated via `/daily-log`)

### Slash Commands

- `/review [方案或结论]`: Invoke a strict NeurIPS/ICML reviewer persona for critical analysis
- `/run-exp [参数]`: Run an attack experiment with standardized reporting
- `/analyze [条件]`: Compare results across strategies/datasets/methods
