# AAGU-028 · FIX · Retrain 独立方法与 Metrics 输出复用

Block ID: `AAGU-028`
Item Version: 2.1
Item Type: `Block`
当前状态: `awaiting acceptance`
Stable locator: `.workblock/items/AAGU-028/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`


> Git baseline：`e27425e6ad8ba8dd34663098d759d83ab4804023`

> Source branch：`refs/heads/codex/aagu-028-retrain-metrics`

> Remote target：`origin refs/heads/main`
## Human Surface

### 核心意图

将 Retrain 作为可独立配置、执行和复用结果的 Unlearning 方法。Metrics 只读取已经完成的 GU / Retrain 输出进行比较，避免每个 GU 或每次评价都重新训练参照模型。本项是用户明确要求的实验执行前置 FIX；完成、验收并落地之前，不启动整轮正式研究实验。

### 本次增量

在 AAGU-026 已接受的模块化配置、Selection→GU 和 Cache V2 基础上，补齐 Retrain 方法注册、小表、真实执行消费者及独立结果身份；同一已验证删除请求和相同 Dataset/Split、模型、训练与删除语义下，Retrain 结果可供 GNNDelete、GIF 等参照评价复用。更换 GU 专属参数或 Metrics 配置不重复执行该 Retrain。

将活动 Metrics 路径改为显式引用并读取已持久化的 GU / Retrain 输出，接通 modular 的 post_unlearning_utility_and_retrain_gap。移除 eval_collateral.py 内部隐式重训练路径，不保留兼容 fallback。补充从实验定义、Selection、Unlearning / Retrain 产物到 Metrics 的数据流说明与最小可执行示例；不在本 Block 运行完整科研矩阵。

### 核心验收

- Retrain 可通过独立 Unlearning YAML 选择并由真实入口执行；可直接消费已有 Selection，过程中不调用 Selector producer。不增加第二套 Retrain 算法或隐藏方法分发；正式适配器每个 cell 也只执行当前方法，不成对调用 GU 与 Retrain。
- 在临时 CPU 小图上，以同一真实 Dataset/Split 和删除请求运行独立 Retrain，保存可复核的模型/预测与所需评价输入。明确删除监督、边/特征、训练图及评价图语义；不能仅排除 train_mask 就无条件宣称覆盖所有删除语义。
- GNNDelete、GIF 与 Retrain 输出可按同一实际请求配对；Metrics 只读产物计算已注册的 utility / retrain-gap 指标。单方法指标及必要预测独立保存，差值在结果收集后计算；禁止训练及模型前向后，单独重算 Metrics 仍成功；改变指标集合或 GU 专属参数不触发匹配 Retrain 的 producer。
- 验证冷运行、热读取、跨 GU 复用、独立 Metrics 重算的数值和身份一致性；持久化输出不因舍入后重算而改变同一评价身份的数值。身份不同或缺失时明确 MISS/拒绝，不自动重训、猜测、下载或修复输入。
- 真实数据/划分、实际删除请求、模型训练条件或删除语义变化时，不能误用旧 Retrain。核对所复用 Artifact 的内容哈希、完整性、代码/producer 与依赖身份；不把整个实验编号或 Metrics 配置放入 Retrain 计算身份。
- 通过已批准范围内的 CPU 集成验证、可重跑示例、数据流说明及配对报告，由用户明确接受、返工或拒绝。完成软件验证不等于正式实验已运行或已接受。

## Confirmed acceptance contract

- Class: `FIX`; Priority: `P0`，位于正式实验执行之前。
- Route: `formal`; Primary surface: `execution / artifact identity / metrics integration`; Decision owner: 用户。
- Minimum real evidence: 隔离 CPU 小图上的真实独立 Retrain 与 GNNDelete/GIF 输出；冷/热与跨方法复用的 producer 记录；禁止训练后的 Metrics-only 运行；同请求/错身份验证；原始输出与指标读回一致性；可重跑命令和数据流说明。
- Report size: 同目录配对 REPORT.md / REPORT.html，由实现阶段生成；登记阶段不创建报告或伪证据。
- Post-candidate decision: 形成精确候选后停在人类验收；接受并落地后才可能解除本项正式实验前置。仍须满足各实验自己的定义、输入绑定、设备和运行批准。
- Execution topology reason: 使用 linked worktree 形成独立修复候选，保留 AAGU-015 现有候选和验收边界；具体 branch、owner、session 和工作目录在 Claim 时绑定。

