# AAGU-002 · GATE · Device Readiness Pilot Acceptance

Block ID: `AAGU-002`

Item Version: 2.1

当前状态: `working / claimed`

Item Type: Block

Stable locator: `.workblock/items/AAGU-002/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`


> Git baseline：`943015daa68a37b96b306154d7c748a4120f9b64`

> Source branch：`refs/heads/codex/aagu-002-device-readiness`

> Remote target：`origin refs/heads/main`
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
- 登记时尚未形成 runtime candidate、receipt、report 和目标身份；本轮实测与缺口见下方 Verify。

### 本轮执行授权 — 2026-09-06

用户在核对 002 尚未完成后明确要求“那你把这个推进了呀”。本轮沿用同一 Human Surface，授权 Claim 后核查与复用 SM-005/006 已有证据，使用既有 autodl-opengu 及唯一活跃检出执行有界、只读的 Device Readiness 探测与必要拒绝路径验证。该执行授权取代上方登记时的 registration-only 限制；它不接受候选，也不授权正式科研矩阵、设备付费开通、bootstrap、安装或历史结果/缓存清理。

使用独立 linked worktree 形成候选和配对报告；本机负责审查与 CPU 验证，真实设备观察来自固定 SSH 目标。优先复用现用 Core/Adapter，不把 SM-001 的旧登记记录或历史 GPU 成功自动当作当前就绪。缺 GPU、身份错误或合同缺项时输出 REFUSED 和精确缺口，保持后续实验不下发。

## Restart and next action

本轮 Claim 已建立，保持 `ongoing`。先审阅 [实测报告](REPORT.md) 与 [SM-001 同号记录修正建议](evidence/SM001-record-proposal.md)。SM-001 只读协议检查返回实际 1.0 / 支持 2.1，当前 Skill 禁止自动升级接手；确认同号修正后再由 SM-001 实施完整门禁。其实现独立接受后，在同一 AAGU-002 复验真实 READY/REFUSED 和下发拒绝路径；当前不转 awaiting_acceptance、不启动后续矩阵。

## Verify — 2026-09-06

- 当前结果：设备事实满足本轮预期，但 AAGU-002 整体 `FAIL / REFUSED`。产品实现尚未修复，原 Human Surface 的门禁验收没有完成。
- 真实 SSH：`autodl-opengu` → `gpu4090`，唯一活跃检出 `/autodl-fs/data/OpenGU/GULib-master`，干净 main `b4da08647756810d24a7e51a23422bee7fbea3db`，1 张可用 RTX 4090。两端 Core 对应 `1e30a32925cecb8c29d72297fbf93bdd547259ba`，60 文件 payload 校验通过。
- 真实 adapter 在旧输出已存在时拒绝重复执行；进程内缺 GPU 注入也明确拒绝。没有新建远端任务，队列前后文件 SHA-256 相同。GPU 容量未测量；当前 device comparison 是人工规范化观察，不能当成生产下发许可。
- 隔离的真实 Core 复现：`ready=false` 仍写入 inbox，入队前 preflight 调用数为 0；执行前第二道检查才 blocked，进程调用数为 0。空预检 `{}` 被 recipe binding 判为 ready=true。这两项产品要求均 FAIL。
- 干净检查点：`e3ce4a1cd1e2cd03107b3b63b92a6fdaa167b2fc`。11 项证据完整性、来源和缺口复核通过，不代表 Gate PASS。后续报告/Record/修正建议不改变已测 Core、adapter、recipe 或 probe，复用上述真实观察；新增部分检查报告结构、链接、渲染与内容一致性。
- 当前规范化证据：[verification.json](evidence/verification.json)；决策投影：[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)。源代码复现可从对应 evidence 脚本重跑。
- SM-001 仍为原记录、未 Claim、未修改；没有推送、安装或正式实验。当前本地 main 的 002 登记增量尚未同步，亦不满足正式实验三方 SHA 对齐条件。
- Run 工具在创建上述 checkpoint 后报告 `git-head-ref-unreadable`；人工 read-only `git rev-parse HEAD`、最新提交标题与干净 status 已确认提交实际成功，未重复提交或修改工具。

## Status history

- 2026-09-06：用户要求推进同一 002；补齐运行位置与明确执行授权，原 Human Surface 和 formal 验收目标保持不变。
- 2026-09-06：完成真实设备观察、adapter 拒绝验证与两项 Core 门禁缺口复现；配对报告建议返工，Claim 保持 ongoing，等待同号 SM-001 记录修正后继续依赖实现。
