"""Hybrid alpha sweep — reuses cached IF + IM scores across alpha values.

The point of this script: compute (TracIn IF) and (IM initial spread) ONCE for a
given dataset/model/method/seed, then evaluate Hybrid at multiple alpha values
purely through the fusion arithmetic (normalize + alpha-weighted sum + topk).

This is a 100x+ speedup over re-running demo_attack.py per alpha, because the
gradient matrix and MC IM rounds dominate runtime; fusion is microseconds.

Output:
  results/hybrid_alpha_sweep/{dataset}_{model}_{method}_{ratio}_seed{N}.csv
    columns: alpha, jaccard_vs_alpha0.5, top10_overlap_vs_alpha0.5

Example:
  python scripts/sweep_hybrid_alpha.py \\
      --dataset_name cora --base_model SGC --unlearning_methods SGU \\
      --unlearn_ratio 0.05 --alphas 0.1,0.3,0.5,0.7,0.9
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch


def _split_demo_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--alphas", type=str, default="0.1,0.3,0.5,0.7,0.9")
    parser.add_argument("--fusion_method", type=str, default="rank", choices=["rank", "linear"])
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--dataset_name", type=str, default="cora")
    parser.add_argument("--base_model", type=str, default="SGC")
    parser.add_argument("--unlearning_methods", type=str, default="SGU")
    parser.add_argument("--unlearn_ratio", type=float, default=0.05)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--out_dir", type=str, default="./results/hybrid_alpha_sweep")
    own, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining
    return own


_OWN = _split_demo_args()

# Imports must come AFTER sys.argv is sanitized — config.py runs parameter_parser at import.
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402
from attack.attack_strategies.hybrid_strategy import HybridStrategy  # noqa: E402


def main():
    alphas = [float(a) for a in _OWN.alphas.split(",")]
    out_dir = Path(_OWN.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    args = parameter_parser()
    args["seed"] = _OWN.seed
    args["dataset_name"] = _OWN.dataset_name
    args["base_model"] = _OWN.base_model
    args["unlearning_methods"] = _OWN.unlearning_methods
    args["unlearn_ratio"] = _OWN.unlearn_ratio
    args["fusion_method"] = _OWN.fusion_method

    # Build the AttackManager so the pipeline trains its base model and we can
    # snatch (data, model, candidates) for fusion.
    manager = AttackManager(args)
    pipeline = manager.pipeline

    # Reach into the pipeline for the trained pre-unlearn model + data.
    # NOTE: pipelines vary; this uses the AttackPipeline contract.
    data = pipeline.data
    if not hasattr(pipeline, "_get_trained_model"):
        raise RuntimeError(
            "Pipeline does not expose _get_trained_model — alpha sweep requires "
            "the pre-unlearn base model. Update pipeline_adapter.py to expose it."
        )
    model = pipeline._get_trained_model()
    device = next(model.parameters()).device
    data = data.to(device)
    model.eval()

    train_mask = data.train_mask
    candidates = train_mask.nonzero(as_tuple=False).squeeze(-1).to(device)
    n_train = int(train_mask.sum().item())
    if _OWN.k is None:
        k = max(1, int(round(_OWN.unlearn_ratio * n_train)))
    else:
        k = int(_OWN.k)

    print(f"\n[Sweep] Data: {_OWN.dataset_name}/{_OWN.base_model}, "
          f"|V_train|={n_train}, k={k}, alphas={alphas}, fusion={_OWN.fusion_method}\n")

    # Build a single Hybrid instance — its sub-strategies will fill the cache.
    hybrid = HybridStrategy(args)

    # First call populates IF + IM cache. Subsequent calls only re-fuse.
    sweep_rows = []
    selections = {}
    for i, alpha in enumerate(alphas):
        hybrid.alpha = alpha
        t0 = time.time()
        selected = hybrid.select_nodes(data.clone(), model, k)
        elapsed = time.time() - t0
        selections[alpha] = set(selected.tolist())
        print(f"[Sweep] alpha={alpha:.2f}  selected={len(selected)} nodes  time={elapsed:.3f}s")
        sweep_rows.append({"alpha": alpha, "time_s": elapsed, "k": k})

    # Compute Jaccard vs the median alpha (default 0.5 if present, else middle entry).
    ref_alpha = 0.5 if 0.5 in selections else alphas[len(alphas) // 2]
    ref = selections[ref_alpha]
    for row in sweep_rows:
        sel = selections[row["alpha"]]
        inter = len(ref & sel)
        union = len(ref | sel)
        row["jaccard_vs_ref"] = inter / union if union else 1.0
        # Top-k overlap is just |ref ∩ sel| / k (since both have size k)
        row["overlap_count"] = inter
        row["ref_alpha"] = ref_alpha

    out_path = out_dir / (
        f"{_OWN.dataset_name}_{_OWN.base_model}_{_OWN.unlearning_methods}_"
        f"r{_OWN.unlearn_ratio:.2f}_seed{_OWN.seed}_{_OWN.fusion_method}.csv"
    )
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["alpha", "k", "time_s", "ref_alpha", "overlap_count", "jaccard_vs_ref"]
        )
        writer.writeheader()
        writer.writerows(sweep_rows)

    print(f"\n[Sweep] Results -> {out_path}")
    print(f"[Sweep] First-call time amortizes IF+IM compute; later calls should be <0.05s.\n")


if __name__ == "__main__":
    main()
