# AAGU-007 · EXP · 最小正式实验 Gate（Target-Direct）

Block ID: `AAGU-007`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

作为本轮正式实验的共同起点，在 AAGU-002 设备就绪且 AAGU-034 公共入口修正已接受后，先完成并接纳最小的 Target-Direct 端到端实验，证明当前科学定义、设备条件和证据链足以支撑一条真实正式运行路径。007 先于 031 Selector 大组、后续 GU 矩阵、修复重跑与正式计时实验。

### 本次增量

消费 AAGU-015 已接受的 Selector 定义、AAGU-028 的独立 GU/Retrain 与离线 Metrics 能力及 AAGU-002 的设备就绪证据，按获批 Target-Direct 配方运行最小切片，核对 Selector → Score/Selection → 独立 GU/Retrain 输出 → 收集与离线指标比较。把源码/数据身份、产物、来源链和解释边界收敛为独立证据包；不重新决定 IF 科学定义，也不运行完整矩阵。

007 验证一条最小正式运行链；031 消费该 gate 后执行 015 的 306-cell Selector 范围与 Q1–Q4 分析。007 不依赖 031 的全量结果，不要求 030 完成总表；后续任务只复用身份仍有效且确实覆盖其入口的证据，并自行完成方法、输入和成本检查，不将一个 Target-Direct 小切片说成所有专题均已验证。

### 核心验收

- gate 使用获批实验配方与明确的源码/数据身份，运行产物和来源链能逐项回溯。
- 人能够区分正式 gate 证据与 smoke、配置预检或后续矩阵扩展，不把前者之外的状态写成科研接受。
- 用户基于真实证据明确接受、返工或拒绝该 Target-Direct gate，之后才允许继续扩展实验矩阵。
- 明确交接给 031、后续 GU/重跑与计时路线的已验证环节、Artifact/输出引用和未覆盖条件；不以 smoke、CPU 软件验证或历史 SyncMate 小作业替代本轮正式 gate。

## Orchestration contract

- Class: `EXP`
- Priority: `P0` after experiment-definition and device gates.
- Source anchor: legacy target-direct experiment Todo.
- Outcome: run and accept the smallest authorized Target-Direct end-to-end gate before the current research experiment branches expand.
- Fact owner: [007 ordinary experiment](../../../experiments/configs/aagu007/experiment.yaml); OpenGU DocMap remains scientific framing and historical navigation only.
- Dependencies are projected by WORKPLAN, not copied into lifecycle status.
- Prerequisites: AAGU-002、AAGU-015、AAGU-028、AAGU-034；001/006/026/009 的已接受基础从这些前置继承。
- Downstream: AAGU-031、后续 GU 矩阵与 AAGU-027 等正式研究路线；方案整理和隔离 CPU 软件验证不因本 gate 而阻塞。

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `research evidence`.
- Minimum evidence: approved recipe, pinned source/data identity, authorized gate artifacts, provenance, and explicit human decision.
- Confirmation: deferred until claim/real execution under the user's delegated registration authority.
- Report size: decide at claim.

## Boundaries

- No selector/IF decision in this Block; consume only an independently approved scientific definition.
- Do not choose a split or deletion budget from historical public-split, fixed-small-k, or 80/20 evidence; the registered recipe and its verified profile are the only executable authority.
- No GPU execution is authorized by registration.

## Status history

- 2026-08-26: registered from the prominent target-direct experiment Todo.
- 2026-09-06：用户要求 007 位于所有实际实验之前，并明确与 031 的关系；沿用同一编号与 Target-Direct 最小正式范围，改为共同实验入口。仅修正合同与编排，保持 registered / not claimed，未启动作业。

## 公共配置与入口修正前置 · 2026-09-06

- 根据用户本轮要求，新增 `AAGU-007 depends_on AAGU-034`。034 独立修正公共配置与执行入口并迁移旧 V2 注册；007 消费其接受后的统一路径完成最小正式验证，不能继续按本记录中的历史 V2 启动说明直接执行。既有科学范围、设备/数据条件、输出核验与其他前置继续有效。
- 事实 owner：[AAGU-034 修正合同](../AAGU-034/WORKITEM.md)。本次只更新前置和编排，007 的 registered / not claimed 生命周期不变，未启动作业。

## AAGU-034 接口迁移

当前配置引用公共小表，登记入口为 `opengu-aagu007-v1`，同一普通表展开4个独立方法输出。034 已接受并合入；正式运行仍须审阅本轮配置/运行。本次仅更新基线，没有Claim007或运行实验。历史formal-v2原文已移入配置档案，不再是本轮执行入口。

## 034 收口后的执行基线 · 2026-09-07

- 本次核查源码为 main `7e488c0d9c44f1c8892b427907d834be4b76f9ef`（034 合入点）；这是文档核查快照，后续 Claim/提交必须重新绑定实际源码、配置指纹及数据身份。
- 当前科学切片为 Cora、70/10/20 划分（split seed 2024）、Degree 1%、训练 seeds `[122, 722]`、独立 GNNDelete 与 Retrain，共4个方法输出。旧 formal-v2 的双预算不再作为本轮执行依据；本次不改变当前组合表的科学范围。
- 统一执行链为 `experiments/run.py → modular_config → modular_run`；SyncMate recipe 调用 `experiments/run.py experiments/configs/aagu007/experiment.yaml --run-id aagu007-v1`。Selector 只声明 `selector_refs`，运行时自动解析实际 Score/Selection 与缓存复用，禁止手填旧 Selection。后续 Metrics 绑定真实 Output，按同 seed 比较 GNNDelete 与 Retrain。
- 034 的软件接受包含统一配置、独立输出、分阶段核验和当前交付范围修正；不等于007真实SSH/GPU、正式数据、成本或科研gate已验证。运行前按当前 [Core依赖绑定](../../../scripts/syncmate/CORE_DEPENDENCY.md) 核对实际解释器及安装载荷，不把034旧记录中的部署快照当作当前状态。
- **剩余配置差异：固定公共目录识别。** [理想稿](IDEAL_CONFIG.md) 已约定四类引用只写文件名，由字段定位 `experiments/configs/{datasets,selectors,unlearning,evaluations}/`。当前解析器仍基于组合表父目录解析，正式表仍写 `../datasets/cora.yaml` 等相对路径；该便捷引用规则尚未实现，不能称为034已交付能力。
- 后续目录修正应同步覆盖解析、引用指纹/注册、活动配置和来源记录；验证从不同组合表位置得到同一公共实例及有效配置，并拒绝缺失或越界引用。不引入旧相对路径兼容分支，不改变算法、预算、seed或手改历史Artifact。完成后再审阅007最终配置。
- 本轮仅更新同一007的基线与剩余工作说明，保持 `registered / not claimed`，未授权或启动正式作业。
