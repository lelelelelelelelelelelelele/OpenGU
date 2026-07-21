# Syncmate

Syncmate is a tiny companion protocol for this repo. It does not try to turn
the project into a distributed system; its optional runner-agent is a bounded
single-runner poller, not a scheduler or remote shell. Its job is to give
local AI agents, remote AI agents, humans, and future dashboards the same view
of device identity, run artifacts, result deltas, and next safe actions.

## Principle

All tracked project files stay identical across devices. The only intentional
device-specific area is:

```text
.syncmate/
  device.yaml     # generated or edited local identity/config, untracked
  state.json      # generated local snapshot, untracked
  history.jsonl   # compact local timeline written with state snapshots, untracked
  setup_plan.md   # optional generated setup command plan, untracked
  last_preflight.json # optional latest setup/sync readiness check, untracked
  remote_status_*.json # optional saved peer snapshots or imported publish packages
  last_bundle_inspect_*.json # optional saved portable-bundle audit reports
  last_handoff_pack_inspect_*.json # optional saved evidence-pack audit reports
  bundle_*.zip    # optional portable artifact bundles for offline transfer
  handoff_pack_*.zip # optional evidence-only handoff packages, untracked
  receipt*.md     # optional post-sync evidence summaries, untracked
  checklist.md    # optional short current-state sync checklist, untracked
  runbook.md      # optional device-level operating runbook, untracked
  export_manifest.* # optional trusted downstream manifests, untracked
  results_table.* # optional trusted metric tables parsed from indexed artifacts
  workflow.json   # optional saved automation stage-state report, untracked
  automation_core.json # optional saved transfer/checksum/results ledger with artifact/result examples
  automation_core.md # optional human-readable core receipt rendered from the ledger
  acceptance.json # optional final sync acceptance verdict, untracked
  action_plan.*   # optional saved next-command plan for AI/dashboard handoff
  staging/        # optional temporary transfer area, untracked
```

Create `.syncmate/device.yaml` on each machine with `init-device`. This file is
the only intentional difference between otherwise identical checkouts.

## OpenGU Repair Profile

OpenGU cache/result invalidation is project-specific and should not be treated
as generic file sync. Use `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`
when a local collector discovers that a server-side experiment result, result
cache, selection cache, or collected trusted row is wrong and needs coordinated
repair across devices.

## MVP Commands

```bash
python scripts/syncmate/syncmate.py self
python scripts/syncmate/syncmate.py layout [node_id ...]
python scripts/syncmate/syncmate.py landings [node_id ...]
python scripts/syncmate/syncmate.py checklist [node_id ...]
python scripts/syncmate/syncmate.py runbook [node_id ...]
python scripts/syncmate/syncmate.py overview
python scripts/syncmate/syncmate.py lifecycle
python scripts/syncmate/syncmate.py smoke
python scripts/syncmate/syncmate.py runner-queue submit --recipe smoke
python scripts/syncmate/syncmate.py runner-queue contract --json
python scripts/syncmate/syncmate.py runner-queue validate --write
python scripts/syncmate/syncmate.py runner-queue run --once
python scripts/syncmate/syncmate.py runner-queue dashboard
python scripts/syncmate/syncmate.py setup-plan
python scripts/syncmate/syncmate.py init-device --role collector
python scripts/syncmate/syncmate.py add-peer <node_id> --ssh <ssh_alias> --repo-path <remote_repo>
python scripts/syncmate/syncmate.py preflight [node_id ...]
python scripts/syncmate/syncmate.py status
python scripts/syncmate/syncmate.py publish
python scripts/syncmate/syncmate.py import-publish <publish.json>
python scripts/syncmate/syncmate.py bundle
python scripts/syncmate/syncmate.py inspect-bundle <bundle.zip>
python scripts/syncmate/syncmate.py import-bundle <bundle.zip>
python scripts/syncmate/syncmate.py handoff-pack
python scripts/syncmate/syncmate.py inspect-handoff-pack <handoff_pack.zip>
python scripts/syncmate/syncmate.py fingerprint
python scripts/syncmate/syncmate.py compare [node_id ...]
python scripts/syncmate/syncmate.py progress
python scripts/syncmate/syncmate.py history
python scripts/syncmate/syncmate.py index
python scripts/syncmate/syncmate.py inventory
python scripts/syncmate/syncmate.py export
python scripts/syncmate/syncmate.py results
python scripts/syncmate/syncmate.py remote-status <node_id>
python scripts/syncmate/syncmate.py collect <node_id>
python scripts/syncmate/syncmate.py verify <node_id>
python scripts/syncmate/syncmate.py handoff [node_id ...]
python scripts/syncmate/syncmate.py refresh
python scripts/syncmate/syncmate.py sync [node_id ...]
python scripts/syncmate/syncmate.py brief
python scripts/syncmate/syncmate.py summary
python scripts/syncmate/syncmate.py reports [node_id ...]
python scripts/syncmate/syncmate.py receipt [node_id ...]
python scripts/syncmate/syncmate.py workflow [node_id ...]
python scripts/syncmate/syncmate.py automation-core [node_id ...]
python scripts/syncmate/syncmate.py acceptance [node_id ...]
python scripts/syncmate/syncmate.py next
python scripts/syncmate/syncmate.py archive-orphans
python scripts/syncmate/syncmate.py integrate
python scripts/syncmate/syncmate.py doctor
python scripts/syncmate/syncmate.py gate
python scripts/syncmate/syncmate.py dashboard
```

Default behavior is guidance-first, with one executable automation core for
results:

- `self` reports this device's role, path, git state, and setup health.
- `setup-plan` prints a safe first-run command plan for collector/runner setup.
  It does not modify `.syncmate/device.yaml` unless `--write` is used, and
  `--write` only saves `.syncmate/setup_plan.md`.
- `init-device` creates the untracked `.syncmate/device.yaml` for this checkout.
- `add-peer` records a runner/peer in the collector's untracked setup file.
- `layout` is the read-only path map. It shows `.syncmate/` state files,
  peer result roots, local landing folders, an example remote-to-local artifact
  mapping, and where trusted index/results outputs live.
- `landings` is the local result inbox view. It shows each peer landing folder,
  whether the folder exists, trusted artifact counts, complete/incomplete leaves,
  parsed result rows, and the next useful sync command.
- `checklist` is the short human/AI handoff checklist. It combines the
  acceptance verdict, landing inbox, next commands, manual actions, and useful
  report paths; `checklist --write` saves `.syncmate/checklist.md`. A full
  `sync` run writes it automatically after collect, verify, and results
  extraction complete.
- `runbook` is the device-level operating manual. It turns the current setup,
  role, peer list, landing contract, evidence files, and safest next commands
  into one page; `runbook --write` saves `.syncmate/runbook.md`.
- `overview` is the read-only status API for AI agents or dashboards. It
  combines layout, summary, gate, receipt, and next-command payloads in one
  response; use `--require-preflight --require-verify` for strict acceptance.
- `lifecycle` is the read-only setup-to-acceptance phase light. It compresses
  setup, preflight, sync, collect, verify, trusted results, and final acceptance
  into one current phase plus one primary command.
- `workflow` is the read-only stage-state API for the automation loop. It marks
  setup, remote status, diff, collect/import, verify, trusted index, results,
  and final gate stages as `ok`, `waiting`, `action-needed`, or `blocked`.
  `workflow --write` saves the same machine-readable view to
  `.syncmate/workflow.json`.
