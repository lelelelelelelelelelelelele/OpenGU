# AAGU-018 · 修复 D-GIF affected-source 标签越界

Block ID: `AAGU-018`

当前状态: `accepted`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Item Type: Block

## Source

- Anchor: `experiments/c_target_v1/core.py::graph_source_scores` currently forms graph-source losses from every two-hop affected node without restricting label-bearing loss terms to `train_mask`.
- Contract context: D-GIF target-direct selection may use the full transductive graph for message passing and `val_mask` for the explicit target direction, while `test_mask` labels remain outside selection.
- Baseline: the current E8 target-direct implementation exists and its formal matrix has not been executed as accepted evidence.

## Intent

- Why now: prevent validation/test neighbor labels from silently entering the D-GIF training-source gradients before formal E8 execution.
- Change: make the graph-source supervision set explicit and restrict `grad1` / `grad2` loss terms to two-hop affected training nodes.
- Human outcome: full-graph message passing and node-deletion structural intervention remain intact, while only training labels contribute to the source gradients.

## Scope

- Update `graph_source_scores` to receive an explicit training-source scope and intersect it with each candidate's affected set.
- Propagate the explicit source scope through the target-direct and BC-target callers.
- Preserve candidate deletion, incident-edge removal, validation-target direction, parameter scope, and stable ranking semantics.
- Add focused train/validation/test regression coverage and run proportionate targeted verification.
- Advance the semantic producer/Recipe identity and identify every affected historical Artifact or aggregate without deleting or overwriting it.
- Run one minimal real Cora selection canary after the focused tests pass.

## Non-goals

- Do not change the 70/10/20 split, 1%/5% budgets, model training, GU method, or full-graph message passing.
- Do not implement or run the three-dataset D-GIF/Degree/Random coverage experiment.
- Do not run the full E8 formal matrix.
- Do not delete, rename, repair, or overwrite existing Cache V2 Artifacts or historical results.
- Do not broaden this Block into a paper-faithfulness redesign beyond the confirmed label-scope defect.

## Acceptance contract

- Route: `formal`.
- Primary surface: scientific contract and data-flow correctness.
- Decision owner: human user; successful verification alone does not accept the Block.
- Report size: concise formal verification and decision note in this WorkItem unless the observed impact expands.

### Acceptance items

- Graph-source loss terms use labels only from affected training nodes.
- Validation/test node features and graph structure still participate in transductive message passing.
- With the target direction held fixed, changing a validation/test-only neighbor label does not alter the graph-source component; changing an affected training label still can.
- Candidate deletion and incident-edge removal retain their existing behavior.
- Affected methods receive fresh semantic evidence identity, while unaffected selectors and historical Artifacts remain untouched.

### Minimum evidence

- Focused toy-graph regression evidence covering train/validation/test neighbors and deleted-graph behavior.
- Targeted test results plus one minimal real Cora selection canary.
- Impact ledger naming the affected selectors and the historical Artifact/aggregate boundary.

## Context and relations

- Blueprint scope: E8 target-direct white-box selection and the D-GIF source contract in the A/B–C–D taxonomy.
- Confirmed Block relations: none.
- The later D-GIF/Degree/Random overlap analysis remains independent follow-up work.

## Registration and execution boundary

- Project config: `.workblock/project.json`.
- Previewed config digest: `5253e4083e30fdda8f4aaf9c7463f28023b6a06902de420e8a139eae6448b157`.
- Registration confirmation: user said `注册！` on 2026-08-26.
- Registration creates this Record and advances the project WorkItem counter only.
- A later user-visible Codex task must use `block-workflow`, claim this same locator, and create a scoped Git candidate before implementation.

## Status history

- 2026-08-26: registered from the confirmed Fix Block preview; ready for a separate execution task to claim.
- 2026-08-26: claimed by the Codex task `AAGU-018 · 修复 D-GIF affected-source 标签越界`; implementation remains bounded by this Record and the stable locator `.workblock/items/AAGU-018/WORKITEM.md`.
- 2026-08-26: rework claimed in the same Codex task after the dashboard validator proved that AAGU-018 and the user-retained AAGU-019 registration were not mapped in `WORKPLAN.md`; acceptance of the earlier candidate does not extend to this new candidate content.
- `accepted`（2026-08-26T13:53:33+08:00）：刘丞毓 基于 已验证候选 7bd5028 与用户明确的验收和收口确认 接受候选 commit `7bd5028df1cdd3179a64b2e5aab8a62226f8fefc`。

## Runtime / Git

