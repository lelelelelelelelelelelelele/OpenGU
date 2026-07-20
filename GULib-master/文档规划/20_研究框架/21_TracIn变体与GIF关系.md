---
title: TracIn、IF 与 GIF 的目标、source 和时间边界
created: 2026-07-10
updated: 2026-07-21
type: framework-note
status: current-evidence-aligned
tags: [tracin, gif, influence, concordance, human-readable]
---

# TracIn、IF 与 GIF 的目标、source 和时间边界

这页只解决一个问题：

> 两个方法都叫“influence”时，它们究竟是在影响什么、怎样表示删节点、看最终模型还是看整条训练轨迹？

当前实验总入口是 [[10_实验矩阵/12_近似策略重合度实验]]。完整数据见 [B/C target matrix](../../reports/bc_target_matrix_REPORT.md)，正式 selection 链路见 [proper-tracin-v1 gate](../../docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md)。

---

## 0. SUP 实验的 17 个方法与 17 个正式 score 输出

本轮 SUP 的正式口径统一为 **17 个 selection methods、17 个正式 score/ranking 输出**。B 只计 `b_param_hutch`；`b_param_lissa` 是内部数值验证 Artifact，不计入方法数或正式输出数。为避免“正文讲了方法族，但读者找不到某个实验列”的问题，先给出完整映射。

对 C/D 统一定义三个算子。令最终 checkpoint 为 $\theta_{200}$，并令

$$
\begin{aligned}
R(q_v) &= \langle q_v(\theta_{200}),H^{-1}g_E(\theta_{200})\rangle,\\
P(q_v) &= \langle q_v(\theta_{200}),g_E(\theta_{200})\rangle,\\
CP_{\mathcal C}(q_v) &= \sum_{c\in\mathcal C}w_c
\langle q_v(\theta_c),g_E(\theta_c)\rangle.
\end{aligned}
$$

其中 $R$ 是 final-point IHVP reference，$P$ 是同 source 的 single-final Hessian-free proxy，$CP$ 是按 checkpoint 学习率 $w_c$ 加权的 trajectory score。两组 checkpoint 为：

$$
\mathcal C_3=\{1,50,200\},\qquad
\mathcal C_6=\{1,10,25,50,100,200\}.
$$

### 0.1 复杂度符号与排期估算

这里衡量的是 **selection 阶段**，不是后续 GU 的成本。$G_p$、$G_g$ 不是标准算法名，而是为了描述当前实现实际做了多少次 forward/backward 而定义的单位成本。

| 符号 | 含义 | 当前实现中实际发生的操作 |
|---|---|---|
| $n$ | candidate pool 大小 | 有多少个候选训练节点需要分别打分 |
| $m$ | 图的边数 | `degree` 只需扫描边并累计度数 |
| $d$ | 参数向量维数 | 梯度、probe 和 IHVP 向量的长度 |
| $G_p$ | 一个候选的 point-gradient 单位成本 | 每个 checkpoint 先共享一次整图 forward，再从保留的计算图中对候选节点 $v$ 的单点 loss 做一次 backward；$nG_p$ 表示对 $n$ 个候选分别取梯度 |
| $G_g$ | 一个候选的 graph-deletion source 单位成本 | 找到 $v$ 的 affected nodes，计算原图 `grad1`；移除 $v$ 的 incident edges，构造 $G_{-v}$，再做删后图 forward/backward 得到 `grad2`；因此通常 $G_g\gg G_p$ |
| $I\cdot H$ | 一次迭代 IHVP solve | $I$ 次 Hessian-vector product；C/D reference 的 $H^{-1}g_E$ 对所有候选共享，所以写成 $+IH$，不是 $+nIH$ |
| $M$ | Hutchinson probe 数 | 正式 SUP 的 B-Hutch 使用 $M=32$ 个 shared Rademacher probes，因此需要 $MIH$，随后做约 $nMd$ 的投影 |
| $C$ | checkpoint 数 | trajectory 方法把候选梯度或 graph-source 计算重复到 $C=3$ 或 $C=6$ 个训练时刻 |

