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
- Those same 18 summaries are the exhaustive repository-local JSON source for the benchmark Selection Artifact inventory: nine dataset/seed cells, each with a cold/warm pair that reuses the same eight affected method identities. Read-back found 72 unique affected Selection Artifact IDs (144 cold/warm references) and no cold/warm mismatch:
  - `citeseer_seed2024` (`score_9ebd0b10_9b68a451`): `gt_simple=sel_2d776e8f_639715b7`; `gt_full=sel_1e9c1046_d63a6e3b`; `p_simple=sel_21e4fe67_8c24ea1c`; `p_graph=sel_e3989f57_5a98a588`; `tracin_cp_simple_3=sel_ac474dcf_c02fa2b4`; `tracin_cp_simple_6=sel_e35ef264_8b11c9f7`; `tracin_cp_graph_3=sel_5ec748ee_23238f8a`; `tracin_cp_graph_6=sel_a7e893c5_39b20f17`.
  - `citeseer_seed212` (`score_21530297_45ec7349`): `gt_simple=sel_4816a882_744bc9d0`; `gt_full=sel_74951965_8ab8e885`; `p_simple=sel_99927146_efc9f6d5`; `p_graph=sel_7d4130bc_f81c7578`; `tracin_cp_simple_3=sel_149a1ba7_79a4779a`; `tracin_cp_simple_6=sel_0844aaea_0be7149b`; `tracin_cp_graph_3=sel_9d776b53_9a951179`; `tracin_cp_graph_6=sel_dbde0a55_f5082ab0`.
  - `citeseer_seed42` (`score_3b846e1d_c23ae08c`): `gt_simple=sel_240872a6_488cb6a7`; `gt_full=sel_ea885ddf_af33e798`; `p_simple=sel_8e31d7d2_80a5c7f4`; `p_graph=sel_117af3fc_27992a83`; `tracin_cp_simple_3=sel_006db3ad_fba85c4f`; `tracin_cp_simple_6=sel_810c5647_0099752e`; `tracin_cp_graph_3=sel_b9823573_f3846e9c`; `tracin_cp_graph_6=sel_410fc976_2c3f7b35`.
  - `cora_seed2024` (`score_b75ae9e4_ede60612`): `gt_simple=sel_952cee8a_e0c2523d`; `gt_full=sel_a9b8adff_6b08701c`; `p_simple=sel_4f9d12c3_30b6511c`; `p_graph=sel_fae4dfc8_9b5c7b61`; `tracin_cp_simple_3=sel_7d1802e1_89345e3e`; `tracin_cp_simple_6=sel_143d16e5_31bb2ca6`; `tracin_cp_graph_3=sel_c5e5621a_c9e1c809`; `tracin_cp_graph_6=sel_1e5fb399_05fd00aa`.
  - `cora_seed212` (`score_31e7adf8_b0836423`): `gt_simple=sel_e6f818d8_1f5a62ef`; `gt_full=sel_acc18a86_f3166be5`; `p_simple=sel_39a85e5f_19087ae3`; `p_graph=sel_35b68a90_72a9928f`; `tracin_cp_simple_3=sel_ceb4dabe_3b497aff`; `tracin_cp_simple_6=sel_2fb1436e_3b497aff`; `tracin_cp_graph_3=sel_61976748_00516dae`; `tracin_cp_graph_6=sel_7f334d8e_f85309b6`.
  - `cora_seed42` (`score_c8df2f02_a36035f7`): `gt_simple=sel_d29513c9_b02b1ed9`; `gt_full=sel_dcb6726b_f0386447`; `p_simple=sel_be95b036_78766aea`; `p_graph=sel_2567cf3c_31e13ec0`; `tracin_cp_simple_3=sel_f84c9fd1_d75ef403`; `tracin_cp_simple_6=sel_4ef03ddb_3dbb38e0`; `tracin_cp_graph_3=sel_08207461_069c8767`; `tracin_cp_graph_6=sel_ac51534e_e3ace18b`.
  - `pubmed_seed2024` (`score_029989ca_fa575ca0`): `gt_simple=sel_4f0e49f8_69582695`; `gt_full=sel_964e9ce8_b2cd9a6c`; `p_simple=sel_97c39f34_a74e6650`; `p_graph=sel_9274738d_009dde66`; `tracin_cp_simple_3=sel_8d3d15e2_80197195`; `tracin_cp_simple_6=sel_ffef463e_b4f74a1a`; `tracin_cp_graph_3=sel_2383b797_a2ef2f9b`; `tracin_cp_graph_6=sel_5d031ee8_99521a5a`.
  - `pubmed_seed212` (`score_a171f5b1_3cb7fb07`): `gt_simple=sel_78f97724_d6913e12`; `gt_full=sel_caec6900_65e77096`; `p_simple=sel_9936126f_b4d15800`; `p_graph=sel_0e7dbc9f_2b714d86`; `tracin_cp_simple_3=sel_28daa066_813a0f60`; `tracin_cp_simple_6=sel_3bb34294_3cc3f8cc`; `tracin_cp_graph_3=sel_b334a36c_4fc40f49`; `tracin_cp_graph_6=sel_02d6f50a_044bc0e5`.
  - `pubmed_seed42` (`score_3ee14f6e_d625896a`): `gt_simple=sel_c6ede8cd_32eaff7d`; `gt_full=sel_a1ac5929_116e8d62`; `p_simple=sel_d87219ef_f50ed709`; `p_graph=sel_ef231edd_7e1452d4`; `tracin_cp_simple_3=sel_e540a80c_1530241d`; `tracin_cp_simple_6=sel_edfdcc91_3dcdb938`; `tracin_cp_graph_3=sel_1334abbb_bd8ed880`; `tracin_cp_graph_6=sel_58a1b993_71968a5c`.