- `automation-core` is the read-only machine ledger for the executable sync
  evidence: missing artifacts, fetched artifacts, SHA-256 acceptance, trusted
  index counts, and trusted result rows. Its JSON includes compact peer-level
  examples for missing, fetched, verified, indexed, checksum-failed artifacts,
  plus trusted result rows extracted from indexed artifacts. `automation-core
  --write` saves `.syncmate/automation_core.json` and
  `.syncmate/automation_core.md`.
- `acceptance` is the final machine verdict for the automation core. It checks
  the hard evidence from preflight, checksum verification, trusted index, and
  the trusted results table, then writes `.syncmate/acceptance.json` with
  `acceptance --write`.
- `smoke` runs a temporary local end-to-end rehearsal: it creates a throwaway
  collector and local runner, writes sample artifacts, performs manifest diff,
  incremental collect, SHA-256 verify, trusted results extraction, receipt, and
  dashboard generation. It does not touch the current checkout's `.syncmate/`.
- `preflight` validates the local setup before SSH automation. It checks device
  role, peer SSH/repo fields, landing paths, result roots, and artifact policy,
  then prints the exact safe next command for the incremental sync path.
- `status` scans local `results/runs/`, writes `.syncmate/state.json`, and
  appends a compact `.syncmate/history.jsonl` event unless `--no-write-state`
  is used.
- `publish` emits a copyable local status package for a runner or collector:
  device/git/fingerprint, log progress, result layout, and a manifest inventory
  summary. `publish --write` saves `.syncmate/publish_<device_id>.json`.
- `import-publish` ingests a copied `publish` JSON package and saves it as
  `.syncmate/remote_status_<node_id>.json`. It is the offline receiver for
  `compare`, `dashboard`, `overview`, and `doctor`; it does not download files
  or mark result artifacts trusted.
- `bundle` writes a portable zip containing the same status metadata plus full
  manifest items and selected result artifacts.
- `inspect-bundle` audits a copied bundle without extracting files. It reports
  source device/git/fingerprint, manifest inventory, sample items, and
  manifest/zip structure errors. Add `--write` to save
  `.syncmate/last_bundle_inspect_<node_id>.json` for `status`, `reports`,
  `dashboard`, and AI handoff.
- `import-bundle` ingests a copied bundle, extracts only missing artifacts into
  `results/runs/<node_id>/...`, verifies SHA-256, writes `last_collect` and
  `last_verify` reports, updates `.syncmate/artifact_index.json`, and writes
  `.syncmate/results_table.*` after clean verification unless `--no-results`
  is supplied. `import-bundle --dry-run --write-plan` saves the offline delta
  as a `last_diff` report without extracting files.
- `handoff-pack` writes an evidence-only zip for another AI, device, or visual
  dashboard. It refreshes dashboard/runbook/checklist/brief by default, includes
  saved sync evidence and SHA-256s for those evidence files, but deliberately
  excludes raw `results/runs/` artifacts. Use `bundle`/`import-bundle` or
  `collect --apply` for the data path.
- `inspect-handoff-pack` audits a copied evidence pack without extracting
  files. It verifies the pack manifest, member paths, per-file SHA-256 values,
  package SHA-256, setup-file policy, and confirms no raw `results/runs/`
  artifacts are present. Add `--write` to save
  `.syncmate/last_handoff_pack_inspect_<node_id>.json`.
- `fingerprint` prints a stable local sync-state token plus component hashes,
  useful for AI/human state handoff and quick "did this side change?" checks.
- `compare` compares the local fingerprint with saved peer fingerprints from
  `.syncmate/remote_status_<node_id>.json`. It is read-only and does not SSH.
- `progress` scans recent text logs under `log/`, reports newest log age, and
  flags error-like tails without copying full log files.
- `history` shows the compact local timeline of state-writing commands, with
  deltas for result leaves, indexed artifacts, log errors, and saved reports.
- `index` shows `.syncmate/artifact_index.json`, the persistent checksum index
  of artifacts that have been verified by `collect --apply` or `verify --apply`.
  `index --check` recomputes local checksums for indexed artifacts and returns
  nonzero if any indexed file is missing, changed, or unsafe.
- `inventory` groups the trusted artifact index into experiment leaves
  (`cell/method_strategy/seed`) and highlights incomplete leaves.
- `export` emits a trusted downstream manifest from `.syncmate/artifact_index.json`.
  By default it exports only complete leaves, not every file under `results/runs`.
- `results` extracts trusted metric rows from indexed `attack.json`,
  `collateral.json`, and `_meta.json`. It never scans unverified files.
- `remote-status` prints the read-only command a collector or remote AI should
  run on the peer.
- `remote-status --apply` SSHes to the peer, captures its `status --json`
  snapshot, including the peer's lightweight `progress` log summary and stable
  `fingerprint` token, and saves `.syncmate/remote_status_<node_id>.json`.
- `collect` prints a collection plan.
- `collect --diff` SSHes to the peer, reads its manifest, and reports which
  selected artifacts are missing locally or checksum-conflicting. It writes
  `.syncmate/last_diff_<node_id>.json` unless `--no-save` is used. The report
  also includes `remote_inventory`, a per-experiment-leaf completeness summary
  of the peer manifest.
- `collect --apply` reads the remote manifest, fetches only missing selected
  artifacts, extracts them into `results/runs/<node_id>/`, and verifies SHA-256.
  Its report separates the planned delta (`to_fetch`) from artifacts that
  actually landed (`missing_fetched` / `fetched`) and checksum failures.
- `verify` prints a checksum verification plan for a peer landing.
- `verify --apply` re-reads the peer manifest, verifies that the local landing
  has every selected artifact with matching SHA-256, and writes
  `.syncmate/last_verify_<node_id>.json`. It never downloads files. A report is
  not `status=verified` if the remote manifest itself has incomplete leaves.
- `handoff` prints a peer-specific runbook for local/remote AI agents.
  `handoff --write` saves `.syncmate/handoff_<node_id>.md`.
- `refresh` first runs the local preflight gate, then runs remote status and
  diff for all configured peers, saves reports, and regenerates the dashboard.
  It only downloads when `--apply` is explicit, and only writes verification
  reports when `--verify` is explicit.
- `sync` is the one-shot executable path: status, manifest diff, incremental
  collect, checksum verify, trusted results table, dashboard, acceptance,
  receipt, and brief. It also runs the local preflight gate before any SSH call. Use
  `--dry-run` to stop after status/diff.
- `brief` prints or writes a current-state AI handoff brief with status, gate,
  top diagnostics, next commands, recent history, and useful local files.
- `summary` prints a compact status, peer, gate, and next-action digest for
  humans, AI agents, or lightweight scripts.
- `reports` inspects saved peer reports without dumping full manifests; it
  shows compact diff/collect/verify/index counts plus a few missing/conflict or
  incomplete-leaf examples.
- `receipt` summarizes the latest sync evidence: preflight state, trusted
  result-table rows, landing path, fetched files, verified checksums, indexed
  artifacts, unresolved missing/conflicts, and local artifact examples. It reads
  saved reports and does not SSH.
- `workflow` shows the saved automation state as ordered stages and includes the
  same next-command queue. It does not SSH or copy files; `--write` only saves
  `.syncmate/workflow.json`.
- `next` prints an ordered command queue plus manual actions for the current
  sync state. `next --write` saves the same queue and command contracts to
  `.syncmate/action_plan.json` and `.syncmate/action_plan.md`.
- `archive-orphans` previews safe archival for local reports/index entries that
  belong to peers no longer present in `.syncmate/device.yaml`; `--apply` moves
  old reports into `.syncmate/archive/` and rewrites only local sync state.
