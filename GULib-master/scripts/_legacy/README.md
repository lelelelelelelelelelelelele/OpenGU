# Legacy plotting scripts

Archived 2026-05-07. Kept for audit / git-blame trail; **do not run on a fresh checkout**.

| File | Status | Why retired |
|---|---|---|
| `plot_paper_figures.py` | STALE (pre-Phase-B) | Reads `results/relative/` which was gitignored 2026-05-05 as bug-polluted. Self-aborts unless `ALLOW_LEGACY_PLOT=1`. |
| `plot_phase_b_cora.py` | functional but wrong filenames | Outputs `fig1_f1_drop.pdf` etc. into `results/paper_figures/`; the paper expects `FIG-1_Generalization.pdf` etc. under `report/paper/overleaf/figures/`. Last useful when there were only 2 cells. |

**Active replacement**: `scripts/plot_neurips_figures.py` (top-level `scripts/`) generates all 6 paper figures (FIG-1 / FIG-2 / FIG-3 / FIG-4a / FIG-4b / FIG-5) directly into the Overleaf figures dir from `results/_phase_b_aggregate.csv`.
