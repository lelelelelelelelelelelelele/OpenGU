# Cache source identity and generation provenance

Ordinary experiment cache matching excludes only the source-code member of the
Recipe's top-level `producer` / `producer_version` mapping. The mapping retains
its existing semantic version. New ordinary requests store `source_fingerprint:
null` in the Recipe; the Artifact header still records the real producer source.
No manual computation version or per-experiment reuse permission is introduced.

| Field | Effective matching | Preserved evidence |
|---|---|---|
| `producer[_version].source_fingerprint` | Excluded | Original header; generation and consumption producer in run cell |
| Existing producer semantic version | Included | Recipe and header |
| Checkpoint `implementation`, `trajectory_implementation` | Excluded | Unmodified checkpoint metadata; generation/consumption metadata |
| Dataset, graph, split and candidate hashes | Included | Original Recipe and payload validation |
| Parameters, Selection references and content hashes | Included | Original dependency checks |
| Actual checkpoint / ensemble state hash | Included | Verified tensor state |

Historical Recipe bytes, hash, Artifact ID, header and payload are never rewritten.
The resolver builds a process-local effective-input projection from index rows,
invalidated when the SQLite database or WAL changes. It reads no payload directory
to find candidates and persists no alias index or migrated identity. The selected
candidate is then verified against its original Recipe, header, payload hash and
dependencies. Downstream references retain that original Artifact's Recipe hash.

Different content hashes under identical effective inputs fail closed, even when
an exact historical Recipe exists. Identical bytes may reuse the earliest known
Artifact; explicit historical references remain exact. Invalid/unverified members
also block automatic reuse. Dependency conflicts block their consumers. A source
fingerprint must never be used to override a content or actual ensemble-state
conflict. Immutable provenance embedded in a payload can itself cause different
content hashes; this is still a reported conflict, not permission to ignore hash
validation or select one result.

Training/ensemble checkpoint lookup compares the producer-owned effective
metadata, then verifies the stored file SHA and tensor state hash. Multiple actual
states for the same inputs block reuse. Trajectories also retain every checkpoint
step, update learning rate and state hash. External checkpoint bytes remain exact.

Algorithm bugs require explicit scope analysis and invalidation of affected
Artifacts and their real descendants before re-execution. Ordinary code changes
no longer perform that scientific/operational decision implicitly. Do not promote
historical results to scientific validity solely because effective matching succeeds.

## Read-only audit

From the active checkout, `python -B -m scripts.cache_source_audit --store
<absolute-cache-root> --run <historical-run.json>` reports every historical cell's
metadata-level eligibility and the original references, conflicts and reasons.
Representative existing payloads are read through the real materialization seam
with a producer sentinel; their hashes/mtimes and the SQLite hash are compared.
This is engineering evidence, not a matrix run, result collection or scientific
acceptance. It does not claim all payload bytes were read or that current model
state was reconstructed for every historical cell.

The current project has no formal Artifact retire/unlink/GC writer. The audit is
not that writer and never modifies Cache V2 or SQLite. Exact deletion eligibility
requires original source, byte-level duplicate evidence, all dependency/consumer
references, retained objects, exclusive operational ownership and an approved
project-owned retirement operation. A timeout's timestamp window is only a lead.
