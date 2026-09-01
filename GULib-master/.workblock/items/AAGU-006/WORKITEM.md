# AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复

Block ID: `AAGU-006`

Item Version: 2.1

当前状态: `awaiting acceptance`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

> Git baseline：`9d36a30a38e3f90d4bc2081014c400037ed25404`

> Source branch：`refs/heads/codex/aagu-006-dataset-split-authority`

> Remote target：`origin refs/heads/codex/e7-two-surrogate-groups-20260805`

Execution topology: `parallel`

Parallel owner: `Codex` session `统计现有 Fix Blocks` branch `refs/heads/codex/aagu-006-dataset-split-authority`

Item Type: Block

## Human Surface

### 核心意图

让正式实验的数据划分成为可声明、可复用、可校验的独立数据状态，而不是由每次实验运行或随机种子临时重切。实验配置默认使用 `0.7 / 0.1 / 0.2` 和 split seed 2024，但允许注册任意总和为 1、满足对应实验目标语义的合法比例与非负 split seed。同一 dataset 与同一归一化 split contract 只生成一个持久化划分；不同合法合同拥有不同身份，从而同时保证复用和实验多样性。通用 OpenGU 可以保留零 validation 的合同；target-direct 因攻击目标取自 validation mask，只要求自己的注册比例提供非空 validation。

### 本次增量

复用 OpenGU 现有的“划分后保存 pickle、后续直接加载”基础设施，把 split mapping 设为唯一数据划分输入，并由 dataset family、归一化比例和 split seed 确定性派生 processed profile 与候选集合/数量。删除预算的 ratio 或固定 `k` 仍由实验注册独立拥有；若注册 ratio，运行时只把它投影到候选集合得到实际整数数量。`0.7`、`0.70` 等等价写法必须得到同一身份和同一 pickle 路径；首次 miss 生成 masks、pickle 与 manifest，后续命中直接复用。Cache V2 不建立 split-specific 根，但其 Recipe/Artifact 绑定实际 `split_hash` 和候选集身份；只有非法比例、不满足当前实验目标定义，或声明与持久化事实冲突时才 fail closed，不能因为比例不是默认值而拒绝。

### 核心验收

- 正式实验 YAML 显式声明 split mapping，当前 default 为 `0.7 / 0.1 / 0.2` 与 split seed 2024；另一组满足 target-direct 目标语义的合法比例能通过同一入口注册和运行准备，不被 default gate 拒绝。
- 同一 dataset + 等价 ratios + 同一 split seed 在多次运行和不同实验 seed 下得到同一 canonical profile、同一 pickle 路径与同一 `split_hash`；真实 cold/warm 测试证明只生成一次且不覆写。
- 不同合法 split contract 得到不同 profile 并可并存；非法比例、manifest、持久化 masks 或 Cache V2 输入身份冲突才明确拒绝。当前正式实验注册均能解析到显式 split mapping，且复用 OpenGU 持久化路径而非另建私有数据系统。

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
- Confirmation: the user explicitly requested this in-place rework and confirmed that AAGU-006 must use protocol 2.1 before the new candidate is presented.
- Report size: paired `REPORT.md` / `REPORT.html` after Verify because this Block changes the human-visible data/research contract; registration and claim create no empty report.

## Boundaries

