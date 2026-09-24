# Table 01: IF / naive selectors across GU methods

## Table 02 v2 (configuration review)

[table02_v2.yaml](table02_v2.yaml) defines the complete 1449-cell matrix:
207 selection conditions across GIF, IDEA, GNNDelete, MEGU, GraphEraser,
GraphRevoker and Retrain. All methods use the current public instances and
production code. Its experiment ID is `exp011-t2`; each execution
requires a fresh run ID. Existing artifacts are reused only on exact identity.
Formal execution awaits user approval.

The complete table uses public `gif_h64.yaml` / `idea_h64.yaml` instances and
`profiles/gif_idea_fixed_pt.yaml`: two-layer GCN, hidden width 64, iteration 100,
and the verified per-dataset scale/damp mapping. Training seeds remain separate.
The two `evaluation_refs` request Retrain-gap and Flip/Hop. Ordinary Unlearning
already exports single-method metrics and utility, so those need no extra refs.
After all Outputs are available (cache hits or fresh computation), the same run
pairs GU with its exact Retrain and exports the requested metrics. No second
Metrics submission is required. Re-running under a fresh run ID can therefore
backfill metrics while reusing exact Outputs; cache misses still compute normally.

The ordinary independent Metrics stage remains available for explicitly bound
historical Outputs. It does not redefine pairing or metric semantics.

## Additional Table 02 (2026-09-13)

[Table 02](table02.md) adds a 10% IF / RR / naive comparison owned by
AAGU-011. A single `table02.yaml` expands the 207 selection conditions across
four GU methods plus the matched Retrain reference, for 1035 method cells.
It retains three training seeds, uses three RR sampling seeds per R and ten
Random sampling seeds, and excludes GIF/IDEA.
The Table 01 description and historical execution evidence below remain scoped
to Table 01; the old “No IM” statement does not describe Table 02.

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

## AAGU-047 numerical recovery

The first table01 run stopped on GraphRevoker aggregation weights. Both shard
optimizers share a zero-weight norm/normalization hazard. Their numerical repair
uses a dtype machine-epsilon lower bound during optimization and a defined
vector-norm gradient at zero; the optimizer, objective and output validation are
retained. This changes both shard producers and original ensemble checkpoints;
old GraphEraser/GraphRevoker outputs remain immutable historical evidence and
are not reused as repaired outputs. Other GU, Selection and Retrain identities
are unchanged.

`recovery_gate.yaml` covers three datasets, gt_full, the two shard methods and
seeds 42/2024 (12 cells), including the condition implicated by the failed run.
After it passes, `opengu-aagu011-table01-v2` executes the unchanged scientific
`table01.yaml` under a new run identity. No failed run is overwritten. Previously
verified Retrain references remain usable by exact semantic pairing across this
unrelated-to-Retrain source change; the analysis records each source SHA.


### GPA数值恢复

047恢复gate在PubMed GraphRevoker分区目标出现nonfinite并失败，保留原run。048修复GPA的无边batch与零概率目标/梯度边界，采用recovery_gate_v2.yaml（相同3图、gt_full、两分片方法、seed42/2024、10%），run aagu048-gpa-gate-v1。完整主表仍使用未启动过的aagu011-table01-v2，科学配置不变。新的GR producer与初始ensemble重算，GE与其余GU/Selection/Retrain继续按完整身份复用。
