"""Cleanup IF-family stale collateral artifacts so experiments/run.py re-runs them.

After commit 949d0f8 (fix(IF-family) write-back patch), GIF/IDEA cells that
were generated before the fix carry stale `collateral.json` + `predictions.npz`
(perf_unlearn / gap / hop_decay / pred_shift / logits_unlearned all reflect
the originally-trained model instead of the post-unlearn weights).

Workflow on the server:
    # 1. Cherry-pick / merge the fix
    git cherry-pick 949d0f8

    # 2. Run this cleanup (deletes 240 files: 120 cells x {collateral.json, predictions.npz})
    python scripts/cleanup_if_family_collateral.py

    # 3. Re-run via the canonical runner — it sees "incomplete" cells (missing
    #    collateral.json) and re-runs them. demo_attack hits ResultCache for
    #    the same selected_nodes/f1_after/mia_auc, eval_collateral runs fresh
    #    with the patched approxi(). Other 4 methods (GNNDelete/MEGU/Eraser/Revoker)
    #    stay "complete" and are skipped.
    python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
    python experiments/run.py experiments/configs/phase_b_cora_gat.yaml

    # 4. Gate + ship as usual
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
    bash scripts/ship_results.sh cora

What we delete (per cell):
    collateral.json     — perf_unlearn / gap / hop_decay / pred_shift (stale)
    predictions.npz     — logits_unlearned is stale; logits_before/retrained
                          are correct but bundled in the same file, must be regenerated

What we keep:
    attack.json         — selected_nodes / f1_after / mia_auc are bug-free
    _meta.json          — preserves audit; experiments/run.py will overwrite with new
                          git_sha + timestamp on re-run

Cell list: GIF + IDEA × {cora_GCN_r0.05, cora_GAT_r0.05} × 6 strategies × 5 seeds = 120 cells.
"""
from __future__ import annotations

import argparse
import pathlib
import sys


METHODS = ("GIF", "IDEA")
BACKBONES = ("GCN", "GAT")
STRATEGIES = ("random", "degree", "pagerank", "tracin", "im", "hybrid")
SEEDS = (42, 212, 722, 1337, 2024)
RATIO_TAG = "r0.05"
DATASET = "cora"
CELL_OUTPUTS_TO_DELETE = ("collateral.json", "predictions.npz")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default="results/runs",
                    help="cell root (default: results/runs); on the server cells live"
                         " here. On a local mirror after MIGRATION_RUNBOOK §3.4 they live"
                         " under results/runs/4090/, so pass --root results/runs/4090.")
    ap.add_argument("--dry_run", action="store_true",
                    help="enumerate without deleting")
    ap.add_argument("--methods", default=",".join(METHODS),
                    help="comma-sep methods to clean (default: GIF,IDEA)")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.exists():
        print("ERROR: root not found: {}".format(root), file=sys.stderr)
        return 2

    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    print("[plan] root={}  methods={}  backbones={}  strategies={}  seeds={}".format(
        root, methods, list(BACKBONES), list(STRATEGIES), list(SEEDS)))
    expected = len(methods) * len(BACKBONES) * len(STRATEGIES) * len(SEEDS)
    print("[plan] expected {} cells (= {} methods x {} backbones x {} strategies x {} seeds)".format(
        expected, len(methods), len(BACKBONES), len(STRATEGIES), len(SEEDS)))
    print()

    n_cells_seen = 0
    n_cells_clean = 0
    n_files_deleted = 0
    n_files_missing = 0
    missing_dirs = []

    for backbone in BACKBONES:
        for method in methods:
            for strategy in STRATEGIES:
                for seed in SEEDS:
                    cell_name = "{}_{}_{}".format(DATASET, backbone, RATIO_TAG)
                    leaf = "{}_{}".format(method, strategy)
                    cell = root / cell_name / leaf / "seed{}".format(seed)

                    if not cell.exists():
                        missing_dirs.append(str(cell))
                        continue

                    n_cells_seen += 1
                    deleted_here = False
                    for fname in CELL_OUTPUTS_TO_DELETE:
                        p = cell / fname
                        if p.exists():
                            if args.dry_run:
                                print("[DRY-RUN] would rm {}".format(p))
                            else:
                                p.unlink()
                            n_files_deleted += 1
                            deleted_here = True
                        else:
                            n_files_missing += 1
                    if deleted_here:
                        n_cells_clean += 1

    print()
    print("[summary]")
    print("  cells seen (dir exists)       : {} / {}".format(n_cells_seen, expected))
    print("  cells cleaned                 : {}".format(n_cells_clean))
    print("  files deleted                 : {}".format(n_files_deleted))
    print("  files already missing         : {}".format(n_files_missing))
    print("  dirs missing (cell never ran) : {}".format(len(missing_dirs)))
    if missing_dirs and len(missing_dirs) <= 5:
        for d in missing_dirs:
            print("    - {}".format(d))
    elif missing_dirs:
        for d in missing_dirs[:3]:
            print("    - {}".format(d))
        print("    - ... ({} more)".format(len(missing_dirs) - 3))

    if args.dry_run:
        print("\n[dry_run] no files deleted. Re-run without --dry_run to apply.")
        return 0

    if n_cells_clean == 0:
        print("\n[warn] no cells were cleaned. Either --root is wrong, or the cells weren't shipped yet.")
        return 1

    print("\n[next] kick experiments/run.py — incomplete cells will re-run, others skip:")
    print("  python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml")
    print("  python experiments/run.py experiments/configs/phase_b_cora_gat.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