因此，$O(nG_p)$ 不是“$n$ 乘一个没定义的神秘常数”，而是“共享一次整图 forward 后，对 $n$ 个候选分别 backward”的简写。$O(nG_g)$ 则表示 $n$ 次候选级删图干预，其中每个候选都要额外构造删后图并运行 forward/backward。checkpoint 方法前面的 3 或 6 表示整套计算在不同训练参数快照上重复。

C-simple 数学上只需要 `grad1`，应介于 $G_p$ 与完整 $G_g$ 之间；但当前 ScoreBundle producer 把 C-simple 与 D-full 放在同一个候选循环中共同计算，连同 `grad2` 一起产出，所以表中按当前共享实现统一记作 $G_g$。这些表达式是排期用的 operation-count model，不是脱离模型结构的精确 wall-clock 公式。

下面的时间全部是 **EST（排期估算）**，不是新的正式 benchmark。小图栏按当前 Planetoid candidate pool（约 60–140 个训练候选）已有 producer 计时取整；大图栏以 ogbn-arxiv（约 90,941 个训练候选、116 万条边）和历史 TracIn cold selection 约 5,110 秒作为 $nG_p$ 的量级锚点，再按当前未向量化的候选循环外推。该历史 Artifact 只记录 `cuda: 0`，**没有记录 GPU 型号**，所以大图栏不能直接称为 4090、A100 或 H100 实测。

| 主导成本项 | 对应方法 | 小图 EST | ogbn-arxiv EST（历史锚点） | 排期判断 |
|---|---|---:|---:|---|
| $O(n)$ / $O(m+n)$ | `random`、`degree` | $<0.1$ s | $<10$ s | 可忽略 |
| $O(nG_p)$ | A、C-point final、`legacy` | 1–2 s | 1–2 h | 大图已明显昂贵 |
| $O(nG_p+IH)$ | C-point reference | 1–3 s | 1–2 h，外加约 1–5 min IHVP | $IH$ 是共享附加项，不改变主量级 |
| $O(3nG_p)$ / $O(6nG_p)$ | C-point trajectory | 2–6 s / 4–12 s | 3–6 h / 6–12 h | checkpoint 数近似线性放大 |
| $O(nG_p+MIH+nMd)$ | B-Hutch SUP diagnostic | 7–25 s | 2–6 h | 32 probes × 20 HVP，不能当作一次 $IH$ |
| $O(nG_g)$ / $O(nG_g+IH)$ | C-simple、D-final/reference | 2–6 s | 2–10 d | 候选级删图循环是主瓶颈 |
| $O(3nG_g)$ / $O(6nG_g)$ | C-simple、D trajectory | 7–18 s / 15–35 s | 1–4 wk / 2–8 wk | 当前实现不适合全候选大图扫描 |

这里估的是 **cold selection producer**。一旦 score/ranking Artifact 已缓存，读取 top-$k$ 通常是秒级或亚秒级，不能拿 warm-hit 时间代表算法计算成本。大图上的天/周级数字不是精确承诺，而是“当前逐候选全图 backward / 删图实现不可直接扩展”的工程警示。

