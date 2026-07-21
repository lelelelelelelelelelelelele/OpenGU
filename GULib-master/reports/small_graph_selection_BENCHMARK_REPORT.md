# 小图 Selection 全量实测报告

> **Verdict:** PASS — full cold/warm matrix and GPU telemetry complete

> **Authority:** ACCEPTED GT — one-time grandfathered public-split exception; no GPU rerun required.

## 1. 实测口径

- 正式矩阵：`Cora/CiteSeer/PubMed × seeds 42/212/2024`，共 9 cells。
- 正式 ScoreBundle 固定为 **17 个 score/ranking 输出**；`b_param_lissa` 仅是历史数值验证项，不进入本轮 bundle。
- cold method time：共享 ScoreBundle 已生成后，每个 ranking 首次物化 max-k Selection Artifact 的完整冷路径。
- cold ScoreBundle total：exact miss lookup、共享计算、17 输出构造、校验和落盘的总时间。
- warm read：同一 recipe 在 producer-call sentinel 下的 exact ScoreBundle 读取时间；17 个 Selection Artifact 也必须全部命中。
- 方法级时间包含逐 Artifact 的索引、校验与文件系统访问；warm hit 是零 producer 的正确性证据，不保证共享文件系统上的每次 wall-clock 都短于 cold。
- Experiment Git SHA：`9240b9a7bd61b17b4c841981ec2892fdf100dc4b`。

### 1.1 一次性 GT 特例

本轮 SSH 结果被指定为该 public Planetoid 17-output benchmark 的权威 GT，用于后续 selection 性能、ranking 与资源分析，不再因 dataset 根目录迁移重复消耗 GPU。该例外成立于以下已经完成的核验：

- 运行时使用的 `/autodl-fs/data/OpenGU-shared/Planetoid` 三套 public cache，在删除前已对 9 个有效输入逐文件验证为与 SSH active `data/raw/{cora,citeseer,pubmed}` 完全相同；当前 active 端重新计算的 source fingerprint 分别为 Cora `8201869d...`、CiteSeer `fba32999...`、PubMed `3ccd7393...`。
- `9240b9a` 到当前 accepted main 的 B/C `produce()` ScoreBundle 计算块逐字一致；`experiments/bc_target_v2/core.py` 与 `experiments/c_target_v1/core.py` 的 Git blob 未变化。后续修改只增加 canonical path 解析、dataset/Git provenance、Recipe 身份隔离与 SyncMate 调度，不改变 17 个 score 或 stable ranking 语义。
- 实测本身已覆盖 `9/9` cells、`153/153` cold miss→warm exact hit、0 failures，以及完整 GPU peak telemetry；重跑只能生成新的 v3.1 Recipe/Artifact 身份，不能增加本报告所需的算法或资源证据。

该特例只接受现有 v3.0 **result payload 与结论**。它不把历史 cache 冒充成 v3.1 warm hit，不把 worktree/shared path 写成当前 canonical path，也不把 `legacy` score 升格为 proper TracIn。未来新运行仍必须遵守 active-root fail-closed 合同。

## 2. Cell 总览

| Dataset | Seed | Status | Device | Cold bundle (s) | Warm read (s) | Peak alloc (MiB) | Peak reserve (MiB) | Failure |
|---|---:|---|---|---:|---:|---:|---:|---|
| Cora | 42 | success | cuda:0 | 9.1624 | 0.9635 | 187.8 | 208.0 | — |
| Cora | 212 | success | cuda:0 | 7.0050 | 0.1325 | 187.8 | 208.0 | — |
| Cora | 2024 | success | cuda:0 | 6.9413 | 0.1546 | 187.8 | 208.0 | — |
| CiteSeer | 42 | success | cuda:0 | 7.6537 | 0.1286 | 357.0 | 384.0 | — |
| CiteSeer | 212 | success | cuda:0 | 7.3706 | 0.1427 | 357.0 | 384.0 | — |
| CiteSeer | 2024 | success | cuda:0 | 6.9745 | 0.9430 | 357.0 | 384.0 | — |
| PubMed | 42 | success | cuda:0 | 5.1406 | 0.1448 | 268.2 | 314.0 | — |
| PubMed | 212 | success | cuda:0 | 5.0778 | 0.1315 | 268.2 | 314.0 | — |
| PubMed | 2024 | success | cuda:0 | 5.9085 | 0.1388 | 268.2 | 314.0 | — |

