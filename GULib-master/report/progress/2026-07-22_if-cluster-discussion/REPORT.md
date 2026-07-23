---
title: "IF 簇方法比较：效果、机制与普遍性边界"
date: 2026-07-22
status: discussion-draft
audience: advisor-discussion
tags: [progress/discussion, experiment/selection, method/influence-function]
---

# IF 簇方法比较：效果、机制与普遍性边界

> [!summary] 本次讨论希望决定什么
> 不是从 17 个 selector 中强行挑一个“冠军”，而是判断：**IF 簇是否真的比旧 IF / degree 更强；不同 IF 公式分别在什么条件下有效；当前证据更适合支撑“方法优越性”还是“条件性与异质性”叙事。**

## 1. 一页结论

### 1.1 最重要的结论

**当前实验不支持“新 IF 簇普遍优于旧 IF、random 或 degree”。**

- 在 3 datasets × 3 seeds 的正式 GNNDelete 矩阵中，D-full 的 reference/proxy 组是 **IF 内部 pooled 平均最强**的一组，但优势主要由 Cora 驱动。
- CiteSeer 上反而是 C-point 更合适；D-full 与 B 都没有形成正收益。
- PubMed 是近似 selector-insensitive 的 null regime：17 个方法均未超过 random。
- degree 仍是最稳定的强基线；当前复杂 IF 没有可靠地超过它。
- `p_graph` 很好地近似 `gt_full`，说明近似公式是可信的；但**公式逼真不等于删除后伤害更大**。
- checkpoint 从 3 增加到 6 没有单调收益，不能把“更多 checkpoint”写成稳定改进。

因此，最准确的概括不是“D 组最强”，而是：

> [!important] 三种响应机制
> **Cora：D/B-aligned；CiteSeer：C-point-aligned；PubMed：null。**
>
> 这个结论目前是描述性的，因为每个数据集只有 3 个 seed；它揭示了普遍性问题，但还不能被写成已经证明的机制定律。

### 1.2 对论文的直接影响

| 可能的论文主张 | 当前证据判断 | 建议 |
|---|---:|---|
| “新 IF 簇整体优于旧 IF” | **不成立** | 删除该强主张 |
| “D-full 是普遍最优 selector” | **不成立** | 改成“在 Cora / pooled IF 内领先” |
| “图删除源比点源更贴近 GU 脆弱性” | **部分支持** | 作为条件性机制假设，不作普遍定律 |
| “cheap proxy 可以逼近 expensive reference” | **成立** | 保留 `p_graph ≈ gt_full` 的 fidelity 贡献 |
| “复杂 IF 稳定超过 degree” | **不成立** | degree 必须保留为强基线 |
| “不同数据集存在 selector regime 异质性” | **有明确描述性证据** | 可作为 audit / diagnostic 主线 |

## 2. 这轮实验到底比较了什么

### 2.1 正式实验身份

| 项目 | 固定设置 |
|---|---|
| 下游任务 | selected-set → GNNDelete 的直接效果评估 |
| Backbone / GU | GCN / GNNDelete |
| 数据集 | Cora、CiteSeer、PubMed |
| 划分 | `planetoid_public_fixed` |
| 删除预算 | 固定 $k=7$ |
| 矩阵 | 17 selectors × 3 datasets × 3 seeds = **153/153 cells** |
| 完整性 | **612/612 artifacts，0 failure** |
| 正式代码 SHA | `1c83bb433fcd31b81c5adbaee550dbaf6b4f03cd` |
| result manifest SHA-256 | `e45aa4b193d53b854c709e3de543517417fa6a9f0d3eb1f013aea9bc3e16d236` |

这轮衡量的是 selector 选出的节点，在**实际 GNNDelete 流程**中造成的结果；不是只看 score 排名相似度，也不是 OpenGU 的 80/20 旧 protocol，更不是 E7 surrogate transfer。

### 2.2 IF 簇的结构

