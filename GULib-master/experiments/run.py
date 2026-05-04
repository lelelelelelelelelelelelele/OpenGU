"""
experiments/run.py — YAML-driven experiment runner.

Replaces the ad-hoc bash scripts under scripts/experiments/. One yaml config
describes a full experiment matrix (dataset × model × method × strategy × seed).
Runner subprocess-calls demo_attack.py and eval_collateral.py per cell, with
output redirected to the canonical `results/runs/` layout:

    results/runs/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{seed}/
        attack.json          # demo_attack output (single-strategy comparison JSON)
        collateral.json      # eval_collateral output (gap, collateral, hop_decay)
        predictions.npz      # logits_{before,unlearned,retrained} + masks (forward-only metric cache)
        _meta.json           # config snapshot + git_sha + timestamp + hostname

Skip-if-exists by default: if all 4 files exist, the cell is skipped. Use
--force to re-run.

Usage:
    python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
    python experiments/run.py experiments/configs/phase_b_arxiv.yaml --force
    python experiments/run.py experiments/configs/<cfg>.yaml --dry_run

Schema (see experiments/configs/phase_b_cora_gcn.yaml for a worked example):
    name: <str>           # cell prefix; informational
    dataset: <str>
    base_model: <str>
    ratio: <float>
    methods: [<str>, ...]
    strategies: [<str>, ...]
    seeds: [<int>, ...]
    defaults:
        save_predictions: <bool>      # default true
        run_collateral: <bool>        # default true
        no_cache: <bool>              # default false (use cache)
        num_epochs: <int>             # default 100
        batch_size: <int>             # default 64
        cuda: <int>                   # default 0
    extra_args: [<str>, ...]          # passed verbatim to demo_attack and eval_collateral
    model_overrides:                  # injected as extra_args; per-model knobs
        GCN:
            gcn_num_layers: 3
            gcn_hidden: 256
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. `pip install pyyaml` (or via the gnn env).", file=sys.stderr)
    raise


REPO_ROOT = Path(__file__).resolve().parents[1]


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def _python_bin() -> str:
    # Prefer current interpreter (whichever launched run.py). Falls back via env.
    return os.environ.get("PYTHON_BIN", sys.executable)


def cell_dir(cfg: Dict[str, Any], method: str, strategy: str, seed: int) -> Path:
    cell = f"{cfg['dataset']}_{cfg['base_model']}_r{cfg['ratio']}"
    leaf = f"{method}_{strategy}"
    return REPO_ROOT / "results" / "runs" / cell / leaf / f"seed{seed}"


def is_complete(d: Path) -> bool:
    expected = ["attack.json", "collateral.json", "predictions.npz", "_meta.json"]
    return all((d / f).exists() for f in expected)


def model_overrides(cfg: Dict[str, Any]) -> List[str]:
    """Extract per-model overrides as a flat list of CLI flags."""
    overrides = (cfg.get("model_overrides", {}) or {}).get(cfg["base_model"], {}) or {}
    out: List[str] = []
    for k, v in overrides.items():
        out.extend([f"--{k}", str(v)])
    return out


def run_cell(cfg: Dict[str, Any], method: str, strategy: str, seed: int,
             *, force: bool, dry_run: bool) -> str:
    out_dir = cell_dir(cfg, method, strategy, seed)
    if not force and is_complete(out_dir):
        return "skipped"
    if dry_run:
        return "would_run"

    out_dir.mkdir(parents=True, exist_ok=True)
    py = _python_bin()
    defaults = cfg.get("defaults", {}) or {}
    extra = list(cfg.get("extra_args", []) or [])
    extra += model_overrides(cfg)

    # 1) demo_attack: writes attack.json
    cmd1 = [
        py, str(REPO_ROOT / "demo_attack.py"),
        "--dataset_name", cfg["dataset"],
        "--base_model", cfg["base_model"],
        "--unlearning_methods", method,
        "--strategies", strategy,
        "--unlearn_ratio", str(cfg["ratio"]),
        "--seed", str(seed),
        "--save_path", str(out_dir / "attack.json"),
        "--num_epochs", str(defaults.get("num_epochs", 100)),
        "--batch_size", str(defaults.get("batch_size", 64)),
        "--cuda", str(defaults.get("cuda", 0)),
    ]
    if defaults.get("no_cache", False):
        cmd1.append("--no_cache")
    cmd1 += extra
    print(f"\n[run] demo_attack {method}/{strategy}/seed{seed} → {out_dir.relative_to(REPO_ROOT)}")
    rc = subprocess.run(cmd1, cwd=str(REPO_ROOT)).returncode
    if rc != 0:
        print(f"[FAIL] demo_attack rc={rc} for {out_dir}", file=sys.stderr)
        return "failed_attack"

    # 2) eval_collateral: writes collateral.json + predictions.npz
    if defaults.get("run_collateral", True):
        cmd2 = [
            py, str(REPO_ROOT / "eval_collateral.py"),
            "--dataset_name", cfg["dataset"],
            "--base_model", cfg["base_model"],
            "--unlearning_methods", method,
            "--strategies", strategy,
            "--unlearn_ratio", str(cfg["ratio"]),
            "--random_seed", str(seed),
            "--output_dir", str(out_dir),
        ]
        if defaults.get("save_predictions", True):
            cmd2.append("--save_predictions")
        cmd2 += extra
        print(f"[run] eval_collateral {method}/{strategy}/seed{seed}")
        rc = subprocess.run(cmd2, cwd=str(REPO_ROOT)).returncode
        if rc != 0:
            print(f"[FAIL] eval_collateral rc={rc} for {out_dir}", file=sys.stderr)
            return "failed_collateral"

    # 3) _meta.json — audit trail
    meta = {
        "config_name": cfg.get("name", "unnamed"),
        "config": {k: v for k, v in cfg.items() if k != "_source_path"},
        "method": method,
        "strategy": strategy,
        "seed": seed,
        "timestamp": datetime.now().isoformat(),
        "git_sha": _git_sha(),
        "hostname": socket.gethostname(),
        "python": py,
    }
    (out_dir / "_meta.json").write_text(json.dumps(meta, indent=2))
    return "completed"


def expand_matrix(cfg: Dict[str, Any]):
    """Yield (method, strategy, seed) triples in (method, strategy, seed) order."""
    for method in cfg["methods"]:
        for strategy in cfg["strategies"]:
            for seed in cfg["seeds"]:
                yield method, strategy, seed


def load_config(path: Path) -> Dict[str, Any]:
    # Force UTF-8 — Windows default codec (GBK) chokes on Chinese comments.
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["_source_path"] = str(path)
    required = ["dataset", "base_model", "ratio", "methods", "strategies", "seeds"]
    missing = [k for k in required if k not in cfg]
    if missing:
        raise SystemExit(f"Config {path} missing required keys: {missing}")
    return cfg


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("config", type=Path, help="path to yaml config")
    ap.add_argument("--force", action="store_true", help="re-run even if outputs exist")
    ap.add_argument("--dry_run", action="store_true", help="report what would run, no execution")
    ap.add_argument("--limit", type=int, default=None, help="cap number of cells (debug)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    print(f"=== Loaded {args.config.name} ===")
    print(f"  cell: {cfg['dataset']}_{cfg['base_model']}_r{cfg['ratio']}")
    print(f"  methods × strategies × seeds = {len(cfg['methods'])} × {len(cfg['strategies'])} × {len(cfg['seeds'])}")
    print(f"  total cells: {len(cfg['methods']) * len(cfg['strategies']) * len(cfg['seeds'])}")
    if cfg.get("model_overrides", {}).get(cfg["base_model"]):
        print(f"  model_overrides: {cfg['model_overrides'][cfg['base_model']]}")

    counters: Dict[str, int] = {"completed": 0, "skipped": 0, "would_run": 0,
                                 "failed_attack": 0, "failed_collateral": 0}
    t0 = time.time()
    for idx, (method, strategy, seed) in enumerate(expand_matrix(cfg)):
        if args.limit is not None and idx >= args.limit:
            break
        status = run_cell(cfg, method, strategy, seed,
                          force=args.force, dry_run=args.dry_run)
        counters[status] = counters.get(status, 0) + 1

    elapsed = time.time() - t0
    print("\n=== Summary ===")
    for k, v in counters.items():
        if v > 0:
            print(f"  {k}: {v}")
    print(f"  elapsed: {elapsed:.1f}s")
    failures = counters.get("failed_attack", 0) + counters.get("failed_collateral", 0)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
