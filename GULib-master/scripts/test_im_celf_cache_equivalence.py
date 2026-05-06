"""
Equivalence + caching tests for the IM CELF refactor (fix/im-celf-shared-cache).

Verifies four properties on cora:
  1. parallel-MC numba kernel produces the same selected nodes as serial.
  2. Cache MISS → compute → SAVE writes a valid npz to results/score_cache/im_celf/.
  3. Cache HIT path returns the same selected nodes + scores as the MISS path.
  4. Cache key is method-agnostic and GU-seed-agnostic: changing
     `unlearning_methods` or the GU `seed` arg between runs still hits
     the same cache entry.

Runs on cora (~135 train nodes), small enough that both parallel and
serial paths complete in seconds.

Usage:
    H:/conda_package/envs/gnn/python.exe scripts/test_im_celf_cache_equivalence.py
"""
import argparse
import os
import shutil
import sys
import tempfile


def _extract_demo_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--k", type=int, default=20)
    parser.add_argument("--keep_cache_dir", action="store_true",
                        help="If set, do NOT delete the temp cache dir on exit "
                             "(useful for inspecting the npz files).")
    # Echoed to parameter_parser
    parser.add_argument("--dataset_name", type=str, default="cora")
    parser.add_argument("--base_model", type=str, default="GCN")
    parser.add_argument("--unlearning_methods", type=str, default="GIF")
    parser.add_argument("--unlearn_ratio", type=float, default=0.05)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=64)

    demo_args, remaining = parser.parse_known_args()
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

import numpy as np
import torch

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402
from attack.attack_strategies.im_strategy import IMStrategy  # noqa: E402


def _seed_everything(seed: int):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)


def _build_strategy(args, parallel_mc, enable_cache, cache_dir, override=None):
    a = dict(args)
    a["im_parallel_mc"] = parallel_mc
    a["enable_score_cache"] = enable_cache
    a["score_cache_dir"] = cache_dir
    if override:
        a.update(override)
    return IMStrategy(a)


def _list_celf_cache(cache_dir):
    p = os.path.join(cache_dir, "im_celf")
    if not os.path.isdir(p):
        return []
    return sorted([f for f in os.listdir(p) if f.endswith(".npz")])


