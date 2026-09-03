# AAGU-025 · FIX · 通用缓存原位接入 Cache V2

Block ID: `AAGU-025`
Item Version: 2.1
Item Type: `Block`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/main`

> Git baseline：`7a2c11fb06cff01363d7773c446370e1588ade4a`

> Source branch：`refs/heads/codex/aagu-025-unified-cache-v2`

> Remote target：`origin refs/heads/main`
当前状态: `accepted`
Stable locator: `.workblock/items/AAGU-025/WORKITEM.md`

## Human Surface

### 核心意图

保留正常的缓存能力，让通用执行与正式执行统一使用 Cache V2，不再依赖 `results/cache`、`results/selection_cache` 和 `results/score_cache` 三个 Legacy 活动目录。ScoreCache 的存在与默认开启不是缺陷；需要修复的是原有缓存能力尚未原位升级到统一的 V2 入口。

### 本次增量

将通用 AttackManager、Result／Selection／Score 消费者及原有配置和调用逻辑接入既有 Cache V2 Recipe／Artifact 合同，保持正常默认缓存能力。移除旧后端选择、Legacy 读写和自动建目录路径，不新增 Legacy/V2 双轨开关、兼容回退或另一套缓存体系；不以关闭 ScoreCache 或禁止正常缓存代替修复。现有缓存开关控制统一缓存能力，其语义必须一致。

### 核心验收

在隔离环境通过真实入口验证默认缓存可用、冷启动精确 MISS、再次精确 HIT，以及身份不匹配时拒绝复用旧 Artifact。正常执行不读取或重建三个 Legacy 根，通用与正式执行的相关回归通过，现有缓存开关语义一致。真实旧 payload 与现存 Cache V2 Artifact 的路径和内容均保持不变；以配对 Markdown／HTML 报告提供 behavior / integration / data 证据，由用户决定接受或返工。

## Scope

- 更新通用 AttackManager、Result／Selection／Score 消费者及相邻 CLI、YAML 配置和执行入口，使原有缓存能力默认消费既有 Cache V2 身份与证据合同。
- 处理上述消费者实际依赖的适配与调用链，移除 Legacy 后端选择、回退、读写及目录创建逻辑；不通过新增模式开关保留两套实现。
- 保持 Cache V2 的现有职责边界：Cache 负责精确 Recipe／Artifact 解析、校验与存储，实验层负责输入身份和 MISS 后的计算，不把数据加载或实验计算移入 Cache。
- 为默认执行、缓存开关、冷／热缓存、身份拒绝和 Legacy 路径不再出现建立确定性回归，并验证通用与正式入口的集成行为。
- 更新受影响的代码说明和测试；形成精确候选及同一 item directory 内的配对报告。

## Non-goals

- 不移动、删除或改写任何真实本机／SSH 旧 payload；物理归档仍属于 AAGU-023。
- 不修复、重命名、覆盖或手工删除现存 `results/cache_v2` Artifact，不把旧 payload 无依据地转换为可信 V2 证据。验证使用隔离的临时 Artifact store。
- 不重跑正式 GPU 实验，不改变正式研究的矩阵、数据划分、删除预算或指标定义。
- 不以关闭正常缓存、仅替换目录字符串、新增 Legacy/V2 选项或兼容回退满足验收。
- 不在本 Block 中重写 AAGU-023 的 inventory、ledger 或报告，也不据此宣称旧证据归档完成。

## Acceptance contract

- Route: `formal`。
- Primary surface: behavior / integration / data。
- Minimum real evidence: 隔离环境中的真实消费者冷／热执行、精确 Recipe／Artifact 身份与 HIT/MISS 证据、身份不匹配拒绝复用证据、现有缓存开关行为、三个 Legacy 根的访问／创建检测、通用与正式入口的相关回归，以及真实旧 payload 和现存 V2 Artifact 未改动证明。
- 构造器测试或静态引用扫描只能支持其局部判断，不能代替完整消费者的缓存读写与身份验证。
- Decision owner: 用户。
- Post-candidate decision: 形成 clean exact candidate，完成约定 Verify 与报告后停在 `awaiting_acceptance`；Verify PASS 不自动接受或 Apply。
- Report size: paired Markdown/HTML Report，位于同一 Block item directory。

## Source and relations

- 来源是 AAGU-023 候选 `2f9dd79d19a81b91c1b3ec7aeaba0b03245f8996` 的人类审阅与后续通用入口诊断，不是已经接受的归档结论。
- 诊断时本地主线为 `15e4bb06837e52b79ae5a251cef2633510da2b58`。临时目录中的真实构造器测试观察到：通用默认初始化创建三个 Legacy 根；仅关闭 `use_cache` 仍创建 ScoreCache 根；V2 路线同时关闭两类开关才不创建旧根。该测试未加载数据或运行训练，不构成本 FIX 的完成证据。
- 用户明确纠正：缓存默认开启和 ScoreCache 本身均正常；原有能力应更新为默认接入统一 V2，而不是新增路径选择或关闭能力。本 Block 以此为修复方向。
- 已确认依赖：`AAGU-023 depends_on AAGU-025`，具体约束是旧 Cache 归档闭环需要消费本 FIX 已接受并落地的修复，证明旧活动路径不再被依赖或重建；AAGU-023 的只读盘点不因此暂停。
- AAGU-025 不依赖 AAGU-023 完成。AAGU-023 的证据分类、报告纠正及物理归档仍保留在原 Block，代码修复由本独立 FIX 验收。

## Boundary

以下保留注册时授权边界；当前 Run 由本任务另行明确授权，当前状态以顶部字段与同一 Claim 为准。

- 本次只注册独立 FIX Block，未 Claim、未实施，未创建后续 Codex task。
- 后续通过 `block-workflow` 重新读取当前 Record、仓库事实和项目指令，Claim 同一 Block 后实施；Claim 时重新确定实际基线和执行身份。
- 注册不授权远端写入、正式 GPU 执行、payload 归档或删除、接受、Apply、推送或安装。

## Run boundary

- Parent: `refs/heads/main`; source: `refs/heads/codex/aagu-025-unified-cache-v2`.
- Owned scope: `attack/` cache consumers and identity adapters, `cache_v2/` required typed-payload integration, `demo_attack.py`, `eval_collateral.py`, `parameter_parser.py`, affected `experiments/` consumer/config paths, directly dependent prewarm/monitor/Legacy conversion scripts, adjacent tests/docs, and this item directory.
- Checks: isolated real consumer cold/hot execution, complete identity rejection, cache switches, forbidden Legacy root access, generic/formal regression, and before/after real cache file manifests.
- Closeout mode: `commit`; stop at `awaiting_acceptance`.

## Verify and Report

- Decision: `待决定`；Agent 建议接受此次软件接入，用户尚未作出决定。
- Candidate: 当前源分支的干净 HEAD，包含本 Record、配对报告及证据；精确 OID 和已测检查点之间的差异复核见 [最终候选核验](../../runtime/aagu025-final-verify.json)。
- 已测检查点：`ab005b66a5a1c8e415a62f8e549629af480d6d51`。干净候选上的 293 项相关回归通过，通用配置 dry-run 展开 180 个 cell；修改 Python 的 AST 解析及 diff check 通过。
- 真实消费者证据：隔离 CPU 合成输入经生产 AttackManager、demo CLI、策略、V2 store/resolver 和 pipeline 编排完成冷/热与正式 Artifact 接入；具体 GU 方法及数据准备使用测试夹具。这是软件接入验收，不是正式 GPU 研究结果。
- 身份与保护：冷/热复用同一 Artifact；图、特征、标签、候选集、划分、模型与种子变化后拒绝旧结果；开关组合、损坏拒绝、冲突隔离与 Legacy 文件访问审计通过。本机四个真实缓存根的 75 个文件路径、大小及 SHA-256 前后一致，未访问 SSH 或运行正式 GPU 实验。
- 配对报告：[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)，由 [render_report.py](render_report.py) 从本 item 证据生成；桌面与窄屏已实际查看，结构检查通过。
- 报告后续提交仅完成本 item 的 Record、报告和证据；按最终实际 diff 复核其不会改变已验证的产品行为后，复用上述检查点结果，并单独验证报告生成、链接和显示。
- Run 在同一 Claim 的 `awaiting_acceptance` 停留。未执行接受、Apply、Remote、Install、清理或 AAGU-023 物理归档。

## Authorized delivery setup

- 2026-09-04: 用户明确接受软件候选 `0501316e1774985d3339e14ea3693fd5e3c022e3`，并要求 SSH 同步安装、尝试补齐 `install.json`。此授权追加 `.workblock/actions/install.json` 与 `.workblock/policy.json` 的最小安装配置，保留本 Block、父线和原软件验收合同。
- 安装目标：`autodl-opengu:/autodl-fs/data/OpenGU` 的唯一活跃 main 检出；本次仅同步已落地源码并核验完整文件身份，不进行环境 bootstrap、实验执行或 payload 处理。
- 配置验证：project-installer envelope 校验、真实 SSH 路径/分支/干净状态检查；安装后核对三方 SHA、全部 tracked 内容、缓存保护清单及变更 Python AST。
- 原回归证据继续绑定 `ab005b66a5a1c8e415a62f8e549629af480d6d51`；部署配置不改变已验证的软件行为。用户的接受决定由 Closeout 统一写回当前投影。

## Status history

- 2026-09-03: 用户确认 AAGU-025 完整形成预览并回复“可以注册”；注册为 formal、sequential 的独立代码 FIX，状态保持 `registered / not claimed`。

- 2026-09-03: 按当前任务授权，Claim 同一 Block（claimId `2c1c77d4-4401-4397-8126-a24303fe598a`），在记录的 main 基线上实施；仅形成候选、Verify 与报告，等待用户验收。

- 2026-09-03: 完成统一 V2 接入、干净代码检查点 Verify 与配对报告；当前投影为 `awaiting acceptance`，决定保持 `待决定`。最终报告候选复核后，同一 Claim 转为 `awaiting_acceptance`，按用户要求停止。
- `accepted`（2026-09-04T05:01:19+08:00）：用户 基于 用户明确接受已验证软件候选 0501316e，并授权补齐 install.json、在 SSH 同步安装；交付配置候选 5b19532b 已完成独立配置与报告差异核验。 接受当前已验证候选。
