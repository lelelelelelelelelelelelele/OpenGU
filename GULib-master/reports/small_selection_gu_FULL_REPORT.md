---
title: Small-graph 17-Selection to GNNDelete GU Full Matrix
date: 2026-07-22
status: accepted-formal-matrix
datasets: [Cora, CiteSeer, PubMed]
model: GCN
gu_method: GNNDelete
seeds: [42, 212, 2024]
selection_k: 7
---

# 小图 17-Selection → GNNDelete GU 全量实测报告

> **执行 Verdict：PASS。** 正式 gate 通过后，9 个 dataset-seed stage 全部验收；共 `153/153` GU cells、`612/612` 四件套 artifact、`0` failures。远端与本地逐文件 SHA-256 全量一致。

> **科学 Verdict：degree 胜出，TracIn 未胜出。** 在同 dataset-seed 配对口径下，`degree` 相对 random 的平均额外 F1 drop 为 **+2.30 pp**；标准 TracInCP 对应的最佳 point 变体 `tracin_cp_point_6` 只有 **+0.17 pp**，且 degree 在 9 格中有 8 格更强。

> **IF 内部 Verdict：效果与 reference fidelity 必须分开。** D-full reference `gt_full` 是本轮最强 IF row（相对 random **+1.19 pp**）；`p_graph` 是更均衡的可扩展 D-full proxy（**+0.80 pp**，对 `gt_full` 为 1 胜 / 6 平 / 2 负）。增加 checkpoint 不产生单调收益。

## 1. 回答两个研究问题

### 1.1 TracIn 是否比 degree 或其他方法更强？

**否，至少在本轮 GCN / GNNDelete / public fixed split / k=7 的 3×3 配对矩阵中不是。**

- `degree`：mean F1 drop `+2.83 pp`；paired $\Delta$ vs random `+2.30 pp`；6 胜 / 0 平 / 3 负。
- 标准 TracInCP point 最佳项 `tracin_cp_point_6`：mean F1 drop `+0.70 pp`；paired $\Delta$ vs random `+0.17 pp`；对 degree 为 **1 胜 / 0 平 / 8 负**，平均少 `2.13 pp`。
- 所有 checkpoint 变体中最强的是项目特定的 D-full graph trajectory `tracin_cp_graph_6`：paired $\Delta$ vs random `+0.47 pp`；对 degree 仍为 **1/0/8**，平均少 `1.83 pp`。
- `legacy` 是 deployed cross-gradient negative control，不是 proper TracIn；其 paired $\Delta$ 为 `+0.24 pp`，不能用于给 TracIn 正名。

因此，后续任何 GU 实验都应把 degree 保留为 mandatory control。不能再用“TracIn 理论上更复杂”推断其 top-k GU outcome 更强。

### 1.2 IF 家族内部哪种公式效果更好，同时可行？

本轮给出三层答案：

1. **最强 IF reference：`gt_full`。** 它纳入 graph-deletion source，paired $\Delta$ vs random 为 `+1.19 pp`，高于 point/simple reference 与 checkpoint variants。
2. **最均衡的 D-full 代表：`p_graph`。** 它的平均 F1 drop 比 `gt_full` 低 `0.39 pp`，9 个配对 cell 中 6 个 outcome 打平，3 个 selected set 完全相同；同时不需要把迭代 IHVP reference 作为部署前提。
3. **标准 TracInCP 代表：`tracin_cp_point_6`。** 6 checkpoints 比 3 checkpoints 平均高 `0.24 pp`，但仅 2 胜 / 7 平 / 0 负，且总体仍接近 random。checkpoint 数增加不是稳定的效果杠杆：graph 6 vs 3 近乎相同，simple 6 反而更差。

如果下一轮只保留一个 IF proxy，应选 `p_graph`；若同时保留 small-graph reference，则用 `gt_full + p_graph`。`tracin_cp_point_6` 只在明确研究 proper TracIn / trajectory 问题时保留，不能替代 degree control。

