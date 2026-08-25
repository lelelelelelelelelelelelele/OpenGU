# AAGU-002 · GATE · Device Readiness Pilot Acceptance

Block ID: `AAGU-002`

当前状态: `registered / not claimed`

Item Type: Block

## Block human acceptance surface

### 当前基线
SyncMate Device Contract 已定义协议语义，但实际 alias resolver、远端连通性、设备身份、GPU/path/capability probe、READY/REFUSED receipt 和 dispatch guard 尚未作为一个真实设备 pilot 被接纳。

### 这次增量
把 Device Readiness 形成一个独立的端到端 pilot：alias resolver → SSH connectivity → identity/GPU/path/capability probe → READY/REFUSED receipt → dispatch guard，并分别确认 AAGU 能否安全消费其结果。

### 完成后人会看到什么
在正式 GPU 实验之前，系统能对目标设备给出可复核的 READY 或 REFUSED 结论，并阻止未就绪环境进入 dispatch。

### 验收项目
- 设备 alias 被解析到明确且唯一的目标，不允许静默落到错误 checkout 或旧环境。
- 连通性、身份、GPU、路径和能力检查形成一份可复核 receipt，失败原因可定位。
- dispatch guard 只允许满足 readiness contract 的目标继续，smoke 结果不被写成 formal acceptance。

### 主要证据
- 实际 SSH/远端 bootstrap 与 alias resolver receipt：判断目标身份和连通性。
- identity/GPU/path/capability probe receipt：判断设备是否真正满足 contract。
- READY/REFUSED 与 dispatch guard evidence：判断未就绪设备是否被安全阻断。

### 关键 non-goals
- 不运行正式科研 GPU 矩阵。
- 不把一次 no-GPU smoke 或 SSH 成功写成科研实验接受。
- 不修改 FlowChunk，也不扩展 SyncMate Core 到科研逻辑。

### 需要人的决定
AAGU 研究负责人和 SyncMate Device owner 共同确认该 readiness gate 是否足以允许后续正式执行；结果尚未观测。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记并保留既有任务合同。
- Primary surface: `lifecycle / integration / security boundary`
- Minimum real evidence: 真实目标上的 resolver、SSH、identity/GPU/path/capability probe、READY/REFUSED receipt 和 dispatch guard；不以 smoke 代替接受。
- Post-candidate decision: Device owner 与 AAGU gate owner 必须明确批准、返工或拒绝。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: OpenGU staged migration 中的 Device Readiness 与 SyncMate Device Contract；没有额外稳定 Graph/Blueprint ID。
- Suggested relations: `AAGU-002 depends_on AAGU-001`；cross-project implementation companion `SM-001` must be independently accepted before AAGU consumes its implementation result.
- Unconfirmed suggestions: formal GPU execution is not authorized by this registration.

## Runtime and authorization boundaries

- Registration only; no SSH, remote bootstrap, device probing, dispatch, GPU run, push, install, or external write.
- Later execution may use live provider only under explicit Device Readiness authorization and must preserve remote checkout identity.
- Current runtime candidate, receipt, report, and target identity are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem in a later execution task. Re-read the current Device Contract and remote AGENTS first; execute the smallest real pilot and stop at the formal readiness decision.
