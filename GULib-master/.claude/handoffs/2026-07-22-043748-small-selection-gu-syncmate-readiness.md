# Handoff: Small-graph selection to GU outcomes and SyncMate readiness

## Session Metadata

- Created: 2026-07-22 04:37:48 Asia/Shanghai
- Project: `E:\project\OpenGU\GULib-master`
- Local handoff branch: `codex/docs-small-selection-gu-handoff-20260722`
- Intended implementation parent: `main@894a714c1c1b592ff9ba22a9ef06f6899b57ba4e`
- Session duration: approximately 2 hours of audit, clarification, and SSH preflight

### Recent Commits

- `894a714` merge: enforce k5 one-cell formal gate
- `337ed6c` docs(dashboard): reconcile staged k5 plan
- `e9bdae1` merge: sync current main into k5 gate fix
- `70ab9de` fix(baseline): require formal k5 one-cell gate
- `e12a4f8` merge: accept grandfathered selection benchmark

## Handoff Chain

- **Continues from:**
  [`2026-07-15-155534-understand-if-abc-target-loss.md`](./2026-07-15-155534-understand-if-abc-target-loss.md)
- **Supersedes:** the execution portion of the older handoff's plan-only state;
  its A/B/C conceptual explanation remains authoritative.

## Current State Summary

The accepted SSH public-Planetoid 17-output selection benchmark is complete and
must not be rerun merely to repeat the same selection analysis. The user has now
clarified the actual downstream research questions: (1) whether proper TracIn
is stronger than degree, IM, random, and other selectors under real GU outcomes;
and (2) which IF-family formula is most effective while remaining feasible.
The earlier suggestion to compress the experiment to six generic representatives
was rejected because it destroys the structured IF ablation. The unrelated
459-row CPU set-deletion/retrain diagnostic is explicitly shelved and is not GU.

SSH hardware and the active checkout are ready: a clean `main@894a714...`, an
idle RTX 4090, and canonical public raw datasets are present. SyncMate is only
partially ready. The remote runner setup passes preflight and its queue is valid,
but no runner-agent is serving, the local collector has no `device.yaml`, the
allowlist has no GU/IF downstream recipe, and a bounded smoke job correctly
blocked on stale smoke-recipe metadata. No formal experiment was launched.

## Codebase Understanding

## Architecture Overview

The work has three distinct layers which must not be conflated:

1. **Selection benchmark:** one trained public-split GCN cell produces a shared
   ScoreBundle containing 17 score/ranking outputs. This layer measures ranking,
   cold/warm behavior, shared compute, memory, and selection failures.
2. **Selector-to-GU integration:** a selected top-k node set becomes an explicit
   OpenGU unlearning-task input with immutable Selection Artifact provenance.
3. **GU outcome:** GNNDelete, GraphEraser, or another OpenGU updater produces the
   four-file result cell and is compared with exact retraining.

The 17-output bundle is a structured formula grid, not 17 arbitrary alternatives:

| Group | Methods | Question |
|---|---|---|
| Controls | `random`, `degree` | budget and structural baselines |
| A/B | `a_grad_norm`, `b_param_hutch` | raw gradient magnitude vs predicted parameter movement |
| C-point | `r_point`, `p_point`, `tracin_cp_point_3`, `tracin_cp_point_6` | point-source IF and checkpoint approximations |
| C-simple | `gt_simple`, `p_simple`, `tracin_cp_simple_3`, `tracin_cp_simple_6` | `grad1` source and approximations |
| D-full | `gt_full`, `p_graph`, `tracin_cp_graph_3`, `tracin_cp_graph_6` | graph-deletion `grad1-grad2` source and approximations |
| Negative control | `legacy` | deployed cross-gradient legacy behavior |

Only the point checkpoint variants are close to standard TracInCP. The simple
and graph checkpoint variants are project-specific source ablations. `legacy`
is not proper TracIn. The existing `proper-tracin-v1` gate is only a real
Cora/GCN/seed-2024 selection canary; it is not a three-dataset result and has no
GU outcome.

The existing 17-output GT uses the public Planetoid fixed split. It may be reused
unchanged only in a controlled public-profile GU experiment using the same
selector model, split, and candidate identity. It cannot be relabeled as an
OpenGU 80/20 canonical result. A formal canonical GU result must recompute every
included model-dependent selector on the exact OpenGU split/model/checkpoints;
it need not recompute selectors excluded from the hypothesis-focused matrix.

## Critical Files

