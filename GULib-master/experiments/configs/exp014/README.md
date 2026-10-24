# EXP-014 · ogbn-arxiv selector timing

The question is whether the existing selectors can generate valid deletion
requests on ogbn-arxiv within practical time and memory limits. This preparation
initially contained four submissions covering five selector conditions. Random and Degree
share a two-condition job; the other selectors retain independent jobs. It does not
run GU, Retrain, downstream utility evaluation, or a multi-seed effect study.

| Selector | Configuration | Recipe ID | Run ID |
| --- | --- | --- | --- |
| Random + Degree | `baselines.yaml` | `exp014-baselines-r1` | `e14b1` |
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

These five selector types are the scope. The conditional RR cost declarations
below extend IM's parameter measurements. PageRank, trajectory selectors and
surrogate variants are not included; this is not every project selector.

## Progressive RR cost measurements

Only `rr_count` changes. The candidate pool, split, deletion budget, IM seed and
propagation probability remain fixed. Reuse the verified historical RR-1024
result (selector 366.55 seconds, process 380.39 seconds, original code SHA
`e5a61494b63d0a403f1d88acff05184e6f446dd6`) with its environment and timing
provenance labeled. Preserve the EXP-014 RR-65536 timeout as a failed attempt;
neither existing result is scheduled for an automatic rerun.

| RR count | Configuration | Recipe ID | Run ID | Scheduling role |
| --- | --- | --- | --- | --- |
| 4096 | `rr4096.yaml` | `exp014-rr4096-r1` | `e14c1` | First new measurement |
| 8192 | `rr8192.yaml` | `exp014-rr8192-r1` | `e14c2` | Conditional intermediate tier |
| 16384 | `rr16384.yaml` | `exp014-rr16384-r1` | `e14c3` | Expansion after 4096 |
| 32768 | `rr32768.yaml` | `exp014-rr32768-r1` | `e14c4` | Conditional further expansion |

After the currently authorized ETR batch releases the checkout, run the
independent D-full job, then start IM at RR-4096. Use real producer timings to
decide whether to proceed to RR-16384 or first measure RR-8192. RR-32768 runs
only if the observed costs leave reasonable headroom. This table is a set of
reviewed candidates, not an unconditional four-job batch.

Each RR job has a 7200-second whole-job cap. After a timeout/resource failure,
or a completed job taking at least 6480 seconds (90% of the cap), record the
outcome and stop IM expansion. The runner retains the full 7200-second cap for
a running job; the 6480-second threshold is not an early-kill instruction.
Scheduling estimates are disclosed heuristics, not measured costs or bounds.
Stopping IM does not cancel other independent Recipes, including D-full.

These four IM caps sum to at most eight job-hours plus termination overhead;
that sum is a spending ceiling, not a completion estimate. The user explicitly
authorized this bounded exploration without a pre-run cold completion forecast.
Do not replace a missing estimate with a timeout value. Report cache reuse
separately and do not remove cache content to manufacture cold measurements.

## Timing and acceptance

Use `run.json` cell `timing.current_access.wall_seconds` for the current
selector entry, including necessary model preparation and Selection validation.
Its exclusive `model_prepare` and `selector_access` phases separate model
preparation from the remaining selection path. `score_access_seconds` and
`selection_seconds` are access-path observations, not guaranteed pure kernel
compute times; do not add them again to the enclosing wall time. Dataset load,
startup, export and report generation are outside the selector-entry wall;
Runner start-to-finish time is the separate whole-job measure.

Each model-based selector uses its own process so an earlier selector cannot share
an in-memory model with a later selector or prevent its result from being exported.
Random and Degree share input loading but retain separate selector-entry timing;
their whole-job wall time is one shared observation and must not be counted twice.
The executor's batch ordering, rather than YAML display order, determines which
baseline runs first. Persistent
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

R-point, IM-RR65536 and D-full each have a user-approved 7200-second
(two-hour) whole-job timeout, including any required model preparation. Their
combined serial cap is six job-hours. The combined Random/Degree job retains
its 21600-second timeout. These are spending caps, not completion estimates;
termination overhead is additional. Submit jobs individually and do not retry
failed attempts automatically. The user waived the pre-run cold completion
forecast for this bounded exploration; keep the estimate unknown instead of
substituting a cap. Review the declarations, synchronize through the registered
installation action and pass formal preflight before execution.

Successful execution still requires trusted collection and validation of the
selected node count, uniqueness, candidate membership and exact input/artifact
identity. OOM, timeout, failure and not-run are distinct outcomes. No attack
effectiveness claim follows from a successful selector run.

Live preparation, estimates, attempts and evidence references belong to
`self/research/experiments/EXP-014.json`; this document does not duplicate run state.
