# §2 Related Work

> Status: outline
> Parent: §2
> Depends on: literature notes in `self/paper_library_synthesis_2026-02-16.md`
> Updated: 2026-05-05

## Subsections

- **2.1 Approximate Graph Unlearning** — three families (learning-based, IF-based, shard-based) + feature-preserving (MEGU) and certified-gradient (IDEA) outliers
- **2.2 Adversarial Unlearning** — prior on tabular/images (camouflage, deletion-as-poisoning); graph adversarial-deletion is the gap
- **2.3 Influence-based Selection** — TracIn, classical IM/CELF; we adapt both to deletion-amplification
- **2.4 MIA on GNNs and model auditing** — Olatunji et al. shadow-model MIA is related literature; this paper reports a method-native posterior-shift deletion-membership audit instead of standard shadow-model MIA

## Evidence binding

- Primary source: `self/paper_library_synthesis_2026-02-16.md` (~734 lines)
- Refs: pruthi2020estimating (TracIn), goyal2011celf++ (IM), olatunji2021membership (MIA), method papers cited in §4

## Open questions

- **Q-2.1**: include vision-graph application context (scene graphs / skeleton-action / 3D point cloud) or trim for venue?
