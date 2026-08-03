# Handoff: Consolidate self/dashboard source, generated, and append-only guidance

## Session Metadata
- Created: 2026-08-02 01:36:16
- Project: E:\project\OpenGU\GULib-master
- Branch: codex/docs-context-architecture-20260726
- Session duration: about 1 hour of repository guidance review

### Recent Commits
- `a53b148` docs(experiments): record ssh inventory and replacement plan
- `2d26360` docs(experiments): design evidence replacement tree
- `f2b9876` docs(results): track legacy retirement centrally
- `72f0410` docs(agents): consolidate results and syncmate guidance
- `7a1ffc5` docs(experiments): route repairs through human runbook

## Current State Summary

The user approved a focused docs-edit follow-up for `self/dashboard`: preserve the valuable source/generated/append-only boundaries while removing stale and over-broad rules from the old `self/dashboard/CLAUDE.md`. This directory currently has no `AGENTS.md`. The intended result is a concise scoped agent guide whose facts are owned once, links remain small, generators own derived outputs, and the live dashboard does not claim authority over unrelated experiment definitions, reports, or project documentation. The docs edit has not yet been implemented.

## Architecture Overview

The durable ownership model is:

- `WORKPLAN.md`: sole live operational state, current priorities, blockers, and dependencies; handwritten source.
- `progress.html`: generated projection of WORKPLAN via `scripts/dashboard/refresh.py`; never hand-edited.
- `config_inventory.csv`: source ledger for configuration/result-state inventory.
- `config_inventory.html`: generated projection via `scripts/dashboard/gen_config_inventory.py`; never hand-edited.
- `VALIDATION_LOG.md`: append-only validation evidence. Corrections are new superseding entries, not history rewrites.
- The AutoReport events JSONL under `results/_journal/` is the append-only machine audit source outside this directory; its Markdown/HTML are rebuildable projections.
- Frozen reports and archives: immutable historical evidence or presentation artifacts, not live task state.

The scoped guide should describe only how an agent safely maintains files under `self/dashboard` and how to follow ownership links. Stable experiment entry points, SSH/GPU/data/gate facts, report-pair policy, and current task details remain with their existing owners.

## Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `self/dashboard/CLAUDE.md` | Old scoped guidance | Contains useful ownership rules plus stale/conflicting instructions that need disposition |
| `self/dashboard/WORKPLAN.md` | Live operational source | Must remain the only live priorities/dependencies source |
| `self/dashboard/progress.html` | Generated live dashboard | Must be regenerated, never manually edited |
| `scripts/dashboard/refresh.py` | WORKPLAN-to-HTML generator | Already exists; contradicts the old CLAUDE statement that it is pending |
| `tests/test_dashboard_refresh.py` | Generator validation | Relevant acceptance test for the docs-edit boundary |
| `self/dashboard/config_inventory.csv` | Inventory source | Owns the editable inventory facts |
| `self/dashboard/config_inventory.html` | Inventory projection | Generated from CSV, never edited directly |
| `scripts/dashboard/gen_config_inventory.py` | Inventory generator | Owns projection behavior |
| `tests/test_config_inventory_dashboard.py` | Inventory generator validation | Relevant acceptance test |
| `self/dashboard/VALIDATION_LOG.md` | Human/AI validation record | Append-only; successful proof belongs here, not speculative task state |
| `results/_journal/RULES.md` | AutoReport ownership outside dashboard | Link only if needed; do not restate its protocol |
| `AGENTS.md` | Repository-level guidance | Owns project-wide navigation, evidence invariants, runtime boundary, and Git workflow |

## Key Patterns Discovered

- Source documents are edited; generated projections are rebuilt from their owners.
- Append-only evidence is corrected through a new superseding record, never by silently changing history.
- Live state, generated views, frozen reports, and archive evidence are distinct information classes.
- A scoped AGENTS file should contain only actions an agent in that directory needs to perform.
- Current tasks and status must be linked to WORKPLAN, not duplicated in scoped guidance.
- `progress.html` is a human-facing generated artifact, not default agent context.
- Small one-off validation checks belong in the project TODO/check ledger; validated proof may then be appended to VALIDATION_LOG.

## Work Completed

### Tasks Finished

- [x] Identified source/generated/append-only rules worth preserving.
- [x] Confirmed `scripts/dashboard/refresh.py` and its tests already exist.
- [x] Confirmed `config_inventory.csv -> config_inventory.html` has a generator and tests.
- [x] Identified stale or conflicting statements in the current `CLAUDE.md`.
- [x] Confirmed the user wants this docs-edit work continued in a separate task.

## Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `.claude/handoffs/2026-08-02-013616-self-dashboard-docs-edit.md` | Added this handoff | Transfer the scoped docs-edit boundary to a fresh task |

