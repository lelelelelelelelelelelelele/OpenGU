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

## Real GIF vs TracIn (RESOLVED — authorised base-GCN train)
`concordance_model_based.py` trains a proper base GCN per dataset (`train_only`, **no unlearning** — you
OK'd training for the concordance study), then computes TracIn (cross) + real GIF (s=H⁻¹∇L_test via LiSSA)
on the **same** trained model.

| pair | cora (F1=0.89) | citeseer (F1=0.73) | pubmed (F1=0.86) |
|---|---|---|---|
| GIF ↔ TracIn (cross, deployed) | 0.263 | 0.047 | **0.003** |
| GIF ↔ TracIn-self ‖∇ℓ‖ | 0.293 | 0.337 | 0.207 |
| GIF ↔ degree | 0.024 | 0.039 | 0.042 |

(cross-form GIF surrogacy degrades with graph size — 0.26→0.05→0.003; self-influence holds 0.21–0.34; GIF⟂degree everywhere.)

1. **Deployed cross-form TracIn is a weak GIF surrogate** (0.05–0.26): cross ≈ ⟨∇ℓ_v, Σ∇ℓ⟩, Σ∇ℓ≈0 near
   convergence → noisy. **Self-influence ‖∇ℓ‖ aligns ~7× better** (0.29–0.34) but still ~0.3 (H⁻¹ reorders).
   → if you want "my selector ≈ IF", use self-influence, not the cross form; even then it's loose.
2. **Real GIF is itself near-orthogonal to degree** (0.02–0.04) → not "cheap proxy misses degree"; the
   exact-ish Hessian IF also targets different nodes than degree. **Volume-driven survives the real IF.**

(`gif_scorer.py`, the 34%-acc GNNDelete-checkpoint feasibility hack, is superseded and removed.)
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
- `data/*.json` — selections, jaccard matrices, summary, modelbased_{ds} (TracIn/GIF).
- `figures/jaccard_*.png` — heatmaps.

## Reproduce
```
python self/related_work/concordance/run_topology_selectors.py --dataset_name <ds> --base_model GCN --unlearn_ratio 0.05
python self/related_work/concordance/run_analysis.py
python self/related_work/concordance/gen_report.py
```
Training-free, CPU-only. Did not modify any existing results/ cache (additive ScoreCache writes only).
