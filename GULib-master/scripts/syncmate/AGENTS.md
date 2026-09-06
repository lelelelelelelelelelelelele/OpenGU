# SyncMate Agent Guide

This directory contains the repository-local companion tool for experiment synchronization. Read [README.md](README.md) for the user-facing command contract; this file owns only the maintainer-facing agent guardrails.

## Boundaries

- SyncMate is a companion protocol, not a distributed system. Its optional `runner-agent serve` is a bounded single-runner poller with one local lock and one concurrent job, not a general scheduler or remote shell.
- Do not change experiment semantics, training code, research claims, matrices, or result schemas from this directory unless the user explicitly asks.
- Tracked project files stay identical across devices. Device identity and generated synchronization evidence belong under untracked `.syncmate/`.
- Runner nodes do not communicate with one another; collectors pull from runners.
- Keep Runner Queue schema v1 data-only. Reviewed static recipes bind argv, configuration SHA-256, checkout policy, timeout, expected evidence paths, and acceptance eligibility. Jobs must not gain arbitrary command, argument, path, environment, cache, or expression fields.
- A `done` job is execution evidence only. Acceptance requires the controller's normal collect, SHA-256 verification, trusted index/results, and gate chain. Failed, blocked, stale, or recovered jobs do not bypass it.
- Never auto-retry a `running` job. Inspect it first; recovery must be explicit and audited, and every retry receives a new job ID.

## OpenGU Repair Routing

SyncMate does not decide whether a defect belongs to Selection/selector logic or a GU method, and it does not infer the affected evidence range.

1. First use the rerun and cache-repair guidance in the experiment section of OpenGU DocMap to confirm the repair chain, invalidation scope, evidence boundary, and required re-acceptance.
2. Only after that decision, use the [OpenGU machine repair Runbook](OPENGU_CACHE_REPAIR_RUNBOOK.md) for the approved machine operations.

Do not add generic destructive remote cleanup or execute an unconfirmed repair. A machine procedure requires an explicit profile, exact scope, dry-run, and confirmation path.

## Evidence and Data Paths

- Raw returned artifacts land under `results/runs/`; trusted state exists only after checksum verification into `.syncmate/artifact_index.json`.
- Generic manual collection defaults to `attack.json`, `collateral.json`, and `_meta.json`. Recipe-driven collection follows its saved output contract. The ordinary modular experiment exports one summary plus independent method leaves with `attack.json`, `output-references.json`, `predictions.npz`, and `_meta.json`; its collateral comparison is separate post-processing.
- `.syncmate/device.yaml` is the only intentional per-device setup difference and remains untracked.
- SSH peer definitions may declare `python_executable`; generated and executed remote SyncMate commands must use it instead of assuming the login-shell `PATH`.
- Generated local handoff and evidence files stay under `.syncmate/`; do not promote them to tracked experiment facts.

## Command Layers

- Guidance and read-only inspection commands do not mutate collection state.
- Local setup writers may configure the local device or peer registry.
- Remote/data-movement commands require the exact reviewed peer, scope, and apply mode.
- Offline artifact transfer must preserve the same checksum and trusted-index acceptance chain as SSH collection.
- Evidence-only handoff packages must not contain or extract raw `results/runs/` artifacts.

The executable evidence chain is:

```text
preflight -> remote-status -> manifest diff -> collect/import missing artifacts -> verify SHA-256 -> artifact index -> trusted results table -> acceptance/dashboard evidence
```

Downstream aggregation must not read unverified files directly. Trusted result tables are derived from `.syncmate/artifact_index.json`.

## Validation

Use the project interpreter owned by `experiments/AGENTS.md`; do not duplicate its concrete path here. With that interpreter as `<project-python>`, validate proportionately:

```text
<project-python> -m py_compile scripts/syncmate/syncmate.py
<project-python> -m pytest tests/test_syncmate.py -q
<project-python> scripts/syncmate/syncmate.py smoke --json
```

Run the closest targeted test first, then the full SyncMate test file before treating a behavioral change as verified. Any cache cleanup must use resolved, narrow local paths and remain separate from experiment Cache/Artifact repair.

## Documentation

- [README.md](README.md) owns the user-facing contract and command details.
- This file owns agent maintenance guardrails; do not duplicate them in compatibility files.
- Update the existing SyncMate planning/progress source when behavior, command semantics, generated files, or validation results change.
