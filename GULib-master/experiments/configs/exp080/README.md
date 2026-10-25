# EXP-080 ratio response configuration

## Complete tables including ETR

Add ETR directly to each existing `cc_*.yaml` main table and its gate. Each
submission retains all applicable GU methods and explicit same-request Retrain;
exact matching Score, Selection, Output and Evaluation artifacts are reused by
the ordinary cache lookup. An added method does not require a separate scientific
table or joining method-specific exports. The unsubmitted ETR-only ratio tables
and Recipes have been retired; their frozen preparation remains in Git history.

The complete main scope is 2310 rows: base2016, Cora50%126, CiteSeer50%168.
Their gates have32,6,8 rows. ETR adds294 scientific conditions; the existing
Retrain rows appear once per condition. Training seeds, selectors, IM draws,
budgets, profiles and evaluation definitions are unchanged for existing methods.

The three existing rectangles remain necessary: Cora50% excludes GraphEraser
and GraphRevoker under the fixed1000-sample aggregation constraint. ETR is
included there. PubMed remains deferred. Every run uses a fresh run ID and a
complete reviewed declaration; historical results and scientific decisions are
preserved. Work Plan owns the current queue order, budgets and execution facts.

The current prepared scope is **Cora + CiteSeer**. PubMed is deferred. The
`cc_*.yaml` definitions replace the previous ten-group submission plan; Work Plan
owns live attempts and result acceptance. Preparing these declarations does not
submit a run.

Method, model, training, selector, split and evaluation parameters remain
unchanged. In particular, GraphEraser and GraphRevoker retain
`num_opt_samples: 1000`. Existing exact cache artifacts are eligible for ordinary
reuse; a new experiment ID or run ID does not force recomputation.

Before ETR, the original matrix contained3087 unique conditions and the retained
Cora/CiteSeer scope contained2016 main rows. The complete current scope contains
**2310 unique main output rows**, with no duplicated Retrain rows across the
three main tables. PubMed remains deferred, and the same42 infeasible Cora
sharded endpoints remain excluded. Seeds, selectors, deletion ratios and all
evaluation definitions are unchanged for the existing methods.

## Current submission declarations

| Main Recipe | Dataset | Deletion ratios | GU methods plus explicit Retrain | Main rows | Gate rows | New run IDs (gate / main) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `exp080-cc-base-r4` | Cora, CiteSeer | 5%, 7.5%, 10%, 15%, 22%, 33% | All seven GU methods | 2016 | 32 | `e80g401` / `e80r401` |
| `exp080-cc-cora-high-r4` | Cora | 50% | GIF, IDEA, MEGU, GNNDelete, ETR | 126 | 6 | `e80g402` / `e80r402` |
| `exp080-cc-citeseer-high-r4` | CiteSeer | 50% | All seven GU methods | 168 | 8 | `e80g403` / `e80r403` |

The existing configuration interface represents Cartesian products and has no
per-condition exclusions. These three rectangles preserve every feasible
Cora/CiteSeer condition without changing the 1000-sample aggregation setting.
They are not separate per-method or per-seed experiments.

Each main declaration has a `-g4` gate Recipe using Degree and training seed 42;
the base gate checks 5% and 33%, and the two endpoint gates check 50%. The gates
contain46 rows in total and are exact subsets of their main tables. A main run
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
