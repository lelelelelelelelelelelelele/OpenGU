# A.6 Influence-Selector Taxonomy and Concordance

## Purpose

Separate all influence-family selectors by mechanism before comparing their selected sets:

- A/B: target-free parameter-change family;
- C: evaluation-conditioned IF without post-deletion `grad2`;
- D: graph-aware GIF with `grad1-grad2`;
- legacy cross-TracIn and topology selectors: external controls.

## Historical evidence boundary

- Datasets: Planetoid Cora, CiteSeer, PubMed.
- Model: two-layer GCN.
- Seeds: 42, 212, 2024.
- Budgets: the retired study used fixed small node counts; those counts are not
  valid inputs for the current ratio-conditioned experiment.
- Target: validation mean cross-entropy; test labels are downstream utility only.
- Evidence is descriptive over 3 datasets × 3 seeds.
- This is a local selector/set-deletion study, not an end-to-end approximate-GU result.

Historical navigation only: `../../../reports/bc_target_matrix_REPORT.md` and
`../../../results/bc_target_v2/aggregate/`. These retained artifacts may support
mechanism discussion, but are excluded from new figure/table inputs. Current
target-direct evidence must come from `target_direct_formal_v2` under the
registered 1%/5% contract and is still pending formal execution.

## Table plan

| Test type | Pair | Spearman | Interpretation |
|---|---|---:|---|
| A/B within-group | A vs B reference | 0.962 | A is a strong Hessian-free proxy for B ranking in this setting |
| C/D cross-group | C-simple vs D-full | 0.040 | adding the graph-deletion source changes the mechanism |
| D within-group | P-graph vs GT-full | 0.984 | single-final D proxy closely reproduces the D reference |
| D trajectory ablation | graph CP-3 / CP-6 vs GT-full | 0.498 / 0.529 | more checkpoints do not automatically approach final GIF |

Also report B reference vs D-full (`0.023`) and C-point vs D-full (`0.112`) as cross-group separation evidence.

## Writing constraints

- Say “A strongly proxies B ranking,” not “A and B are equivalent.”
- Describe all inverse-Hessian terms as computed through iterative IHVP solves; keep solver, HVP, and probe details in reproducibility settings rather than the selector taxonomy.
- Reserve GIF/D for the `grad1-grad2` source.
- Report selection fidelity separately from downstream set-deletion damage.
- Do not infer significance or an approximate-GU vulnerability from this local matrix.

## Status

Historical local mechanism evidence retained read-only; current target-direct
evidence remains pending and must not inherit acceptance from this study.
