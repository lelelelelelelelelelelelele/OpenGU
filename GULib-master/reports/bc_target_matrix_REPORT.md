---
title: A/B–C–D Influence Selection and Set-Deletion Matrix
date: 2026-07-20
status: accepted-local-matrix
datasets: [Cora, CiteSeer, PubMed]
model: GCN
seeds: [42, 212, 2024]
budgets: [3, 7, 14]
---

# A/B–C–D Influence Selection and Set-Deletion Matrix

## Verdict

本地 A/B–C–D 实验已完成以下闭环：

- 3 个 Planetoid 数据集；
- 3 个确定性 seed；
- 18 个完整 score/ranking 方法；
- k=3/7/14 三个删除预算；
- 9 个正式 Cache V2 Score Artifacts；
- 每个方法-预算的集合级删点、删边、重新训练验证；
- 不执行逐候选 exact retrain。

Selection 层的核心结论：

1. A 对 B reference 的全排序 Spearman 为 `0.962`，说明梯度 magnitude 是 B 排序的强 Hessian-free 代理，但二者不定义等价。
2. B reference 与 D-GIF 的 Spearman 仅 `0.023`，说明“参数移动大”与 graph-aware “伤害目标 E”不是同一排序。
3. 固定 source 后，single-final Hessian-free proxy 很可靠：
   - point：Spearman `0.969`；
   - simple：`0.958`；
   - graph：`0.984`。
4. `gt_simple`（C-IF）与 `gt_full`（D-GIF）的 Spearman 只有 `0.040`；删除图引起的邻居梯度变化不能默认忽略。
5. 3/6-checkpoint D graph trajectory 对 final `gt_full` 的 Spearman 仅 `0.498/0.529`，多 checkpoint 没有自动优于 single-final `p_graph`。

所有 \(H^{-1}g\) reference 均通过迭代 IHVP 求解。B-Hutch / B-LiSSA 的 `0.968` 只作为两种实现的一致性 sanity check，保留在复现结果中，不构成独立 selector 结论。

下游层单独回答：这些排名形成的 top-k 集合真正删掉并重训练后，validation target 与 test utility 如何变化。它不把 GIF reference overlap 当成真实 outcome 的替代。

下游结论是：`p_graph` 与 `gt_full` 的实际效果几乎相同，证明其 proxy fidelity 确实传递到选中集合；但 validation damage 最大的通常是 point/checkpoint selector。k=7 时 `tracin_cp_point_6` 的 mean validation-loss increase 为 `0.0707`，而 `gt_full` 为 `0.0118`。因此“最像 final GIF”和“最能破坏有限 top-k 集合”必须作为两个轴报告。

## Acceptance scope

| Item | Accepted setting |
|---|---|
| Datasets | Planetoid Cora / CiteSeer / PubMed |
| Model | two-layer GCN |
| Seeds | 42 / 212 / 2024 |
| Candidate pool | standard `train_mask` |
| Target E | `val_mask` mean cross-entropy |
| Test labels | selection 完成后只作 utility |
| Budgets | 3 / 7 / 14 |
| Training | Adam, 200 epochs, lr 0.01, wd 0.0005 |
| Hidden / dropout | 16 / 0.5 |
| Schedule | milestones 100/150, gamma 0.5 |
| Checkpoints | 1 / 10 / 25 / 50 / 100 / 200 |
| 3-checkpoint view | 1 / 50 / 200 |
| Affected set | candidate + undirected two-hop nodes |
| IHVP | LiSSA 20, scale 25, damp 0.01 |
| B-Hutchinson | 32 Rademacher probes, seed 1729 |
| Ranking | score descending, node ID ascending |
| Per-candidate exact retrain | not performed |

Candidate counts are 140 for Cora, 120 for CiteSeer, and 60 for PubMed. Each dataset uses 500 validation nodes as E.

## A/B–C–D taxonomy

| Layer | Score | Question |
|---|---|---|
| A | \(\lVert g_v\rVert\) | 训练梯度本身多大 |
| B | \(\lVert H^{-1}g_v\rVert\) | 删除后参数预计移动多远 |
| C-IF | \(q_v^\top H^{-1}g_E\), \(q_v\in\{g_v,\mathrm{grad1}_v\}\) | 不含删除后 `grad2` 时是否伤害目标 E |
| D-GIF | \((\mathrm{grad1}_v-\mathrm{grad2}_v)^\top H^{-1}g_E\) | 纳入图删除 source 后是否伤害目标 E |

