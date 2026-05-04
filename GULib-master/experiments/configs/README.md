# Phase B Experiment Configs

> Created 2026-05-04. Replaces the ad-hoc bash scripts under `scripts/experiments/`.

## How to run

```bash
# From repo root
python experiments/run.py experiments/configs/<config>.yaml
python experiments/run.py experiments/configs/<config>.yaml --force      # re-run even if outputs exist
python experiments/run.py experiments/configs/<config>.yaml --dry_run    # what would run, no execution
python experiments/run.py experiments/configs/<config>.yaml --limit 5    # debug: first 5 cells only
```

## Three-layer artifact decoupling

Every cell in `results/runs/{cell}/{method}_{strategy}/seed{N}/` writes:

| Layer | File | Depends on | Recompute cost |
|---|---|---|---|
| **L1 Selection** | `attack.json` carries `selected_nodes`; canonical store is `results/selection_cache/{hash}.json` | (dataset, model, ratio, **strategy**, seed) — **method-agnostic** | seconds (im/tracin) |
| **L2 Training artifacts** | `predictions.npz` — logits_{before, unlearned, retrained} + labels + masks | (dataset, model, ratio, **method**, **strategy**, seed) | minutes (full train+unlearn+retrain) |
| **L3 Metrics** | `attack.json`, `collateral.json` | L1 + L2 + metric definitions | milliseconds (offline recompute possible) |
| Audit | `_meta.json` | config + git_sha + hostname + timestamp | — |

**Adding a new forward-only metric** (e.g., new MIA variant, new collateral statistic): no re-train needed. Load `predictions.npz`, compute, write a new `metric_<name>.json` next to it.

## Configs

| File | Cell | Cells × Time |
|---|---|---|
| `sanity_one_cell.yaml` | 1×1×1 | ~20s — for verifying environment after refactor |
| `phase_b_cora_gcn.yaml` | 5 method × 6 strategy × 5 seed = 150 cells | ~75 min on a single 4090 |
| `phase_b_cora_gat.yaml` | same matrix on GAT | ~90 min |
| `phase_b_arxiv_feasibility.yaml` | 5 method × random × 1 seed = 5 cells | gate before main matrix |
| `phase_b_arxiv.yaml` | 3 method × 4 strategy × 3 seed = 36 cells | ~25-30 GPU-hours |

## Path scheme

```
results/runs/
  cora_GCN_r0.05/                # cell = (dataset, model, ratio)
    GIF_random/                   # leaf = (method, strategy)
      seed42/
        attack.json               # L3
        collateral.json           # L3
        predictions.npz           # L2
        _meta.json                # audit
      seed212/...
    GIF_im/...
    MEGU_tracin/...
  cora_GAT_r0.05/...
  ogbn-arxiv_GCN_r0.05/...
```

3 levels deep before the leaf folder. Glob patterns:

- All seeds for one (method, strategy): `cora_GCN_r0.05/GIF_random/seed*/attack.json`
- All strategies for one method: `cora_GCN_r0.05/GIF_*/seed42/attack.json`
- All methods for one strategy: `cora_GCN_r0.05/*_random/seed42/attack.json`
- Cross-dataset: `*_GCN_r0.05/GIF_random/seed42/attack.json`
- Cross-model on cora: `cora_*_r0.05/GIF_random/seed42/attack.json`

## Strategy names (post-2026-05-04 cleanup)

`im_v4` and `hybrid_v4` were renamed to `im` and `hybrid` in the registry. The old CELF / coupled-RNG implementations are no longer registered. The v4 algorithm is now canonical.

## Server checklist (fresh env)

1. `git pull` to get latest code (Phase A.1–A.5 fixes + runner)
2. Conda env per `requirements.txt` (PyTorch + PyG 2.6.1 + numba + ogb + pyyaml)
3. `python experiments/run.py experiments/configs/sanity_one_cell.yaml --force` — confirms env
4. `python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml` — gate
5. If gate passes: `python experiments/run.py experiments/configs/phase_b_arxiv.yaml`
6. Cora can run in parallel on a second GPU: `phase_b_cora_gcn.yaml` + `phase_b_cora_gat.yaml`
