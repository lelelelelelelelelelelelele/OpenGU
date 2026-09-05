# AAGU-015 · 能力覆盖与缺口

检查日期：2026-09-05。检查对象为 015 配置候选 `5c5bce4dc5e0ca8a656dbc99e83d378f9d82c6c6` 和当时干净的主项目 `53e1da5b9bfc133ad7526d2aa39e9f647ac15586`。这是代码、注册及已有回执审阅；不声称重新验证远端环境或运行了 015 实验。后续无关文档提交不改变这些被检查源码的身份。

## 1. 职责

| 任务 | 本次关系 |
|---|---|
| AAGU-026 | 已接受的独立配置解析、方法级缓存身份与 Selection→GU 消费能力；接受范围并非所有未来评价组合 |
| SM-005 | 使用 026 的具体配置验证远程执行、观察、回传和校验；已有 Degree、B-Hutch 和 D-full 证据 |
| AAGU-015 | 当前阶段实验方案、实际配置、入口映射和覆盖检查；不承担所有缺失能力的开发或全量实验 |

## 2. 可用入口

| 入口 | 已有能力 | 对 015 的限制 | 核对位置 |
|---|---|---|---|
| modular | 17 个 Selector；完整 Score/排名/Selection；固定 Selection→GNNDelete/GIF；utility Evaluation | 015 的 retrain-gap case 不在该消费者支持表内；Dataset/Selection 仍需实际绑定 | [modular_run](../../../experiments/modular_run.py)、[方法分发](../../../experiments/target_direct_v1/methods.py)、[modular_gu](../../../experiments/modular_gu.py)、[评价注册](../../../experiments/modular_evaluation.py) |
| target-direct formal v2 | 三数据集、三 seed、两预算、17 Selector；固定 Selection 和 checkpoint；GNNDelete、重训练比较及 collateral 产物 | 固定 recipe；GU 表、manifest 与构建器均限制为 GNNDelete；不能直接接收 015 的任意 modular YAML 或 GIF | [stage](../../../experiments/target_direct_v1/syncmate_stage.py)、[构建 GU 配置](../../../experiments/target_direct_v1/build_gu_config.py)、[manifest](../../../experiments/target_direct_v1/build_manifest.py) |
| 通用 run.py→eval_collateral.py | 读取 Selection，运行方法；重新训练参照；输出 gap、collateral、预测 | 使用另一种配置和输出合同；存在代码不等于 015 全组合身份及删除语义已验证，不作为绕过 modular 缺口的自动回退 | [runner](../../../experiments/run.py)、[评估脚本](../../../eval_collateral.py)、[pipeline](../../../attack/pipeline_adapter.py) |
| SM-005 原子 stage | 真实 Cora Degree/GNNDelete/utility、B-Hutch 首次与 warm、D-full Selector-only 运行 | 仅接受自己注册的固定验证单元；不是 015 矩阵 launcher | [主项目 stage](E:/project/OpenGU/GULib-master/experiments/syncmate_atomic_stage.py)、[SM-005 报告](E:/project/SyncMate/.workblock/items/SM-005/REPORT.md) |

上述入口没有一个可据当前证据直接宣称完整覆盖 015。`post_unlearning_utility_and_retrain_gap` 的“仅一个消费者”是独立 Evaluation 注册的限制，不表示全仓库只有一段重训练代码。

## 3. 按方案检查覆盖