B 不需要额外 target loss，因为它的目标就是 parameter displacement magnitude。C 与 D 需要 \(g_E\)，但只有 D 使用 `grad1-grad2` 的完整 graph-deletion source。

## Full method matrix

### Controls, A and B

| Family | Method | Definition | Role |
|---|---|---|---|
| control | `random` | deterministic seeded random | budget-matched control |
| control | `degree` | candidate degree | structural control |
| A | `a_grad_norm` | \(\lVert g_v\rVert\) | gradient magnitude |
| B | `b_param_lissa` | \(\lVert H^{-1}g_v\rVert\) | parameter-change reference |
| B implementation | `b_param_hutch` | shared-probe norm estimate | IHVP implementation sanity |

### Complete C-IF and D-GIF configurations

| Source | Hessian reference | Single-final proxy | 3 checkpoints | 6 checkpoints |
|---|---|---|---|---|
| C-point \(g_v\) | `r_point` | `p_point` | `tracin_cp_point_3` | `tracin_cp_point_6` |
| C-simple \(a_v=\mathrm{grad1}\) | `gt_simple` | `p_simple` | `tracin_cp_simple_3` | `tracin_cp_simple_6` |
| D-full \(q_v=\mathrm{grad1}-\mathrm{grad2}\) | `gt_full` | `p_graph` | `tracin_cp_graph_3` | `tracin_cp_graph_6` |

Reference and proxy definitions:

\[
\begin{aligned}
\text{point IF} &: \langle g_v,H^{-1}g_E\rangle,\\
\text{simple IF} &: \langle a_v,H^{-1}g_E\rangle,\\
\text{full GIF} &: \langle q_v,H^{-1}g_E\rangle,\\
\text{single-final proxy} &: \langle \text{same source},g_E\rangle,\\
\text{checkpoint proxy} &: \sum_c w_c\langle \text{source}(\theta_c),g_E(\theta_c)\rangle.
\end{aligned}
\]

`legacy = <g_v, -sum_j g_j>` is retained as a training-residual negative control. Only point checkpoint variants correspond closely to standard TracInCP; simple and graph versions are project-specific graph-source ablations.

## Experiment matrix coverage

| Layer | Coverage |
|---|---:|
| Dataset-seed selection cells | 9 |
| Methods per cell | 18 |
| Complete rankings | 162 |
| C/D rankings | 108 |
| Budgets per ranking | 3 |
| Pre-registered selection comparison rows | 378 |
| Dataset-seed downstream cells | 9 |
| Downstream method-budget rows | 486 |

k does not enter Score Artifact identity. One complete ranking per method is safely reused for k=3/7/14.

## Selection results

### A/B proxy and group separation

Global means over 9 dataset-seed cells:

| Comparison | k | Common | Jaccard | Spearman |
|---|---:|---:|---:|---:|
| A vs B-LiSSA | 3 | 0.741 | 0.656 | 0.962 |
| A vs B-LiSSA | 7 | 0.778 | 0.684 | 0.962 |
| A vs B-LiSSA | 14 | 0.881 | 0.793 | 0.962 |
| B-Hutch vs B-LiSSA | 3 | 0.704 | 0.578 | 0.968 |
| B-Hutch vs B-LiSSA | 7 | 0.810 | 0.696 | 0.968 |
| B-Hutch vs B-LiSSA | 14 | 0.841 | 0.735 | 0.968 |
| B-LiSSA vs D-GIF | 3 | 0.185 | 0.111 | 0.023 |
| B-LiSSA vs D-GIF | 7 | 0.175 | 0.104 | 0.023 |
| B-LiSSA vs D-GIF | 14 | 0.262 | 0.159 | 0.023 |

A strongly tracks B ranking. The B-Hutch/B-LiSSA rows are retained only as an IHVP implementation consistency check. The B/D disagreement is a semantic target difference, not evidence that B failed.

### Same-source Hessian removal

| Proxy vs reference | k=3 common / J | k=7 common / J | k=14 common / J | Spearman |
|---|---|---|---|---:|
| `p_point` vs `r_point` | 1.000 / 1.000 | 0.889 / 0.812 | 0.937 / 0.897 | 0.969 |
| `p_simple` vs `gt_simple` | 0.926 / 0.911 | 0.921 / 0.878 | 0.976 / 0.956 | 0.958 |
| `p_graph` vs `gt_full` | 0.926 / 0.889 | 0.905 / 0.833 | 0.929 / 0.870 | 0.984 |

