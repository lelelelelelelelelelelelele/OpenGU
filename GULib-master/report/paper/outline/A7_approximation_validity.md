# A.7 Approximation Validity of IM and Trajectory Influence Proxies

## Purpose

Test whether the proxy objectives used by two selector families retain the
signals they claim to represent:

- IM: whether coalition-level coverage collapses to a costly degree ranking;
- trajectory influence: whether a multi-checkpoint, evaluation-conditioned
  score remains aligned with an eval-IF reference.

This section complements A.6. A.6 defines the A/B--C--D influence taxonomy and
compares selector groups; A.7 tests whether representative proxy objectives are
valid within their intended semantic axes.

## Evidence boundary

### IM coverage proxy

- Retained source: `../../../self/related_work/concordance/data/summary.json`.
- Datasets: Cora, CiteSeer, PubMed, Photo, Computers, and CS.
- Metric: top-set Jaccard between IM and degree at the recorded 5% budget.
- Scope: one deterministic selector configuration per dataset; no GU outcome.

### Trajectory influence proxy

- Primary source: `../../../docs/tracin_v2_gates_ACCEPTANCE_REPORT.md`.
- Matrix: Cora/CiteSeer/PubMed x GCN/GAT x seeds 2024/7/42 (18 runs).
- Metric: full-ranking Spearman and common@7 against the eval-IF reference.
- Target: disjoint Planetoid validation loss; test labels are not used for
  selection.
- Scope: isolated selector prototype. Formal ScoreArtifact/cache integration,
  Hybrid composition, and an end-to-end GU canary remain pending.

## Table plan

### IM does not reduce to degree at the set level

| Dataset | Cora | CiteSeer | PubMed | Photo | Computers | CS | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| IM vs degree Jaccard | 0.187 | 0.177 | 0.061 | 0.046 | 0.030 | 0.032 | 0.089 |

The evidence supports an independent coalition-coverage signal. It does not
show that IM produces the largest downstream attack effect.

### Trajectory proxy alignment is strong but heterogeneous

| Configuration | V2 vs eval-IF Spearman | common@7 across seeds |
|---|---:|---:|
| Cora / GCN | 0.877 | `[5,6,5]` |
| CiteSeer / GCN | 0.950 | `[6,5,4]` |
| PubMed / GCN | 0.908 | `[5,3,5]` |
| Cora / GAT | 0.825 | `[6,7,5]` |
| CiteSeer / GAT | 0.962 | `[6,6,5]` |
| PubMed / GAT | 0.762 | `[4,4,1]` |

The configuration means span `0.762--0.962`. PubMed/GAT is the explicit
dataset-by-backbone boundary and prevents a universal proxy-equivalence claim.

## Writing constraints

- Say “IM does not degenerate to degree at the set level,” not “IM is better
  than degree.”
- Say “the isolated trajectory proxy is usually aligned with eval-IF,” not
  “production TracIn is accepted.”
- Keep the historical deployed cross-final selector separate. Its artifacts do
  not validate the paper-aligned trajectory score.
- Do not use selector overlap as a substitute for GU damage, retrain gap, or
  statistical significance.
- Refer to Cache V2, Hybrid, and GU-canary work only as the production boundary.

## Status

Drafted from retained evidence. IM set-level validity is accepted for the
reported six-dataset configuration. Trajectory influence has a conditional
prototype pass; production/main-runner claims remain pending.
