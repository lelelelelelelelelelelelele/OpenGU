# AAGU-021 · 小图 D-full GIF 计时验证与线性拟合

Block ID: `AAGU-021`

当前状态: `registered / ready after dependency`

Item Type: Block

## Source

- Anchor: the registered D-full GIF primitive and timing application at `.workblock/items/AAGU-020/WORKITEM.md`.
- User-defined sequence: validate the probe on a small graph before using the identical probe on a large graph.
- Baseline: the current small-graph Selector timings mix full ScoreBundle prerequisites, scoring, ranking, and cache behavior; they do not establish the candidate-count timing law for D-full GIF alone.

## Intent

- Why now: prove that the AAGU-020 timing lane measures the intended D-full GIF work and determine whether candidate computation scales linearly before spending large-graph resources.
- Change: run the accepted AAGU-020 application on a canonical small-graph context over controlled candidate counts and fit a transparent fixed-plus-linear timing model.
- Human outcome: see how shared preparation, candidate scoring, and per-candidate cost change for `N = 1, 10, 20, 30`, with enough repeated observations to judge whether linear extrapolation is justified.

## Scope

- Use canonical Cora with one fixed GCN checkpoint, split, target set, D-full GIF parameters, candidate ordering, and declared device.
- Use deterministic nested candidate subsets for `N = 1, 10, 20, 30`; retain candidate IDs and identity hashes.
- Repeat each candidate count at least three times after an explicit warmup policy and report median plus observed spread.
- Record shared-preparation time, candidate-compute time, total time, per-candidate time, peak device memory, and environment identity.
- Verify the probe scores agree with the production Selector for the same candidate IDs and context.
- Fit `T_candidate(N) = a + bN`, report `a`, `b`, `R^2`, residuals, and the measurement domain; do not hide a poor fit.
- Produce a compact paired Markdown/HTML result surface bound to this WorkItem.

## Non-goals

- Do not run ogbn-arxiv or any other large graph.
- Do not time ranking, Top-k materialization, Selection Artifact access, GU, Retrain, or Metrics.
- Do not compare all 17 selectors or generalize the fitted slope to other selector families.
- Do not treat a small-graph fit as a final large-graph runtime claim.
- Do not change the D-full GIF formula or AAGU-020 scoring contract to force a linear result.

## Acceptance contract

- Route: `practical`.
- Primary surface: timing data and model-fit judgment.
- Decision owner: human user after reviewing the compact paired report; successful execution alone does not accept the Block.
- Report size: paired `REPORT.md` and `REPORT.html` with bounded evidence.

### Acceptance items

- The small-graph probe runs end to end through the same D-full GIF primitive used by the production Selector.
- Candidate IDs, scores, context identity, and timing phase boundaries are reviewable and internally consistent.
- Repeated `N = 1, 10, 20, 30` observations expose fixed cost, candidate cost, noise, and memory rather than only one aggregate duration.
- The linear fit is reproducible from recorded observations and explicitly states whether extrapolation is supported over the measured range.
- No downstream Selector ranking or GU experiment work enters the measurements.

### Minimum evidence

- One canonical Cora identity and score-equivalence evidence tying the probe to the production Selector.
- The repeated timing table with phase-separated durations and memory observations.
- Reproducible fit parameters, residual view, and an explicit extrapolation-supported or extrapolation-not-supported judgment.

## Context and relations

- Blueprint scope: D-full GIF candidate-scaling validation before large-graph capacity estimation.
- Confirmed relation: `AAGU-021 depends_on AAGU-020`; no valid candidate can form until the AAGU-020 primitive and timing contract are accepted and applied.
- The large-graph probe remains a separate follow-up Block.

## Registration and execution boundary

- Project config: `.workblock/project.json`.
- Previewed config digest: `a1a32bb014f171660538f73756ff3b0a8dea4b62288b88f7c7a606c2d0241682`.
- Registration confirmation: the user explicitly requested registration of AAGU-021 and AAGU-022 on 2026-08-27 after defining the three-step Selector timing sequence.
- Registration creates this Record and advances the project WorkItem counter only.
- A later user-visible Codex task must use `block-workflow`, re-read AAGU-020 and this Record, and claim AAGU-021 only after its dependency is satisfied.

## Status history

- 2026-08-27: registered as the small-graph timing-validation step after AAGU-020; ready only after its dependency is accepted and applied.
