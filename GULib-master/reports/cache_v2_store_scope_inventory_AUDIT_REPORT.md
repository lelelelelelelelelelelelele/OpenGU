# Cache V2 Store Scope Inventory Audit

Date: 2026-07-29

Source of truth: this Markdown file

Status: **inventory complete; no Store migration or cleanup performed**

> [!summary] Verdict
> E8 is now the only target-direct formal configuration that requires the
> canonical shared `results/cache_v2` Store and its `index.sqlite`. Neither the
> local E8 worktree nor the SSH active checkout contains an E8 Cache/Result
> Artifact, so no migration, import, deletion, or index repair is needed. The
> local primary workspace retains two separate historical ScoreBundle Stores;
> they require a separately approved cutover plan and remain untouched.

## Scope and method

- Tracked entry points/configs were inspected at
  `codex/cache-v2-e8-canonical-root@65885e7` with `git grep`.
- Local primary Store was read from
  `E:/project/OpenGU/GULib-master/results/cache_v2`; its unrelated dirty
  `experiments/AGENTS_DRAFT.md` was observed but not read, changed, staged, or
  copied. The current E8 worktree has no `results/cache_v2` directory.
- SSH active checkout was read at
  `/autodl-fs/data/OpenGU/GULib-master`, `main@0566ec75b2a492520b392851be663d27790e9fba`.
  Its only unrelated status entries were two deleted generated SGU `.pyc`
  files; no SSH state was changed.
- Index counts were read from SQLite in read-only mode. No Artifact payload,
  header, index row, Legacy cache, config, or result layout was modified.

## Physical Store observations

| Location / Store | Index | Artifact types and index rows | Payload / header files | Consumer refs | Notes |
|---|---|---:|---:|---:|---|
| Local primary `results/cache_v2/bc_target_v2` | `index.sqlite3` | Score: 9 | 9 / 9 | 0 | Experiment-owned B/C ScoreBundle Store |
| Local primary `results/cache_v2/c_target_v1` | `index.sqlite3` | Score: 6 | 6 / 6 | 0 | Experiment-owned C-target ScoreBundle Store |
| Local primary aggregate | 2 indexes, 32 files | Score: 15 | 15 / 15 | 0 | No root-level canonical `index.sqlite` |
| Current E8 worktree | absent | 0 | 0 / 0 | 0 | No Cache V2 directory; no E8 payload exists |
| SSH active `results/cache_v2` | `index.sqlite` | Selection: 1 | 1 / 1 | 0 | Schema v1; SHA-256 `c8bb5e5b26a2067907dee06ef4e987b04398a7dbe7eceb5c5b9fa5c3647bed07` |
| SSH active E8 paths | absent | 0 | 0 / 0 | 0 | Neither `cache_v2/target_direct_formal_v2` nor `runs/target_direct_formal_v2` exists |

The SSH index also contains `trace.jsonl`, `producer_counter.json`, and
`legacy_freeze.json`; its sole payload is an immutable Selection Artifact.
The index schema is `schema_version=1` with the current recorded fingerprint.

## Tracked caller/config classification

