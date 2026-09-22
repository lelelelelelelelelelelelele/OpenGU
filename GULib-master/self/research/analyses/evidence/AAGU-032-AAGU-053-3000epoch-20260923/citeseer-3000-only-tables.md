# CiteSeer: current 3000-epoch result tables

> Scope: generated only from the current AAGU-032 and AAGU-053 run manifests; previous-parameter result files were not read.
> Metric note: `utility.f1_after` / `f1_before` is computed by direct argmax accuracy in `experiments/unlearning_outputs.py`. Tables therefore label the endpoint test accuracy. Since these are single-label classification tasks, micro-F1 would numerically equal accuracy; macro-F1 is not present in these artifacts.

## AAGU-032 · Retrain test accuracy

Entries are mean ± sample SD over 3 training seeds; levels are percentages. AAGU-032 contains only full Retrain outcomes, so this table describes retained-task utility, not the behavior of GNNDelete or forgetting quality.

| Selector | 1% | 5% | 10% | 15% |
|---|---:|---:|---:|---:|
| gt_full | 75.53 ± 0.79 % | 75.98 ± 0.40 % | 74.82 ± 1.50 % | 73.97 ± 0.09 % |
| gt_full_all_trainable | 75.63 ± 0.53 % | 75.48 ± 0.57 % | 75.38 ± 0.60 % | 75.03 ± 0.23 % |
| degree | 74.87 ± 0.76 % | 75.18 ± 0.61 % | 75.03 ± 0.57 % | 75.43 ± 0.09 % |
| random | 75.08 ± 0.84 % | 74.77 ± 0.15 % | 74.77 ± 0.69 % | 74.52 ± 0.43 % |
| gt_simple | 75.08 ± 0.54 % | 75.93 ± 0.38 % | 75.23 ± 0.60 % | 75.03 ± 0.31 % |
| r_point | 75.48 ± 0.09 % | 75.28 ± 1.00 % | 74.92 ± 0.94 % | 73.92 ± 0.68 % |
| p_graph | 75.48 ± 0.76 % | 75.73 ± 0.71 % | 74.72 ± 1.13 % | 73.82 ± 0.23 % |
| p_point | 75.63 ± 0.61 % | 75.43 ± 0.76 % | 75.03 ± 0.95 % | 73.92 ± 0.17 % |
| gt_full_all_trainable_hops3 | 75.63 ± 0.53 % | 75.58 ± 0.23 % | 75.48 ± 0.57 % | 75.28 ± 0.23 % |
| gt_full_sgc_all_trainable_hops3 | 75.08 ± 0.90 % | 74.22 ± 0.87 % | 74.02 ± 0.79 % | 74.17 ± 0.54 % |

## AAGU-053 · GNNDelete and same-request Retrain

Each GU/Retrain comparison uses identical selected nodes. `n` is the number of selector requests (Degree: 1; other selectors: 3), with one training seed. Means ± sample SD describe variation across requests, not across independently trained models. Difference columns are percentage points.

| Selector | n | P0 test acc. (%) | GNNDelete (%) | Retrain (%) | P0−GU (pp) | P0−Retrain (pp) | Retrain−GU (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| degree | 1 | 74.47 % | 73.12 % | 74.62 % | 1.35 pp | -0.15 pp | 1.50 pp |
| random | 3 | 74.47 ± 0.00 % | 75.68 ± 0.30 % | 74.72 ± 0.71 % | -1.20 ± 0.30 pp | -0.25 ± 0.71 pp | -0.95 ± 0.83 pp |
| rr_1024 | 3 | 74.47 ± 0.00 % | 74.47 ± 0.45 % | 75.78 ± 0.88 % | -0.00 ± 0.45 pp | -1.30 ± 0.88 pp | 1.30 ± 0.92 pp |
| rr_4096 | 3 | 74.47 ± 0.00 % | 75.28 ± 0.76 % | 74.92 ± 0.69 % | -0.80 ± 0.76 pp | -0.45 ± 0.69 pp | -0.35 ± 1.44 pp |
| rr_16384 | 3 | 74.47 ± 0.00 % | 73.77 ± 0.57 % | 74.77 ± 0.52 % | 0.70 ± 0.57 pp | -0.30 ± 0.52 pp | 1.00 ± 0.09 pp |
| im_celf | 3 | 74.47 ± 0.00 % | 74.52 ± 1.52 % | 73.92 ± 0.31 % | -0.05 ± 1.52 pp | 0.55 ± 0.31 pp | -0.60 ± 1.83 pp |

Exact 48 paired requests: `AAGU-053-paired-GNNDelete-Retrain.csv`. Equal-request-weight dataset means, including the posterior-change membership AUC: `AAGU-053-dataset-summary.csv`. This AUC is an auxiliary update-detection measure, not a standalone privacy guarantee.
