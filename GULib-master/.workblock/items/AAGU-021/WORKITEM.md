# AAGU-021 · 小图 D-full GIF 计时验证与线性拟合

Block ID: `AAGU-021`

Item Version: 2.1

当前状态: `registered / ready after dependency`

Item Type: Block

## Human Surface

### 核心意图

先在小图上证明 AAGU-020 的计时通道测到的确实是目标 D-full GIF 工作，并判断候选计算在受控范围内是否近似线性，再决定能否把同一探针用于昂贵的大图容量估计。

### 本次增量

在 AAGU-020 被接受并落地后，使用固定的 Cora、GCN checkpoint、split、目标集、参数、candidate ordering 和设备，对嵌套的 `N = 1, 10, 20, 30` 候选集合重复计时；分别记录共享准备、候选计算、总时长、单位候选成本、峰值显存与环境身份，并透明拟合 `T_candidate(N) = a + bN`。

### 核心验收

- 探针通过生产 Selector 使用的同一原语端到端运行，candidate IDs、分数、上下文身份和计时边界彼此一致，分数与 Selector 结果相符。
- 每个 N 在明确 warmup 后至少有三次观测，报告 median、spread、内存、拟合参数、`R^2` 与残差，不隐藏不支持线性的结果。
- paired Report 明确判断测量区间内是否支持外推；本 Block 不运行大图、排名、GU 或其他 selector 家族，成功执行本身不自动接受。

## Source

- Anchor: the registered D-full GIF primitive and timing application at `.workblock/items/AAGU-020/WORKITEM.md`.
- User-defined sequence: validate the probe on a small graph before using the identical probe on a large graph.
- Baseline: the current small-graph Selector timings mix full ScoreBundle prerequisites, scoring, ranking, and cache behavior; they do not establish the candidate-count timing law for D-full GIF alone.

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
