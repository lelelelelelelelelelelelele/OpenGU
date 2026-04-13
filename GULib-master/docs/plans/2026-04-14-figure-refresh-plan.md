# Figure Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign the report figures using existing experiment outputs only, without running new experiments.

**Architecture:** Freeze the current data sources and treat this task as a visualization-only refresh for the MSc report. Keep the scope centered on report readability, simpler figure narratives, and clearer mapping from metrics to method comparisons. Avoid introducing any new claims that are not already supported by the completed experiment tables.

**Tech Stack:** Markdown, Python plotting scripts, CSV/JSON experiment aggregates, PNG/PDF figure outputs

---

### Task 1: Freeze the data inputs

**Files:**
- Read: `results/evaluation/stats/final_paper_stats.csv`
- Read: `results/evaluation/stats/`
- Read: `results/paper_figures/`
- Read: `report/paper/figures/`

**Step 1: Record the frozen data sources**

Write down the exact files that are allowed as inputs for the refresh:
- `results/evaluation/stats/final_paper_stats.csv`
- any already-generated supporting CSV files in `results/evaluation/stats/`
- existing collateral and relative result aggregates already used by the plotting scripts

**Step 2: State the non-goal clearly**

Record in notes and commit messages that:
- no new experiments are to be run
- no result table is to be expanded with fresh executions
- this branch is only for visualization redesign

**Step 3: Verify existing figure inventory**

List the current figure assets from:
- `results/paper_figures/`
- `report/paper/figures/`

Expected outcome:
- identify which figures are reusable
- identify which figures should be retired or replaced for the report

### Task 2: Choose the report figure set

**Files:**
- Modify: `report/msc_progress_report_draft.md`
- Create or modify: `report/docs/figure_refresh_notes.md`

**Step 1: Define the essential report story**

Reduce the report figure set to the minimum needed for the course report. Recommended core set:
- one overall method-family comparison figure
- one GNNDelete-focused vulnerability figure
- one collateral-damage or attribution figure

**Step 2: Mark weak figures for redesign**

Current likely redesign candidates:
- `Figure 2`
- `Figure 4a` or any significance-heavy variant
- `Figure 5`

**Step 3: Decide what to demote**

Move non-essential figures to:
- supplementary status
- appendix-only use
- no-use status if they do not support the report well

### Task 3: Redesign the plots

**Files:**
- Modify: `scripts/plot_paper_figures.py`
- Modify: `scripts/plot_supp_figures.py`
- Modify: `scripts/evaluation/generate_figures.py`
- Output: `results/paper_figures/`
- Output: `report/paper/figures/`

**Step 1: Simplify Figure 2**

Possible redesign directions:
- fewer methods on one plot
- fewer ratios on one plot
- one panel per method family instead of one crowded combined plot

Expected outcome:
- the scaling story becomes readable without dense legend-hunting

**Step 2: Replace or demote Figure 4a**

Do not force a significance threshold visualization if it makes the figure harder to interpret. Consider alternatives such as:
- mean plus error bars
- effect-size-oriented comparisons
- removing the figure from the main report

Expected outcome:
- no main figure depends on a visually weak significance threshold plot

**Step 3: Redesign Figure 5**

Focus on the easiest-to-explain collateral metrics, such as:
- retrain gap
- prediction shift
- fraction flipped

Expected outcome:
- the figure directly supports the text in the report without extra explanation burden

### Task 4: Reconnect figures to the report

**Files:**
- Modify: `report/msc_progress_report_draft.md`
- Modify: `report/overleaf_upload_2026-04-14/main_report/msc_project_report.md` if the upload bundle is refreshed

**Step 1: Insert only the selected figures**

Add only the final report-grade figures to the main report body.

**Step 2: Write concise captions**

Each caption should explain:
- what metric is being shown
- what comparison the reader should notice
- why the figure matters to the report argument

**Step 3: Align text with visuals**

Ensure section text describes the same comparisons shown by the refreshed figures.

### Task 5: Verify and package

**Files:**
- Modify: `report/msc_progress_report_draft.md`
- Modify: `report/overleaf_upload_2026-04-14/`

**Step 1: Re-render figure outputs**

Run the project plotting commands needed to regenerate:
- `results/paper_figures/`
- any copied report figure outputs used in the upload bundle

**Step 2: Visually inspect outputs**

Check for:
- readable labels
- non-overlapping legends
- consistent naming
- clear grayscale/print readability where possible

**Step 3: Refresh the Overleaf upload bundle**

Copy the final chosen figures and updated report markdown into the upload folder so the next session can continue from a clean package.
