# EE5003 Final Presentation Speech Script

- Audience: EE5003 course assessment / supervisor-style academic review
- Language: English PPT + English script
- Main timed deck: 14 slides
- Estimated total speaking time: 14:55

## Slide 1: Title

Goal: Open the talk, name the problem, and state the thesis.

Estimated Time: 0:35

Key Lines:
- This project audits approximate graph unlearning under adversarial deletion requests.
- The question is whether a malicious requester can choose deletions that amplify approximation error.
- The answer depends strongly on the unlearning family.

Speaker Notes:
Good afternoon. I am Liu Chengyu, and this presentation summarizes my EE5003 MSc project on adversarial deletion attacks against approximate graph unlearning. The core question is whether a deletion interface can be exploited by choosing nodes whose removal causes much more damage than a normal request should. I study this problem across several graph unlearning families, build an evaluation workflow on top of OpenGU, and show that these methods do not inherit safety behavior equally.

## Slide 2: Why Graph Unlearning Matters

Goal: Explain why this problem is practically important.

Estimated Time: 1:00

Key Lines:
- Graph models are used in settings where deletion requests are realistic.
- Approximate unlearning is attractive because exact retraining is expensive.
- That same approximation creates a security surface.

Speaker Notes:
Graph unlearning matters because graph neural networks are used in citation, recommendation, and social systems where node-level removal is a realistic requirement. In practice, exact retraining after every deletion request is often too expensive, so approximate unlearning methods are attractive. But approximation also creates risk. If the retained model only approximates the effect of deletion, then a malicious requester may exploit the deletion interface itself by choosing nodes that maximize retained-model damage. So the deletion API is not only a compliance mechanism; it can also become an attack interface.

## Slide 3: Research Question And Objectives

Goal: Define the research question and the four project objectives.

Estimated Time: 1:00

Key Lines:
- Can malicious deletion requests degrade utility beyond ordinary deletion at the same budget?
- Compare method families, not just one algorithm.
- Add attribution metrics and practicality analysis.

Speaker Notes:
The main research question is whether malicious deletion requests can amplify approximation error and degrade retained-model utility beyond what ordinary deletion would cause at the same budget. I organized the project around four objectives. First, build an attack pipeline with multiple deletion strategies. Second, compare vulnerability across different graph unlearning families. Third, introduce attribution metrics that separate true deletion impact from approximation-induced spillover. And fourth, test whether adversarial node selection is efficient enough to be practically relevant rather than only conceptually possible.

## Slide 4: Method Families And Threat Model

Goal: Clarify the method families and the attacker capability.

Estimated Time: 1:15

Key Lines:
- The study covers learning-based, IF-based, and shard-based unlearning.
- These families differ in mechanism, so family-level robustness may differ too.
- The attacker controls only the deletion request.

Speaker Notes:
The evaluation spans several unlearning families. Learning-based unlearning is represented by GNNDelete, which learns a direct unlearning correction. Influence-function-based unlearning is represented by GIF, which approximates deletion through local influence-style updates. The broader benchmark also includes IDEA, MEGU, and the shard-based GraphEraser, which partitions the graph and retrains affected shards. I make this distinction early because the mechanisms are genuinely different, so it would be surprising if they all inherited the same robustness behavior. The threat model is deliberately practical. The attacker can choose which nodes to delete through the normal interface, but does not modify labels, features, optimizer settings, or hidden training code. This is not a poisoning attack. I also track collateral damage on retained nodes.

## Slide 5: Attack Pipeline And Experimental Matrix

Goal: Explain the workflow and experimental scope.

Estimated Time: 1:15

Key Lines:
- The pipeline is select nodes, unlearn, exact retrain, and compare.
- Structured attacks include TracIn, IM-v4, and Hybrid-v4.
- The final matrix covers 5 methods, 2 datasets, 3 backbones, 6 strategies, and 950 runs.

Speaker Notes:
The workflow has four steps. First, select deletion targets, either randomly or with a structured strategy such as TracIn, IM-v4, or Hybrid-v4. Second, apply the chosen graph unlearning method. Third, run an exact retrain control on the same deletion set. This shows what the post-deletion model should ideally look like without approximation error. Fourth, compare the main outputs: relative F1 drop, retrain gap, collateral effects, and efficiency. The completed evaluation covers five unlearning methods, two citation-graph datasets, three GNN backbones, six node-selection strategies, and 950 total runs.

