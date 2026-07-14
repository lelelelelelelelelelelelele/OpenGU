---
title: TracIn 变体与 GIF 的关系
created: 2026-07-10
type: framework-note
tags: [tracin, gif, influence, concordance, human-readable]
---

# TracIn 变体与 GIF 的关系

这页只解决一个问题：

> 我们说 TracIn、proper TracIn、GIF、self-influence、parameter-change IF 时，到底在算什么？它们为什么会选出不同节点？

这里不复制所有实验产物。权威数字和脚本仍在 repo：

- [FINDING_tracin_misspecification.md](../../self/related_work/concordance/FINDING_tracin_misspecification.md)
- [HANDOFF.md](../../self/related_work/concordance/HANDOFF.md)
- [concordance_model_based.py](../../self/related_work/concordance/concordance_model_based.py)
- [if_selector_diagnostic.py](../../self/related_work/concordance/if_selector_diagnostic.py)
- [ifdiag_cora_GCN_r0.05_seed2024.json](../../self/related_work/concordance/data/ifdiag_cora_GCN_r0.05_seed2024.json)
- [cora_GCN_r0.05_seed2024.json（topology sidecar）](../../self/related_work/concordance/data/cora_GCN_r0.05_seed2024.json)
- [report.html](../../self/related_work/concordance/report.html)

### 证据与复现契约

本页引用的 `ifdiag_cora_GCN_r0.05_seed2024.json` 是 2026-07-10 生成的 32-probe 历史 artifact（SHA-256：`36f9b68cf083495a53d2d32e5fbd581afeb6bfa71618475a07f658da8998ccf2`）。其中 topology 对照来自 `cora_GCN_r0.05_seed2024.json`（SHA-256：`1ece38c13dd1929b8b5479705c502474fd8bf9f8ae37ded6d9b05a29629dedc4`）。它们早于当前 diagnostic schema v2，因此没有新版 `recipe_hash`；保留原内容是为了让本文数字仍有稳定证据，不把旧文件伪装成新版 artifact。

当前脚本的 canonical reproduction command 是：

```powershell
E:/conda_package/envs/gnn/python.exe self/related_work/concordance/if_selector_diagnostic.py --dataset_name cora --base_model GCN --unlearn_ratio 0.05 --seed 2024 --num_epochs 100 --batch_size 64 --lissa_iter 100 --lissa_scale 25.0 --lissa_damp 0.01 --hutch_probes 32 --hutch_seed 1729
```

新版结果声明 diagnostic schema、algorithm version、完整 recipe/config、实现源码 fingerprint 和稳定 recipe hash，默认写入带 recipe hash 的新文件名。已有目标默认不覆盖；`--overwrite` 也只能覆盖 recipe hash 完全相同的新版结果，不能覆盖不同配置或缺少 recipe hash 的旧 artifact。写入采用同目录临时文件后 `os.replace`。

topology sidecar 的路径和内容 hash 也进入 Recipe；它存在时才导入 degree / PageRank / IM 对照。缺少 sidecar 的 clean run 仍能完成 model-based 五种 score，但 topology 对照为空且 Recipe hash 不同，不会冒充完整复现。

证据边界也要一起记住：该命令只跑 CPU selector diagnostic，不执行 GU；Cora follow-up 是单 dataset、单 backbone、单 seed；`||H^-1 g_v||` 是 LiSSA + 32-probe Hutchinson 估计，不是逐节点精确 inverse-Hessian；`E=test_mask` 只用于机制校准，不能直接变成正式攻击的 test-label query。

---

## 0. 先记住一句话

**TracIn 不是一个自动清楚的名字。它必须说明“候选节点梯度在和哪个方向做内积”。**

统一写法是：

```text
score(v) = <g_v, u>
```

其中：

- `v` 是候选删除节点；
- `g_v = grad loss_v` 是这个候选节点自己的训练损失梯度；
- `u` 是参考方向；
- 不同 TracIn / GIF 的区别，主要就在 `u` 是什么。

