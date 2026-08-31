# AAGU-003 · EXP · Formal GPU Evidence Acceptance Gate

Block ID: `AAGU-003`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

把正式 GPU 实验从“已经运行”提升为“证据可以被项目接纳”：每项科研结论都必须能追溯到批准的实验定义、数据与划分（split）、代码 SHA、设备就绪结论、运行产物和明确的人类决定，工程交付、队列完成或无 GPU 冒烟检查都不能替代这一步。

### 本次增量

在各独立 EXP Block、AAGU-001 实验定义合同、AAGU-002 设备就绪门以及 WORKPLAN 声明的其余前置全部满足后，统一复核正式矩阵、实验配方、来源身份、结果产物、日志、指标语义和来源链，并形成项目级科研证据包。本 Block 不为迎合结果而改实验定义，也不开发新的 SyncMate 消费端或产品化功能。

### 核心验收

- 正式运行严格绑定批准的矩阵、实验配方、数据/split、固定源码身份和设备就绪结论，正式运行清单与经 SHA 校验的产物可相互复核。
- 每个结论都明确记录 PASS、FAIL、NOT OBSERVED 或 NOT CONFIRMED；冒烟检查、空跑检查、部署成功和队列状态不会被提升为科学证据。
- AAGU 研究负责人能从验收报告判断哪些结果可接纳、哪些必须返工或仍缺证据，并作出明确决定。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记并保留既有任务合同。
- Primary surface: `data / research evidence`
- Minimum real evidence: 批准矩阵、pinned SHA、设备 readiness、完整 artifacts、provenance 和可复核 acceptance report。
- Post-candidate decision: AAGU 研究负责人必须明确批准或拒绝科研证据。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: OpenGU experiments/AGENTS、正式 GPU gate 与 WORKPLAN 实验 timeline；没有额外稳定 Graph/Blueprint ID。
- Suggested relations: `AAGU-003 depends_on AAGU-001`; `AAGU-003 depends_on AAGU-002`。理由是正式执行必须消费已批准定义和 readiness 结论。
- Unconfirmed suggestions: no automatic relation to any smoke report.

## Runtime and authorization boundaries

- Registration only; no GPU execution, remote dispatch, result collection, push, install, or external write.
- Future execution must occur from the active SSH checkout under experiment AGENTS, with source/data/cache/result identity checks.
- Current implementation candidate, experiment run identity, evidence, and report are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem only after AAGU-001 and AAGU-002 provide accepted prerequisites. Re-read experiment AGENTS and the approved matrix before any formal run.
