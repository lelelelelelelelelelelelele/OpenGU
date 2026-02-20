# Strategy Fixture Format

These fixtures define golden regression cases for attack strategy outputs.

## JSON Schema

Each file under `tests/fixtures/strategies/*.json` uses this shape:

- `name`: Unique case ID.
- `strategy`: One of `random`, `degree`, `pagerank`, `im`, `tracin`, `hybrid`.
- `args`: Strategy args passed to the constructor.
- `seed` (optional): Global RNG seed applied before selection.
- `k` or `ratio`: Selection size.
- `graph`:
  - `num_nodes`
  - `x`
  - `edge_index`
  - `y`
  - `train_mask` (optional)
- `model` (optional for model-dependent strategies):
  - `type` (`linear`)
  - `in_features`
  - `out_features`
  - `weight`
  - `bias`
- `expected_selected_nodes`: Golden selected node IDs.
- `assert_subset_of_train_mask` (optional): If true, selected nodes must be in `train_mask`.

## Maintenance Rules

- Do not auto-refresh fixture expectations in tests.
- Update fixtures only when behavior changes are intentional.
- Every fixture update must append an entry to `tests/fixtures/strategies/CHANGELOG.md`.
