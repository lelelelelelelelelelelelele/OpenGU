# Evaluation Outputs

This directory stores generated artifacts only.

## Layout

- `step0/`: Step0 outputs (logs, JSON summaries, plots, markdown reports).
- `attack/`: attack chart input/output.
- `stats/`: 聚合统计 CSV（`final_paper_stats.csv` 等，由 `scripts/evaluation/final_data_aggregator.py` 生成）。

## Note

All executable tooling has been moved to `scripts/evaluation`.
`results/step0_validation` is now treated as legacy read-only historical data.
