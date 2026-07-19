---
title: C 目标 TracIn、IF 与 GIF 近似有效性实验配置与结果
created: 2026-07-16
updated: 2026-07-17
type: supplementary-experiment-report
status: implemented-multi-dataset
tags: [eval-impact, tracin, influence-function, gif, graph-source, cache-v2]
aliases: [C目标实验, TracIn近似有效性实验, GIF近似GT实验]
---

# C 目标 TracIn、IF 与 GIF 近似有效性实验配置与结果

> 状态：**Cora / CiteSeer / PubMed，GCN，3 seeds，k=3/7/14 的 selection 与集合级下游矩阵已实施。** 坚决不做逐候选 exact retrain。

关联页面：

- [[20_IF目标层级对比实验计划]]：A/B/C 总对比与 B 实验；
- [[20_研究框架/21_TracIn变体与GIF关系]]：IF、GIF、TracIn 的概念关系；
- [完整验收报告](../../reports/bc_target_matrix_REPORT.md)。

## 0. 先给结论

本轮最重要的结论不是“TracIn 好或坏”，而是：

> **固定 source 后，用 \(g_E\) 替换 \(H^{-1}g_E\) 的 single-final Hessian-free proxy 很可靠；但改变 source，或把多个 checkpoint 简单累积起来，并不会自动更接近 full GIF。**

九个 dataset-seed 单元的全局结果：

| 固定 source 的比较 | k=7 common | k=7 Jaccard | 全排序 Spearman |
|---|---:|---:|---:|
| `p_point` vs `r_point` | 0.889 | 0.812 | 0.969 |
| `p_simple` vs `gt_simple` | 0.921 | 0.878 | 0.958 |
| `p_graph` vs `gt_full` | 0.905 | 0.833 | 0.984 |

相反：

| Source mismatch | k=7 common | k=7 Jaccard | 全排序 Spearman |
|---|---:|---:|---:|
| `gt_simple` vs `gt_full` | 0.111 | 0.066 | 0.040 |
| `r_point` vs `gt_full` | 0.190 | 0.107 | 0.112 |

多 checkpoint 的 graph 版本：

| 方法 vs `gt_full` | k=7 common | k=7 Jaccard | 全排序 Spearman |
|---|---:|---:|---:|
| `tracin_cp_graph_3` | 0.349 | 0.220 | 0.498 |
| `tracin_cp_graph_6` | 0.365 | 0.232 | 0.529 |

因此当前推荐顺序是：

1. full graph source 下优先 `p_graph`；
2. `gt_full` 作为 operation-level GIF reference；
3. checkpoint 数量不是单调增益，3/6 checkpoint 只保留为 trajectory ablation；
4. `p_point`、`p_simple` 只能解释各自 source 的 IF，不应写成 full GIF proxy。

真实 set-level 删除又给出另一条结论：`p_graph` 与 `gt_full` 的平均下游效果几乎一致，但 damage 最大的通常是 point/checkpoint selector。k=7 时 `tracin_cp_point_6=0.0707`，`gt_full=0.0118`。所以近似 GIF 的有效性与攻击式 selection 的有效性必须分开验收。

## 1. 两种“真值”必须分开

### 1.1 Selection reference

本页 selection 层的主 reference 是：

\[
\mathrm{GT}_{\mathrm{full}}(v;E)
=
\left\langle
\mathrm{grad1}_v-\mathrm{grad2}_v,\,
H^{-1}g_E
\right\rangle .
\]

它是操作性的 graph-aware GIF reference，不是数学上的 exact truth，也不是 exact-retrain truth。LiSSA 仍是有限迭代近似。

### 1.2 Downstream outcome

selection 做完后，真正的集合级 outcome 是：

1. 同时删掉 top-k 节点；
2. 删除这些节点关联的边；
3. 从同一初始化重新训练模型；
4. 实测 validation loss / accuracy 和 test utility。

所以：

- `gt_full` 回答“某个近似是否复现 GIF reference”；
- set-level retraining 回答“选中的整个集合删掉后实际效果怎样”。

两者都需要，不能用高 overlap 代替下游效果，也不能用一次下游结果反推逐候选 GIF 定义。

## 2. 三种 source

### 2.1 Candidate-only point source

