# AAGU-005 · SyncMate 的 OpenGU 接入与联调

Block ID: `AAGU-005`

Item Version: 2.1

当前状态: `accepted`

Item Type: Block

Stable locator: `.workblock/items/AAGU-005/WORKITEM.md`

Acceptance Route: `practical`

Execution topology: `parallel`

> Apply target ref：`refs/heads/main`


> Git baseline：`c9e094c55b42b2833fb24fcef5fe08f057605f68`

> Source branch：`refs/heads/codex/aagu-005-consumer-evidence`

> Remote target：`origin refs/heads/main`
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
- Orchestration: 保留 SUPPORT、P3 与 `AAGU-005 depends_on AAGU-001`；当前执行线与下一步由 WORKPLAN 拥有，不添加两项目互相等待的循环依赖。
- Coordination: 两边可独立推进；集成前绑定双方精确提交、Core 制品与接口合同。接口缺陷由代码所属项目修复，另一侧核验，不跨仓库代改。
- Related work: 026 已有模块化消费者是接入基础；015 提供当前阶段配置和 Selector 证据；028 的 Retrain/Metrics 软件修复已接受并落地，正式运行仍须满足各自实验门槛。002 Device Readiness、007 等科研验收及 SM-003 产品化合同保持独立。
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
- 写入只限 OpenGU 接入范围。`experiments/modular_execution.py` 只涉及必要运行上下文与产物路径接入；科研算法、Selector、GU、Retrain、Metrics 语义不因接入改变。028 已接受的方法与指标合同保持其归属，不在本 Block 重做。
- SM-005 不继续修改 OpenGU 源码；本侧不修改 SyncMate Core、其 WorkItem、报告或安装策略。保留双方既有数据、缓存、结果和队列；不 stash/reset/clean 或整体回滚其他任务内容。
- 本机进行 CPU 接入测试、配置检查、控制与审阅。当前不新跑 GPU 实验；未来正式数据和 GPU 运行须遵循 `experiments/AGENTS.md`。职责拆分不授权整轮研究矩阵。
- 两边分别提交、验收和 Closeout。部署与安装遵循各自注册动作及已有具体授权，不能把原任务的准备脚本当作完成回执。

## Restart and next action

用户已要求修复整理中发现的全部接入问题。本侧代码修复与 CPU 消费闭环验证已完成，见 [REPORT.html](REPORT.html) / [REPORT.md](REPORT.md)；当前建议接受本 WorkItem 已约定的代码验证范围，等待用户决定。

产品检查点为 `f7956bb994b20b629b60e8f1a4da20fc78ea6b88`。当前 source HEAD 还包含随后更新的报告、证据与状态；最终 identity、diff 和证据复用说明见本 linked worktree `.workblock/runtime/aagu005-report-qa/final-candidate.md`。不要重放已接受 SM-005 的安装或新增 GPU 运行。接受后沿用同一 locator Closeout。

## Repair and Verify · 2026-09-06

- 授权：用户明确指出接入接口与检查需要整体修复。本次继续同一 AAGU-005、同一 linked source 和 Claim；Resume 后 revision 2、phase ongoing。Human Surface、独立消费端归属和不新增 GPU 的约束保持原样。
- 修复：Adapter 正确传递 stage / ratio / config_path / gate_only；静态配置摘要更新为当前 028 已接受 YAML 的摘要。20 个 GU 配方直接消费执行器产物清单，分别涵盖 GNNDelete / Retrain；配方中的方法条件与真实矩阵消费者一致。
- 收集检查：独立 Output 解码、当前字节 SHA、Recipe/Artifact/内容身份、三处引用、Selection 与 checkpoint、模型/训练/删除语义、方法参数和重算指标共同核验。两种方法必须共享同一输入与请求，Retrain 不消费已训练 checkpoint；不再读取旧 collateral 或凭 npz 文件名判断成功。
- 相邻消费：结果表正确呈现独立方法结果；基础 Adapter 按需加载实验策略模块，避免独立 smoke 因缺少实验树失败。未修改 SyncMate Core、算法、正式 YAML、正式数据或缓存。
- 验证：8 个相关测试文件共 311 passed，0 failure/error/skip。新增检查覆盖 20 个配方清单、20 个真实预检签名、3 个 seed 下真实矩阵方法条件、gate/stage 两个真实 CPU 生产→收集→接受→结果表场景，以及 12 类拒绝情形。原始结果见 [repair-tests.xml](evidence/repair-tests.xml)，具体输出与复用边界见 [repair-verification.json](evidence/repair-verification.json)。
- 真实消费观察：临时 20 节点 CPU 图分别执行 GNNDelete 和 Retrain；真实本地 Git runner 经 Core 收集并校验后，collector 无远端 Store 仍通过检查；再次收集 fetched=0。检查期间模型 forward 与训练更新被禁止，源 Store 文件哈希保持一致。测试范围明确为可丢弃的 CPU 验证。
- 修复过程还暴露了重复索引被去重放过、旧配置摘要、过时的基础 smoke 断言和导入依赖；均已修正并纳入最终回归。原始失败快照保留，不将历史失败改为历史成功。
- clean 产品检查点上只读 audit：6/6 原子配方、20/20 正式 GU 配方、配置摘要与预检参数通过；CLI 编译和 Core smoke 通过。预检测试隔离设备/正式数据边界，runtime_ready 未观察，不声称正式 GPU gate 通过。
- 人类验收：当前建议接受代码与 CPU 接入验证，报告决定仍为待决定；最终报告检查通过后 Claim 进入 awaiting_acceptance。未 merge、push、install；SSH 主线 c9e094c5 尚不含此修复。

