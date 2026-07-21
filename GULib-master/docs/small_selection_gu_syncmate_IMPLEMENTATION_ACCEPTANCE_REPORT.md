# Small-selection → GU + SyncMate implementation acceptance

Date: 2026-07-22  
Status: **implementation PASS; formal SSH gate pending**

## Verdict

The code line is ready to enter Git acceptance. It provides a fail-closed,
hypothesis-preserving path from the accepted public 17-output Selection GT to
real OpenGU GU cells, plus a static gate recipe, nine bounded matrix recipes,
and verified collector contracts. No GU result is claimed by this report; the first formal result is
created only after this line is merged into `main` and executed from the clean,
pinned SSH active checkout.

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
- Added the static SyncMate recipe
  `opengu-small-selection-gu-gate-v1`, exact four-artifact execution
  validation, a GU-specific collector profile, and post-collection acceptance.
- Added nine gate-conditioned static recipes covering the complete 17 x 3 x 3
  screen. Each stage has an exact 68-file allowlist and a dedicated collector
  acceptance that validates all 17 selector labels, Cache V2 provenance,
  attack status, collateral row, prediction identity, Git SHA, and checksums.
- Added resumable stage execution: complete leaves are skipped by content
  fingerprint; incomplete leaves are rerun; source/store/profile/SHA drift
  blocks instead of silently mixing evidence.
- Repaired stale generic smoke/preflight binding. Text config hashes normalize
  line endings, and the recipes use the exact dispatched checkout rather than
  the unavailable historical base object.

## Identity and fail-closed evidence

| Evidence | Frozen value / rule |
|---|---|
| Accepted selector code SHA | `9240b9a7bd61b17b4c841981ec2892fdf100dc4b` |
| Cora cold summary SHA-256 | `977a6ff2384f31da8974df98affa7b2109a8f69df3f0191c0990e1101e5bacf7` |
| Benchmark manifest SHA-256 | `3212232a4274190e4c5a075eeea20fc92f982e7f4293670037795c2932e0e479` |
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
| New nine-stage SyncMate/config contract | local syntax + definition smoke PASS; SSH focused pytest pending first review commit |
| Earlier Phase-B/Cache-V2/AutoReport changed-surface suite | **138 passed** |
| `py_compile` on changed Python modules | PASS |
| Disposable local Cora public-profile stage + verify | PASS |
| Disposable staged bytes | 31.45 MB, removed after verification |
| Local SyncMate end-to-end smoke | PASS; 3/3 artifacts verified/indexed, 1 row parsed, temp workspace removed |
| `git diff --check` | PASS |
| Full repository `pytest -q` | INCOMPLETE: tool timeout after 604 s; no failure output was emitted |

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

## Next acceptance steps

1. Commit this implementation and pin its introduction SHA in the reviewed
   SyncMate recipe metadata.
2. Merge with `--no-ff` into `main`, push, and synchronize the SSH active
   checkout with `git pull --ff-only`.
3. Stage and verify all three `planetoid_public_fixed` profiles before timed runs.
4. Configure the local collector/peer and update the runner's untracked artifact
   policy for the exact four files.
5. Run a pinned SyncMate smoke, then the single formal GU recipe.
6. Collect, checksum-verify, index, and gate the four files. Expansion remains
   blocked until that acceptance passes.
7. Dispatch the nine reviewed dataset-seed recipes sequentially. Each stage
   must collect and accept 68 files before the next stage is trusted.
8. Aggregate and return all 612 verified files to the local collector, together
   with a matching Markdown/HTML scientific report.
