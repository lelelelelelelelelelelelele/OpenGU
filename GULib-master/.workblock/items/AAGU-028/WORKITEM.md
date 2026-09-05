# AAGU-028 · FIX · Retrain 独立方法与 Metrics 输出复用

Block ID: `AAGU-028`
Item Version: 2.1
Item Type: `Block`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-028/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

将 Retrain 作为可独立配置、执行和复用结果的 Unlearning 方法。Metrics 只读取已经完成的 GU / Retrain 输出进行比较，避免每个 GU 或每次评价都重新训练参照模型。本项是用户明确要求的实验执行前置 FIX；完成、验收并落地之前，不启动整轮正式研究实验。

### 本次增量

在 AAGU-026 已接受的模块化配置、Selection→GU 和 Cache V2 基础上，补齐 Retrain 方法注册、小表、真实执行消费者及独立结果身份；同一已验证删除请求和相同 Dataset/Split、模型、训练与删除语义下，Retrain 结果可供 GNNDelete、GIF 等参照评价复用。更换 GU 专属参数或 Metrics 配置不重复执行该 Retrain。

将活动 Metrics 路径改为显式引用并读取已持久化的 GU / Retrain 输出，接通 modular 的 post_unlearning_utility_and_retrain_gap。移除 eval_collateral.py 内部隐式重训练路径，不保留兼容 fallback。补充从实验定义、Selection、Unlearning / Retrain 产物到 Metrics 的数据流说明与最小可执行示例；不在本 Block 运行完整科研矩阵。

### 核心验收

- Retrain 可通过独立 Unlearning YAML 选择并由真实入口执行；可直接消费已有 Selection，过程中不调用 Selector producer。不增加第二套 Retrain 算法或隐藏方法分发。
- 在临时 CPU 小图上，以同一真实 Dataset/Split 和删除请求运行独立 Retrain，保存可复核的模型/预测与所需评价输入。明确删除监督、边/特征、训练图及评价图语义；不能仅排除 train_mask 就无条件宣称覆盖所有删除语义。
- GNNDelete、GIF 与 Retrain 输出可按同一实际请求配对；Metrics 只读产物计算已注册的 utility / retrain-gap 指标。禁止训练入口后，单独重算 Metrics 仍成功；改变指标集合或 GU 专属参数不触发匹配 Retrain 的 producer。
- 验证冷运行、热读取、跨 GU 复用、独立 Metrics 重算的数值和身份一致性；持久化输出不因舍入后重算而改变同一评价身份的数值。身份不同或缺失时明确 MISS/拒绝，不自动重训、猜测、下载或修复输入。
- 真实数据/划分、实际删除请求、模型训练条件或删除语义变化时，不能误用旧 Retrain。核对所复用 Artifact 的内容哈希、完整性、代码/producer 与依赖身份；不把整个实验编号或 Metrics 配置放入 Retrain 计算身份。
- 通过已批准范围内的 CPU 集成验证、可重跑示例、数据流说明及配对报告，由用户明确接受、返工或拒绝。完成软件验证不等于正式实验已运行或已接受。

## Confirmed acceptance contract

- Class: `FIX`; Priority: `P0`，位于正式实验执行之前。
- Route: `formal`; Primary surface: `execution / artifact identity / metrics integration`; Decision owner: 用户。
- Minimum real evidence: 隔离 CPU 小图上的真实独立 Retrain 与 GNNDelete/GIF 输出；冷/热与跨方法复用的 producer 记录；禁止训练后的 Metrics-only 运行；同请求/错身份验证；原始输出与指标读回一致性；可重跑命令和数据流说明。
- Report size: 同目录配对 REPORT.md / REPORT.html，由实现阶段生成；登记阶段不创建报告或伪证据。
- Post-candidate decision: 形成精确候选后停在人类验收；接受并落地后才可能解除本项正式实验前置。仍须满足各实验自己的定义、输入绑定、设备和运行批准。
- Execution topology reason: 使用 linked worktree 形成独立修复候选，保留 AAGU-015 现有候选和验收边界；具体 branch、owner、session 和工作目录在 Claim 时绑定。

## Source and relations