## Delivery audit · 2026-09-06

- 用户在核对两个 005 的接受状态后要求“对，做整理吧”。本轮承接已有消费端交付、整理报告并核对证据；未把该指令投影为完整接入范围的提前接受。
- 通过标准 parallel Start 创建 `E:/project/OpenGU-worktrees/aagu-005-consumer-evidence/GULib-master`；同一 AAGU-005 Claim 为 `1d37bd2a-2b00-44d2-8c82-cdf36beb7e8d`，owner codex，session 澄清两个005事项。正式关联仍为本 WorkItem locator；Git baseline / branch 见顶部运行字段。
- 交接提交 `e8f23a94dc7d753283442cadb1b45d8c1962234e` 已包含在 `c9e094c55b42b2833fb24fcef5fe08f057605f68`。所审 Adapter、配方、输出布局、原子 stage、modular_execution 及相邻两份测试相对交接提交无变化。后续 028 的方法/输出变更另由其原始 163 项与合并核验说明适用范围，不能仅叠加测试数量宣称整个接入通过。
- SM-005 已接受并在 `6a938e2acc4616044f8340b66f8369b1a42254b0` 合并、推送。双端安装为 Core 0.4.0；本地和 SSH 消费端均 `ready=true`、60 文件内容一致、errors 为空。重建 wheel 的 ZIP 摘要不同，实际载荷与原依赖清单一致。SM-005 安装回执的 partial 仅指其本地临时制品删除被自动审批拒绝，本 Block 不重复安装或处理该清理。
- SSH 只读读回为 clean `c9e094c5`，取代交接时“仅 preflight，尚未同步”的旧观察；原始版本和运行记录保留。新证据：[完整核对](evidence/observations.json)、[SSH 读回](evidence/remote-readback.json)。
- 新只读跨接口检查比较真实配置/配方与执行器枚举：6 个 SM-005 原子配方通过；20 个 target-direct GU 配方产物集合不一致。gate 每项声明 4、执行器枚举 8 个文件；整组每项声明 68、执行器枚举 136 个文件。差异包括旧 collateral.json、新 output-references.json 及未声明的独立 Retrain 输出。
- 真实预检调用还复现 `TypeError: float() argument must be a string or a number, not 'WindowsPath'`：Adapter 把 config_path 放入 ratio 位置，且未传 gate_only；异常发生在设备或数据预检之前。OpenGU GU 接受检查仍读取旧 collateral，源码定位记录在报告中。上述问题本轮未修改实现，不得记为 PASS。
- 本轮以项目 Python 运行 `tests/test_syncmate_atomic_stage.py` 和 `tests/test_retrain_outputs.py::test_aggregate_serialization_is_lossless`：13 passed，0 failure / error；[原始 XML](evidence/targeted-checks.xml)。支持原子入口拒绝行为、合同核对和已落地 F1 无损读回，不覆盖正式 GU 端到端。
- 配对报告结构、实际桌面渲染和全部证据链接已核对；看板从同一 WorkItem 重建，修正仍指向已关闭 028 的旧当前线，7 项看板检查通过。具体观察见 [整理验证](evidence/verification.md)。生成状态随最新事实变化，优先级和依赖未改。
- Agent 建议先修复上述接入缺口，再接受完整 AAGU-005；报告当前决定为待决定，状态保持 working / claimed。原始 SM-005 GPU 证据仍对应其各自版本，未新增 GPU 实验、队列任务、正式数据或缓存写入。

## Status history

- 既有登记：以 SyncMate 产品化取舍为目标，保持 registered / not claimed。
- 2026-09-05：按用户确认，将同一 AAGU-005 重定义为跨项目可行性与正确性检验，纳入完整实际远程工作链、项目配置与 Adapter 复用边界；补齐执行字段，保留编号、状态、practical 路线和编排依赖。未 Claim、执行或形成候选证据。
- 2026-09-05：后续用户讨论让 SM-005 承担实际检验，AAGU-005 只监控其完成；该意图已传达给 SM-005，但协调任务中断，当前 canonical Record 未形成相应监控版本。保留这段历史，不将旧意图视为最新执行边界。
- 2026-09-06：用户明确跨项目协作：AAGU-005 承担 OpenGU 消费端，SM-005 承担 SyncMate Core，分别修改与验收。取代“SM-005 同时拥有两边代码、AAGU-005 只监控并自动完成”的旧安排；沿用同一编号、practical 路线和 parallel 拓扑，登记状态仍为 registered / not claimed。
- 2026-09-06：按“做整理” Claim 同一 Block，在独立分支整理交付、报告与复现证据；发现正式 GU 接口缺口，保持 working / claimed，未执行完整接受或 Closeout。

- 2026-09-06：按用户明确的整体修复要求完成消费端代码修复及 311 项检查，形成同一 AAGU-005 待验收候选；此前 Delivery audit 为修复前历史观察。
- `accepted`（2026-09-06T04:24:32.6908840+08:00）：用户 基于 用户已阅读修复原因、实现与验证边界，确认：明白了，就已经修复好了呗。那其实我觉得 005 这部分已经算是修复好了。接受同一 AAGU-005 当前候选的代码正确性与 CPU 接入验证范围。 接受当前已验证候选。
