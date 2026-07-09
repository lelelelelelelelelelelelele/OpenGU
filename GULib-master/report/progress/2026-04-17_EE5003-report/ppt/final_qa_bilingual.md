# EE5003 Defense Q&A Handbook (Bilingual)

## Purpose

This document is a defense-oriented bilingual Q&A handbook prepared for an MSc project presentation setting with a supervisor and one examiner. The expected questioning style is academic, selective, and possibly sharp. The goal is not to memorize long speeches, but to prepare short, defensible answers that are accurate, calm, and easy to adapt during live discussion.

---

## Opening Strategy

### General Answering Principles

- Start with a direct answer in one sentence.
- Then give one or two supporting reasons.
- Stay within the scope of the report and avoid over-claiming.
- Prefer phrases like `in the tested settings`, `based on the completed experiments`, and `a plausible interpretation is`.
- If challenged, defend the design logic first, then the result.

### General Answering Principles（中文）

- 先用一句话正面回答。
- 然后补一到两个支撑理由。
- 严格限定在报告范围内，不要把结论说满。
- 多用这些表达：`在本报告测试设定下`、`基于已完成实验`、`一个合理解释是`。
- 如果被追问，先守住设计逻辑，再解释结果。

### Useful Bridging Sentences

- `My short answer is yes, but with an important scope boundary.`
- `I would separate the empirical result from the broader claim.`
- `What I can claim confidently from this report is...`
- `I do not claim universality here; I only claim that under the tested settings...`
- `That is exactly why I used exact retraining as a control.`

### 常用缓冲句（中文）

- `我的简短回答是可以，但是要加一个范围限定。`
- `我会把经验结果和更广的理论结论分开。`
- `基于这份报告，我能比较有把握主张的是……`
- `这里我不主张普适性，我只主张在当前测试设定下……`
- `这也正是为什么我一定要加入 exact retrain 对照。`

---

## Core Questions

### Q1

**Question (EN)**: What is the core research question of your project?

**问题（中文）**：你的项目最核心的研究问题是什么？

**Suggested Answer (EN)**:
The core question is whether a malicious user can exploit the deletion interface of approximate graph unlearning by choosing nodes whose removal amplifies approximation error and degrades retained-model utility beyond ordinary deletion at the same budget.

**参考回答（中文）**：
我的核心研究问题是：恶意用户是否可以通过选择特定删除节点，利用 approximate graph unlearning 的 deletion interface，放大 approximation error，并使保留模型的性能下降超过同等预算下的普通删除。

**Answer Strategy**:
Give the question in one sentence and include both parts: `adversarial deletion choice` and `approximation error amplification`.

### Q2

**Question (EN)**: Why is this problem important?

**问题（中文）**：为什么这个问题重要？

**Suggested Answer (EN)**:
It is important because graph unlearning is motivated by practical deletion requests, but many methods rely on approximation rather than exact retraining. Once deletion is approximate, the deletion interface itself can become a security surface, not just a compliance feature.

**参考回答（中文）**：
这个问题重要，是因为 graph unlearning 的出发点本来就是处理真实删除请求，但很多方法并不是 exact retrain，而是依赖近似更新。一旦删除是近似的，deletion interface 就不只是合规功能，也可能变成一个安全攻击面。

**Answer Strategy**:
Tie together practicality, compliance, and security surface. Do not answer only from a privacy angle.

### Q3

**Question (EN)**: What is your main contribution?

**问题（中文）**：你的主要贡献是什么？

**Suggested Answer (EN)**:
My main contribution is twofold. Empirically, I show a clear vulnerability spectrum across graph unlearning families under adversarial deletion. Practically, I build a reusable adversarial-audit workflow on top of OpenGU, including selection strategies, exact retrain controls, collateral analysis, aggregation, and figure generation.

**参考回答（中文）**：
我的主要贡献有两部分。第一，经验结果上，我展示了 graph unlearning families 在 adversarial deletion 下存在明显的 vulnerability spectrum。第二，在工程和实验流程上，我在 OpenGU 上搭建了一套可复用的 adversarial audit workflow，包括节点选择策略、exact retrain 对照、collateral analysis、统计汇总和作图流程。

**Answer Strategy**:
Always give both the scientific contribution and the workflow contribution.

### Q4

**Question (EN)**: Why did you compare across method families instead of focusing on one method only?

**问题（中文）**：为什么你要跨方法家族比较，而不是只分析一个方法？