设单点训练梯度为 $g_v$，Hessian 为 $H$，评估目标梯度为 $g_{eval}$；图删除前后的源梯度分别为 $g_{before}$、$g_{after}$。

| 组别 | 代表方法 | 核心信号 | 在本轮中的角色 |
|---|---|---|---|
| Control | `random`, `degree` | 随机 / 结构中心性 | 下限与强基线 |
| A | `a_grad_norm` | $\lVert g_v\rVert$ | target-free 梯度幅值 |
| B | `b_param_hutch` | 近似 $\lVert H^{-1}g_v\rVert$ | 参数移动量代理 |
| C-point | `r_point`, `p_point`, `tracin_cp_point_{3,6}` | eval-conditioned point influence | 不显式使用删除后图 |
| C-simple | `gt_simple`, `p_simple`, `tracin_cp_simple_{3,6}` | `grad1` source | 简化 source ablation |
| D-full | `gt_full`, `p_graph`, `tracin_cp_graph_{3,6}` | $g_{before}-g_{after}$ | 显式 graph-deletion source |
| Legacy | `legacy` | $\langle g_v,-\sum_j g_j\rangle$ | 旧 IF 负对照；不是 proper TracIn |

其中，只有 point checkpoint 变体最接近标准 TracInCP；simple / graph checkpoint 版本是本项目为区分 source 构造而设计的 ablation。

## 3. 两条证据轴：公式逼真度与真实 GU 效果

这是本次比较最需要避免混淆的地方。

### 3.1 公式 / 排名 fidelity

前置 selection 验证显示：

| 比较 | Spearman $\rho$ | 解释 |
|---|---:|---|
| A vs B reference | 0.962 | 梯度幅值与参数移动信号高度接近 |
| `p_graph` vs `gt_full` | **0.984** | D-full 的 cheap proxy 几乎复现 reference 排名 |
| graph CP-3 / CP-6 vs `gt_full` | 0.498 / 0.529 | checkpoint graph 近似只保留中等一致性 |
| `p_point` vs `r_point` | 0.969 | C-point proxy 忠实 |
| `p_simple` vs `gt_simple` | 0.958 | C-simple proxy 忠实 |
| C-simple vs D-full | 0.040 | simple source 与 graph-deletion source 几乎不是同一排序 |
| B reference vs D-full | 0.023 | 参数移动与 graph-deletion source 基本正交 |
| C-point vs D-full | 0.112 | 点影响与删除图影响差异显著 |

这说明不同组并不是同一个 IF 的轻微数值变化，而是在测不同对象。

### 3.2 实际 GNNDelete 结果

但 fidelity 不自动转化为更大的删除伤害。例如 `p_graph` 与 `gt_full` 的排名高度一致，实际 F1 drop 也接近；二者仍然在 7/9 cells 中输给 degree。

> [!warning] 结论边界
> 我们可以说“`p_graph` 是 `gt_full` 的可靠近似”，不能据此说“D-full 已成为可靠的攻击 selector”。前者是估计问题，后者是跨数据集的下游有效性问题。

## 4. 全局结果：D 在 IF 内领先，但没有赢下强基线

下表按每个 dataset-seed cell 先聚合组内 selector，再与同 cell 的基线配对。F1 drop 越大，表示删除后性能下降越多。

| IF 组 | 平均 F1 drop (pp) | 相对 random (pp) | 对 random W/T/L | 相对 legacy (pp) | 相对 degree (pp) | 对 degree W/T/L |
|---|---:|---:|---:|---:|---:|---:|
| D reference/proxy (`gt_full`,`p_graph`) | **1.53** | **+0.99** | 4/2/3 | +0.75 | -1.31 | 2/0/7 |
| B (`b_param_hutch`) | 1.02 | +0.49 | 3/1/5 | +0.24 | -1.81 | 1/1/7 |
| D checkpoint (`graph3`,`graph6`) | 0.98 | +0.44 | 3/0/6 | +0.20 | -1.86 | 1/0/8 |
| C-point | 0.50 | -0.03 | 4/1/4 | -0.28 | -2.33 | 1/1/7 |
| C-simple | 0.05 | -0.48 | 2/0/7 | -0.73 | -2.78 | 0/0/9 |
| `degree` | **2.83** | +2.30 | 6/0/3 | — | — | — |
| `legacy` | 0.78 | +0.24 | — | — | -2.06 | — |
| `random` | 0.53 | — | — | — | -2.30 | — |

