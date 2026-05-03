# Defense Deck Recolor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Recolor the generated defense PPT into a navy-led academic deck with red used only as risk emphasis, while preserving the formal dark cover and closing slides.

**Architecture:** The recolor is centralized in the single PptxGenJS generator, so the safest approach is to update palette constants first, then rebalance card/stat usage slide by slide where repeated colored blocks currently create a templated feel. A small regression check will keep the old maroon/gold palette from returning unintentionally.

**Tech Stack:** Node.js, PptxGenJS, node:test, PowerPoint COM export for visual QA

---

### Task 1: Add regression coverage for the new palette direction

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
- Test: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

**Step 1: Write the failing test**

Read the generator source and assert that:
- the old maroon primary color is absent
- the old gold accent color is absent
- the new navy and red palette entries are present

**Step 2: Run test to verify it fails**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

Expected: FAIL while the old palette is still present.

**Step 3: Write minimal implementation**

Update the palette constants and slide color usage in the generator.

**Step 4: Run test to verify it passes**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

Expected: PASS.

### Task 2: Rebalance slide color usage

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.js`

**Step 1: Replace the global palette**

Introduce navy-led primary colors, a neutral border, and a single red emphasis color.

**Step 2: Rework recurring card patterns**

Reduce multicolor card fills on content slides. Prefer white cards with subtle borders and reserve strong fill colors for truly important callouts.

**Step 3: Preserve formal cover/closing**

Keep the cover and takeaways slides dark, but with navy instead of maroon.

**Step 4: Rebuild the PPT**

Run: `node report/0417_5003report/ppt/build_final_15min_defense.js --output-dir report/0417_5003report/ppt`

Expected: A regenerated PPT with the new palette.

### Task 3: Visually verify representative slides

**Files:**
- Verify: `report/0417_5003report/ppt/final_15min_defense.pptx`

**Step 1: Export slides to images**

Use PowerPoint COM export into `report/0417_5003report/ppt/rendered`.

**Step 2: Inspect representative slides**

Check slides 1, 4, 7, 8, 11, 12, and 13 for:
- overuse of red
- inconsistent card hierarchy
- low contrast
- new spacing regressions

**Step 3: Fix any remaining issues and re-export if needed**

Repeat until the deck feels visually coherent and no new layout problems appear.
