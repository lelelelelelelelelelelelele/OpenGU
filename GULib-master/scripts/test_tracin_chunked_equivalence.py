"""
Numerical equivalence test for the TracIn dense vs chunked paths.

Forces TracIn to run twice on the same (data, model, candidates):
  - dense   path: tracin_chunk_threshold_gb = 1e9   (always dense)
  - chunked path: tracin_chunk_threshold_gb = 0.0   (always chunked, chunk=50)

Asserts:
  - top-k selected node sets are bit-identical (this is what the attack uses)
  - score correlation > 0.9999
  - max abs diff is small (~1e-4 for fp32)

Runs on cora by default (~135 train nodes, both paths complete in seconds).
The chunk_size of 50 forces multiple chunks, exercising the streaming logic.

Usage:
    H:/conda_package/envs/gnn/python.exe scripts/test_tracin_chunked_equivalence.py
    H:/conda_package/envs/gnn/python.exe scripts/test_tracin_chunked_equivalence.py \
        --dataset_name citeseer --base_model GCN
"""
import argparse
import os
import sys


def _extract_demo_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--chunk_size", type=int, default=50,
                        help="Force chunk size for the chunked path (small to "
                             "exercise multi-chunk streaming on tiny graphs).")
    parser.add_argument("--rtol", type=float, default=1e-4)
    parser.add_argument("--atol", type=float, default=1e-5)
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

import time
import numpy as np
import torch

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402
from attack.attack_strategies.tracin_strategy import TracInStrategy  # noqa: E402


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


def main() -> int:
    print("=" * 72)
    print("TracIn dense vs chunked equivalence test")
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
    args["enable_score_cache"] = False  # never touch real cache

    _seed_everything(_demo_args.seed)

    if args.get("cuda", 0) >= 0 and torch.cuda.is_available():
        torch.cuda.set_device(args["cuda"])

    print(f"\nDataset: {args['dataset_name']}  Model: {args['base_model']}  Seed: {args['seed']}")

    # Build manager + train base model exactly the way an attack run would.
    manager = AttackManager(args, use_cache=False)
    manager.pipeline._ensure_base_model_trained()
    data = manager.data
    model = manager.pipeline.model
    device = manager.device

    # Build candidate set the same way TracInStrategy.select_nodes does.
    if hasattr(data, "train_mask") and data.train_mask is not None:
        candidates = data.train_mask.nonzero(as_tuple=False).squeeze(-1).to(device)
    else:
        candidates = torch.arange(data.num_nodes, device=device)

    n_cand = candidates.shape[0]
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nn_cand = {n_cand}  num_params = {num_params}  "
          f"theoretical G size = {n_cand*num_params*4/1e6:.1f} MB")

    # Force dense
    args_dense = dict(args)
    args_dense["tracin_chunk_threshold_gb"] = 1e9
    args_dense["enable_score_cache"] = False
    strat_dense = TracInStrategy(args_dense)

    t0 = time.perf_counter()
    scores_dense = strat_dense.compute_scores(model, data, candidates).detach().cpu()
    t_dense = time.perf_counter() - t0

    # Force chunked
    args_chunked = dict(args)
    args_chunked["tracin_chunk_threshold_gb"] = 0.0
    args_chunked["tracin_chunk_size"] = _demo_args.chunk_size
    args_chunked["enable_score_cache"] = False
    strat_chunked = TracInStrategy(args_chunked)

    t0 = time.perf_counter()
    scores_chunked = strat_chunked.compute_scores(model, data, candidates).detach().cpu()
    t_chunked = time.perf_counter() - t0

    # Diagnostics
    diff = (scores_dense - scores_chunked).abs()
    max_abs = float(diff.max().item())
    mean_abs = float(diff.mean().item())
    rel = (diff / (scores_dense.abs() + 1e-12)).max().item()
    sd = scores_dense.numpy().astype(np.float64)
    sc = scores_chunked.numpy().astype(np.float64)
    if sd.std() == 0 or sc.std() == 0:
        corr = float("nan")
    else:
        corr = float(np.corrcoef(sd, sc)[0, 1])

    print("\n" + "-" * 72)
    print(f"dense path     : {t_dense:.2f}s  scores[:3] = {scores_dense[:3].tolist()}")
    print(f"chunked path   : {t_chunked:.2f}s  scores[:3] = {scores_chunked[:3].tolist()}")
    print(f"max abs diff   : {max_abs:.3e}")
    print(f"mean abs diff  : {mean_abs:.3e}")
    print(f"max rel diff   : {rel:.3e}")
    print(f"correlation    : {corr:.10f}")
    print("-" * 72)

    # Top-k assertion: this is what the attack actually selects on.
    k = max(1, int(args["unlearn_ratio"] * n_cand))
    top_dense = set(candidates[scores_dense.to(device).topk(k).indices].cpu().tolist())
    top_chunked = set(candidates[scores_chunked.to(device).topk(k).indices].cpu().tolist())
    sym_diff = top_dense ^ top_chunked

    print(f"top-{k} dense   = {sorted(list(top_dense))[:10]}{'...' if k>10 else ''}")
    print(f"top-{k} chunked = {sorted(list(top_chunked))[:10]}{'...' if k>10 else ''}")
    print(f"symmetric diff = {sorted(list(sym_diff))}")

    failures = []
    if not torch.allclose(scores_dense, scores_chunked,
                          rtol=_demo_args.rtol, atol=_demo_args.atol):
        failures.append(f"scores not allclose (rtol={_demo_args.rtol}, atol={_demo_args.atol})")
    if corr < 0.9999:
        failures.append(f"correlation {corr:.6f} < 0.9999")
    if top_dense != top_chunked:
        failures.append(f"top-{k} mismatch: |sym_diff|={len(sym_diff)}")

    print("\n" + "=" * 72)
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS — dense and chunked paths produce equivalent results")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
