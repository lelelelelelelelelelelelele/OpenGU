# Defense Deck Font Update Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Unify the generated 15-minute defense deck typography so every slide uses `Times New Roman`.

**Architecture:** The deck typography is controlled centrally in `build_final_15min_defense.js` through heading/body font constants and shared text helpers. The safest implementation is to update those constants, add a small regression test for the expected font family, then rebuild the `out-test` presentation to confirm the generator still produces the deck assets.

**Tech Stack:** Node.js, PptxGenJS, node:test

---

### Task 1: Lock in the approved font family with a regression test

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
- Test: `report/0417_5003report/ppt/build_final_15min_defense.test.mjs`

**Step 1: Write the failing test**

Add assertions that expect the generator source to contain `Times New Roman` and reject `Georgia` and `Calibri`.

**Step 2: Run test to verify it fails**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: FAIL because the current generator still defines `Georgia` / `Calibri`.

**Step 3: Write minimal implementation**

Update the generator font constants so both heading and body text resolve to `Times New Roman`.

**Step 4: Run test to verify it passes**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

### Task 2: Apply the font change in the deck generator

**Files:**
- Modify: `report/0417_5003report/ppt/build_final_15min_defense.js`

**Step 1: Update heading font constant**

Set the shared heading font constant to `Times New Roman`.

**Step 2: Update body font constant**

Set the shared body font constant to `Times New Roman`.

**Step 3: Review for stray hard-coded font references**

Confirm the script no longer references `Georgia` or `Calibri`.

### Task 3: Rebuild and verify generated artifacts

**Files:**
- Verify: `report/0417_5003report/ppt/out-test/final_15min_defense.pptx`
- Verify: `report/0417_5003report/ppt/out-test/final_15min_script.md`

**Step 1: Rebuild the out-test deck**

Run: `node report/0417_5003report/ppt/build_final_15min_defense.js --output-dir report/0417_5003report/ppt/out-test`
Expected: regenerated `.pptx` and copied script markdown.

**Step 2: Run the regression test suite**

Run: `node --test report/0417_5003report/ppt/build_final_15min_defense.test.mjs`
Expected: PASS.

**Step 3: Sanity-check the outputs**

Confirm the rebuilt `out-test` directory still contains the expected presentation and script files after the font change.
