# AAGU-024 · 未 Claim WorkItems 升级为 2.1 Human Surface

Block ID: `AAGU-024`
Item Version: 2.1
Item Type: `Block`
Work Type: `DOCS/PROTOCOL`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-024/WORKITEM.md`

## Human Surface

### 核心意图

让尚未开始的 AAGU Blocks 在未来 Claim 前就能被人直接理解：每份 Record 先清楚说明为什么做、这次做什么、怎样验收，同时保留实验依赖、运行边界和研究证据事实，不再要求人从旧版长篇合同中重建核心意图。

### 本次增量

只把 14 个 `registered / 未 Claim` Blocks（AAGU-001、002、003、005、007、008、010、011、012、013、014、020、021、022）原位升级为 WorkItem 2.1：从各自现有事实提炼唯一且首个 Human Surface，移除旧权威入口冲突，并保留原 ID、状态、依赖、执行/授权边界、来源和历史。已 accepted、awaiting_acceptance、ongoing 的 Blocks 与 Todos 均不修改。

### 核心验收

1. 14 个成员全部声明 `Item Version: 2.1`，首个二级区块均为唯一 `## Human Surface`，且只含顺序正确、内容清楚的 `核心意图 / 本次增量 / 核心验收`；当前 2.1 validator 全部通过。
2. 每份 Human Surface 都来自该 Record 与 live WORKPLAN 的已有事实，完整自然语言可直接理解；不引入新的实验结论、依赖、数据身份、formal evidence 或执行授权。
3. 成员的 ID、当前状态、关系、priority、运行/SSH/GPU 边界和历史保持语义一致；AAGU-004、006、009、018、019、015–017、023 以及所有 live Claims 的内容与摘要均零变化。
4. COMP-042 的 exact candidate 能在 Campaign / Graph 中同时加载旧协议与这些 2.1 成员：旧版只显示真实机器事实，2.1 展示逐字 Human Surface；真实截图进入 paired Report。
5. 迁移候选只包含 owner Record、14 个成员 Record、paired Report/evidence 与必要的确定性验证，不运行实验、不 SSH、不改 WORKPLAN 生成投影、不 Claim 任何成员。

## Source

- Protocol authority: WB-228 精确候选 `bbb299034a58438c691a3f7a5380b005cfe80219` 与已预切换安装的 2.1 validators。
- Project authority: canonical AAGU WorkItems、runtime Claims 和 `self/dashboard/WORKPLAN.md`；WorkItem 负责生命周期合同，WORKPLAN 负责当前编排。
- Display dependency: COMP-042 的 mixed-version Campaign / Graph exact candidate，只用于只读验收投影，不成为 AAGU 状态或关系权威。
- User decision: 已完成、awaiting_acceptance、ongoing 不更新；只升级尚未执行的 AAGU Blocks，并推进到候选后人工验收。

## Scope

- Migration members: AAGU-001、002、003、005、007、008、010、011、012、013、014、020、021、022。
- 对每个成员原位增加 2.1 Human Surface，处理与 `## Intent` / `## Acceptance Brief` 并行的旧权威标题，但保留仍有价值的详细事实。
- 确定性结构校验、逐项语义审计、状态/关系/Claim 零变化 guard、COMP-042 只读 Campaign 视觉验收。
- paired Markdown/HTML Report 与 evidence 截图、before/after 摘要和验证记录。

## Non-goals

- 不修改 AAGU-004、006、009、018、019、015、016、017、023。
- 不 Claim 或执行 14 个成员，不更改依赖，不运行 CPU/GPU 实验，不访问 SSH，不生成研究结论。
- 不手工修改 WORKPLAN 的生成投影，不改 Cache V2、AutoReport、results 或 DocMap。
- 本 Block 不 closeout WB-228 或 COMP-042，不 Merge / Apply AAGU-024，不 push、不 cleanup。

## Acceptance contract

- Route: `formal`。
- Primary surface: COMP-042 mixed-version Campaign / Graph 中的 AAGU 2.1 Human Surface，加上逐项 Record before/after 审计。
- Minimum real evidence: 14/14 协议 validator、字段/状态/关系/Claim 不变清单、代表性旧版与 2.1 同图截图、paired Report 和 Git candidate path audit。
- Decision owner: 用户。
- Post-candidate decision: 形成 clean exact candidate 后停在 `awaiting acceptance`，由用户阅读 Campaign 与 Report 决定接受或返工。
- Report size: paired Markdown/HTML Report，evidence 保存截图与确定性验证输出。

## Registration boundary

只注册 AAGU-024；不 Claim、不升级成员、不执行实验、不修改外部项目。

