# E8 IF Target-Direct Formal Preflight Audit

Date: 2026-07-24

Source of truth: this Markdown file

Status: **preparation PASS; formal execution NO-GO**

> [!danger] Verdict
> The updated target-direct lane is prepared and locally validated, but no formal
> experiment was started. The active SSH checkout is clean `main@fb0d9a33`, while
> the preparation line, including this dual-budget revision, remains unmerged on
> `codex/fix-target-direct-formal-orchestration-20260724`. The SSH runner also has
> no visible GPU, no accepted `gnn_20` interpreter, and none of the three approved
> 70/10/20 processed profiles. These are hard blockers, not warnings.

## Contract disposition

| Contract item | Prepared behavior | Status |
|---|---|---|
| Matrix | Candidate scope is Cora/CiteSeer/PubMed × seeds 42/212/2024 × 17 selectors × ratios 1%/5% = 306 cells; expansion is not yet authorized | PASS |
| Split vs budget | `70/10/20` is the leakage-safe split; `{0.01, 0.05}` are deletion ratios and cannot replace it | PASS |
| Split implementation | Import-safe `utils/node_split.py` is shared by native OpenGU preprocessing and target-direct staging; the formal layer owns only materialization/verification and evidence identity | PASS |
| Budget | Per ratio derive `k(r) = max(1, floor(r × candidate_count))` from each verified profile | PASS |
| Expected profile checks | Cora 1,895→18/94; CiteSeer 2,328→23/116; PubMed 13,801→138/690 | PASS as preflight expectations; execution still derives them |
| White-box identity | Selection and downstream GNNDelete bind the same OpenGU GCN architecture and exact checkpoint hashes | PASS |
| Formal parameter scope | `last_layer` only | PASS |
| `all_trainable` | Deferred by user; absent from formal config and SyncMate recipes | PASS |
| Cache Store | E8 uses the canonical shared Cache V2 Store at `results/cache_v2` with one `index.sqlite` for ScoreBundle and Selection Artifacts; legacy/public/surrogate results are not inputs | PASS |
| Cross-ratio score semantics | Current 17 prefix-stable methods share one immutable ScoreBundle per dataset/seed; 1%/5% Selection recipes remain distinct; budget-conditioned methods require a separate score recipe | PASS |
| Selection evidence | One cold 17-way ScoreBundle, cold 1%/5% Selection projection, strict warm reads for both ratios, per-method timing, peak GPU memory, failure state, checkpoint identity | PASS |
| Downstream evidence | Attack, collateral, predictions, metadata, exact Selection Artifact and checkpoint provenance | PASS |
| Formal start | Requires accepted preparation line on clean pinned SSH `main`, GPU, environment, profiles, and SyncMate acceptance | BLOCKED |

## Prepared implementation

The branch adds a frozen target-direct formal configuration and one bounded
executor. It exposes:

- one import-safe deterministic split implementation shared by native OpenGU
  and target-direct, with explicit ratios and either a split seed or caller
  Generator; the no-local-RNG path preserves native global-RNG behavior;
- a thin profile layer that retains canonical path enforcement, manifests,
  file hashes, mask disjointness/exhaustiveness, and Selection candidate
  identity without owning a second split algorithm;
- 9 static Selection recipes, one per dataset/seed cell, each producing both
  ratio projections from one immutable ScoreBundle;
- 2 formal Cora/seed42/degree GNNDelete gate recipes, one for 1% and one for 5%;
- 18 static candidate downstream recipes (dataset/seed/ratio), each bounded to
  17 selectors and 68 artifacts (306 cells / 1,224 artifacts in total), with
  execution explicitly unauthorized;
- immutable cold-1%, cold-5%, warm-1%, warm-5%, and receipt evidence for each
  Selection stage;
- collector-side checksum and scientific-identity checks;
- ratio-specific manifest/config identity: `degree` is first in each ratio, each
  gate runs `--limit 1`, and any later explicitly authorized full stage for that
  ratio must use the same config/fingerprint and resume its accepted degree cell.

E8 consumes the canonical shared Cache V2 Store at `results/cache_v2` and its
single `index.sqlite`; the Store is not scoped by experiment, dataset, seed,
or stage. Its reviewable, experiment-owned products remain isolated under
`results/runs/target_direct_formal_v2/{selection,checkpoints,evidence,runtime,gu}`.

The manifest builder now permits an approved seed subset for a gate/stage while
still requiring the exact 17-method set. It rejects any summary whose scope is
not `last_layer`, whose Git provenance is dirty or different, whose `k` does not
derive from the verified candidate pool, or whose checkpoint data identity
differs from the processed profile.

## Git state

| Item | Value |
|---|---|
| Preparation branch | `codex/fix-target-direct-formal-orchestration-20260724` |
| Original audited parent | `main@41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` |
| Current local/origin/SSH main | `fb0d9a332c4086e98c6c988d6a02851a8d7a2b79` |
| Implementation commit | `a4db487d95e1de0e1210331fbdbc0b83c1749201` |
| SyncMate registration commit | `ffb474c` |
| Deferred-stress correction | `47569f9c96066038abbada24bc0d98d98650723f` |
| Preflight report commits | `27690db`, `264b389` |
| Merge/push performed by this task | No |

This is a pre-integration audit with a fixed temporal boundary. After repository
closeout, Git reachability and the final closeout report—not the historical
“unmerged” wording below—are authoritative for acceptance state.

`main` advanced while this task was active. A read-only overlap audit found no
newer-main edits to the target-direct modules, formal config,
`scripts/syncmate/syncmate.py`, or their tests. That reduces conflict risk but
does not authorize integration. The preparation line must still be accepted
through the repository Git workflow before formal work.

## Validation evidence

