# results/score_cache/ — npz-backed score caches

> Created: 2026-05-07
> Maintained by: `attack/score_cache.py` (the `ScoreCache` class)
> Upper rules: `self/dashboard/CLAUDE.md`

## Purpose

Caches **per-candidate score arrays** that are expensive to compute and reusable
across cells. Three namespaces today:

| Namespace | Producer | Cache key (what's shared across) | Cache value |
|---|---|---|---|
| `if/` | `tracin_strategy.py::compute_scores` | dataset + base_model + ratio + GU seed + loss_type + **method** + graph_fingerprint | TracIn scores for each candidate node |
| `im/` | `im_strategy.py::compute_initial_marginal_gains` | propagation_prob + mc_rounds + candidate_fraction + im_selector_seed + graph_fingerprint | Single-node spread σ({v}) for each candidate |
| `im_celf/` | `im_strategy.py::compute_im_celf` | propagation_prob + mc_rounds + candidate_fraction + im_selector_seed + im_batch_size + k + graph_fingerprint | (selected_nodes, marginal_gains) for full CELF run |

## File layout

```
results/score_cache/
├── if/
│   ├── <key>.npz       # candidates: int64[M], scores: float32[M]
│   └── <key>.json      # sidecar config for debugging
├── im/
│   └── ...
└── im_celf/
    └── ...
```

`<key>` is the first 32 hex chars of SHA-256 over the cache config dict.

## Cross-cell sharing rules (key design property)

| Cache | Shared across method? | Shared across GU seed? | Shared across k? |
|---|---|---|---|
| `if/` | ❌ (key includes `unlearning_methods`) | ❌ (key includes `seed`) | ✅ (no k in key) |
| `im/` | ✅ | ✅ (key uses `im_selector_seed`, default 2024 fixed) | ✅ |
| **`im_celf/`** | **✅** | **✅** (same fixed `im_selector_seed`) | ❌ (k in key — different k = different selection) |

**Practical impact for B.2 arxiv**: one IM CELF run on (arxiv, default
hyperparams, k=6773) covers **all 6 methods × 3 GU seeds × IM strategy** =
**18 cells**. Run once, hit cache 17 times. See
`self/dashboard/EXPERIMENT_DASHBOARD.md §3` for the recorded fact.

**Why TracIn (`if/`) is per-method/per-seed**: empirically, training the base
GNN under different (method-specific arg dicts, seeds) produces different
weight tensors, and TracIn scores depend on the trained weights. IM by contrast
is pure topology + IM hyperparams.

## Safety rules

- **Never rename files** — names ARE the cache key
- **Whole directory is safely deletable** — caches rebuild on next run
- **Don't hand-edit npz** — corruption silently produces wrong selections

## When to clear `im_celf/`

- Changed CELF algorithm (e.g. switched batch-CELF for plain CELF) → old entries invalid
- Changed `_simulate_spread_numba` semantics → old entries invalid
- Changed graph topology (data preprocessing, candidate set definition) → graph_fingerprint mismatches automatically; safe to leave
- Changed only IM hyperparams (prob, mc, fraction, batch_size) → key differs automatically; safe to leave

## When NOT to clear

- Changed unlearning method → IM cache is method-agnostic by design
- Changed GU training seed → cache decoupled via `im_selector_seed`
- Added a new method to the matrix → cache covers it
- Refactored TracIn (`if/` cache) → `im_celf/` unaffected

## CPU-only IM workflow (post-fix/im-celf-shared-cache)

The full-CELF `im_celf/` cache enables a 2-machine workflow that saves
GPU rental cost:

```bash
# Machine A (cheap CPU instance, 32+ cores):
#   IM is pure CPU (no GPU operations in select_nodes path),
#   numba prange parallelises MC rounds across cores.
python scripts/prewarm_selection_cache.py \
    experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    --strategies im
# → writes results/score_cache/im_celf/<key>.npz

tar czf im_celf_cache.tar.gz results/score_cache/im_celf/

# Transfer to Machine B (GPU instance):
scp im_celf_cache.tar.gz <gpu-host>:/path/to/repo/

# On Machine B:
tar xzf im_celf_cache.tar.gz
python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml
# → all (method × IM strategy) cells hit cache: [ScoreCache] HIT im_celf
```

Time/cost on autodl (estimated, 2026-05-07):
- CPU 32-core instance @ ~¥0.5-1/h × ~10 min = ~¥0.1 for IM
- GPU instance @ ~¥4-5/h × 0 min for IM = ¥0 (cache hit)
- vs. running IM on GPU instance directly: ~¥10-20 per run × N_methods
