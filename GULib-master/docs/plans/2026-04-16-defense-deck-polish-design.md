# Defense Deck Polish Design

**Context**

The current 15-minute defense deck is already presentation-ready, but several slides still create a "working draft" impression in a final-defense setting. The most important issues are: slide 12 still reads like an unfinished project update, and slides 10 and 12 contain visible text overlap in the rendered deck. Slide 5 is also text-heavy for a short oral presentation.

**Design Goal**

Refine the generated PPT so it reads as a completed MSc project defense deck: concise, visually stable, and aligned with the final submitted report. The update should stay within the existing visual language and only adjust the highest-impact slides.

**Approved Scope**

- Keep the overall deck style unchanged.
- Change slide 12 from "Next Steps" framing to "Future Work" framing.
- Keep future directions brief so the slide still signals project completion.
- Fix confirmed overlap and crowding issues on slides 10 and 12.
- Reduce information density on slide 5 without redesigning the whole deck.

**Slide-Level Decisions**

1. Slide 5
   - Compress the four pipeline steps into keyword-led phrasing.
   - Tighten the matrix card copy so it reads faster in a live talk.

2. Slide 10
   - Preserve the GraphEraser explanation page structure.
   - Fix the `Caution` card so the title and body no longer collide.
   - Slightly rebalance nearby elements so the right column has more breathing room.

3. Slide 12
   - Rename the slide to `Limitations And Future Work`.
   - Reduce the structure from `3 limitations + 3 next steps` to `2 limitations + 2 future work`.
   - Keep a short completion/closure stat card so the page reads as a finished project, not an in-progress report.

**Non-Goals**

- No full-deck redesign.
- No changes to the scientific claims or figure assets.
- No attempt to fully rework the result slides unless needed to preserve spacing consistency.

**Verification**

- Add a regression test covering the new slide 12 framing and shortened content markers.
- Rebuild the PPT.
- Export the deck to slide images and visually inspect the edited slides for overlap, truncation, and cramped spacing.
