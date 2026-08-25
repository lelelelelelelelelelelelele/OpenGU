# AAGU-001 · FIX · Experiment Definition and Registration Contract

Block ID: `AAGU-001`

当前状态: `registered / not claimed`

Item Type: Block

## Block human acceptance surface

### 当前基线
OpenGU 的正式实验方向、实验入口和 SyncMate 工程连接已有局部事实，但科学 owner、recipe、矩阵、acceptance gate 与工具职责边界尚未在一个正式注册块中闭合。

### 这次增量
把 OpenGU 的正式实验定义与 SyncMate 的执行/证据连接点收敛成一个可审阅合同；研究定义链接到 OB owner，SyncMate 只提供通用执行边界与证据连接。

### 完成后人会看到什么
一份可批准的正式实验定义入口，明确配置、矩阵、recipe、验收门、证据接纳条件和 SyncMate 的连接边界。

### 验收项目
- 各正式实验节点的研究问题、变量、矩阵和 recipe 可以从唯一 owner 逐项确认。
- 科研 claim、实验执行、设备就绪、证据接纳与 SyncMate Core/adapter 的责任边界清楚分开。
- 计划能够进入 OpenGU 的注册执行链，并明确什么只能算 smoke、什么才可进入 formal acceptance。

### 主要证据
- OpenGU 实验指令、当前 OB 计划和配置入口：判断科研定义是否完整。
- SyncMate M1、Device Contract 与 consumer 边界材料：判断工具连接是否越界。
- 注册后的 dry-run/recipe/matrix 证据包：判断定义是否可执行，而不是把 dry-run 当成实验结果。

### 关键 non-goals
- 不运行正式 GPU 实验。
- 不把 SyncMate 变成科研 claim 或 acceptance 的决定者。
- 不在本 Block 内实现 Device Readiness、FlowChunk adapter 或产品化增强。

### 需要人的决定
AAGU 研究负责人确认各正式实验 owner、注册矩阵、acceptance gate 和 SyncMate 连接边界；结果尚未观测。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 用户已确认按 AAGU 重新登记并保留既有任务合同。
- Primary surface: `research definition / integration contract`
- Minimum real evidence: 可审阅的实验定义、recipe、矩阵、gate 和 dry-run；这些只能证明计划可执行，不证明正式实验已接受。
- Post-candidate decision: AAGU 研究负责人必须明确批准、返工或拒绝该实验定义。
- Report size: paired Markdown/HTML report after Verify.

## Context and relations

- Blueprint scope: 当前 OpenGU OB 实验入口与目录级 AGENTS；没有额外稳定 Graph/Blueprint ID，故不虚构节点。
- Suggested relations: `AAGU-002 depends_on AAGU-001`；`AAGU-003 depends_on AAGU-001`。理由是设备验收和正式执行都必须消费已批准的实验定义。
- Cross-project references: SyncMate SM records are implementation companions, not duplicate scientific acceptance records.

## Runtime and authorization boundaries

- Registration only; no claim, implementation, experiment dispatch, GPU run, push, install, or external write.
- Future execution must use the OpenGU active checkout and experiment-specific AGENTS; local dry-run is not formal GPU acceptance.
- Current runtime candidate, branch, evidence identity, and report identity are not yet formed.

## Restart and next action

Use `block-workflow` to claim this exact WorkItem only in a later execution task. First reread this Record, the current OpenGU experiment instructions, and the SyncMate boundary documents; then form the experiment-definition candidate and stop at the formal human decision gate.