## 2. 正式实验口径与身份

| Field | Frozen value |
|---|---|
| SSH active checkout | `/autodl-fs/data/OpenGU/GULib-master` |
| Formal experiment Git SHA | `1c83bb433fcd31b81c5adbaee550dbaf6b4f03cd` |
| Branch / cleanliness | `main`; 每个 stage 前 preflight status 为空，stage 后 journal 归档并恢复 clean |
| Gate config | `syncmate_small_selection_gu_gate_v5.yaml`; SHA-256 `26c1b120...bd10` |
| Full config | `syncmate_small_selection_gu_full_v5.yaml`; SHA-256 `bdabc12b...e1dd` |
| Result identity | `results/runs/__syncmate_small_selection_gu_full_v5__` |
| Model / GU / k | two-layer GCN, hidden 64 / GNNDelete / exact `k=7` |
| Datasets | Cora / CiteSeer / PubMed `planetoid_public_fixed` |
| Public split | train `140/120/60`; validation `500`; test `1000` |
| Seeds | `42`, `212`, `2024` |
| Selection GT | accepted 17-output public benchmark; manifest SHA-256 `3212232a4274190e4c5a075eeea20fc92f982e7f4293670037795c2932e0e479` |
| Full-result checksum manifest | 612 rows; SHA-256 `e45aa4b193d53b854c709e3de543517417fa6a9f0d3eb1f013aea9bc3e16d236` |
| Claim boundary | controlled public-profile GNNDelete comparison；不是 OpenGU 80/20，也不是跨 GU-family / backbone 普遍结论 |

Selection 没有在 GU timed run 内重新计算。每个 stage 从 accepted GT materialize 新的 authoritative Cache V2 Selection Artifact，并校验 selector label、exact k、content hash、source manifest、dataset profile 和 Git provenance。

## 3. Gate、9-stage 与 SyncMate 验收

| Unit | Job ID | Cells | Artifacts | Result |
|---|---|---:|---:|---|
| Gate · Cora/42/degree | `gu-gate-v5-20260722-0702` | 1/1 | 4/4 | accepted |
| Cora · 42 | `gu-full-v5-cora-s42-20260722-0705` | 17/17 | 68/68 | accepted |
| Cora · 212 | `gu-full-v5-cora-s212-20260722-0713` | 17/17 | 68/68 | accepted |
| Cora · 2024 | `gu-full-v5-cora-s2024-20260722-0720` | 17/17 | 68/68 | accepted |
| CiteSeer · 42 | `gu-full-v5-citeseer-s42-20260722-0727` | 17/17 | 68/68 | accepted |
| CiteSeer · 212 | `gu-full-v5-citeseer-s212-20260722-0738` | 17/17 | 68/68 | accepted |
| CiteSeer · 2024 | `gu-full-v5-citeseer-s2024-20260722-0747` | 17/17 | 68/68 | accepted |
| PubMed · 42 | `gu-full-v5-pubmed-s42-20260722-0754` | 17/17 | 68/68 | accepted |
| PubMed · 212 | `gu-full-v5-pubmed-s212-20260722-0802` | 17/17 | 68/68 | accepted after direct collector gate |
| PubMed · 2024 | `gu-full-v5-pubmed-s2024-20260722-0810` | 17/17 | 68/68 | accepted after direct collector gate |

最后两个 PubMed dispatch 的 collector-side live watch 发生一次空 payload 解析，返回 `could not read runner queue`；远端唯一 job 已正常被同一 runner 领取，receipt 最终为 `done`、`exit_code=0`。没有重复 dispatch，也没有重跑 cell。随后调用 dispatch 正常路径使用的同一 collector acceptance，完成 68/68 collect、verify 和 scientific gate。该问题属于监控层瞬时空读，不影响 runner result、artifact checksum 或实验身份。

最终独立审计：

