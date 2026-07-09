# A mis-specified influence selector, and a cheap, scalable fix

*Selection-concordance study, 2026-06-27. Self-contained chapter — drop into the thesis
methods/validation section or appendix. Numbers are seeded and reproducible; see Reproduce.*

## TL;DR

The node-selection strategy we deploy as "TracIn" ranks candidates by the **wrong quantity**.
On a trained base GCN its top-k overlap with the real graph influence function (GIF) is only
**0.10–0.14** — barely above the random-overlap floor (~0.025) and far below a faithful surrogate.
A one-line change — contract each node gradient with a **held-out evaluation/query** loss gradient
instead of the **training-gradient sum** — recovers **0.65–0.74** overlap with GIF at *identical* cost
(pure gradient inner products, no Hessian, scales to ogbn-arxiv). The residual ~0.25–0.35 gap to
GIF is the expected inverse-Hessian whitening, the Hessian-free ceiling.

This likely is the long-suspected influence-code issue (we had flagged "a problem rooted in OpenGU,
never fixed"); the concordance experiment is what finally surfaced and pinned it.

## 1. A shared projection view

For a trained model with parameters θ̂, per-node loss ℓ_v, candidate/training set T, and a
held-out evaluation/query set E, all model-based selectors can be read as a projection of the
same candidate gradient `g_v = ∇ℓ_v` onto some reference direction `u`:

`score(v) = ⟨g_v, u⟩`.

Important: **E is not the deletion candidate pool**. The nodes eligible for unlearning are still
drawn from T. E only defines the target loss whose change we want to predict: "if v is removed
from training, what happens to this held-out/query loss?" In a diagnostic study we may use the
test split as E to compare against GIF; in an attack threat model E should be a validation/query
set or pseudo-labeled probe set, because selecting with true test labels would be label leakage.

| name | projection score for candidate v | reference direction u | Hessian? | cost |
|---|---|---|---|---|
| **deployed cross-TracIn** | `⟨∇ℓ_v, -Σ_{j∈T} ∇ℓ_j⟩` | training/regularization residual (`≈ \|T\|λθ̂` under L2 stationarity) | no | O(\|T\|·d) |
| **proper TracIn** (the fix) | `⟨∇ℓ_v, ∇L_E⟩`, where `L_E = Σ_{e∈E} ℓ_e` | held-out/query loss sensitivity | no | O(\|T\|·d) |
| **GIF** (real graph IF) | `⟨∇ℓ_v, H⁻¹∇L_E⟩` | curvature-preconditioned held-out/query loss sensitivity | yes (LiSSA) | O(\|T\|·d) + HVP iters |
| **self-influence** | `⟨∇ℓ_v, ∇ℓ_v⟩ = \|∇ℓ_v\|²` | candidate-dependent own-gradient direction | no | O(\|T\|·d) |

The deployed score is `-(G @ Gᵀ·1)` in `attack/attack_strategies/tracin_strategy.py`
(`G` = stacked per-candidate gradients), i.e. it contracts each node gradient with
`-Σ_j ∇ℓ_j`. The negative sign matters: under the standard L2-regularized stationary condition,
`Σ_j ∇ℓ_j ≈ -\|T\|·λ·θ̂`, so the deployed reference direction becomes approximately `+\|T\|·λ·θ̂`.
It is therefore a parameter/regularization direction, not an evaluation-loss direction.

The proper TracIn (Pruthi et al. 2020, single-checkpoint, influence on the *evaluation* loss)
contracts with `∇L_E`. GIF (Wu et al. 2023) is the same target direction with the inverse-Hessian
preconditioner. The candidate backward pass is unchanged across the deployed, proper, GIF, and
self forms; GIF only adds one LiSSA solve for `s = H⁻¹∇L_E` before the per-candidate dot products.

## 2. Diagnosis (seeded, 3 datasets, same trained base GCN)

A base GCN is trained per dataset (`train_only`, no unlearning), seeded/deterministic; all four
quantities are computed on that one model. Top-k set overlap (Jaccard@k, k = 0.05·|V_train|):

| pair | cora (F1=.88) | citeseer (F1=.73) | pubmed (F1=.86) |
|---|---|---|---|
| GIF ↔ **proper TracIn** ⟨∇ℓ,∇L_E⟩ **(fix)** | **0.742** | **0.727** | **0.647** |
| GIF ↔ deployed cross-TracIn | 0.113 | 0.142 | 0.098 |
| GIF ↔ TracIn-self ‖∇ℓ‖ | 0.249 | 0.298 | 0.133 |
| GIF ↔ degree | 0.024 | 0.051 | 0.041 |
| proper TracIn ↔ degree | 0.024 | 0.043 | 0.045 |

Random-overlap floor for two independent k-subsets ≈ k/(2|V_train|) ≈ **0.025**.
So: proper TracIn ≈ **26–29×** the floor; deployed cross ≈ **4–6×** the floor (a poor surrogate);
self-influence is intermediate (5–12×).

## 3. Mechanism (corrected)

> ⚠️ We initially mis-explained this as "Σ_j ∇ℓ_j ≈ 0 at convergence, so the deployed score is
> numerical noise." That is **wrong**. Measured ‖Σ_j ∇ℓ_j‖ is **large** — 69.6 (cora), 68.5
> (citeseer), 255 (pubmed) — not near zero.

At the L2-regularized optimum, `(1/|T|)Σ∇ℓ_j + λθ̂ = 0`, so **Σ_j ∇ℓ_j ≈ −|T|·λ·θ̂**: a large
training-gradient residual pointing opposite the parameter vector. Because the deployed score uses
the negative contraction, `−⟨∇ℓ_v, Σ_j∇ℓ_j⟩ ≈ ⟨∇ℓ_v, |T|·λ·θ̂⟩`. It therefore ranks nodes by how much
their gradient aligns with the **parameter / regularization-residual direction** — **the wrong
criterion** — not by influence on the held-out evaluation loss. It is not noise; it is a deterministic
ranking of the wrong thing. The proper TracIn contracts with `∇L_E`, the actual direction of
evaluation-loss change, which is why it tracks GIF.

## 4. The fix (~5 lines, same complexity)

In `attack/attack_strategies/tracin_strategy.py`, replace the contraction vector:

```python
# deployed (mis-specified): negative contraction with the training-gradient sum
col_sum = G.sum(dim=0)              # Σ_j ∇ℓ_j ≈ -|T| λ θ under L2 stationarity
scores  = -(G @ col_sum)            # reference direction is therefore ≈ +|T| λ θ

# fixed (proper TracIn): contract with the eval/query-loss gradient
g_eval  = grad of CE on a held-out eval/query set, w.r.t. params, flattened   # ∇L_E
scores  =  G @ g_eval               # influence on eval loss; topk = most influential
```

No Hessian, no extra forward over the candidates (the per-candidate gradients `G` are unchanged),
so the chunked / CPU-offload path for ogbn-arxiv works as-is. **Threat-model note:** `L_E` should be
a *held-out validation / query* set or model pseudo-labels — using test labels for selection would
be label leakage in an attack setting.

## 5. Implications

- **Scope.** Only **TracIn** and **Hybrid** (which fuses TracIn) are affected; degree, pagerank, IM,
  random are untouched, as are all unlearning / MIA / collateral / retrain-gap results for non-TracIn
  strategies. Re-running just the TracIn + Hybrid cells suffices for corrected attack numbers — **not**
  the whole matrix.
- **Prior "IF loses to degree" evidence is partly compromised** for the TracIn arm: it was measured
  with a selector that ranks by the wrong criterion. The corrected selector should be re-run before
  any claim about influence-based selection's attack strength.
- **The volume-driven conclusion survives.** Both GIF (real IF) and the fixed proper-TracIn are
  ⟂ degree (0.02–0.05) — even the correct influence selector targets a different node set than the
  structural-volume centrality that wins the attack. So "high-influence ≠ high-damage under approximate
  unlearning" holds independently of the TracIn bug; the bug only invalidates the *TracIn-specific*
  numbers, not the headline.
- **A clean validation story for the thesis.** Small graphs admit exact-ish GIF as a gold standard;
  proper TracIn (Hessian-free, scalable) is validated against it at ~0.7 fidelity and then used at
  scale — the standard cheap-proxy/expensive-gold pattern, now with the proxy actually pinned to the
  gold.

## Reproduce

```
python self/related_work/concordance/concordance_model_based.py --dataset_name cora      # citeseer, pubmed
```
Trains one base GCN (this study only), seeded, CPU; writes `data/modelbased_{ds}.json`
(`gif_tracinproper`, `gif_tracin`, `gif_tracinself`, `gif_degree`, `tracinproper_degree`).
LiSSA is a first-order H⁻¹ estimate — a scale/iteration sensitivity sweep is the one remaining
robustness check before quoting exact magnitudes.
