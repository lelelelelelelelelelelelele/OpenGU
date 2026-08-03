# OpenGU SyncMate M1 Migration Completion Report

> Date: 2026-08-03
> Branch: `codex/syncmate-m1-opengu-20260803`
> Switch commit: `0db0a5763e3c726fe792e8993b58510104617d28`
> Core implementation commit: `1e96e479b346690458b1363b3606f72145b96561`
> Verdict: **The authorized local OpenGU migration is complete: the exact compatibility path now uses independent Core and all default-path gates pass.**

## Final ownership

- `scripts/syncmate/syncmate.py` is a 4,104-byte facade whose SHA-256 exactly matches the reviewed `syncmate_compat.py` source: `538BB6930440BD7FEF3F691CFF3547BB5E66B5E3E09B15BDE0A586466050C295`.
- Independent `syncmate_core.legacy` owns generic compatibility, transfer, queue, checksum, manifest, trusted-index/export and CLI implementation.
- OpenGU owns all 76 reviewed recipes, five preflight dispatch profiles, verified-result interpretation, Selection/GU/target-direct acceptance, cache repair and runbooks.
- `.syncmate/` remains ignored and Device-owned. `done` remains execution evidence, not project acceptance.

## Fresh verification

| Gate | Verified result |
|---|---|
| Source-backed default suite | `208 passed`, no candidate selector |
| Portable default suite | `212 passed` in Python 3.8.20 venv with only local `syncmate==0.2.0` wheel installed |
| Dependency verifier | `ready=true`; version `0.2.0`; audited source `4f0242306ba2707cbaadb9abce3c45d9ea4d0d51`; module inside venv `site-packages` |
| Compilation | default entry, M1 helper, adapter, recipes, results, acceptance and verifier exit 0 |
| Default smoke | `passed=true`, `temporary=true`, `cleaned=true` |
| Gate 1/2 | temporary and cleaned; `formal_evidence=false`; Gate 2 `project_acceptance=not_evaluated` |
| API/CLI | frozen 106 attributes plus 2 provenance attributes, missing 0; frozen 43 tested commands; old/new parser 52/52, missing 0, extra 0 |
| Recipes | 76; canonical SHA-256 `c8ae1581f2346f3c4d79e9867bcd3642703651581cad9e3357d29cf843a7adaa` |
| Core ownership | Core suite `50 passed`; concrete Project marker scan 0 |

## Switch and rollback

The user explicitly approved a four-path switch. Commit `0db0a5763e3c726fe792e8993b58510104617d28` changes only:

1. `scripts/syncmate/syncmate.py`
2. `tests/test_syncmate.py`
3. `scripts/syncmate/README.md`
4. `scripts/syncmate/CORE_DEPENDENCY.md`

Deleted files: **0**. `syncmate_compat.py`, `syncmate_m1.py`, all Project modules, repair/runbook files and historical evidence remain. If the switch itself must be undone, use `git revert 0db0a5763e3c726fe792e8993b58510104617d28`; do not reset or delete history.

## Backup and preservation

- Valid backup directory: `backups/syncmate-switch-20260803-042220`
- ZIP: `syncmate-switch-20260803-042220.zip`
- ZIP SHA-256: `7376719675EA8CE9370F3DB1BE2E39B42C3FA2CD0E35DE661C6263838EA301C5`
- Manifest: 58 copied files, 19,511,406 bytes; all 48 active untracked files covered with missing 0 and extra 0.
- Active SyncMate/OpenGU and FlowChunk porcelain-v2 snapshots match the backup exactly; their protected source hashes are unchanged.
- Feature SyncMate stayed clean; OpenGU was clean immediately after the switch commit. Active OpenGU retains the old entry SHA because active checkout modification was not authorized.

Earlier failed backup attempts are retained with `.incomplete` / `.invalid-checksums.zip` suffixes and are not cited as valid recovery artifacts.

## Authorized-scope limitations

- No merge, push, tag, publication, gitlink/submodule update, SSH connection, remote/GPU execution, or formal experiment evidence promotion occurred.
- Cross-device installation remains unverified until an authorized Core remote/tag/package source exists.
- The local feature branches are the completed implementation and evidence locations; active checkouts remain intentionally untouched.
