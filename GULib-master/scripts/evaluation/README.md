# Evaluation Tools

Unified Step0 evaluation tooling lives here.

## Entry point

```bash
python -m scripts.evaluation --help
```

## Commands

- `extract`: extract metrics from Step0 logs.
- `plot --type step0`: generate Step0 figures and derived artifacts.
- `plot --type attack`: generate attack effectiveness figures from data-driven JSON.
- `report`: generate Step0 markdown report.
- `all`: run extract + step0 plot/report (+ optional attack plot).

## Examples

```bash
python -m scripts.evaluation extract \
  --logs-dir results/step0_validation/round2_logs \
  --out-json results/evaluation/step0/all_metrics_detailed.json

python -m scripts.evaluation plot --type step0 \
  --input-json results/step0_validation/round2_results.json \
  --out-dir results/evaluation/step0/plots

python -m scripts.evaluation plot --type attack \
  --input-json results/evaluation/attack/attack_matrix.json \
  --out-dir results/evaluation/attack/plots
```

## Runners

New runner module entry points:

- `python -m scripts.evaluation.runners.run_round2`
- `python -m scripts.evaluation.runners.run_ratio05`
- `python -m scripts.evaluation.runners.run_cross_dataset_resume`

These runners now write outputs under `results/evaluation/step0`.
