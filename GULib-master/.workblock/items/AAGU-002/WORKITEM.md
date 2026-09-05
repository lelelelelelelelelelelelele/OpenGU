# AAGU-002 · GATE · Device Readiness Pilot Acceptance

Block ID: `AAGU-002`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

Stable locator: `.workblock/items/AAGU-002/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

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

### 本轮执行授权 — 2026-09-06

用户在核对 002 尚未完成后明确要求“那你把这个推进了呀”。本轮沿用同一 Human Surface，授权 Claim 后核查与复用 SM-005/006 已有证据，使用既有 autodl-opengu 及唯一活跃检出执行有界、只读的 Device Readiness 探测与必要拒绝路径验证。该执行授权取代上方登记时的 registration-only 限制；它不接受候选，也不授权正式科研矩阵、设备付费开通、bootstrap、安装或历史结果/缓存清理。

使用独立 linked worktree 形成候选和配对报告；本机负责审查与 CPU 验证，真实设备观察来自固定 SSH 目标。优先复用现用 Core/Adapter，不把 SM-001 的旧登记记录或历史 GPU 成功自动当作当前就绪。缺 GPU、身份错误或合同缺项时输出 REFUSED 和精确缺口，保持后续实验不下发。

## Restart and next action

Use `block-workflow` to claim this exact WorkItem under the user's current execution authorization. Re-read the current Device Contract and remote AGENTS; reuse existing evidence, execute the smallest readiness pilot, and present the observed READY/REFUSED conclusion for the formal decision. Do not infer acceptance or start the downstream research matrix.

## Status history

- 2026-09-06：用户要求推进同一 002；补齐运行位置与明确执行授权，原 Human Surface 和 formal 验收目标保持不变。
