# §6 Conclusion / Discussion / Limitations

> Status: outline
> Parent: §6
> Depends on: §1–§5 stable
> Updated: 2026-05-05

## Subsections

### 6.1 Summary of contributions
Mirror §1 contribution list with realized findings (paired effect numbers, fingerprint geometry, hop-decay signatures).

### 6.2 Intra-family Outliers — Within-family Heterogeneity  *(aligned to OpenGU 4-category taxonomy)*
- MEGU and IDEA are not a separate "robust family" — they belong to **different parent categories** (Learning-based and IF-based respectively, per upstream OpenGU README). What unifies them is geometric: both sit far from their parent-category centroids in the Vulnerability Fingerprint, near the origin.
- **Mechanism reading**: mutual-evolution (MEGU) and certified-gradient (IDEA) are *intra-category alternatives* whose specific design decouples from the loss-gradient signal that TracIn and IM exploit — even though their family-mates (GNNDelete, GIF) do not exhibit this decoupling. The finding is **within-family heterogeneity**, not cross-family family-level robustness.
- **Open**: extend to other intra-family outliers — does GUKD (Learning, distillation) or CGU (IF, certified) also sit at the origin? Suggests a meta-property orthogonal to the official taxonomy.
- **Honest framing question (Q-6.2.1)**: is null effect a *robustness victory of the specific design* or an *evaluation gap of our selectors*? Probably both — write it that way.

### 6.3 Limitations *(condense from `self/limitations.md`)*
- **L1** (downgraded post-2026-05-04 per Phase A.2): GraphEraser shard-count not exhaustively swept — partial coverage in §A.2
- **L2**: ogbn-arxiv 3 seeds (not 5) — power tradeoff at scale
- **L3**: TracIn G-matrix doesn't scale to feature-dim 8415 → Physics dataset out of scope
- **L4**: grey-box assumption — white-box attacker not evaluated; coalition-of-users is the realistic threat
- **L5** *(downgraded by §A.5 ratio sweep)*: per-family budget elasticity now characterized on cora/GCN at r ∈ {0.01, 0.05, 0.10, 0.20}; arxiv ratio sweep remains future work
- **L6**: 6 GU methods covering 3 of 4 OpenGU categories (Partition: GraphEraser+GraphRevoker; IF: GIF+IDEA; Learning: GNNDelete+MEGU). All 3 covered categories have intra-family pairs (n=2). "Others" category (UtU, Projector) not covered. 2→3 within-family extension (e.g., GST as 3rd IF, GUKD as 3rd Learning) deprioritized — marginal value < 1→2 pairing — listed as future work. *Contingency*: if GraphRevoker fails feasibility gate, Partition reverts to n=1.
- **L7** *(visualization scope)*: 7-axis experimental design rendered via section-conditional slicing; cross-cell generalization rests on inductive consistency across tested slices, not Cartesian coverage. Detailed discussion: `outline/06_3_visualization_limitation.md`. Untested cells (citeseer/GAT, arxiv/GAT, joint α×ratio grid) explicitly OOS.

### 6.4 Broader impact
- Defensive insight (Shard Protection) is dual-use: same mechanism could mask malicious unlearning requests
- Responsible disclosure note for deletion-API platform operators
- No release of attack-tuned model checkpoints; only methodology and code

## Evidence binding

- Source: `self/limitations.md`, dashboard §4 (out-of-scope)
- Forward refs: §A.2 shard-count, §A.4 IM hyperparams

## Open questions

- **Q-6.2.1**: framing of MEGU/IDEA — robustness victory vs evaluation gap (affects narrative spin)
- **Q-6.3**: should L1 be in main paper limitations or only in appendix once §A.2 is filled?

## Cross-refs

- ← §5.1 (origin cluster = mechanism-incomparable)
- ← §5.5 (deletion-visibility axis decoupling complements null F1 effect)
