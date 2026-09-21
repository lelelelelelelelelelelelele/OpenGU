# AAGU-052: table01 GIF configuration repair

This is the same AAGU-011 table and gate condition matrix. Only the local GIF
instance changes: 2000 iterations, scale 65536, damp 0.00390625. All other
instances resolve to the existing public configurations. Historical AAGU-011
YAML and outputs are preserved.

Nine existing checkpoints (three datasets, seeds 42/212/2024) had observed
extreme Hessian Ritz values spanning approximately -108.502 to 42529.358.
A predeclared 1.25 margin, rounded up to powers of two, gives shift 256 and
scale 65536. These are empirical spectral estimates, not certified bounds.
The implemented GIF target is explicitly (H + 256 I) delta = v.

On the three seed42 Random inputs, matched relative residuals after 2000
steps were 0.000114/0.000061/0.000231. Doubling the budget to 4000 changed
delta by only 0.027%/0.019%/0.072%. The selection rule was residual <=0.001
and relative delta change <=1%; no test metric or Retrain gap selected the
configuration. This does not certify the undamped equation or forgetting.

Canonical evidence and current execution state belong to
`.workblock/items/AAGU-052/WORKITEM.md` and its `evidence/rework-20260911/`.
New run IDs: aagu052-gif-gate-v1, aagu011-table01-v3.
