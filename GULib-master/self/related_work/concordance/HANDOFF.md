# Selection-Concordance study — hand-off (2026-06-27)

Branch: `research/selection-concordance-2026-06-27` (11 commits, off the docs branch).
Deliverable: **`self/related_work/concordance/report.html`** (open in a browser — self-contained).

## What this answers
Do the attack's node-selection strategies pick the **same** nodes? Set-overlap
(Jaccard@k) of the top-k selected sets, training-free, across datasets. Motivated by
the cora single-cell finding + the open questions from our discussion (is IM just
degree? is TracIn just degree? is my cheap TracIn ≈ real GIF?).

## Results (GCN, r=0.05, seed 2024, k=r·|V_train|)

| pair | cora | citeseer | pubmed | Photo | Computers | CS | mean |
|---|---|---|---|---|---|---|---|
| degree ↔ pagerank | 0.831 | 0.503 | 0.568 | 0.611 | 0.599 | 0.705 | **0.64** |
| IM ↔ degree | 0.187 | 0.177 | 0.061 | 0.046 | 0.030 | 0.032 | **0.09** |
| TracIn ↔ degree | 0.024 | — | — | — | — | — | (cora only) |
| TracIn ↔ IM | 0.029 | — | — | — | — | — | (cora only) |

(All 6 datasets done. Larger/denser graphs make IM *more* distinct from degree — Computers/CS/Photo ≈ 0.03–0.05.)

### Findings
1. **IM does NOT degenerate to degree** — distinct on every dataset (0.03–0.19), most distinct on
   the larger/denser graphs (Computers 0.03, Photo 0.05). My earlier code-level guess "IM≈degree at
   low p / small k" was wrong at the **set** level; CELF's submodular selection genuinely diverges.
   (Single-node IM spread can still track degree — the *combination* differs, exactly as suspected.)
2. **degree ≈ pagerank but dataset-dependent** (0.50–0.83). Correlated, not interchangeable; cora is
   the high-overlap outlier.
3. **TracIn near-orthogonal to degree AND IM** (cora 0.02–0.03). The influence attack targets a
   genuinely different node set → "the attack is just degree" is refuted; and since degree wins the
   attack while sharing ~no nodes with TracIn, the winning signal is **structural volume, not influence**
   (set-level support for the volume-driven reading).

## Real GIF vs TracIn (RESOLVED — authorised base-GCN train, seeded)
`concordance_model_based.py` trains a proper base GCN per dataset (`train_only`, **no unlearning** — you
OK'd training for the concordance study), seeded/deterministic, then on the **same** trained model computes:
real GIF (s=H⁻¹∇L_test via LiSSA), proper TracIn ⟨∇ℓ_v,∇L_test⟩, deployed cross-TracIn ⟨∇ℓ_v,Σ∇ℓ⟩, self ‖∇ℓ‖.

| pair | cora (F1=.88) | citeseer (F1=.73) | pubmed (F1=.86) |
|---|---|---|---|
| GIF ↔ **TracIn-proper** ⟨∇ℓ,∇L_test⟩ (FIX) | **0.742** | **0.727** | **0.647** |
| GIF ↔ TracIn-cross (deployed) | 0.113 | 0.142 | 0.098 |
| GIF ↔ TracIn-self ‖∇ℓ‖ | 0.249 | 0.298 | 0.133 |
| GIF ↔ degree | 0.024 | 0.051 | 0.041 |
| TracIn-proper ↔ degree | 0.024 | 0.043 | 0.045 |

1. **The cheap fix recovers IF fidelity.** Proper TracIn (contract with ∇L_test, *Hessian-free*, same cost as
   the deployed strategy, scales to arxiv) ≈ GIF at **0.65–0.74**. The residual ~0.25–0.35 gap is the honest
   H⁻¹ whitening (Hessian-free ceiling). The deployed cross-form sits at **0.10–0.14** (~2× the random floor).
2. **⚠ Mechanism correction.** An earlier claim that "Σ∇ℓ≈0 at convergence → noise" was WRONG: measured ‖Σ∇ℓ‖
   is large (69 / 68 / 255), ≈ the L2-reg residual (∝ θ). The cross-form just contracts with the **wrong
   direction** (aggregate-training/regularisation, not test descent) → ranks by the wrong criterion.
3. **Real GIF and the fixed TracIn are both ⟂ degree** (0.02–0.05) → even the correct influence selector targets
   different nodes than degree. **Volume-driven survives the real IF.**

→ Production recommendation: replace the deployed cross-TracIn with proper TracIn (≈5-line change: contract
∇L_val/query, not Σ∇ℓ). Affects only TracIn + Hybrid; re-run just those cells if you want corrected attack
numbers. (`gif_scorer.py`, the 34%-acc GNNDelete-checkpoint feasibility hack, is superseded and removed.)
LiSSA is first-order — run a scale/iteration sensitivity sweep before quoting exact magnitudes.

## Caveats
- Single seed, single ratio (0.05), single backbone (GCN). Directional, not yet a finished finding.
- TracIn/Hybrid rows are cora-only (model-based selectors need a trained model; only cora is cached).
- IM uses batch-CELF (im_batch_size=5), which slightly reduces submodular diversity vs classic CELF
  (batch=1). Re-check IM distinctness with batch=1 before claiming it's intrinsic.

## Next steps (priority order)
1. **LiSSA sensitivity** (scale/iter) for the GIF scores + extend model-based cells to Photo/Computers/CS.
2. **Seed × ratio sweep** {2024,1,2,3} × {0.01,0.05,0.1} → error bars → finding.
3. **Attack-outcome join**: per selector, (overlap-with-degree, Δacc-under-unlearning) → the decisive
   "different nodes AND worse" table that nails the volume-driven claim.
4. **Coverage-aware damage selector** prototype (submodular greedy on predicted collateral with
   receptive-field discount) — the one untried lever that could beat degree (per NOTES.md §how-to-solve).

## Files (all under `self/related_work/concordance/`)
- `run_topology_selectors.py` — training-free selection runner (degree/pagerank/im/random).
- `concordance_model_based.py` — trains a base GCN (this study only) → TracIn + real GIF on the same model.
- `run_analysis.py` — Jaccard matrices + heatmaps + summary.
- `gen_report.py` → `report.html` — the deliverable.
- `FINDING_tracin_misspecification.md` — standalone chapter on the deployed-TracIn bug + the fix (thesis-ready).
- `data/*.json` — selections, jaccard matrices, summary, modelbased_{ds} (TracIn/GIF).
- `figures/jaccard_*.png` — heatmaps.

## Reproduce
```
python self/related_work/concordance/run_topology_selectors.py --dataset_name <ds> --base_model GCN --unlearn_ratio 0.05
python self/related_work/concordance/run_analysis.py
python self/related_work/concordance/gen_report.py
```
Training-free, CPU-only. Did not modify any existing results/ cache (additive ScoreCache writes only).