- 远端 result root 恰好 `612` files；合法四件套 `612`；`_meta.json` `153`。
- Cora / CiteSeer / PubMed 各 `51` cells；每个 leaf 恰好 4 files；无多余文件。
- 本地 durable copy：expected `612`、actual `612`、verified `612`、missing `0`、mismatch `0`、extra `0`。
- Gate 与 9 个 stage 的 journal、runner logs、runtime/store evidence 共 `874` files，证据包 SHA-256 `ecf158abcc062ba3b74fa7585d177e8bef7264736e24f809d65db4c9093122f1`。

## 4. 指标口径

主比较使用同一 dataset-seed 内的 budget-matched random 配对差：

$$
\Delta_{\mathrm{GU}}(S)=\mathrm{F1Drop}(S)-\mathrm{F1Drop}(\mathrm{random})
$$

正值表示 selector 比 random 造成更大的 GNNDelete 后 F1 下降。表中 W/T/L 都是 9 个 `(dataset, seed)` 配对 cell 的符号计数；只有 3 datasets × 3 seeds，因此本报告作描述性判断，不把 pooled n=9 写成普遍显著性证明。

Collateral 的 `gap` 按实际实现 `attack/attack_eval.py` 定义为：

$$
\mathrm{gap}=\mathrm{perf}_{\mathrm{retrain}}-\mathrm{perf}_{\mathrm{unlearn}}
$$

正值表示 approximate unlearn 的 F1 低于 exact retrain，属于额外近似损失；负值不等于“忘得更好”，只表示 approximate model 的 F1 高于 retrain。这里使用实现与 artifact 的存储语义，避免把相反符号的文档旧描述带入结论。

## 5. 全 17 selector 的 GU 效果

| Selector | Family | Mean F1 drop | Δ vs random | W/T/L vs random | Δ vs degree | W/T/L vs degree |
|---|---|---:|---:|---:|---:|---:|
| `degree` | control | +2.83 pp | +2.30 pp | 6/0/3 | +0.00 pp | 0/9/0 |
| `gt_full` | D-full-reference | +1.72 pp | +1.19 pp | 3/2/4 | -1.11 pp | 2/0/7 |
| `p_graph` | D-full-final-proxy | +1.33 pp | +0.80 pp | 4/2/3 | -1.50 pp | 2/0/7 |
| `b_param_hutch` | B-parameter-movement | +1.02 pp | +0.49 pp | 3/1/5 | -1.81 pp | 1/1/7 |
| `tracin_cp_graph_6` | D-full-checkpoint | +1.00 pp | +0.47 pp | 3/0/6 | -1.83 pp | 1/0/8 |
| `tracin_cp_graph_3` | D-full-checkpoint | +0.96 pp | +0.42 pp | 2/1/6 | -1.88 pp | 1/1/7 |
| `legacy` | legacy-negative-control | +0.78 pp | +0.24 pp | 5/0/4 | -2.06 pp | 2/0/7 |
| `a_grad_norm` | A-gradient-magnitude | +0.76 pp | +0.22 pp | 3/0/6 | -2.08 pp | 0/0/9 |
| `tracin_cp_point_6` | C-point-checkpoint | +0.70 pp | +0.17 pp | 5/0/4 | -2.13 pp | 1/0/8 |
| `random` | control | +0.53 pp | +0.00 pp | 0/9/0 | -2.30 pp | 3/0/6 |
| `tracin_cp_point_3` | C-point-checkpoint | +0.46 pp | -0.08 pp | 4/1/4 | -2.38 pp | 1/0/8 |
| `p_point` | C-point-final-proxy | +0.43 pp | -0.10 pp | 4/0/5 | -2.40 pp | 3/0/6 |
| `r_point` | C-point-reference | +0.41 pp | -0.12 pp | 4/0/5 | -2.42 pp | 3/0/6 |
| `gt_simple` | C-simple-reference | +0.29 pp | -0.24 pp | 2/1/6 | -2.54 pp | 0/1/8 |
| `p_simple` | C-simple-final-proxy | +0.11 pp | -0.42 pp | 1/2/6 | -2.72 pp | 0/1/8 |
| `tracin_cp_simple_3` | C-simple-checkpoint | -0.02 pp | -0.56 pp | 1/0/8 | -2.86 pp | 0/0/9 |
| `tracin_cp_simple_6` | C-simple-checkpoint | -0.17 pp | -0.70 pp | 1/0/8 | -3.00 pp | 0/0/9 |

