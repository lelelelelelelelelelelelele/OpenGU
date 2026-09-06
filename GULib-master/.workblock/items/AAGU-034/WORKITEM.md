# AAGU-034 · 实验配置与统一执行入口修正

Block ID: `AAGU-034`
Item Version: 2.1
Item Type: Block
当前状态: `accepted`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

> Git baseline：`2b9bcafbfc789d0c60362b4246eee2a34440213b`

> Source branch：`refs/heads/codex/aagu-034-unified-execution`

> Remote target：`origin refs/heads/main`
Stable locator: `.workblock/items/AAGU-034/WORKITEM.md`

## Human Surface

### 核心意图

将已接受的 001 模块合同与 026 模块化实现收敛为实际可用的一套实验 YAML 规范和一个通用执行入口。公共 Dataset/Split、Selector、Unlearning、Evaluation 小表由公共目录持有，实验组合表引用它们并声明本轮训练 seed 与预算；配置检查、真实训练、缓存和执行注册消费同一份展开后的有效配置。

本项是 AAGU-026 的后续返工修正，解决其入口与配置规格未统一的问题，并接管 015 的冗余配置生成和 001 文档表述修正。用户明确要求另插一个 FIX Block，不将公共设施整改继续塞入 032 的实验方案范围。历史已接受记录保留，新发现与修正由本项承担。

### 本次增量

1. 以 015 使用的通用小表格式为统一依据，将可复用配置整理到 experiments/configs/selectors/、datasets/、unlearning/、evaluations/。同语义实例只维护一份，015、032、模板及仍有效的执行配置引用公共表；数据划分或方法参数不同的实例明确区分。
2. 统一 experiments/run.py 的配置检查与实际执行路径，复用 modular_config/modular_run 及现有训练、缓存、独立输出能力。SyncMate/项目执行上下文提供设备、路径、运行身份与正式检查，调用同一入口/内核；不另造专用矩阵执行框架。
3. 盘点仍被注册计划消费的旧 target-direct 与旧扁平 YAML 路径，迁移需要保留的消费者、预检、输出与收集接缝后，删除被替代的专用配置解析、调度分支、重复小表与过时注册。不得用兼容层、回退或第二套配置规格保留旧路径；共享评分算法与证据读取模块按实际依赖保留。
4. 取消 015 按 seed/预算生成 424 份 YAML 的方式及对应冗余文件。用普通组合表与运行时内存展开表达其原有科学范围；多个数据集可各用一张组合表，不因此引入新的多数据集调度抽象。后续阶段绑定真实 Selection/Output 引用，不能为减少文件数量改为重新抽样或伪造资产。
5. 大表仅允许显式覆盖训练 seed 与预算：大表指定值优先于小表填写值，小表填写值优先于方法默认值；省略大表字段则沿用小表。覆盖不写回源文件，最终有效值和来源必须可审阅。训练 seed 配对模型型 Selector 与 GU/Retrain，不改 Dataset/Split seed 或 Random 抽样 seed；不开放任意参数覆盖。
6. 同步修正 001 合同、模板、配置目录说明、实验入口说明、受影响测试及当前任务引用，并重建由生成器拥有的投影。032 继续只负责科学方案与最终组合配置的验收。

### 核心验收

