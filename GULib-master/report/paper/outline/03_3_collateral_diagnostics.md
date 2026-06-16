# §3.3 Collateral Diagnostics  *(was: Evaluation Metrics)*

> Status: outline (current draft `overleaf/sec/3_method.tex` §3.3)
> Parent: §3 Attack Framework
> Depends on: nothing (writeable now)
> Updated: 2026-05-07

## Content

Position as **paper contribution**, not standard evaluation. Rationale: F1 drop alone conflates "targeted forgetting" with "approximation-error spillover". The three diagnostics decompose this.

### F1 shift decomposition (foundation)

Before defining the collateral diagnostics, we make explicit a three-term decomposition:

$$
\Delta F_{\text{noise}}
= \mathbb{E}_{R_5}[\Delta F_{\text{total}}(R_5)],
\qquad
\Delta F_{\text{rand}}(r)
= \mathbb{E}_{R_r}[\Delta F_{\text{total}}(R_r)].
$$

where:
- $\Delta F_{\text{total}}(S) = F_1(f_\theta; V_{\text{te}}) - F_1(\mathcal{U}(f_\theta, \cdot, S); V_{\text{te}})$ — observed F1 drop after attack-driven unlearning of set $S$; positive means utility degradation.
- $\Delta F_{\text{noise}}$ — **k=5 noise floor**: expected F1 drop when only five uniformly random training nodes are unlearned. This diagnoses the method's intrinsic near-zero-volume response.
- $\Delta F_{\text{rand}}(r)$ — **budget-matched random baseline**: expected F1 drop under random deletion at the same ratio $r$ as the attack.
- $\Delta F_{\text{volume}}(r) = \Delta F_{\text{rand}}(r) - \Delta F_{\text{noise}}$ — **budget-induced shift**: the extra random-deletion response from moving from k=5 to the attack budget.
- $\Delta F_{\text{attack}}(S) = \Delta F_{\text{total}}(S) - \Delta F_{\text{rand}}(r)$ — **attack-specific** signal; estimated as paired-effect = strategy drop minus same-seed budget-matched random drop.

So

$$\Delta F_{\text{total}}(S)=\Delta F_{\text{noise}}+\Delta F_{\text{volume}}(r)+\Delta F_{\text{attack}}(S).$$

This decomposition surfaces three distinct findings:
- $\Delta F_{\text{noise}}$ varies across methods even at negligible deletion volume — most methods ≈ 0, but **partition methods exhibit negative $\Delta F_{\text{noise}}$** (Shard Protection, §5.3); the k=5 random baseline (`results/baseline/k5_random/`) captures this.
- $\Delta F_{\text{volume}}$ separates budget-induced random-deletion degradation from intrinsic method response.
- $\Delta F_{\text{attack}}$ is what our attack toolkit (TracIn / IM / Hybrid) induces above the same-budget random selector; this is the quantity plotted in the §5.1 Vulnerability Fingerprint and tested in paired $t$-tests.

Reporting all three terms is what allows §5.3 to attribute Shard Protection to the k=5 noise floor, separate budget effects, and keep attack claims tied to budget-matched random.

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
- **Q-3.3.3** *(decomposition)*: report $\Delta F_{\text{noise}}$ in main text §5 (1D bar chart per method) or as appendix supplementary table? Lean main text — Shard Protection visibility justifies the column inch.

## Cross-refs

- → §5.1 (fingerprint axes are $\Delta F_{\text{attack}}$ at α=0 and α=1)
- → §5.3 (Shard Protection lives in the $\Delta F_{\text{noise}}$ k=5 diagnostic; this section provides the formal scaffold)
- → §5.4 (hop-decay curves — orthogonal collateral signal)