| File | Purpose | Relevance |
|---|---|---|
| `self/dashboard/WORKPLAN.md` | current operational source of truth | read first; formal placement and GT exception live here |
| `reports/small_graph_selection_BENCHMARK_REPORT.md` and `.html` | accepted public 17-output SSH GT | ranking/resource authority; no automatic GU authority |
| `reports/bc_target_matrix_REPORT.md` and `.html` | A/B/C/D taxonomy and historical CPU deletion diagnostic | formula map and motivation; not a GU result |
| `docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md` and `.html` | proper-TracIn selection gate | establishes terminology and current one-cell scope |
| `experiments/bc_target_v2/benchmark_selection.py` | 17-output benchmark runner | source of accepted public selection evidence |
| `experiments/bc_target_v2/syncmate_recipe.py` | bounded small-selection executor | currently selection-only and CUDA-bound |
| `scripts/syncmate/syncmate.py` | queue, recipe allowlist, collection, and gates | requires reviewed GU recipe and smoke repair |
| `scripts/syncmate/README.md` | user-facing SyncMate contract | dispatch/agent/collector workflow |
| `scripts/syncmate/CLAUDE.md` | SyncMate guardrails | no arbitrary job commands; verified collection only |
| `reports/dataset_layout_AUDIT_REPORT.md` and `.html` | canonical dataset inventory | distinguishes public raw from OpenGU processed pairs |
| `.planning/ssh_downstream_gt_20260722/task_plan.md` | shelved CPU diagnostic plan | explicitly not the GU execution plan |

### Key Patterns Discovered

- Keep **attack strength** and **feasibility** as separate axes. Strength should
  use retrain gap/deletion residual with retained/test utility as a constraint;
  feasibility should use cold compute, component prerequisites, peak memory,
  cache behavior, and failure state.
- Do not select a generic representative subset before preserving the formula
  contrasts. At one primary budget, running all 17 GU outcomes is scientifically
  reasonable because it retains the complete A/B/C/D grid.
- The accepted ScoreBundle shares intermediates. Per-method selection materialize
  time is not the standalone formula production cost. Feasibility claims need
  component timings or a separate method-isolated benchmark.
- Formal one-cell gates are real matrix cells and run only from accepted, clean,
  pinned SSH `main`; branch smokes are disposable and non-formal.
- Queue completion is not acceptance. SyncMate must collect, checksum-verify,
  index, and gate the artifacts before aggregation.

## Work Completed

### Tasks Finished

- [x] Accepted the 9-cell, 17-output public selection GT as a one-time
  grandfathered authority without requesting a duplicate GPU rerun.
- [x] Clarified that the old 459-row CPU set-deletion/retrain matrix is a
  selection-effect diagnostic, not OpenGU graph unlearning.
- [x] Reframed the downstream design around the user's two actual questions:
  proper TracIn vs baselines and IF-formula effect/feasibility.
- [x] Audited the 17-method A/B/C/D factorial structure and proper-TracIn naming.
- [x] Verified SSH active root, exact Git SHA, clean branch, GPU availability,
  Python/CUDA stack, idle process state, disk, raw datasets, and processed files.
- [x] Verified remote SyncMate runner preflight, queue schema, allowlist, and
  selection-recipe preflight.
- [x] Ran one pinned, allowlisted SyncMate smoke job. It fail-closed to `blocked`
  before execution and produced no OpenGU result.
- [x] Created this validated handoff on a short-lived documentation branch.

## Files Modified

| File | Changes | Rationale |
|---|---|---|
| `.claude/handoffs/2026-07-22-043748-small-selection-gu-syncmate-readiness.md` | created current state and next-session instructions | enable a clean new session |
| `.planning/ssh_downstream_gt_20260722/task_plan.md` | marked the CPU diagnostic plan shelved/non-GU | prevent accidental execution as the formal outcome |
| `.planning/ssh_downstream_gt_20260722/progress.md` | recorded scope correction | preserve why the 459-row plan was stopped |

Do not stage `reports/small_graph_selection_BENCHMARK_REPORT.md` merely because
local `git status` shows `M`: its working-tree blob hash equals the HEAD blob
`51d0cfabbc3f6780771fc499dfe7a829a04b370a`; this is a stat/line-ending anomaly
that predates the handoff branch.

## Decisions Made

| Decision | Options Considered | Rationale |
|---|---|---|
| Do not rerun the accepted public 17-output benchmark | rerun all 9 cells; grandfather existing GT | source bytes and scorer semantics were verified; duplicate compute adds no evidence |
| Withdraw the six-representative GU proposal | six generic methods; hypothesis-preserving grid | six methods cannot answer the IF internal-formula question |
| Use all 17 at the primary budget for a controlled screen | all budgets; one budget; small subset | `k=7` preserves formulas at 153 GU cells per GU method without a 3x budget expansion |
| Add proper TracIn and IM explicitly | call checkpoint/legacy outputs TracIn; omit IM | neither the final proper-TracIn matrix nor IM is contained in the accepted 17 |
| Treat public and canonical GU lanes separately | reuse public IDs as canonical; recompute everything | model-dependent selectors require exact split/model/checkpoint identity |
| Keep SyncMate fail-closed | bypass queue after smoke failure; repair/extend recipe metadata | formal evidence must not use arbitrary SSH commands or stale binding metadata |