- `integrate` prints the local follow-up commands for aggregation/dashboard work.
- `manifest` emits a checksum manifest for local result roots. Collectors use
  the same command over SSH when applying an incremental collection.
- `doctor` turns raw status issues into recommended next actions.
  It also checks configured peers, saved remote status reports, diff reports,
  collection reports, verification reports, and orphaned local sync state for
  peers that are no longer configured.
- `gate` uses the same diagnostics as `doctor`, but returns a pass/fail exit
  code for scripts and AI agents. Use
  `gate --require-preflight --require-verify` before aggregate or integration
  steps.
- `dashboard` writes `.syncmate/status.html`, a local-only static status page.

Use `--json` when a dashboard or AI agent needs machine-readable output.

## State Fingerprint

`fingerprint` is the lightweight state check for multi-agent handoff:

```bash
python scripts/syncmate/syncmate.py fingerprint
python scripts/syncmate/syncmate.py fingerprint --json
python scripts/syncmate/syncmate.py fingerprint --expect <token-prefix>
python scripts/syncmate/syncmate.py compare
python scripts/syncmate/syncmate.py compare gpu4090 --json
```

The token is computed from setup, git state, result summaries, log error
summary, saved peer reports, artifact index, any export manifest, and any
trusted results table. By
default it excludes volatile timestamps and age strings so repeated checks of
the same state produce the same token. Use `--include-timestamps` only when you
need audit-exact report identity.

`compare` reads saved remote-status reports and compares component hashes. A
full token difference is normal across devices because `device`, `progress`,
`results`, and collector-side reports often differ. Treat `git` under
`attention_components` as the high-signal warning that tracked project files may
not be synchronized. `doctor` and `gate` surface that high-signal mismatch as
`fingerprint-attention`, so the automated path can stop before collecting or
aggregating results from a divergent checkout.

## Local History

`history` is a tiny local timeline for repeated checks:

```bash
python scripts/syncmate/syncmate.py history
python scripts/syncmate/syncmate.py history --json --limit 5
```

It is appended when commands write `.syncmate/state.json` (`status`, `refresh`,
`dashboard`, and `integrate` by default). Each entry is compact: device id, git
dirty flag, result leaf count, log error count, saved report counts, indexed
artifact count, and deltas from the previous entry. It does not store full
manifests or full snapshots. Use `--no-write-state` on state-writing commands
when you want a read-only check that does not append history.

## Progress And Logs

`progress` is intentionally observation-only:

```bash
python scripts/syncmate/syncmate.py progress
python scripts/syncmate/syncmate.py progress --json --limit 5
```

It scans `.log`/`.txt`/`.out`/`.err` files under `log/`, reads only each recent
file's tail, and reports the last non-empty line plus error-like keyword hits
such as `Traceback`, `RuntimeError`, `OOM`, `killed`, or `failed`. Full logs are
not transferred in v0. When a collector runs `remote-status <node_id> --apply`,
the remote `status --json` snapshot includes the same progress summary, so local
AI can see recent runner log health before deciding whether to collect results.

## Device Setup

Start with a dry setup plan when a checkout has no `.syncmate/device.yaml` yet:

```bash
python scripts/syncmate/syncmate.py setup-plan
python scripts/syncmate/syncmate.py setup-plan \
  --role collector \
  --device-id local-laptop \
  --peer-id gpu4090 \
  --peer-ssh autodl-4090 \
  --peer-repo-path ~/autodl-fs/OpenGU/GULib-master \
  --write

python scripts/syncmate/syncmate.py setup-plan \
  --role collector \
  --device-id local-laptop \
  --peer-id local-runner \
  --peer-local \
  --peer-repo-path ../GULib-runner-copy \
  --result-root results/runs \
  --write
```

`setup-plan` prints the exact `init-device`, runner initialization,
`add-peer`, `preflight`, `sync --dry-run`, and `sync` commands for the values you provide.
It marks each action as `needed`, `optional`, or `not-needed`; it never edits
`device.yaml`.
With `--peer-local`, it generates a same-machine rehearsal plan: no SSH runner
initialization command is emitted, and the collector-side `add-peer` command
records `transport: local` plus the runner checkout's `repo_path`.

On the collector/local side:

```bash
python scripts/syncmate/syncmate.py init-device \
  --role collector \
  --device-id local-laptop \
  --artifact-include attack.json collateral.json _meta.json
```

On a runner/server side:

```bash
python scripts/syncmate/syncmate.py init-device --role runner --device-id gpu4090 --collector-hint local-laptop
```

`init-device` refuses to overwrite an existing `.syncmate/device.yaml` unless
`--force` is explicit.

Add runner peers from the collector:

```bash
python scripts/syncmate/syncmate.py add-peer gpu4090 \
  --ssh autodl-4090 \
  --repo-path ~/autodl-fs/OpenGU/GULib-master \
  --python-executable /root/miniconda3/bin/python \
  --result-root results/runs/cora_GCN_r0.05 \
  --result-root results/runs/cora_GAT_r0.05 \
  --artifact-include attack.json collateral.json _meta.json

python scripts/syncmate/syncmate.py add-peer h800 \
  --ssh autodl-h800 \
  --repo-path ~/autodl-fs/OpenGU/GULib-master \
  --python-executable /root/miniconda3/bin/python \
  --result-root results/runs/ogbn-arxiv_GCN_r0.01 \
  --artifact-include attack.json collateral.json _meta.json predictions.npz
```

For same-machine rehearsals, demos, or two local checkouts, use local transport
instead of SSH:

```bash
python scripts/syncmate/syncmate.py add-peer local-runner \
  --local \
  --repo-path ../GULib-runner-copy \
  --result-root results/runs \
  --artifact-include attack.json collateral.json _meta.json
```

This records `transport: local` in `.syncmate/device.yaml`. The later
`remote-status`, `collect`, `verify`, `sync`, and `refresh` commands use the
same reports and landing layout as SSH peers, but read files directly from the
local `repo_path`. It is useful for checking the automation loop before renting
or reconnecting a server.

`add-peer` requires the local role to be `collector` or `runner+collector`.
Existing peer entries are protected unless `--force` is explicit. The default
landing path is `results/runs/<node_id>`.
For non-interactive SSH sessions, set `python_executable` to the peer's exact
environment interpreter; remote status, manifest, queue dispatch, and generated
handoff commands use that value instead of assuming `python` is on `PATH`.
Landing paths and result roots should be repo-relative paths without `..`;
`doctor` flags unsafe or duplicate peer landings before any transfer runs.

Collected artifacts keep the runner's run/cell layout under that landing. For
example, if `gpu4090` exposes:

```text
results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json
```

then the collector stores it as:

```text
results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json
```

Only selected artifact files are copied. Transfer and checksum reports stay in
`.syncmate/last_collect_<node_id>.json` and
`.syncmate/last_verify_<node_id>.json`.
The persistent trusted-artifact index is stored in
`.syncmate/artifact_index.json`.
After a clean verification, run `results --write --check` to parse trusted
metric rows into `.syncmate/results_table.json` and
`.syncmate/results_table.csv`; those files are generated sync state, not raw
experiment output.
`sync` runs this extraction automatically after verification unless
`--no-results` is supplied, then the same run writes the dashboard and receipt
with the new result-row counts.
To inspect the whole path contract without contacting any peer:

```bash
python scripts/syncmate/syncmate.py layout
python scripts/syncmate/syncmate.py layout gpu4090 --json
python scripts/syncmate/syncmate.py landings
python scripts/syncmate/syncmate.py landings gpu4090 --json
python scripts/syncmate/syncmate.py checklist
python scripts/syncmate/syncmate.py checklist gpu4090 --write
python scripts/syncmate/syncmate.py runbook
python scripts/syncmate/syncmate.py runbook --write
```

`layout` answers where artifacts will be read from, where they will land under
`results/runs/<node_id>/`, and where accepted checksums and trusted result rows
are recorded.
`landings` answers what is already present in those folders: which peer
landings exist locally, how many trusted artifacts are indexed, how many
complete/incomplete leaves exist, how many trusted result rows are available,
and which command is the next useful action.
`checklist` compresses that same evidence into a short Markdown handoff for the
next human or AI session: final verdict, per-peer landing status, executable
next commands, manual actions, and the important `.syncmate/` report paths.
`runbook` is wider than `checklist`: it includes setup guidance for missing
device configuration, collector and runner flows, peer commands, landing rules,
and evidence files. Use it as the first page for a new local/remote AI session.

For a single machine-readable status object, use:

```bash
python scripts/syncmate/syncmate.py overview
python scripts/syncmate/syncmate.py overview --json
python scripts/syncmate/syncmate.py overview --require-preflight --require-verify --json
python scripts/syncmate/syncmate.py lifecycle
python scripts/syncmate/syncmate.py lifecycle --json
```

`overview` does not contact peers and does not write state. It combines the
path contract from `layout`, the compact status from `summary`, the acceptance
decision from `gate`, the evidence counts from `receipt`, and the executable
queue from `next`. This is the preferred read-only payload for a future
dashboard or for another AI agent deciding what to do next.
`lifecycle` is the thinner product-facing view for the same decision. It labels
the current phase as `setup-needed`, `peer-needed`, `preflight-needed`,
`sync-needed`, `collect-needed`, `verify-needed`, `results-needed`,
`gate-needed`, `accepted`, or `review`, then points to the primary command and
the evidence files that prove the phase.

Before configuring a real peer, run the local smoke test:

```bash
python scripts/syncmate/syncmate.py smoke
python scripts/syncmate/syncmate.py smoke --keep
python scripts/syncmate/syncmate.py smoke --workdir tmp/syncmate-smoke --json
```

`smoke` uses a temporary collector plus a temporary local runner. It creates one
sample result leaf, runs the same local-transport manifest diff, incremental
collection, checksum verification, artifact indexing, results-table extraction,
receipt, and dashboard code paths, then removes the temporary workspace when it
passes. Use `--keep` or `--workdir` when you want to inspect the generated
`results/runs/local-runner/...` landing and `.syncmate/` reports.

For unusual peer layouts, use `scripts/syncmate/setup.example.yaml` as the
field reference. `--artifact-include` and `--artifact-exclude` write the same
`artifact_policy` fields safely without hand-editing YAML.

Before the first SSH call, validate the local contract:

```bash
python scripts/syncmate/syncmate.py preflight
python scripts/syncmate/syncmate.py preflight --write
python scripts/syncmate/syncmate.py preflight gpu4090 --json
```

`preflight` is read-only and does not contact the peer. It answers whether the
collector can safely enter the automation core: remote status, manifest diff,
incremental collect, checksum verify, and trusted result extraction.
`preflight --write` saves `.syncmate/last_preflight.json`, which is shown by
`brief` and `dashboard` as the latest local sync-readiness evidence. `sync` and
saved `refresh` runs update the same report with the live preflight they already
perform; `refresh --no-save` leaves it untouched.

## AI Handoff

Generate a peer-specific runbook when a local AI, remote AI, or human needs the
same operational picture:

```bash
python scripts/syncmate/syncmate.py handoff gpu4090 --write
python scripts/syncmate/syncmate.py handoff --write
```

Without node ids, `handoff --write` generates one handoff file per configured
peer plus `.syncmate/handoff_all.md`.

The handoff file records:

- the collector device and peer identity,
- remote result roots and local landing,
- the resolved artifact policy,
- the current saved workflow, Automation Core summary, and acceptance verdict
  for that peer,
- suggested next commands and manual actions derived from the saved reports,
- collector commands for preflight, status, fingerprint, compare, progress,
  history, doctor, remote-status, diff, collect, verify, summary, brief,
  workflow, automation-core, acceptance, next, inventory, export, results, gate, and
  dashboard,
- the remote-side `init-device` command for creating the runner setup marker,
- remote-side read-only commands for `self`, `progress`, `status`, and
  `manifest`,
- expected report paths under `.syncmate/`, including `workflow.json`,
  `automation_core.json`, `automation_core.md`, and `acceptance.json`.

This is deliberately a runbook, not a daemon. It gives both sides the same
next-step contract while keeping the only device-specific state under
`.syncmate/`.

## Safety Boundaries

- Code synchronization remains git-only.
- Local and peer git revisions should match before artifacts are accepted.
  `doctor` flags mismatches reported by remote status, diff, collect, or verify
  reports.
- Result synchronization is artifact-based.
- Runner nodes do not communicate with each other.
- Collector nodes pull from runners; runners do not push by default.
- Conflicts are detected and reported. Syncmate v0 does not auto-merge or
  overwrite tracked project files.
- Default artifact policy is json/meta only: `attack.json`, `collateral.json`,
  and `_meta.json`; `predictions.npz` is excluded.
- Add extra artifacts only through `.syncmate/device.yaml` `artifact_policy`
  so the collector, runner, and dashboard all see the same checksum policy.
- Incremental collection never overwrites checksum-mismatched local files unless
  `collect --apply --overwrite` is explicitly used.

## Incremental Collection

After the collector has a `.syncmate/device.yaml` with peers, check runner state:

```bash
python scripts/syncmate/syncmate.py preflight gpu4090
python scripts/syncmate/syncmate.py remote-status gpu4090 --apply
```

This writes `.syncmate/remote_status_gpu4090.json`, including the runner's
device id, role, git state, fingerprint token, result leaves, and result layout
summary.
`doctor` uses the same report to flag missing remote snapshots, remote status
errors, dirty remote worktrees, and incomplete remote artifacts.

Preview the collection plan:

```bash
python scripts/syncmate/syncmate.py collect gpu4090
```

Ask the peer what is new without downloading anything:

```bash
python scripts/syncmate/syncmate.py collect gpu4090 --diff
```

This writes `.syncmate/last_diff_gpu4090.json`, so `doctor` and `dashboard`
can show pending missing files or checksum conflicts before any transfer. It
also records remote leaf completeness, so a manifest with 90 leaves can still
show `remote_incomplete=1` when one cell has only part of the expected artifact
set.

For the normal read-only daily check, refresh every configured peer at once:

```bash
python scripts/syncmate/syncmate.py refresh
```

This runs remote status plus diff for each peer, writes the corresponding
`.syncmate/remote_status_*.json` and `.syncmate/last_diff_*.json` files, then
regenerates `.syncmate/status.html`, `.syncmate/workflow.json`, and
`.syncmate/automation_core.json`, `.syncmate/automation_core.md`,
`.syncmate/acceptance.json`,
`.syncmate/action_plan.*`, `.syncmate/runbook.md`, and `.syncmate/checklist.md`.

For the normal one-shot sync after peers are configured, use:

```bash
python scripts/syncmate/syncmate.py sync
python scripts/syncmate/syncmate.py sync gpu4090
```