## 3. 方法级 cold / warm Selection 时间

| Dataset | Seed | Method | Cold selection (ms) | Warm selection (ms) | Cold outcome | Warm outcome | Status |
|---|---:|---|---:|---:|---|---|---|
| Cora | 42 | `a_grad_norm` | 1222.731 | 2637.590 | miss_saved | hit | success |
| Cora | 42 | `b_param_hutch` | 2269.844 | 2744.252 | miss_saved | hit | success |
| Cora | 42 | `degree` | 2157.279 | 2865.136 | miss_saved | hit | success |
| Cora | 42 | `gt_full` | 2285.796 | 2694.369 | miss_saved | hit | success |
| Cora | 42 | `gt_simple` | 2235.524 | 2383.186 | miss_saved | hit | success |
| Cora | 42 | `legacy` | 2304.373 | 285.899 | miss_saved | hit | success |
| Cora | 42 | `p_graph` | 2140.669 | 287.862 | miss_saved | hit | success |
| Cora | 42 | `p_point` | 2126.445 | 304.929 | miss_saved | hit | success |
| Cora | 42 | `p_simple` | 2205.524 | 292.551 | miss_saved | hit | success |
| Cora | 42 | `r_point` | 2065.667 | 286.541 | miss_saved | hit | success |
| Cora | 42 | `random` | 2179.714 | 322.264 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_graph_3` | 2138.960 | 296.392 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_graph_6` | 2246.771 | 296.753 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_point_3` | 2207.657 | 295.741 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_point_6` | 2236.006 | 281.822 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_simple_3` | 2365.102 | 286.046 | miss_saved | hit | success |
| Cora | 42 | `tracin_cp_simple_6` | 2326.838 | 239.897 | miss_saved | hit | success |
| Cora | 212 | `a_grad_norm` | 193.280 | 345.680 | miss_saved | hit | success |
| Cora | 212 | `b_param_hutch` | 284.104 | 381.531 | miss_saved | hit | success |
| Cora | 212 | `degree` | 280.614 | 304.790 | miss_saved | hit | success |
| Cora | 212 | `gt_full` | 314.743 | 290.863 | miss_saved | hit | success |
| Cora | 212 | `gt_simple` | 311.303 | 278.416 | miss_saved | hit | success |
| Cora | 212 | `legacy` | 326.659 | 292.236 | miss_saved | hit | success |
| Cora | 212 | `p_graph` | 297.062 | 370.113 | miss_saved | hit | success |
| Cora | 212 | `p_point` | 276.712 | 307.251 | miss_saved | hit | success |
| Cora | 212 | `p_simple` | 292.062 | 286.312 | miss_saved | hit | success |
| Cora | 212 | `r_point` | 288.682 | 280.345 | miss_saved | hit | success |
| Cora | 212 | `random` | 283.237 | 274.826 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_graph_3` | 302.789 | 282.134 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_graph_6` | 299.692 | 291.767 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_point_3` | 277.913 | 277.739 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_point_6` | 316.347 | 314.685 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_simple_3` | 306.921 | 382.622 | miss_saved | hit | success |
| Cora | 212 | `tracin_cp_simple_6` | 290.380 | 304.978 | miss_saved | hit | success |
| Cora | 2024 | `a_grad_norm` | 203.445 | 296.281 | miss_saved | hit | success |
| Cora | 2024 | `b_param_hutch` | 281.453 | 284.784 | miss_saved | hit | success |
| Cora | 2024 | `degree` | 279.872 | 282.633 | miss_saved | hit | success |
| Cora | 2024 | `gt_full` | 287.310 | 290.615 | miss_saved | hit | success |
| Cora | 2024 | `gt_simple` | 288.736 | 249.157 | miss_saved | hit | success |
| Cora | 2024 | `legacy` | 314.171 | 280.014 | miss_saved | hit | success |
| Cora | 2024 | `p_graph` | 332.486 | 283.879 | miss_saved | hit | success |
| Cora | 2024 | `p_point` | 280.342 | 285.458 | miss_saved | hit | success |
| Cora | 2024 | `p_simple` | 312.026 | 228.137 | miss_saved | hit | success |
| Cora | 2024 | `r_point` | 268.009 | 222.045 | miss_saved | hit | success |
| Cora | 2024 | `random` | 321.650 | 224.734 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_graph_3` | 259.013 | 228.327 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_graph_6` | 290.501 | 282.537 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_point_3` | 284.660 | 296.116 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_point_6` | 277.312 | 306.286 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_simple_3` | 284.313 | 374.165 | miss_saved | hit | success |
| Cora | 2024 | `tracin_cp_simple_6` | 327.154 | 295.563 | miss_saved | hit | success |
| CiteSeer | 42 | `a_grad_norm` | 190.481 | 431.866 | miss_saved | hit | success |
| CiteSeer | 42 | `b_param_hutch` | 326.306 | 321.229 | miss_saved | hit | success |
| CiteSeer | 42 | `degree` | 294.809 | 312.045 | miss_saved | hit | success |
| CiteSeer | 42 | `gt_full` | 315.230 | 304.948 | miss_saved | hit | success |
| CiteSeer | 42 | `gt_simple` | 311.476 | 323.448 | miss_saved | hit | success |
| CiteSeer | 42 | `legacy` | 296.251 | 307.450 | miss_saved | hit | success |
| CiteSeer | 42 | `p_graph` | 307.753 | 307.229 | miss_saved | hit | success |
| CiteSeer | 42 | `p_point` | 341.181 | 374.570 | miss_saved | hit | success |
| CiteSeer | 42 | `p_simple` | 350.067 | 311.982 | miss_saved | hit | success |
| CiteSeer | 42 | `r_point` | 292.828 | 314.697 | miss_saved | hit | success |
| CiteSeer | 42 | `random` | 305.736 | 300.579 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_graph_3` | 314.160 | 297.211 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_graph_6` | 308.926 | 317.949 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_point_3` | 295.532 | 309.275 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_point_6` | 308.244 | 313.048 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_simple_3` | 360.284 | 332.393 | miss_saved | hit | success |
| CiteSeer | 42 | `tracin_cp_simple_6` | 288.363 | 318.422 | miss_saved | hit | success |
| CiteSeer | 212 | `a_grad_norm` | 178.047 | 340.028 | miss_saved | hit | success |
| CiteSeer | 212 | `b_param_hutch` | 374.151 | 303.054 | miss_saved | hit | success |
| CiteSeer | 212 | `degree` | 337.222 | 289.163 | miss_saved | hit | success |
| CiteSeer | 212 | `gt_full` | 344.424 | 347.876 | miss_saved | hit | success |
| CiteSeer | 212 | `gt_simple` | 272.910 | 298.545 | miss_saved | hit | success |
| CiteSeer | 212 | `legacy` | 264.189 | 280.543 | miss_saved | hit | success |
| CiteSeer | 212 | `p_graph` | 276.630 | 288.915 | miss_saved | hit | success |
| CiteSeer | 212 | `p_point` | 277.247 | 282.109 | miss_saved | hit | success |
| CiteSeer | 212 | `p_simple` | 314.098 | 291.463 | miss_saved | hit | success |
| CiteSeer | 212 | `r_point` | 310.514 | 307.807 | miss_saved | hit | success |
| CiteSeer | 212 | `random` | 321.119 | 313.603 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_graph_3` | 301.738 | 301.716 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_graph_6` | 342.091 | 305.013 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_point_3` | 319.598 | 303.123 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_point_6` | 288.022 | 292.663 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_simple_3` | 282.717 | 310.949 | miss_saved | hit | success |
| CiteSeer | 212 | `tracin_cp_simple_6` | 319.132 | 309.156 | miss_saved | hit | success |
| CiteSeer | 2024 | `a_grad_norm` | 190.741 | 2570.941 | miss_saved | hit | success |
| CiteSeer | 2024 | `b_param_hutch` | 285.362 | 2588.932 | miss_saved | hit | success |
| CiteSeer | 2024 | `degree` | 390.880 | 3652.728 | miss_saved | hit | success |
| CiteSeer | 2024 | `gt_full` | 319.092 | 2718.543 | miss_saved | hit | success |
| CiteSeer | 2024 | `gt_simple` | 295.338 | 2613.364 | miss_saved | hit | success |
| CiteSeer | 2024 | `legacy` | 318.217 | 2930.877 | miss_saved | hit | success |
| CiteSeer | 2024 | `p_graph` | 300.514 | 2601.442 | miss_saved | hit | success |
| CiteSeer | 2024 | `p_point` | 279.439 | 2516.252 | miss_saved | hit | success |
| CiteSeer | 2024 | `p_simple` | 287.052 | 2597.938 | miss_saved | hit | success |
| CiteSeer | 2024 | `r_point` | 346.727 | 2660.460 | miss_saved | hit | success |
| CiteSeer | 2024 | `random` | 300.965 | 2521.141 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_graph_3` | 309.729 | 2493.627 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_graph_6` | 292.883 | 2553.067 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_point_3` | 304.450 | 2707.871 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_point_6` | 300.831 | 2871.084 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_simple_3` | 312.586 | 3885.406 | miss_saved | hit | success |
| CiteSeer | 2024 | `tracin_cp_simple_6` | 1981.020 | 2991.661 | miss_saved | hit | success |
| PubMed | 42 | `a_grad_norm` | 201.881 | 325.192 | miss_saved | hit | success |
| PubMed | 42 | `b_param_hutch` | 370.191 | 319.397 | miss_saved | hit | success |
| PubMed | 42 | `degree` | 309.903 | 312.683 | miss_saved | hit | success |
| PubMed | 42 | `gt_full` | 323.079 | 318.935 | miss_saved | hit | success |
| PubMed | 42 | `gt_simple` | 320.163 | 295.750 | miss_saved | hit | success |
| PubMed | 42 | `legacy` | 303.035 | 315.829 | miss_saved | hit | success |
| PubMed | 42 | `p_graph` | 289.459 | 317.080 | miss_saved | hit | success |
| PubMed | 42 | `p_point` | 296.943 | 298.747 | miss_saved | hit | success |
| PubMed | 42 | `p_simple` | 294.241 | 303.412 | miss_saved | hit | success |
| PubMed | 42 | `r_point` | 303.075 | 308.760 | miss_saved | hit | success |
| PubMed | 42 | `random` | 322.479 | 310.885 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_graph_3` | 313.285 | 313.604 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_graph_6` | 319.378 | 291.566 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_point_3` | 304.302 | 294.748 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_point_6` | 410.309 | 296.453 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_simple_3` | 299.954 | 306.762 | miss_saved | hit | success |
| PubMed | 42 | `tracin_cp_simple_6` | 337.899 | 321.136 | miss_saved | hit | success |
| PubMed | 212 | `a_grad_norm` | 238.997 | 397.142 | miss_saved | hit | success |
| PubMed | 212 | `b_param_hutch` | 385.357 | 356.967 | miss_saved | hit | success |
| PubMed | 212 | `degree` | 340.420 | 342.774 | miss_saved | hit | success |
| PubMed | 212 | `gt_full` | 311.207 | 326.588 | miss_saved | hit | success |
| PubMed | 212 | `gt_simple` | 297.879 | 311.212 | miss_saved | hit | success |
| PubMed | 212 | `legacy` | 308.218 | 304.823 | miss_saved | hit | success |
| PubMed | 212 | `p_graph` | 363.532 | 326.682 | miss_saved | hit | success |
| PubMed | 212 | `p_point` | 327.874 | 347.738 | miss_saved | hit | success |
| PubMed | 212 | `p_simple` | 376.344 | 302.558 | miss_saved | hit | success |
| PubMed | 212 | `r_point` | 406.243 | 311.043 | miss_saved | hit | success |
| PubMed | 212 | `random` | 314.660 | 311.631 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_graph_3` | 356.886 | 308.057 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_graph_6` | 290.398 | 303.083 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_point_3` | 287.574 | 285.973 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_point_6` | 306.188 | 305.038 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_simple_3` | 305.457 | 292.267 | miss_saved | hit | success |
| PubMed | 212 | `tracin_cp_simple_6` | 306.757 | 295.352 | miss_saved | hit | success |
| PubMed | 2024 | `a_grad_norm` | 196.064 | 366.174 | miss_saved | hit | success |
| PubMed | 2024 | `b_param_hutch` | 303.953 | 370.857 | miss_saved | hit | success |
| PubMed | 2024 | `degree` | 320.076 | 296.135 | miss_saved | hit | success |
| PubMed | 2024 | `gt_full` | 338.912 | 341.608 | miss_saved | hit | success |
| PubMed | 2024 | `gt_simple` | 346.879 | 305.931 | miss_saved | hit | success |
| PubMed | 2024 | `legacy` | 283.332 | 302.504 | miss_saved | hit | success |
| PubMed | 2024 | `p_graph` | 321.055 | 297.795 | miss_saved | hit | success |
| PubMed | 2024 | `p_point` | 385.446 | 299.094 | miss_saved | hit | success |
| PubMed | 2024 | `p_simple` | 299.420 | 295.587 | miss_saved | hit | success |
| PubMed | 2024 | `r_point` | 300.958 | 334.501 | miss_saved | hit | success |
| PubMed | 2024 | `random` | 318.795 | 330.595 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_graph_3` | 345.337 | 316.793 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_graph_6` | 318.782 | 321.299 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_point_3` | 323.200 | 378.328 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_point_6` | 336.122 | 291.994 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_simple_3` | 334.789 | 317.209 | miss_saved | hit | success |
| PubMed | 2024 | `tracin_cp_simple_6` | 314.008 | 321.571 | miss_saved | hit | success |

## 4. 汇总与失败状态

- 成功 cells：**9/9**；失败 cells：**0**。
- ScoreBundle cold total：mean `6.8038s`，max `9.1624s`。
- ScoreBundle warm exact read：mean `0.3200s`，max `0.9635s`。
- 方法级 cold selection：mean `522.404ms`，max `2365.102ms`。
- 方法级 warm selection：mean `660.689ms`，max `3885.406ms`。

## 5. Evidence

- Repository-retained manifest: `results/bc_target_v2/selection_benchmark_20260721/benchmark_manifest.json`
- Repository-retained cell summaries: `results/bc_target_v2/selection_benchmark_20260721/cells/`
- Historical runtime cache/worktree: retired after result/report hash verification；不再作为可复用 cache authority。
- Algorithm version: `bc-target-matrix-v3.0`
- Experiment Git SHA: `9240b9a7bd61b17b4c841981ec2892fdf100dc4b`
- Dataset identity and grandfathering audit: `reports/dataset_layout_AUDIT_REPORT.{md,html}`
