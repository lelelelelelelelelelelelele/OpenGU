# OpenGU SyncMate M1 Adapter Milestone Report

> Date: 2026-08-03
> Branch: `codex/syncmate-m1-opengu-20260803`
> Parent: `a53b14857f08c9167b17197ecb4311920607ace4`
> Verdict: **The OpenGU adapter candidate and local Gate 1/2 vertical slice are verified. The retained compatibility entry must not be replaced yet.**

## Delivered Project boundary

- Added `scripts/syncmate/opengu_adapter.py`, which owns the reviewed OpenGU `smoke` recipe, its fixed argv, normalized setup hash, project preflight, and the rule that execution completion is not formal project acceptance.
- Added `scripts/syncmate/syncmate_m1.py`, a thin candidate that imports the independent `syncmate_core` package and exposes `contract`, `smoke`, and `runner-smoke`.
- Added candidate tests and a minimal README ownership/navigation section. Existing Project recipes, result interpretation, acceptance, cache repair, runbooks, and the old compatibility file remain OpenGU-owned and unchanged.
- The exact-path runner fixture installs the candidate at `scripts/syncmate/syncmate.py` in a temporary clean Git repository, proving the intended compatibility location without changing the real old file.

## Fresh local evidence

| Check | Result |
|---|---|
| Candidate plus retained target tests | `194 passed` (`7` candidate + `187` legacy), exit 0 |
| Python compilation | old entry, candidate, and adapter exit 0 |
| Gate 1 contract | exit 0; independent Core module path reported; physical replacement false |
| Gate 1 smoke | exit 0; temporary and cleaned; formal evidence false; acceptance not evaluated |
| Gate 2 runner smoke | exit 0; exact-path clean fixture; exact Git/config SHA; fixed argv; receipt/manifest SHA; cleaned |
| Dependency warnings | two existing `llvmlite/pkg_resources` deprecation warnings |

Gate 2 used normalized setup SHA `03fb31feae5edb3fde21b9eab2fcc892fecb764e05fafe44b38c753fdde9f8a1`. The receipt recorded `status=done`, but both Core and Project layers retained `not_evaluated`; the adapter returned `accepted=false` and `formal_evidence=false`.

## Preserved boundaries

- `scripts/syncmate/syncmate.py` was not edited, replaced, copied over, or deleted. Its SHA-256 remained `B5A0700E0ED29D141B1F6997F52359CFAAAC42FFAD5DEA1E6C41E6DFE64A8BF6` in both active and feature checkouts.
- `.syncmate/` evidence existed only in temporary fixtures and was cleaned; it was not tracked.
- No merge, push, submodule/gitlink change, FlowChunk write, SSH connection, GPU execution, remote process, or remote write occurred.
- The active OpenGU checkout acquired unrelated concurrent edits during the task. This work was isolated in its feature worktree; only the target monolith hash—not the active checkout's global dirty set—is asserted unchanged.

## Why replacement is blocked

The original `tests/test_syncmate.py` imports `scripts.syncmate.syncmate` directly, so its 187 passes validate the retained monolith rather than the new candidate. The retained CLI also exposes many more commands than the candidate's three-command M1 slice. In addition, the candidate currently needs an explicitly installed or `PYTHONPATH`-supplied `syncmate_core`; without it, import fails instead of falling back to embedded Core code.

Consequently this milestone does not request approval to replace the old file. The next slice must migrate or route the remaining CLI and make the original suite exercise the candidate exact path. Only then should the exact replacement list be presented for explicit approval.

## Gate 3 status

Read-only `ssh -G opengu-4090` alias parsing succeeded. Live connectivity, remote project path, device identity, GPU capability, cache state, and `DEVICE_READY` were not verified. No remote/GPU authority was inferred.
