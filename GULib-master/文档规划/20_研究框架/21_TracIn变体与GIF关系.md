---
title: TracIn、IF 与 GIF 的目标、source 和时间边界
created: 2026-07-10
updated: 2026-07-20
type: framework-note
status: current-evidence-aligned
tags: [tracin, gif, influence, concordance, human-readable]
---

# TracIn、IF 与 GIF 的目标、source 和时间边界

这页只解决一个问题：

> 两个方法都叫“influence”时，它们究竟是在影响什么、怎样表示删节点、看最终模型还是看整条训练轨迹？

当前实验总入口是 [[10_实验矩阵/12_近似策略重合度实验]]。完整数据见 [B/C target matrix](../../reports/bc_target_matrix_REPORT.md)，正式 selection 链路见 [proper-tracin-v1 gate](../../docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md)。

---

## 0. 先记住三句话

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
