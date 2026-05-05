# §A.5 Ablation — Deletion Ratio Sweep  *(USER REQUESTED)*

> Status: outline (runs to schedule)
> Parent: §A Appendix
> Depends on: new Phase B runs on canonical cell (cora/GCN)
> Updated: 2026-05-05

## Purpose

Characterize **per-family budget elasticity**. Removes the "r=0.05 only" weakness (current §6.3 L5) and converts each family's predicted fingerprint position into a **scaling profile**.

Specifically tests:
- **Learning-based canonical (GNNDelete)**: known low-ratio fragility (peak at r=0.01) — does it persist with clean Phase B data?
- **IF-based canonical (GIF)**: Newton-step approximation is bounded → predict near-linear scaling
- **Partition pair (GraphEraser, GraphRevoker)**: Shard Protection — does protection survive at higher r, or is there a critical threshold $r^*$? Does GraphRevoker's "efficient partial retraining" yield a different elasticity curve than GraphEraser's full-shard retrain?
- **Intra-family outliers (MEGU in Learning, IDEA in IF)**: do null effects hold across all r? If MEGU stays null while GNNDelete escalates, the outlier-distance grows with budget — a budget-conditional finding.

## Experimental design

- **Ratios**: $r \in \{0.01,\ 0.05,\ 0.10,\ 0.20\}$ — 4 points spanning reviewer-question low-budget to clearly-visible regime
- **Methods**: all 6 (GraphEraser, **GraphRevoker**, GIF, IDEA, GNNDelete, MEGU) — covers 3 OpenGU categories with n=2 each
- **Strategies**: random, im, tracin — 3 strategies (skip full hybrid α-sweep; endpoints suffice for elasticity)
- **Cell**: cora/GCN (canonical, single-cell to keep ablation scoped)
- **Seeds**: 5

**Total runs**: 6 × 4 × 3 × 5 = **360** on cora/GCN. Estimate ~3–5h on 4090. (If GraphRevoker fails feasibility, falls back to 5 × 4 × 3 × 5 = 300.)

## Output

- **Figure**: 4-panel grid, one panel per family. x-axis = $r$, y-axis = paired effect (vs same-seed random); one line per (method, strategy) inside each panel.
- **Reading guide**:
  - Linear in $r$ → effect proportional to budget (predicted: GIF/GST)
  - Sub-linear / saturating → bounded approximation (predicted: GNNDelete possibly saturates)
  - Negative or flat → Shard Protection persists / null effect persists
  - Threshold (knee) → critical $r^*$ where mechanism breaks (most informative finding)

## Tie-back

- §5.3 Shard Protection: forward-cite "protection survives r ∈ [...]" or "knee at $r^* ≈ ...$"
- §6.3 L5: removes the "r=0.05 focus" limitation
- §1 contribution (4): budget-elasticity profile complements the static fingerprint

## Open questions

- **Q-A.5.1**: $r=0.20$ may break some unlearning algorithms (e.g., GraphEraser shard imbalance). Need sanity pre-check; if any method fails at high r, drop it from that ratio rather than hide.
- **Q-A.5.2**: include hybrid α=0.5 at each $r$? Adds 25% runs (90 more). Skip unless cycles permit.
- **Q-A.5.3**: arxiv ratio sweep? Likely skip — too costly; cite as scaling future work in §6.3.
- **Q-A.5.4**: report budget-elasticity as a single number per (method, strategy) — e.g., $\partial \Delta F / \partial r$ at $r=0.05$? Adds a clean summary statistic.

## Cross-refs

- ← §5.3 Shard Protection (high-r robustness)
- ← §6.3 L5 (limitation removed by this ablation)
- → §A.3 (orthogonal axis: A.3 sweeps α, A.5 sweeps r; the joint α×r grid is out of scope)
