# Method framework — compact v6

Owner: AAGU-064. Review candidate; v5 is retained unchanged.

- `method-framework-v6.pdf`: compact vector figure.
- `method-framework-v6.drawio`: editable primitives from the same generator.
- `method-framework-v6.png`: preview.
- `method-framework-v5-v6-comparison.pdf`: both versions at a 396 pt width.

The layout uses one horizontal level. Access refers to Section 3.2 instead of
repeating the permission taxonomy; the model/ensemble illustrations are removed.
The same request branches to GU and full retraining. The diagnosis panel follows
the current Section 4.3, with GU gap, Random-relative gap amplification, and the
starting-point/random-response components. Prediction-level diagnostics remain
in the manuscript appendix. Random, Degree and PageRank are named as baselines.

At 396 pt width the figure is 99 pt high, versus 152 pt for v5 (35% less height).
Most labels are 7.2–9.9 pt; the smallest is 6.9 pt. These are geometric sizes,
not claims that the current manuscript already includes the figure.

Run `build_figure.py` with reportlab, pypdf and pypdfium2. It rebuilds PDF, draw.io,
PNG and the comparison. Preserve manual draw.io edits in a separate version.
