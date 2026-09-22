# Independent SyncMate Core dependency

The OpenGU entry requires the installed `syncmate` distribution at version `0.4.0` on Python 3.8 or newer. [core_dependency.json](core_dependency.json) is the authoritative binding for the published source commit, wheel SHA-256, and every wheel payload file. The bound payload is source commit `a1fdf4d1be746b56587bd0210c9e7775b6960e6f`, including the existing observer/return implementation. AAGU-071 rebuilt a wheel from that exact Git archive and verified all 68 payload files against the already-installed local package. The wheel ZIP digest differs from the original installation ZIP, but every payload byte matches. No package was installed or changed by AAGU-071; version equality alone is insufficient.

Verify the active interpreter before using `scripts/syncmate/syncmate.py`:

```powershell
python scripts/syncmate/verify_core_dependency.py --json
```

The verifier checks distribution/module versions, the actual imported module location, the complete package file set, and installed file SHA-256 values against the reviewed wheel payload. It rejects missing, modified, residual, or shadowed modules. Source provenance belongs to the pinned release and installation receipt; Core no longer self-declares a commit through a Python attribute.

SyncMate owns its independent `.workblock/actions/install.json`: publish the exact source, then install the same verified wheel on the controller and SSH runner. OpenGU's install action only synchronizes OpenGU code. The current binding was verified locally. Remote installation identity must be rechecked before any formal dispatch; AAGU-071 does not claim remote verification. Subsequent checks must use the active interpreter. Remote GitHub acquisition follows the registered one-shot academic acceleration policy; a local verified wheel transferred over SSH does not require remote GitHub or PyPI access.

Version 0.4.0 adds the `syncmate.run-handoff/v1` contract: device setup stores connection facts, the project declares output layout, and each submission snapshots its route and collection scope. Executor, automatic return and manual recollection check the same contract. It automatically collects and verifies completed jobs independently of scientific acceptance, derives return scope from reviewed artifact paths, and preserves previous verified runs during scoped collection. Job-scoped watch retains full queue-health visibility. GPU execution semantics and job-envelope guards are unchanged.
