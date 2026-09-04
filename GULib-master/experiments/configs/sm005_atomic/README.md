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