**Suggested Answer (EN)**:
Because the broader question is about whether safety behavior is inherited uniformly across approximate graph unlearning mechanisms. A single-method study can show a failure case, but it cannot reveal whether the vulnerability is method-specific or family-level.

**参考回答（中文）**：
因为我更关心的问题是：不同 approximate graph unlearning mechanism 是否会一致地继承某种安全行为。如果只看一个方法，我们最多证明一个 failure case，但无法判断这是方法特例，还是 family-level 的现象。

**Answer Strategy**:
Emphasize that family comparison answers a more general and more meaningful question.

### Q5

**Question (EN)**: Why is the threat model reasonable?

**问题（中文）**：你的 threat model 为什么是合理的？

**Suggested Answer (EN)**:
It is reasonable because it is operationally realistic. The attacker only controls which nodes to delete through the normal interface and does not rely on label poisoning, hidden hyperparameter changes, or privileged access. So the attack model is limited, but still practically relevant.

**参考回答（中文）**：
这个 threat model 是合理的，因为它在操作层面是现实可行的。攻击者只控制“删谁”，也就是正常 deletion interface 下的节点选择，而不依赖标签投毒、隐藏超参数修改或特权访问。因此这个攻击模型是受限的，但仍然有现实意义。

**Answer Strategy**:
Defend the realism of the threat model, not its maximal power.

### Q6

**Question (EN)**: Why did you use exact retraining as a control?

**问题（中文）**：为什么你一定要用 exact retraining 作为对照？

**Suggested Answer (EN)**:
Because utility drop alone is not enough to prove fragility. Some deleted nodes may be genuinely important. Exact retraining on the same deletion set tells me what the ideal post-deletion performance should look like without approximation error. That makes it possible to attribute the extra gap to the approximate unlearning mechanism.

**参考回答（中文）**：
因为单纯看到 utility drop，并不能直接说明方法脆弱。有些被删节点本来就可能很重要。对同一 deletion set 做 exact retraining，可以给出“没有 approximation error 时应有的 post-deletion performance”。这样我才能把多出来的差距归因到 approximate unlearning mechanism 本身。

**Answer Strategy**:
This is one of your strongest methodological defenses. Answer it clearly and confidently.

### Q7

**Question (EN)**: How do you know the damage is due to approximation error rather than node importance?

**问题（中文）**：你怎么知道性能下降主要来自 approximation error，而不是节点本身就很重要？

**Suggested Answer (EN)**:
That is exactly where the exact retrain control matters. In the strongest GNNDelete case, exact retraining on the same deletion set shows only a small intrinsic decrease, while approximate unlearning shows a much larger collapse. So the large additional gap is best interpreted as approximation-induced error rather than pure node importance.

**参考回答（中文）**：
这正是 exact retrain 对照的作用。在最强的 GNNDelete case 里，同一 deletion set 下，exact retraining 只显示出很小的 intrinsic decrease，但 approximate unlearning 出现了明显更大的 collapse。因此，更合理的解释是大部分额外损失来自 approximation-induced error，而不是纯粹的节点重要性。

**Answer Strategy**:
Use the contrast logic: same deletion set, different post-deletion behavior.

### Q8

**Question (EN)**: Why do you conclude that GNNDelete is the most fragile case?

**问题（中文）**：为什么你认为 GNNDelete 是最脆弱的情况？

**Suggested Answer (EN)**:
Because across the tested settings, GNNDelete consistently shows the largest attack-over-random degradation and the strongest retrain-gap behavior. In the strongest case, it also shows substantial collateral changes on non-target predictions, which suggests that the disturbance spreads beyond the deleted nodes.

**参考回答（中文）**：
因为在本报告测试设定下，GNNDelete 持续表现出最大的 attack-over-random degradation，以及最明显的 retrain gap。在最强 case 里，它还伴随着显著的非目标节点预测变化，这说明扰动并不局限于被删除节点，而是扩散到了 retained part。

**Answer Strategy**:
Use `consistency across tested settings` plus `strongest-case evidence`.

### Q9

**Question (EN)**: Why is GIF comparatively stable?

**问题（中文）**：为什么 GIF 相对稳定？

**Suggested Answer (EN)**:
Empirically, GIF shows much smaller relative F1 drop and smaller attack-over-random gains in the tested settings. I present this as an observed stability pattern rather than a full mechanism-level explanation, because this report focuses more on adversarial auditing than on theoretical derivation.

