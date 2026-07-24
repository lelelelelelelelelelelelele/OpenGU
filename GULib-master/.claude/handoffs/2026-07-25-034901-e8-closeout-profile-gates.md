# Handoff: E8 closeout, deterministic profiles, and dual-budget gates

## Session Metadata

- Created: 2026-07-25 03:49:01 +08:00
- Project: `C:\Users\ADMIN\.codex\worktrees\b8ad\OpenGU\GULib-master`
- Branch: `codex/fix-target-direct-formal-orchestration-20260724`
- Session duration: multi-session E8 preparation and split audit

### Recent Commits

- `e44b3e3` — `refactor(data): share deterministic node split`
- `c4a3ad1` — `fix(experiments): add dual-budget target-direct canaries`
- `af3f59b` — `docs(reports): fix preflight acceptance boundary`
- `264b389` — `docs(reports): normalize preflight markdown`
- `27690db` — `docs(reports): record target-direct formal no-go`

## Handoff Chain

- **Continues from**:
  `.claude/handoffs/2026-07-22-043748-small-selection-gu-syncmate-readiness.md`
- **Supersedes**: the prior handoff for current E8 readiness and execution state

## Current State Summary

The E8 target-direct implementation line is complete, committed, locally
validated, and clean, but not accepted into `main`. It now uses one public
deterministic split implementation for native OpenGU preprocessing and E8
profile staging, preserves the leakage-safe 70/10/20 profile, and supports
separate 1%/5% train-candidate deletion budgets. No formal profile, Cache V2
artifact, result, or job has been created. The next session must first close
Git locally and on SSH, then stage/verify the three profiles, then run the two
Cora/seed42/degree formal gates only when environment and GPU requirements are
genuinely satisfied.

## Codebase Understanding

### Architecture Overview

- `utils/node_split.py` owns deterministic node partitioning, masks, sorted
  indices, and induced split edges without importing `config.py`.
- `utils/dataset_utils.py::transductive_split_node` preserves native global-RNG
  behavior and optionally forwards an explicit split seed or Generator.
- `experiments/target_direct_v1/split_profile.py` is the formal evidence layer:
  canonical paths, materialization/verification, file hashes, graph/split
  contracts, disjoint/exhaustive masks, and Selection candidate identity.
- `experiments/target_direct_v1/run_selection.py` includes the shared split
  helper in its producer source fingerprint.
- `experiments/target_direct_v1/syncmate_stage.py` and
  `experiments/configs/syncmate_target_direct_formal_v2.yaml` own bounded
  Selection/GU orchestration and dual-budget identity.

### Critical Files

| File | Purpose | Relevance |
|---|---|---|
| `utils/node_split.py` | Shared deterministic split | Single algorithm source |
| `experiments/target_direct_v1/split_profile.py` | Stage/verify formal profiles | G1 data gate |
| `experiments/configs/syncmate_target_direct_formal_v2.yaml` | Frozen E8 contract | Ratios, expected counts, roots |
| `experiments/target_direct_v1/syncmate_stage.py` | Bounded stage executor | Preflight, Selection, GU gates |
| `reports/target_direct_formal_preflight_AUDIT_REPORT.md` and `.html` | Formal readiness evidence | Human acceptance pair |
| `reports/target_direct_selection_PREPARATION_REPORT.md` and `.html` | Scientific contract | Split/budget/checkpoint semantics |
| `self/dashboard/WORKPLAN.md` | Live source of truth | Current authorization and blockers |

### Key Patterns Discovered

- A data split and a deletion budget are orthogonal identities.
- Formal preprocessing is untimed and performed once per dataset; model seeds
  share the same deterministic split.
- Formal execution starts only from a clean, pinned, accepted SSH `main`.
- Current methods share one budget-independent ScoreBundle per dataset/model
  seed, while Selection Artifacts remain ratio-conditioned.
- New E8 roots are isolated under `target_direct_formal_v2`; legacy/public
  split/fixed-k/surrogate artifacts cannot be formal inputs.

## Work Completed

### Tasks Finished

- [x] Bound Selection and GNNDelete to the exact same target checkpoint.
- [x] Add bounded SyncMate stages and fail-closed formal preflight.
- [x] Replace one 5% canary with distinct 1% and 5% canaries.
- [x] Remove `all_trainable` from executable scope; retain `last_layer`.
- [x] Share deterministic split code between OpenGU and E8.
- [x] Validate import safety, deterministic identity, ratios/counts,
  disjoint/exhaustive masks, induced edges, native compatibility, and exact
  native-to-target-direct equivalence.
- [x] Commit split refactor as full SHA
  `e44b3e3d990aba82561bee759c5ff57c800f8d27`.

### Files Modified

All implementation and paired-report changes are committed through `e44b3e3`.
The E8 worktree was clean before this handoff document was created.

### Decisions Made

| Decision | Options Considered | Rationale |
|---|---|---|
| E8 split is 70/10/20 with seed 2024 | Public 140/500/1000; OpenGU 80/0/20 | IF target needs a disjoint validation objective without test leakage |
| Candidate pool is the full 70% train set | Public train set; fixed top-7 | Formal budget must reflect actual trainable candidates |
| Deletion ratios are 1% and 5% | Single 5%; exact k=7 | Align with modern-IM budget semantics |
| Main parameter scope is `last_layer` | `all_trainable` stress ladder | User deferred the high-cost stress run |
| Old 153 cells are diagnostic only | Reuse as formal; delete blindly | Wrong split/k/checkpoint identity but still useful provenance |
| Close Git before formal profiles/jobs | Run from feature worktree | Repository formal workflow requires accepted pinned main |

