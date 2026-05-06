# §6.3 Limitation L7 — High-Dimensional Slicing as Display Strategy

> Status: outline — working document for L7 paragraph
> Parent: §6.3 Limitations (with cross-link to §A appendix design)
> Depends on: nothing (writeable now; refines as figures lock)
> Updated: 2026-05-05

## 1. The dimensionality problem (sized)

The experimental design has ≥7 axes:

| Axis | Levels | Levels (canonical) |
|---|---|---|
| method | GraphEraser, GraphRevoker, GIF, IDEA, GNNDelete, MEGU (3 OpenGU categories, n=2 each) | 6 |
| dataset | cora, citeseer, ogbn-arxiv | 3 |
| backbone | GCN, GAT | 2 |
| strategy | random, degree, pagerank, im, tracin (+ hybrid α extension) | 5–10 |
| seed | 5 small / 3 arxiv | ~5 |
| ratio | r ∈ {0.01, 0.05, 0.10, 0.20} (main fixes 0.05) | 4 |
| α (hybrid) | {0.0, 0.25, 0.5, 0.75, 1.0} (main fixes 0.5) | 5 |

Full Cartesian product ≈ 36,000 runs. Our main matrix + ablations sample ≈ 1,500 — **<5 % of the design space**. No single 2D plot can honestly summarize this. Reviewers will rightly ask which axes were tested vs. held fixed, and what conclusions hold under which conditioning.

## 2. The strategy we adopted: section-conditional slicing

Rather than projecting to a low-dim space, we **condition on different axes in different sections**, varying only what each claim requires:

| Section | Fixed / collapsed | Varied | Claim addressed |
|---|---|---|---|
| §5.1 main fingerprint | dataset=cora, backbone=GCN, r=0.05 | 6 methods × 5 seeds | family cluster geometry (canonical cell) |
| §5.2 scaling | backbone=GCN, r=0.05 | dataset ∈ {cora, citeseer, arxiv} | fingerprint scale-invariance |
| §A backbone robustness (small-multiples) | dataset=cora, r=0.05 | backbone ∈ {GCN, GAT} | fingerprint backbone-invariance |
| §5.3 / §5.4 / §5.5 | strategy collapsed to paired-effect summary | method × dataset × backbone | per-axis single-claim (Shard Protection / hop-decay / update-detection) |
| §A.3 α-sweep | dataset=cora, r=0.05 | method × backbone × α | synergy / redundancy diagnostic |
| §A.5 ratio sweep | dataset=cora, backbone=GCN, α ∈ {0, 1} | method × strategy × r | per-family budget elasticity |

This converts "visualize 7-D data" into a sequence of "claim-conditional 2-D/3-D plots", each independently readable.

## 3. What this slicing supports — and what it doesn't

### Supported claims
- **Method fingerprint** at canonical cell: 30 raw points → 6 ellipse-summarized clusters
- **Family cluster** for the 2 paired families (IF: GIF+GST; mechanism-decoupled: MEGU+IDEA)
- **Scale invariance** of geometry across {cora, citeseer, arxiv} at (GCN, r=0.05)
- **Backbone invariance** across {GCN, GAT} at (cora, r=0.05)
- **Budget elasticity** per family at (cora, GCN)
- **Synergy diagnostic** per family at (cora, r=0.05)

### Untested cells (explicit out-of-scope)
- **Joint (dataset, backbone)** off-diagonal: citeseer/GAT, arxiv/GAT
- **Joint (α, r)** grid: is synergy budget-dependent?
- **Strategy × ratio** for degree/pagerank/hybrid (only random/im/tracin in §A.5)
- **Within-family extension beyond n=2**: the IF and mechanism-decoupled cluster claims are *point-pair coherence*, not regression. A third member (e.g., adding CGU to mechanism-decoupled) would strengthen but is not in budget.
- **Single-representative families** (Learning-based, Shard-based): no intra-family coherence test possible

### How generalization is justified
Cross-cell claims rest on **inductive consistency across tested slices**, not on a Cartesian-complete low-dim projection. We do *not* claim the 2-D fingerprint is a sufficient statistic for the full design; we claim that in every conditioning tested, the geometry was consistent. Failures at untested cells would not be a contradiction — they would be a discovery the paper is not equipped to make.

## 4. Alternatives considered and why rejected

| Strategy | Pros | Cons | Decision |
|---|---|---|---|
| PCA on per-cell feature vector | one 2-D plot covers variance | axes lose physical meaning; "PC1" doesn't answer "which mechanism" | rejected — sacrifices interpretability |
| UMAP / t-SNE | better cluster preservation | non-linear, n < 100 unstable, hyperparameter-fragile | rejected |
| Parallel coordinates | shows all axes simultaneously | visually noisy at 30+ points; cluster reading hard | rejected for headline; possible for §A appendix |
| Heatmap + hierarchical clustering | compact 5×5 summary tables | destroys 2-D Cartesian geometry that **is** our claim | used selectively for §5.4 hop-decay tables |
| Small-multiples grid | honest, panel-by-panel comparison | grows large with axes | adopted for backbone / dataset robustness panels |
| Glyph plots / Chernoff faces | per-cell information density | non-quantitative | rejected |
| **Section-conditional slicing (ours)** | each claim has a clean plot; scope is explicit | multiple figures; reader integrates across sections | **adopted** |

The core decision: the (Δ_IM, Δ_TracIn) axes have direct mechanistic meaning (structural-spread vulnerability vs. gradient-signal vulnerability). Any visualization that destroys these axes — PCA, UMAP, glyphs — trades the paper's central conceptual contribution for compactness. We chose to pay in figure count instead.

## 5. Draft limitation paragraph for §6.3 L7

> **L7 (visualization scope).** The experimental design spans seven axes (method, dataset, backbone, strategy, seed, ratio, hybrid mixing α), well beyond what any single visualization can render honestly. We report results via section-conditional slicing — fixing a subset of axes per claim and varying only the axes germane to that claim — rather than a unified low-dimensional projection. Cross-cell generalizations (e.g., fingerprint geometry across (dataset, backbone) cells) rely on inductive consistency across tested slices, not on Cartesian-complete coverage. Untested combinations — notably citeseer/GAT, arxiv/GAT, the joint α × ratio grid, and strategy sweeps at non-default ratios — are explicitly out of scope. We chose this conditioning approach over dimensionality reduction (PCA, UMAP) to preserve the physical meaning of the fingerprint axes (structural-spread vs. gradient-signal vulnerability), at the cost of requiring readers to integrate across multiple figures.

## 6. Open questions

- **Q-L7.1**: include the §5 paragraph in main text §6.3, or move full discussion to §A and keep a one-sentence pointer in §6.3?
- **Q-L7.2**: produce one "all-axes" appendix figure (parallel coordinates or compact heatmap of paired-effect over the full sampled design) as reassurance that we did look at the full data, even if it's not the headline?
- **Q-L7.3**: do reviewers in target venue expect a single summary plot? If yes, the cheapest concession is an appendix biplot; consider before submission.

## Cross-refs

- ↔ §5.1 canonical cell (the *primary* slicing decision)
- ↔ §5.2 (dataset slice), §A backbone robustness (backbone slice)
- ↔ §A.3 (α slice), §A.5 (ratio slice)
- ↔ `self/limitations.md` (project-level limitations index — sync L7 there too)