三个直接判断：

1. **D reference/proxy 是 IF 内部最有希望的组。**它相对 random 平均增加 0.99 pp F1 drop。
2. **它不是稳定胜者。**对 random 只有 4/9 wins；对 degree 只有 2/9 wins。
3. **C-simple 是明确的负 ablation。**它在 9/9 cells 中都没有超过 degree，并且整体低于 random 与 legacy。

如果把 14 个新 IF selector 全部混合成一个“新 IF 簇”，其 cell-level 平均相对 legacy 为 **-0.14 pp**，W/T/L = 2/0/7。因此不能再说“新 IF 簇整体比旧 IF 强”。

## 5. 为什么 pooled 结论没有普遍性：三数据集逐一看

### 5.1 Regime 总表

| 数据集 | 相对 random 最好的方向 | D ref/proxy 相对 random | B 相对 random | C-point 相对 random | 判断 |
|---|---|---:|---:|---:|---|
| Cora | degree / D / B | **+3.42 pp** | +2.60 pp | -0.11 pp | **D/B-aligned** |
| CiteSeer | degree / C-point | -0.07 pp | -0.67 pp | **+0.29 pp** | **C-point-aligned** |
| PubMed | 无稳定正方向 | -0.37 pp | -0.47 pp | -0.28 pp | **null** |

### 5.2 Cora：D/B 确实强，但 degree 仍领先

相对 random 的 F1 drop 增益：

- `degree`: **+5.93 pp**
- `gt_full`: +4.00 pp
- `p_graph`: +2.83 pp
- `b_param_hutch`: +2.60 pp
- graph CP-3 / CP-6: +2.30 / +2.27 pp
- `a_grad_norm`: +1.87 pp
- `legacy`: +0.73 pp
- C-point family: -0.11 pp

解释：显式 graph-deletion source 与参数移动量在 Cora 上确实捕获了有效脆弱性，但结构中心性仍提供了更强且更便宜的攻击方向。

### 5.3 CiteSeer：D/B 失效，C-point 反而最合理

CiteSeer 的 random F1 drop 只有 0.10 pp；相对 random：

- `degree`: **+1.07 pp**
- C-point family: **+0.29 pp**
  - point CP-6: +0.47 pp
  - `p_point`: +0.33 pp
  - `r_point`: +0.27 pp
  - point CP-3: +0.10 pp
- `legacy`: +0.07 pp
- D reference/proxy: -0.07 pp
- D checkpoint: -0.13 pp
- A: -0.53 pp
- B: -0.67 pp
- C-simple: -1.23 pp

这不是“Cora 上 D 组的弱化版”，而是方向发生了变化：只有 C-point 保留了 modest positive signal。

### 5.4 PubMed：当前固定 $k=7$ 下没有方法有效

PubMed 的 random F1 drop 为 0；17 个 selector 全部不高于 random。legacy 为 -0.07 pp、degree 为 -0.10 pp，D reference/proxy 为 -0.37 pp，B 为 -0.47 pp，D checkpoint 为 -0.82 pp。

因此这里没有理由比较“哪一种 IF 更强”；更合理的问题是：**$k=7$ 是否低于 PubMed 的可检测阈值，或者 GNNDelete 在该设置下是否把 selector 差异压平。**

## 6. B、C、D 三组应怎样评价

### 6.1 B：最紧凑的非 D 候选，但跨数据集不稳

