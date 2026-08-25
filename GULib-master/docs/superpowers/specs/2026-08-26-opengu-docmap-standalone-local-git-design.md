# OpenGU DocMap Standalone Local Git Design

## Decision

Migrate the existing OpenGU DocMap vault from
`E:\project\OpenGU\GULib-master\文档规划` to
`E:\project\OpenGU-DocMap`. The destination is both the canonical Obsidian
vault and an independent local Git repository with no remote configured.

The migration changes the storage and version-control boundary only. It does
not create a parallel framework or reorganize the existing note taxonomy.

## Current baseline

The existing DocMap already separates the dynamic workbench, experiment
matrix, research framework, and review/reporting surfaces. It is registered in
Obsidian and paired with `gdrive:obsidian-bisync/OpenGU-DocMap`, but its tracked
files belong to the parent `E:\project\OpenGU` Git repository.

The approved working snapshot contains six uncommitted tracked DocMap changes.
Those changes are user-owned migration input and must appear unchanged in the
standalone repository's first snapshot.

## Target boundaries

### Standalone DocMap repository

Owns the complete human-readable OpenGU research map, including current notes,
images, HTML companions, experiment planning, paper-reading notes, and future
evidence-chain records. It tracks all durable vault content while ignoring
`.obsidian/` and `.trash/` runtime state.

### Parent OpenGU repository

Continues to own code, configuration, formal experiment definitions, tests,
and runtime evidence contracts. It no longer tracks the DocMap subtree. Active
repository guidance may point to the sibling DocMap location, while historical
records retain their historical path wording when changing it would alter
provenance.

### Obsidian and rclone

Obsidian registers `E:\project\OpenGU-DocMap` as the same logical vault.
The existing remote remains `gdrive:obsidian-bisync/OpenGU-DocMap`. Because the
local endpoint changes intentionally, the new pair is initialized with a
reviewed `--resync` after a dry run and external backup. `.git/**`,
`.obsidian/**`, and `.trash/**` stay excluded.

## Migration transaction

1. Back up the old vault, Obsidian registry, and relevant bisync state.
2. Reconcile the old-path local and remote pair and prove zero differences.
3. Copy the verified current vault to the destination and compare durable-file
   paths, sizes, and SHA-256 hashes.
4. Initialize the destination Git repository, add runtime ignores and a short
   boundary README, and commit the complete current snapshot.
5. Rewrite only live file links whose targets cross the old vault boundary;
   preserve historical path prose.
6. On the isolated parent migration branch, remove the tracked old subtree and
   update active entry-point references.
7. Back up and update `obsidian.json` while Obsidian is stopped.
8. Dry-run and initialize the new-path bisync pair, then prove zero differences.
9. Retire the old local path recoverably, integrate the parent cleanup with a
   no-ff merge, and verify unrelated state is unchanged.

## Acceptance checks

- Every durable old-vault file exists at the destination with the same content
  before intentional link/boundary edits are applied.
- The standalone repository has one local `main` branch, no remote, a readable
  boundary README, and a clean committed working tree.
- The six pre-existing modified DocMap files are present in the standalone
  commit; no unrelated `.workblock` content is included.
- Obsidian resolves the same logical vault at the new path.
- The new-path rclone pair reports zero differences against the existing
  OpenGU-DocMap remote.
- Active Markdown entry links work from their new locations and the migration
  introduces no new broken local-file links.
- The old vault path is retired without deleting the external recovery backup.
- Parent Git changes are scoped to DocMap removal, active-reference repair, and
  the migration design/plan; unrelated dirty state remains untouched.

## Non-goals

- No remote Git repository is created or pushed.
- No paper, experiment, result, cache, WorkItem, or research conclusion is
  reclassified during the migration.
- The evidence-chain schema and Legacy issue redesign are not implemented in
  this storage-boundary change.
- No existing rclone pair other than OpenGU DocMap is synchronized.

## Approval

The user approved this design in the current Codex task on 2026-08-26 and asked
for inline execution.
