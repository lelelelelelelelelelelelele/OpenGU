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

The H16 rework generation `calibration_h16_r2.yaml` uses the measured
`lambda_min=-2.492925` and `lambda_max=13919.159832` to reduce the spectral
radius of the shifted Richardson recurrence. It tests `(scale=9000,
damp=0.22755555555555556)` (`mu=2048`) and `(scale=15000,
damp=0.5461333333333334)` (`mu=8192`) for both GIF and IDEA over 100/200/400
iterations. These are stability/convergence candidates, not F1-selected
production parameters.

The H16 r3 generation `calibration_h16_r3_random.yaml` fixes the preferred
r2 pair `(scale=9000,damp=0.22755555555555556)` (`mu=2048`) and varies only
the Random selector seed across `104245`, `104246`, and `104247`. It runs both
GIF and IDEA at 100/200/400 iterations to test request-to-request stability;
it does not retune parameters by seed or by F1.
