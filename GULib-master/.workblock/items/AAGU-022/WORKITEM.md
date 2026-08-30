# AAGU-022 · 大图 D-full GIF 计时探针与全量外推

Block ID: `AAGU-022`

当前状态: `registered / ready after dependency`

Item Type: Block

## Source

- Anchor: the small-graph timing-validation contract at `.workblock/items/AAGU-021/WORKITEM.md`, which in turn depends on the AAGU-020 D-full GIF primitive.
- User-defined sequence: after the identical probe is validated on a small graph, apply it to a large graph and estimate the full Selector scoring time without first running every candidate.
- Baseline: historical aggregate or small-graph Selector durations do not establish D-full GIF capacity on a large graph; the estimate must come from the same phase-separated scoring primitive on the real large-graph context.

## Intent

- Why now: obtain a decision-useful estimate of D-full GIF full-candidate scoring time and memory demand before committing to an expensive complete large-graph Selector run.
- Change: run the accepted timing probe on canonical `ogbn-arxiv` over bounded candidate subsets, verify the large-graph scaling law, and project total scoring time for the complete candidate set.
- Human outcome: see measured large-graph shared cost, candidate slope, uncertainty, memory headroom, and a clearly qualified estimate of how long a complete D-full GIF scoring pass would take.

## Scope

- Use the canonical OpenGU `ogbn-arxiv` processed graph/split, one fixed GCN checkpoint, target set, D-full GIF parameters, candidate set, and declared GPU environment.
- Reuse the exact AAGU-020 primitive and AAGU-021 timing schema; do not create a large-graph-only formula or code path.
- Begin with deterministic nested candidate subsets aligned with the small-graph schedule (`N = 1, 10, 20, 30`) and use a declared time/memory cap with fail-closed early stopping.
- Repeat feasible points sufficiently to report median and spread; retain candidate IDs, graph/split/checkpoint hashes, code identity, device identity, and peak memory.
- Separate graph/model/context preparation, target-side IHVP preparation, candidate D-full GIF computation, and total probe time.
- Fit the candidate-count model only when measured observations support it; report slope, intercept, `R^2`, residuals, uncertainty, and any degree/affected-set cost variation.
- Estimate complete-candidate scoring time as shared preparation plus the supported candidate-count projection; report the candidate denominator and assumptions explicitly.
- Produce a compact paired Markdown/HTML capacity report bound to this WorkItem.

## Non-goals

- Do not run all candidates or produce the final full ranking unless a later explicit execution decision authorizes it.
- Do not compare all 17 selectors or generalize the result beyond the fixed D-full GIF recipe and environment.
- Do not run GU, Retrain, Metrics, or a downstream attack matrix.
- Do not treat this bounded capacity probe as formal scientific effectiveness evidence.
- Do not download, reconstruct, rename, or substitute the canonical large-graph data or split.
- Do not silently fall back to CPU, change the IF formula, reduce semantic scope, or extrapolate when the measured model is not supported.

## Acceptance contract

- Route: `practical`.
- Primary surface: large-graph timing, scaling, and resource-capacity data.
- Decision owner: human user after reviewing the paired capacity report; process success alone does not accept the estimate.
- Report size: paired `REPORT.md` and `REPORT.html` with bounded evidence and an explicit recommendation.

### Acceptance items

- The probe executes the same D-full GIF primitive and phase definitions accepted on the small graph against the canonical large-graph identity.
- Every measured point binds candidate IDs, model/data identity, device, phase durations, and peak memory.
- The report distinguishes observed timings from fitted values and states whether the candidate-count model is supported.
- Any full-candidate estimate includes its denominator, assumptions, uncertainty, and resource limits rather than a bare multiplication.
- No full Selector ranking or downstream GU experiment is started by this Block without a separate explicit decision.

### Minimum evidence

- Canonical `ogbn-arxiv` preflight and identity evidence plus at least three feasible measured candidate-count points, unless a recorded resource failure itself establishes infeasibility earlier.
- Phase-separated timing and peak-memory evidence with repeated-observation spread for feasible points.
- A reproducible fit and full-candidate estimate, or a fail-closed conclusion explaining why the observed scaling does not support extrapolation.

## Context and relations

- Blueprint scope: D-full GIF large-graph scalability and Selector runtime planning.
- Confirmed relation: `AAGU-022 depends_on AAGU-021`; no valid large-graph candidate can form until the small-graph timing contract is accepted and applied.
- Through AAGU-021, this Block also inherits the accepted AAGU-020 primitive without reopening its implementation scope.

## Registration and execution boundary

- Project config: `.workblock/project.json`.
- Previewed config digest: `a9b9e5218b648a3d79dab9d401aea9762cb12fe6f2ea22d55145eb286cb6d336`.
- Registration confirmation: the user explicitly requested registration of AAGU-021 and AAGU-022 on 2026-08-27 after defining the three-step Selector timing sequence.
- Registration creates this Record and advances the project WorkItem counter only.
- Registration does not authorize SSH, GPU execution, dataset preparation, external writes, full-candidate scoring, or formal experiment dispatch.
- A later user-visible Codex task must use `block-workflow`, re-read AAGU-020/AAGU-021 and this Record, and claim AAGU-022 only after its dependency and the required execution authorization are satisfied.

## Status history

- 2026-08-27: registered as the canonical large-graph D-full GIF capacity-probe step after AAGU-021; ready only after its dependency and execution gates are satisfied.
