# GraphRevoker Sanity Run — Pre-Phase-B Feasibility Gate

> Purpose: verify GraphRevoker runs end-to-end before promoting it into the 6-method Phase B matrix (paper §4.2).
> Branch: `nips-prep`
> Created: 2026-05-05

## Why a gate is needed

`unlearning_manager.py:40` currently aliases `"GraphRevoker"` → `grapheraser` class. So the legacy round2 / step0 data labelled "GraphRevoker" was actually GraphEraser. The real `graphrevoker` class (`unlearning/unlearning_methods/GraphRevoker/graphrevoker.py:16`) has its own partition / aggregator / trainer modules but has never been exercised through the official dispatcher path. We need a 30-second sanity run to confirm:

1. The class instantiates with the current arg set
2. Inherited `Shard_based_pipeline.run_exp` correctly resolves to graphrevoker's overridden methods (partition/aggregator)
3. End-to-end produces a sensible attack.json + collateral.json + predictions.npz

## Step 1 — un-alias the dispatcher (1 line)

File: `unlearning_manager.py:40`

```python
# before
"GraphRevoker": grapheraser,

# after
"GraphRevoker": graphrevoker,
```

The `graphrevoker` class is already imported on line 14, so no import change needed.

## Step 2 — run the sanity yaml

```powershell
# from repo root, gnn env
python experiments/run.py experiments/configs/sanity_graphrevoker.yaml --force
```

Expected wall-clock: 20–60 seconds (cora, single seed, single strategy).

`--force` bypasses skip-if-exists; this is the **first** GraphRevoker run on the new dispatcher, so there's no prior output, but `--force` also helps re-run cleanly if you iterate.

## Step 3 — pass / fail criteria (all four must hold)

| Check | Expected | Where to look |
|---|---|---|
| Process exits cleanly | `rc=0`, `Summary` block shows `completed: 1` | stdout |
| Output files written | 4 files present | `results/runs/cora_GCN_r0.05/GraphRevoker_random/seed42/{attack.json, collateral.json, predictions.npz, _meta.json}` |
| F1 sane | within `[0.78, 0.88]` (baseline ≈ 0.84) | `attack.json::*::f1_after_unlearn` (or similar; check key) |
| MIA AUC sane | finite, > 0, not exactly 0.000 | `attack.json::*::mia_auc` (Phase A.3 already fixed `Shard_based_pipeline.py:177`) |

Selected node count: should be `round(0.05 × |V_train|)` ≈ 70 on cora (sanity check that strategy is honoring `unlearn_ratio`).

## Step 4 — failure modes and likely root causes

| Symptom | Likely cause | Fix |
|---|---|---|
| `KeyError: 'num_opt_samples'` | param not in args dict | already in `parameter_parser.py:144`; ensure parser is invoked |
| `AttributeError` on partition / aggregator method | inherited `run_exp` uses a method GraphRevoker doesn't override but expects in subclass shape | check `graphrevoker.py` class methods vs `Shard_based_pipeline.run_exp` call sites |
| F1 ≈ identical to GraphEraser baseline | dispatcher change didn't take effect | confirm edit on line 40, restart Python (no cached module imports) |
| `mia_auc = 0.000` | Phase A bug regression or stale cache | re-run with `--force`, check `Shard_based_pipeline.py:177` not re-commented |
| F1 way out of `[0.78, 0.88]` (e.g., 0.5) | something deeper wrong (training config, GraphRevoker-specific param missing) | inspect logs in `log/GraphRevoker/cora/GCN/` |

## Step 5 — after pass

1. Append a `V-2026-05-XX-NN` entry to `self/dashboard/VALIDATION_LOG.md` documenting:
   - dispatcher edit (sha)
   - sanity F1 / MIA / wall-clock
   - "GraphRevoker now feasible for Phase B"
2. Remove "pending feasibility gate" annotation from:
   - `report/paper/outline_v2.md` `Locked decisions` block
   - `report/paper/outline/04_experimental_setup.md` (4.2 paragraph)
3. Add `GraphRevoker` to the `methods:` list in:
   - `experiments/configs/phase_b_cora_gcn.yaml`
   - `experiments/configs/phase_b_cora_gat.yaml`
   - (skip arxiv — keep B.2 budget tight)
4. Update `self/dashboard/EXPERIMENT_DASHBOARD.md` §1 Phase B notes if relevant

## Step 6 — fallback if it fails

If GraphRevoker can't be brought up cleanly within ~30 minutes of debugging, drop it. The 5-method plan still holds; only Partition-based stays at n=1.

Files to revert (paper outline):
- `outline/04_experimental_setup.md` — remove GraphRevoker from 4.2
- `outline/05_1_vulnerability_fingerprint.md` — Partition reverts to n=1, "convergent pair" prediction removed
- `outline/06_conclusion_limitations.md` — L6 reverts to "5 methods"
- `outline/A3_alpha_synergy.md`, `outline/A5_ratio_sweep.md` — counts back to 5
- `sections/abstract.md` — back to 5 methods, drop GraphRevoker
- `outline_v2.md` — Locked decisions block update

(Ping me; reversion takes ~5 min.)

## Reference: legacy round2 data — read with caveat

`results/evaluation/step0/method_compatibility.json:262-287` shows:

| ratio | F1 | wall-clock |
|---|---|---|
| 0.005 | 0.8413 | 8.4s |
| 0.02 | 0.8487 | 10.2s |
| 0.05 | 0.8413 | 10.0s |
| 0.1 | 0.8358 | 10.6s |
| 0.2 | 0.8247 | 9.6s |

**Caveat**: this data was collected when `unlearning_manager.py` aliased `"GraphRevoker"` to `grapheraser`. So these numbers are the *GraphEraser* performance under a `GraphRevoker` label. They are useful only as an **upper bound** for plausible cora/GCN/r=0.05 F1. If the un-aliased GraphRevoker produces F1 wildly outside [0.78, 0.88], something is wrong.
