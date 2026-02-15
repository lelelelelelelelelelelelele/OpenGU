# Round 1: Breadth Scan Results

**Date**: 2026-02-16
**Config**: GCN × Cora × 270 unlearn nodes × 100 epochs × 1 run
**Command template**: `python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods {METHOD} --unlearn_task node --downstream_task node --num_epochs 100 --num_runs 1`

## Results Table

| # | Method | Status | F1 After | Unlearn Time (s) | AUC | Notes |
|---|--------|--------|----------|-------------------|-----|-------|
| 1 | GraphEraser | ✅ | 0.8432 | 10.61 | 0.0000 | Shard-based, partition 2.94s |
| 2 | GIF | ✅ | 0.8708 | 0.42 | 0.6157 | Fast, IF-based |
| 3 | GUIDE | ✅ | 0.8303 | 8.38 | 0.9853 | Shard-based, high AUC |
| 4 | GST | ❌ | - | - | - | `TypeError: forward() got unexpected keyword argument 'use_batch'` |
| 5 | GNNDelete | ✅ | 0.8229 | 0.90 | 0.6052 | Learning-based deletion weights |
| 6 | CEU | ❌ | - | - | - | `AttributeError: 'dict' has no attribute 'num_features'` (data preprocessing returns dict) |
| 7 | CGU | ❌ | - | - | - | `AssertionError: assert base_model == 'SGC'` (only supports SGC backbone) |
| 8 | SGU | ✅ | 0.8838 | 0.77 | 0.0000 | Learning-based, retains performance well |
| 9 | MEGU | ✅ | 0.8745 | 0.38 | 0.0000 | Fast unlearning |
| 10 | UTU | ❌ | - | - | - | `KeyError: 'UTUTrainer'` (trainer not registered in task/__init__.py) |
| 11 | GUKD | ✅ | 0.9022 | 0.59 | 0.0000 | Knowledge distillation, best F1 |
| 12 | D2DGN | ✅ | 0.9004 | 0.83 | 0.0000 | Second best F1 |
| 13 | IDEA | ✅ | 0.8561 | 0.60 | 0.5188 | IF-based |
| 14 | Projector | ✅ | 0.8395 | 2.48 | 0.0000 | Runs on CPU, slow training (~2min) |
| 15 | GraphRevoker | ✅ | 0.8432 | 12.38 | 0.0000 | Shard-based, partition 4.10s |

## Summary

- **✅ Passed**: 11/15 methods (GraphEraser, GIF, GUIDE, GNNDelete, SGU, MEGU, GUKD, D2DGN, IDEA, Projector, GraphRevoker)
- **❌ Failed**: 4/15 methods (GST, CEU, CGU, UTU)
- **Critical methods for attack research**: GIF ✅, GUIDE ✅, GST ❌

## Error Analysis

| Method | Error Type | Root Cause | Fixable? |
|--------|-----------|------------|----------|
| GST | TypeError | Scattering transform `forward()` API changed, `use_batch` kwarg removed | Needs code fix in `GSTTrainer.py:192` |
| CEU | AttributeError | `ceu_process()` returns dict instead of PyG Data; pipeline expects Data object | Needs code fix in `dataset_utils.py` or `IF_based_pipeline.py` |
| CGU | AssertionError | Hardcoded `assert base_model == 'SGC'` — by design only supports SGC | Not a bug; CGU only works with linear GNN |
| UTU | KeyError | `UTUTrainer` not registered in `task/__init__.py::trainer_mapping` | Needs registration fix |

## Key Observations

1. **F1 range**: 0.8229 (GNNDelete) to 0.9022 (GUKD) — all ✅ methods maintain reasonable performance
2. **Speed**: MEGU (0.38s) and GIF (0.42s) are the fastest; GraphRevoker (12.38s) and GraphEraser (10.61s) are slowest
3. **Projector runs on CPU** despite `--cuda 0`, training takes ~2 minutes (slow but functional)
4. **AUC reported as 0.0000 for most methods** — only GIF (0.6157), GUIDE (0.9853), GNNDelete (0.6052), IDEA (0.5188) report MIA AUC
5. **GUKD and D2DGN achieve highest F1** (>0.90), suggesting strong model utility preservation
