# Metrics-Led Results Restructure Design

**Context**

The main report defines the central utility metric correctly:

- `relative_f1_drop = F1_random_unlearn - F1_attack_unlearn`

and explains why it is needed: direct post-unlearning utility change can be misleading, especially for shard-based methods such as GraphEraser, where deletion may improve the downstream score and produce a negative raw drop. The current defense deck does not preserve that definition cleanly. Instead, the PPT script discusses `relative F1 drop` informally, lacks a dedicated metrics overview page, and introduces collateral damage only after the audience has already been asked to interpret family-level results.

**Design Goal**

Restructure the middle of the defense deck so the audience learns the metrics framework before seeing the results, while preserving a concise final-defense pace and keeping the deck size stable.

**Approved Scope**

- Correct the `relative_f1_drop` explanation in the PPT source and speaker script.
- Add a dedicated `Metrics Framework` slide before the main results.
- Keep the total deck size stable by replacing the current `What Was Built In OpenGU` slide in the timed flow.
- Reorder the results arc so the audience sees:
  1. metrics definitions,
  2. family-level spectrum,
  3. ratio sensitivity / ablation,
  4. attribution and collateral damage,
  5. GraphEraser / shard protection interpretation,
  6. efficiency / practicality.
- Preserve the existing figure assets unless a different local figure is needed to support the approved narrative.

**Chosen Storyline**

1. **Pipeline and matrix** still introduces the experiment setup.
2. **Metrics Framework** defines `relative_f1_drop`, `retrain_gap`, and collateral metrics together.
3. **Main Finding** now explicitly says the spectrum is read through `relative_f1_drop`, because it measures attack-over-random and remains interpretable when shard-based methods have negative raw drops.
4. **Ratio Sensitivity** keeps the current scaling figure as the main ablation-style support page.
5. **Attribution And Collateral Damage** clarifies `drop_retrain + retrain_gap` and explains how `fraction_flipped` / `mean_pred_shift` diagnose spillover.
6. **GraphEraser** becomes the page that explains the shard-protection interpretation after the audience already understands why raw utility alone is insufficient.
7. **Attack Practicality** closes the results section with efficiency rather than introducing the main metric definition late.

**Slide-Level Decisions**

1. Replace current slide 6 (`What Was Built In OpenGU`) with `Metrics Framework`.
2. Keep current slide 7 as the family-spectrum figure page, but revise the copy so GraphEraser is explicitly introduced as a shard-protection case rather than merely “behaves differently.”
3. Keep current slide 8 as the ratio-sensitivity / ablation page and make the ratio role explicit in the talk track.
4. Retain current slide 9 as the attribution page, but expand the on-slide logic so `relative_f1_drop`, `drop_retrain`, `retrain_gap`, and collateral metrics read as one framework.
5. Retain current slide 10 as the GraphEraser evidence page and align its copy with the “shard protection effect” framing already used in the report.
6. Keep current slide 11 as the efficiency page, but remove any wording that incorrectly substitutes a vague explanation for the formal metric definition.

**Non-Goals**

- No new experiments.
- No new figure generation unless a missing figure is required to support the approved storyline.
- No global deck redesign.
- No change to the thesis-level claims already aligned with the main report.

**Verification**

- Add regression tests that expect the corrected `relative_f1_drop` formula and the new `Metrics Framework` slide content in both the source script and generator.
- Rebuild the `out-test` deck and companion speech script.
- Export and inspect the revised results block visually, especially slides 6–11, to ensure the new metrics slide and updated text still fit cleanly.
