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

在 AAGU-001 实验框图、参数合同与注册规范被接受后，把已经收敛的 IF/GIF Selector 讨论转成一轮可执行、可复核的实验：先独立回答 Selector 的评分、排序、选集与成本问题，再把同一批固定 Selection 交给图遗忘方法和完整重训练，判断 Selector 差异是否真的转化为遗忘效果差异。D-full（`gt_full`）是当前 GIF 定义下的操作性参考，不作为数学真值或 exact-retrain 真值。

### 本次增量

沿用同一 AAGU-015 身份，继承 AAGU-001 的公共实验合同与 AAGU-006 的数据/划分权威，将原科学定义 Todo 原地 Promote 为两阶段 EXP Block。

阶段 S 形成并执行 selector-only 定义：为 Cora、CiteSeer、PubMed 建立明确的 Dataset/Split 引用，为 17 个 Selector 建立独立可执行 YAML，并以 GCN、训练 seeds `[42, 212, 2024]`、训练候选预算 `[0.01, 0.05]` 组成候选矩阵。保存完整 Score、排名和 Selection，按 Q1–Q4 分别分析 GIF proxy、graph source、目标类别和 checkpoint 累积差异，并在三个小数据集上记录 cold compute、warm artifact access、Selection materialization、总时长及可获得的资源开销。

阶段 U 直接消费阶段 S 已验证的 Selection Artifact，不重新选点。第一层 GU 范围为 GNNDelete 与 GIF；同一 Selection 配对完整重训练，评价删除目标、保留节点效用、测试效用、retrain gap、collateral 与预测变化。下游评价不得反馈改变本轮 Selector。

YAML 是本 Block 的第一项可审阅产物，不是最终实验结论。正式矩阵只能在配置展开、单 cell canary、真实输入绑定和成本门槛通过后按批准范围调度；Block 注册本身不授权 SSH 或 GPU 实验。

### 核心验收

- 形成可由已接受正式入口解析的模块化 YAML：三个 Dataset/Split 实例、17 个 Selector 实例、GNNDelete/GIF 实例，以及阶段 S、阶段 U 的实验大表；未知字段和不匹配引用失败关闭。
- dry-run 在不训练、不写 Cache V2、不创建伪结果的条件下展开 `3 datasets × 3 seeds × 2 budgets × 17 selectors = 306` 个 selector cell，以及候选 `306 × 2 GU = 612` 个 GU cell，并列出实际共享依赖、默认展开值和配置摘要。
- 正式执行前绑定真实 data/split/candidate、checkpoint、代码、Recipe/Artifact 与设备身份；缺哈希、缺 checkpoint、身份不一致或 GPU/路径前置失败时停止。
- 阶段 S 保存候选对齐的有限 Score、完整排名与合法 Selection；在相同候选池和预算口径内报告 Spearman、Kendall、top-K common fraction 与 Jaccard，并按 Q1–Q4 分组解释。
- 三个数据集的时间证据明确区分 cold compute、warm access、Selection materialization 与共享准备；不得把 warm HIT 或整包时间解释为某个方法的冷计算成本。
- 阶段 U 证明固定 Selection 被复用且 Selector producer 未调用；每个纳入科学结论的 GU cell 有对应完整重训练与评价证据。AAGU-026 的模块消费者本身不替代 retrain/evaluation 证据链，实施时必须绑定并验证真实入口。
- 产出绑定本 WorkItem 的 Markdown/HTML 配对报告，区分技术完成、实测观察与可支持的科学判断。低相关、攻击不强或假设不成立仍可构成有效研究结果，不自动算技术失败。
- 用户能够根据配对报告明确接受、返工或拒绝；进程成功、cache HIT、测试通过或矩阵完成均不自动构成研究验收。

## Confirmed acceptance contract

- Class: `EXP`；Priority: `P0`。
- Route: `formal`；Primary surface: executable experiment definitions and selector/GU research evidence；Decision owner: 用户。
- Minimum real evidence: 实际 parser 的 YAML 展开证据、三个数据集的真实输入与 split 身份、正式 job/recipe 回执、Score/Selection/GU/Retrain 原始产物、时间与资源记录、完整性校验、逐 cell 指标及配对报告。
- Report size: 配对 Markdown/HTML；登记阶段不创建空报告或伪证据。
- Post-candidate decision: Verify 后停在人类验收；没有自动 Apply、push、安装、清理或继续作图/写论文授权。

