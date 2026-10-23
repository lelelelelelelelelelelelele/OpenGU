# EXP-014 · ogbn-arxiv selector timing

The question is whether the existing selectors can generate valid deletion
requests on ogbn-arxiv within practical time and memory limits. This preparation
contains five independent, single-condition selector submissions. It does not
run GU, Retrain, downstream utility evaluation, or a multi-seed effect study.

| Selector | Configuration | Recipe ID | Run ID |
| --- | --- | --- | --- |
| Random | `random.yaml` | `exp014-random-r1` | `e14r1` |
| Degree | `degree.yaml` | `exp014-degree-r1` | `e14r2` |
| R-point | `r-point.yaml` | `exp014-r-point-r1` | `e14r3` |
| IM-RR, 65536 sets | `rr65536.yaml` | `exp014-rr65536-r1` | `e14r4` |
| D-full (`gt_full`) | `d-full.yaml` | `exp014-d-full-r1` | `e14r5` |

Each configuration binds the existing `datasets/ogbn-arxiv.yaml` random
70/10/20 split (split seed 2024), the training-node candidate pool and a 5%
deletion budget. This is not the OGB official time split. Dataset counts must
come from `recipe.py generate --node gpu4090`, which validates the persisted
manifest, graph and masks. They are not copied from a historical Recipe.

R-point and D-full use the shared selector definitions: two-layer GCN, hidden
width 64, dropout 0.5, 3000 training epochs, training seed 42. Their other
parameters remain owned by the existing definitions and resolved dry-run.
Random and IM use sampling seed 11. Degree, Random and IM do not declare an
unused model training seed. IM uses propagation probability 0.1 and RR-65536,
matching that setting in the small-graph main table. The historical RR-1024
result is background evidence, not evidence that RR-65536 will finish.

These five selectors are the initial scope. PageRank, other RR counts,
trajectory selectors and surrogate variants are not measured by these Recipes;
the result must not be described as covering every project selector.

## Timing and acceptance

Use `run.json` cell `timing.current_access.wall_seconds` for the current
selector entry, including necessary model preparation and Selection validation.
Its exclusive `model_prepare` and `selector_access` phases separate model
preparation from the remaining selection path. `score_access_seconds` and
`selection_seconds` are access-path observations, not guaranteed pure kernel
compute times; do not add them again to the enclosing wall time. Dataset load,
startup, export and report generation are outside the selector-entry wall;
Runner start-to-finish time is the separate whole-job measure.

Each Recipe uses its own process so an earlier selector cannot share an in-memory
model with a later selector or prevent its result from being exported. Persistent
checkpoint, Score and Selection caches still work normally. Inspect all relevant
cache states and `producer_called` fields before classifying a measurement:

- Cold end-to-end selector evidence needs actual required model preparation and
  actual Score/Selection production. Topology selectors need no checkpoint.
- A checkpoint hit with Score/Selection misses measures selection with a prepared
  model; it is not a cold training-inclusive measurement.
- Score/Selection hits measure reuse. A new run ID does not force recomputation.

Do not delete caches, change scientific seeds to manufacture misses, or substitute
historical producer time for current access time. If cold measurements are missing,
report the gap and agree a supported measurement procedure before further runs.

The current selector result contract does not automatically report per-selector
peak host memory or GPU memory, or enforce a per-selector memory ceiling. These
Recipes alone therefore answer time and output-validity questions, not the full
peak-memory question. Mark unobserved memory as unavailable. Additional resource
observation, if required, must be established before execution.

Each declaration has a 21600-second (six-hour) whole-job timeout. It is a safety
cap, not a completion estimate, and five caps total at most 30 job-hours before
allowing for termination overhead. There is no automatic batch submission or
retry. Before any GPU launch, record an evidence-based all-MISS serial estimate
for the agreed full scope in Work Plan, check the required gate, synchronize the
reviewed version and pass formal preflight. This preparation does not launch jobs.

Successful execution still requires trusted collection and validation of the
selected node count, uniqueness, candidate membership and exact input/artifact
identity. OOM, timeout, failure and not-run are distinct outcomes. No attack
effectiveness claim follows from a successful selector run.

Live preparation, estimates, attempts and evidence references belong to
`self/research/experiments/EXP-014.json`; this document does not duplicate run state.
