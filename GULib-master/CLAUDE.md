# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GULib is a research framework built on top of **OpenGU** (Open Graph Unlearning) for studying adversarial attacks on Graph Neural Network (GNN) unlearning methods. It evaluates how approximate unlearning algorithms can be exploited by strategically selecting nodes/edges for forced unlearning that cause performance collapse.

The framework integrates 16 GU algorithms, 37 datasets, and 13+ GNN backbones via PyTorch Geometric.

## ⚡ Start Here: Live Dashboard

**Single source of truth for current experiment state, bugs, and findings:** `self/dashboard/`

| File | Read when |
|------|-----------|
| `self/dashboard/WORKPLAN.md` | **Beginning every session (2026-06-27+)** — single operational hub: state snapshot + 硬伤 C1–C5 + 实验/ablation/写作/画图 four-stage task plan + link index. Generates `progress.html`. (Supersedes `PROGRESS.md`, now a redirect pointer.) |
| `self/dashboard/progress.html` | Visual kanban of WORKPLAN.md (derived snapshot — never hand-edit; regen via `scripts/dashboard/refresh.py`) |
| `self/dashboard/EXPERIMENT_DASHBOARD.md` | ⚠️ FROZEN 2026-05-07 — historical coverage matrix + bug archive only (Phase B "[ ]" is long done) |
| `self/dashboard/METRICS_CATALOG.md` | Working with metrics (F1, MIA, Retrain Gap, Collateral, Hop-decay) |
| `self/dashboard/METRIC_FIELD_SEMANTICS.md` | Before using `f1_before`, `perf_before`, or `logits_before` |
| `self/dashboard/VALIDATION_LOG.md` | Need empirical evidence for a claim (append-only) |
| `self/dashboard/PAPER_LIABILITIES_MAP.md` | Mapping paper 硬伤 L1–L9 → overleaf 行号 (when editing the paper to close a caveat) |
| `self/dashboard/CLAUDE.md` | First time entering the folder — rules & maintenance |

**NEVER duplicate dashboard content into other docs.** Always link to the path. This avoids drift.

## Git Workflow

Repository Git rules are defined in `AGENTS.md` and explained with executable PowerShell examples in `docs/GIT_WORKFLOW.md`. Every coherent improvement starts from an explicit parent branch and is accepted back into that parent with `git merge --no-ff`; routine synchronization uses `git pull --ff-only`. Never infer the current working line from a dated sentence in this file—check `git branch --show-current` and `git worktree list`.

**Cache directories also have CLAUDE.md** — read before touching:
- `results/cache/CLAUDE.md` — hash-named ResultCache, do NOT rename
- `results/selection_cache/CLAUDE.md` — hash-named SelectionCache, cross-method shared
- `results/experiments/CLAUDE.md` — MG-0/1/2/3/p2/im_v4 子目录的真正含义对应表

## Running Experiments

### Formal Remote Execution Lane

- Feature/fix branches may run unit tests, integration tests, and explicitly non-formal smoke checks only. A formal MVP/one-cell gate is already part of the real experiment matrix and therefore runs only after the complete code line has been accepted into `main`.
- Pin every formal matrix to one exact full `main` SHA. If a formal gate finds a code defect, stop, fix it on a new branch, accept that fix into `main`, and restart the gate with the new SHA and result/cache identity; do not mix cells across SHAs.
- The default lane for formal GPU experiments is the **aligned, intentionally clean SSH active checkout**. A formal run does not require a separate worktree merely because it is formal.
- Use an isolated worktree only when there is a concrete boundary that requires it: concurrent branch work, unresolved tracked/operational contamination, validation of an unaccepted fix, or a demonstrated result/cache identity collision.
- Before claiming isolation is necessary, inspect `git status --short --branch`, `git worktree list`, and the canonical runner's `--dry_run` classification. Historical ignored results alone are not evidence of a collision when the fingerprinted runner reports the intended cells as `would_run`.
- Formality comes from accepted source/config provenance, complete four-file cell artifacts, gates, and recorded logs—not from the checkout directory. A one-cell gate run made with the same full config/fingerprint remains part of the formal matrix and is skipped, not overwritten, during expansion.
- Current experiment placement and any explicit exception are recorded in `self/dashboard/WORKPLAN.md`; do not infer an isolation requirement from an older acceptance report that happened to use a fresh checkout.

### Canonical Dataset Location on SSH

- The SSH authority is the active checkout
  `/autodl-fs/data/OpenGU/GULib-master`. Canonical dataset sources must resolve
  below that checkout, not below `OpenGU-shared`, another worktree, an
  experiment checkout, a backup, or an archive.
