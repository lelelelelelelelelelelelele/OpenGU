# Repository Agent Instructions

These instructions apply to all work under `GULib-master/`.

## Start Here

1. Read the root `CLAUDE.md` before changing code, experiments, or reports.
2. Read the nearest subfolder `CLAUDE.md` before touching that subtree.
3. For current experiment state, use `self/dashboard/WORKPLAN.md`; do not infer it from an old branch name or dated report.

## Core Principles

- One coherent improvement belongs to one branch with one explicit parent.
- Preserve reviewable history and accept completed work through meaningful merge commits.
- Protect shared branches, other worktrees, remote experiment state, and unrelated dirty files.

## Git Workflow (Mandatory)

The authoritative human-readable workflow is [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md).

- Treat `main`, `release/*`, and explicitly designated `research/*` branches as integration lines. Do not develop directly on them.
- Before editing, name the intended parent branch. Create one short-lived branch for one coherent improvement from that parent.
- A child branch must merge back into its recorded parent first. If the parent is itself an improvement line, only merge that parent into `main` after the whole line is accepted.
- Accept completed improvements with an explicit merge commit: `git merge --no-ff <child>`. Do not use squash merge or rebase merge for accepted project work.
- Use `git pull --ff-only` for synchronization. `--no-ff` is for accepting an improvement, not for routine pulls.
- Before switching or merging, run `git status --short --branch` and `git worktree list`. Preserve unrelated dirty files and never move a branch that is checked out in another worktree.
- Suggested branch names are `feat/*`, `fix/*`, `experiment/*`, `docs/*`, and `chore/*`. Agent-created branches use `codex/<type>-<topic>-YYYYMMDD`.
- Keep commits reviewable and scoped. A heterogeneous worktree must be split into semantic commits; never use `git add -A` blindly.
- Do not merge into `main`, push, delete branches, prune refs, or rewrite shared history unless the user explicitly authorizes that step.

## Human-Readable Reports

For acceptance reports, experiment reports, architecture reviews, milestone summaries, and advisor-facing reports, produce matching Markdown and static HTML files. Markdown is the editable source of truth; both files must agree on conclusions and key numbers. Follow existing `docs/` and `reports/` conventions.

### Obsidian / Markdown layout rules

- Do not remove comparison tables merely because they are wide. Preserve tables when row/column alignment materially improves comparison.
- If a table is hard to read, first shorten cell text, move formulas or explanations outside the table, or split it into smaller same-purpose tables. Use callouts for definitions, verdicts, warnings, and evidence summaries—not as a blanket replacement for tables.
- In Obsidian-facing Markdown, write math with `$...$` and `$$...$$`; do not use `\(...\)` or `\[...\]` as the canonical delimiters.
- For display math inside a callout, prefix the opening delimiter, every equation line, and the closing delimiter with `>`.
- Visually verify edited tables and formulas in Obsidian reading view. Source-level Markdown checks alone are not sufficient acceptance evidence.
