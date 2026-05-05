# §3.3 Collateral Diagnostics  *(was: Evaluation Metrics)*

> Status: outline (current draft `overleaf/sec/3_method.tex` L78–101)
> Parent: §3 Attack Framework
> Depends on: nothing (writeable now)
> Updated: 2026-05-05

## Content

Position as **paper contribution**, not standard evaluation. Rationale: F1 drop alone conflates "targeted forgetting" with "approximation-error spillover". The three diagnostics decompose this.

### Retrain gap
$\mathrm{Gap}(S) = L(f^{\mathrm{R}};V_{\mathrm{te}}) - L(f^{\mathrm{U}};V_{\mathrm{te}})$ — separates approximation error from data-informativeness.

### Prediction shift
Fraction of non-target test nodes with flipped predicted label between $f_\theta$ and $f^{\mathrm{U}}$.

### Hop-distance decay  *(novel contribution)*
- For each test node $v\notin S$, $h(v)=\min_{u\in S}d_G(v,u)$.
- 4 buckets: $h\in\{1,2,3,>3\}$.
- Per-bucket F1 change reveals **localized vs propagating** attack signatures.
- Ties to GCN num-layers (k-hop receptive field).

## Evidence binding

- Implementation: `attack/attack_eval.py::evaluate_collateral_damage` (Phase A.5 done 2026-05-04)
- Forward: §5.4 hop-decay curves figure (per family)

## Open questions

- **Q-3.3.1**: 4th diagnostic (e.g. label-flip rate per class)? Currently no — skip unless reviewer pressure-test surfaces gap.
- **Q-3.3.2**: hop-decay normalization — absolute F1 change or relative-to-bucket-baseline? Affects cross-method comparability.

## Cross-refs

- → §5.4 (hop-decay curves)
- → §5.3 (Shard Protection — retrain gap interpretation as regularization)
