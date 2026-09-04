# AAGU-001 · FIX · 实验合同与注册规范

Block ID: `AAGU-001`

Item Version: 2.1

当前状态: `awaiting acceptance`

Item Type: Block

Stable locator: `.workblock/items/AAGU-001/WORKITEM.md`

Acceptance Route: `formal`

Execution topology: `sequential`

> Apply target ref：`refs/heads/main`


> Git baseline：`8383e30239398c5268965e088afdfba7abc74ca9`

> Source branch：`refs/heads/codex/aagu-001-experiment-contract`

> Remote target：`origin refs/heads/main`
## Human Surface

### 核心意图

建立一份可独立验收、供后续实验共同使用的实验合同与注册规范。最重要的交付是具体、可追溯的参数共识：现在有哪些参数和值、分别由谁拥有、后续比较哪些配置、哪些科学选择仍待决定，以及修改参数应影响哪些缓存。实验由 Dataset/Split、Selector、Unlearning 三块参数表组合，不让实验大表污染各模块的身份。SyncMate 只承担通用执行与证据连接，不替代科研判断。

### 本次增量

固定一张实验组合大表、三类独立模块小表的职责与引用规则，并给出真实配置的字段清单与填写示例。小表按配置实例分别保存：每个 selector、每个 unlearning 方法各有自己的配置；同一方法的变体只需不同配置表，不另造变体机制。已有参数和矩阵保持原计划与配置为事实来源，但不能只给链接或空模板：必须展示当前有效值、来源、可变项、待定项与身份影响。用一个已有且定义明确的实验验证合同和注册链可用，不要求一次定义或批准全部实验。

具体 IF 定义与 selector 选择由 AAGU-015 等对应科研任务决定。每轮执行前记录本轮问题和必要定义，运行后在对应实验中分析真实结果、解释现象并形成下一轮设计，保留本轮原始定义与证据。本 Block 只形成公共合同、真实参数示例与注册规范；配置解析、按方法缓存身份和消费者的实现修复由 AAGU-026 承接。不运行正式 GPU 实验，也不实现设备就绪检查、FlowChunk 适配器或产品化增强。

### 核心验收

- 一份可审阅的实验合同说明大表和三类小表的必要信息、填写规则、事实所有者，以及计划、配置、执行记录和结果证据的关联方式，并明确注册、执行与证据接纳的条件。
- 至少一份真实参数清单逐项列出当前有效值及来源、模块归属、后续允许比较的配置或待定选择、改变时应 HIT/MISS 的真实消费者。覆盖已划分数据、候选集合与预算、两侧模型、IF 参数范围与数值近似、轨迹、GU 专属参数；不能用笼统的“输入/参数/版本”或纯链接代替。
- 配置示例明确 selector-only、已有 Selection 直接进入 GU、不同实验复用小表、同方法不同配置表的变体、两侧不同模型或精确共享 checkpoint；明确这些是合同要求及实现验收目标，不声称当前全部已支持。实验 ID/case ID 只作追踪，不进入小模块计算键。
- 至少一个已有且定义明确的实验完成合同示例、来源追溯和注册后的空跑检查（dry-run），证明合同及注册链可用；不新增正式运行，也不把 dry-run 当作实验结果。
- 科研决定、设备与执行职责、证据接纳以及 SyncMate 的工具边界清楚分开，SyncMate 不成为科研 Claim 或 acceptance 的决定者。
- AAGU 研究负责人能够独立批准、返工或拒绝这份公共规范。验收不以全部实验参数、selector 或矩阵冻结为前提；具体实验仍须按规范完成本轮定义与批准后才能执行，已有真实结果的解释归对应实验所有。

## Confirmed acceptance contract

- Route: `formal`
- Confirmation source: 2026-09-04 用户确认保留 AAGU-001 编号，将范围收窄为独立的“实验合同与注册规范”，不新增参数梳理 Block，并将 AAGU-001 调整为 AAGU-015 的前置；随后确认三块参数表、模块缓存独立、变体仅用不同配置表，以及将实现修复单独登记为 AAGU-026。
- Primary surface: `experiment contract / registration specification`
- Minimum real evidence: 可审阅的三类参数表与组合规则、带当前值和来源的真实参数清单、参数变更影响矩阵、注册与证据接纳条件，以及一个已有明确实验的合同示例、来源关联和现有注册入口 dry-run；这些证明公共规范可用，不证明 AAGU-026 的实现完成或正式实验结果已被接受。
- Post-candidate decision: AAGU 研究负责人必须明确批准、返工或拒绝该公共规范；接受 AAGU-001 不等于批准所有具体实验。
- Report size: paired Markdown/HTML report after Verify.

## Confirmed modular configuration contract

这是本次登记固定的设计共识，不是已经实现的新配置接口。001 的后续候选据此整理字段、实际参数来源和完整示例；026 消费接受后的合同实现运行链。

