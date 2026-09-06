# Appendix A.3 — Alpha Sweep (implemented 2026-05-06)

## Status: runnable

Runner extension landed in `feat/a3-alpha-sweep` branch:

- **`run.py::cell_dir`** suffixes hybrid leaves with `_alpha{x.xx}` when an explicit non-default `hybrid_alpha` is set (top-level cfg field or `--hybrid_alpha` in `extra_args`). Default 0.5 stays under bare `_hybrid` so it shares with main matrix.
- **`run.py::run_cell`** auto-injects `--hybrid_alpha <value>` from top-level `hybrid_alpha:` into both demo_attack and eval_collateral commands.
- **`attack/result_cache.py::CACHE_KEY_FIELDS`** now includes `fusion_method`, `candidate_fraction`, `mc_rounds`, `im_batch_size`, `im_selector_seed` (in addition to pre-existing `alpha`, `hybrid_alpha`). Sweeping any of these no longer hits stale entries.
- **`tests/test_phase_b_invariants.py`** locks in cell_dir disambiguation (8 parametrized cases) and ResultCache key isolation (7 fields).
- **Schema**: yaml uses `hybrid_alpha: <float>` as a top-level field. Per-alpha yaml is the recommended pattern (one yaml per alpha point); `expand_matrix` was deliberately not extended to keep the change minimal.

`experiments/configs/A3_cora_GCN_alpha0.25.yaml` is a worked example. To run the full sweep, copy it 4× per backbone, changing the `name:` and `hybrid_alpha:` fields only.

## Design (once runner supports it)

- **Cells**: 6 methods × 5 alphas × 2 backbones (GCN, GAT) × 5 seeds = **300 raw**
- **Cache hit**: alpha=0.0 ≡ IM and alpha=1.0 ≡ TracIn already in main matrix → effective new = 6 × 3 × 2 × 5 = **180 cells**
- **Wall-clock**: ~90 min cora/GCN + ~120 min cora/GAT on a single 4090
- **Alpha grid**: {0.00, 0.25, 0.50, 0.75, 1.00}
- **Cell dataset**: cora only (small enough; arxiv α-sweep deferred to future work, see §A.5 caveat)
- **Ratio**: r=0.05 only

## Output structure (proposed)

```
results/runs/cora_GCN_r0.05/{method}_hybrid_alpha{0.00,0.25,0.50,0.75,1.00}/seed{N}/{4 files}
results/runs/cora_GAT_r0.05/{method}_hybrid_alpha{0.00,0.25,0.50,0.75,1.00}/seed{N}/{4 files}
```

`hybrid_alpha0.00` aliases to `im` (cache reuse), `hybrid_alpha1.00` aliases to `tracin`. Aggregator handles the aliasing.

## Aggregator

`scripts/plot_supp_figures.py::plot_alpha_synergy` (TBD): reads the 5 alpha points per method per backbone, plots f(alpha) with chord overlay, computes curvature index (signed area between curve and chord), and tags the curve as concave/convex/linear/flat per the §A.3 reading guide.

## Decision gate

Hold this work until **after** the main Phase B matrix completes and validates the fingerprint. If the fingerprint shows MEGU/IDEA at the origin, A.3 mainly confirms with flat curves; if MEGU/IDEA show non-trivial fingerprint coordinates, A.3 becomes a load-bearing diagnostic and the runner extension is worth doing.