The graph-aware final proxy is the strongest accepted approximation to the full GIF reference.

### Source mismatch

| Comparison | k=3 common / J | k=7 common / J | k=14 common / J | Spearman |
|---|---|---|---|---:|
| `gt_simple` vs `gt_full` | 0.111 / 0.067 | 0.111 / 0.066 | 0.151 / 0.085 | 0.040 |
| `r_point` vs `gt_full` | 0.148 / 0.089 | 0.190 / 0.107 | 0.262 / 0.154 | 0.112 |

Skipping `grad2` or using only the candidate gradient changes the source object. High point-IF fidelity does not imply full-GIF fidelity.

### Checkpoint ablation

| Checkpoint proxy vs same-source reference | k=7 common | k=7 Jaccard | Spearman |
|---|---:|---:|---:|
| `tracin_cp_point_3` | 0.746 | 0.607 | 0.901 |
| `tracin_cp_point_6` | 0.762 | 0.625 | 0.903 |
| `tracin_cp_simple_3` | 0.857 | 0.779 | 0.765 |
| `tracin_cp_simple_6` | 0.873 | 0.807 | 0.771 |
| `tracin_cp_graph_3` | 0.349 | 0.220 | 0.498 |
| `tracin_cp_graph_6` | 0.365 | 0.232 | 0.529 |

Six checkpoints are only marginally better than three. Neither beats the corresponding single-final proxy. Checkpoint accumulation changes the temporal object, so it is not guaranteed to approximate a final-point GIF reference.

### Dataset detail at k=7

| Dataset | B-Hutch vs LiSSA | P-point vs R-point | P-simple vs GT-simple | P-graph vs GT-full |
|---|---|---|---|---|
| Cora | 0.810 / 0.685 / 0.986 | 0.952 / 0.917 / 0.967 | 1.000 / 1.000 / 0.963 | 0.857 / 0.750 / 0.983 |
| CiteSeer | 0.714 / 0.569 / 0.946 | 0.810 / 0.685 / 0.944 | 0.810 / 0.717 / 0.920 | 0.905 / 0.833 / 0.974 |
| PubMed | 0.905 / 0.833 / 0.972 | 0.905 / 0.833 / 0.996 | 0.952 / 0.917 / 0.990 | 0.952 / 0.917 / 0.997 |

Each cell shows common fraction / Jaccard / full-ranking Spearman.

## Set-level downstream configuration

For every dataset, seed, method and k:

1. slice top-k from the cached full ranking;
2. remove selected nodes from `train_mask`;
3. remove all graph edges incident to selected nodes;
4. train one same-recipe GCN from the same deterministic initialization;
5. compare to the same-seed undeleted base model;
6. deduplicate identical selected sets across methods.

| Metric | Interpretation |
|---|---|
| validation loss increase | primary target damage |
| validation accuracy drop | secondary target damage |
| test loss increase | utility degradation |
| test accuracy drop | utility degradation |
| retained-train accuracy drop | training behavior |
| removed directed edges | structural exposure |

This is a selection-effect downstream test. It is not an approximate-GU algorithm test, and it does not introduce per-candidate exact retraining.

## Downstream results

### Coverage and runtime

| Measure | Value |
|---|---:|
| Dataset-seed cells | 9 |
| Method-budget rows | 486 |
| Unique selected sets retrained | 370 |
| Sum of per-cell runtime | 2466.2 s |
| Base model state matches selector model | 9 / 9 |
| CiteSeer/PubMed exact downstream warm hits | passed |

### Global outcome by budget

| k | Highest validation-loss method | Mean increase | Paired vs random | Validation accuracy drop | Test accuracy drop |
|---:|---|---:|---:|---:|---:|
| 3 | `tracin_cp_point_6` | 0.0218 | +0.0209 | 0.0138 | 0.0154 |
| 7 | `tracin_cp_point_6` | 0.0707 | +0.0596 | 0.0404 | 0.0560 |
| 14 | `tracin_cp_point_3` | 0.2898 | +0.2691 | 0.1484 | 0.1660 |

