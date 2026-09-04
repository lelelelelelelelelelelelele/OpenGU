# AAGU-005 · SyncMate 跨项目可行性与正确性检验

Block ID: `AAGU-005`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

Stable locator: `.workblock/items/AAGU-005/WORKITEM.md`

Acceptance Route: `practical`

Execution topology: `parallel`

> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

检验 SyncMate 作为跨项目复用的远程实验工具是否可行、行为是否正确，以及怎样在实际工作中发挥清晰作用。通用能力包括远程连接、会话与任务执行、实验进度监控、结果回传与校验；每个项目通过自己的配置文件和 Adapter 提供实验入口、参数、进度与产物含义。实验只在远程运行，本机按需承担控制、监控、结果收集和分析。

### 本次增量

以当前 Core、项目 Adapter 和实际接入为基线，检验“项目配置与任务定义 → 远程连接与运行准备 → 提交与执行 → 进度监控 → 结果回传与完整性校验 → 交给项目分析和验收”的完整工作链。以 OpenGU 为实际消费场景，并用最小的非 OpenGU 配置与 Adapter 样例检查复用边界，判断更换项目时哪些内容只需配置、哪些需要 Adapter，是否必须修改通用 Core。

交付可复核的成功路径、关键失败路径和分层结论，区分已有且可用的能力、项目接入问题、工具实现缺陷与尚未验证的能力，并据此给出最小修复范围。安装文档冲突、某个解释器缺包等作为具体问题核对归属，不用它们替代工具整体检验；本机不具备训练环境不构成远程实验不可行的证据。产品化投入取舍可作为检验后的建议，不再是本 Block 的主要验收对象。

### 核心验收

- 可行性：通过一条最小实际远程工作链，证明项目配置可以驱动任务执行、监控和结果回传，使用者能判断当前阶段与下一步；代码存在、旧 smoke 或单纯 SSH 连通不能替代本次完整链路证据。
- 正确性：任务与配置、代码版本、远程会话或进程、运行回执和返回产物相互对应；进度能追溯到实际运行观察并标明时间，回传文件完整且校验一致，不将过期快照或其他任务产物算作当前结果。
- 失败行为：对配置或运行身份不匹配、任务失败、缺失或损坏产物等关键场景，能定位失败阶段、保留原因并指出下一步，不输出虚假的成功、完整或已验收状态。
- 跨项目复用：OpenGU 场景与最小非 OpenGU Adapter 样例说明同一 Core 如何消费项目配置、执行入口、进度与产物约定；项目科研逻辑不写入通用 Core。样例验证与真实第二项目接入的证明范围明确区分。
- 人能依据配对报告判断工具在哪些环节已可用、哪些需要修复或补充验证，并决定接受或返工本次检验。执行完成、回传校验通过和科研结果被接受分别表达。

## Confirmed acceptance contract

- Route: `practical`
- Confirmation source: 2026-09-05 用户确认 005 正式定义为 SyncMate 工具的可行性与正确性检验，包含实际工作链，并明确实验仅在远程运行、通用能力通过项目配置与 Adapter 跨项目复用。
- Primary surface: `tool feasibility / correctness / remote workflow integration`
- Minimum real evidence: 当前能力与职责清单、最小实际远程工作链回执和产物校验、关键失败路径观察、OpenGU 与最小非 OpenGU Adapter 的复用检查，以及按 Core/Adapter/设备接入归属的问题和最小修复建议。未观测环节必须明确保留，不以测试替代实际链路证据。
- Post-candidate decision: AAGU 项目负责人和 SyncMate owner 根据证据明确接受或返工本次检验；需要产品实现时再确定具体 SM 工作项范围。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: SyncMate 的 Core/Project/Device 分工与远程实验生命周期；项目配置和 Adapter 拥有实验参数、执行入口、进度解释、产物格式及科研验收语义，Core 拥有通用连接、运行控制、监控、回传和校验机制。
- Orchestration: 保留 SUPPORT、P3 与 `AAGU-005 depends_on AAGU-001`；编排事实由 WORKPLAN 拥有，本次不改变依赖或当前主推进线。
- Related work: AAGU-002 负责正式 Device Readiness 试点与验收；005 可复用其已有证据或指出缺口，不替代其正式决定。保留 SM-003 作为相关 SyncMate 工作项入口，其现有合同须在后续承接时另行核对，不随本次修改自动改变或启动。
- Remote execution mechanism: 远程会话与进程管理是通用能力的一部分；具体采用 tmux 或既有 runner 的方式在检验时核对，不把会话存在等同于实验进度或成功。

## Runtime and authorization boundaries

- 本次只修改同一 Block 的定义，保持 registered / not claimed；不启动验证任务、远程操作、环境安装、产品实现或科研实验，也不预填报告和证据。
- 后续 Run 使用独立 Git worktree，目标为登记时实际观察到的 canonical `refs/heads/main`；Git 工作位置不改变实验仅在远程执行的边界。本机控制/收集端只检查它自身需要的工具依赖，不要求具备远程训练环境。
- 实际链路检验优先采用预先定义的最小远程验证任务与独立临时产物，不产生新的科研结论。若必须使用科研实验才能回答某项问题，需消费该实验独立批准的合同及正式运行条件，不能借工具检验绕过实验授权。
- 本 Block 拥有检验、证据和最小修复建议；发现需修改 SyncMate 产品、安装方式或项目 Adapter 时，按实际责任归属承接到明确的实现范围，不扩展成整套发布、升级或恢复系统。保留真实数据、缓存、运行结果和其他项目文件。

## Restart and next action

在后续执行任务中使用 `block-workflow` Claim 同一 locator，重读本 Human Surface、当前 Core/Adapter 与设备事实，先确定最小远程验证任务、产物和失败场景，再完成可行性与正确性检验。提供配对报告后停在人类验收，不把检验通过自动投影为科研接受或产品实现授权。

## Status history

- 既有登记：以 SyncMate 产品化取舍为目标，保持 registered / not claimed。
- 2026-09-05：按用户确认，将同一 AAGU-005 重定义为跨项目可行性与正确性检验，纳入完整实际远程工作链、项目配置与 Adapter 复用边界；补齐执行字段，保留编号、状态、practical 路线和编排依赖。未 Claim、执行或形成候选证据。
