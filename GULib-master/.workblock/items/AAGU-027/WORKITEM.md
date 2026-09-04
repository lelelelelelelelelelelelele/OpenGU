# AAGU-027 · EXP · IF-family Collateral 重跑与双端证据验收

Block ID: `AAGU-027`
Item Version: 2.1
Item Type: `Block`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-027/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

在 AAGU-001 实验框图与公共合同、AAGU-009 软件修复分别完成并被接受后，按当前批准的实验定义重新生成 GIF/IDEA collateral 证据，完成双端运行、收集、完整性核验及独立研究证据验收。

### 本次增量

承接原 AAGU-009 中的 SSH 运行准备、正式重跑、旧结果可逆隔离、结果收集及验收责任。先消费 001 的实验组合表与 Dataset/Split、Selector、Unlearning 小表，审阅本轮研究问题、配置、矩阵、指标及证据接纳条件；定义被批准后才准备正式执行。历史 120 格只说明待处理旧证据的范围，不自动成为当前可执行矩阵。

本地负责软件与配置审阅、collector 配置、收集及 SHA-256/trusted read-back；SSH 活跃检出负责 runner 配置、正式 GPU 执行和原始产物。双方代码与执行身份、已持久化数据/划分和所需 Artifact 可追溯后，按获批范围运行并形成配对报告。SyncMate 只连接执行与证据，不决定科学定义或接受结论。

### 核心验收

- 001 的公共框架与 009 的软件修复均已被接受；本轮实验按 001 完成定义、登记和批准。记录三类配置引用、真实输入/划分、预算、模型、方法、种子、指标、代码与运行身份。
- 双端配置分别通过当前实际解释器读取验证，collector 指向正确 runner；正式 GPU、数据和共享运行前置及本实验 preflight 实际通过。SSH 可连接或文件存在不能单独算就绪。
- 历史证据按精确清单保留；如需隔离，先核对范围、路径与哈希，采用可恢复整叶操作，不删除、原地改写或使用 --force。Cache V2 Artifact 不被手工修改。
- 正式运行具有 job/recipe 回执和完整产物。若合同批准对旧删除请求做逐格替换，逐格核对 selected_nodes；若数据/划分/预算或选择语义改变，形成独立新实验身份，明确不可逐格等同，不能伪称原结果已修复。
- 收集后通过 SHA-256、trusted index、完整性及结果回读，证明本地报告对应远端同一批产物；旧污染数字仍不得作为已接受的新证据。
- 用户能基于同目录 REPORT.md / REPORT.html 明确接受、返工或拒绝本轮证据；通过测试、dry-run、进程退出或队列 done 均不自动构成研究验收。

## Confirmed acceptance contract

- Class: `EXP`；Priority: `P1` after prerequisites.
- Route: `formal`；Primary surface: `research evidence / local-SSH integration`；Decision owner: 用户。
- Minimum real evidence: 批准的当前实验合同、双端身份与 preflight、运行回执、完整产物、必要的历史隔离/对照清单、收集校验和可信回读。
- Report size: 配对 Markdown/HTML；登记阶段不创建空报告或执行证据。
- Post-candidate decision: Verify 后停在人类验收；没有自动 Apply、push、安装或清理授权。

## Source and relations

- Source anchor: 用户在本任务中要求“009 只修代码，跑实验和 SSH 部分移到新 Block”，并重申正式运行必须在 001 实验框图之后，015 同样遵守。
- `AAGU-027 depends_on AAGU-001`：消费已接受的公共框架，不能先跑旧 YAML 再补实验定义。
- `AAGU-027 depends_on AAGU-009`：使用已接受的软件修复。009 的软件回归可先进行，正式实验不可借用其 FIX 身份提前执行。
- `AAGU-010 depends_on AAGU-027`：010 的真实回读与汇总验收消费这里被接受的 collateral evidence。
- 015 的关系仍为 `AAGU-015 depends_on AAGU-001`。本轮若使用由 015 决定的 IF 科学定义，还须引用其已接受决定；不把 IF-family GU 与所有 IF selector 决策混成同一任务。
- AAGU-026 owns modular configuration/cache implementation. 若本轮合同需要尚未实现的能力，执行前须满足对应实现前置，不能回退旧路径绕过 001；不在这里提前代替本轮定义作判断。
- Graph placement: `experiments`。本 WorkItem 拥有本次实验范围和接受要求；编排位置由 WORKPLAN/Graph 表达。

## Historical scope and two-end observations

- 原提案范围为 Cora、r=0.05、GCN/GAT、GIF/IDEA、6 strategies、5 seeds，共 120 个旧 cell。原 source branch 的 repair-scope/preflight 仅作历史来源，不能直接作为当前矩阵或恢复命令。
- 本任务 2026-09-04 只读观察：本地 E:\project\OpenGU\GULib-master\.syncmate 下未发现 device.yaml；通过 E:\conda_package\envs\gnn\python.exe 调用项目 SyncMate self 时缺少 syncmate_core。此项说明该本地解释器的接入未验证，不推断其他环境均不可用。
- 同次只读观察：autodl-opengu 可连接，远端 /autodl-fs/data/OpenGU/GULib-master/.syncmate/device.yaml 存在。文件存在不代表内容、peer、解释器、GPU、数据或本轮运行身份已通过检查；旧的 SSH connection refused 不再作为现状沿用。
- 本地配置与远端配置分别拥有 collector/runner 身份，不能把一端文件存在投影为另一端已配置，也不能照抄配置掩盖角色差异。执行时须刷新上述观察。

## Scope and execution boundaries

- 本次仅注册，未 Claim、运行、隔离历史结果、配置双端、写 SSH、push 或部署。
- 在 001 和 009 接受前，不启动本 Block 的正式执行；本轮实验合同也须独立批准。001 的完成不是所有矩阵的统一批准。
- 保留既有数据/划分、Selection 与 Cache V2 的精确身份和证据边界；不得因旧配置存在便重新下载数据、改 split、清 cache 或扩大历史失效范围。
- 正式执行遵循 experiments/AGENTS.md 和当前注册 launcher；数据根为 SSH active checkout 下的 canonical processed root；无 GPU 时停止，不回退 CPU 冒充正式运行。

## Restart and next action

确认 001、009 的当前接受事实，读取它们的最新交付及本 Record；在后续执行任务中使用 block-workflow Claim 同一 locator。先按 001 形成并审阅本轮实验合同，再处理双端准备和正式 gate；获准运行后完成执行、收集与研究证据验收。保留 AAGU-010 的后续消费边界。

## Status history

- 2026-09-04: 按用户确认的修复/实验拆分注册独立 EXP；从 009 接收正式重跑和 SSH/收集责任，依赖 001 与 009，010 改为消费这里的接受证据。状态 registered / not claimed；未继承旧 Claim、旧运行批准或历史结果的可信身份。
