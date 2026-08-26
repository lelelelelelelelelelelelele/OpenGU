# AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复

Block ID: `AAGU-006`

当前状态: `awaiting acceptance / candidate verified`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Item Type: Block

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

## Confirmed acceptance brief

### 当前基线

目标实验的活跃计划、可执行配置和历史文字尚未收敛到一个可验证的 dataset/split 身份，因此后续实验定义与 target-direct 执行不能安全前进。

### 这次增量

把活跃规划和可执行配置统一到一个明确的 dataset/split 权威入口，删除活跃表面中并行保留的过时 split/budget 路径。

### 完成后人会看到什么

从 WORKPLAN 进入目标实验时，所有活跃链接和 recipe 都指向同一个已验证的数据/划分合同，不再有可被误执行的旧口径。

### 验收项目

- 活跃计划、owner 链接和可执行 recipe 对 dataset/split 的定义一致。
- 旧 split/budget 身份无法从当前正式入口启动，且没有用兼容分支保留第二条活跃路径。
- 不一致的 dataset/split 或预算身份会 fail closed，而不是静默改写或降级。
- 仓库的定向合同测试、注册 dry-run 和 dashboard drift 校验一致支持这个权威入口。

### 主要证据

- dataset/split 权威定义与活跃消费者对照：帮助判断是否真正只剩一个合同。
- 定向 RED/GREEN 合同测试和注册 dry-run：帮助判断正确路径可执行且冲突路径会被拒绝。
- WORKPLAN/dashboard 重建与 drift 检查：帮助判断人类可见状态没有继续引用旧口径。

### 关键 non-goals

- 不在本 Block 选择 IF/selector，不运行正式 GPU 实验，不重解释或删除历史证据。

### 需要人的决定

用户已批准按这个范围开工；Verify 完成后由用户对精确候选明确接受、拒绝或要求返工，验证通过不代表自动接受。

## Boundaries

- No IF scientific decision, selector choice, formal GPU run, result reinterpretation, or historical evidence deletion.
- Registration only; later execution must claim this exact locator.

## Status history

- 2026-08-26: registered from the prominent WORKPLAN dataset/split repair Todo under delegated registration authority.
- 2026-08-26: claimed by the Codex task `AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复` after the user explicitly said to start this P0 root Block.

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
