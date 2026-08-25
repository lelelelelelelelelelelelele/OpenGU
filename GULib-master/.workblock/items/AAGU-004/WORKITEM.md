# AAGU-004 · FlowChunk Second-Consumer Robustness D0

Block ID: `AAGU-004`

当前状态: `awaiting acceptance`

Item Type: Block

## Block human acceptance surface

### 当前基线
SyncMate M1 已完成 Core 抽离与 OpenGU consumer 交付；FlowChunk 仍有独立 dirty state、submodule/local path 与 artifact-channel 边界，旧 D0 报告只完成了静态鲁棒性审计，尚未形成 canonical Block report。

### 这次增量
先审计 FlowChunk 是否已经具备安全接入 SyncMate 的 consumer 边界，并给出 D1 adapter 的 go/no-go；本 Block 不直接实现 adapter。

### 完成后人会看到什么
能够清楚判断 FlowChunk 的失败是 Core 鲁棒性问题、consumer adapter 缺失、外部 artifact contract 不清，还是当前 dirty/deployment 状态导致的证据不足。

### 验收项目
- Core、consumer-owned adapter、recipe/preflight、acceptance parser 和 artifact channel 的责任边界被逐项检查。
- FlowChunk 的 pinned source、dirty state、local submodule path 和外部运行产物限制被准确记录，不把静态检查写成集成接受。
- D0 给出明确的 D1 go/no-go、缺口和最小下一步；不把 smoke 写成 formal acceptance。

### 主要证据
- FlowChunk read-only baseline 与源代码/配置扫描：判断是否存在真实 consumer boundary。
- SyncMate contract 与旧 D0 findings 的对照：判断 Core 与 adapter 的缺口。
- D0 canonical report：判断是否授权另一个独立的 D1 WorkItem。

### 关键 non-goals
- 不修改 FlowChunk、`.gitmodules`、submodule、dirty files 或远端状态。
- 不实现 SM-002/D1 adapter。
- 不运行正式 GPU 实验，也不宣称 FlowChunk 已被接入或接受。

### 需要人的决定
AAGU 研究负责人确认 D0 是否充分、需要返工，或是否允许另行启动 SM-002/D1；结果尚未观测。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记、保留既有 D0 事实与待决定状态。
- Primary surface: `integration / contract`
- Minimum real evidence: read-only baseline、边界/契约审计、consumer 缺口、artifact-channel 判断和 D0 report；不以 smoke 代替 acceptance。
- Post-candidate decision: AAGU 研究负责人必须明确批准 D0、要求返工或拒绝 D1 授权。
- Report size: paired Markdown/HTML report after Verify, co-located in this WorkItem.

## Context and relations

- Blueprint scope: SyncMate consumer boundary 与 FlowChunk 当前 checkout；没有额外稳定 Graph/Blueprint ID。
- Suggested relations: SM-002 is a separate implementation companion and may only be started after an explicit D0 decision; this is a cross-project dependency, not a duplicate Record.
- Unconfirmed suggestions: old project-level D0 report is historical context only, not this WorkItem's acceptance report.

## Runtime and authorization boundaries

- This Record preserves the completed D0 read-only audit and its requested paired report under the corrected AAGU project identity.
- No FlowChunk edits, `.gitmodules`/submodule updates, remote writes, implementation, GPU run, or formal experiment were performed.
- No SM-002/D1 WorkItem was claimed or started; any later D1 work requires a separate explicit decision.
- D0 audit identity: `AAGU-004-D0-read-only-20260824`; no code implementation candidate was formed.
- Evidence identity: static read-only audit bound to FlowChunk `83df11bc6c98097de316a94a5bceb74ff2079668`, gitlink `e57c8536e7dbccb0ae75b82b8c6f44db885ce62c`, and SyncMate `ccf69fc2e1a7beff492a83cbb2b900c1f03c5a4c`.
- Report identity: co-located `REPORT.md` and `REPORT.html`, verified together with this WorkItem at the current Git candidate; no duplicate EOL-sensitive report digest is used.
- HTML rendering: `PASS` after AAGU identity rebinding via Microsoft Edge headless at 1440x1000 and 1440x4400; title, current-decision projection, first screen, evidence table, decision section, technical appendix, and full-page layout were visually checked without obvious overflow or broken content.

## Restart and next action

Current execution owner: this user-visible Codex task, bound to this exact WorkItem locator for identity correction only. D0 read-only audit and canonical paired report remain complete; stop at the human go/no-go decision. No SM-002/D1 claim or implementation is authorized by this record.

## Status history

- 2026-08-24: completed the read-only D0 audit and paired report under the superseded project identity; no SM-002/D1 claim, FlowChunk mutation, or external execution/write.
- 2026-08-25: user confirmed AAGU as the authoritative project identity and approved preserving this D0 record/report as `AAGU-004`; decision remains pending.
