---
title: Root CLAUDE.md Decomposition and AGENTS Placement Audit
date: 2026-07-26
status: accepted-as-migration-inventory
scope: root CLAUDE.md lines 5-307, compared with AGENTS.md and AGENTS_DRAFT.md
---

# Root CLAUDE.md Decomposition and AGENTS Placement Audit

## Verdict

**ACCEPTED as a migration inventory; not yet an instruction-file replacement.**

The 307-line root `CLAUDE.md` contains valuable operational knowledge, but it
currently mixes four different ownership levels:

1. stable repository-wide agent constraints;
2. formal-experiment constraints that belong under `experiments/`;
3. live or historical research status that belongs in `self/` and the document map;
4. old command lists, incident notes, and agent-specific slash-command hints.

The audit covers all **13 substantive blocks** in the root file. The target
layout is deliberately small:

| Target | Owns |
|---|---|
| root `AGENTS.md` | stable repository purpose, navigation, execution boundaries, evidence invariants, compact Git rule |
| `experiments/AGENTS.md` | formal SSH lane, fixed-SHA gate, dataset/preflight/result identity, matrix runner rules |
| nearest local `AGENTS.md` / retained local `CLAUDE.md` | narrow cache, dashboard, or SyncMate implementation rules |
| `文档规划/`, `docs/`, `self/`, `reports/` | method design, runbooks, active state, historical findings, and human-facing evidence |

The existing `AGENTS_DRAFT.md` now covers repository positioning, entry
points, execution locations, a minimal pipeline, runtime/validation, map,
Git, and the two-line evidence-infrastructure boundary recorded below. It
should **not** absorb dated status, method-line details, or a formal SSH
runbook.

## Block-by-block disposition

| # | Root `CLAUDE.md` block | What it currently says | Preserve? | Destination / AGENTS decision | Audit finding |
|---|---|---|---|---|---|
| 1 | Project Overview (5-9) | Research purpose and historical counts of methods, datasets, and backbones. | Yes, rewritten. | Root `AGENTS.md`: **yes**. | Keep the research question and evidence-repository framing; drop volatile counts. The draft is already the stronger version. |
| 2 | Start Here: Live Dashboard (11-26) | Dashboard table, live-state roles, and no-duplication rule. | Yes, compressed. | Root `AGENTS.md`: **one pointer only**; `self/dashboard/CLAUDE.md`: detailed table. | `WORKPLAN.md` remains the live source. Repeating the whole table at root creates a second routing map. |
| 3 | Git Workflow (28-35) | Parent-first work, `--no-ff`, `--ff-only`, cache-local notes. | Yes, rewritten. | Root `AGENTS.md`: **yes**, as the approved compact Git section. | Remove the dependency on `docs/GIT_WORKFLOW.md` after reference migration. `results/experiments/CLAUDE.md` is a dead reference. Cache details remain local. |
| 4 | Formal Remote Execution Lane (39-57) | Accepted-main requirement, full SHA, SSH active checkout, worktree criteria, deployment-root boundary. | Yes, intact in meaning. | `experiments/AGENTS.md`: **yes**; root only links to it. | This is a formal-run contract, not a universal Git rule. It matches the intended fixed-SHA/SSH separation. |
| 5 | Canonical Dataset Location on SSH (59-80) | Active-checkout dataset roots, split semantics, preflight, duplicate handling. | Yes, intact in meaning. | `experiments/AGENTS.md`: **yes**. | Dataset identity is formal-evidence correctness. Keep detail with the runner/preflight rules, not at root. |
| 6 | Basic commands and Phase-B runner (82-102) | Legacy `main.py` examples, argument catalogue, YAML runner and gate command. | Partly. | Experiment runbook / `experiments/AGENTS.md`: **not root**. | Keep only current canonical entry points. The statement “No formal test suite exists” is stale: repository pytest suites exist. |
| 7 | Architecture (104-146) | Execution flow, dispatchers, pipeline classes, data flow, MIA-only attack description. | Yes, split. | Root `AGENTS.md`: minimal flow and map; durable architecture doc: details. | The draft’s one-line pipeline is sufficient at root. The current pipeline list has a duplicated `Shard_based_pipeline` bullet and should not be copied verbatim. |
| 8 | Dependencies and Environment (147-167) | Python stack and full `gnn` interpreter path. | Yes, compressed. | Root `AGENTS.md`: **yes** for interpreter and local CPU boundary. | Package versions belong in `../requirements.txt`; tool-shell explanation does not need a root instruction block. |
| 9 | Important Notes (169-178) | `--no_cache`, import side effect, ScaleGUN status, GraphRevoker history, seed, logs, rerun and checkpoint-collision advice. | Split; do not retain as one block. | Root: config import side effect only; experiments/local cache docs: cache and checkpoint matters; evidence docs: historical defects. | A blanket destructive cleanup command is unsafe as root guidance. Old defect and static-status notes are not universal instructions. |
| 10 | Status & Engineering Bottlenecks (180-199) | Dated project phase, active branch, hardware facts, bottlenecks and resolved incidents. | Preserve as evidence, remove from root. | `self/dashboard/WORKPLAN.md`, `self/limitations.md`, archived reports: **not AGENTS**. | The file itself says this list has drifted. It must not compete with the live dashboard. |
| 11 | Phase-B Toolkit (201-213) | A table of scripts, commands and pointers. | Preserve current entries only. | `文档规划/10_实验矩阵/15_实验运行入口与脚本.md`: **not AGENTS**. | The table includes a nonexistent `scripts/redo_collateral.sh`; the current tracked rerun helper is `scripts/redo_collateral_if_family.py`. |
| 12 | Project Context, Attack Structure, Result Storage (215-291) | Research narrative, method findings, attack files, Phase-B artifacts, baselines, journal/cache locations. | Split. | `self/` and `文档规划/`: research/method detail; `experiments/AGENTS.md`: formal cell artifacts; root: two evidence-infrastructure rules only. | The former `self/concordance/HANDOFF.md` pointer was wrong and the later handoff has now been retired; historical study evidence remains in `self/related_work/concordance/report.html`, while current status lives in the experiment map. AutoReport V3 is a root-level integrity boundary, but the whole storage catalogue is not. |
| 13 | Document Workflow and Slash Commands (293-307) | V3 journal explanation, daily-log pointer, Claude slash commands. | Split. | Root: AutoReport authority rule; `report/daily-log/` / skills: daily-log workflow; Claude-specific commands: remove from shared instruction surface. | V3 JSONL is the audit authority. The historical `results/_journal/RULES.md` is explanatory archive material and must not override V3 design. |