- 一份普通实验组合 YAML 能经同一通用入口完成 dry-run 与隔离 CPU 实际执行；注册的项目/SyncMate 调用复用同一解析、展开、执行链，不能出现新格式只支持 dry-run、实际执行仍走另一专用解析器的状态。
- 公共配置中 17 个 Selector 的方法语义、默认值与真实依赖经过迁移前后核对。TracIn 必须结合实际训练轨迹验证 3/6 个 checkpoint 的选择，不把两份 YAML 的字段差异直接判为算法差异，也不能把 _6 默默变成全部 100 个 epoch。
- 015 的原有三数据集、17 方法、三训练 seed、两预算及阶段含义保持；032 的 7 方法 × 2 预算 × 3 训练 seed 仍为 42 条件。维护文件数量与逻辑条件数量分别列明，不为注册生成逐条件/逐阶段 YAML。
- 通过实际命令入口在临时数据、临时 Store 上完成至少两训练 seed、两预算、模型型与无需模型的 Selector、独立 Retrain 和指标读取。断言真实训练使用覆盖后的 seed，选点数来自覆盖后预算，重训使用真实删除集合；再次执行禁止训练/评分 producer 仍正确 HIT，输出身份一致。
- 核对缓存影响边界：仅预算变化复用预算无关评分并区分 Selection；训练 seed 影响使用该模型的计算，不影响无需模型的 Degree/Random。缓存读取展开后的有效输入及 producer 身份，公共文件路径本身不进入计算键；真实实现变化导致的 MISS 如实报告。
- 当前有效的执行注册、配置指纹、预检、输出清单与收集核验在迁移后相互一致。使用隔离本地/CPU 消费者验证注册与收集接缝；旧专用解析、过时注册及 424 份生成 YAML 在活动代码/配置中退役，活跃引用检查无遗漏。
- 交付配对 Markdown/HTML 验收报告：列出规范、一个可复用模板、迁移前后配置与入口映射、文件数量、真实命令及测试结果、保留的共享模块和待正式验证事项。用户可独立判断修正是否完成；不把内核测试或 dry-run 说成端到端命令与正式运行已验证。

## Execution contract

- Class: FIX；Priority: P0；Route: formal；Primary surface: 公共配置/入口整改与真实执行、缓存、注册/收集验证；Decision owner: 用户。
- Confirmation source: 2026-09-06 用户已审阅六项问题清单，明确其不属于 032、应作为前序实现返工插入新的 FIX Block，并要求核对无误后注册。本轮仅授权登记、必要关系与编排更新，不 Claim 或实施。
- Prerequisites: AAGU-001 公共合同、AAGU-026 模块化实现、AAGU-015 已接受 Selector 定义与配置、AAGU-028 独立 Retrain / Metrics 能力。均消费其当前已落地成果，不重开其历史生命周期。
- Execution topology: parallel；后续在 linked worktree 中形成独立候选。owner、session、分支和工作目录由 Claim 时决定，Init 不预先绑定。
- 本项的软件验证不依赖 AAGU-007 正式实验结果，避免整改与首次正式验证互相等待；接受后的本项是 007 使用统一入口开展最小正式实验的前置。
- 使用现有依赖与模块分层；不添加任意 override 框架、另一套 Cache、专属调度器或兼容路径。
- 完成约定验证后停在 awaiting_acceptance，等待用户接受；本次登记不授权后续 Claim、实现、正式 GPU/SSH 作业、数据准备、push/install/Apply 或清理。

## Source and relations

- `AAGU-034 correction_of AAGU-026`：修正已经结束的模块化实现中两套 Selector YAML 规格、多个执行路径和完成表述未收敛的问题；不撤销其已验证的真实缓存/消费者证据。
- `AAGU-034 depends_on AAGU-001, AAGU-026, AAGU-015, AAGU-028`。
- `AAGU-007 depends_on AAGU-034`：最小正式实验应验证本项接受后的统一入口及对应注册。原设备、数据、批准与其他前置继续有效。
- `AAGU-032 depends_on AAGU-034`：科学方案讨论可继续，最终可执行配置与模板的验收消费公共修正。032 不再负责通用入口/公共目录/旧路径清理。
- 031、033 经既有 007/032 关系继承修正前置，二者仍互不依赖；030 的独立方案准备不新增等待本项的条件。
- 任务与依赖事实见 [当前编排](../../../self/dashboard/WORKPLAN.md) 及 canonical .workblock/graph.json；生命周期只由各自 WorkItem 和 live Claim 持有。

## Observed baseline and evidence boundaries

