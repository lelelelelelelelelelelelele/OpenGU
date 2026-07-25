# Dashboard Todo Wrapping Design

## Goal

Make the four-column Todo board in `self/dashboard/progress.html` remain readable
when `WORKPLAN.md` contains long task descriptions, status details, paths, and
inline code. `WORKPLAN.md` remains the source of truth and `progress.html`
remains generated.

## Root cause

The generator appends the final table column as an inline `.sub` element and
forces it to `white-space: nowrap`. The surrounding flex item retains its
default intrinsic minimum width, while long `code` tokens have no emergency
wrapping rule. In a four-column board these rules either overflow the column or
compress the task text into an unreadably narrow strip.

## Design

- Render each Todo as three semantic regions: checkbox, content, and optional
  GPU badge.
- Inside the content region, keep the task on the primary line and render the
  status/detail field as a separate block below it.
- Allow the content flex item to shrink with `min-width: 0`.
- Apply normal wrapping to status details and emergency wrapping to long task,
  reference, and inline-code tokens.
- Keep the short GPU badge on one line, but do not otherwise change filtering,
  task-state parsing, progress counts, colors, or Markdown ownership.

## Verification

- Add a focused regression test that builds a representative long Todo and
  asserts the generated template contains the required structural classes and
  wrapping contracts.
- Run the focused dashboard test, regenerate `progress.html`, and run the
  generator against the current `WORKPLAN.md`.
- Inspect the generated diff to ensure only the intended template, embedded
  generated snapshot, and timestamp changed.

## Non-goals

- Shortening or rewriting `WORKPLAN.md` tasks.
- Hand-editing `progress.html`.
- Adding JavaScript collapse/expand behavior.
- Redesigning the state-snapshot cards.