- Current owner: Codex task `AAGU-018 · 修复 D-GIF affected-source 标签越界`, claimed 2026-08-26 (Asia/Shanghai); this task owns only Block `AAGU-018` at the stable locator above.
- Registration baseline: `9d36a30a38e3f90d4bc2081014c400037ed25404` on parent `refs/heads/codex/e7-two-surrogate-groups-20260805`.
- Source branch/worktree: `codex/aagu-018-dgif-affected-source` at `C:\Users\ADMIN\.codex\worktrees\aagu018\OpenGU\GULib-master`.
- Apply target observation: the parent ref is checked out at `E:\project\OpenGU\GULib-master`; at claim it equals the registration baseline and is the projected local no-ff target after explicit acceptance.
- Inherited state: the registered WorkItem and its scoped project-counter advance through the registration baseline.
- Excluded state: the parent worktree's uncommitted `.workblock/project.json` advance to 20 and `.workblock/items/AAGU-019/WORKITEM.md` belong to a separate Block and must not enter this branch or candidate.
- Ownership: implementation is limited to D-GIF graph-source computation, its BC-target/target-direct/c-target callers, focused tests, semantic Recipe identities, and this item package. Generated canary output remains runtime evidence.

## Authorization and safety boundaries

- Runtime profile: `local-git`; scoped branch/worktree edits, focused commits, local tests, read-only inspection of historical artifacts, and one disposable local Cora selection canary are allowed.
- Verify may read the repository-local Cora data and write only isolated temporary/cache/output paths declared for this Block; it must not mutate formal datasets, existing Cache V2 Artifacts, historical results, or trusted indexes.
- No private-data, live-provider, external-write, destructive, remote, SSH, install, push, Apply, cleanup, or formal-matrix action is authorized before explicit human acceptance.
- After-accept policy locator: `.workblock/policy.json`; current policy is `remote=push`, `install=skip`, but only `block-closeout` may act on it after acceptance.

## Candidate, evidence, and restart

- Verified implementation checkpoint: `ebb63c9f4cd603ad60fafb0a2e7b9c91c284f0ab`, based on registration baseline `9d36a30a38e3f90d4bc2081014c400037ed25404`. The current candidate lineage additionally contains the formal decision projection, the user's explicitly retained AAGU-019 registration, and this dashboard-mapping rework; no AAGU-019 implementation and no further production or test source change is included.
- Evidence: focused toy-graph RED/GREEN and mutation regression; caller/Recipe tests; disposable current-source Cora canary at `C:\Users\ADMIN\AppData\Local\Temp\AAGU-018-canary-20260826T054340Z`; `.workblock/items/AAGU-018/evidence/impact-ledger.md`; and the dashboard generator check plus its dedicated unit tests.
- Current human surface: this WorkItem. The rework candidate is verified and awaits a new explicit accept/reject decision; acceptance of an earlier candidate does not accept this changed candidate.
- Restart point: if accepted, invoke `block-closeout` on this same stable locator and follow `.workblock/policy.json`. If rejected, keep rework in AAGU-018.
- Prohibited next actions: do not create a sibling Record/relation, run the full E8 matrix, modify historical Artifacts, merge, push, install, or mark this Block accepted.

## Work events

- 2026-08-26 root-cause finding: `graph_source_scores` indexes `data.y` with every node in the structural affected set for `grad1` and every affected neighbor for `grad2`; BC-target and target-direct both reuse this path. Full-graph logits and incident-edge deletion are separate and need no redesign.
- 2026-08-26 baseline: `tests/test_c_target_v1.py`, `tests/test_bc_target_v2.py`, and `tests/test_target_direct_recipe.py` passed 29/29 before production edits; only third-party deprecation warnings were emitted.
- 2026-08-26 RED: the two focused toy-graph tests failed at the missing explicit `source_ids` argument while the existing 8 c-target tests passed. This confirms the regression catches the absent training-source contract before implementation.
- 2026-08-26 GREEN: `graph_source_scores` now intersects each structural affected set with explicit `source_ids`; the c-target caller passes the full training set even when candidates are limited, and BC-target/target-direct pass their complete training candidates. The focused c-target file passed 10/10 and the combined target-direct/BC-target set passed 45/45.
- 2026-08-26 semantic identity: c-target is now `c-target-gif-tracin-v1.1`, BC-target is `bc-target-matrix-v3.2`, and target-direct is `target-direct-opengu-gcn-score-bundle-v3`; new Recipes record the affected/intersected training-source scope.
- 2026-08-26 impact read-back: the tracked ledger names current local score Artifacts, old summary/downstream/aggregate boundaries, known historical selection identities, and unaffected selectors. No historical evidence was mutated.
- 2026-08-26 first real-data canary: a disposable one-candidate Cora run completed cold under the initial implementation source. A later Recipe contract hardening changed the producer source fingerprint, so that earlier canary is superseded and is not used as evidence for the final implementation checkpoint.
- 2026-08-26 review correction: two read-only reviews found no critical implementation defect. The candidate then added fail-closed Recipe enforcement, exact deleted-graph and non-training-structure regressions, all 72 affected benchmark Selection Artifact identities (144 matching cold/warm references), and the SUP source score identity to the impact ledger.
- 2026-08-26 current-source canary: the replacement one-candidate Cora run completed cold with exit code 0, `c-target-gif-tracin-v1.1`, source fingerprint `682ebe0a9e8bdba2f580907b7a484924ed57832aa74e5cc46e5fdbe8feac3390`, Recipe `521725cb4556f6709236d35786ea3d80b28f206a0dacac00d630a02e159edd0c`, verified Artifact `score_521725cb_31186b50`, and `p_graph` ranking `[0]`. Its isolated root is the current path recorded above; this is validation evidence, not formal experiment evidence.
- 2026-08-26 registration carry-through: after acceptance, the user confirmed that the target worktree's only dirty state was the already authorized AAGU-019 registration and requested that its WorkItem plus `nextWorkItemNumber=20` be preserved in this candidate. AAGU-019 remains `registered / ready after dependency`; it is not claimed, implemented, or accepted here.
- 2026-08-26 dashboard rework RED: `python -B -X utf8 scripts/dashboard/refresh.py --check` exits 2 because AAGU-018 and AAGU-019 have no manual WORKPLAN mapping. This task reclaims AAGU-018 only; AAGU-006 remains read-only, AAGU-019 remains registration-only, and the allowed rework is limited to mapping both retained Records plus generator-owned projections.
- 2026-08-26 dashboard rework GREEN: the repair queue now maps AAGU-018 and AAGU-019 as P0 FIX nodes with `AAGU-019 depends_on AAGU-018`; the generator rebuilt the lifecycle projection and `progress.html` for all 19 WorkItems. `scripts/dashboard/refresh.py --check` passes, `tests.test_dashboard_refresh` passes 3/3, AAGU-006 remains the unique Current node, and no AAGU-006 path changed.

