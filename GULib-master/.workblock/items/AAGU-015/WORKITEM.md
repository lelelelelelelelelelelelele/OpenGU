# AAGU-015 · EXP · Selector 两阶段实验与证据

Block ID: `AAGU-015`

Item Version: 2.1

当前状态: `awaiting acceptance`

Item Type: Block

Stable locator: `.workblock/items/AAGU-015/WORKITEM.md`

Acceptance Route: `formal`

Execution topology: `parallel`

> Apply target ref：`refs/heads/main`


> Git baseline：`19b3b865ba617ed0216ae43c0ea2225731290de8`

> Source branch：`refs/heads/codex/aagu-015-selector-evidence`

> Remote target：`origin refs/heads/main`
## Human Surface

### 核心意图

将当前阶段的 IF/GIF Selector 研究问题整理成可审阅的实验方案，落实为真实 YAML，并核对每项实验与已有执行能力的对应关系。用户验收的是本阶段的实验定义材料：方案清楚、配置一致、入口及缺口明确。015 不规划所有未来实验，不承担整套执行框架或所有缺失能力的开发，也不要求跑完矩阵。

### 本次增量

交付本 WorkItem 下的 [实验方案](EXPERIMENT_PLAN.md)、[能力覆盖说明](CAPABILITY_COVERAGE.md) 和配对报告，保留并核对已经生成的 449 份 YAML。阶段 S 明确三数据集、17 Selector、三训练 seed、两预算的 Q1–Q4 比较、控制和指标；阶段 U 说明固定 Selection、GNNDelete/GIF、重训练参照和 Metrics 的关系。

“链路”在本次交付中指方案到配置、配置到已有入口的映射与检查。026 拥有已接受的模块化执行代码，SM-005 拥有工具工作链验证，015 不重复它们。当前不受支持的 Retrain 独立方法、评价或运行绑定逐项标为缺口，不用占位配置或历史结果冒充完整可执行。

### 核心验收

- 当前阶段的实验方案明确 Q1–Q4、比较对象、控制变量、数据/划分、seed、预算、模型/方法配置、指标输入和解释边界；不预写科研结论，也不扩展为所有未来实验计划。
- Dataset/Split、17 Selector、两种 GU 和 Evaluation 均对应真实 YAML，实际入口可解析并无写入展开为 306 个 S cell / 612 个 U cell；默认值、来源和共享依赖可复核。
- 覆盖表逐项指出已有入口、实际支持、尚未验证和缺失能力。明确 modular、target-direct、通用评估及 SM-005 的差别；不能把“代码存在/配置可解析”写成全方案运行通过。
- 说明真实输入与 Selection 的后续绑定、执行与 Metrics 的职责、证据复用和运行边界。独立 Retrain 的登记/实现核对有源码依据；未支持的需求不伪造 YAML、不自动建立实现 Block。
- 配对 Markdown/HTML 报告与方案、配置、覆盖表一致，用户可据此决定接受或返工。验收不要求全量实验、正式成本或科学结果；能力缺口的明确记录不等于这些能力已实现。

## Confirmed acceptance contract

- Class: `EXP`；Priority: `P0`。保留既有分类，不据此扩大运行或代码范围。
- Route: `formal`；Primary surface: current-stage experiment design, YAML and capability coverage；Decision owner: 用户。
- Minimum real evidence: 完整阶段方案、实际配置展开、源文件/入口审阅、缺口核对和配对报告。已有精确检查点的未变消费者测试可复用。
- Report size: 同目录 Markdown/HTML。
- Confirmation source: 用户明确“实验方案文档、对应 YAML、能力覆盖说明与配置检查”后要求“那你做那倒是做呀”；当前阶段即可，不要求所有未来方案。
- Post-candidate decision: Verify 后停在人类验收；接受方案不自动授权 GPU、全矩阵、Apply、push、安装或清理。

## Experiment design scope

- 具体方案由本次 [EXPERIMENT_PLAN.md](EXPERIMENT_PLAN.md) 绑定实际 YAML，理论来源链接至 DocMap，历史结果不复制为本轮结论。
- S：Cora/CiteSeer/PubMed，GCN，seeds 42/212/2024，train 候选预算 1%/5%，17 Selector；306 cell 为方案覆盖。
- U：固定 Selection→GNNDelete/GIF，配对重训练与 Metrics；612 cell 是 GU 组合，不包含一个已注册的 Retrain 方法。
- [CAPABILITY_COVERAGE.md](CAPABILITY_COVERAGE.md) 区分通用能力、015 配置映射、输入绑定与尚未支持的评价；明确运行完整覆盖当前未成立。
- AAGU-020→021→022 仍独立拥有 D-full 计时原语、小图拟合与大图外推；015 不重做专项实现或执行。

## Source and relations

- Original source anchor retained: unresolved IF scientific-definition and selector-choice boundary recorded on 2026-08-26。
- Original desired outcome retained: the user and a dedicated scientific task choose the IF definition, Selector scope, claims, and experiment linkage before formal execution。
- Scientific fact owner: [OpenGU DocMap IF target-level experiment plan](E:/project/OpenGU-DocMap/10_实验矩阵/20_IF目标层级对比实验计划.md)。
- `AAGU-015 depends_on AAGU-001`：消费已接受的公共实验框架与模块合同。
- `AAGU-015 depends_on AAGU-006`：继承已接受的数据、split 与预算身份边界。
- `AAGU-015 depends_on AAGU-026`：可执行模块化 YAML、方法级缓存身份和 Selection→GU 复用路径须先被接受并落到目标 ref。
- `AAGU-015 depends_on AAGU-009`：阶段 U 使用 GIF 修复路径，不能在软件修复未被接受时形成正式实验候选。
- 015 的交付供后续获准的实验执行使用；全量结果、可视化、结论审计与论文写入属于后续工作，不从本 Block 的实现验证推导科学结论，也不自动创建后续 Block。

