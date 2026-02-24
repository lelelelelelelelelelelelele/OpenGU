# Fixture Changelog

## 2026-02-24

- Fixed `im_basic_k3` expected nodes from `[1, 3, 7]` to `[12, 9, 1]`: original values were incorrectly generated from the buggy numba path; correct Python-path baseline has always been `[12, 9, 1]`.

## 2026-02-21

- Added initial golden fixtures for `random`, `degree`, `pagerank`, `im`, `tracin`, and `hybrid`.
- Added dedicated `tracin` cases for:
  - non-contiguous `train_mask` candidate mapping
  - no-`train_mask` baseline behavior
