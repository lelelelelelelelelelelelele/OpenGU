# §4 Experimental Setup

> Status: outline (current draft `overleaf/sec/4_experiment.tex`, 50 lines)
> Parent: §4
> Depends on: Phase B configs in `experiments/configs/`
> Updated: 2026-05-05

## Subsections

- **4.1 Datasets and backbones** — Cora (2,708) / Citeseer (3,327) / ogbn-arxiv (169,343) × GCN / GAT
- **4.2 Unlearning methods** — **6 methods** under the official OpenGU 4-category taxonomy (Partition / IF / Learning / Others; see upstream `OpenGU/README.md`). Coverage:
  - **Partition-based**: GraphEraser + **GraphRevoker** *(pending feasibility gate — re-wire `unlearning_manager.py:40` to dispatch to `graphrevoker` class instead of alias to `grapheraser`; sanity test on cora/GCN single seed before committing main matrix runs)*. GUIDE excluded per INSTRUCTIONS.md hard constraint.
  - **IF-based**: GIF (canonical Newton-step) + IDEA (certified-gradient — predicted intra-family outlier)
  - **Learning-based**: GNNDelete (deletion-aware proximal) + MEGU (mutual-evolution — predicted intra-family outlier)
  - **Others** (UtU, Projector): not covered in this paper; future work
  - **Backup / contingency** (3rd-member 2→3 candidates, deprioritized — marginal value < 1→2 pairing): GST (3rd IF), GUKD (3rd Learning). Add only if cycles permit or if GraphRevoker fails feasibility.
  Family selection rationale: with GraphRevoker re-wired, **all 3 covered categories have intra-family pairs (n=2)**, enabling consistent intra-family coherence testing across Partition / IF / Learning (§5.1). Partition pair is canonical+canonical (both legit partition methods, neither pre-labeled outlier); IF and Learning pairs are canonical+predicted-outlier.
- **4.3 Attack budget and seeds** — main matrix r=0.05, 5 seeds Cora/Citeseer (42, 212, 722, 1337, 2024), 3 seeds ogbn-arxiv. IM selector seed fixed at 2024. Ratio sweep r ∈ {0.01, 0.05, 0.10, 0.20} on cora/GCN reported in §A.5.
- **4.4 Reporting protocol** — paired effect (per-seed F1 difference vs matched random), 95% bootstrap CI, one-sided t-test against $\mu \le 0$. MIA via shadow-model.
- **4.5 Implementation** — PyTorch + PyG, Adam (lr 1e-2, wd 5e-4), 100 epochs Cora/Citeseer (200 arxiv). batch-CELF candidate-fraction 0.1, 50 MC rounds, 34× speedup over brute CELF.
- **4.6 Scaling to ogbn-arxiv** *(NEW)*:
  - Why 3 seeds not 5 (GPU-h budget; brief power note)
  - TracIn G-matrix at 169K nodes — chunked or subsampled (Physics OOS, see §6.3)
  - IM candidate-fraction at scale
  - GCN config differs (3 layers / hidden 256) — affects hop-decay buckets

## Evidence binding

- Existing draft: `overleaf/sec/4_experiment.tex`
- Phase B config: `experiments/configs/phase_b_arxiv*.yaml`, `phase_b_cora_*.yaml`
- 4.6 sourcing: `self/limitations.md`

## Open questions

- **Q-4.6.1**: §4.6 lives here (protocol) or moved to §5 as "scaling validation" prelude? *Current vote: §4.6 — protocol stays with protocol.*
- **Q-4.3**: report power-analysis explicitly for the 3-seed arxiv setting?

## Cross-refs

- → §3.3 (metrics defined there)
- → §5.2 (results on arxiv use this protocol)