所以真正要问的不是“这是不是 TracIn”，而是：

> 这个 selector 用候选节点 `g_v` 去投影哪个目标方向？

---

## 1. T 和 E 先分清

这个问题里最容易混的是 `T` 和 `E`。

| 符号 | 是什么 | 作用 |
|---|---|---|
| `T` | training / candidate pool | 从这里挑要 unlearn 的节点 |
| `E` | evaluation / query set | 定义“我们关心哪个 loss 变坏” |

**E 不是要删除的节点池。**

一个 selector 的目标可以是：

```text
从 T 里挑节点 v，
让删除 v 后，
E 上的 loss 变化最大。
```

诊断实验里可以用 test split 当 `E` 来校准 GIF / TracIn，因为这是机制诊断；真正攻击设定里不能拿真实 test label 来选点，否则是 label leakage。攻击里更合理的是 validation/query set 或 pseudo-labeled probe set。

---

## **2. 先按“影响谁”分三组**

不要先背公式。先问一句：

> 我现在想选“对谁影响大”的训练点？：

| 组 | 代表 score | 需要 `E` 吗 | 需要 `H^-1` 吗 | 它问什么 |
|---|---|---|---|---|
| A. training-objective / model-state | `||g_v||` 或 `||g_v||^2` | 不需要 | 不需要 | 这个点自己的训练 loss 梯度大不大 |
| B. parameter-change IF | `||H^-1 g_v||` | 不需要 | 需要 | 删除这个点会不会让参数移动很大 |
| C. eval / generalization impact IF | `<grad L_E, H^-1 g_v>` | 需要 | 需要 | 删除这个点会不会影响 `E` 上的 loss |

其中 C 也常写成：

```text
<g_v, H^-1 grad L_E>
```

如果 Hessian 近似看成对称矩阵，这两个写法是同一件事：一个是“先把候选点方向曲率修正”，一个是“先把 eval 方向曲率修正”。

所以，不是“只有两组”。概念上是三组：

```text
||g_v||                 -> 训练目标 / 自身梯度 magnitude
||H^-1 g_v||            -> 参数变化 / model-editing impact
<grad L_E, H^-1 g_v>    -> eval 或泛化影响
```

只是 2026-07-10 的 Cora/GCN first-pass 里，A 和 B 的 top-k 很像，所以看结果会像“两团”。这不代表它们概念上是一组。

旧 deployed cross-TracIn 不是第四组干净目标。它是旧代码实际用过的 legacy selector，应该单独当反例看。

---

## 3. 五个分数在问什么

### 3.1 deployed cross-TracIn：旧代码实际在算什么

旧代码的分数可以写成：

```text
score_cross(v) = <g_v, - sum_{j in T} g_j>
```

也就是：候选节点 `v` 的梯度，和“所有候选/训练节点梯度之和的负方向”做内积。

它问的是：

> 这个节点的梯度，是否和训练梯度残差方向对齐？

问题在于，训练收敛后 `sum_j g_j` 并不等于我们关心的 `grad L_E`。在 L2 regularization 下，训练梯度和正则项满足近似平衡：

```text
(1 / |T|) sum_{j in T} g_j + lambda * theta ~= 0
```

所以：

```text
- sum_j g_j ~= |T| * lambda * theta
```

这说明 deployed cross-TracIn 大致是在看：

```text
<g_v, parameter / regularization direction>
```

它不是在问“删除这个点会不会让 E 的 loss 变坏”。它更像在问“这个点的梯度是否沿着参数/正则残差方向”。

这就是为什么它和 GIF 重合低：它瞄准的方向本来就不一样。

---

### 3.2 proper TracIn：Hessian-free 的 eval-impact proxy

proper TracIn 的分数是：

```text
score_proper(v) = <g_v, grad L_E>
```

其中：

