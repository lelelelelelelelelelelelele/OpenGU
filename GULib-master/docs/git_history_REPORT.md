# OpenGU/GULib Git History Report

Generated: 2026-07-10
Scope: repository snapshot `GULib-master`, branch `main` at `3f631fb` (`Merge research selection concordance baseline`); collected from the Windows research checkout.

## Verdict

This repository has two lives. The first is the upstream OpenGU framework history through `upstream/main` (`475e045`, 2025-07-12). The second is the local GULib research fork: from 2026-02 onward it becomes an attack-research workspace, then a Phase B / paper-production system, then a rebuttal-prep and concordance-analysis workspace.

The current `main` is not a thin fork. It is 268 commits ahead of `upstream/main`, 0 behind, with 828 changed files relative to upstream and a shortstat of 226,563 insertions and 1,191 deletions. Most of that mass is research infrastructure, experiment configs/results, reports, paper artifacts, dashboard state, tests, and local/server runbooks rather than changes to the original OpenGU algorithm implementations alone.

## Snapshot

| Item | Value |
|---|---:|
| All reachable commits | 425 |
| Commits on `main` | 405 |
| Merge-base with upstream | `475e045` (`Update dataset_utils.py`, 2025-07-12, bwfan-bit) |
| `main` ahead of upstream | 268 |
| `main` behind upstream | 0 |
| `main` ahead of `origin/release/phase-b-fixes` | 32 |
| `origin/release/phase-b-fixes` ahead of `main` | 0 |

Author distribution across all refs:

| Author | Commits |
|---|---:|
| lele (primary identity) | 246 |
| Frank (primary identity) | 100 |
| lele (NUS identity) | 37 |
| 艾煜明 | 19 |
| bwfan-bit | 15 |
| Frank (GitHub noreply identity) | 3 |
| lele_ssh | 3 |
| OpenGU Dev | 2 |

Commit density by month shows the project rhythm clearly:

| Month | Commits | Reading |
|---|---:|---|
| 2024-12 | 105 | Upstream import and early OpenGU shaping |
| 2025-01 to 2025-07 | 32 | Upstream maintenance / low-velocity framework work |
| 2026-02 | 99 | Attack framework and Phase A exploration |
| 2026-04 | 13 | Report/deck packaging and figure refresh |
| 2026-05 | 139 | Phase B, bug audit, arxiv scale, paper push |
| 2026-06 | 27 | Resume diagnosis, dashboard consolidation, clean data merge |
| 2026-07 | 10 | Concordance branch merge, doc-map sync, local planning hygiene |

## Development Phases

### 1. Upstream OpenGU Baseline: 2024-12 to 2025-07

The root history starts with upstream-style commits from Frank and bwfan-bit: initial upload, README/docs edits, ReadTheDocs material, and periodic merges from `bwfan-bit/OpenGU`. This phase is the generic Open Graph Unlearning framework: datasets, model backbones, pipeline classes, task routing, unlearning method implementations, and basic scripts.

Important conclusion: treat commits up to `475e045` as the framework base. They explain architecture, not the later attack-research agenda.

### 2. Attack-Research Fork and Phase A: 2026-02

The research fork begins after the upstream merge-base, with commits such as `4e8e671` (`init`) and then the stepwise construction of attack machinery:

| Date range | Main movement |
|---|---|
| 2026-02-16 to 2026-02-17 | Framework validation, cross-dataset validation, random selection experiments |
| 2026-02-17 to 2026-02-19 | Strategy abstraction, random / degree / PageRank, TracIn infrastructure |
| 2026-02-19 to 2026-02-21 | IM/CELF, hybrid IF-IM, result and selection cache, cross-method experiments |
| 2026-02-24 to 2026-02-27 | IM serious bug, IM v4, relative evaluation, GUIDE and GNNDelete corrections |

This is the phase where `attack/`, `demo_attack.py`, `eval_collateral.py`, `run_experiments.py`, `scripts/evaluation/`, `tests/`, and the early `self/` knowledge base become central. The history is exploratory and bug-discovery-heavy; many commits are experiment checkpoints rather than polished library releases.

### 3. Report and Defense Packaging: 2026-04 to early 2026-05

The April history shifts toward human-facing artifacts: MSc report draft, figure refresh, Overleaf bundle, defense deck structure, and report archive organization. The key pattern is not algorithmic novelty; it is turning Phase A evidence into explainable report/deck material.

This is also where report directories begin to matter as historical snapshots. Later commits reorganize report archives rather than deleting them.

### 4. Phase B and Paper Push: 2026-05

May is the densest and riskiest period: 139 commits, many of them fixes, runner changes, arxiv scaling, and paper integration. This phase introduces the project as a production-like experiment system.

Key strands:

| Strand | Representative commits / topics |
|---|---|
| Cache and strategy correctness | `af1c8ba` prewarm selection cache, `3f4d557` IM CELF shared cache, `bbce51e` topology-only seed anchor |
| Pipeline correctness | `13f1e89` train before TracIn/Hybrid selection, `ddb7109` cache key completeness and strategy isolation, `57fbdd3` block failed-unlearning ResultCache pollution |
| Arxiv scale | TracIn chunking, IM shared cache, arxiv runbooks, H20/A800/4090 execution split |
| Phase B matrix | YAML-driven `experiments/run.py`, `phase_b_*` configs, `gate_runs.py`, pass/fail gates |
| Paper output | Overleaf sections, six figures, `_phase_b_aggregate.csv`, k=5 noise-floor baseline, terminology rename from MIA AUC to update-detection AUC |

