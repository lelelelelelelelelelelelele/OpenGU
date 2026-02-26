# Post-Mortem: GNNDelete Assertion Failure & Evaluation Corruption

## 1. Executive Summary
During the generalization experiments (MG-1, MG-2), a critical logic error was identified in the `GNNDelete` implementation. This error caused all unlearning tasks to fail silently and return a constant baseline F1 (random guess level), leading to misleadingly high "Attack Success" metrics.

## 2. Incident Timeline
- **Discovery**: 2026-02-26. Observed `f1_after` consistently at **0.1877** for Citeseer across all 6 strategies.
- **Diagnosis**: Audit of `gnndelete.py` revealed an `AssertionError` triggered by a hardcoded `df_size` calculation that mismatched the injected attack nodes.
- **Containment**: Fallback mechanism within the training pipeline swallowed the error, returning original model weights.
- **Resolution**: Fixed `gnndelete.py` to use dynamic node counting. Re-ran Baseline K=5 and relative evaluations.

## 3. Failure Signatures (How we located it)
Any result set matching these criteria was flagged as corrupted:
1.  **Strategy Invariance**: `f1_after(Random) == f1_after(IM) == f1_after(Hybrid)`.
2.  **Dataset-specific Constants**: F1 values clustering around random-guess baselines (e.g., ~0.18 for Citeseer).
3.  **Zero Training Signal**: $|f1\_after - f1\_before| < 1e-7$ in individual caches.

## 4. Current Verification Status
A full-repository audit (1375 files) was conducted on 2026-02-27:
- **Identical F1 Groups**: 0 (All cleared)
- **Zero Delta Entries**: 0 (All cleared)
- **GNNDelete MG-1/2**: Re-evaluated and confirmed to have varied F1 values (e.g., 0.16 to 0.24 variation per strategy).

## 5. Prevention & Future Actions
- **Bug Fix**: `df_size = len(df_nodes)` implemented in `delete_node` and `delete_edge`.
- **Validation**: Added `scripts/evaluation/full_results_audit.py` to the regular CI/CD pipeline to detect silient failures.
- **Data Integrity**: `final_paper_stats.csv` now exclusively contains post-fix verified data.