\[
g_v=\nabla_\theta \ell_v(\theta;G).
\]

只包含候选节点自己的训练 loss gradient。

### 2.2 No-grad2 simple source

令 \(A_v\) 为候选与两跳 affected nodes：

\[
a_v=\mathrm{grad1}_v
=
\nabla_\theta
\sum_{i\in A_v}\ell_i(\theta;G).
\]

它在原图上加入 affected neighbors，但不构造删后图梯度。

### 2.3 Full graph-deletion source

在移除候选 \(v\) 关联边的图 \(G_{-v}\) 上：

\[
b_v=\mathrm{grad2}_v
=
\nabla_\theta
\sum_{i\in A_v\setminus\{v\}}\ell_i(\theta;G_{-v}),
\]

\[
q_v=a_v-b_v.
\]

`grad1` 与 `grad2` 都在同一参数 \(\theta\) 上做 forward/backward，不重训练模型。full source 逐候选构造删后图，但仍不是逐候选 exact retrain。

| Source | 候选自身 | 原图 affected neighbors | 删后图邻居变化 | 逐候选删图 forward/backward |
|---|---:|---:|---:|---:|
| \(g_v\) | 是 | 否 | 否 | 否 |
| \(a_v=\mathrm{grad1}\) | 是 | 是 | 否 | 否 |
| \(q_v=\mathrm{grad1}-\mathrm{grad2}\) | 是 | 是 | 是 | 是 |

## 3. 固定实验配置

| 配置 | 值 |
|---|---|
| Datasets | Cora、CiteSeer、PubMed |
| Model | two-layer GCN |
| Seeds | 42、212、2024 |
| Candidate pool | 标准 `train_mask` |
| Candidate counts | Cora 140；CiteSeer 120；PubMed 60 |
| Target E | 500 个 `val_mask` nodes，mean CE |
| Budgets | 3、7、14 |
| Optimizer | Adam |
| Epochs | 200 |
| LR / weight decay | 0.01 / 0.0005 |
| Hidden / dropout | 16 / 0.5 |
| Scheduler | milestones 100/150，gamma 0.5 |
| Checkpoints | 1、10、25、50、100、200 |
| 3-checkpoint view | 1、50、200 |
| 6-checkpoint view | 全六个 |
| TracIn weights | 各 checkpoint 对应 update learning rate |
| Affected hops | 2 |
| IHVP | LiSSA 20 iterations，scale 25，damp 0.01 |
| Ranking | score 降序，node ID 升序 tie-break |
| Exact candidate retrain | 未执行 |

正式 C 选择只读取 validation labels。test accuracy/loss 只在 selection Artifact 落盘后作为 downstream utility。

## 4. 完整 C 方法配置矩阵

### 4.1 Reference

| 方法 | Source | Target direction | Hessian | Checkpoint | 角色 |
|---|---|---|---:|---:|---|
| `r_point` | \(g_v\) | \(H^{-1}g_E\) | 是 | final | candidate-only point IF |
| `gt_simple` | \(a_v\) | \(H^{-1}g_E\) | 是 | final | no-grad2 IF approximate GT |
| `gt_full` | \(q_v\) | \(H^{-1}g_E\) | 是 | final | full graph-aware GIF GT |

三项共用一次：

\[
s_E=H^{-1}g_E,
\]

随后只计算 \(g_v^\top s_E\)、\(a_v^\top s_E\)、\(q_v^\top s_E\)。不存储完整 \(H^{-1}\)。

### 4.2 Single-final Hessian-free

| 方法 | Score | 相对 reference 只改变什么 |
|---|---|---|
| `p_point` | \(\langle g_v,g_E\rangle\) | 去掉 point IF 的 Hessian |
| `p_simple` | \(\langle a_v,g_E\rangle\) | 去掉 simple IF 的 Hessian |
| `p_graph` | \(\langle q_v,g_E\rangle\) | 去掉 full GIF 的 Hessian |

### 4.3 Multi-checkpoint