No dashboard guide, source document, generator, test, or derived HTML was changed by this handoff.

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Preserve source/generated/append-only boundaries | Delete all old guidance, retain whole old file, extract only durable rules | These boundaries directly prevent drift and unsafe manual edits |
| Keep WORKPLAN as the sole live operational source | Duplicate current state into AGENTS, use progress.html as source, keep WORKPLAN | Live state should have one editable owner |
| Treat generated HTML as projections | Manual HTML edits, two-way synchronization, generator-owned output | Existing generators and tests already establish one-way ownership |
| Replace over-broad scoped authority with narrow maintenance actions | Dashboard owns all metrics/bugs/findings, directory-only maintenance guide | Experiment definitions and other evidence already have separate owners |

## Pending Work

## Immediate Next Steps

1. Read the current `self/dashboard/CLAUDE.md`, root `AGENTS.md`, generator headers, and focused tests; build a keep/rewrite/delete disposition for every old rule.
2. Propose the minimal final self/dashboard AGENTS structure and decide whether the old `CLAUDE.md` should be deleted or reduced to a compatibility pointer based on the repository's now-approved convention.
3. Implement the approved docs-only diff, run link checks and focused dashboard tests, inspect generated-output drift without hand-editing it, and report exact validation evidence.

### Blockers/Open Questions

- [ ] Should `self/dashboard/CLAUDE.md` be deleted outright or retained as a one-line compatibility pointer? Earlier cleanup favored deleting retired CLAUDE files, but this exact file has not received a final file-level disposition.
- [ ] Should the new scoped AGENTS be entirely English to match the root guide, or bilingual? Prefer concise English unless current repository convention provides stronger evidence.
- [ ] Which semi-manual catalog files need a short maintenance sentence, and which can be omitted because they have no special scoped behavior?
- [ ] Does the old blanket requirement that every file carry `Last updated` still serve an executable purpose? It appears ceremonial and should not be retained without evidence.

### Deferred Items

- Editing WORKPLAN task content, experiment matrices, metrics definitions, or historical validation entries: outside this docs-governance task.
- Redesigning dashboard UI or generator output: outside scope unless a documentation claim cannot be made true without a minimal generator fix and the user approves expansion.
- SyncMate and result-replacement execution: handled by separate tasks.

## Context for Resuming Agent

## Important Context

The old `CLAUDE.md` says every session must read WORKPLAN first, calls `refresh.py` pending, points experiment configuration to `scripts/experiments/`, and broadly declares the directory the unique authority for experiment state, metrics, bugs, and findings. Those statements conflict with current on-demand context loading, the existing generator, current `experiments/` ownership, and the repository's distributed owner model. Do not copy them into the new guide.

Preserve these concrete rules: edit WORKPLAN rather than progress.html; edit config_inventory.csv rather than config_inventory.html; append or supersede VALIDATION_LOG entries rather than rewriting them; do not hand-edit generated outputs; do not copy live dashboard state into AGENTS or other documents. Keep links minimal and point to owners rather than restating their procedures.

This is authorized as docs-edit work, but unrelated dirty files remain user-owned. Review the diff narrowly and do not commit, merge, or push unless separately requested.

## Assumptions Made

- The preferred endpoint is a new scoped AGENTS file under self/dashboard containing only durable guidance.
- Existing generator behavior is correct enough to document unless focused validation proves otherwise.
- The current root AGENTS rule that generated artifacts are rebuilt from sources is authoritative and should not be duplicated at length.

## Potential Gotchas

- `progress.html` and `config_inventory.html` are tracked generated files; a generator run may change them. Any change must be explained by the source/generator and reviewed, not accepted as incidental noise.
- VALIDATION_LOG is large and historical. Do not reformat, reorder, or clean existing entries during this docs edit.
- `PROGRESS.md` and `EXPERIMENT_DASHBOARD.md` are retired/frozen historical surfaces; do not accidentally reactivate them as live owners.
- A statement can be true but still not belong in this scoped file if another owner already maintains it.
- Do not turn the guide into a directory catalog; include only entries with special maintenance behavior.

## Environment State

### Tools/Services Used

- Local Git and repository read-only inspection.
- Existing dashboard generator and test discovery.
- Session-handoff validator for this document.

### Active Processes

- No dashboard generator, test, or watcher is currently running for this handoff.

### Environment Variables

- None required for the docs-only audit. Use the project interpreter from its owning experiment guidance if tests require it.

## Related Resources

- `self/dashboard/CLAUDE.md`
- `self/dashboard/WORKPLAN.md`
- `self/dashboard/VALIDATION_LOG.md`
- `scripts/dashboard/refresh.py`
- `scripts/dashboard/gen_config_inventory.py`
- `tests/test_dashboard_refresh.py`
- `tests/test_config_inventory_dashboard.py`
- `AGENTS.md`

---

**Security Reminder**: This handoff contains no credentials or secret values. Validate again after every material edit.
