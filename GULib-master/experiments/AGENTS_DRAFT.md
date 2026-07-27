# Formal Experiment Agent Guide

> Working draft. This file is the intended local instruction surface for
> `experiments/`. It does not replace root `AGENTS.md` or authorize a formal
> run until reviewed and accepted.

## 1. Scope and Entry Points

`experiments/` owns executable experiment definitions, matrix expansion,
preflight, and lane-specific gates. The normal matrix entry point is
`experiments/run.py + YAML`; the authoritative operational route and current
configuration status are in
`文档规划/10_实验矩阵/15_实验运行入口与脚本.md` and
`self/dashboard/WORKPLAN.md`.

Before changing or running an experiment, read the root agent instructions,
the live work plan, this file, the relevant YAML/README, and the nearest
family-specific documentation. `if_benchmark/`, `im_benchmark/`,
`im_score_benchmark/`, `tracin_v2/`, target-direct, and baseline lanes have
different semantic targets; a result from one lane must not be represented as
evidence for another.

## 2. Lane Classification

- **Local development** covers static inspection, CPU analysis, targeted tests,
  `--dry_run`, and explicitly disposable smoke checks. It is not formal
  experimental evidence.
- **Accepted experiment-line smoke** may validate a branch change with isolated
  output, but it cannot be resumed or cited as a matrix cell.
- **Formal gate or matrix** is an evidence-producing run. A one-cell gate is
  formal when it will be extended into the same matrix, even if it is small.
  Its source, configuration, dataset/split, cache/artifact identity, and
  results must remain on the same declared formal line.

## 3. Formal Start Gate

Start a formal gate or matrix only when all of the following are true:

1. All active code, configuration, and documentation work blocks that affect
   the run are closed and accepted into `main`.
2. The SSH active checkout is the sole formal location:
   `/autodl-fs/data/OpenGU/GULib-master`, on clean `main`, synchronized to the
   exact full `main` SHA recorded for the job.
3. The formal YAML, method/strategy lane, requested datasets, splits, output
   identity, and acceptance gate are declared before execution. Do not infer
   them from an old report, a result directory, or a branch name.
4. The canonical runner or lane preflight has first run in dry-run mode and its
   classification is recorded. `--dry_run` validates expansion only; it is not
   a result.
5. Preflight resolves the requested and real dataset paths, content and split
   identity, code SHA, config fingerprint, and every mutable output beneath the
   active checkout. It fails closed on an external root or an ambiguous identity.

Do not create an SSH worktree merely because a run is formal. Use one only for
a concrete collision, contamination, concurrent branch, or unaccepted-fix
boundary and record why the active checkout could not be used.

## 4. Dataset, Runtime, and Evidence Boundaries

- Canonical source data stays inside the active checkout: raw adapter caches
  under `data/raw/<dataset>/` and OpenGU graph/split pairs under
  `data/processed/{transductive,inductive}/`. Planetoid source leaves are
  lowercase `cora`, `citeseer`, and `pubmed`; PyG `processed/data.pt` is not an
  OpenGU canonical split pickle.
- A timed formal run never downloads or preprocesses data. Stage and verify
  data through the accepted flow before the gate begins. Historical duplicates,
  other worktrees, backups, and archives are recovery evidence, not sources.
- Mutable formal state resolves only inside the active checkout, normally under
  `results/`, `data/`, `log/`, or `logs/`. `/autodl-fs/data` is a deployment
  boundary, not a scratch root.
- Cache V2 Artifacts are exact and immutable; legacy caches are read-only
  evidence unless an approved migration says otherwise. Never clear, rename,
  patch, or overwrite cache/result evidence to make a semantic change appear
  complete.
- AutoReport V3 JSONL is the audit fact source. Markdown and HTML summaries are
  rebuildable views, never handwritten evidence.

## 5. Runner and Gate Discipline

- For normal matrices, use `E:/conda_package/envs/gnn/python.exe` locally and
  the accepted SSH `gnn_20` environment remotely. `experiments/run.py` with a
  versioned YAML is the matrix definition; shell scripts only wrap, diagnose,
  or sequence declared YAMLs.
- Run `--dry_run` before an execution change. Use `--limit` or a dedicated
  sanity configuration for a non-formal check. Do not relabel a CPU/local
  sanity run as a remote formal gate.
- For a standard `experiments/run.py` matrix cell, require
  `attack.json`, `collateral.json`, `predictions.npz`, and `_meta.json`; the
  metadata must carry the matching configuration fingerprint and Git SHA.
  A selection-only or method-specific lane follows its declared artifact
  contract instead of pretending to be a complete matrix cell.
- Run the declared acceptance gate before extending a matrix. A passing
  infrastructure or selector gate proves only its stated contract, not
  comparative attack effectiveness or a paper-level conclusion.
- `--force`, reruns, cache invalidation, result replacement, and migration are
  controlled repair operations. Declare the defect and invalidation boundary
  first; preserve the superseded evidence and use a new identity whenever the
  code, recipe, dataset/split, or formal claim changes.

## 6. Defect, Restart, and Closeout

If a formal run exposes a source defect, stop the affected matrix. Create and
accept a fix through the recorded parent chain into `main`, then restart the
formal gate under the new full SHA and a new result/cache identity. Earlier
results remain diagnostic only; never mix their cells with the restarted
matrix.

After a formal stage, retain the config, full SHA, dataset/split fingerprints,
preflight and gate receipts, result/artifact paths, and any remote-to-local
verification record. Update live operational state only through its owning
source; do not rewrite generated dashboards, aggregates, or reports by hand.

## 7. Rule Allocation

| Rule type | Canonical owner | This file's role |
|---|---|---|
| Repository purpose, normal Git work blocks, local-vs-SSH overview | root `AGENTS.md` | Link and comply; do not duplicate. |
| Formal SHA, active checkout, dataset/preflight, runner/gate, result identity | `experiments/AGENTS.md` | Own the stable mandatory boundary. |
| Current matrix, commands, machine placement, and ordered runbook steps | `文档规划/10_实验矩阵/15_实验运行入口与脚本.md` + `WORKPLAN.md` | Read on demand; do not copy dated operational state. |
| IF, IM, TracIn, target-direct, and baseline semantics | nearest experiment-family README/design/plan | Require local reading; do not flatten research claims into general rules. |
| Cache implementation and journal writer internals | `cache_v2/`, `results/*`, and reporting design documents | Preserve their contracts; no duplicate implementation manual here. |

Do not create a second prose “formal rules” document. This file is the
normative stable contract; the document map remains the human runbook. If a
future workflow needs a checklist, generate a job-specific preflight manifest
from the runner rather than copying rules into another static page.
