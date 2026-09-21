# AAGU-066: fixed Cora H16 paired validation

`gate.yaml` covers Random seed 104248; `table.yaml` covers 104246/104247/104248.
Both use the ordinary experiment schema, accepted GIF/IDEA H16 PT references,
10% of persisted training nodes, and independent 3000-epoch seed42 Retrain.
`validation.yaml` freezes diagnostic budgets, thresholds, input/PT identities,
and exact existing scalar evidence. The SyncMate fingerprint binds both files
and every referenced experiment YAML.

This experiment has a registered direct runner rather than the ordinary
cache-producing executor. Do not execute these tables through `experiments/run.py`.
Random uses the same deterministic score/ranking primitive as the ordinary lane.
No Score, Selection, Output, training, HVP, or iteration-vector cache is written.
The fixed PT is read strictly; Retrain always starts from fresh initialization.

## Validate and submit

```powershell
E:/conda_package/envs/gnn/python.exe experiments/aagu066_validation.py experiments/configs/aagu066/gate.yaml --dry_run
E:/conda_package/envs/gnn/python.exe experiments/aagu066_validation.py experiments/configs/aagu066/table.yaml --dry_run
```

After the software candidate is accepted/landed and local main, origin/main,
and the clean active SSH checkout agree, use the standard SyncMate entry:

```text
python scripts/syncmate/syncmate.py runner-agent dispatch gpu4090 --recipe opengu-aagu066-h16-gate-v1 --wait --json
```

Collect and verify the saved gate handoff through the existing SyncMate flow.
`done` only means execution completed. Confirm its collected numerical verdict,
then dispatch `opengu-aagu066-h16-v1`. The full runner requires the successful
same-commit gate before any computation and imports that request's checked
scalar results instead of training seed104248 again. No implicit retry or
overwrite is supported; another run identity needs a reviewed registration.

## Results and acceptance

Each request saves `selection.json`, `reference.json`, `gif.json`, `idea.json`,
and `retrain.json`, indexed and hashed by `run.json`. These are experiment
results, not reusable computation caches. Gradients, HVP vectors, model updates,
and predictions remain in memory and are discarded after evaluation.

All models are evaluated with the same raw-logit forward on both the original
and retained graph. Test/validation populations stay fixed; retained training
and deleted-node metrics have separate masks. The unchanged PT on the retained
graph is the graph-only control. Metrics include accuracy/macro-F1, same-graph
logit L2/max differences and prediction flips, weight absolute/relative L2,
and paired Retrain differences. No F1 threshold selects a parameter or budget.

GIF/IDEA execute the production T=100 update for missing paired evaluations.
For 104246/104247, exact 065 scalar diagnostics are validated against the current
data/PT/request/parameter identities and the newly computed update norm.
For 104248, one recurrence records 0..400, retaining only T/2T/4T vectors in
memory; its T=100 vector is checked against the production solver. Original
weights remain unchanged. Existing 065 budget consistency is a **difference
of update norms**, not a vector-distance claim; the same frozen 1e-3 norm
criterion applies to the whole table. The new request additionally reports
actual vector differences. Shifted residual <=1e-3, norm-budget consistency
<=1e-3, finite predictions, non-negligible update-to-RHS (>1e-6), and same-graph
logit change (>1e-8) are numerical checks. Original-equation residuals remain
visible and are not misrepresented as shifted-system failures or inverse proof.

After SyncMate checksum/index verification, generate the unified decision surface:

```text
python experiments/aagu066_report.py --recipe opengu-aagu066-h16-v1 --node-id gpu4090 --output .workblock/items/AAGU-066
```

The report generator refuses unverified or mismatched deliveries. It produces
Markdown, a self-contained HTML report, and three solver trajectory plots.
Scientific acceptance remains a human decision; collecting files or passing
numerical checks does not automatically open CiteSeer/PubMed validation.
