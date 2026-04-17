# EE5003 Final Presentation Speech Script

- Audience: EE5003 course assessment / supervisor-style academic review
- Language: English PPT + English script
- Main timed deck: 13 slides
- Estimated total speaking time: 14:25

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
- The attacker controls only the deletion request.
- Success is measured by extra damage over random deletion plus collateral effects.

Speaker Notes:
The evaluation spans several unlearning families. Learning-based unlearning is represented by GNNDelete. Influence-function-based unlearning is represented by GIF. The broader benchmark also includes IDEA, MEGU, and the shard-based GraphEraser. The threat model is deliberately practical. The attacker can choose which nodes to delete through the normal interface, but does not modify labels, features, optimizer settings, or hidden training code. This is not a poisoning attack. The attack succeeds if carefully chosen deletions create more retained-model degradation than random deletion at the same ratio. I also track collateral damage on retained nodes.

## Slide 5: Attack Pipeline And Experimental Matrix

Goal: Explain the workflow and experimental scope.

Estimated Time: 1:30

Key Lines:
- The pipeline is select nodes, unlearn, exact retrain, and compare.
- Structured attacks include TracIn, IM-v4, and Hybrid-v4.
- The final matrix covers 5 methods, 2 datasets, 3 backbones, 6 strategies, and 950 runs.

Speaker Notes:
The workflow has four steps. First, select deletion targets, either randomly or with a structured strategy such as TracIn, IM-v4, or Hybrid-v4. Second, apply the chosen graph unlearning method. Third, run an exact retrain control on the same deletion set. This shows what the post-deletion model should ideally look like without approximation error. Fourth, compare retained-model utility, retrain gap, and collateral effects. The completed evaluation covers five unlearning methods, two citation-graph datasets, three GNN backbones, six node-selection strategies, and 950 total runs.

## Slide 6: What Was Built In OpenGU

Goal: Show the implemented engineering work behind the analysis.

Estimated Time: 1:00

Key Lines:
- The output is a reusable adversarial-audit workflow, not only experiment logs.
- I implemented execution, result discovery, collateral analysis, aggregation, and figure generation.
- This makes the final analysis reproducible from stored outputs.

Speaker Notes:
A major project outcome is the workflow itself. I extended OpenGU into a reusable adversarial-audit pipeline instead of treating each experiment as an isolated manual run. The completed assets cover experiment execution, result auto-discovery, collateral evaluation, statistical aggregation, and figure generation. I also did practical debugging and cleanup to make the pipeline stable enough for repeated analysis. This matters because the project contributes both findings and infrastructure. The results in the report can be reproduced from stored outputs rather than depending on ad hoc manual processing.

## Slide 7: Main Finding: Vulnerability Spectrum

Goal: Present the main family-level result.

Estimated Time: 2:00

Key Lines:
- Vulnerability differs strongly across graph unlearning families.
- GNNDelete is the most fragile representative in the tested settings.
- GIF stays comparatively stable, while GraphEraser behaves differently again.

Speaker Notes:
This is the main result of the project. When I compare relative F1 drop across datasets and backbones at the same deletion ratio, I do not see one shared failure pattern. Instead, I see a clear vulnerability spectrum across method families. GNNDelete is consistently the most fragile representative. GIF remains comparatively stable, with much smaller degradation under the same attack budgets. GraphEraser does not show the same collapse pattern and in these settings often improves relative to its own post-unlearning baseline. The broader takeaway is that approximate unlearning robustness is not inherited uniformly. The mechanism matters, and family-level comparisons are therefore necessary.
## Slide 8: Deep Dive: GNNDelete Is The Most Fragile

Goal: Explain the strongest failure case in concrete numbers.

Estimated Time: 1:30

Key Lines:
- On Cora at ratio 0.01, IM-v4 produces a 21.53% retrain gap.
- At the same time, 26.2% of non-target predictions change.
- Exact retraining shows only a small intrinsic decrease, so the main problem is approximation error.

