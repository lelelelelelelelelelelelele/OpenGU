# Methods: paired Flip / Hop

`post_unlearning_flip_hop` compares persisted GU predictions with independently
persisted Retrain predictions for the **same deletion request**. It is a Metrics-only
evaluation; it never trains, invokes a GU producer, or performs a model forward pass.
Existing evaluation cases keep their definitions.

Let S be the deleted nodes, T the bound Dataset/Split test mask, and E = T \\ S.
For each node v, define D(v) = 1[argmax GU(v) != argmax Retrain(v)]. Ties use the
first class index, as in NumPy argmax. `fraction_flipped = sum(v in E) D(v) / |E|`.
`node_count` is |E| and `flipped_count` is the numerator. Empty E yields null.
This measures GU–Retrain disagreement, not accuracy, change from the original
model, or proof of forgetting. The remaining training `retain_mask` is not E.

On the **bound original graph before deletion**, interpret each edge as undirected
and compute the minimum shortest-path distance from any node in S. Partition E
into distances 1, 2, 3, and >3 or unreachable. The last group is named `gt3`.
Self-loops and duplicate edges do not change distance. Group labels do not imply
that disagreement must decrease with distance.

For each prefix `1`, `2`, `3`, `gt3`, export `<prefix>_hop_count`,
`<prefix>_hop_flipped_count`, and `<prefix>_hop_flip_rate`. An empty group has count
and disagreement count zero, and rate **null**, never zero. Group counts sum to
`node_count`, and group disagreement counts sum to `flipped_count`. Across cells,
pooled rates must be computed from summed numerators/denominators; an unweighted
mean of group rates is not a pooled Flip rate.

Pairing requires exact Selection reference, Dataset/Split input reference, original
graph fingerprint, and the full pairing identity (nodes, model, training, deletion
semantics, training graph and prediction evaluation graph). Zero or multiple
matching Retrain candidates, including repeated identical references, are rejected.
Resolved labels, masks, selected nodes, original/evaluation edges and prediction
shapes must also agree. GU-specific parameters are not Retrain pairing axes.
An explicitly supplied Retrain reference is checked by the same rules.

The evaluation receipt binds both Output references, requested metric names,
producer version, actual retained-test mask hash and size, original graph and
Dataset/Split identity, prediction graph, undirected grouping/empty-group/tie rules,
NumPy version, and implementation fingerprint. Metrics never rewrites an input
Artifact. Original-graph hops remain original-graph hops even when predictions
were evaluated on a retained graph; the two graphs have separate identity fields.

The ordinary Metrics run exports these values, receipt ID, full metric identity
and Retrain baseline reference in each GU cell's `metrics.json`. Paired-only runs
do not export standalone Retrain metric cells. Combining this case with
`post_method_metrics` also exports the latter for Retrain. `eval_collateral.py`
accepts the same evaluation YAML and preserves the new test-mask Flip; older
collateral diagnostics retain their historical definition in other cases.

## Configuration and bounded verification

Use [the public evaluation](../../experiments/configs/evaluations/post_unlearning_flip_hop.yaml)
in the ordinary `evaluation_refs` list, alongside any existing evaluations.
See [the Metrics template](../../experiments/configs/flip_hop_metrics.template.yaml).
Bind each source `run.json` and SHA-256 to completed GU/Retrain runs and use the
same bound Dataset/Split. Use a new output run ID. The template's null references
must be filled before execution; this is not a registered formal run.

```powershell
& E:/conda_package/envs/gnn/python.exe -B -m pytest tests/test_flip_hop_metrics.py -q
```

The test fixture persists hand-authored predictions and synthetic model-state
tensors using the real Cache V2 store; it does not train a model. It exercises the
ordinary Metrics entry, exports and reads checksummed result documents, and
forbids training, GU/Selector producers and forward calls throughout. This is
CPU software evidence only. AAGU-010 owns the separate 828-pair real-result backfill;
passing this test neither performs that backfill nor validates a scientific claim.