## Scientific scope

### Stage S · Selector-only

- Datasets: Cora、CiteSeer、PubMed；继承 AAGU-006 接受的 70/10/20、split seed 2024 与持久化 split 身份。
- Model: 第一层固定 GCN；训练 seeds 为 42、212、2024。
- Budgets: 训练候选集合的 1% 与 5%，`floor_with_minimum_one`。
- Selectors: `degree`、`random`、`a_grad_norm`、`b_param_hutch`、`r_point`、`gt_simple`、`gt_full`、`p_point`、`p_simple`、`p_graph`、`tracin_cp_point_3`、`tracin_cp_point_6`、`tracin_cp_simple_3`、`tracin_cp_simple_6`、`tracin_cp_graph_3`、`tracin_cp_graph_6`、`legacy`。
- Q1: 同 source 的 Hessian-free proxy 与 IF/GIF 参考之间的一致性。
- Q2: point、simple、full graph source 改变造成的排序和选集差异。
- Q3: 参数变化目标与 validation-conditioned 目标之间的差异。
- Q4: 最终 checkpoint 与 3/6 checkpoint 累积之间的差异。
- Outputs: 完整 Score、稳定排名、Selection、成对比较摘要、时间与资源记录。矩阵 cell 数不等于独立训练次数；共享 checkpoint、Score 或无模型方法的复用必须由真实身份证明。

### Stage U · Selection to Unlearning

- 直接引用已验证 Selection，不因实验编号、GU 参数或 GU 方法变化重新选点。
- GU 方法第一层为 GNNDelete 与 GIF；两侧模型、训练和 checkpoint 独立声明，只有精确身份一致时才共享。
- 同一 Selection 配对完整重训练；报告删除目标、保留节点、测试效用、retrain gap、collateral 与预测变化。
- 在全量调度前先通过单 cell canary 和阶段 S 的成本门槛；候选 612-cell 矩阵未经过正式调度决定时不得执行。

### Timing boundary

- AAGU-015 在三个小数据集上拥有本轮每个 Selector 的运行与缓存访问时间证据。
- AAGU-020→AAGU-021→AAGU-022 独立拥有 D-full 评分原语、Cora 候选数拟合和 ogbn-arxiv 容量外推。015 不重复实现这条专项路径；只有在对应结果被接受后才可在后续分析中引用。

## Source and relations

- Original source anchor retained: unresolved IF scientific-definition and selector-choice boundary recorded on 2026-08-26。
- Original desired outcome retained: the user and a dedicated scientific task choose the IF definition, Selector scope, claims, and experiment linkage before formal execution。
- Scientific fact owner: [OpenGU DocMap IF target-level experiment plan](../../../../../OpenGU-DocMap/10_实验矩阵/20_IF目标层级对比实验计划.md)。
- `AAGU-015 depends_on AAGU-001`：消费已接受的公共实验框架与模块合同。
- `AAGU-015 depends_on AAGU-006`：继承已接受的数据、split 与预算身份边界。
- `AAGU-015 depends_on AAGU-026`：可执行模块化 YAML、方法级缓存身份和 Selection→GU 复用路径须先被接受并落到目标 ref。
- `AAGU-015 depends_on AAGU-009`：阶段 U 使用 GIF 修复路径，不能在软件修复未被接受时形成正式实验候选。
- 两个后续独立 Block 将分别拥有结果可视化、结论审计与论文写入；它们消费 AAGU-015 的已接受结果，不在本 Block 内提前制作。

## Scope and execution boundaries

- 当前只完成 Promote/注册，不 Claim、不修改正式配方、不训练、不运行 SSH/GPU、不写 Cache V2、不生成结果。
- 后续使用 `block-workflow` Claim 同一 stable locator，在 linked worktree 中实施，先交付并核验 YAML 与展开结果，再进入正式执行门槛。
- 不把 AAGU-001 示例 YAML、旧集中式配置或历史结果直接当成 AAGU-015 的已批准配方或证据。
- 不在本 Block 内制作最终论文图、修改论文正文或预写方向性结论。
- Cache V2 Artifact 只由注册生产者创建和验证，不手工改名、覆盖、修复或删除。
- 正式 GPU 运行遵循 `experiments/AGENTS.md`；缺少 job ID、recipe receipt、远端代码/数据/设备身份或完整收集校验时，状态为 NOT OBSERVED。

