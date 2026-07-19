# SyncMate Bounded Runner Agent Acceptance Report

Date: 2026-07-16
Scope: `scripts/syncmate/` Runner Queue v1 upgrade only.

## Verdict

**Conditionally accepted for bounded no-GPU handoff rehearsal.** The upgrade
implements the requested agent/control boundary without changing OpenGU
training, `experiments/run.py`, result schemas, cache semantics, or formal GPU
experiments. It is not approved as a general scheduler or experiment launcher.

## Implemented boundary

| Concern | Implemented behavior |
|---|---|
| Job input | Existing `syncmate-runner-queue/v1` YAML remains data-only: id, recipe, timestamp, requester, note. |
| Recipe authority | Static code definitions freeze argv, config path/SHA-256, baseline policy, timeout, expected artifacts, predicate, and acceptance eligibility. |
| Runner | `runner-agent serve` has a 1–60 s bounded poll, one filesystem lock, and one concurrent job. |
| Recovery | A running job is never retried. `inspect` precedes explicit audited `recover`; retries use new IDs. |
| Controller | `dispatch` preflights, requires a configured runner peer, and sends only validated id/recipe/requester/note via fixed SyncMate CLI. |
| Trust | Queue `done` is execution evidence only. SyncMate still performs collect, SHA-256 verification, trusted indexing/results, and gate. |

`opengu-preflight-v1` binds the existing Phase-B config SHA-256 but writes
three isolated, explicitly synthetic no-GPU artifacts. It does not run training
or mutate cache state.

## Objective assessment of the supplied standard

The standard is sound where it matters most: static recipe authority,
single-runner locking, immutable evidence, no automatic stale retry, and
controller-side acceptance ordering eliminate the main ways a simple YAML queue
can become an unsafe remote launcher.

One wording adjustment was necessary. Requiring the runner checkout HEAD to
equal the tool's own release commit exactly makes future SyncMate fixes
self-blocking: the tool cannot run after it changes itself. The implementation
therefore accepts either the frozen baseline or an ancestor checkout whose
post-baseline changes are limited to SyncMate tooling/tests/this report. It
records expected and observed Git state and blocks any OpenGU experiment/config
change; config SHA-256 remains exact. This is a deliberate, narrow release
model—not a relaxation to arbitrary dirty or divergent checkouts.

The first preflight recipe intentionally produces a synthetic leaf that the
normal result gate does not accept as a formal experiment. That is correct:
checksum collection and verification can succeed while the final acceptance
gate refuses to promote rehearsal evidence to a research conclusion.

## Verification

| Check | Exact result |
|---|---|
| Python compilation | `gnn/python.exe -m py_compile scripts/syncmate/syncmate.py tests/test_syncmate.py` passed. |
| Full SyncMate tests | `162 passed in 5.39s`. |
| Real no-GPU recipe | `runner-preflight --recipe opengu-preflight-v1 --json` passed; exact Phase-B config SHA and baseline Git binding matched; generated three synthetic artifacts, then removed. |
| Bounded-agent state exercise | Temporary queue: `serve=completed`, stale running job=`blocked`, explicit recovery=`recovered`. |
| Unsafe dispatch exercise | Collector dispatch to a configured non-runner peer was blocked before any peer invocation. |
| Two-checkout local handoff | Controller dispatch=`submitted`; runner serve=`completed`; watch=`done`; collect fetched `3`; checksum verify reported `3` current artifacts. Final gate=`false` by design for the synthetic unknown-layout preflight leaf, so no acceptance was emitted. |

## Known limits and next step

- No remote SSH host or GPU experiment was used.
- The test-only preflight is deliberately not publishable experiment evidence.
- A future real recipe requires a separate reviewed static definition, frozen
  output predicate, tests, and explicit approval. It must not be added through
  YAML fields.
