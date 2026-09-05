# AAGU-012 · EXP · X4 退化分解与副作用分析

Block ID: `AAGU-012`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

Stable locator: `.workblock/items/AAGU-012/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

承接 X4 对 GU 主结果的解释：分析选集差异与实际损伤的关系，区分删除后的重训练变化和 GU 相对重训练的差异，并按已批准指标观察保留节点、hop 与预测行为的副作用。

### 本次增量

在同一 AAGU-012 编号下，将原 GraphRevoker 独立补缺任务改登记为 Phase 2 的 X4 退化分解与副作用分析。消费 AAGU-030 明确的比较与输出表，以及 X3/AAGU-011 已收集核验的 original/GU/Retrain、Selection 和节点级输出，优先离线复用已有产物形成科研分析。

原表 SUPP 的 overlap-vs-damage 关联分析必须保留。退化分解、collateral/hop、预测差异按已有专题与 030 对齐后的定义落实；不因分区名称自动增加未经批准的控制实验或指标。GraphRevoker 回到 X3 的 GU 方法维度，不再单独作为本项名称或验收对象。

027 拥有其登记范围内的 collateral 证据生产/收集，010 拥有其汇总字段能力；本项拥有科研比较和解释，不重复承担它们的运行或修复。只有数据、请求、模型、输出与指标身份匹配时才复用相关证据；输出缺失时明确交回生产任务补齐，不在 Metrics 中隐式重训练。

### 核心验收

- 每项 X4 分析对应 030 批准的比较、控制、指标输入和具体 X3/其他匹配产物；不混用历史数据或不匹配的 split、seed、Selection。
- 完成原表的选集重合度—攻击损伤关联分析，明确匹配键、比较范围、逐 seed 值、缺失及局限；重合度不直接替代攻击效果结论。
- 对同一评价集合和协议，报告原模型、匹配 Retrain 与 GU 的性能变化；若采用 P0−Pu=(P0−Pr)+(Pr−Pu)，保留符号及两项分量，明确它是描述性分解，不能自动解释为因果贡献。
- 根据批准范围形成 retained/hop/collateral/预测行为等比较图表；结合节点级差异解释聚合指标。输出缺失时标明未验证，不补造结果或隐式增加运行。
- 交付可复跑的离线分析、输入引用清单与配对 REPORT.md / REPORT.html，用户能接受、返工或拒绝具体科研解释。012 的完成不以重跑一整套 GU 矩阵为目标。

## Orchestration contract

- Class: `EXP`
- Priority: `P1`；Phase 2，X4。
- Source anchor: 原 GraphRevoker replacement Todo 的稳定编号；2026-09-06 用户要求 011/012 按 X3/X4 改登记。
- Dependencies: AAGU-030（分析定义与覆盖）、AAGU-011（匹配的主结果及节点级输出）。012 对 011 的依赖表示消费 X3 产物，不表示旧 replacement 队列的先后位置。
- 本项不是 AAGU-013 代理迁移的默认前置；代理实验依赖其自身分组配置与匹配参照，不因曾与旧 012 相邻而等待 X4。
- AAGU-031 不依赖本项，当前 Phase 1 继续优先。
- Fact owner: 本 WorkItem 拥有 X4 分析与验收范围；科学定义由 030 对齐的 DocMap 专题拥有。X4 是分区别名，AAGU-012 是稳定 WorkItem 身份。

## Confirmed acceptance contract

- Route: `formal`.
- Primary surface: `research evidence`.
- Minimum evidence: 批准的分析表、核验且身份匹配的输入、逐项比较/缺失记录、可复跑分析和解释边界。
- Confirmation source: 用户要求“把它俩重新注册……注册成 X3、X4 这种，就不应该叫 replacement”。本次沿用原编号修改当前合同。
- Decision owner: 用户；完成验证后走正式研究验收。
- Report size: 配对 Markdown/HTML。

## Boundaries

- 本轮仅改登记、Phase 和相关依赖，保持 registered / not claimed，不运行分析或 GPU 作业。
- 后续以 block-workflow 在 linked worktree Claim 同一 AAGU-012，消费核验输出做本地分析；新增正式运行在其生产范围中明确登记，不从分析脚本隐式启动。
- 历史修复证据保留原语义，不改名为新的研究结果；不修改不可变 Cache V2 Artifact。

## Sources and handoff

- [完整实验表](../AAGU-030/WORKITEM.md)、[X3 主矩阵](../AAGU-011/WORKITEM.md)、[原实验清单](../../../self/dashboard/config_inventory.csv)。
- [Collateral 证据生产](../AAGU-027/WORKITEM.md)、[汇总字段能力](../AAGU-010/WORKITEM.md)。
- 使用 block-workflow 重新读取并 Claim AAGU-012；执行任务标题为 `AAGU-012 · X4 退化分解与副作用分析`，按本合同提交精确候选和正式验收报告。

## Status history

- 2026-08-26: registered from the prominent GraphRevoker experiment Todo.
- 2026-09-06：按用户要求保留 AAGU-012 编号，改登记为 X4 退化分解与副作用分析。原 GraphRevoker 独立 replacement 定位被取代，GraphRevoker 回归 X3 方法维度；保留原登记历史。未 Claim、执行或验收。
