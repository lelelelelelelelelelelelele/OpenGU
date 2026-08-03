# Handoff: Execute the ordered replacement of pre-June experiment evidence

## Session Metadata
- Created: 2026-08-02 01:36:16
- Project: E:\project\OpenGU\GULib-master
- Branch: codex/docs-context-architecture-20260726
- Session duration: about 2 hours across the experiment-governance discussion

### Recent Commits
- `a53b148` docs(experiments): record ssh inventory and replacement plan
- `2d26360` docs(experiments): design evidence replacement tree
- `f2b9876` docs(results): track legacy retirement centrally
- `72f0410` docs(agents): consolidate results and syncmate guidance
- `7a1ffc5` docs(experiments): route repairs through human runbook

## Current State Summary

The design for replacing old experiment evidence is complete, but execution has not begun. Every result produced on or before `2026-05-31 23:59:59` is now treated as a non-authoritative candidate rather than an automatic deletion target. The approved strategy is to rerun still-needed registered batches in dependency order, accept each new batch through the normal gate and collection chain, rebuild downstream projections, record an old-to-new mapping, and only then place old local and SSH payloads into a separately authorized retirement operation. The repository is currently paused at readiness stages R1-R3; no deletion, formal GPU gate, matrix expansion, or result retirement is authorized by this handoff.

## Architecture Overview

Each replacement batch follows one state machine:

`INVALIDATED -> REGISTERED -> GATED -> RUNNING -> COLLECTED -> ACCEPTED -> PROJECTED -> REPLACED -> RETIRED`

The execution tree is dependency-ordered rather than directory-ordered:

- R1: close current work blocks and align local `main`, `origin/main`, and the SSH active checkout to one clean full SHA.
- R2: establish the local SyncMate collector/peer boundary and rebuild queue projections from actual queue state.
- R3: verify a real GPU, the formal `gnn_20` interpreter, canonical processed profiles, and registered dry-runs.
- R4: run only E8 G1/G2/G3, then pause for human review.
- R5 branches: separately replace target-direct, method-specific, dataset/budget, and conditional-mechanism batches.
- R6: rebuild aggregates, tables, figures, reports, and dashboards from newly accepted evidence.
- R7: record old-to-new mappings and reference scans; retirement remains a separate destructive authorization.

Overlapping registered batches are rerun whole. Only exact immutable Cache V2 Score/Selection identities may be reused. Legacy caches, matching directory names, and similar-looking parameters do not establish identity.

## Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `docs/superpowers/specs/2026-08-01-experiment-evidence-replacement-tree-design.md` | Approved replacement-tree design | Primary ordering, pause points, state machine, and non-goals |
| `reports/experiment_evidence_replacement_tree_DESIGN.html` | Human-readable design projection | Must agree with the Markdown design |
| `self/dashboard/WORKPLAN.md` | Sole live task and dependency source | Owns current R1-R3 state and EVIDENCE-RENEWAL-1 |
| `experiments/AGENTS.md` | Formal experiment execution rules | Owns launcher choice, local dry-run, SSH/GPU/data/SHA/preflight/gate constraints |
| `results/AGENTS.md` | Returned-result organization rules | Prevents unverified or ambiguous artifacts entering downstream use |
| `scripts/syncmate/AGENTS.md` | Current OpenGU collection and verification boundary | Owns current collect, SHA-256, trusted-index, and runner-queue guardrails |
| `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md` | Approved machine repair procedure after scope is decided | Not a generic deletion authority |
| `results/_journal/RULES.md` | AutoReport evidence rules | Keeps historical baseline facts separate from current completion state |
| `self/dashboard/config_inventory.csv` | Source ledger for produced/usable/accepted/rerun states | Downstream projection source, not a replacement for the retirement ledger |

## Key Patterns Discovered

- Formal GPU gates fail closed and never fall back to CPU.
- A process exit code or queue `done` state does not make an artifact trusted evidence.
- New code fixes require a new complete SHA and result/cache identity before rerunning affected gates; old and new cells are never mixed.
- The cutoff is an evidence policy, not a recursive filesystem-delete command and not an mtime-only classifier.
- A batch reaches `REPLACED` only after its accepted successor is projected into every relevant downstream consumer and old references reach zero.
- `RETIRED` requires separate approval and should prefer reversible quarantine/archive before deletion.
- Current SyncMate independentization is being handled in another task. This task must not redesign or migrate SyncMate core while executing OpenGU readiness.

## Work Completed

### Tasks Finished

- [x] Established the `2026-05-31 23:59:59` evidence cutoff.
- [x] Replaced the earlier Legacy-only cleanup idea with a full evidence-renewal policy.
- [x] Completed read-only local and SSH inventory used by the design snapshot.
- [x] Designed the replacement state machine, dependency tree, pause points, and non-goals.
- [x] Added the live EVIDENCE-RENEWAL-1 entry and R1-R3 status to WORKPLAN.
- [x] Confirmed that overlapping registered batches may be completely rerun because the matrix is manageable.

## Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `.claude/handoffs/2026-08-02-013616-experiment-evidence-replacement-execution.md` | Added this handoff | Transfer the approved design and current execution boundary to a fresh task |

