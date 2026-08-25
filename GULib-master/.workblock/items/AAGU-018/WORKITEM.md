# AAGU-018 · 修复 D-GIF affected-source 标签越界

Block ID: `AAGU-018`

当前状态: `registered / ready for claim`

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