| 参数表 | 必要内容与所有权 | 不应混入的内容 |
|---|---|---|
| Dataset/Split | 数据集名称及版本/内容身份、预处理身份、已持久化划分引用与 split hash；划分方法、比例与 seed 作为可追溯生成信息；消费者核对实际节点与 mask | selector/GU 参数；仅凭数据集名字猜测实际划分；消费阶段重新 split |
| Selector | 方法及其有效配置；候选集合定义/身份；预算（比例或 K、分母、取整规则、实际 K）；选择方向、规则、随机性；需要模型的方法独立声明模型结构、训练参数和 checkpoint/轨迹依赖；IF 类方法拥有自己的求导范围和数值求解配置 | GU 专属参数、其他 selector 专属字段、全局实验 ID/case ID；不需要模型的 degree/random 不被迫绑定 GCN |
| Unlearning | GU 方法及自身参数、目标模型与训练配置、实际 checkpoint 身份；消费已验证 Selection 的引用以及对应 Dataset/Split | 反向覆盖 selector 模型、预算或求解配置；要求为新实验重算未变化的选点 |

实验大表记录研究问题、轮次、实验/case 编号、三类小表的明确引用、矩阵组合、执行终点、指标/接纳条件，以及运行记录/结果证据引用。具体指标配置由评价消费者拥有，不反向进入未使用它们的 selector 身份。执行可以止于 selector，也可以直接引用已有 Selection 执行 GU；不要求每个矩阵 cell 各写一份独立科研合同。每轮合同中的设计定义与运行后的记录/分析分开保存；下一轮设计不覆盖上一轮原始定义。

- 每个配置实例一个文件；同一方法可有多份配置表，例如同一 IF 方法不同求导范围、同一 TracIn 方法不同 checkpoint 集合、同一 GU 方法不同学习率。它们复用同一受支持的方法实现；文件名只是定位/展示，不另设变体注册层、隐式继承或大表覆盖。新增尚未支持的算法不属于“仅改配置”的承诺。
- 所有有效计算字段必须有明确类型、默认值/必填规则、允许值与归属；展开默认值后按规范化语义计算身份，拒绝未知或无效字段，避免悄悄忽略参数。语义变化产生新请求键，排版、注释、等价值写法、文件路径或展示名称变化不能单独导致 MISS。
- 小模块键只包含它实际消费的输入身份、有效参数和相关 producer 版本/实现指纹，不包含整张实验大表或无关下游代码。实验/case 编号可以出现在运行追踪记录中，不参与计算键。共享依赖真正变化时影响所有真实消费者；“正交”不是取消依赖传播。
- 删除预算是 Selector 的输入。最终 Selection 记录明确的节点编号、候选身份、实际 K 与选择规则；GU 消费这个结果，不独立重解释预算。Score 与最终 Selection 是不同缓存层：只有明确预算无关且前缀稳定的评分才能跨 K 复用；预算相关评分必须纳入预算。
- Selector 和 GU 各自声明模型与训练配置，可以是 Selector=SGC、GU=GCN；同为两层 GCN 也不自动意味着相同权重。仅当实际数据/划分、模型/训练配置及 checkpoint 身份匹配时复用相同 checkpoint，不用“共享”标记掩盖不匹配。
- 求导参数范围属于使用该定义的 IF/梯度 selector 配置；数值近似指实际求解计算的设置，如 LiSSA 迭代/缩放/阻尼或 Hutchinson 采样数/seed，应逐项说明当前实现怎样使用，而不是作为所有 selector 的共同参数包。轨迹属于实际消费多个 checkpoint 的方法（如 TracIn），并非仅在 unlearning 才需要，也非每个 GU 方法都必需。
- 不同 selector 分别形成方法级 Score/Selection 身份；可共享相同模型、轨迹或其他中间结果，但不能让一个方法的专属参数使其余 16 个方法整包失效。新配置 MISS 不等于旧 Artifact 损坏：旧缓存保留供原配置复用，不删除或重写。

### Existing configuration anchors for the later parameter table

以下仅为登记时读取的现有配置实例，不是为所有实验批准统一值，也不是已完成的字段盘点。执行 001 时必须重新核对入口的有效参数、消费者与代码版本，并分清当前可执行值、历史计划值和待定研究选择。

| 当前实例 | 已观察值 | 归属与后续比较边界 |
|---|---|---|
| [target-direct formal v2](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml) 的 split | train/val/test = 0.7/0.1/0.2；split seed = 2024 | Dataset/Split；不同合法划分应引用不同已生成资产，不能就地覆盖原资产 |
| 同配置的 budget | 0.01、0.05；分母 train_candidate_count；floor_with_minimum_one | Selector；比较不同预算配置，最终 Selection 变化；预算无关评分可复用 |
| 同配置的 model/training 与 GU | GCN；2 层；hidden=64；epochs=100；GU=GNNDelete；当前声明精确共享 checkpoint | 应拆为分别声明的 Selector 和 GU 参数；SGC/GCN 跨模型组合是合同目标，不声称此 formal 入口现已支持 |
| 同配置的参数范围与轨迹 | main_parameter_scope=last_layer；checkpoint epochs=[1,10,25,50,75,100] | 各 IF/梯度方法与 TracIn 的真实依赖；其他范围、轨迹配置是不同配置表，具体科学取舍由对应实验确认 |

