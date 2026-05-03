# Defense Deck Font Update Design

**Context**

The current 15-minute defense deck is generated from a single PptxGenJS script and still mixes `Georgia` for headings with `Calibri` for body text. For the final academic-defense tone the user wants, that split typography feels less formal than a fully unified serif treatment.

**Design Goal**

Update the generated deck so all slide text uses `Times New Roman`, giving the presentation a more consistent and traditional defense-deck appearance without changing layout, content, or palette.

**Approved Scope**

- Change both heading and body font constants in the PPT generator to `Times New Roman`.
- Keep all copy, slide order, colors, images, and layout structure unchanged.
- Regenerate the `out-test` deck to verify the updated font styling flows through the generated assets.
- Add a regression check so the old `Georgia` and `Calibri` defaults do not quietly return.

**Non-Goals**

- No deck redesign.
- No copy edits.
- No figure replacements.
- No layout retuning unless the font swap causes a visible breakage.

**Verification**

- Add a regression test that expects `Times New Roman` and rejects `Georgia` / `Calibri` in the generator source.
- Rebuild the test output deck from the generator.
- Confirm the expected `.pptx` and companion script are still emitted successfully.
