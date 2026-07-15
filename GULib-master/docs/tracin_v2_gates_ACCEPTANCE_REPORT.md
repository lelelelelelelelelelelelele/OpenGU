---
title: TracIn V2 UNSTABLE Gates — Acceptance Report
date: 2026-07-15
status: conditional-prototype-pass
branch: codex/experiment-tracin-v2-gates-20260715
parent: codex/docs-framework-briefing-20260714
---

# TracIn V2 UNSTABLE Gates — Acceptance Report

## Decision

**CONDITIONAL PROTOTYPE PASS; KEEP UNSTABLE.**

The isolated multi-checkpoint scorer, Recipe identity, Cora selector diagnostic,
same-machine repeat, and reduced cross-machine selector gate work. The legacy
TracIn strategy, Hybrid, default runner, and all Legacy caches were left
untouched.

This is not a production acceptance. A formal Cache V2 ScoreArtifact/store,
Hybrid parent gate, and GU canary do not exist yet. The Adam lane is explicitly
an `adam_lr_weighted_gradient_heuristic`, not a proof that Adam follows the
original SGD/GD TracIn derivation.

## Implemented isolated lane

- `experiments/tracin_v2/core.py`: multi-checkpoint eval/self scores, legacy
  replay, finite/shape checks, stable `score desc, node_id asc` ordering.
- `experiments/tracin_v2/recipe.py`: UNSTABLE Recipe with full hashes for data,
  `T`, `E`, model/checkpoints, parameter schema, optimizer/loss semantics,
  target profile, seeds, numerics, and fixed-graph graph semantics.
- `experiments/tracin_v2/run_cora_gate.py`: public-split Cora GCN trajectory,
  post-epoch checkpoints weighted by the LR of the preceding optimizer update,
  attack-safe validation target, single-final/deployed/self/IF references, and
  atomic external JSON report.
- `tests/test_tracin_v2_unstable.py`: formula, sign, collapse, tie, manifest,
  mutation, non-finite, negative-weight, and invalid-node gates.

The lane is not registered in `AttackManager`, `BUILTIN_STRATEGIES`, Cache V2
producer registry, or the default experiment runner. Output under known Legacy
cache roots is rejected.

## Gate status

| Gate | Status | Evidence |
|---|---|---|
| G0 formula fixture | PASS | Two-checkpoint eval/self hand calculation; single-checkpoint collapse; legacy sign; deterministic ties |
| G1 Recipe identity | PARTIAL PASS | Semantic mutations miss and strict hashes/manifests fail closed; formal ScoreArtifact/store/conflict gate remains absent |
| G2 Cora selector | PROTOTYPE PASS | Local CPU SGD semantic lane and Adam compatibility lane completed |
| G3 Legacy replay/isolation | PARTIAL PASS | Legacy formula replayed; no Legacy import/cache access; formal before/after store snapshot gate remains absent |
| G4 cross-machine | REDUCED PASS | `last_layer`, local CPU vs remote CPU; distinct Recipe, stable ranking/top-k |
| G5 Hybrid | NOT RUN | No V2 ScoreArtifact parent yet |
| G6 GU canary | NOT RUN | Default/experimental runner integration intentionally absent |

## Test suite

Local (`torch 2.2.1+cu121`, PyG 2.6.1):

```text
75 passed in 2.09s
```

Remote `autodl-opengu` isolated sibling worktree (`torch 2.1.2+cu118`,
PyG 2.6.1):

```text
75 passed in 2.77s
```

## G2: Cora all-parameter Adam compatibility gate

Setting:

```text
Cora Planetoid public split
T = 140 public training nodes
E = 500 validation nodes (attack-safe holdout; disjoint from T)
GCN hidden = 16
optimizer = Adam, 100 epochs
post-epoch checkpoints = [1, 10, 25, 50, 100]
weights = LR used by the preceding update
parameter scope = all trainable
k = 7
LiSSA reference = deterministic full-batch Neumann recursion, 50 iterations
```

Model test accuracy was `0.8110`.

