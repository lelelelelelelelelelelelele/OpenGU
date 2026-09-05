# AAGU-033 · D-full 有效性正式运行与分析

Block ID: `AAGU-033`
Item Version: 2.1
Item Type: Block
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-033/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

将 AAGU-032 经用户验收的 D-full 有效性实验表与配置转成真实运行证据，回答其删除集合相较 Degree 是否造成更大的 GCN 真实重训练性能下降。本项在 AAGU-007 最小正式实验验收后推进，与 AAGU-031 的 Selector Stage S 正式运行与 Q1–Q4 分析并行，拥有独立的实验范围、结果和人工验收。

### 本次增量

消费 032 最终接受并落地的方案、实际 YAML 与配置检查，以及 007 已接受且身份仍有效的最小正式运行证据。按批准范围逐数据集完成 Score / Selection → 独立 Retrain → Metrics、远端产物收集与身份核验、逐 seed 对照分析和配对 Markdown/HTML 报告。先完成首个获批数据集的运行与分析，再按方案和用户决定逐个推进后续数据集。

模型使用 032 已确认的 GCN 路线；D-full（当前实现 gt_full）变体、Degree 对照、数据/split、候选集合、预算、seed、删除及评价语义和计划数量均以 032 最终接受版本为准。本次不提前冻结仍待验收的参数建议，也不把本 Block 登记视为方案已接受。033 可以独立生产所需 Score/Selection；如 031 或其他已验证来源存在精确匹配的 Artifact，可按身份复用，复用机会不构成对 031 全矩阵完成的等待。

### 核心验收

- 032 已接受方案与本轮配置、源码完整 Git SHA、正式数据/split、candidate、checkpoint、producer 和 Artifact 逐项对应；正式执行满足 007 接受、当前设备与版本条件、共享 stage check 及本范围 preflight。007 未覆盖的入口、输入或方法完成有界补充验证，不把最小切片泛化为所有专题均已验证。
- 计划范围、实际完成、失败与缺失 cell 明确列出。每个获批比较包含对应 Selection、独立 Retrain 输出和离线 Metrics；只使用收集且核验通过的实际产物，不以 dry-run、smoke 或历史软件样例替代正式结果，不静默缩小矩阵。
- 按 032 的公平比较规则报告固定 test 集上的 accuracy / micro-F1、相对未删除基线的变化和逐 seed 的 Degree 对照差值。辅助 loss 与主效用分开；如沿用 F1_Retrain_Degree - F1_Retrain_variant，正值只表示该变体造成更大重训练损害，不解释为近似 GU 的 retrain gap。
- 结果为正、无明显差异或弱于 Degree 均如实呈现；“必须超过 Degree”不作为验收条件，不使用 test 结果回流选点或调参。实际覆盖与结论适用范围一致。
- 交付可追溯的运行/收集/验证清单、产物引用和配对 Markdown/HTML 分析报告，区分实测、推断与未知；用户据此独立接受或要求返工。031 的完成或接受不自动完成本项。

## Execution contract

- Class: EXP；Priority: P0；Route: formal；Primary surface: 正式实验产物与 D-full 有效性分析；Decision owner: 用户。
- Confirmation source: 2026-09-06 用户在明确“032 负责方案、实际运行位于 007 验收后”的边界后，要求新建 032 的运行 Block，并明确其与 Selector 运行线为平行关系。本次只授权登记与 Graph/编排更新，不启动执行。
- Prerequisites: AAGU-007 已接受的最小正式实验、AAGU-032 已接受的实验表与实际配置。002 的设备基础和 001/015/026/028 等方案/实现从两项前置继承；正式运行时仍需核对其当前有效性。
- Parallel research branch: AAGU-031 与 AAGU-033 均从 007 后展开，彼此没有 depends_on；031 消费 015，033 消费 032。资源调度按实际 GPU 与任务状态协调，研究上的并行不等于必须同时占用 GPU。
- Workstream: Phase 1，与 031 同阶段承接早期正式实验；不等待 030 总表、011/012 后续 GU 主矩阵或 020～022/029 计时能力路线。若最终获批方案确需新增能力，应先明确具体缺口与真实依赖。
- 后续使用 linked worktree 维护本项配置绑定、收集和分析材料；分支、owner、session 和工作目录在 Claim 时确定。正式 GPU 作业仅在 SSH 活跃检出运行，遵循 [实验执行规则](../../../experiments/AGENTS.md) 的版本、设备、正式数据和缓存边界。
- Launcher 与产物合同消费 032 最终接受版本及其实际消费者；不根据历史配方名猜入口。采用已注册的运行/收集通道，不因存在 YAML 就直接展开作业。

## Scope and evidence boundaries

- [032 方案与配置 owner](../AAGU-032/WORKITEM.md)、[007 最小正式实验 gate](../AAGU-007/WORKITEM.md)、[031 并行 Selector 运行线](../AAGU-031/WORKITEM.md)、[当前编排](../../../self/dashboard/WORKPLAN.md)。
- 032 持续拥有方案与参数选择，本项负责其已接受版本的运行和分析；不代替或修改正在实施的 032，不重复注册相同方案。
- 不扩大到近似 GU 主矩阵、全部 17 个 Selector 或 SGC/SGN 等其他模型，不自动把一个数据集扩大为所有数据集；范围变化须有新的明确决定。
- 精确复用由 consumed input、producer 与依赖 Artifact 身份决定。不得手改、覆盖、删除历史 Cache V2 Artifact、正式数据或结果，也不得在未核验时把已有文件标为 HIT 或可信证据。
- 代码或入口缺陷、输入身份不清、GPU 不可用、已有产物冲突时停止受影响运行并记录真实缺口；不降级到 CPU 正式实验，不自行使用 force、临时 split 或同名副本继续。
- 完成 Verify 与报告后进入 awaiting_acceptance，等待用户对同一 Block 的决定；本次登记不构成 Claim、执行批准、科研接受、Apply、部署或清理。

## Restart and next action

后续使用 block-workflow 重读同一 locator、007/032 的最新接受与交付事实、当前项目指令及 live Claim。先确定前置已满足和当前批准范围，再 Claim 同一 Block、绑定执行上下文，分批运行并收集分析。与 031 协调共享资源和精确产物复用，不等待其全量完成，也不改动其生命周期。

## Status history

- 2026-09-06：按用户要求登记为 032 的独立正式运行与分析 Block，前置 007 和 032，与 031 平行；registered / not claimed，未新建执行任务、Claim 或运行科研作业。
