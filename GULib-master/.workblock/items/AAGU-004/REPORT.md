# AAGU-004 · FlowChunk Second-Consumer Robustness D0

> 当前验收决定：`待决定`

报告事实日期：2026-08-24 · AAGU 身份重绑定：2026-08-25 · 报告新鲜度：本轮只读复核

## 这次改变了什么

本轮只完成 FlowChunk 作为 SyncMate 第二 consumer 的 D0 边界审计，并在本
WorkItem 目录生成这份 canonical Markdown/HTML 报告。没有修改 FlowChunk、
`.gitmodules`、submodule、dirty files、远端状态，也没有运行 GPU、SSH、训练、
rollout、评测或正式实验。

## 现在实际看到了什么

FlowChunk 当前 checkout 为 `exp/unified-a2a-vita`，`HEAD=83df11bc6c98097de316a94a5bceb74ff2079668`。工作树有 26 条既有状态项：2 条 staged、3 条已跟踪文件修改、21 条 untracked；其中 staged 的 `.gitmodules` 使用本机路径 `E:/project/SyncMate`，staged `scripts/syncmate` gitlink 为 `e57c8536e7dbccb0ae75b82b8c6f44db885ce62c`。本轮保留这些状态。

当前独立 SyncMate checkout 的 `HEAD` 与 `origin/main` 都是
`ccf69fc2e1a7beff492a83cbb2b900c1f03c5a4c`，但其工作树也有既有修改和未跟踪
内容；这个工作树状态不被当作可发布 pin。本轮没有调整 pin 或发布方式。

SyncMate Core 已提供 consumer-owned 的 recipes、artifact names、preflight、
acceptance 和 results 扩展面，并且 source scan 未发现 FlowChunk/OpenGU 专属
语义泄漏。可是 FlowChunk 当前 submodule 仍是 generic profile：测试/说明只证明
generic `smoke` 和通用 artifact transfer；没有 FlowChunk-owned adapter、正式
recipe registry、项目 preflight、acceptance parser 或 metric parser。

FlowChunk 自身已有可供未来 adapter 消费的 evidence 基础：配置通过
`FLOW_DATA_ROOT`、`FLOW_CACHE_ROOT`、`FLOW_RUN_ROOT` 注入；Gaussian Flow 的
train/rollout/evaluate 入口写出 `manifest.json`、`resolved_config.json`、
`metrics.json`、trace/checkpoint，并保留 Git/provenance 字段。问题是这些 run
位于外部 `FLOW_RUN_ROOT`，而当前 SyncMate Core 的 recipe config 与
`expected_artifact_paths` 强制 repository-relative、固定安全路径；本轮没有
观察到已批准的 staging 或受限 artifact channel，也没有把外部 run 接入可信
收集链。

## 最关键的证据

| 证据 | 观察 | 判断 |
|---|---|---|
| FlowChunk baseline | `E:/project/flow-chunking-smoothness`；branch `exp/unified-a2a-vita`；`HEAD=83df11b...`；26 条既有状态项；staged `.gitmodules`/gitlink 保持原样 | `PASS`（只读基线记录） |
| Pin/deployment boundary | FlowChunk staged gitlink=`e57c853...`；独立 SyncMate=`ccf69fc...`；submodule URL=`E:/project/SyncMate` | `NOT CONFIRMED`（不可作为已闭合的跨机器集成基线） |
| Core contract | `E:/project/SyncMate/syncmate_core/project.py` 提供扩展面；`contracts.py` 将 config/artifact path 限定为安全 repository-relative 路径和固定 recipe tuple | `PASS`（Core 边界静态审计） |
| Consumer readiness | FlowChunk `scripts/syncmate/README.md` 与 generic tests 只暴露 `smoke`；`docs/VLA_ADAPTER.md` 是 adapter 要求说明，不是已实现 adapter | `NOT READY` |
| Artifact channel | FlowChunk 的 manifest/provenance 基础存在；正式 run 使用外部 `FLOW_RUN_ROOT`，未观察到 repo 内 staging 或显式、可校验的外部 channel | `NOT READY` |
| Runtime/integration acceptance | 本轮没有执行 SyncMate transfer、recipe、preflight、GPU 或 formal run | `NOT OBSERVED` |

主要来源：

- FlowChunk 规则：`E:/project/flow-chunking-smoothness/AGENTS.md`、
  `src/flowchunk/AGENTS.md`、`configs/AGENTS.md`、`experiments/AGENTS.md`、
  `scripts/AGENTS.md`。
