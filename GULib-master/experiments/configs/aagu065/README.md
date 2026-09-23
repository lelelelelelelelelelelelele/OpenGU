# AAGU-065 Cora fixed-PT calibration

AAGU-065 owns one-point Observer calibration for Cora H16 and H64. The active
parameter path is generated from the exact `(Cora, hidden)` checkpoint; the
old author/shifted values and prior H16 R2 files remain historical inputs and
are not active candidate tables.

## Calibration sequence

1. `theory_h16.yaml` or `theory_h64.yaml` identifies the persisted Cora split,
   model, training identity and exact checkpoint. Run
   `experiments/aagu062_theory.py` only after the matching checkpoint is present
   in the SSH active checkout. This calculates the GIF and IDEA loss Hessian
   Ritz range and derives the registered `rho=0.8` and `rho=0.5` proposals.
   Finite Lanczos estimates are not full-spectrum certificates.
2. `experiments/aagu062_generate_candidates.py` consumes that theory JSON and
   creates method YAMLs at T=100/200/400 plus one ordinary `run.py` Observer
   table. The table uses Random seed 104245, a 10% train-mask deletion request,
   and disables GIF/IDEA GU output cache reads and writes.
3. After the Observer run is collected and its run.json SHA-256 is verified,
   `experiments/analyze_observer_calibration.py` checks all Observer artifacts and applies
   the Work Plan's frozen gate. It never changes YAML or chooses by F1.
4. Only a `stable` method result with complete coverage of both theoretical
   proposals and T=100/200/400 may freeze the smallest passing `mu=scale*damp`.
   Multi-selector/seed validation YAMLs are created afterward and use the
   frozen parameters for this exact checkpoint condition only.

The gate requires finite HVP probe/RHS/repeat relative errors <=1e-5, finite
updates and shifted residual <=1e-3 at all three budgets, update-norm variation
from T=100 <=1e-3, and at T=100 update/RHS ratio >1e-6 plus original-graph
same-graph logits max-abs change >1e-8. The original-system residual is reported
separately. F1 is not a parameter-selection criterion.

The existing `observer_h16.yaml` and its accepted run concern the old R2 pair;
they do not validate the new theory-derived candidate pairs. `observer_h64_calibration.yaml`
is the single active H64 aggregate. A duplicate H64 draft table is not used.

## Remaining checkpoint cases

AAGU-067 and AAGU-068 use their own CiteSeer/PubMed H16/H64 checkpoint in
exactly the same sequence. Their `theory_h16.yaml` and `theory_h64.yaml` files
are inputs only and contain no scale/damp values. As of the latest SSH check,
the registered CiteSeer/PubMed seed42 checkpoints are absent from the active
checkout. Keep their paired-PT recipes as preparation; do not create or run
candidate tables until the corresponding checkpoint is present and verified.

The six conditions remain independent: Cora, CiteSeer, and PubMed each have
separate H16 and H64 theory results, candidate tables, Observer analyses and
frozen parameters. No cross-dataset or cross-width parameter transfer is valid.
