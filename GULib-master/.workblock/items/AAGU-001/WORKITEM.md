# AAGU-001 · FIX · Experiment Definition and Registration Contract

Block ID: `AAGU-001`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

把 OpenGU 已分散存在的正式实验方向、实验入口和 SyncMate 工程连接收敛为一份可批准、可追溯的实验定义合同。最终需要让每个科学问题、配置、矩阵和验收门都有明确的事实所有者，同时让 SyncMate 只承担通用执行与证据连接，不替代科研判断。

### 本次增量

在现有局部事实之上，形成正式实验的统一定义入口：逐项明确研究问题、变量、实验配方（recipe）、矩阵、证据接纳条件和注册执行链，并清楚分开科研判断、实验执行、设备就绪、证据接纳以及 SyncMate 核心/适配器的职责。本 Block 只形成定义与连接合同，不运行正式 GPU 实验，也不实现设备就绪检查、FlowChunk 适配器或产品化增强。

### 核心验收

- 每个正式实验节点都能从唯一事实所有者追溯到明确的研究问题、变量、矩阵和实验配方；注册后的空跑检查（dry-run）只能证明计划可执行，不能冒充实验结果。
- 科研决定、设备与执行职责、证据接纳以及 SyncMate 的工具边界清楚分开，SyncMate 不成为科研 Claim 或 acceptance 的决定者。
- AAGU 研究负责人能够据此明确批准、返工或拒绝实验定义；在批准前，正式实验结果仍是“未观测”。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记并保留既有任务合同。
- Primary surface: `research definition / integration contract`
- Minimum real evidence: 可审阅的实验定义、recipe、矩阵、gate 和 dry-run；这些只能证明计划可执行，不证明正式实验已接受。
- Post-candidate decision: AAGU 研究负责人必须明确批准、返工或拒绝该实验定义。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: 当前 OpenGU OB 实验入口与目录级 AGENTS；没有额外稳定 Graph/Blueprint ID，故不虚构节点。
- Suggested relations: `AAGU-002 depends_on AAGU-001`；`AAGU-003 depends_on AAGU-001`。理由是设备验收和正式执行都必须消费已批准的实验定义。
- Cross-project references: SyncMate SM records are implementation companions, not duplicate scientific acceptance records.

## Runtime and authorization boundaries

- Registration only; no claim, implementation, experiment dispatch, GPU run, push, install, or external write.
- Future execution must use the OpenGU active checkout and experiment-specific AGENTS; local dry-run is not formal GPU acceptance.
- Current runtime candidate, branch, evidence identity, and report identity are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem only in a later execution task. First reread this Record, the current OpenGU experiment instructions, and the SyncMate boundary documents; then form the experiment-definition candidate and stop at the formal human decision gate.