def main() -> int:
    print("=" * 72)
    print("IM CELF refactor: parallel-MC + shared cache equivalence test")
    print("=" * 72)

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
    # IM hyperparams (small enough to run fast on cora)
    args["propagation_prob"] = 0.1
    args["mc_rounds"] = 30
    args["candidate_fraction"] = 1.0
    args["im_batch_size"] = 5

    _seed_everything(_demo_args.seed)

    # Build manager just to load data (IM doesn't need a trained model).
    print("\n[init] Loading dataset (cora)...")
    manager = AttackManager(args, use_cache=False)
    data = manager.data
    edge_index = data.edge_index
    num_nodes = data.num_nodes

    if hasattr(data, "train_mask") and data.train_mask is not None:
        candidate_set = data.train_mask.nonzero(as_tuple=False).squeeze(-1).tolist()
    else:
        candidate_set = list(range(num_nodes))

    k = _demo_args.k
    print(f"[init] num_nodes={num_nodes}, num_edges={edge_index.size(1)}, "
          f"|candidate_set|={len(candidate_set)}, k={k}")

    # Use a temp cache dir so we don't pollute or shadow the real cache.
    tmp_cache = tempfile.mkdtemp(prefix="im_celf_test_")
    print(f"[init] using temp cache dir: {tmp_cache}")

    failures = []

    try:
        # ---- Test 1: parallel MC vs serial MC produce same selection ----
        print("\n[Test 1] parallel-MC vs serial-MC numba kernels")
        strat_serial = _build_strategy(args, parallel_mc=False,
                                       enable_cache=False, cache_dir=tmp_cache)
        strat_parallel = _build_strategy(args, parallel_mc=True,
                                         enable_cache=False, cache_dir=tmp_cache)

        sel_s, sc_s = strat_serial.compute_im_celf(edge_index, num_nodes, k, list(candidate_set))
        sel_p, sc_p = strat_parallel.compute_im_celf(edge_index, num_nodes, k, list(candidate_set))

        sel_s_t = torch.tensor(sel_s)
        sel_p_t = torch.tensor(sel_p)
        max_score_diff = float((sc_s - sc_p).abs().max().item())
        same_set = set(sel_s) == set(sel_p)
        same_order = sel_s == sel_p

        print(f"  serial   top-5: {sel_s[:5]}  scores[:3]={sc_s[:3].tolist()}")
        print(f"  parallel top-5: {sel_p[:5]}  scores[:3]={sc_p[:3].tolist()}")
        print(f"  set-equal:    {same_set}")
        print(f"  order-equal:  {same_order}")
        print(f"  max score diff: {max_score_diff:.3e}")

        if not same_set:
            failures.append(f"Test 1: parallel vs serial selected DIFFERENT node sets "
                            f"(sym diff size={len(set(sel_s) ^ set(sel_p))})")
        if max_score_diff > 1e-6:
            failures.append(f"Test 1: max score diff {max_score_diff:.3e} > 1e-6")

        # ---- Test 2: cache MISS path writes npz ----
        print("\n[Test 2] cache MISS path writes npz to im_celf/")
        strat_cache = _build_strategy(args, parallel_mc=True,
                                      enable_cache=True, cache_dir=tmp_cache)
        sel_first, sc_first = strat_cache.compute_im_celf(edge_index, num_nodes, k, list(candidate_set))

        cache_files = _list_celf_cache(tmp_cache)
        print(f"  cache files after MISS run: {cache_files}")
        if not cache_files:
            failures.append("Test 2: no npz file written to im_celf/ after first run")

        # ---- Test 3: cache HIT path returns same result ----
        print("\n[Test 3] cache HIT returns same selection + scores")
        strat_hit = _build_strategy(args, parallel_mc=True,
                                    enable_cache=True, cache_dir=tmp_cache)
        sel_hit, sc_hit = strat_hit.compute_im_celf(edge_index, num_nodes, k, list(candidate_set))

        hit_set_eq = set(sel_first) == set(sel_hit)
        hit_order_eq = sel_first == sel_hit
        hit_score_diff = float((sc_first - sc_hit).abs().max().item())
        print(f"  set-equal:    {hit_set_eq}")
        print(f"  order-equal:  {hit_order_eq}")
        print(f"  max score diff: {hit_score_diff:.3e}")

        if not hit_set_eq:
            failures.append("Test 3: cache HIT returned different selection")
        if not hit_order_eq:
            failures.append("Test 3: cache HIT returned different order")
        if hit_score_diff > 0.0:
            failures.append(f"Test 3: cache HIT scores differ by {hit_score_diff:.3e}")

        # ---- Test 4: cache HIT across method change + GU seed change ----
        print("\n[Test 4] cache key is method-agnostic AND GU-seed-agnostic")
        # Change unlearning_methods + seed; cache should still HIT.
        strat_x = _build_strategy(args, parallel_mc=True,
                                  enable_cache=True, cache_dir=tmp_cache,
                                  override={"unlearning_methods": "GNNDelete",
                                            "seed": 9999,
                                            "random_seed": 9999})
        sel_x, sc_x = strat_x.compute_im_celf(edge_index, num_nodes, k, list(candidate_set))

        files_after_x = _list_celf_cache(tmp_cache)
        x_set_eq = set(sel_first) == set(sel_x)
        x_order_eq = sel_first == sel_x
        x_score_diff = float((sc_first - sc_x).abs().max().item())
        new_files = set(files_after_x) - set(cache_files)
        print(f"  cache files after method+seed change: {files_after_x}")
        print(f"  newly written:    {sorted(new_files) if new_files else '(none — HIT!)'}")
        print(f"  set-equal:        {x_set_eq}")
        print(f"  order-equal:      {x_order_eq}")
        print(f"  max score diff:   {x_score_diff:.3e}")

        if new_files:
            failures.append(f"Test 4: changing unlearning_methods/seed wrote new "
                            f"cache file {sorted(new_files)} — cache key is NOT "
                            f"method/seed-agnostic (regression)")
        if not x_set_eq:
            failures.append("Test 4: selection differs after method/seed change")
        if x_score_diff > 0.0:
            failures.append(f"Test 4: scores differ after method/seed change by {x_score_diff:.3e}")

    finally:
        if not _demo_args.keep_cache_dir:
            shutil.rmtree(tmp_cache, ignore_errors=True)

    print("\n" + "=" * 72)
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS — IM CELF cache + parallel MC equivalent across (method, seed)")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