### 5.1 Proxy/reference 与 checkpoint 对照

| Pair | Mean left − right F1 drop | W/T/L | Identical selected sets | Interpretation |
|---|---:|---:|---:|---|
| `p_graph - gt_full` | -0.39 pp | 1/6/2 | 3/9 | D-full proxy 基本保留 outcome，reference 稍强 |
| `p_point - r_point` | +0.02 pp | 1/7/1 | 3/9 | point final proxy 与 reference outcome 等价 |
| `p_simple - gt_simple` | -0.18 pp | 0/8/1 | 6/9 | simple proxy 与 reference 高度重合，但两者攻击都弱 |
| `point_6 - point_3` | +0.24 pp | 2/7/0 | 1/9 | 6 checkpoints 略高，证据仍弱 |
| `graph_6 - graph_3` | +0.04 pp | 2/3/4 | 0/9 | checkpoint 数基本无效 |
| `simple_6 - simple_3` | -0.14 pp | 0/6/3 | 5/9 | 更多 checkpoint 反而略差 |

这支持“reference fidelity”和“有限 top-k GU damage”分轴报告。`p_graph` 是很好的 D-full proxy，但忠实近似 reference 不保证超过 degree。

## 6. 数据集异质性

| Selector | Cora Δrandom | CiteSeer Δrandom | PubMed Δrandom |
|---|---:|---:|---:|
| `degree` | +5.93 pp | +1.07 pp | -0.10 pp |
| `gt_full` | +4.00 pp | -0.07 pp | -0.37 pp |
| `p_graph` | +2.83 pp | -0.07 pp | -0.37 pp |
| `b_param_hutch` | +2.60 pp | -0.67 pp | -0.47 pp |
| `tracin_cp_graph_6` | +2.27 pp | -0.13 pp | -0.73 pp |
| `tracin_cp_graph_3` | +2.30 pp | -0.13 pp | -0.90 pp |
| `legacy` | +0.73 pp | +0.07 pp | -0.07 pp |
| `a_grad_norm` | +1.87 pp | -0.53 pp | -0.67 pp |
| `tracin_cp_point_6` | +0.47 pp | +0.47 pp | -0.43 pp |
| `random` | +0.00 pp | +0.00 pp | +0.00 pp |
| `tracin_cp_point_3` | +0.10 pp | +0.10 pp | -0.43 pp |
| `p_point` | -0.50 pp | +0.33 pp | -0.13 pp |
| `r_point` | -0.50 pp | +0.27 pp | -0.13 pp |
| `gt_simple` | +0.77 pp | -1.23 pp | -0.27 pp |
| `p_simple` | +0.23 pp | -1.23 pp | -0.27 pp |
| `tracin_cp_simple_3` | +0.17 pp | -1.23 pp | -0.60 pp |
| `tracin_cp_simple_6` | +0.17 pp | -1.23 pp | -1.03 pp |

全局均值主要由 Cora 驱动。CiteSeer 只有 degree 和 point family 有小幅正效果；PubMed 的 3-seed 均值中没有 selector 超过 random。固定 k=7 对三个 public train pools 代表不同删除比例，因此不应把本表解释成 dataset-size 无关排序。

## 7. Collateral 与 GU 内部耗时

