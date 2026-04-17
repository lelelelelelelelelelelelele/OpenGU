# 答辩高频 8 问速答版（中文）

适用场景：导师 + examiner 的学术型问答。

使用方式：每题先记住“短答版”，如果对方继续追问，再接“展开版”。

---

## 1. 你的项目最核心的问题是什么？

### 短答版
我的核心问题是：恶意用户能不能通过精心选择删除节点，利用 approximate graph unlearning 的 deletion interface，放大 approximation error，从而让保留模型性能异常下降。

### 展开版
重点不只是“删节点会不会掉点”，而是“掉点中有多少是正常删除带来的，有多少是 approximate unlearning 机制本身额外放大的”。

### 回答关键词
- adversarial deletion
- approximation error
- retained-model utility

---

## 2. 为什么这个问题重要？

### 短答版
因为 graph unlearning 本来就是为真实删除请求服务的，但很多方法依赖近似更新而不是 exact retrain，所以 deletion interface 本身可能变成攻击面。

### 展开版
如果 exact retraining 太贵，系统就会采用 approximate unlearning；但一旦是 approximation，就可能出现“删除请求被恶意利用”的问题。所以这不是单纯的合规问题，也有安全风险。

### 回答关键词
- practical deletion request
- compliance
- security surface

---

## 3. 你的主要贡献是什么？

### 短答版
我的贡献有两部分：一是经验上展示了不同 graph unlearning family 在 adversarial deletion 下存在明显 vulnerability spectrum；二是工程上搭建了一套基于 OpenGU 的可复用 adversarial audit workflow。

### 展开版
前者是 scientific finding，后者是 enabling infrastructure。也就是说，我不仅得到了结果，还把结果变成了一套可重复执行的评估流程。

### 回答关键词
- family-level comparison
- vulnerability spectrum
- reusable workflow

---

## 4. 为什么你一定要用 exact retraining 作对照？

### 短答版
因为只看删除后的性能下降，不能判断那是节点本身重要，还是 approximate unlearning 本身出了问题；exact retraining 给了我最关键的归因基线。

### 展开版
同一个 deletion set 下，如果 exact retraining 只出现很小下降，而 approximate unlearning 出现很大 collapse，那么额外那一部分就更合理地归因于 approximation-induced error，而不是节点重要性本身。

### 回答关键词
- attribution
- control
- same deletion set

---

## 5. 你怎么知道问题主要来自 approximation error，而不是删掉的节点本来就很重要？

### 短答版
因为我比较的是同一个 deletion set 下的 approximate unlearning 和 exact retraining；如果 exact retraining 没有同样大的崩塌，那么额外损失就不是节点重要性单独能解释的。

### 展开版
这是我整个方法里最核心的逻辑。节点重要性只能解释“正常应有的损失”，但解释不了 approximate 版本为什么比 exact 版本差得多。

### 回答关键词
- exact vs approximate
- intrinsic loss
- extra gap

---

## 6. 为什么你认为 GNNDelete 是最脆弱的？

### 短答版
因为在当前测试设定下，GNNDelete 持续表现出最大的 attack-over-random degradation，并且在 strongest case 中 also shows very large retrain gap 和明显 collateral damage。

### 展开版
我不是只看一个极端点，而是看多个 setting 下方向一致的 pattern。最强 case 只是说明问题最明显，但结论不是只建立在单点异常上。

### 回答关键词
- consistent pattern
- strongest case
- collateral damage

---

## 7. 为什么 GraphEraser 反而有时会变好？这个结果可信吗？

### 短答版
我认为这个结果在当前测试设定下是可信的，但解释要谨慎。一个合理解释是删除某些 bridge 或 hub 节点后，shard-local classification 反而更容易了。

### 展开版
我不会把它说成“GraphEraser 普遍鲁棒”。我只会说，在当前 datasets 和 settings 下，它没有表现出像 GNNDelete 那样的 collapse pattern，并且出现了我称为 shard protection effect 的现象。

### 回答关键词
- plausible interpretation
- shard protection effect
- not universal robustness

---

## 8. 如果继续做，最值得做的下一步是什么？

### 短答版
我认为最值得做的是两步结合：先在更大数据集上验证这个 pattern 是否还成立，再对 GNNDelete 做更细的 mechanism-level ablation。

### 展开版
因为现在我已经有了比较清楚的经验模式，下一步最有价值的不是继续堆更多小实验，而是验证 generalization，并解释为什么 GNNDelete 会在 adversarial deletion 下这么脆弱。

### 回答关键词
- larger datasets
- generalization
- GNNDelete ablation

---

## 一页记忆版

### 你只要先记住这 8 句

1. 我的问题是：恶意删除选择会不会放大 approximate unlearning 的误差。
2. 这个问题重要，因为 deletion interface 可能不仅是合规功能，也是攻击面。
3. 我的贡献是：发现 family-level vulnerability spectrum，并搭建了可复用 workflow。
4. exact retraining 是关键对照，因为它决定了我能不能做正确归因。
5. 额外损失如果显著大于 exact retraining，就更像 approximation error，而不是节点重要性。
6. GNNDelete 最脆弱，因为它在多个 setting 下都表现出最明显的 attack-over-random degradation。
7. GraphEraser 的“变好”可以解释，但我只做有边界的结论，不说它普适鲁棒。
8. 下一步最值得做的是：更大数据集验证 + GNNDelete 机制级 ablation。

---

## 遇到刁钻追问时的万能稳答句

- 在本报告测试设定下，这个结果是明确的。
- 我这里区分经验结论和更广义的理论结论。
- 我不把这个现象表述成普适性结论。
- 这也正是我加入 exact retrain control 的原因。
- 我认为更稳妥的说法是：这是一个强 pattern，但仍然有 scope boundary。
