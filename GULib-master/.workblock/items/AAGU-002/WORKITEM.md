# AAGU-002 · GATE · Device Readiness Pilot Acceptance

Block ID: `AAGU-002`

Item Version: 2.1

当前状态: `accepted`

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

在正式实验之前，确认 OpenGU 的目标设备可识别、可连接，已有运行要求与超时、耗时字段能够被当前入口消费，并通过有界 Smoke Test。002 提供设备与接口准备证据；最小正式端到端实验由 AAGU-007 负责。

### 本次增量

核查固定 SSH 设备的身份、GPU、路径和依赖，验证 OpenGU 已登记 recipe 的 timeout_seconds 经现用 Core 原样进入执行合同，定位并核验已有耗时字段及其基准/本轮访问含义，运行组件 Smoke Test 和实际子进程 Timeout 小测试，并提供验收报告。现有 OpenGU 预检的失败路径保留证据；不在 002 接手 SyncMate 通用设备协议、重做最小正式实验或实现完整组件计时和大图外推。

### 核心验收

- 固定设备的别名、连接、身份、GPU、路径和依赖有可复核真实观察，现有实验预检在条件失败时明确拒绝启动实验。
- 已登记 recipe 的作业超时字段与执行合同一致；已有耗时证据位置和字段含义清楚，HIT 保留历史基准，缺失值不当成 0。
- Smoke Test 完成预检、传输、校验、可信索引及导出；用户据此接受 002 的准备结果。最小正式实验、真实新运行的耗时与产物验收留在 007，002 接受不等于 007 已运行或被接受。
- 最小测试真实触发 Timeout：任务被终止并生成明确失败回执，不能误报成功或残留 running；后续正常任务仍可完成。报告区分实际软件小测试与 007 的正式科研实验，由用户审阅当前结果后决定。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 2026-09-06 用户明确“002 的字段已经配好了，可以跑一些 Smoke Test，但真实的测试是不是应该在 007 里测？如果是的话，这个就应该 accept 了？”；当前 007 Record 确实拥有最小正式端到端实验。上述 Human Surface 按这次范围澄清修正，条件接受以当前字段和 smoke 核验通过为依据。
- Primary surface: `lifecycle / integration / security boundary`
- Minimum real evidence: 固定 SSH 设备真实观察、现有 OpenGU preflight 拒绝证据、已登记字段的真实消费、Smoke Test；最小正式运行证据属于 007。
- Post-candidate decision: 用户随后修正为“需要提供 Smoke Test 和验收报告……可以做一组最小的实验……测试 Timeout，然后把验收报告给我”。因此先交付当前候选与验收报告，等待用户审阅决定，不沿用上一条条件接受自动 Closeout。
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

本轮交付设备、字段、组件 Smoke 和真实子进程 Timeout 验证及配对验收报告。按用户最后修正，形成当前可验收候选后转 awaiting_acceptance，交付报告等待决定，不执行 Closeout。AAGU-007 保留原状态，不启动其正式实验。

## 当前验收依据 — 2026-09-06

- 用户最后澄清：提供 Smoke Test、最小 Timeout 验证与验收报告，不需要正式真实实验。此前 NOT CONFIRMED 针对重复加入 007 的范围，不再作为当前 002 的判断；原始设备、预检与隔离测试证据均保留。
- [scope-smoke.json](evidence/scope-smoke.json)：当前 OpenGUProjectExtension 的 38 个 recipe 全部经已安装 Core 验证，timeout_seconds、recipe、完整 Git SHA、配置 SHA 一致；60 个 Core payload 文件哈希通过。
- 同次 Smoke Test 的 12 项检查全部通过，3 个示例 Artifact 完成传输、SHA 校验、可信索引和导出，临时目录已清理。没有提交真实作业。
- [component-smoke.xml](evidence/component-smoke.xml)：15 项现有测试通过。其中临时持久化的 20 节点图实跑 Selector/Score/Selection、独立 GNNDelete 冷/热复用及独立 Metrics 读取；其余核对静态原子实验入口、配置、输出合同、GPU/旧输出拒绝。运行设备为 CPU，证据为软件 smoke，不是正式科研实验。
- [timeout-smoke.json](evidence/timeout-smoke.json)：实际安装的 Core 在临时干净 Git 仓库执行三个真实本地子进程。正常任务完成，配置 1 秒预算的任务触发超时且保存 failed 回执、子进程已退出、最终产物不存在；随后正常任务仍完成，最终队列 idle。没有 mock subprocess.run，没有远端作业；只验证直接子进程，不声称覆盖任意后代进程树。
- 5 份已有真实 summary 的 SHA 与已核验耗时索引一致；Score 基准与本轮访问、Selection 时间、GU 历史时间的含义已定位。作业级 timeout 不是逐组件首次测量预算；GU 访问和完整模型准备耗时仍有缺口，不宣称完整计时器或大图预估已完成。
- 设备真实观察及缺 GPU 注入拒绝复用前序有明确输入、源码、Core 和时间身份的证据；不因无运行代码变更而重复科研实验。007 正式启动仍需当时版本、设备、数据与配方检查。
- 当前请求范围内结果为 PASS，报告等待用户验收；通用 Core 的隔离异常发现保留为附带事实，不在此接手修复，不作为 002 的隐藏前置条件。

## 当前解释修正 — 2026-09-06

用户明确指出任务是 OpenGU 002，SM-001 不属于本轮。上一轮要求先处理 SM-001 的建议撤回。设备核查已有真实观察；上一轮并未新跑 OpenGU 最小任务，而是执行探测、现有 adapter 预检及隔离队列复现，因此不能宣称完整 002 已完成。

`ready` 由预检对真实 GPU、路径、依赖、数据及已有结果等条件的检查结果计算。当前 OpenGU adapter 会正常返回该字段；空对象样例是通用 Core 的受控异常测试。明确拒绝的隔离任务虽已入队，但执行前被 blocked，进程启动次数为 0，不能把它描述为“缺 GPU 仍开始实验”。原验收所要求的完整门禁链路尚未补齐观察，当前为证据不足，不能仅凭字段测试判定 OpenGU 实验失败或宣告通过。

## 历史核查与解释 — 由当前验收范围取代

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
- 2026-09-06：用户明确 002 负责字段/Smoke、007 负责最小正式实验，并在此条件下要求 accept；38 个 recipe 合同、已有耗时记录与 12 项 Smoke 核验通过，按同一 002 收口。
- 2026-09-06：用户随后纠正为先提供 Smoke Test、最小 Timeout 验证及验收报告；完成 15 项组件/入口检查和正常→超时→继续正常的真实子进程验证，暂停收口，形成待验收候选。
- 当前候选仅包含同一 item 内的说明、测试复现工具和证据；OpenGU 与 SyncMate 产品源码、实验 recipe、设备配置、历史数据/缓存未修改。当前 15 项检查及 3 个队列任务的产品代码检查点为 `0d2bbe1d250d91697d0cf1204e0b1eefc3e1a4b1`，测试脚本和证据哈希见 [source-manifest.json](evidence/source-manifest.json)。最终候选只核验新增报告、Record、证据完整性和渲染；通过后 Claim 转 awaiting_acceptance，等待人审阅。
- `accepted`（2026-09-06T06:24:43.9630555+08:00）：用户 基于 用户审阅 Smoke Test 与 Timeout 验收报告后明确：那可以 accept 了。接受同一 OpenGU AAGU-002 的设备、字段、CPU 组件 Smoke 和真实子进程 Timeout 验证；007 正式实验不在此次接受范围。 接受当前已验证候选。