The main lesson: May commits should be read as a hardening sequence after finding that naive Phase A artifacts were not paper-safe. The repository becomes much more audit-oriented: cache keys, seeds, failure propagation, generated figures, and runbooks are all part of the research claim boundary.

### 5. Resume, Dashboard, and Operational Hub: 2026-06

June history has fewer commits but high structural importance. The merge `5428bae` brings `release/phase-b-fixes` into `main` with clean Phase B data, paper integration, and a 2026-06 resume diagnosis.

Then the project reorganizes its operational memory:

| Commit | Meaning |
|---|---|
| `470995f` | Resume-phase state, freeze old dashboard, record L8/GraphRevoker findings and research paths |
| `51f4cd9` | Generate `progress.html` from progress source |
| `44f7988` | Add `WORKPLAN`, config inventory, dashboard rendering fixes |
| `3daabdc` | Consolidate onto `self/dashboard/WORKPLAN.md` as the single operational hub |
| `5da2217` | Data-driven config inventory heatmap and CSV generator |

This is the point where the repo stops being just code plus results and becomes a governed research workspace. `self/dashboard/WORKPLAN.md` is the live current-state hub; older dashboards and reports are historical evidence.

### 6. Concordance, Rebuttal Prep, and Sync Tooling: 2026-06-27 to 2026-07-10

The `research/selection-concordance-2026-06-27` branch is now merged into `main` by `3f631fb`. Its theme is mechanism clarification: do degree, PageRank, IM, TracIn, and GIF select the same nodes, and what does deployed TracIn actually measure?

Key sequence:

| Commit cluster | Meaning |
|---|---|
| `1cfe16c` to `3ee470c` | Training-free topology-selector runner, Jaccard@k analysis, self-contained HTML report |
| `3788511` to `b3e10cc` | GIF/IF-as-scorer and real GIF vs TracIn on trained base GCN |
| `0115b80` / `289a541` | Expand to CS and pubmed; refresh reports |
| `21865db` / `4827256` | Proper Hessian-free TracIn and correction that deployed cross-form is degenerate |
| `4f6faf5` / `cc9d669` | Standalone chapter and finding document for TracIn mis-specification |
| `7e2fc37` | Add SyncMate workspace synchronization helper |
| `81eea19` | Sync OpenGU document map and 4090 run state |

This is the current conceptual layer: it sharpens mechanism claims for rebuttal / advisor discussion rather than merely adding experiment volume.

## Branch Topology

`main` currently contains both major modern branches:

| Branch / ref | Status |
|---|---|
| `main` | Current branch, equals `origin/main`, at `3f631fb` |
| `release/phase-b-fixes` / `origin/release/phase-b-fixes` | Merged into `main`; `main` is 32 commits ahead, release has no unmerged commits |
| `research/selection-concordance-2026-06-27` | Merged into `main` via `3f631fb` |
| `paper/alignment-experiment` | Side branch at `565aaf6`; not an ancestor of `main` |
| `backup/*` branches | Historical safety snapshots, not the current working line |
| `upstream/main` | Framework baseline at `475e045`; current `main` is 268 commits ahead |

## Hot Areas

Relative to upstream, the biggest conceptual additions are:

- `attack/`: selection strategies, attack manager, pipeline adapter, result cache, selection cache, score cache.
- `experiments/`: Phase B YAML matrix, baseline k=5 framework, arxiv configs, IF/IM benchmarks.
- `scripts/`: evaluation, figures, gates, cache tools, arxiv deployment, SyncMate.
- `self/`: project memory, dashboard, metrics catalog, validation log, limitations, concordance study.
- `report/` and `results/`: paper/report artifacts, archived progress snapshots, Phase B aggregate data, figure outputs.
- `tests/`: regression tests around strategies, cache behavior, collateral evaluation, Phase B invariants, SyncMate.

The code changes to original OpenGU internals are comparatively targeted: `pipeline/`, `model/base_gnn/`, `task/`, `unlearning/unlearning_methods/*`, `unlearning_manager.py`, and `utils/dataset_utils.py` have fixes/adapters, but the main expansion is the attack/evaluation/research-control layer around OpenGU.

## How To Read This Repo Now

1. Start with `CLAUDE.md` for project context and operational warnings.
2. Use `self/dashboard/WORKPLAN.md` for current state, not old progress files.
3. Use `self/dashboard/VALIDATION_LOG.md` and `self/limitations.md` for evidence-backed claims and known gaps.
4. Treat `self/related_work/concordance/` as the current mechanism-clarification layer.
5. Treat `report/progress/` and older report directories as historical snapshots, not live truth.
6. Treat `results/cache/`, `results/selection_cache/`, and `results/score_cache/` as hash-keyed generated stores; their `CLAUDE.md` files warn against renaming or hand-editing.
7. When tracing paper numbers, follow `experiments/run.py` -> `results/runs/...` / aggregate CSV -> figure scripts -> paper/report artifacts.

## Practical Takeaways

- The repo's development history is evidence-driven and corrective: many major commits exist because a measurement, cache, seed, or mechanism assumption was found unsafe.
- The most important transition is 2026-05: Phase B hardening changes the project from exploratory scripts into an auditable experiment pipeline.
- The second most important transition is 2026-06-27 onward: the dashboard and concordance work clarify what claims are still live and what mechanisms can be defended.
- The current `main` is up-to-date with both the Phase B release line and the concordance research branch, but it intentionally leaves some side branches as archival or speculative.
- For future work, avoid broad refactors. The historical shape says narrow, evidence-preserving changes are safer: update source docs, regenerate derived reports, and keep cache/result semantics explicit.