`sync` is intentionally explicit: the command name means it may contact peers
and copy missing selected artifacts. It first runs the same local preflight
checks as `preflight`, saves that report to `.syncmate/last_preflight.json`, and
if they block, no SSH command is attempted. When the preflight passes, it runs
remote status, manifest diff, `collect --apply`, `verify --apply`, writes
`.syncmate/results_table.*`, then writes `.syncmate/status.html`,
`.syncmate/workflow.json`, `.syncmate/automation_core.json`,
`.syncmate/automation_core.md`, `.syncmate/acceptance.json`,
`.syncmate/action_plan.*`, `.syncmate/runbook.md`,
`.syncmate/checklist.md`, `.syncmate/receipt*.md`, `.syncmate/brief.md`,
`.syncmate/state.json`, and a history event. It still never overwrites
checksum-conflicting local files unless `--overwrite` is supplied. Use
`--no-results` when you want the transfer/verification artifacts without
regenerating the trusted metric table. Use `--no-checklist` when you want the
full sync side effects without the short handoff note.

The executable core is:

```text
preflight -> remote-status -> manifest diff -> collect missing artifacts -> verify SHA-256 -> results table -> acceptance/dashboard evidence
```

`sync` also returns an `automation_core` object in JSON mode and embeds the same
summary in the receipt, acceptance, and checklist files it writes. This is the
compact evidence ledger for the automation path: remote missing files, actually
fetched missing files, checksum-verified artifacts, checksum failures, indexed
trusted artifacts, and the trusted results-table delta
(`previous/current/added/changed/removed` rows). It is derived from the saved
diff, collect, verify, artifact-index, and results reports; it does not trust
directory timestamps or unverified files.
If you rerun `receipt --write` later, the same core transfer/checksum/results
summary is reconstructed from saved reports. The exact result-row delta is only
available during `sync`, before the previous `results_table.json` is replaced;
later receipts mark that delta as unavailable instead of guessing.

The read-only state-machine view for that same core is:

```bash
python scripts/syncmate/syncmate.py workflow --json
python scripts/syncmate/syncmate.py workflow --require-preflight --json
python scripts/syncmate/syncmate.py workflow --write
python scripts/syncmate/syncmate.py automation-core --write --json
python scripts/syncmate/syncmate.py acceptance --write --json
```

`workflow` is for AI agents and dashboards that need to know which stage is
currently `waiting`, `action-needed`, or `blocked` without running SSH or
changing sync evidence. Add `--write` to save that view as
`.syncmate/workflow.json` for another local AI, a later session, or a lightweight
visualization.
Use `automation-core --json` when an AI or visualization needs the compact
transfer/checksum/results ledger without parsing HTML or Markdown. The peer
entries include the concrete artifact examples that explain the counts:
`missing`, `fetched`, `verified`, `indexed`, `checksum_failed`, `conflicts`,
and the `trusted_results` rows parsed from the artifact index.
Use `acceptance --json` when the next actor only needs the final verdict:
whether preflight, checksum verification, trusted index, and trusted result
rows are ready to use.

The raw copied files are only a cache. The durable acceptance boundary is
`.syncmate/artifact_index.json`; `results_table.*` is derived only from indexed
artifacts whose checksums matched the peer manifest.
For a quick human check after `sync`, open `.syncmate/status.html` or read
`.syncmate/acceptance.json` or `.syncmate/receipt_<node_id>.md`: these show how
many artifacts were fetched, verified, indexed, and parsed into trusted result
rows.

Use dry-run mode when you only want to inspect remote deltas:

```bash
python scripts/syncmate/syncmate.py sync --dry-run
```

Dry-run saves remote status and diff reports but does not collect files or write
verification reports.

Run the automated v0 collection:

```bash
python scripts/syncmate/syncmate.py collect gpu4090 --apply
```

Or collect all configured peers after refreshing their status/diff:

```bash
python scripts/syncmate/syncmate.py refresh --apply
```

Collect and immediately write verification reports for every configured peer:

```bash
python scripts/syncmate/syncmate.py refresh --apply --verify
```

After collection, run the explicit acceptance check:

```bash
python scripts/syncmate/syncmate.py verify gpu4090 --apply
```

This writes `.syncmate/last_verify_gpu4090.json`. A clean verification has
`missing=0`, `conflicts=0`, `remote_incomplete=0`, and `status=verified`.
Because `verify` does not download anything, it is safe to use as a final gate
before downstream aggregation. It also refreshes
`.syncmate/artifact_index.json` with the artifacts that matched the peer
manifest.

Use the automation gate when the next step needs a machine-readable decision:

```bash
python scripts/syncmate/syncmate.py gate --require-verify
python scripts/syncmate/syncmate.py gate --require-preflight --require-verify
python scripts/syncmate/syncmate.py gate --require-preflight --require-verify --require-results
```

By default, `gate` fails on `warn` and `error` diagnostics. Use `--fail-on error`
for a more relaxed check, or `--strict` / `--fail-on info` when a workflow
should also stop on informational diagnostics.
With `--require-preflight`, `gate` requires `.syncmate/last_preflight.json` to
exist, be fresh, cover the currently configured peers, and have no blocking
errors. A warning-only preflight remains a warning, so the default gate blocks
it while `--fail-on error` can intentionally allow it.
Fingerprint attention diagnostics, especially a differing `git` component from
saved remote status, are `error` severity and therefore block even relaxed
`--fail-on error` gates.
With `--require-verify`, `gate` requires every configured peer to have a fresh
clean verification report, a trusted artifact index entry, and a passing local
`index --check` integrity scan. It also rejects incomplete trusted inventory
leaves and incomplete remote manifest leaves, so a cell with only `attack.json`
but missing `collateral.json` or `_meta.json` is blocked even when the collected
file checksums match.
With `--require-results`, `gate` also requires
`.syncmate/results_table.json` and `.syncmate/results_table.csv` to exist,
parse cleanly, and match the current trusted artifact index. If the table is
missing, stale, or parse-error-bearing, run
`python scripts/syncmate/syncmate.py results --write --check`.

For a compact handoff-sized view, use:

```bash
python scripts/syncmate/syncmate.py sync gpu4090
python scripts/syncmate/syncmate.py brief
python scripts/syncmate/syncmate.py brief --write
python scripts/syncmate/syncmate.py brief --json
python scripts/syncmate/syncmate.py summary
python scripts/syncmate/syncmate.py summary --require-verify --json
python scripts/syncmate/syncmate.py summary --require-preflight --require-verify --json
python scripts/syncmate/syncmate.py lifecycle
python scripts/syncmate/syncmate.py lifecycle --json
python scripts/syncmate/syncmate.py landings
python scripts/syncmate/syncmate.py landings gpu4090 --json
python scripts/syncmate/syncmate.py trace gpu4090
python scripts/syncmate/syncmate.py trace gpu4090 --check --json
python scripts/syncmate/syncmate.py checklist
python scripts/syncmate/syncmate.py checklist --write
python scripts/syncmate/syncmate.py runbook
python scripts/syncmate/syncmate.py runbook --write
python scripts/syncmate/syncmate.py reports gpu4090
python scripts/syncmate/syncmate.py reports --json
python scripts/syncmate/syncmate.py receipt gpu4090
python scripts/syncmate/syncmate.py receipt gpu4090 --write
python scripts/syncmate/syncmate.py workflow
python scripts/syncmate/syncmate.py workflow --json
python scripts/syncmate/syncmate.py workflow --write
python scripts/syncmate/syncmate.py automation-core --json
python scripts/syncmate/syncmate.py automation-core --write
python scripts/syncmate/syncmate.py acceptance --json
python scripts/syncmate/syncmate.py acceptance --write
python scripts/syncmate/syncmate.py next
python scripts/syncmate/syncmate.py next --require-verify
python scripts/syncmate/syncmate.py next --require-preflight --require-verify
python scripts/syncmate/syncmate.py next --require-preflight --require-verify --require-results
```

