# Slide 2 Layout Fix Design

**Context**

After the deck typography was unified to `Times New Roman`, slide 2 (`Why Graph Unlearning Matters`) no longer feels balanced. The core problem is not content volume but layout drift: the large lead sentence dominates the page, the three cards sit too low and feel visually disconnected, and the lower-right red `Delete` callout looks cramped and detached from the grid.

**Design Goal**

Keep the current three-column structure, but rebalance slide 2 so the hierarchy is cleaner, the text positions feel intentional, and the lower-right emphasis block aligns with the rest of the page.

**Approved Scope**

- Keep the three parallel cards on slide 2.
- Do not change the slide copy.
- Reduce the visual dominance of the lead sentence.
- Move and resize the three cards so their title/body positions read as a coherent row.
- Enlarge and realign the lower-right red `Delete` callout so it reads as part of the layout rather than a floating patch.

**Chosen Approach**

Use a layout-only rebalance:
- slightly reduce and compress the lead sentence
- raise the three cards and reduce their height so the page breathes more evenly
- give the red `Delete` callout more room and align it to the third-column area

This preserves the slide structure while addressing the root cause: the previous geometry was tuned for the older font pairing and no longer fits the updated serif typography.

**Non-Goals**

- No deck-wide redesign
- No wording changes
- No new icons, images, or charts
- No changes to slides other than slide 2 unless verification reveals a regression

**Verification**

- Add a regression test that locks in the new slide-2 geometry markers in the generator source.
- Rebuild the `out-test` deck.
- Export slide 2 to PNG and visually inspect spacing, text placement, and callout alignment.
