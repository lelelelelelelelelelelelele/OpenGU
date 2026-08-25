# A.7 Approximation Validity of Modern IM and Trajectory Influence Proxies

## Purpose

Test whether two selector families retain the signals they claim to represent
under budgets that can be transferred to graph unlearning:

- modern IM: whether a method is computationally usable, what form of score or
  certificate it returns, and whether its selected set improves independent IC
  spread over degree;
- trajectory influence: whether an evaluation-conditioned multi-checkpoint
  score remains aligned with its reference and produces a stronger
  target-direct GU outcome than degree.

This section complements A.6. A.6 defines the A/B--C--D influence taxonomy and
compares selector groups. A.7 evaluates approximation validity, runtime, score
semantics, and the boundary between selector fidelity and downstream GU damage.

## Evidence already retained

### Historical IM coverage observation

- Source: `../../../self/related_work/concordance/data/summary.json`.
- Datasets: Cora, CiteSeer, PubMed, Photo, Computers, and CS.
- Metric: top-set Jaccard between the deployed IM selector and degree at the
  recorded 5% candidate budget.
- Scope: one deterministic selector configuration per dataset; no independent
  spread evaluation and no GU outcome.

| Dataset | Cora | CiteSeer | PubMed | Photo | Computers | CS | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| IM vs degree Jaccard | 0.187 | 0.177 | 0.061 | 0.046 | 0.030 | 0.032 | 0.089 |

This retained evidence only shows that the deployed IM set differs from degree.
It does not show that IM is better than degree. The new experiment below must
test that claim using independent spread and, conditionally, GU retrain gap.

### Historical trajectory diagnostic

- Source: `../../../docs/tracin_v2_gates_ACCEPTANCE_REPORT.md`.
- Matrix: Cora/CiteSeer/PubMed x GCN/GAT x seeds 2024/7/42.
- Primary retained metric: full-ranking Spearman against the eval-IF reference.
- Scope: isolated selector prototype; not a target-direct GU result.

| Configuration | V2 vs eval-IF Spearman |
|---|---:|
| Cora / GCN | 0.877 |
| CiteSeer / GCN | 0.950 |
| PubMed / GCN | 0.908 |
| Cora / GAT | 0.825 |
| CiteSeer / GAT | 0.962 |
| PubMed / GAT | 0.762 |

The configuration means span `0.762--0.962`; PubMed/GAT remains the explicit
boundary against a universal proxy-equivalence claim. Historical fixed-$k$
overlap fields remain traceable in the source report, but they are not a budget
for the new A.7 experiment.

## New A.7 experiment contract

The detailed modern-IM matrix and approval gates are maintained in
[`22_IM成熟算法可用性与Degree超越实验计划.md`](../../../../../OpenGU-DocMap/10_实验矩阵/22_IM成熟算法可用性与Degree超越实验计划.md).

### A.7a Modern IM selector validity

| Axis | Pre-registered value |
|---|---|
| Datasets | Cora, CiteSeer, PubMed |
| Data profile | canonical OpenGU transductive 80/0/20 processed split |
| Candidate ground set | complete persisted train candidates |
| Ratios | 1% and 5% of candidate count |
| Selector seeds | 42, 212, 2024 |
| Primary methods | degree, random, corrected IMM, OPIM-C, RR-SNI, RR-Shapley, RR-$k$-semivalue |
| Candidate pruning | none |
| Primary evaluator | selector-independent common-random RR/live-edge samples |

This is a `3 datasets x 3 seeds x 2 ratios x 7 methods = 126` row
selection matrix.

Expected counts from the current canonical split contract are:

| Dataset | Expected train candidates | $k$ at 1% | $k$ at 5% |
|---|---:|---:|---:|
| Cora | 2,166 | 21 | 108 |
| CiteSeer | 2,661 | 26 | 133 |
| PubMed | 15,773 | 157 | 788 |

The formal manifest, rather than this table, is the final authority for
candidate counts and $k$. It must record the resolved canonical path, split and
candidate fingerprints, exact ratio, rounding rule, and full Git provenance.

The experiment reports four separate outputs:

