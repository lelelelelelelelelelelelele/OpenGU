# Round 2: Deep Validation Results

**Date**: 2026-02-16
**Config**: GCN x Cora x 5 unlearn ratios x 100 epochs x 1 run

## F1 Score by Method and Unlearn Ratio

| Method | Category | r=0.005 (~13n) | r=0.02 (~54n) | r=0.05 (~135n) | r=0.1 (~270n) | r=0.2 (~541n) | F1 Drop |
|--------|----------|----------------|---------------|----------------|---------------|---------------|---------|
| D2DGN | Learning-based | 0.8967 | 0.8967 | 0.8967 | 0.9004 | 0.8930 | 0.0037 |
| GIF | IF-based | 0.8801 | 0.8801 | 0.8764 | 0.8745 | 0.8579 | 0.0222 |
| GNNDelete | Learning-based | 0.8303 | 0.7989 | 0.7934 | 0.8155 | 0.7472 | 0.0831 |
| GUIDE | Shard-based | 0.8303 | 0.8303 | 0.8303 | 0.8303 | 0.8303 | 0.0000 |
| GUKD | Learning-based | 0.9022 | 0.9004 | 0.9022 | 0.9022 | 0.8985 | 0.0037 |
| GraphEraser | Shard-based | 0.8413 | 0.8487 | 0.8413 | 0.8358 | 0.8247 | 0.0166 |
| GraphRevoker | Shard-based | 0.8413 | 0.8487 | 0.8413 | 0.8358 | 0.8247 | 0.0166 |
| IDEA | IF-based | 0.8653 | 0.8653 | 0.8653 | 0.8635 | 0.8450 | 0.0203 |
| MEGU | Learning-based | 0.8801 | 0.8782 | 0.8745 | 0.8745 | 0.8616 | 0.0185 |
| Projector | Learning-based | 0.8616 | 0.8432 | 0.8487 | 0.8026 | SKIP | 0.0590 |
| SGU | Learning-based | 0.8856 | 0.8856 | 0.8838 | 0.8893 | 0.8838 | 0.0018 |

## Unlearning Time by Method and Unlearn Ratio

| Method | r=0.005 | r=0.02 | r=0.05 | r=0.1 | r=0.2 |
|--------|---------|--------|--------|-------|-------|
| D2DGN | 0.76s | 0.78s | 0.70s | 0.64s | 0.65s |
| GIF | 0.39s | 0.41s | 0.37s | 0.39s | 0.40s |
| GNNDelete | 0.65s | 1.00s | 0.78s | 0.69s | 0.85s |
| GUIDE | 5.92s | 8.76s | 7.52s | 8.27s | 7.20s |
| GUKD | 0.48s | 0.50s | 0.48s | 0.49s | 0.49s |
| GraphEraser | 7.05s | 9.50s | 9.21s | 8.56s | 9.53s |
| GraphRevoker | 8.38s | 10.22s | 9.96s | 10.61s | 9.62s |
| IDEA | 0.46s | 0.49s | 0.47s | 0.44s | 0.44s |
| MEGU | 0.40s | 0.36s | 0.35s | 0.39s | 0.34s |
| Projector | 1.96s | 1.90s | 2.18s | 1.90s | - |
| SGU | 0.64s | 0.64s | 0.62s | 0.64s | 0.64s |

## Key Findings

### Most Vulnerable Methods (highest F1 drop):
1. **GNNDelete**: F1 drop = 0.0831 (8.3%)
2. **Projector**: F1 drop = 0.0590 (5.9%)
3. **GIF**: F1 drop = 0.0222 (2.2%)
4. **IDEA**: F1 drop = 0.0203 (2.0%)
5. **MEGU**: F1 drop = 0.0185 (1.8%)
6. **GraphEraser**: F1 drop = 0.0166 (1.7%)
7. **GraphRevoker**: F1 drop = 0.0166 (1.7%)
8. **GUKD**: F1 drop = 0.0037 (0.4%)
9. **D2DGN**: F1 drop = 0.0037 (0.4%)
10. **SGU**: F1 drop = 0.0018 (0.2%)
11. **GUIDE**: F1 drop = 0.0000 (0.0%)

### Most Robust Methods (lowest F1 drop):
- **GUIDE**: F1 drop = 0.0000
- **SGU**: F1 drop = 0.0018
- **D2DGN**: F1 drop = 0.0037

### GUIDE Anomaly
GUIDE shows identical F1 (0.8303) across all ratios. This suggests it may be re-training
sub-models from scratch rather than performing incremental unlearning, making it inherently
robust but also meaning the unlearning mechanism is effectively a full retrain.


## Implications for Attack Research

1. **GNNDelete** is the most promising attack target (10.0% F1 drop at r=0.2)
2. **GIF** and **MEGU** show moderate vulnerability (~2-3% drop)
3. **GUIDE**, **SGU**, **GUKD**, **D2DGN** are robust to random node removal
4. Attack strategies (TracIn/IM/Hybrid) may amplify these drops by selecting critical nodes

## Plots

See `plots/` directory for:
- `round1_overview.png`: All 15 methods bar chart
- `all_methods_combined.png`: F1 vs unlearn size for all methods
- `vulnerability_ranking.png`: Methods ranked by F1 drop
- `{Method}_f1_curve.png`: Individual method F1 curves
- `category_comparison.png`: Average vulnerability by method category
- `time_vs_ratio.png`: Unlearning time scaling