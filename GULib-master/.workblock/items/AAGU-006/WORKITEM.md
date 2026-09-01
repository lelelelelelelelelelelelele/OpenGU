# AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复

Block ID: `AAGU-006`

Item Version: 2.1

当前状态: `awaiting acceptance / candidate verified`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

> Git baseline：`9d36a30a38e3f90d4bc2081014c400037ed25404`

> Source branch：`refs/heads/codex/aagu-006-dataset-split-authority`

Execution topology: `parallel`

Parallel owner: `Codex` session `统计现有 Fix Blocks` branch `refs/heads/codex/aagu-006-dataset-split-authority`

Item Type: Block

## Human Surface

### 核心意图

让正式实验的数据划分成为可声明、可复用、可校验的独立数据状态，而不是由每次实验运行或随机种子临时重切。实验配置默认声明 `0.7 / 0.1 / 0.2` 的 train/validation/test 比例和固定 split seed；同一数据集与同一划分合同只生成一次，之后所有模型、selector 和 unlearning 实验消费同一份已持久化划分。

### 本次增量

复用 OpenGU 现有的“划分后保存 pickle、后续直接加载”基础设施，把当前 target-direct 的硬编码常量收敛为 YAML 驱动的通用 split profile 合同。运行代码读取配置中的比例、split seed 和 profile 身份：首次没有匹配 profile 时生成 masks、pickle 与 manifest；已有完全匹配的 profile 时直接命中并复用，不重新划分。Cache V2 不建立按 seed 分裂的新目录，但其 Recipe/Artifact 必须绑定实际 `split_hash` 和候选集身份，任何配置、manifest 与持久化数据不一致都 fail closed。

### 核心验收

- 正式实验 YAML 能显式声明并默认使用 `0.7 / 0.1 / 0.2` 与固定 split seed，运行入口不再用另一套硬编码比例覆盖注册内容。
- 真实冷路径测试会完成一次划分、保存可再次加载的 processed profile；真实热路径测试会命中同一 profile，证明没有重新划分或覆写，且不同模型、selector、unlearning seed 仍消费相同的 masks 与 `split_hash`。
- split 比例、split seed、profile、manifest、持久化 masks 或 Cache V2 输入身份发生冲突时会明确拒绝；测试同时证明复用了 OpenGU 的持久化数据加载路径，而不是另建 target-direct 私有数据系统。

## Orchestration contract

- Class: `FIX`
- Priority: `P0 / first`
- Source anchor: legacy WORKPLAN target-direct dataset/split conflict.
- Outcome: active planning and executable configuration point to one verified dataset/split identity; obsolete split/budget wording is removed from the active view rather than retained as a parallel lane.
- Fact owner: [target-direct formal v2 recipe](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml); `experiments/AGENTS.md` owns the operational boundary but does not duplicate the recipe values.
- Blocks: experiment-definition and target-direct execution nodes until accepted.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `data / research contract`.
- Minimum evidence: authoritative split identity, consistent owner links and recipe, contract tests/dry-run, and dashboard drift validation.
- Confirmation: user delegated registration now; confirm or correct this contract only when the Block is claimed for real execution.
- Report size: paired `REPORT.md` / `REPORT.html` after Verify because this Block changes the human-visible data/research contract; registration and claim create no empty report.

## Boundaries

- No IF scientific decision, selector choice, formal GPU run, result reinterpretation, or historical evidence deletion.
- Registration only; later execution must claim this exact locator.

## Status history

- 2026-08-26: registered from the prominent WORKPLAN dataset/split repair Todo under delegated registration authority.
- 2026-08-26: claimed by the Codex task `AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复` after the user explicitly said to start this P0 root Block.
- 2026-09-01: the user explicitly requested rework and authorized an in-place protocol 2.1 upgrade; the same locator now defines the reusable YAML-driven split-profile contract before Run resumes.
- 2026-09-01: the user selected single-owner `parallel` so this same source can resume truthfully in its existing linked worktree while canonical A remains owned by AAGU-024.

## Claim and runtime record

- Stable locator: `.workblock/items/AAGU-006/WORKITEM.md`; this task owns only Block `AAGU-006`.
- Registration baseline: `9d36a30a38e3f90d4bc2081014c400037ed25404` on parent `refs/heads/codex/e7-two-surrogate-groups-20260805`.
- Source branch/worktree: `codex/aagu-006-dataset-split-authority` at `C:\Users\ADMIN\.codex\worktrees\aagu006\OpenGU\GULib-master`.
- Inherited state: accepted AAGU-018 and the retained AAGU-019 registration landed on the Apply target at `6be95c74f230cbfcb6a99d0166ba8b1d143e5416`, then converged into this branch by merge checkpoint `77b03eb246a918d611c251927a65722ebb147c71`; AAGU-019 implementation remains outside this Block.
- Excluded state: no unrelated dirty state is present. AAGU-019 hard retirement, formal GPU execution, historical Artifact mutation, and scientific IF/selector decisions remain independently owned and excluded.
- Runtime profile: `local-git`; owned writes are limited to the dataset/split contract, its active consumers/generators, focused tests, and this item package.
- External boundaries: no formal GPU run, SSH write, live provider, historical Artifact mutation, push, install, Apply, cleanup, or destructive action is authorized before explicit acceptance.
- Candidate: the clean `codex/aagu-006-dataset-split-authority` `HEAD`; its verified implementation/parent-convergence checkpoint is `77b03eb246a918d611c251927a65722ebb147c71`, and this tracked Record/Report projection advances the live candidate normally.
- Evidence: `tests/test_dashboard_refresh.py`, the target-direct split/recipe/manifest/stage suites, `scripts/dashboard/refresh.py --check`, the registered local dry-run, and the paired `REPORT.md` / `REPORT.html` in this item directory.
- Current human surface: `.workblock/items/AAGU-006/REPORT.md` and `.workblock/items/AAGU-006/REPORT.html`.
- Restart point: wait for an explicit accept/reject decision. If accepted, invoke `block-closeout` with this same stable locator; if rejected, keep rework inside AAGU-006.

