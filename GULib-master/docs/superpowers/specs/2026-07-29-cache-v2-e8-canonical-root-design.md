# Cache V2 E8 Canonical Root Design

## Work Block

- Parent: `main@ca2207e6145c8e9391232d25a456b90e8f00943e`
- Branch: `codex/cache-v2-e8-canonical-root`
- Worktree: `C:/Users/ADMIN/.codex/worktrees/e8-cache-root/OpenGU`
- Closeout: focused commits on the branch; no merge, push, remote experiment,
  Cache migration, or Cache deletion without separate user direction

Expected implementation paths:

- `experiments/configs/syncmate_target_direct_formal_v2.yaml`
- `experiments/target_direct_v1/syncmate_stage.py`
- `experiments/target_direct_v1/run_selection.py`
- `experiments/c_target_v1/score_store.py`
- `scripts/syncmate/syncmate.py`
- `tests/test_c_target_v1.py`
- `tests/test_target_direct_syncmate_stage.py`
- `tests/test_syncmate.py`
- `reports/target_direct_formal_preflight_AUDIT_REPORT.md`
- `reports/target_direct_formal_preflight_AUDIT_REPORT.html`

The follow-up inventory may add:

- `reports/cache_v2_store_scope_inventory_AUDIT_REPORT.md`
- `reports/cache_v2_store_scope_inventory_AUDIT_REPORT.html`

## Problem

Cache V2 already defines Cache identity and physical storage as independent
from experiment, YAML, batch, and stage identity. E8 violates that invariant
in its orchestration layer:

- the frozen YAML declares separate experiment-owned Score and Selection
  roots;
- `syncmate_stage.py` appends `dataset-seed` stage names to both roots;
- `ScoreBundleStore` opens `index.sqlite3`, while Selection materialization
  opens the canonical `index.sqlite`.

Consequently, identical Recipes outside the same E8 stage cannot resolve the
same indexed Artifact. The target-direct Recipe itself already binds the
dataset, split, candidates, selector model, training seed, checkpoint state,
algorithm version, and budget semantics. Directory isolation adds no valid
identity and prevents intended reuse.

The local and SSH active checkouts were audited before this design. Neither
contains `results/cache_v2/target_direct_formal_v2` or
`results/runs/target_direct_formal_v2`; the SSH canonical index has zero
target-direct Artifacts and zero target-direct consumer references. No E8
Artifact migration or deletion is required.

## Phase 1: E8 Canonical Store Conformance

### Configuration

Replace:

```yaml
score_cache_root: results/cache_v2/target_direct_formal_v2/score
selection_store_root: results/cache_v2/target_direct_formal_v2/selection
```

with:

```yaml
cache_v2_root: results/cache_v2
```

The reviewed E8 loader must require that this value resolve exactly to the
active checkout's `results/cache_v2`. A descendant, sibling, absolute external
path, experiment name, or stage name must fail closed. Remove the
experiment-shaped `claims.cache_v2_identity` field; Artifact Recipes and
Artifact IDs remain the only Cache identities.

Experiment-owned paths remain unchanged under
`results/runs/target_direct_formal_v2`:

- Selection cold/warm summaries and receipts;
- target checkpoints;
- generated manifests, GU YAML, and logs;
- runtime files;
- GU result artifacts.

### Stage Path Derivation

`_stage_paths()` must return the same canonical Cache root for both
`score_store` and `selection_store` for every dataset/seed stage. Stage names
continue to scope only result, checkpoint, evidence, runtime, and log paths.

The target-direct selection command may retain its existing
`--cache-root` and `--selection-cache-root` arguments for compatibility, but
the E8 orchestrator must pass the same canonical absolute path to both.
`run_selection.py` must reject unequal resolved roots so direct callers cannot
recreate the split Store.

### Shared SQLite Index

`ScoreBundleStore` must accept an optional caller-supplied `CacheIndex`.
Its existing default `root/index.sqlite3` remains unchanged for historical
BC/C-target consumers in this branch. E8 supplies
`CacheIndex(cache_v2_root / "index.sqlite")`, so its Score and Selection
Artifacts share the canonical Cache V2 index and its type-aware uniqueness
constraints.

The supplied index must resolve below the supplied Store root and use the
existing Cache V2 schema. No lookup may scan another root or fall back to
Legacy caches.

### SyncMate and Reports

Changing the frozen YAML requires recalculating
`TARGET_DIRECT_CONFIG_SHA256`. SyncMate recipe argv, collected result roots,
artifact allowlists, and queue semantics remain unchanged.

The target-direct preflight audit Markdown and HTML must stop describing
experiment-isolated Cache roots as a passing condition. They must state that
E8 consumes the canonical shared Store while its reviewable run products
remain isolated under `results/runs/target_direct_formal_v2`.

## Phase 1 Tests

Tests must prove:

1. the frozen E8 config exposes only `cache_v2_root` for Cache storage;
2. the root resolves exactly to checkout-local `results/cache_v2`;
3. old split-root keys and non-canonical descendants fail closed;
4. two different E8 stages receive identical Score and Selection Store roots;
5. direct target selection rejects unequal Score and Selection roots;
6. a ScoreBundle stored through the injected canonical `CacheIndex` is an
   exact warm hit from a second `ScoreBundleStore` instance without calling
   its producer;
7. Selection materialization can use the same `index.sqlite` without schema
   conflict;
8. SyncMate binds the new exact YAML SHA-256;
9. Markdown and HTML reports agree on the canonical Cache conclusion.

Implementation follows red-green-refactor: each new behavioral assertion is
observed failing before production code changes, then the closest tests and
the complete affected test files are run green.

## Phase 1 Acceptance

- No Cache path contains `target_direct_formal_v2`, dataset, seed, or stage.
- E8 Score and Selection use one canonical root and `index.sqlite`.
- Recipe fields and Artifact ID computation are unchanged.
- `results/runs/target_direct_formal_v2` layout is unchanged.
- No existing Cache payload, header, index row, or Legacy source is modified,
  moved, imported, retired, or deleted.
- Targeted target-direct, C-target Store, manifest, and SyncMate tests pass.
- The frozen YAML hash and both audit report formats match the final source.

## Phase 2: Repository-Wide Store Scope Inventory

After Phase 1 is committed, perform a read-only inventory of tracked Cache V2
callers/configs and the current local and SSH active Store state. Classify each
entry as:

1. **canonical formal consumer** — already uses `results/cache_v2`;
2. **explicit isolated canary** — isolation is part of a bounded validation
   contract and must not be interpreted as a formal experiment default;
3. **experiment-owned Store requiring follow-up** — a non-canary producer or
   consumer prevents cross-experiment reuse and needs a separately approved
   cutover/migration plan;
4. **historical or inactive reference** — retained only for provenance and not
   an active Cache owner.

The inventory records the owning entry point, configured root, index filename,
Artifact types, Recipe/producer family, local and SSH payload/index counts,
consumer references, and migration risk. It produces matching Markdown and
HTML audit reports. It does not edit configs, import Artifacts, rebuild
indexes, move payloads, delete directories, or run GPU experiments.

## Non-Goals

- Repository-wide Cache cutover in the E8 implementation commit.
- Legacy Cache retirement or fallback changes.
- Cross-GPU Cache synchronization.
- Changing target-direct scientific parameters, Recipes, checkpoints,
  Selection semantics, GU matrices, result schemas, or SyncMate collection.
- Treating experiment output directories as Cache storage.
