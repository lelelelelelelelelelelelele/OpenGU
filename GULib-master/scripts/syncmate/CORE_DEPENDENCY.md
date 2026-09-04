# Independent SyncMate Core dependency

The OpenGU entry requires the installed `syncmate` distribution at version `0.3.1` on Python 3.8 or newer. [core_dependency.json](core_dependency.json) pins the published source commit, wheel SHA-256, and every wheel payload file. The current source is SyncMate commit `114b8af29065a90e56919b8922369bd21bdce2c2`; the wheel SHA-256 is `db1d59ec4e8a57e81dd4735eba48defc465e65404fdb1e1b93478bd90f3b717f`.

Verify the active interpreter before using `scripts/syncmate/syncmate.py`:

```powershell
python scripts/syncmate/verify_core_dependency.py --json
```

The verifier checks distribution/module versions, the actual imported module location, the complete package file set, and installed file SHA-256 values against the reviewed wheel payload. It rejects missing, modified, residual, or shadowed modules. Source provenance belongs to the pinned release and installation receipt; Core no longer self-declares a commit through a Python attribute.

SyncMate owns its independent `.workblock/actions/install.json`: publish the exact source, then install the same verified wheel on the controller and SSH runner. OpenGU's install action only synchronizes OpenGU code. The 0.3.1 wheel has been installed and read back on both endpoints; subsequent checks must use the active interpreter. Remote GitHub acquisition follows the registered one-shot academic acceleration policy; a local verified wheel transferred over SSH does not require remote GitHub or PyPI access.

Version 0.3.1 repairs job-scoped watch when unrelated historical queue records are malformed. The full queue health remains visible. GPU execution semantics and job-envelope guards are unchanged.
