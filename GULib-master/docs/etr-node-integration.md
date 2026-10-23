# ETR node unlearning

The ordinary `experiments/run.py` YAML lane supports `method: ETR` with
`OpenGU.GCNNet`, training-node Selection requests, independently configured
Retrain and the existing Output v2 / paired evaluations. Use the public
`experiments/configs/unlearning/etr.yaml` reference in `unlearning_refs`.

```yaml
kind: unlearning
schema_version: 1
method: ETR
parameters:
  etr_erase_ratio: 0.01
  etr_l: 0.3
```

Model/training settings and an optional external pure state dict use the ordinary
GU configuration contract. An explicit `checkpoint` skips initial training.
Different ETR parameters, Selection, checkpoint, model, deletion/evaluation
protocol or algorithm source produce distinct computation identities. ETR does
not run Retrain internally. Add a separate `retrain.yaml` reference for paired
evaluation. This integration does not add ETR to the legacy `main.py` lane.

## Algorithm source and protocol

The main reference is the OpenGU-derived
[Unlearning_Benchmark](https://github.com/idea-iitd/Unlearning_Benchmark/tree/9c95ac387b528967cc1c3aebbd20ce78bcf418c8),
specifically `GULib-master/task/ETRTrainer.py` and the ETR pipeline/utilities.
The adapted kernel retains its MIT notice in
`unlearning/unlearning_methods/ETR/LICENSE.benchmark`.
The [authors' implementation](https://github.com/AllminerLab/ETR/tree/c88ec741480015df2060e511c461c647552e32ba)
is an auxiliary algorithm reference, not the numerical comparison target.

1. Restrict edit-gradient edges to pairs of training nodes. Preserve node IDs,
   features and labels. Find two-hop affected training nodes, excluding requests.
2. Compute original training, forget-subgraph and affected-subgraph gradients;
   parameter importance is the squared gradient. Cross entropy uses label
   smoothing 0.1, matching the benchmark; the model is in training mode.
3. Erase scales parameters by the benchmark's two importance-ratio quantiles.
4. Recompute affected-subgraph gradients on the edited model and retained graph,
   then apply the benchmark's Rectify equation once with `etr_l`.

No optimizer step occurs. The reference's Adam object only calls `zero_grad`;
the kernel uses `model.zero_grad(set_to_none=True)` directly, so unused `etr_lr`
and `etr_wd` knobs are not exposed. Both effective edit parameters are in cache
identity. The model input is copied, preserving the initial checkpoint.

Deletion removes incident edges and selected supervision while retaining feature
rows. Evaluation uses the ordinary configured original graph (default) or retained
graph. The benchmark trainer's own retained-graph F1 must not be confused with
the project's default original-graph comparison. Ordinary Retrain trains on the
full retained graph; ETR's train-only edit subgraphs are method-specific.

The benchmark uses PyG's exact seed mapping for subgraph loss. This differs from
the authors' `output[:batch_size]` indexing; the integration follows the benchmark
mapping. It also follows the benchmark's filtering of seeds absent from subgraph
edges: the requested deletion set is unchanged, but gradient seed counts can be
smaller. Rectify population coefficients still use the full request and affected
node counts, exactly as the benchmark does. Verification records both counts.

The implementation does not manufacture edges or substitute unrelated seeds for
empty subgraphs. It fails explicitly on an empty connected seed population, zero
erase quantiles, or non-finite edits. A one-seed loss keeps a one-dimensional label
tensor. These boundary adaptations prevent invalid results and do not alter the
verified nondegenerate benchmark computation. Edge/feature deletion, other GU
architectures and Observer events are not supported by this ETR adapter.

## Reproduce the CPU comparison

`experiments/verify_etr_cpu.py` accepts an existing legacy Cora 80/0/20 graph,
a directory containing pinned benchmark sources, and a new output directory:

```powershell
python experiments/verify_etr_cpu.py --root <new-verification-directory> `
  --data-file <cora0.8_0_0.2.pkl> --reference-directory <reference-directory>
```

The reference directory must contain the unchanged benchmark files under these
local names: `ETRTrainer.py`, `etr_utils.py`, `etr_pipeline.py`. Their SHA-256
digests are fixed in the verifier. The verifier loads the actual reference
pipeline request hook and trainer; bindings only select CPU, supply the request
file and redirect model saving. It does not compare the kernel to itself.

The verifier writes its protocol before running. It preserves all 542 original
test nodes and holds 270 validation nodes out of the old training population with
NumPy seed 2024, resulting in 1896/270/542 train/validation/test nodes. This is a
separately named local verification split, not the formal dataset profile.
All graph features and edges are preserved. Source and derived dataset hashes,
node lists, configs and initial checkpoint identity are saved.

The two cases are Random 10% (189 nodes) and Degree 5% (94 nodes), with budgets
floored against the same 1896 training candidates. GCN uses two layers, 64 hidden
channels, 100 initial/retrain epochs, Adam lr 0.01, weight decay 0.0005 and seed 42.
Reference and integrated edits reset the same random state, including dropout.

For each case the verifier executes the ordinary CLI dry-run, cold run and warm
run, verifies exported result files, compares independently executed benchmark
Erase/Rectify states and logits with the kernel and persisted Output, and checks
that the same Selection reaches ETR and Retrain. CPU float32 tolerances are fixed
in advance at `atol=1e-6`, `rtol=1e-5`. It saves raw stage states and predictions,
not just accuracy. CLI logs and failed attempts remain reviewable.

Timing scopes differ: the benchmark's reported edit timer excludes its initial
full-training gradient; the integrated compute timer includes subgraph preparation
and all four gradient passes. The verifier records both scopes. These checks
validate software integration, not paper-score reproduction or GPU performance.