- 核查锚点：2026-09-06，canonical main@f03b40e160953add7b280792d1e13048852f2a3f；032 linked candidate@de403104bf83522e34c7570e27cb976152af9527。后续 Run 必须读取届时最新 main 与源文件，不把本登记快照当作 Claim baseline。
- V2 的 17 份独立 Selector 小表创建于 026 提交 35eeced6；015 的同名小表创建于 59baa2ae。gt_full 的方法参数相同，但通用解析器要求 candidate/budget，V2 解析器拒绝这两字段。015 当前 449 份 YAML 中 424 份属于 generated/。
- 当前 run.py 对 kind: experiment 明确只放行 dry-run；真实 modular_run.execute(context=...) 已存在，SyncMate atomic stage 使用它。旧 target_direct_v1.syncmate_stage 仍被 opengu_recipes/opengu_adapter 调用。必须统一这些实际接缝，不能只改文档或移动文件。
- 032 未接受候选中的两轴展开、模板与 55 项 CPU 验证仅作为可复用参考；034 不依赖 032 被接受，不整包合入 032 的实验方案或把其旧回执当成本项新验收。必要实现由本项在自身候选中复核。
- 保留现有评分算法、删除语义、正式数据、历史结果及 Cache V2 Artifact。禁止手工改名、覆盖、修复或删除缓存/证据，不因 YAML 迁移清空缓存。不新增算法、模型、科学矩阵或指标定义。
- 实施中的 CPU 小图验证使用临时资产与独立 Store；正式远端部署、GPU 验证和科研矩阵由后续明确批准的门槛与执行任务承担。登记与软件测试不冒充正式实验就绪。

## Restart and next action

用户已确认阶段核验、Core 清单去重及当前交付范围三处返工通过，并明确要求 closeout。最新软件修正位于本 source branch；此前311项结果保留其原检查点含义，本轮独立 validator 结论由用户回传，Agent 未重跑测试。下一步按同一 WorkItem 完成接受投影与 Closeout；不启动正式实验。Core 去重独立提交为 SyncMate `7231b69201822f04d171f0980ab86009dfa7d398`，未更新安装包或消费者依赖绑定，不把源码接受称为部署完成。

## Status history

- 2026-09-06：按用户明确要求登记独立 FIX，归为 026 的后续返工，插在 007 正式实验和 032 最终配置验收之前；registered / not claimed。未创建执行任务、Claim、修改产品代码或运行科研作业。
- `accepted`（2026-09-07T05:21:07+08:00）：用户 基于 用户确认独立 validator 已通过阶段核验、清单去重与当前交付范围三处返工，并明确要求 closeout；本轮不重跑产品测试。 接受当前已验证候选。

## Run · 2026-09-06

- 用户在本任务明确授权使用 block-workflow Claim/实施，同一 Block 停在人类验收；后续又明确授权先提交 canonical 的 AAGU-007 草案再继续。该授权覆盖原登记阶段的未 Claim 边界，不包含正式 GPU/SSH 作业或 Closeout。
- 已核对最新 WorkItem、WORKPLAN、Graph factVersion 20、001/015/026/028 已接受记录和 live Claim。007 草案12个关联文件按用户授权单独提交为 `2b9bcafbfc789d0c60362b4246eee2a34440213b`；旧格式 dry-run 展开4个独立方法输出，未启动正式实验。
- Owner: codex；session: AAGU-034 · 实验配置与统一执行入口修正；linked source: `E:/project/OpenGU/.worktrees/aagu-034/GULib-master/GULib-master`；authority: `E:/project/OpenGU/GULib-master`。
- canonical Claim: `30005e0e-80bc-40da-955b-85602b1c501d`，revision 1，ongoing。仅拥有本 Block 的配置/入口/文档/测试与验收表面；保留正式 Cache V2、数据与历史 evidence。
- 实施过程记录在本机 ignored `.planning/aagu-034/`；持久验证与报告见下方。


