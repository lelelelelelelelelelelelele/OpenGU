---
title: TracIn、IF 与 GIF 的 A/B–C–D 关系
created: 2026-07-09
updated: 2026-07-20
type: research-framework
tags: [tracin, influence-function, gif, selector, abcd-taxonomy]
---

# TracIn、IF 与 GIF 的 A/B–C–D 关系

这页只解决一件事：把 influence 系 selector 按实际计算对象分组，避免把 IF、GIF 与 TracIn proxy 混写。所有含 $H^{-1}g$ 的 reference 统一表述为“通过迭代 IHVP 求解”；具体 solver、HVP 与 probe 设置属于实现细节。

> [!summary] 一句话分类
> **A/B 是 target-free 参数变化组，C 是 IF，D 是 graph-aware GIF。**
> C 不含删除后图梯度 `grad2`；D 使用完整的 `grad1-grad2` graph-deletion source。

相关证据：

- [[10_实验矩阵/20_IF目标层级对比实验计划]]
- [[10_实验矩阵/21_C目标TracIn与GIF近似有效性实验计划]]
- [[10_实验矩阵/11_策略输出重合度实验]]
- [A/B–C–D 验收报告](../../reports/bc_target_matrix_REPORT.md)

## 1. A/B：参数变化组

> [!info] A · Gradient magnitude
> $$
> A(v)=\lVert g_v\rVert
> $$
> **问题：** 候选点自身的训练梯度有多大？
>
> **角色：** Hessian-free 排序信号；在当前矩阵中是 B 的强 proxy。

> [!info] B · Parameter displacement
> $$
> B(v)=\lVert H^{-1}g_v\rVert
> $$
> **问题：** 删除候选点后，参数预计移动多远？
>
> **角色：** target-free parameter-change reference。

A 与 B 的定义不同，但当前三数据集 × 三 seed 上：

> [!success] 已有证据
> A vs B reference 的全排序 Spearman = **0.962**。
>
> 因此可以说：**A 是当前设置下 B 排序的强 Hessian-free proxy。**
> 不能说：A 与 B 数学等价。

这与 self-TracIn 用梯度信息代理 influence 排序的思路一致。

## 2. C：eval-conditioned IF

C 使用目标集合 $E$ 的梯度，但不包含删除后图梯度 `grad2`。

> [!example] C-point · Candidate-only IF
> **Reference**
> $$
> \langle g_v,H^{-1}g_E\rangle
> $$
> **Hessian-free proxy**
> $$
> \langle g_v,g_E\rangle
> $$

> [!example] C-simple · No-grad2 IF
> **Reference**
> $$
> \langle \mathrm{grad1}_v,H^{-1}g_E\rangle
> $$
> **Hessian-free proxy**
> $$
> \langle \mathrm{grad1}_v,g_E\rangle
> $$

所以 $\langle g_v,H^{-1}g_E\rangle$ 是 point IF，不是 GIF。

## 3. D：graph-aware GIF

D 使用完整 graph-deletion source：

$$
q_v=\mathrm{grad1}_v-\mathrm{grad2}_v.
$$

> [!important] D-full · Graph-aware GIF
> **Reference**
> $$
> \langle q_v,H^{-1}g_E\rangle
> $$
> **Hessian-free proxy**
> $$
> \langle q_v,g_E\rangle
> $$
> 后者就是 `p_graph`。

> [!note] D-trajectory · Checkpoint ablation
> 这里的 **trajectory 不是动态图**，而是模型训练过程中保存的一组参数快照（checkpoint）。本轮模型训练到 200 epochs，并在第 `1 / 10 / 25 / 50 / 100 / 200` epoch 保存 checkpoint。
>
> 对每个候选节点 $v$，每个 checkpoint $c$ 都单独计算一次 graph-aware 分数：
> $$
> s_c(v)=\langle q_v(\theta_c),g_E(\theta_c)\rangle,
> \qquad q_v=\mathrm{grad1}_v-\mathrm{grad2}_v.
> $$
> 然后按该 checkpoint 前一次 optimizer update 的学习率 $w_c$ 加权求和：
> $$
> \mathrm{score}(v)=\sum_c w_c s_c(v).
> $$
>
> | 方法 | 使用的训练时刻 | 含义 |
> |---|---|---|
> | `p_graph` | 只用第 200 epoch | single-final、Hessian-free 的 graph-aware proxy |
> | `tracin_cp_graph_3` | 第 1、50、200 epoch | 3-checkpoint trajectory ablation |
> | `tracin_cp_graph_6` | 第 1、10、25、50、100、200 epoch | 6-checkpoint trajectory ablation |
> | `gt_full` | 第 200 epoch | 带 $H^{-1}$ 的完整/reference GIF |
>
> 因此 `graph_3` 与 `graph_6` 使用的是同一个 graph-deletion source 和同一种加权求和公式；它们真正改变的是 **checkpoint 数量与时间采样密度**。`p_graph` 就是只取最终 200 epoch 的同源对照，但不宜称作 “naive GIF”：它去掉了 $H^{-1}$，准确名称应为 **single-final Hessian-free GIF proxy**。`gt_full` 才是这里的 final/full GIF reference。增加 checkpoint 会把问题从“最终模型上的影响”改成“训练轨迹上的累计影响”，所以不能预设 checkpoint 越多就越接近 `gt_full`。

