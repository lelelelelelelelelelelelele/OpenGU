# EXP-080 ratio response configuration

The original `response_ratios.yaml` and `response_ratios_gate.yaml` preserve the
first preparation and failed `e80g1` identities. Current execution uses the
`isolated_*.yaml` definitions. Work Plan owns live attempts and result acceptance.

Method, model, training, selector, split and evaluation parameters remain
unchanged. In particular, GraphEraser and GraphRevoker retain
`num_opt_samples: 1000`. Existing exact cache artifacts are eligible for ordinary
reuse; a new experiment ID or run ID does not force recomputation.

The original matrix contains 3087 unique conditions. The current executable
scope contains **3045 unique conditions**. Its 10 main Recipes declare 5208 rows,
including 2163 repeated explicit Retrain rows needed by independent paired
evaluation. These repeated rows may reuse exact existing Retrain and evaluation
artifacts; they are not extra independent baselines. Ten small gates declare
160 output rows, separately from the main scope.

## Independent failure scopes

- GIF, IDEA, MEGU and GNNDelete each have a separate full-range group, including
  the same-request Retrain baseline.
- Each sharded method has a separate group for ratios through 0.33 across the
  three datasets. Its 0.5 endpoint is isolated separately for CiteSeer and PubMed.
- Every group has a registered subset gate. Its main Recipe starts only after
  that gate's collection, SHA-256 verification and project acceptance succeed.
- A method-specific failure stops its Recipe and preserves its evidence;
  independent groups may continue. Within one Recipe the existing executor
  remains fail-fast. Shared version/device/lock failures and data/cache identity
  errors stop further submission. No failed job is automatically retried.

## Explicitly unavailable endpoint

**Cora, ratio 0.5, GraphEraser and GraphRevoker** are excluded under the original
1000-sample aggregation setting: fewer than 1000 training nodes remain. This
accounts for 42 GU conditions over all existing selector/training repetitions.
GraphEraser exposed the guard in `exp080-20261017-e80g1`; GraphRevoker contains
the same explicit feasibility guard but did not execute before that failure.

These points have status `not_run_parameter_infeasible`, not utility zero,
successful unlearning, or a measured failure score. Plots must show a gap or
mark the unavailable endpoint and explain the fixed aggregation constraint.
The absence alone does not establish that sharded unlearning is meaningless at
high deletion ratios. No 900-sample fallback is used.
