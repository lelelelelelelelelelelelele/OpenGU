# §5.2 Scaling Validation on ogbn-arxiv

> Status: outline
> Parent: §5 Results
> Depends on: Phase B.1 (feasibility 5-cell) + B.2 (full 36-cell arxiv matrix)
> Updated: 2026-05-05

## Claim

Vulnerability Fingerprint geometry observed on Cora/Citeseer **persists at 169K-node scale** — vulnerability is intrinsic to mechanism, not an artifact of small-graph anomalies.

## Content

- Cell-by-cell comparison: arxiv fingerprint vs Cora/Citeseer fingerprint, same method
- 11-item metric gate from `phase_b_arxiv_feasibility.yaml` (B.1) — pass/fail summary up front
- Heterogeneity discussion if any family shifts region at scale
- FIG-1 (Generalization) embedded here (or merged into §5.1 fingerprint plot's marker scheme)

## Evidence binding

- Data: `results/runs/arxiv_*_r0.05/{method}_{strategy}/seed*/`
- Gate definitions: `experiments/configs/phase_b_arxiv_feasibility.yaml` + `self/dashboard/METRICS_CATALOG.md`

## Open questions

- **Q-5.2.1**: separate §5.2 figure, or just an extra dataset color in the §5.1 fingerprint? *Lean toward including arxiv as a dataset marker in §5.1, keep §5.2 as discussion-only with cell-level table.*
- **Q-5.2.2**: how to handle if arxiv breaks the cluster pattern (e.g., GNNDelete drops to origin) — write as positive scaling-related finding?

## Cross-refs

- ← §5.1 (extends fingerprint claim to scale)
- ← §4.6 (scaling protocol details)
- → §6.3 (limitation: 3 seeds, Physics OOS)
