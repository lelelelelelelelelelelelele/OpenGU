# 论文复审入口：采用关系与本轮更新

2026-10-25 · 状态：准备中，尚未冻结复审输入，正文整合尚未完成。

本入口纳入作者本轮的图表取舍、正文解读与恢复要求。先对齐 **DocMap 当前章节、旧 Overleaf 正文、XLX v8/v9 候选**，再冻结明确版本交给「论文攻坚 -- XLX」。旧 review 保留其历史输入和判断，不自动沿用为当前论文评分。

## 本轮明确采用的边界

- 论文 **Fig. 4 继续采用 EXP-080 的 CiteSeer 两排比例图**：上排 accuracy，下排与同请求 Retrain 的预测不一致率。两排是同组实验的互补读数，不拆成两项独立发现。
- EXP-079 按需承担分析、Q3支撑、反例和附录。已有图不自动获得主图位置；当前正文已有引用也须在采用目录中逐项确认。
- **原 Q1–Q3 的整体研究价值与局部 B 案例分别评价。** 不因 B 的确认结果或控制缺口，直接否定或接受全部 Q1–Q3；也不因整体范围广而免除 B 的证据要求。
- 079/e79r5、e79r6、080、086/087/088 分别保留数据、seed、split、方法实现、执行身份与科学采用边界。图表的论文采用不等于科学接受状态变更。
- XLX v8/v9 与其重组方案均为候选。本轮不自动批准其替代原 Q1–Q3 或恢复排除主张。

## 三套材料的阅读与采用关系

| 顺序 | 入口 | 本轮角色与待办 |
| --- | --- | --- |
| 1 | [DocMap论文主页面](E:/project/OpenGU-DocMap/40_论文写作/40_论文写作.md)、[结果章节](E:/project/OpenGU-DocMap/40_论文写作/06_结果.md) | 当前写作导航和原Q1–Q3候选正文；逐项核对历史数字、方法限制及证据批次，不整体自动采用 |
| 2 | [Overleaf主文件](../../overleaf/main.tex)、[Results源码](../../overleaf/sections/results.tex) | 当前落盘投稿文本，需与DocMap及本轮解读逐段对照；整篇整合尚未完成 |
| 3 | [Fig. 4采用记录](../../figures/exp080-ratio-response-20261025/REPORT.md)（[HTML](../../figures/exp080-ratio-response-20261025/REPORT.html)） | 两排比例图、英文段落、配对数值、展示边界与源表的共同入口 |
| 4 | [079响应模式报告](E:/project/OpenGU/GULib-master/self/research/analyses/EXP-079/e79r5/RESPONSE_PATTERN_REPORT.md) | 分析、Q3支撑与反例；使用主线现存入口，原response-figure-study工作树路径已不存在 |
| 5 | [XLX v8](E:/project/OpenGU/GULib-master/paper_writing/outline/OUTLINE.v8.md)、[候选v9](C:/Users/ADMIN/.codex/worktrees/paper-v1-figures/OpenGU/GULib-master/paper_writing/outline/OUTLINE.v9.md) | 比较候选结构、段落与图表组织；不设为默认采用稿 |
| 6 | [第三轮旧审稿输入](E:/project/OpenGU/GULib-master/paper_writing/review/2026-10-24-round3/REVIEW_INPUTS.json)、[旧pre-v1判断](C:/Users/ADMIN/.codex/worktrees/paper-v1-figures/OpenGU/GULib-master/paper_writing/review/2026-10-25-pre-v1/REPORT.md) | 历史异议与处置背景，不能充当新一轮完整输入 |
| 7 | [EXP-087](E:/project/OpenGU/GULib-master/self/research/experiments/EXP-087.json)、[EXP-088](E:/project/OpenGU/GULib-master/self/research/experiments/EXP-088.json) | 沿真实回执刷新各阶段执行与接纳，文字概述可能滞后；不把聊天暂停当作作业停止 |

## Fig. 3/4 的更新怎样进入复审

上一版交接误将XLX图册的 `F03_endpoint_response` / `F04_truth_partition` 对应为论文Fig. 3/4。本轮纠正，**图册文件编号不能代替论文编号**。

当前 Results 源码已有 `fig:response-pattern-profiles`，引用079/e79r5的PubMed请求响应图；这是现存正文引用，最终采用与主图位置仍按本轮目录确认。EXP-080比例图由 `fig:exp080-budget-response` 标识，继续承担作者确认的论文Fig. 4。最终编号以采用稿编译结果为准。