## Required root additions

The following compact text is the only infrastructure material that should be
added to the root draft beyond its existing map and pipeline description:

```md
## Critical Evidence Infrastructure

- `cache_v2/` stores exact, immutable Recipe/Artifact evidence. Dataset loading,
  split construction, candidate construction, and selection computation belong
  to the experiment layer; never rename, overwrite, repair, or delete a V2
  Artifact by hand.
- AutoReport V3 writes append-only JSONL audit facts. Its Markdown and HTML
  files are rebuildable projections; change producers or generators, then
  rebuild, rather than hand-editing either evidence surface.
```

This is intentionally not an IF, IM, TracIn, or method-policy section. Those
are evolving research lanes and are routed through `文档规划/`, `self/`, and
experiment configuration rather than frozen into a repository-wide agent rule.

## Verified reference and drift checks

| Check | Result | Consequence |
|---|---|---|
| Dashboard files, cache-local CLAUDE files, SSH validators, runner, gate script, and dataset audit | Present | Retain as local or experiment-level pointers. |
| `results/experiments/CLAUDE.md` | Missing | Remove the root reference; its historical mapping table is in `self/dashboard/EXPERIMENT_DASHBOARD.md`. |
| `self/concordance/HANDOFF.md` | Missing and retired | Route historical study readers to `self/related_work/concordance/report.html`; route current terminology and execution state to `FINDING_tracin_misspecification.md` and the experiment map. |
| `scripts/redo_collateral.sh` | Missing | Retire the old table row; use the tracked `scripts/redo_collateral_if_family.py` only where the current runbook calls for it. |
| “No formal test suite exists” | Contradicted by tracked pytest suites | Remove; validation policy should state proportional test scope instead. |
| Pipeline hierarchy list | Has one duplicated class bullet | Do not migrate verbatim; retain the verified three-class abstraction only in durable architecture material. |
| V3 AutoReport authority | Confirmed by V3 design and acceptance report | Root rule must name JSONL as fact authority and MD/HTML as projections. |
| Cache V2 ownership | Confirmed by Cache V2 design and acceptance report | Root rule must preserve the experiment-versus-cache boundary. |

## Migration sequence

1. Finish and approve `AGENTS_DRAFT.md`, including the two evidence rules above.
2. Create and approve `experiments/AGENTS_DRAFT.md`; migrate formal lane,
   dataset, preflight, gate, and result-identity material there.
3. Redirect or relocate the retained architecture, runbook, research-context,
   and historical material to their owning documents. Correct the three broken
   root references as part of that migration.
4. Replace root `AGENTS.md` only after the draft is approved. Migrate all
   callers from `docs/GIT_WORKFLOW.md`, then delete that duplicate document in
   the same accepted work block.
5. Reduce root `CLAUDE.md` to a short Claude-specific launcher or retire it
   once its remaining unique content has an owner. Do not delete it before the
   reference migration is complete.

## Acceptance evidence

- Scope review: every root-level `##` section and every substantive `###`
  block in `CLAUDE.md` lines 5-307 is represented in the disposition table.
- Current-state checks: paths, scripts, code symbols, pipeline classes, and
  report authority claims were checked in the primary local checkout on
  2026-07-26.
- This report changes no executable experiment, cache, result, remote state,
  or current instruction file. It is an accepted decision inventory, not
  authorization to delete or rewrite the listed sources.

## Known follow-up

`self/dashboard/CLAUDE.md` and `results/_journal/RULES.md` themselves contain
older wording that should be examined in the separate `self/` documentation
inventory. That follow-up must distinguish live dashboard ownership from
historical journal compatibility; it must not flatten them into root rules.
