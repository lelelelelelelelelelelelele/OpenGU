# OpenGU DocMap Standalone Local Git Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the existing OpenGU DocMap to a standalone local Git repository while preserving its Obsidian and Google Drive identities.

**Architecture:** Treat the migration as a recoverable transaction across three boundaries: the parent OpenGU Git repository, the standalone vault repository, and the Obsidian/rclone runtime. Copy and verify before retiring the old path; isolate parent Git changes in a dedicated worktree and integrate them only after the new vault passes all checks.

**Tech Stack:** Git, PowerShell 7, Obsidian Windows registry JSON, rclone bisync, Markdown/HTML/SVG/PNG files.

**Spec:** `docs/superpowers/specs/2026-08-26-opengu-docmap-standalone-local-git-design.md`

## Global Constraints

- Source: `E:\project\OpenGU\GULib-master\文档规划`.
- Destination: `E:\project\OpenGU-DocMap`.
- Remote: `gdrive:obsidian-bisync/OpenGU-DocMap`.
- Standalone Git has no remote.
- Preserve the six pre-existing modified DocMap files and exclude unrelated parent-worktree state.
- Exclude `.obsidian/**` and `.trash/**` from Git, and exclude `.git/**`,
  `.obsidian/**`, and `.trash/**` from rclone.
- Do not rewrite historical path prose merely because the live path changes.

---

### Task 1: Establish a synchronized recovery baseline