## Slide 6: Attack Selection Logic

Goal: Explain that structured attacks differ by selection logic, not only by name.

Estimated Time: 0:45

Key Lines:
- TracIn or IF-style selection is model-aware.
- IM-v4 is graph-structural and aims at spread or disruption.
- Hybrid combines model-side influence with topology-side spread.

Speaker Notes:
Before defining the metrics, I want to clarify what the attack strategies are actually doing. These are not just arbitrary labels. TracIn, or more broadly IF-style logic, is model-aware: it tries to pick nodes with high training influence on the learned model. IM-v4 is graph-structural: it tries to pick nodes that maximize spread or disruption in the graph itself. Hybrid combines both signals. I put a small formula on the slide, but it is only there as shorthand intuition, not something I need the audience to parse line by line. So the benchmark is not only comparing heuristics; it is comparing attacker logics, including model-aware selection, graph-structural selection, and a hybrid of the two.

## Slide 7: Metrics Framework

Goal: Define the core metrics before the main results.

Estimated Time: 0:50

Key Lines:
- `relative_f1_drop = F1_after(k=5, random) - F1_after(attack)`.
- Use a tiny random-trigger baseline because raw utility drop can be misleading for shard-based methods.
- `retrain_gap` and collateral metrics explain where the degradation comes from.

Speaker Notes:
Before showing the main results, I want to define the metrics clearly. The main utility metric is relative F1 drop, but the important design choice is the reference point. Instead of relying only on raw F1 before minus F1 after, I first trigger each method with a very small random deletion, k equals 5, and use that post-unlearning F1 as the baseline. This matters because shard-based methods such as GraphEraser can show method-induced score shifts after deletion, so raw drop alone can be misleading. Relative F1 drop therefore measures extra damage beyond that small-trigger baseline. To explain why a method degrades, I then use retrain gap and collateral metrics. Retrain gap compares approximate unlearning against exact retraining on the same deletion set, and collateral metrics track how much the retained nodes are disturbed.

## Slide 8: Main Finding: Family Spectrum

Goal: Present the main family-level result.

Estimated Time: 1:50

Key Lines:
- Relative F1 drop reveals a clear family-level vulnerability spectrum.
- GNNDelete is the most fragile representative in the tested settings.
- GIF stays comparatively stable, while GraphEraser shows shard protection.

Speaker Notes:
This is the main result of the project. When I compare relative F1 drop across datasets and backbones at the same deletion ratio, I do not see one shared failure pattern. Instead, I see a clear vulnerability spectrum across graph unlearning families. GNNDelete is consistently the most fragile representative. GIF remains comparatively stable, with much smaller extra drops beyond the k equals 5 baseline. GraphEraser behaves qualitatively differently again: because raw utility change can be negative, the relative metric is the cleaner way to compare it against the other families. In the tested settings, GraphEraser shows a shard protection pattern rather than the expected collapse. The companion strategy view leads to the same concentration pattern: the strongest extra damage still clusters on GNNDelete rather than spreading evenly across families. So the broader takeaway is that robustness is mechanism-dependent, and the metric definition matters for reading that spectrum correctly.

## Slide 9: Ratio Sensitivity And Ablation

Goal: Show how attack strength changes with deletion ratio.

Estimated Time: 1:20

Key Lines:
- The ratio figure works like an ablation on deletion budget.
- GNNDelete stays sensitive even at very small ratios.
- GIF remains comparatively flat, showing much weaker amplification.

Speaker Notes:
To make the spectrum more concrete, I next use the ratio-sensitivity figure as an ablation-style view. The question here is not only which method is worse at one fixed budget, but how attack strength changes as the deletion ratio increases. GNNDelete already shows strong amplification even at a very small ratio, which means the vulnerability appears early rather than only under large deletion budgets. GIF remains much flatter across the same range. So this page supports the interpretation that the family difference is structural rather than a one-point artifact of the ratio chosen for the main comparison.

