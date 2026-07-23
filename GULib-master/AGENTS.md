# Repository Agent Instructions

These instructions apply to all work under `GULib-master/`.

## Project Overview

GULib is a Python/PyTorch Geometric research framework for adversarial attacks
on graph unlearning. The main research question is how strategically selected
node, edge, or feature deletion requests affect approximate unlearning methods.
This is an experiment/evidence repository: provenance, cache identity, metric
semantics, and reproducibility are part of correctness.

## Tech Stack

- Python with PyTorch, PyTorch Geometric, NumPy, scikit-learn, and related
  scientific/graph packages.
- YAML-driven experiment matrices, pytest contract/regression tests, and
  Markdown plus static HTML for human-facing evidence.

## Quick Navigation / Start Here

1. Read the root `CLAUDE.md` before changing code, experiments, or reports.
2. Read the nearest context-specific subfolder `CLAUDE.md` before touching that subtree.
3. For current experiment state, use `self/dashboard/WORKPLAN.md`; do not infer it from an old branch name or dated report.

## Project Map and File Organization

- `main.py`, `config.py`, `parameter_parser.py`, and `unlearning_manager.py`
  define the primary CLI, path construction, and method dispatch.
- `pipeline/`, `unlearning/`, `model/`, and `task/` contain the shared
  unlearning pipelines, method implementations, GNN backbones, and trainers.
- `attack/` contains selection strategies, attack orchestration, metrics, and
  the Legacy Result/Selection/Score cache clients.
- `cache_v2/` contains versioned Recipe/Artifact contracts and immutable
  selection/score artifacts.
- `experiments/` contains canonical runners, YAML matrices, and experiment
  families; `scripts/` contains validation, dashboard, plotting, and
  operational tools.
- `tests/` contains targeted pytest regression and contract tests.
- `self/dashboard/` is the live operational hub; `docs/`, `report/`, and
  `reports/` contain durable design, paper, and human-facing evidence.
- `data/`, `results/`, `log/`, and `logs/` contain inputs or generated runtime
  state. Treat them as evidence-bearing trees, not scratch space.

## Core Principles

- One coherent improvement belongs to one branch with one explicit parent.
- Preserve reviewable history and accept completed work through meaningful merge commits.
- Protect shared branches, other worktrees, remote experiment state, and unrelated dirty files.
- Fail closed when provenance, dataset identity, split identity, cache identity,
  or metric semantics are ambiguous.

## Runtime, Validation, and Common Commands

- Use the conda `gnn` interpreter for Python work:
  `E:/conda_package/envs/gnn/python.exe`. Do not rely on `conda activate` in a
  non-interactive shell.
- The local RTX 5070 is incompatible with the pinned CUDA/PyTorch stack. Local
  work is CPU analysis and targeted tests only; GPU experiments run on the
  accepted AutoDL `gnn_20` environment.
- `config.py` parses CLI arguments at import time. Avoid importing it from
  lightweight tests or notebooks unless the CLI context is intentionally set.
- Run the smallest relevant pytest set for a code change, for example:

  ```powershell
  E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_<area>.py
  ```

- Expand to adjacent contract/regression tests when changing shared runners,
  cache keys, artifact schemas, dataset resolution, metric semantics, or
  dispatch. Do not claim repository-wide acceptance from one targeted test.
- For experiment YAML or runner changes, run the canonical `--dry_run` and
  record its classification before any execution. A dry run is validation, not
  a formal result.
- Documentation-only edits do not require the Python suite, but links,
  generated counterparts, commands, and stated paths must be checked.

## Canonical Dataset Location (Mandatory)

These rules apply to every agent and are especially strict for formal runs on
the SSH active checkout at `/autodl-fs/data/OpenGU/GULib-master`.

- Canonical **source datasets** must resolve inside the active checkout. Raw
  adapter caches belong under `data/raw/<dataset>/`; OpenGU-persisted graph and
  split pairs belong under `data/processed/{transductive,inductive}/`.
- For Planetoid datasets, use the OpenGU lowercase leaves
  `data/raw/{cora,citeseer,pubmed}`. PyG's `raw/` and `processed/data.pt`
  beneath each leaf are part of that raw-adapter cache; they are not OpenGU
  canonical processed split pickles.
- Retired sibling dataset roots, another worktree's `data/`, experiment
  checkouts, backups, and archives are recovery/evidence sources only. Never
  use them as formal dataset roots, create new authoritative copies there, or
  symlink canonical active paths to them.
- Method-owned artifacts under `data/<Method>/`, unlearning targets under
  `data/unlearning_task/`, and result/cache directories are allowed runtime
  outputs. They are not alternative locations for canonical source datasets.
- When a dataset is missing, first stage and verify it under active
  `data/raw/`, then generate the canonical `data/processed/...` pair through
  the accepted OpenGU preprocessing flow with an explicit split/config/seed.
  Never substitute PyG `processed/data.pt` for an OpenGU canonical pickle.
- A formal SSH run must not download or preprocess a dataset inside the timed
  run. Preflight must resolve and record the requested path, real path,
  content fingerprint, split identity, and Git provenance, and must fail if a
  source resolves outside the active checkout.
- Do not delete historical duplicates merely because they are noncanonical.
  Inventory and hash them first, then remove only exact targets approved by
  the user. Current availability and known gaps live in
  `self/dashboard/WORKPLAN.md` and `reports/dataset_layout_AUDIT_REPORT.md`.

## Generated State and Cache Safety

