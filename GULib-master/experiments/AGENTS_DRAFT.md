# Formal Experiment Agent Guide

> Working draft for the future `experiments/AGENTS.md`. Until this draft is
> reviewed and accepted, the [root agent instructions](../AGENTS.md) remain
> binding, and this file does not by itself authorize a formal run.

## 1. Scope, Registration, and Authorities

These rules apply to experiment definitions, formal gates, full matrices,
reruns, and evidence collection under `experiments/`. Local inspection,
targeted tests, `--dry_run`, and disposable smoke checks may support
development, but they are not formal experiment evidence.

Before changing, starting, resuming, or repairing an experiment, read:

- the [root agent instructions](../AGENTS.md);
- the [live WORKPLAN](../self/dashboard/WORKPLAN.md) for current registration,
  readiness, blockers, and the exact experiment plan;
- the [experiment runbook](../文档规划/10_实验矩阵/15_实验运行入口与脚本.md)
  for current launch and collection procedures; and
- for failures or resumed work, the
  [rerun and cache repair runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md).

The WORKPLAN is the sole source of current operational state. The registered
experiment plan owns the experiment-specific claim, matrix, launcher, gate,
and acceptance criteria. The runbooks own reusable execution and repair
procedures. Do not reconstruct a run or recovery command from an old branch
name, process list, log, result directory, or dated report.

Experiment families such as IF, IM, TracIn, target-direct, surrogate-transfer,
and baseline reconstruction have different claims and evidence contracts.
Read the registered family plan instead of flattening them into a generic
matrix.

## 2. Registered and Unregistered Experiment Plans

A registered experiment may be declared by its stable ID, such as `A7` or
`E8`, plus its canonical YAML, script, or registered plan. Do not duplicate its
full planning table in a task message. A repair may reference the same ID, but
must additionally state the defect, invalidated evidence boundary, replacement
Git SHA, and new result/cache identity.

An unregistered experiment must declare, before execution:

| Field | Required declaration |
|---|---|
| Question | Claim or failure mode being tested |
| Lane | Local check, disposable smoke, formal gate, or formal matrix |
| Matrix | Dataset, model, method, strategy, seed, ratio, and budget |
| Baseline | Matched baseline and why it is valid |
| Evidence | Required artifacts, metrics, and acceptance gate |
| Identity | YAML or launcher, full Git SHA, dataset/split fingerprint, and cache/artifact identity |
| Recovery | Invalidating failures, isolation boundary, and restart procedure |

Register a new experiment, or an explicit extension of an existing one, when
the claim, dataset or split, method semantics, baseline, core metric, or matrix
scope changes. A renamed directory or reused ID does not preserve identity
across such a change.

## 3. Stage Cleanliness and Local-Origin-SSH Alignment

Formal execution starts only at a repository-wide stage boundary:

1. Every active work block is closed, reviewed, and accepted into `main`.
   Historical branch refs may remain, but no unaccepted work line remains
   active.
2. The primary local `main`, `origin/main`, and the SSH active checkout
   `main` resolve to the same recorded 40-character SHA.
3. The primary local and SSH tracked trees are clean, including source,
   configuration, and documentation used by the run.
4. The SSH checkout is the single active formal checkout at
   `/autodl-fs/data/OpenGU/GULib-master`.

Managed ignored runtime outputs may remain only when their ownership and
identity are already registered. An unexplained dirty path, SHA mismatch,
wrong branch, external source/config path, or incomplete work block blocks the
formal gate.

Verify the stage explicitly:

```powershell
git status --short --branch
git rev-parse main
git rev-parse origin/main
```

```bash
cd /autodl-fs/data/OpenGU/GULib-master
git status --short --branch
git rev-parse HEAD
python scripts/validate_ssh_deployment_layout.py --base /autodl-fs/data
```

Record and compare the full SHAs; a short SHA is not sufficient provenance.
Do not create another worktree merely because a run is formal.

## 4. Minimal Gate Before Full Expansion

Every full formal experiment must first pass a registered, representative
minimal gate. A registered experiment uses its registered gate. An
unregistered experiment must define and register one before the full run.

The gate and the later expansion must use the same:

- full Git SHA and clean stage;
- canonical dataset, split, candidate set, and fingerprints;
- configuration or versioned Recipe;
- cache and artifact semantics; and
- output identity and acceptance logic.

The gate must exercise the fragile parts of the real lane, including:

- dataset and split resolution;
- cache cold miss, write, warm exact hit, and provenance checks when caching is
  used;
- method, selector, seed, ratio, and budget propagation;
- required artifact production; and
- metric, AutoReport, and acceptance-gate logic.

Only expand the same registered matrix after the gate passes. A failure stops
the expansion. Local tests, dry runs, and disposable smoke checks remain useful
pre-gate validation, but none substitutes for the formal minimal gate.

## 5. Canonical Launchers and Command Examples

Do not assume every formal experiment is launched by one Python command. Use
the launcher registered for that experiment: a YAML matrix runner, a
standalone Python or module runner, a gate/resume runner, a SyncMate recipe, or
an accepted shell/PowerShell orchestration wrapper.

The current Phase B main matrix still uses `experiments/run.py + YAML`; this is
current for that lane, not a universal rule:

```powershell
# Local expansion check only
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/<config>.yaml --dry_run
```