| 方法 | Source | Checkpoints | Score |
|---|---|---:|---|
| `tracin_cp_point_3` | \(g_v\) | 3 | \(\sum_c w_c\langle g_v(\theta_c),g_E(\theta_c)\rangle\) |
| `tracin_cp_point_6` | \(g_v\) | 6 | 同上 |
| `tracin_cp_simple_3` | \(a_v\) | 3 | \(\sum_c w_c\langle a_v(\theta_c),g_E(\theta_c)\rangle\) |
| `tracin_cp_simple_6` | \(a_v\) | 6 | 同上 |
| `tracin_cp_graph_3` | \(q_v\) | 3 | \(\sum_c w_c\langle q_v(\theta_c),g_E(\theta_c)\rangle\) |
| `tracin_cp_graph_6` | \(q_v\) | 6 | 同上 |

只有 point 版本接近原始 TracInCP。simple/graph checkpoint 版本是本项目的 graph-aware trajectory ablation，报告中不会把它们冒充原论文的标准实现。

### 4.4 Control

| 方法 | 定义 | 角色 |
|---|---|---|
| `legacy` | \(\langle g_v,-\sum_{j\in T}g_j\rangle\) | 旧 training-residual target negative control |
| `random` / `degree` / A / B | 见 [[20_IF目标层级对比实验计划]] | 外部锚点与目标层级对照 |

## 5. Selection 实验矩阵

| 轴 | 数量 |
|---|---:|
| Datasets | 3 |
| Seeds | 3 |
| Score/ranking methods | 18 |
| C methods | 12 |
| Budgets per ranking | 3 |
| Selection cells | 9 |
| 完整排名数 | 162 |
| C 排名数 | 108 |
| 预注册 reference-pair rows | 378 |

每个 cell 保存完整 score vectors 和 full rankings；k=3/7/14 是同一排名的三个切片。

## 6. Selection 结果

### 6.1 Single-final：固定 source 后去掉 Hessian

九个数据集-seed 单元的全局均值：

| Proxy vs same-source reference | k | common | Jaccard | Spearman |
|---|---:|---:|---:|---:|
| `p_point` vs `r_point` | 3 | 1.000 | 1.000 | 0.969 |
| `p_point` vs `r_point` | 7 | 0.889 | 0.812 | 0.969 |
| `p_point` vs `r_point` | 14 | 0.937 | 0.897 | 0.969 |
| `p_simple` vs `gt_simple` | 3 | 0.926 | 0.911 | 0.958 |
| `p_simple` vs `gt_simple` | 7 | 0.921 | 0.878 | 0.958 |
| `p_simple` vs `gt_simple` | 14 | 0.976 | 0.956 | 0.958 |
| `p_graph` vs `gt_full` | 3 | 0.926 | 0.889 | 0.984 |
| `p_graph` vs `gt_full` | 7 | 0.905 | 0.833 | 0.984 |
| `p_graph` vs `gt_full` | 14 | 0.929 | 0.870 | 0.984 |

`p_graph` 是当前 full GIF reference 的最佳 scalable proxy。这里的“去掉 Hessian”成立，是因为 \(q_v\) 和 \(g_E\) 均保持不变。

### 6.2 k=7 的分数据集结果

| Dataset | `p_point` vs `r_point` | `p_simple` vs `gt_simple` | `p_graph` vs `gt_full` |
|---|---|---|---|
| Cora | common 0.952 / J 0.917 / ρ 0.967 | 1.000 / 1.000 / 0.963 | 0.857 / 0.750 / 0.983 |
| CiteSeer | 0.810 / 0.685 / 0.944 | 0.810 / 0.717 / 0.920 | 0.905 / 0.833 / 0.974 |
| PubMed | 0.905 / 0.833 / 0.996 | 0.952 / 0.917 / 0.990 | 0.952 / 0.917 / 0.997 |

### 6.3 Source mismatch：simple/point 不能代替 full GIF

| 比较 | k | common | Jaccard | Spearman |
|---|---:|---:|---:|---:|
| `gt_simple` vs `gt_full` | 3 | 0.111 | 0.067 | 0.040 |
| `gt_simple` vs `gt_full` | 7 | 0.111 | 0.066 | 0.040 |
| `gt_simple` vs `gt_full` | 14 | 0.151 | 0.085 | 0.040 |
| `r_point` vs `gt_full` | 3 | 0.148 | 0.089 | 0.112 |
| `r_point` vs `gt_full` | 7 | 0.190 | 0.107 | 0.112 |
| `r_point` vs `gt_full` | 14 | 0.262 | 0.154 | 0.112 |

