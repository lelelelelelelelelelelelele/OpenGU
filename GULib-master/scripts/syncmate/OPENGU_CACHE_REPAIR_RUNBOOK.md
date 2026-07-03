# OpenGU Cache And Result Repair Runbook

This runbook is the OpenGU-specific repair profile for SyncMate. It describes
how a local collector, a runner/server, and their AI agents should coordinate
when a result is discovered to be wrong after it has already been produced or
collected.

It is guidance, not an automatic deletion command. Prefer plan, archive,
verify, rerun, and recollect over silent destructive cleanup.

## Mental Model

OpenGU has four different state layers that can disagree:

| Layer | Path | Meaning | Trust rule |
|---|---|---|---|
| Runner result artifacts | `results/runs/<cell>/<method_strategy>/seedN/` | `attack.json`, `collateral.json`, `predictions.npz`, `_meta.json` from one experiment leaf | Complete only if files parse and `_meta.json` fingerprint matches the intended config |
| ResultCache | `results/cache/*.json` | Full attack-run metrics for one `(method, dataset, model, ratio, seed, strategy, ...)` config | Method/metric/output cache; hash name is not human semantic |
| SelectionCache | `results/selection_cache/*.json` | Selected node IDs for one strategy config | Cross-GU-method selector cache; hash name is not human semantic |
| Collector trusted state | `.syncmate/artifact_index.json`, `.syncmate/results_table.*` | Checksummed and parsed artifacts after collection | Trusted only after SHA-256 verification |

The two cache directories are not interchangeable:

- `results/cache/` answers: "Can I reuse this finished attack result and its
  metrics?"
- `results/selection_cache/` answers: "Can I reuse this selected node set for
  this strategy config?"

## Decision Matrix

| Problem found | Clear or quarantine runner `results/runs`? | Invalidate `results/cache`? | Invalidate `selection_cache`? | Notes |
|---|---:|---:|---:|---|
| Metric/evaluator bug, such as F1 drop, MIA AUC, retrain gap, collateral metrics | Yes, affected leaves | Yes, affected configs | No | The selected nodes are still valid; only downstream metrics are wrong. |
| GU method bug, such as GraphRevoker/GraphEraser/GIF/GNNDelete/IDEA method behavior | Yes, affected method leaves | Yes, affected method configs | No, unless selector also changed | This is the user's "revoker class" case: result cache and result artifacts are the primary repair targets. |
| Selector bug, such as TracIn gradient/scoring, IM formula, Hybrid fusion, PageRank/degree implementation | Yes, all leaves using the bad strategy output | Yes, all downstream method configs using that strategy output | Yes, affected strategy configs | This is the user's "TracIn wrong" case. Bad selected nodes poison all downstream GU metrics. |
| Dataset split, node indexing, preprocessing, train/val/test mask semantics changed | Yes, affected dataset/cell | Yes | Yes | Node IDs may no longer mean the same thing. Method checkpoints may also be stale. |
| Config mistake, such as wrong ratio, alpha, strategy, seed, method list, or yaml override | Yes, wrong leaves | Usually yes for wrong configs that may be reused | Only if the mistake changed selected nodes and cache key cannot distinguish it | A new correct config may produce a new hash, but old wrong artifacts can still be collected or trusted if not marked invalid. |
| Architecture shape change, such as `gcn_hidden` or `gcn_num_layers` | Yes, affected leaves | Usually yes; ResultCache key includes these fields | Usually no | Also clear method checkpoint/data caches that do not encode shape, such as `data/GNNDelete/`, `data/UTU/`, and relevant partition/checkpoint dirs. |
| Corrupt or interrupted artifact file | Yes, that leaf | Only if the cache entry was written from the corrupt/incomplete run | No | `experiments/run.py` can rerun corrupt/stale leaves, but SyncMate trusted state must also stop trusting old collected copies. |

Rule of thumb:

```text
metric or GU method wrong -> result artifacts + ResultCache
selector or node-ID semantics wrong -> SelectionCache + all downstream result artifacts + ResultCache
collector trust wrong -> .syncmate index/results table must be rebuilt after artifact quarantine
```

## OpenGU Key Details

`ResultCache` identity is defined in `attack/result_cache.py`. The current key
includes dataset, base model, unlearning method, ratio/k, seed, strategy, task
flags, GCN architecture, `alpha`, `hybrid_alpha`, Hybrid/IM hyperparameters,
and `im_selector_seed`.

`SelectionCache` identity is defined in `attack/selection_cache.py` and
`attack/attack_manager.py`. It hashes a strategy config containing dataset,
base model, ratio, seed anchor, strategy name, k, split flags, graph
fingerprint, and strategy-parameter fingerprint. The key intentionally does
not include GU method, because one selected node set can be reused by multiple
unlearning methods.

TracIn and Hybrid deserve special care:

- A pure TracIn scoring bug invalidates `selection_cache` entries for
  `strategy_name=tracin` and every result leaf/cache entry generated from those
  selected nodes.
- If Hybrid uses the same broken TracIn score path, invalidate Hybrid
  selection entries and downstream results too.
- If only a TracIn CLI/config parameter was wrong and the key already encodes
  it, the correct rerun can create a separate cache entry, but the wrong entry
  still needs an invalidation record so collectors do not continue to trust it.

## Two-Sided Repair Protocol

### 1. Freeze The Affected Scope

Before collecting more data, name the scope in structured terms:

```yaml
bug_id: 2026-07-03-tracin-gradient-example
reason: tracin selected nodes were computed with the wrong gradient score
datasets: [cora]
base_models: [GCN]
ratios: [0.05]
methods: [GIF, GNNDelete, GraphEraser, GraphRevoker]
strategies: [tracin, hybrid]
seeds: [42, 212, 722]
runner_nodes: [gpu4090]
cache_layers: [selection_cache, result_cache, results_runs, syncmate_trust]
remote_action: quarantine_then_rerun
```

If the issue is a GraphRevoker/GU-method bug, the same record should usually
look like:

```yaml
cache_layers: [result_cache, results_runs, syncmate_trust]
methods: [GraphRevoker]
strategies: [random, degree, pagerank, tracin, im, hybrid]
```

### 2. Preserve Evidence

On the collector:

```bash
python scripts/syncmate/syncmate.py handoff-pack --write
python scripts/syncmate/syncmate.py index --check
python scripts/syncmate/syncmate.py results --write --check
python scripts/syncmate/syncmate.py trace --check
```

Save the generated `.syncmate/` evidence before changing local landings or
trusted indexes.

### 3. Build A Repair Plan

For every affected leaf, identify:

- runner node id
- result leaf path under `results/runs/<cell>/<method_strategy>/seedN/`
- cache layer(s) to invalidate
- whether the selector output is bad or only the downstream method/metric is bad
- whether method-local checkpoint/data caches are stale
- rerun command or yaml config that will regenerate the leaf

Do not identify cache entries by hash filename alone. Inspect the `config`
field inside each cache JSON and match it to the structured scope.

### 4. Runner-Side Action

Runner-side action should be explicit and preferably reversible:

1. Move affected `results/runs/<cell>/<method_strategy>/seedN/` leaves to a
   dated quarantine folder, or delete only after a backup exists.
2. Invalidate matching `results/cache/*.json` entries whose `config` matches
   the affected method/metric scope.
3. Invalidate matching `results/selection_cache/*.json` entries only when the
   selected node IDs are wrong.
4. Clear method-local checkpoint/data caches only when their semantics are
   stale, especially for architecture-shape changes.
5. Rerun the exact intended yaml/cell.
6. Re-run the project gate for the regenerated result root.

For selector bugs, remember the fan-out:

```text
bad SelectionCache entry
  -> bad selected_nodes
  -> bad attack.json/collateral.json for every GU method using that strategy
  -> bad ResultCache entries for those method/strategy/seed configs
  -> bad collector trusted rows if already collected
```

### 5. Collector-Side Action

The collector must not keep trusting previously collected copies after a runner
has invalidated them.

Current SyncMate can archive orphaned peer state, verify checksums, and rebuild
trusted result tables, but it does not yet implement project-aware invalidation.
Until that exists, treat the collector cleanup as a manual/profile action:

1. Quarantine affected local landing leaves under
   `results/runs/<node_id>/<cell>/<method_strategy>/seedN/`.
2. Rebuild or rewrite `.syncmate/artifact_index.json` so invalid artifacts are
   no longer trusted.
3. Regenerate `.syncmate/results_table.json` and `.syncmate/results_table.csv`
   from the remaining trusted index.
4. Collect regenerated runner artifacts.
5. Verify and gate before using the results downstream.

Normal verification sequence:

```bash
python scripts/syncmate/syncmate.py remote-status <node_id> --apply
python scripts/syncmate/syncmate.py collect <node_id> --diff
python scripts/syncmate/syncmate.py collect <node_id> --apply
python scripts/syncmate/syncmate.py verify <node_id> --apply
python scripts/syncmate/syncmate.py results --write --check
python scripts/syncmate/syncmate.py trace --check
python scripts/syncmate/syncmate.py gate --require-preflight --require-verify --require-results
```

## Future SyncMate State Model

The durable version should make invalidation a first-class sync state, not an
ad hoc deletion.

Suggested statuses:

```text
trusted
invalidated
prune-requested
pruned-local
pruned-remote
rerun-needed
rerun-complete
recollected
accepted
```

Suggested future commands:

```bash
python scripts/syncmate/syncmate.py invalidate-plan --profile opengu --scope <scope.yaml>
python scripts/syncmate/syncmate.py invalidate-export <bug_id>
python scripts/syncmate/syncmate.py invalidate-import <request.json>
python scripts/syncmate/syncmate.py repair-plan --profile opengu --bug-id <bug_id>
python scripts/syncmate/syncmate.py repair-apply --profile opengu --bug-id <bug_id> --confirm <bug_id>
```

The intended flow is:

```text
collector detects bad result
  -> writes invalidation request with scope and evidence
  -> runner imports request and performs a dry-run repair plan
  -> runner archives/invalidates/reruns
  -> collector recollects and verifies
  -> both sides converge on accepted state
```

## Do Not

- Do not rename hash-named cache files.
- Do not edit cache JSON by hand to "fix" metrics or selected node IDs.
- Do not clear `selection_cache/` for a pure metric bug.
- Do not keep collector `.syncmate/artifact_index.json` entries for artifacts
  that the runner has invalidated.
- Do not rely on `results/runs` presence alone; use `_meta.json`,
  config fingerprints, SHA-256 verification, and the trusted index.
- Do not make generic SyncMate silently delete remote cache. OpenGU cache repair
  needs a profile, a scope, and a reversible plan.
