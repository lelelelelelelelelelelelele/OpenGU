"""
Training-free topology-selector runner for the selection-concordance study.

Builds AttackPipeline ONLY to obtain the processed Data object (load_data +
process_data); AttackPipeline.__init__ instantiates a *random-init* model and
does NOT train (training happens later in run_exp, which we never call). We
then call select_nodes(data, model=None, k) on the pure-topology strategies
(degree / pagerank / im / random), which ignore the model entirely.

Outputs one JSON per (dataset, base_model, ratio, seed):
    self/related_work/concordance/data/{dataset}_{model}_r{ratio}_seed{seed}.json

NO TRAINING. CPU-only (CUDA_VISIBLE_DEVICES='' set before torch import) to avoid
the dead local sm_120 GPU. Does not touch results/ caches; writes only under
self/related_work/concordance/data/.

Usage:
    python self/related_work/concordance/run_topology_selectors.py \
        --dataset_name citeseer --base_model GCN --unlearn_ratio 0.05 \
        --seed 2024 --strategies degree,pagerank,im,random
"""
import os
# Force CPU BEFORE any torch import (local GPU is sm_120/incompatible).
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import sys
import json
import time
import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_local():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--dataset_name", default="cora")
    p.add_argument("--base_model", default="GCN")
    p.add_argument("--unlearning_methods", default="GIF")
    p.add_argument("--unlearn_ratio", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=2024)
    p.add_argument("--strategies", default="degree,pagerank,im,random")
    a, _ = p.parse_known_args()
    return a


LOCAL = parse_local()

# Sanitize sys.argv BEFORE importing anything that triggers config.py's
# import-time parameter_parser() call (mirrors demo_attack.py's pattern).
sys.argv = [
    sys.argv[0],
    "--dataset_name", LOCAL.dataset_name,
    "--base_model", LOCAL.base_model,
    "--unlearning_methods", LOCAL.unlearning_methods,
    "--unlearn_ratio", str(LOCAL.unlearn_ratio),
    "--proportion_unlearned_nodes", str(LOCAL.unlearn_ratio),
    "--random_seed", str(LOCAL.seed),
    "--cuda", "-1",
    "--num_epochs", "1",
    "--batch_size", "64",
]

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import torch  # noqa: E402
from parameter_parser import parameter_parser  # noqa: E402
from attack.pipeline_adapter import AttackPipeline  # noqa: E402
from attack.attack_strategies import (  # noqa: E402
    RandomStrategy, DegreeStrategy, PageRankStrategy, IMStrategy,
)

STRAT_CLS = {
    "random": RandomStrategy,
    "degree": DegreeStrategy,
    "pagerank": PageRankStrategy,
    "im": IMStrategy,
}


def candidate_count(data):
    tm = getattr(data, "train_mask", None)
    if tm is not None:
        if tm.dim() > 1:
            tm = tm.squeeze(-1)
        return int(tm.nonzero(as_tuple=False).view(-1).numel())
    return int(data.num_nodes)


def main():
    args = parameter_parser()
    args["dataset_name"] = LOCAL.dataset_name
    args["base_model"] = LOCAL.base_model
    args["unlearning_methods"] = LOCAL.unlearning_methods
    args["unlearn_ratio"] = LOCAL.unlearn_ratio
    args["proportion_unlearned_nodes"] = LOCAL.unlearn_ratio
    args["random_seed"] = LOCAL.seed
    args["seed"] = LOCAL.seed
    args["cuda"] = -1

    print(f"[concordance] building pipeline (NO TRAINING) for "
          f"{LOCAL.dataset_name}/{LOCAL.base_model} r={LOCAL.unlearn_ratio} seed={LOCAL.seed}")
    pipe = AttackPipeline(args)          # loads data + random-init model; no train
    data = pipe.data
    n_cand = candidate_count(data)
    k = max(int(n_cand * LOCAL.unlearn_ratio), 1)
    print(f"[concordance] num_nodes={data.num_nodes} candidates(train)={n_cand} k={k}")

    strategies = [s.strip() for s in LOCAL.strategies.split(",") if s.strip()]
    out = {
        "dataset": LOCAL.dataset_name,
        "base_model": LOCAL.base_model,
        "unlearn_ratio": LOCAL.unlearn_ratio,
        "seed": LOCAL.seed,
        "num_nodes": int(data.num_nodes),
        "num_candidates": n_cand,
        "k": k,
        "selections": {},
        "timings": {},
        "errors": {},
    }

    for name in strategies:
        cls = STRAT_CLS.get(name)
        if cls is None:
            out["errors"][name] = "unknown strategy"
            print(f"[concordance] SKIP unknown strategy {name}")
            continue
        try:
            t0 = time.time()
            strat = cls(args)
            sel = strat.select_nodes(data, None, k)
            sel_list = [int(x) for x in (sel.cpu().tolist() if hasattr(sel, "cpu") else list(sel))]
            dt = time.time() - t0
            out["selections"][name] = sel_list
            out["timings"][name] = round(dt, 3)
            print(f"[concordance] {name:<9} k={len(sel_list)} in {dt:.2f}s")
        except Exception as e:
            import traceback
            out["errors"][name] = f"{type(e).__name__}: {e}"
            print(f"[concordance] ERROR {name}: {e}")
            traceback.print_exc()

    out_path = OUT_DIR / f"{LOCAL.dataset_name}_{LOCAL.base_model}_r{LOCAL.unlearn_ratio}_seed{LOCAL.seed}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[concordance] wrote {out_path}")


if __name__ == "__main__":
    main()