## Slide 10: Attribution And Collateral Damage

Goal: Explain how the project separates attack success from approximation-induced spillover.

Estimated Time: 1:10

Key Lines:
- Relative F1 drop says the attack beat the k=5 baseline.
- Retrain gap says how much extra error comes from approximation.
- Collateral metrics show how strongly retained nodes are disturbed.

Speaker Notes:
This slide summarizes the attribution logic. Relative F1 drop tells us whether a structured attack beats the k equals 5 method baseline, but it does not by itself explain why. That is why the exact retrain control is essential. It tells us what should happen on the same deletion set if approximation error were absent. The gap between approximate unlearning and exact retraining is the retrain gap, and that is the part we should attribute to the mechanism. I then use collateral metrics, such as prediction flips and mean prediction shift on retained nodes, to show how far the disturbance propagates beyond the requested deletions. So the three metrics answer three different questions: did the attack work, where did the error come from, and how far did it spread.

## Slide 11: GraphEraser And Shard Protection

Goal: Support the shard-protection reading with a concrete GraphEraser view.

Estimated Time: 1:00

Key Lines:
- The observed GraphEraser score distribution shifts upward after unlearning.
- That is why raw utility drop alone is not the right cross-family metric here.
- This is setting-specific evidence for a shard protection effect, not universal robustness.

Speaker Notes:
GraphEraser behaves differently enough that it deserves its own evidence slide. Here I show the observed score shift for GraphEraser on Cora with a GCN backbone. The after-unlearning distribution moves upward across the tested attack strategies, which is why I said earlier that raw utility drop alone can be misleading for shard-based methods. A plausible explanation is that removing bridge or hub nodes changes the partition structure in a way that makes shard-local classification easier and reduces cross-shard interference. This is still a narrow claim. I am not saying GraphEraser is universally robust. I am saying that under the tested settings, the evidence is more consistent with a shard protection effect than with the collapse pattern seen in GNNDelete.

## Slide 12: Statistical Support And Effect Size

Goal: Strengthen the main result with support and effect-size evidence.

Estimated Time: 1:10

Key Lines:
- Figure 4a asks how strongly the attack-over-random gap is supported.
- Figure 4b asks how large that extra damage is.
- GNNDelete is strong on both support and effect size.

Speaker Notes:
I then strengthen the main result with statistical-support and effect-size evidence. Figure 4a asks how strongly the attack-over-random difference is supported, while Figure 4b asks how large that difference is once support is established. This matters because a visible pattern alone can still look thin if we do not show whether it is consistent. The key read is that GNNDelete is strong on both axes: it shows both clear support and large extra damage. The other families are more moderate, which is consistent with the main spectrum rather than a contradiction to it.

## Slide 13: Limitations And Future Work

Goal: Close the project honestly without making the deck sound unfinished.

Estimated Time: 1:00

Key Lines:
- This is a completed MSc project with clearly bounded claims.
- The main limits are benchmark scope and the lack of deeper GNNDelete mechanism analysis.
- The most credible future work is larger-benchmark validation plus targeted GNNDelete ablations.

Speaker Notes:
This project has clear limitations, and I want to state them directly. The evidence is strong within the tested citation benchmarks and backbones, but it should not be treated as universal across all graph domains. The second limit is explanatory depth: GNNDelete is clearly fragile in these experiments, but the mechanism-level reason still needs more targeted ablation. At the same time, this is a completed MSc project, not a midstream progress report. The most credible future work is to validate the same pattern on larger graph benchmarks such as PubMed and to run more targeted ablations that explain when and why GNNDelete fails.

## Slide 14: Takeaways

Goal: Close the main story in three memorable points.

Estimated Time: 0:45

Key Lines:
- Approximate graph unlearning can and should be stress-tested through adversarial deletion requests.
- Robustness differs substantially across method families.
- The project contributes both findings and a reusable workflow.

Speaker Notes:
To conclude, this project shows that approximate graph unlearning can and should be stress-tested through adversarial deletion requests. The main result is a clear family-level vulnerability spectrum defined through relative F1 drop: GNNDelete is the most fragile case in the tested settings, GIF is comparatively stable, and GraphEraser exhibits a shard protection effect rather than collapse. Just as importantly, the project leaves behind a practical OpenGU-based audit workflow that can support future work from a completed course submission. Thank you, and I welcome your questions.

