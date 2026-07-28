# Cache V2 Full-Repository Store Inventory Audit

> **Verdict:** E8 is correctly configured as a consumer of the one shared canonical Cache V2 Store, `results/cache_v2/index.sqlite`. A full read-only inventory found no E8 target-direct Artifact to migrate or remove. The other physical stores are either experiment-owned defaults, isolated canary evidence, or historical archives; none should be cut over, migrated, or deleted without a separate owner-approved plan.

## Audit boundary and method

- **Code/config snapshot:** current E8 worktree `codex/cache-v2-e8-canonical-root` at `e0bceac1d1ade9dc74bb2f75bdd672919c608515`.
- **Local physical snapshot:** `E:/project/OpenGU/GULib-master` at `6ef57ce95566161b8137d692893ccbf80391293e`; its unrelated untracked user draft was preserved. The current E8 worktree and the two other Codex worktrees contain no Cache V2 index.
- **SSH physical snapshot:** `/autodl-fs/data/OpenGU/GULib-master` at `0566ec75b2a492520b392851be663d27790e9fba`. Its only Git dirt is two deleted generated SGU `__pycache__` files; this audit did not repair them.
- **Method:** tracked code/config root scan; read-only enumeration of every `index.sqlite` and `index.sqlite3`; read-only SQLite inspection for all local indexes; SSH index/path enumeration plus header/payload census. No Store, config, run, queue, cache, or archive was modified.
- **Remote SQL evidence:** the active canonical index SHA-256 is still `c8bb5e5b26a2067907dee06ef4e987b04398a7dbe7eceb5c5b9fa5c3647bed07`. It exactly matches the direct CacheIndex inspection recorded in [the preceding scope inventory](cache_v2_store_scope_inventory_AUDIT_REPORT.md): schema v1 and one verified Selection Artifact. SSH has no SQLite or Python command-line client, so archived indexes are classified from their physical Cache V2 header/payload pairs rather than reopened remotely.

## Tracked root and consumer map

| Classification | Entrypoint / configuration | Declared or resolved Store root | Current role and reuse boundary |
|---|---|---|---|
| **Canonical formal consumer** | `experiments/configs/syncmate_target_direct_formal_v2.yaml`; `experiments/target_direct_v1/syncmate_stage.py`; `run_selection.py` | `results/cache_v2` / `index.sqlite` | E8 accepts only this root, rejects split legacy roots and stage-shaped roots, and shares one injected `CacheIndex` between Score and Selection operations. There is no E8 payload yet. |
| **Canonical generic consumer** | `experiments/run.py`; `cache_v2_cora_degree_canary.yaml` | default `results/cache_v2` | Generic Cache V2 runner/canary family; may reuse only exact compatible Artifacts in the shared root. |
| **Explicit isolated canary** | `cache_v2_gate4_cora_degree_canary.yaml`; `scripts/cache_v2_gate4_canary.py` | `results/cache_v2/syncmate_gate4` | Isolated Gate 4 canary root; not a consumer of E8's canonical Store. No active local index is present. |
| **Explicit isolated canary** | small-selection MVP/dataset/full SyncMate v1 configs | `results/cache_v2/small_selection_syncmate_v1` | Historical isolated SyncMate selection root; no active local index is present. |
| **Explicit isolated canary** | `syncmate_small_selection_gu_gate_v1` through `v5` | `results/cache_v2/syncmate_small_selection_gu_v1` through `v5` | Versioned GU infrastructure gates. Their completed evidence is archived, not an active canonical Store. |
| **Experiment-owned Store requiring follow-up** | `experiments/bc_target_v2/{run_matrix,run_selection}.py` | default `results/cache_v2/bc_target_v2` plus optional `selection_artifacts` child | B/C score-bundle family; reusable only within its compatible recipe/producer contracts. Local score Store exists. |
| **Experiment-owned Store requiring follow-up** | `experiments/c_target_v1/run_cora_gcn.py` | default `results/cache_v2/c_target_v1` | C-target score-bundle family; legacy-compatible default `index.sqlite3`. Local score Store exists. |
| **Experiment-owned Store requiring follow-up** | `experiments/tracin_v2/run_formal_selection_gate.py`; B/C benchmark entrypoints | caller-supplied absolute Store roots / per-cell roots | No single tracked default root should be silently folded into the canonical Store. Local planning evidence exists; no general migration decision is implied. |
| **Historical/inactive** | local `.planning/**/index.sqlite`, local `results/runs/**/_evidence/**/store`, SSH `results/_archive_ssh_peer_layout_20260724/**` | evidence-local Store roots | Immutable diagnostic/canary evidence. No tracked active runner points at these exact paths. Retain unchanged. |
| **Out of Cache V2 scope** | Legacy `results/cache`, `results/selection_cache`, `results/score_cache` | Legacy hash/NPZ cache roots | Separate Legacy evidence governed by its own contracts. It was inventoried only as a boundary and not touched. |

