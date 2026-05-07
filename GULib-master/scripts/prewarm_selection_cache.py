"""
Pre-compute and cache strategy selections for every (seed, strategy) combo
in a Phase B yaml config. Skips the GU pipeline entirely.

Use case: rent a big GPU (A100 80GB) for the expensive selection step, scp
the resulting `results/selection_cache/` directory to a cheap GPU (4090),
and run the full B.2 yaml there with all selections already cached.

Workflow:
    # On A100
    python scripts/prewarm_selection_cache.py experiments/configs/phase_b_arxiv.yaml
    tar czf selection_cache.tar.gz results/selection_cache/

    # scp to 4090, then unpack and run normally
    tar xzf selection_cache.tar.gz
    python experiments/run.py experiments/configs/phase_b_arxiv.yaml
    # Every cell hits the cache; only GU + retrain + MIA actually run.

Caveat: The cache key fingerprints (dataset, base_model, seed, k, graph,
strategy params) but NOT training hyperparameters (num_epochs, lr, dropout).
This is fine when both machines run the SAME yaml. If you change training
hyperparameters between machines, invalidate the cache first
(rm results/selection_cache/*.json).
"""
import argparse
import os
import sys


def _extract_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("yaml_path", type=str, help="Phase B config yaml")
    parser.add_argument("--strategies", type=str, default=None,
                        help="Comma-separated subset of strategies to prewarm. "
                             "Default: all reusable strategies in the yaml.")
    parser.add_argument("--seeds", type=str, default=None,
                        help="Comma-separated seed override. Default: yaml seeds.")
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--force", action="store_true",
                        help="Recompute even if cache hits.")
    args, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining
    return args


_args = _extract_args()

import time  # noqa: E402
import yaml  # noqa: E402
import torch  # noqa: E402

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser  # noqa: E402
from attack import AttackManager  # noqa: E402
from attack.selection_cache import SelectionResult  # noqa: E402


def _candidate_node_count(data) -> int:
    train_mask = getattr(data, "train_mask", None)
    if train_mask is not None:
        if train_mask.dim() > 1:
            train_mask = train_mask.squeeze(-1)
        return int(train_mask.nonzero(as_tuple=False).view(-1).numel())

    train_indices = getattr(data, "train_indices", None)
    if train_indices is not None:
        return int(len(train_indices))

    return int(data.num_nodes)


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


def _build_args(cfg, seed, method=None):
    """Reconstruct CLI args for parameter_parser using the yaml config.

    `method` selects the unlearning_methods value for this prewarm pass.
    Defaults to cfg["methods"][0] for backward compatibility — but callers
    that prewarm method-dependent strategies (tracin, hybrid) MUST iterate
    over cfg["methods"] and pass each method explicitly so per-method
    ScoreCache entries (`if/<key>.npz`) get written for every method.
    """
    defaults = cfg.get("defaults", {}) or {}
    extra = list(cfg.get("extra_args", []) or [])
    overrides = (cfg.get("model_overrides", {}) or {}).get(cfg["base_model"], {}) or {}

    if method is None:
        method = cfg["methods"][0]

    cli = [
        "--dataset_name", str(cfg["dataset"]),
        "--base_model", str(cfg["base_model"]),
        "--unlearning_methods", str(method),
        "--unlearn_ratio", str(cfg["ratio"]),
        "--cuda", str(_args.cuda),
        "--num_epochs", str(defaults.get("num_epochs", 100)),
        "--batch_size", str(defaults.get("batch_size", 64)),
    ]
    cli += extra
    for k, v in overrides.items():
        cli += [f"--{k}", str(v)]

    sys.argv = [sys.argv[0]] + cli
    args = parameter_parser()
    args["dataset_name"] = str(cfg["dataset"])
    args["base_model"] = str(cfg["base_model"])
    args["unlearning_methods"] = str(method)
    args["unlearn_ratio"] = float(cfg["ratio"])
    args["num_epochs"] = int(defaults.get("num_epochs", 100))
    args["batch_size"] = int(defaults.get("batch_size", 64))
    args["cuda"] = _args.cuda
    args["random_seed"] = int(seed)
    args["seed"] = int(seed)
    return args


