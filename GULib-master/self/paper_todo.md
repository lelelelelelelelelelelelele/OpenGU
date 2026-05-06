# Paper TODO

> Last updated: 2026-05-06

## Correct privacy-audit terminology

### Status

Open. The experiments can stay as-is, but the paper wording must be corrected before submission.

### Issue

The manuscript currently describes the privacy-side metric as standard shadow-model MIA:

- `report/paper/overleaf/sec/4_experiment.tex`: "MIA AUC using the shadow-model attack..."
- `report/paper/overleaf/sec/5_results.tex`: "MIA AUC post-unlearning, shadow-model attack..."

The Phase B pipeline records `attack.json::mia_auc` from each OpenGU method's `average_auc`. In the active node-unlearning path, this is not a Shokri/Olatunji-style shadow-model membership inference attack. It is a posterior-shift deletion audit:

- positives: nodes requested for unlearning
- negatives: held-out test nodes
- score: L2 distance between model posterior outputs before and after unlearning
- metric: ROC-AUC over that score

Representative implementation:

- `attack/pipeline_adapter.py` reads `self.method.average_auc`
- `unlearning/unlearning_methods/GIF/gif.py::mia_attack()` uses `self.unlearning_nodes` vs `self.data.test_indices`
- `attack/MIA_attack.py` contains shadow-model helpers, but they are not used by the current Phase B result path

### Decision

Keep the metric. It is reasonable for this paper because it directly audits whether an unlearning update exposes the deleted set. It is better aligned with a deletion-selection / graph-unlearning threat model than standard train-vs-test membership inference.

Do not claim it is standard shadow-model MIA.

The GraphEraser/GraphRevoker shard-based path should not be treated as a separate metric. It has the same high-level audit target as GIF/MEGU/IDEA/GNNDelete:

- positives: deleted/unlearned nodes
- negatives: held-out test nodes
- score family: before-vs-after posterior distance
- output: ROC-AUC

The difference is implementation cost and model-native posterior construction. GIF/MEGU/IDEA/GNNDelete can compute posterior shifts with full-batch single-model forwards. GraphEraser/GraphRevoker must query shard/submodel ensembles, reconstruct per-query shard data, load affected/unaffected shard models, and aggregate submodel posteriors. This explains the observed ~12 min GraphEraser audit cost versus ~1s for single-model methods. This is not currently classified as a correctness bug.

Paper implication: describe the reported value as a **method-native update-detection AUC**. It is acceptable as a complementary diagnostic, but avoid overclaiming calibrated cross-family privacy ranking. In particular, do not write that GraphEraser is strictly "more private" or "less private" than a single-model method solely from this AUC.

### Required paper edits

Replace "MIA AUC", "shadow-model attack", and broad "membership leakage" language where it refers to the reported metric with a more precise term, e.g.:

- update-detection AUC
- deletion-detection AUC
- deletion-membership audit
- posterior-shift audit
- unlearning verification risk

Suggested reporting-protocol wording:

```tex
(c)~an update-detection AUC inherited from the OpenGU evaluation protocol:
positives are nodes requested for unlearning, negatives are held-out test
nodes, and the attack score is the L2 shift in posterior outputs before
versus after unlearning.
```

Suggested limitation wording:

```tex
Our privacy-side audit is a posterior-shift deletion-membership test rather
than a full shadow-model MIA; implementing and scaling shadow-model MIA
across all GU families is left to future work.
```

### Files to revisit

- `report/paper/overleaf/sec/2_related_work.tex`
- `report/paper/overleaf/sec/4_experiment.tex`
- `report/paper/overleaf/sec/5_results.tex`
- `report/paper/overleaf/sec/6_conclusion.tex`
- `report/paper/outline/02_related_work.md`
- `report/paper/outline/04_experimental_setup.md`
- `report/paper/outline/05_5_mia.md`
- `self/dashboard/METRICS_CATALOG.md`
