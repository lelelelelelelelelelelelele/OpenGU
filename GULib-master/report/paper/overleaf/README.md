# Overleaf submission package — NeurIPS 2025/2026

> Created 2026-05-04. NeurIPS 2026 `.sty` file is not yet released as of this
> date; the 2025 `.sty` is shipped here. When 2026 official files appear,
> drop them into this directory and update `\usepackage{neurips_2025}` →
> `\usepackage{neurips_2026}` in `main.tex`. Macros are stable year-over-year.

## Files

```
overleaf/
├── main.tex                  # entry point
├── neurips_2025.sty          # NeurIPS style (replace with 2026 when out)
├── references.bib            # citation skeleton
├── README.md                 # this file
├── sec/
│   ├── 0_abstract.tex
│   ├── 1_intro.tex
│   ├── 2_related_work.tex
│   ├── 3_method.tex
│   ├── 4_experiment.tex
│   ├── 5_results.tex
│   ├── 6_conclusion.tex
│   ├── A_appendix.tex
│   └── B_checklist.tex       # NeurIPS-mandatory checklist
└── figures/
    ├── FIG-1_Generalization.pdf
    ├── FIG-2_Scaling.pdf
    ├── FIG-3_Spectrum.pdf
    ├── FIG-4a_Significance.pdf
    └── FIG-4b_Effect.pdf
```

## How to upload to Overleaf

1. Zip this entire directory:
   ```powershell
   cd H:\project\OpenGU\GULib-master\report\paper
   Compress-Archive -Path overleaf\* -DestinationPath overleaf_v0.zip -Force
   ```
2. Overleaf → **New Project** → **Upload Project** → drop in `overleaf_v0.zip`.
3. Set the main document to `main.tex` (Menu → Settings → Main document).
4. Compile. Should produce a 9-page paper plus appendix and checklist.

## Phase B refresh (after server data lands)

All numbers that need refreshing are wrapped in `\interim{...}` and render in
red bold. Find them:

```bash
grep -rn '\\interim' sec/
```

Replace each `\interim{...}` with the final number. The `\interim` macro
itself stays defined so you can re-mark new placeholders if needed.

The five existing figure PDFs in `figures/` were generated from pre-Phase-B
data. After Phase B:
1. Re-run `scripts/evaluation/generate_figures.py` from the repo root to
   regenerate the 5 PDFs from `results/runs/`.
2. Drop the new PDFs into `figures/` (overwrite).
3. Re-zip and re-upload to Overleaf, or sync via Overleaf's Git integration.

## Section ↔ data binding (for Phase B refresh)

| Section | Numbers to refresh | Source after Phase B |
|---|---|---|
| Abstract (`0_abstract.tex`) | F1 collapse %, paired effect, $p$-value, Shard Protection % | aggregate `results/runs/cora_GCN_r0.05/*/seed*/attack.json` |
| **Table 1 Panel A** (`5_results.tex`) | 30 cells × 6 metrics on cora/GCN | `results/runs/cora_GCN_r0.05/{method}_{strategy}/seed*/attack.json` + `collateral.json` |
| **Table 1 Panel B** | 12 cells × 6 metrics on ogbn-arxiv | `results/runs/ogbn-arxiv_GCN_r0.05/{method}_{strategy}/seed*/*.json` |
| Results §5.2 GNNDelete narrative | mean F1 drop, CI | `results/runs/cora_GCN_r0.05/GNNDelete_im/seed*/attack.json` |
| Results §5.3 GIF narrative | TracIn paired effect | `results/runs/cora_GCN_r0.05/GIF_tracin/seed*/attack.json` |
| Results §5.4 Shard narrative | F1 gain ranges | `results/runs/cora_GCN_r0.05/GraphEraser_*/seed*/attack.json` |
| Results §5.6 Significance | $p$-value matrix, Jaccard note | recompute from per-seed effects |
| Results §5.6 Retrain gap, Hop decay | per-method gap, decay buckets | `results/runs/*/collateral.json` |
| Appendix A.1 | speedup multiplier | `experiments/im_benchmark/results/bench_results.json` |
| Appendix Table A.1 | cora/GAT 30-row master table | `results/runs/cora_GAT_r0.05/*/seed*/*.json` |
| Appendix Table A.2 | full 5-seed raw expansion | aggregate over all seeds |

## Open issues to address before submission

- [ ] `\interim{...}` placeholders all replaced with Phase B numbers (~25 spots)
- [ ] FIG-3 (Spectrum), FIG-4a/b (Significance) regenerated with Phase B data
- [ ] FIG-1 (Generalization) updated to N=5 with error bars (currently single-seed)
- [ ] Hop-decay figure added to §5.6 (or deferred to Appendix A.2)
- [ ] References: replace skeleton entries with real arXiv/conference BibTeX
- [ ] Author block in `main.tex`: fill in once de-anonymization allowed
- [ ] §5.5 MEGU/IDEA framing: confirm "mechanism-incomparable" framing with
      Phase B numbers; if Phase B reveals non-zero effect, reframe as
      "small-but-real" instead of "null"
- [ ] Appendix B (NeurIPS Checklist): re-confirm each Yes/No once final
      results land — particularly Q7 (statistical significance) and
      Q8 (compute resources)
