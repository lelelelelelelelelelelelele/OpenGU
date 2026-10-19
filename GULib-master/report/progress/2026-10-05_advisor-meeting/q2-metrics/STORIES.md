# 问题 2：同一删除请求，为什么得到不同的 GU 响应？

2026-10-18 · 三张叙事图候选 · EXP-079/e79r5 · GCN 选点 · 十训练 seed

**问题 2 同时问两件事：同一 selector 对实际效用造成什么变化；这些变化与同请求 Retrain 的效用和预测行为有什么关系。** 2026-10-19 更新：先看所有四类请求的原始效用，再读相对 Random 与 Retrain 的差值。各图共用同一批请求，不是独立实验。

## 图 1：先看四种请求后模型本身的准确率

![PubMed：Random、Degree、R-point、D-full 的原始准确率](primary_pubmed_accuracy.png)

**横轴是四类独立请求，纵轴是准确率原值，没有减 Random，也没有减 Retrain。** 实心圆是 GU，空心菱形是同 selector 的 Retrain，按 Random 对 Random、Degree 对 Degree、R-point 对 R-point、D-full 对 D-full 叠加。同色短线连接两个均值，不表示时间轨迹。GU 的灰色虚线是自己的删除前平均准确率（Before）。浅色点为十个训练 seed，大点及误差线为均值和点态 95% t 区间。前五面板共享纵轴，灰色 GraphRevoker 诊断面板使用独立纵轴；重复画出的 Retrain 仍是同一份参照。

PubMed 的原值说明，不能把“比 Retrain 的变化小”说成“selector 对 GU 都无效”：GIF/IDEA 的 Random 为 88.58%，D-full 为 87.65%；GraphEraser 的 Random 为 87.17%，R-point 为 86.18%。MEGU 变化更小，GNNDelete 则出现方向不同的响应。是否有明确方向仍需同 seed 配对区间；区间跨零不代表等效。运行稳定性要另外看 seed 变异，不能由 selector 均值变化小推断。

**[完整一级指标图页：三数据集 × 准确率、交叉熵、分类 AUC](PRIMARY.html)。** 同时提供原值、seed SD 和不依赖 Retrain 的 Selected − Random 配对表。GIF/IDEA 以 GIF 代表（准确率相同，CE 差小于 1e-8，AUC 差小于 0.001 pp），完整原值均保留。

这批十 seed 实验包含上述四类请求，不能代表所有选点算法。Selector 可用于检查 GU 是否保留同请求 Retrain 的效用响应；仅凭响应不同不能认定 GU 没有反映真实变化或遗忘失败。

### 同一张图的两个分析角度：scale 与 pattern

**保留原来的三个主问题。** Scale 与 pattern 加入问题 2 的实验分析，不替换研究主线，也不单独宣布为新的核心问题；当前按 selector 对齐的 GU/Retrain 原值图同时承载这两个角度。

- **Scale（变化幅度）：** 在各方法实际性能水平和自身 Before 的背景下，看删除后下降多少、不同请求之间相差多少，以及同请求 GU 与 Retrain 相差多少。幅度较小不能单独推出方法更好。
- **Pattern（响应关系）：** 固定数据集和选点来源，看同一个 GU 对不同 selector 的分组、排序和变化方向，再与 Retrain 对照。重点是哪些请求表现相近、哪些引起不同响应，以及这些关系是否在其他条件下保留；不只看最大 drop 或平均性能。

以当前 PubMed 均值图为例，Retrain 呈现 Random、Degree 接近且高于两个 IF 请求的关系；GraphEraser 保留了这一分组及两种 IF 的顺序；GIF/IDEA 保留了大体分组，但两种 IF 的均值顺序相反；MEGU 的请求间变化较小，GNNDelete 则是 Random 最低。这些是同一张图的描述性读法，不能用整体下降大小替代，也不能直接推广为整个算法类别的性质。

跨数据集、选点来源和 seed 的检验属于这些分析的证据要求。均值接近时排序容易翻转，因此应结合配对不确定性，优先讨论可重复的分组与方向；当前均值图并未单独验证完整排序或稳定性。

**IM 并非没做。** EXP-011 已有三档 IM（RR-4096、RR-16384、RR-65536），覆盖三数据集、六 GU 和 Retrain，但只有三个训练 seed，每个 seed 有三次 IM 选点重复。当前图来自未纳入 IM 的 EXP-079 十 seed 矩阵，所以不能直接把 IM 当作十 seed 数据拼进来。[原汇报](../REPORT.html)第 3 节保留了 IM 与 IF、Degree、PageRank、Random 的比较。

### 原图留作参照诊断：大的 gap 还需结合初始水平理解

