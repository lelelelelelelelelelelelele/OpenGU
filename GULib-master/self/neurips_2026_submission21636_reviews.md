---
title: NeurIPS 2026 Submission 21636 Reviews
type: paper-review-note
status: review-synthesis
submission: https://openreview.net/forum?id=TjLY6k0uxK#discussion
date: 2026-07-24
---

# NeurIPS 2026 Submission 21636 - Review synthesis

> [!note]
> This note records review evidence and actionable revision directions. It does not treat review scores as a measure of research value. All three reviewers recognized either the problem motivation or the core empirical observation. The main risks are evidence consistency, threat-model boundaries, claim strength, and manuscript readability.

## 1. Review snapshot

| Reviewer | Quality | Clarity | Significance | Originality | Rating | Confidence | Core judgment |
|---|---:|---:|---:|---:|---:|---:|---|
| WnUp | 1 | 2 | 1 | 2 | 1 - Strong Reject | 4 | Motivation and metrics have value, but presentation, metric choice, coverage, and Table 2 credibility are serious concerns. |
| 3ZdK | 1 | 1 | 3 | 2 | 2 - Reject | 4 | The empirical observation is valuable and technically plausible, but numbers, threat model, and theory claims need correction. |
| YRQd | 2 | 2 | 2 | 2 | 3 - Borderline Reject | 5 | The question is worthwhile, but node-only scope, generic heuristics, and strong Shard Protection claims limit the contribution. |

## 2. Reviewer WnUp

### Recognized strengths

- The GDPR/right-to-forget deletion-set threat model is motivated and practically plausible.
- The `noise` and `volume` metrics separate selector effects from deletion-size effects.
- The paper provides broad tables/plots and attempts statistical significance tests.

### Main concerns

- **Presentation and clarity:** Concepts are introduced too quickly, and the manuscript contains development residue such as dispatcher fixes, selector seed fixes, legacy fields, and result paths.
- **Retrain Gap:** The chosen F1-difference metric is not aligned with common unlearning literature. The reviewer suggests considering KL divergence between a gold model and the unlearned model because F1 differences can hide predictive-distribution changes.
- **Incomplete coverage:** The paper claims Cora, Citeseer, and ogbn-arxiv evaluation, but the visible paper and appendix mainly show Cora.
- **Table 2 credibility:** Some random-attack rows appear to improve F1 by as much as 19.3 percent. Check metric direction, difference definitions, and the experiment pipeline.
- **Verdict labels:** A reproducible rubric is missing; qualitative labels should be tied to explicit thresholds or statistical criteria.

### Requested extensions/questions

- Report mean and standard deviation for all metrics.
- Consider RL/MDP for combinatorial delete-set selection.
- Add Citeseer/ogbn-arxiv and more realistic networks.
- Explain why implementation details remained in the final paper.
- Consider edge deletion.

### Interpretation

RL, edge deletion, and realistic large networks are extension directions. The urgent items are Table 2, metric semantics, missing results, and manuscript residue.

## 3. Reviewer 3ZdK

### Recognized strengths

- The paper identifies a useful observation: robustness to random deletion does not imply robustness to strategic deletion.
- The decomposition into random effect, attack-specific excess degradation, retrain gap, prediction shift, hop-distance decay, and update-detection AUC is informative.
- `Significance = 3`; the rating definition explicitly describes the paper as technically solid enough that the rejection reasons are mainly evaluation and presentation limitations.

### Main concerns

- **Readability:** The style is mechanistic, several introductions/headings/captions are hard to read, and development-stage sentences remain in the manuscript.
- **Unsupported theory claim:** `L2-SURROGATE is bounded above by L2-DIRECT(TraceIn)` needs a formal proof. Otherwise delete or downgrade it to an empirical/design assumption.
- **Threat model:** Ordinary users usually cannot select arbitrary high-impact nodes. L1 assumes public graph/training mask access; L2-DIRECT assumes production weights/gradients/checkpoints. These should be presented as explicit access tiers, not as default deletion-API permissions.
- **Inconsistent interpretation:** The results describe GIF as more degree-aligned, while the conclusion calls it TracIn-aligned.
- **Numerical inconsistencies:** GraphRevoker values do not match across Table 2, Table 3, Figure 5, and Appendix Tables 5/6, including examples such as `+0.7` versus `-0.04` and `+1.0` versus `+0.19 +/- 0.89`.
- **External validity:** The motivation includes recommendation, fraud detection, citation analysis, and KG retrieval, but the experiments are mostly transductive citation-style node classification.

### Interpretation

This is the clearest acknowledgment that the study has value and is technically plausible. However, numerical inconsistency directly damages reproducibility and credibility; treat it as P0.

## 4. Reviewer YRQd

### Recognized strengths

- The adversarial-versus-random deletion question is meaningful.
- The access levels and comparison across six selectors and three GU families are recognized.