| 方法学角色（正文名称） | 代码 / Artifact ID | 公式 / 精确定义 | selection 成本 | GU 建议 |
|---|---|---|---|---|
| control | `random` | $u_v\sim U(0,1)$；固定 seed 后按 $u_v$ 排序 | `C0` · $O(n)$ | **核心**：budget-matched baseline |
| control | `degree` | $\deg(v)$ | `C1` · $O(m+n)$ | **可选**：结构 anchor；优先复用既有 GU 证据 |
| A | `a_grad_norm` | $\lVert g_v\rVert$ | `C2` · $O(nG_p)$ | 否：B 的便宜 SUP 排序 proxy |
| B parameter-change diagnostic | `b_param_hutch` | $\lVert H^{-1}g_v\rVert$ | `C4` · $O(nG_p+MIH+nMd)$ | 否：完善 SUP 与实现 sanity check |
| C-point reference | `r_point` | $R(g_v)$ | `C3` · $O(nG_p+IH)$ | **可选**：C/D 机制对照 |
| C-point final proxy | `p_point` | $P(g_v)$ | `C2` · $O(nG_p)$ | 否：与 reference 组内比较 |
| C-point trajectory | `tracin_cp_point_3` | $CP_{\mathcal C_3}(g_v)$ | `C3` · $O(3nG_p)$ | 否：checkpoint ablation |
| C-point trajectory | `tracin_cp_point_6` | $CP_{\mathcal C_6}(g_v)$ | `C4` · $O(6nG_p)$ | **可选**：若验证高 damage 能否传递到 GU |
| C-simple reference | `gt_simple` | $R(\mathrm{grad1}_v)$ | `C4` · $O(nG_g+IH)$ | 否：C/D source 边界诊断 |
| C-simple final proxy | `p_simple` | $P(\mathrm{grad1}_v)$ | `C4` · $O(nG_g)$ | 否：与 reference 组内比较 |
| C-simple trajectory | `tracin_cp_simple_3` | $CP_{\mathcal C_3}(\mathrm{grad1}_v)$ | `C5` · $O(3nG_g)$ | 否：checkpoint ablation |
| C-simple trajectory | `tracin_cp_simple_6` | $CP_{\mathcal C_6}(\mathrm{grad1}_v)$ | `C5` · $O(6nG_g)$ | 否：checkpoint ablation |
| D-GIF reference | `gt_full` | $R(\mathrm{grad1}_v-\mathrm{grad2}_v)$ | `C4` · $O(nG_g+IH)$ | **核心**：full GIF reference |
| D-GIF final proxy | `p_graph` | $P(\mathrm{grad1}_v-\mathrm{grad2}_v)$ | `C4` · $O(nG_g)$ | **核心**：scalable D proxy |
| D-GIF trajectory | `tracin_cp_graph_3` | $CP_{\mathcal C_3}(\mathrm{grad1}_v-\mathrm{grad2}_v)$ | `C5` · $O(3nG_g)$ | 否：3/6 ablation 中的低预算版本 |
| D-GIF trajectory | `tracin_cp_graph_6` | $CP_{\mathcal C_6}(\mathrm{grad1}_v-\mathrm{grad2}_v)$ | `C5` · $O(6nG_g)$ | **核心**：trajectory representative |
| negative control | `legacy` | $\langle g_v,-\sum_{j\in T}g_j\rangle$ | `C2` · $O(nG_p)$ | 否：negative control |

> [!note] B 是一个方法，不是两个方法族
> `b_param_hutch` 与 `b_param_lissa` 都估计同一个 $B(v)=\lVert H^{-1}g_v\rVert$。前者用 32 个 shared Rademacher probes，是正式 SUP 输出；后者逐候选运行 LiSSA，只作为数值验证 Artifact。二者全排序 Spearman 为 **0.968**，因此正式 SUP 只保留 `b_param_hutch`；两者都不作为真实 IF/GU 主线。

这张表就是本轮 SUP 的完整正式集合：**17 个方法、17 个 score/ranking 输出**。PageRank、IM 与 Hybrid 在本文用于解释更大的研究坐标，但**不属于这轮 A/B–C–D SUP 矩阵**。

> [!important] Selection 与 GU 的执行边界
> 17 项都生成完整节点分数、排序与各预算的 top-$k$ Selection Artifact；这一步回答“不同定义选中了谁”。本地 set-deletion downstream 可以验证选中集合是否真的造成损伤，但它不是某个 approximate GU 方法的 end-to-end 实验。
>
> 第一批 GU shortlist 为 `random`、`gt_full`、`p_graph`、`tracin_cp_graph_6`。A/B 只服务于 SUP 的目标层级与实现一致性检查，不进入 GU；`degree`、`r_point` 和 `tracin_cp_point_6` 是第二批可选项。

