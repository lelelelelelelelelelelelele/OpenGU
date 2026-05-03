# Slide 2 Layout Fix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebalance slide 2 of the generated defense deck so the existing three-column layout looks clean and correctly aligned with `Times New Roman`.

**Architecture:** Slide 2 is generated inline inside `build_final_15min_defense.js`, so the safest change is to factor its geometry into a small local layout object and update the affected text, card, and callout positions there. A source-level regression test will lock in the new slide-2 layout markers, and the rebuilt `out-test` PPT plus exported slide image will verify the visual result.

**Tech Stack:** Node.js, PptxGenJS, node:test, PowerPoint COM export

---

### Task 1: Add a failing regression test for the approved slide-2 geometry

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
- Test: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

**Step 1: Write the failing test**

Add assertions that expect the generator source to define slide-2 layout markers for:
- a `slide2` layout object
- a compressed lead sentence geometry
- a larger aligned `Delete` callout geometry

**Step 2: Run test to verify it fails**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: FAIL because the current generator still hardcodes the old slide-2 positions inline.

**Step 3: Write minimal implementation**

Move slide-2 geometry into a local object and update the lead sentence, card row, and callout coordinates to match the approved layout.

**Step 4: Run test to verify it passes**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

### Task 2: Implement the slide-2 layout rebalance

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.js`

**Step 1: Add local slide-2 layout constants**

Create a `slide2` layout object containing the lead sentence, cards, and `Delete` callout geometry.

**Step 2: Reposition the lead sentence**

Reduce its size and height so it reads as a strong intro line without overpowering the slide.

**Step 3: Reposition the three cards**

Raise the cards, reduce their height, and keep their row alignment consistent.

**Step 4: Resize and realign the `Delete` callout**

Increase the red callout block and align it visually to the right-hand column zone.

### Task 3: Rebuild and visually verify slide 2

**Files:**
- Verify: `report/0417_5003report/ppt/out-test/final_15min_defense.pptx`
- Verify: `report/0417_5003report/ppt/out-test/qa-current/slide2.png`

**Step 1: Rebuild the out-test deck**

Run: `node report/0417_5003report/ppt/build_final_15min_defense.js --output-dir report/0417_5003report/ppt/out-test`
Expected: regenerated `.pptx` and copied script markdown.

**Step 2: Run the test suite**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

**Step 3: Export slide 2**

Use PowerPoint COM export to render slide 2 to PNG for visual QA.

**Step 4: Inspect the exported image**

Check that:
- the lead sentence no longer dominates the page
- the card row feels aligned and less scattered
- the red callout has enough internal room and no longer looks detached
