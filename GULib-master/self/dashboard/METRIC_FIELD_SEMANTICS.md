# Metric Field Semantics

> Last updated: 2026-05-06
> Purpose: disambiguate similarly named F1 fields before Phase B results are read or plotted.

## Rule Of Thumb

Do not treat every field named `before` as the same baseline.

For Phase B node-unlearning runs, the paper-safe primary utility read is:

```text
relative_f1_drop = baseline_f1_after(k=5 random) - attack_f1_after
```

This read deliberately avoids `f1_before`.

## Field Map

| Field | File | Current source | Method-agnostic? | Use in Phase B? |
|---|---|---|---|---|
| `attack.json.results[*].f1_before` | `attack.json` | `method.poison_f1` via `attack/pipeline_adapter.py` | No. Node tasks often leave it `None`; old fallback values can be post-unlearning artifacts. | No. Treat as legacy/optional. |
| `attack.json.results[*].f1_after` | `attack.json` | post-unlearning F1 from `method.average_f1` | No, by definition method-specific. | Yes, for utility reads and relative F1. |
| `collateral.json.results[*].perf_before` | `collateral.json` | `eval_collateral.py` pre-trains `model_before` using the current method's `train_only` path | Not guaranteed. For GraphEraser/GraphRevoker this may be a SISA/shard-trained before model. | Use as a sanity range only unless the analysis explicitly wants method-specific before. |
| `collateral.json.results[*].perf_retrain` | `collateral.json` | exact retrain after excluding selected nodes, using current method's retrain path | Method-specific for shard methods. | Yes, paired with `perf_unlearn` for retrain gap. |
| `collateral.json.results[*].perf_unlearn` | `collateral.json` | approximate unlearned model after deleting selected nodes | Method-specific. | Yes. |
| `predictions.npz.logits_before` | `predictions.npz` | same model as `collateral.perf_before` | Same caveat as `perf_before`. | Yes for offline recompute, but preserve the caveat. |

## Intended But Not Yet Materialized Field

`canonical_f1_before` would mean:

```text
F1(clean vanilla base model trained on the original train mask)
key = dataset + backbone + seed + split + model/training hyperparameters
```

That value should be independent of GU method. It is the cleanest denominator
for raw `F1_before - F1_after` style claims, but Phase B does not currently
persist it as a first-class artifact.

## GraphEraser / SISA Caveat

GraphEraser `train_only` is not "do nothing." It partitions the graph, trains
shard models, and aggregates them without deleting nodes. That is a valid
GraphEraser-before state, but it is not the same object as a vanilla full-graph
GCN/GAT/GIN model.

Therefore:

- GraphEraser `method_perf_before` / `perf_before` is reasonable for a
  GraphEraser-internal comparison.
- It is not a canonical selector model and should not define TracIn/Hybrid
  selection semantics.
- It should not be mixed with vanilla before values in a cross-method raw F1
  drop table.

## Safe Reporting Policy

Use these names in paper notes and scripts:

| Name to use | Meaning |
|---|---|
| `attack_f1_after` | F1 after the strategy-driven unlearning run. |
| `baseline_f1_after` | F1 after k=5 random unlearning baseline. |
| `relative_f1_drop` | `baseline_f1_after - attack_f1_after`; primary cross-method utility read. |
| `method_perf_before` | Method-specific before model from `train_only`; may be SISA for shard methods. |
| `canonical_f1_before` | Vanilla base model before; only use after a separate canonical artifact exists. |

Avoid writing "f1_before" without one of these qualifiers.