This handoff does not modify experiment code, configurations, results, caches, SSH state, SyncMate state, or Git integration branches.

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Rerun and replace in dependency order | Immediate bulk deletion, directory-by-directory cleanup, ordered replacement | New evidence must exist and be accepted before old payload retirement is safe |
| Treat all cutoff-era results as non-authoritative candidates | Legacy-only invalidation, automatic deletion of all old files | The old runtime and identity predate the current formal workflow, but audit history still matters |
| Rerun complete registered batches even when they overlap | Manual cross-batch cell deduplication, whole batches | Whole batches keep identities, manifests, failure recovery, and acceptance auditable |
| Retire only after mapping and reference scan | Delete first and rerun later, archive everything immediately | Prevents loss of provenance and broken reports while still allowing later cleanup |
| Pause after E8 G3 | Automatically proceed through G4/G5 | G3 evidence may change the scientific target and G4/G5 require separate authorization |

## Pending Work

## Immediate Next Steps

1. Re-verify the current Git/worktree/SSH/readiness snapshot because the 2026-08-01 inventory is drift-prone; report current facts separately from the design snapshot.
2. Audit R1 without mutating Git: identify the current branch parent, diff scope, validations, and exact closeout actions needed before `main` alignment. Use the OpenGU Git/SSH closeout guidance if applicable, but do not merge or push without explicit approval.
3. After R1 authorization and completion, audit R2 and R3 in order. Do not launch a formal gate until the same clean full SHA, a real GPU, `gnn_20`, required processed profiles, and registered dry-run identities all pass.

### Blockers/Open Questions

- [ ] Has the current documentation work block been reviewed and authorized for merge into `main` and push to origin?
- [ ] Has the separate SyncMate independence task changed the current OpenGU command path or consumer layout? Re-check before configuring R2.
- [ ] Are the SSH GPU, formal interpreter, processed profiles, and queue state different from the 2026-08-01 snapshot?
- [ ] What machine-readable inventory/retirement-ledger schema and generator should be implemented before the first replacement batch reaches `REPLACED`?
- [ ] Which exact registered batch is first after R1-R3: the design says E8 G1/G2/G3, but current WORKPLAN and registered recipes must be rechecked before execution.
- [ ] After G3, the user must explicitly decide whether G4 is still scientifically justified. G5 remains separately unauthorized.

### Deferred Items

- E8 G4/G5 and all full-matrix expansion: deferred to explicit post-G3 review.
- E1, E4, E2, E3, A5, PubMed, arxiv, A3, and E7 replacement branches: deferred until their dependency gates and pause conditions are met.
- Local or SSH deletion/archive of old payloads: deferred until a batch is `REPLACED` and destructive scope is separately approved.
- Broad SyncMate refactoring or submodule migration: owned by the dedicated SyncMate task.

## Context for Resuming Agent

## Important Context

Do not redesign the replacement tree from scratch: the Markdown design and HTML projection already exist and current WORKPLAN already registers the active readiness stages. The unfinished work is evidence-backed execution, beginning with a current-state refresh and R1 audit. Keep design claims, newly verified facts, and planned actions visibly separate.

The user explicitly prefers staged rerun and replacement over immediate deletion. Even if old and new matrices overlap, rerun each complete registered batch. Never infer permission to remove local or SSH files from the cutoff policy. Preserve unrelated dirty work and stop at every human/scientific pause point.

The SSH endpoint and runtime inventory are temporally unstable. Resolve them from current project configuration and read-only checks instead of copying an old host or port into new authority documents.

## Assumptions Made

- The existing replacement-tree design remains the approved plan unless current evidence reveals a contradiction.
- The first useful task is a read-only R1-R3 refresh, not a formal experiment launch.
- Human-facing execution/acceptance reports will follow the repository rule of paired Markdown and HTML.

## Potential Gotchas

- The current branch is not `main`; formal gates require the accepted work to reach the three aligned `main` checkouts first.
- The 2026-08-01 snapshot reported no container GPU, missing `gnn_20`, missing 70/10/20 profiles, and no local SyncMate collector/peer. These are historical snapshot facts until reverified.
- `results/runs/` and archives mix old and newer artifacts; never delete or classify a whole directory by mtime.
- Historical E1 50/50 and E4 40/40 demonstrate feasibility only; they do not satisfy the new unified identity.
- New aggregate/table/figure generation must read only newly accepted evidence and must not silently backfill from invalidated history.
- Creating an inventory ledger is not permission to act on the ledger's retirement candidates.

## Environment State

### Tools/Services Used

- Local Git and repository read-only inspection.
- Prior SSH inventory captured in the approved replacement-tree design; it must be refreshed before use.
- Session-handoff validator for this document.

### Active Processes

- No experiment or cleanup process was started by this handoff task.

### Environment Variables

- None recorded. Resolve runtime paths from current project-owned guidance.

## Related Resources

- `docs/superpowers/specs/2026-08-01-experiment-evidence-replacement-tree-design.md`
- `reports/experiment_evidence_replacement_tree_DESIGN.html`
- `self/dashboard/WORKPLAN.md`
- `experiments/AGENTS.md`
- `results/AGENTS.md`
- `scripts/syncmate/AGENTS.md`

---

**Security Reminder**: This handoff contains no credentials or secret values. Validate again after every material edit.
