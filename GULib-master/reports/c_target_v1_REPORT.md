---
title: C Target GIF–TracIn Approximation Local Experiment
date: 2026-07-16
status: accepted-single-seed
dataset: Cora
model: GCN
seed: 2024
---

# C Target GIF–TracIn Approximation Local Experiment

## Verdict

The local Cora/GCN experiment is implemented, cached, and reproducible. It performs **no per-candidate exact retraining**.

The main result is not simply “TracIn works” or “TracIn fails.” It is more precise:

> Replacing (H^{-1}g_E) by (g_E) works well when the source is held fixed. Replacing the full graph source (mathrm{grad1}-mathrm{grad2}) by (mathrm{grad1}) or (g_v) does not.

On the accepted seed-2024 run, the graph-aware Hessian-free score

\[
P_{\mathrm{graph}}(v)=
\langle \mathrm{grad1}_v-\mathrm{grad2}_v,g_E\rangle
\]

recovered 6 of the full GIF GT top-7 candidates: Jaccard@7 = 0.7500, common fraction = 0.8571, Spearman = 0.9658. By contrast, the no-grad2 approximate GT recovered only 1/7, and both single-final and multi-checkpoint point TracIn recovered 0/7 against full GIF GT.

## Scope and definitions

| Item | Accepted setting |
|---|---|
| Dataset / model | Planetoid Cora / two-layer GCN |
| Candidate pool | all 140 standard `train_mask` nodes |
| Target (E) | 500 `val_mask` nodes, mean cross-entropy |
| Seed | 2024 |
| Training | Adam, 200 epochs, lr 0.01, weight decay 0.0005 |
| Checkpoints | 1, 10, 25, 50, 100, 200 |
| TracInCP weights | learning rate used by the preceding update |
| Affected set | candidate plus undirected two-hop neighbors |
| Parameters | all trainable GCN parameters |
| IHVP | one shared LiSSA solve, 20 iterations, scale 25, damp 0.01 |
| Ranking | score descending, node ID ascending tie-break |
| Main top-k | (k=\lfloor140\times0.05\rfloor=7) |

The score hierarchy is:

| ID | Score | Meaning |
|---|---|---|
| GT-full | \(\langle \mathrm{grad1}-\mathrm{grad2},H^{-1}g_E\rangle\) | operational full graph-aware GIF reference |
| GT-simple | \(\langle \mathrm{grad1},H^{-1}g_E\rangle\) | no-grad2 approximate GT |
| R-point | \(\langle g_v,H^{-1}g_E\rangle\) | candidate-only point IF reference |
| P-graph | \(\langle \mathrm{grad1}-\mathrm{grad2},g_E\rangle\) | graph-aware Hessian-free proxy |
| P-simple | \(\langle \mathrm{grad1},g_E\rangle\) | no-grad2 Hessian-free proxy |
| P-point | \(\langle g_v,g_E\rangle\) | final-checkpoint point proxy |
| TracInCP-point | \(\sum_c w_c\langle g_v(\theta_c),g_E(\theta_c)\rangle\) | multi-checkpoint point proxy |
| legacy | \(\langle g_v,-\sum_{j\in T}g_j\rangle\) | old training-residual negative control |

For every candidate, `grad1` uses the affected-set sum loss on the original graph. `grad2` uses affected neighbors on a graph whose edges incident to the candidate have been removed. Both gradients are evaluated at the same trained parameters; this is a forward/backward intervention, not retraining.

## Main results

| Reference | Candidate score | Top-7 intersection | Jaccard@7 | Common fraction | Spearman | Kendall | Interpretation |
|---|---|---:|---:|---:|---:|---:|---|
| GT-full | GT-simple | 1 | 0.0769 | 0.1429 | 0.0491 | 0.0410 | dropping grad2 destroys full-GIF fidelity |
| GT-simple | P-simple | 7 | 1.0000 | 1.0000 | 0.9624 | 0.8797 | Hessian-free approximation works for the simple source |
| R-point | P-point | 6 | 0.7500 | 0.8571 | 0.9692 | 0.8639 | final point proxy works for the point reference |
| R-point | TracInCP-point | 6 | 0.7500 | 0.8571 | 0.9482 | 0.8189 | checkpoint point proxy also works for the point reference |
| GT-full | P-graph | 6 | 0.7500 | 0.8571 | 0.9658 | 0.8557 | best full-GIF approximation in this run |
| GT-full | P-point | 0 | 0.0000 | 0.0000 | 0.1385 | 0.0972 | candidate-only source is misaligned with full GIF |
| GT-full | TracInCP-point | 0 | 0.0000 | 0.0000 | 0.1035 | checkpoints do not repair the source mismatch |
| GT-full | legacy | 1 | 0.0769 | 0.1429 | -0.1102 | -0.0742 | negative control remains misaligned |

