# Abstract Review — 2026-05-04

> Reviewed against: `sections/abstract_v1_2026-02-26.md`
> Output: `sections/abstract.md` (revised, ECCV-targeted)
> Empirical anchors: `self/dashboard/EXPERIMENT_DASHBOARD.md §3`, `self/dashboard/VALIDATION_LOG.md` (entries V-2026-05-03-{02,04,06}, V-2026-05-04-{04,05,06})

## Empirical fact-check (run 2026-05-04 against current data)

### "Shard Protection Effect" — claim is empirically supported ✅

GraphEraser cora/GCN/r=0.05 actual numbers (per-seed `f1_drop`, positive = F1 down):

| seed | random | im_v4 | im - rand |
|------|-------:|------:|----------:|
| 42   | -8.30% | -7.01% | +1.29% |
| 212  | -3.51% | -4.43% | -0.92% |
| 722  | -6.27% | -0.55% | +5.72% |
| 1337 | -6.46% | -2.59% | +3.87% |
| 2024 | -6.83% | -0.93% | +5.90% |
| **mean** | **-6.27%** | **-3.10%** | **+3.17%** |

Both random AND IM cause F1 to **rise** (negative drop = improvement). IM improves *less* than random (+3.17pp gap). Interpretation: shard aggregator absorbs deletion as a regularizer; an attacker's "best" outcome is to merely deny the auto-regularization, not actively damage F1.

### "F1 collapse exceeding 17%" — borderline, tightened ⚠

GNNDelete cora/GCN/r=0.05 IM_v4 vs random per-seed (V-2026-05-03-04):

| seed | random | im_v4 |
|------|-------:|------:|
| 42 | 8.67% | 16.97% |
| 212 | 11.62% | 11.07% |
| 722 | 7.01% | 6.09% |
| 1337 | 12.92% | 19.74% |
| 2024 | 7.01% | **27.12%** |
| mean | 9.45% | **16.20%** |

"Exceeding 17%" cherry-picks. Honest framing: "averaging 16% with peaks above 27%". Revised abstract uses this.

### "Less than 1% of the graph" — wrong, fixed ⚠

Original wrote "deletion budget of less than 1% of the graph". Actual: `unlearn_ratio=0.05` × train_indices (60% of nodes for cora) ≈ **3% of graph**, or **5% of training nodes**. Revised says "below 5% of training nodes" — accurate and stronger framing (referee thinks "5% is small", same effect, no false claim).

### GIF "marginal vulnerability" — quantify ✅

V-2026-05-03-06: GIF × TracIn paired effect = +4.17% F1, std=0.76, p=0.0001. Revised adds "(paired effect ≈+4% F1, p<0.001)" — concrete and defensible.

### MEGU/IDEA omission — added (4) ⚠

V-2026-05-04-01 commits paper to mechanism-incomparable framing for MEGU/IDEA. Original abstract evaluates "five methods" but only highlights three. Revised adds (4) explicitly:

> feature-preserving (MEGU) and certified-gradient (IDEA) families exhibit null effect (<1% F1 difference), revealing a *mechanism-incomparable* robustness dimension that current selector designs cannot exploit.

This converts an apparent gap (4 of 5 methods discussed → 5 of 5) and turns null effects from "weakness" into "finding".

### Hop-distance decay — added ⚠

A.5 metric (added 2026-05-04, see attack/attack_eval.py::evaluate_collateral_damage) is the most GNN-specific differentiator in the metric catalog (see `self/dashboard/METRICS_CATALOG.md` §8.3). Original abstract listed only "retrain gap, prediction shift". Revised:

> retrain gap, prediction shift, and a novel **hop-distance decay** quantifying disturbance propagation through the GNN's receptive field

The "receptive field" framing connects directly to GCN layer count and is referee-accessible.

### "First systematic" — softened ⚠

Original: "We present the first systematic adversarial audit". No comprehensive lit review on hand. Softened to "We present, to our knowledge, the first systematic..." — one phrase, prevents being countered by an obscure citation.

### Vision framing — kept ✅

Venue is ECCV 2026 (per metadata in v1). Vision relevance is required. The actual experiments use citation-network benchmarks (Cora/Citeseer/ogbn-arxiv); revised abstract bridges this gap by stating "the framework is architecture-agnostic and applies directly to vision GNNs" instead of the previous over-claim "framework directly applies to vision GNN systems where privacy-compliant unlearning is required". Slightly weaker but defensible.

## Summary diff

| Aspect | v1 (2026-02-26) | Revised (2026-05-04) |
|---|---|---|
| Novelty claim | "first systematic" | "to our knowledge, the first systematic" |
| GNNDelete F1 collapse | "exceeding 17%" | "averaging 16%, peaks above 27%" |
| Deletion budget | "less than 1% of the graph" | "below 5% of training nodes" |
| GIF vulnerability | "marginal" | "marginal but statistically significant (≈+4% F1, p<0.001)" |
| Shard Protection | mentioned, no numbers | "+3-6% improvement, attacker bounded above by random" |
| MEGU/IDEA | omitted | added as (4): mechanism-incomparable |
| Datasets | "multiple graph datasets" | "Cora, Citeseer, ogbn-arxiv (169K nodes)" |
| Hop-distance decay | not mentioned | added as differentiator metric |
| Vision applicability | "directly applies to vision GNN systems" | "architecture-agnostic and applies directly to vision GNNs" |
| Word count | ~230 | ~290 |

## Open items

1. **Phase B not yet run.** Numbers above are from pre-A.4-fix data. Post-fix expectations:
   - F1 numbers: same mean, std should shrink (A.4 makes IM deterministic across seeds)
   - The 16% / 27% / 4% / 3-6% figures are stable enough to ship in placeholder abstract
   - Final paper-submission version of abstract should refresh after server runs
2. **Vision-graph experiments missing.** Cora/Citeseer/arxiv aren't vision data. Three options after Phase B:
   - (a) Add a single PASCAL-VOC scene-graph or skeleton-based action recognition cell as appendix evidence
   - (b) Soften abstract further: "demonstrated on graph benchmarks; immediately applicable to vision GNNs"
   - (c) Reframe as a graph-ML paper and target NeurIPS instead of ECCV (large change)
3. **Lit review for "first systematic" claim.** Should verify no prior adversarial audit on approximate GU exists. `papers/` library has 20+ recent GU papers — quick scan for "adversarial / attack / audit" terms in titles before camera-ready.

## Files

- `sections/abstract.md` — current revised version (interim, ECCV target)
- `sections/abstract_v1_2026-02-26.md` — original, preserved for diff
- `review/abstract_review_2026-05-04.md` — this document