001 的真实参数清单还须从当前实现追到未出现在此 YAML 的有效数值近似和 GU 参数，记录默认值的真实出处；不得把旧计划中的数值或一个身份探针的测试值写成当前正式实验参数。

## Context and relations

- Blueprint scope: 当前 OpenGU OB 实验入口与目录级 AGENTS；没有额外稳定 Graph/Blueprint ID，故不虚构节点。
- Fact owner: [本 WorkItem](WORKITEM.md) 拥有公共合同与注册规范的任务范围和验收要求；具体科学问题、参数与矩阵继续引用原研究计划和配置。
- Confirmed relations: `AAGU-001 depends_on AAGU-006`；`AAGU-015 depends_on AAGU-001`。公共规范继承已接受的数据与划分边界，AAGU-015 消费该规范形成具体科学定义；AAGU-001 不依赖 AAGU-015 的选择结果。
- Existing downstream relations: `AAGU-002 depends_on AAGU-001`；`AAGU-003 depends_on AAGU-001`。设备与证据 gate 消费公共规范，各具体实验的定义与科学批准仍由对应任务提供。
- Implementation consumer: [AAGU-026](../AAGU-026/WORKITEM.md) `depends_on AAGU-001`，落实独立配置、方法级身份和真实缓存复用；001 不反向依赖 026，也不以其实现完成作为本合同的验收条件。
- Cross-project references: SyncMate SM records are implementation companions, not duplicate scientific acceptance records.

## Runtime and authorization boundaries

- 2026-09-04 用户“同意 做吧”授权执行本前置合同 Block；原登记阶段的 registration-only 边界保留在历史中。本轮只做合同、参数来源、示例和本地验证，不派发实验、不运行正式 GPU、不 push/install/Apply 或写远端。
- Future execution must use the OpenGU active checkout and experiment-specific AGENTS; local dry-run is not formal GPU acceptance.
- 当前执行分支与 baseline 已由 Run 记录；候选、Verify 与 Report 在下方 Execution record 中追加，不把本地检查当作正式实验结果。

## Execution record

- 当前 owner：本任务 `01a06c2f-8e35-7bf2-8023-ab3be063830b`，session `AAGU-001 · 三层实验参数合同`；2026-09-04 Claim 同一 WorkItem，仅拥有 001 的独立验收范围。
- 产物：[公共合同](../../../docs/experiment_contract/README.md)、[真实参数表](../../../docs/experiment_contract/PARAMETERS.md)、[8 份独立实例](../../../docs/experiment_contract/examples/)、[有界验证脚本](evidence/verify_contract.py)。示例不是当前 launcher 的新输入接口。
- 工作观察：追到 GCN properties 的实际 lr=0.005、decay=1e-6；区分基础训练 100 轮与节点遗忘 50 轮；列出 17 种评分实际消费依赖。formal 配置解析与 sanity dry-run 分开，未运行 Selection/GU producer。
- 源码与正式 YAML 未修改；026 未 Claim。内容 checkpoint `c0c433f66eb1def3dab06e05ac7ebd4ecbef026c` 的验证回执见 [evidence/verification.json](evidence/verification.json)：8 份实例、25 个文档链接、真实 parser 默认值/预算/快照检查及 existing sanity dry-run 均通过；看板校验及 7 个看板测试通过。
- 人类验收入口：[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)。HTML 已真实渲染并查看桌面/窄屏首尾；建议接受公共合同，当前决定仍为待决定。待验收候选以本 source branch 的干净 HEAD 为准；报告与看板下一步对齐后的同脚本完整复验保存在 [最终回执](../../runtime/evidence/AAGU-001/verify-final-aligned.json)。
- 证据边界：正式资产哈希与 GPU 运行 NOT OBSERVED，缓存实现未修改，001 的人类接受 NOT CONFIRMED。报告不是 026 的实现证据，也不是正式研究结论。

## Restart and next action

本轮停在 formal 人工验收。用户接受后以同一 locator 进入 block-closeout；要求返工则在同一 source branch 与 Claim 中 Resume。不得自动转为 AAGU-026 的运行时/缓存实现；026 须等本合同接受并落实其前置后再执行。

## Status history

- 2026-09-04: 内容候选完成真实配置与现有入口验证，形成配对验收报告并观察桌面/窄屏渲染；投影为 `awaiting acceptance`，等待用户对 001 的决定。不将 Verify PASS 写成人类接受。

- 2026-09-04: 用户“同意 做吧”后执行前置 001；从登记提交启动 sequential source branch，Claim 进入 ongoing，WorkItem 为 `working / claimed`。未将该同意解释为尚未形成的候选验收。

- 2026-09-04: 按用户确认收窄同一 WorkItem 的标题、范围和验收条件，调整为 AAGU-015 的前置；本次仅修订登记合同，状态保持 `registered / not claimed`，未 Claim 或实施公共规范。
- 2026-09-04: 按用户确认补入三块独立参数表、实验组合大表、预算归 Selector、两侧模型独立、按方法缓存身份和变体只用不同配置表的共识；真实参数来源清单成为核心验收，实现修复单独登记 AAGU-026。状态仍为 `registered / not claimed`，没有实施、候选或验收决定。