The top-7 sets make the source mismatch concrete:

| Score | Top-7 node IDs |
|---|---|
| GT-full | 109, 18, 2, 52, 8, 4, 61 |
| P-graph | 109, 52, 2, 4, 8, 18, 37 |
| GT-simple | 13, 24, 45, 2, 71, 27, 14 |
| P-point | 57, 48, 30, 27, 51, 21, 14 |
| TracInCP-point | 48, 51, 30, 57, 25, 21, 27 |

Thus, the point methods are internally coherent with R-point but answer a different approximation problem from full GIF. Adding checkpoints changes the training-time aggregation; it does not change (g_v) into the graph-deletion source (\mathrm{grad1}-\mathrm{grad2}).

## Model and runtime quality gates

| Measure | Value |
|---|---:|
| Train accuracy | 99.29% |
| Validation accuracy | 79.20% |
| Test accuracy, diagnostic only | 81.50% |
| Base training time | 2.62 s |
| Score producer time | 7.61 s |
| Graph-source time | 2.51 s |
| Shared IHVP time | 0.24 s |
| Cold-run total time | 10.36 s |
| Affected-set size min / mean / max | 2 / 40.31 / 234 |

An earlier 30-epoch SGD run reached only 20.4% validation accuracy. Its cache is retained as an infrastructure pilot, but none of its overlap values are used as the accepted scientific result.

## Cache V2 evidence

The accepted full run is stored as a typed Cache V2 `SCORE` bundle:

| Field | Value |
|---|---|
| Artifact ID | `score_9c9b34fd_004f3774` |
| Recipe SHA-256 | `9c9b34fd64ab8424280d048255168cc5b7595a2752293f6db5e768e7905eed8e` |
| Content SHA-256 | `004f37749c23e524ddec1f9c33e7623df60317339d68255424fea9af23e6303f` |
| Payload | `results/cache_v2/c_target_v1/artifacts/score/9c/score_9c9b34fd_004f3774/payload.json` |

The payload contains all 140 ordered candidate IDs, all eight complete score vectors, deterministic full rankings, affected-set sizes, timings, accuracy, and provenance. The cold run created the Artifact. The exact warm run, executed with `--fail-if-producer-called`, returned the same Artifact with `producer_called=false`. A 139-candidate mismatch exited non-zero with `ProducerCalledError` and wrote no result, proving that a different Recipe does not silently reuse the 140-candidate Artifact.

Legacy `results/cache`, `results/selection_cache`, and `results/score_cache` were content-hash-sentinelled before and after execution and remained unchanged.

## Reproduction

Run from the repository root with the local CPU environment:

```powershell
& 'E:\conda_package\envs\gnn\python.exe' -m experiments.c_target_v1.run_cora_gcn `
  --dataset Cora --optimizer adam --lr 0.01 --epochs 200 `
  --checkpoint-epochs 1,10,25,50,100,200 `
  --milestones 100,150 --gamma 0.5 `
  --output results\c_target_v1\cora_gcn_seed2024_adam200_n140_replay.json
```

To assert the exact warm hit, append `--fail-if-producer-called`. A new dataset, seed, candidate set, target set, checkpoint manifest, model state, or numerical recipe creates a distinct Recipe rather than overwriting this Artifact.

Implementation anchors:

- `experiments/c_target_v1/run_cora_gcn.py`: experiment orchestration and summary;
- `experiments/c_target_v1/core.py`: GCN, gradients, LiSSA, graph deletion, scoring, metrics;
- `experiments/c_target_v1/recipe.py`: semantic Artifact Recipe;
- `experiments/c_target_v1/score_store.py`: typed exact-only Cache V2 ScoreBundle;
- `tests/test_c_target_v1.py`: payload, cold/warm/mismatch, graph, and ranking tests;
- `results/c_target_v1/cora_gcn_seed2024_adam200_n140_accepted_cold.json`: accepted cold summary;
- `results/c_target_v1/cora_gcn_seed2024_adam200_n140_accepted_warm.json`: accepted warm summary.

## Limits and next extension

- This is one dataset, one model, and one seed. It is a mechanism result, not a cross-dataset claim.
- GT-full is an operational GIF reference using a finite LiSSA approximation; it is not an exact-retrain ground truth.
- The affected set is the frozen two-hop definition used by this experiment.
- `test_mask` was used only to report diagnostic accuracy; (g_E) uses `val_mask`.
- The current multi-checkpoint method is point-source TracInCP. A graph-source trajectory, \(\sum_c w_c\langle q_v(\theta_c),g_E(\theta_c)\rangle\), is the natural next ablation if a second-stage experiment is desired. The current result already shows why that source change matters.

The v1 acceptance decision is therefore: **accept the cache-backed mechanism experiment and P-graph signal; reject GT-simple, P-point, and point TracInCP as substitutes for full GIF on this run.**