Speaker Notes:
To make the spectrum more concrete, I focus on the strongest failure case. On Cora at deletion ratio 0.01, the IM-v4 strategy drives GNNDelete to a retrain gap of 21.53 percent, while 26.2 percent of non-target predictions change. That second number is especially important because it shows that the damage is not confined to the deleted targets. The effect spreads into retained parts of the graph. When I compare the same deletion set against exact retraining, the exact retrain result shows only a small intrinsic drop. So the collapse is mainly caused by approximation error rather than node importance alone.

## Slide 9: Attribution And Collateral Damage

Goal: Explain how the project distinguishes true deletion effect from spillover.

Estimated Time: 1:10

Key Lines:
- Utility drop alone is not enough to prove fragility.
- Exact retraining isolates the mechanism-induced component.
- Collateral changes on retained nodes are a core diagnostic.

Speaker Notes:
This slide summarizes the attribution logic. If we only observe lower utility after deletion, that does not automatically mean the unlearning method is fragile. Some nodes are naturally important, so any correct system may lose a small amount of utility after removing them. That is why the exact retrain control is essential. It tells us what should happen on the same deletion set without approximation error. The gap between approximate unlearning and exact retraining is the part we should attribute to the mechanism. Collateral damage then tells us how far the disturbance spreads beyond the requested deletion targets.

## Slide 10: Why GraphEraser Behaves Differently

Goal: Support the shard-protection reading with a concrete GraphEraser view.

Estimated Time: 1:00

Key Lines:
- The observed GraphEraser score distribution shifts upward after unlearning.
- A plausible explanation is easier shard-local classification after removing bridge or hub nodes.
- This remains setting-specific evidence, not a claim of universal robustness.

Speaker Notes:
GraphEraser behaves differently enough that it deserves its own evidence slide. Here I show the observed score shift for GraphEraser on Cora with a GCN backbone. The after-unlearning distribution moves upward across the tested attack strategies, which is consistent with the non-collapse pattern seen earlier. A plausible explanation is that removing bridge or hub nodes changes the partition structure in a way that makes shard-local classification easier and reduces cross-shard interference. This is still a narrow claim. I am not saying GraphEraser is universally robust. I am only saying that under the datasets and settings tested here, adversarial deletion did not trigger the same collapse pattern that appeared in GNNDelete.

## Slide 11: Attack Strength And Practicality

Goal: Show that structured attacks beat random deletion and are practical to run.

Estimated Time: 1:40

Key Lines:
- Relative F1 drop measures attack-over-random advantage more fairly.
- The largest advantage appears on GNNDelete.
- IM-v4 cuts selection time to 18.9 seconds with only 1.3% spread loss.

Speaker Notes:
Beyond the family comparison, I also wanted to know whether structured attacks are practical. Figure 3 compares the main strategies using relative F1 drop, which asks how much worse structured deletion is than random deletion at the same budget. Again, the largest attack-over-random advantage appears on GNNDelete, while the other families remain more moderate. On the efficiency side, the key optimization is IM-v4. Compared with the baseline CELF-style selection, IM-v4 reduces selection time from 653 seconds to 18.9 seconds while losing only 1.3 percent in spread. That means adversarial node selection is not only possible in principle, but operationally feasible.

## Slide 12: Limitations And Future Work

Goal: Close the project honestly without making the deck sound unfinished.

Estimated Time: 1:00

Key Lines:
- This is a completed MSc project with clearly bounded claims.
- The main limits are benchmark scope and the lack of deeper GNNDelete mechanism analysis.
- The most credible future work is larger-benchmark validation plus targeted GNNDelete ablations.

Speaker Notes:
This project has clear limitations, and I want to state them directly. The evidence is strong within the tested citation benchmarks and backbones, but it should not be treated as universal across all graph domains. The second limit is explanatory depth: GNNDelete is clearly fragile in these experiments, but the mechanism-level reason still needs more targeted ablation. At the same time, this is a completed MSc project, not a midstream progress report. The most credible future work is to validate the same pattern on larger graph benchmarks such as PubMed and to run more targeted ablations that explain when and why GNNDelete fails.

