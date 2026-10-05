# Handoff: Surrogate transfer discussion and EXP-079

## Session Metadata
- Created: 2026-10-05, Asia/Shanghai
- Project: E:/project/OpenGU/GULib-master
- Branch: main
- Latest analysis commit: 9ab02266
- Scope: Continue the user's surrogate research discussion in a fresh session. No new GPU submission authorized by this handoff.

## Current State Summary
EXP-013 completed and was analyzed. We now have GIN-to-GCN figures over three datasets and six GU methods, discussion text, and conditional transfer conclusions. EXP-079 is preparing a ten-training-seed validation. Its ignored YAML preview passes the native dry-run with 2520 logical cells, but there is no formal EXP-079 config delivery, submission Recipe, GPU job, or new result. The user wants to continue discussing surrogate questions, with readable figures one at a time.

## Important Context
The user's scientific question is whether surrogate selections transfer to a GCN victim, both in selected nodes and in the response across GU methods. Do not make seed the primary comparison axis. Fix dataset, selection algorithm, and budget, average repetitions, then compare direct versus surrogate GU response vectors. Seeds quantify uncertainty and stability. Separate selection overlap, effect correlation, and absolute F1-drop magnitude.

The user corrected the earlier seed-only YAML: old seeds belong in the full matrix too; exact cache HIT avoids recomputation. We changed the preview to seeds [42,212,2024,0,1,2,3,4,5,6]. Old 756 cells plus new 1764 cells equals 2520 logical cells, not 2520 new computations. Cache reuse is conditional on matching semantic identities and existing artifacts; remote hits have NOT been checked. Evaluations and result records still execute. Cached repeats do not increase independent sample count.

Latest question: why parameter_profile_ref contains five parent segments. Live source inspection in experiments/modular_config.py:53 confirms this field resolves relative to the containing YAML, with no public-name lookup. The current preview lives under self/research/experiments/drafts/EXP-079, so ../../../../../experiments/configs/profiles/gif_idea_fixed_pt.yaml is correct there. Once formally placed under experiments/configs/exp079, use ../profiles/gif_idea_fixed_pt.yaml. Likewise surrogate selector references can become ../exp013/selectors/NAME.yaml. Do not arbitrarily shorten the current draft path, copy shared profiles, or add compatibility resolution. No path mutation was made in the handoff turn.

## Immediate Next Steps
1. Read this handoff and the existing GIN discussion report; continue in Chinese with the user's surrogate scientific question. Briefly acknowledge the YAML path explanation above, then focus on research.
2. Discuss the precise claim the ten-seed study should test: conditional selection reuse, across-GU response relationship, paired F1-drop differences, and advantage relative to Random/Degree.
3. If asked to prepare formal execution, resume EXP-079 rather than creating a duplicate experiment. Read live state and Runbook, deliver formal YAML and Recipe together, validate, and use registered synchronization/submission. Do not dispatch merely because the preview passed.
4. Analyze seven new seeds independently as follow-up evidence, then combine with the original three only after identity checks. Preserve all datasets, GU methods, surrogate architectures, and baselines unless scope is explicitly changed.

## Architecture Overview
Work Plan owns experiment lifecycle: ignored self/research/experiments/EXP-079.json is live state; tracked self/research/analyses/EXP-013.json owns analysis/decision. Pure state maintenance and analysis do not require a Block Claim. Software and formal executable-definition changes use development delivery. Formal GPU data and Cache V2 live remotely; local work is CPU analysis/dry-run/review.
Cache identity uses input/producer/dependency identities, not matrix labels or unrelated Git changes. experiments/modular_gu.py:154 resolves a cached GU output with default reuse; its producer runs only on MISS. Evaluation still runs.

## Critical Files
All paths below are repository-relative.
- self/research/experiments/EXP-079.json: live planned validation state.
- self/research/experiments/drafts/EXP-079/surrogate_multiseed.yaml: current ten-seed preview.
- self/research/experiments/drafts/EXP-079/preview-check.json: verified parameter expansion.
- self/research/experiments/drafts/EXP-079/dry-run.json: native launcher output.
- experiments/configs/exp013/surrogate_to_gcn.yaml: original executable matrix.
- self/research/analyses/EXP-013/gin_transfer_discussion_REPORT.md: paper discussion source.
- self/research/analyses/EXP-013/gin_transfer_discussion_REPORT.html: readable report.
- self/research/analyses/EXP-013/gin_transfer_figure.py: source generator for figures and discussion.
- self/research/analyses/EXP-013/gin_to_gcn_methods_gt_full.png: three-dataset multi-GU figure.
- self/research/analyses/EXP-013/gin_to_gcn_methods_r_point.png: companion selection-algorithm figure.
- self/research/analyses/EXP-013/gin_transfer_summary.csv: means, sample SD, n.
- self/research/analyses/EXP-013/gin_transfer_seed_values.csv: individual seed values.
- self/research/analyses/EXP-013/gin_transfer_contrasts.csv: paired contrasts.
- self/research/analyses/EXP-013/transfer_conclusion_REPORT.md: conditional transfer conclusions.
- self/research/analyses/EXP-013/record_transfer_conclusion.py: conclusion generator.
- self/research/analyses/EXP-013/post_analysis.py: earlier diagnostics, not the primary paper axis.
- self/research/RUNBOOK.md: current experiment process.