| Selector | gap (retrain − unlearn) | Fraction flipped | Mean unlearn | Mean attack inner total |
|---|---:|---:|---:|---:|
| `degree` | +1.41 pp | 3.96% | 0.432s | 1.106s |
| `gt_full` | +1.12 pp | 3.92% | 0.423s | 1.092s |
| `p_graph` | +1.27 pp | 5.02% | 0.452s | 1.193s |
| `b_param_hutch` | +0.43 pp | 2.07% | 0.450s | 1.180s |
| `tracin_cp_graph_6` | -3.20 pp | 2.12% | 0.458s | 1.172s |
| `tracin_cp_point_6` | -3.22 pp | 2.78% | 0.419s | 1.119s |
| `random` | -0.74 pp | 1.89% | 0.405s | 1.074s |
| `gt_simple` | -1.02 pp | 2.24% | 0.423s | 1.098s |
| `tracin_cp_simple_6` | -2.01 pp | 2.24% | 0.426s | 1.109s |

`degree`、`gt_full`、`p_graph` 同时给出正 paired F1 damage 和正 approximation gap；checkpoint/point rows 的 gap 多为负。后者不能写成更好的 unlearning，因为本指标只比较 utility，没有直接证明删除信息被更彻底移除。

153 cells 的 `attack.json` 内部计时汇总为：unlearn mean/max `0.440/0.574 s`，attack inner total mean/max `1.144/1.368 s`，Selection Artifact reuse mean/max `0.596/2.241 s`。这些是 artifact 内部阶段时间，不等于整个 stage wall-clock；完整 stage 还包括进程初始化、base/retrain/collateral 路径、日志与 SyncMate collect/verify。

## 8. Selection cold / ScoreBundle / warm / GPU 可行性

这部分引用已接受的一次性 GT，不声称 GU run 重新执行了 Selection producer：

- 9/9 ScoreBundle cells 成功；153/153 method cold miss → warm exact hit；0 failures。
- 一次生成 17 outputs 的 cold ScoreBundle total：mean `6.8038 s`，max `9.1624 s`。
- ScoreBundle warm exact read：mean `0.3200 s`，max `0.9635 s`。
- 方法级 cold Selection Artifact 物化：global mean `522.4 ms`，max `2365.1 ms`。
- 峰值 GPU allocated/reserved：`357.0/384.0 MiB`。

| Selector | Cold mean / max | Warm mean / max | Success |
|---|---:|---:|---:|
| `degree` | 523.5 / 2157.3 ms | 962.0 / 3652.7 ms | 9/9 |
| `gt_full` | 537.8 / 2285.8 ms | 848.3 / 2718.5 ms | 9/9 |
| `p_graph` | 514.4 / 2140.7 ms | 564.6 / 2601.4 ms | 9/9 |
| `b_param_hutch` | 542.3 / 2269.8 ms | 852.3 / 2744.3 ms | 9/9 |
| `tracin_cp_graph_6` | 523.3 / 2246.8 ms | 551.4 / 2553.1 ms | 9/9 |
| `tracin_cp_graph_3` | 515.8 / 2139.0 ms | 537.5 / 2493.6 ms | 9/9 |
| `legacy` | 524.3 / 2304.4 ms | 588.9 / 2930.9 ms | 9/9 |
| `a_grad_norm` | 312.9 / 1222.7 ms | 856.8 / 2637.6 ms | 9/9 |
| `tracin_cp_point_6` | 531.0 / 2236.0 ms | 585.9 / 2871.1 ms | 9/9 |
| `random` | 518.7 / 2179.7 ms | 545.6 / 2521.1 ms | 9/9 |
| `tracin_cp_point_3` | 511.7 / 2207.7 ms | 572.1 / 2707.9 ms | 9/9 |
| `p_point` | 510.2 / 2126.4 ms | 557.3 / 2516.3 ms | 9/9 |
| `r_point` | 509.2 / 2065.7 ms | 558.5 / 2660.5 ms | 9/9 |
| `gt_simple` | 520.0 / 2235.5 ms | 784.3 / 2613.4 ms | 9/9 |
| `p_simple` | 525.6 / 2205.5 ms | 545.5 / 2597.9 ms | 9/9 |
| `tracin_cp_simple_3` | 539.1 / 2365.1 ms | 720.9 / 3885.4 ms | 9/9 |
| `tracin_cp_simple_6` | 721.3 / 2326.8 ms | 599.7 / 2991.7 ms | 9/9 |

