# §4 Experimental Setup

> Status: outline (current draft `overleaf/sec/4_experiment.tex`, 50 lines)
> Parent: §4
> Depends on: Phase B configs in `experiments/configs/`
> Updated: 2026-07-20

## Subsections

- **4.1 Datasets and backbones** — Cora (2,708) / Citeseer (3,327) / ogbn-arxiv (169,343) × GCN / GAT
- **4.2 Unlearning methods** — **6 methods** under the official OpenGU 4-category taxonomy (Partition / IF / Learning / Others; see upstream `OpenGU/README.md`). Coverage:
  - **Partition-based**: GraphEraser + **GraphRevoker**. GraphRevoker's real dispatcher and shard-ensemble path passed the seed42 canary and the four-strategy E4 execution gate; pre-fix rows remain invalid, and archived multi-seed evidence must be used for final numbers. GUIDE is not evaluated in this paper; make no empirical claim about it.
  - **IF-based**: GIF (canonical Newton-step) + IDEA (certified-gradient — predicted intra-family outlier)
  - **Learning-based**: GNNDelete (deletion-aware proximal) + MEGU (mutual-evolution — predicted intra-family outlier)
  - **Others** (UtU, Projector): not covered in this paper; future work
  - **Backup / contingency** (3rd-member 2→3 candidates, deprioritized — marginal value < 1→2 pairing): GST (3rd IF), GUKD (3rd Learning). Add only if cycles permit or if GraphRevoker fails feasibility.
  Family selection rationale: with GraphRevoker re-wired, **all 3 covered categories have intra-family pairs (n=2)**, enabling consistent intra-family coherence testing across Partition / IF / Learning (§5.1). Partition pair is canonical+canonical (both legit partition methods, neither pre-labeled outlier); IF and Learning pairs are canonical+predicted-outlier.
- **4.3 Attack budget and seeds** — main matrix r=0.05, 5 seeds Cora/Citeseer (42, 212, 722, 1337, 2024), 3 seeds ogbn-arxiv. IM selector seed fixed at 2024. Ratio sweep r ∈ {0.01, 0.05, 0.10, 0.20} on cora/GCN reported in §A.5.
- **4.4 Reporting protocol** — paired effect (per-seed F1 difference vs matched random), 95% bootstrap CI, one-sided t-test against $\mu \le 0$. Update-detection AUC: positives are requested-for-unlearning nodes, negatives are held-out test nodes, score is before-vs-after posterior $L_2$ shift, metric is ROC-AUC.
- **4.5 Implementation** — PyTorch + PyG, Adam (lr 1e-2, wd 5e-4), 100 epochs Cora/Citeseer (200 arxiv). Batched CELF candidate-fraction 0.1, 50 MC rounds, 34× speedup over brute CELF.
- **4.6 Scaling to ogbn-arxiv** *(NEW)*:
  - Why 3 seeds not 5 (GPU-h budget; brief power note)
  - TracIn G-matrix at 169K nodes — chunked or subsampled (Physics OOS, see §6.3)
  - IM candidate-fraction at scale
  - GCN config differs (3 layers / hidden 256) — affects hop-decay buckets
- **4.7 Artifact generations, replay, and stability audit** — separate three non-overlapping evidence ledgers:
  - **V1 Baseline**: retain Legacy V1 outputs as a frozen, read-only historical baseline. They are not authoritative Cache V2 hits and do not count toward V2 completion.
  - **V2 Replay**: start formal matrix completion from zero under accepted Cache V2 runner paths; a selector enters the replay only after its versioned producer passes its acceptance gate. A paper cell is complete only when `attack.json`, `collateral.json`, `predictions.npz`, and `_meta.json` are present and the recorded config fingerprint matches the replay configuration. Infrastructure canaries validate the pipeline but are excluded from the paper matrix.
  - **V1↔V2 Check**: compare only exactly matched cells (dataset/split, backbone, GU method, selector algorithm and version, ratio, seed, candidate/budget, and training hyperparameters). If V1 provenance cannot establish an exact match, label the pair non-comparable.
  - Report paired V2−V1 deltas for F1/attack effect, retrain gap, prediction shift, and update-detection AUC; report selected-node overlap only when selector semantics are unchanged, and explicitly flag sign or method-ranking reversals.
  - Do not pool V1 and V2 rows. Primary tables and claims use V2 only; the compact V1↔V2 table is a reproducibility audit, not extra sample size or a formal equivalence claim.

## Evidence binding

- Existing draft: `overleaf/sec/4_experiment.tex`
- Phase B config: `experiments/configs/phase_b_arxiv*.yaml`, `phase_b_cora_*.yaml`
- 4.6 sourcing: `self/limitations.md`
- 4.7 runner contract: `experiments/run.py`, `experiments/configs/README.md`
- 4.7 Cache/Legacy boundary: `docs/cache_v2_rollout_syncmate_ACCEPTANCE_REPORT.md`, `docs/cache_v2_cutover_archive_readiness_ACCEPTANCE_REPORT.md`

## Open questions

- **Q-4.6.1**: §4.6 lives here (protocol) or moved to §5 as "scaling validation" prelude? *Current vote: §4.6 — protocol stays with protocol.*
- **Q-4.3**: report power-analysis explicitly for the 3-seed arxiv setting?
- **Q-4.7**: claim formal V1/V2 equivalence only if metric-specific margins are fixed before inspecting replay results; otherwise retain the default descriptive stability audit.

## Cross-refs

- → §3.3 (metrics defined there)
- → §5.2 (results on arxiv use this protocol)
