# AAGU-030 · 本轮完整实验表与配置映射

Block ID: `AAGU-030`
Item Version: 2.1
Item Type: Block
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-030/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

将原 HTML 实验进度大表承载的实验类别和组合整理为本轮全量重跑的完整实验表，明确每类实验比较什么、使用哪些配置、交付哪些分析以及由哪个执行 Block 承接。保留原科学类别，复用 015 已接受的 Selector 专题；新增建议与已确认范围分别列明。

### 本次增量

以 `self/dashboard/config_inventory.csv` 及其 HTML、已接受的 001 合同和 015 方案为来源，完成原条目到本轮实验类别、模块配置、分析输出与执行 Block 的逐项映射。A5 分为“删除比例”和“数据集”。核对八分区草稿中的遗漏、范围扩张和坐标变化，校正实验总览与大图；主矩阵、SUPP、A3、A5、A6 和 ARXIV 均有明确归属。后来的迁移、专门计时等专题单独说明来源。运行状态与历史状态分开，历史完成数不冒充本轮完成。

本项归下一研究阶段。当前阶段优先运行并分析 015 已确定的 Selector 实验；它不等待本项完成。本项同时核对既有 007/008/011/012/013/014/027 等执行 Block：可复用、需按用户已确认范围调整、独立 replacement 已无必要、或尚缺承接，各有清楚说明；不为已有任务重复注册一套编号。

### 核心验收

- 原始 29 条配置和当前清单后增条目逐项可追溯；每项归属、是否保留为科研实验/诊断、原矩阵坐标及本轮配置映射明确。重复配置视图和异质 SUPP 计数不得算成唯一运行数。
- 每类表明确问题、比较对象、控制变量、数据/模型/方法/seed/预算、指标输入、预期输出和解释边界。复用 015 的既定 Q1–Q4，不将其三数据集、三 seed、两预算和 17 Selector 强套全部原实验。
- 原表及已批准专题对应真实 Dataset/Split、Selector、GU/Retrain、Metrics 配置引用；通过现有消费者的解析与无写入矩阵展开。仍待决定或尚无实现支持的项明确显示，不伪装成 execution-ready。
- 完整表、八分区大图、HTML 展示和执行 Block 映射一致；A5 两子项清楚，CiteSeer/GIN/20%/alpha 网格等已发现遗漏有明确处置。新增科学建议单列，不静默改变已批准设计。
- 交付配对 Markdown/HTML 报告，用户能逐类核对覆盖和后续执行责任。验收以表格、配置与覆盖核对为准，不要求运行科研矩阵。

## Execution contract

- Class: DOCS/CONFIG；Priority: P1；Route: formal；Decision owner: 用户。
- 本次用户已确认“本轮完整实验表与配置映射”四项交付，并要求按 Phase 分组、当前优先启动 015 对应阶段。
- 使用 linked worktree 独立整理；Apply target 由 allocator 读取当前 canonical checkout 的实际 symbolic ref。
- Prerequisites: AAGU-001、AAGU-015、AAGU-026、AAGU-028 已接受的合同、配置与独立输出能力。
- 015 后续 Selector 执行不是本项的完成前置，本项也不是其运行前置。Stage S 结果可在可用时作为后续建议的来源，不重写其事先定义。
- 科学说明由 OpenGU DocMap 拥有；配置由 experiments/configs 拥有；Phase、优先级、执行 Block 映射由 WORKPLAN/Graph 拥有。生成物只从所属事实源重建。
- 不自动执行正式实验、改变已有 WorkItem 生命周期、清除历史数据或修改 Cache V2；新执行任务只在已有范围与用户授权内形成。

## Source and scope

- [原实验清单](../../../self/dashboard/config_inventory.csv)、[原 HTML 大表](../../../self/dashboard/config_inventory.html)。
- [001 合同](../AAGU-001/WORKITEM.md)、[015 方案](../AAGU-015/EXPERIMENT_PLAN.md)。
- [实验总览](E:/project/OpenGU-DocMap/10_实验矩阵/10_实验-框架总览.md) 当前含 agent 误读后写入的八分区草稿，不能作为改变原科学设计的授权。
- 011 的独立 CiteSeer 补缺任务按用户决定已不再必要，CiteSeer 原实验范围仍须保留在全量重跑表中；本项先形成可审阅的任务处置与覆盖映射。

## Restart and next action

使用 block-workflow 读取同一 WorkItem、现有来源和 live Claim 后实施本项表格与配置映射。当前阶段优先级以 WORKPLAN 为准，不因该计划工作延迟 015 已确定范围的实际运行与分析。

## Status history

- 2026-09-06：用户确认独立整理完整实验表，并要求归入新的后续 Phase；登记本项，未 Claim、实施或运行实验。
