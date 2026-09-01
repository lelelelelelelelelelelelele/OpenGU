---
title: 图遗忘攻击研究阶段进展汇报
date: 2026-08-26
status: ready-to-submit
audience: advisor
author: 刘丞毓
coverage: after 2026-07-22 meeting to 2026-08-26
---

# 图遗忘攻击研究阶段进展汇报

**汇报人：** 刘丞毓<br>
**覆盖区间：** 2026 年 7 月 22 日会议后至 2026 年 8 月 26 日<br>
**文档性质：** 导师书面阶段汇报

## 核心判断

7 月 22 日会议之后没有新增一套完整 formal matrix，因此本次不以“新增了多少实验结果”为主线。更准确的阶段进展有三部分：第一，重新审计既有 IF 实验后，确认 153-cell 矩阵应被解释为 **L1 surrogate-transfer / engineering screen**，而不是严格的 target-direct white-box 实验；第二，从论文投稿和评审中明确了研究问题、证据标准与主张边界；第三，把这些收获转化为一条先建立 white-box reference、再验证 surrogate transfer、最后重写论文的最小计划。

## 1. IF 的代理（surrogate）实验：旧结果应如何重新解释

### 1.1 关键变化不是多跑了一组结果，而是修正了实验身份

7 月 22 日会议时，项目已经完成 17 selectors × 3 datasets × 3 seeds 的 GNNDelete 矩阵，共 153/153 个 GU cells 和 612/612 个四文件产物。会后审计发现，selector 由 GateGCN（hidden=16，200 epochs）产生，而 GU target 是 OpenGU GCN（hidden=64，100 epochs）；二者的模型状态也没有被证明完全相同。同时，旧配置名保留了 `r=0.05`，实际每格却固定删除 `k=7` 个节点。

因此，这组实验不能再被称为“IF 直接作用于同一个 victim checkpoint 的严格白盒比较”。更准确的定位是：攻击者在一个相关 GCN surrogate 上生成删除选集，再把选集迁移到另一个 GCN target 上执行 GNNDelete。这个修正没有增加新数字，但改变了旧数字能够回答的问题。

| 可以回答 | 不能回答 |
|---|---|
| IF 排名在相关 GCN 模型之间是否具有一定迁移性 | 某 IF selector 在同一 victim checkpoint 上是否优于 random/degree |
| cheap proxy 是否能复现 expensive reference 的选集排序 | 旧 `k=7` 是否代表真实 1%/5% 删除预算 |
| surrogate 选集进入真实 GU 后是否仍呈现条件性效果 | PubMed 的旧 null regime 是否具有普遍性 |

### 1.2 旧矩阵仍然留下了三个有价值的观察

1. **代理逼近本身是可行的。** `p_graph` 与 `gt_full` 的选集排名 Spearman 相关系数为 0.984，说明较便宜的 proxy 可以较好复现昂贵 reference 的排序。
2. **fidelity 不等于攻击效果。** D reference/proxy 组相对 random 的 pooled 增量约为 +0.99 个百分点，但 degree 的平均增量为 +2.30 个百分点；估得更像 IF reference，并不自动意味着造成更大的 GU 退化。
3. **效果具有条件性。** IF 信号主要由 Cora 驱动，跨数据集并不稳定；尤其 PubMed 的旧结果受到 `k=7` 预算过小的限制，不能继续作为“所有 selector 都无效”的强证据。

这使论文中的 IF 故事从“寻找普遍最强的 selector”转向两个更清楚的问题：IF 排名能否跨模型迁移，以及这种迁移能保留多少真实 GU 攻击效果。

### 1.3 已形成两组代理迁移实验设计，但尚未产生正式结果

| 实验组 | 迁移关系 | 主要问题 |
|---|---|---|
| Group 1：GCN surrogate | GCN selector → GAT / GIN victim + GNNDelete | 常见 GCN surrogate 的选集与攻击效果能否跨 backbone 保留 |
| Group 2：SGC analytical surrogate | SGC selector → GCN / GAT / GIN victim + GNNDelete | 更易分析的 SGC 是否能成为稳定、可解释的 IF surrogate |

每个 victim 都需要自己的 target-direct white-box reference，同时保留 random 和 degree。比较必须固定 dataset、split、candidate pool、删除预算和 victim checkpoint，只改变 selector 的来源。该两组方案已经形成研究设计和证据合同，但尚未运行正式 GPU matrix，因此本次不能报告新的迁移比例或攻击效果。

## 2. 从论文投稿与评审中获得了什么

NeurIPS 投稿收到三位评审，评分分别为 1、2、3。评分并不理想，但反馈并非认为研究问题没有价值；三位评审都在不同程度上认可“战略性删除不同于随机删除”这一问题或核心经验观察。真正阻碍论文的是证据一致性、威胁模型和主张强度没有和实验覆盖对齐。

