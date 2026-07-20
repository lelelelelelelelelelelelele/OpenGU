# Historical finding: a mis-specified selector and a useful single-final proxy

*Selection-concordance study, 2026-06-27. Updated terminology: 2026-07-20.*

> **Historical evidence, not the current TracIn acceptance source.** This study used
> `proper TracIn` as an early label for the final-checkpoint point-source score
> `⟨g_v(θ_final), ∇L_E(θ_final)⟩`. That label is retired. Standard TracInCP accumulates
> weighted gradient products over multiple checkpoints. The historical comparison also used
> candidate-only point gradients, so its Hessian reference is a point IF diagnostic rather than
> the later full graph-deletion GIF reference. Current evidence lives in
> [`reports/bc_target_matrix_REPORT.md`](../../../reports/bc_target_matrix_REPORT.md) and
> [`docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md`](../../../docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md).

## TL;DR

The deployed selector historically called `TracIn` ranks candidates by

```text
-⟨g_v, sum_{j in T} g_j⟩.
```

On trained base GCNs, its top-k overlap with the historical eval-target point-IF diagnostic is
only `0.098–0.142`. Replacing the training-gradient residual direction with the held-out/query
gradient at the same final checkpoint gives `0.647–0.742` overlap with that point-IF diagnostic.

This result established two useful facts:

1. the deployed cross-gradient selector targets the wrong direction for eval-loss influence;
2. a same-source, single-final Hessian-free projection can be a useful diagnostic proxy.

It did **not** establish that standard multi-checkpoint TracInCP had been implemented, that point
IF equals full graph GIF, or that the proxy had passed a production attack gate.

## 1. Historical projection view

Let `T` be the deletion-candidate/training pool and `E` a disjoint evaluation/query set. Define
`g_v = ∇ℓ_v` and `g_E = ∇L_E`. The historical study compared:

| Current name | Score | What it measures |
|---|---|---|
| deployed cross-gradient Legacy | `⟨g_v, -Σ_{j∈T}g_j⟩` | alignment with the training/regularization residual |
| single-final point eval proxy | `⟨g_v(θ_final), g_E(θ_final)⟩` | final-state point-source alignment with target `E` |
| point IF diagnostic | `⟨g_v, H^-1g_E⟩` | final-state curvature-corrected point influence on `E` |
| final grad-norm proxy | `||g_v||^2` | the candidate's own final-state gradient magnitude |

Two later distinctions were outside this original study:

- standard TracInCP uses `Σ_c w_c⟨g_v(θ_c),g_E(θ_c)⟩` over an ordered checkpoint set;
- full graph GIF replaces point source `g_v` with a graph-deletion source such as
  `q_v=grad1_v-grad2_v`.

`E` is not the deletion-candidate pool. A diagnostic may use the test split as `E`; a formal attack
must use a validation/query set or a provenance-bound pseudo-labeled probe set to avoid test-label
leakage.

## 2. Historical results

A seeded base GCN was trained separately for each dataset. The reported metric is top-k Jaccard,
with `k=0.05*|V_train|`.

| Pair | Cora | CiteSeer | PubMed |
|---|---:|---:|---:|
| point IF diagnostic vs single-final point eval proxy | `0.742` | `0.727` | `0.647` |
| point IF diagnostic vs deployed cross-gradient | `0.113` | `0.142` | `0.098` |
| point IF diagnostic vs final grad norm | `0.249` | `0.298` | `0.133` |
| point IF diagnostic vs degree | `0.024` | `0.051` | `0.041` |
| single-final point eval proxy vs degree | `0.024` | `0.043` | `0.045` |

The random-overlap floor for two independent k-subsets is approximately `0.025` in this setting.
The single-final point proxy therefore captured the historical point-IF direction much better than
the deployed residual selector, while both eval-target diagnostics remained nearly orthogonal to
degree.

## 3. Why the deployed direction is wrong

An early explanation said `Σ_j g_j` should be almost zero at convergence and the deployed score
was numerical noise. That explanation was wrong: measured norms were `69.6` on Cora, `68.5` on
CiteSeer, and `255` on PubMed.

At an L2-regularized stationary point,

```text
(1/|T|) Σ_j g_j + λθ ≈ 0,
```

so `-Σ_j g_j ≈ |T|λθ`. The deployed selector therefore ranks candidates by alignment with a
parameter/regularization-residual direction. It is deterministic, but it does not explicitly target
the held-out/query loss.

## 4. The five-line change was a diagnostic, not the production fix

The original note proposed changing only the contraction vector:

```python
# deployed Legacy direction
col_sum = G.sum(dim=0)
scores = -(G @ col_sum)

# historical single-final diagnostic
g_eval = grad_of_held_out_or_query_loss
scores = G @ g_eval
```

This remains a legitimate single-final point-source ablation. It cannot be used as a production
TracIn replacement by itself because it omits the checkpoint trajectory, checkpoint weights,
optimizer semantics, source definition, formal Recipe/Producer identity, and parent Artifact chain.

## 5. What later evidence changed

The accepted B/C matrix broadened the original diagnosis:

- B-Hutchinson vs B-LiSSA Spearman is `0.968`;
- point IF vs full graph GIF is only `0.112`;
- simple IF vs full graph GIF is only `0.040`;
- with full graph source fixed, `p_graph` vs `gt_full` reaches `0.984`;
- 3/6-checkpoint graph trajectory vs final `gt_full` reaches only `0.498/0.529`;
- selector fidelity and set-deletion damage have different winners.

Therefore the modern conclusion is not merely “replace the direction with `g_E`.” It is:

> Keep target, graph-deletion source, and temporal/checkpoint semantics separate. Validate a proxy
> against a same-source reference, then validate the selected set's downstream damage independently.

## 6. Implications

- Old TracIn and Hybrid attack cells remain historical products but are not proper-TracIn evidence.
- Random, degree, PageRank, and IM are not invalidated by this selector-definition issue.
- The old `0.647–0.742` result remains useful as discovery evidence for a single-final point proxy;
  it is not the current primary SUP result.
- The formal `proper-tracin-v1` Score → Selection path has now passed its conditional selection gate.
  Hybrid and approximate-GU canaries remain separate follow-up gates.

## Reproduce the historical diagnostic

```text
python self/related_work/concordance/concordance_model_based.py --dataset_name cora
```

Use `citeseer` or `pubmed` for the other historical cells. The output field names retain their old
`gif_tracinproper` naming for compatibility; interpret them using the current table above.
