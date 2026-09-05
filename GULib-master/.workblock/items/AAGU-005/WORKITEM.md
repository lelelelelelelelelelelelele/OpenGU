# AAGU-005 · SyncMate 的 OpenGU 接入与联调

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

让 OpenGU 通过自己的配置、Adapter 和静态配方使用 SyncMate，完成可追溯的任务提交、执行和产物返回。AAGU-005 与 SM-005 组成同一条跨项目工作链：本 Block 拥有 OpenGU 消费端，SM-005 拥有通用 Core；各自在本项目内修改、验证、提交和验收，共享联调证据。

### 本次增量

沿用同一 AAGU-005，接收此前 SM-005 实测和修复过程中产生的 OpenGU 消费端工作，负责后续 Adapter、静态配方、实验入口与运行上下文接入、产物路径和声明、Core 依赖身份检查及相邻配置、文档、测试。先核对已交付提交及证据，再在本 Block 的独立 OpenGU linked worktree 继续本侧必要修改；不重复实现已落地代码。

与 SM-005 共享绑定双方版本、配置、job 和产物的同一组证据。已有 Degree、B-Hutch、D-full 真实运行、冷热缓存和自动回传结果按代码与接口差异判断能否复用；不能把旧接口证据自动视作新接口实测。AAGU-015 的配置、Selector 输出和复用检查保持其独立接受范围。

### 核心验收

- OpenGU 的配置、Adapter、静态配方和入口与声明的 Core 接口、精确依赖身份一致；任务定义不能携带任意命令、路径或环境表达式。
- 已批准的产物声明与消费者实际输出位置一致，分数、排名、Selection 等内容保留各自身份；错误身份、产物缺失和返回冲突不产生虚假成功。执行、完整性校验和科研接受分别表达。
- 本侧针对性代码检查通过，既有证据逐项说明适用版本和复用理由；新的接口尚未真实运行时明确记录未测边界。当前用户要求仅验证代码，不以新增 GPU 实验作为本轮必需步骤，也不声称新接口已经真实联调通过。
- OpenGU 源码由 AAGU-005 在独立 linked worktree 修改；SyncMate Core 由 SM-005 修改。共用文件先协调具体代码段，保留其他任务变化。015 的实验设计与 028 的 Retrain/Metrics 实现不在此重做。
- 配对 Markdown/HTML 报告说明本侧增量、代码检查、可复用实测证据及未测边界，由用户独立接受或返工。SM-005 完成不自动完成本 Block，本 Block 完成也不自动接受 SM-005 或科研实验。

## Confirmed acceptance contract

- Route: `practical`；Primary surface: `OpenGU consumer integration / code correctness`。
- Decision owner: 用户，以 OpenGU 项目负责人身份决定本侧结果；SM-005 另行拥有通用工具验收。
- Confirmation source: 2026-09-06 用户明确这是跨 Project 协同，要求使用 AAGU-005 与 SM-005，让它们分别做两边的修改。按两个现有 Block 协作承接，保留各自仓库、编号、locator 和独立验收。
- Minimum evidence: 经原执行任务确认的提交与接口交接、本侧针对性代码检查、精确 Core 依赖身份、已有实测证据的适用性判断、明确失败行为和未测边界。
- Latest runtime constraint: SM-005 执行任务已转达用户当前要求 GPU 暂不可恢复，“你就测试代码正确就行”；本轮不等待 GPU、不发起新实验。未来真实联调须沿用当时有效的项目运行条件与具体授权。
- Report size: Verify 后形成同目录 Markdown/HTML 报告；本次职责登记不预填结果。
- Post-candidate decision: 各项目分别接受和 Closeout；接收历史提交不是对后续未验证候选的提前接受，职责划分不扩大部署或科研运行范围。

## Context and relations

- Partner: [SM-005 · SyncMate 跨项目可行性与正确性检验](E:/project/SyncMate/.workblock/items/SM-005/WORKITEM.md)。SM-005 拥有通用连接、任务控制、状态、回传、校验及公共接口；AAGU-005 拥有这些接口在 OpenGU 的具体消费。
- Orchestration: 保留 SUPPORT、P3 与 `AAGU-005 depends_on AAGU-001`；WORKPLAN 拥有编排。本次不改变 028 主推进线，不添加两项目互相等待的循环依赖。
- Coordination: 两边可独立推进；集成前绑定双方精确提交、Core 制品与接口合同。接口缺陷由代码所属项目修复，另一侧核验，不跨仓库代改。
- Related work: 026 已有模块化消费者是接入基础；015 提供当前阶段配置和 Selector 证据；028 拥有 Retrain/Metrics 修复并阻挡整轮正式研究运行。002 Device Readiness、007 等科研验收及 SM-003 产品化合同保持独立。
- Evidence: 引用 SM-005 原始报告和证据，标明 owner、受测提交及复用理由，不移动、改写或复制成新运行结果。

