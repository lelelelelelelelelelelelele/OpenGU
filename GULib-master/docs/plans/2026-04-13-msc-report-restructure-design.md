# MSc Report Restructure Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure the existing Markdown draft into a course-style MSc project report that remains easy to migrate to Word, PDF, and Overleaf later.

**Architecture:** Keep the main report focused on the MSc course submission requirements and rewrite the current progress- and paper-like sections into report-style sections. Move stronger paper-oriented positioning into a short companion note so the main report stays compliant while still supporting future extension.

**Tech Stack:** Markdown, existing report assets, existing project logs and summaries

---

### Task 1: Define the report structure

**Files:**
- Modify: `report/msc_progress_report_draft.md`
- Create: `report/docs/msc_report_companion_note.md`

**Step 1: Rewrite the front matter**

Replace the current title and cover page with a course-report version containing:
- approved project title
- full name placeholder
- student ID placeholder
- MSc project type placeholder
- `Dept of Electrical & Computer Engg, NUS`
- calendar year

**Step 2: Rename major sections**

Use course-report headings such as:
- Introduction
- Background and Literature Context
- Project Objectives and Scope
- Methodology and Experimental Setup
- Implementation and Experiment Progress
- Results and Analysis
- Limitations
- Future Applications and Next Steps
- Conclusion
- References

**Step 3: Remove prohibited positioning**

Delete or rewrite wording that frames the submission as:
- a progress report
- a dissertation or thesis
- a research paper or paper draft

### Task 2: Rewrite the body in report style

**Files:**
- Modify: `report/msc_progress_report_draft.md`

**Step 1: Keep the strongest evidence**

Preserve the existing concrete outcomes:
- 950 runs
- five analysis figures
- statistical aggregation
- method-family comparison
- IM-v4 efficiency result

**Step 2: Reframe unfinished items**

Move incomplete or future-facing material into:
- `7. Limitations`
- `8. Future Applications and Next Steps`

Avoid timeline promises that imply unfinished course requirements.

**Step 3: Fix consistency issues**

Resolve mismatches such as:
- six strategies vs nine strategies
- report vs paper wording
- progress-oriented declaration language

### Task 3: Add a companion note for later continuation

**Files:**
- Create: `report/docs/msc_report_companion_note.md`

**Step 1: Clarify scope**

State that the course report summarizes completed MSc project work, while later paper-oriented extensions remain outside the scope of the current submission.

**Step 2: Record migration guidance**

Capture how the Markdown can later be migrated to:
- Word or PDF for submission
- Overleaf or LaTeX for follow-up expansion

**Step 3: Record future-paper positioning**

Briefly explain that the current stage results can serve as the empirical foundation for later publication-oriented work.

### Task 4: Verify the rewritten files

**Files:**
- Modify: `report/msc_progress_report_draft.md`
- Create: `report/docs/msc_report_companion_note.md`

**Step 1: Read both files**

Check for:
- prohibited paper or thesis wording
- missing required cover-page items
- section order clarity
- obvious internal inconsistencies

**Step 2: Summarize remaining manual follow-up**

List any items the user still needs to fill manually, such as:
- approved title confirmation
- full name
- student ID
- exact MSc project type
