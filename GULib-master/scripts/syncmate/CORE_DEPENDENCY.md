# Independent SyncMate Core dependency

The OpenGU compatibility candidate requires the `syncmate` Python distribution at version `0.2.0` on Python 3.8 or newer. The package must expose audited Core source commit `4f0242306ba2707cbaadb9abce3c45d9ea4d0d51` through `syncmate_core.__source_commit__`.

Verify the active interpreter before using the candidate:

```powershell
python scripts/syncmate/verify_core_dependency.py --json
```

The verifier fails closed when the distribution is absent, either version source disagrees, or the audited source commit differs. It does not search sibling directories or fall back to the retained Project monolith.

A wheel built from the local Core worktree proves local packaging and disposable-install behavior only. Until the Core commits are explicitly pushed/tagged to an authorized remote, another device cannot reproduce this dependency from a published Git or package index reference; remote publication remains unverified and is outside this local migration.