- Source anchor: 2026-08-27 任务 Clarify selector timing in paper（01a04258-40c2-75f3-80a7-52f7bf841e25）。用户原话：“你只需要把 retrain 也注册成一个 unlearning 方法就行。”随后明确同意“删除 eval_collateral.py 内部隐式重训路径，不保留兼容 fallback”，并要求说明 metric 数据流与实验关系。
- 原始对话定位：rollout-2026-08-27T16-31-15-01a04258-40c2-75f3-80a7-52f7bf841e25.jsonl，user message 时间 2026-08-27T09:21:27.102Z / 2026-08-27T11:17:53.135Z。登记前已核对原始消息；方法注册要求此前未形成独立 WorkItem。
- 2026-09-05 本任务用户明确本项属于很靠前的 FIX，“在建好之前就不能跑整个实验”；随后授权“登记这个 block，然后我们就准备开始做”。本轮授权登记，后续 Claim 才开始实施。
- `AAGU-028 depends_on AAGU-001`：继承已接受的实验配置与证据合同。
- `AAGU-028 depends_on AAGU-026`：消费已接受的独立配置、方法缓存和 Selection→GU 实现。026 最终验收未包含独立 Retrain；本项承接遗漏的历史实现需求，不虚构它已被实现或已被验收。
- `AAGU-007 depends_on AAGU-028`、`AAGU-027 depends_on AAGU-028`：既有正式 GU 实验执行根必须等待本 FIX 接受并落地；其后续实验继承该前置。正式 Selector 计时路线同样遵守用户本次设定的实验运行门槛。
- AAGU-015 交付本阶段方案、YAML 与能力覆盖检查，可以独立验收这些材料；本 FIX 不作为其材料验收依赖。任何使用 015 方案的正式执行仍须先满足本 FIX。
- Graph placement: `repair`。优先级、当前线与运行前置由 [WORKPLAN](../../../self/dashboard/WORKPLAN.md) 拥有；本 Record 拥有修复范围与验收。
- 当前代码定位：[方法配置](../../../experiments/modular_config.py)、[GU 消费](../../../experiments/modular_gu.py)、[Evaluation](../../../experiments/modular_evaluation.py)、[既有 run_retrain](../../../attack/pipeline_adapter.py)、[隐式调用路径](../../../eval_collateral.py)、[结果读回](../../../attack/result_cache.py)。执行前须重读当前事实。

## Scope and execution boundaries

- 保留原数据、划分、checkpoint、Selection 和历史结果；不手工删除、覆盖、迁移或改标 Cache V2 Artifact。发生语义变化时产生独立新身份。
- 从已支持的节点删除、GNNDelete/GIF 与本阶段评价出发实现完整最小链路，不扩展所有未来 GU、模型或研究指标；不承接排名比较、完整实验调度或其他不相关算法开发。
- 本地仅进行代码修改与隔离 CPU 软件验证。正式 GPU、SSH 写入、整轮实验、push、install、Apply、清理不属于本次登记或候选实现授权。
- 不修改 SyncMate 通用框架来替代 OpenGU 的方法、产物或 Metrics 职责。若已注册项目执行 stage 消费旧隐式路径，在同一 OpenGU 修复中更新必要调用，不添加 fallback。
- 用户已明确本项为正式实验前置；015 的方案材料、无写入检查和本 FIX 必需的软件验证可以先行。已有历史运行不得因本登记被批量重标为有效或无效。

## Restart and next action

使用 block-workflow 执行此 stable locator。先重读最新 Record、AAGU-001/026 接受事实、项目指令和 live Claim，在 linked worktree 中 Claim 同一 Block 后再实施。先复现方法未注册、Metrics 隐式重训和结果读回问题，再逐层完成独立执行、持久化复用及 Metrics-only 消费。任务标题使用 AAGU-028 · FIX · Retrain 独立方法与 Metrics 输出复用；完成约定软件证据后停在 formal 人类验收。

## Status history

- 2026-09-05: 用户确认此前明确提出的 Retrain 独立方法要求，指定为正式实验之前的前置 FIX，并授权登记。本次 registered / not claimed；未创建任务、Claim、实现或运行实验。