The static consumer check found archive-name strings only in the retired-path validator and its tests, not in experiment configuration or runner arguments. It cannot prove that an untracked shell command has never named a historical root; that is why historical evidence remains retained rather than being treated as disposable.

## Local full-tree physical census

Every local physical Cache V2 index is ignored by Git, as intended for generated evidence. The local primary checkout contains **17 indexes**, **174 header/payload Artifact pairs**, and **2,555,904 index bytes**. All 17 local indexes opened as schema v1.

| Local location | Indexes | Artifact census | Index bytes | Classification / consumer reference |
|---|---:|---:|---:|---|
| `.planning/cache_v2_selection_materializer_20260714` and `.planning/tracin_sup_selection_20260720` | 5 | Selection: 3; Score: 2 | 540,672 | Historical local planning and TracIn evidence; no active tracked runtime consumer. |
| `results/cache_v2/bc_target_v2` | 1 | Score: 9 | 180,224 | B/C default score Store; `index.sqlite3`. |
| `results/cache_v2/c_target_v1` | 1 | Score: 6 | 143,360 | C-target default score Store; `index.sqlite3`. |
| `results/runs/gpu4090-gu-20260722/_evidence/full-v5/*/store` | 9 | Selection: 153 | 1,585,152 | Imported/frozen v5 full-GU evidence, not an active Store root. |
| `results/runs/gpu4090-gu-20260722/_evidence/gate-v5/store` | 1 | Selection: 1 | 106,496 | Imported/frozen v5 gate evidence, not an active Store root. |
| Current E8 worktree and the two other listed Codex worktrees | 0 | 0 | 0 | No `results/cache_v2` directory or CacheIndex. |

There is no local primary `results/cache_v2/index.sqlite` canonical index, and neither the local primary checkout nor the E8 worktree has `cache_v2/target_direct_formal_v2` or `results/runs/target_direct_formal_v2`.

## SSH active checkout and archive census

The SSH active checkout contains **25 indexes**, **196 header/payload Artifact pairs**, and **14,454,784 index bytes**. Exactly one index is active; the other 24 are inside the controlled peer-layout archive.

| SSH location | Indexes | Artifact census | Index bytes | Status / risk |
|---|---:|---:|---:|---|
| `results/cache_v2/index.sqlite` | 1 | Selection: 1 | 11,177,984 | **Active canonical Store.** Schema v1 by identical-SHA direct inspection; checksum above. It is shared by E8 by configuration, but contains no E8 target-direct Artifact. |
| `_archive_ssh_peer_layout_20260724/peer_roots/OpenGU-cache-v2-rollout/20260717` | 3 | Selection: 3; Score: 1; Prediction: 1; Evaluation: 1 | 327,680 | Historical Gate 3/4 rollout evidence. Keep archive-only. |
| `_archive_ssh_peer_layout_20260724/peer_roots/OpenGU-small-selection-gu/20260722` | 15 | Selection: 175 | 2,293,760 | Historical v4/v5 full and gate evidence. Keep archive-only. |
| `_archive_ssh_peer_layout_20260724/peer_roots/cache-v2-canary` | 3 | Selection: 3 | 319,488 | Historical canary/tamper/recheck evidence. Keep archive-only. |
| `_archive_ssh_peer_layout_20260724/peer_roots/cache-v2-materializer` | 3 | Selection: 11 | 335,872 | Historical materializer evidence. Keep archive-only. |
| **Archive subtotal** | **24** | **195** | **3,276,800** | No active root or runner promotion. |

Direct SSH path checks found neither `results/cache_v2/target_direct_formal_v2` nor `results/runs/target_direct_formal_v2`. Thus E8 has no live or archived target-direct formal Store to migrate, reconcile, or delete.

## Findings and decisions

1. **E8 is shared canonical at the Store/index level.** Both ScoreBundleStore and Selection use `results/cache_v2/index.sqlite`; stage names belong only in result/checkpoint/evidence/runtime/log paths.
2. **The broader inventory does not reveal a second active SSH Store.** Remote historical Stores are contained beneath the one approved archive tree. Local B/C and C-target stores are still experiment-owned and intentionally not silently assimilated.
3. **No migration is presently justified.** No E8 Artifact requires migration, reconciliation, or deletion: there is no target-direct result root and no evidence of a Store collision requiring a data operation.
4. **No deletion or cleanup is authorized or needed.** Legacy caches, local evidence Stores, remote archives, and the unrelated local user draft were all preserved.

## Explicit non-actions and follow-up boundary

- No Legacy cache cleanup; no all-repository cutover; no Store migration; no Artifact deletion.
- No formal GPU job, queue action, SyncMate collection, recipe/parameter change, or results-layout change.
- No merge, push, branch deletion, remote repair, or modification of the SSH checkout.
- A future global Store-governance task would need separate approval, an ownership matrix, exact producer/recipe compatibility review, a dry-run migration plan, and evidence-retention policy. This audit does not authorize any of those actions.
