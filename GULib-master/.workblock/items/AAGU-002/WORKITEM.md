# AAGU-002 · GATE · Device Readiness Pilot Acceptance

Block ID: `AAGU-002`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

在任何正式 GPU 实验之前，用一个真实设备试点证明目标环境确实可识别、可连接且满足运行条件。人最终需要看到可复核的 READY（就绪）或 REFUSED（拒绝）结论，并确信未就绪的设备不会被静默放行到任务下发。

### 本次增量

在已有 SyncMate 设备合同语义之上，贯通设备别名解析、SSH 连通、设备身份、GPU/路径/能力探测、READY/REFUSED 回执和任务下发门禁，并确认 AAGU 能否安全消费这份结果。本 Block 不运行正式科研矩阵，不把无 GPU 冒烟检查或单纯 SSH 成功写成科研接受，也不修改 FlowChunk 或把 SyncMate 核心扩展到科研逻辑。

### 核心验收

- 设备别名必须解析到明确且唯一的目标，不能落到错误 checkout 或旧环境；连通性、身份、GPU、路径和能力检查都要有可复核回执，失败原因可定位。
- 任务下发门禁只能让满足设备就绪合同的目标继续，并能用真实 READY/REFUSED 证据阻断未就绪环境。
- AAGU 研究负责人和 SyncMate 设备负责人能共同决定该 gate 是否足以授权后续正式执行；试点成功本身仍不等于科研实验已接受。

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
