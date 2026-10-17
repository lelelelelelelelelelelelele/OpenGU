# EXP-080 ratio response configuration

The current prepared scope is **Cora + CiteSeer**. PubMed is deferred. The
`cc_*.yaml` definitions replace the previous ten-group submission plan; Work Plan
owns live attempts and result acceptance. Preparing these declarations does not
submit a run.

Method, model, training, selector, split and evaluation parameters remain
unchanged. In particular, GraphEraser and GraphRevoker retain
`num_opt_samples: 1000`. Existing exact cache artifacts are eligible for ordinary
reuse; a new experiment ID or run ID does not force recomputation.

The original matrix contains 3087 unique conditions. The current scope contains
**2016 unique main output rows**, with no duplicated Retrain rows across the
three main tables. It defers 1029 PubMed rows and excludes the same 42 infeasible
Cora endpoint rows described below. Seeds, selectors, deletion ratios and all
evaluation definitions are unchanged within the retained conditions.

## Current submission declarations

| Main Recipe | Dataset | Deletion ratios | GU methods plus explicit Retrain | Main rows | Gate rows | New run IDs (gate / main) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `exp080-cc-base` | Cora, CiteSeer | 5%, 7.5%, 10%, 15%, 22%, 33% | All six GU methods | 1764 | 28 | `e80g301` / `e80r301` |
| `exp080-cc-cora-high` | Cora | 50% | GIF, IDEA, MEGU, GNNDelete | 105 | 5 | `e80g302` / `e80r302` |
| `exp080-cc-citeseer-high` | CiteSeer | 50% | All six GU methods | 147 | 7 | `e80g303` / `e80r303` |

The existing configuration interface represents Cartesian products and has no
per-condition exclusions. These three rectangles preserve every feasible
Cora/CiteSeer condition without changing the 1000-sample aggregation setting.
They are not separate per-method or per-seed experiments.

Each main declaration has a `-gate` Recipe using Degree and training seed 42;
the base gate checks 5% and 33%, and the two endpoint gates check 50%. The gates
contain 40 rows in total and are exact subsets of their main tables. A main run
requires its gate's trusted collection and project acceptance, or an explicitly
verified equivalent existing gate. Gates are prerequisite checks, not additional
independent research samples.

The unchanged executor is fail-fast within a table. On failure, preserve the
evidence and inspect the cause; do not automatically retry or split further.
The main timeout remains 21600 seconds and the gate timeout 7200 seconds. These
are execution caps, not completion estimates. Formal runtime and HIT counts for
these new run IDs are not yet observed.

## Cache and historical evidence

Dataset/Split bindings and fingerprints, effective selectors, method/model/
training parameters, and evaluation definitions are checked against the original
matrix for every retained row. This revision changes no producer implementation,
formula, dependency version or cache policy. Recipe configuration fingerprints
change to bind the smaller tables; those are distinct from computational cache
identities. Exact existing artifacts remain eligible for normal reuse; missing
or mismatched entries still MISS or fail closed under the existing rules.

The original `response_ratios*.yaml` and the submitted GIF/IDEA/MEGU
`isolated_*.yaml` declarations retain their historical identities. Never-submitted
GNNDelete and sharded declarations are retired from the active Recipe directory;
their prior versions remain in Git history. Existing run IDs, returned results,
timeout evidence and Cache V2 artifacts are preserved. PubMed's existing results
are retained even though it is outside the current prepared scope.

Preparation evidence is maintained by Work Plan under
`.syncmate/exp080-two-datasets-20261018/`, including the exact matrix comparison,
dry-runs, official Recipe generation receipts and submission previews. Formal
execution still requires one synchronized source version and registered
preflight, including the post-timeout ScoreBundle lock check.

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