```bash
# Formal SSH execution only after the stage and minimal gate are ready
python experiments/run.py experiments/configs/<config>.yaml
python scripts/gate_runs.py experiments/configs/<config>.yaml
```

Registered specialized entry points include, for example:

```bash
# E2 enumeration / repair preflight
python scripts/redo_collateral_if_family.py \
  experiments/configs/phase_b_cora_gcn.yaml --dry_run

# E3 preflight, registered one-cell gate, then same-SHA expansion
python experiments/baseline_k5/rerun_cora_noise_anchor.py --preflight-only
python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --gate-only --expected-git-sha <full-sha>
python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --resume --expected-git-sha <same-full-sha>
```

E8 uses the registered target-direct/SyncMate path rooted at
`experiments/target_direct_v1/` and
`experiments/configs/syncmate_target_direct_formal_v2.yaml`. Shell wrappers
may sequence registered commands, logging, collection, and shutdown, but they
do not replace the experiment definition or provenance.

For an exact start, resume, or recovery command, follow the
[live WORKPLAN](../self/dashboard/WORKPLAN.md), the experiment plan linked
there, the [experiment runbook](../文档规划/10_实验矩阵/15_实验运行入口与脚本.md),
and the [rerun and cache repair runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md).
Do not revive a stale wrapper path merely because the script still exists.

## 6. Single Dataset Authority, Cache, and Evidence Boundaries

The SSH active checkout is the only authoritative dataset root for formal
runs. Two canonical dataset channels exist inside that one checkout:

- Public Planetoid fixed-split lanes read lowercase
  `data/raw/{cora,citeseer,pubmed}` leaves. Their eight raw files and PyG
  `processed/data.pt` belong to the raw-adapter cache.
- OpenGU integrated lanes read graph/split pairs from
  `data/processed/{transductive,inductive}/`.

These channels have different split semantics and must never be relabelled as
each other. PyG `processed/data.pt` is not an OpenGU canonical processed split
pickle.

Another worktree, sibling checkout, shared dataset root, backup, archive, or
symlink is recovery material, not a formal source. Method-owned paths under
`data/<Method>/`, unlearning targets under `data/unlearning_task/`, and
result/cache directories are runtime outputs, not alternative source datasets.

A timed formal run must not download or preprocess source data. Before the
gate, resolve and record the requested path, real path, canonical root,
content fingerprint, split and candidate identity, and Git provenance. Fail
closed if any source resolves outside the active checkout or its identity is
ambiguous.

Cache V2 Artifacts are exact and immutable. A semantic or producer change
creates a new versioned Recipe and identity; it does not overwrite an existing
Artifact. Legacy IF, Selection, and Score caches are read-only evidence unless
an explicitly approved migration says otherwise. Inventory exact paths and
hashes before any cache invalidation, retirement, migration, or deletion.

All mutable experiment outputs must resolve inside the active checkout,
normally under `results/`, `data/`, `log/`, or `logs/`.

## 7. Gate, Collection, and Progress Update

For a standard `experiments/run.py` cell, collect `attack.json`,
`collateral.json`, `predictions.npz`, and `_meta.json`; metadata must match the
registered configuration fingerprint and full Git SHA. A selection-only,
baseline, or method-specific lane follows its own registered artifact contract
and must not present partial artifacts as a standard complete cell.

Run the declared acceptance gate and retain its receipt together with the
configuration, full SHA, dataset/split fingerprints, cache or artifact
references, result paths, logs, and remote-to-local verification record.
AutoReport V3 JSONL is the machine audit source; generated Markdown and HTML
views are projections and must not be hand-edited.

The browser-readable experiment progress table is
[config_inventory.html](../self/dashboard/config_inventory.html), generated
from [config_inventory.csv](../self/dashboard/config_inventory.csv). After a
registered experiment reaches a declared terminal state and its artifacts and
gate evidence are collected:

1. update the appropriate produced, usable, accepted-remote, or rerun state in
   the CSV source;
2. record an explanatory warning when evidence is partial or invalidated; and
3. regenerate the HTML view:

   ```powershell
   E:/conda_package/envs/gnn/python.exe scripts/dashboard/gen_config_inventory.py
   ```

Never hand-edit the HTML. Disposable local checks and unregistered smoke runs
do not update the table unless they are explicitly registered. Append a new
empirical acceptance claim to
[VALIDATION_LOG.md](../self/dashboard/VALIDATION_LOG.md) only with its evidence
boundary intact.

## 8. Defect, Repair, Restart, and Closeout

If a formal run exposes a code, configuration, data, metric, cache, or
provenance defect, stop the affected matrix and follow the
[rerun and cache repair runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md).

Declare the affected experiment ID and cells, the defect, the invalid SHA and
result/cache/artifact boundary, and which old evidence is retained only for
diagnosis. Fix and validate the issue on its work block, accept it through the
recorded parent chain into `main`, and restore the clean local-origin-SSH
alignment.

Then run the registered minimal gate again under the new full `main` SHA and a
new result/cache identity before restarting the matrix. Never combine cells
from the superseded SHA with the restarted matrix.

Closeout is complete only after the registered gate and artifact collection
pass, the progress source is updated and regenerated, and the WORKPLAN records
the current terminal or blocked state.