## Restart and next action

确认 AAGU-001、AAGU-006、AAGU-026、AAGU-009 的最新接受和落地事实，读取本 Record、`experiments/AGENTS.md` 及当前模块接口。使用 `block-workflow` Claim 同一 locator，在 linked worktree 中先生成真实 YAML 与无写入展开证据；到正式调度门槛时按 Record 核对 canary、成本和远端前置，不能把注册解释为运行授权。

## Status history

- 2026-08-26: registered as a numbered Todo candidate; promotion and acceptance contract are deferred to the scientific-definition task.
- 2026-09-04: 用户重申实验运行必须在 001 实验框图之后，015 同样遵守；将已有 001 前置关系写入同一 Todo，补齐 2.1 Human Surface。保留 todo candidate、未 Promote、未 Claim、未实施或接受。
- 2026-09-05: 用户确认已讨论的 Selector 两阶段实验 formation preview；同一 AAGU-015 原地 Promote 为 `EXP` Block，新增可执行 YAML、三小图 17-selector、时间证据、固定 Selection→GNNDelete/GIF 与 paired-retrain 范围。状态为 `registered / not claimed`；未 Claim、运行或生成实验结果。
- 2026-09-05: 用户明确要求使用 block-workflow 执行同一 locator，任务标题为 `AAGU-015 · Selector 两阶段实验与证据`。在 `main@19b3b865ba617ed0216ae43c0ea2225731290de8` 上核实 001、006、026、009 已接受并落地，标准 start 创建 linked source 并 Claim；此前“仅 Promote/注册”描述保留为历史阶段，不再限制已授权的本地实施。

## Run checkpoint · YAML 与正式门槛

- 实际 source project：`E:/project/OpenGU-worktrees/aagu-015-selector-evidence/GULib-master/GULib-master`；Git 根位于其父目录。使用标准 start 返回的路径，不根据目录名猜测。
- Canonical Claim：主项目 `.workblock/runtime/claims/AAGU-015.json`；claimId `6f286852-d42c-43ce-be07-9b773247a673`，owner `codex`，session `AAGU-015 · Selector 两阶段实验与证据`，phase `ongoing`。本轮不转 awaiting_acceptance。
- 已实现 [配置源表与运行说明](../../../experiments/configs/aagu015/README.md)、[生成器](../../../experiments/aagu015/definitions.py) 和定义专用回归。生成源表不承担实验执行；424 份生成 YAML 均使用已接受的 modular schema。
- 阶段 S 展开 306 cell，阶段 U 展开 612 个候选 GU cell；完整有效配置、字段来源、预算预期及依赖组由实际 parser/dry-run 输出。输入空值明确表示未绑定，不伪造 data、split、checkpoint 或 Selection 哈希。
- Stage U 不含 selector_refs；已有入口会拒绝缺完整重训练消费者的评价 case。当前只证明声明与失败关闭，未证明真实固定 Selection→GU→Retrain/Evaluation 已完成。
- 当前前置差距：canonical `.syncmate/device.yaml` 缺失；本轮配置尚在 linked source；没有注册到本轮 YAML 的正式 launcher；真实数据身份、checkpoint、单 cell canary、时间与成本证据均未观察。旧 target-direct recipe 和历史结果不能替代。
- 执行顺序的用户决定边界：`experiments/AGENTS.md` §7 要求正式实验先使用三端同一已落地 main，而本 Record 的最终 formal 接受依赖实验结果。需要用户明确同一 015 的配置/入口先行落地边界；不得自行把配置检查点升级为整个 EXP 已接受，或以 candidate 分支绕过正式版本要求。
- 下一步：审阅本配置检查点并明确上述先行落地顺序；随后在同一 015 补齐真实 launcher、完整重训练/评价与输入绑定，经 canary/成本门槛后再由用户决定矩阵调度范围。
