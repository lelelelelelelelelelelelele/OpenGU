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
- Suggested relations: `AAGU-002 depends_on AAGU-001`。原记录曾关联 SM-001；2026-09-06 用户明确本轮只处理 OpenGU 002，不接手 SM-001，其记录升级不作为本轮推进条件。若未来消费新的外部实现，仍须核验所消费版本的实际证据。
- Unconfirmed suggestions: formal GPU execution is not authorized by this registration.

## Runtime and authorization boundaries

- Registration only; no SSH, remote bootstrap, device probing, dispatch, GPU run, push, install, or external write.
- Later execution may use live provider only under explicit Device Readiness authorization and must preserve remote checkout identity.
- 登记时尚未形成 runtime candidate、receipt、report 和目标身份；本轮实测与缺口见下方 Verify。

### 本轮执行授权 — 2026-09-06

用户在核对 002 尚未完成后明确要求“那你把这个推进了呀”。本轮沿用同一 Human Surface，授权 Claim 后核查与复用 SM-005/006 已有证据，使用既有 autodl-opengu 及唯一活跃检出执行有界、只读的 Device Readiness 探测与必要拒绝路径验证。该执行授权取代上方登记时的 registration-only 限制；它不接受候选，也不授权正式科研矩阵、设备付费开通、bootstrap、安装或历史结果/缓存清理。

使用独立 linked worktree 形成候选和配对报告；本机负责审查与 CPU 验证，真实设备观察来自固定 SSH 目标。优先复用现用 Core/Adapter，不把 SM-001 的旧登记记录或历史 GPU 成功自动当作当前就绪。缺 GPU、身份错误或合同缺项时输出 REFUSED 和精确缺口，保持后续实验不下发。

## Restart and next action

本轮 Claim 已建立，保持 `ongoing`。只在 OpenGU 002 核验当前注册实验入口所消费的实际运行条件与最小验证证据。`ready` 是预检输出，不是需要用户填写的新参数；确认检查真的执行、失败时不启动实验，不能把布尔字段自身当作证据。把入队和开始执行分别观察，工具层的隔离异常测试不自动证明 OpenGU 实验已经错误启动。不接手 SM-001、不要求用户先升级其记录；尚未完整交付 002 验收，也不启动后续矩阵。

## 当前解释修正 — 2026-09-06

用户明确指出任务是 OpenGU 002，SM-001 不属于本轮。上一轮要求先处理 SM-001 的建议撤回。设备核查已有真实观察；上一轮并未新跑 OpenGU 最小任务，而是执行探测、现有 adapter 预检及隔离队列复现，因此不能宣称完整 002 已完成。

`ready` 由预检对真实 GPU、路径、依赖、数据及已有结果等条件的检查结果计算。当前 OpenGU adapter 会正常返回该字段；空对象样例是通用 Core 的受控异常测试。明确拒绝的隔离任务虽已入队，但执行前被 blocked，进程启动次数为 0，不能把它描述为“缺 GPU 仍开始实验”。原验收所要求的完整门禁链路尚未补齐观察，当前为证据不足，不能仅凭字段测试判定 OpenGU 实验失败或宣告通过。

## Verify — 2026-09-06

- 上一轮结论曾写成 AAGU-002 整体 `FAIL / REFUSED`；当前按上方解释修正为：设备事实满足本轮预期，完整 OpenGU gate 仍为 `NOT CONFIRMED`。保留真实观察，不把通用 Core 的异常样例自动扩张为 OpenGU 实验失败。
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
- 2026-09-06：按用户纠正撤回上一条的 SM-001 接手及升级前置条件；明确 ready 是检查输出、入队与执行分别判断，继续限定在 OpenGU 002，未接受或放行。