1. cold/warm time, peak RSS, RR count, and RR incidence scale;
2. guarantee status: paper-equivalent guarantee, conservative certificate,
   empirical confidence interval, or no guarantee;
3. score form: full static score, budget-conditioned full score, dynamic
   residual trace, or selection only;
4. degree comparison: independent spread difference/ratio with paired 95% CI,
   plus Jaccard and rank correlation only as interpretation metrics.

No method is promoted because it merely has low overlap with degree. Promotion
requires an independent spread ratio of at least `1.02`, a positive paired 95%
CI lower bound on at least two of the three small datasets, no loss larger than
1% on the remaining dataset, and passage of the registered time/RSS gate.

### A.7a Large-graph runtime and quality gate

Only methods that pass the small-graph gate proceed to the canonical
ogbn-arxiv processed graph. The registered matrix uses the complete persisted
train candidates, ratios 1% and 5%, seeds 42/212/2024, and six methods:
degree, corrected IMM, OPIM-C, RR-SNI, RR-Shapley, and
RR-$k$-semivalue. This is `3 seeds x 2 ratios x 6 methods = 36` rows.

The first canary is seed 42 at 1%. A method stops expansion if its cold runtime
exceeds 600 seconds, peak RSS exceeds 16 GiB, or its RR incidence structure
exceeds the registered resource limit. Candidate pruning is not an allowed
fallback. Promotion requires beating degree at both ratios with positive paired
confidence bounds while satisfying the time and memory gates.

### A.7b Target-direct trajectory validity

The
[target-direct preparation audit](../../../reports/target_direct_selection_PREPARATION_REPORT.md)
shows that the previous 153-cell matrix cannot be used as A.7 evidence: its
directory/configuration said 5%, while its external Selection Artifact fixed
every cell to $k=7$, and the selector and GU target did not share the same
checkpoint state.

The corrected first-round contract is:

- source: canonical checkout-local Planetoid data;
- split: fixed 70/10/20 so the selection target is a validation-mask objective
  disjoint from both train candidates and final test evaluation;
- budget: 5% of train candidates, with one fail-closed `expected_k` shared by
  selection and GU;
- identity: the ScoreBundle, Selection Artifact, and GNNDelete target all bind
  the same checkpoint file hash and state hash;
- comparisons: degree and random, reported per dataset and seed;
- outcomes: target F1 drop, absolute retrain gap, collateral effect,
  update-detection AUC, runtime, memory, and failure status.

This trajectory lane starts at 5% because it is a GPU GU matrix. A 1% extension
is a separate ratio-sensitivity decision after the 5% gate; it must not be
silently mixed into the first result identity.

### Conditional GU test for modern IM

Only a modern-IM method that passes A.7a may enter a GU canary. The first canary
uses Cora/CiteSeer, GCN, GIF/GNNDelete, seeds 42/212/2024, and a 5% canonical
train-candidate budget. Degree remains the primary comparator and random the
negative control. A second IM winner or a 1% GU ratio requires a new approval.

## Historical boundary

The public Planetoid selector studies remain recoverable as mechanism
diagnostics. Their small fixed budgets are not part of the new A.7 matrix and
are not used to justify a GU claim.

## Writing constraints

- Say “historical IM differs from degree at the set level,” until the new
  independent-spread comparison is available.
- Say “a modern IM method exceeds degree” only if the pre-registered paired
  spread gate passes; use GU retrain gap for the downstream attack claim.
- Keep full static scores, budget-conditioned scores, dynamic residual traces,
  and set-level approximation guarantees as separate output types.
- Say “the historical trajectory prototype is aligned with eval-IF,” not
  “production TracIn is accepted.”
- Do not use selector overlap as a substitute for spread, GU damage, retrain
  gap, or statistical significance.
- Keep the invalid fixed-$k=7$ target-direct matrix out of all new A.7 result
  tables.

## Status

The historical IM set-overlap observation and trajectory ranking diagnostic
remain retained with limited scope. The new canonical 1%/5% modern-IM matrix
and corrected 5% target-direct trajectory matrix are pre-registered but have
not been run. Formal execution remains subject to a separate experiment
approval.