这说明 `grad2` 不是一个可以默认忽略的细节。no-grad2 的 IF reference 和 full GIF reference 在本矩阵中几乎是两个不同排序。

### 6.4 Checkpoint ablation

全局均值：

| 方法 vs same-source reference | k=7 common | k=7 Jaccard | Spearman |
|---|---:|---:|---:|
| `tracin_cp_point_3` | 0.746 | 0.607 | 0.901 |
| `tracin_cp_point_6` | 0.762 | 0.625 | 0.903 |
| `tracin_cp_simple_3` | 0.857 | 0.779 | 0.765 |
| `tracin_cp_simple_6` | 0.873 | 0.807 | 0.771 |
| `tracin_cp_graph_3` | 0.349 | 0.220 | 0.498 |
| `tracin_cp_graph_6` | 0.365 | 0.232 | 0.529 |

6 checkpoints 对 3 checkpoints 只有小幅改善；两者都没有超过对应 single-final proxy。尤其 graph trajectory 明显弱于 `p_graph`。

### 6.5 为什么多 checkpoint 没有自动变好

`gt_full` 是 final trained point 的局部 GIF reference：

\[
q_v(\theta_*)^\top H(\theta_*)^{-1}g_E(\theta_*).
\]

TracInCP 累积的是整个训练轨迹：

\[
\sum_c w_c q_v(\theta_c)^\top g_E(\theta_c).
\]

即使 source 名称相同，这两个对象仍不同：

- final GIF 关心最终点的局部曲率；
- TracInCP 关心训练路径上的梯度对齐累计。

所以 checkpoint 版本跳过 \(H^{-1}\) 的同时，也改变了时间语义。它可以是有用 selector，但不能预设会更接近 final GIF。

### 6.6 Cross-seed 稳定性

k=7 的三对 seed 平均 Jaccard：

| Dataset | `gt_full` | `p_graph` | `gt_simple` | `r_point` |
|---|---:|---:|---:|---:|
| Cora | 0.504 | 0.504 | 0.833 | 0.833 |
| CiteSeer | 0.358 | 0.358 | 0.833 | 0.620 |
| PubMed | 0.685 | 0.620 | 0.409 | 0.504 |

full graph source 在 CiteSeer 的小预算稳定性有限；但 `p_graph` 基本跟随 `gt_full`，说明 proxy 没额外制造大量不稳定。三 seed 结果只作描述性证据，不做显著性 claim。

## 7. 集合级下游配置

每个 C 方法和 k 都接受相同验证：

1. top-k 从该方法的完整排名切出；
2. 删除节点的 train membership；
3. 删除全部 incident graph edges；
4. 相同 seed、相同初始化、相同 GCN recipe 重训练；
5. 与 undeleted same-seed base 比较；
6. identical selected sets 只训练一次，结果复用到对应方法行。

主要指标：

- validation loss increase；
- validation accuracy drop；
- test loss increase；
- test accuracy drop；
- removed directed edges；
- runtime。

`gt_full` 与 `p_graph` 是两种独立的 C-GIF selection；`gt_simple` 与 `p_simple` 是两种 C-IF selection；point 和 checkpoint 路线也分别保留。没有只挑一次 top-7。

## 8. 集合级下游结果

### 8.1 全局结果

| 项目 | 数量 |
|---|---:|
| Dataset-seed cells | 9 |
| C 方法-预算结果 | 324 |
| 全部方法-预算结果 | 486 |
| 实际唯一 selected-set 重训练 | 370 |
| Base/selector state hash 一致 | 9 / 9 |

k=7 的 C 方法均值：