是否包含 `grad2` 是 C-IF 与 D-GIF 的分界：

> [!warning] C/D 分界证据
> `gt_simple`（C）vs `gt_full`（D）的 Spearman = **0.040**。
>
> 因此 `grad2` 不是小修正；D 不能继续放在 “C-GIF” 的伞下。

## 4. 方法近似与 IHVP 实现不要混称

### 4.1 A 近似 B 的排序

- **比较：** A vs B reference
- **Spearman：** `0.962`
- **名称：** B-ranking Hessian-free proxy
- **含义：** A 很好地复现 B 的排序，但不等于 B。

### 4.2 固定 source 后去掉 Hessian

- **C-point：** `p_point` vs `r_point`，Spearman `0.969`
- **C-simple：** `p_simple` vs `gt_simple`，Spearman `0.958`
- **D-full：** `p_graph` vs `gt_full`，Spearman `0.984`

这三个数字只能在各自相同 source 内解释，不能跨 C/D 混用。

## 5. IHVP 实现边界

正文统一写作：**reference 中的 $H^{-1}g$ 通过迭代 IHVP 求解。** LiSSA、HVP、shared probes、迭代次数和 probe 数量只在实验实现与复现配置中记录，不构成新的 selector、方法分组或论文贡献。

## 6. 组内与组间测试

### 6.1 组内：reference–proxy fidelity

- **A/B：** A vs B reference → `0.962`
- **C-point：** `p_point` vs `r_point` → `0.969`
- **C-simple：** `p_simple` vs `gt_simple` → `0.958`
- **D-full：** `p_graph` vs `gt_full` → `0.984`
- **D-trajectory：** graph CP-3 / CP-6 vs `gt_full` → `0.498 / 0.529`

组内测试回答：同一目标或同一 source 的 scalable 方法有没有复现 reference。

### 6.2 组间：机制是否选中相同节点

- **A/B vs D：** B reference vs D-full → `0.023`
- **C-point vs D：** `r_point` vs `gt_full` → `0.112`
- **C-simple vs D：** `gt_simple` vs `gt_full` → `0.040`

组间测试回答：不同目标是否实际退化成相同排序。低相关不表示某个实现失败。

> [!todo] 尚未补齐
> 完整 A/B vs C 交叉矩阵仍需汇总；现有结果已经足以确认 C 与 D 的分界。

## 7. Legacy 与 topology 的位置

- **deployed cross-TracIn：** legacy negative control。它使用
  $\langle g_v,-\sum_{j\in T}g_j\rangle$，方向是 training residual。
- **degree / PageRank / IM：** topology anchors，用于检查 influence selector 是否退化为结构中心性或覆盖信号。
- **Hybrid：** 必须按其 influence source 标明为 legacy、C-IF 或 D-GIF，不能只写一个笼统 Hybrid。

这些对象都不属于 D。

## 8. 证据边界

- 本地矩阵覆盖 Cora、CiteSeer、PubMed × seeds 42/212/2024 × k=3/7/14；
- 正式 $E$ 使用 `val_mask`，test labels 只在 selection Artifact 落盘后报告 utility；
- 迭代 IHVP reference 是 operational reference，不是数学 exact truth；
- set-deletion 验证的是 selector 效果，不是某个 approximate GU 方法的 end-to-end gap；
- production proper-TracIn、Hybrid gate 与 GU canary 仍需独立验收。

## 9. 固定写法

> [!success] 可以写
> - A strongly proxies B ranking in the accepted setting.
> - Inverse-Hessian terms are computed through iterative IHVP solves.
> - C is IF; D is graph-aware GIF with the `grad1-grad2` source.
> - Selection fidelity and finite-set deletion damage are separate axes.

> [!danger] 不要写
> - A and B are equivalent.
> - Solver variants are separate selector families.
> - “C-GIF”作为正式组名。
> - 更像 GIF 就一定造成更大 damage。
