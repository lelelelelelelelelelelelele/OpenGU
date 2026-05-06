# §3.3 Collateral Diagnostics  *(was: Evaluation Metrics)*

> Status: outline (current draft `overleaf/sec/3_method.tex` L78–101)
> Parent: §3 Attack Framework
> Depends on: nothing (writeable now)
> Updated: 2026-05-05

## Content

Position as **paper contribution**, not standard evaluation. Rationale: F1 drop alone conflates "targeted forgetting" with "approximation-error spillover". The three diagnostics decompose this.

### F1 shift decomposition (foundation)

Before defining the three collateral diagnostics, we make explicit a decomposition that paired-effect reporting already implicitly performs:

$$\Delta F_{\text{total}}(S) \;=\; \Delta F_{\text{arch}}(k) \;+\; \Delta F_{\text{attack}}(S)$$

where:
- $\Delta F_{\text{total}}(S) = F_1(\mathcal{U}(f_\theta, \cdot, S); V_{\text{te}}) - F_1(f_\theta; V_{\text{te}})$ — observed F1 shift after attack-driven unlearning of set $S$
- $\Delta F_{\text{arch}}(k) = \mathbb{E}_{R\sim\text{Uniform}(\mathcal{D}_{\text{tr}}, k)}[\Delta F_{\text{total}}(R)]$ — **architectural baseline**: expected F1 shift when *any* uniformly-random set of size $k=|S|$ is unlearned. Method-specific (depends on $\mathcal{U}$'s mechanism), seed-stable in expectation.
- $\Delta F_{\text{attack}}(S) = \Delta F_{\text{total}}(S) - \Delta F_{\text{arch}}(k)$ — **attack-specific** signal; estimated as paired-effect = strategy F1 minus same-seed random F1.

This decomposition surfaces two distinct findings:
- $\Delta F_{\text{arch}}$ varies across methods even at zero attack signal — most methods ≈ 0 (small data effect), but **partition methods exhibit negative $\Delta F_{\text{arch}}$** (Shard Protection, §5.3); the k=5 random baseline (`results/baseline/k5_random/`) already captures this.
- $\Delta F_{\text{attack}}$ is what our attack toolkit (TracIn / IM / Hybrid) induces above the architectural baseline; this is the quantity plotted in the §5.1 Vulnerability Fingerprint.

Reporting both terms separately is what allows §5.3 to honestly attribute Shard Protection to the architectural term, not to the attack.

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
- **Q-3.3.3** *(decomposition)*: report $\Delta F_{\text{arch}}$ in main text §5 (1D bar chart per method) or as appendix supplementary table? Lean main text — Shard Protection visibility justifies the column inch.

## Cross-refs

- → §5.1 (fingerprint axes are $\Delta F_{\text{attack}}$ at α=0 and α=1)
- → §5.3 (Shard Protection lives in $\Delta F_{\text{arch}}$ term; this section provides the formal scaffold)
- → §5.4 (hop-decay curves — orthogonal collateral signal)