- No IF scientific decision, selector choice, formal GPU run, result reinterpretation, or historical evidence deletion.
- Implementation and local verification only; formal GPU execution and every post-accept action remain outside this Run.
- No global prohibition or deletion of historical/alternate valid split profiles; diversity remains supported through canonical per-contract identities.

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
- Candidate: the clean `codex/aagu-006-dataset-split-authority` `HEAD`; implementation checkpoint `13083d6822ccaf23d1801732c4af3c16c7abe4d6` contains the valid-split code, and the tracked Record/Report projection advances the same ordinary candidate normally. Superseded candidate `40e45bba` was never Applied.
- Evidence: `250 passed, 1 deselected`, `scripts/dashboard/refresh.py --check`, the 29-recipe registration audit, the clean-checkpoint registered local preflight, and the paired `REPORT.md` / `REPORT.html` in this item directory.
- Current human surface: `.workblock/items/AAGU-006/REPORT.md` and `.workblock/items/AAGU-006/REPORT.html`.
- Restart point: wait for the user's decision on this same candidate; do not Apply, push, install, execute formal GPU work, or clean up without matching authority.

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
- 2026-09-01 rework Resume: installed block-workflow 2.1.2 validated a single-owner linked source, resumed this exact branch with three Git identity commands, and transitioned the existing Claim `eed658bd-1f4f-4eaf-b258-7dd607616064` to `ongoing` revision 4. AAGU-024 and its candidate remain unchanged.
- 2026-09-02 implementation Verify before candidate: the registered YAML split contract, OpenGU processed-pair cold/warm path, manifest/GU adapter identity, Cache V2 recipe identity and dashboard suites passed `111/111`. The real temporary PyG cold path wrote the pair and manifest once; the warm path returned `reused` with identical bytes and `mtime_ns`. A clean-candidate registered dry-run remains the next check.
- 2026-09-02 clean-candidate Verify: implementation checkpoint `439b876c` passed the same `111/111` set; the registered Cora/seed42/1% dry-run bound that clean SHA, failed closed on the declared local environment mismatches, returned `generated_artifacts=[]`, and left the exact profile absent with zero local processed files.
- 2026-09-02 acceptance surface: the paired Report has one valid Human Result and one pending decision projection. Browser inspection observed one decision, no horizontal overflow or broken images, readable desktop hierarchy, and all five intended evidence sections.
- 2026-09-02 acceptance rework: the user rejected frozen-default semantics. Default remains 70/10/20, but all legal split contracts must be accepted; equivalent contracts must converge on one persisted profile, while different legal contracts retain distinct identities. Candidate `40e45bba` and its Report are superseded without Apply.
- 2026-09-02 valid-split implementation: formal YAML now declares split and dataset node counts; canonical profile and candidate count are derived by both target-direct and SyncMate registration consumers, while the independently registered budget ratio or fixed `k` remains a separate experiment parameter. A valid 60/20/20 seed42 contract passes the same loader/direct-runner path, while real file tests prove equivalent default reuse and distinct-contract coexistence.
- 2026-09-02 valid-split Verify: implementation checkpoint `13083d68` passed `250` related tests with one installed-SyncMate-Core bootstrap test explicitly deselected. A registered local preflight bound that clean SHA, stopped at the declared environment/prerequisite gates with `generated_artifacts=[]`, and kept the processed file count at zero.
- 2026-09-02 valid-split acceptance surface: the rebuilt Markdown/HTML Report passed the report contract. Browser inspection observed one Human Result and one pending decision, no horizontal overflow, no broken images or console errors, and readable desktop hierarchy, decision and registration-evidence table.

## 2026-09-02 formal verification and decision note

- `PASS` — the formal YAML explicitly owns the current default `0.7 / 0.1 / 0.2`, split seed 2024 and materialize-on-miss; profile and candidate count are derived from split, while the deletion budget ratio or fixed `k` remains independently registered.
- `PASS` — valid `0.6/0.2/0.2 + seed42` passes the same loader and direct runner; it is not rejected for differing from the default.
- `PASS` — real PyG/file tests prove `0.7` and `0.70` reuse one pair without changing bytes, `mtime_ns` or `split_hash`, while another valid contract creates a distinct coexisting pair and split hash.
- `PASS` — AAGU-006/AAGU-007 and all 29 registered target-direct recipes consume the same formal-v2 YAML contract; Cache V2 keeps one root and binds exact split/candidate/target identities.
- `PASS · scoped` — `250` related tests pass with the unavailable installed-Core bootstrap test excluded; registered local preflight consumes the recipe and creates no formal split or experiment Artifact when formal gates are not met.
- `NOT CONFIRMED` — the independent SyncMate Core distribution is not installed in this local project interpreter; installed-package bootstrap is therefore outside the observed PASS set.
- `NOT OBSERVED` — no AutoDL RTX 4090 formal materialization, Selection/GU gate, full matrix or scientific result was run.
- Agent recommendation: accept the verified candidate. This is not human acceptance; the decision remains with the user.

## Superseded 2026-08-26 verification note

The observations below describe the previous candidate only. The 2026-09-01 Human Surface materially expands AAGU-006 to the executable split-profile contract, so the old Agent recommendation is no longer a current acceptance recommendation.

- `PASS` — WORKPLAN routes executable AAGU-006 and AAGU-007 nodes to `syncmate_target_direct_formal_v2.yaml`; AAGU-015 keeps its scientific-definition Owner but is explicitly forbidden from reopening historical split/budget lanes.
- `PASS` — dashboard drift validation resolves explicit WorkItem fact-owner links and rejects a semantically different WORKPLAN Owner; its RED test failed before the implementation and passes now.
- `PASS` — the frozen recipe remains `planetoid_70_10_20_seed2024` with 1%/5% floor budgets and exact per-dataset candidate counts; the registered dry-run consumes it and fails closed before any invalid local formal execution.
- `PASS` — the accepted AAGU-018/AAGU-019 parent projection and AAGU-006 authority projection coexist in one regenerated dashboard; AAGU-006 is counted as awaiting/WIP and `70` combined tests pass on the converged branch.
- `NOT OBSERVED` — no formal AutoDL GPU cell, full matrix, downstream GU outcome, or scientific attack-effect result was run in this implementation Block.
- `NOT CONFIRMED` — AAGU-019's hard retirement of obsolete executable packages is not complete and is not claimed here.
- Agent recommendation: accept this candidate as the active dataset/split authority repair. This recommendation does not accept the Block; the user remains the decision owner.