- pooled F1 drop 为 1.02 pp，高于 C-point 与 C-simple。
- Cora 上有明确正信号；CiteSeer、PubMed 均低于 random。
- 因此 B 的价值更像“低成本 parameter-movement probe”，而不是当前可声明的通用 selector。
- 历史 B-LiSSA 只用于公式校验，未进入正式 17-method 矩阵，不能混入正式效果排名。

### 6.2 C-point：全局平均不强，但不能直接判死刑

- pooled 结果基本等于 random：-0.03 pp。
- 它在 CiteSeer 上是唯一形成组级正收益的 IF 方向。
- 这说明 C-point 可能对应另一种数据 regime，而不是 D-full 的低质量近似。
- 如果后续只看 pooled mean，会把这种方向反转抹掉。

### 6.3 C-simple：可以作为失败机制证据

- pooled 相对 random 为 -0.48 pp，相对 legacy 为 -0.73 pp。
- 对 degree 是 0/0/9。
- 它与 D-full 的 selection Spearman 只有 0.040。
- 这支持一个清晰的负结论：只保留 `grad1` source，并不能替代真实 graph-deletion source。

### 6.4 D-full：当前 IF 内最有希望，但结论必须限定

- reference/proxy pooled 相对 random +0.99 pp，为 IF 内最高。
- `p_graph` 与 `gt_full` Spearman 0.984，且二者 F1 drop 只差 -0.39 pp；9 cells 中 3 个 selected set 完全一致。
- 优势几乎由 Cora 提供；CiteSeer 与 PubMed 均未超过 random。
- 所以 D 的稳健贡献是“**cheap proxy fidelity + Cora-specific effectiveness**”，不是“跨数据集最优”。

## 7. checkpoint 与辅助指标：有信号，但还不能下强结论

### 7.1 checkpoint 数量没有单调规律

| 组别 | CP-6 − CP-3 F1 drop | W/T/L |
|---|---:|---:|
| C-point | +0.24 pp | 2/7/0 |
| D-graph | +0.04 pp | 2/3/4 |
| C-simple | -0.14 pp | 0/6/3 |

CP-6 对 point 有轻微帮助，对 graph 几乎无变化，对 simple 反而略差。当前不能把 checkpoint 数量当成通用增益旋钮。

### 7.2 辅助指标提示 D 可能“触发更新”，但未通过多重比较

- `gt_full` 的 update-detection AUC 为 0.984，较 legacy 高 +0.125；未校正 exact sign test $p=0.031$。
- `p_graph` 的 update-detection AUC 为 0.966，较 legacy 高 +0.107；未校正 $p=0.031$。
- `p_graph` 的 prediction flip 为 5.02%，较 legacy 高 +3.48 pp；未校正 exact $p=0.094$。

但是在 14 selectors × 5 metrics 的探索性比较中，没有结果在 Holm 校正后仍显著。它们适合写成“机制线索”，不适合写成 confirmatory claim。

> [!note] 关于 retrain gap
> 当前保存定义是 `perf_retrain - perf_unlearn`。负 gap 不能直接解释成“遗忘更好”，因此本次汇报不把 gap 的正负当作 selector 排名主指标。

### 7.3 工程可行性不是当前瓶颈

- 9/9 ScoreBundle cells 成功，153/153 method cold miss 随后均能 warm exact hit，0 failures。
- 共享计算后一次生成 17 个输出：cold 总时间 mean 6.8038 s、max 9.1624 s。
- ScoreBundle warm exact read：mean 0.3200 s、max 0.9635 s。
- 方法级 cold Selection Artifact 物化：global mean 522.4 ms、max 2365.1 ms。
- 峰值 GPU allocated / reserved：357 / 384 MiB。

因此，下一步是否继续某个 IF 方向，应由科学信号决定，而不是由显存或缓存架构限制决定。17 个方法的逐项 cold / warm 明细保留在正式 GU 报告中。

## 8. 为什么这轮很容易出现“不普遍”

