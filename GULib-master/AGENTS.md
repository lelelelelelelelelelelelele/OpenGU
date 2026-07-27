# Adversarial Attacks on Graph Unlearning — Agent Guide

> Working draft. This document is being reviewed section by section and does not replace `AGENTS.md` yet.

## 1. Project Positioning and Information Entry Points

This repository is a research project on adversarial attacks against graph unlearning. It extends GULib, OpenGU's graph-unlearning library, to study a core question: when an attacker strategically selects node, edge, or feature deletion requests, can approximate graph-unlearning methods exhibit abnormal utility degradation, approximation error, privacy, or prediction-behavior changes?

The framework connects OpenGU's data processing, model training, and graph-unlearning methods to attack-side deletion-target selection, attack execution, and post-hoc evaluation. Research compares random, topology-based, influence/gradient-based, and fused selection mechanisms across unlearning methods, datasets, models, and deletion budgets, and builds reviewable evidence from performance, retrain-gap, collateral, and update-detection diagnostics.

This repository is both a codebase and an experiment/evidence repository: source code and YAML define executable experiments; datasets and splits, cache identities, result artifacts, and reports support conclusions. Every experiment conclusion must be traceable to an explicit configuration, dataset and split, code version, and artifact evidence.

Current research framing, experiment design, and review thinking start at `文档规划/_文档地图.md`. Current tasks, priorities, and dependencies have one live source: `self/dashboard/WORKPLAN.md`.

Do not duplicate live dashboard state into other documents; link to its owning source instead. If provenance, dataset or split identity, cache or artifact identity, or metric semantics are ambiguous, fail closed: do not treat the result as trusted evidence.

## 2. Execution Locations

The local machine is for CPU analysis, targeted tests, and viewing verified results. Formal GPU experiments, formal datasets, and runtime cache/result state live in the SSH active checkout.

Devices share Git-tracked source and configuration. An experiment artifact becomes trusted evidence only after the required collection and verification flow; detailed SSH, synchronization, dataset, and cache rules are loaded on demand from their local `AGENTS.md` files.

## 3. Minimal Execution Pipeline

Experiment matrices are expanded by `experiments/run.py`; single runs enter through `main.py`:

`CLI / YAML`
→ `parameter_parser`, `config`
→ dataset loading and split
→ `model_zoo`
→ `UnlearningManager` and the selected method / pipeline
→ deletion-target selection, unlearning or retraining, and metric evaluation
→ reviewable artifacts and current state

`attack/` owns selection strategies, attack orchestration, and evaluation. `cache_v2/` owns versioned selection/score evidence contracts.

## 4. Critical Evidence Infrastructure

- `cache_v2/` stores exact, immutable Recipe/Artifact evidence. Dataset loading, split construction, candidate construction, and selection computation belong to the experiment layer; never rename, overwrite, repair, or delete a V2 Artifact by hand.
- AutoReport V3 writes append-only JSONL audit facts. Its Markdown and HTML files are rebuildable projections; change producers or generators, then rebuild, rather than hand-editing either evidence surface.
- When a repository generator owns a dashboard, report, aggregate, figure, or manifest, change its source or generator, then rebuild and validate; never hand-edit the derived output.

## 5. Runtime and Validation

Use the local machine for code changes, CPU analysis, targeted tests, and reviewing verified evidence. For local Python work, use `E:/conda_package/envs/gnn/python.exe`. `config.py` parses CLI arguments at import time; do not import it from lightweight tests or notebooks unless the CLI context is intentionally supplied. Run formal GPU experiments from the active SSH checkout; `experiments/AGENTS.md` owns the detailed rules for the remote environment, datasets, pinned SHAs, and formal gates. Before running or modifying an experiment matrix, read `文档规划/10_实验矩阵/15_实验运行入口与脚本.md`; the formal entry point is `experiments/run.py` with YAML configuration. Validate changes in proportion to their risk: run the smallest relevant tests for code, `--dry_run` for experiment configurations, and link plus generated-artifact checks for documentation.

## 6. Repository Map

```text
GULib-master/
├── Entry Points, Orchestration, and Validation
│   ├── main.py  config.py  parameter_parser.py  unlearning_manager.py
│   ├── experiments/
│   ├── scripts/
│   └── tests/
│
├── Graph Unlearning Implementation
│   ├── dataset/
│   ├── model/
│   ├── task/
│   ├── pipeline/
│   ├── unlearning/
│   └── utils/
│
├── Attack Research Extensions
│   ├── attack/
│   └── cache_v2/
│
├── Research, Documentation, and Reports
│   ├── self/
│   ├── 文档规划/
│   ├── docs/
│   ├── report/
│   ├── reports/
│   └── papers/
│
└── Runtime Evidence
    └── results/
```

## 7. Git Workflow

- Each short-lived branch represents one reviewable work block. Before the first edit, declare and record its parent branch, scope and expected paths, acceptance checks, and closeout mode (`commit` / `merge-parent` / `push` / `cleanup`).
- Use the primary local workspace by default for discussion, review, and continued work on the same block. Create a worktree only for concurrent code changes, isolated validation, or a demonstrated conflict, and state its boundary, branch, and path in advance.
- After each reviewable sub-block, proactively review the diff, run proportionate validation, and create a focused commit. Do not leave unexplained task changes except for drafts, validation failures, or unresolved major design decisions.
- `main`, `release/*`, and designated `research/*` branches are integration lines; do not develop on them directly. Each child branch merges back to its recorded parent with `git merge --no-ff`. Check status and worktrees before switching, merging, or cleaning up; use `git pull --ff-only` for routine synchronization.
- Before starting a formal gate or matrix, close every active work block and accept it into `main`; then follow `experiments/AGENTS.md` for SSH, pinned-SHA, preflight, and result-identity checks.