- `results/bc_target_v2/selection_benchmark_20260721/benchmark_manifest.json`: the retained `bc_target_v2.small_graph_selection_benchmark` aggregate covers those 18 summaries and is affected for the eight source-dependent fields above.
- `results/bc_target_v2/downstream/*.json`: all nine retained downstream summaries consume one of the old BC score bundles. Rows selected by the eight affected fields are historical-only under the corrected contract; rows for unaffected selectors are not reclassified by this Block.
- `results/bc_target_v2/aggregate/*`: `selection_metrics.csv`, `selection_aggregate.csv`, `cross_seed_stability.csv`, `downstream_metrics.csv`, `downstream_aggregate.csv`, `global_downstream.csv`, and `matrix_summary.json` aggregate the old affected rows and must not support corrected source-scope claims.
- Human projections that quote those affected rows include `reports/small_graph_selection_BENCHMARK_REPORT.{md,html}`, `reports/sup_selection_RESULTS_BRIEFING.{md,html}`, `reports/bc_target_matrix_REPORT.{md,html}`, `reports/small_selection_gu_FULL_REPORT.{md,html}`, `report/progress/2026-07-22_if-cluster-discussion/REPORT.{md,html}`, and the corresponding entries in `self/dashboard/VALIDATION_LOG.md`. This Block records the boundary but does not hand-edit generator-owned or historical projections.
- The repository report for the disposable SUP max-k canary names source score Artifact `score_a4403e0f_1635edf3` and three affected Selection Artifacts: `sel_9f322d5e_98386c3a` (`gt_full`), `sel_c44b45af_6d5d4348` (`p_graph`), and `sel_97b6c1dd_1944dff0` (`tracin_cp_graph_6`). Its declared temporary store no longer exists, so these are report-only historical identities, not current local cache entries.

## Required use boundary

- Preserve every old file and Artifact as immutable history.
- A corrected claim for an affected score, selected-node set, downstream row, or aggregate requires fresh production under the new Recipe identity and the project gate appropriate to that experiment.
- Degree, random, point-source, magnitude, and Hessian-only selector evidence is not invalidated by this label-scope defect.
- This ledger does not authorize any rerun, quarantine, cache cleanup, result rewrite, formal matrix, or downstream report rebuild.
