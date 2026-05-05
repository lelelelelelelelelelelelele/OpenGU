"""
Selection-only feasibility test.

Loads dataset + trains base model + times each requested strategy's
`select_nodes` call. Skips unlearning, retrain, and MIA entirely — used to
validate that the selection phase alone is tractable on a large graph
(notably ogbn-arxiv) before committing to a full run.

Reuses the same arg-extraction trick as `demo_attack.py` so config.py's
import-time `parameter_parser()` does not choke on demo-only flags.

Example:
    # arxiv IM + TracIn feasibility (matches phase_b_arxiv defaults)
    python scripts/feasibility_selection_only.py \
        --dataset_name ogbn-arxiv --base_model GCN \
        --unlearn_ratio 0.05 --seed 42 \
        --num_epochs 200 --batch_size 256 \
        --gcn_num_layers 3 --gcn_hidden 256 \
        --candidate_fraction 0.1 --mc_rounds 50 \
        --strategies im,tracin

    # cora sanity (sub-second baseline)
    python scripts/feasibility_selection_only.py \
        --dataset_name cora --base_model GCN --unlearn_ratio 0.05 --seed 42
"""
import argparse
import os
import sys


def _extract_demo_args():
    """Strip script-only flags from sys.argv before parameter_parser sees it."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--strategies", type=str, default="im,tracin")
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--no_cache", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--repeat", type=int, default=1,
                        help="Run each strategy this many times (skipping cache).")
    parser.add_argument("--candidate_subset_size", type=int, default=None,
                        help="If set, restrict the candidate set (train_mask) to "
                             "this many uniformly-sampled nodes for the probe. "
                             "Used to extrapolate time/memory to the full set "
                             "without committing to a full run on a small GPU.")
    # Echo of common parameter_parser args (kept in argv after parse_known_args
    # by re-appending below)
    parser.add_argument("--dataset_name", type=str, default="cora")
    parser.add_argument("--base_model", type=str, default="GCN")
    parser.add_argument("--unlearning_methods", type=str, default="GIF")
    parser.add_argument("--unlearn_ratio", type=float, default=0.05)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=64)

    demo_args, remaining = parser.parse_known_args()

    # The "echoed" args still need to reach parameter_parser, so re-append them.
    # Note: --seed is NOT echoed; parameter_parser only knows --random_seed
    # and we set seed-related fields on args programmatically after parsing.
    echoed = [
        "--dataset_name", str(demo_args.dataset_name),
        "--base_model", str(demo_args.base_model),
        "--unlearning_methods", str(demo_args.unlearning_methods),
        "--unlearn_ratio", str(demo_args.unlearn_ratio),
        "--cuda", str(demo_args.cuda),
        "--num_epochs", str(demo_args.num_epochs),
        "--batch_size", str(demo_args.batch_size),
    ]
    sys.argv = [sys.argv[0]] + remaining + echoed
    return demo_args


_demo_args = _extract_demo_args()

import time
import torch

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402


def _seed_everything(seed: int):
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)


def _peak_mem_mb(device: torch.device) -> float:
    if device.type == "cuda":
        return torch.cuda.max_memory_allocated(device) / (1024 ** 2)
    return -1.0


def main():
    print("=" * 70)
    print("Selection-only feasibility test")
    print("=" * 70)

    args = parameter_parser()
    args["dataset_name"] = _demo_args.dataset_name
    args["base_model"] = _demo_args.base_model
    args["unlearning_methods"] = _demo_args.unlearning_methods
    args["unlearn_ratio"] = _demo_args.unlearn_ratio
    args["num_epochs"] = _demo_args.num_epochs
    args["batch_size"] = _demo_args.batch_size
    args["random_seed"] = _demo_args.seed
    args["seed"] = _demo_args.seed
    args["cuda"] = _demo_args.cuda

    _seed_everything(_demo_args.seed)

    if args.get("cuda", 0) >= 0 and torch.cuda.is_available():
        torch.cuda.set_device(args["cuda"])

    strategies = [s.strip() for s in _demo_args.strategies.split(",") if s.strip()]
    print(f"\nDataset: {args['dataset_name']}  Model: {args['base_model']}  "
          f"Seed: {args['seed']}  Strategies: {strategies}")

    # AttackManager init: loads data + trains base model. The trained model
    # is what model-coupled strategies (tracin, hybrid) consume.
    print("\n[init] Building AttackManager (loads data, trains base model)...")
    t_init0 = time.perf_counter()
    manager = AttackManager(args, use_cache=not _demo_args.no_cache)
    t_init1 = time.perf_counter()

    data = manager.data
    model = manager.model
    device = manager.device

    print(f"[init] num_nodes={data.num_nodes}  num_edges={data.edge_index.size(1)}  "
          f"train_size={int(data.train_mask.sum().item()) if hasattr(data, 'train_mask') else 'N/A'}  "
          f"init_time={t_init1 - t_init0:.1f}s  device={device}")

    if _demo_args.k is not None:
        k = _demo_args.k
    else:
        k = int(data.num_nodes * args["unlearn_ratio"])
    print(f"[init] k={k}  ({args['unlearn_ratio'] * 100:.1f}% of num_nodes)")

    # Probe-mode: shrink train_mask uniformly to make a cheap measurement
    # whose time and tracin-G-matrix memory scale linearly in N. This lets
    # us size the GPU before committing to a full ~75 min, ~40 GB run.
    full_train_size = int(data.train_mask.sum().item()) if hasattr(data, "train_mask") else data.num_nodes
    probe_size = _demo_args.candidate_subset_size
    probe_active = probe_size is not None and probe_size < full_train_size
    if probe_active:
        full_mask = data.train_mask.clone()
        train_idx = full_mask.nonzero(as_tuple=False).squeeze(-1)
        rng = torch.Generator(device="cpu").manual_seed(_demo_args.seed)
        perm = torch.randperm(train_idx.shape[0], generator=rng)[:probe_size]
        small_mask = torch.zeros_like(full_mask)
        small_mask[train_idx[perm].to(full_mask.device)] = True
        data.train_mask = small_mask
        # k must not exceed candidate set size; pin to a smaller k for the probe
        probe_k = max(1, min(k, probe_size // 2))
        print(f"[probe] candidate_subset_size={probe_size} (full train={full_train_size}, "
              f"ratio={probe_size/full_train_size:.4f}); probe_k={probe_k} (vs full k={k})")
    else:
        full_mask = None
        probe_k = k

    available = manager.list_strategies()
    invalid = [s for s in strategies if s not in available]
    if invalid:
        print(f"\n[warn] Unknown strategies dropped: {invalid}  (available={available})")
        strategies = [s for s in strategies if s in available]

    print("\n" + "-" * 70)
    print(f"{'strategy':<10} {'run':<5} {'time(s)':<10} {'peak_mem(MB)':<14} top-5 selected")
    print("-" * 70)

    measurements = {}  # strategy -> (time_s, peak_mb)
    for name in strategies:
        strat = manager._strategies[name]
        for r in range(_demo_args.repeat):
            if device.type == "cuda":
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats(device)
                torch.cuda.synchronize(device)
            t0 = time.perf_counter()
            selected = strat.select_nodes(data, model, probe_k)
            if device.type == "cuda":
                torch.cuda.synchronize(device)
            t1 = time.perf_counter()
            top5 = selected[:5].tolist() if hasattr(selected, "tolist") else list(selected[:5])
            mem = _peak_mem_mb(device)
            print(f"{name:<10} {r:<5} {t1 - t0:<10.2f} {mem:<14.1f} {top5}")
            measurements[name] = (t1 - t0, mem)

    if probe_active:
        # Restore full train_mask in case caller chains further work on `data`.
        data.train_mask = full_mask
        scale = full_train_size / probe_size
        print("\n" + "-" * 70)
        print(f"[extrapolation]  probe -> full (x{scale:.1f})")
        print(f"  assumption: tracin time + G-matrix memory scale linearly in N;")
        print(f"              IM time scales sub-linearly (CELF reuses spread)")
        print("-" * 70)
        print(f"{'strategy':<10} {'time_full':<14} {'mem_full(GB)':<14} {'fits 24GB?':<10}")
        print("-" * 70)
        for name, (t, m) in measurements.items():
            if name == "tracin":
                t_full = t * scale
                m_full_gb = (m * scale) / 1024.0
                fits = "OK" if m_full_gb < 22.0 else "OOM"
                print(f"{name:<10} {t_full:>8.0f}s ({t_full/60:.1f}m)  {m_full_gb:<14.1f} {fits:<10}")
            elif name == "im":
                # IM is CPU-bound; arxiv full-run with current params (cand_frac=0.1,
                # mc_rounds=50) is roughly time_subset × scale^0.5 (CELF lazy heap)
                t_full = t * (scale ** 0.5)
                print(f"{name:<10} {t_full:>8.0f}s ({t_full/60:.1f}m)  ~CPU only    n/a")
            else:
                print(f"{name:<10} {t * scale:>8.0f}s ({t * scale / 60:.1f}m)  ?            ?")

    print("\n[done] Selection-only feasibility test complete.")


if __name__ == "__main__":
    main()
