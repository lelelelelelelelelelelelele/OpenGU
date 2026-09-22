# PubMed: current 3000-epoch result tables

> Scope: generated only from the current AAGU-032 and AAGU-053 run manifests; previous-parameter result files were not read.
> Metric note: `utility.f1_after` / `f1_before` is computed by direct argmax accuracy in `experiments/unlearning_outputs.py`. Tables therefore label the endpoint test accuracy. Since these are single-label classification tasks, micro-F1 would numerically equal accuracy; macro-F1 is not present in these artifacts.

## AAGU-032 · Retrain test accuracy

Entries are mean ± sample SD over 3 training seeds; levels are percentages. AAGU-032 contains only full Retrain outcomes, so this table describes retained-task utility, not the behavior of GNNDelete or forgetting quality.

| Selector | 1% | 5% | 10% | 15% |
|---|---:|---:|---:|---:|
| gt_full | 88.31 ± 0.10 % | 87.76 ± 0.35 % | 86.49 ± 0.71 % | 85.83 ± 0.43 % |
| gt_full_all_trainable | 88.49 ± 0.04 % | 88.14 ± 0.38 % | 87.42 ± 0.22 % | 87.20 ± 0.94 % |
| degree | 88.39 ± 0.26 % | 88.51 ± 0.22 % | 88.75 ± 0.04 % | 88.45 ± 0.15 % |
| random | 88.47 ± 0.08 % | 88.36 ± 0.17 % | 88.76 ± 0.19 % | 88.62 ± 0.37 % |
| gt_simple | 88.39 ± 0.12 % | 88.31 ± 0.24 % | 88.01 ± 0.29 % | 87.95 ± 0.32 % |
| r_point | 88.26 ± 0.17 % | 87.74 ± 0.33 % | 86.11 ± 0.62 % | 85.09 ± 0.70 % |
| p_graph | 88.28 ± 0.32 % | 87.94 ± 0.06 % | 86.71 ± 0.51 % | 85.93 ± 0.73 % |
| p_point | 88.49 ± 0.14 % | 87.60 ± 0.30 % | 86.12 ± 0.56 % | 85.13 ± 0.72 % |
| gt_full_all_trainable_hops3 | 88.61 ± 0.01 % | 88.24 ± 0.16 % | 87.68 ± 0.60 % | 87.06 ± 0.74 % |
| gt_full_sgc_all_trainable_hops3 | 88.67 ± 0.04 % | 88.80 ± 0.12 % | 88.46 ± 0.42 % | 88.71 ± 0.06 % |

## AAGU-053 · GNNDelete and same-request Retrain

Each GU/Retrain comparison uses identical selected nodes. `n` is the number of selector requests (Degree: 1; other selectors: 3), with one training seed. Means ± sample SD describe variation across requests, not across independently trained models. Difference columns are percentage points.

| Selector | n | P0 test acc. (%) | GNNDelete (%) | Retrain (%) | P0−GU (pp) | P0−Retrain (pp) | Retrain−GU (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| degree | 1 | 88.56 % | 87.22 % | 88.72 % | 1.34 pp | -0.15 pp | 1.50 pp |
| random | 3 | 88.56 ± 0.00 % | 86.23 ± 0.71 % | 88.62 ± 0.18 % | 2.33 ± 0.71 pp | -0.05 ± 0.18 pp | 2.38 ± 0.53 pp |
| rr_1024 | 3 | 88.56 ± 0.00 % | 85.49 ± 0.10 % | 88.35 ± 0.09 % | 3.08 ± 0.10 pp | 0.21 ± 0.09 pp | 2.87 ± 0.13 pp |
| rr_4096 | 3 | 88.56 ± 0.00 % | 85.50 ± 1.11 % | 88.59 ± 0.09 % | 3.07 ± 1.11 pp | -0.03 ± 0.09 pp | 3.09 ± 1.14 pp |
| rr_16384 | 3 | 88.56 ± 0.00 % | 84.49 ± 0.48 % | 88.31 ± 0.26 % | 4.07 ± 0.48 pp | 0.25 ± 0.26 pp | 3.82 ± 0.72 pp |
| im_celf | 3 | 88.56 ± 0.00 % | 86.82 ± 0.12 % | 88.44 ± 0.12 % | 1.74 ± 0.12 pp | 0.13 ± 0.12 pp | 1.61 ± 0.23 pp |

Exact 48 paired requests: `AAGU-053-paired-GNNDelete-Retrain.csv`. Equal-request-weight dataset means, including the posterior-change membership AUC: `AAGU-053-dataset-summary.csv`. This AUC is an auxiliary update-detection measure, not a standalone privacy guarantee.
