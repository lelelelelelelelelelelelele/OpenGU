# OpenGU Runner Queue Integration Prompt

Copy the prompt below into a future OpenGU integration task.

---

You are integrating OpenGU with the existing **SyncMate Runner Queue**. First
learn and map the boundary; do not run an experiment or change an experiment,
cache, result schema, or queue protocol until the integration plan is accepted.

## Read first

1. `CLAUDE.md` and the nearest subtree instructions.
2. `scripts/syncmate/CLAUDE.md` and `scripts/syncmate/README.md`, especially
   **Runner Queue: Bounded Runner Agent** and **SyncMate / OpenGU Integration
   Boundary**.
3. Run this read-only command and treat its JSON as the protocol contract:

   ```bash
   E:/conda_package/envs/gnn/python.exe scripts/syncmate/syncmate.py runner-queue contract --json
   ```

4. The OpenGU experiment entry points and their existing YAML/configuration
   boundaries. Also read any per-directory `CLAUDE.md` before proposing edits.

## Fixed ownership boundary

```text
OpenGU adapter: proposes/submits declared work and reads queue evidence
Runner Queue + bounded runner-agent: owns inbox -> running -> done | failed | blocked transitions
SyncMate: owns collection, checksum verification, trusted index, and acceptance gate
```

Queue completion means only that the allowlisted runner recipe completed. It is
**not** trusted experiment evidence. Trust is established only through the
normal SyncMate collection and verification path.

## Non-negotiable constraints

- Preserve `syncmate-runner-queue/v1`; use `runner-queue contract --json` as
  the exact schema/state authority.
- Queue YAML may select an allowlisted recipe only. Never introduce arbitrary
  `command`, `args`, shell, Python-expression, path, cache, or environment
  fields in a job.
- OpenGU must never move a job between `inbox`, `running`, `done`, `failed`, or
  `blocked`. Only `runner-queue run --once` or the bounded local
  `runner-agent serve` claims and transitions work.
- The runner agent may poll a local inbox under one exclusive lock and run one
  job at a time. Do not turn it into a scheduler, remote shell, multi-runner
  coordinator, distributed system, or a replacement for SyncMate.
- A controller may dispatch only through `runner-agent dispatch <configured-runner>`;
  its remote invocation is limited to validated job id, declared recipe,
  requester, and note. Do not add arbitrary remote CLI fragments.
- A running job is never auto-retried. Inspect first and use audited explicit
  recovery; every retry gets a new job id.
- Do not change training semantics, `experiments/run.py`, result schemas,
  cache invalidation, or `results/runs/` merely to make queue integration easy.
- Never treat a `done` receipt/result as enough to update paper tables or
  acceptance. Continue through SyncMate's normal collect -> SHA-256 verify ->
  artifact index -> trusted result table -> gate path.
- Preserve unrelated dirty changes. Work on a dedicated branch; do not merge or
  push without explicit authorization.

## First deliverable: integration proposal, not code

Return a concise proposal containing:

1. The current OpenGU launch/config boundary and the narrowest useful future
   runner recipe.
2. A frozen, minimal input schema for that recipe, including a stable config
   reference, expected outputs, timeout/exit behavior, and evidence handoff.
3. The exact division between queue receipt/result evidence and SyncMate's
   trusted artifact evidence.
4. Failure and blocked-state behavior, including what must remain manual.
5. Files that would change, tests to add, and a real dry-run/smoke validation
   plan that does not run a formal GPU experiment.

Do not implement the new recipe in the first response. Ask for approval after
the proposal. If approved, add the recipe only as a reviewed static allowlist
entry with dedicated tests; do not make recipe selection dynamic from YAML.

---

This prompt deliberately starts with a proposal because an OpenGU experiment
recipe must freeze its input and evidence contract before the runner can safely
execute it.