## Pending Work

## Immediate Next Steps

1. Run the `opengu-git-ssh-closeout` read-only audit and review both clean
   short-lived lines currently present:
   - `codex/docs-daily-log-blocks-20260724@3ef14ee`
   - `codex/fix-target-direct-formal-orchestration-20260724@e44b3e3`
2. With explicit closeout authority, accept each reviewed coherent line into
   `main` using separate `--no-ff` merge commits, run combined targeted tests
   and dry-runs, push `main`, fast-forward the clean SSH checkout, then remove
   only verified merged short-lived branches/worktrees. Preserve backup
   branches and stashes.
3. From the clean SSH active checkout at the exact accepted `main` SHA, restore
   or prove an accepted formal Python environment, then stage and verify the
   three deterministic profiles once:
   - Cora: 1895/271/542
   - CiteSeer: 2328/333/666
   - PubMed: 13801/1972/3944
4. Run Cora/seed42 Selection and verify one cold ScoreBundle, both ratio
   projections, both strict warm reads, checkpoint identity, timing, VRAM, and
   failure state.
5. Run canonical GU dry-runs separately for 1% and 5%, then run and accept the
   Cora/seed42/degree 1% gate and the separate 5% gate.
6. Stop after the two gates. The 306-cell candidate expansion is not authorized
   unless the user explicitly grants it after reviewing gate evidence.

### Blockers/Open Questions

- [ ] SSH is reachable, but `nvidia-smi -L` currently says `No devices found`.
- [ ] `/root/miniconda3/envs/gnn_20/bin/python` is absent.
- [ ] `/root/miniconda3/bin/python` has PyTorch 2.1.2+cu118 and PyG 2.6.1 but
  CUDA is unavailable; do not silently substitute it as the accepted formal
  environment.
- [ ] No `planetoid_70_10_20_seed2024` processed profile exists yet.
- [ ] The E8 branch is currently 8 commits ahead and 11 behind
  `main@6427743540a2c8802288dbff01be1c231b10b91d`.

### Deferred Items

- Full `3 datasets × 3 seeds × 17 selectors × 2 ratios = 306` expansion:
  candidate only, not authorized.
- Physical deletion of old diagnostic results/caches: requires a separate exact
  inventory, hashes, and explicit target approval. Fresh V2 identities already
  prevent reuse.
- `all_trainable`: not configured or scheduled.

## Context for Resuming Agent

## Important Context

- Read root `AGENTS.md`, root `CLAUDE.md`, `docs/GIT_WORKFLOW.md`,
  `self/dashboard/WORKPLAN.md`, and relevant cache/dashboard `CLAUDE.md` files
  before acting.
- Use `opengu-git-ssh-closeout` for Git acceptance and cleanup.
- Local main, origin/main, and SSH main currently equal full SHA
  `6427743540a2c8802288dbff01be1c231b10b91d`.
- Primary local worktree is clean on
  `codex/docs-daily-log-blocks-20260724@3ef14ee`; the Codex E8 worktree is clean
  on `codex/fix-target-direct-formal-orchestration-20260724@e44b3e3` before
  this tracked handoff.
- Preserve backup branches and all local/SSH stashes.
- Do not run formal profiles/jobs from a feature worktree.
- Do not confuse 70/10/20 with 1%/5%.
- Do not use the public 140/500/1000 split, OpenGU 80/0/20 split, fixed k=7,
  or the old surrogate checkpoint as new formal inputs.
- Formal Cora budgets are derived from the verified 1895 candidates:
  k=18 at 1%, k=94 at 5%.

### Assumptions Made

- Raw Cora/CiteSeer/PubMed adapter caches remain complete inside the SSH active
  checkout.
- Existing profile staging code will be used only after the full improvement
  line is accepted.
- SyncMate remains the preferred recoverable orchestrator once the runner
  environment is restored.

### Potential Gotchas

- `config.py` parses CLI arguments at import time; use the pure helper for
  lightweight split tests.
- A dry-run is validation, not a formal result.
- The two ratio gates are separate acceptance requirements.
- An apparently available local RTX 5070 is incompatible with the pinned local
  PyTorch stack and is not a formal runner.
- The historical May Cora matrix used 2166 train candidates and selected 108 at
  5%; the July 153-cell lane used public 140 candidates and k=7. Do not merge
  their identities.
- Do not delete old evidence as part of Git closeout.

## Environment State

### Tools/Services Used

- SSH alias: `autodl-opengu`
- SSH active checkout: `/autodl-fs/data/OpenGU/GULib-master`
- Local test interpreter: `E:/conda_package/envs/gnn/python.exe`
- SyncMate local device id: `local-gu-controller`
- SyncMate runner id: `gpu4090`

### Active Processes

- No formal E8 process or queue job was started.
- No process is intentionally left running by this handoff.

### Environment Variables

- No task-specific environment variables are required or recorded.

## Related Resources

- `.claude/handoffs/2026-07-22-043748-small-selection-gu-syncmate-readiness.md`
- `reports/target_direct_formal_preflight_AUDIT_REPORT.md`
- `reports/target_direct_selection_PREPARATION_REPORT.md`
- `experiments/configs/syncmate_target_direct_formal_v2.yaml`
- `self/dashboard/WORKPLAN.md`
- `docs/GIT_WORKFLOW.md`

---

**Security check required:** run `validate_handoff.py` before using this
handoff in another session.