def _prewarm_seed(cfg, seed, strategies, method, force=False):
    """Init AttackManager once for (this seed, this method); cache every requested strategy.

    `method` is the unlearning_methods to instantiate AttackManager with.
    For topology-only strategies (im, degree, pagerank, random) the choice
    of method does not affect the cache key, so a single method covers all.
    For per-method strategies (tracin, hybrid), the caller must invoke this
    once per method to populate per-method ScoreCache entries.
    """
    print("\n" + "=" * 70)
    print(f"[prewarm] seed={seed}  method={method}  strategies={strategies}")
    print("=" * 70)

    _seed_everything(seed)
    args = _build_args(cfg, seed, method)
    if torch.cuda.is_available():
        torch.cuda.set_device(args["cuda"])

    t0 = time.perf_counter()
    manager = AttackManager(args, use_cache=True)
    t_init = time.perf_counter() - t0
    print(f"[prewarm] AttackManager init (data + base train) in {t_init:.1f}s")

    data, model = manager.data, manager.model
    k = int(_candidate_node_count(data) * args["unlearn_ratio"])

    available = manager.list_strategies()
    reusable = AttackManager.REUSABLE_SELECTION_STRATEGIES
    trained_model_strategies = {
        name for name in strategies
        if name in available and getattr(manager._strategies[name], "requires_trained_model", False)
    }
    method_name = str(args.get("unlearning_methods", ""))
    is_shard_method = method_name in AttackManager.SHARD_METHODS_REQUIRE_CANONICAL_SELECTOR_CACHE
    base_model_ensured = False  # lazy: only train when a cache MISS actually requires it

    summary = []
    for name in strategies:
        if name not in available:
            print(f"[skip] {name}: unknown strategy")
            continue
        if name not in reusable:
            print(f"[skip] {name}: not in REUSABLE_SELECTION_STRATEGIES; "
                  f"would not be picked up by run.py later")
            continue

        selection_config = manager._build_selection_config(name, k)
        cached, key, source = manager.selection_cache.get(selection_config)
        if cached is not None and not force:
            # SelectionCache key for tracin is method-agnostic, so a shard
            # method (GraphEraser) can legitimately hit a cache written by
            # an earlier GIF/GNNDelete prewarm pass — accept it.
            print(f"[hit ] {name} key={key}  source={source}")
            summary.append((name, "hit", 0.0, key))
            continue

        # Cache MISS — we'd actually need to compute. Now (and only now) refuse
        # if this is a shard/SISA method asked to compute a trained-model
        # selector: it has no canonical full-graph model to differentiate on.
        if name in trained_model_strategies and is_shard_method:
            raise SystemExit(
                f"[FATAL] prewarm_selection_cache: SelectionCache MISS for "
                f"strategy={name} method={method_name} key={key}, and "
                f"{method_name} is a shard/SISA method that cannot compute "
                "trained-model selectors. Put a canonical full-model method "
                "(GIF or GNNDelete) first in the yaml so it writes the cache, "
                "then this shard method will hit it. Or use experiments/run.py "
                "top-to-bottom."
            )

        # Lazy: train base model only on the first real compute.
        if name in trained_model_strategies and not base_model_ensured:
            manager.pipeline._ensure_base_model_trained()
            model = manager.pipeline.model
            base_model_ensured = True

        strat = manager._strategies[name]
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        t_sel0 = time.perf_counter()
        selected = strat.select_nodes(data, model, k)
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        t_sel = time.perf_counter() - t_sel0

        result = SelectionResult(
            strategy_name=name,
            selected_nodes=[int(x) for x in selected.cpu().tolist()],
            selection_time=float(t_sel),
            selection_key=key or "",
            metadata={
                "dataset_name": selection_config.get("dataset_name"),
                "base_model": selection_config.get("base_model"),
                "seed": selection_config.get("seed"),
                "graph_fingerprint": selection_config.get("graph_fingerprint"),
                "prewarm": True,
            },
        )
        path = manager.selection_cache.save(result, selection_config)
        print(f"[save] {name} key={key}  time={t_sel:.2f}s  -> {path}")
        summary.append((name, "save", t_sel, key))

    return summary


def main():
    with open(_args.yaml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    yaml_strategies = cfg.get("strategies", [])
    yaml_seeds = cfg.get("seeds", [])

    if _args.strategies:
        strategies = [s.strip() for s in _args.strategies.split(",") if s.strip()]
    else:
        # Only prewarm cacheable strategies — others would just be wasted work.
        reusable = AttackManager.REUSABLE_SELECTION_STRATEGIES
        strategies = [s for s in yaml_strategies if s in reusable]
    if _args.seeds:
        seeds = [int(s) for s in _args.seeds.split(",") if s.strip()]
    else:
        seeds = [int(s) for s in yaml_seeds]

    # Method-dependent strategies (tracin, hybrid) need per-method prewarm
    # because their ScoreCache key includes unlearning_methods. Topology-only
    # strategies (im, degree, pagerank) and random use method-agnostic cache
    # keys, so a single method run is enough — no point looping methods.
    METHOD_DEPENDENT_STRATEGIES = {"tracin", "hybrid"}
    yaml_methods = list(cfg.get("methods", []) or [])
    if not yaml_methods:
        raise SystemExit("[FATAL] yaml has no `methods` field")
    needs_method_loop = any(s in METHOD_DEPENDENT_STRATEGIES for s in strategies)
    methods = yaml_methods if needs_method_loop else [yaml_methods[0]]

    print(f"[plan] yaml={_args.yaml_path}  dataset={cfg['dataset']}  "
          f"model={cfg['base_model']}  ratio={cfg['ratio']}")
    print(f"[plan] strategies={strategies}  seeds={seeds}  methods={methods}  force={_args.force}")
    print(f"[plan] total prewarm passes: {len(strategies) * len(seeds) * len(methods)} "
          f"(method-loop {'ON' if needs_method_loop else 'OFF'}; "
          f"topology-only strategies will hit cache after the first pass)")

    all_summary = []
    t_global = time.perf_counter()
    for seed in seeds:
        for method in methods:
            s = _prewarm_seed(cfg, seed, strategies, method, force=_args.force)
            all_summary.extend([(seed, *row) for row in s])
    t_total = time.perf_counter() - t_global

    print("\n" + "=" * 70)
    print("[summary]")
    print("=" * 70)
    n_save = sum(1 for r in all_summary if r[2] == "save")
    n_hit = sum(1 for r in all_summary if r[2] == "hit")
    t_compute = sum(r[3] for r in all_summary if r[2] == "save")
    print(f"  computed: {n_save}   hit (already cached): {n_hit}")
    print(f"  selection compute time: {t_compute:.1f}s   wall total: {t_total:.1f}s")
    print(f"  cache dir: ./results/selection_cache/  (ls -lh to see written files)")
    print("\nTo transfer to another machine:")
    print("  tar czf selection_cache.tar.gz results/selection_cache/")


if __name__ == "__main__":
    main()