- Raw adapter caches live under `data/raw/<dataset>/`. Planetoid uses lowercase
  `data/raw/{cora,citeseer,pubmed}`; its nested PyG `processed/data.pt` remains
  part of the public/raw adapter cache.
- OpenGU canonical graph/split pairs live only under
  `data/processed/{transductive,inductive}/`. A public Planetoid `data.pt`
  must never be relabeled or copied as an OpenGU canonical split pickle.
- `data/<Method>/`, `data/unlearning_task/`, and result/cache trees are allowed
  generated artifacts, not alternative canonical dataset roots.
- Formal runs must use the active `root_path`/canonical `processed_root`, must
  not download or preprocess inside the timed run, and must record resolved
  path, content/split fingerprints, and Git provenance. Missing datasets are
  staged into active `data/raw/` and processed through the accepted OpenGU
  flow before the formal run starts.
- Existing duplicates are recovery evidence until separately approved for
  deletion. See `reports/dataset_layout_AUDIT_REPORT.md` for the hash audit and
  `self/dashboard/WORKPLAN.md` for the current availability snapshot.

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
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
E:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/cora_GCN_r0.05    # pass/fail check
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

1. Development loaders may download raw datasets to `data/raw/`; formal SSH
   runs require the canonical active raw cache to exist before timing begins
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
E:/conda_package/envs/gnn/python.exe main.py ...
E:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py
E:/conda_package/envs/gnn/python.exe demo_attack.py ...