## Work events

- 2026-08-26 root cause: the executable target-direct formal recipe was already frozen to one reviewed profile and budget contract, but the human control plane had no machine-checkable connection between a WorkItem's declared fact owner and its WORKPLAN Owner. AAGU-006 pointed only to generic experiment guidance and AAGU-007 pointed to a broad DocMap overview, so historical public-split/fixed-small-k material could still look like a parallel execution authority even though the launcher would reject it.
- 2026-08-26 scope boundary: AAGU-006 owns active authority routing and fail-closed dashboard validation. AAGU-019 separately owns hard retirement of obsolete executable packages and historical publication inputs; this Block does not absorb that cleanup.
- 2026-08-26 baseline: the dashboard, split-profile, recipe and SyncMate stage suites passed `20/20` before implementation.
- 2026-08-26 RED: `test_drift_checks_reject_plan_owner_that_disagrees_with_workitem` failed because `validate_drift` returned no error for a real WorkItem authority link paired with a different WORKPLAN Owner.
- 2026-08-26 GREEN: dashboard parsing now resolves an explicit WorkItem fact-owner link against the WorkItem locator and rejects a semantically different WORKPLAN Owner. AAGU-006 and AAGU-007 both route to the registered formal-v2 recipe, while `experiments/AGENTS.md` states that historical public/80-20/fixed-small-k material cannot supply current executable values. The focused set passed `21/21`.
- 2026-08-26 registered dry-run observation: the Cora/seed42/1% degree-gate dry-run accepted the frozen recipe, then correctly stopped before execution on the non-main local candidate, non-AutoDL checkout, missing processed profile and Selection receipt, and unreviewed local GPU. It reported `generated_artifacts=[]`; this is fail-closed contract evidence, not a formal run.
- 2026-08-26 inherited dashboard gap: the registration baseline contains AAGU-018 without a WORKPLAN mapping, and the separately preserved AAGU-019 registration adds the same gap. Their owning task was given the exact `refresh.py --check` failures. Until those independent mappings land, global dashboard Verify remains incomplete rather than being hidden or repaired inside AAGU-006.
- 2026-08-26 parent convergence: AAGU-018 was explicitly accepted and no-ff applied at parent commit `6be95c7`. Its accepted AAGU-018/AAGU-019 mappings were merged into AAGU-006 while preserving this Block's recipe Owner for AAGU-006; the dashboard generator rebuilt all 19 WorkItems and passed drift validation.
- 2026-08-26 pre-review Verify: the combined AAGU-006 plus accepted-parent suite passed `67/67`; dashboard projection, corrected-root Python compilation, ancestry, clean-status, and diff checks passed. A repeated registered Cora/seed42/1% dry-run bound `HEAD=77b03eb`, accepted the formal-v2 recipe, then stopped only at the declared non-main/non-AutoDL/device/profile/receipt gates with `generated_artifacts=[]`.
- 2026-08-26 review correction: independent review reproduced that the noncanonical phrase `awaiting human acceptance` parsed as an unknown lifecycle and made the dashboard undercount WIP while still passing projection equality. The Record now uses the existing `awaiting acceptance / candidate verified` grammar, unknown lifecycle values fail drift validation, and WORKPLAN routes directly to the human decision instead of repeating claim/implementation.
- 2026-08-26 post-review Verify: three lifecycle regressions cover the canonical candidate status, fail-closed unknown status, and the retained AAGU-019 registration status. The combined suite passed `70/70`; the regenerated dashboard projects AAGU-006 as awaiting/WIP, reports two waiting decisions, and passes drift validation.

## Formal verification and decision note

- `PASS` — WORKPLAN routes executable AAGU-006 and AAGU-007 nodes to `syncmate_target_direct_formal_v2.yaml`; AAGU-015 keeps its scientific-definition Owner but is explicitly forbidden from reopening historical split/budget lanes.
- `PASS` — dashboard drift validation resolves explicit WorkItem fact-owner links and rejects a semantically different WORKPLAN Owner; its RED test failed before the implementation and passes now.
- `PASS` — the frozen recipe remains `planetoid_70_10_20_seed2024` with 1%/5% floor budgets and exact per-dataset candidate counts; the registered dry-run consumes it and fails closed before any invalid local formal execution.
- `PASS` — the accepted AAGU-018/AAGU-019 parent projection and AAGU-006 authority projection coexist in one regenerated dashboard; AAGU-006 is counted as awaiting/WIP and `70` combined tests pass on the converged branch.
- `NOT OBSERVED` — no formal AutoDL GPU cell, full matrix, downstream GU outcome, or scientific attack-effect result was run in this implementation Block.
- `NOT CONFIRMED` — AAGU-019's hard retirement of obsolete executable packages is not complete and is not claimed here.
- Agent recommendation: accept this candidate as the active dataset/split authority repair. This recommendation does not accept the Block; the user remains the decision owner.