## Scope and execution boundaries

- 沿用同一 locator、Claim 和 linked source，完成本阶段方案、真实配置及覆盖检查。
- 不开发新 GU/Selector、通用 Retrain 方法、Metrics 框架或 SyncMate；代码缺口按实际事实记录，其后续实现责任不自动归入 015。
- 不自动绑定运行数据/Selection、不下载重切、不运行训练、GU、重训练或 306/612 矩阵。
- 方案文件明确数据/删除语义和运行前置，后续实际运行仍遵循 experiments/AGENTS.md。
- 配置与报告不预写科学方向结论；Cache V2 和历史结果不作手工改名、覆盖、修复或删除。

## Restart and next action

本轮完成实验方案、配置与能力覆盖材料的验证后提交 formal 人类验收。若用户返工则修改同一 015；后续实现、正式执行及新的 Block 必须按具体范围决定，不从本方案验收自动触发。

## Status history

- 2026-08-26: registered as a numbered Todo candidate; promotion and acceptance contract are deferred to the scientific-definition task.
- 2026-09-04: 用户重申实验运行必须在 001 实验框图之后，015 同样遵守；将已有 001 前置关系写入同一 Todo，补齐 2.1 Human Surface。保留 todo candidate、未 Promote、未 Claim、未实施或接受。
- 2026-09-05: 用户确认已讨论的 Selector 两阶段实验 formation preview；同一 AAGU-015 原地 Promote 为 `EXP` Block，新增可执行 YAML、三小图 17-selector、时间证据、固定 Selection→GNNDelete/GIF 与 paired-retrain 范围。状态为 `registered / not claimed`；未 Claim、运行或生成实验结果。
- 2026-09-05: 用户明确要求使用 block-workflow 执行同一 locator，任务标题为 `AAGU-015 · Selector 两阶段实验与证据`。在 `main@19b3b865ba617ed0216ae43c0ea2225731290de8` 上核实 001、006、026、009 已接受并落地，标准 start 创建 linked source 并 Claim；此前“仅 Promote/注册”描述保留为历史阶段，不再限制已授权的本地实施。
- 2026-09-05: 用户纠正原意：“实验的方案 以及把实验设计的链路打通 而不是直接跑所有实验”。此前 Record 和报告把范围扩大为完整实验执行，是 Agent 对登记语义的误读；该解释现被明确取代。保留既有候选矩阵与软件成果，将验收对齐为方案、链路实现和必要最小验证。没有全量执行授权；不再要求先行特殊合入配置来满足本次验收。

- 2026-09-05: 用户进一步明确 015 交付当前阶段的实验方案文档、对应 YAML、能力覆盖说明与配置检查，并要求实际完成这三项。此前“015 必须补齐所有消费者及重训练代码”的解释被取代；本轮完成定义材料，不重开 026 或重复 SM-005，不自动新增 Retrain Block。

## Run checkpoint · 当前阶段方案与覆盖检查

- Source project：`E:/project/OpenGU-worktrees/aagu-015-selector-evidence/GULib-master/GULib-master`；沿用 `refs/heads/codex/aagu-015-selector-evidence`。
- Canonical Claim 位于主项目 runtime；claimId `6f286852-d42c-43ce-be07-9b773247a673`，owner `codex`，session `AAGU-015 · Selector 两阶段实验与证据`。生命周期由运行流程推进，报告本身不构成接受。
- 配置检查点 `59baa2ae909e7fba92278d9201c635b80be65cdc` 通过 8 项针对性回归、324 个实际 parser 计划、2 个 CLI dry-run；本轮未修改 YAML、配置生成器或实验消费者，按实际差异复用检查。
- 代码覆盖核对主项目 `53e1da5b9bfc133ad7526d2aa39e9f647ac15586`：包含 SM-005 新增的 Cora 原子 GPU 入口；旧 015 分支不包含这些主项目增量，覆盖报告明确区分两处源码，不为方案审阅合并或复制主项目。
- 实际交付：[方案](EXPERIMENT_PLAN.md)、[覆盖表](CAPABILITY_COVERAGE.md)、[配置说明](../../../experiments/configs/aagu015/README.md)、[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)。
- 核验材料：[配置摘要](evidence/definition-summary.json)、[逐 S cell](evidence/stage-s-cells.csv)、[逐 U cell](evidence/stage-u-cells.csv)、[本轮覆盖核对](evidence/capability-audit.json)。精确候选、差异与检查读回保留在忽略的 runtime 中。
- 历史配置检查时 source 所列保护目录中 7 个现存文件前后哈希相同；该范围不等于主项目全部历史结果，也不是本轮科研产物。
- 本轮未开展 SSH/GPU、数据准备、正式实验或科研结果验收。覆盖表中的缺口保持明确，不作为本阶段方案材料未交付，也不声称已补齐代码。
