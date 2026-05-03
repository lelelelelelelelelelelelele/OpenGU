# Metrics-Led Results Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Correct the `relative_f1_drop` explanation in the defense deck and insert a metrics-led results arc that teaches the core metrics before the audience is asked to interpret the figures.

**Architecture:** The timed deck and its speech script are both maintained as local source files under `report/0417_5003report/ppt`. The safest path is to update the source speech script and the PptxGenJS generator together so slide titles, on-slide copy, and speaker notes stay aligned. A regression test will lock in the corrected formula and the presence of the new metrics slide before we regenerate the out-test deck for visual QA.

**Tech Stack:** Node.js, PptxGenJS, Markdown, node:test, PowerPoint COM export

---

### Task 1: Add failing regression tests for the corrected metric definition and new slide structure

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
- Test: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

**Step 1: Write the failing test**

Add assertions that expect:
- a `Metrics Framework` slide in the generated script
- the corrected formula text `relative_f1_drop = F1_random_unlearn - F1_attack_unlearn`
- an explanation that shard-based methods can have negative raw drop / shard protection behavior
- revised result-slide labels such as `GraphEraser shows shard protection`

**Step 2: Run test to verify it fails**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: FAIL because the current deck still lacks the metrics slide and still uses the older informal wording.

**Step 3: Write minimal implementation**

Update the speech script and PPT generator so the corrected metrics-led structure is present.

**Step 4: Run test to verify it passes**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

### Task 2: Rewrite the speech script to follow the metrics-led storyline

**Files:**
- Modify: `report/0417_5003report/ppt/final_15min_script.md`

**Step 1: Replace the old slide-6 section**

Rewrite slide 6 as `Metrics Framework`.

**Step 2: Update results sections**

Revise slides 7–11 so they:
- define `relative_f1_drop` correctly
- explain why raw drop can mislead on GraphEraser
- introduce attribution / collateral as part of the framework rather than as a late add-on
- make the ratio figure read as an ablation-style support page

**Step 3: Update the continuous full script**

Align the long-form talk track with the revised slide order and definitions.

### Task 3: Update the PPT generator to match the new slide contents

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.js`

**Step 1: Replace slide 6**

Swap the current workflow-contribution page for a metrics summary page with compact equations and interpretation blocks.

**Step 2: Revise slides 7–11**

Update captions, readout cards, and narrative callouts so they match the corrected metrics-led story.

**Step 3: Preserve fit and pacing**

Keep the same broad deck size and ensure the new text remains visually legible.

### Task 4: Rebuild and verify the revised deck

**Files:**
- Verify: `report/0417_5003report/ppt/out-test/final_15min_defense.pptx`
- Verify: `report/0417_5003report/ppt/out-test/final_15min_script.md`

**Step 1: Run the tests**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

**Step 2: Rebuild the out-test deck**

Run: `node report/0417_5003report/ppt/build_final_15min_defense.js --output-dir report/0417_5003report/ppt/out-test`
Expected: regenerated `.pptx` and copied script markdown.

**Step 3: Export revised results slides**

Render slides 6–11 to images for visual QA.

**Step 4: Inspect the revised results block**

Check that:
- the metrics page is readable and not crowded
- the corrected formula appears clearly
- the results pages now read in the intended order
- the GraphEraser page clearly supports the shard-protection interpretation