## Slide 15: Backup Appendix

Goal: Keep statistical-support figures available for Q&A.

Estimated Time: 0:00

Key Lines:
- The appendix keeps the full strategy-spectrum figure available.
- It is backup material, not part of the main timed flow.
- Use it when asked about full method-by-strategy ranking.

Speaker Notes:
This backup slide is reserved for questions about the full strategy-by-method ranking after the main story has already been told.

## Continuous Full Script

Good afternoon. I am Liu Chengyu, and this presentation summarizes my EE5003 MSc project on adversarial deletion attacks against approximate graph unlearning. The motivating question behind this work is straightforward but important. If a system provides a deletion interface, can a malicious user exploit that interface by choosing nodes whose removal causes much more harm than a normal request should? In this project, I study that question across several graph unlearning families, build an evaluation workflow on top of OpenGU, and show that approximate unlearning methods do not inherit safety behavior equally.

To begin, graph unlearning matters because graph neural networks are increasingly used in settings where deletion requests are realistic. Examples include citation networks, recommendation systems, and social graphs. In these settings, removing data is not an unusual edge case; it is a plausible operational requirement driven by privacy, user control, and compliance. However, exact retraining after every request is often too expensive. That is why approximate unlearning methods are attractive. The problem is that approximation is also where risk enters. Once deletion is only approximated, the deletion interface itself can become an attack surface.

That leads to the main research question of the project: can malicious deletion requests amplify approximation error and degrade retained-model utility beyond what ordinary deletion would cause at the same budget? I organized the work around four objectives. First, build an attack pipeline that supports multiple node-selection strategies. Second, compare vulnerability across method families rather than presenting only a single-method case study. Third, introduce attribution metrics that separate true deletion impact from approximation-induced spillover. And fourth, evaluate whether adversarial node selection is efficient enough to be practically relevant rather than only a theoretical concern.

The evaluation covers several unlearning families. Learning-based unlearning is represented by GNNDelete. Influence-function-based unlearning is represented by GIF. The broader benchmark also includes IDEA, MEGU, and the shard-based GraphEraser. The threat model is deliberately practical and limited. The attacker can choose which nodes to delete through the normal deletion interface, but cannot poison labels, modify hidden hyperparameters, or change training code. So this is not a training-time attack. The attack succeeds if carefully chosen deletions produce more post-unlearning degradation than random deletion at the same ratio, especially when collateral effects also appear on retained nodes.

The experimental workflow has four clear steps. First, select deletion targets, either randomly or with a structured strategy such as TracIn, IM-v4, or Hybrid-v4. Second, apply the graph unlearning method to that deletion set. Third, run an exact retrain control on the same deletion set. This exact retrain baseline is essential because it tells us what the post-deletion model should ideally look like if approximation error were not present. Finally, compare the main outputs: relative F1 drop, retrain gap, collateral changes, and efficiency. The completed matrix is fairly broad for a course project: five methods, two citation-graph datasets, three GNN backbones, six selection strategies, and in total 950 experiment runs.

Before defining the metrics, I also want to clarify what the attack strategies are actually doing. These are not just arbitrary labels. TracIn, or more broadly IF-style logic, is model-aware: it tries to pick nodes with high training influence on the learned model. IM-v4 is graph-structural: it tries to pick nodes that maximize spread or disruption in the graph itself. Hybrid combines both signals. I put a small formula on the slide, but it is only there as shorthand intuition, not something I need the audience to parse line by line. So the benchmark is not only comparing heuristics; it is comparing attacker logics, including model-aware selection, graph-structural selection, and a hybrid of the two.

Before turning to the results, I want to define the metrics clearly. The main utility metric is relative F1 drop, but the important design choice is the reference point. Instead of relying only on raw F1 before minus F1 after, I first trigger each method with a very small random deletion, k equals 5, and use that post-unlearning F1 as the baseline. This matters because shard-based methods such as GraphEraser can show method-induced score shifts after deletion, so raw drop alone can be misleading. Relative F1 drop therefore measures extra damage beyond that small-trigger baseline. To explain where the degradation comes from, I then use retrain gap and collateral metrics. Retrain gap compares approximate unlearning against exact retraining on the same deletion set, and collateral metrics track how much the retained nodes are disturbed.

