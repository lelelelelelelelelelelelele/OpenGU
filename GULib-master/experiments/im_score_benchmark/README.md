# Modern IM score benchmark

This package implements the pre-registered modern influence-maximization
selector lane without changing the production AttackManager.

Implemented outputs:

- directed static-IC reverse-reachable sampling;
- RR-SNI, candidate-restricted RR-Shapley, and budget-conditioned
  RR-k-semivalue full score vectors;
- deterministic RR maximum-coverage greedy;
- corrected IMM using an independent final fixed-size RR batch;
- an OPIM-C-shaped anytime dual-sample selector with a conservative
  union-Hoeffding certificate;
- independent common-random spread evaluation against degree;
- public-Planetoid and canonical OpenGU processed-data runners;
- aggregate plus Markdown/HTML result rendering.

Timing rows use a conservative end-to-end interpretation.  Degree includes
degree-score construction; each RR static score includes the shared RR sample
and reducer phases plus top-k materialization.  The artifact also preserves
online and shared-precompute times separately so cross-budget amortization can
be analyzed without hiding score-generation cost.

The legacy Numba-CELF lane performs one registered two-node runtime warmup
before selector timing.  Warmup time is recorded once under shared timings and
again as `excluded_one_time_setup_wall_seconds` on affected rows; it is not
silently charged to whichever legacy method happens to run first.

Important theory boundary:

- corrected IMM is marked as local-validation-only until the implementation
  line is accepted;
- the current OPIM-C certificate is deliberately
  `paper_equivalent=false`. It is a conservative independent-RR bound, not a
  claim that the tight SIGMOD 2018 certificate has been reproduced.

## Local validation

These commands do not read a dataset, open SSH, or run a GU cell:

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_im_score_benchmark.py
E:/conda_package/envs/gnn/python.exe -m experiments.im_score_benchmark.local_smoke
E:/conda_package/envs/gnn/python.exe -m experiments.im_score_benchmark.local_acceptance `
  --json .planning/im_local_acceptance.json `
  --markdown .planning/im_local_acceptance.md `
  --html .planning/im_local_acceptance.html
```

## Runner safety

Both dataset runners are preflight-only unless `--execute` is supplied.
Execution also requires `--approval-token IM-SELECTOR-A`. A formal run adds
`--formal`, which fails unless Git is on a clean `main` checkout.

Preflight examples:

```powershell
E:/conda_package/envs/gnn/python.exe -m experiments.im_score_benchmark.run_planetoid --dataset Cora
E:/conda_package/envs/gnn/python.exe -m experiments.im_score_benchmark.run_arxiv
```

Do not cite a diagnostic run as formal evidence. The full registered matrix
remains disabled in `registered_plan.json` until a later explicit approval.
