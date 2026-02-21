# Round 2: Deep Validation Results

**Date**: 2026-02-22
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
| Projector | Standalone | 0.8616 | 0.8432 | 0.8487 | 0.8026 | SKIP | 0.0590 |
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

## Plots

See `plots/` directory for generated figures.