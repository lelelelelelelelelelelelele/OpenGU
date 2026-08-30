---
title: 2026-08-26 学长会议纪要
date: 2026-08-26
type: meeting-notes
status: recorded
author: 刘丞毓
tags: [advisor-meeting, senior-review, contribution, experiment-plan]
---

# 2026-08-26 学长会议纪要

## 1. 会议材料

本次会议使用的书面阶段材料已归档在本目录：

- [`REPORT.md`](REPORT.md)：可检索的 Markdown 版本；
- [`OpenGU_导师阶段进展汇报_2026-08-26.docx`](OpenGU_导师阶段进展汇报_2026-08-26.docx)：会议使用的 Word 版本。

这两份文件记录会前汇报口径。本纪要只记录现场实际讨论和会后要求，不反向改写会前材料。

## 2. 会议中实际讲述的内容

本次主要讲了后续实验计划，而不是新增正式结果。讨论焦点是：考察 `degree` selector 在 **10% 删除预算**下与 `top-k` 选点或排序之间的关联。

当前只记录该研究方向，不把它写成已经得到的结论。正式执行前仍需明确：

1. `10%` 的分母是全图节点、训练候选节点还是其他候选集合；
2. `top-k` 指固定排名前缀、不同预算下的排名稳定性，还是与攻击效果的关联；
3. 对照组、seed、dataset、GU method 和主要指标；
4. 结果继续扩展或停止的判定条件。

这些定义应在全量实验配置修复后冻结，并进入注册实验配置与证据链。

## 3. 学长提出的两个要求

### 3.1 一周内提供 Abstract、Introduction 和 Contribution

截止目标按会议日期后一周记录为 **2026-09-02**。三个交付物中，最优先的是先想清楚 Contribution，再据此写 Abstract 和 Introduction。

Contribution 当前有三个候选支点：

1. **代码库 / 平台贡献。** 项目构建了一套较完整的图遗忘对抗攻击代码库或实验平台。现场英文短语记录为 `The Versary Attacked`，其准确名称和含义仍需确认；在确认前不把它作为论文正式术语。
2. **核心 insight 或 decomposition。** 需要提出一个能组织结果、解释现象并区别于单纯 benchmark 的核心认识或分解。这一点尚未定稿，是本周最重要的思考任务。
3. **大规模实验验证。** 用足够广、配置一致且可追溯的实验验证方法或 insight。该点是待完成的论文证据要求，不代表当前已经拥有可直接引用的完整矩阵。

### 3.2 修复整个实验配置

需要对正式实验配置做一次全量审计和修复，而不是只修单个 YAML。至少要统一：dataset/split 身份、候选集合、删除比例与实际 `k`、selector 来源、victim checkpoint、随机种子、指标语义、产物身份以及运行入口。

修复完成前，不把新实验结果写进 Abstract、Introduction 或 Contribution 的强主张。

## 4. 会后执行顺序

1. 先写一页 Contribution memo：分别回答平台是什么、核心 insight/decomposition 是什么、实验如何验证它。
2. 根据 Contribution memo 起草 Abstract 和 Introduction，三项于 2026-09-02 前形成可评审版本。
3. 并行完成全量实验配置盘点，列出当前配置、缺陷、修复动作和验证方式。
4. 配置冻结后再注册 `degree × 10% × top-k` 的最小实验，不直接扩展完整矩阵。

## 5. 状态边界

- `degree × 10% × top-k`：会议讨论的实验计划，尚无正式结果；
- 三点 Contribution：学长提出的候选结构，尚未形成论文定稿；
- Abstract / Introduction / Contribution：一周内交付任务；
- 全量实验配置：待审计与修复，当前不能标记完成。