## Verify · 2026-09-06

- 干净软件检查点：`380105002579c99ad003418648a85e67da413a0a`。完整相关 Verify 执行后工作树仍干净，349项测试通过（224.90秒，2条依赖警告），配置审计、dashboard projection check、SyncMate smoke均exit 0。全测试collect-only为750项，未宣称全部750项执行。
- 普通命令真实执行 **PASS**：20节点/10训练候选，Degree、Random、a_grad_norm，两训练seed122/722，两预算0.1/0.2，独立GNNDelete/Retrain共产生24输出；实际训练使用覆盖seed，选点数1/2，源YAML字节不变。直接CLI Stage S后绑定真实summary执行Retrain，无重采样。
- 缓存边界 **PASS**：warm禁用训练/评分仍全部HIT且输出身份一致；Score分组1/1/2、Selection分组2/2/4。有效实现与方法参数变化只影响相关producer，文件路径不进入计算键。TracIn选择函数变更会更新依赖它的producer指纹，不能承诺旧Score及下游身份继续HIT；未改写历史缓存。
- 17方法与checkpoint语义 **PASS**：同图与原评分公式比较的最大绝对误差均0；真实100-epoch轨迹的公共point 3/6评分分别绑定[1,50,100]与[1,10,25,50,75,100]；六种TracIn配置使用同一检查，错误100步输入拒绝。
- 独立Retrain/Metrics **PASS**：真实删除集合、保留监督与去除关联边可从输出验证；12行配对指标由保存输出读取，额外消费者回归在禁用训练和模型forward时仍完成。
- 注册/收集接缝 **PASS（隔离本地/CPU）**：1项007普通注册为4输出/17文件；同形CPU两预算测试经过真实命令、队列/receipt、33文件收集与核验、8结果读取；重复fetched=0，9类故障拒绝。只替换OS/GPU策略，未实际SSH/GPU运行；生产预检在本机拒绝错误根/GPU且不读正式数据。
- 配置迁移与当前引用 **PASS**：活动YAML 522→46，公共小表28、普通组合表18；015为12张维护文件/306 S/612 U/306独立Retrain，032为42条件。424张生成表删除，35历史配置Git原文保留，旧专用运行/注册/无消费者adapter退役。120文档链接核查通过，13个外部DocMap目标在canonical布局下解析。
- 初轮回归暴露旧flat入口、旧注册常量以及已不存在的Cache V1私有hash API测试。已按实际职责更新或退役，保留有效不变量，并由真实普通命令/Cache V2消费者测试覆盖；没有恢复兼容入口。替换清单及原因见evidence/retired-tests.json。
- **NOT OBSERVED**：正式SSH/GPU、真实数据上的成本/显存与旧缓存命中、015全矩阵、007科研gate、032科学方案接受。CiteSeer/PubMed和后续Selection/Output仍需真实资产绑定；本项未准备正式数据或启动作业。
- formal人类表面：[REPORT.md](REPORT.md) / [REPORT.html](REPORT.html)，唯一Human Result和当前待决定投影已检查。headless Edge桌面1440×1000、窄屏390×844及正文/边界真实渲染已查看，首屏决定清晰，无溢出/断图。Agent建议接受软件修正，决定权仍归用户。
- 证据：[观察与349项结果](evidence/observations.json)、[精确命令与退出码](evidence/verify-checkpoint.json)、[配置审计](evidence/configuration-audit.json)、[HTML测量](evidence/render-qa.json)。原始日志/JUnit位于canonical ignored `.workblock/runtime/aagu-034-verify/`，临时数据根记录在回执；正式数据、Cache V2与历史结果不在本项修改范围。

### 首轮报告候选的 Verify 复用（历史）

