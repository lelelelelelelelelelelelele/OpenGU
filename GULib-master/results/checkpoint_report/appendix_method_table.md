# Appendix: Method Compatibility & Vulnerability Details

> Data source: `results/step0_validation/method_compatibility.json`, `results/step0_validation/round2_results.json`
> Dataset: Cora | Backbone: GCN | Unlearn Task: Node | 77+ experiment runs

## A1. Method Compatibility Summary

| Method | Status | Pipeline Type | Max F1 Drop | Vulnerability Level |
|--------|--------|--------------|-------------|-------------------|
| GNNDelete | OK | Learning-based | 8.31% | **High** |
| Projector | OK | Learning-based | 5.90% | **High** |
| GraphEraser | OK | Shard-based | 2.40% | Moderate |
| GraphRevoker | OK | Shard-based | 2.40% | Moderate |
| GIF | OK | IF-based | 2.22% | Moderate |
| IDEA | OK | Learning-based | 2.03% | Moderate |
| MEGU | OK | Learning-based | 1.85% | Low |
| D2DGN | OK | Learning-based | 0.74% | Stable |
| SGU | OK | Learning-based | 0.55% | Stable |
| GUKD | OK | Learning-based | 0.37% | Stable |
| GUIDE | OK | IF-based | 0.00% | **Immune** |
| GST | FAIL | IF-based | - | N/A |
| CEU | FAIL | Learning-based | - | N/A |
| CGU | FAIL | Special (SGC only) | - | N/A |
| UTU | FAIL | Learning-based | - | N/A |

## A2. F1 Score by Unlearn Ratio (Successful Methods)

| Method | ratio=0.005 | ratio=0.02 | ratio=0.05 | ratio=0.1 | ratio=0.2 | Max Drop |
|--------|------------|-----------|-----------|----------|----------|----------|
| GNNDelete | 0.8303 | 0.7989 | 0.7934 | 0.8155 | 0.7472 | 0.0831 |
| Projector | 0.8616 | 0.8432 | 0.8487 | 0.8026 | SKIP | 0.0590 |
| GraphEraser | 0.8413 | 0.8487 | 0.8413 | 0.8358 | 0.8247 | 0.0240 |
| GraphRevoker | 0.8413 | 0.8487 | 0.8413 | 0.8358 | 0.8247 | 0.0240 |
| GIF | 0.8801 | 0.8801 | 0.8764 | 0.8745 | 0.8579 | 0.0222 |
| IDEA | 0.8653 | 0.8653 | 0.8653 | 0.8635 | 0.8450 | 0.0203 |
| MEGU | 0.8801 | 0.8782 | 0.8745 | 0.8745 | 0.8616 | 0.0185 |
| D2DGN | 0.8967 | 0.8967 | 0.8967 | 0.9004 | 0.8930 | 0.0074 |
| SGU | 0.8856 | 0.8856 | 0.8838 | 0.8893 | 0.8838 | 0.0055 |
| GUKD | 0.9022 | 0.9004 | 0.9022 | 0.9022 | 0.8985 | 0.0037 |
| GUIDE | 0.8303 | 0.8303 | 0.8303 | 0.8303 | 0.8303 | 0.0000 |

## A3. Unlearning Time by Ratio (seconds)

| Method | ratio=0.005 | ratio=0.02 | ratio=0.05 | ratio=0.1 | ratio=0.2 |
|--------|------------|-----------|-----------|----------|----------|
| GraphRevoker | 8.38 | 10.22 | 9.96 | 10.61 | 9.62 |
| GraphEraser | 7.05 | 9.50 | 9.21 | 8.56 | 9.53 |
| GUIDE | 5.92 | 8.76 | 7.52 | 8.27 | 7.20 |
| Projector | 1.96 | 1.90 | 2.18 | 1.90 | - |
| GNNDelete | 0.65 | 1.00 | 0.78 | 0.69 | 0.85 |
| D2DGN | 0.76 | 0.78 | 0.70 | 0.64 | 0.65 |
| SGU | 0.64 | 0.64 | 0.62 | 0.64 | 0.64 |
| GUKD | 0.48 | 0.50 | 0.48 | 0.49 | 0.49 |
| GIF | 0.39 | 0.41 | 0.37 | 0.39 | 0.40 |
| MEGU | 0.40 | 0.36 | 0.35 | 0.39 | 0.34 |
| IDEA | 0.46 | 0.49 | 0.47 | 0.44 | 0.44 |

## A4. Failed Methods - Error Details

| Method | Error | Root Cause |
|--------|-------|-----------|
| GST | `forward() got unexpected keyword argument 'use_batch'` | API incompatibility with GCN backbone |
| CEU | `'dict' has no attribute 'num_features'` | Data format mismatch |
| CGU | Only supports SGC backbone | Architecture constraint |
| UTU | `UTUTrainer not registered` | Trainer mapping missing |
