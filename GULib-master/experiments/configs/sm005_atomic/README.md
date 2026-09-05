# SM-005 single-cell GPU verification

This registered verification plan consumes AAGU-026's independent instances:
Cora / Degree / GNNDelete / post_unlearning_utility. It is owned by SyncMate
SM-005's real workflow test. It does not accept AAGU-007 or expand its formal
dual-budget scientific gate.

The existing canonical split producer materialized and verified the explicit
70/10/20, split seed 2024 profile on the SSH active checkout. `dataset.yaml`
binds that graph and its manifest by SHA-256. The preparation receipt is in
SyncMate `.workblock/runtime/sm-005/dataset-preparation.stdout`; the producer
script is retained alongside it. Input production precedes the measured run.
There are 1,895 training candidates; the 1% budget removes 18 nodes. Training
uses seed 42, GCN 2 layers / hidden 64, 100 epochs; GNNDelete uses its registered
defaults, including 50 unlearning epochs. The expanded config is in the run
summary. This one cell supports execution and evidence-chain validation only.

The static recipe `opengu-sm005-atomic-gpu-v1` invokes
`experiments.syncmate_atomic_stage` through SyncMate's queue. The stage requires
the canonical SSH checkout, installed pinned Core, a visible RTX 4090, verified
Dataset/Split input, and exactly one matching running queue job. Core captures
the exact clean-main Git SHA and config digest at dispatch. No job fields can
override commands, parameters, device, or output paths.

The stage writes one immutable `summary.json` under
`results/runs/modular/sm005-cora-degree-gnndelete/sm005-gpu-v1/`. Queue receipt
and checksum manifest bind the submitting job and full source SHA to this
output. Existing output blocks execution. Collect only this leaf with
`summary.json` in the peer artifact policy, verify SHA-256 into the trusted
index, and interpret it together with the queue receipt. `done` is execution
success; scientific acceptance remains a separate human decision.

## B-Hutch repeat and cache verification

The second reviewed cell uses `experiment_b_hutch32.yaml`: the same Cora split,
1% budget, GNNDelete and utility evaluation, with `b_param_hutch` replacing
Degree. Its last-layer Hutchinson estimator uses 32 probes (seed 1729) and the
registered LiSSA defaults (20 iterations, scale 25, damping 0.01). This changes
the selector only; no data preparation or cache cleanup is part of this test.

Run `opengu-sm005-b-hutch32-first-v1`, then
`opengu-sm005-b-hutch32-warm-v1` through the same SyncMate dispatch/runner path.
Both recipes bind the exact same scientific configuration. Their output leaves
are `results/runs/modular/sm005-cora-b-hutch32-gnndelete/` followed by
`sm005-b-hutch32-first-v1/summary.json` and
`sm005-b-hutch32-warm-v1/summary.json`, respectively. Existing leaves refuse
execution; the run ID cannot be supplied by an arbitrary queue field.

Preserve the shared Cache V2 store and checkpoint root. Record the first run's
actual cache state (it is not guaranteed cold), then compare checkpoint,
Score, Selection and GU identities, HIT flags and producer observations after
the second run. Verify both collected summaries before interpreting them.
Evaluation is computed from the verified GU result on each run; it has no
separate HIT flag. No duration-only inference counts as cache verification.

## D-full, stopping at Selector

`opengu-sm005-d-full-selector-v1` consumes `experiment_d_full_selector.yaml`
with `gt_full` (D-full), the same Cora input and 1% train-candidate budget.
It reuses the registered last-layer model/training and graph-source / LiSSA
defaults. It scores all 1,895 candidates and selects 18 nodes. The reviewed
shape is one Selector, zero GU, zero Evaluation, checked before data access
and again against the result. This test does not exercise GU result readback.

Its immutable output is
`results/runs/modular/sm005-cora-d-full-selector/sm005-d-full-selector-v1/summary.json`.
Run once via the normal SyncMate queue, collect and verify this exact output,
and report actual checkpoint / Score / Selection HIT flags. Existing caches
are preserved; no warm rerun or downstream unlearning is implied.

## D-full warm run for automatic return

The additional reviewed recipe `opengu-sm005-d-full-return-v1` uses the exact
same D-full YAML and shared cache/checkpoint roots. It writes a fresh run record
at `results/runs/modular/sm005-cora-d-full-selector/sm005-d-full-return-v1/summary.json`.
This output directory records an invocation; it is not a second computation cache.
Inspect checkpoint / Score / Selection HIT and producer flags to prove reuse;
startup and input/hash verification still take time even on a full HIT.

With the reviewed Core supporting automatic return, dispatch this recipe with
`--wait --json` in a persistent background controller process and run the
existing bounded remote worker. The same controller invocation must wait,
collect the declared summary and verify SHA-256 without later Agent commands.
Its scope comes from the recipe, so no per-run `device.yaml.result_roots` entry
is needed. Device policy still selects filenames and the local landing.
This is a transfer test, with zero GU / Evaluation and no scientific acceptance.