```text
L_E = sum_{e in E} loss_e
```

它问的是：

> 这个候选节点的训练梯度，是否和 evaluation/query loss 的梯度方向一致？

直觉上，如果 `g_v` 和 `grad L_E` 对齐，说明这个训练点和 E 上的 loss 方向关系更强。删除这个点时，E 上的 loss 可能更受影响。

它叫 Hessian-free，是因为它没有乘 `H^-1`。它只做梯度内积，所以成本和旧 deployed TracIn 基本同阶。

---

### 3.3 GIF / real influence：proper TracIn 加上曲率修正

GIF 的 eval-impact 形式可以写成：

```text
score_GIF(v) = <g_v, H^-1 grad L_E>
```

它问的是：

> 考虑训练 loss 曲率以后，这个候选节点对 E 的 loss 影响有多大？

和 proper TracIn 比，它们关心的是同一个目标 `E`，但 GIF 多了一个 `H^-1`：

```text
proper TracIn:  u = grad L_E
GIF:            u = H^-1 grad L_E
```

所以可以这样理解：

> proper TracIn 是不看地形坡度修正的方向；GIF 是经过 Hessian 曲率预条件化后的方向。

如果 proper TracIn 和 GIF 高重合，说明 Hessian-free proxy 对这个 eval-impact 目标是有用的。它不是完全等价，因为 `H^-1` 会改变方向，但它们至少在问同一个问题。

---

### 3.4 self-influence / grad-norm：training-objective magnitude

self-influence 常写成：

```text
score_self(v) = <g_v, g_v> = ||g_v||^2
```

它问的是：

> 这个点自己的梯度范数大不大？

它没有一个固定的 `u`。每个候选节点都拿自己和自己比。

所以 self-influence 不能简单当成 proper TracIn 或 GIF 的替代品。它更接近“这个点自己的训练 loss 梯度是不是很大”，而不是“它对某个 held-out/query loss 方向影响大不大”。

它也不等于 parameter-change IF。parameter-change IF 还要看 `H^-1` 曲率修正。

---

### 3.5 parameter-change IF：model editing 意义上的“参数影响大”

如果你的本意是：

> 选出删除后会让模型参数 / 模型状态改变很大的点。

那更贴近 IF / model editing 的分数是：

```text
Delta theta_v ~= - H^-1 g_v
score_param(v) = ||H^-1 g_v||
```

它问的是：

> 如果只删除这个训练点，近似更新方向会不会很大？

这个目标不需要 `E`，所以它不是 test-set influence。它也不是 proper TracIn / GIF 那条 eval-impact 线。它是另一组：parameter-change IF。

实际计算上，逐候选点精确求 `H^-1 g_v` 很贵。这次诊断用 Hutchinson shared probes 估计 `||H^-1 g_v||`，目的是先看 selector 集合会不会和 `||g_v||`、eval-impact IF、degree、IM 混在一起。

---

## 4. 一张表记住边界

| 名称 | 分数 | 参考方向 `u` | 它真正问的问题 | 和 GIF 的关系 |
|---|---|---|---|---|
| deployed cross-TracIn | `<g_v, -sum_T g_j>` | 训练梯度残差 / 正则方向 | 这个点是否沿参数残差方向 | 目标错位，重合低 |
| proper TracIn | `<g_v, grad L_E>` | evaluation/query loss 梯度 | 这个点是否影响 E 的 loss | 和 GIF 同目标，少 `H^-1` |
| GIF | `<g_v, H^-1 grad L_E>` | 曲率修正后的 E 梯度 | 考虑 Hessian 后影响 E 的 loss | 小图 gold/reference |
| self-influence / grad-norm | `<g_v, g_v>` 或 `||g_v||` | 候选点自己的梯度 | 这个点自身训练梯度大不大 | 不是固定 E 目标 |
| parameter-change IF | `||H^-1 g_v||` | 不是投影到固定 `u`，而是删除点的 IF 更新范数 | 删除这个点会不会让参数移动很大 | 不是 eval-impact GIF，但同属 IF/model-editing 线 |

