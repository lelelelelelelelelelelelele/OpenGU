# Appendix A.5 — Deletion-Ratio Sweep

## Design

| Ratio | Config | Role |
|---|---|---|
| 0.01 | `A5_ratio_0.01.yaml` | low-budget regime — tests if vulnerability persists below main matrix |
| 0.05 | (already in `phase_b_cora_gcn.yaml`) | reuse main-matrix cells |
| 0.10 | `A5_ratio_0.10.yaml` | mid-budget |
| 0.20 | `A5_ratio_0.20.yaml` | high-budget — tests for knee / Shard Protection threshold |

Per ratio: 6 methods × 3 strategies (random, im, tracin) × 5 seeds = 90 cells.
Total new (r ∈ {0.01, 0.10, 0.20}): **270 cells**, ~3-5h on a single 4090.

Strategies skipped here:
- `degree`, `pagerank` — covered in main matrix at r=0.05; not needed for elasticity
- `hybrid` — A.3 covers the alpha dimension separately; A.5 is the r dimension

## Run order

```bash
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/A5_ratio_0.01.yaml
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/A5_ratio_0.10.yaml
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/A5_ratio_0.20.yaml
```

Run **after** `phase_b_cora_gcn.yaml` (main matrix) so the r=0.05 cells in cache are reusable for the elasticity plot.

## Output

Each ratio writes to `results/runs/cora_GCN_r{ratio}/{method}_{strategy}/seed{N}/{4 files}`.
Aggregator script (TBD): `scripts/plot_supp_figures.py::plot_ratio_elasticity` reads all four ratio cells and produces the per-family elasticity plot for §A.5.

## Caveats

- **r=0.20 may break methods**: GraphEraser at high deletion ratio can yield empty or imbalanced shards; sanity-check before queuing all 90 cells. Drop offending cells in the paper rather than hide.
- **GraphRevoker contingent**: see `SANITY_GRAPHREVOKER.md`; if it fails the gate, drop GraphRevoker from all three configs and report n=5 partition reverts to n=1.