- `self/dashboard/WORKPLAN.md` is the source of truth for current status.
  `self/dashboard/progress.html` is derived; never hand-edit it. Regenerate it
  with `E:/conda_package/envs/gnn/python.exe scripts/dashboard/refresh.py`.
- Follow the nearest cache-specific `CLAUDE.md` before inspecting or changing
  `results/cache/`, `results/selection_cache/`, or `results/score_cache/`.
  Never rename or hand-edit hash-named cache files.
- Do not clear caches to switch algorithm semantics. For the active E7/Cache V2
  lane, Legacy IF/Selection caches are read-only evidence. A changed algorithm
  or producer creates a new explicitly versioned V2 Recipe; existing V2
  Artifacts are not deleted or overwritten and are retired only through an
  explicit approved action.
- Cache invalidation, deletion, migration, freeze, or retirement is a material
  evidence operation. Inventory exact paths and hashes first, use a dry run
  when supported, and obtain explicit user approval before mutating existing
  evidence.
- Do not hand-edit generated reports, dashboards, aggregate CSVs, figures, or
  manifests when a repository generator owns them. Change the source or
  generator, regenerate, and validate the output.

## SSH Deployment Root Boundary

- The AutoDL deployment root `/autodl-fs/data` contains only the platform
  entries `.sys`, `.gitignore`, and the single active `OpenGU` checkout. Do
  not create sibling clones, worktree roots, canary stores, evidence roots,
  queue-operation roots, or shared dataset roots there.
- On the active checkout, all mutable experiment paths must resolve inside
  `/autodl-fs/data/OpenGU/GULib-master`, normally below `results/`, `data/`,
  `log/`, or `logs/`. The experiment runner must fail closed on an external
  absolute output path.
- Validate the top-level contract with
  `python scripts/validate_ssh_deployment_layout.py --base /autodl-fs/data`.
- Historical sibling evidence was relocated, without symlinks, under the
  ignored `results/_archive_ssh_peer_layout_20260724/` tree. Use
  `reports/ssh_deployment_layout_CLOSEOUT_REPORT.md` as the relocation
  authority; do not recreate an old absolute path to make a historical
  command work.
- Tracked reports, commands, configs, and imported machine summaries must not
  retain a retired `/autodl-fs/data` sibling prefix. Human-facing history uses
  the current archive/canonical access path plus a relocation notice. A
  controlled machine-summary path migration must record its baseline commit
  and pre-migration aggregate hash, then update every consuming SHA-256.

## Workflow Instructions: Git (Mandatory)

The authoritative human-readable workflow is [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md).

- Treat `main`, `release/*`, and explicitly designated `research/*` branches as integration lines. Do not develop directly on them.
- Before editing, name the intended parent branch. Create one short-lived branch for one coherent improvement from that parent.
- A child branch must merge back into its recorded parent first. If the parent is itself an improvement line, only merge that parent into `main` after the whole line is accepted.
- Accept completed improvements with an explicit merge commit: `git merge --no-ff <child>`. Do not use squash merge or rebase merge for accepted project work.
- Use `git pull --ff-only` for synchronization. `--no-ff` is for accepting an improvement, not for routine pulls.
- Before switching or merging, run `git status --short --branch` and `git worktree list`. Preserve unrelated dirty files and never move a branch that is checked out in another worktree.
- Suggested branch names are `feat/*`, `fix/*`, `experiment/*`, `docs/*`, and `chore/*`. Agent-created branches use `codex/<type>-<topic>-YYYYMMDD`.
- Keep commits reviewable and scoped. A heterogeneous worktree must be split into semantic commits; never use `git add -A` blindly.
- Improvement branches are for code/config/documentation changes plus unit, integration, and explicitly non-formal smoke tests. A branch smoke must use disposable output and must not be cited or resumed as a formal matrix cell.
- Formal experiments, including the one-cell MVP/gate that will become part of a matrix, start only after the complete improvement line is accepted into `main`. Run them from the intentionally clean SSH active checkout on `main`, with the exact full `main` SHA recorded and pinned for every stage of that matrix.
- If a formal run exposes a code defect, stop the matrix. Create a fix branch from the pinned `main`, test it, merge it through the recorded parent chain into `main`, then restart the formal gate under the new `main` SHA and a new result/cache identity. Results from the superseded SHA are diagnostic only.
- Do not merge into `main`, push, delete branches, prune refs, or rewrite shared history unless the user explicitly authorizes that step.

## Human-Readable Reports

For acceptance reports, experiment reports, architecture reviews, milestone summaries, and advisor-facing reports, produce matching Markdown and static HTML files. Markdown is the editable source of truth; both files must agree on conclusions and key numbers. Follow existing `docs/` and `reports/` conventions.

### Obsidian / Markdown layout rules

- Do not remove comparison tables merely because they are wide. Preserve tables when row/column alignment materially improves comparison.
- If a table is hard to read, first shorten cell text, move formulas or explanations outside the table, or split it into smaller same-purpose tables. Use callouts for definitions, verdicts, warnings, and evidence summaries—not as a blanket replacement for tables.
- In Obsidian-facing Markdown, write math with `$...$` and `$$...$$`; do not use `\(...\)` or `\[...\]` as the canonical delimiters.
- For display math inside a callout, prefix the opening delimiter, every equation line, and the closing delimiter with `>`.
- Visually verify edited tables and formulas in Obsidian reading view. Source-level Markdown checks alone are not sufficient acceptance evidence.
