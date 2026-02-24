# IM_V4 Migration Note (MG0-MG3 + Ratio)

## Scope

This migration applies to:

- `scripts/experiments/run_mg0_completion.sh`
- `scripts/experiments/run_mg1_citeseer.sh`
- `scripts/experiments/run_mg2_gat.sh`
- `scripts/experiments/run_mg3_extended.sh`
- `scripts/experiments/run_ratio_sensitivity.sh`

## Strategy Mapping

| Before | After |
|---|---|
| `im` | `im_v4` |
| `hybrid` | `hybrid_v4` |

Default strategy sets are now switched to IM_V4 line in MG0-MG3 and Ratio scripts.

## Data Retention

- Historical outputs are kept as-is.
- No existing result file or directory is deleted by this migration.
- Output base directories remain unchanged (for example, `results/experiments/mg0_completion`, `results/experiments/ratio_sensitivity`).

## Running Recommendation (Same Output Base)

Because output base paths remain unchanged:

1. Run one normal (non-repair) round first to create new timestamped run folders with IM_V4 strategies.
2. Then run repair only on the new run folders when needed.

## Repair Risk and Mitigation

### Risk

Normal runs do not overwrite old runs (`run_experiments.py` writes timestamped `*_seed*` run directories).  
But repair under the same output base may still target historical run folders that were created with old strategy config.

### Mitigation

- Preferred: run a new non-repair round first, then repair that new run.
- Or: pass `--repair_dir` explicitly to the new migrated run directory.

## Ratio Script Compatibility

`run_ratio_sensitivity.sh` now uses IM_V4 profile by default.  
`--use_im_v4` is kept as a compatibility no-op alias (it does not change output path or strategy set anymore).
