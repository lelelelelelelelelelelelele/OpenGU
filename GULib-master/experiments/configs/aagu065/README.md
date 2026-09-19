# AAGU-065 Cora fixed-PT calibration

These two small experiments are calibration diagnostics only:

- `calibration_h16.yaml` consumes the fixed Cora/GCN hidden=16 pure PT and
  runs GIF/IDEA at the author pair and one shifted pair over 100/200/400
  iterations.
- `calibration_h64.yaml` does the same for hidden=64.

Both configs declare one independent Random request (seed `104245`) and 10%
of the persisted `train_mask`. Every GU instance names the explicit pure
`state_dict` PT produced by the 3000-epoch seed-42 checkpoint run. Because the
PT lane is external, the ordinary config parser intentionally reports the
training optimizer fields as not applicable; the calibration runner records
the fixed training contract and verifies the loaded PT/file hashes at runtime.

The author comparison is retained from `experiments/configs/aagu059/SOURCES.md`:
GIF uses scale `1000`, IDEA uses scale `500`, both with zero damping and
100/200/400 iterations. The shifted candidate is `scale=4096,damp=0.005`, so
the production target is `(H + 20.48 I) delta = v`; the runner reports both
this shifted residual and the original `(H delta - v)` residual. The candidate
is a calibration probe, not a promise of convergence or a Table parameter.

Run only from the SSH active checkout with the registered AAGU-065 runner;
local use is limited to parser dry-runs and review.

The H16 rework generation `calibration_h16_r1.yaml` is derived from the first
production HVP/Ritz measurement. It keeps the previous shifted target
`mu=20.48` and tests `(scale=8192,damp=0.0025)` and
`(scale=16384,damp=0.00125)` for both GIF and IDEA over 100/200/400
iterations. These are new calibration candidates, not frozen settings.