Now I come to the central result. When I compare relative F1 drop across datasets and backbones at the same deletion ratio, I do not observe one shared failure pattern. Instead, I observe a clear vulnerability spectrum across graph unlearning families. GNNDelete is consistently the most fragile representative in the tested settings. GIF remains comparatively stable, with much smaller extra drops beyond the k equals 5 baseline. GraphEraser behaves differently again, and the relative metric is exactly what makes that comparison interpretable: in the tested settings, it shows a shard protection pattern rather than the expected collapse. The companion strategy view leads to the same concentration pattern: the strongest extra damage still clusters on GNNDelete rather than spreading evenly across families. So the core takeaway is that robustness in approximate graph unlearning is mechanism-dependent, and the metric definition matters for reading that spectrum correctly.

To make that spectrum more concrete, I then use the ratio-sensitivity figure as an ablation-style view. The question here is how attack strength changes as the deletion ratio increases. GNNDelete already shows strong amplification even at a very small ratio, which means the vulnerability appears early rather than only under large deletion budgets. GIF remains much flatter across the same range. So this page supports the interpretation that the family difference is structural rather than a one-point artifact of the chosen ratio.

This is why attribution and collateral analysis are central rather than optional. Relative F1 drop tells us whether a structured attack beat the k equals 5 baseline, but it does not by itself explain why. The exact retrain control provides the right reference point for that same deletion set. The gap between approximate unlearning and exact retraining is the retrain gap, and that is the part we should attribute to the mechanism itself. Collateral damage adds another layer of evidence: if predictions on retained non-target nodes shift substantially, then the mechanism is producing spillover beyond the intended deletion boundary. So the three metrics answer three different questions: did the attack work, where did the error come from, and how far did it spread.

GraphEraser then requires a different interpretation because its behavior is counterintuitive. In the tested settings, deletion often improves downstream performance instead of reducing it. I describe this as a shard protection effect. The supporting slide shows the observed GraphEraser score shift on Cora with a GCN backbone, where the after-unlearning distribution moves upward across the tested strategies. That is why raw utility drop alone is not the right cross-family metric here. A plausible explanation is that removing bridge or hub nodes changes the partition structure in a way that makes shard-local classification easier and reduces cross-shard interference. At the same time, I want to be careful about the claim. This does not prove that GraphEraser is universally robust. The narrower claim is simply that, under the evaluated datasets and settings, the evidence is more consistent with a shard protection effect than with the collapse pattern seen in GNNDelete.

I then strengthen the main result with statistical-support and effect-size evidence. Figure 4a asks how strongly the attack-over-random difference is supported, while Figure 4b asks how large that difference is once support is established. This matters because a visible pattern alone can still look thin if we do not show whether it is consistent. The key read is that GNNDelete is strong on both axes: it shows both clear support and large extra damage. The other families are more moderate, which is consistent with the main spectrum rather than a contradiction to it.

Of course, the project also has clear limits. The evidence is strong within the evaluated citation benchmarks and backbones, but the conclusions should not be treated as universal across every graph domain. Some mechanisms, especially GNNDelete, still deserve deeper mechanism-level ablation to explain exactly why the approximation fails so badly under adversarial deletion. This is still a completed MSc project rather than an unfinished progress report. The most credible future work is to extend the evaluation to larger datasets such as PubMed and run more targeted ablations on GNNDelete.

To conclude, this MSc project shows that approximate graph unlearning can and should be stress-tested through adversarial deletion requests. The main finding is a clear vulnerability spectrum across method families: GNNDelete is the most fragile case in the tested settings, GIF is comparatively stable, and GraphEraser exhibits a shard protection effect rather than the expected collapse. Just as importantly, the project contributes a practical OpenGU-based audit workflow that makes these evaluations reproducible and extendable. So the final output is both an analytical finding and an operational foundation for future work from a completed course submission. Thank you, and I welcome your questions.