> [!note] 实际总运行时间
> 上表是方法独立运行时的渐近与相对成本。正式 ScoreBundle producer 会共享候选梯度、目标梯度、IHVP 和 graph-source 中间量，因此一次性产出 17 个正式 score 的实际成本低于逐项成本之和；LiSSA validation 是额外审计开销，不计入正式矩阵。selection 排名一旦缓存，后续 GU 只读取 top-$k$ 节点。

### 0.2 先记住三句话

1. `<g_v,g_E>` 只是 **single-final eval proxy**，不是标准多 checkpoint TracInCP。
2. `<g_v,H^-1 g_E>` 是 **point IF**；图删除的 full GIF 还要把候选点对邻居和边的影响放进 source。
3. “最像 GIF”和“实际删掉 top-k 后伤害最大”是两个不同问题。

---

## 1. 用一个通用式看懂大部分方法

对候选删除节点 `v`，记它的训练 loss gradient 为 `g_v`。很多 target-aware selector 都可以写成：

```text
score(v) = <source_v, target_direction>
```

这里有三个独立选择：

- `target_direction`：想伤害谁；
- `source_v`：怎样表示“删掉节点 v”；
- checkpoint policy：只看最终模型，还是沿训练轨迹累计。

方法名容易漂移，这三个选择不会。

---

## 2. `T` 和 `E`：从哪里挑，想伤害谁

| 符号 | 含义 | 作用 |
|---|---|---|
| `T` | training / candidate pool | 从这里挑要 unlearn 的节点 |
| `E` | evaluation / query set | 定义“我们关心哪个 loss 变坏” |

`E` 不是删除候选池。目标是：

```text
从 T 里挑 v，预测删掉 v 后 E 上的 loss 如何变化。
```

机制诊断可以用 test split 当 `E`；正式攻击选点不能用真实 test labels，否则是 label leakage。正式路径使用 validation/query set 或明确记录 teacher 的 pseudo-label probe set。

---

## 3. 目标轴：A / B / C 不是一回事

| 层 | 分数 | 回答的问题 | 需要 `E` |
|---|---|---|---|
| A · gradient magnitude | `||g_v||` | 这个点自己的训练梯度大不大 | 否 |
| B · parameter change | `||H^-1 g_v||` | 删掉它后参数预计移动多远 | 否 |
| C · target impact | `<source_v,H^-1 g_E>` | 这次变化是否会伤害 `E` | 是 |

当前 3 datasets × 3 seeds 的实验中：

- A vs B-LiSSA Spearman = `0.962`；
- B-Hutchinson vs B-LiSSA = `0.968`；
- B-LiSSA vs C-full GIF = `0.023`。

读法是：A/B 在当前矩阵里经验上很像，但不是定义等价；B/C 则明确在问不同的问题。

### 3.1 B-Hutchinson 到底在做什么

它不是一个新 influence 目标，而是 B 的快速算法：

```text
参考 B-LiSSA：对很多候选点分别估计 H^-1 g_v

B-Hutchinson：
  先对少量共享随机 probe 求 H^-1 z_r
  再用这些共享结果估计每个 ||H^-1 g_v||
```

所以 Hutchinson 是“多个候选点共用一批曲率探针”，不是把 HVP 删掉。

---

## 4. source 轴：point IF 不是 full GIF

在 GNN 中，删掉一个节点不仅删掉它自己的 loss，还会删边并改变邻居收到的 message。

| 名称 | source | 看到的删除效应 |
|---|---|---|
| point | `g_v` | 只看候选点自己的 loss gradient |
| simple | `a_v=grad1_v` | 原图上加入受影响邻域 |
| full graph | `q_v=grad1_v-grad2_v` | 显式加入删边后邻居梯度的变化 |

因此：

```text
point IF      = <g_v, H^-1 g_E>
simple IF     = <a_v, H^-1 g_E>
full GIF ref  = <q_v, H^-1 g_E>
```

实验上：

- point IF vs full GIF Spearman = `0.112`；
- simple IF vs full GIF = `0.040`；
- 固定 full source 后，`p_graph=<q_v,g_E>` vs `gt_full` = `0.984`。