- FlowChunk evidence：`BLUEPRINT.md`、`configs/compute/*.yaml`、
  `configs/experiment/smoke_local.yaml`、`experiments/gaussian_flow/README.md`、
  `src/flowchunk/artifacts/manifest.py`、`scripts/validate_gaussian_flow_*.py`。
- SyncMate contract：`E:/project/SyncMate/AGENTS.md`、`README.md`、
  `syncmate_core/contracts.py`、`syncmate_core/project.py`、`syncmate_core/runner.py`。
- 历史上下文（不是本 WorkItem 的报告）：
  `E:/project/SyncMate/reports/syncmate_d0_flowchunk_robustness_REPORT.md`，
  2026-08-05，结论同为 D0 scoped PASS / D1 adapter NOT READY。

## 判断详情

### 1. Core、consumer adapter 与责任边界 — `PASS`（scoped）

在审计 SyncMate Core 与 FlowChunk consumer 入口时，审计者期待看到通用 Core
只负责证据转移、校验、trusted index/export，并把 recipe、preflight、acceptance
和结果语义交给 consumer。实际观察到 `ProjectExtension`/`ProjectAdapter` 扩展面，
generic preflight 返回未实现、generic acceptance 为 `not_evaluated`，且 Core
source scan 未发现 FlowChunk/OpenGU 专属语义。因此 Core/consumer 责任边界的
静态判断得到支持；这不等于第二 consumer 已集成或接受。

主要证据：`E:/project/SyncMate/syncmate_core/project.py`、
`E:/project/SyncMate/syncmate_core/contracts.py`。

### 2. FlowChunk adapter、recipe、preflight、parser — `NOT READY`

在审计 FlowChunk 当前 `scripts/syncmate` 时，审计者期待看到一个由 FlowChunk
拥有的 reviewed static recipe、项目 preflight、acceptance predicate 与只读
trusted-index parser。实际只观察到 generic profile 的 `smoke`、通用 artifact
policy 测试，以及 `docs/VLA_ADAPTER.md` 中的设计要求；没有对应的 FlowChunk
实现文件。因此 D1 adapter 的最小实现条件尚未具备。

主要证据：`E:/project/flow-chunking-smoothness/scripts/syncmate/README.md`、
`scripts/syncmate/docs/VLA_ADAPTER.md`、
`scripts/syncmate/tests/test_syncmate_generic.py`。

### 3. Pin、dirty state 与本机 submodule path — `NOT CONFIRMED`

在审计当前 checkout 时，审计者期待看到可跨机器复现的、已闭合的 SyncMate
依赖身份。实际观察到 FlowChunk 的 staged gitlink 为 `e57c853...`，独立
SyncMate `HEAD=origin/main=ccf69fc...`，且 `.gitmodules` 使用本机路径
`E:/project/SyncMate`；FlowChunk 与 SyncMate 两边都存在既有 dirty/untracked
状态。因此不能把当前状态写成“已完成跨机器集成基线”。本轮没有清理、重置、推进
gitlink 或替换 URL。

主要证据：两侧 `git status --porcelain=v1`、`git rev-parse HEAD`、
`git submodule status`、FlowChunk staged diff。

### 4. Artifact channel 与外部 `FLOW_RUN_ROOT` — `NOT READY`

在审计证据通道时，审计者期待看到 FlowChunk 生成的最小 evidence 能以固定、可
校验的路径进入 SyncMate trusted chain。实际观察到 FlowChunk 的 manifest、
resolved config、metrics、trace/checkpoint 和 provenance 结构已存在，但运行根
目录由 `FLOW_RUN_ROOT` 指向 checkout 外部；SyncMate Core 的 recipe contract
拒绝绝对路径、`..` 和非 repository-relative artifact path。因此当前只能说
FlowChunk 有 adapter 输入基础，不能说外部 artifact 已可安全收集或已被可信索引。

主要证据：`E:/project/flow-chunking-smoothness/BLUEPRINT.md`、
`configs/compute/local_5070.yaml`、`experiments/gaussian_flow/README.md`、
`src/flowchunk/artifacts/manifest.py`、
`E:/project/SyncMate/syncmate_core/contracts.py`。

### 5. 人的 D0 / D1 go-no-go 决定 — `NOT OBSERVED`

在当前报告生成阶段，AAGU 研究负责人尚未对 D0 是否充分、是否要求返工，以及
是否允许另立 D1 implementation WorkItem 作出决定。因此本报告只能提出建议，不能
写入接受，也不能把任何 D1/SM-002 动作视为已授权。

