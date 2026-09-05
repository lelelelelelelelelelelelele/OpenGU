# AAGU-032 · D-full 有效性实验表与配置

Block ID: `AAGU-032`
Item Version: 2.1
Item Type: Block
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-032/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

为早期 D-full 有效性研究形成一份用户可以直接验收的实验表及其实际配置：只用 GCN 方案和独立 Retrain，比较以 D-full（当前代码 gt_full）为核心的 4～5 个变体与 Degree，检验选出的删除集合能否造成更大的真实重训练性能下降。先按一个数据集组织，完成该数据集的未来运行与分析后再逐个推进。

用户明确本轮只用 GCN，SGN 和 SGC 暂不纳入；只有未来效果不好并经新的范围决定后才考虑其他模型。本项交付实验设计和配置材料，供用户验收；不以完成真实科研矩阵为本次验收要求。

### 本次增量

复用 AAGU-001 实验合同、AAGU-015 已接受的 Selector 定义与表格以及 AAGU-028 独立 Retrain / Metrics 能力，交付聚焦本问题的实验方案表、对应 YAML、配置解析与无写入展开结果及配对 Markdown/HTML 验收报告。主表逐项列明科学问题、Selector/变体及有效参数、Degree 对照、模型、数据划分、候选集、预算、seed、删除语义、指标、计划输出和未来执行顺序。

已讨论的首轮建议是 Cora、当前 70/10/20 划分、训练候选预算 1%/5%、seeds 42/212/2024；作为待验收方案明确写出来源和实际配置。用户尚未指定 4～5 个变体的具体清单，实施时结合现有方法及真实参数形成明确、有比较意义的候选表，标注待验收，不宣称其逐项已由用户确认；不能把 D-full 参数变体和不同 IF 方法混称，也不默认扩展成全部 17 个 Selector。Random 只作为可选对照建议单列。

### 核心验收

- 实验表能直接回答本轮为什么只用 GCN + Retrain、每个变体改变什么、其与 Degree 如何公平比较；已确认要求和仍待验收的具体变体/参数建议清晰区分。
- 定义固定的数据/split、候选 train_mask、预算分母与取整、真实删除监督/边/特征及训练/评价图语义；同 seed 比较保持相同初始化和训练规则。Selector 只使用获准训练/验证输入，test 不回流选点或调参。
- 主结果为固定 test 集上的 accuracy / micro-F1、相对未删除模型的下降量及逐 seed 的 Degree 对照差值；正的 F1_Retrain_Degree - F1_Retrain_variant 表示变体攻击更强。辅助 loss 诊断与主效用分开，不把“必须超过 Degree”作为验收条件，也不把 Retrain 损害说成近似 GU 的 retrain gap。
- 表中可配置的行对应现有模块化消费者能够解析的真实 YAML，完成无写入矩阵展开和表格/配置数量核对；缺失正式输入身份或尚未支持的字段明确记录，不能伪造运行就绪、cache HIT 或实验结果。
- 交付同一 WorkItem 下的实验方案和 Markdown/HTML 验收报告，链接配置与检查证据，说明 Cora 首轮和后续逐数据集推进边界，以及未来 Score/Selection -> Retrain -> Metrics 的复用关系。让用户验收后再决定正式执行。

## Execution contract

- Class: DOCS/CONFIG；Priority: P0；Route: formal；Decision owner: 用户。
- Primary surface: 实验方案表、配置映射与配置检查；Report size: 配对 Markdown/HTML。
- Prerequisites: AAGU-001、AAGU-015、AAGU-028 的已接受合同、方案和运行接口，以及 AAGU-034 已接受的公共配置与统一入口修正；026 的模块化能力由现有方案与实现继承。
- Execution topology: parallel，使用新任务的 linked worktree 形成独立候选；分支、owner、session 和工作目录在 Claim 时绑定。Apply target 为 allocator 核对的 canonical refs/heads/main。
- 本设计 Block 不依赖 AAGU-002 设备就绪、AAGU-031 实际矩阵完成、AAGU-030 总表整理或 AAGU-020～022 计时路线。未来正式执行仍消费实际设备/版本/输入/运行批准，不能把这些运行条件误设为当前文档制作的前置。
- 当前用户明确授权登记此 Block、创建一个新 session 并在该 session 中使用 block-workflow 实施此验收材料；这同时授权实际配置解析/无写入检查和必要的针对性软件验证，不授权正式训练、评分、重训练科研矩阵、GPU 作业或新的模型路线。
- 完成一个经过 Verify 的候选后，进入 awaiting_acceptance 并向用户提交同一 Block 的材料；未获得用户明确接受前，不 Apply、merge、push、install 或清理 Claim。