结论不是“IF 无效”，而是：

> 要近似 full GIF，先要用同一个 graph-deletion source；不能靠 Hessian 或更多 checkpoint 弥补 source 定义的错位。

---

## 5. 时间轴：single-final 不是 TracInCP

### 5.1 single-final eval proxy

```text
score_final(v) = <source_v(theta_final), g_E(theta_final)>
```

它只问：在最终模型上，候选 source 与目标 loss 梯度是否对齐。历史文档把 point 版 `<g_v,g_E>` 叫作 `proper TracIn`；这个命名已经废止。

### 5.2 TracInCP

```text
score_TracInCP(v) = sum_c w_c <source_v(theta_c), g_E(theta_c)>
```

它沿多个 checkpoint 累计影响，必须说明：

- checkpoint 是哪些；
- 每个 checkpoint 用什么权重；
- target `E`、loss、符号和排序方向；
- point / simple / full graph 哪个 source。

当前 graph source 的 3/6-checkpoint 版本对 final `gt_full` 的 Spearman 只有 `0.498/0.529`，低于 single-final `p_graph=0.984`。这不表示 TracInCP 没有用；它表示 trajectory score 和 final-state GIF reference 本来就不是同一个时间对象。

### 5.3 self-influence 也要分 final 和 trajectory

```text
final grad norm:       ||g_v(theta_final)||^2
TracInCP self:         sum_c w_c ||g_v(theta_c)||^2
```

两者都不需要 `E`，但不能因为都叫 self-influence 就混为同一实现。

---

## 6. Legacy deployed cross-gradient 到底是什么

旧 `attack/attack_strategies/tracin_strategy.py` 计算：

```text
score_legacy(v) = <g_v, -sum_{j in T} g_j>
```

在 L2 regularization 下，训练收敛点近似满足：

```text
(1/|T|) sum_j g_j + lambda * theta ~= 0
```

所以 `-sum_j g_j` 更像参数/正则残差方向，而不是 `g_E`。它不是随机噪声，而是在稳定地按另一个目标排序。

历史三数据集诊断中，它与 eval-target IF diagnostic 的 top-k overlap 只有 `0.098–0.142`。因此旧结果只能标作 `deployed-cross-gradient-legacy`，不能当作 TracInCP 或 full GIF 证据。

---

## 7. 你刚才问的工程词，用人话怎么理解

### 7.1 “Adam 不能直接冒充论文 SGD TracIn”

TracIn 论文里的直觉是：一步参数更新大致等于“学习率 × 梯度”。Adam 还会对每个参数做不同的动量和缩放。

所以我们现在的 Adam 路径可以当作一个有用的轨迹启发式，但不能写成严格重放了论文中的 SGD/GD 更新。当前正式名称是 `adam_lr_weighted_gradient_heuristic`。

### 7.2 “node loss 不等于 graph deletion”

普通表格数据里，删一条训练样本主要少一项 loss。GNN 里删节点还会删边，邻居的 message 和表示也会变。

因此 point `g_v` 只是“这个节点自己”；full source `grad1-grad2` 才进一步表示“它从图上被删掉后，邻居也变了”。

### 7.3 Recipe / Producer / Artifact 是什么

| 工程词 | 人话 | 为什么要有 |
|---|---|---|
| Recipe | 这次 score 到底怎么算的完整配方 | 配方变了就不能误命中旧结果 |
| ProducerVersion | 哪一版代码实现了这个配方 | 同名算法改了实现时仍然可追溯 |
| Score Artifact | 实际保存的候选 ID、score 和排名文件 | 下游选点和实验知道自己使用了哪份 score |

可以把它们理解成：

```text
Recipe = 菜谱
ProducerVersion = 厨师和做法版本
Artifact = 最后端上来的那盘菜
```

名字都叫 TracIn 不够；菜谱、做法版本或 target `E` 不同，就必须是不同结果身份。

### 7.4 CPU / GPU numerics 边界

