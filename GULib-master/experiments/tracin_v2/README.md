# TracIn V2 UNSTABLE gates

This directory is an isolated experiment lane for the multi-checkpoint
TracInCP contract. It is deliberately absent from the attack strategy registry,
the default runner, and all Legacy cache paths.

Gate order:

1. `G0`: pure scoring formulas, sign, single-checkpoint collapse, stable ties.
2. `G1`: semantic Recipe mutations must produce cache misses.
3. `G2`: Planetoid checkpoint-capture and selector comparison on CPU.

Local example:

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_tracin_v2_unstable.py

E:/conda_package/envs/gnn/python.exe -m experiments.tracin_v2.run_planetoid_gate `
  --data-root E:/project/OpenGU/GULib-master/data/raw/Planetoid `
  --output C:/temp/tracin_v2_cora_sgd.json `
  --dataset Cora `
  --model gcn `
  --optimizer sgd `
  --target-profile attack_safe_holdout
```

The Planetoid gate accepts `Cora`, `CiteSeer`, and `PubMed`, with either a
two-layer `gcn` or `gat` selector model. Use `--topk N` for a fixed comparison
budget across datasets; otherwise `--topk-ratio` is applied independently to
each candidate set. `run_cora_gate.py` remains as a compatibility entry point.

The JSON is a gate report, not a formal Cache V2 ScoreArtifact. Adam runs are
explicitly identified as `adam_lr_weighted_gradient_heuristic`; only the SGD
lane is used for the paper-aligned TracInCP semantic sanity.
