# AAGU-018 · 修复 D-GIF affected-source 标签越界

Block ID: `AAGU-018`

当前状态: `working / claimed`

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

- Candidate: implementation complete but not yet committed or formally verified; the source branch still needs a scoped checkpoint and final candidate verification.
- Evidence: focused toy-graph RED/GREEN regression; caller/Recipe tests; disposable real Cora canary at `C:\Users\ADMIN\AppData\Local\Temp\AAGU-018-canary-20260826T052609`; and `.workblock/items/AAGU-018/evidence/impact-ledger.md`.
- Current human surface: this WorkItem. Results are not yet observed; no acceptance decision is implied.
- Restart point: implementation, focused GREEN, impact ledger, and one disposable Cora canary are complete; next allowed action is scoped commit, candidate-level verification, and the formal human note.
- Prohibited next actions: do not create a sibling Record/relation, run the full E8 matrix, modify historical Artifacts, merge, push, install, or mark this Block accepted.

## Work events

- 2026-08-26 root-cause finding: `graph_source_scores` indexes `data.y` with every node in the structural affected set for `grad1` and every affected neighbor for `grad2`; BC-target and target-direct both reuse this path. Full-graph logits and incident-edge deletion are separate and need no redesign.
- 2026-08-26 baseline: `tests/test_c_target_v1.py`, `tests/test_bc_target_v2.py`, and `tests/test_target_direct_recipe.py` passed 29/29 before production edits; only third-party deprecation warnings were emitted.
- 2026-08-26 RED: the two focused toy-graph tests failed at the missing explicit `source_ids` argument while the existing 8 c-target tests passed. This confirms the regression catches the absent training-source contract before implementation.
- 2026-08-26 GREEN: `graph_source_scores` now intersects each structural affected set with explicit `source_ids`; the c-target caller passes the full training set even when candidates are limited, and BC-target/target-direct pass their complete training candidates. The focused c-target file passed 10/10 and the combined target-direct/BC-target set passed 45/45.
- 2026-08-26 semantic identity: c-target is now `c-target-gif-tracin-v1.1`, BC-target is `bc-target-matrix-v3.2`, and target-direct is `target-direct-opengu-gcn-score-bundle-v3`; new Recipes record the affected/intersected training-source scope.
- 2026-08-26 impact read-back: the tracked ledger names current local score Artifacts, old summary/downstream/aggregate boundaries, known historical selection identities, and unaffected selectors. No historical evidence was mutated.
- 2026-08-26 real-data canary: a disposable one-candidate Cora run completed cold with `c-target-gif-tracin-v1.1`, Artifact `score_df3c73d2_1b10b067`, Recipe `df3c73d2236055d9a83614cf864ad3d91d9b05ac179c08d0475d06e19b5188b9`, and selected node `0`. Its isolated root is the temporary path recorded above; this is validation evidence, not formal experiment evidence.