**方法审计更新：[原论文与当前实现对照](METHOD_AUDIT.html)。图中 GraphRevoker 实际是 GPA + optimal 配置版，当前 adapter 未接入论文的 contrastive 聚合模块，不能用于完整 GraphRevoker 的方法优劣结论。** [Before 来源核验](BEFORE_AUDIT.html)确认本批 Cora 没有误取单 shard；但数值能复算不代表完整方法实现正确。图和原数值保留为诊断，不以探索性聚合对照替换正式结果。

![删除前、Random、D-full 与同请求 Retrain 的准确率](story01_retrain_context.png)

**一句话发现：同样看到很大的 GU–Retrain gap，实际背景可能不同；只画 gap 会隐藏各方法起点和随机删除后的表现。**

以 Cora 的 D-full / GCN 请求为例，GNNDelete 从 89.91% 降到 69.48%，Random 后是 76.99%，同请求 Retrain 是 89.19%。因此这里既有方法对随机删除的下降，也有 D-full 的额外影响。GraphRevoker 的情况不同：初始准确率已经是 70.68%，D-full 后为 65.74%。其 23.45 pp gap 不能全部称为该请求新造成的损伤。

**反例与范围。** CiteSeer 中多数端点接近，PubMed 的方法差别也不像 Cora 那样悬殊。分片方法与完整 GCN 起点不同；这里的 Retrain 是共同的 full-graph 参照，不是每个 GU 架构各自精确重训。因此图 1 是参照诊断，不是严格控制架构后的近似误差排名，也没有识别性能差异的因果机制。

**可用于正文的表述。** “The same retraining gap can arise against substantially different starting performance. Reporting the pre-deletion model and random-request outcome alongside the matched retraining endpoint distinguishes overall performance differences from the additional effect of targeted selection.”

## 图 2：同一 selector 的 Retrain 效应，不能直接当作各 GU 的损伤

![两个 selector 在六种 GU 上的额外准确率损失及 Retrain 参照](story02_selector_across_gu.png)

**一句话发现：固定请求后，各 GU 对定向选择的额外响应不同，而且这种关系随数据集改变。** 每幅面板内，各 GU 使用同一批选集，橙/蓝点是 GU 相对 Random 的额外损失 A_M；绿线是相同请求在 Retrain 上的额外损失 A_R。正值表示比 Random 更差。绿色阴影和横线属于同一个共享参照，不能算作六次复现。

Cora 的 D-full 请求在 Retrain 上额外损失 0.71 pp，到了 GNNDelete 是 7.51 pp，而 MEGU 为 0.05 pp。PubMed 则提供反向例子：同一 D-full 在 Retrain 上额外损失 1.61 pp，GNNDelete 的均值却为 -0.46 pp。这表明“对 Retrain 有影响”不能直接换算成“对所有 GU 都有同样影响”。负均值的证据强弱仍应读区间。

为检验“放大或削弱”，计算逐训练 seed 的 E=A_M−A_R，再给配对区间，不能靠两组误差线是否重叠判断。下表保留该量及反例；完整六 GU、两策略、三数据集结果见 CSV。

| 条件 | ΔU [95% CI] | Retrain ΔU [95% CI] | E [95% CI] | Δ分歧 [95% CI] |
| --- | --- | --- | --- | --- |
| Cora / gt_full / GNNDelete | +7.51 [+4.80, +10.21] | +0.71 [+0.32, +1.11] | +6.80 [+4.06, +9.53] | +10.34 [+7.14, +13.54] |
| Cora / gt_full / GraphRevoker | +2.90 [+0.18, +5.63] | +0.71 [+0.32, +1.11] | +2.19 [-0.53, +4.91] | +2.65 [+0.17, +5.14] |
| PubMed / gt_full / GNNDelete | -0.46 [-1.30, +0.39] | +1.61 [+1.13, +2.09] | -2.07 [-3.04, -1.10] | +2.93 [+0.53, +5.33] |
| CiteSeer / r_point / GIF | -0.38 [-0.72, -0.03] | -0.34 [-0.96, +0.29] | -0.04 [-0.67, +0.59] | +2.42 [+1.22, +3.62] |
| CiteSeer / r_point / GraphEraser | -0.71 [-1.13, -0.28] | -0.34 [-0.96, +0.29] | -0.37 [-1.19, +0.45] | -0.89 [-1.88, +0.10] |

**反例与范围。** CiteSeer 的效用差异小，不能硬排出稳定的 GU 易受影响次序。这一图研究同 selector 在不同 GU 上的响应，不声称 D-full/R-point 优于所有策略；Degree 和完整策略范围仍由[完整指标页](REPORT.html)与 EXP-011 支撑。GIF/IDEA 数值重合，不作为独立验证。不同 GU 的训练和架构也不同，这里比较的是整个已配置系统的响应。

