# Self Workspace Index

> Status: active
> Role: `self/` 主入口；定义 thesis 研究工作区的当前入口、文档权威性和阅读路径。
> Use this when: 你要快速判断“现在该看什么”“哪些结论已经稳定”“方法论和阶段报告分别放在哪”。
> See also: `thesis_transition_memo.md`, `../report/paper/stage_report_2026-02-27.md`, `../report/0417_5003report/main_report/msc_project_report.md`

## 1. Workspace Roles

- `self/`: 长期维护的研究控制中心。放方法论、研究逻辑、假说、thesis 方向与计划骨架。
- `report/`: 阶段性输出空间。放组会报告、课程报告、答辩材料、阶段总结。
- `results/`: 证据产物空间。放实验输出、relative/collateral 结果、统计表和缓存。

这三个目录的关系是：

- `self/` 解释“为什么做、怎么做、下一步做什么”
- `report/` 解释“某个阶段已经写成什么结论”
- `results/` 保存“这些结论对应的直接实验产物”

## 2. Fast Path

如果你只有 5-10 分钟，按下面顺序读：

1. [thesis_transition_memo.md](thesis_transition_memo.md)
   当前 thesis 线的承上启下文档。说明已稳定结论、未解机制问题、可检验假说和双候选 proposed 方向。
2. [../report/0417_5003report/main_report/msc_project_report.md](../report/0417_5003report/main_report/msc_project_report.md)
   2026-04 的 EE5003 最终课程报告，代表已经封口的课程 deliverable。
3. [../report/paper/stage_report_2026-02-27.md](../report/paper/stage_report_2026-02-27.md)
   2026-02 的阶段报告，代表中期实验与图表资产的里程碑。

## 3. Deep Path

如果你要继续 thesis 研究，建议按这个顺序深入：

1. `thesis_transition_memo.md`
2. `PROJECT_MASTER_CONTEXT.md`
3. `flow.md`
4. `plan_flow_v2_delta.md`
5. `generalization_experiment_checklist.md`
6. `paper_library_synthesis_2026-02-16.md`

说明：

- 第 1 步决定当前 thesis 方向和问题边界。
- 第 2-4 步提供方法、指标和实现流程的主参考。
- 第 5 步提供 2026-02 阶段的实验覆盖与结果盘点。
- 第 6 步提供文献证据与 reviewer-style 研究机会图。

## 4. Canonical Docs

当前应该持续维护的核心文档只有这几份：

- `README.md`
  `self/` 总入口和导航。
- `thesis_transition_memo.md`
  thesis 线的当前研究议程。
- `flow.md`
  方法与实现流程参考。
- `plan_flow_v2_delta.md`
  v2 指标、归因框架和实验设计补丁层。

其余文件仍然保留，但默认不再与以上文档争夺“当前主文档”的位置。

## 5. External Anchors

这些文件不在 `self/`，但构成当前研究链条的重要锚点：

- [../report/paper/stage_report_2026-02-27.md](../report/paper/stage_report_2026-02-27.md)
  2026-02 阶段里程碑，总结 950 runs、图表资产和当时的下一步判断。
- [../report/0417_5003report/main_report/msc_project_report.md](../report/0417_5003report/main_report/msc_project_report.md)
  2026-04 最终课程报告，是课程 deliverable 的正式终点。
- [../report/0417_5003report/ppt/final_15min_script.md](../report/0417_5003report/ppt/final_15min_script.md)
  2026-04 最终答辩口径，代表 oral framing。
- [../results/README.md](../results/README.md)
  结果目录说明。

## 6. Self Inventory

| File | Status | Role | Notes |
|------|--------|------|-------|
| `README.md` | active | `self/` 主入口 | 当前阅读入口 |
| `thesis_transition_memo.md` | active | thesis 过渡文档 | 当前研究议程与假说 |
| `PROJECT_MASTER_CONTEXT.md` | reference | 项目总背景与早期统一口径 | 仍有价值，但 thesis 当前方向以 `thesis_transition_memo.md` 为准 |
| `flow.md` | reference | 方法与流程主参考 | 保留为实现/指标入口 |
| `plan_flow_v2_delta.md` | reference | v2 增量补丁 | 用于理解归因、collateral、统计检验升级 |
| `generalization_experiment_checklist.md` | reference | 2026-02 实验覆盖与完成度仪表盘 | 绑定阶段证据，不是当前主计划 |
| `experiment_params.md` | reference | 旧实验参数备忘 | 用于复现实验设定 |
| `analysis_phase_a.md` | historical | 早期单阶段分析 memo | 可追溯早期 mechanism intuition |
| `宏观plan.md` | historical | 早期长期规划 | 反映项目起始设计，不代表当前 thesis 议程 |
| `GU代码综述_2026-02-16.md` | reference | 代码实现综述 | 适合回查 repo 架构与方法位置 |
| `paper_library_synthesis_2026-02-16.md` | reference | 文献综合与 reviewer 视角材料 | 仍是写作与研究机会的重要背景 |
| `generalization_experiment_checklist.md.bak` | excluded backup | 备份文件 | 保留但不维护，不应作为阅读入口 |

## 7. Non-Markdown Assets

- `datasets.png`
  目录内图像素材，非核心文档，不参与当前文档链条。

## 8. Maintenance Rules

- 以后新增长期研究逻辑、thesis 假说或方法论文档，优先放到 `self/`。
- 以后新增阶段汇报、课程汇报、答辩材料，放到 `report/`。
- 以后新增实验输出、缓存和统计表，放到 `results/`。
- 如果某份旧文档不再代表当前方向，不删除；优先加状态头并在这里更新其定位。
