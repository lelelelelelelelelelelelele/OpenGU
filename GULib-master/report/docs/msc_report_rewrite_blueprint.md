# MSc Report Rewrite Blueprint

## Purpose

This document is the working blueprint for rewriting the main Markdown report into a stronger MSc course report.

It is intended to do three things:

- make the report read like a finished course submission rather than a progress summary
- add the missing explanatory depth in `Introduction`, `Methodology`, and `Metrics`
- preserve a structure that can later be migrated to LaTeX without major reorganization

This blueprint does not convert the report into a paper draft. It strengthens the course-report version while keeping the work reusable for later extension.

## Audience and Writing Target

The target reader is a course examiner or academic reader who may not already know the graph unlearning subfield in detail.

The report therefore needs to do two things at the same time:

- document the completed project clearly and honestly
- explain the technical context well enough that the results and claims can be followed without relying on unstated field knowledge

The writing target is:

- more technical than the current summary-style draft
- less compressed than a paper abstract or short workshop submission
- still clearly a report, not a thesis chapter and not a publication manuscript

## Title Handling

The approved project title must remain on the cover page.

The working rule for the report is:

- formal title: use the approved course title
- subtitle: use the concrete project focus, such as adversarial deletion attacks on approximate graph unlearning
- body text: focus directly on the actual study rather than repeatedly explaining why the title is broader than the reported case study

This is a fixed external constraint, not a defect in the report.

## Narrative Strategy

The main narrative should be:

1. Graph neural networks are used on structured relational data, and data removal requests create a practical machine-unlearning problem.
2. Approximate graph unlearning methods are efficient but may introduce approximation error.
3. If deletion requests are strategically chosen, that approximation error may become an attack surface.
4. This project builds an evaluation framework to test that possibility across several graph unlearning families.
5. The experiments reveal a vulnerability spectrum, with substantially different behavior across learning-based, influence-based, and shard-based methods.

This narrative keeps the report centered on the completed project while naturally motivating later extension.

## Chapter Blueprint

### 1. Introduction

The current draft is too compressed. The rewritten chapter should expand into four linked tasks:

#### 1.1 GNN Context

Explain what graph-structured data is and why GNNs are used for it.

Include:

- nodes, edges, and features as the basic representation
- common graph tasks such as node classification, link prediction, and graph classification
- why message passing makes GNNs sensitive to local and global graph structure

This section should help a reader who knows machine learning but not necessarily graph learning.

#### 1.2 Why Graph Unlearning Matters

Define machine unlearning and then narrow to graph unlearning.

Explain:

- why retraining from scratch is expensive
- why deletion requests arise in privacy-sensitive or regulation-sensitive settings
- why graph data creates additional difficulty because one node can influence many others through connectivity and propagation

#### 1.3 Why Approximate Unlearning Creates Risk

This section should connect efficiency to vulnerability.

Explain:

- exact retraining as the conceptual ideal
- approximate unlearning as the practical shortcut
- approximation error as the key risk
- why a malicious user could treat the deletion interface itself as an attack surface

End with a clear motivating question:

Can strategically selected deletion requests amplify approximation error enough to damage the retained model beyond the intrinsic effect of removing the requested data?

#### 1.4 Report Purpose

State clearly that the document is an MSc course report focused on one concrete case study under the broader approved project title.

Keep this short. Do not over-explain the title constraint.

### 2. Background and Literature Context

This chapter should remain selective rather than turning into a survey.

It should do three jobs:

- define the main graph unlearning families
- explain what each family trades off
- position the present work as an evaluation and auditing framework rather than as a new unlearning algorithm

Suggested structure:

- partition- or retraining-based methods
- influence-function-based methods
- learning-based compensation methods
- prior evaluation axes: efficiency, fidelity, privacy
- current gap: robustness under adversarial deletion selection

Each family description should include both mechanism intuition and likely vulnerability intuition.

### 3. Project Objectives and Scope

This chapter can remain concise, but it should distinguish:

- project objectives
- completed scope
- explicitly deferred scope

Keep the current factual coverage but write it as stable report content, not as a mid-project checkpoint.

### 4. Methodology and Experimental Setup

This is the chapter that most needs to be thickened.

#### 4.1 Threat Model

Do not keep this as a short paragraph only. Spell out:

- attacker goal
- attacker control over deletion requests
- attacker knowledge assumptions
- budget assumption
- evaluation target: retained-data degradation after unlearning

If useful, distinguish attacker capability from strategy requirement. For example:

- TracIn and Hybrid need model-aware information
- IM, Degree, and PageRank are more structural

#### 4.2 Attack Pipeline

Retain the four-step pipeline but explain each step's purpose:

- pre-unlearning training gives the reference model
- selection strategy determines which nodes to request for deletion
- approximate unlearning processes the request
- retrain controls and retained-set metrics separate true deletion effect from approximation damage

Mention the reusable pipeline components, but keep the code paths secondary to the method explanation.

#### 4.3 Node-Selection Strategies

The current table is too thin by itself. Add a short paragraph for each group:

- `Random`: reference baseline
- `Degree` and `PageRank`: structural centrality heuristics
- `TracIn`: gradient-based influence proxy
- `IM-v4`: influence maximization through batched CELF-style search
- `Hybrid-v4`: fusion of graph-structural and trajectory-based signals

For each one, explain:

- what information it uses
- why it might identify influential deletion targets
- whether it is cheap, expensive, white-box-like, or graph-structural

#### 4.4 Evaluation Metrics

This subsection should become a genuine metrics framework.

Minimum required metrics and descriptions:

