# Table 01: IF / naive selectors across GU methods

User-approved 2026-09-09. One scientific table, 270 GU cells:
Cora/CiteSeer/PubMed × R-point/D-full(last-layer, two-hop)/Degree/Random/PageRank
× GIF/GNNDelete/MEGU/IDEA/GraphEraser/GraphRevoker × seeds 42/212/2024 × 10%.
The budget denominator is the persisted training candidate pool. Dataset/Split,
model, training and method parameters are resolved from the public YAML instances.
No IM, SGC, alternative IF variant, or extra budget is added to this table.

`gate.yaml` is the same lanes at PageRank/seed42, 18 cells, followed by
`table01.yaml`. Its exact outputs can be reused in the full table.
`references.yaml` supplies 45 independent Retrain references; existing 032
outputs are reused only on exact semantic identity, including Selection.
Cache HIT counts are observed from receipts, not promised from method names.

The execution entry is `experiments/run.py <yaml> --run-id <unique-id>` through
the registered SyncMate route. Use `--dry_run` for no-write expansion. Formal
execution requires the live shared stage check and experiment preflight.

`post_method_metrics.yaml` is the same evaluation as 032. Each method's
post-deletion F1 is compared within dataset/seed/budget. Pairing to independent
Retrain is an explicit downstream analysis; aggregation does not retrain.
Shard method before/after metrics compare the shard ensemble to itself;
the canonical full GCN reference is stored separately, so the change in model
architecture is not mislabeled as an unlearning update.

Selection/Score, original models, shard initial ensembles and method Outputs
are reused on exact identities. Missing PageRank references and new GU Outputs
are computed. A clean full table requires 270 observed GU cells, 45 matching
reference cells, and verified collection, with failures/missing explicitly
reported. Completion of execution is distinct from user scientific acceptance.
