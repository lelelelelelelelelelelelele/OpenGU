# ICLR 2027 paper workspace

This directory starts a separate ICLR 2027 draft. The previous manuscript in
`../overleaf/` is preserved unchanged as a reference; its section text has not
been copied into this draft. The `references.bib` file is a copy of the prior
draft's bibliography and should be reviewed as citations are added.

## Template provenance

- Official author guide: <https://iclr.cc/Conferences/2027/AuthorGuidelines>
- Official style package: <https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip>
- Downloaded on 2026-09-23. The original ZIP is retained here; its extracted
  contents are under `official_files/iclr2027/`.
- SHA-256 of the downloaded ZIP:
  `0D940DFA9398AE99A18F24A85A8A683F367204B6AF6D17D2899E60A67102529E`
- The `.sty`, `.bst`, and support files at this directory's root are copies of
  the official files, kept there so `main.tex` uses the standard ICLR paths.

## Draft entry point

Use `main.tex` as the new writing entry point. It keeps ICLR's official style,
anonymous author block, and bibliography style. Red `TODO` markers are prompts,
not paper claims. The mandatory ICLR AI-use statement and recommended
reproducibility statement are included as placeholders; replace them with
accurate content before submission.

The ICLR 2027 author guide currently specifies double-blind submission and a
9-page main-text limit for initial submission (10 pages for rebuttal and
camera-ready). References and appendices are outside the main-text limit.

## Deadline status checked on 2026-09-23

The abstract deadline was September 18, 2026 (AoE), which has passed. The full
paper deadline is September 25, 2026, 11:59 PM AoE. Check the official author
guide for any later updates.

## Current manuscript state

This directory now contains a paragraph-level first draft based on the current
paper-writing outlines and evidence. The abstract is carried verbatim; the
other sections are newly drafted. Upload this directory to Overleaf and use
main.tex as the entry point.

This remains a review draft, not a submission-ready manuscript. The title is
provisional, protocol details remain marked TODO, and results in AAGU-011/012
and the 2026-09-23 AAGU-032/053 analysis have not received scientific
acceptance. Blue notes identify draft status or evidence limits. The required
ICLR AI-use statement and reproducibility statement are placeholders.

The central six-method tables use the report's F1 values and mean plus sample
standard deviation over three training seeds. The random request is reused
across those seeds, so these tables are descriptive rather than estimates over
independent random requests. The separate AAGU-032/053 analysis reports test
accuracy, despite the serialized field name containing f1; it is not combined
with the F1 tables.

The 3000-epoch analysis uses archived outputs. Its report records that all
AAGU-032 method outputs were cache hits and AAGU-053 had both cache hits and
producer executions. The manuscript does not describe the entire matrix as
freshly recomputed. Results distinguish test performance from forgetting
quality and privacy.