| 方法 | Family | Validation loss increase | Validation accuracy drop | Test accuracy drop |
|---|---|---:|---:|---:|
| `tracin_cp_point_6` | C-point | 0.0707 ± 0.0210 | 0.0404 | 0.0560 |
| `tracin_cp_point_3` | C-point | 0.0674 ± 0.0207 | 0.0391 | 0.0569 |
| `p_point` | C-point | 0.0616 ± 0.0332 | 0.0331 | 0.0421 |
| `tracin_cp_graph_3` | C-GIF trajectory | 0.0602 ± 0.0425 | 0.0367 | 0.0404 |
| `r_point` | C-point | 0.0602 ± 0.0277 | 0.0336 | 0.0387 |
| `tracin_cp_graph_6` | C-GIF trajectory | 0.0499 ± 0.0308 | 0.0362 | 0.0396 |
| `tracin_cp_simple_3` | C-IF trajectory | 0.0368 ± 0.0243 | 0.0142 | 0.0207 |
| `tracin_cp_simple_6` | C-IF trajectory | 0.0363 ± 0.0240 | 0.0144 | 0.0196 |
| `gt_simple` | C-IF reference | 0.0360 ± 0.0274 | 0.0124 | 0.0164 |
| `p_simple` | C-IF final proxy | 0.0307 ± 0.0331 | 0.0082 | 0.0132 |
| `p_graph` | C-GIF final proxy | 0.0127 ± 0.0233 | 0.0082 | 0.0071 |
| `gt_full` | C-GIF reference | 0.0118 ± 0.0243 | 0.0069 | 0.0082 |

random 的 k=7 validation-loss increase 为 `0.0110`。相对 random：

- `tracin_cp_point_6`: `+0.0596`；
- `p_point`: `+0.0505`；
- `tracin_cp_graph_3`: `+0.0492`；
- `gt_simple`: `+0.0250`；
- `p_graph`: `+0.0017`；
- `gt_full`: `+0.0007`。

### 8.2 Fidelity 与真实效果是两个轴

同 source 的 proxy/reference 在下游仍然非常接近。下面报告 proxy validation-loss increase 减去 reference：

| Proxy minus reference | k=3 | k=7 | k=14 |
|---|---:|---:|---:|
| `p_point - r_point` | 0.0000 | +0.0014 | +0.0013 |
| `p_simple - gt_simple` | -0.0012 | -0.0053 | +0.0005 |
| `p_graph - gt_full` | -0.0012 | +0.0010 | +0.0015 |

因此 `p_graph` 的高 fidelity 不只是排序数字：它与 `gt_full` 选出的集合也产生近乎相同的平均下游效果。

但 `gt_full` 本身并不是有限 top-k 集合删除中的最大-damage selector：

- k=7：`gt_full=0.0118`，`tracin_cp_point_6=0.0707`；
- k=14：`gt_full=0.0442`，`tracin_cp_point_3=0.2898`。

这不推翻 GIF reference。它说明：

1. `gt_full` 是 final point 的逐候选局部一阶 reference；
2. top-k 同时删除、删边并重新优化是有限幅度、含候选交互的 set-level problem；
3. “复现局部 GIF”与“寻找最破坏性的有限集合”可以产生不同 winner。

### 8.3 Checkpoint 方法的双重身份

graph checkpoint 方法对 `gt_full` 的 selection fidelity 较低，却产生更大的实际 damage：

| 方法 | Spearman vs `gt_full` | k=7 validation-loss increase |
|---|---:|---:|
| `p_graph` | 0.984 | 0.0127 |
| `tracin_cp_graph_3` | 0.498 | 0.0602 |
| `tracin_cp_graph_6` | 0.529 | 0.0499 |

所以：

- 若目标是 **近似 final GIF**，选 `p_graph`；
- 若目标是 **攻击式选择、最大化当前 set-level damage**，checkpoint 方法值得保留；
- 但不能把 checkpoint 方法造成更大 damage 写成“它更接近 GIF”。

### 8.4 数据集差异

k=7 每个数据集的最高 validation-loss increase：

| Dataset | Winner | Mean increase |
|---|---|---:|
| Cora | `tracin_cp_graph_3` | 0.0983 |
| CiteSeer | `gt_simple` | 0.0548 |
| PubMed | `tracin_cp_point_6` | 0.0771 |

没有一个 C 配置在三个数据集上统一获胜。PubMed 上 `gt_full` / `p_graph` 甚至低于 random，而 point checkpoint 仍明显高于 random；这进一步说明 source、trajectory 与有限集合交互需要分别解释。

### 8.5 预算趋势

