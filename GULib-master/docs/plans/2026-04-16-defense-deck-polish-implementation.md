# Defense Deck Polish Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refine the generated defense PPT so it reads as a completed MSc project defense deck and remove confirmed overlap issues on slides 10 and 12.

**Architecture:** The deck is generated from a single PptxGenJS script, so the safest path is to update content and layout there, then regenerate the PPT and re-run visual QA on the affected slides. A lightweight regression test will lock in the new slide-12 framing and prevent the old "Next Steps" wording from reappearing.

**Tech Stack:** Node.js, PptxGenJS, node:test, PowerPoint COM export for slide-image QA

---

### Task 1: Add regression coverage for the revised closing slide

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
- Test: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

**Step 1: Write the failing test**

Add assertions that expect the generated build script to emit:
- `Limitations And Future Work`
- `Future work 1`
- `Completed MSc project`

And assert that `Next step 1` is absent.

**Step 2: Run test to verify it fails**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

Expected: FAIL because the current deck still uses `Limitations And Next Steps` and `Next step 1`.

**Step 3: Write minimal implementation**

Update the slide-generation script so the closing slide uses the approved wording and shorter content.

**Step 4: Run test to verify it passes**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

Expected: PASS.

### Task 2: Reduce density and fix layout on the affected slides

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.js`

**Step 1: Adjust slide 5 copy**

Shorten the four pipeline-step descriptions and the experimental-matrix card copy.

**Step 2: Adjust slide 10 layout**

Increase spacing around the right-side explanation area and fix the `Caution` card text collision.

**Step 3: Adjust slide 12 layout**

Change the title, reduce to `2 + 2` cards, and reposition the stat card so the slide feels finished instead of crowded.

**Step 4: Rebuild the PPT**

Run: `node report/0417_5003report/ppt/build_final_15min_defense.js --output-dir report/0417_5003report/ppt`

Expected: A regenerated `final_15min_defense.pptx` and `final_15min_script.md`.

### Task 3: Visually verify the edited slides

**Files:**
- Verify: `report/0417_5003report/ppt/final_15min_defense.pptx`

**Step 1: Export slides to images**

Use PowerPoint COM export into `report/0417_5003report/ppt/rendered`.

**Step 2: Inspect slides 5, 10, and 12**

Check for:
- title/body overlap
- overly tight card padding
- clipped text
- "unfinished project" wording

**Step 3: Fix any remaining issues and re-export if needed**

Repeat until a full pass reveals no overlap on the edited slides.