# WRONG: conda not available in non-interactive bash
conda activate gnn && python main.py  # ❌ conda: command not found
```

The `gnn` environment contains all required dependencies (PyTorch, PyG, pytest, etc.).

## Important Notes

- **Never use `--no_cache`** unless explicitly testing cache behavior itself. This flag disables both result cache AND selection cache, causing IM strategy to re-run for ~500s each time instead of using cached selections (sub-second).
- `config.py` executes `parameter_parser()` at import time, so importing it outside of a CLI context (e.g., in a notebook) will fail or use defaults
- ScaleGUN is currently commented out in `unlearning_manager.py`
- GraphRevoker dispatches to its real `graphrevoker` class. The historical pre-2026-05-05 alias and the later single-shard collateral path are fixed; old affected results remain invalid. Current acceptance boundary: `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`.
- Seed is hardcoded to 2024 in `main.py::seed_everything()`
- Logs are timestamped and organized at `log/{method}/{dataset}/{model}/`
- Bug 修复后数据刷新：Phase B 没有"修补"流程，重跑 `experiments/run.py <yaml>` 即可（旧的 HOWTO_REPAIR_CORRUPTED_RESULTS.md 描述的是 pre-Phase-B 流程，已删除 2026-05-06）
- **改 GNN 架构维度必清方法目录**："架构"指 `gcn_hidden` / `gcn_num_layers` —— 这俩改了 state_dict tensor shape 会变。GNNDelete / UTU checkpoint 路径（`data/{Method}/checkpoint_node/{dataset}/{base_model}/original/{seed}/`）只带 dataset+base_model+seed，**不带架构维度**，所以 yaml 加 `model_overrides: {gcn_hidden: 256}` 或改 `--gcn_num_layers 3` 跟之前跑过的不一样时，必须先 `rm -rf data/GNNDelete/ data/UTU/`，否则旧 checkpoint 触发 state_dict 维度不匹配 RuntimeError（2026-05-06 B.1 GNNDelete crash 真实根因）。GraphEraser/GraphRevoker 文件名带 `partition_method/num_shards` 但同样不带架构，规则同。**不属于"改架构"、可以放心改的**：加新 method（每个 method 自己的 `data/<Method>/` 独立目录）、改 strategy / seed / dataset / base_model（路径已带）、改 lr / num_epochs / batch_size / unlearn_ratio / alpha / hybrid_alpha / fusion_method / candidate_fraction（不改 tensor shape，只影响数值）。ResultCache 的 `CACHE_KEY_FIELDS` 已包含 `gcn_hidden`/`gcn_num_layers`，所以 yaml override 后 cache 不会 collide，但**方法自己的磁盘 checkpoint 仍会**。

### ⚠ Status & Engineering Bottlenecks

**Current research status / 硬伤 C1–C5 → `self/dashboard/WORKPLAN.md` §0–§3** (single hub, 2026-06-27+). Do not read the dated list below for *current* state — it has drifted.

**Project phase (2026-06)**: NeurIPS paper **submitted, awaiting review** — this is the rebuttal-prep / 完善期, no longer a deadline crunch. thesis 锁死 = *systematic audit + extreme heterogeneity + Vulnerability Fingerprint* (reframe to "结构杠杆主轴" `565aaf6` is held for re-submission only). Active branch: `research/selection-concordance-2026-06-27`.

**Local GPU is dead — GPU experiments are remote-only**: this machine's RTX 5070 is sm_120 (Blackwell); the pinned torch 2.2.1+cu121 only ships kernels to sm_90, so every CUDA kernel crashes and rebuilding per requirements.txt does not fix it. **All GPU runs go to the AutoDL image `gnn_20`** (rentable on demand); local conda `gnn` (`E:/conda_package/envs/gnn/python.exe`) is **CPU/analysis only**. Do not mix new-stack and old-stack results in one matrix.

The engineering/hardware bottlenecks below (recorded 2026-05-05) are still accurate as scale/hardware facts; full list + decision status in `self/limitations.md` (L1–L8), historical bug archive in `EXPERIMENT_DASHBOARD.md §3`:

- **arxiv collateral retrain OOM on 24GB GPU**: peak memory ~22 GB, 4090 边缘 OOM。3/5 B.1 cell（GIF/GNNDelete/IDEA random）缺 collateral.json，待 ≥80GB GPU 上 5 min 补完。详见 `self/limitations.md` 隐含在 L2.
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
| `文档规划/10_实验矩阵/15_实验运行入口与脚本.md` | 当前 runner / yaml / dry-run / gate 入口；2026-05 deadline Runbook 已退休 |
| `self/attack_flow.md` | 一个 cell 时序拆解 + CPU/GPU 占用图 |
| `self/limitations.md` | paper §5 candidates：实测瓶颈 + decision status |

## Project Context (Attack Research)

This project is developing **adversarial attacks on GNN unlearning**. The core idea: strategically select nodes for forced unlearning to cause performance collapse in approximate unlearning algorithms. See `self/` directory for detailed context:

- **`self/dashboard/`**: live state — start here every session
- **`self/related_work/`**: citation library (`refs.bib` + `NOTES.md`) and **`concordance/`** — the selection-concordance study driving the current branch. Asks: do degree / PageRank / IM / TracIn / GIF select the *same* nodes? Jaccard@k across 6 datasets (training-free) + real GIF-vs-TracIn on a trained base GCN. Deliverable `concordance/report.html`; entry point `concordance/HANDOFF.md`. Findings: IM ≠ degree at the **set** level (most distinct on larger graphs), TracIn ⟂ degree & IM (set-level support for the volume-driven reading), and the cheap Hessian-free "proper TracIn" ≈ real GIF (0.65–0.74) while the deployed cross-TracIn is degenerate (~0.10–0.14).
- **`self/limitations.md`**: 实测瓶颈 + paper §5 candidates（每条带 evidence + decision status；L1–L8）
- **`self/attack_flow.md`**: 一个 cell 时序图 + CPU/GPU 占用（调试卡死位置必看）
- `self/thesis_transition_memo.md`: thesis 战略层（含早期 NeurIPS 执行计划，phase 现已是 submitted/rebuttal-prep）
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
- `results/_journal/archive/auto_report_*.md`: frozen v1/v2 journals; never append/rewrite
- `results/_journal/auto_report.events.jsonl`: append-only V3 machine event audit stream
- `results/_journal/auto_report_baseline.json`: curated legacy facts and invalidation boundaries (not run events)
- `results/_journal/auto_report.md` + `.html`: bounded, rebuildable current-state projection (not audit originals)
- `results/cache/`, `results/selection_cache/`: hash-named caches (per-dir CLAUDE.md; only the .md is tracked)

**Untracked since 2026-05-05** (~1300 files of pre-Phase-B bug-polluted data; `.gitignore`'d, Phase B regenerates clean): `results/relative/`, `results/experiments/`, `results/collateral/`, `results/step0_validation/`, `results/runs/` (only output dir, ignored), `results/_deprecated_tracin_bug/`. Historical mapping table preserved at `self/dashboard/EXPERIMENT_DASHBOARD.md §7`.

### Document Workflow

Research journal rules: `results/_journal/RULES.md` v3
- Historical v1/v2 Markdown is frozen under `archive/`; compatibility reading remains, while default legacy writing is retired.
- High-volume experiment progress is appended as structured V3 JSONL events with stable cell/run identity and stage/cache provenance.
- Human current status comes from the bounded Markdown/HTML projection, not from reading the entire append-only log.
- Decisions belong in durable design/validation docs or explicit V3 metadata, not fixed next-step prose in the generated view.

Daily summaries: `report/daily-log/YYYY-MM-DD_log.md` (generated via `/daily-log`)

### Slash Commands

- `/review [方案或结论]`: Invoke a strict NeurIPS/ICML reviewer persona for critical analysis
- `/run-exp [参数]`: Run an attack experiment with standardized reporting
- `/analyze [条件]`: Compare results across strategies/datasets/methods