## Pending Work

## Immediate Next Steps

1. **Choose and record the experiment lane before coding.** Recommended staged
   design: a controlled public-profile screen that reuses the accepted rankings,
   followed by an OpenGU-canonical confirmatory shortlist. Do not silently mix
   their node IDs or claims.
2. **Create a new implementation branch from current `main`, not from this docs
   branch.** Implement the selector-to-unlearning-task adapter, immutable input
   provenance, the GU recipe/config, the machine acceptance manifest, and tests.
3. **Repair and extend SyncMate as reviewed code.** Fix the stale generic smoke
   binding, add a static GU/IF recipe with exact config SHA and reachable
   introduced Git SHA, define its four-file artifact policy/collector profile,
   and test blocked/failed/done behavior.
4. **Configure the local collector only after the artifact contract is frozen.**
   Initialize the local `.syncmate` device configuration, add peer `gpu4090` via SSH alias
   `autodl-opengu`, use `/root/miniconda3/bin/python`, and validate a dry-run.
5. **Merge through the recorded parent chain only with explicit user approval.**
   After the complete line reaches `main`, pin one full SHA and run a formal
   Cora/seed42/k=7/GNNDelete gate from the clean SSH active checkout. Expand only
   if the gate and SyncMate collection/verification pass.

### Proposed Hypothesis-Preserving Matrix

For a controlled public-profile GNNDelete screen, the initial primary budget can
be `k=7`:

- existing 17 methods x 3 datasets x 3 seeds = **153 GU cells**;
- add `proper-tracin-v1` and IM only after they are aligned to this profile,
  giving 19 x 3 x 3 = **171 GU cells**;
- do not expand every method to `k=3/14` initially;
- run budget sensitivity and a second GU family only on a preregistered set such
  as `random`, `degree`, IM, proper TracIn, `r_point`, `p_point`, `gt_full`, and
  `p_graph`.

For formal OpenGU-canonical confirmation, recompute only the included selectors
on the exact canonical split/model. A reasonable core is:

- question 1: `random`, `degree`, IM, deployed legacy, proper TracIn;
- question 2: `a_grad_norm`, `b_param_hutch`, `r_point/p_point`,
  `gt_simple/p_simple`, and `gt_full/p_graph`;
- optionally retain `tracin_cp_point_6` as a bridge to the public 17-output grid,
  but never relabel it as the production proper-TracIn result.

### Blockers/Open Questions

- [ ] **Experiment lane:** does the next result target a controlled public-split
  mechanism claim, an OpenGU-canonical paper claim, or both in sequence?
- [ ] **Proper TracIn coverage:** current accepted gate is only
  Cora/GCN/seed2024 selection-only; three datasets/seeds and GU integration are
  missing.
- [ ] **Canonical PubMed:** active SSH has Cora and CiteSeer transductive 80/20
  processed pairs, but no PubMed pair. A three-dataset canonical run is blocked
  until PubMed is generated through the accepted preprocessing flow.
- [ ] **SyncMate local collector:** local `.syncmate` device configuration is missing.
- [ ] **SyncMate GU recipe:** no allowlisted selector-to-GU recipe exists.
- [ ] **Generic smoke recipe:** expected config SHA is stale and its base Git
  binding references `a177e2c...`, which is absent from the remote object store.
- [ ] **Statistics:** three seeds support a paired screen, but a close
  TracIn-vs-degree result should expand only that comparison to five seeds before
  a strong significance claim.

### Deferred Items

- The 459-row CPU set-deletion/retrain diagnostic is shelved. It may remain as
  historical mechanism evidence but must not be called GU or run as a substitute.
- Full `k=3/7/14` x all selectors x multiple GU-family expansion is deferred
  until the `k=7` gate establishes runtime, correctness, and a stable effect.
- C.6 surrogate transfer remains a separate E7 question and must not be folded
  into the direct-selector comparison without an explicit model-identity design.

## Context for Resuming Agent

## Important Context

The user is correcting experimental logic, not merely asking for an execution
queue. Lead with the two hypotheses and use them to justify every method row.
Do not propose a generic compact subset that drops the C-point/C-simple/D-full
reference-proxy comparisons. Conversely, do not multiply all 17 by all budgets
and all GU methods before a one-budget gate.

The phrase "TracIn" is especially dangerous here:

