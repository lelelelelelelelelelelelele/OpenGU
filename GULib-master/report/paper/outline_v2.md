# Paper Outline v2 — Index

> Created: 2026-05-05 — restructured as **index-only** per user request
> Target venue: NeurIPS 2026 (deadline 2026-05-07)
> Submission scaffold: `overleaf/sec/`
>
> **This file is just the order + pointers.** Each subsection has its own dedicated file under `outline/`. Discuss/edit one piece at a time there; this file rarely changes.

---

## Section order and file map

| § | Title | File | Status | Data dep. |
|---|---|---|---|---|
| 0 | Abstract | `sections/abstract.md` (interim, refresh in C.5) | drafted, awaits Phase B numbers | Phase B |
| 1 | Introduction | `outline/01_intro.md` | outline | — (write after §3/§5) |
| 2 | Related Work | `outline/02_related_work.md` | outline | literature only |
| 3 | **Attack Framework** *(was: Method)* | — | — | — |
| 3.1 | Threat Model + Access Spectrum | `outline/03_1_threat_model.md` | outline | none, writeable now |
| 3.2 | Selection Strategies (incl. α as mixing parameter) | `outline/03_2_selectors.md` | outline | none, writeable now |
| 3.3 | Collateral Diagnostics *(was: Metrics)* | `outline/03_3_collateral_diagnostics.md` | outline | none, writeable now |
| 4 | Experimental Setup | `outline/04_experimental_setup.md` | outline (incl. §4.6 Scaling to ogbn-arxiv) | Phase B configs |
| 5 | **Results** | — | — | — |
| 5.1 | **Vulnerability Fingerprint** *(headline 2D plot)* | `outline/05_1_vulnerability_fingerprint.md` | outline | Phase B main matrix |
| 5.2 | Scaling Validation on ogbn-arxiv | `outline/05_2_scaling_arxiv.md` | outline | Phase B.1 + B.2 |
| 5.3 | Shard Protection Effect | `outline/05_3_shard_protection.md` | outline | Phase B GraphEraser cells |
| 5.4 | Collateral Damage and Hop-decay | `outline/05_4_hop_decay.md` | outline | Phase B collateral.json |
| 5.5 | MIA Audit | `outline/05_5_mia.md` | outline | Phase B (post bug-fix) |
| 6 | Conclusion / Limitations | `outline/06_conclusion_limitations.md` | outline | §1–§5 stable |
| 6.3-L7 | Limitation: high-dim slicing as display strategy | `outline/06_3_visualization_limitation.md` | drafted (limitation paragraph ready) | none — writeable now |
| A.1 | Ablation: IM Selector Seed Decoupling | `outline/A1_im_seed.md` | outline (must-have) | existing pre/post A.4 + B |
| A.2 | Ablation: GraphEraser Shard Configuration | `outline/A2_shard_count.md` | outline (must-have, supports §5.3) | new runs needed |
| A.3 | **Ablation: α-sweep as Synergy Diagnostic** | `outline/A3_alpha_synergy.md` | outline (confirmed scope) | new runs scheduled |
| A.4 | Ablation: IM Hyperparameters | `outline/A4_im_hyperparams.md` | outline (should-have) | new runs (small) |
| A.5 | **Ablation: Deletion Ratio Sweep** | `outline/A5_ratio_sweep.md` | outline (must-have, user-requested) | new runs on cora/GCN |
| B | NeurIPS Reproducibility Checklist | `outline/B_checklist.md` | outline (mechanical) | §1–§6 stable |

---

## Per-file conventions

Each `outline/*.md` has the same shape:
- **Status** (outline / drafting / drafted / under review)
- **Parent** §
- **Depends on** (data / phase / other section)
- **Content claims** (bullets)
- **Evidence binding** (data path, figure path, code refs)
- **Open questions** (Q-§.N — answerable by user, drives discussion)
- **Cross-refs** (← upstream / → downstream sections)

---

## Locked decisions (2026-05-05, revised after upstream OpenGU README check + +1 Partition pair)

- **Family taxonomy**: aligned with **upstream OpenGU 4-category taxonomy** (Partition / IF / Learning / Others) — `H:/project/OpenGU/README.md`. Paper covers 3 of 4 categories with intra-family pair in each; "Others" deferred.
- **Methods = 6, all 3 covered categories have n=2 intra-family pairs**:
  - Partition-based: **GraphEraser** + **GraphRevoker** *(GraphRevoker pending feasibility gate — un-alias `unlearning_manager.py:40` + sanity test in separate local session)*
  - IF-based: **GIF** (canonical) + **IDEA** (predicted intra-family outlier)
  - Learning-based: **GNNDelete** (canonical) + **MEGU** (predicted intra-family outlier)
- **Three pair signatures**: convergent (Partition pair predicted) vs outlier (IF, Learning predicted) — contrast across signatures is a headline insight
- **F1 shift decomposition** $\Delta F_{\text{total}} = \Delta F_{\text{arch}} + \Delta F_{\text{attack}}$: Shard Protection lives in the **architectural term** (k=5 baseline already captures it; not an attack-specific finding); fingerprint plots the **attack term** only. Decomposition formalized in §3.3, separated reporting in §5.1 (attack term) + §5.3 (arch term bar chart).
- **Backup / contingency** (deprioritized; 2→3 marginal value < 1→2): GST (3rd IF), GUKD (3rd Learning) — listed as future work or fallback if GraphRevoker fails sanity
- **Canonical cell** for §5.1 headline figure: cora/GCN/r=0.05
- **§A.5 ratio sweep added** — must-have

