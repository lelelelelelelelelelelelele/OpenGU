# AAGU-024 · 未 Claim WorkItems 升级为 2.1 Human Surface

Block ID: `AAGU-024`
Item Version: 2.1
Item Type: `Block`
Work Type: `DOCS/PROTOCOL`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/main`

> Git baseline：`be0dd0fad09458d6111ab2e422c8c8bdd3d90bfc`

> Source branch：`refs/heads/codex/aagu-024-workitem-2-1`

> Remote target：`origin refs/heads/main`
当前状态: `accepted`
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

## Work and verification

- 2026-09-01：同一 stable locator 已由任务 `AAGU-024 · Upgrade unclaimed WorkItems to 2.1` Claim；Git baseline 为 `be0dd0fad09458d6111ab2e422c8c8bdd3d90bfc`，source branch 为 `refs/heads/codex/aagu-024-workitem-2-1`。
- 2026-09-01：14 个 scope members 已原位完成结构迁移；当前 2.1 Human Surface validator 为 `14/14 PASS`。
- 2026-09-01：去掉迁移专属的 `Item Version` 与旧/新 human section 后，14 个成员其余非空行均与 baseline 逐字一致；9 个禁止修改 WorkItems、`self/dashboard/WORKPLAN.md`、既有 AAGU-004/006/009 Claims 均保持不变，成员 Claim 数为 0。
- 2026-09-01：AAGU-010 的成员 Record 仍写 `P1 after accepted collateral evidence`，live WORKPLAN 仍投影为 `P0 / AAGU-009`；这是 baseline 已存在的只读差异，本次迁移未选择或改写任一权威事实。
- 2026-09-01：结构子块尝试通过当前 installed `run_git.py finish` 形成 checkpoint 时，被 `unrelated-dirty-state` 安全停止；该调用只执行 1 个 `git status`，没有 stage 或 commit。只读诊断确认 nested project 的 porcelain `-z` 返回 Git-root-relative `GULib-master/...`，而 finish 的 owned paths 按 project-relative `.workblock/...` 比较；等待主任务提供已验证的 2.1 合法入口，不手工绕过或修改 installed Skill。
- 2026-09-01：主任务随后以可逆 hotfix 更新 installed `run_git.py`，最终安装 SHA-256 为 `BC2B64DD7EC8F2ABC68500D0598BC1D09009D25841F4DFD48AC81A876AB272C0`；它把 nested project 的 status paths 归一为 project-relative，让 candidate HEAD 读取向上定位真实 `.git`，并跳过不含 `HEAD` 的空 `.git/` 标记目录。含空 `.git/` 的 nested fixture finish 仍为 3 个 Git commands，project 外 dirt guard 继续 fail-closed。原 WB-228 exact candidate `bbb2990...` 备份保存在 `C:\Users\ADMIN\.codex\skill-backups\aagu-nested-finish-pre-hotfix-bbb2990\block-workflow`。此 hotfix 尚未进入 WB-228 Git candidate，必须作为本候选的工具链边界保留，不能声称 2.1 协议候选已包含该修复。
- 2026-09-01：收到 COMP-042 exact candidate `f6832b9dec0be903d9f8d83f50ba2bc2864dfbd7` 后，以其产品代码注册 clean AAGU 临时 Git 快照；首次 `getCompanionView()` 在 AAGU-001 处返回 `Unsupported Item Type ...: Block.`。根因是产品对任何显式 Item Version 都额外要求带反引号的 Item Type，但当前 2.1 协议门禁没有这项要求，且受保护的 AAGU-006/009/019 也是显式 2.0 + `Item Type: Block`。没有改 live AAGU 或伪造 fixture；25 个 live 文件哈希均未变化。
- 2026-09-01：COMP-042 在同一 Block 修正后形成新 exact candidate `08be674abc60c9249982a1c3f341a080cd8b5121`。从 fresh registry 重新加载同一 clean AAGU snapshot，24/24 nodes、20 relations、1.0/2.0/2.1 三种版本全部成功；14 个迁移成员 Human Surface available，legacy/2.0 代表集合不显示 Human Surface/Result。
- 2026-09-01：三张真实 Windows native 截图覆盖同屏 mixed-version Campaign、AAGU-020 2.1 正例与 AAGU-004 legacy 负例；fixture 前后 clean，live 非 owner graph/WorkItems 与既有 Claims 零变化。
- 2026-09-01：paired `REPORT.md` / `REPORT.html` 已生成并通过 current Report validator；HTML 在 1280×720 与 390×844 均无横向溢出，三张证据图无断图，warning/error console 为 0。Agent 建议接受；当前决定仍由用户作出。
- 2026-09-02：用户明确接受当前迁移，并在原 integration ref 已退役后授权将 Apply target 改为 `refs/heads/main`、Remote target 改为 `origin refs/heads/main`，同时授权按项目 policy 完成本地 no-ff merge 与 ordinary push；迁移内容与既有验收证据不变。

## Human-facing result

- Markdown: `.workblock/items/AAGU-024/REPORT.md`
- HTML: `http://127.0.0.1:18768/.workblock/items/AAGU-024/REPORT.html`
- Evidence: `.workblock/items/AAGU-024/evidence/`
- Decision owner: 用户。
- Current projection: awaiting acceptance；不代表已接受、已 Apply 或已 closeout。

## Status history

- `accepted`（2026-09-02T06:33:47.7129248+08:00）：User 基于 User explicitly accepted AAGU-024, retargeted Apply to main, and authorized the policy push to origin/main. 接受当前已验证候选。