Larger budgets amplify the target effect and cross-dataset variance. These are descriptive means over nine cells, not significance claims.

### Complete C/D result at k=7

| Method | Family | Validation loss increase | Validation accuracy drop | Test accuracy drop |
|---|---|---:|---:|---:|
| `tracin_cp_point_6` | C-point | 0.0707 ± 0.0210 | 0.0404 | 0.0560 |
| `tracin_cp_point_3` | C-point | 0.0674 ± 0.0207 | 0.0391 | 0.0569 |
| `p_point` | C-point | 0.0616 ± 0.0332 | 0.0331 | 0.0421 |
| `tracin_cp_graph_3` | D-GIF trajectory | 0.0602 ± 0.0425 | 0.0367 | 0.0404 |
| `r_point` | C-point | 0.0602 ± 0.0277 | 0.0336 | 0.0387 |
| `tracin_cp_graph_6` | D-GIF trajectory | 0.0499 ± 0.0308 | 0.0362 | 0.0396 |
| `tracin_cp_simple_3` | C-IF trajectory | 0.0368 ± 0.0243 | 0.0142 | 0.0207 |
| `tracin_cp_simple_6` | C-IF trajectory | 0.0363 ± 0.0240 | 0.0144 | 0.0196 |
| `gt_simple` | C-IF reference | 0.0360 ± 0.0274 | 0.0124 | 0.0164 |
| `p_simple` | C-IF final proxy | 0.0307 ± 0.0331 | 0.0082 | 0.0132 |
| `p_graph` | D-GIF final proxy | 0.0127 ± 0.0233 | 0.0082 | 0.0071 |
| `gt_full` | D-GIF reference | 0.0118 ± 0.0243 | 0.0069 | 0.0082 |

The random k=7 mean is 0.0110. B-LiSSA and B-Hutchinson produce -0.0005 and -0.0078, respectively.

### Proxy/reference outcome preservation

Mean proxy-minus-reference validation-loss increase:

| Pair | k=3 | k=7 | k=14 |
|---|---:|---:|---:|
| `p_point - r_point` | 0.0000 | +0.0014 | +0.0013 |
| `p_simple - gt_simple` | -0.0012 | -0.0053 | +0.0005 |
| `p_graph - gt_full` | -0.0012 | +0.0010 | +0.0015 |

The same-source final proxies preserve not only the reference ranking but also the mean downstream effect. `p_graph` is therefore accepted as a faithful scalable proxy for `gt_full`.

### Fidelity is not finite-set optimality

`p_graph` is the best approximation to the final GIF reference, but the final GIF reference is not the strongest finite-set damage selector in this experiment:

| Method | Spearman to same/full reference | k=7 validation-loss increase |
|---|---:|---:|
| `p_graph` vs `gt_full` | 0.984 | 0.0127 |
| `tracin_cp_graph_3` vs `gt_full` | 0.498 | 0.0602 |
| `tracin_cp_graph_6` vs `gt_full` | 0.529 | 0.0499 |
| `p_point` vs `r_point` | 0.969 | 0.0616 |
| `tracin_cp_point_6` vs `r_point` | 0.903 | 0.0707 |

This is the decisive two-axis result:

- approximation question: `p_graph` best reproduces final GIF;
- attack-selection question: point/checkpoint methods often create larger finite-set deletion damage.

There is no contradiction. The first is a local per-candidate reference at the final model. The second contains simultaneous top-k deletion, graph intervention, parameter re-optimization and candidate interactions.

### Dataset-specific k=7 winners

| Dataset | Winner | Validation loss increase |
|---|---|---:|
| Cora | `tracin_cp_graph_3` | 0.0983 |
| CiteSeer | `gt_simple` | 0.0548 |
| PubMed | `tracin_cp_point_6` | 0.0771 |

No single source/checkpoint configuration wins on all datasets.

### B implementation rows in downstream evaluation

Paired validation-loss difference from random:

| Method | k=3 | k=7 | k=14 |
|---|---:|---:|---:|
| B-LiSSA | -0.0052 | -0.0116 | -0.0287 |
| B-Hutchinson | -0.0018 | -0.0188 | -0.0205 |

The two rows are implementations of the same B target, not distinct selectors. Their consistency is a reproducibility check; the substantive result is that B does not maximize validation damage here. Parameter movement magnitude is not eval-impact, although B may still be useful for algorithm-specific approximate-unlearning gap outside this local protocol.