## Source and scientific boundary

- 2026-09-06 本任务用户先提出只用 Retrain、以 g four / D-full 为核心、4～5 个变体加 Degree、逐数据集测试有效性；随后明确“我们只用 GCN 方案，SGN 和 SGC 方案先暂时不用，如果效果不好再说”，并要求“先创建一个 block，然后给这个 block 开一个新的 session，把这个 block 做一下”，交付给用户验收的实验表。
- [015 已接受实验方案](../AAGU-015/EXPERIMENT_PLAN.md)、[015 当前 WorkItem](../AAGU-015/WORKITEM.md)、[028 独立 Retrain](../AAGU-028/WORKITEM.md)、[031 Stage S 运行](../AAGU-031/WORKITEM.md)。
- 理论和历史来源：[DocMap 论文伴读](E:/project/OpenGU-DocMap/20_研究框架/论文伴读/2210.07441_Characterizing-the-Influence-of-Graph-Elements.md)；[原论文 §5.5 / Table 4](https://arxiv.org/html/2210.07441#S5.SS5)。
- 原表的 IF vs Degree 是删除攻击后的 GCN test accuracy，低值表示强攻击，9 格中 8 格优于 Degree；CiteSeer 5% 为 69.5 vs 69.4，优势并非逐格保证。原文的 SGC 评分/public split/5%、10%、15% 不覆盖用户当前仅 GCN 的选择；本项目方案按 GCN 有效性检验与概念复现定位，不承诺逐值复现原表。
- 旧 DocMap 存在 k=3/7/14 的本地集合删除重训练历史，不能混作本轮已执行结果或恢复已退役预算。科学论证链接 DocMap，当前增量实验表由同一 WorkItem 持有，YAML 由 experiments/configs 持有；不得手改生成报告/看板。
- 不重做 015/026/028 已接受的通用实现，不扩大到近似 GU 主矩阵，不修改历史 Cache V2 Artifact、正式数据和结果。

## Restart and next action

在用户要求的新任务中使用 block-workflow，重读当前 canonical locator 与现有 Claim，在该任务的 linked source 中 Claim 同一 AAGU-032，完成 GCN + Retrain 的实验表、对应配置与检查，并提交人类验收。不要另行登记相同题目的 Block，也不要将“做这个 Block”解释为运行科研矩阵。

## Status history

- 2026-09-06：依据本任务已讨论方案及用户明确创建 Block、开新 session 制作验收实验表的指令登记。登记时未 Claim、未制作候选、未运行正式实验；后续由新任务承担同一 Block 的实施与验收报告。

## 公共设施责任修正 · 2026-09-06

- 用户明确公共 YAML 目录、两套解析器、统一实际执行入口、旧注册与 015 的 424 份生成 YAML 退役不属于 032，另登记 [AAGU-034](../AAGU-034/WORKITEM.md) 作为 026 的后续返工。新增 `AAGU-032 depends_on AAGU-034`，用于最终可执行配置与模板验收；科学方案讨论可继续。
- 032 linked source 中已有两轴展开/模板/测试作为 034 可复核的参考，未经接受不整包落地主线。034 不依赖 032 接受，避免循环；032 后续候选应重新对齐本责任划分和最新公共接口。
- 本轮只登记新 FIX 与必要前置，不更改 032 的 live Claim、候选状态或历史验证，也不表示接受或关闭 032。
