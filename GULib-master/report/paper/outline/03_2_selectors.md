# §3.2 Selection Strategies

> Status: outline (current draft `overleaf/sec/3_method.tex` L36–76)
> Parent: §3 Attack Framework
> Depends on: nothing (writeable now)
> Updated: 2026-05-05

## Content (6 selectors)

### Black-box
- **Random** — uniform without replacement
- **Degree** — top-$k$ by node degree (high-influence heuristic)
- **PageRank** — top-$k$ by personalized PageRank centrality

### Grey-box
- **TracIn** (pseudo-IF) — gradient inner-product across checkpoints (Eq. 2). Top-$k$ by $|\mathrm{TracIn}(v)|$.
- **IM (batch-CELF)** — IC simulation under $p_{uv}=1/\deg(v)$, lazy submodular evaluation. Key design: `im_selector_seed=2024` decoupled from GNN training seed (Phase A.4 fix; Jaccard 1.0 across GNN seeds).
- **Hybrid IF+IM** — $\alpha\cdot\widetilde{\mathrm{TracIn}}(v) + (1-\alpha)\cdot\widetilde{\mathrm{IM}}(v)$, min-max normalized.
  - **REFRAMED**: $\alpha$ is a mixing parameter. $\alpha=1$ ≡ TracIn-only, $\alpha=0$ ≡ IM-only — these are the **basis axes** of the Vulnerability Fingerprint (§5.1). The curve $f(\alpha)$ is the **synergy diagnostic** in §A.3 (shape ↔ independence/synergy/redundancy).
  - Default α=0.5 used in main matrix; sweep in §A.3.

## Evidence binding

- Existing draft: `overleaf/sec/3_method.tex` L36–76
- IM seed decoupling: dashboard §3.3 + V-2026-05-04-04
- Code: `attack/attack_strategies/{tracin,im,hybrid}_strategy.py`

## Open questions

- **Q-3.2.1**: explicit convexity statement for $f(\alpha)$ in §3.2 (preview), or save full discussion for §A.3?
- **Q-3.2.2**: keep α=0.5 as default in the *main* table, or fold α=0.5 row into the §A.3 sweep entirely?

## Cross-refs

- → §3.1 (access tier per strategy)
- → §5.1 (fingerprint axes = α=0 / α=1 endpoint effects)
- → §A.3 (α-sweep synergy curve)
