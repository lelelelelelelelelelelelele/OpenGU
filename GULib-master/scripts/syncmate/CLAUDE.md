# SyncMate Maintenance Notes

This folder contains the repo-local companion tool for local/server experiment
synchronization. Read `scripts/syncmate/README.md` for the user-facing contract;
this file is the maintainer-facing guardrail for AI agents.

## Boundaries

- SyncMate is a companion protocol, not a distributed system. Its optional
  `runner-agent serve` is a bounded single-runner poller (one local lock, one
  concurrent job), not a general scheduler or remote shell.
- Do not change experiment semantics, training code, or result schemas while
  working in this folder unless the user explicitly asks for that.
- Tracked project files should stay identical across devices. Device-specific
  identity and generated sync evidence belong under untracked `.syncmate/`.
- Runner nodes do not communicate with each other. Collectors pull from runners.
- Keep `runner-queue` YAML schema v1 data-only. Recipes are reviewed static
  code metadata that bind argv, config SHA-256, checkout policy, timeout,
  expected evidence paths, and acceptance eligibility. Never add command,
  argument, path, environment, cache, or expression fields to jobs.
- A `done` queue result is execution evidence only. Only the controller's
  normal collect -> SHA-256 verify -> trusted index/results -> gate sequence
  can accept evidence. Failed/blocked/stale jobs never enter that sequence.
- Never auto-retry `running` jobs. Use `runner-agent inspect`, then an explicit
  audited `runner-agent recover`; a retry always receives a new job id.
- Raw artifacts live under `results/runs/`; trusted state is derived only after
  checksum verification into `.syncmate/artifact_index.json`.
- OpenGU-specific cache/result invalidation guidance lives in
  `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`. Do not add generic
  destructive remote cleanup without an explicit profile, scope, dry-run, and
  confirmation path.

## Data Paths

- `results/runs/<node_id>/<cell>/<method_strategy>/<seed>/` is the collector
  landing layout for peer artifacts.
- Default trusted artifacts are `attack.json`, `collateral.json`, and
  `_meta.json`. `predictions.npz` is intentionally not included by default.
- `.syncmate/device.yaml` is the only intentional per-device setup difference
  and must remain untracked.
- `.syncmate/action_plan.*`, `workflow.json`, `automation_core.json`,
  `automation_core.md`,
  `acceptance.json`, `runbook.md`, `checklist.md`, `brief.md`, and
  `status.html` are generated local handoff/evidence files.

## Command Layers

- Guidance/read-only: `self`, `layout`, `landings`, `overview`, `lifecycle`, `summary`,
  `trace`, `reports`, `workflow`, `automation-core`, `acceptance`, `next`, `doctor`,
  `gate`, `fingerprint`, `compare`, `progress`, `history`, `index`,
  `inventory`, `export`, and `results` without `--write`.
- Local setup writers: `setup-plan --write`, `init-device`, `add-peer`.
- Remote/data movement: `remote-status --apply`, `collect --diff`,
  `collect --apply`, `verify --apply`, `refresh --apply`, and `sync`.
- Offline artifact transfer: `bundle`, `inspect-bundle`, `import-bundle`.
- Evidence-only transfer: `handoff-pack` and `inspect-handoff-pack`; these must
  not include or extract raw `results/runs/` artifacts.

## Automation Core

The executable core is:

```text
preflight -> remote-status -> manifest diff -> collect/import missing artifacts -> verify SHA-256 -> artifact index -> trusted results table -> acceptance/dashboard evidence
```

Do not make downstream aggregation read directly from unverified files.
`results_table.*` must be derived from `.syncmate/artifact_index.json`.
Keep `automation-core` focused on this chain: incremental delta, fetched
artifacts, SHA-256 verification, trusted index entries, and extracted trusted
result rows.

## Validation

Use the root project Python:

```bash
E:/conda_package/envs/gnn/python.exe -m py_compile scripts/syncmate/syncmate.py
E:/conda_package/envs/gnn/python.exe -m pytest tests/test_syncmate.py -q
E:/conda_package/envs/gnn/python.exe scripts/syncmate/syncmate.py smoke --json
```

For narrow changes, run the closest targeted pytest subset first, then run the
full SyncMate test file before treating a code change as verified.

After test runs, remove local caches if they were created:

```powershell
Remove-Item -Recurse -Force .pytest_cache, scripts/syncmate/__pycache__, tests/__pycache__ -ErrorAction SilentlyContinue
```

Use a path-safety check before any broader cleanup.

## Documentation Rules

- Keep `README.md` as the user-facing source of truth.
- Keep this file short and focused on maintenance guardrails.
- Update `.planning/syncmate/progress.md` when a SyncMate iteration changes
  behavior, command semantics, generated files, or validation results.
