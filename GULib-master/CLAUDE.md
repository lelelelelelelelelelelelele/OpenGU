# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GULib is a research framework built on top of **OpenGU** (Open Graph Unlearning) for studying adversarial attacks on Graph Neural Network (GNN) unlearning methods. It evaluates how approximate unlearning algorithms can be exploited by strategically selecting nodes/edges for forced unlearning that cause performance collapse.

The framework integrates 16 GU algorithms, 37 datasets, and 13+ GNN backbones via PyTorch Geometric.

## Running Experiments

```bash
# Basic experiment (from GULib-master directory)
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Memory profiling mode
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GIF --cal_mem True

# Key arguments (see parameter_parser.py for all 300+ options):
#   --dataset_name: cora, citeseer, pubmed, CS, Physics, flickr, Photo, Computers, ogbn-arxiv, ...
#   --base_model: GCN, GAT, GIN, SAGE, SGC, S2GC, SIGN, Cheb, APPNP, GCN2, GATv2, TAG, LightGCN, ...
#   --unlearning_methods: GraphEraser, GIF, GUIDE, GNNDelete, CEU, CGU, SGU, GST, Projector, MEGU, UTU, GUKD, D2DGN, IDEA, ScaleGUN, GraphRevoker
#   --unlearn_task: node, edge, feature
#   --downstream_task: node, edge
#   --is_transductive: True/False
#   --is_balanced: True/False
#   --unlearn_ratio: fraction of nodes/edges to unlearn
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
- **IF_based_pipeline**: For influence-function-based methods (GIF, GST, GUIDE)
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

Use the **conda `gnn` environment** for all Python operations:

```bash
# Activate before running any Python commands
conda activate gnn

# Or specify full path if needed
H:\conda_package\envs\gnn\python.exe main.py ...
```

The `gnn` environment contains all required dependencies (PyTorch, PyG, pytest, etc.).

## Important Notes

- `config.py` executes `parameter_parser()` at import time, so importing it outside of a CLI context (e.g., in a notebook) will fail or use defaults
- ScaleGUN is currently commented out in `unlearning_manager.py`
- GraphRevoker reuses the `grapheraser` class in the method map
- Seed is hardcoded to 2024 in `main.py::seed_everything()`
- Logs are timestamped and organized at `log/{method}/{dataset}/{model}/`

## Project Context (Attack Research)

This project is developing **adversarial attacks on GNN unlearning**. The core idea: strategically select nodes for forced unlearning to cause performance collapse in approximate unlearning algorithms. See `self/` directory for detailed context:

- `self/PROJECT_MASTER_CONTEXT.md`: Research background, hypothesis, methodology
- `self/宏观plan.md`: Experiment plan, code modules to build, priority ordering
- `self/flow.md`: Function-level design, input/output specs, test cases

### Attack Module Structure (Under Development)

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
attack/attack_eval.py           # F1 drop, MIA AUC, retrain gap
```

### Result Storage Convention

Experiment results go to `results/{attack_strategy}/{unlearning_method}/{dataset}/{model}/run_{timestamp}.json`. Each JSON contains `config` (parameters), `metrics` (F1 drop, MIA AUC, timing), and `selected_nodes`. The original framework logs remain at `log/`.

### Document Workflow

Research journal: `results/_journal/auto_report.md` (append-only, governed by `RULES.md` v2)
- Experiment entries: auto-appended by `report_writer.py` after each run
- Decision entries: manually appended when making strategic choices (see RULES.md v2)
- Session separators: added at start of each Claude Code session

Daily summaries: `daily_log/YYYY-MM-DD_log.md` (generated via `/daily-log`)

### Slash Commands

- `/review [方案或结论]`: Invoke a strict NeurIPS/ICML reviewer persona for critical analysis
- `/run-exp [参数]`: Run an attack experiment with standardized reporting
- `/analyze [条件]`: Compare results across strategies/datasets/methods