**参考回答（中文）**：
从实验上看，GIF 在本报告测试设定下表现出更小的 relative F1 drop，以及更小的 attack-over-random gain。所以我把它表述为一个 observed stability pattern，而不是完整的机制层解释，因为这份报告更侧重 adversarial auditing，而不是理论推导。

**Answer Strategy**:
Do not invent a deep causal explanation you did not fully test.

### Q10

**Question (EN)**: Why does GraphEraser sometimes improve after deletion? Is that believable?

**问题（中文）**：为什么 GraphEraser 删除后反而会变好？这个结果可信吗？

**Suggested Answer (EN)**:
I think it is believable within the tested settings, but it should be interpreted carefully. A plausible explanation is that deleting bridge or hub nodes changes the shard structure in a way that makes local sub-model classification easier. However, I do not claim universal robustness. I only claim that under the current datasets and settings, GraphEraser did not show the same collapse pattern as GNNDelete.

**参考回答（中文）**：
我认为在当前测试设定下，这个结果是可信的，但需要谨慎解释。一个合理解释是，删除 bridge 或 hub 节点后，shard 结构发生变化，从而让局部子模型的分类任务变得更容易。不过我并不主张 GraphEraser 具有普适鲁棒性；我只主张在当前数据集和实验设置下，它没有表现出像 GNNDelete 那样的 collapse pattern。

**Answer Strategy**:
Defend plausibility, but immediately add a scope boundary.

### Q11

**Question (EN)**: Why did you use relative F1 drop instead of raw score differences only?

**问题（中文）**：为什么你用 relative F1 drop，而不只是看原始分数差？

**Suggested Answer (EN)**:
Because relative F1 drop is better for comparing structured attacks against a random baseline at the same deletion budget. It makes the attack-over-random advantage easier to interpret across methods whose absolute post-unlearning scores may already differ.

**参考回答（中文）**：
因为 relative F1 drop 更适合在相同 deletion budget 下，把 structured attack 和 random baseline 做公平比较。不同方法原本的 post-unlearning absolute score 可能就不同，所以 relative F1 drop 更容易反映真正的 attack-over-random advantage。

**Answer Strategy**:
Frame it as a fairness and interpretability choice.

### Q12

**Question (EN)**: Why does IM-v4 matter so much in your project?

**问题（中文）**：为什么 IM-v4 在你的项目里这么重要？

**Suggested Answer (EN)**:
IM-v4 matters because it turns adversarial node selection from a conceptual possibility into a practical one. It reduces selection time dramatically while preserving most of the spread quality, so it supports the claim that adversarial deletion can be operationally feasible.

**参考回答（中文）**：
IM-v4 重要，是因为它把 adversarial node selection 从“概念上可行”推进到了“实践中也可行”。它显著降低了选择时间，同时保留了大部分 spread quality，因此支撑了 adversarial deletion 在操作层面具备现实性的结论。

**Answer Strategy**:
Connect IM-v4 directly to practical relevance, not just algorithm speed.

### Q13

**Question (EN)**: What is the biggest limitation of your work?

**问题（中文）**：你这项工作最大的局限是什么？

**Suggested Answer (EN)**:
The biggest limitation is scope. The conclusions are strong within the tested datasets, backbones, and methods, but they are not universal claims across all graph domains. A second limitation is that the report identifies strong empirical patterns, but does not fully complete mechanism-level explanation for every method.

**参考回答（中文）**：
我认为最大的局限是 scope。我的结论在当前测试的数据集、backbone 和方法范围内是有力的，但并不是对所有 graph domain 的普适结论。第二个局限是，这份报告清楚识别了经验模式，但还没有对每一种方法都完成完整的 mechanism-level explanation。

**Answer Strategy**:
A good limitation answer is honest but not self-destructive.

### Q14

**Question (EN)**: If you had more time, what would be the most valuable next step?

**问题（中文）**：如果再给你更多时间，最值得做的下一步是什么？

**Suggested Answer (EN)**:
The most valuable next step would be to combine scale extension and mechanism analysis: first validate whether the same pattern holds on larger datasets such as PubMed, and then run targeted GNNDelete ablations to explain why its approximation error becomes so severe under adversarial deletion.

