# AAGU-018 affected evidence ledger

Observed read-only on 2026-08-26. No Artifact, result, aggregate, report, index, or cache entry listed here was edited, renamed, moved, deleted, or overwritten.

## Corrected semantic identities

- `c_target_gif_tracin_score_bundle`: `c-target-gif-tracin-v1.0` → `c-target-gif-tracin-v1.1`.
- `bc_target_selection_score_bundle`: current producer `bc-target-matrix-v3.1` → `bc-target-matrix-v3.2`.
- `target_direct_opengu_gcn_selection_score_bundle`: `target-direct-opengu-gcn-score-bundle-v2` → `target-direct-opengu-gcn-score-bundle-v3`.
- New Recipes declare `graph_intervention.source_scope=affected_intersection_train_mask` and `loss.graph_source_set=affected_intersection_train_mask`; the changed source files also advance each source fingerprint and therefore force a new Cache V2 Recipe identity.

## Score fields affected by the label-scope defect

- Affected: `gt_simple`, `gt_full`, `p_simple`, `p_graph`, `tracin_cp_simple_3`, `tracin_cp_simple_6`, `tracin_cp_graph_3`, and `tracin_cp_graph_6`.
- Unaffected computations: `a_grad_norm`, `b_param_hutch`, `b_param_lissa`, `degree`, `legacy`, `p_point`, `r_point`, `random`, `tracin_cp_point_3`, and `tracin_cp_point_6`.
- The BC/target-direct score bundle has one mixed Artifact identity. Unaffected fields need not change numerically, but an old mixed bundle cannot satisfy the corrected Recipe or warm-hit the new producer.

## Existing Cache V2 score Artifacts

All observed headers are still `status=valid` as historical bytes. They do not meet the corrected affected-source contract and must not be cited as corrected D-GIF/C-simple evidence.

### `results/cache_v2/c_target_v1` (`c-target-gif-tracin-v1.0`)

- `score_352bdc51_b724c086`
- `score_9c9b34fd_004f3774`
- `score_cba1133f_6149fda0`
- `score_cc91de53_1a8a72f8`
- `score_ee930537_b9d130cb`
- `score_f1162cd2_4acbf305`

### `results/cache_v2/bc_target_v2` (`bc-target-matrix-v2.0`)

- `score_23f2cbea_e1dd24dd`
- `score_26488c63_c1a785de`
- `score_4346d28a_bbe857e7`
- `score_46167175_175575a6`
- `score_5f4c4971_a329f277`
- `score_5f61998d_88b47a75`
- `score_65315186_8efc051a`
- `score_8b3257d6_c87fd4da`
- `score_f69e8b38_375b858e`

There is no local `results/cache_v2/target_direct_formal_v2` or target-direct score Artifact. The formal target-direct matrix remains unexecuted; future score production must use the new target-direct identity.

## Historical result and aggregate boundary

- `results/c_target_v1/*.json`: 10 retained `c_target_v1.run_summary` files at `c-target-gif-tracin-v1.0` reference five of the six local score IDs. They remain historical validation records only for the affected fields.
- `results/bc_target_v2/selection/*.json` and `cache_checks/*.json`: 12 retained `bc_target_v2.selection_summary` files at `bc-target-matrix-v2.0` reference the nine local BC score Artifacts.
- `results/bc_target_v2/selection_benchmark_20260721/cells/*/{cold,warm}.json`: 18 retained `bc-target-matrix-v3.0` summaries reference nine score IDs (`score_029989ca_fa575ca0`, `score_21530297_45ec7349`, `score_31e7adf8_b0836423`, `score_3b846e1d_c23ae08c`, `score_3ee14f6e_d625896a`, `score_9ebd0b10_9b68a451`, `score_a171f5b1_3cb7fb07`, `score_b75ae9e4_ede60612`, and `score_c8df2f02_a36035f7`) that are not present in the observed local Cache V2 root.
- `results/bc_target_v2/selection_benchmark_20260721/benchmark_manifest.json`: the retained `bc_target_v2.small_graph_selection_benchmark` aggregate covers those 18 summaries and is affected for the eight source-dependent fields above.
- `results/bc_target_v2/downstream/*.json`: all nine retained downstream summaries consume one of the old BC score bundles. Rows selected by the eight affected fields are historical-only under the corrected contract; rows for unaffected selectors are not reclassified by this Block.
- `results/bc_target_v2/aggregate/*`: `selection_metrics.csv`, `selection_aggregate.csv`, `cross_seed_stability.csv`, `downstream_metrics.csv`, `downstream_aggregate.csv`, `global_downstream.csv`, and `matrix_summary.json` aggregate the old affected rows and must not support corrected source-scope claims.
- Human projections that quote those affected rows include `reports/small_graph_selection_BENCHMARK_REPORT.{md,html}`, `reports/sup_selection_RESULTS_BRIEFING.{md,html}`, `reports/bc_target_matrix_REPORT.{md,html}`, `reports/small_selection_gu_FULL_REPORT.{md,html}`, `report/progress/2026-07-22_if-cluster-discussion/REPORT.{md,html}`, and the corresponding entries in `self/dashboard/VALIDATION_LOG.md`. This Block records the boundary but does not hand-edit generator-owned or historical projections.
- The repository report for the disposable SUP max-k canary names three affected Selection Artifacts: `sel_9f322d5e_98386c3a` (`gt_full`), `sel_c44b45af_6d5d4348` (`p_graph`), and `sel_97b6c1dd_1944dff0` (`tracin_cp_graph_6`). Its declared temporary store no longer exists, so these are report-only historical identities, not current local cache entries.

## Required use boundary

- Preserve every old file and Artifact as immutable history.
- A corrected claim for an affected score, selected-node set, downstream row, or aggregate requires fresh production under the new Recipe identity and the project gate appropriate to that experiment.
- Degree, random, point-source, magnitude, and Hessian-only selector evidence is not invalidated by this label-scope defect.
- This ledger does not authorize any rerun, quarantine, cache cleanup, result rewrite, formal matrix, or downstream report rebuild.
