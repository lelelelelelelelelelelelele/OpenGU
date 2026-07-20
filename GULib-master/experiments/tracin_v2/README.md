# TracIn V2 gates and formal proper-TracIn candidate lane

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

## Formal selection-only lane

`run_formal_selection_gate.py` is the next gated layer. It builds a
`proper-tracin-v1` Recipe entirely from pre-compute inputs, stores the produced
score as an immutable Cache V2 Score Artifact, and materializes one max-k
Selection Artifact whose ordered prefixes serve smaller SUP budgets.

Output checkpoint/final-state hashes live in Score payload provenance rather
than the Recipe, so an exact warm lookup can skip model training and gradient
computation. The command also snapshots all three Legacy cache roots before and
after execution and fails if they change. Existing Planetoid raw files are
required; the formal gate does not auto-download datasets.

```powershell
E:/conda_package/envs/gnn/python.exe -m experiments.tracin_v2.run_formal_selection_gate `
  --data-root E:/project/OpenGU/GULib-master/data/raw/Planetoid `
  --score-store-root C:/temp/proper-tracin/score `
  --selection-store-root C:/temp/proper-tracin/selection `
  --legacy-results-root E:/project/OpenGU/GULib-master/results `
  --output C:/temp/proper-tracin/cold.json `
  --dataset Cora --model gcn --seed 2024 --optimizer adam `
  --epochs 30 --checkpoint-epochs 1,5,10,20,30 --budgets 14,7,3
```

This lane is still not registered in `AttackManager` or `experiments/run.py`.
Its Planetoid public-split gate is infrastructure/semantic evidence, not an
OpenGU canonical GU or paper-result claim. Hybrid and GU canaries remain later
gates.
