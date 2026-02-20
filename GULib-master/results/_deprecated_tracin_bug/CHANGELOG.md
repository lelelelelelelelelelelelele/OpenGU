# TracIn Bug Deprecation Log

**Date**: 2026-02-21
**Fix commit**: 55c8971 (seed 2024)

## Bug Description

TracIn strategy had a node ID mapping bug: `topk_indices` were indices into the `candidates` array, but were returned directly instead of mapping back to actual node IDs via `candidates[topk_indices]`. This caused all tracin experiments to select wrong nodes, producing unreliable results (some showing negative f1_drop).

## Impact Scope

- All tracin experiment results prior to commit 55c8971 are invalid
- Other strategies (random, degree, pagerank, im, hybrid) are unaffected

## Moved Files

### collateral/ (6 files - all contain tracin strategy results)
- `GIF/cora/GCN/collateral_20260219_230539.json`
- `GNNDelete/cora/GCN/collateral_20260219_230458.json`
- `GraphEraser/cora/GCN/collateral_20260219_231324.json`
- `GraphEraser/cora/GCN/collateral_20260220_005032.json`
- `GUIDE/cora/GCN/collateral_20260220_082118.json`
- `GUIDE/cora/GCN/collateral_20260220_083132.json`

### mg0_completion/ (2 files)
- `phase_a/20260221_021359_seed42/GIF_cora_GCN_r0.05_s42.json`
- `phase_a/20260221_021359_seed42/GNNDelete_cora_GCN_r0.05_s42.json`

### demo_logs/ (4 files)
- `2026-02-18_cora_GCN_GNNDelete.log`
- `2026-02-19_6strategies_cora_GCN_GIF.log`
- `2026-02-19_6strategies_cora_GCN_GNNDelete.log`
- `2026-02-19_6strategies_cora_GCN_GraphEraser.log`

## Additionally Cleaned (Step 1)

- 21 tracin cache entries deleted from `results/cache/` (not moved, just deleted)