**参考回答（中文）**：
如果有更多时间，我认为最值得做的下一步是把“扩大规模”和“机制分析”结合起来：先在更大的数据集比如 PubMed 上验证同样模式是否还存在，再针对 GNNDelete 做更细的 ablation，解释为什么它在 adversarial deletion 下会出现这么严重的 approximation error。

**Answer Strategy**:
Give one coherent next step, not a shopping list.

### Q15

**Question (EN)**: What should the audience remember as your final takeaway?

**问题（中文）**：你最希望听众记住的最终 takeaway 是什么？

**Suggested Answer (EN)**:
The final takeaway is that approximate graph unlearning should be evaluated not only for utility and efficiency, but also for robustness under adversarial deletion requests. Different method families behave very differently, and that difference is both measurable and practically important.

**参考回答（中文）**：
我最希望听众记住的是：approximate graph unlearning 不应该只从 utility 和 efficiency 角度评价，还应该从 adversarial deletion robustness 的角度去审视。不同方法家族的行为差异非常大，而且这种差异既可以被测量，也有实际意义。

**Answer Strategy**:
End on the project's broadest insight, not on a single number.

---

## Likely Tough Questions

### Tough Q1

**Question (EN)**: Are you really evaluating unlearning robustness, or are you just finding important nodes?

**问题（中文）**：你这到底是在评估 unlearning robustness，还是只是在找重要节点？

**Suggested Answer (EN)**:
If I only showed utility drop after deletion, that criticism would be fair. But the exact retrain control changes the interpretation. Important nodes can explain some intrinsic loss, but they cannot explain why approximate unlearning collapses much more than exact retraining on the same deletion set. That extra gap is exactly the robustness problem.

**参考回答（中文）**：
如果我只是展示删除后的 utility drop，那这个质疑是成立的。但 exact retrain 对照改变了这个解释。重要节点确实可以解释一部分 intrinsic loss，但它不能解释为什么同一个 deletion set 下，approximate unlearning 比 exact retraining 坍塌得严重得多。这个额外差距正是 robustness 问题本身。

**Answer Strategy**:
This is a very likely examiner question. Defend with the control logic.

### Tough Q2

**Question (EN)**: Why should anyone believe that your strongest case is not just an outlier?

**问题（中文）**：为什么别人要相信你最强的 case 不是一个偶然的 outlier？

**Suggested Answer (EN)**:
I do not rely only on a single extreme example. The strongest case is useful for illustration, but the broader claim comes from repeated family-level patterns across multiple settings, plus the consistent direction of attack-over-random comparisons. So the strong case is an example of the pattern, not the entire basis for the conclusion.

**参考回答（中文）**：
我并不是只依赖一个极端案例。最强 case 主要是为了说明问题，但更广的结论来自多个 setting 下反复出现的 family-level pattern，以及 attack-over-random comparison 方向上的一致性。所以最强 case 是这个模式的一个例子，而不是全部结论的唯一基础。

**Answer Strategy**:
Shift from `single case` to `pattern across settings`.

### Tough Q3

**Question (EN)**: Your explanation for GraphEraser sounds speculative. How do you justify it academically?

**问题（中文）**：你对 GraphEraser 的解释听起来有点推测性，你怎么从学术上自圆其说？

**Suggested Answer (EN)**:
I agree that it is an interpretation, not a proven mechanism. That is why I phrase it as a plausible explanation rather than a definitive claim. The empirical result itself is solid within the tested settings, while the mechanism-level explanation remains a motivated interpretation that should be tested more directly in future work.

**参考回答（中文）**：
我同意这更像是一种 interpretation，而不是已经被证明的机制。这也是为什么我在报告里把它表述成 plausible explanation，而不是 definitive claim。经验结果本身在当前测试设定下是明确的，但机制层解释仍然是一个有根据的推断，需要在后续工作中做更直接的验证。

**Answer Strategy**:
The safest academic move is to distinguish result from interpretation.

### Tough Q4

**Question (EN)**: Why did you not include larger datasets if you want to make a broad claim?

**问题（中文）**：如果你想得出较广的结论，为什么不直接加入更大的数据集？

**Suggested Answer (EN)**:
Because this report is positioned as a completed MSc project with a strong empirical core, not as a final universal benchmark paper. I chose a scope that was large enough to support meaningful cross-family comparison, but still feasible within the project timeline. I therefore make a bounded claim rather than a universal one.

