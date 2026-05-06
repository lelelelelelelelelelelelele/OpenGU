# §B NeurIPS Reproducibility Checklist

> Status: outline (fill once §1–§6 stable)
> Parent: §B
> Depends on: §1–§6 + final code release decision
> Updated: 2026-05-06

## Content

NeurIPS 2026 reproducibility checklist — mostly mechanical once paper stable. Existing scaffold: `overleaf/sec/B_checklist.tex` (86 lines).

## Items to confirm ahead of submission

- [ ] All claims in abstract/intro have evidence references in §5
- [ ] Code release statement (currently "upon acceptance" — confirm policy)
- [ ] Compute disclosure (4090 GPU-hours per Phase B config)
- [ ] Dataset license / source acknowledgement (Cora/Citeseer/ogbn-arxiv)
- [ ] No PII / responsible-use statement (covered by §6.4)
- [ ] Random seed disclosure (table of seeds in §4.3)
- [ ] Negative results disclosure: MEGU/IDEA null effect documented in §5 + §6.2
- [ ] **Appendix `app:hyperparams` 补完**：列出 6 个方法的 key hyperparameters（目前为 "To be expanded" placeholder，checklist #6 引用了它，不能是空的）
- [ ] **Appendix `app:impl`  interim 替换**：Phase B 跑完后把 GPU-hours、cell count 等所有 `\interim{}` 替换为最终数字（checklist #8 引用了 compute disclosure，不能留 placeholder）

## Cross-refs

- → all sections for traceability
