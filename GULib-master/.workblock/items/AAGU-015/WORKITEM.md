# AAGU-015 · EXP · Selector 两阶段实验与证据

Block ID: `AAGU-015`

Item Version: 2.1

当前状态: `working / claimed`

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

把已收敛的 IF/GIF Selector 讨论整理成清楚的实验方案，并打通方案所需的可执行链路：配置与数据接入 → checkpoint → Selector 评分、排名和 Selection → 固定 Selection 的 GU 与完整重训练 → 评价和证据输出。用必要的最小验证证明链路成立，供后续按批准范围执行实验。015 的交付是实验设计与链路实现，不以跑完设计矩阵或形成科学结论为验收条件。D-full（`gt_full`）是当前 GIF 定义下的操作性参考，不作为数学真值或 exact-retrain 真值。

### 本次增量

沿用同一 AAGU-015 身份，继承 AAGU-001 的公共实验合同、AAGU-006 的数据/划分权威和已接受的模块接口，交付两阶段实验设计、配置及可运行链路。

阶段 S 设计 Cora、CiteSeer、PubMed × GCN × 训练 seeds `[42, 212, 2024]` × 训练候选预算 `[0.01, 0.05]` × 17 个 Selector 的候选矩阵。明确 Q1–Q4 的对照、评分/排名/选集产物、比较指标和时间拆分；实现从 Dataset/Split 引用、checkpoint 准备到 Score/Selection 输出及分析的链路。矩阵展开用于审阅覆盖和依赖，不代表本 Block 必须执行全部 cell。

阶段 U 打通已验证 Selection Artifact → GNNDelete/GIF → 同一 Selection 的完整重训练 → 删除目标、保留节点、测试效用、retrain gap、collateral 与预测变化评价。使用最小端到端验证确认固定 Selection 被复用、Selector producer 未重新调用，以及评价消费了正确模型。下游评价不得反馈改变本轮 Selector。

YAML 是第一项可审阅产物，仍需补齐链路。软件回归与隔离的最小链路验证用于证明实现；真实数据 canary、SSH/GPU 和全量实验调度遵循项目运行规则并另行明确范围。015 的接受不自动授权任何全量实验。

### 核心验收

- 方案明确两阶段研究问题、对照、变量、候选范围、指标与解释边界；Q1–Q4 有对应比较设计，不预写方向性结论。
- 模块化 YAML 可由实际入口解析；无写入 dry-run 展开 306 个 Selector cell 和 612 个候选 GU cell，列出默认值、来源及共享依赖。未知字段和不匹配引用失败关闭。
- 打通数据与划分的验证/绑定、候选构造及 checkpoint 准备/复用；实际身份可追溯，缺失或不匹配输入在写缓存和结果前停止。不得以空引用、伪造哈希或重建不一致划分冒充接通。
- 阶段 S 链路可保存候选对齐的有限 Score、完整排名和合法 Selection；比较入口支持 Spearman、Kendall、top-K common fraction、Jaccard；时间接口区分共享准备、cold compute、warm access、Selection materialization 和总时长。用针对性检查及最小验证确认消费者和字段语义，不要求收集三数据集全量科学结果。
- 阶段 U 的最小端到端验证证明固定 Selection 被复用、Selector producer 未重调，以及 GU、同选集完整重训练和评价接通。AAGU-026 的模块消费者和配置解析不能替代这一链路验证。
- 最小验证覆盖实际消费者及必要的失败路径，记录输入、代码和产物身份，明确软件 fixture、隔离 smoke 与正式数据 canary 各自能证明什么；306/612 全量执行、正式成本统计和科学结论不属于本次完成条件。
- 产出绑定本 WorkItem 的 Markdown/HTML 配对报告，让用户审阅实验方案、链路实现和验证证据，并决定接受、返工或拒绝。维持 formal 人类验收路线；这里的证据是实现与链路验证证据，不是要求本 Block 跑出全量研究结果。

## Confirmed acceptance contract

- Class: `EXP`；Priority: `P0`。
- Route: `formal`；Primary surface: experiment design, executable pipeline and bounded integration evidence；Decision owner: 用户。`EXP` 保留既有分类，不据此扩张执行范围。
- Minimum real evidence: 实验方案与指标合同、实际 parser 展开、数据/checkpoint/Artifact 接缝验证、最小 Selector→固定 Selection→GU/完整重训练→评价回执及必要失败路径、配对报告。正式三数据集完整输入、全矩阵 job 和逐 cell 科研指标不是 015 的强制验收材料。
- Report size: 配对 Markdown/HTML；登记阶段不创建空报告或伪证据。
- Post-candidate decision: Verify 后停在人类验收；没有自动 Apply、push、安装、清理或继续作图/写论文授权。

## Experiment design scope

### Stage S · Selector-only