| Check | Result |
|---|---|
| Dual-budget runner/manifest/SyncMate suite | **197 passed** |
| Final expanded targeted suite | **242 passed, 1 warning in 10.73 s** |
| Shared split/native/target-direct/provider suite | **28 passed** |
| Python compilation | PASS |
| `git diff --check` | PASS |
| Local formal Selection preflight | Correctly blocked: feature branch/dirty during development, wrong checkout, missing profile, incompatible RTX 5070 |
| Canonical GU dry-run entries | Both 1% and 5% correctly blocked before runner load because real G1/G2 profile, checkpoint, manifest, and Selection evidence do not exist |
| Candidate expansion preflight | Correctly adds `306-cell candidate expansion is not authorized` and requires both ratio gates |
| SyncMate temporary smoke | PASS; 3/3 disposable artifacts collected and verified, temporary root cleaned |
| Formal jobs launched | **0** |

The warning is the existing CuPy CUDA-path probe. The local RTX 5070 is
incompatible with the pinned PyTorch/CUDA stack and is not accepted for formal
execution.

## SSH and SyncMate readiness

Latest read-only SSH evidence:

| Check | Observation | Verdict |
|---|---|---|
| Git | Clean `main...origin/main` at `fb0d9a33` | PASS |
| GPU | `nvidia-smi`: `No devices were found` | BLOCK |
| k5 contention | No GPU exists to contend for; this is not a wait-on-k5 state | BLOCK |
| Python environment | `/root/miniconda3/envs/gnn_20/bin/python` absent | BLOCK |
| Raw datasets | Canonical `data/raw/{cora,citeseer,pubmed}` caches present | PASS |
| Processed profiles | No `planetoid_70_10_20_seed2024` pair/manifest for any dataset | BLOCK |
| SSH SyncMate runner | `.syncmate/device.yaml` present as runner `gpu4090` | PASS |
| Local SyncMate collector | Ignored config prepared as `local-gu-controller` with exact peer/path/result roots | PASS |
| SyncMate transport dry-run | Blocked at missing remote `gnn_20` executable; no files collected | BLOCK |

SyncMate has not submitted a queue job. Its dry-run contacted the peer only for
status/manifest discovery and returned a fail-closed error for the missing
interpreter.

## Why `last_layer` is retained without an `all_trainable` run

This is a computational-scope decision, not a claim that last-layer and
all-parameter influence are scientifically equivalent.

- Koh and Liang's classical deep-learning IF implementation relies on gradients
  and Hessian-vector products to avoid explicit inverse-Hessian construction.
  This establishes the core scalability pressure.
  [ICML 2017 paper](https://proceedings.mlr.press/v70/koh17a.html)
- TracIn lists “cherry-picking layers of a deep neural network” as one of its
  explicit scaling mechanisms.
  [NeurIPS 2020 paper](https://proceedings.neurips.cc/paper/2020/hash/e6385d39ec9394f2f3a354d9d2b88eec-Abstract.html)
- Yeh et al. state that following influence through all parameters is often
  computationally infeasible for large models and that methods commonly select
  the last layer. They also show a cancellation limitation for last-layer
  influence in language models. The first point supports feasibility; the
  second prevents overclaiming general equivalence.
  [NeurIPS 2022 paper](https://proceedings.neurips.cc/paper_files/paper/2022/hash/d07022783ff6f7bf7a288c207b7dcbd1-Abstract-Conference.html)
- FastIF reports that standard IF cost scales poorly with model/data size and
  obtains large speedups through candidate restriction and faster IHVP
  estimation.
  [EMNLP 2021 paper](https://aclanthology.org/2021.emnlp-main.808/)
- Scaling Up Influence Functions introduces an Arnoldi inverse-Hessian
  approximation to reach full-size Transformer models, reinforcing that
  all-parameter IF requires a separate scalable-method study.
  [paper](https://arxiv.org/abs/2112.03052)

Therefore the current E8 claim boundary is:

1. formal results describe the reviewed `last_layer` target-direct estimators;
2. they do not claim equality to an all-parameter IF computation;
3. `all_trainable` is not configured, scheduled, or required for this matrix;
4. any future all-parameter study would need a separate cost/approximation
   contract and fresh Cache V2 identity.

## Exact blockers

1. The preparation branch, including the dual-budget revision, is not accepted
   into current `main`.
2. The SSH host exposes no GPU device.
3. The accepted `gnn_20` interpreter is absent.
4. The approved 70/10/20 OpenGU processed profiles are absent.
5. Consequently, real target checkpoints, cold/warm Selection receipts,
   external manifests, and canonical runner dry-run evidence do not exist.

## Approved continuation sequence

After infrastructure is restored and Git integration is explicitly authorized:

1. accept the preparation branch through the recorded parent workflow;
2. fast-forward the SSH active checkout to the exact accepted full `main` SHA
   and record it;
3. stage and verify all three processed profiles before timing;
4. run the Cora/seed42 Selection recipe and collect/verify its five artifacts,
   including one shared ScoreBundle identity and both ratios' cold/warm evidence;
5. run the canonical GNNDelete dry-run separately against the real 1% and 5%
   manifests/checkpoint;
6. run and accept the Cora/seed42/degree 1% formal gate (4 artifacts);
7. run and accept the separate Cora/seed42/degree 5% formal gate (4 artifacts);
8. stop at canary acceptance unless the user explicitly authorizes the
   306-cell candidate expansion;
9. if authorized, run ratio-specific stages sequentially through SyncMate and
   accept each only after exact artifact collection, SHA-256 verification,
   checkpoint/scope/ratio checks, and downstream metric parsing.

No step in this sequence may reuse the old public-split, surrogate, fixed-`k=7`,
or wrong-budget evidence as a formal input.