| 评审暴露的问题 | 研究上的收获 | 下一版处理方式 |
|---|---|---|
| Table 2/3、Figure 5 与附录数字不一致 | 数字来源和实验身份是论文可信度的一部分 | 建立 paper-number ledger，只从 accepted evidence 回填 |
| L0/L1/L2 与现实删除 API 边界不清 | white-box、surrogate transfer 与 black-box 必须分开回答 | 明确 checkpoint 可见性、selector 来源和查询权限 |
| “普遍更强”“architectural immunity”等表述过强 | 当前结果更支持条件性漏洞，而不是单一方法冠军 | 主线调整为 adversarial GU audit 与 Vulnerability Fingerprint |
| Retrain Gap、预测变化和 utility drop 混用 | 不同指标回答不同问题，不能相互替代 | 固定定义、方向和可引用边界，避免由单指标推出机制结论 |

论文带来的最大收获是：本项目真正有价值的部分不一定是提出一个在所有数据集上获胜的新 selector，而是建立一套能够区分攻击者权限、selector 目标、GU operator 和数据 regime 的系统性审计框架。IF 可以作为机制探针和可迁移攻击信号来研究；degree 则必须作为强控制组，而不是被弱化为简单 baseline。

## 3. 下一阶段计划

下一阶段不直接扩展大矩阵，而是按“先定义、再建立 reference、最后验证迁移”的顺序推进。

### 3.1 立即完成的基础工作

1. **统一 Dataset/Split 权威入口。** 固定 processed profile、split、candidate pool、budget 与 Recipe 身份，消除同名配置实际使用不同数据或删除数的风险。
2. **明确 IF 科学目标。** 区分 predictive influence、graph-deletion influence 与 GU-operator vulnerability，之后再决定保留哪些代表 selector。
3. **完成 target-direct 与设备 gate。** 同一 victim checkpoint 同时服务于 selector 和 GNNDelete，并验证本地、Git、SSH、GPU 与正式数据身份一致。

### 3.2 最小实验路径

| 阶段 | 最小动作 | 继续扩展的条件 |
|---|---|---|
| A. Target-direct reference | Cora 单 seed、1%/5% budget，比较 random、degree 和少量代表性 IF/D-GIF | 结果身份完整，配对结果可重复，且能够改变论文判断 |
| B. Surrogate transfer gate | 分别运行 GCN→GAT/GIN 与 SGC→GCN/GAT/GIN 的最小 registered gate | 同时报选集 overlap、原始 GU outcome 与相对 white-box reference 的配对差值 |
| C. 有条件扩矩阵 | 增加 seeds、datasets，必要时再加 GU family | 至少两个 regime 出现稳定信号；否则停止扩展并报告负结果 |

### 3.3 同步推进论文重写

- 将 contribution 从“普遍更强的 IF selector”收缩为“战略性删除的系统审计、代理迁移边界与条件性漏洞图谱”；
- 为所有表格和图建立来源账本，旧 TracIn、D-GIF、GraphRevoker 和 Retrain Gap 数字未通过新证据链前不进入重投稿；
- 分开报告 selection fidelity、transferability 和 downstream GU damage，不再用一种指标替代另一种结论。

## 4. 希望导师确认的三个问题

1. 是否同意把 IF 部分从“方法优越性”调整为“target-direct reference + surrogate transfer”的问题设置？
2. 是否同意先做最小 target-direct gate，再进入两组 surrogate 实验，而不是立即扩充数据集和 backbone？
3. 是否接受论文主线转向 adversarial GU audit 与 Vulnerability Fingerprint，并把 degree 固定为强控制组？

## 一句话总结

这段时间的进展不在于新增了一张完整结果表，而在于把旧 IF 矩阵重新放回正确的 surrogate-transfer 语境，从投稿反馈中明确论文真正缺少的证据，并据此形成了可执行的下一轮实验和写作路线。

## 证据入口

- 7 月 22 日会议基线：`report/progress/2026-07-22_if-cluster-discussion/REPORT.md`
- 旧矩阵身份复核与 target-direct 准备：`reports/target_direct_selection_PREPARATION_REPORT.md`
- 两组 E7 代理迁移设计：`E:\project\OpenGU-DocMap\10_实验矩阵\24_E7代理选集迁移实验计划.md`
- NeurIPS 评审汇总：`self/neurips_2026_submission21636_reviews.md`
- 当前执行线：`self/dashboard/WORKPLAN.md`
- D-GIF 标签边界修复：`.workblock/items/AAGU-018/WORKITEM.md`