**参考回答（中文）**：
因为这份报告的定位是一个已经完成的 MSc project，而不是最终形态的 universal benchmark paper。我选择的是一个既足以支持有意义 family comparison、又在项目周期内可完成的范围。所以我的做法不是去强行做普适结论，而是给出一个有边界的结论。

**Answer Strategy**:
Defend scope as a principled project decision, not as an omission alone.

### Tough Q5

**Question (EN)**: Could your results depend too much on the benchmark framework rather than the methods themselves?

**问题（中文）**：你的结果会不会过度依赖 benchmark framework，而不是方法本身？

**Suggested Answer (EN)**:
That is a valid caution, and I partially address it by comparing multiple methods within the same evaluation environment. Using a shared framework reduces evaluation inconsistency and makes the comparisons more controlled. At the same time, I would not claim framework-independence without further external replication.

**参考回答（中文）**：
这是一个合理提醒。我部分缓解这个问题的方式，是在同一个 evaluation environment 里比较多个方法。共享 framework 至少减少了评估不一致性，使比较更受控。但与此同时，如果没有额外外部复现，我也不会主张这些结果已经完全 framework-independent。

**Answer Strategy**:
Acknowledge the concern, then explain why a shared framework is also a strength.

### Tough Q6

**Question (EN)**: Is your work more of a systems contribution or a scientific contribution?

**问题（中文）**：你的工作更像是系统工程贡献，还是科学问题贡献？

**Suggested Answer (EN)**:
I would say it is a scientific evaluation project enabled by systems work. The workflow is necessary because without it, the comparison would not be reproducible or scalable. But the final contribution is still a scientific conclusion about vulnerability differences across graph unlearning families.

**参考回答（中文）**：
我会说，这是一个由系统工程支撑起来的 scientific evaluation project。workflow 很重要，因为没有它，这种比较就不够可复现，也不够可扩展。但最终的核心贡献仍然是一个 scientific conclusion，也就是 graph unlearning families 在 vulnerability 上存在显著差异。

**Answer Strategy**:
Position the workflow as enabling infrastructure, not as the only outcome.

### Tough Q7

**Question (EN)**: If someone disagrees with your interpretation, what part of your result is still safe?

**问题（中文）**：如果有人不认同你的解释，哪些结论仍然是稳的？

**Suggested Answer (EN)**:
Even if one questions some interpretation, the safe empirical conclusions remain: first, adversarial deletion can produce attack-over-random degradation; second, the magnitude differs across method families; third, GNNDelete is the most fragile case in the tested settings; and fourth, exact retrain controls are necessary for proper attribution.

**参考回答（中文）**：
即使有人不接受部分机制解释，稳固的经验结论仍然成立：第一，adversarial deletion 确实能带来 attack-over-random degradation；第二，这种幅度在不同 method families 之间明显不同；第三，在当前测试设定下，GNNDelete 是最脆弱的情况；第四，exact retrain 对照对于正确归因是必要的。

**Answer Strategy**:
This answer is useful when you need to retreat from interpretation without losing the core result.

---

## Fast Defense Sheet

### English 20-Second Summary

- The project asks whether malicious deletion choices can amplify approximation error in graph unlearning.
- The key finding is a family-level vulnerability spectrum.
- GNNDelete is most fragile, GIF is comparatively stable, and GraphEraser behaves differently in the tested settings.
- Exact retraining is the key control that separates node importance from mechanism-induced error.
- IM-v4 shows that adversarial deletion selection is practically feasible.

### 中文 20 秒总结

- 我的项目研究的是：恶意删除选择是否会放大 graph unlearning 中的 approximation error。
- 关键发现是不同 method family 存在明显 vulnerability spectrum。
- 在当前测试设定下，GNNDelete 最脆弱，GIF 相对稳定，GraphEraser 表现不同。
- exact retraining 是最关键的对照，用来区分节点重要性和机制误差。
- IM-v4 说明 adversarial deletion selection 在实践中是可行的。

### If You Need To Answer Very Safely

- `In the tested settings, the result is clear.`
- `I would separate the empirical finding from the broader theoretical claim.`
- `The exact retrain control is the key reason I can make that attribution.`
- `I do not claim universality, only a strong pattern within the completed scope.`

### 如果你想答得特别稳

- `在当前测试设定下，这个结果是明确的。`
- `我会把经验发现和更广义的理论结论区分开。`
- `我之所以能做这个归因，关键就在于 exact retrain 对照。`
- `我不主张普适性，只主张在已完成范围内存在一个很强的模式。`