`brief` is the one-page current-state handoff. It combines the strict gate,
compact workflow stage state, Automation Core transfer/checksum/results counts,
top diagnostics, latest saved preflight, executable next commands, recent
history deltas, and pointers to
`.syncmate/state.json`, `.syncmate/history.jsonl`, `.syncmate/status.html`,
`.syncmate/workflow.json`, `.syncmate/automation_core.json`,
`.syncmate/automation_core.md`, `.syncmate/acceptance.json`,
`.syncmate/action_plan.json`,
`.syncmate/action_plan.md`, `.syncmate/checklist.md`,
`.syncmate/runbook.md`, `.syncmate/brief.md`, and
`.syncmate/last_preflight.json`. Use `brief --write` when handing work to
another AI or returning to the project later. In write mode it also refreshes
`.syncmate/action_plan.json` and `.syncmate/action_plan.md`, so the prose
handoff and the executable next-command queue stay in sync.
`checklist` is the shorter operation-facing handoff: use it when you mainly
need the current verdict, landing folders, and the next commands to run. A full
`sync` run writes `.syncmate/checklist.md`; `checklist --write` refreshes the
same note later from saved evidence.
`runbook` is the larger operating page for the current device. It is useful
when a session starts cold and needs setup commands, normal collector flow,
runner-side offline commands, peer-specific sync commands, and evidence paths
in one document.
`sync` is the preferred executable handoff command when the collector is ready
to pull current results from a peer. Use the lower-level commands below it when
you need to debug one stage at a time.
`next --require-preflight --require-verify` is the stricter AI/dashboard queue:
it inserts `preflight --write` when the saved setup-readiness report is missing,
stale, blocked, or missing a configured peer, and it ends with
`gate --require-preflight --require-verify`.
Add `--require-results` when the automation handoff should also refresh and
check the trusted metric table; `next` will insert
`results --write --check` before the final `gate` if the saved table is missing
or stale.
`summary` condenses peer reports, indexed artifacts, gate state, top
diagnostics, and suggested next actions into one short output. With
`--require-verify`, it uses the same verification and artifact-index gate as
`gate --require-verify`; with `--require-preflight`, it also requires the saved
preflight report used by `gate --require-preflight`; with `--require-results`,
it includes the same trusted results-table check used by `gate`.
`reports` is the detail view for saved per-peer reports; use it when a full
manifest JSON is too large but you still need examples of missing files,
conflicts, checksum failures, or incomplete remote leaves.
`trace` is the artifact-to-result evidence chain. It reads the trusted artifact
index and saved results table, then shows each trusted leaf's remote path,
collector landing path, per-artifact SHA-256 status, and matching result rows.
Add `--check` when you want it to re-hash local files and fail if an indexed
artifact has drifted, gone missing, or points outside the repo.
`receipt` is the post-sync evidence view. It does not contact peers; it reads
the saved diff/collect/verify reports plus `.syncmate/artifact_index.json` and
answers: where did the results land, how many files were fetched, how many
checksums were verified, which local artifacts are trusted, and what still
blocks acceptance. `receipt --write` saves `.syncmate/receipt.md` or
`.syncmate/receipt_<node_id>.md`.
`workflow` reads the same saved evidence but organizes it as a stage machine:
per peer it shows setup, remote-status, diff, collect/import, verify, and index;
globally it shows preflight, trusted results-table freshness, and final gate.
By default it requires verification/index and results-table freshness, matching
the strict automation core; use `--no-require-results` only when debugging the
transfer path before metric extraction is ready. `workflow --write` writes
`.syncmate/workflow.json`, which is also listed by `layout`, `overview`, and
`brief`.
`automation-core` reads the same saved evidence but keeps only the compact
machine ledger: transfer delta, checksum acceptance, trusted index, and trusted
result rows. `automation-core --write` writes `.syncmate/automation_core.json`
and `.syncmate/automation_core.md`.
`acceptance` reads the same hard evidence and returns the final verdict for
aggregation or handoff. By default it requires saved preflight, clean
verification/index evidence, and a fresh trusted results table. It writes
`.syncmate/acceptance.json` with `acceptance --write`.
`next` turns the same state into an ordered queue such as remote-status, diff,
collect, verify, then gate; non-executable recommendations remain under manual
actions. Each queued command also carries a small command contract in JSON:
evidence files it reads/writes/inspects and side effects such as contacting a
peer, copying selected artifacts, verifying checksums, updating the trusted
index, or extracting trusted results. Use `next --write` when this queue should
become a durable handoff artifact; it writes `.syncmate/action_plan.json` plus
`.syncmate/action_plan.md`. If the latest diff was saved by
`import-bundle --dry-run --write-plan`, `next` recommends the matching
`import-bundle <bundle.zip>` step instead of SSH/local `collect --apply`,
because bundle import performs extraction, checksum verification, artifact
indexing, and results-table refresh in one offline path.

When peers are renamed or removed, inspect obsolete local sync state:

```bash
python scripts/syncmate/syncmate.py archive-orphans
python scripts/syncmate/syncmate.py archive-orphans --apply
```

The default is dry-run. `--apply` moves orphaned report files under
`.syncmate/archive/<timestamp>_orphaned/` and saves the previous
`artifact_index.json` before removing orphaned peer entries.

The executable automation core is intentionally small:

1. Read the peer manifest, including the `remote_inventory` leaf-completeness
   summary. SSH peers run `syncmate manifest --json` remotely; local peers with
   `transport: local` scan the configured local `repo_path` directly.
2. Compare remote SHA-256 checksums with local files under the peer landing
   directory.
3. Copy only missing files into `results/runs/<node_id>/...`, stripping the
   remote `results/runs/` prefix. SSH peers stream through remote `tar`; local
   peers copy from the local filesystem.
4. Recompute SHA-256 locally, write `.syncmate/last_collect_<node_id>.json`,
   and refresh `.syncmate/artifact_index.json` with the artifacts that passed
   verification.
5. Extract metrics only from trusted indexed artifacts, writing
   `.syncmate/results_table.json` and `.syncmate/results_table.csv` for
   downstream aggregation and acceptance checks.

`collect --apply` performs the transfer and immediate checksum acceptance;
`verify --apply` can re-run the acceptance check without copying; the
`results --write --check` command performs the trusted extraction. `sync`
chains those pieces for SSH/local peers, while `import-bundle` performs the
same transfer/checksum/results sequence from a copied offline bundle.

Inspect the durable trusted-artifact index at any time:

```bash
python scripts/syncmate/syncmate.py index
python scripts/syncmate/syncmate.py index --check
python scripts/syncmate/syncmate.py inventory
python scripts/syncmate/syncmate.py inventory --only-incomplete
python scripts/syncmate/syncmate.py inventory --csv
python scripts/syncmate/syncmate.py export
python scripts/syncmate/syncmate.py export --csv
python scripts/syncmate/syncmate.py export --write --check
python scripts/syncmate/syncmate.py results
python scripts/syncmate/syncmate.py results --csv
python scripts/syncmate/syncmate.py results --write --check
python scripts/syncmate/syncmate.py trace --check
```

`inventory --csv` emits one row per trusted experiment leaf, suitable for quick
spreadsheet review or downstream scripts. `inventory --only-incomplete` is the
quick check for cells whose trusted files are hash-valid but whose expected
artifact set is still incomplete; those leaves block `gate --require-verify`.

