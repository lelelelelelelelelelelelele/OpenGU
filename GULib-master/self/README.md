# Self 文档入口

`self/` 保存研究过程材料、历史判断和 dashboard。当前研究定义与实验计划在
[OpenGU DocMap](../../../OpenGU-DocMap/_文档地图.md)，当前任务编排在
[WORKPLAN](dashboard/WORKPLAN.md)，生命周期在 [WorkItems](../.workblock/items/)。
本页只做导航，不维护另一份研究计划或任务状态。

## 从这里开始

| 你要做什么 | 入口 | 如何使用 |
|---|---|---|
| 看下一步、优先级与依赖 | [WORKPLAN](dashboard/WORKPLAN.md) | 看当前编排；通过条目进入 WorkItem |
| 看研究问题、实验矩阵和论文论证 | [OpenGU DocMap](../../../OpenGU-DocMap/_文档地图.md) | 使用独立研究文档库的当前入口 |
| 修改 dashboard | [AGENTS.md](dashboard/AGENTS.md) | 区分手写节点、WorkItem 状态和生成视图 |
| 查代码合同与设计 | [docs 入口](../docs/README.md) | 区分合同、实现说明与历史验收报告 |
| 查正式运行及结果产物 | [results 说明](../results/README.md)、[AutoReport V3](../docs/auto_report_v3_DESIGN.md) | 按配置、代码版本和产物核对证据 |
| 查人工验证发现 | [VALIDATION_LOG](dashboard/VALIDATION_LOG.md) | 按条目日期与后续 superseded 记录阅读 |

## 按用途查研究材料

这些材料保存了各自阶段的论证与证据，不能凭其中的 `active`、`OPEN` 或旧下一步
判断当前任务。用于新结论前，要回到 DocMap、当前代码和对应实验版本核对。

| 材料 | 仍然有用的内容 | 阅读边界 |
|---|---|---|
| [评审意见](neurips_2026_submission21636_reviews.md) | 当次审稿意见与问题来源 | 当前修订安排看 DocMap / WorkItem |
| [Limitations](limitations.md) | 曾实测的限制与当时决策 | 版本相关的限制需要复核，旧 OPEN 不等于当前待办 |
| [指标目录](dashboard/METRICS_CATALOG.md)、[字段语义](dashboard/METRIC_FIELD_SEMANTICS.md) | 指标与字段解释 | 历史覆盖率、缺陷状态不替代当前证据 |
| [Paper Liabilities Map](dashboard/PAPER_LIABILITIES_MAP.md) | 2026-06-20 的证据缺口与论文行号核对 | 历史快照，不能直接套用于当前稿件 |
| [v2 方法设计](plan_flow_v2_delta.md) | 归因、collateral 与显著性设计来源 | 当前参数与方法定义看当前合同及代码 |
| [Degree 分解提案](research_path_degree_severity_decomposition.md)、[跨架构共识 idea](idea_cross_arch_consensus.md) | 候选研究思路及论证过程 | 不自动成为已采纳路线或可执行任务 |
| [Related work](related_work/NOTES.md)、[文献综合](paper_library_synthesis_2026-02-16.md) | 文献卡片与历史定位分析 | 新写作需要核对原论文与当前论证 |
| [TracIn 历史 finding](related_work/concordance/FINDING_tracin_misspecification.md) | 既往术语及方法误配的追溯 | 不作为当前正式实验完成证据 |

## 历史背景与阶段成果

- [Thesis transition memo](thesis_transition_memo.md)：2026-05 的课程报告到 thesis 过渡判断。
- [PROJECT_MASTER_CONTEXT](PROJECT_MASTER_CONTEXT.md)：项目最初的目标、方法族和实现概览。
- [flow](flow.md)、[attack flow](attack_flow.md)、[代码综述](GU代码综述_2026-02-16.md)：历史设计与代码阅读材料；函数名、路径和耗时应重新核对。
- [早期分析](analysis_phase_a.md)、[实验覆盖清单](generalization_experiment_checklist.md)、[参数备忘](experiment_params.md)、[宏观规划](宏观plan.md)：早期实验与规划记录。
- [旧 paper todo](paper_todo.md)、[冻结实验看板](dashboard/EXPERIMENT_DASHBOARD.md)、[配置清单验收](dashboard/CONFIG_INVENTORY_ACCEPTANCE.md)：对应阶段的任务或验收记录。
- [2026-02 阶段报告](../report/paper/stage_report_2026-02-27.md)、[EE5003 课程报告](../report/progress/2026-04-17_EE5003-report/main_report/msc_project_report.md)、[答辩讲稿](../report/progress/2026-04-17_EE5003-report/ppt/final_15min_script.md)：已交付的阶段成果。

## 新内容放哪里

- 当前研究问题、实验解释、矩阵与论文思考进入 OpenGU DocMap；此处通过链接引用。
- 当前任务与依赖写入 WORKPLAN；生命周期交给对应 WorkItem，不在研究笔记里另建任务事实源。
- 代码合同、实现说明进入 `docs/`；阶段汇报、课程报告与答辩成果进入 `report/`。
- 实验产物由其执行和收集流程写入 `results/`；不要通过整理文档修改实验事实。
- 旧材料只有在仍承担明确参考用途时才保留。删除或合并前核对独有内容是否已被吸收、引用是否仍有效；不能仅凭文件日期裁定。