## Source and relations

- Source anchor: 2026-08-27 任务 Clarify selector timing in paper（01a04258-40c2-75f3-80a7-52f7bf841e25）。用户原话：“你只需要把 retrain 也注册成一个 unlearning 方法就行。”随后明确同意“删除 eval_collateral.py 内部隐式重训路径，不保留兼容 fallback”，并要求说明 metric 数据流与实验关系。
- 原始对话定位：rollout-2026-08-27T16-31-15-01a04258-40c2-75f3-80a7-52f7bf841e25.jsonl，user message 时间 2026-08-27T09:21:27.102Z / 2026-08-27T11:17:53.135Z。登记前已核对原始消息；方法注册要求此前未形成独立 WorkItem。
- 2026-09-05 本任务用户明确本项属于很靠前的 FIX，“在建好之前就不能跑整个实验”；随后授权“登记这个 block，然后我们就准备开始做”。本轮授权登记，后续 Claim 才开始实施。
- `AAGU-028 depends_on AAGU-001`：继承已接受的实验配置与证据合同。
- `AAGU-028 depends_on AAGU-026`：消费已接受的独立配置、方法缓存和 Selection→GU 实现。026 最终验收未包含独立 Retrain；本项承接遗漏的历史实现需求，不虚构它已被实现或已被验收。
- `AAGU-007 depends_on AAGU-028`、`AAGU-027 depends_on AAGU-028`：既有正式 GU 实验执行根必须等待本 FIX 接受并落地；其后续实验继承该前置。正式 Selector 计时路线同样遵守用户本次设定的实验运行门槛。
- AAGU-015 交付本阶段方案、YAML 与能力覆盖检查，可以独立验收这些材料；本 FIX 不作为其材料验收依赖。任何使用 015 方案的正式执行仍须先满足本 FIX。
- Graph placement: `repair`。优先级、当前线与运行前置由 [WORKPLAN](../../../self/dashboard/WORKPLAN.md) 拥有；本 Record 拥有修复范围与验收。
- 当前代码定位：[方法配置](../../../experiments/modular_config.py)、[GU 消费](../../../experiments/modular_gu.py)、[Evaluation](../../../experiments/modular_evaluation.py)、[既有 run_retrain](../../../attack/pipeline_adapter.py)、[隐式调用路径](../../../eval_collateral.py)、[结果读回](../../../attack/result_cache.py)。执行前须重读当前事实。

## Scope and execution boundaries

- 保留原数据、划分、checkpoint、Selection 和历史结果；不手工删除、覆盖、迁移或改标 Cache V2 Artifact。发生语义变化时产生独立新身份。
- 从已支持的节点删除、GNNDelete/GIF 与本阶段评价出发实现完整最小链路，不扩展所有未来 GU、模型或研究指标；不承接排名比较、完整实验调度或其他不相关算法开发。
- 本地仅进行代码修改与隔离 CPU 软件验证。正式 GPU、SSH 写入、整轮实验、push、install、Apply、清理不属于本次登记或候选实现授权。
- 不修改 SyncMate 通用框架来替代 OpenGU 的方法、产物或 Metrics 职责。若已注册项目执行 stage 消费旧隐式路径，在同一 OpenGU 修复中更新必要调用，不添加 fallback。
- 用户已明确本项为正式实验前置；015 的方案材料、无写入检查和本 FIX 必需的软件验证可以先行。已有历史运行不得因本登记被批量重标为有效或无效。

## Restart and next action

同一 AAGU-028 已完成本轮返工和软件 Verify，等待用户决定。当前验收入口：[REPORT.html](REPORT.html) / [REPORT.md](REPORT.md)。候选为 source branch 当前 clean HEAD；软件检查点、报告增量的验证复用见 Current Verify。此前 06fcd98f 报告只保留为 Git 历史，不代表当前实现或人类接受。

用户提出返工时沿用同一 locator；明确接受后才转 block-closeout。正式 SSH/GPU、矩阵、Apply、push、install 和清理均未执行。

## Status history

