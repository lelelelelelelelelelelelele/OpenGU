# Adversarial Attacks on Graph Unlearning — Agent Guide

> Active repository-level guidance. Directory-level `AGENTS.md` files add scoped ownership and operational detail.

## 1. Project Positioning and Information Entry Points

This repository is a research project on adversarial attacks against graph unlearning. It extends GULib, OpenGU's graph-unlearning library, to study a core question: when an attacker strategically selects node, edge, or feature deletion requests, can approximate graph-unlearning methods exhibit abnormal utility degradation, approximation error, privacy, or prediction-behavior changes?

The framework connects OpenGU's data processing, model training, and graph-unlearning methods to attack-side deletion-target selection, attack execution, and post-hoc evaluation. Research compares random, topology-based, influence/gradient-based, and fused selection mechanisms across unlearning methods, datasets, models, and deletion budgets, and builds reviewable evidence from performance, retrain-gap, collateral, and update-detection diagnostics.

This repository is both a codebase and an experiment/evidence repository: source code and YAML define executable experiments; datasets and splits, cache identities, result artifacts, and reports support conclusions. Every experiment conclusion must be traceable to an explicit configuration, dataset and split, code version, and artifact evidence.

Research materials and scientific records belong to the independent private [OpenGU research repository](E:/project/OpenGU-research/README.md). Research framing starts in [OpenGU DocMap](../../OpenGU-DocMap/_文档地图.md). [Work Plan](E:/project/OpenGU-research/self/research/index.html) independently owns experiment creation, preparation, runs, reruns, analysis, scientific decisions and experiment dependencies; its continuously maintained local state is `E:/project/OpenGU-research/self/research/experiments/EXP-NNN.json` (Git-ignored), while versioned analysis and scientific decisions live in `E:/project/OpenGU-research/self/research/analyses/EXP-NNN.json`. State updates never require a commit; completed analysis is committed only in research Git with its original execution SHA. A research commit does not change code HEAD or require another deployment; formal runs still verify local code main, private bundle and SSH code main. Development contracts and lifecycle belong to canonical WorkBlock records and Companion. An experiment may reference a blocking development Block; Work Plan never manages or synchronizes Block lifecycle.

Pure experiment maintenance, including creating, revising, validating or retiring scientific YAML and submission Recipes through existing interfaces, follows [the experiment Runbook](E:/project/OpenGU-research/self/research/RUNBOOK.md) without a Block Claim or software-candidate cycle. Development Blocks own changes to program behavior or interface contracts, such as parsers, algorithms, runners, metric implementations, and cache or result schemas. Tracked configuration and Recipe changes still require review, commit, version synchronization and formal preflight before execution. Do not duplicate either system's live state. Ordinary Block edits require no experiment-record update or dashboard commit. If provenance, dataset/split, cache identity or metric semantics are ambiguous, do not treat the result as trusted evidence.

## 2. Execution Locations

The local machine is for CPU analysis, targeted tests, and viewing verified results. Formal GPU experiments, formal datasets, and runtime cache/result state live in the SSH active checkout.

Devices share Git-tracked source and configuration. An experiment artifact becomes trusted evidence only after the required collection and verification flow; detailed SSH, synchronization, dataset, and cache rules are loaded on demand from their local `AGENTS.md` files.

## 3. Minimal Execution Pipeline

Registered experiment definitions enter the execution chain through the launcher owned by their plan and directory-level guidance:

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

### Figure generation: reuse the saved source

- Every data-driven figure must have a saved, executable Python entry point. Preserve its helper modules, input locations/version, generation command, output paths, and required plotting environment. A one-off terminal snippet, notebook output, or image alone is not a delivered figure source. Formal sources belong in version control; honor explicit isolated-draft/no-Git instructions for exploratory work.
- Before creating or revising a figure, read [the figure-source index](E:/project/OpenGU-research/report/paper/FIGURE_SOURCES.md), then search existing generators with `rg`. Compare the intended question, data cohort, metric/reference, aggregation and uncertainty, and visual layout. If an existing entry fits, modify and reuse it; do not write a parallel replacement because a new chat or paper figure number is being used. New entry points require a concrete reason why the closest existing sources do not fit, recorded beside the source and in the index.
- Use a stable descriptive identity for each figure; Fig. 1/3/4 are manuscript positions, not source identities. Record the currently adopted artifact and its generator together. Reuse does not authorize silently adopting an old metric, cohort, baseline, or obsolete visualization plan.
- Keep adopted colors, method/selector order, fonts, dimensions, axis scales/ranges, and uncertainty definitions explicit in the source or its shared style module. Default to preserving them. Explain intentional changes and compare against the adopted output; do not silently replace an adopted figure with an exploratory variant.
- Deliver the generator and its dependencies with any changed figure. Verify source data/series and compare the regenerated figure at paper width with the previous adopted output; numerical checks and visual inspection serve different purposes. Record changed inputs/parameters/styles and the actual checks. Reusing a filename or obtaining a successful exit code does not establish consistency.
- Conceptual/vector diagrams retain their editable native sources and established generation/export chain; do not force an unrelated Python redraw. Review frontends display the adopted artifact or convert its format, rather than independently replotting experimental values.

## 5. Runtime and Validation

Use the local machine for code changes, CPU analysis, targeted tests, and reviewing verified evidence. `config.py` parses CLI arguments at import time; do not import it from lightweight tests or notebooks unless the CLI context is intentionally supplied. Run formal GPU experiments from the active SSH checkout; `experiments/AGENTS.md` owns experiment entry-point selection, local experiment commands, and the detailed remote environment, dataset, pinned-SHA, and formal-gate rules. Validate changes in proportion to their risk: run the smallest relevant tests for code, the registered dry-run for experiment configurations, and link plus generated-artifact checks for documentation.

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
│   ├── docs/
│   ├── report/
│   ├── reports/
│   └── reports/  (software reports; research sources live in OpenGU-research)
│
└── Runtime Evidence
    └── results/
```

The independently versioned Obsidian research map lives beside this repository
at `E:\project\OpenGU-DocMap`.

## Independent private research repository

Manuscripts, scientific analyses, figures and their generators, editorial reviews and Work Plan records are owned by `E:/project/OpenGU-research`. Code Git owns algorithms, metrics, runners, software tests, formal YAML and Recipes. The Work Plan generator in this code repository requires an explicit `--research-root`; training, submission and SSH preflight do not read that repository. Existing history still contains unpublished material: do not publish current code main or rewrite history as part of this split. See [repository boundary](docs/research-repository.md).
