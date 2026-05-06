# Appendix A.3 — Alpha Sweep (SPEC, runner extension required)

## Why this is a spec, not a runnable yaml

`experiments/run.py` keys cell output paths on `(dataset, base_model, ratio, method, strategy, seed)`. The Hybrid strategy's `alpha` parameter is read inside `attack/attack_strategies/hybrid_strategy.py` from `args["alpha"]`, but `run.py` never passes alpha through, and the cell directory does not encode alpha. **Two hybrid runs at different alphas would overwrite each other's `attack.json`.**

This file documents the alpha-sweep design and what `run.py` needs in order to run it. Until the runner extension lands, **do not create A3_*.yaml files** that look runnable but quietly collide.

## Required runner change (estimated 30-60 min)

1. **`run.py::run_cell`**: when `strategy == "hybrid"` and `cfg` carries `alpha`, append `--alpha <value>` to both `cmd1` (demo_attack) and `cmd2` (eval_collateral).
2. **`run.py::cell_dir`**: when alpha is set and not 0.5 (default), suffix the strategy name in the path: `hybrid_alpha{alpha:.2f}` instead of `hybrid`. Example: `cora_GCN_r0.05/gnndelete_hybrid_alpha0.25/seed42/`.
3. **`demo_attack.py` / `eval_collateral.py`**: confirm both accept `--alpha <float>` and propagate it into `args["alpha"]` for the Hybrid strategy.
4. **`expand_matrix`**: optionally expand alpha-grid into the iteration; for now an outer loop that generates one yaml per alpha is fine.

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
