# OpenGU SyncMate M1 Migration Completion Report

> Date: 2026-08-03
> Branch: `main`
> Switch commit: `0db0a5763e3c726fe792e8993b58510104617d28`
> Core implementation commit: `1e96e479b346690458b1363b3606f72145b96561`
> Core main merge commit: `a1aa7d0657ca640dd2ee82d7ef1acbe5bbd25e52`
> OpenGU main merge commit: `3493f34ebee29098031973e5aeda7918e733bcb6`
> Verdict: **The OpenGU migration is integrated into local `main`: the exact compatibility path uses independent Core and all merged default-path gates pass.**

## Final ownership

- `scripts/syncmate/syncmate.py` is a 4,104-byte facade whose SHA-256 exactly matches the reviewed `syncmate_compat.py` source: `538BB6930440BD7FEF3F691CFF3547BB5E66B5E3E09B15BDE0A586466050C295`.
- Independent `syncmate_core.legacy` owns generic compatibility, transfer, queue, checksum, manifest, trusted-index/export and CLI implementation.
- OpenGU owns all 76 reviewed recipes, five preflight dispatch profiles, verified-result interpretation, Selection/GU/target-direct acceptance, cache repair and runbooks.
- `.syncmate/` remains ignored and Device-owned. `done` remains execution evidence, not project acceptance.

## Fresh verification

| Gate | Verified result |
|---|---|
| Source-backed default suite | `209 passed` on merged `main`, no candidate selector |
| Portable default suite | `213 passed` in Python 3.8.20 venv with only the current-main `syncmate==0.2.0` wheel installed |
| Dependency verifier | `ready=true`; version `0.2.0`; audited source `4f0242306ba2707cbaadb9abce3c45d9ea4d0d51`; module inside venv `site-packages` |
| Current-main wheel | 141,675 bytes; SHA-256 `4D556F37B2D7BB39BC6EB4E70E8B9159C3417B8BF35FF683BDB0161FCBA98850` |
| Compilation | default entry, M1 helper, adapter, recipes, results, acceptance and verifier exit 0 |
| Default smoke | `passed=true`, `temporary=true`, `cleaned=true` |
| Gate 1/2 | temporary and cleaned; `formal_evidence=false`; Gate 2 `project_acceptance=not_evaluated` |
| API/CLI | frozen 106 attributes plus 2 provenance attributes, missing 0; frozen 43 tested commands; old/new parser 52/52, missing 0, extra 0 |
| Recipes | 76; merged canonical SHA-256 `bb36f6943f7c519f9c7309a837c5e7a93598a72359d28da6fb0fa3614efc016a`; all 29 changes versus the feature digest are the approved normalized target-direct `config_sha256` |
| Core ownership | Core suite `50 passed`; concrete Project marker scan 0 |

## Switch and rollback

The user explicitly approved a four-path switch. Commit `0db0a5763e3c726fe792e8993b58510104617d28` changes only:

1. `scripts/syncmate/syncmate.py`
2. `tests/test_syncmate.py`
3. `scripts/syncmate/README.md`
4. `scripts/syncmate/CORE_DEPENDENCY.md`

Deleted files: **0**. `syncmate_compat.py`, `syncmate_m1.py`, all Project modules, repair/runbook files and historical evidence remain. To undo the complete main integration, revert merge `3493f34ebee29098031973e5aeda7918e733bcb6` with mainline parent 1; do not reset or delete history.

## Backup and preservation

- Valid backup directory: `backups/syncmate-switch-20260803-042220`
- ZIP: `syncmate-switch-20260803-042220.zip`
- ZIP SHA-256: `7376719675EA8CE9370F3DB1BE2E39B42C3FA2CD0E35DE661C6263838EA301C5`
- Manifest: 58 copied files, 19,511,406 bytes; all 48 active untracked files covered with missing 0 and extra 0.
- The dirty OpenGU docs checkout and FlowChunk remain untouched. SyncMate's two pre-existing untracked files remain untracked and were not committed.
- Immediate pre-merge recovery is under `backups/syncmate-main-integration-20260803-180056`: two verified Git bundles, five copied dirty/untracked payload files and 24 SHA-256 entries.

Earlier failed backup attempts are retained with `.incomplete` / `.invalid-checksums.zip` suffixes and are not cited as valid recovery artifacts.

## Authorized-scope limitations

- The local `main` merge is complete; no push, tag, publication or gitlink/submodule update occurred.
- A bounded read-only SSH probe passed transport/authentication and found `/autodl-fs/data/OpenGU/GULib-master`; it wrote no remote state.
- Remote deployment remains pending: the remote new verifier is absent and the current container exposes zero GPU device nodes. No GPU job, formal experiment or evidence promotion occurred.
