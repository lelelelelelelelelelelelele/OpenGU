---
title: 评审意见与 rebuttal
created: 2026-07-09
updated: 2026-07-09
type: review-rebuttal-workbench
tags: [review, rebuttal, advisor, paper]
---

# 评审意见与 rebuttal

这里集中放 reviewer / advisor / AI review 意见，以及它们拆出来的 rebuttal 任务。执行任务同步到 [[00_动态工作台/02_TODO台账]] 和 [WORKPLAN.md](../../self/dashboard/WORKPLAN.md)。

---

## Review 材料入口

| 材料 | 位置 | 用途 |
|---|---|---|
| AI 模拟审稿 2026-06-28 | [[AI审稿_2026-06-28]] | 当前 5/10 weak reject 压力测试 |
| Draft review 2026-05-06 | [draft_review_2026-05-06.md](../../report/paper/review/draft_review_2026-05-06.md) | 初稿逻辑、overclaim、结构审查 |
| Abstract review 2026-05-04 | [abstract_review_2026-05-04.md](../../report/paper/review/abstract_review_2026-05-04.md) | 摘要数字和措辞 fact-check |
| Figure review | [figure_review.md](../../report/paper/review/figure_review.md) | 图质量和投稿可用性审查 |
| Advisor report 2026-06-16 | [advisor_report_2026-06-16.html](../../report/advisor_report_2026-06-16.html) | 导师汇报入口 |
| 0701 current status | [current-status-report.html](../../report/progress/2026-07-01_advisor-report/current-status-report.html) | 当前状态汇报 |

---

## AI 审稿拆解

| 痛点 | 审稿含义 | 对应处理 |
|---|---|---|
| 实验完成度和 claim 强度不匹配 | 主结果像 Cora-heavy audit，Citeseer/arxiv 和未完成语句会被抓 | E1 / E5 / W3 |
| 叙述过满 | `architectural immunity`、`Shard Protection`、`strictly governed` 等机制措辞偏强 | W1 / W3 |
| 统计力度偏弱 | GNNDelete 结果抓眼但方差大，headline collapse 需要对冲或加 seed | C2 / A7 / W3 |
| fingerprint 可能偏轻 | 如果只剩描述性画像，贡献感不足 | W1 / W2 / A9 / 重投 reframe 备选 |

---

## Rebuttal 必答题

1. 为什么 degree/PageRank 强不等于贡献被证伪？
   - 当前口径：贡献是 systematic audit + extreme heterogeneity + fingerprint，不是证明 IM/IF 最强。
   - 待写作：retrain gap 作为主指标，结构 selector 强作为 finding。

2. scope 是否足够？
   - 当前风险：Cora-heavy，arxiv 仍像 pilot。
   - 待补证：E1 Citeseer clean，E5 arxiv 补量。

3. GNNDelete collapse 是否统计可靠？
   - 当前风险：高方差，部分 cell 不显著。
   - 待处理：A7 或 W3 对冲措辞。

4. GraphRevoker 是否影响 6-method audit？
   - 当前风险：旧数据退化，不能洗坏数据。
   - 待处理：E4 修复 + 整 method 重跑。

---

## 写作动作

- [ ] 清掉 “Phase B.2 refresh / await H800 retrain” 这类暴露未完成的句子。
- [ ] 弱化强机制措辞，把 “immunity / strictly governed” 改成观测性、设置内表述。
- [ ] 把主叙事从 raw-F1 改成 retrain gap + heterogeneity。
- [ ] 明确 update-detection AUC，不写成标准 shadow-model MIA。
- [ ] 给 GNNDelete collapse 加方差 / n.s. 对冲。
- [ ] 把 future-work 和 current thesis 分清：rebuttal 不做重投式结构杠杆 reframe。
