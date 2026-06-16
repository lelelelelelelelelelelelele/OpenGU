"""
Verify that topology-only strategies (degree, pagerank, im) produce
SelectionCache keys that are stable across (unlearning_methods, GU seed).

Verifies:
  1. degree cell on (GIF, seed=42) and (GNNDelete, seed=212) yield same key
  2. Same for pagerank
  3. Same for im (already wired via im_selector_seed anchor)
  4. random differs across seeds (sanity — random IS seed-dependent)
  5. tracin differs across (method, seed) (sanity — TracIn IS model-dependent)

This is a tiny test on cora — no model training, no actual selection;
just constructs AttackManager and inspects _build_selection_config keys.

Usage:
    H:/conda_package/envs/gnn/python.exe scripts/test_topology_strategy_cache_keys.py
"""
import argparse
import os
import sys


def _extract_demo_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--dataset_name", type=str, default="cora")
    parser.add_argument("--base_model", type=str, default="GCN")
    parser.add_argument("--unlearn_ratio", type=float, default=0.05)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--unlearning_methods", type=str, default="GIF")

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

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402


def _make_manager(method: str, seed: int):
    args = parameter_parser()
    args["dataset_name"] = _demo_args.dataset_name
    args["base_model"] = _demo_args.base_model
    args["unlearning_methods"] = method
    args["unlearn_ratio"] = _demo_args.unlearn_ratio
    args["num_epochs"] = _demo_args.num_epochs
    args["batch_size"] = _demo_args.batch_size
    args["random_seed"] = seed
    args["seed"] = seed
    args["cuda"] = _demo_args.cuda
    return AttackManager(args, use_cache=False)


def _key_for(mgr: AttackManager, strategy: str, k: int) -> str:
    cfg = mgr._build_selection_config(strategy, k)
    return mgr.cache.build_selection_key(cfg) if mgr.cache else mgr._stable_hash(cfg)


def main() -> int:
    print("=" * 72)
    print("Topology-only strategy cache key test (degree / pagerank / im)")
    print("=" * 72)

    print("\n[init] Building 4 AttackManagers: (GIF, 42), (GIF, 212), (GNNDelete, 42), (GNNDelete, 212)")
    mgr_a = _make_manager("GIF", 42)         # baseline
    mgr_b = _make_manager("GIF", 212)        # different seed, same method
    mgr_c = _make_manager("GNNDelete", 42)   # different method, same seed
    mgr_d = _make_manager("GNNDelete", 212)  # both different

    k = 100
    failures = []
    print()

    # Topology-only: keys must be EQUAL across (method, seed)
    for strat in ("degree", "pagerank", "im"):
        ka = _key_for(mgr_a, strat, k)
        kb = _key_for(mgr_b, strat, k)
        kc = _key_for(mgr_c, strat, k)
        kd = _key_for(mgr_d, strat, k)
        same = (ka == kb == kc == kd)
        verdict = "[OK] shared" if same else "[FAIL] DIFFERENT"
        print(f"  {strat:10s} (GIF,42)={ka[:12]} (GIF,212)={kb[:12]} (GND,42)={kc[:12]} (GND,212)={kd[:12]}  {verdict}")
        if not same:
            failures.append(f"{strat}: keys differ across (method, seed) — should be topology-only")

    # random: must differ across seeds
    ra = _key_for(mgr_a, "random", k)
    rb = _key_for(mgr_b, "random", k)
    print(f"\n  random     (GIF,42)={ra[:12]} (GIF,212)={rb[:12]}  "
          f"{'[OK] seed-dependent' if ra != rb else '[FAIL] should differ'}")
    if ra == rb:
        failures.append("random: keys equal across seeds — should be seed-dependent")

    # tracin: must differ across SEEDS (model trained with different seed →
    # different weights → different gradient → different selection).
    # Note: tracin SelectionCache key is intentionally method-agnostic
    # at the AttackManager level — the design assumes "same (dataset,
    # base_model, seed) yields the same trained base model regardless of
    # unlearning_method that wraps the training". The TracIn ScoreCache
    # (tracin_strategy.py) IS method-aware as a conservative belt-and-
    # suspenders measure, but it's a separate cache layer.
    ta = _key_for(mgr_a, "tracin", k)
    tb = _key_for(mgr_b, "tracin", k)
    print(f"\n  tracin     (GIF,42)={ta[:12]} (GIF,212)={tb[:12]}  "
          f"{'[OK] seed-dependent' if ta != tb else '[FAIL] should differ across seeds'}")
    if ta == tb:
        failures.append("tracin: keys equal across seeds — should be model-seed-dependent")

    print("\n" + "=" * 72)
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS — topology-only strategies share keys; model-dependent strategies don't")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