| 方案要求 | 已有支持 | 本轮判断与后续缺口 |
|---|---|---|
| 配置、默认值与矩阵 | 实际 parser / dry-run；449 份 YAML | 定义检查已通过；不证明运行输入已绑定 |
| 数据/划分、候选身份 | read_dataset 校验 manifest、数据哈希和实际 mask；SM-005 有已绑定 Cora | 015 三张表仍为空；缺口是本计划的绑定，不能说整个项目没有数据或读取能力 |
| checkpoint 准备/复用 | modular_model 与 target-direct 准备代码；SM-005 有 checkpoint HIT | 本轮真实输入上的准备与共享未执行；按依赖身份复用，不要求重建已有能力 |
| 17 方法评分、排名、选集 | METHODS / resolve_methods；026 数值与消费者证据 | 方法存在；D-full 真实回执只证明对应单元，不代表全矩阵结果 |
| Q1–Q4 对比 | [比较原语](../../../experiments/c_target_v1/core.py) 已含 Spearman、Kendall、Jaccard、common fraction | 方案已给定输入配对和输出口径；当前没有 015 专用分析输出，不把原语当完整分析报告 |
| 时间拆分 | [method_cache](../../../experiments/target_direct_v1/method_cache.py) 和 [run_selection](../../../experiments/target_direct_v1/run_selection.py) 已记录 compute/access/Selection/准备时间 | 共享计算归属及本轮汇总需执行时记录；未观测的成本不填造 |
| 固定 Selection→两种 GU | modular 消费者支持并有 026 CPU 验证 | U 引用未绑定；SM-005 验证部分实际 GU，但不覆盖 GIF 与全部评价 |
| 同请求 Retrain 与三模型评价 | 通用辅助重训练及评估函数；target-direct 的固定 GNNDelete 路径 | modular 未接通该 case；须核对监督、边/特征与评估图语义，不自动认定完整覆盖 |
| 删除目标、保留节点及预测诊断 | attack_eval / 通用 collateral 有部分代码 | 015 当前 Evaluation YAML 只选择六项 retrain-gap 指标；扩展指标需要明确消费者和字段 |
| GU 冷/热读回一致性 | SM-005 B-Hutch 有精确缓存身份与字节校验证据 | 其 f1_drop 0.1089 / 0.1088 差异仍是已报告缺陷；与传输成功区分，不能宣称评价值等价 |
| 运行、收集与设备身份 | SyncMate 已有真实工具链证据 | 后续运行事项；不是本次方案文档验收要求 |

## 4. Retrain 作为独立 Unlearning 方法：登记与实现核对

**登记：未找到专门 Block。** 检查了主项目 27 份 WorkItem、WORKPLAN 和当前 graph：存在 paired-retrain、collateral 修复/重跑及评价描述，但没有以“Retrain 独立方法＋Metrics 消费复用输出”为交付的 Block。AAGU-026 的接受不包含这项独立方法；AAGU-027 承接的是 IF-family collateral 重跑。这里只报告当前可见登记，不把历史讨论等同注册，也不新建 Block。

**实现：已有组成部分，独立方法未完成。**

| 检查层 | 当前事实 |
|---|---|
| 方法注册 | `unlearning_manager.method_map` 没有 Retrain；modular 的 `gu_defaults` 与 `GU_METHODS` 只支持 GNNDelete/GIF |
| 现有重训练 | `AttackPipeline.run_retrain(selected_nodes)` 已存在，返回重训练模型与效用；它是辅助调用，不是可独立选择的 GU 实例 |
| 现有 Metrics | `evaluate_retrain_gap` / `evaluate_collateral_damage` 可比较模型；predictions.npz 支持保存三组 logits |
| 执行与评价分离 | 当前 `eval_collateral.py` 仍主动运行 GU 与 run_retrain，再算指标；不能说 Metrics 全部已改成只消费独立持久化输出 |
| 缺失的完整接口 | 可解析的 Retrain 方法表、对应执行消费者及独立结果身份、复用参照输出的 Metrics 接入和实际验证 |

依据：[GU 小表解析](../../../experiments/modular_config.py)、[GU 分发](../../../experiments/modular_gu.py)、[UnlearningManager](../../../unlearning_manager.py)、[run_retrain](../../../attack/pipeline_adapter.py)、[Metrics 函数](../../../attack/attack_eval.py)、[调用路径](../../../eval_collateral.py)。

Stage U 继续保留 GNNDelete/GIF 两种已注册方法和重训练评价需求；不增加无法解析的 Retrain YAML，不把 612 个 GU cell 偷换成已包含独立 Retrain 的矩阵。

## 5. 本次验收与后续实现

本次可验收的是方案、真实配置、检查结果及上述覆盖说明。这里明确列出的运行/能力缺口不是伪装成通过的项目，也不自动变成 015 必须开发的代码任务。后续若要执行受影响单元，先明确缺口的实现归属和验收，再绑定输入并按获批范围运行。未登记的能力需求不在本轮擅自创建 Block。
