---
title: Paper resubmission blueprint — structural leverage and objective misalignment
status: dormant-until-resubmission
last_updated: 2026-07-22
source_archive: archive/paper-alignment-20260507
wip_archive: archive/paper-alignment-wip-20260507
---

# Paper resubmission blueprint

> [!important] Activation gate
> This is a dormant resubmission blueprint, not the current rebuttal narrative. The submitted thesis remains *systematic audit + extreme heterogeneity + Vulnerability Fingerprint*. Activate this document only after a reject/resubmit decision or an explicit thesis-change decision.

This document extracts the durable ideas from the retired `paper/alignment-experiment` branch. It replaces the branch as the human-readable recovery entry point. The exact historical files remain recoverable through immutable archive tags, but their old numbers and figures are not paper-ready evidence.

## 1. Durable sources

| Entry | What it preserves | Use rule |
|---|---|---|
| Blueprint archive tag | Abstract/intro pivot and early FIG-5 | Narrative provenance only; do not cherry-pick |
| WIP archive tag | Later results text, early fingerprint and Jaccard paragraph | Recover questions only; recompute values |
| [Alignment audit](../../reports/paper_alignment_branch_AUDIT_REPORT.md) | Blob, PDF, generator and data-provenance evidence | Ledger for keep/supersede decisions |

Verified exact targets:

- `archive/paper-alignment-20260507` → `565aaf64ea480b3df880e1d9b460211a328f98ad`
- `archive/paper-alignment-wip-20260507` → `eb9595cb76456aebd232e04ef5abdfb88a480c52`
- Alignment audit baseline → `main@b94130339e1a2490957fcc3c5373fb491422dc84`

These tags are local repository refs until explicitly backed up or pushed. Do not delete the tags during ordinary branch cleanup.

## 2. Extracted story spine

### Central question

Does attacker access level predict the damage caused by adversarial deletion requests against approximate graph unlearning?

### Durable answer

The observed ordering is not monotonic in access. Low-access structural selectors can outperform model-coupled gradient selectors. The honest mechanism hypothesis is **objective misalignment**: TracIn optimizes influence on predictive loss and IM optimizes propagation spread, while the attack target is error in the approximate unlearning operator. Degree/PageRank may align with that target through structural leverage without requiring model access.

This is a hypothesis supported by the audit pattern, not a license to claim that degree universally wins or that access is causally irrelevant. Claims must be scoped to the final accepted matrix.

### Reusable introduction structure

1. Approximate GU assumes deletion requests are benign; a deletion API makes the deletion set an attack surface.
2. The conventional hierarchy expects greater model access to yield stronger attacks.
3. The audit tests that hierarchy with a calibrated access spectrum and same-seed random controls.
4. The empirical inversion motivates the objective-misalignment hypothesis.
5. The contribution is a systematic adversarial audit and diagnostic framework, not a claim that the proposed informed selectors are always strongest.

### Reusable contribution scaffold

- **Calibrated threat model:** L0, L1 structural, L2-direct and L2-surrogate access with explicit cost assumptions.
- **Empirical audit:** method × selector × backbone × seed comparisons using paired effects against budget-matched random deletion.
- **Diagnostic kit:** architectural/attack decomposition, retrain gap, prediction shift, hop-distance decay, update-detection AUC and selection-overlap analysis.
- **Mechanism hypothesis:** test whether structural leverage and selector/objective alignment explain heterogeneous vulnerability.

## 3. Material that must not be copied forward

- The old `6/12` versus `1/12` significance headline.
- The GraphRevoker×GAT negative-correlation or TracIn-breakthrough wedge.
- Claims of universal partition immunity, “Shard Protection,” or universal structural dominance.
- Old retrain-gap, method-ranking, arXiv coverage and Citeseer scope numbers.
- Either archived FIG-3, or either old FIG-5, as final evidence.
- The old Jaccard/effect correlation `r=0.18, p=.004`; retain the question, then recompute.

Every number must come from the final accepted evidence set after the current experiment gates close.

## 4. FIG-5 and overlap-analysis specification

The useful artifact is the design and analysis contract, not the old PDF bytes.

- Left panel: non-random tuple scatter of a declared structural-alignment measure versus same-seed paired effect; show Pearson, Spearman and sample size.
- Right panel: strategy-level mean paired effect in a fixed, documented order; random is the reference and should not appear as a competing non-random bar.
- Companion text: mean Jaccard overlap of PageRank, IM, Hybrid and TracIn selections with Degree, recomputed from versioned selection artifacts.
- Required inputs: final aggregate CSV, graph/pickle identity, all selection-artifact identities, included/excluded method gate, and script commit.
- Required checks: schema/unit assertions, expected tuple counts, input hashes, PDF text inspection, visual inspection and clean LaTeX compilation.
- Tracking rule: generate to a temporary path first; only the reviewed final `FIG-5_Alignment.pdf` is force-added at its exact repository path.

The archived 39,699-byte FIG-5 and the ignored 68,286-byte FIG-5 are visual/history references only.

## 5. Activation checklist

The operational source of truth is [`self/dashboard/WORKPLAN.md`](../../self/dashboard/WORKPLAN.md). The relevant gates are:

1. **E4:** import and validate the accepted post-fix GraphRevoker evidence locally; decide inclusion rather than silently mixing invalid rows.
2. **F2:** converge on `scripts/plot_neurips_figures.py` as the sole generator; fix schema, units, repository root and fail-fast contracts.
3. **F5:** recompute alignment/Jaccard statistics from the final accepted matrix, regenerate FIG-5, visually inspect it, compile the paper and track the final PDF.
4. **W10:** only after the resubmission gate opens, manually rewrite abstract/intro from current main using this blueprint and refill validated numbers.

## 6. Rewrite protocol

Start from the then-current paper, not from the archive commit. Draft claims as placeholders tied to evidence IDs, run the full paper-liability audit, and only then fill numbers. Compare against the archived text for lost ideas, but never cherry-pick the old paper commit: its results prose, figures and scientific scope are superseded.