最终待决定对象是本 source branch 的干净 HEAD，报告与Record提交使其前进。相对上述实测检查点，仅加入本item的报告/运行证据/Verify记录和WORKPLAN、progress.html的生命周期生成投影；实验代码、公共YAML、方法、执行注册与测试合同均无差异。该diff不改变349项测试所回答的问题，复用其精确检查点结果。新增变化独立检查：Human Surface/Human Result结构、报告确定性重建、报告链接与渲染、dashboard重建及check、Git diff --check和最终干净HEAD；最终逐命令结果保存在canonical runtime final-verify.json。

当前保持待决定，不写accepted，不Merge/Apply/push/install，不释放Claim或清理worktree。人明确决定前，不继续正式实验。

## Rework · 2026-09-06 · 旧 SyncMate 残留与两份配置路径

- 用户追问并授权清除旧 SyncMate Python 错误痕迹；再次检查发现 M1 helper 与 OpenGUAdapter 仍作为早期验证支路存在。删除该 helper、无当前消费者的 Adapter 及七项只验证旧入口的测试，修正文档中的保留说明；历史已接受记录和证据不改写。
- 当前 syncmate.py → 独立 Core → OpenGUProjectExtension 保留。007 与 032 两份既有普通 YAML 内容不变；补充从不同 cwd 调用真实 run.py 的两项回归，核对公共引用解析、4/42 条件、2/6 批次、无 producer 和所有源 YAML 字节不变。
- 最邻近的完整 adapter 文件回归10项通过，尚待干净候选上的受影响 SyncMate 全部回归及报告更新。

### Rework Verify · 2026-09-06

- 干净检查点 `81a220e927a5f2600a3c3104d5551af5b7d5d124`，当前 SyncMate 四文件205项通过；745项全测试collect-only成功，配置审计、smoke与dashboard check均exit 0，验证后工作树干净。
- 007/032 **PASS**：从不同cwd分别执行真实CLI，公共相对路径解析正确，2/6批次、4/42条件，无producer，活动YAML原文字节未改；没有新增或改动两项的科学范围。
- 旧 SyncMate 清理 **PASS**：M1 helper、旧OpenGUAdapter/ADAPTER和过时标记不在活动Python中；现代syncmate.py与OpenGUProjectExtension继续通过真实Core、队列、预检、收集校验和结果消费者验证。历史材料保持其原证据含义。
- 复用边界：实际diff仅触及旧M1支路、adapter中无消费者部分、两项CLI测试以及说明/记录。原实验解析、执行内核、方法、数据与缓存代码未改，原检查点139项不受影响结果复用；七项旧M1测试明确退役。最新证据：[回执](evidence/rework-checkpoint.json)、[205项结果与复用名单](evidence/rework-observations.json)。
- 报告提交相对此干净检查点仅更新本item证据/报告/记录与生命周期生成投影，不改变产品或测试合同。新增表面完成结构、确定性重建、链接、真实渲染、dashboard与Git差异检查；最终候选与逐项结果保存在canonical runtime本轮final-verify.json。
- 当前决定保持待决定；验证不等于接受，canonical main尚未合并，所以其旧文件会保留到获准Closeout。未执行Apply、push、install、SSH/GPU、数据准备或历史缓存清理。

### 本轮补充检查的偏差记录

补充检查中的一次仓库全域 `pytest --collect-only` 误导入 `tests/` 外有顶层执行副作用的旧 IM 基准脚本，触发了本地数据下载/处理和 CPU 计算；该进程已停止。随后明确限定 `pytest tests --collect-only`，745项收集通过。逐文件核对创建时间、路径、Git忽略状态和SHA-256后，移除了本次误操作新增的57个文件（40数据、11日志、6编译缓存），并验证均不存在；没有删除既有文件或历史证据。这次误操作及其产物不计入任何正式实验通过结论。详见[新增文件与清理核验](evidence/collection-side-effects.json)及命令回执的interrupted_checks。

正式执行与历史证据边界未因此获得批准；当前候选的205项隔离测试和745项限定目录收集结果独立有效。

