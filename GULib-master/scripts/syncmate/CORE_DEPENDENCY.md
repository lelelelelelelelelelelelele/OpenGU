# Independent SyncMate Core dependency

The OpenGU entry requires the installed `syncmate` distribution at version `0.3.2` on Python 3.8 or newer. [core_dependency.json](core_dependency.json) pins the published source commit, wheel SHA-256, and every wheel payload file. The current source is SyncMate commit `2866eaabec8b2805cf0f18ca656d4f71e7fb8714`; the wheel SHA-256 is `fb84dd3ff4d989a276e1c117ebde19ed9d88ff118a402b8a786bd8c0271b5d47`.

Verify the active interpreter before using `scripts/syncmate/syncmate.py`:

```powershell
python scripts/syncmate/verify_core_dependency.py --json
```

The verifier checks distribution/module versions, the actual imported module location, the complete package file set, and installed file SHA-256 values against the reviewed wheel payload. It rejects missing, modified, residual, or shadowed modules. Source provenance belongs to the pinned release and installation receipt; Core no longer self-declares a commit through a Python attribute.

SyncMate owns its independent `.workblock/actions/install.json`: publish the exact source, then install the same verified wheel on the controller and SSH runner. OpenGU's install action only synchronizes OpenGU code. The 0.3.2 wheel has been installed and read back on both endpoints; subsequent checks must use the active interpreter. Remote GitHub acquisition follows the registered one-shot academic acceleration policy; a local verified wheel transferred over SSH does not require remote GitHub or PyPI access.

Version 0.3.2 automatically collects and verifies completed jobs independently of scientific acceptance, derives return scope from reviewed artifact paths, and preserves previous verified runs during scoped collection. Job-scoped watch retains full queue-health visibility. GPU execution semantics and job-envelope guards are unchanged.
