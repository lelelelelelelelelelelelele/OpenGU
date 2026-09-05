# AAGU-011 · EXP · X3 GU 主矩阵与结果

Block ID: `AAGU-011`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

Stable locator: `.workblock/items/AAGU-011/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

承接 X3 的 GU 主矩阵运行与主结果，回答策略性删除是否改变图遗忘结果、不同 GU 方法和 Selector 的表现有何差异。沿用原实验大表的科学类别与已批准比较，形成完整、可复用且可审阅的研究证据。

### 本次增量

在同一 AAGU-011 编号下，将原 CiteSeer 独立补缺任务改登记为 Phase 2 的 X3 GU 主矩阵与结果。消费 AAGU-030 对原表完成的配置映射、AAGU-031 可匹配的 Selector 产物和 AAGU-007 的正式 GU gate，按最终批准矩阵执行独立 GU 与匹配的 Retrain，并收集主指标和后续 X4 所需输出。

原 CORA 主矩阵包括 GCN/GAT、六种 GU、六个策略槽位、五个训练 seed 和 5% 删除比例；准确配置及已纠正算法的映射由 030 列明，不直接复活旧错误实现。GraphRevoker 是 GU 方法维度。CiteSeer 保留在原 A5“数据集”子项的 5%/20% 范围，不因改登记而删除，也不自动扩成所有三小图的完整主矩阵。A3/A5/A6 的分析类别及执行产物归属由 030 分别映射。

015 的 Stage U 定义若纳入本轮组合，由 030 注明来源与范围；不把 015 的 17 Selector、三 seed 或两预算强套原主矩阵。复用 Selection 必须核对实际数据、模型、checkpoint、候选和预算；新增条件须形成自身匹配的选集。

### 核心验收

- 030 批准的 X3 比较逐项对应本轮配置、数据/split、训练 seed、Selection、GU/Retrain 输出和代码身份；planned/observed/failed/unavailable 明细完整，不静默缩小范围。
- 正式设备、共享 stage check 和专题 preflight 通过后按注册 launcher 运行；007 gate 仅在身份和适用范围匹配时复用，各方法仍满足自身最小验证。
- 同 Selection 的 GU 与匹配 Retrain 独立执行并保存输出；主结果报告逐 seed utility、GU–Retrain 差异、相对匹配 random 的变化及已批准指标。原始预测、mask 等输入足以供 X4 复核。
- 形成完整主表、比较图、运行/收集清单和可复用 Output/Selection 引用；历史结果不重标为本轮完成，缺失和不适用有明确原因。
- 配对 REPORT.md / REPORT.html 支持用户独立接受、返工或拒绝 X3 证据；本次改登记不代表已执行或已接受。

## Orchestration contract

- Class: `EXP`
- Priority: `P1`；Phase 2，X3。
- Source anchor: 原 CiteSeer replacement Todo 的稳定编号；2026-09-06 用户要求 011/012 按 X3/X4 改登记。
- Dependencies: AAGU-030（完整表与配置）、AAGU-031（当前阶段 Selector 证据）、AAGU-007（正式 GU gate）。001/002/026/028 的合同与运行基础从这些前置继承。
- 旧 AAGU-008 K5 anchor 不作为本项前置；AAGU-031 不依赖本项或 030，当前 Selector 阶段继续优先。
- Fact owner: 本 WorkItem 拥有 X3 执行与验收范围；科学表格由 030 对齐原清单并落在 OpenGU DocMap，最终可执行身份由对应配置/recipe 拥有。
- X4/AAGU-012 消费这里的匹配输出。X3 是分区别名，AAGU-011 仍是唯一 WorkItem 身份。

## Confirmed acceptance contract

- Route: `formal`.
- Primary surface: `research evidence`.
- Minimum evidence: 批准矩阵、真实身份、独立 GU/Retrain 产物、主指标、收集校验和范围覆盖。
- Confirmation source: 用户要求“把它俩重新注册……注册成 X3、X4 这种，就不应该叫 replacement”。本次沿用原编号改登记。
- Decision owner: 用户；完成验证后走正式研究验收。
- Report size: 配对 Markdown/HTML。

## Boundaries

- 本轮仅更新登记、Phase 和依赖；保持 registered / not claimed，不启动 GPU 作业。
- 后续以 block-workflow 读取同一 locator、最新配置与 live Claim；本地 linked worktree 维护配置与分析，正式 GPU 在 SSH 活跃检出执行并满足已落地 pinned SHA 规则。
- 保留原实验类别；新增矩阵、控制或算法建议单列。历史证据与 Cache V2 不手工删除、覆盖或改名。

## Sources and handoff

- [完整实验表](../AAGU-030/WORKITEM.md)、[原实验清单](../../../self/dashboard/config_inventory.csv)。
- [Selector 运行与分析](../AAGU-031/WORKITEM.md)、[GU gate](../AAGU-007/WORKITEM.md)、[X4 分析](../AAGU-012/WORKITEM.md)。
- 使用 block-workflow 重新读取并 Claim AAGU-011；执行任务标题为 `AAGU-011 · X3 GU 主矩阵与结果`，按本合同形成精确候选与正式验收报告。

## Status history

- 2026-08-26: registered from the prominent CiteSeer experiment Todo.
- 2026-09-06：按用户要求保留 AAGU-011 身份和原始登记历史，当前标题与合同改为 X3 GU 主矩阵与结果。原 CiteSeer 独立 replacement 定位被取代，CiteSeer 科学范围继续保留在原 A5 数据集子项。未 Claim、执行或验收。