同一公式在不同 Torch/CUDA/CPU 上可能差最后几位小数。我们不把两份不同的浮点内容强行冒充同一 Artifact；但会另外检查排名相关、top-k 和并列情况。

这就是为什么 cross-machine gate 同时报告：绝对数值差、Spearman/Kendall、ordered top-k 是否一致。

### 7.5 “Hybrid 必须绑定父 Artifact”

Hybrid 是把 TracIn 和 IM 两份上游 score 融合。因此它必须记录：

```text
我融合的是哪一份 TracIn Score Artifact
我融合的是哪一份 IM Artifact
alpha / normalization / tie-break 是什么
```

否则一个 Hybrid 结果出问题时，我们无法判断是 TracIn、IM 还是融合参数造成的。

### 7.6 “Legacy cache 冻结”

它不是说删掉旧 cache。正确操作是：

- 旧 cache 保留，只读，用来追溯旧结果；
- 新公式用新 Recipe / Artifact 身份；
- 新路径 miss 时不能悄悄 fallback 到旧 TracIn；
- 不通过“清 cache”来偷偷切换算法定义。

---

## 8. 当前证据的最短正确读法

| 观察 | 可以说 | 不能说 |
|---|---|---|
| A/B Spearman `0.962` | 当前矩阵上两者排序很像 | A 在定义上就等于 B |
| B-Hutch vs B-LiSSA `0.968` | shared-probe 可有效近似 B | Hutchinson 是一个新 influence 目标 |
| `p_graph` vs `gt_full` `0.984` | 固定 full source 后可有效去掉 Hessian | `p_graph` 数学上等于 exact GIF |
| point/simple vs full GIF 低相关 | source 不能省略 | point/simple IF 没有自己的用途 |
| checkpoint graph 对 final GIF 忠实度低 | trajectory 不等于 final-state GIF | TracInCP 无效 |
| point checkpoint damage 更大 | fidelity 和 damage 必须分开验收 | GIF reference 没意义 |

---

## 9. 旧文档和旧结果的处理

| 旧名称 / 结果 | 新处理 |
|---|---|
| `proper TracIn = <g_v,g_E>` | 改称 `single-final point eval proxy` |
| `GIF = <g_v,H^-1g_E>` | 改称 `point IF reference`；full GIF 使用 `q_v=grad1-grad2` |
| deployed `TracInStrategy` | `deployed-cross-gradient-legacy` |
| 旧 TracIn / Hybrid attack cells | 保留为 produced history，不当 proper TracIn evidence |
| 2026-06 concordance `0.65–0.74` | 保留为 single-final point diagnostic 的历史证据 |

历史 finding 已按这个口径降级：[FINDING_tracin_misspecification.md](../../self/related_work/concordance/FINDING_tracin_misspecification.md)。

---

## 10. 自测问题

1. `T` 和 `E` 分别是什么？为什么 `E` 不是删除候选池？
2. A、B、C 分别影响谁？
3. point IF 和 full GIF 的 source 差在哪里？
4. single-final proxy 和 TracInCP 的时间差在哪里？
5. 为什么 Adam LR-weighted score 只能标作 heuristic？
6. Recipe、ProducerVersion、Artifact 各自防止什么混用？
7. 为什么 Hybrid 必须记录它的 TracIn / IM 父 Artifact？
8. 为什么旧 cache 应保留只读，而不是删掉？

---

## 11. 证据入口

- [B/C target matrix 报告](../../reports/bc_target_matrix_REPORT.md)
- [C-target 实验计划与结果](../10_实验矩阵/21_C目标TracIn与GIF近似有效性实验计划.md)
- [TracIn V2 prototype gates](../../docs/tracin_v2_gates_ACCEPTANCE_REPORT.md)
- [proper-tracin-v1 selection gate](../../docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md)
- [历史 concordance finding](../../self/related_work/concordance/FINDING_tracin_misspecification.md)
- [历史 selector diagnostic](../../self/related_work/concordance/if_selector_diagnostic.py)