当前边界会系统性影响跨数据集比较：

1. **固定 $k=7$ 不是固定删除比例。**public train pool 分别为 140 / 120 / 60，对应约 5.0% / 5.8% / 11.7%。
2. **只有 GCN + GNNDelete。**尚不能判断是 selector regime，还是特定 GU/backbone 的交互。
3. **每个数据集只有 3 seeds。**足以暴露方向反转，不足以稳定估计小效应。
4. **只测 top-$k$。**没有预算曲线，无法区分“排序错误”与“预算低于作用阈值”。
5. **只有三个小图数据集。**可提出异质性问题，但不足以学习或验证 regime predictor。

这也解释了为何当前最诚实的贡献是审计式结论，而不是“找到了普遍更强的 IF”。

## 9. 建议与学长讨论的三种路线

### 路线 A：接受 audit / heterogeneity 主线

可以保留并强化：

- IF 定义不是越复杂越好，source 选择会改变 selection 对象。
- fidelity 与 downstream effectiveness 是两条不同证据轴。
- 不同数据集出现 D/B、C-point、null 三种 regime。
- degree 是必须面对的强结构基线。
- proxy 的可靠性贡献可独立于 attack superiority 成立。

这是当前证据最完整、风险最低的路线。

### 路线 B：仍要做 method-superiority 主张

当前证据不足，必须补一个窄而有判别力的 generality gate：

| 维度 | 建议设置 |
|---|---|
| Selector | random、degree、B、最佳 C-point、`p_graph` / `gt_full` |
| Budget | 统一 5% + 至少一个 $k$-sweep |
| Dataset / seed | 3 datasets × 5 seeds |
| 第一阶段 | GCN + GNNDelete，约 75–90 cells |
| 扩展条件 | informed family 在至少 2/3 datasets 超过 random，且不被 degree 全面压制 |
| 第二阶段 | 只有通过上条，才增加第二 backbone 或第二 GU |

如果 gate 仍然出现 Cora-only，那么应停止“普遍更强”的资源投入。

### 路线 C：把条件性本身发展成方法

将问题改为：“能否在运行前识别该数据集更接近 D/B、C-point 还是 null regime，并选择相应 selector？”

这可能形成 meta-selector / regime diagnostic，但需要更多数据集与可解释的图统计量；不能只用当前 3 个数据集训练结论。

## 10. 建议会议上直接问的四个问题

1. **论文目标是什么？**我们接受“系统审计 + 极端异质性”，还是仍要求一个 universally stronger method？
2. **D 的贡献怎样定性？**是保留为 graph-deletion source 的机制候选，还是把重点放在 `p_graph ≈ gt_full` 的可行性贡献？
3. **是否值得补窄 generality gate？**如果值得，是否接受“不过 gate 就停止扩展”的预注册式判据？
4. **是否发展 regime diagnostic？**这会把工作从 selector 竞赛转成“何时哪类 influence signal 有效”。

## 11. 五分钟口头汇报稿

> 我们这次把 IF 簇完整放进了实际 GNNDelete 流程，而不是只比较 selection score。正式矩阵是 17 个 selector、3 个数据集、3 个 seed，共 153 个 cell，全部成功。
>
> 先说结论：新的 IF 簇并没有普遍超过旧 IF，也没有普遍超过 random，更没有超过 degree。D-full 的 reference 和 proxy 在 IF 内 pooled 平均最好，相对 random 多约 0.99 个百分点的 F1 drop；但它在 9 个 dataset-seed cell 里只赢 random 4 次，赢 degree 2 次。所以不能写成 D 组普遍更强。
>
> 真正有意思的是三个数据集出现了三种方向。Cora 是 D/B-aligned，`gt_full`、`p_graph` 和 B 都有效，但 degree 仍最好；CiteSeer 上 D 和 B 都不行，反而只有 C-point 有 modest positive signal；PubMed 上所有方法都没有超过 random，是一个 null regime。也就是说 pooled 的 D 优势主要来自 Cora，并不具有当前意义上的普遍性。
>
> 公式层面还是有一个扎实结果：`p_graph` 和 `gt_full` 的 Spearman 是 0.984，说明 cheap proxy 能很好复现 expensive reference。但这也恰好说明 fidelity 和 downstream damage 不能混为一谈——估得准，并不代表跨数据集都能造成更强的 GU 退化。
>
> 所以现在需要决定论文方向。如果做 audit，我们已经有一条诚实而完整的主线：IF source 存在目标错配、数据集异质性很强、degree 是难以击败的基线。如果还要坚持 method-superiority，我建议只补一个窄 gate：5 个代表 selector、统一 5% budget、3 数据集 5 seeds；只有 informed family 至少在 2/3 数据集超过 random，才扩第二个 GU 或 backbone。否则就停止把 D 写成通用方法。

