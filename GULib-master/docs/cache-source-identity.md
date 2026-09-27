# Cache source identity and generation provenance

Every cache position retains its real source fingerprint. Source-only reuse is
explicitly registered in [one JSON file](../cache_v2/source_compatibility.json).
The [candidate helper](../cache_v2/source_compatibility.py) supplies ordered source
candidates; each storage layer retains its full identity and integrity checks.

## Lookup and maintenance

- Each group declares a stable `cache_scope`, `producer`, optional `applies_to`
  conditions, ordered `fingerprints`, a reason and evidence references. A scope is
  a cache purpose, never a disk path, function name, run or individual cache file.
- Artifact scopes use existing type names (`prediction`, `score`, `selection`,
  etc.). Producers are the GU method, Selector name, or the existing semantic
  version for other formal Artifacts. Conditions retain semantic version and,
  where needed, the exact model configuration.
- Checkpoint scopes are `training_checkpoint`, `ensemble_checkpoint`, and
  `selector_trajectory`. GraphRevoker upper and lower caches are separate groups.
  Selector training, trajectory, Score and Selection each retain their identity.
- An unregistered position or unknown current source yields only the current
  source. No null fingerprint, automatic grouping or speculative history entry.
- Query the current complete Recipe or deterministic checkpoint path first.
  Only after a clean MISS, try other members of directly applicable groups in
  file/member order, deduplicated. The current source must itself belong to each
  group used; there is no transitive expansion or unique-group requirement.
- Multiple source fields are stored as complete reviewed combinations; never
  take their Cartesian product. All non-source fields remain unchanged.
- Stop at the first valid HIT. Do not compare payloads across different Recipes.
  Invalid, unverified, corrupt or natively conflicting candidates retain existing
  fail-closed behavior; they are not converted into clean MISSes.
- The registry loads once per process, on the first lookup needing historical
  candidates. Restart the consumer after changing it. `explain_exact` remains
  exact; `explain_compatible` performs the ordered source queries.

No source-compatibility path scans the Artifact index, checkpoint directory or
trajectory payloads. No database columns, aliases, rewritten identities or cache
migration are added. Existing explicit Selection prefix-budget coverage remains
its separate, pre-existing feature.

## Preserved evidence

Recipe, Artifact ID, header, payload, dependencies and checkpoint metadata keep
their original values. Generation and consumption source are recorded separately.
The actual loaded checkpoint/ensemble state continues into downstream identity;
its hash is never substituted to force a GU HIT. Writes use the current complete
source identity. Unknown algorithm changes remain ineligible for historical reuse.

GraphRevoker fingerprints the selected model factory branch and common setup,
plus actual model initialization/forward, ensemble, partition and training
implementations. Unselected Backbone branches no longer affect its upper key.
The selected factory projection uses Python AST with normalized subscript nodes,
so Python 3.8/3.11 representation differences do not change that component.

Observer presence permits result-cache reuse. A HIT emits no execution callbacks;
its declared observation documents say `not_executed` / `result_cache_hit`, contain
no new steps or measurements, and bind the actual consumed Output. An explicitly
requested uncached run still produces fresh observations.

## Reviewed sources

AAGU-086 registers the five affected old GU methods for the reviewed GCN model,
and GraphRevoker ensemble checkpoints. Other positions use the same interface
without fabricated historical members. Fingerprints are centralized in JSON.

Evidence: canonical [AAGU-086 method review](../.workblock/items/AAGU-086/design/consensus.md),
[checkpoint metadata](../.workblock/items/AAGU-086/evidence/graphrevoker-checkpoint-metadata.json),
and the original `.syncmate/sequence-20260925-precheck/` producer/GraphRevoker
comparisons. These local evidence paths belong to the canonical project, not a
second copy in each code worktree. Historical `b51cf184` versus `116cc714` reviews
identify Observer hooks and unused factory branches; current candidate changes
restore exact identity and query/observation/provenance behavior, not algorithms.
Only those reviewed sources are included; mere presence in an inventory is not
an equivalence proof. Detailed actual read evidence is in the canonical Report.

## Read-only audit and retirement

`python -B -m scripts.cache_source_audit --store <absolute-cache-root> --run
<historical-run.json>` checks historical cells using current measured GU sources,
unchanged other inputs and the registered candidate chain. It reads representative
payloads with a producer sentinel and compares bytes/mtimes and index SHA.
This audits historical effective inputs, not a forecast of every future live
checkpoint choice or scientific acceptance. Offline inventory enumeration is
separate from normal source lookup.

No formal Artifact retire/unlink/GC writer currently exists. The audit is not
that writer. Cross-source content differences alone require neither deletion nor
query blocking. Preserve raw historical differences; retire only exact confirmed
objects through an authorized project-owned operation when available.