| Classification | Entry points / configs | Configured root and index | Artifact / producer family | Current evidence and reuse assessment | Risk / required follow-up |
|---|---|---|---|---|---|
| Canonical formal consumer | `experiments/target_direct_v1/syncmate_stage.py`, `run_selection.py`, `experiments/configs/syncmate_target_direct_formal_v2.yaml` | `results/cache_v2`, `index.sqlite` | Target-direct V1 ScoreBundle + Cache V2 Selection materialization | E8 has no local or SSH payload/index rows yet; Score and Selection now share one root/index | Formal execution remains blocked by clean-main, AutoDL, GPU, and profile gates; no migration is needed before a future formal run |
| Canonical formal consumer | `experiments/run.py` Cache V2 dispatch and `experiments/configs/cache_v2_cora_degree_canary.yaml` | default / explicit `results/cache_v2`, `index.sqlite` | Cache V2 Selection through the generic runner / degree adapter | The SSH canonical index has one Selection row, but this read-only inventory does not attribute its Recipe to a specific historical caller | Keep exact Recipe resolution; do not infer cross-experiment reuse from root equality alone |
| Explicit isolated canary | `cache_v2_gate4_cora_degree_canary.yaml`, `scripts/cache_v2_gate4_canary.py` | `results/cache_v2/syncmate_gate4`, its own index | Gate 4 Selection canary | No matching local-primary or SSH-active substore was observed | Isolation is intentional for the bounded canary; do not fold it into a formal default without a new review |
| Explicit isolated canary | `syncmate_small_selection_{mvp,dataset_gate,full}_v1.yaml` and `syncmate_small_selection_gu_gate_v1` through `v5` | `results/cache_v2/small_selection_syncmate_v1` and `syncmate_small_selection_gu_v*` | Public-profile B/C selection and external-selection GU gates | No matching live substore was observed in the inspected roots | Names, `require_empty_roots`, and controlled-public claims make these validation lanes rather than a cross-experiment formal Store default |
| Experiment-owned Store requiring follow-up | `experiments/bc_target_v2/run_selection.py`, `run_matrix.py` | default `results/cache_v2/bc_target_v2`; Selection defaults to its `selection_artifacts` child; Score index is `index.sqlite3` | B/C V2 ScoreBundle plus Selection projections | Local primary has 9 indexed Score Artifacts and zero consumer refs | A separate cutover/migration decision is required before claiming canonical reuse; this audit performed none |
| Experiment-owned Store requiring follow-up | `experiments/c_target_v1/run_cora_gcn.py` | default `results/cache_v2/c_target_v1`, `index.sqlite3` | C-target V1 ScoreBundle | Local primary has 6 indexed Score Artifacts and zero consumer refs | The historical default remains supported; any canonical-root conversion needs its own compatibility and provenance plan |
| Experiment-owned Store requiring follow-up | `experiments/bc_target_v2/benchmark_selection.py` and `experiments/tracin_v2/run_formal_selection_gate.py` | benchmark default is per-cell `bc_target_v3_benchmark_20260721`; TracIn accepts separate caller-supplied score/selection roots | B/C benchmark and formal TracIn score/selection producers | Only tracked historical summaries/references were found, not a live inspected Store | Per-run/per-stage root shapes prevent intended reuse and need explicit policy before any cutover |
| Historical or inactive reference | tracked B/C benchmark summaries, C-target summaries, prior acceptance/design reports, and replay instructions | historical paths include retired worktrees and named replay/canary roots | Historical Score/Selection evidence | These entries explain provenance only; they are not current Store owners | Retain read-only; do not rewrite historical paths or import their Artifacts during E8 work |

## Consumer references and cache safety

All three inspected SQLite indexes report `consumer_refs=0`. Tracked source
defines the `ConsumerRef` API in `cache_v2/index.py`, but this inventory found
no separate tracked producer that adds consumer references. Thus no consumer
claim can authorize migration or cross-store reuse; only an exact Recipe and
Artifact resolution can do so.

The local primary Stores use the backward-compatible ScoreBundle default
`index.sqlite3`. E8 deliberately injects `CacheIndex(root / "index.sqlite")`
only for its canonical root. This report does not reinterpret the two local
`.sqlite3` Stores as corrupt, duplicate them, or alter their schema.

## Conclusions and non-actions

1. E8 ScoreBundle and Selection Artifacts will use the canonical shared Store
   and one `index.sqlite`; `results/runs/target_direct_formal_v2` remains an
   experiment result/evidence directory, never a Store.
2. No E8 Cache/Result Artifact exists locally or on SSH active, so the
   expected no-migration/no-deletion condition is confirmed.
3. The canonical SSH Store currently contains one Selection Artifact and no
   consumer references. Local primary retains 15 historical Score Artifacts in
   two experiment-owned stores.
4. Repository-wide cutover, Legacy retirement, Artifact import, cache rebuild,
   configuration edits outside E8, GPU execution, merge, push, and deletion
   are explicitly **not implemented** by this audit.