## Slide 13: Takeaways

Goal: Close the main story in three memorable points.

Estimated Time: 0:45

Key Lines:
- Approximate graph unlearning can and should be stress-tested through adversarial deletion requests.
- Robustness differs substantially across method families.
- The project contributes both findings and a reusable workflow.

Speaker Notes:
To conclude, this project shows that approximate graph unlearning can and should be stress-tested through adversarial deletion requests. The main result is a clear family-level vulnerability spectrum: GNNDelete is the most fragile case in the tested settings, GIF is comparatively stable, and GraphEraser exhibits a shard protection effect rather than collapse. Just as importantly, the project leaves behind a practical OpenGU-based audit workflow that can support future work from a completed course submission. Thank you, and I welcome your questions.

## Slide 14: Backup Appendix

Goal: Keep statistical-support figures available for Q&A.

Estimated Time: 0:00

Key Lines:
- The appendix separates statistical support from effect size.
- It is backup material, not part of the main timed flow.
- Use it when asked about evidence beyond the primary spectrum figure.

Speaker Notes:
This backup slide is reserved for questions about significance and effect size. It separates how strongly the attack-over-random difference is supported from how large that difference is.

## Continuous Full Script

Good afternoon. I am Liu Chengyu, and this presentation summarizes my EE5003 MSc project on adversarial deletion attacks against approximate graph unlearning. The motivating question behind this work is straightforward but important. If a system provides a deletion interface, can a malicious user exploit that interface by choosing nodes whose removal causes much more harm than a normal request should? In this project, I study that question across several graph unlearning families, build an evaluation workflow on top of OpenGU, and show that approximate unlearning methods do not inherit safety behavior equally.

To begin, graph unlearning matters because graph neural networks are increasingly used in settings where deletion requests are realistic. Examples include citation networks, recommendation systems, and social graphs. In these settings, removing data is not an unusual edge case; it is a plausible operational requirement driven by privacy, user control, and compliance. However, exact retraining after every request is often too expensive. That is why approximate unlearning methods are attractive. The problem is that approximation is also where risk enters. Once deletion is only approximated, the deletion interface itself can become an attack surface.

That leads to the main research question of the project: can malicious deletion requests amplify approximation error and degrade retained-model utility beyond what ordinary deletion would cause at the same budget? I organized the work around four objectives. First, build an attack pipeline that supports multiple node-selection strategies. Second, compare vulnerability across method families rather than presenting only a single-method case study. Third, introduce attribution metrics that separate true deletion impact from approximation-induced spillover. And fourth, evaluate whether adversarial node selection is efficient enough to be practically relevant rather than only a theoretical concern.

The evaluation covers several unlearning families. Learning-based unlearning is represented by GNNDelete. Influence-function-based unlearning is represented by GIF. The broader benchmark also includes IDEA, MEGU, and the shard-based GraphEraser. The threat model is deliberately practical and limited. The attacker can choose which nodes to delete through the normal deletion interface, but cannot poison labels, modify hidden hyperparameters, or change training code. So this is not a training-time attack. The attack succeeds if carefully chosen deletions produce more post-unlearning degradation than random deletion at the same ratio, especially when collateral effects also appear on retained nodes.

The experimental workflow has four clear steps. First, select deletion targets, either randomly or with a structured strategy such as TracIn, IM-v4, or Hybrid-v4. Second, apply the graph unlearning method to that deletion set. Third, run an exact retrain control on the same deletion set. This exact retrain baseline is essential because it tells us what the post-deletion model should ideally look like if approximation error were not present. Finally, compare retained-model utility, retrain gap, and collateral changes. The completed matrix is fairly broad for a course project: five methods, two citation-graph datasets, three GNN backbones, six selection strategies, and in total 950 experiment runs.

A major output of the project is the workflow itself. I did not want the contribution to be only a one-off collection of experiment logs. So I extended OpenGU into a reusable adversarial-audit pipeline. The completed assets include experiment execution, result auto-discovery, collateral-damage analysis, statistical aggregation, and figure generation. I also spent time on debugging and cleanup to make the workflow stable enough for repeated use. This matters because the project leaves behind a reproducible operational base. The analysis is tied to a usable process, not only to manual interpretation after the fact.