## Formal verification and decision note

### Observable result

`graph_source_scores` now forms both graph-source losses only from the candidate's affected nodes that are also in the explicit training source set. Full-graph message passing, validation-target direction, candidate deletion, incident-edge removal, parameter scope, and stable ranking remain on their prior paths. The dashboard also maps the retained AAGU-018/AAGU-019 Records without changing AAGU-006 as the unique Current line.

### Judgement items

- `PASS` — affected graph-source loss labels are restricted to explicit training nodes; validation/test label changes are invariant while an affected training-label change can change `p_graph`.
- `PASS` — validation/test features and a non-training structural edge still change the fixed-direction graph-source score, proving transductive information flow remains active without using those labels as source supervision.
- `PASS` — the numerical regression matches an independently constructed incident-edge-deleted `grad1 - grad2`; a deliberate mutation back to the original graph made that regression fail, while candidate deletion and incident-edge removal retain their contract.
- `PASS` — c-target, BC-target, and target-direct pass the complete training source scope and use fresh semantic versions; their Recipe builders fail closed without that contract, and the impact ledger bounds every affected historical identity without rewriting it.
- `PASS` — WORKPLAN maps both retained Records in the P0 repair queue, projects AAGU-019 as blocked by AAGU-018, keeps AAGU-006 as the unique Current node, and regenerates `progress.html` without touching AAGU-006.

### Verification evidence

- Final focused command: `python -B -X utf8 -m pytest tests/test_c_target_v1.py tests/test_bc_target_v2.py tests/test_target_direct_recipe.py tests/test_target_direct_manifest.py tests/test_target_direct_syncmate_stage.py tests/test_target_direct_split_profile.py tests/test_gu_target_v1.py tests/test_gu_target_v1_aggregate.py -q` — `63 passed`; the same result was reproduced after the formal projection commit.
- Dashboard verification: `python -B -X utf8 -m unittest tests.test_dashboard_refresh -v` — `3 passed`; `python -B -X utf8 scripts/dashboard/refresh.py --check` — `PASS` after generator rebuild, replacing the reproduced two-item drift failure.
- Python compilation of all changed production/test files and `git diff --check` both passed before and after the formal projection commit.
- Current-source Cora canary: cold create, one candidate, exit 0, valid/verified Artifact `score_521725cb_31186b50`; its header binds the corrected source fingerprint, `source_scope=affected_intersection_train_mask`, and `graph_source_set=affected_intersection_train_mask`.

### Known gaps and recommendation

- `NOT OBSERVED` — the full E8 formal matrix, three-dataset coverage experiment, downstream GU outcomes, and rebuilt human reports were intentionally not run; the canary is not formal experiment evidence.
- `NOT CONFIRMED` — no scientific performance or attack-effect conclusion is claimed by this implementation Block.
- Agent recommendation: accept the new clean candidate for closeout if the five judgement items match human intent. The prior candidate decision is not reused; otherwise reject this candidate into the same AAGU-018 Record with the disputed item and do not create a sibling Block.
