# AAGU-031 · Selector Stage S 正式运行与 Q1–Q4 分析

Block ID: `AAGU-031`
Item Version: 2.1
Item Type: Block
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-031/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

优先启动 015 已完成定义的 Selector 阶段，把其已接受的实验表、配置和软件验证转成真实数据上的分数、排名、选集以及 Q1–Q4 科研分析。当前研究阶段应尽快形成可审阅结果，不等待下一阶段的完整实验表整理。

### 本次增量

直接消费 015 的 Stage S 方案及其生成配置：Cora/CiteSeer/PubMed、GCN、训练 seeds 42/212/2024、训练候选预算 1%/5%、17 个 Selector，共 306 个计划 cell。先完成真实输入/身份绑定、已注册入口和正式运行前置核对，再按最小正式验证、成本检查、分批运行、收集核验与分析的顺序推进。Q1–Q4 的比较对象、控制变量及解释边界沿用 015，不重新设计。

015 的已接受软件样例不计作本轮研究结果。保留其独立已接受 WorkItem；本项承接实际运行与分析。Stage U 的 GU/Retrain 正式矩阵、原 HTML 的完整 GU 主矩阵以及后续消融/泛化由下一阶段拥有。

### 核心验收

- 015 三个数据集、seed、预算、候选集合、17 方法和 Q1–Q4 均有从批准定义到本轮配置及实际 Artifact 的可追溯映射；完整 mask、candidate、checkpoint 与 producer 身份通过验证，不以预计数量替代实际身份。
- 正式运行前满足 AAGU-002 设备就绪、已接受代码与配置落地、共享 stage check 及专题 preflight；明确实际 launcher、最小正式切片、成本门槛、失败恢复边界和分批计划。证据仍有效的既有 gate 可复用，不把下一阶段的总表工作增加为前置。
- 完成 Stage S 计划范围的完整分数向量、排名、按预算派生的 Selection 和逐阶段成本，附 planned/observed/failed/unavailable 明细。重复依赖按真实身份复用；不能把配置去重组数当实际 HIT 或把部分运行称完整覆盖。
- 用收集且核验通过的产物形成 Q1–Q4 成对比较，包含 Spearman/Kendall、common fraction/Jaccard、逐 seed 结果和成本；常量分数/指标无定义显示原因，结论与实际覆盖相匹配。
- 交付可复用的 Score/Selection 引用清单及配对 Markdown/HTML 分析报告；用户能检查比较、范围、缺失和研究结论。未完成 cell 需明确返工或范围决定，不静默缩小矩阵。

## Execution contract

- Class: EXP；Priority: P0；Route: formal；Decision owner: 用户。
- Confirmation source: 2026-09-06 用户要求按 Phase 分组，并明确“重点是之前的这个阶段，就是 015 所对应的这阶段，其实应该赶紧开始”。该指令确立当前阶段优先级与独立承接范围，正式作业仍满足已存在的设备、身份和最小验证门槛。
- Execution topology 为 parallel，使用 linked worktree 维护本项定义绑定/收集/分析产物；正式 GPU 作业仅在 SSH 活跃检出执行，遵守实验目录的 pinned SHA 规则。
- Prerequisites: AAGU-015 已接受方案、AAGU-002 设备就绪、AAGU-028 已接受运行基础。001/006/026/009 的已接受合同与实现从 015 继承。
- AAGU-030 不是本项依赖；旧 007/008/011/012 的 GU/replacement 编排也不是 Stage S 前置。阶段分组与输入依赖分开，不因编号相邻而阻塞。
- 本项可先完成只读准备与身份核对；正式 GPU gate/matrix 在本轮设备、版本、输入、launcher、成本和调度条件明确后按注册范围执行，不从“已存在 YAML”直接铺开全矩阵。
- 不改变已批准科学定义，不重写历史 Cache V2 Artifact，不用临时 split、其他目录同名数据或 toy 样例替代正式输入。缺失数据准备或执行能力按实际责任承接，不重复注册已接受的实现任务。

## Source and configuration

- [015 已接受方案](../AAGU-015/EXPERIMENT_PLAN.md)、[015 当前验收](../AAGU-015/WORKITEM.md)。
- [Stage S 源表](../../../experiments/configs/aagu015/stage_s.yaml)、[配置入口及运行边界](../../../experiments/configs/aagu015/README.md)。
- 已生成的 stage_s 大表由现有 `experiments/run.py` 消费；正式提交与收集沿已接受的项目运行通道绑定，不能凭名字切换到旧 target-direct recipe。
- [设备 gate](../AAGU-002/WORKITEM.md)、[实验执行规则](../../../experiments/AGENTS.md)、[WORKPLAN](../../../self/dashboard/WORKPLAN.md)。

## Restart and next action

当前先推进 AAGU-002 设备准备与就绪结论；本项复用 015 已确定表格完成真实输入绑定和最小运行准备。使用 block-workflow Claim 同一 WorkItem，读取当前入口/代码/数据事实，按现有 gate 顺序运行并分析 Stage S，不等待 AAGU-030。

## Status history

- 2026-09-06：按用户要求将 015 对应研究阶段设为当前优先阶段，登记独立 Stage S 正式运行与分析承接 Block；未 Claim 或启动 GPU 作业。