### Main concerns

- **Narrow scope:** Only node deletion is studied; edge addition, edge deletion, and rewiring are absent.
- **Insufficient adaptive-attack evidence:** The selectors are mostly generic heuristics, and Degree is often stronger than model-aware TracIn/Hybrid. This does not yet show that selectors exploit each method's approximation error.
- **Overstated Shard Protection claim:** Two partition methods, limited datasets/backbones, and non-adaptive selectors do not support architectural immunity or universal Shard Protection.

### Interpretation

The rating is `3 - Borderline Reject` with confidence 5. The reviewer is not saying the core experiment is invalid; the evidence is insufficient for the current contribution wording. Reframe immunity/protection as a conditional pattern observed under the evaluated matrix and selector family.

## 5. Cross-review synthesis

### Commonly recognized value

1. Deletion requests are not necessarily benign; strategic deletion differs from random deletion.
2. Final F1 alone is insufficient; the metric decomposition is useful.
3. The main problem is not that the research question has no value. The evidence chain and manuscript wording do not yet reach the acceptance bar.

### Shared risks and priorities

1. **P0 - Numbers and provenance:** Audit Table 2/3, Figure 5, and Appendix Tables 5/6. Check random-after-F1 increases, signs, units, aggregation, and same-seed pairing.
2. **P0 - Claim calibration:** Remove or narrow universal language such as `architectural immunity` and `Shard Protection`. Use conditional empirical pattern language with explicit method/backbone/dataset/selector scope.
3. **P1 - Threat model:** Define L0/L1/L2 knowledge and permissions explicitly. Separate a realistic deletion API from upper-bound research access.
4. **P1 - Manuscript cleanup:** Remove dispatcher/seed/legacy-field/path/cache details. Rewrite terminology, introduction, captions, and the verdict rubric.
5. **P1 - Metric defense:** Add the Retrain Gap equation and explain the relation between F1 difference and predictive-distribution metrics. Consider adding KL; if not, justify the current metric.
6. **P1 - Coverage honesty:** Add Citeseer/ogbn-arxiv or explicitly downgrade them to incomplete/feasibility evidence. Do not claim coverage without showing results.
7. **P2 - Selector interpretation:** Explain why Degree is strong. Distinguish structural-importance proxies from method-adaptive approximation-error attacks.
8. **P2 - Future work:** Edge/rewiring, RL/MDP, and realistic deletion-API settings can remain limitations/future work. Do not turn every reviewer suggestion into a new main line.

## 6. Recommended next action

Do not rewrite the whole paper first, and do not start with RL or edge attacks.

1. Build a **paper-number audit ledger** mapping every paper number to aggregate input, seed, method, dataset, backbone, selector, metric definition, and generator script.
2. Audit GraphRevoker and the Table 2/3/Figure 5/Appendix mismatches. Mark any untraceable number as `do_not_claim`.
3. Rewrite the contribution/claim language from `architectural immunity / adaptive attack` to `conditional vulnerability patterns / systematic adversarial audit` where the evidence requires it.
4. Clean manuscript residue, then decide which experiments are worth the remaining effort.

## 7. Psychological reading note

The combined conclusion is not that the paper has no value. A more accurate statement is:

> The core empirical observation is valuable and the study is not technically hopeless. The submitted version did not give reviewers enough confidence in its numerical consistency, threat model, claim strength, and presentation quality.

The immediate goal is not to prove that the paper deserved acceptance. It is to turn it into an audit that a reviewer can trust, reproduce, and cite accurately.

## 8. Handoff prompt

Use this prompt when continuing the work:

```text
Continue work on `self/neurips_2026_submission21636_reviews.md` in the OpenGU project.

Context: NeurIPS 2026 Submission 21636 received ratings 1/2/3. All three reviewers recognized the value of the adversarial deletion audit or its empirical observation. The main risks are:
1) numerical inconsistencies across Table 2/3, Figure 5, and Appendix Tables 5/6;
2) over-strong claims about Shard Protection, architectural immunity, and adaptive attacks;
3) unclear L0/L1/L2 threat-model permissions;
4) the relation between Retrain Gap and KL/predictive-distribution metrics;
5) incomplete Citeseer/ogbn-arxiv coverage and manuscript development residue.

Do not begin with RL, edge rewiring, or large new experiments. First read the current paper, `self/dashboard/WORKPLAN.md`, the metric-semantics documents, and the final aggregate inputs. Build a paper-number audit ledger. Prioritize the GraphRevoker and Table 2/3/Figure 5/Appendix discrepancies, including source, sign, unit, seed pairing, metric definition, and generator script.

Output:
- a P0/P1/P2 issue table;
- an evidence path for each disputed number;
- claims that can stay, must be narrowed, or must be removed;
- the smallest defensible revision plan.

Lead with the conclusion. Do not interpret review scores as a judgment of research value.
```
