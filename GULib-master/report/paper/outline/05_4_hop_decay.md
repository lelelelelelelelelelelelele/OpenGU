# §5.4 Collateral Damage and Hop-distance Decay

> Status: outline
> Parent: §5 Results
> Depends on: Phase B (collateral.json files contain hop-decay buckets)
> Updated: 2026-05-05

## Claims

1. **Retrain gap** separates approximation error from data-informativeness. Methods differ in how faithfully they approximate retrain-from-scratch — independent of attack F1 drop.
2. **Prediction shift** scales with budget across families but with family-distinct slopes.
3. **Hop-distance decay** reveals two distinct attack signatures:
   - **Localized**: damage concentrated at $h\le 2$, drops sharply beyond — selector hit the receptive field cleanly
   - **Propagating**: damage roughly uniform across $h\in\{1,2,3,>3\}$ — approximation error bleeds globally

## Content

- Per-method collateral table (retrain gap, prediction shift, MIA AUC)
- **Hop-decay curve figure** (FIG-2): per-family lines, bucket on x-axis, F1 change on y-axis. Compare to GCN num-layers (2 vs 3 on arxiv).
- Discussion: which family-strategy combinations propagate vs localize; ties to whether the attack exploits the *mechanism* or just the *data*

## Evidence binding

- Data: `results/runs/{cell}/{method}_{strategy}/seed*/collateral.json` — already includes 4-bucket hop-decay (Phase A.5 done 2026-05-04)
- Implementation: `attack/attack_eval.py::evaluate_collateral_damage`

## Open questions

- **Q-5.4.1**: bucket boundaries — keep $\{1,2,3,>3\}$ or normalize to GCN-layer-count (e.g., within-RF / boundary / outside-RF)?
- **Q-5.4.2**: error bars per bucket across seeds — overlay or separate panel?

## Cross-refs

- ← §3.3 (diagnostic definitions)
- → §6.2 (mechanism interpretation: propagation patterns vs receptive-field structure)