- `f1_drop = F1_before - F1_after`
- `relative_f1_drop = F1_random_unlearn - F1_attack_unlearn`
- `retrain_gap = F1_retrain - F1_unlearn`
- `drop_retrain = F1_before - F1_retrain`
- `fraction_flipped`: fraction of retained nodes whose predicted label changes
- `mean_pred_shift`: average shift in retained-node prediction probabilities

The section should explain the attribution logic explicitly:

`total_drop = drop_retrain + retrain_gap`

Interpretation rule:

- `drop_retrain` captures the utility cost of deleting the data itself
- `retrain_gap` captures the extra approximation error introduced by the unlearning method

This should be presented as one of the report's key analytical contributions.

#### 4.5 Experimental Matrix

Keep the phase table, but preface it with one paragraph explaining why the experiments are organized across:

- datasets
- backbones
- seeds
- deletion budgets
- strategy families

That paragraph should tell the reader what the matrix is trying to validate rather than only listing where experiments were run.

### 5. Implementation and Experimental Work

This chapter should stay in the report, but its tone needs control.

It should explain:

- what infrastructure had to be built
- what reproducibility and aggregation work was necessary
- what debugging and cleanup were important for trustworthy results

It should not read like a daily log.

Practical rule:

- emphasize why the pipeline matters for the validity of the study
- de-emphasize routine execution details unless they affected interpretation or trustworthiness

### 6. Results and Analysis

Each subsection should follow the same writing pattern:

1. what question this result addresses
2. what the main empirical pattern is
3. what that pattern implies about mechanism, robustness, or boundary conditions

Suggested subsection logic:

#### 6.1 Cross-Family Vulnerability Spectrum

Question:

Do different graph unlearning families respond differently to adversarial deletion?

Interpretation target:

- learning-based methods are most fragile
- influence-based methods are comparatively stable
- shard-based methods behave qualitatively differently

#### 6.2 GNNDelete as the Fragile Extreme

Question:

How severe can the failure become, and under what budget?

Interpretation target:

- low-budget deletions can already trigger substantial collapse
- retrain control shows the damage is driven mainly by approximation error

#### 6.3 Collateral Damage and Attribution

Question:

Is the damage confined to the deleted data, or does it spill over to the retained set?

Interpretation target:

- retrain gap and retained-node disturbance are essential stability diagnostics
- GNNDelete's success is coupled with large collateral damage

#### 6.4 Shard Protection Effect

Question:

Why does GraphEraser improve under deletion in the tested settings?

Interpretation target:

- present the shard-purification interpretation carefully as a plausible explanation, not an over-claimed universal law

#### 6.5 Strategy Comparison and Efficiency

Question:

Which attack strategies provide meaningful advantage, and are they practical to run?

Interpretation target:

- distinguish attack-over-random support from absolute effect size
- show IM-v4 as the main engineering result for practical selection

### 7. Limitations

This chapter should remain candid and specific.

It should describe limits in:

- dataset coverage
- privacy-audit completeness
- mechanism ablation completeness
- remaining data quality checks
- domain generality

The goal is not to weaken the report, but to bound the claims responsibly.

### 8. Future Applications and Next Steps

This chapter should stay concrete rather than aspirational.

Good next steps:

- larger datasets
- privacy audit completion
- GNNDelete mechanism ablations
- broader domain validation

Avoid promising a paper or publication outcome as if it were guaranteed.

### 9. Conclusion

The conclusion should restate:

- the problem studied
- the main cross-family finding
- the methodological contribution of the evaluation framework
- the fact that the project now provides a stable basis for future continuation

## Main Deficiencies in the Current Draft

The current Markdown draft is usable, but several weaknesses should be fixed during rewriting.

### Tone Problems

- repeated progress-report wording such as `completed project work`, `current submission point`, and `present report version`
- several sentences that sound like internal project bookkeeping rather than report prose

### Introduction Problems

- GNNs are mentioned without enough setup for a non-specialist reader
- graph unlearning is introduced too quickly
- approximate unlearning is named before its risk is fully motivated
- the attack-surface logic is present but under-explained

### Methodology Problems

- the threat model is too short
- strategy descriptions are mostly names plus one line
- metrics are listed but not fully defined
- the attribution logic is important but currently under-emphasized

### Analysis Problems

- some results are reported before the reader has enough metric intuition
- some sections tell what happened without spending enough space on why it matters
- implementation and analysis occasionally blend together in a way that weakens the scientific narrative

## Working Rewrite Rules

When rewriting the main report later, apply these rules consistently:

- prefer report voice over progress voice
- define concepts before using them heavily
- explain each metric before using it in interpretation
- do not assume the reader already knows GU-specific terminology
- keep paper-oriented ambitions secondary to the course-report purpose
- retain cautious interpretation language where the mechanism explanation is plausible but not fully proven

## LaTeX Migration Mapping

The later LaTeX migration should be structural before stylistic.

Recommended mapping:

- Markdown level-1 sections -> `\section{}`
- Markdown level-2 subsections -> `\subsection{}`
- metric formulas -> displayed equations or compact inline equations where appropriate
- strategy and phase summaries -> tables
- result figures -> figure environments with captions that answer a concrete question

Migration rules:

- preserve the report-style section order first
- move headings and text before reformatting tables
- migrate the strengthened Markdown version before doing any paper-style reorganization
- keep the approved title and use the subtitle to identify the concrete study

## Immediate Next Step After This Blueprint

Once this blueprint is accepted, the next content step should be to rewrite the main Markdown report chapter by chapter using this document as the governing guide, starting with:

1. `Introduction`
2. `Methodology and Experimental Setup`
3. `Results and Analysis`

These three chapters will deliver the biggest quality gain for the least structural disruption.
