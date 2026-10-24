# Independent Ret references

`ret-deterministic-v1` identifies a new learning procedure. Its output is not a reconstruction of any historical Retrain artifact. It requires GCN and exactly 3000 epochs. Run GPU compatibility and same-device reproducibility probes before interpreting a formal matrix.

The policy is configured at the ordinary launcher boundary before CUDA initialization: deterministic algorithms enabled with `warn_only=False`, CUBLAS workspace `:4096:8`, deterministic cuDNN with benchmarking disabled, and both TF32 flags disabled. A conflicting environment, late initialization, changed readback, or unsupported operation fails. There is no numerical fallback. The execution receipt records library/runtime versions, dtype, device, GPU/driver availability, backend settings, initial weights, CPU/CUDA/Python/NumPy RNG hashes, and training snapshots at epochs 1, 2, 10, 100, 1000, 3000. Full environment information stays in the run Observer; its digest participates in the reference computation identity.

## Source-free requests

First prepare and bind requests in a **separate ordinary selector-stage invocation**, including any proxy checkpoint, Score and Selection. The new Ret unlearning lane consumes only these prepared assets: model/Score/Selection MISS fails, and no proxy training or selection production is permitted under the global new numerical policy. Preparation has its own execution identity and scientific budget. Single-checkpoint target-direct selectors are supported; IM and trajectory checkpoint selectors are outside this lane. Each Ret instance declares one arm:

```yaml
kind: unlearning
schema_version: 1
method: Retrain
model:
  architecture: OpenGU.GCNNet
  hidden_channels: 64
training:
  epochs: 3000
  seed: 42
reference:
  policy: ret-deterministic-v1
  arm: joint
```

The experiment attaches only Ret instances with this policy, enables `execution.gu_cache.Retrain: disabled`, and attaches `observers: [{name: ret_reference_trace, methods: [Retrain]}]`. The usual dataset/selector/unlearning references and seed/budget axes apply. No new launcher is introduced. Reference outputs use ordinary run-owned Output storage; they never write or replace computation-cache Outputs. Their policy, arm, graph, training settings and numerical environment digest participate in identity. Explicit implementation fingerprints include the reference trainer, policy and Observer. No source-compatibility group is registered.

| arm | training supervision | training edges | role |
| --- | --- | --- | --- |
| joint | retained(S) | retained(S) | node-deletion training reference |
| supervision_only | retained(S) | original | diagnostic control |
| topology_only | original | retained(S) | diagnostic control |
| none | original | original | undeleted baseline |

Every arm for S validates on **retained(S) edges and original val_mask**. Features, labels and held-out masks are unchanged. Primary endpoint is final epoch 3000; the auxiliary endpoint is the earliest epoch attaining maximum validation accuracy. Validation does not stop or alter training. Test labels are read only for the fixed final/best endpoints. Both endpoints are probed on the original graph (primary) and retained graph (secondary); these probes do not certify deployment compliance. Repeated none training across S yields duplicate final weights and S-specific validation selection. It does not create independent baseline samples.

## Exact-source references and four-repetition probe

Use `stage: retrain_diagnostics`, the exact Dataset reference, and `output_inputs` containing a checksum-bound source run plus explicit `cell_ids`. The source must contain cached, original unlearning-stage Ret Outputs with GCN/3000 epochs/original evaluation graph. Dataset/Split, ordered Selection prefix, model and seed are verified before training. The source path never runs Selector or Original producers.

```yaml
ret_reference:
  policy: ret-deterministic-v1
  mode: reference
  arms: [joint, supervision_only, topology_only, none]
```

For a bounded probe use `mode: probe` and `arms: [joint]`. Each exact source request runs off1/off2/on1/on2 with identical initialization/training seeds. Off means no epoch-end validation or best selection; state/RNG audit snapshots and final export remain active. The probe records initialization/RNG/final weights/logit differences; it does not relax any old historical-reproduction threshold. To observe the current backend policy without changing it, use `policy: ret-observed-v1` **only for probe mode**, in a fresh process. This policy cannot produce new study references. CPU repeat equality does not establish GPU repeatability or identify the cause of historical GPU differences.

## Collected and run-owned evidence

Each cell returns `selection.json`, `metrics.json`, and `observers/ret_reference_trace/{result.json,trace.jsonl}` through the existing Recipe/collection acceptance path. Source-bound cells expand by arm with distinct cell IDs; former Dataset indices map by exact fingerprint. All 3000 rows per repetition are retained. The light reader verifies coverage, earliest-best choice, window summaries, deterministic settings and endpoint/RNG bindings.

Heavy assets stay under the invocation's runtime root. The result manifest binds relative paths and SHA-256 for pure state_dict best/final PT files and original/retained logits NPZ. Runtime assets must be retained while endpoint analyses depend on them. `experiments.ret_reference_reading.load_endpoints(run_path, run_sha256, cell_id, dataset_root=..., store_root=...)` verifies exact run/cell, source Output, every weight file/state hash, logits file hash, dimensions and metrics. For source-free cells it also checks final weights and original logits against the actual Output. It performs no forward or training. CE readback allows absolute 1e-5 / relative 1e-6 CPU-vs-device reduction error; accuracy and prediction bindings remain exact.

The returned original-graph best/final logits can be compared with exact same-request GU logits using the existing `prediction_triangle`/`cross_entropy` functions. Compare all predefined requests and seeds; do not infer GU–Ret disagreement from Ret accuracy. Source-free **joint final** is a normal Ret Output consumable by existing metrics. Other arms remain diagnostic controls and must not substitute for a legal joint reference.

## New Original from none.final

The manifest's none `endpoints.final.weights.path` is a standard pure state_dict checkpoint. Point the existing GIF/MEGU `checkpoint` field to that file and preserve its declared execution seed and model. Use one external checkpoint instance per seed; the existing parser rejects relabeling external checkpoints with a seed matrix. `none.best` depends on S and is not a common Original.

External checkpoint runs now persist the existing exact `prepare_model` receipt in `cell.cache_provenance.original_checkpoint`. The two-graph metrics case consumes that checksum-bound receipt, verifies its declared path, file SHA, state hash, Dataset/GCN/seed/numerical/implementation identity and original prediction reproduction. Missing or conflicting evidence fails, with no scanning, internal-cache fallback or training. Existing internal checkpoint verification is retained. Old external Outputs without an exact receipt cannot use this reader. External cases bypass evaluation reuse so the exact file is checked on each invocation.

Recipe generation dry-runs configuration and queries only Dataset metadata when needed; it does not load external checkpoint weights. The exact checkpoint must exist on the execution host at run time. Local availability is not substituted for remote verification.

## Validation boundary

The development tests use disposable CPU graphs, real 3000-epoch training, both native CLI/Recipe/collection lanes, exact-source off/off/on/on, four arms, test-label perturbation and callback state/RNG/gradient/mode checks, endpoint damage rejection, and none.final → GIF/MEGU → two-graph diagnostics. GPU operator support, same-GPU repeats, the planned scientific matrix, and paper acceptance remain separate observations.
