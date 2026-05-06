# §A.4 Ablation — IM Hyperparameters  *(SHOULD)*

> Status: outline (lower priority)
> Parent: §A Appendix
> Depends on: extra Phase B runs (small)
> Updated: 2026-05-05

## Purpose

Defends two claims:
1. The "34× speedup with <2% spread loss" claim about batch-CELF in §4.5
2. The IM scaling story to ogbn-arxiv (§4.6)

## Content

- **candidate-fraction sweep**: $\{0.05, 0.1, 0.2\}$ on cora/GCN/GIF/r=0.05
- **MC rounds sweep**: $\{25, 50, 100\}$ on cora/GCN/GIF/r=0.05
- Report: paired effect + selection-set Jaccard with full-CELF reference + wall-clock

## Evidence binding

- Data: `results/runs/cora_GCN_r0.05/gif_im/seed*` with `_meta.json::im_candidate_fraction` and `im_mc_rounds` recorded
- Reference: full-CELF baseline (1 seed, no batch optimization)

## Open questions

- **Q-A.4.1**: include arxiv-scale verification (smaller candidate-fraction at 169K)? Adds runs but supports §4.6.
- **Q-A.4.2**: prioritize this against the must-have A.1/A.2/A.3 in 3-day window? *Vote: skip if cycles tight; this is a methodology defense, not a finding.*

## Cross-refs

- ← §3.2 (IM strategy definition)
- ← §4.5 (speedup claim)
- ← §4.6 (scaling protocol)