- 2026-09-06: 本轮独立调度与离线指标修正完成，163 项测试和示例通过；当前 awaiting acceptance，人类决定待定。

- 2026-09-06: 用户明确要求方法独立执行、独立保存指标，差值与预测比较在结果收集后处理；审查即时评价需求并删除 GU→Retrain 成对调度。在同一 Block 返工；此前候选及报告不再作为当前验收结论。

- 2026-09-05: 已完成本地 CPU 验证和正式配对报告；当前 awaiting acceptance，人的决定待定。

- 2026-09-05: 用户确认此前明确提出的 Retrain 独立方法要求，指定为正式实验之前的前置 FIX，并授权登记。本次 registered / not claimed；未创建任务、Claim、实现或运行实验。

## Execution record

- 2026-09-05：本任务 01a07195-b039-7e41-8697-79771fbf7f4f Claim 同一 AAGU-028；owner codex，canonical Claim revision 1 / ongoing。Linked source 为 E:/project/OpenGU-worktrees/aagu-028-retrain-metrics/GULib-master/GULib-master。
- 已复现：Retrain 小表被拒绝，旧 eval_collateral 运行 GU 和隐式 Retrain，AttackResult 舍入后读回相对差值从 8.15 变为 8.14。
- 实现独立 Retrain、精确节点删除/评价图合同和 Cache V2 单方法完整输出；Metrics 从显式引用读取原始预测。删除旧 AttackPipeline.run_retrain 与 eval_collateral 训练入口；更新 target-direct 的必要消费者及明确 checkpoint 训练条件。
- [数据流与可重跑示例](../../../docs/retrain_outputs.md)；[软件 Verify 脚本](evidence/verify.py)。开发期真实 CPU 检查与示例已通过；最终候选将在干净 HEAD 上统一验证。
- 一次命令目录状态未保持，三个本任务编辑短暂落到 canonical A。逐项核对并转回 linked source，恢复原内容/换行后确认 canonical Git 工作区干净；没有对共享 Skills 或正式数据做修复。
- 软件证据只支持约定本地 CPU 消费链；未进行正式矩阵、SSH/GPU、Apply、push、install 或清理。完成 Verify 后进入 formal 人类验收。

## Previous Verify record — 2026-09-05

- 统一软件检查点：`936394329433bf518fb22c800ca7233af1fb5dbe`，在干净 HEAD 上执行 [verify.py](evidence/verify.py)。17 个测试文件共 160 项通过、0 失败、0 跳过；24 节点可重跑示例退出码 0。细项、运行命令、完整输出引用和原始日志哈希见 [observations.json](evidence/observations.json)。
- 实际观察：独立 Retrain 不训练原 checkpoint、不调用 Selector；冷运行后保存完整 state／logits，热读与跨 GNNDelete/GIF 复用成功。禁止训练和选择入口后 Metrics 两次重算身份与数值相同，Store 未变；模型重建前向逐元素一致。数据／split、请求、模型／训练、删除语义、producer 和依赖错配均按测试拒绝。
- 原始证据：source 下 `.workblock/runtime/aagu-028-verify2/`。两侧 10 个保护根核对，3,995 个历史文件内容哈希未变。第一次统一 Verify 的唯一失败为旧 AttackResult 测试要求舍入；更正为无损序列化断言后，上述完整套件通过。首轮失败保留在 `.workblock/runtime/aagu-028-verify1/`，不作为通过证据。
- 最终候选加入 Report／Record／证据摘要后，复用上述检查点的产品验证；检查实际差异仅为人类表面、证据与进度记录，不改变产品、训练、身份、配置或测试条件。新变化单独检查报告生成确定性、Human Surface 合同、链接、diff whitespace 和浏览器实际渲染。最终 live HEAD 与差异清单保存在 ignored `.workblock/runtime/aagu-028-final-verification.json`，不创建第二套候选类型。
- [配对报告](REPORT.md)首屏含实际增量、核心观察、Agent 建议和唯一待决定投影。HTML 经 Chromium 1440×1000 真实渲染并查看首屏／全页：决定区在首屏，正文、表格和证据链接可读，无横向溢出、断图或脚本错误。390px 宽度额外检查文档无横向溢出；[报告 QA 记录](evidence/report_qa.json)。
- Agent 建议接受本次软件修复；决定者为用户，当前仍待决定。正式 target-direct SSH/GPU、真实数据成本和完整矩阵为 NOT OBSERVED；未作 Apply、push、install 或清理。

