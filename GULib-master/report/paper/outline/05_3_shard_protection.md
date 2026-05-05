# §5.3 Shard Protection Effect  *(finding subsection)*

> Status: outline
> Parent: §5 Results
> Depends on: Phase B (cora/GCN, cora/GAT, citeseer/GCN GraphEraser cells; existing data corroborates)
> Updated: 2026-05-05

## Claim

GraphEraser exhibits a **counter-intuitive defensive property**: F1 *increases* under both random and adversarial deletion at small budgets ($r \le 0.05$). The attacker's gain on this family is **bounded above by random selection** — i.e., adversarial selection cannot beat random.

## Content arc

1. Empirical observation (table: paired effect across strategies, all near zero or negative)
2. **Fingerprint geometry** (forward-link to §5.1): GraphEraser's coordinates near origin or Q3 — visible at a glance
3. **Mechanism interpretation**: shard partitioning + aggregation acts as deletion-induced regularizer; small-budget deletion removes some shard's noise without crossing inter-shard information
4. **Robustness check**: §A.2 ablation — effect persists across shard counts ∈ {5, 10, 20} and aggregator variants; confirms mechanism-driven not hyperparameter artifact
5. **Implication**: defensive insight — partition-aggregate architectures attenuate small-budget targeted forgetting; dual-use note → §6.4

## Evidence binding

- Data: `results/runs/{cora,citeseer}_{GCN,GAT}_r0.05/grapheraser_*/seed*/attack.json`
- Pre-Phase-B corroboration: `mg0_completion` results show consistent pattern (with caveat: bug-polluted, see dashboard §3.1 — but the *direction* is robust to the MIA bug since it's an F1 finding, not MIA)
- Robustness: §A.2 shard-count ablation

## Open questions

- **Q-5.3.1**: framing — "defensive discovery" vs "evaluation gap" (i.e., maybe better selectors could break it). Honest answer: A.2 should include hybrid-targeted-at-shard variants if cycles permit.
- **Q-5.3.2**: explicit theoretical bound on attacker gain on shard-based methods? Currently empirical; theoretical statement (e.g., "bounded by partition variance") would lift the contribution but is risky to claim in 3 days.

## Cross-refs

- ← §5.1 (geometric position in fingerprint)
- → §A.2 (shard-count robustness)
- → §6.2 / §6.4 (mechanism interpretation + dual-use)
