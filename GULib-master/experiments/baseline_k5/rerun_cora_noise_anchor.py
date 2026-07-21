"""Clean k=5 random-baseline rerun for the paper's Cora noise anchor.

The run starts from the canonical ``results/baseline/k5_random`` directory;
the pre-v2 evidence is preserved in ``k5_random_OLD_20260227``.  The formal
lane is deliberately staged: run the registered one-cell gate first, then
pass ``--resume`` to expand the same immutable gate into the full matrix.
It covers the entire Cora x {GCN, GAT} six-method scorecard,
uses five independent baseline seeds, and writes ``method_perf_before`` for
every retained cell.

Usage (on the formal GPU checkout):
    python experiments/baseline_k5/rerun_cora_noise_anchor.py --preflight-only
    python experiments/baseline_k5/rerun_cora_noise_anchor.py \
        --gate-only \
        --expected-git-sha <40-character-accepted-main-sha>
    python experiments/baseline_k5/rerun_cora_noise_anchor.py \
        --resume \
        --expected-git-sha <40-character-accepted-main-sha>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from .run_all_baselines import (
        BASELINE_K,
        BASELINE_ROOT,
        REPO_ROOT,
        SEEDS,
        compute_averaged_baseline,
        run_single_baseline,
    )
    from .baseline_contract import (
        BEFORE_METRIC,
        SCHEMA,
        SCHEMA_VERSION,
        expected_config,
        load_valid_record,
    )
    from .formal_preflight import build_formal_preflight, collect_git_provenance
except ImportError:
    from run_all_baselines import (
        BASELINE_K,
        BASELINE_ROOT,
        REPO_ROOT,
        SEEDS,
        compute_averaged_baseline,
        run_single_baseline,
    )
    from baseline_contract import (
        BEFORE_METRIC,
        SCHEMA,
        SCHEMA_VERSION,
        expected_config,
        load_valid_record,
    )
    from formal_preflight import build_formal_preflight, collect_git_provenance


DATASET = "cora"
BACKBONES = ("GCN", "GAT")
METHODS = ("GIF", "GNNDelete", "GraphEraser", "GraphRevoker", "IDEA", "MEGU")
GATE_SCHEMA = "opengu.k5_noise_anchor.gate"
GATE_SCHEMA_VERSION = 1
GATE_MANIFEST_NAME = "formal_one_cell_gate_manifest.json"
# The canary deliberately exercises the highest-risk shard/SISA before-metric
# path and GraphRevoker's method-specific partition configuration.
GATE_METHOD = "GraphRevoker"
GATE_BACKBONE = "GCN"
GATE_SEED = 111


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reuse only compatible v2 cells already present in the canonical root",
    )
    parser.add_argument(
        "--gate-only",
        action="store_true",
        help="run or validate only the registered one-cell formal gate",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="report formal readiness without creating artifacts or starting GPU work",
    )
    parser.add_argument(
        "--expected-git-sha",
        help="full accepted main SHA; required for an actual formal run",
    )
    return parser


def _git_provenance():
    repo_root = Path(__file__).resolve().parents[2]
    sha = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        text=True,
        encoding="utf-8",
    ).strip()
    dirty = bool(
        subprocess.check_output(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            text=True,
            encoding="utf-8",
        ).strip()
    )
    return {"git_sha": sha, "git_dirty": dirty}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gate_identity() -> dict:
    return {
        "dataset": DATASET,
        "backbone": GATE_BACKBONE,
        "method": GATE_METHOD,
        "seed": GATE_SEED,
        "baseline_k": BASELINE_K,
    }


def _gate_paths(result_root: Path | None = None) -> tuple[Path, Path]:
    root = Path(result_root) if result_root is not None else BASELINE_ROOT
    artifact = (
        root
        / GATE_METHOD
        / DATASET
        / GATE_BACKBONE
        / f"baseline_seed{GATE_SEED}_k{BASELINE_K}.json"
    )
    return artifact, root / GATE_MANIFEST_NAME


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)


def _validate_gate(preflight: dict, result_root: Path | None = None) -> dict:
    root = Path(result_root) if result_root is not None else BASELINE_ROOT
    artifact, manifest_path = _gate_paths(root)
    if not manifest_path.is_file():
        raise ValueError(f"formal one-cell gate manifest is missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("schema") != GATE_SCHEMA
        or manifest.get("schema_version") != GATE_SCHEMA_VERSION
        or manifest.get("kind") != "formal_one_cell_gate"
    ):
        raise ValueError("formal one-cell gate manifest has an incompatible schema")
    if manifest.get("gate") != gate_identity():
        raise ValueError("formal one-cell gate identity does not match the registered canary")

    expected_sha = preflight["git"]["git_sha"]
    if manifest.get("git_sha") != expected_sha:
        raise ValueError(
            f"formal one-cell gate SHA mismatch: {manifest.get('git_sha')} != {expected_sha}"
        )
    expected_fingerprint = preflight["dataset_source"]["source_fingerprint"]
    if manifest.get("dataset_source_fingerprint") != expected_fingerprint:
        raise ValueError("formal one-cell gate dataset fingerprint mismatch")

    expected_relative = artifact.relative_to(root).as_posix()
    artifact_meta = manifest.get("artifact") or {}
    if artifact_meta.get("relative_path") != expected_relative:
        raise ValueError("formal one-cell gate artifact path mismatch")
    if not artifact.is_file():
        raise ValueError(f"formal one-cell gate artifact is missing: {artifact}")
    observed_digest = _sha256_file(artifact)
    if artifact_meta.get("sha256") != observed_digest:
        raise ValueError("formal one-cell gate artifact digest mismatch")

    record = load_valid_record(
        artifact,
        expected_config(
            dataset=DATASET,
            model=GATE_BACKBONE,
            method=GATE_METHOD,
            seed=GATE_SEED,
            k=BASELINE_K,
        ),
    )
    record_config = record.get("config") or {}
    if record_config.get("git_sha") != expected_sha:
        raise ValueError("formal one-cell gate artifact was produced by a different SHA")
    if record_config.get("git_dirty") is not False:
        raise ValueError("formal one-cell gate artifact was produced from a dirty checkout")
    return manifest


def _run_gate(preflight: dict, result_root: Path | None = None) -> int:
    root = Path(result_root) if result_root is not None else BASELINE_ROOT
    artifact, manifest_path = _gate_paths(root)
    if manifest_path.exists():
        try:
            _validate_gate(preflight, root)
        except Exception as exc:
            print(f"Refusing incompatible formal one-cell gate: {exc}")
            return 2
        print(f"Validated existing formal one-cell gate: {manifest_path}")
        return 0

    ok = run_single_baseline(
        GATE_METHOD,
        DATASET,
        GATE_BACKBONE,
        GATE_SEED,
        BASELINE_K,
    )
    if not ok:
        print("Formal one-cell gate failed; full matrix remains blocked")
        return 1

    try:
        record = load_valid_record(
            artifact,
            expected_config(
                dataset=DATASET,
                model=GATE_BACKBONE,
                method=GATE_METHOD,
                seed=GATE_SEED,
                k=BASELINE_K,
            ),
        )
        expected_sha = preflight["git"]["git_sha"]
        record_config = record.get("config") or {}
        if record_config.get("git_sha") != expected_sha:
            raise ValueError("gate artifact Git SHA does not match formal preflight")
        if record_config.get("git_dirty") is not False:
            raise ValueError("gate artifact records a dirty checkout")
        final_git = collect_git_provenance(REPO_ROOT)
        if (
            final_git["git_sha"] != expected_sha
            or final_git["branch"] != "main"
            or final_git["dirty"]
        ):
            raise ValueError("Git provenance changed or became dirty during the gate")
        payload = {
            "schema": GATE_SCHEMA,
            "schema_version": GATE_SCHEMA_VERSION,
            "kind": "formal_one_cell_gate",
            "completed_at": datetime.now().isoformat(),
            "git_sha": expected_sha,
            "dataset_source_fingerprint": preflight["dataset_source"][
                "source_fingerprint"
            ],
            "gate": gate_identity(),
            "artifact": {
                "relative_path": artifact.relative_to(root).as_posix(),
                "sha256": _sha256_file(artifact),
            },
            "formal_preflight": preflight,
            "final_git": final_git,
        }
        _write_json_atomic(manifest_path, payload)
        _validate_gate(preflight, root)
    except Exception as exc:
        print(f"Formal one-cell gate validation failed: {exc}")
        return 1

    print(f"Formal one-cell gate PASS: {gate_identity()}")
    print(f"Gate manifest: {manifest_path}")
    print("Next step: rerun this entrypoint with --resume and the same full SHA")
    return 0


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    if not args.preflight_only and not args.expected_git_sha:
        print("Refusing formal run without --expected-git-sha <40-character SHA>")
        return 2
    preflight = build_formal_preflight(
        REPO_ROOT,
        expected_git_sha=args.expected_git_sha,
        dataset=DATASET,
    )
    print(json.dumps(preflight, indent=2))
    if not preflight["ready"]:
        return 2
    if args.preflight_only:
        return 0

    existing = (
        list(BASELINE_ROOT.rglob("*.json")) if BASELINE_ROOT.exists() else []
    )
    gate_artifact, gate_manifest_path = _gate_paths()
    if args.gate_only:
        allowed_gate_files = {gate_artifact.resolve(), gate_manifest_path.resolve()}
        unexpected = [
            path for path in existing if path.resolve() not in allowed_gate_files
        ]
        if unexpected:
            print("Refusing gate run with unrelated JSON artifacts in canonical root:")
            for path in unexpected[:20]:
                print(f"  {path}")
            return 2
        if existing and not args.resume:
            print(
                f"Refusing non-empty gate root ({len(existing)} JSON files): "
                f"{BASELINE_ROOT}"
            )
            print("Use --gate-only --resume only after an interrupted gate.")
            return 2
        return _run_gate(preflight)

    if not args.resume:
        print("Refusing full K5 matrix before the registered formal one-cell gate")
        print(
            "Run --gate-only first; after it passes, rerun with --resume and "
            "the same full SHA."
        )
        return 2
    try:
        gate_manifest = _validate_gate(preflight)
    except Exception as exc:
        print(f"Refusing full K5 matrix: {exc}")
        return 2

    if not existing:
        print(
            "Refusing full K5 matrix because the canonical result root is empty "
            "after gate validation"
        )
        return 2

    summary = []
    failures = []
    total = len(BACKBONES) * len(METHODS) * len(SEEDS)
    position = 0

    print(f"Clean k={BASELINE_K} Cora noise-anchor rerun: {total} cells")
    for backbone in BACKBONES:
        for method in METHODS:
            successes = 0
            for seed in SEEDS:
                position += 1
                ok = run_single_baseline(method, DATASET, backbone, seed, BASELINE_K)
                print(f"[{position}/{total}] {method}/{backbone}/seed{seed}: {'OK' if ok else 'FAIL'}")
                if ok:
                    successes += 1
                else:
                    failures.append(f"{method}/{backbone}/seed{seed}")

            averaged = compute_averaged_baseline(method, DATASET, backbone, BASELINE_K)
            has_anchor = averaged is not None and averaged.get("method_perf_before") is not None
            summary.append({
                "method": method,
                "backbone": backbone,
                "seeds_ok": successes,
                "method_perf_before": averaged.get("method_perf_before") if averaged else None,
                "method_noise_drop": averaged.get("method_noise_drop") if averaged else None,
                "anchor_present": has_anchor,
            })
            if successes != len(SEEDS) or not has_anchor:
                failures.append(f"{method}/{backbone}: incomplete aggregate or missing method_perf_before")

    BASELINE_ROOT.mkdir(parents=True, exist_ok=True)
    final_git = collect_git_provenance(REPO_ROOT)
    if (
        final_git["git_sha"] != preflight["git"]["git_sha"]
        or final_git["branch"] != "main"
        or final_git["dirty"]
    ):
        failures.append("Git provenance changed or became dirty during the run")

    manifest = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "kind": "clean_cora_k5_noise_anchor",
        "timestamp": datetime.now().isoformat(),
        "dataset": DATASET,
        "backbones": list(BACKBONES),
        "methods": list(METHODS),
        "seeds": list(SEEDS),
        "baseline_k": BASELINE_K,
        "before_metric": BEFORE_METRIC,
        "result_root": str(BASELINE_ROOT.resolve()),
        "formal_preflight": preflight,
        "formal_one_cell_gate": gate_manifest,
        "final_git": final_git,
        **_git_provenance(),
        "summary": summary,
        "failures": failures,
    }
    path = BASELINE_ROOT / "clean_cora_noise_anchor_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest: {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