## Received handoff · 2026-09-06

原执行任务已确认停止 OpenGU 写入、提交与后续远端安装，且没有运行中的 OpenGU 命令。交接时 OpenGU 实现已提交并普通 push，工作区干净；不是待搬移的未提交补丁。此处为来源检查点，接手时重读 Git 和 Claim。

- OpenGU 基线 `e27425e6ad8ba8dd34663098d759d83ab4804023`，交付 tip `e8f23a94dc7d753283442cadb1b45d8c1962234e`。
- 范围：`scripts/syncmate/` 的 Adapter、配方、新增 `opengu_layout.py`、依赖清单与文档；`experiments/modular_execution.py`、`experiments/syncmate_atomic_stage.py`、原子配置说明；`docs/modular_experiments.md` 及两份对应测试。
- 接口：`syncmate.run-handoff/v1`、`adapter.result_roots()`、配方 `run_identity`、共享 `modular_output_path`，stage 执行前核对 queue receipt 的 `output_contract`。新静态配方 `opengu-sm005-d-full-handoff-v1` 尚未提交运行。
- Core 0.4.0 来源 `5dd378cb5a732d47108e58299df462320648bda8`；wheel SHA-256 `a6ecf6de385d80538b1983c49f5dee8048f4787847084fee6cadc3c761a435d2`。原任务报告双端已安装并读回，OpenGU 依赖清单为 60 文件；接手时按既有证据核验，不重放安装。
- 原任务报告 Core 91 项、OpenGU 入口/原子配方/依赖/modular consumers 221 项通过；OpenGU 日志在 [原检查日志](E:/project/SyncMate/.workblock/runtime/sm005-output-contract/opengu-installed-tests.txt)。本次登记仅接收该事实，执行任务仍须核对证据适用性。
- SSH OpenGU 当时仍为旧基线，尚未同步新消费端；已准备的本地安装 preflight 不等于部署完成。015 的 Closeout 若先完成代码同步，接手者应复用读回，不重复执行。
- 原任务已调整本地 ignored `.syncmate/device.yaml`；连接事实与既有可信索引保持，快照位于 SyncMate runtime 的 `sm005-output-contract`。不凭该设备快照推导科研接受。

## Runtime and authorization boundaries

- 使用 `block-workflow` Claim 同一 locator，采用 `parallel` linked worktree；具体 source branch、baseline、owner 和工作区在 Claim 时绑定。本次登记不代替 Claim。
- 写入只限 OpenGU 接入范围。`experiments/modular_execution.py` 只涉及必要运行上下文与产物路径接入；科研算法、Selector、GU、Retrain、Metrics 语义不因接入改变。涉及 028 正在修改的共同文件，先协调具体代码段。
- SM-005 不继续修改 OpenGU 源码；本侧不修改 SyncMate Core、其 WorkItem、报告或安装策略。保留双方既有数据、缓存、结果和队列；不 stash/reset/clean 或整体回滚其他任务内容。
- 本机进行 CPU 接入测试、配置检查、控制与审阅。当前不新跑 GPU 实验；未来正式数据和 GPU 运行须遵循 `experiments/AGENTS.md`。职责拆分不授权整轮研究矩阵。
- 两边分别提交、验收和 Closeout。部署与安装遵循各自注册动作及已有具体授权，不能把原任务的准备脚本当作完成回执。

## Restart and next action

读取本 Record、项目指令、Git 与 live Claim，在独立 linked worktree 接手同一 AAGU-005。先核对上述已落地提交、Core 接口依赖、221 项检查及旧实测的复用边界，完成本侧最小必要代码核验与报告。与 SM-005 共享结果但分别验收；不启动 AAGU-010、重复矩阵或新 GPU 实验。

## Status history

- 既有登记：以 SyncMate 产品化取舍为目标，保持 registered / not claimed。
- 2026-09-05：按用户确认，将同一 AAGU-005 重定义为跨项目可行性与正确性检验，纳入完整实际远程工作链、项目配置与 Adapter 复用边界；补齐执行字段，保留编号、状态、practical 路线和编排依赖。未 Claim、执行或形成候选证据。
- 2026-09-05：后续用户讨论让 SM-005 承担实际检验，AAGU-005 只监控其完成；该意图已传达给 SM-005，但协调任务中断，当前 canonical Record 未形成相应监控版本。保留这段历史，不将旧意图视为最新执行边界。
- 2026-09-06：用户明确跨项目协作：AAGU-005 承担 OpenGU 消费端，SM-005 承担 SyncMate Core，分别修改与验收。取代“SM-005 同时拥有两边代码、AAGU-005 只监控并自动完成”的旧安排；沿用同一编号、practical 路线和 parallel 拓扑，登记状态仍为 registered / not claimed。
