# AAGU-029 · 指定节点评分与分阶段计时接口

Block ID: `AAGU-029`
Item Version: 2.1
Item Type: Block
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-029/WORKITEM.md`
Acceptance Route: `practical`
Execution topology: `parallel`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

为大图实验提供一个独立的 Selector 计时入口：在完整图和既定模型上只给显式指定的少量节点打分，例如计算 10 个节点的 gt_full influence，从实测取得固定准备与逐点评分成本，支撑后续运行可行性和时间估算。

### 本次增量

先从 gt_full 做到端到端可用，抽象 score_nodes(context, method, node_ids)。完整图、模型/checkpoint、训练集合、Hessian/source 集合及评价目标由 context 固定，node_ids 只限定评分查询。避免为少量查询隐式生成全候选逐点梯度。输出指定节点及分数、查询覆盖、输入与实现身份，并分别记录准备/IHVP/候选评分时间和逐点或分批时间、受影响邻域规模；明确 GPU 同步与计时开销。当前仅登记未来工作，不实施接口或运行实验。

### 核心验收

- 同一模型、完整图与参考集合下，少量节点评分与全量结果中对应节点一致；可验证实际候选循环只访问指定节点，且训练/评价/source 集合没有缩小。
- 查询数量与删除预算 K 独立；部分 Score 具有明确覆盖和身份，不冒充全候选排名或完整 Selection，也不覆盖既有缓存。
- 计时区分一次性准备与节点相关计算；HIT 保留历史计算基准，当前读取消耗另列。非逐点独立的方法不通过截断参考集合改变算法含义。
- 从当前配置和消费者出发完成隔离 CPU 真实调用验证与配对 Markdown/HTML 报告。真实大图/GPU 基准由之后获准的具体实验承担，不用小测试声称完成跨规模估算。

## Confirmed acceptance contract

- Confirmation source: 2026-09-06 用户明确认可指定 10 节点的独立计时接口，要求“这个是未来的 block，你可以先把 block 创建下来，因为它是大图实验的一环”。本次授权为登记，后续 Run 再 Claim。
- Route: practical；Primary surface: Selector partial-query correctness / timing evidence。
- Decision owner: 用户。
- Minimum evidence: 完整参考集合保持、subset/full 对应分数一致、实际查询范围计数、独立阶段计时、不可混用的部分 Score 身份和可读报告。
- Report size: paired Markdown/HTML after Verify。

## Context and relations

- Related: AAGU-002 设备与运行就绪、AAGU-015 实验定义及成本口径；本 Block 为未来大图实验提供计时能力，不自动完成两者。
- Prerequisites: 已接受的 AAGU-001 配置合同与 AAGU-026 模块化消费基础。
- 当前入口：experiments/target_direct_v1/methods.py、method_cache.py；底层候选与 source 分离能力位于 experiments/c_target_v1/core.py。
- 完整大表耗时模型、跨规模拟合及预测误差校准是另一个独立课题；SyncMate 的运行限时及停滞检测不在本接口内重复实现。

## Runtime and authorization boundaries

- 当前 registration only；不 Claim、执行、SSH/GPU、部署或修改历史结果/Cache V2。
- 后续实现使用独立 linked worktree，保留其他任务修改；不修改科研定义或采用旧实验入口替代当前注册入口。
- 所有成本估计保留实测、推断和未知的区别；不得将 10 点测量标成全量实测。

## Restart and next action

后续使用 block-workflow 读取同一 locator，重读当前指令、实现及 live Claim，Claim 后实现并验证最小 gt_full 指定节点评分/计时链路。当前不创建执行任务。

## Status history

- 2026-09-06：按用户已确认接口设计登记为未来 Block，registered / not claimed。
