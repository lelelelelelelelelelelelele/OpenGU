# Small-selection → GU + SyncMate implementation acceptance

> [!NOTE]
> **路径哈希迁移说明（2026-07-24）**：本报告引用的 benchmark/summary SHA-256 已随 retired SSH path normalization 重算；实验数值和验收结论未改。原始字节可从 Git `41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` 复核。

Date: 2026-07-22
Status: **implementation PASS; formal v5 gate and 153-cell matrix accepted**

## Verdict

The code line is ready to enter Git acceptance. It provides a fail-closed,
hypothesis-preserving path from the accepted public 17-output Selection GT to
real OpenGU GU cells, plus a static gate recipe, nine bounded matrix recipes,
and verified collector contracts. Gate v2 exposed a processed-profile contract
gap before training (`train_indices` absent); gate v3 then exposed the explicit
pair loader's missing graph metadata (`num_classes`). Both are diagnostic only.
The v4 profile derives and verifies OpenGU split and graph compatibility fields
from immutable Planetoid tensors, and gate v4 passed end to end. The first full
stage then produced all 68 files but exposed a SyncMate protocol bug: the runner
validated only the last 16 KB of a larger valid JSON envelope. V5 validates the
complete envelope while retaining a bounded, hashed diagnostic tail. The v4
stage remains diagnostic because it was not accepted by SyncMate.

The active v5 line subsequently completed its formal gate and all nine bounded
dataset-seed stages on clean SSH `main@1c83bb4`. SyncMate accepted `153/153`
GU cells and `612/612` artifacts with zero GU failures. A separate sorted
SHA-256 manifest was then re-verified against the durable local copy with zero
missing, mismatched, or extra files. Scientific outcomes are reported in
`reports/small_selection_gu_FULL_REPORT.{md,html}`.

## Frozen first gate

| Field | Value |
|---|---|
| Lane | controlled public-profile GU |
| Dataset / split | Cora / Planetoid public fixed split |
| Base model | GCN, 2 layers, 64 hidden |
| GU method | GNNDelete |
| Selector | degree |
| Seed / budget | 42 / k=7 |
| Training | 100 epochs, CUDA 0 |
| Output | `attack.json`, `collateral.json`, `predictions.npz`, `_meta.json` |
| Claim boundary | infrastructure/provenance gate; not a method comparison |

## Gate-conditioned full screen

| Field | Frozen value |
|---|---|
| Expansion condition | the four-file gate is checksum-verified and accepted |
| Matrix | 17 selectors x 3 datasets x 3 seeds = 153 cells |
| Datasets | Cora, CiteSeer, PubMed; Planetoid public fixed profile |
| Seeds | 42, 212, 2024 |
| Model / GU / budget | GCN / GNNDelete / exact k=7 |
| Execution units | 9 static dataset-seed recipes; 17 selectors per recipe |
| Required artifacts | 4 per cell, 68 per stage, 612 total |
| Resume rule | same main SHA, source hashes, profile identity, and Selection manifest only |
| Scientific questions | TracIn vs degree/controls; effect and feasibility across IF formulas |

## What changed

- Added the named `planetoid_public_fixed` processed profile under
  `data/processed/transductive/`. It is staged before a formal timed run and
  verifies raw source fingerprint, public split counts, processed-file hashes,
  graph fingerprint, candidate-set hash, and candidate count.
- Added a grandfathered-GT adapter. It consumes the retained Cora cold summary
  and benchmark manifest by fixed SHA-256, validates the exact 17-output grid,
  and materializes fresh Cache V2 Selection Artifacts. It never follows the
  deleted worktree/cache paths recorded in the old summary.
- Preserved scientific selector labels (`a_grad_norm`, `p_graph`,
  `tracin_cp_point_6`, etc.) through artifact recipe, runner result key, and
  metadata. Formula rows are not relabelled as `degree` or `external`.
- Added exact-k propagation to attack and collateral consumers, so k=7 is not
  inferred from a dataset ratio.
- Added the active static SyncMate recipe
  `opengu-small-selection-gu-gate-v5`, exact four-artifact execution
  validation, a GU-specific collector profile, and post-collection acceptance.
- Added nine gate-conditioned static recipes covering the complete 17 x 3 x 3
  screen. Each stage has an exact 68-file allowlist and a dedicated collector
  acceptance that validates all 17 selector labels, Cache V2 provenance,
  attack status, collateral row, prediction identity, Git SHA, and checksums.
- Added resumable stage execution: complete leaves are skipped by content
  fingerprint; incomplete leaves are rerun; source/store/profile/SHA drift
  blocks instead of silently mixing evidence.
- Superseded v1 after a fail-closed dataset-pickle diagnostic, v2 after its
  pre-training `train_indices` diagnostic, and v3 after its `num_classes`
  diagnostic. V4 uses fresh gate/full config, evidence, Selection store, result
  roots, and recipe ids; v1/v2/v3/v4 cannot be
  resumed by the active wrappers.
- Gate v4 passed and collected 4/4 checksum-verified files. The first 17-cell
  full v4 stage completed its GU subprocess and wrote 68/68 files, but its
  16,000-byte-truncated stage JSON could not pass the exact-envelope validator.
  V5 fixes that parser and uses new gate/full/cache/result identities under a
  new pinned `main` SHA.
