# §A.2 Ablation — GraphEraser Shard Configuration  *(MUST)*

> Status: outline (data needs collection)
> Parent: §A Appendix
> Depends on: extra Phase B runs — GraphEraser × shard ∈ {5, 10, 20} on cora/GCN
> Updated: 2026-05-05

## Purpose

Lock down the **Shard Protection Effect** (§5.3) as a mechanism-driven property, not a hyperparameter coincidence. If F1-increase persists across shard counts and aggregator variants, the §5.3 claim survives the obvious reviewer challenge.

## Content

- Shard counts: $\{5, 10, 20\}$ (default in our main matrix is method-default, document which)
- Aggregator: mean (default); attention if implemented
- Strategies: random + im + hybrid (covers black-box + grey-box ends)
- Cell: cora/GCN/r=0.05, 5 seeds (cheap on 4090)

## Expected outcome

- Paired effect remains $\le 0$ across all shard counts → mechanism-driven (claim holds)
- Or: shard count modulates protection strength → modify §5.3 claim to "for shard count in [a, b]"

## Evidence binding

- Code: `unlearning/unlearning_methods/GraphEraser/grapheraser.py` — shard-count parameter
- Output: `results/runs/cora_GCN_r0.05/grapheraser_{strategy}/seed*/attack.json` with `_meta.json::shard_count` recorded

## Open questions

- **Q-A.2.1**: include hybrid-targeting-shard-boundary variant (selector aware of partition structure)? More expensive, but addresses §5.3 Q-5.3.1 ("could a smarter attacker break it?")
- **Q-A.2.2**: same on cora/GAT? Bigger ablation but supports claim's generality

## Cross-refs

- ← §5.3 (this ablation backs that claim)
- → §6.2 (mechanism interpretation)
