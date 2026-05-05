# §A.3 Ablation — α-sweep as Synergy Diagnostic  *(USER CONFIRMED, runs scheduled)*

> Status: outline — runs scheduled (cora/GCN + cora/GAT × 6 method (3 OpenGU categories: Partition[GraphEraser, GraphRevoker] / IF[GIF, IDEA] / Learning[GNNDelete, MEGU]) × α ∈ {0.0, 0.25, 0.5, 0.75, 1.0})
> Parent: §A Appendix (but with §5.1 forward-link)
> Depends on: extra Phase B runs after main matrix completes
> Updated: 2026-05-05

## Reframed purpose

Not "defending α=0.5". Instead: $f(\alpha) := \text{paired effect of Hybrid}_\alpha$ is the **synergy diagnostic**. Curve shape tells us how IM and TracIn signals interact per family.

## Curve interpretation

| $f(\alpha)$ shape | Reading | Mechanism |
|---|---|---|
| Linear (chord between endpoints) | IM and TracIn select disjoint, additive sets | two axes independent |
| Concave (above chord) | Mixed selection beats both ends | **synergy** — nodes targeted by both signals |
| Convex (below chord) | Mixed selection worse than either end | **redundancy** — selectors competing for overlapping nodes |
| Flat at zero | Method robust to both directions | **mechanism-incomparable** (predicted: MEGU, IDEA) |

## Experimental design  *(USER CONFIRMED)*

- 5 α values: $\{0.0, 0.25, 0.5, 0.75, 1.0\}$
- 6 methods: GraphEraser, **GraphRevoker**, GIF, IDEA, GNNDelete, MEGU (GraphRevoker contingent on feasibility gate)
- 2 cells: cora/GCN, cora/GAT (4090 fast; arxiv NOT in scope — too costly)
- 5 seeds per (method, α, cell)
- Total new runs: 6 × 5 × 2 × 5 = **300 runs** (α=0.0 ≡ IM and α=1.0 ≡ TracIn already in main matrix → effective new = 6 × 3 × 2 × 5 = **180 runs**)

## Tie-back to §5.1 fingerprint

The two endpoints (α=0, α=1) **are** the fingerprint axes. The interior α gives the synergy color of the trajectory between fingerprint endpoints. Plot:
- Per family, one panel showing $f(\alpha)$ with chord overlaid as dashed reference
- Concave/convex/linear/flat region annotations

## Evidence binding

- Data path: `results/runs/cora_{GCN,GAT}_r0.05/{method}_hybrid_alpha{0.0,0.25,0.5,0.75,1.0}/seed*/attack.json`
- Config: NEW yaml needed `experiments/configs/A3_alpha_sweep.yaml` (TBD)
- Plot: `scripts/plot_supp_figures.py::plot_alpha_synergy` (TBD)

## Open questions

- **Q-A.3.1**: 5 α points enough, or interpolate to 7 ({0, 0.15, 0.3, 0.5, 0.7, 0.85, 1})? More points = smoother curve diagnostic but 250 → 350 runs.
- **Q-A.3.2**: report curvature index (e.g., area between curve and chord, signed) as a single-number summary per family?
- **Q-A.3.3**: also include cora/GCN α-sweep at lower budget (r=0.02) to test whether synergy is budget-dependent?

## Cross-refs

- ← §3.2 (Hybrid α defined there with forward-link here)
- ← §5.1 (axes are α=0/α=1; interior α is path between)
- → §6.2 (flat curve of MEGU/IDEA = geometric statement of mechanism-incomparable)
