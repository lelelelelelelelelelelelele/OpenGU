# Docs 文档入口

`docs/` 保存工程合同、实现说明和对应版本的设计/验收记录。
当前研究定义在 [OpenGU DocMap](../../../OpenGU-DocMap/_文档地图.md)，任务与依赖在
[WORKPLAN](../self/dashboard/WORKPLAN.md)，生命周期在 [WorkItems](../.workblock/items/)。
研究背景和阶段材料可从 [self 入口](../self/README.md) 查找。

## 按问题找文档

| 问题 | 文档 | 使用边界 |
|---|---|---|
| 实验配置各部分负责什么 | [实验合同](experiment_contract/README.md)、[参数清单](experiment_contract/PARAMETERS.md) | 合同定义不等于所有字段都已在当前运行时实现；查看对应 WorkItem 与代码 |
| 当前执行路径如何使用缓存 | [通用执行缓存](generic_cache_v2.md) | 与实际消费者及实现版本一起核对 |
| Cache V2 的身份与层次为何这样设计 | [Dataset 解耦](cache_v2_dataset_decoupling_DESIGN.md)、[正式 Artifact](cache_v2_gate2_formal_artifacts_DESIGN.md)、[比较层](cache_v2_gate3_comparison_harness_DESIGN.md) | 设计背景；有更新时以当前合同与已落地实现为准 |
| AutoReport 事件和投影如何分工 | [AutoReport V3](auto_report_v3_DESIGN.md) | 事件是审计原件，Markdown/HTML 是可重建投影 |
| 哪份 agent 指导生效 | [根 AGENTS](../AGENTS.md)、[实验 AGENTS](../experiments/AGENTS.md)、[dashboard AGENTS](../self/dashboard/AGENTS.md) | 直接读取现行规则，不从旧审计报告执行迁移步骤 |

## 历史记录如何使用

- `*_ACCEPTANCE_REPORT.md`：记录某个候选和范围当时的验收证据。判断当前完成状态时回到对应 WorkItem；不要将旧通过结果套到后来修改的版本。
- `*_PROGRESS_REPORT.md`、`*_REPORT.md`：对应日期或阶段的观察。Git 审计中的分支、路径与远端状态需要重新核对。
- [plans/](plans/)：早期课程报告、图表与答辩制作方案；成果已在 [EE5003 报告目录](../report/progress/2026-04-17_EE5003-report/) 落地，不能再按这些计划重开制作任务。
- [superpowers/plans/](superpowers/plans/)、[superpowers/specs/](superpowers/specs/)：历史实施与设计材料；执行范围由当前 WorkItem 决定。
- [历史 Phase B runbook](history/phase_b_202605_runbooks.md)：历史操作记录，不是当前运行入口。
- [AGENTS 拆分审计](claude_agents_decomposition_ACCEPTANCE_REPORT.md)：2026-07 的迁移依据；仓库级迁移已合入，dashboard 的现行规则已归入其 AGENTS.md。
- [旧 self 文档盘点](self_documentation_iteration_PLAN.md)：保留当时的逐文档判断；其中的阶段状态与执行限制不作为今天的指令。

## 维护原则

先确定文档的使用者和事实归属，再决定更新、合并或删除。当前说明应直接指向唯一来源；
已经被消费的临时工作分支不承担长期归档职责。历史报告只在仍有证据或解释价值时保留。
改变路径或删除文件前检查引用；改变科学结论前核对对应代码、配置与实验产物。

本轮已修复入口和 AGENTS 归属。`self/limitations.md`、指标目录与 Paper Liabilities Map
中的旧数字、缺陷状态和论文行号仍需逐项对照当前研究证据后裁定，不能靠目录整理宣称已验证。