## Report rework · 2026-09-06 · 展示注册时的核心问题

- 用户指出验收表面只有增量与测试观察，未呈现034登记时要解决的真实问题；同一Claim返回ongoing（revision 5）。此次只返工报告，不改变产品、配置、测试合同或原始Human Surface。
- 已从首次登记提交619d0f75135727ad09d00d658ef48d16e9bf4841读取原文，核对Human Surface未变；首屏补充“两套配置规格、普通入口只支持dry-run、旧注册路径仍有效、424份生成副本”的问题起点，并将登记六项逐一关联修正与证据。区分原始事实、验收要求和后补发现，不将测试数代替问题是否解决。
- 此次仅检查报告原文追溯、问题到证据对应、Markdown/HTML结构、生成一致性、链接、桌面/窄屏及原始问题表真实渲染。软件结果复用38010500与81a220e9的实测检查点，以及8a554419的最终差异复核；不重复执行产品测试。当前仍待人决定。

- 报告返工 Verify：登记引文与首次Git原文一致，原Human Surface未修改；六项问题对照、证据链接、唯一Human Result/待决定投影与确定性HTML重建检查通过。已实际查看桌面、窄屏及完整问题对照表；决定入口在550/740px处，无溢出或断图。最新表面证据见evidence/report-problem-check.json；本次仅报告变更，软件检查不重复执行，继续停在人类验收。


## Core 接缝返工 · 2026-09-06

- 用户否定专用 stage 和随实现调整测试的做法，要求设备只由 device.yaml / SyncMate 配置决定，Core 负责提交与回传，普通实验入口复用已有内核。同一 Claim revision 7 返回 ongoing；此前的接受建议不再适用于当前返工。
- 先提交验收测试 cdc08804，普通入口设备参数及旧注册入口 RED 共7项。夹具随后补齐模型资源、比例预算、训练型评分和Core本地transport；33条验收断言经AST逐条比较完全不变。保留原始与更正后的文件hash及原因于 evidence/core-contract-freeze.json，不声称测试文件整体未改。
- 删除 experiments/syncmate_stage.py 及其手读队列/receipt、硬编码GPU型号、执行设备和SSH绝对根。注册直接指向普通YAML命令；设备沿Core现有reader进入ExecutionContext。Core保留队列、Git绑定、进程与文件核验职责；没有修改独立Core或增加配置生成器。
- 旧输出测试的生产preflight替换、强改CPU及手写running/receipt夹具退役，改用Core正常提交与真实子进程。当前软件候选须经固定合同及相关消费者/SyncMate回归后才能再次进入人类验收。


### Core 返工 Verify · 2026-09-06

- 软件检查点 c40ee9dae7e63c3e921e221554fbc41fccabd27e。最终分批覆盖257项有效通过结果，逐测试检查点及原始JUnit摘要见 evidence/core-rework-observations.json；各轮失败及复用边界显式保留，不将部分通过的整轮报为PASS。
- 固定行为验收7项PASS：真实Core submit/run完成Selector、Unlearning、Metrics，与直接CLI同配置、同数据、源YAML字节不变；实际回执CPU、Python、cwd、Git身份可见。返回文件1/33/1，热执行HIT，损坏与缺失均拒绝。设备缺项/非法/越界在producer前失败。未替换生产预检、进程或设备策略。
- 33条冻结断言未改；四处夹具更正有原始/更正hash和AST核验。旧stage文案、全注册表hash快照断言退役，保留真实白名单、绑定、路径与消费者边界。此前替换预检的接缝PASS不能作为设备贯通证明，已在报告撤回该表述。
- 007/032原表未改，跨cwd解析4/42条件通过；配置审计46张活动YAML，015科学条件306/612/306保持。Core smoke与固定依赖核验exit 0。
- 运行内存不足、CRLF示例hash和测试import错误均如实记录并完成受影响串行重跑。未启动正式SSH/GPU或改变远端device.yaml；后续runner需在原设备文件声明execution_device。
- 报告/Record候选相对c40ee9da仅更正人类表面、证据和dashboard投影。软件结果按实际diff复用，新增表面执行结构、确定性生成、链接、桌面/窄屏真实渲染、dashboard与Git干净检查。
- Agent建议接受当前软件修正，决定权仍归用户。保持同一Claim、人类验收边界；不写accepted，不Apply/push/install/Closeout或清理。

