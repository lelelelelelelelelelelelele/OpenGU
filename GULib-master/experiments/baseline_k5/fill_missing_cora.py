"""Fill k=5 noise floor for the 4 (method, backbone) combos missing on Cora.

Targets:
    GraphRevoker x GCN   (added post dispatcher fix; not in original k=5 batch)
    GraphRevoker x GAT   (same reason)
    IDEA         x GCN   (original k=5 batch only ran GAT for IDEA)
    MEGU         x GCN   (same)

Idempotent: per-seed JSON files are reused if already present, only missing
cells are computed. Existing GIF / GNNDelete / GraphEraser averaged files are
NOT touched.

Usage (from project root, with the gnn env active):
    python experiments/baseline_k5/fill_missing_cora.py

Override python (rare):
    PYTHON=/path/to/python python experiments/baseline_k5/fill_missing_cora.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
GEN = REPO_ROOT / "experiments" / "baseline_k5" / "generate_baseline.py"
ROOT = REPO_ROOT / "results" / "baseline" / "k5_random"
LOG_DIR = REPO_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG = LOG_DIR / f"fill_k5_missing_{datetime.now():%Y%m%d_%H%M%S}.log"

DATASET = "cora"
BASELINE_K = 5
SEEDS = [111, 333, 555, 777, 999]
# Cora has 2708 nodes; k/N must be passed as --unlearn_ratio BEFORE parameter_parser
# runs, otherwise config.py captures the default 0.1 and pipeline_adapter's path
# assertion fails (added 2026-05-06, post-original-k5-batch).
DATASET_NUM_NODES = {"cora": 2708, "citeseer": 3327, "pubmed": 19717}

# Method-specific extra args (matches phase_b_cora_gcn.yaml::method_overrides).
METHOD_EXTRA_ARGS = {
    "GraphRevoker": ["--partition_method", "gpa"],  # default lpa_base unsupported by GraphRevoker
}
COMBOS = [
    ("GraphRevoker", "GCN"),
    ("GraphRevoker", "GAT"),
    ("IDEA",         "GCN"),
    ("MEGU",         "GCN"),
]

PY = os.environ.get("PYTHON") or sys.executable


def log(msg: str) -> None:
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def run_one(method: str, backbone: str, seed: int) -> str:
    cdir = ROOT / method / DATASET / backbone
    cdir.mkdir(parents=True, exist_ok=True)
    cfile = cdir / f"baseline_seed{seed}_k{BASELINE_K}.json"
    if cfile.exists():
        return "skip"
    n_nodes = DATASET_NUM_NODES[DATASET]
    ratio_k = BASELINE_K / n_nodes
    cmd = [
        PY, str(GEN),
        "--dataset_name", DATASET,
        "--base_model", backbone,
        "--unlearning_methods", method,
        "--random_seed", str(seed),
        "--baseline_k", str(BASELINE_K),
        # Sync ratio BEFORE parameter_parser runs — config.py captures it at import time
        "--unlearn_ratio", str(ratio_k),
        "--proportion_unlearned_nodes", str(ratio_k),
    ]
    cmd += METHOD_EXTRA_ARGS.get(method, [])
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"\n>>> {' '.join(cmd)}\n")
        try:
            r = subprocess.run(cmd, cwd=str(REPO_ROOT), stdout=f, stderr=subprocess.STDOUT, timeout=900)
        except subprocess.TimeoutExpired:
            return "timeout"
    return "ok" if r.returncode == 0 and cfile.exists() else "fail"


def aggregate(method: str, backbone: str) -> bool:
    cdir = ROOT / method / DATASET / backbone
    if not cdir.exists():
        return False
    f1a, f1b, f1d, details = [], [], [], []
    for s in SEEDS:
        p = cdir / f"baseline_seed{s}_k{BASELINE_K}.json"
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("f1_after") is not None: f1a.append(d["f1_after"])
        if d.get("f1_before") is not None: f1b.append(d["f1_before"])
        if d.get("f1_drop") is not None: f1d.append(d["f1_drop"])
        details.append({"seed": s, "f1_after": d.get("f1_after"),
                        "f1_before": d.get("f1_before"), "f1_drop": d.get("f1_drop")})
    if not f1a:
        return False
    out = {
        "f1_after": float(np.mean(f1a)),
        "f1_after_std": float(np.std(f1a)),
        "f1_before": float(np.mean(f1b)) if f1b else None,
        "f1_drop": float(np.mean(f1d)) if f1d else None,
        "n_seeds": len(f1a),
        "seeds_used": [d["seed"] for d in details if d.get("f1_after") is not None],
        "per_seed_details": details,
        "config": {
            "dataset_name": DATASET, "base_model": backbone,
            "unlearning_methods": method, "k": BASELINE_K,
            "strategy": "random", "averaged": True,
            "timestamp": datetime.now().isoformat(),
        },
    }
    (cdir / f"baseline_averaged_k{BASELINE_K}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    log(f"  [AVG] {method}/{DATASET}/{backbone}: f1_after={out['f1_after']:.4f} +/- {out['f1_after_std']:.4f}  n={out['n_seeds']}")
    return True


def main() -> int:
    log(f"===== fill_missing_cora.py  {datetime.now()} =====")
    log(f"PY:        {PY}")
    log(f"REPO_ROOT: {REPO_ROOT}")
    log(f"DATASET:   {DATASET}")
    log(f"BASELINE_K:{BASELINE_K}")
    log(f"SEEDS:     {SEEDS}")
    log("COMBOS:")
    for m, b in COMBOS:
        log(f"  - {m} x {DATASET}/{b}")
    log(f"LOG:       {LOG}")
    log("")

    # quick sanity: the python we picked must work and the generator must exist
    if not GEN.exists():
        log(f"ERROR: generator missing at {GEN}")
        return 2
    try:
        subprocess.run([PY, "-c", "import sys"], check=True, capture_output=True)
    except Exception as e:
        log(f"ERROR: PY does not run: {PY}  ({e})")
        log("       set PYTHON env var to a working python")
        return 2

    counters = {"ok": 0, "skip": 0, "fail": 0, "timeout": 0}
    total = len(COMBOS) * len(SEEDS)
    i = 0
    for method, backbone in COMBOS:
        log(f"----- {method} x {DATASET}/{backbone} -----")
        for s in SEEDS:
            i += 1
            tag = f"[{i}/{total}]"
            status = run_one(method, backbone, s)
            counters[status] += 1
            log(f"{tag} [{status.upper():4s}] {method}/{backbone}/seed={s}")

    log("")
    log(f"===== per-seed phase done: {counters} =====")
    log("")
    log(f"===== aggregating into baseline_averaged_k{BASELINE_K}.json =====")

    n_avg_ok = 0
    for method, backbone in COMBOS:
        if aggregate(method, backbone):
            n_avg_ok += 1
        else:
            log(f"  [WARN] {method}/{DATASET}/{backbone}: aggregation skipped (no usable seeds)")

    log("")
    log(f"===== ALL DONE  {datetime.now()} =====")
    log(f"  per-seed: {counters}")
    log(f"  aggregate: {n_avg_ok}/{len(COMBOS)} cells")
    log(f"  log: {LOG}")

    if counters["fail"] or counters["timeout"] or n_avg_ok < len(COMBOS):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
