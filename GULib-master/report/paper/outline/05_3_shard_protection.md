# §5.3 Shard Protection — the Q3 Signature of Partition Family

> Status: outline (rewritten 2026-05-07 around the noise/volume/attack decomposition)
> Parent: §5 Results
> Depends on: Phase B GraphEraser + GraphRevoker cells; k=5 random baseline data already exists
> Updated: 2026-05-07

## Reframe — what Shard Protection actually is

Shard Protection is **not** an attack-specific finding. It is the **k=5 noise-floor diagnostic** $\Delta F_{\text{noise}}$ (defined in §3.3) for the Partition family, observed under near-zero-volume random deletion. The k=5 random baseline (`experiments/baseline_k5/`) already captures this signal — deleting only five random nodes produces F1 *increase* on shard methods. Our attack does not cause it; our attack does not amplify it.

So the integration into the paper is:
- **§5.1 Vulnerability Fingerprint** plots the *attack-specific* term $\Delta F_{\text{attack}}$ (= paired effect). Partition family lands near origin / Q3 here because $\Delta F_{\text{attack}}$ stays close to zero on shard methods — the attack adds little above the random baseline.
- **§5.3 (this section)** explicitly addresses $\Delta F_{\text{noise}}$, which is *negative* on shard methods. This is the Shard Protection signature; $\Delta F_{\text{volume}}(r)=\Delta F_{\text{rand}}(r)-\Delta F_{\text{noise}}$ then measures how much deletion volume changes that baseline.

The fingerprint and Shard Protection are surfaced separately because they answer different questions: $\Delta F_{\text{noise}}$ diagnoses the method's near-zero-volume response, $\Delta F_{\text{volume}}$ diagnoses budget-induced random deletion, and $\Delta F_{\text{attack}}$ measures whether an adversarial selector exceeds budget-matched random.

## Claim

For partition-aggregate methods (GraphEraser, GraphRevoker), the **k=5 noise floor** is **negative** — i.e., a partition-aggregate model's downstream F1 *increases* when an arbitrary tiny set of training nodes is removed. We name this signature *Shard Protection*. The same protective trend persists under budget-matched random deletion at $r=5\%$, while the attack-specific term $\Delta F_{\text{attack}}$ stays near zero across strategies; **adversarial selection cannot beat the same-budget random baseline** on shard methods within our budget regime.

## Content arc

1. **Diagnostic recap** (forward-link to §3.3): $\Delta F_{\text{noise}}$ is the k=5 intrinsic response; $\Delta F_{\text{volume}}(r)=\Delta F_{\text{rand}}(r)-\Delta F_{\text{noise}}$ is the budget-induced shift; $\Delta F_{\text{attack}}$ is the paired attack excess.
2. **Noise-floor plot** (1D bar chart, per method): $\Delta F_{\text{noise}}$ across the 6 methods. Most methods stay near zero; Partition family shows visibly *negative* bars — Shard Protection visible at a glance. Source: `results/baseline/k5_random/`.
3. **Fingerprint cross-reference** (§5.1): with Shard Protection isolated to $\Delta F_{\text{noise}}$, the partition pair sits near origin in the fingerprint $\Delta F_{\text{attack}}$ space — the "no above-baseline attack signal" geometric statement.
4. **Mechanism interpretation**: shard partitioning + aggregation acts as a deletion-induced regularizer. Small-budget deletion removes within-shard noise without crossing inter-shard information; the aggregator absorbs the perturbation.
5. **Intra-family robustness** (§A.2 ablation): the negative $\Delta F_{\text{noise}}$ persists across shard counts $\{5, 10, 20\}$ and aggregator variants — mechanism-driven, not hyperparameter artifact.
6. **Honest scope**: Shard Protection is a property of *running a partition-aggregate model on data − S for any reasonable S*, not a property our attack induces. Reporting it via the decomposition is what makes the honesty visible.
7. **Implications for adversarial budget**: an attacker on a partition-aggregate deployment cannot force performance drop at small $r$; the structural-attack failure mode is exactly the architectural protection. Dual-use note → §6.4.

## Evidence binding

- $\Delta F_{\text{noise}}$ data: `results/baseline/k5_random/{method}/{dataset}/{model}/baseline_seed*_k5.json` (k=5 noise floor)
- $\Delta F_{\text{rand}}(r)$ data: Phase B random-strategy cells `results/runs/{cell}/{method}_random/seed*/attack.json` (budget-matched random)
- $\Delta F_{\text{volume}}(r)$: derived as $\Delta F_{\text{rand}}(r)-\Delta F_{\text{noise}}$
- $\Delta F_{\text{attack}}$ data (paired-effect): `results/runs/{cell}/{method}_{strategy}/seed*/attack.json` minus same-seed random
- Shard ablation: §A.2 — `results/runs/cora_GCN_r0.05/{grapheraser,graphrevoker}_*/seed*/` with `_meta.json::num_shards` recorded
- Mechanism reference: GraphEraser paper (Chen et al. CCS 2022) on shard isolation; GraphRevoker paper (WWW 2024) on partial retraining

## Open questions

- **Q-5.3.1**: framing — "defensive discovery" vs "evaluation gap"? Now resolved by the diagnostic split: Shard Protection = $\Delta F_{\text{noise}} < 0$ is a measured property; whether a smarter selector could induce $\Delta F_{\text{attack}} > 0$ on shard methods is a separate question (current evidence: no, within our selectors).
- **Q-5.3.2**: explicit theoretical bound on $\Delta F_{\text{attack}}$ for shard methods? Empirically near zero; theoretical statement (e.g., "bounded by inter-shard mutual information") would lift contribution but risky in 3 days. Defer to discussion / future work.
- **Q-5.3.3** *(NEW)*: does the partition pair (GraphEraser vs GraphRevoker) show *similar* $\Delta F_{\text{noise}}$? Predicted yes — both are partition-aggregate. If divergent, the "Shard Protection is family-level" claim weakens to method-level; report honestly.

## Cross-refs

- ← §3.3 (formal definition of $\Delta F_{\text{noise}}$, $\Delta F_{\text{volume}}(r)$, and $\Delta F_{\text{attack}}$)
- ← §5.1 (Q3 / origin geometric position in fingerprint = "no above-baseline attack signal" reading)
- → §A.2 (shard-count robustness)
- → §6.2 (mechanism: partition-aggregate as deletion regularizer)
- → §6.4 (dual-use note: defensive insight on real deletion-API platforms)