Fig. 4 正文保留两个分析层面：第一，R-point请求的效用损伤在多种GU上是否延续，以及预算曲线怎样呈现这种效应；第二，部分GU维持较高accuracy，却未复现同请求Retrain的响应，并有更大的预测分歧。先读完整曲线，再用33%/50%端点量化，不能只用一个高预算点替代轨迹。

相对Random的有符号分歧增量是单独补充图，不替换Fig. 4原始D。预算差D(50%)−D(10%)与同预算D(selector)−D(Random)分别解释。真值分解、两评价图和C&S控制按明确解释缺口选用，不自动成为主图或独立贡献。

所有文字继续保留三seed/固定split、均值±样本SD、历史实现和GCN参照的范围；GIF/IDEA重合不算两份独立证据。含旧GNNDelete或历史MEGU的图表行需按其具体生产身份标注采用限制，不因归档图已进入正文而追认有效性。accuracy平稳不证明没有更新，D增大不单独证明隐私泄露或遗忘失败。

## 对 reviewer 的新要求

1. 对原Q1、Q2、Q3逐问评价，再评价三问的整体论证价值；另列B案例的支持、反例、未确认与控制缺口。
2. 每条意见标明所读文本、图、证据批次与定位；区分“原稿遗漏但已有证据”“补充后仍缺证据”“主张不成立或需收窄”。
3. 给出旧意见→本轮修改→维持/修正理由的对照，不因旧包漏写而重复判定已完成工作缺失，也不预设新评分。
4. 理论、实验、分析复审使用同一冻结包。历史root三风格模拟不冒充新独立复审；本次入口更新本身不是启动复审或写作放行。

## 冻结前还需完成什么

| 待办 | 完成条件 | 当前状态 |
| --- | --- | --- |
| 逐段采用目录 | 对DocMap、Overleaf、v8/v9逐段标记保留、改写、待证据、移附录或排除，并确定唯一采用文本 | 待完成 |
| 图表与证据对齐 | 文字—论文图标识—源表—配置/方法/执行身份一致，明确079与B的职责 | 已记录选择，整合待完成 |
| 工作区修改保存 | 按来源形成可恢复检查点，不丢弃或整体合并其他任务修改 | 见本次状态核对 |
| 复审快照 | 保存采用稿、所用DocMap章节、图与必要证据入口，生成精确SHA和文件哈希清单 | 尚未冻结；当前清单只记录入口来源 |
| 交给XLX | 明确包版本及尚缺科学证据，再按有效授权恢复 | 本次未发送或唤醒 |

## 工作区状态核对

下表是本次只读Git核对、入口编辑之前的状态；原准备清单中“全为0 tracked”与其Git读取错误、残留文字不一致，不能作为现值。未提交修改不会被自动清理。

| 工作区 | HEAD / 分支 | 实际观察 |
| --- | --- | --- |
| main | c555e63a / main | 无tracked修改；已有本交接的两个untracked文件 |
| paper-v1-figures | cc6f35bb / codex/paper-v1-figures | 8项tracked修改：两个绘图源码、CAPTIONS、F01三种格式、MANIFEST、references.bib；归属原任务，未改动 |
| response-figure-study | 不适用 | 原路径不存在；079报告可从主线读取 |
| round4-integration | 117687cb / codex/round4-gu-profile-inputs | 无tracked修改 |
| DocMap | d6bfdbb / main | 无tracked修改 |

本次未连接SSH核对GPU状态。第二节点续跑仍按SM-027→AAGU-121的有效依赖与授权处理，与本地正文对齐分别推进。

## 来源、恢复指令与交付边界

- [用户提供的复审准备清单](C:/Users/ADMIN/.codex/visualizations/2026/10/24/01a16ea7-c8f2-7ba2-bbf1-06bd2e7649f2/review-preparation-20261025/REPORT.md)保留为原始准备记录。本入口整合其选择，并更正本次实际发现的失效路径和状态差异。
- [更新后的session交接与四段恢复指令](E:/project/OpenGU/GULib-master/.claude/handoffs/2026-10-25-062327-paper-session-restart.md)供合作者接手，采用关系以本入口为准。
- [来源与状态清单](SOURCE_INVENTORY.json)记录入口文件哈希和Git观察，不是已经冻结的论文审稿包；改变采用文件后需重新生成。

本次仅更新复审入口、两处写作导航与交接，生成同内容HTML并检查链接。未整合论文正文、改科学决定、提交/合并分支、部署、启动实验或向XLX发消息。