- Raised the processed-profile manifest to v3. It now derives
  `train/val/test_indices` and induced split edge tensors from the public masks,
  plus `name`, `num_features`, `num_classes`, and `num_edges` from graph tensors.
  All are persisted before timing and rejected if they drift.
- Repaired stale generic smoke/preflight binding. Text config hashes normalize
  line endings, and the recipes use the exact dispatched checkout rather than
  the unavailable historical base object.

## Identity and fail-closed evidence

| Evidence | Frozen value / rule |
|---|---|
| Accepted selector code SHA | `9240b9a7bd61b17b4c841981ec2892fdf100dc4b` |
| GU recipe introduction SHA | `218f6421c2cb31b71ebfad113fee15b9ad0a3d36` |
| Active GU v5 recipe introduction SHA | `324d3a0434614ec0d206e18f784560ae90f5f945` |
| Gate v5 config SHA-256 | `26c1b120c91cc96c14a659e15881687605be9b1e8fedd12aa54e085120e1bd10` |
| Full v5 config SHA-256 | `bdabc12b1a1cb83938c21eeb3b0e899d80855af38f036e38d08186a1ae4451dd` |
| Cora cold summary SHA-256 | `9e166ce6ad80c038eda11e1b5bdacbf541c17c19c416010c81ec708d3e929cee` |
| Benchmark manifest SHA-256 | `c46a5d3eb65f3196eeb7a21dcf67b8502d0cb08404803ea86e6a8c278297c49a` |
| SSH canonical public source fingerprint | `8201869db05fe584d6ee429b1c965be6b4cb4214b312c70963ac3be7b45e888f` |
| Source candidate count | 140 |
| Matrix requirement | exact 17 labels and full candidate permutations; 153 downstream cells |
| Downstream requirement | exact dataset/split/candidate identity and k |
| Formal checkout | clean SSH active `main`, job-bound full SHA |
| Reuse policy | new downstream Selection store; deleted old cache is never revived |

## Validation

| Check | Result |
|---|---|
| Focused gate GU/SyncMate/provider/demo/strategy suite before matrix extension | **222 passed** |
| SSH GU/SyncMate/provider/demo suite including new stage contracts | **214 passed** |
| SSH Cache-V2/Gate4/Phase-B/AutoReport/B-C suite | **144 passed** |
| Active v5 GU/profile/provider/SyncMate focused suite | **197 passed** |
| Large stage-envelope regression | PASS; >16 KB JSON is validated in full, diagnostic tail remains bounded and SHA-256 recorded |
| Formal v4 gate | PASS; 4/4 fetched, checksum-verified, and GU-accepted at `main@85c775a` |
| Full v4 Cora/seed42 diagnostic | GU subprocess exit 0 and 68/68 files present; SyncMate rejection due solely to truncated JSON validation |
| Real three-dataset v4 stage + verify | PASS; Cora/CiteSeer/PubMed all accepted |
| Cross-entry-point OpenGU split-contract smoke | PASS; indices and induced edges match all masks; `process_data` loads 3/3 |
| Cross-entry-point model construction | PASS; GCNNet instantiated for all 3 datasets with 1433/7, 3703/6, 500/3 feature/class metadata |
| Observed public split counts | Cora 140/500/1000; CiteSeer 120/500/1000; PubMed 60/500/1000 |
| Disposable v4 profile bytes | about 203 MB, removed after verification |
| `py_compile` on changed Python modules | PASS |
| Disposable local Cora public-profile stage + verify | PASS |
| Disposable staged bytes | 31.45 MB, removed after verification |
| Local SyncMate end-to-end smoke | PASS; 3/3 artifacts verified/indexed, 1 row parsed, temp workspace removed |
| `git diff --check` | PASS |
| Full repository `pytest -q` | INCOMPLETE: tool timeout after 604 s; no failure output was emitted |
| Strategy golden suite | 10/11; `degree_basic_k3` tie mismatch reproduces unchanged on `main@894a714`, so it is a pre-existing baseline issue |

The focused counts overlap and must not be added together. The full-suite timeout
is recorded as a gap, not converted into a pass. The formal SSH gate is the
remaining integration acceptance.

## Claim boundary

Passing the first gate proves that one immutable accepted ranking can be
transferred into a real GNNDelete cell, executed with exact k, collected,
checksum-verified, indexed, and accepted without losing provenance. It does not
show that degree is better than TracIn, nor which IF formula is best. Those
questions require the gate-conditioned 153-cell structured matrix. The public-profile screen and
the OpenGU 80/20 confirmatory lane remain explicitly separate.

## Final execution outcome

1. The complete v5 implementation line was accepted into `main`; local,
   `origin/main`, and the SSH active checkout were aligned before formal work.
2. All three `planetoid_public_fixed` profiles were staged and verified before
   timing. No formal stage downloaded or preprocessed a dataset.
3. Gate job `gu-gate-v5-20260722-0702` passed and collected `4/4` artifacts.
4. The nine dataset-seed jobs ran sequentially. Every stage accepted `17/17`
   cells and `68/68` checksum-verified artifacts before the next stage started.
5. The complete result root contains exactly `153` leaves and `612` files.
   Remote-to-local SHA-256 verification passed `612/612`; manifest SHA-256 is
   `e45aa4b193d53b854c709e3de543517417fa6a9f0d3eb1f013aea9bc3e16d236`.
6. Results, verification receipts, gate/stage evidence, machine-readable
   aggregates, and the paired scientific report are retained locally under
   `results/runs/gpu4090-gu-20260722/`.