| k | Global winner | Validation-loss increase | Paired vs random |
|---:|---|---:|---:|
| 3 | `tracin_cp_point_6` | 0.0218 | +0.0209 |
| 7 | `tracin_cp_point_6` | 0.0707 | +0.0596 |
| 14 | `tracin_cp_point_3` | 0.2898 | +0.2691 |

预算变大后，point trajectory 的优势显著扩大；同时标准差也增大，说明较大集合的非线性与数据集差异更强。

## 9. Cache 与结果文件

### 9.1 Score Artifact

正式缓存根：

```text
results/cache_v2/bc_target_v2/
```

九个 Score Artifacts：

| Dataset | Seed | Artifact |
|---|---:|---|
| Cora | 42 | `score_26488c63_c1a785de` |
| Cora | 212 | `score_46167175_175575a6` |
| Cora | 2024 | `score_4346d28a_bbe857e7` |
| CiteSeer | 42 | `score_5f4c4971_a329f277` |
| CiteSeer | 212 | `score_65315186_8efc051a` |
| CiteSeer | 2024 | `score_f69e8b38_375b858e` |
| PubMed | 42 | `score_8b3257d6_c87fd4da` |
| PubMed | 212 | `score_5f61998d_88b47a75` |
| PubMed | 2024 | `score_23f2cbea_e1dd24dd` |

Artifact payload 保存：

- ordered candidate IDs；
- 18 个完整 score vectors；
- 18 个 deterministic full rankings；
- dataset/model/checkpoint hashes；
- source intervention 与 affected-set metadata；
- LiSSA/Hutchinson 参数；
- seeds、numerics、runtime；
- `per_candidate_exact_retrain_performed=false`。

三数据集都通过 exact warm hit；recipe mismatch fail closed。

### 9.2 聚合输出

```text
results/bc_target_v2/aggregate/
  matrix_summary.json
  selection_metrics.csv
  selection_aggregate.csv
  cross_seed_stability.csv
  downstream_metrics.csv
  downstream_aggregate.csv
  global_downstream.csv
```

## 10. 复现命令

```powershell
& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.run_matrix `
  --stage selection

& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.run_matrix `
  --stage downstream

& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.aggregate
```

温命中检查：

```powershell
& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.run_selection `
  --dataset PubMed --seed 42 `
  --output results\bc_target_v2\cache_checks\pubmed_seed42_warm.json `
  --fail-if-producer-called
```

## 11. 已通过与未覆盖

### 已通过

- 3 datasets × 3 seeds；
- k=3/7/14；
- C-point / C-IF / C-GIF；
- single-final / 3 checkpoints / 6 checkpoints；
- Hessian reference / Hessian-free proxy；
- 全部方法集合级下游重训练；
- Cache V2 cold/warm/mismatch；
- 无逐候选 exact retrain。

### 未覆盖

- GAT 或其他 backbone；
- canonical 5 seeds 与显著性检验；
- 具体 approximate GU 方法的 end-to-end gap；
- checkpoint 权重、checkpoint epoch 的更大搜索；
- 不同 affected-hop 或 source normalization。

这些是后续扩展，不影响本轮对 source、Hessian 和 checkpoint 三个变量的结论。

## 12. 解释规则

| 观察 | 可以说 | 不能说 |
|---|---|---|
| `p_graph` 高 fidelity | full source 下可以有效跳过 Hessian | `p_graph` 等于 GIF |
| `gt_simple` 与 `gt_full` 低重合 | 删后图邻居变化不可默认忽略 | simple IF 没有任何用途 |
| point 方法只接近 point reference | candidate-only TracIn 回答 point IF 问题 | 它已逼近 full GIF |
| 6 checkpoint 略优于 3 | 当前轨迹密度有小幅增益 | checkpoint 越多越好 |
| checkpoint graph 低 fidelity | trajectory accumulation 不等于 final GIF | graph-aware TracIn 无效 |
| 下游 damage 与 fidelity 排名不同 | reference fidelity 与实际选择效果是两个轴 | reference 没意义 |

## 13. 一句话记忆

> C-selection 的 full GIF reference 是 \(\langle \mathrm{grad1}-\mathrm{grad2},H^{-1}g_E\rangle\)。本轮最强近似是同 source 的 single-final `p_graph`；多 checkpoint 没有修复 source 或时间语义的差异，真实效果仍要靠集合级删后重训练单独验证。
