# Thesis Transition Memo

> Status: active
> Role: thesis 线的承上启下文档；连接 2026-02 阶段实验、2026-04 课程报告，以及后续解释性研究与 proposed 收束。
> Use this when: 你要决定 thesis 下一步研究问题、可检验假说、或如何从已完成课程报告过渡到 thesis。
> See also: `README.md`, `PROJECT_MASTER_CONTEXT.md`, `../report/paper/stage_report_2026-02-27.md`, `../report/0417_5003report/main_report/msc_project_report.md`

## 1. Purpose

2026-04 的 `report/0417_5003report/` 已经完成 EE5003 课程报告线，后续不再把 thesis 的开放问题继续混入该 deliverable。

这份 memo 的作用是：

1. 固定课程报告已经稳定的结论
2. 把尚未闭合的机制解释问题转成可检验命题
3. 定义 thesis 下一阶段的双候选 proposed 方向

## 2. What Has Been Established

以下结论已经可以作为 thesis 起点，而不是重新从零开始：

### 2.1 Family-level vulnerability spectrum 已建立

- approximate graph unlearning 在 adversarial deletion 下呈现明显 family difference
- GNNDelete 在已测设置中最脆弱
- GIF 相对稳定
- GraphEraser 在已测设置中呈现 shard protection pattern

稳定落点：

- `../report/paper/stage_report_2026-02-27.md`
- `../report/0417_5003report/main_report/msc_project_report.md`
- `../report/0417_5003report/ppt/final_15min_script.md`

### 2.2 Relative metric 的必要性已建立

- 直接看 raw utility drop 会误读 shard-based family
- `relative_f1_drop` 作为相对 `k=5 random baseline` 的指标，已成为跨 family 比较的关键口径

### 2.3 Attribution logic 已建立

- `retrain_gap` 用于分离删除集本身的影响与 approximate unlearning 的额外误差
- collateral metrics 用于度量 retained-set disturbance
- 这条归因链已经是当前项目最重要的方法论资产之一

### 2.4 Attack strategy comparison 已从“random vs smart”推进到“informed selectors among themselves”

- TracIn / IM / Hybrid 不存在统一全局最优
- selector effectiveness 是 method-dependent 的

## 3. What Remains Unresolved

课程报告已经回答了“是否存在 family-level vulnerability difference”，但尚未充分回答下面这些 thesis 级问题：

1. 为什么某些 family 更脆弱，尤其是 GNNDelete？
2. 为什么某些 selector 对某些 family 有效，而对另一些 family 不稳定？
3. GraphEraser 的“增益”到底是普遍鲁棒，还是某些 partition simplification 条件下的局部现象？
4. 当前的 attack signals 中，哪些真的在刻画 mechanism weakness，哪些只是 proxy for important-node deletion？

这些问题不能用事后解释来回答，必须改写成可检验命题。

## 4. Testable Hypotheses

### H1. Propagation Reach Hypothesis

删除目标的传播范围越大，越容易造成 retained-set damage。

可观测方向：

- spread / topology influence 与 `fraction_flipped`、`mean_pred_shift` 是否正相关
- 这种相关性在不同 family 上是否强弱不同

### H2. Training Influence Hypothesis

删除目标的 training influence 或 gradient alignment 越强，越容易放大 approximate unlearning 的 `retrain_gap`。

可观测方向：

- TracIn-like score 与 `retrain_gap` 的关系
- 这种关系在 GIF 与 GNNDelete 上是否一致

### H3. Family-Specific Sensitivity Hypothesis

不同 GU family 对“结构影响大”和“训练影响大”两类节点的敏感性不同。

可观测方向：

- IM-like structural selector 与 TracIn-like model-aware selector 在各 family 上的效果排序
- 是否存在可重复的 family-specific response profile

### H4. Conditional Shard Protection Hypothesis

shard-based methods 的异常增益主要发生在某些 partition simplification 条件下，而不是普遍鲁棒。

可观测方向：

- GraphEraser 的增益是否依赖 bridge / boundary / hub 类节点
- 若选择更接近 shard-boundary-disruptive 的节点，当前保护效应是否减弱

## 5. Dual Proposed Lanes

当前 thesis 不宜直接拍板单一路线，而应保留两条连贯的候选主线。

### Lane A: Diagnosis-Oriented Proposed

目标：

- 解释为什么不同 family 在 adversarial deletion 下表现出系统性差异
- 产出一个 family-aware vulnerability diagnosis / mechanism audit 框架

适合的 thesis 价值：

- 机制解释清楚
- 与课程报告形成自然延续
- 不依赖必须做出一个“大新算法”

### Lane B: Small Attack Improvement Proposed

目标：

- 在诊断信号的基础上，提出一个小而解释驱动的 attack selector 改进
- 不是重新发明一套巨大方法，而是在已知 TracIn / IM / Hybrid 之上做 mechanism-aware refinement

适合的 thesis 价值：

- 与已有 attack pipeline 连贯
- 结果更容易体现在定量提升上
- 但前提是要有足够强的机制证据支撑，不然容易退化成 heuristic stacking

## 6. Decision Gates

后续 thesis 应如何在两条 lane 之间收束，取决于下面这些判断：

### 6.1 优先收束到 Lane A 的条件

- family-specific mechanism pattern 能被稳定复现
- 假说 H1-H4 中至少有 2 条获得比较清晰的支持
- 小改 selector 带来的提升不稳定，或难以超越解释性贡献

### 6.2 优先收束到 Lane B 的条件

- 至少识别出一个稳定、可迁移的 vulnerability signal
- 该 signal 能转化为一个小而明确的 selector refinement
- 改进在多个配置上优于现有 informed selectors，且不是纯粹随机波动

## 7. Current Working Position

当前推荐立场：

- thesis 第一阶段优先做解释性研究，而不是直接扩展课程报告或急于定义一个大 proposed
- 解释性研究的输出形式必须是 testable hypotheses，而不是 post hoc story
- 如果解释证据足够稳定，再从 Lane A 自然过渡到 Lane B

## 8. Relation To Existing Docs

- `PROJECT_MASTER_CONTEXT.md`
  保存项目的早期统一背景和原始目标设定，适合作为背景参考。
- `flow.md` + `plan_flow_v2_delta.md`
  保存方法、指标与归因框架的实现参考。
- `generalization_experiment_checklist.md`
  保存 2026-02 阶段实验覆盖与完成度。
- `../report/paper/stage_report_2026-02-27.md`
  对应中期阶段的阶段报告。
- `../report/0417_5003report/main_report/msc_project_report.md`
  对应已经完成的课程报告。

这份 memo 不替代这些文档，而是给出一个当前 thesis 线的解释与收束入口。