## 12. 附录：17 个 selector 的总体排序

| 排名 | Selector | 平均 F1 drop (pp) | 相对 random (pp) | 对 random W/T/L | 相对 degree (pp) |
|---:|---|---:|---:|---:|---:|
| 1 | `degree` | 2.83 | +2.30 | 6/0/3 | — |
| 2 | `gt_full` | 1.72 | +1.19 | — | -1.11 |
| 3 | `p_graph` | 1.33 | +0.80 | — | -1.50 |
| 4 | `b_param_hutch` | 1.02 | +0.49 | 3/1/5 | -1.81 |
| 5 | `tracin_cp_graph_6` | 1.00 | +0.47 | — | -1.83 |
| 6 | `tracin_cp_graph_3` | 0.96 | +0.42 | — | -1.87 |
| 7 | `legacy` | 0.78 | +0.24 | — | -2.06 |
| 8 | `a_grad_norm` | 0.76 | +0.22 | — | -2.08 |
| 9 | `tracin_cp_point_6` | 0.70 | +0.17 | — | -2.13 |
| 10 | `random` | 0.53 | — | — | -2.30 |
| 11 | `tracin_cp_point_3` | 0.46 | -0.08 | — | -2.37 |
| 12 | `p_point` | 0.43 | -0.10 | — | -2.40 |
| 13 | `r_point` | 0.41 | -0.12 | — | -2.42 |
| 14 | `gt_simple` | 0.29 | -0.24 | — | -2.54 |
| 15 | `p_simple` | 0.11 | -0.42 | — | -2.72 |
| 16 | `tracin_cp_simple_3` | -0.02 | -0.56 | — | -2.85 |
| 17 | `tracin_cp_simple_6` | -0.17 | -0.70 | — | -3.00 |

> [!caution] 读表方式
> 该排序只是 9 个 cell 的 pooled 描述，不应覆盖第 5 节的 dataset-specific direction reversal。尤其是 C-point：全局排名低，但在 CiteSeer 上是唯一有正组级信号的 IF 方向。

## 13. 证据来源与可复核入口

- GU 正式矩阵与逐方法汇总：[`reports/small_selection_gu_FULL_REPORT.md`](../../../reports/small_selection_gu_FULL_REPORT.md)
- B/C 目标矩阵及历史 retrain 对照：[`reports/bc_target_matrix_REPORT.md`](../../../reports/bc_target_matrix_REPORT.md)
- IF / GIF 公式分类与 selection fidelity：[`report/paper/outline/A6_if_gif_taxonomy.md`](../../paper/outline/A6_if_gif_taxonomy.md)
- 正式 cell 指标：`results/runs/gpu4090-gu-20260722/analysis/cell_metrics.csv`
- dataset-selector 汇总：`results/runs/gpu4090-gu-20260722/analysis/dataset_selector_summary.csv`

本稿中的显著性均按 cell 配对解释；未特别注明者为描述性统计。14-selector、多指标探索未产生 Holm 校正后显著结果，因此所有“机制优势”均保留为待验证假设。