方法级时间是在 shared ScoreBundle 已经生成后逐 Artifact 的索引、校验和文件系统访问，不能解释为每个 scorer 独立重算的成本。某些 warm wall-clock 大于 cold 是共享文件系统抖动；producer sentinel 和 exact hit 才是 cache correctness 证据。

结论是：17 个公式在这三张小图上都**工程可行**，没有显存或失败门槛。选择哪一行应由 scientific role 决定，而不是由小图 runtime 决定。

## 9. 与既有 local set-deletion 结果的关系

既有 `bc_target_matrix_REPORT` 在 exact set deletion + retrain validation target 上，k=7 的 strongest row 是 `tracin_cp_point_6`；本轮真实 GNNDelete GU outcome 则由 degree 胜出。这不是结果冲突，而是两个不同问题：

- local downstream：选中集合被真正删掉并重新训练后，validation loss / test utility 如何变化；
- 当前矩阵：同一 selected set 进入特定 approximate GU method 后，GNNDelete outcome 与 exact retrain gap 如何变化。

反转说明 selection-only validation damage 不能替代 target-GU 实验；GU algorithm 与 selected set 的 interaction 是实证对象。这也正面验证了本轮坚持跑完整 17×3×3，而不是只挑旧 validation winner 的必要性。

## 10. 可引用结论与不应扩张的结论

### 可引用

- 在本轮 controlled public-profile GNNDelete 矩阵中，degree 是最强且最稳定的 selector control。
- 标准 TracInCP point variants 没有超过 degree，平均只接近 random。
- D-full `gt_full` 是最强 IF reference；`p_graph` 是 fidelity / feasibility 更均衡的 proxy。
- 更多 checkpoints 不自动提高 GU damage。
- selector 排序具有强 dataset heterogeneity，Cora 效应不能外推到 PubMed。
- Cache V2 + SyncMate 支撑了 9 个 stage 的 selection reuse、串行 dispatch、回传和 checksum acceptance；612 文件已在本地 durable 落盘。

### 不应扩张

- 不写“degree 对所有 GU family / backbone 普遍最强”；本轮只有 GNNDelete + GCN。
- 不把 public fixed split 改称 OpenGU canonical 80/20。
- 不把 `legacy` 改称 proper TracIn。
- 不把 3 datasets × 3 seeds 的描述性 W/T/L 写成大样本显著性。
- 不用 negative gap 宣称更彻底遗忘。
- 本轮不是 E7 query-free surrogate-transfer：`selector_model_id != target_model_id` 的 C.6a/C.6b 问题仍未回答。

## 11. Evidence 与机器可读输出

- Formal results：`results/runs/gpu4090-gu-20260722/__syncmate_small_selection_gu_full_v5__/`
- Formal gate：`results/runs/gpu4090-gu-20260722/__syncmate_small_selection_gu_v5__/`
- Verification receipts：`results/runs/gpu4090-gu-20260722/_verification/`
- Gate + stage evidence：`results/runs/gpu4090-gu-20260722/_evidence/{gate-v5,full-v5}/`
- Machine-readable aggregate：`results/runs/gpu4090-gu-20260722/analysis/`
  - `summary.json`
  - `cell_metrics.csv`
  - `selector_summary.csv`
  - `dataset_selector_summary.csv`
  - `pairwise_summary.csv`
  - `selection_timing_summary.csv`
- Selection performance authority：`results/bc_target_v2/selection_benchmark_20260721/benchmark_manifest.json`
- Implementation contract：`docs/small_selection_gu_syncmate_IMPLEMENTATION_ACCEPTANCE_REPORT.{md,html}`

机器聚合由 `experiments/gu_target_v1/aggregate.py` 执行。它在输出统计前重新验证固定 Git SHA、153-cell grid、每 leaf 四件套、Selection manifest authority 和 612-row checksum manifest；任一缺件、漂移或 failure 都会 fail closed。
