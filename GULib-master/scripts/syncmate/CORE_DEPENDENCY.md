# Independent SyncMate Core dependency

Only explicit SyncMate integration requires the installed `syncmate` distribution. Native OpenGU execution does not import Core or this adapter directory. The authoritative [core_dependency.json](core_dependency.json) binds version `0.5.1`, source commit `2ccd13d3403cf9e27962e563e006d2b9820b565c`, wheel SHA-256 `18c1134fe6ca5f7f0462ebe50b0a473f7e9f29a9717c2d0c6a6a168655ea7be5`, and all 72 wheel payload files. RECORD is installation metadata and is excluded.

Verify the active interpreter before integrated execution:

```powershell
python scripts/syncmate/verify_core_dependency.py --json
```

The verifier checks distribution/module versions, imported module location, complete payload file set and SHA-256, rejecting missing, modified, residual or shadowed modules. Updating this declaration binds a reviewed Core release; it does not install or upgrade Core.

Core owns `syncmate.run-handoff/v1`, the optional `syncmate.progress/v1` publisher and local query, transport, checksums and trusted indexing. OpenGU owns scientific execution, its native device/root policy, result layout, batch/stage positions and exact return declarations. The adapter maps these interfaces only when `--syncmate` is selected; failed explicit setup cannot silently become native execution.

SyncMate owns its independent `.workblock/actions/install.json`. OpenGU's install action synchronizes OpenGU code only. Recheck installed identity and the formal experiment preflight before any formal dispatch; historical endpoint verification does not establish current identity. Source provenance comes from the pinned release and installation receipt.
