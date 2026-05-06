"""Re-run eval_collateral.py for IF-family cells (GIF + IDEA only).

Why: commit `949d0f8` (fix(IF-family): write params_esti back) makes
`AttackPipeline._get_trained_model()` return the actual post-unlearn weights
instead of the stale baseline for GIF/IDEA. Cells written before that commit
have stale `collateral.json` + `predictions.npz` (perf_unlearn / gap /
hop_decay / pred_shift / logits_unlearned all point at the original-trained
model). attack.json is unaffected and stays untouched.

What this does:
1. Loads the yaml config, expands the matrix
2. Filters to (method ∈ {GIF, IDEA}) by default, all (strategy, seed)
3. For each cell:
   - Sanity: attack.json + cache must already exist (we don't re-run demo_attack)
   - Delete stale collateral.json + predictions.npz (defensive — eval_collateral overwrites,
     but explicit delete keeps "no orphan partial files" invariant)
   - Run eval_collateral.py with --output_dir → writes new collateral.json + predictions.npz
   - Refresh _meta.json's git_sha + timestamp so audit reflects the post-fix re-eval

Usage (on the 4090 / H800 server):
    # First: ensure the fix commit is on the working tree
    git log --oneline | head -3   # should show 949d0f8 in history
    # OR cherry-pick if on a branch without the fix
    git cherry-pick 949d0f8

    # Then run:
    python scripts/redo_collateral_if_family.py experiments/configs/phase_b_cora_gcn.yaml
    python scripts/redo_collateral_if_family.py experiments/configs/phase_b_cora_gat.yaml

    # Optional flags:
    --methods GIF,IDEA       # default; comma-sep list, can extend if other methods get same fix
    --dry_run                # just enumerate, no delete/run
    --no_meta_refresh        # leave _meta.json untouched (audit stays at original git_sha)
    --strategies random,...  # subset; default = all 6 in yaml
    --seeds 42,212           # subset; default = all 5 in yaml

Exit codes: 0 = all PASS; non-zero = at least one cell failed.
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
from typing import List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. `pip install pyyaml` (or activate gnn env).", file=sys.stderr)
    raise

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METHODS = ("GIF", "IDEA")


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
    return os.environ.get("PYTHON", sys.executable)


def cell_dir(cfg: dict, method: str, strategy: str, seed: int) -> Path:
    cell = "{}_{}_{}".format(cfg["dataset"], cfg["base_model"], "r{}".format(cfg["ratio"]))
    leaf = "{}_{}".format(method, strategy)
    return REPO_ROOT / "results" / "runs" / cell / leaf / "seed{}".format(seed)


def method_overrides(cfg: dict, method: str) -> List[str]:
    override = (cfg.get("method_overrides", {}) or {}).get(method, {}) or {}
    return list(override.get("extra_args", []) or [])


def model_overrides(cfg: dict) -> List[str]:
    overrides = (cfg.get("model_overrides", {}) or {}).get(cfg["base_model"], {}) or {}
    out: List[str] = []
    for k, v in overrides.items():
        out.extend(["--{}".format(k), str(v)])
    return out


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["_source_path"] = str(path)
    return cfg


def has_attack(d: Path) -> bool:
    p = d / "attack.json"
    if not p.exists():
        return False
    try:
        json.loads(p.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def refresh_meta(d: Path, cfg: dict, method: str, strategy: str, seed: int) -> None:
    meta_path = d / "_meta.json"
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        meta = {}
    # Preserve original audit fields, append a re-eval marker.
    history = meta.get("collateral_redo_history", [])
    history.append({
        "previous_git_sha": meta.get("git_sha"),
        "previous_timestamp": meta.get("timestamp"),
        "reason": "fix(IF-family) write-back patch (commit 949d0f8)",
    })
    meta["collateral_redo_history"] = history
    meta["git_sha"] = _git_sha()
    meta["timestamp"] = datetime.now().isoformat()
    meta["hostname"] = socket.gethostname()
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def redo_cell(cfg: dict, method: str, strategy: str, seed: int,
              dry_run: bool, refresh_meta_flag: bool) -> str:
    d = cell_dir(cfg, method, strategy, seed)
    rel = d.relative_to(REPO_ROOT)

    if not d.exists():
        print("[SKIP] {} — directory missing (cell never ran)".format(rel))
        return "missing"

    if not has_attack(d):
        print("[SKIP] {} — attack.json missing/corrupt; demo_attack first".format(rel))
        return "no_attack"

    coll_path = d / "collateral.json"
    npz_path = d / "predictions.npz"

    if dry_run:
        print("[DRY-RUN] would redo {} (delete coll/npz + eval_collateral)".format(rel))
        return "dry_run"

    # Delete stale outputs
    for p in (coll_path, npz_path):
        if p.exists():
            p.unlink()

    # Build CLI for eval_collateral
    py = _python_bin()
    defaults = cfg.get("defaults", {}) or {}
    extra = list(cfg.get("extra_args", []) or [])
    extra += method_overrides(cfg, method)
    extra += model_overrides(cfg)

    cmd = [
        py, str(REPO_ROOT / "eval_collateral.py"),
        "--dataset_name", cfg["dataset"],
        "--base_model", cfg["base_model"],
        "--unlearning_methods", method,
        "--strategies", strategy,
        "--unlearn_ratio", str(cfg["ratio"]),
        "--random_seed", str(seed),
        "--output_dir", str(d),
        "--num_epochs", str(defaults.get("num_epochs", 100)),
        "--batch_size", str(defaults.get("batch_size", 64)),
        "--cuda", str(defaults.get("cuda", 0)),
    ]
    if defaults.get("save_predictions", True):
        cmd.append("--save_predictions")
    cmd += extra

    print("[run] eval_collateral {}/{}/seed{} → {}".format(method, strategy, seed, rel))
    t0 = time.time()
    rc = subprocess.run(cmd, cwd=str(REPO_ROOT)).returncode
    dt = time.time() - t0
    if rc != 0:
        print("[FAIL] rc={} (dt={:.1f}s) {}".format(rc, dt, rel), file=sys.stderr)
        return "failed"

    # Sanity: did the new files actually appear?
    if not coll_path.exists() or not npz_path.exists():
        print("[FAIL] {} — eval_collateral exited 0 but outputs missing".format(rel),
              file=sys.stderr)
        return "no_output"

    if refresh_meta_flag:
        refresh_meta(d, cfg, method, strategy, seed)

    print("[OK]   {}  (dt={:.1f}s)".format(rel, dt))
    return "ok"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("yaml", type=Path, help="experiments/configs/phase_b_<dataset>_<model>.yaml")
    ap.add_argument("--methods", default=",".join(DEFAULT_METHODS),
                    help="comma-sep method list to redo (default: GIF,IDEA)")
    ap.add_argument("--strategies", default=None,
                    help="comma-sep strategy subset (default: all in yaml)")
    ap.add_argument("--seeds", default=None,
                    help="comma-sep seed subset (default: all in yaml)")
    ap.add_argument("--dry_run", action="store_true")
    ap.add_argument("--no_meta_refresh", action="store_true",
                    help="leave _meta.json git_sha/timestamp untouched")
    args = ap.parse_args()

    if not args.yaml.exists():
        print("ERROR: yaml not found: {}".format(args.yaml), file=sys.stderr)
        return 2
    cfg = load_yaml(args.yaml)

    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    strategies = ([s.strip() for s in args.strategies.split(",") if s.strip()]
                  if args.strategies else list(cfg.get("strategies", [])))
    seeds = ([int(x) for x in args.seeds.split(",") if x.strip()]
             if args.seeds else list(cfg.get("seeds", [])))

    yaml_methods = set(cfg.get("methods", []) or [])
    bad = [m for m in methods if m not in yaml_methods]
    if bad:
        print("WARN: requested methods not in yaml ({}): {}".format(args.yaml, bad),
              file=sys.stderr)

    print("[plan] yaml={}  methods={}  strategies={}  seeds={}".format(
        args.yaml.name, methods, strategies, seeds))
    total = len(methods) * len(strategies) * len(seeds)
    print("[plan] {} cells (= {} methods x {} strategies x {} seeds)".format(
        total, len(methods), len(strategies), len(seeds)))
    print("[plan] git_sha={}  hostname={}".format(_git_sha()[:7], socket.gethostname()))
    print()

    counters = {"ok": 0, "failed": 0, "missing": 0, "no_attack": 0,
                "no_output": 0, "dry_run": 0}
    t_start = time.time()

    for method in methods:
        for strategy in strategies:
            for seed in seeds:
                status = redo_cell(cfg, method, strategy, seed,
                                   dry_run=args.dry_run,
                                   refresh_meta_flag=not args.no_meta_refresh)
                counters[status] = counters.get(status, 0) + 1

    dt = time.time() - t_start
    print()
    print("[done] {:.1f} min total  status: {}".format(dt / 60, counters))

    return 0 if counters["failed"] == 0 and counters.get("no_output", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