- `legacy` = deployed cross-gradient legacy;
- `tracin_cp_point_{3,6}` = closest current B/C variants to standard TracInCP;
- `tracin_cp_simple_*` and `tracin_cp_graph_*` = project-specific source ablations;
- `proper-tracin-v1` = separately versioned formal recipe, currently only a
  one-cell selection gate.

Strength and feasibility must be reported separately. A selector is stronger
only if it increases the GU-vs-retrain discrepancy/deletion residual under the
same dataset, seed, budget, base model, and GU method; utility damage is a second
axis, not automatically success. A formula is feasible based on compute,
memory, prerequisites, cacheability, and failures. Select the final method from
an effect-cost Pareto frontier rather than one blended score.

## Assumptions Made

- The user still wants Cora/CiteSeer/PubMed with seeds 42/212/2024 as the small
  graph discovery scope.
- `k=7` is the primary budget because it is the middle registered budget and
  avoids immediate 3x expansion.
- GNNDelete is the first GU updater; GraphEraser is a later confirmation family.
- The SSH alias remains `autodl-opengu`; verify it again before any state change.

## Potential Gotchas

- Do not use the old public selection paths as OpenGU canonical provenance.
- Do not regenerate datasets during a timed formal run.
- Do not treat PyG's adapter `data.pt` as the OpenGU processed split pickle.
- Do not infer canonical processed filenames. Current files are
  `cora0.8_0_0.2{,dataset}.pkl` and
  `citeseer0.8_0_0.2{,dataset}.pkl`; PubMed is absent.
- Do not run formal cells from a feature/docs branch or a temporary worktree.
- Do not merge, push, delete branches, or clean the blocked smoke job without
  explicit authority.
- Do not start a long-lived runner-agent before the intended recipe is present
  on accepted `main` and the queue has been audited.
- The remote runner artifact policy currently includes only `cold.json`,
  `warm.json`, and `cell.json`; it is insufficient for GU four-file cells.
- The local tracked report stat anomaly must remain untouched unless the user
  explicitly asks to normalize it.

## Environment State

### SSH Active Checkout

- Path: `/autodl-fs/data/OpenGU/GULib-master`
- Git top-level: `/autodl-fs/data/OpenGU`
- Branch/HEAD: clean `main@894a714c1c1b592ff9ba22a9ef06f6899b57ba4e`
- Worktrees: only the active checkout is registered remotely
- GPU: NVIDIA GeForce RTX 4090, 24,564 MiB, idle at audit time
- Python: `/root/miniconda3/bin/python`
- Torch/PyG environment: torch `2.1.2+cu118`, CUDA available, one device
- Disk: approximately 196 GiB free under `/autodl-fs/data`
- Active experiment/runner processes: none after the audit

### Dataset State

- Public raw leaves present: `data/raw/cora`, `data/raw/citeseer`,
  `data/raw/pubmed`.
- OpenGU transductive processed pairs present: Cora and CiteSeer.
- OpenGU transductive processed pair missing: PubMed.

### SyncMate State

- Remote `.syncmate` device configuration: runner `gpu4090`, preflight `ready`.
- Remote artifact policy: `cold.json`, `warm.json`, `cell.json` only.
- Runner-agent: not serving; no lock; no active/running job.
- Queue: one blocked readiness smoke job,
  `readiness-smoke-20260722-0435`; no formal artifacts were produced.
- Existing small-selection MVP module preflight: `ready=true` on the active
  clean 4090 with canonical `data/raw/cora`.
- Local collector: blocked because its `.syncmate` device configuration is missing; no peers.
- Current allowlist: smoke, synthetic OpenGU preflight, Cache V2 gate4, and the
  three small-selection stages. There is no GU/IF downstream recipe.

### Tools/Services Used

- SSH alias: `autodl-opengu`
- Local project Python for repository checks:
  `E:/conda_package/envs/gnn/python.exe`
- System Python 3.13 was used only for the external session-handoff scaffold,
  because that skill uses `list[str]` syntax unsupported by repository Python 3.8.

### Active Processes

- No remote experiment or SyncMate runner-agent process is active.
- No local background process was started.

### Environment Variables

- None required or recorded.

## Related Resources

- `self/dashboard/WORKPLAN.md`
- `reports/small_graph_selection_BENCHMARK_REPORT.md`
- `reports/bc_target_matrix_REPORT.md`
- `docs/proper_tracin_v1_selection_gate_ACCEPTANCE_REPORT.md`
- `reports/dataset_layout_AUDIT_REPORT.md`
- `scripts/syncmate/README.md`
- `scripts/syncmate/CLAUDE.md`
- `docs/GIT_WORKFLOW.md`
- Previous A/B/C handoff linked above

---

**Security note:** this handoff contains no credentials, tokens, or raw host
secrets. Re-run the handoff validator after any edit.