**可用于正文的表述。** “A request's effect on exact retraining does not determine its utility effect across approximate unlearning systems. Under matched deletion requests, the additional loss varies across GU methods and can change direction across datasets.”

## 图 3：同一 selector 的效用和行为响应，也不必同步

![相对 Random 的准确率损失与 GU–Retrain 分歧增量](story03_utility_behavior.png)

**一句话发现：某些条件下准确率提高了，与同请求 Retrain 的预测分歧却增加；另一些 GU 并不表现出这种分离。** 横轴是额外准确率损失，纵轴是额外预测分歧。左上象限表示准确率比 Random 更高、但分歧也更大；右上表示两者同时增加。零轴只是比较基准，不是遗忘正确性的阈值。

CiteSeer 的 GIF / R-point 是清楚的例子：ΔU=-0.38 [-0.72, -0.03] pp，而 Δ分歧=+2.42 [+1.22, +3.62] pp。MEGU 的平均效用也改善、平均分歧增加，不过效用区间应单独阅读。GraphEraser 则是反例：同一 R-point 下 ΔU=-0.71 [-1.13, -0.28] pp，Δ分歧=-0.89 [-1.88, +0.10] pp；它不支持“所有 GU 的分歧都会上升”。

**解释边界。** GraphEraser 的分歧变化区间跨零，因此它提供方向不同的均值，尚不能确认分歧降低。这说明单独按准确率给请求排序会遗漏预测行为变化；它不证明这种分歧就是隐私风险或遗忘失败。也尚未区分 GU 自己改变了哪些节点、Retrain 改变了哪些节点。若后续追问原因，需要核对两侧相对初始模型的逐节点变化，不能用这张散点图补写机制。横纵误差线分别为点态区间，不是二维联合置信域；这里是探索性分析。

**可用于正文的表述。** “Utility preservation does not imply preservation of prediction agreement with retraining. For the same selector, the relationship between these two responses is method-dependent: improved accuracy can coexist with increased disagreement, while other GU methods show mean decreases in both quantities.”

## 怎样放进论文

### 待补充的两个方向（2026-10-19）

- **大数据集：ogbn-arxiv。** 本次口述“Archive”按既有候选记录；检验当前请求响应现象能否在更大数据条件下保留，并沿用按 selector 对齐的 GU/Retrain 原值展示。
- **新增 GU 方法。** 补充现有方法之外的覆盖，检验观察是否依赖少数实现；具体新增方法名单待定。

已并入 [dataset 与 GU 扩充计划](../../../../../../OpenGU-DocMap/30_评审与汇报/2026-10-15_dataset与GU扩充计划_REPORT.html)及 TODO R5。沿用“论文大体完成后再推进”；本次只记录，不启动实验，也不作为已完成的覆盖或结论。

### 图表顺序

先用图 1 的原始效用比较回答“各 selector 之后模型实际怎样”，再用图 2 的差值总结同请求在不同 GU 上的响应；图 3 支撑“效用与行为不总一致”的发现。旧四端点图仅作为参照诊断保留，不能凭它解释 gap 的因果来源。完整一级指标和差值都保留，成稿时再按版面选择。

这三条经验发现可以由同一 framework 串起来：它固定请求、提供 Random 和 Retrain 参照，让不同 GU 的响应及其差异可比较。无需把三个观察强行解释成同一个机制。

## 证据、图源和复现

- [图 1 PDF](story01_retrain_context.pdf) · [图 2 PDF](story02_selector_across_gu.pdf) · [图 3 PDF](story03_utility_behavior.pdf)。
- [完整逐 seed 数据](story_seed.csv) · [完整均值与区间](story_summary.csv) · [生成脚本](build_stories.py) · [核验记录](story_validation.json)。
- [指标与原值完整页](REPORT.html) · [返回导师汇报](../REPORT.html)。
- 来源为经本轮核验的 2,520 份 metrics.json 派生表；本图使用 GCN 选点的两个 selector、三数据集、六 GU，共 360 个 GU 条件，另用同 seed 的 Random 平均值和同请求 Retrain。已检查每个 dataset/seed/selector 的 selection_id 和 Retrain output 在六 GU 间一致。
- 十个训练 seed，固定 split 2024、10% 训练候选节点删除、原图评估；Random 三请求先在 seed 内平均。点态 95% t 区间未作全矩阵多重比较校正，案例为事后探索性选例。未新增 GPU 运行，未改变科学接受状态。