## AutoReport 补修 · 2026-09-06

- 用户认可现有普通入口、设备配置和Core流程，将AutoReport缺失定位为小缺陷，明确要求接入现有新版系统。同一Claim revision 9 ongoing；先前“全部软件修正可接受”的建议撤回至本项验证完成。
- 在产品代码仍为51ac0e19时先固定5项真实行为测试：直接执行和缓存重复、执行失败、dry-run、损坏日志、Core真实提交。原有临时图与Core工作区夹具复用，没有替换事件producer、生产预检或子进程。
- RED：4失败、1通过，28.88秒。真实实验和Core已正常执行，但没有事件；损坏日志未阻止执行。dry-run无事件已通过。日志和JUnit在canonical runtime/aagu-034-autoreport；本次测试文件先提交，再补产品实现。

### AutoReport 补修 Verify · 2026-09-06

- 测试先提交157f30ce，冻结SHA-256见evidence/autoreport-contract.json。随后接回现有record_event/投影器；整份YAML使用显式experiment身份，原单条件producer保持其语义。冻结测试文件逐字节未改，旧Core冻结合同也未修改。
- 干净软件检查点 `5b03cf30b9d7db1d6a0f520b8ec96fa469e5a3a7` 上48项PASS，203.15秒：5项新事件验收、26项既有AutoReport、10项普通命令、7项真实Core/设备合同。开发过程另有31项GREEN，未与48累加。两条本地CUDA依赖警告保留，实际执行为CPU。
- 实际JSONL确认：冷/热分别started/completed，attempt 1/2；错误图started/failed且无summary；dry-run零事件；损坏日志拒绝且原字节保留；Core子进程复用同一producer。完成事件的summary SHA-256逐一核对。观察、逐测试结果、源临时路径及JUnit摘要见evidence/autoreport-observations.json，真实V3投影副本见evidence/autoreport-observed/。
- 设备与Core提交/收集职责保持已认可流程。新日志在执行根生成；Core清单未加入共享journal，不宣称其已通过远端收集。未实施正式SSH/GPU、正式数据或历史缓存操作。
- 报告候选相对此软件检查点仅补报告、证据、Record、现有设计图说明和看板投影；按实际diff复用软件结果。新增人类表面单独检查结构、原Human Surface、冻结测试、链接、确定性重建和真实渲染。Agent建议接受当前软件修正，决定仍待用户，不执行Closeout。

## Selector 声明返工 · 2026-09-07

- 用户在任务“034现在什么状态了”（01a077b4-7fd8-7741-8682-8563ea9f8d34）明确同意只用 selector_refs 声明选点、由缓存自动查找或计算，并授权返工。继承原任务01a073e3-554d-7260-be07-6f41698b1272的同一034候选8ad752ed、source branch及formal报告；同一Claim已Resume并返回ongoing（revision 12）。
- 本轮明确修正原Human Surface第4项中“后续阶段绑定真实Selection”的使用方式：Selector/Unlearning用户配置只声明selector_refs；运行时通过有效输入与producer解析实际Selection，Artifact身份、哈希及HIT/MISS写入结果，供方法和收集核验消费。保留Metrics的真实Output输入、数据身份检查及历史证据，禁止兼容selection_input或重新引入手工绑定分支。
- 执行与核验共用条件展开；迁移015六张U/Retrain表、活动示例、文档及受影响测试。科学方法、数据划分、三训练seed、两预算与306/612/306条件不变。
- 先冻结真实行为测试，再实施；继承的验收建议暂不适用。完成受影响验证后更新同一报告并重新等待人类验收，不Apply/push/install，不运行正式SSH/GPU或修改历史Cache V2。