## D0 verdict 与 Agent 建议

**D0：`PASS`（scoped review complete）。**

本轮已经完成 WorkItem 要求的只读边界核对：Core 的通用责任边界、FlowChunk
当前 pinned/dirty/local-path 状态、consumer 缺口和外部 artifact contract 均有
可复核观察。这个 verdict 只表示 D0 审计本身足够进入人的判断，不表示 FlowChunk
已接入 SyncMate，也不表示科研实验或正式 evidence 已接受。

**D1 adapter：`NOT READY`；当前实现 go/no-go：`NO-GO`。**

最小下一步不是直接写 adapter，而是由人先决定并固定：

1. 可移植的 Core pin/install 方案；
2. FlowChunk 小型 evidence 的 repo 内 ignored staging 或显式、受限、可校验
   artifact channel；
3. 第一批 recipe 范围（建议先 validation/rollout/evaluation，不默认包含 training）；
4. 每个 recipe 的固定 argv、config SHA、Git policy、timeout、expected artifacts
   与 machine-checkable success predicate。

本轮没有创建、claim 或执行任何 SM-002/D1 WorkItem；本报告不构成其授权。

## 验收决定

- 状态说明：尚未观察到人的决定。
- 需要决定：AAGU 研究负责人是否接受这份 D0 scoped report；若接受，是否另行
  授权一个独立 D1 adapter WorkItem。
- 决定对象：D0 只读审计的充分性、D1 当前 `NO-GO` 建议及上述最小前置设计。
- 决定依据：待人填写；Agent 建议不替代人的决定。
- 决定时间：

## 已知缺口与边界

- 尚未观察或确认：FlowChunk-owned adapter、reviewed recipe registry、项目
  preflight、acceptance predicate、metric parser、外部 run root 的安全 staging/channel。
- 尚未执行：SyncMate transfer/verify/index、FlowChunk recipe/preflight、GPU、SSH、
  train、rollout、evaluation 或 formal experiment。
- 本次不判断：FlowChunk 科研质量、模型效果、训练性能、正式实验 gate、远端部署、
  Core 发布接受和任何 D1 实现结果。
- 既有 dirty/untracked 状态属于用户资产；本轮没有清理、覆盖、移动或解释为本轮产物。

## 下次接手

- 当前状态：AAGU-004 已完成 D0 只读审计与配对报告，等待人的 go/no-go 决定。
- 已确认变化：只增加本 WorkItem 的流程/报告事实；FlowChunk 与远端状态未变。
- 下一步：由 AAGU 研究负责人选择 `接受 D0`、`返工 D0` 或保持等待；只有明确授权
  后，才另行创建/claim D1 implementation WorkItem。
- 不要重复：不要把旧 D0 报告当作本 WorkItem 报告；不要把 generic smoke、静态
  Core PASS 或本报告写入当作 FlowChunk 集成接受；不要 claim SM-002。
- 关键入口：本目录 `WORKITEM.md`、`REPORT.md`、`REPORT.html`；历史报告
  `E:/project/SyncMate/reports/syncmate_d0_flowchunk_robustness_REPORT.md`。

## 技术附录

- WorkItem：`E:/project/OpenGU/GULib-master/.workblock/items/AAGU-004/WORKITEM.md`
- Report：本目录 `REPORT.md` 与 `REPORT.html`；两者由同一份 D0 事实生成。
- Implementation candidate：无代码实现 candidate；本轮 identity 是
  `AAGU-004-D0-read-only-20260824`，绑定 FlowChunk `83df11b...`、gitlink
  `e57c853...`、SyncMate `ccf69fc...` 与本轮 status/diff/source scan。
- Evidence run：静态读取审计；无 runner job、GPU run、SSH run 或 artifact transfer。
- Verify 命令类别：`git status --porcelain=v1`、`git rev-parse`、`git submodule status`、
  `git diff --cached --summary`/`.gitmodules`/gitlink、`rg` 源码/配置扫描、只读文件读取。
- Side effects：仅写入本 WorkItem 的流程事实与配对报告；没有 FlowChunk、SyncMate
  runtime、远端、submodule object 或实验 artifact 写入。
- HTML 渲染检查：`PASS`（AAGU 身份重绑定后使用 Microsoft Edge headless，
  1440×1000 首屏与 1440×4400 全页均已目视检查；标题、当前决定、证据表、决定区和
  技术附录可见，无明显溢出、断图或破损内容）。
