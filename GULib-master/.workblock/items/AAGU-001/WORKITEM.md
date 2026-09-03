# AAGU-001 · FIX · 实验合同与注册规范

Block ID: `AAGU-001`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

建立一份可独立验收、供后续实验共同使用的实验合同与注册规范：明确一份实验计划需要记录哪些信息，如何关联已有研究计划、配置、执行记录与结果证据，以及何时可以注册、执行和接纳证据。SyncMate 只承担通用执行与证据连接，不替代科研判断。

### 本次增量

固定实验合同的结构与填写规则，明确研究问题、变量、矩阵、实验配方（recipe）、数据与划分、删除预算、执行入口和证据接纳条件应如何记录、由谁拥有、怎样相互追溯。已有参数、变量和矩阵继续引用原计划与配置；用一个已有且定义明确的实验验证合同和注册链可用，不要求一次定义或批准全部实验。

具体 IF 定义与 selector 选择由 AAGU-015 等对应科研任务决定。每轮执行前记录本轮问题和必要定义，运行后在对应实验中分析真实结果、解释现象并形成下一轮设计，保留本轮原始定义与证据。本 Block 只形成公共合同与注册规范，不运行正式 GPU 实验，也不实现设备就绪检查、FlowChunk 适配器或产品化增强。

### 核心验收

- 一份可审阅的实验合同说明必要信息、填写规则、事实所有者，以及计划、配置、执行记录和结果证据的关联方式，并明确注册、执行与证据接纳的条件。
- 至少一个已有且定义明确的实验完成合同示例、来源追溯和注册后的空跑检查（dry-run），证明合同及注册链可用；不新增正式运行，也不把 dry-run 当作实验结果。
- 科研决定、设备与执行职责、证据接纳以及 SyncMate 的工具边界清楚分开，SyncMate 不成为科研 Claim 或 acceptance 的决定者。
- AAGU 研究负责人能够独立批准、返工或拒绝这份公共规范。验收不以全部实验参数、selector 或矩阵冻结为前提；具体实验仍须按规范完成本轮定义与批准后才能执行，已有真实结果的解释归对应实验所有。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 2026-09-04 用户确认保留 AAGU-001 编号，将范围收窄为独立的“实验合同与注册规范”，不新增参数梳理 Block，并将 AAGU-001 调整为 AAGU-015 的前置。
- Primary surface: `experiment contract / registration specification`
- Minimum real evidence: 可审阅的合同结构与填写规则、注册与证据接纳条件，以及一个已有明确实验的合同示例、来源关联和 dry-run；这些证明公共规范可用，不证明正式实验结果已被接受。
- Post-candidate decision: AAGU 研究负责人必须明确批准、返工或拒绝该公共规范；接受 AAGU-001 不等于批准所有具体实验。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: 当前 OpenGU OB 实验入口与目录级 AGENTS；没有额外稳定 Graph/Blueprint ID，故不虚构节点。
- Fact owner: [本 WorkItem](WORKITEM.md) 拥有公共合同与注册规范的任务范围和验收要求；具体科学问题、参数与矩阵继续引用原研究计划和配置。
- Confirmed relations: `AAGU-001 depends_on AAGU-006`；`AAGU-015 depends_on AAGU-001`。公共规范继承已接受的数据与划分边界，AAGU-015 消费该规范形成具体科学定义；AAGU-001 不依赖 AAGU-015 的选择结果。
- Existing downstream relations: `AAGU-002 depends_on AAGU-001`；`AAGU-003 depends_on AAGU-001`。设备与证据 gate 消费公共规范，各具体实验的定义与科学批准仍由对应任务提供。
- Cross-project references: SyncMate SM records are implementation companions, not duplicate scientific acceptance records.

## Runtime and authorization boundaries

- Registration only; no claim, implementation, experiment dispatch, GPU run, push, install, or external write.
- Future execution must use the OpenGU active checkout and experiment-specific AGENTS; local dry-run is not formal GPU acceptance.
- Current runtime candidate, branch, evidence identity, and report identity are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem only in a later execution task. First reread this Record, the current OpenGU experiment instructions, and the SyncMate boundary documents; then form the shared experiment-contract and registration-specification candidate, validate it with one already-defined experiment, and stop at the formal human decision gate. Do not expand the task into freezing every experiment or making AAGU-015's scientific choices.

## Status history

- 2026-09-04: 按用户确认收窄同一 WorkItem 的标题、范围和验收条件，调整为 AAGU-015 的前置；本次仅修订登记合同，状态保持 `registered / not claimed`，未 Claim 或实施公共规范。
