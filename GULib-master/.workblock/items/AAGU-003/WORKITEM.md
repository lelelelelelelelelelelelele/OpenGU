# AAGU-003 · Formal GPU Execution and Evidence Acceptance

Block ID: `AAGU-003`

当前状态: `registered / not claimed`

Item Type: Block

## Block human acceptance surface

### 当前基线
OpenGU M1 工程交付与 no-GPU smoke 已有证据，但正式 GPU 科研实验尚未运行，也没有可接纳的正式科研 evidence package。

### 这次增量
在 AAGU-001 的批准实验定义和 AAGU-002 的 readiness gate 之后，执行正式 GPU 矩阵并对结果、来源、配置、版本和 artifacts 做科研证据接纳。

### 完成后人会看到什么
每个正式实验结论都能追溯到批准的配置、数据/split、代码 SHA、设备 readiness、运行产物和明确的接纳决定。

### 验收项目
- 正式运行使用批准的矩阵、recipe、数据/split 和 pinned source identity。
- 结果 artifacts、日志、指标语义和 provenance 足以复核，不把 queue done 或单次 smoke 当作科学证据。
- 每个结论都有明确的 PASS、FAIL、NOT OBSERVED 或 NOT CONFIRMED 事实，以及人的接纳决定。

### 主要证据
- formal gate/matrix manifest：判断执行是否严格遵守批准计划。
- SHA-verified run artifacts 与环境/设备 identity：判断结果来源是否可信。
- 科研 acceptance report：判断哪些结果被接受、哪些仍缺证据。

### 关键 non-goals
- 不修改实验定义以迎合已经产生的结果。
- 不把工程 smoke、dry-run、queue 状态或部署成功写成正式科研接受。
- 不在本 Block 内开发新的 SyncMate consumer 或产品化功能。

### 需要人的决定
AAGU 研究负责人对正式 GPU evidence package 做明确接纳或返工决定；结果尚未观测。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记并保留既有任务合同。
- Primary surface: `data / research evidence`
- Minimum real evidence: 批准矩阵、pinned SHA、设备 readiness、完整 artifacts、provenance 和可复核 acceptance report。
- Post-candidate decision: AAGU 研究负责人必须明确批准或拒绝科研证据。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: OpenGU experiments/AGENTS、正式 GPU gate、当前 E8/E3 计划；没有额外稳定 Graph/Blueprint ID。
- Suggested relations: `AAGU-003 depends_on AAGU-001`; `AAGU-003 depends_on AAGU-002`。理由是正式执行必须消费已批准定义和 readiness 结论。
- Unconfirmed suggestions: no automatic relation to any smoke report.

## Runtime and authorization boundaries

- Registration only; no GPU execution, remote dispatch, result collection, push, install, or external write.
- Future execution must occur from the active SSH checkout under experiment AGENTS, with source/data/cache/result identity checks.
- Current implementation candidate, experiment run identity, evidence, and report are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem only after AAGU-001 and AAGU-002 provide accepted prerequisites. Re-read experiment AGENTS and the approved matrix before any formal run.
