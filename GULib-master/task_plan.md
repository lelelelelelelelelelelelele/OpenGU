# AAGU-028 implementation plan

Authority: [.workblock/items/AAGU-028/WORKITEM.md](.workblock/items/AAGU-028/WORKITEM.md).
This plan tracks implementation only; human acceptance remains in that WorkItem.

1. COMPLETE: reread protocol, accepted prerequisites, repository guidance; Claim same Block in linked worktree.
2. COMPLETE: reproduce missing Retrain registration, implicit Metrics training, rounded-result drift; map active consumers.
3. COMPLETE: implement a single independent Retrain consumer, explicit deletion semantics, immutable model/prediction outputs and verified pairing.
4. COMPLETE: connect read-only Metrics and remove implicit retraining; update affected OpenGU launchers.
5. IN PROGRESS: CPU integration, cold/warm/reuse/recompute and rejection tests; runnable example and data flow.
6. PENDING: exact candidate, Verify, paired formal report, awaiting_acceptance Claim.

Boundaries: disposable local CPU inputs only; preserve original assets; no SSH/GPU/formal matrix, Apply, push, install or cleanup.

Errors / surprises:
- Git root is one directory above the project; run_git sourceProject is the nested GULib-master below the caller-provided worktree path. Use its returned exact sourceProject.

- Standalone caller argv exposed OpenGU import-time config parsing. Entry now initializes runtime defaults within its owned CLI context; disposable example2 completed.
