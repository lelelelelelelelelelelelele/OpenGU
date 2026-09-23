# Cora: current 3000-epoch result tables

> Scope: generated only from the current AAGU-032 and AAGU-053 run manifests; previous-parameter result files were not read.
> Metric note: `utility.f1_after` / `f1_before` is computed by direct argmax accuracy in `experiments/unlearning_outputs.py`. Tables therefore label the endpoint test accuracy. Since these are single-label classification tasks, micro-F1 would numerically equal accuracy; macro-F1 is not present in these artifacts.

## AAGU-032 · Retrain test accuracy

Entries are mean ± sample SD over 3 training seeds; levels are percentages. AAGU-032 contains only full Retrain outcomes, so this table describes retained-task utility, not the behavior of GNNDelete or forgetting quality.

| Selector | 1% | 5% | 10% | 15% |
|---|---:|---:|---:|---:|
| gt_full | 90.16 ± 0.21 % | 89.24 ± 0.46 % | 89.79 ± 0.28 % | 88.62 ± 0.85 % |
| gt_full_all_trainable | 89.98 ± 0.38 % | 90.10 ± 0.28 % | 89.79 ± 0.28 % | 89.05 ± 0.95 % |
| degree | 90.10 ± 0.46 % | 89.85 ± 0.18 % | 89.98 ± 0.11 % | 89.73 ± 0.28 % |
| random | 90.10 ± 0.21 % | 89.61 ± 0.43 % | 89.85 ± 0.32 % | 89.24 ± 0.28 % |
| gt_simple | 89.91 ± 0.11 % | 89.73 ± 0.38 % | 89.79 ± 0.46 % | 89.54 ± 0.95 % |
| r_point | 89.67 ± 0.18 % | 89.54 ± 0.21 % | 88.75 ± 0.32 % | 87.64 ± 0.64 % |
| p_graph | 90.04 ± 0.00 % | 89.36 ± 0.38 % | 89.48 ± 0.37 % | 88.68 ± 1.13 % |
| p_point | 89.73 ± 0.11 % | 89.61 ± 0.28 % | 88.87 ± 0.46 % | 87.27 ± 0.49 % |
| gt_full_all_trainable_hops3 | 90.10 ± 0.28 % | 89.85 ± 0.18 % | 89.73 ± 0.21 % | 89.24 ± 0.93 % |
| gt_full_sgc_all_trainable_hops3 | 90.10 ± 0.11 % | 89.85 ± 0.49 % | 89.24 ± 0.46 % | 88.38 ± 0.49 % |

## AAGU-053 · GNNDelete and same-request Retrain

Each GU/Retrain comparison uses identical selected nodes. `n` is the number of selector requests (Degree: 1; other selectors: 3), with one training seed. Means ± sample SD describe variation across requests, not across independently trained models. Test-accuracy difference columns are percentage points.

| Selector | n | P0 test acc. (%) | GNNDelete (%) | Retrain (%) | P0−GU (pp) | P0−Retrain (pp) | Retrain−GU (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| degree | 1 | 90.22 % | 66.97 % | 90.04 % | 23.25 pp | 0.18 pp | 23.06 pp |
| random | 3 | 90.22 ± 0.00 % | 75.83 ± 1.92 % | 90.16 ± 0.43 % | 14.39 ± 1.92 pp | 0.06 ± 0.43 pp | 14.33 ± 1.74 pp |
| rr_1024 | 3 | 90.22 ± 0.00 % | 65.25 ± 1.87 % | 89.79 ± 0.95 % | 24.97 ± 1.87 pp | 0.43 ± 0.95 pp | 24.54 ± 2.31 pp |
| rr_4096 | 3 | 90.22 ± 0.00 % | 72.39 ± 5.75 % | 89.54 ± 0.70 % | 17.84 ± 5.75 pp | 0.68 ± 0.70 pp | 17.16 ± 5.06 pp |
| rr_16384 | 3 | 90.22 ± 0.00 % | 72.45 ± 2.04 % | 89.30 ± 0.37 % | 17.77 ± 2.04 pp | 0.92 ± 0.37 pp | 16.85 ± 2.22 pp |
| im_celf | 3 | 90.22 ± 0.00 % | 68.51 ± 0.77 % | 89.42 ± 0.38 % | 21.71 ± 0.77 pp | 0.80 ± 0.38 pp | 20.91 ± 0.46 pp |

Exact 48 paired requests: `AAGU-053-paired-GNNDelete-Retrain.csv`. Equal-request-weight dataset means, including the posterior-change membership AUC: `AAGU-053-dataset-summary.csv`. This AUC is an auxiliary update-detection measure, not a standalone privacy guarantee.