---

## 5. 当前重合度说明了什么

下面第一张三数据集表来自既有 model-based concordance artifacts；各数据集都在各自的 seeded trained base GCN 上比较 selector，`k = 0.05 * |V_train|`，不是新版 Cora follow-up 一次运行的联合输出。

| pair | cora | citeseer | pubmed | 读法 |
|---|---:|---:|---:|---|
| GIF vs proper TracIn | 0.742 | 0.727 | 0.647 | 高重合：proper TracIn 是 reasonable Hessian-free eval-impact proxy |
| GIF vs deployed cross-TracIn | 0.113 | 0.142 | 0.098 | 低重合：旧实现没有对准 eval-impact IF |
| GIF vs self-influence | 0.249 | 0.298 | 0.133 | 中间：梯度范数有信号，但不是同一目标 |
| GIF vs degree | 0.024 | 0.051 | 0.041 | 几乎正交：真实 IF 也不是 degree |
| proper TracIn vs degree | 0.024 | 0.043 | 0.045 | proper TracIn 也不是结构中心性 |

这里最重要的不是背数字，而是理解结论：

1. **proper TracIn 和 GIF 靠得近**，因为它们都关心 `E` 上的 loss sensitivity。
2. **deployed cross-TracIn 和 GIF 离得远**，因为旧实现用的是 training residual / regularization direction。
3. **GIF / proper TracIn 和 degree 都离得远**，说明 influence signal 和 structural-volume signal 不是同一批节点。

这也是为什么“degree 强”这个发现仍然重要：如果 correct influence selector 仍然和 degree 几乎正交，那么 degree 的强不是因为它偷偷近似了 GIF，而是因为 approximate unlearning 里结构 volume 可能是另一条更致命的攻击信号。

2026-07-10 的历史 32-probe artifact 又补了一次 Cora/GCN 三组 score 诊断，用来回答“参数影响大、训练目标影响大、泛化影响大是不是同一批点”：

| pair | Jaccard@k | 读法 |
|---|---:|---|
| `||H^-1 g_v||` vs `||g_v||` | 0.8462 | parameter-change IF 和 grad-norm 在 Cora/GCN 上很接近 |
| `||H^-1 g_v||` vs eval-impact GIF | 0.2343 | 参数扰动大不等于 eval/generalization 影响大 |
| proper TracIn vs eval-impact GIF | 0.7419 | Hessian-free eval-impact proxy 仍然靠谱 |
| deployed cross-TracIn vs eval-impact GIF | 0.1134 | 旧实现仍然没对准 eval-impact |
| `||H^-1 g_v||` vs degree / IM | 0.0385 / 0.0435 | parameter-change IF 也不是 topology selector |

所以这页最终应该这样读：

> 设计上是三组影响目标；实验上 Cora/GCN 里前两组很像，第三组不同。旧 deployed cross-TracIn 不算干净目标，只是 legacy selector。

---

## 6. 为什么旧解释要修正

以前容易说成：

> 训练收敛后 `sum grad ~= 0`，所以 deployed TracIn 是噪声。

这个说法不对。

更准确的是：

```text
sum_j g_j 不是 0；
它大致对应 L2 regularization residual；
所以 deployed cross-TracIn 不是随机噪声，
而是在稳定地按“错误方向”排序。
```

这点很关键。因为如果它只是噪声，那结论是“实现坏了”。但如果它是错误方向，那结论更具体：

> 它在选择和参数/正则残差方向对齐的点，而不是选择影响 held-out/query loss 的点。

这个解释能说明为什么它有一点点信号，但不接近 GIF。

---

## 7. 和论文 claim 的关系

这件事会影响的 claim：