| Pair | Spearman | Kendall | Jaccard@7 | Reading |
|---|---:|---:|---:|---|
| deployed cross-final vs V2 | 0.2130 | 0.1457 | 0.0000 | Legacy residual direction selects a different set |
| single-final eval vs V2 | 0.9699 | 0.8608 | 0.5556 | Final frame is strongly correlated, but multi-checkpoint changes 2 of 7 nodes |
| V2 vs eval-IF reference | 0.9107 | 0.7609 | 0.5556 | V2 remains close to the same target-aware axis, but is not identical |

The historical approximately 70% result is not reproduced here: that result
used the OpenGU diagnostic split/model. This gate uses a standalone Planetoid
public split and therefore records `historical_overlap_comparable=false`.

The important conclusion is narrower: the old residual formula is not recovered
by multi-checkpoint TracIn, while the single-final eval proxy remains highly rank
correlated but cannot substitute for the full trajectory.

## SGD semantic lane

The 30-epoch SGD run completed with the same five post-epoch checkpoint
semantics, but test accuracy was only `0.1520`. It is retained only as a formula
and checkpoint/LR semantic sanity, not selector-quality evidence.

## Determinism

Two full all-parameter Adam runs on the local machine produced identical:

- Recipe hash;
- checkpoint manifest and state hashes;
- every score value;
- every ordered top-k selection;
- test accuracy.

Only wall-clock `compute_seconds` differed.

## Reduced G4 cross-machine gate

The same `last_layer` Adam profile was run locally and on the remote CPU.
Different Torch/build/numerics profiles correctly produced different Recipe and
checkpoint hashes. Float values were close but not forced into one Artifact:

| Score | max absolute difference | Spearman | Kendall | ordered top-k equal |
|---|---:|---:|---:|---|
| deployed cross-final | 1.0133e-6 | 1.0 | 1.0 | yes |
| single-final eval | 2.9802e-8 | 1.0 | 1.0 | yes |
| TracInCP LR | 9.3132e-10 | 1.0 | 1.0 | yes |
| TracInCP uniform | 1.1921e-7 | 1.0 | 1.0 | yes |
| TracInCP self | 7.4506e-9 | 1.0 | 1.0 | yes |
| eval-IF reference | 1.4901e-8 | 1.0 | 1.0 | yes |

One earlier remote run is excluded: an interrupted `scp` left a partial Cora
`data.pt`. The corrupt file was confined to the sibling worktree, removed after
an absolute-path check, and regenerated from the eight downloaded raw files.
No result from that attempt is used above.

## Evidence files

The gate JSON files live outside the repository under the thread visualization
workspace. SHA-256:

| File | SHA-256 |
|---|---|
| `tracin_v2_cora_adam_gate_final.json` | `cd1c100e59ed1e40317cb358439158f74fdfa21ce1caceb0eec8df9c113fd4d1` |
| `tracin_v2_cora_adam_gate_final_repeat.json` | `e296e0cb4086113fbe6d63f184cc2ce0685916ff887fbad9f64d2c91833bc3bd` |
| `tracin_v2_cora_sgd_semantic_final.json` | `cb730d9782e5f462792ec4f2c0c8d26ebdd3ea9f4c7692ff001185cbceb58554` |
| `tracin_v2_cora_adam_lastlayer_gate_final_local.json` | `3d6465a65870305c046ef4725076be698b1a1f087bb98eca45b8651268c18085` |
| `tracin_v2_cora_adam_lastlayer_gate_final_remote.json` | `7c45d6b12803a24eab60ef5c0279cec115bb21c9f3329c5bb2735abbb334b0a5` |

## Promotion blockers

1. Build a formal immutable ScorePayload/ScoreArtifact store with cold/warm
   exact hit and same-Recipe/different-content conflict quarantine.
2. Add a Legacy directory before/after snapshot gate, not only path guards and
   import isolation.
3. Decide the canonical OpenGU checkpoint capture entry point and whether Adam
   remains a heuristic or gets an update-aware estimator.
4. Run the OpenGU canonical split/model profile; do not compare this public-split
   gate directly to historical `0.7419`.
5. Add Hybrid parent identity/miss tests before any Hybrid run.
6. Only then run a single-seed isolated GU canary; default runner registration
   remains forbidden.

Until these are closed, the correct name is `tracin-v2-unstable`, not stable or
production TracIn.