## Cache V2 and provenance

### Score Artifacts

| Dataset | Seed | Artifact | Candidates | Cold total |
|---|---:|---|---:|---:|
| Cora | 42 | `score_26488c63_c1a785de` | 140 | 61.32 s |
| Cora | 212 | `score_46167175_175575a6` | 140 | 59.93 s |
| Cora | 2024 | `score_4346d28a_bbe857e7` | 140 | 68.05 s |
| CiteSeer | 42 | `score_5f4c4971_a329f277` | 120 | 158.63 s |
| CiteSeer | 212 | `score_65315186_8efc051a` | 120 | 140.93 s |
| CiteSeer | 2024 | `score_f69e8b38_375b858e` | 120 | 140.42 s |
| PubMed | 42 | `score_8b3257d6_c87fd4da` | 60 | 120.08 s |
| PubMed | 212 | `score_5f61998d_88b47a75` | 60 | 100.68 s |
| PubMed | 2024 | `score_23f2cbea_e1dd24dd` | 60 | 99.21 s |

The tracked selection summaries preserve all 18 full score vectors and rankings, candidate and target order hashes, dataset/model/checkpoint hashes, graph intervention metadata, numerical recipe, Artifact/Content hashes, and runtime. The device-local Cache V2 payload store is intentionally Git-ignored and reproducible from the frozen Recipe. Cora, CiteSeer and PubMed exact warm hits all passed with a producer-call failure guard. Recipe mismatch fails closed.

Downstream outputs use independent deterministic recipe hashes and retain selected-set hashes, base/selector state hashes, edge counts, retrained model hashes, effects and runtime.

### Legacy cache isolation

Before the matrix, legacy cache manifests were:

| Path | Files | Bytes | SHA-256 |
|---|---:|---:|---|
| `results/cache` | 1 | 3486 | `b4bd4abab68a8342e45525b8c208894cd3f1ca0af415fb8a4e9f795de4d26000` |
| `results/selection_cache` | 1 | 3051 | `5be6817293be58b5add31edf26d39cd1348883d7a74741bd511650144227d6e0` |
| `results/score_cache` | 1 | 5711 | `c8f3698077ff2bf9faa6553be770494fb361eee997e43054730f54e000f6f554` |

The same manifests are rechecked in final verification.

## Reproduction

```powershell
& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.run_matrix `
  --stage selection

& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.run_matrix `
  --stage downstream

& 'E:\conda_package\envs\gnn\python.exe' -m experiments.bc_target_v2.aggregate
```

Primary evidence:

- `results/bc_target_v2/aggregate/matrix_summary.json`;
- `results/bc_target_v2/aggregate/selection_metrics.csv`;
- `results/bc_target_v2/aggregate/selection_aggregate.csv`;
- `results/bc_target_v2/aggregate/cross_seed_stability.csv`;
- `results/bc_target_v2/aggregate/downstream_metrics.csv`;
- `results/bc_target_v2/aggregate/downstream_aggregate.csv`;
- `results/bc_target_v2/aggregate/global_downstream.csv`.

## Limits and next extension

- Three seeds support a descriptive supplementary conclusion, not a significance claim.
- Full GIF is an operational iterative-IHVP reference, not an exact-retrain ground truth.
- The local downstream validates true set deletion effects but not a particular approximate graph-unlearning algorithm.
- The next server matrix should begin with random, B reference, GT-full, P-graph and TracInCP-graph-6 under GNNDelete and GraphEraser, with independent GU recipes.
- Additional backbones, affected-hop definitions and checkpoint-weight searches remain future work.

## Acceptance decision

Accept:

- A as a strong Hessian-free proxy for B ranking in the accepted setting;
- IHVP implementation consistency as a reproducibility sanity check only;
- `p_graph` as the primary scalable D full-source proxy;
- separate reporting of C-IF and D-GIF;
- selection fidelity and downstream effect as two independent evaluation axes;
- Cache V2 score/ranking reuse across k.

Reject:

- treating B as a broken C/D method;
- promoting an IHVP solver variant to a separate selector or TracIn approximation;
- treating `gt_simple` or point IF as full GIF;
- assuming more checkpoints are automatically closer to final GIF;
- using overlap alone as proof of downstream effectiveness;
- any per-candidate exact-retrain expansion for this experiment.