`export` is the downstream consumption boundary. It reads only
`.syncmate/artifact_index.json`, exports complete trusted leaves by default, and
can write `.syncmate/export_manifest.json` plus
`.syncmate/export_manifest.csv`. Use `export --check` before feeding aggregate
or paper scripts when you want to re-hash local files and fail on drift.
Use `--include-incomplete` only for debugging or manual rescue work.

`results` is the metric extraction boundary. It also reads only
`.syncmate/artifact_index.json`, parses complete trusted leaves by default, and
writes `.syncmate/results_table.json` plus `.syncmate/results_table.csv` with
`--write`. Each row carries the source SHA-256 values for `attack.json`,
`collateral.json`, and `_meta.json`. `results --check` recomputes local
checksums first and returns nonzero if an indexed artifact has drifted.
`gate --require-results` uses the saved table as an acceptance artifact, so the
automated collector path becomes: incremental collect, checksum verify, trusted
index refresh, metric extraction, then result-table freshness validation.
`automation-core --write --json` is the compact receipt for that same path: it
shows what was missing, what was fetched, what checksummed, what entered the
trusted index, and which result rows were extracted. It also renders the same
ledger as `.syncmate/automation_core.md` for quick human review.
`trace --check` is the inspection view for that same boundary: it starts from
`.syncmate/artifact_index.json`, shows the remote artifact path and collector
landing path, re-hashes local files when requested, and reports which
`results_table` rows were extracted from each trusted leaf.

If a local file already exists but has a different checksum, v0 reports it as a
conflict and does not overwrite it. Use `--overwrite` only after confirming the
remote artifact is the intended source of truth.

The default artifact set is intentionally small:

```text
attack.json
collateral.json
_meta.json
```

Large `predictions.npz` files are left out of the MVP. They can be added later
as an explicit policy once the json/meta loop is boringly reliable:

```yaml
artifact_policy:
  include:
    - attack.json
    - collateral.json
    - _meta.json
    - predictions.npz
```

The same key can also be placed on a single peer entry to override only that
runner. `collect --diff`, `collect --apply`, `verify --apply`, and
`refresh --verify` pass the resolved include list to the remote
`manifest --include ...` command, then record the actual include list in the
saved diff, collect, and verify reports.

## Runner Setup Example

On a runner, `.syncmate/device.yaml` can be very small:

```yaml
version: 0
device_id: gpu4090
role: runner
repo_path: ~/autodl-fs/OpenGU/GULib-master
collector_hint: local-laptop
```

Then a remote AI can run:

```bash
python scripts/syncmate/syncmate.py self
python scripts/syncmate/syncmate.py status
python scripts/syncmate/syncmate.py publish --write
python scripts/syncmate/syncmate.py publish --include-items --json
python scripts/syncmate/syncmate.py bundle
python scripts/syncmate/syncmate.py bundle --output /tmp/bundle_gpu4090.zip
python scripts/syncmate/syncmate.py handoff-pack
python scripts/syncmate/syncmate.py inspect-handoff-pack .syncmate/handoff_pack_gpu4090.zip
```

and report the output back to the collector or a human. `publish` is useful
when SSH is not available or when a remote AI needs to hand back a compact
status package: by default it includes manifest counts and sample items; add
`--include-items` when the receiver needs the full checksum manifest.
`bundle` is the offline data path: it includes the selected artifact files
themselves, currently `attack.json`, `collateral.json`, and `_meta.json` unless
the device artifact policy says otherwise.
`handoff-pack` is the offline evidence path: it packages generated Syncmate
state, runbook/checklist/brief, peer reports, trusted result tables, and a
manifest of SHA-256s for those evidence files. It never includes raw
`results/runs/` artifacts, so it is useful for handing context to another AI or
dashboard but not for importing experiment data.
`inspect-handoff-pack` is the receiving-side audit for that evidence path: it
does not extract files, but it verifies the pack manifest, every listed evidence
file checksum, the package SHA-256, and the no-raw-artifacts boundary. Use
`inspect-handoff-pack <handoff_pack.zip> --write` when the inspection itself
should become saved local evidence.

On the collector, import a copied package before comparing state:

```bash
python scripts/syncmate/syncmate.py import-publish path/to/publish_gpu4090.json
python scripts/syncmate/syncmate.py compare gpu4090
python scripts/syncmate/syncmate.py overview --json
```

`import-publish` updates only the saved peer-status view. It tells the local AI
or dashboard what the runner says exists, including fingerprint and manifest
summary, but it does not place files under `results/runs/<node_id>/` and does
not update `.syncmate/artifact_index.json`. Use `collect --apply`,
`verify --apply`, and `results --write --check` for the trusted data path.

When SSH is unavailable but a copied bundle is available, use:

```bash
python scripts/syncmate/syncmate.py inspect-bundle path/to/bundle_gpu4090.zip --write
python scripts/syncmate/syncmate.py import-bundle path/to/bundle_gpu4090.zip --dry-run --write-plan
python scripts/syncmate/syncmate.py import-bundle path/to/bundle_gpu4090.zip
python scripts/syncmate/syncmate.py receipt gpu4090 --write
python scripts/syncmate/syncmate.py gate --require-verify
```

`import-bundle` is incremental: it compares the bundle manifest against the
collector landing and writes only missing files by default. If a local file
already exists with a different checksum, it is reported as a conflict and is
not replaced unless `--overwrite` is explicit. A successful import writes both
`.syncmate/last_collect_<node_id>.json` and
`.syncmate/last_verify_<node_id>.json`, so the normal receipt/gate/results
commands can consume the same evidence as the SSH collection path. Before any
extraction, `import-bundle` audits the bundle manifest and zip members for
missing SHA-256 values, duplicate paths, missing members, and unexpected extra
members. Bundle members are streamed to temporary files first; a file is moved
into `results/runs/<node_id>/...` only after its SHA-256 matches the bundle
manifest. After a clean saved import, `import-bundle` also writes
`.syncmate/results_table.json` and `.syncmate/results_table.csv`; pass
`--no-results` when you only want the transfer and verification reports. Run
`results --write --check` later when you want to explicitly re-hash the trusted
index and refresh the table.
Use `import-bundle --dry-run` first when you want a zero-write preview: it
reports missing files, conflicts, and `to_fetch` counts without extracting
files, writing reports, or touching `.syncmate/artifact_index.json`. Add
`--write-plan` when you want that dry-run delta to become visible to
`status`, `reports`, `dashboard`, and AI handoff; this writes only
`.syncmate/remote_status_<node_id>.json` and
`.syncmate/last_diff_<node_id>.json`, and still does not extract files,
write `last_collect`/`last_verify`, update `.syncmate/artifact_index.json`, or
write `.syncmate/results_table.*`. `next` and `summary` will treat this saved
diff as an offline bundle plan and recommend `import-bundle <bundle.zip>`
rather than `collect <node_id> --apply`. Use `--no-save` only for low-level
debugging where extraction should happen but sync reports should not be
written.
Use `inspect-bundle` when you only need to audit the package itself. It does
not require a configured peer and never compares or writes the local landing.
Without `--write` it is zero-write; with `--write` it only saves
`.syncmate/last_bundle_inspect_<node_id>.json` so the inspection becomes part
of the local status trail before import.

## Runner Queue: Bounded Runner Agent