### Selector 声明返工 Verify · 2026-09-07

- 16项新合同先提交465567dfa6be0d05a36755be9c71eec049acde15。产品改前RED为10失败/6通过；Python 3.8夹具字符串方法更正在冻结前完成，断言未改。冻结文件与原Core/AutoReport合同字节均核对未变。
- 干净产品检查点5ca0d93e5fc5cdfb75f8339d713f17a64b8f324e上311项执行：310 PASS、1个旧测试引用被删除的变量而NameError。867c806ad11aa20f5f14bc6c49c2ce8d62a31294仅补测试从真实Output取得Selection身份，整份Retrain17项重跑PASS。其余294项按确切diff复用，总计311项有效PASS，不重复累加、不将失败整轮标PASS。
- PASS：Selector/Unlearning仅允许selector_refs，selection_input/selection_source在活动代码及配置中清零；实际展开由modular_config的selector_entries/unlearning_entries共同提供给dry-run、执行与核验。六张015 U/Retrain表显式声明相同17小表、seed[42,212,2024]、预算[.01,.05]，306/612/306条件与12表不变；007/032源表及4/42条件不变。
- PASS：无前序产物可直接计算16条件；Stage S之后同声明GU自动HIT相同Score/Selection，24输出冷/热身份相同，禁止训练/评分仍成功；Core真实本地队列、子进程、65文件收集及16条件核验通过，伪造Selection content_hash被拒绝。实际身份与HIT/MISS在结果保留，不手填历史产物。
- PASS：17方法公式、TracIn真实轨迹、预算/训练seed、独立Retrain、Metrics只读消费、AutoReport以及完整SyncMate相关回归通过。配置/归档审计、smoke、dashboard check、20文档链接、实际独立Retrain示例通过；2条CUDA依赖警告如实保留，运行均为临时CPU验证。
- 产品未改评分、Selection、训练、GU producer及历史缓存。报告/证据提交相对867c806a仅修改本item表面与生命周期投影，软件结果按实际diff复用，新增结构、确定性HTML、链接与真实渲染检查另行验证。逐项结果、原始JUnit哈希、失败原因与临时示例路径见evidence/selector-observations.json；旧证据保持历史含义。
- Agent建议接受本次软件修正，决定仍归用户。验证后停在awaiting_acceptance，不进行Closeout/Apply/push/install、正式SSH/GPU、正式数据准备或历史缓存清理。

## 独立 validator 返工与接受 · 2026-09-07

- 阶段核验：Selector、Unlearning、Metrics 按各自交付结构核对，Metrics 的输入摘要数不等同于指标行数。保持方法输出身份和文件摘要验证。
- 清单去重：SyncMate Core 在 manifest_for_roots 按路径生成唯一记录，保留项目对当前交付重复索引的拒绝；修正由独立 SyncMate 源码提交7231b69201822f04d171f0980ab86009dfa7d398持有。
- 验收范围：项目核验器依据经 Core 提交 handoff 绑定的清单筛选本次记录；其他任务历史条目留在索引，既不参与完整性比较，也不重新读取其文件。
- 用户先确认前两处通过，再指出两个任务65+65文件累计索引触发范围误报；范围返工后明确回复“可以验收通过了，closeout”。这是本轮独立 validator 通过结论与接受授权的来源；未收到其原始日志或测试数量，未将此前311项结果改称本轮执行。
- 按用户“只修改，不做测试”的要求，Agent 本轮仅检查源代码、Git 差异和交付身份，未运行任何产品测试。Closeout 可复用用户确认的同一产品内容；若目标或冲突引入新的产品差异，应停止并交回独立验证。