## Rework record — independent method results

- 用户澄清：Retrain 和其他 GU 同级，统一入口依 YAML 独立执行并输出模型；单方法指标及必要预测完整保存。跨方法差值在结果回来后处理，GU 不附带调用 Retrain。审查是否存在必须即时重做的指标，只对真实需要保留充分输入。
- 恢复同一 task、branch、locator 和 Claim；源检查点 06fcd98fd225c40aa1855ac99548a818d51d8282。Claim 当前 ongoing revision 4。原 formal 路线、保护历史产物和 CPU-only 软件验证边界继续有效。

- 实现审查：现有标量、预测比较、更新检测指标不需要 GU 与 Retrain 同时运行；耗时／峰值显存属于执行时观测。泛指 MIA 尚需具体攻击协议，当前不伪造通用实现。补充统一单方法 F1／accuracy、分类 AUC、交叉熵及可用性状态；指标计算身份独立于方法输出。
- target-direct 正式表显式列出同级 GNNDelete 与 Retrain；原 306 个 GU 比较单元的科学范围不变，原有内部重训练移为独立结果单元。每个方法完成与验真不依赖另一方法或 collateral；完整 Cache V2 依赖随结果收集后再做差。未执行正式矩阵。
- 开发验证：原受影响 61 项通过；增加矩阵独立完成／热复用和采集后禁止 forward 的检查后，18 个 Retrain/output 测试通过。最终统一 Verify 待干净候选运行，旧结果不替代本轮。

## Current Verify — independent methods and offline metrics

- 软件检查点：`9de1d5f985e5d6ef1dbf162c8fd144dab799ecb9`。在干净 HEAD 上运行同一 [Verify 脚本](evidence/verify.py)，17 个文件共 163 项测试全部通过，0 失败、0 跳过；24 节点示例成功。原始证据位于 source 的 `.workblock/runtime/aagu-028-rework-verify3/`；[observations.json](evidence/observations.json) 保存实际命令、测试结果、输出引用及原始日志哈希。
- 新行为：GU 先独立完成，再单独调度 Retrain；完成条件不包含另一方法或 collateral。各自记录完整模型/预测与 F1、分类 AUC、交叉熵及可用性状态。复制完整 Store 到新目录后，禁止全局模型前向和优化器训练，单方法指标与跨方法差值仍精确重算，Store 字节未变。
- 指标审查结论：当前登记的比较指标都无需同时执行 GU 与 Retrain；保存原始标量及必要逐节点预测、标签、mask、图即可后处理。运行耗时/峰值显存须执行时采集。更新检测 AUC 缺原模型预测时明确报告缺失，通用 MIA 没有伪造实现。完整审查表见 [数据流说明](../../../docs/retrain_outputs.md)。
- 保护核对：source 和 canonical 的 10 个 cache/result 根未变，3,995 个历史文件哈希相同。本轮所有新运行均为临时 CPU 软件验证。
- 修正事件：首次返工候选统一验证 163 项通过；追加热复用的有效方法条件核对后，一项测试访问小表省略的学习率字段而失败。测试改为改变解析后的默认值后，当前完整套件通过。失败记录保留在 `.workblock/runtime/aagu-028-rework-verify2/`，不作为通过证据。
- 本检查点之后只更新 Report、Record、证据摘要和进度记录；产品、配置、训练/缓存身份及测试条件无更改。最终 live HEAD 的实际 diff 与证据复用理由记于 `.workblock/runtime/aagu-028-rework-final-verification.json`；新增内容单独通过确定性生成、报告/WorkItem Human Surface、链接和 diff 检查，复用上述精确检查点的软件结果。
- HTML 在 Chromium 1440×1000 真实渲染并查看首屏与全页；待决定区在首屏，8 个场景及单方法指标表可读，无横向溢出、断图或脚本错误。390px 宽度检查无文档溢出。[QA 记录](evidence/report_qa.json)。
- Agent 建议接受本次软件修复，当前决定仍由用户作出。正式 GPU stage、完整科研矩阵、真实硬件成本为 NOT OBSERVED；不把软件测试当作研究接受。
