# EXP-014 frozen table input

`SUMMARY.json` is the byte-identical input used by cost candidate `6834a719`:
SHA-256 `9740692d1a306849a10cb1a32b963bfec00e311a5b2f5a98bcbd773eafd0dd76`.
It is copied from the canonical EXP-014 record, not a new analysis or scientific decision.

Run `python -X utf8 report/paper/appendix/exp014-selector-cost-20261025/build.py`
to regenerate only `overleaf/sections/selector_cost_rows.tex`.
The narrative, caption, footnote, and timing boundaries are author-owned in
`overleaf/sections/selector_cost.tex`; the generator never writes them.

RR=65,536 timed out after two hours. Its 6–8 hour completion time is an estimate,
not an observed completion. These data concern request generation only.