The optional queue is a small data-only protocol, with a bounded local runner
agent. It is not an experiment launcher, general scheduler, distributed system,
or remote shell. Jobs are YAML documents in ignored
`.syncmate/runner_queue/inbox/` and move atomically through:

```text
inbox -> running -> done | failed | blocked
```

Jobs select only a static recipe id. They cannot accept shell fragments,
arguments, paths, configurations, environment values, cache operations, or
expressions. Each code-defined recipe freezes its exact argv, fixed config path
and SHA-256, expected OpenGU baseline/check-out policy, timeout, expected raw
artifact paths, success predicate, and whether controller acceptance is
eligible. Binding mismatch becomes `blocked` with expected/observed evidence.

The safe `smoke` recipe remains a temporary local SyncMate smoke check. The
first handoff-capable recipe, `opengu-preflight-v1`, binds the existing Phase B
config but writes clearly marked synthetic no-GPU preflight artifacts only; it
does not call `experiments/run.py`, conduct training, alter cache semantics, or
claim experiment results.

The formal small-graph Selection benchmark is exposed as three ordered static
recipes:

1. `opengu-small-selection-mvp-v1`: Cora × seed 42.
2. `opengu-small-selection-dataset-gate-v1`: Cora/CiteSeer/PubMed × seed 42.
3. `opengu-small-selection-full-v1`: three datasets × seeds 42/212/2024.

Their reviewed YAML files fix the dataset matrix, budgets, canonical
checkout-local `data/raw` root, ignored Cache V2/output roots, CUDA-only device,
RTX 4090 requirement, and per-cell timeout. The first stage requires empty
runtime roots; later stages require accepted prior cells and resume without
overwriting them. Before execution, the recipe blocks on a dirty checkout,
wrong Git/config binding, missing canonical data, unavailable CUDA, or a GPU
other than RTX 4090. A successful cell produces immutable `cold.json`,
`warm.json`, and `cell.json`; controller acceptance collects exactly those
files, verifies SHA-256, and checks the 17-output cold/warm/GPU contract without
coercing Selection evidence into attack/collateral result schemas.

On a checkout configured with `role: runner` or `role: runner+collector`:

```bash
# Producer: creates .syncmate/runner_queue/inbox/<id>.yaml and a receipt.
python scripts/syncmate/syncmate.py runner-queue submit --recipe smoke --requested-by operator

# Any device: inspect the protocol without running work; --write refreshes the manifest.
python scripts/syncmate/syncmate.py runner-queue validate --write
python scripts/syncmate/syncmate.py runner-queue status --json

# Runner only: exactly one job.
python scripts/syncmate/syncmate.py runner-queue run --once --json

# Runner only: supervised bounded poller, one exclusive lock and one job at a time.
python scripts/syncmate/syncmate.py runner-agent serve --poll-seconds 5
python scripts/syncmate/syncmate.py runner-agent inspect --json
# Stale work is never retried automatically; inspect first, then explicitly audit recovery.
python scripts/syncmate/syncmate.py runner-agent recover --block-running --job-id <id> --confirm

# Writes a static, browser-readable queue page from the same manifest.
python scripts/syncmate/syncmate.py runner-queue dashboard
```

Each job requires `protocol: syncmate-runner-queue/v1`, `version: 1`, a safe ID
matching its filename, an ISO timestamp, and an allowlisted recipe. Invalid,
duplicate, mismatched, or stale work blocks rather than overwriting evidence.
Claim/start/finish timestamps and binding observations live in
`receipts/<id>.json`; command outcome and bounded output live in
`results/<id>.json`; `manifest.json` is the current structured state; and
`status.html` is the matching static frontend. All stay untracked beneath
`.syncmate/`.

### SyncMate / OpenGU Integration Boundary

Runner Queue and SyncMate intentionally live together: Queue owns local job
lifecycle and declared execution; the bounded agent can poll only its local
inbox. SyncMate remains the controller, collector, checksum verifier,
trusted-index writer, and acceptance gate. OpenGU is an optional client of that
boundary, not another queue owner.

Use the read-only, machine-readable contract before adding an adapter:

```bash
python scripts/syncmate/syncmate.py runner-queue contract --json
# Optional local copy for a handoff; does not alter jobs.
python scripts/syncmate/syncmate.py runner-queue contract --write
```

From a collector, use only a configured runner peer and the fixed controller
bridge:

```bash
python scripts/syncmate/syncmate.py runner-agent dispatch <runner_id> --recipe opengu-preflight-v1 --wait --json
```

Dispatch preflights the controller, rejects unknown/non-runner peers, and sends
only validated job id, static recipe, requester, and note. `--wait` observes a
terminal result; only `done` for an acceptance-eligible recipe invokes the
normal SyncMate `sync` collection/verification/gate chain. `failed`, `blocked`,
timeout, checksum mismatch, or gate failure never becomes acceptance.

OpenGU may submit declared jobs and inspect `manifest.json`, receipts, and
results. It must not move files between queue states, add command/argument/path
fields to job YAML, invalidate caches, or treat queue completion as trusted
experiment evidence. Any future OpenGU recipe is a reviewed code-level
allowlist addition with a frozen input schema and dedicated tests—not a YAML
switch. The ready-to-use integration prompt is
[`OPENGU_RUNNER_QUEUE_INTEGRATION_PROMPT.md`](OPENGU_RUNNER_QUEUE_INTEGRATION_PROMPT.md).

## Local Status Page

Generate a local HTML page from the same snapshot used by `status` and `doctor`:

```bash
python scripts/syncmate/syncmate.py dashboard
```

Open `.syncmate/status.html` in a browser. The page stays untracked and is safe
to regenerate on each device. `dashboard` also writes
`.syncmate/workflow.json`, the machine-readable stage-state report shown in the
page, `.syncmate/automation_core.json`, the machine-readable
transfer/checksum/results ledger, `.syncmate/automation_core.md`, the
human-readable core receipt, and `.syncmate/acceptance.json`, the final machine
verdict. It also writes `.syncmate/action_plan.json` and
`.syncmate/action_plan.md`, the executable next-command plan with command
contracts, plus `.syncmate/runbook.md` and `.syncmate/checklist.md`, the two
local handoff files linked from the page. On a collector, the page also reads saved
`.syncmate/last_preflight.json`, `.syncmate/remote_status_<node_id>.json`,
`.syncmate/last_bundle_inspect_<node_id>.json`,
`.syncmate/last_diff_<node_id>.json`, `.syncmate/last_collect_<node_id>.json`, and
`.syncmate/last_verify_<node_id>.json` reports, plus
`.syncmate/results_table.json` when it exists. It also embeds the same Sync
Layout view as `layout`, the same Automation Core ledger as `receipt`, and the
same final verdict as `acceptance`. The first dashboard section is an operation
entry table with the exact local commands for `runbook`, `checklist`,
`landings`, `next --write`, `handoff-pack`, `inspect-handoff-pack`,
`sync <node_id>`, peer handoff files, and the evidence file each command writes
or inspects:
peer transport, remote result roots, local landing, example remote-to-local
artifact mapping, trusted index counts, result rows, missing/fetched/checksum
counts, and the exact `sync <node_id>` command. Running
`preflight --write`, `remote-status <node_id> --apply`,
`collect <node_id> --diff`, and `collect <node_id> --apply`, then
`verify <node_id> --apply` before `dashboard` gives the page a recent view of
readiness, automation ledger state, workflow stage state, ordered next
commands, manual actions, path layout, each runner, fingerprint component
comparison, pending delta, last transfer result, final checksum verification,
and trusted results-table status.
Reports older than 24 hours are flagged by `doctor` as stale.