Now I come to the central result. When I compare relative F1 drop across datasets and backbones at the same deletion ratio, I do not observe one shared failure pattern. Instead, I observe a clear vulnerability spectrum across graph unlearning families. GNNDelete is consistently the most fragile representative in the tested settings. GIF remains comparatively stable, with much smaller degradation under the same attack budgets. GraphEraser behaves differently again and does not show the same kind of collapse. In some tested settings, it even improves relative to its own post-unlearning baseline. The core takeaway is that robustness in approximate graph unlearning is mechanism-dependent, so family-level comparison is necessary.

To make that spectrum more concrete, I then focus on the strongest failure case. On Cora at deletion ratio 0.01, the IM-v4 strategy drives GNNDelete to a retrain gap of 21.53 percent, while 26.2 percent of non-target predictions change. That second number is particularly important because it shows that the disturbance is not confined to the deleted nodes. The effect propagates into retained parts of the graph. When I compare the same deletion set against exact retraining, the exact retrain result shows only a small intrinsic decrease. That means the collapse is mainly caused by approximation error in the unlearning mechanism, not simply because the selected nodes were naturally indispensable.

This is why attribution and collateral analysis are central rather than optional. A utility drop alone is not enough to prove fragility, because some deleted nodes may really be important. Any correct system may lose a little utility after removing them. The exact retrain control provides the right reference point for that same deletion set. The gap between approximate unlearning and exact retraining is therefore the part we should attribute to the mechanism itself. Collateral damage adds another layer of evidence: if predictions on retained non-target nodes shift substantially, then the mechanism is producing spillover beyond the intended deletion boundary.

GraphEraser requires a different interpretation because its behavior is counterintuitive. In the tested settings, deletion often improves downstream performance instead of reducing it. I describe this as a shard protection effect. The supporting slide shows the observed GraphEraser score shift on Cora with a GCN backbone, where the after-unlearning distribution moves upward across the tested strategies. A plausible explanation is that removing bridge or hub nodes changes the partition structure in a way that makes shard-local classification easier and reduces cross-shard interference. At the same time, I want to be careful about the claim. This does not prove that GraphEraser is universally robust. The narrower claim is simply that, under the evaluated datasets and settings, adversarial deletion did not trigger the same collapse pattern that appeared in GNNDelete.

Beyond the family-level result, I also wanted to know whether structured attacks are practical. Figure 3 compares the main attack strategies using relative F1 drop, which is useful because it measures the attack-over-random advantage at the same budget. Again, the strongest advantage appears on GNNDelete, while the other families remain more moderate. On the efficiency side, the most important optimization is IM-v4. Compared with the baseline CELF-style approach, IM-v4 reduces selection time from 653 seconds to 18.9 seconds while losing only 1.3 percent in spread. That is a meaningful result because it shows adversarial node selection is not just conceptually possible; it is operationally feasible.

Of course, the project also has clear limits. The evidence is strong within the evaluated citation benchmarks and backbones, but the conclusions should not be treated as universal across every graph domain. Some mechanisms, especially GNNDelete, still deserve deeper mechanism-level ablation to explain exactly why the approximation fails so badly under adversarial deletion. This is still a completed MSc project rather than an unfinished progress report. The most credible future work is to extend the evaluation to larger datasets such as PubMed and run more targeted ablations on GNNDelete.

To conclude, this MSc project shows that approximate graph unlearning can and should be stress-tested through adversarial deletion requests. The main finding is a clear vulnerability spectrum across method families: GNNDelete is the most fragile case in the tested settings, GIF is comparatively stable, and GraphEraser exhibits a shard protection effect rather than the expected collapse. Just as importantly, the project contributes a practical OpenGU-based audit workflow that makes these evaluations reproducible and extendable. So the final output is both an analytical finding and an operational foundation for future work from a completed course submission. Thank you, and I welcome your questions.