## Compute budget summary

Reference per-cell time on cora/GCN: ~30 s/cell (from `phase_b_cora_gcn.yaml` 150-cell / 75-min benchmark).

| Workload | Cells | 4090 estimate | Notes |
|---|---|---|---|
| Cora/GCN main matrix (5+1 method × 6 strategy × 5 seed) | 180 | ~90 min | +1 = GraphRevoker |
| Cora/GAT main matrix | 180 | ~120 min | GAT slower per-cell |
| Citeseer/GCN main matrix | 180 | ~90 min | — |
| §A.3 α-sweep (6 × 3 internal α × 2 cell × 5 seed) | 180 | ~90 min | small graphs only |
| §A.5 ratio-sweep (6 × 4 × 3 × 5) | 360 | ~3 h | cora/GCN only |
| **Small-graph new work total** | — | **~8 h** sustained | parallelizable across 2 GPUs if available |
| Arxiv (5 method × 4 strategy × 3 seed) | 60 | ~12 GPU-h on A100 (B.1.5 split workflow) | unchanged from existing plan |

**Known pitfalls** (`self/limitations.md`):
- L2 TracIn × arxiv G-matrix: needs ≥40 GB GPU. Resolved via 2-stage workflow.
- L3 IM × arxiv default params 10 h+: resolved via tuned `candidate_fraction` + `mc_rounds` in `phase_b_arxiv.yaml`.
- L5 Shard-based MIA CPU-bound (1000% CPU / 0% GPU): rent CPU-rich instances; affects GraphEraser, GraphRevoker MIA timing.

**Decision**: GraphRevoker / α-sweep / ratio-sweep do NOT extend to arxiv — small-graph only. Phase B arxiv budget unchanged.

## How to discuss / iterate

1. Pick one file → discuss its open questions in turn.
2. Decisions land back in that file (status → drafting; questions resolved or escalated).
3. This index file stays thin — only update if section *order* changes or a new piece is added.
4. When a piece is drafted to overleaf section file, mark Status=drafted and link to the `.tex` location.

---

## Mapping to dashboard Phase C TODOs

| C-task (dashboard §1) | Lands in |
|---|---|
| C.1 重画 FIG-4b | §5.1 (now Vulnerability Fingerprint figure) |
| C.2 hop-decay 衰减曲线图 | §5.4 |
| C.3 §method 含 B1/B2 选择讨论 + Shard Protection 解读 | §3.2 + §5.3 |
| C.4 §limitation 含 MEGU/IDEA mechanism-incomparable framing | §6.2 + §6.3 |
| C.5 abstract refresh | `sections/abstract.md` |

---

## Open Questions Index (live)

Each Q lives in its file; this is a roll-up for quick scan.

| Q | File | Topic |
|---|---|---|
| Q-1.1 | `01_intro.md` | contribution ordering: methodology-first vs finding-first |
| Q-2.1 | `02_related_work.md` | vision-graph framing — keep or trim |
| Q-3.1.1 / .2 | `03_1_threat_model.md` | access-spectrum format; deletion-as-poisoning contrast |
| Q-3.2.1 / .2 | `03_2_selectors.md` | f(α) preview in §3.2; α=0.5 as default vs sweep entry |
| Q-3.3.1 / .2 | `03_3_collateral_diagnostics.md` | 4th diagnostic; hop-decay normalization |
| Q-4.6.1 / Q-4.3 | `04_experimental_setup.md` | §4.6 placement; arxiv power analysis |
| Q-5.1.1 / .2 / .3 | `05_1_vulnerability_fingerprint.md` | error ellipse; inset bar; figure name |
| Q-5.2.1 / .2 | `05_2_scaling_arxiv.md` | arxiv as marker vs section; cluster-break handling |
| Q-5.3.1 / .2 | `05_3_shard_protection.md` | defensive vs evaluation gap framing; theoretical bound |
| Q-5.4.1 / .2 | `05_4_hop_decay.md` | bucket boundaries; per-bucket error bars |
| Q-5.5.1 / .2 / .3 | `05_5_mia.md` | merge with §5.4; baseline floor; paired MIA reporting |
| Q-6.2.1 / Q-6.3 | `06_conclusion_limitations.md` | MEGU/IDEA framing spin; L1 placement |
| Q-A.1.1 / .2 | `A1_im_seed.md` | hybrid Jaccard placement; explicit power statement |
| Q-A.2.1 / .2 | `A2_shard_count.md` | partition-aware selector variant; cora/GAT extension |
| Q-A.3.1 / .2 / .3 | `A3_alpha_synergy.md` | 5 vs 7 α points; curvature index; budget-dependence sweep |
| Q-A.4.1 / .2 | `A4_im_hyperparams.md` | arxiv-scale verification; priority in 3-day window |
| Q-A.5.1–.4 | `A5_ratio_sweep.md` | high-r breakage; α-extension; arxiv sweep; elasticity statistic |
| Q-5.1.4 | `05_1_vulnerability_fingerprint.md` | canonical cell choice for headline figure |
| Q-L7.1–.3 | `06_3_visualization_limitation.md` | main vs appendix placement; appendix all-axes figure; venue expectation |