- Datasets: Cora、CiteSeer、PubMed；继承 AAGU-006 接受的 70/10/20、split seed 2024 与持久化 split 身份。
- Model: 第一层固定 GCN；训练 seeds 为 42、212、2024。
- Budgets: 训练候选集合的 1% 与 5%，`floor_with_minimum_one`。
- Selectors: `degree`、`random`、`a_grad_norm`、`b_param_hutch`、`r_point`、`gt_simple`、`gt_full`、`p_point`、`p_simple`、`p_graph`、`tracin_cp_point_3`、`tracin_cp_point_6`、`tracin_cp_simple_3`、`tracin_cp_simple_6`、`tracin_cp_graph_3`、`tracin_cp_graph_6`、`legacy`。
- Q1: 同 source 的 Hessian-free proxy 与 IF/GIF 参考之间的一致性。
- Q2: point、simple、full graph source 改变造成的排序和选集差异。
- Q3: 参数变化目标与 validation-conditioned 目标之间的差异。
- Q4: 最终 checkpoint 与 3/6 checkpoint 累积之间的差异。
- Designed outputs: 完整 Score、稳定排名、Selection、成对比较摘要、时间与资源记录；本次实现对应生产/消费接口并最小验证，不要求运行完整矩阵。矩阵 cell 数不等于独立训练次数；实际复用仍需精确身份。

### Stage U · Selection to Unlearning

- 直接引用已验证 Selection，不因实验编号、GU 参数或 GU 方法变化重新选点。
- GU 方法第一层为 GNNDelete 与 GIF；两侧模型、训练和 checkpoint 独立声明，只有精确身份一致时才共享。
- 设计并接通同一 Selection 的完整重训练和删除目标、保留节点、测试效用、retrain gap、collateral 与预测变化评价；以最小消费者验证证明实现。
- 候选 612-cell 矩阵只作方案展开。后续正式运行先经过独立批准的 canary、成本和设备门槛；它们不是要求 015 跑完所有实验的依据。

### Timing boundary

- AAGU-015 设计并接通 Selector 的时间记录方式，用最小验证检查字段含义；三个小数据集的正式成本统计由后续获准执行产生。
- AAGU-020→AAGU-021→AAGU-022 独立拥有 D-full 评分原语、Cora 候选数拟合和 ogbn-arxiv 容量外推。015 不重复实现这条专项路径；只有在对应结果被接受后才可在后续分析中引用。

## Source and relations

- Original source anchor retained: unresolved IF scientific-definition and selector-choice boundary recorded on 2026-08-26。
- Original desired outcome retained: the user and a dedicated scientific task choose the IF definition, Selector scope, claims, and experiment linkage before formal execution。
- Scientific fact owner: [OpenGU DocMap IF target-level experiment plan](../../../../../OpenGU-DocMap/10_实验矩阵/20_IF目标层级对比实验计划.md)。
- `AAGU-015 depends_on AAGU-001`：消费已接受的公共实验框架与模块合同。
- `AAGU-015 depends_on AAGU-006`：继承已接受的数据、split 与预算身份边界。
- `AAGU-015 depends_on AAGU-026`：可执行模块化 YAML、方法级缓存身份和 Selection→GU 复用路径须先被接受并落到目标 ref。
- `AAGU-015 depends_on AAGU-009`：阶段 U 使用 GIF 修复路径，不能在软件修复未被接受时形成正式实验候选。
- 015 的交付供后续获准的实验执行使用；全量结果、可视化、结论审计与论文写入属于后续工作，不从本 Block 的实现验证推导科学结论，也不自动创建后续 Block。

## Scope and execution boundaries

- 同一 stable locator 已 Claim；在既有 linked source 完成方案与链路实现，运行针对性软件回归和隔离的最小验证。
- 不直接执行 306/612 全量实验，不以收集三数据集完整科研结果作为本次验收要求。真实数据 canary、正式 SSH/GPU 与后续调度仍需明确范围并遵循项目入口和路径规则。
- 不把 AAGU-001 示例 YAML、旧集中式配置或历史结果直接当成 AAGU-015 的已批准配方或证据。
- 不在本 Block 内制作最终论文图、修改论文正文或预写方向性结论。
- Cache V2 Artifact 只由注册生产者创建和验证，不手工改名、覆盖、修复或删除。
- 正式 GPU 运行遵循 `experiments/AGENTS.md`；缺少 job ID、recipe receipt、远端代码/数据/设备身份或完整收集校验时，状态为 NOT OBSERVED。

## Restart and next action

从既有 YAML 和展开检查点恢复同一 Claim，补齐方案中的比较设计、数据/checkpoint 接入及 Selector→固定 Selection→GU/完整重训练→评价链路，以最小验证呈现实现证据。链路通过后按 formal 路线交用户验收；后续正式实验执行不作为 015 的隐含必做项。