**Files:**
- Create outside vault: `C:\Users\ADMIN\Documents\Obsidian\_rclone_bisync_backups\OpenGU-DocMap-migration-<timestamp>\`
- Read: `%APPDATA%\obsidian\obsidian.json`
- Read: `%LOCALAPPDATA%\rclone\bisync\*OpenGU-DocMap*`

**Interfaces:**
- Consumes: the current local vault and its existing rclone pair.
- Produces: a timestamped recovery tree and a zero-difference old-path baseline.

- [ ] **Step 1:** Record source file paths, sizes, SHA-256 hashes, parent Git status, Obsidian registry entry, and matching bisync-state filenames.
- [ ] **Step 2:** Copy the source vault, `obsidian.json`, and exact old-pair bisync state files to the external recovery directory.
- [ ] **Step 3:** Run `rclone bisync <source> gdrive:obsidian-bisync/OpenGU-DocMap --dry-run --resilient --exclude '.git/**' --exclude '.obsidian/**' --exclude '.trash/**'` and inspect the one known difference.
- [ ] **Step 4:** Run the normal old-path bisync with external backup directories only if the dry run shows no conflict or remote-newer overwrite risk.
- [ ] **Step 5:** Run `rclone check` and require zero differences before continuing.

### Task 2: Create and verify the standalone vault repository

**Files:**
- Create: `E:\project\OpenGU-DocMap\.gitignore`
- Create: `E:\project\OpenGU-DocMap\README.md`
- Copy: all source-vault files to `E:\project\OpenGU-DocMap\`

**Interfaces:**
- Consumes: the synchronized source snapshot and baseline manifest.
- Produces: a clean standalone local Git `main` commit with no remote.

- [ ] **Step 1:** Verify the destination does not exist and resolve the exact source, destination, and recovery paths.
- [ ] **Step 2:** Copy the complete vault to the destination without deleting the source.
- [ ] **Step 3:** Compare durable source/destination file maps, sizes, and SHA-256 hashes; stop on any mismatch.
- [ ] **Step 4:** Add `.gitignore` entries for `.obsidian/` and `.trash/` and add a README describing ownership and external evidence locators.
- [ ] **Step 5:** Initialize Git with branch `main`, stage only durable vault content, inspect the staged path list, and commit the current snapshot.
- [ ] **Step 6:** Verify `git remote -v` is empty and `git status --short` is empty.

### Task 3: Repair live cross-boundary links

**Files:**
- Modify: active Markdown files under `E:\project\OpenGU-DocMap\` whose live links resolve into `E:\project\OpenGU\GULib-master\`.
- Modify: active parent-repository entry files whose live links resolve into the old DocMap subtree.
- Preserve: historical reports whose path text is evidence rather than navigation.

**Interfaces:**
- Consumes: the old-to-new root mapping and the baseline live-link inventory.
- Produces: active links that resolve from the new physical layout.

- [ ] **Step 1:** Inventory Markdown link targets and classify them as internal-vault, live cross-boundary, external URL/Obsidian URI, or historical prose.
- [ ] **Step 2:** Rewrite only live cross-boundary link targets using relative paths between `E:\project\OpenGU-DocMap` and `E:\project\OpenGU\GULib-master`.
- [ ] **Step 3:** Run the link audit against both roots and compare with the baseline; require no newly broken active links.
- [ ] **Step 4:** Commit the standalone link repairs as a second focused commit.

### Task 4: Form the parent Git migration candidate

**Files:**
- Delete on migration branch: `GULib-master/文档规划/**`
- Modify: `GULib-master/AGENTS.md` and other active entry-point files identified by Task 3.
- Create: `GULib-master/docs/superpowers/specs/2026-08-26-opengu-docmap-standalone-local-git-design.md`
- Create: `GULib-master/docs/superpowers/plans/2026-08-26-opengu-docmap-standalone-local-git.md`

**Interfaces:**
- Consumes: the verified standalone repository and active-reference inventory.
- Produces: a clean scoped commit on `codex/extract-opengu-docmap-20260826`.

- [ ] **Step 1:** Remove the tracked old DocMap subtree in the isolated worktree with Git-native deletion.
- [ ] **Step 2:** Apply only active parent-reference updates; do not touch `AAGU-006`, `.workblock`, experiment outputs, or unrelated documents.
- [ ] **Step 3:** Run `git diff --check`, inspect the complete diff and staged path list, and confirm no unrelated paths.
- [ ] **Step 4:** Commit the scoped parent migration candidate and verify the worktree is clean.

### Task 5: Switch the Obsidian and rclone endpoints

**Files:**
- Modify with backup: `%APPDATA%\obsidian\obsidian.json`
- Runtime state: `%LOCALAPPDATA%\rclone\bisync\`

**Interfaces:**
- Consumes: the verified standalone repository and existing remote content.
- Produces: a registered new local vault path and initialized new-path bisync state.

- [ ] **Step 1:** Reconfirm Obsidian is stopped and the registry still points to the old exact path.
- [ ] **Step 2:** Replace only that vault path in `obsidian.json`, write UTF-8 without BOM, and read it back.
- [ ] **Step 3:** Run a new-path `rclone bisync --resync --dry-run` with the standard exclusions and inspect all proposed operations.
- [ ] **Step 4:** Run the intentional-path-change `--resync` with recovery backups, then run a normal dry run and `rclone check` requiring zero differences.
- [ ] **Step 5:** Confirm only the OpenGU DocMap pair was touched.

### Task 6: Retire the old path and integrate the parent cleanup

**Files:**
- Retire: `E:\project\OpenGU\GULib-master\文档规划`
- Integrate branch: `codex/extract-opengu-docmap-20260826`

**Interfaces:**
- Consumes: verified destination, registry, rclone pair, and clean parent candidate.
- Produces: one canonical vault location and a parent branch containing the scoped no-ff migration.

- [ ] **Step 1:** Re-read the planning record and verify all recovery paths before the destructive boundary.
- [ ] **Step 2:** Move the old vault directory to the external recovery tree rather than deleting it.
- [ ] **Step 3:** Verify the current parent worktree retains only its pre-existing unrelated state plus expected old-path deletions.
- [ ] **Step 4:** No-ff merge the clean migration branch into `codex/e7-two-surrogate-groups-20260805` with explicit paths checked before and after.
- [ ] **Step 5:** Verify the old path is absent, the new path is canonical, and unrelated `.workblock` state is unchanged.

### Task 7: Run final acceptance verification

**Files:**
- Update: `.planning/opengu-docmap-migration-20260826/{task_plan.md,findings.md,progress.md}`

**Interfaces:**
- Consumes: the complete migrated system.
- Produces: evidence for the user-facing completion report.

- [ ] **Step 1:** Compare the baseline durable-file manifest with the destination, allowing only the declared README, `.gitignore`, and link repairs.
- [ ] **Step 2:** Verify standalone Git `main` is clean, has no remote, and contains the six pre-existing modified files.
- [ ] **Step 3:** Verify parent ancestry, merge shape, scoped path list, and preservation of unrelated status.
- [ ] **Step 4:** Parse `obsidian.json` and verify the exact new vault path.
- [ ] **Step 5:** Run final `rclone check` with exclusions and require zero differences.
- [ ] **Step 6:** Run the active-link audit and report any `NOT CONFIRMED` historical or application-only behavior separately.