| claim | 当前状态 |
|---|---|
| 旧 TracIn attack outcome 代表 proper IF selector | 不稳，应该 refresh 或改名 |
| Hybrid 结果完全干净 | 不稳，因为 Hybrid 复用了 TracIn 分支 |
| random / degree / pagerank / IM 结果 | 不受这个 TracIn 定义问题影响 |
| degree / structural-volume 是独立强信号 | 仍然有支撑，因为 GIF / proper TracIn 都和 degree 低重合 |
| influence-based selector 一定弱于 degree | 不能现在写死，要等 proper TracIn / Hybrid rerun 后再判断 |
| parameter-change IF 和 eval-impact IF 是同一个 selector | 不能这么说；Cora/GCN 上二者 Jaccard 只有 0.2343 |

一句安全口径：

> 旧 deployed TracIn 不能作为 proper eval-impact IF 的证据；但 concordance 也显示，correct eval-impact IF 与 degree 选择的是不同节点，因此 structural-volume signal 和 influence signal 是两条不同轴。

---

## 8. 明天学习时按这个顺序读

### Step 1：先看 `score(v)=<g_v,u>`

只要记住不同方法的核心区别是 `u`，就不会被名字绕晕。

### Step 2：问每个公式“它影响谁”

- 影响训练目标 / 自身梯度 magnitude？对应 `||g_v||`。
- 影响删除后的参数变化？对应 `||H^-1 g_v||`。
- 影响 held-out/query loss？对应 `<grad L_E, H^-1 g_v>` 或 `<g_v, H^-1 grad L_E>`。
- 影响 training residual / regularization direction？这是旧 deployed cross-TracIn，目标不干净。

如果说不出“影响谁”，公式就还没懂。

### Step 3：再看 Jaccard 表

不要把 Jaccard 当最终目的。它只是回答：

> 两个公式最后选出来的是不是同一批节点？

Jaccard 高，说明两个 selector 的 top-k 集合接近；Jaccard 低，说明它们在 attack 预算下实际删除的是不同对象。

### Step 4：最后回到研究问题

我们真正关心的是：

> Approximate graph unlearning 的脆弱性，到底更像 model influence 问题，还是更像 structural volume / coverage 问题？

TracIn/GIF 这组工作是在把 model influence 这条线清理干净。degree/IM/concordance 是在检查 structural / coverage 这条线是不是独立。

---

## 9. 自测问题

明天读完可以用这几个问题检查自己：

1. `T` 和 `E` 分别是什么？为什么 E 不是 deletion candidate pool？
2. deployed cross-TracIn 的 `u` 是什么？为什么它不是 `grad L_E`？
3. proper TracIn 和 GIF 的唯一核心差别是什么？
4. `||g_v||` 和 `||H^-1 g_v||` 概念上为什么不是同一组？为什么 Cora/GCN 上又会高重合？
5. self-influence 为什么不能简单叫 proper TracIn？
6. GIF vs proper TracIn 高重合说明什么？不能说明什么？
7. GIF / proper TracIn vs degree 低重合，对 structural-volume claim 有什么意义？
8. 为什么旧 TracIn / Hybrid 结果需要 refresh，但 random / degree / pagerank / IM 不需要？

---

## 10. 当前下一步

研究上下一步不是“再堆一个表”，而是把这条链闭合：

```text
定义干净的 selector
  -> 看它和 GIF / degree / IM 的重合度
  -> 用 proper TracIn / Hybrid rerun attack outcome
  -> 连接 overlap-with-degree 与 attack damage
  -> 判断 structural-volume 是否真的比 influence 更能解释脆弱性
```

目前已经比较稳的是：

- proper TracIn 是 eval-impact GIF 的便宜近似；
- deployed cross-TracIn 不是；
- correct influence selector 和 degree 仍然选不同节点；
- 所以不能用旧 TracIn outcome 给 IF 线下最终结论，但可以继续推进“结构 volume 与 influence 是不同轴”的论证。
