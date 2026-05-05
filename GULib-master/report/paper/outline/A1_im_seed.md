# §A.1 Ablation — IM Selector Seed Decoupling  *(MUST)*

> Status: outline
> Parent: §A Appendix
> Depends on: existing pre/post Phase A.4 data + new Phase B
> Updated: 2026-05-05

## Purpose

**Reviewer-shield**. Answers the question "how do you control selector stochasticity?" before anyone asks. Validates that the Vulnerability Fingerprint and α-sweep findings are not artifacts of selector noise.

## Content

- **Selection-set Jaccard table** (before vs after A.4 fix):

| Strategy | pre-A.4 (coupled) | post-A.4 (decoupled) |
|---|---|---|
| random | 0.023 | 0.023 (sanity) |
| im (was im_v4) | **0.129** | **1.000** |
| tracin | 0.415 | 0.415 |
| hybrid (was hybrid_v4) | 0.646 | TBD post-B |
| pagerank | 1.000 | 1.000 |
| degree | 1.000 | 1.000 |

- **CI width comparison** for paired-effect:
  - Show paired-effect 95% CI width on cora/GCN/r=0.05/IM strategy before vs after fix
  - Expected: CI width contracts substantially; effect-size mean changes minimally

## Evidence binding

- Data pre-fix: `results/experiments/mg0_completion/phase_a/` (legacy)
- Data post-fix: `results/runs/cora_GCN_r0.05/{method}_im/seed*/attack.json`
- Code: `attack/attack_strategies/im_strategy.py` (`im_selector_seed` arg, default 2024)
- Dashboard reference: §3.3

## Open questions

- **Q-A.1.1**: include hybrid Jaccard post-fix or defer to §A.3?
- **Q-A.1.2**: explicit power-analysis statement (e.g., "effect-size CI width reduced from X to Y, increasing detectable effect threshold from a to b")?

## Cross-refs

- ← §3.2 (selector design choice)
- ← §5.1 (fingerprint validity rests on this)