## Decisions Made
- Keep full ten-seed matrix, letting exact caching reuse old computations.
- Retain GCN direct, GAT, GIN, SGC, Degree, Random; six GU methods plus Retrain.
- Scientific claims remain conditional, not universal GIN substitution or statistical equivalence.
- Paper can lead with GIN-to-GCN across datasets/methods, but preserve other architectures and unsupported conditions in supplemental evidence.
- Strong correlation alone does not demonstrate surrogate necessity: Random/Degree can also correlate because GU response dominates.
- More seeds improve uncertainty estimation; they do not guarantee smaller population SD.
- Use original-graph F1 drop in percentage points. Never silently change metric semantics.
- Update source generators, not generated reports or figures by hand.

## Evidence and Research Findings
Original EXP-013: three datasets Cora/CiteSeer/PubMed; training seeds 42/212/2024; deletion budget 10% of train pool; r_point and gt_full for GCN/SGC/GAT/GIN; Degree and Random (sampling seeds 11/22/33); GNNDelete, GIF, IDEA, MEGU, GraphEraser, GraphRevoker, Retrain. GCN victim throughout. Sharded GCN methods are ensembles, so full-graph GCN direct is a reference rather than strict ensemble white-box access.

Run exp013-full-20260930-r1 / r1 completed 756 cells in 18817 seconds. Execution SHA 62926d95b843af137076eb9dd0a15e1c54c75663. A Windows command-length return issue was recovered through JSON-stdin; 1513 artifacts were verified. Do not re-open the resolved return issue merely from stale controller records. Analysis commits differ from execution SHA.

Across-GU Spearman correlations of three-seed mean F1 drop, five unique response rows (GIF and IDEA duplicate response collapsed):
- GIN gt_full: Cora 1.0, CiteSeer 0.9, PubMed 0.9.
- GIN r_point: Cora 1.0, CiteSeer 0.4, PubMed 0.3.
These are descriptive with few methods. Cora gt_full Random and Degree also correlate about 0.975 with direct; r_point Random/Degree reach 1.0. Thus do not infer unique surrogate advantage.

Examples of GIN gt_full high variation (percentage points; sample SD):
- Cora GraphEraser: 0.923, 2.583, -0.923 => 0.861 +/- 1.754.
- Cora GraphRevoker: 0, 0.923, 4.797 => 1.907 +/- 2.545.
- CiteSeer GraphEraser: -0.901, 0.150, 1.351 => 0.200 +/- 1.127.
- CiteSeer GraphRevoker: 0.150, -0.751, 0.601 => 0 +/- 0.688.
PubMed is steadier for these cases (GE 0.262 +/- 0.089; GR 0.448 +/- 0.180).
Paired direct-surrogate fluctuations can be smaller than marginal SD; inspect paired differences before blaming the surrogate. Do not attribute SGC mismatch to convexity or a GU correlation failure to a GU bug without isolating causes. SGC can be stable while GCN itself varies.

## Files Modified
Previous turn changed only ignored EXP-079 preview YAML, dry-run, preview-check, live state, and generated Work Plan pages. Dry-run confirmed all ten training seeds, Random seeds 11/22/33, budget 0.1, producer_called=false. Work Plan generation and check-links passed for 32 pages, 758 references. Formal config and Recipe remain absent.

Preview SHA256: 5a9a6543984f49dc113600e26612cfc0e99c551f72081d49bc706c6747ce1e83.
Configuration fingerprint: 655e316d244238cf759b191777582c60fce3364d767b0256c45b2d0af4f9bd5e.

EXP-079 engineering time budget is 227280 seconds (63.1 hours), a low-confidence full-scope all-MISS serial planning value required by Runbook, not a prediction of cache-reusing runtime or a launch timeout. Per-job six-hour limit still needs a formal Recipe design. Do not confuse dry-run batches with actual jobs.

## Assumptions Made
Original seven new seeds 0-6 remain the proposed follow-up scope; no user request narrowed architectures or methods. Existing evidence numbers above come from prior completed analysis in this conversation; re-read tables when making a new quantitative claim. Cache behavior was checked in current code; actual remote cache availability was not verified.

## Potential Gotchas
- Both GIF and IDEA may have identical responses; do not inflate independent method count without explaining duplicates.
- Random repeats are averaged within each training seed before computing across-seed SD.
- Three-seed uncertainty is large; avoid equivalence language and causality claims from correlation.
- Earlier mixed selector-by-seed correlation heatmap and per-seed paired presentation confused the user; do not revive these as main figures.
- YAML top-level effective defaults may display training seed42 and budget0.01; actual expanded batches hold matrix overrides. Verify batches.
- config.py parses arguments on import; avoid lightweight imports.
- Explicit UTF-8 reads/writes. Long Chinese Python source lines under gnn Python 3.8 needed an encoding cookie; use normal Python for state helpers.
- Do not overwrite other tasks' current changes listed below.

## Environment State
Use E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py <preview> --dry_run for native config checks.
Use default python for Work Plan generator (gnn Python 3.8 lacks str.removesuffix).
Generator commands: python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --check-links; then same with --check --check-links.
No job or background process was launched in this handoff. No SSH state inspection was done.
Unrelated working changes: report/progress/_Home.md; report/progress/2026-10-05_advisor-meeting/; self/research/analyses/EXP-011/table02-v2-analysis.html; self/research/analyses/EXP-011/table02-v2-tables.html. Preserve these.