## Status history

- 2026-08-26: registered as a numbered Todo candidate; promotion and acceptance contract are deferred to the scientific-definition task.
- 2026-09-04: 用户重申实验运行必须在 001 实验框图之后，015 同样遵守；将已有 001 前置关系写入同一 Todo，补齐 2.1 Human Surface。保留 todo candidate、未 Promote、未 Claim、未实施或接受。
- 2026-09-05: 用户确认已讨论的 Selector 两阶段实验 formation preview；同一 AAGU-015 原地 Promote 为 `EXP` Block，新增可执行 YAML、三小图 17-selector、时间证据、固定 Selection→GNNDelete/GIF 与 paired-retrain 范围。状态为 `registered / not claimed`；未 Claim、运行或生成实验结果。
- 2026-09-05: 用户明确要求使用 block-workflow 执行同一 locator，任务标题为 `AAGU-015 · Selector 两阶段实验与证据`。在 `main@19b3b865ba617ed0216ae43c0ea2225731290de8` 上核实 001、006、026、009 已接受并落地，标准 start 创建 linked source 并 Claim；此前“仅 Promote/注册”描述保留为历史阶段，不再限制已授权的本地实施。
- 2026-09-05: 用户纠正原意：“实验的方案 以及把实验设计的链路打通 而不是直接跑所有实验”。此前 Record 和报告把范围扩大为完整实验执行，是 Agent 对登记语义的误读；该解释现被明确取代。保留既有候选矩阵与软件成果，将验收对齐为方案、链路实现和必要最小验证。没有全量执行授权；不再要求先行特殊合入配置来满足本次验收。

## Run checkpoint · 方案与链路准备

- 实际 source project：`E:/project/OpenGU-worktrees/aagu-015-selector-evidence/GULib-master/GULib-master`；Git 根位于其父目录。使用标准 start 返回的路径，不根据目录名猜测。
- Canonical Claim：主项目 `.workblock/runtime/claims/AAGU-015.json`；claimId `6f286852-d42c-43ce-be07-9b773247a673`，owner `codex`，session `AAGU-015 · Selector 两阶段实验与证据`，phase `ongoing`。本轮不转 awaiting_acceptance。
- 已实现 [配置源表与运行说明](../../../experiments/configs/aagu015/README.md)、[生成器](../../../experiments/aagu015/definitions.py) 和定义专用回归。生成源表不承担实验执行；424 份生成 YAML 均使用已接受的 modular schema。
- 阶段 S 展开 306 cell，阶段 U 展开 612 个候选 GU cell；完整有效配置、字段来源、预算预期及依赖组由实际 parser/dry-run 输出。输入空值明确表示未绑定，不伪造 data、split、checkpoint 或 Selection 哈希。
- Stage U 不含 selector_refs；已有入口会拒绝缺完整重训练消费者的评价 case。当前只证明声明与失败关闭，未证明真实固定 Selection→GU→Retrain/Evaluation 已完成。
- 当前实现差距：数据绑定/准备尚未接通；普通 modular GU 仍缺完整重训练评价消费者；Stage S 比较和时间接口尚未在 015 的最小链路中验证。缺全量实验结果不再列作本 Block 阻塞。
- 后续正式运行条件另列：首次检查时 canonical `.syncmate/device.yaml` 缺失，SSH、正式输入与 GPU canary 未观察；三端同一 main 规则继续适用于正式运行，不限制本次在 linked source 完成代码与隔离最小验证。之前要求用户决定“配置先行落地”的问题撤回。
- 下一步：在同一 015 补齐实验设计与上述消费者接缝，最小验证通过后呈现方案和链路的验收报告。
- 配置检查点 `59baa2ae909e7fba92278d9201c635b80be65cdc` 在干净源码上通过 8 项定义回归、324 张计划的实际 parser 展开、2 个真实 CLI dry-run 和 dashboard 检查。源 worktree 所列保护目录中 7 个现存文件的 SHA-256 前后相同，其余缺失目录仍缺失。此为配置证据，不是完整 EXP Verify。
- 本阶段人类审阅入口：[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)。完整有效值与 YAML 指纹见 [definition-summary.json](evidence/definition-summary.json)，逐 cell 依赖见 [S 表](evidence/stage-s-cells.csv) / [U 表](evidence/stage-u-cells.csv)。研究指标、计时、真实 canary 和矩阵结果均未观察。
- 报告在 1440×1100 桌面、600×1800 窄屏与 1440×3300 完整页面渲染后人工检查可读；430px 首次截图右侧截断，原因未单独验证，未计为通过。后续报告/Record 说明差异不影响配置消费者，复用上述配置检查点的测试并重新验证报告结构、链接、生成一致性及最终差异。
