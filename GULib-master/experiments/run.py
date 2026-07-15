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

Skip-if-complete by default. A cell is "complete" iff:
    1. All 4 files exist (attack.json, collateral.json, predictions.npz, _meta.json)
    2. Each file parses (no truncation from interrupted runs)
    3. _meta.json contains config_fingerprint matching the current yaml + matrix coords

Cells that fail (2) — corrupt — or (3) — stale — are silently re-run.
Cells written before fingerprinting (legacy) print a warning and skip; pass
--force or `rm -rf` the cell to regenerate them. Use --force to re-run any cell.

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
        run_update_detection_auc: <bool>  # default true; false skips optional AUC
        no_cache: <bool>              # default false (use cache)
        num_epochs: <int>             # default 100
        batch_size: <int>             # default 64
        cuda: <int>                   # default 0
    extra_args: [<str>, ...]          # passed verbatim to demo_attack and eval_collateral
    method_overrides:                 # injected only for matching method
        GraphRevoker:
            extra_args: ["--partition_method", "gpa"]
    model_overrides:                  # injected as extra_args; per-model knobs
        GCN:
            gcn_num_layers: 3
            gcn_hidden: 256
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

_MODULE_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_MODULE_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_MODULE_REPO_ROOT))

from scripts.evaluation.reporting.events import (
    ENV_ATTEMPT,
    ENV_CELL_ID,
    ENV_CONFIG_FINGERPRINT,
    ENV_GIT_SHA,
    ENV_IDENTITY_JSON,
    ENV_RUN_ID,
    artifact_ref,
    cache_observation,
    event_path_from_env,
    make_cell_id,
    new_run_id,
    prior_attempt_context,
    record_event,
)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. `pip install pyyaml` (or via the gnn env).", file=sys.stderr)
    raise


REPO_ROOT = _MODULE_REPO_ROOT


def _report_identity(cfg: Dict[str, Any], method: str, strategy: str, seed: int) -> Dict[str, Any]:
    return {
        "dataset": cfg["dataset"],
        "model": cfg["base_model"],
        "method": method,
        "strategy": strategy,
        "ratio": cfg["ratio"],
        "seed": int(seed),
        "k": None,
    }


def _existing_artifact_refs(out_dir: Path) -> List[Dict[str, Any]]:
    refs = []
    for name, artifact_type in (
        ("attack.json", "evaluation"),
        ("collateral.json", "evaluation"),
        ("predictions.npz", "prediction"),
        ("_meta.json", "artifact"),
    ):
        path = out_dir / name
        if path.exists():
            stat = path.stat()
            content_hash = None
            # JSON/meta leaves are small enough to hash on a skip check. Large
            # prediction bundles use size+mtime as a cheap change detector.
            if path.suffix == ".json":
                content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            refs.append(artifact_ref(
                path=str(path),
                artifact_type=artifact_type,
                content_hash=content_hash,
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
            ))
    return refs


def _record_autoreport_event(**kwargs):
    """Keep audit failures visible without discarding completed experiments."""
    try:
        return record_event(**kwargs)
    except Exception as exc:
        print("[AutoReport V3] warning: {0}".format(exc), file=sys.stderr)
        return None


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


def _hybrid_alpha_from_cfg(cfg: Dict[str, Any]) -> Optional[float]:
    """Extract hybrid_alpha from cfg if explicitly set.

    Reads top-level `hybrid_alpha:` first, then falls back to scanning
    `extra_args` for `--hybrid_alpha <val>`. Returns None if absent.
    """
    if "hybrid_alpha" in cfg:
        try:
            return float(cfg["hybrid_alpha"])
        except (TypeError, ValueError):
            return None
    extras = cfg.get("extra_args", []) or []
    for i, tok in enumerate(extras):
        if tok == "--hybrid_alpha" and i + 1 < len(extras):
            try:
                return float(extras[i + 1])
            except (TypeError, ValueError):
                return None
    return None


def method_overrides(cfg: Dict[str, Any], method: str) -> List[str]:
    """Extract method-specific extra CLI args as a flat list."""
    override = (cfg.get("method_overrides", {}) or {}).get(method, {}) or {}
    return list(override.get("extra_args", []) or [])


def cell_dir(cfg: Dict[str, Any], method: str, strategy: str, seed: int) -> Path:
    cell = f"{cfg['dataset']}_{cfg['base_model']}_r{cfg['ratio']}"
    leaf = f"{method}_{strategy}"
    # A3 alpha sweep: when an explicit non-default hybrid_alpha is set,
    # suffix the leaf so different alphas don't overwrite each other's
    # attack.json. Default alpha=0.5 stays under the bare "hybrid" leaf
    # so it can share data with the main matrix's hybrid cells.
    if strategy == "hybrid":
        alpha = _hybrid_alpha_from_cfg(cfg)
        if alpha is not None and abs(alpha - 0.5) > 1e-9:
            leaf = f"{method}_{strategy}_alpha{alpha:.2f}"
    return REPO_ROOT / "results" / "runs" / cell / leaf / f"seed{seed}"


# Bump when the set of fields hashed in _content_fingerprint changes,
# so old fingerprints stop matching and force a clean re-run.
_FINGERPRINT_VERSION = "v2-cache-selection"


def _content_fingerprint(cfg: Dict[str, Any], method: str, strategy: str, seed: int) -> str:
    """Stable hash of every cfg field that meaningfully changes a cell's outputs.

    Excludes `cuda` (different GPU = same outputs modulo fp determinism) so
    swapping devices doesn't trigger spurious re-runs.
    """
    defaults = dict(cfg.get("defaults", {}) or {})
    defaults.pop("cuda", None)
    method_extra = method_overrides(cfg, method)
    payload = {
        "_v": _FINGERPRINT_VERSION,
        "dataset": cfg["dataset"],
        "base_model": cfg["base_model"],
        "ratio": cfg["ratio"],
        "method": method,
        "strategy": strategy,
        "seed": seed,
        "defaults": defaults,
        "extra_args": list(cfg.get("extra_args", []) or []),
        "model_overrides": (cfg.get("model_overrides", {}) or {}).get(cfg["base_model"], {}) or {},
        "cache_v2": cfg.get("cache_v2"),
    }
    if method_extra:
        payload["method_overrides"] = method_extra
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _check_json(path: Path) -> Optional[str]:
    if not path.exists():
        return f"missing {path.name}"
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return f"empty {path.name}"
        data = json.loads(text)
        if not isinstance(data, dict) or not data:
            return f"empty-dict {path.name}"
    except (OSError, ValueError, json.JSONDecodeError) as e:
        return f"corrupt {path.name}: {type(e).__name__}"
    return None


def _check_attack_json(path: Path, expected_strategy: Optional[str] = None) -> Optional[str]:
    error = _check_json(path)
    if error is not None:
        return error
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return f"corrupt {path.name}: {type(exc).__name__}"
    results = data.get("results")
    if not isinstance(results, dict) or not results:
        return f"no-results {path.name}"
    if expected_strategy is not None:
        result = results.get(expected_strategy)
        if not isinstance(result, dict):
            return f"missing-strategy {expected_strategy} in {path.name}"
        if result.get("failed") is True:
            return f"failed-strategy {expected_strategy} in {path.name}"
    return None


def _check_npz(path: Path) -> Optional[str]:
    if not path.exists():
        return f"missing {path.name}"
    try:
        import numpy as np
        with np.load(path) as z:
            if not z.files:
                return f"empty-npz {path.name}"
    except Exception as e:
        return f"corrupt {path.name}: {type(e).__name__}"
    return None


def cell_status(
    d: Path,
    expected_fp: str,
    want_collateral: bool,
    expected_strategy: Optional[str] = None,
) -> Tuple[str, str]:
    """Classify a cell directory.

    Returns (kind, reason). kind ∈ {complete, incomplete, corrupt, stale, legacy}.
        complete   — all files valid, fingerprint matches → skip
        incomplete — file(s) missing → re-run
        corrupt    — file present but unparseable / truncated → re-run
        stale      — fingerprint mismatch (config or fix changed) → re-run
        legacy     — _meta.json has no config_fingerprint (pre-2026-05-06 cell)
                     → skip with warning; user must --force to regenerate
    """
    if not d.exists():
        return "incomplete", "dir missing"

    attack_error = _check_attack_json(d / "attack.json", expected_strategy)
    if attack_error is not None:
        return (
            "incomplete" if attack_error.startswith("missing") else "corrupt",
            attack_error,
        )

    required_jsons = ["_meta.json"]
    if want_collateral:
        required_jsons.append("collateral.json")
    for name in required_jsons:
        r = _check_json(d / name)
        if r is not None:
            return ("incomplete" if r.startswith("missing") else "corrupt"), r

    if want_collateral:
        r = _check_npz(d / "predictions.npz")
        if r is not None:
            return ("incomplete" if r.startswith("missing") else "corrupt"), r

    try:
        meta = json.loads((d / "_meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        return "corrupt", f"meta parse: {type(e).__name__}"

    actual_fp = meta.get("config_fingerprint")
    if actual_fp is None:
        return "legacy", "no config_fingerprint (pre-2026-05-06 cell)"
    if actual_fp != expected_fp:
        return "stale", f"fingerprint {actual_fp} != {expected_fp}"
    return "complete", ""


def model_overrides(cfg: Dict[str, Any]) -> List[str]:
    """Extract per-model overrides as a flat list of CLI flags."""
    overrides = (cfg.get("model_overrides", {}) or {}).get(cfg["base_model"], {}) or {}
    out: List[str] = []
    for k, v in overrides.items():
        out.extend([f"--{k}", str(v)])
    return out


CACHE_V2_RUNNER_STRATEGIES = frozenset({"random", "degree", "pagerank", "im"})


def _repo_path(value: Any) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def cache_v2_settings(cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    raw = cfg.get("cache_v2")
    if raw is None:
        return None
    if not isinstance(raw, dict) or raw.get("mode") != "selection":
        raise ValueError("cache_v2.mode must be 'selection'")
    unsupported = sorted(set(cfg.get("strategies") or []) - CACHE_V2_RUNNER_STRATEGIES)
    if unsupported:
        raise ValueError(
            "Cache V2 runner has no producer for: {0}".format(",".join(unsupported))
        )
    return {
        "mode": "selection",
        "store_root": _repo_path(raw.get("store_root", "results/cache_v2")),
        "dataset_root": _repo_path(raw.get("dataset_root", "data/raw")),
        "legacy_results_root": _repo_path(
            raw.get("legacy_results_root", "results")
        ),
        "allow_download": bool(raw.get("allow_download", False)),
    }


def prepare_cache_v2_selection(
    cfg: Dict[str, Any], *, dry_run: bool
) -> Tuple[Dict[Tuple[str, int], Dict[str, Any]], Dict[str, Any]]:
    settings = cache_v2_settings(cfg)
    if settings is None:
        return {}, {}
    config_path = cfg.get("_source_path")
    if not config_path:
        raise ValueError("Cache V2 runner requires cfg._source_path")
    from cache_v2.selection_materializer import materialize_selection, plan_selection

    common = {
        "config_path": _repo_path(config_path),
        "dataset_root": settings["dataset_root"],
        "store_root": settings["store_root"],
        "legacy_results_root": settings["legacy_results_root"],
        "allow_download": settings["allow_download"],
    }
    if dry_run:
        document = plan_selection(**common)
    else:
        document = materialize_selection(
            **common,
            verify=True,
            fail_if_producer_called=False,
            compare_legacy=False,
            include_nodes=False,
        )
    plan = document.get("plan") or {}
    skipped = plan.get("skipped") or []
    if skipped:
        names = sorted({str(item.get("strategy")) for item in skipped})
        raise ValueError(
            "Cache V2 Selection plan is incomplete: {0}".format(",".join(names))
        )
    if dry_run:
        return {}, document

    jobs = {item["recipe_hash"]: item for item in plan.get("jobs") or []}
    results = {item["recipe_hash"]: item for item in document.get("results") or []}
    if not jobs or set(jobs) != set(results):
        raise ValueError("Cache V2 materialization did not cover every planned Recipe")
    mapping: Dict[Tuple[str, int], Dict[str, Any]] = {}
    for recipe_hash, job in jobs.items():
        result = results[recipe_hash]
        artifact = {
            "store_root": str(settings["store_root"]),
            "artifact_id": result["artifact_id"],
            "artifact_type": "selection",
            "recipe_hash": recipe_hash,
            "content_hash": result["content_hash"],
            "source_file": result["payload_path"],
            "hit_source": "cache_v2:{0}".format(result["artifact_id"]),
            "lookup_policy": "cache_v2_exact_artifact_id",
            "authoritative": True,
            "write_outcome": "reused" if result.get("hit") else "saved",
            "strategy": job["strategy"],
            "k": int(job["k"]),
            "selected_node_count": int(result["selected_node_count"]),
        }
        seeds = (job.get("request_envelope") or {}).get("experiment_seeds") or []
        for seed in seeds:
            key = (str(job["strategy"]), int(seed))
            if key in mapping and mapping[key]["artifact_id"] != artifact["artifact_id"]:
                raise ValueError("Cache V2 consumer mapping is ambiguous: {0}".format(key))
            mapping[key] = dict(artifact)
    expected = {
        (str(strategy), int(seed))
        for strategy in cfg["strategies"]
        for seed in cfg["seeds"]
    }
    if set(mapping) != expected:
        missing = sorted(expected - set(mapping))
        raise ValueError("Cache V2 consumer mapping is incomplete: {0}".format(missing))
    return mapping, document


def _selection_cache_observation(artifact: Mapping[str, Any]) -> Dict[str, Any]:
    return cache_observation(
        cache_type="selection",
        outcome="hit",
        recipe={"strategy": artifact["strategy"], "k": int(artifact["k"])},
        recipe_hash=artifact["recipe_hash"],
        artifact=artifact_ref(
            path=artifact["source_file"],
            artifact_id=artifact["artifact_id"],
            artifact_type="selection",
            recipe_hash=artifact["recipe_hash"],
            content_hash=artifact["content_hash"],
        ),
        hit_source=artifact["hit_source"],
        lookup_policy=artifact["lookup_policy"],
        authoritative=True,
        write_outcome=artifact["write_outcome"],
    )


def run_cell(cfg: Dict[str, Any], method: str, strategy: str, seed: int,
             *, force: bool, dry_run: bool,
             selection_artifact: Optional[Mapping[str, Any]] = None) -> str:
    out_dir = cell_dir(cfg, method, strategy, seed)
    expected_fp = _content_fingerprint(cfg, method, strategy, seed)
    want_collateral = bool((cfg.get("defaults") or {}).get("run_collateral", True))
    status, reason = cell_status(
        out_dir, expected_fp, want_collateral, expected_strategy=strategy
    )
    identity = _report_identity(cfg, method, strategy, seed)
    cell_id = make_cell_id(identity)
    git_sha = _git_sha()
    report_event_path = event_path_from_env()
    v2_mode = cache_v2_settings(cfg) is not None
    if v2_mode and not dry_run and selection_artifact is None:
        raise ValueError("Cache V2 runner cell has no Selection Artifact")

    if not force:
        if status == "complete":
            if not dry_run:
                _record_autoreport_event(
                    identity=identity,
                    stage="run",
                    state="skipped",
                    producer="experiments/run.py",
                    config_fingerprint=expected_fp,
                    git_sha=git_sha,
                    cell_id=cell_id,
                    run_id=new_run_id(cell_id),
                    attempt=1,
                    cache=[cache_observation(
                        cache_type="run_artifact",
                        outcome="hit",
                        recipe={"config_fingerprint": expected_fp},
                        artifact=artifact_ref(path=str(out_dir), artifact_type="artifact"),
                        hit_source=str(out_dir),
                        lookup_policy="complete_files_and_fingerprint",
                        authoritative=True,
                        write_outcome="reused",
                    )],
                    artifacts=_existing_artifact_refs(out_dir),
                    metadata={"reason": "complete cell already materialized"},
                    event_path=report_event_path,
                )
            return "skipped"
        if status == "legacy":
            print(
                f"[run] LEGACY {out_dir.relative_to(REPO_ROOT)} — "
                f"no fingerprint; skipping. Pass --force or rm to regenerate."
            )
            if not dry_run:
                _record_autoreport_event(
                    identity=identity,
                    stage="run",
                    state="skipped",
                    producer="experiments/run.py",
                    config_fingerprint=expected_fp,
                    git_sha=git_sha,
                    cell_id=cell_id,
                    run_id=new_run_id(cell_id),
                    attempt=1,
                    cache=[cache_observation(
                        cache_type="run_artifact",
                        outcome="hit",
                        recipe={"config_fingerprint": None},
                        artifact=artifact_ref(path=str(out_dir), artifact_type="artifact"),
                        hit_source=str(out_dir),
                        lookup_policy="legacy_files_without_fingerprint",
                        authoritative=False,
                        write_outcome="reused",
                    )],
                    artifacts=_existing_artifact_refs(out_dir),
                    metadata={"reason": "legacy cell skipped: {0}".format(reason)},
                    event_path=report_event_path,
                )
            return "skipped_legacy"
        if status in ("corrupt", "stale"):
            print(
                f"[run] {status.upper()} {out_dir.relative_to(REPO_ROOT)}: {reason} "
                f"— regenerating"
            )
        # status == "incomplete" silently falls through (first run / partial dir)

    if dry_run:
        return "would_run"

    out_dir.mkdir(parents=True, exist_ok=True)
    attempt, prior_failed_run_id = prior_attempt_context(
        cell_id, expected_fp, event_path=report_event_path
    )
    run_id = new_run_id(cell_id)
    retry = {
        "attempt": attempt,
        "retry_of": prior_failed_run_id,
    }
    if prior_failed_run_id:
        _record_autoreport_event(
            identity=identity,
            stage="run",
            state="retrying",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            retry=retry,
            metadata={"reason": reason or "retry after failed run"},
            event_path=report_event_path,
        )
    expected_stages = (["selection"] if v2_mode else []) + ["attack"] + (["collateral"] if want_collateral else [])
    _record_autoreport_event(
        identity=identity,
        stage="run",
        state="started",
        producer="experiments/run.py",
        config_fingerprint=expected_fp,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        retry=retry,
        metadata={
            "expected_stages": expected_stages,
            "pre_run_cell_status": status,
            "reason": reason,
            "forced": bool(force),
        },
        event_path=report_event_path,
    )

    child_env = os.environ.copy()
    child_env.update({
        ENV_CELL_ID: cell_id,
        ENV_RUN_ID: run_id,
        ENV_ATTEMPT: str(attempt),
        ENV_CONFIG_FINGERPRINT: expected_fp,
        ENV_GIT_SHA: git_sha,
        ENV_IDENTITY_JSON: json.dumps(identity, sort_keys=True, separators=(",", ":")),
        "OPENGU_AUTOREPORT_EVENT_PATH": str(report_event_path),
    })
    py = _python_bin()
    defaults = cfg.get("defaults", {}) or {}
    run_update_detection_auc = defaults.get("run_update_detection_auc", True)
    if not isinstance(run_update_detection_auc, bool):
        raise ValueError("defaults.run_update_detection_auc must be a YAML boolean")
    extra = list(cfg.get("extra_args", []) or [])
    extra += method_overrides(cfg, method)
    extra += model_overrides(cfg)
    # A3: if yaml uses top-level `hybrid_alpha:` and didn't already inject
    # --hybrid_alpha via extra_args, plumb it through so demo_attack and
    # eval_collateral see the right fusion weight at runtime.
    if strategy == "hybrid" and "hybrid_alpha" in cfg and not any(
        tok == "--hybrid_alpha" for tok in extra
    ):
        extra += ["--hybrid_alpha", str(cfg["hybrid_alpha"])]

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
        "--run_update_detection_auc", str(run_update_detection_auc),
    ]
    if defaults.get("no_cache", False):
        cmd1.append("--no_cache")
    if v2_mode:
        if "--no_cache" not in cmd1:
            cmd1.append("--no_cache")
        cmd1 += [
            "--cache_v2_store_root", str(selection_artifact["store_root"]),
            "--selection_artifact_id", str(selection_artifact["artifact_id"]),
        ]
    cmd1 += extra
    print(f"\n[run] demo_attack {method}/{strategy}/seed{seed} → {out_dir.relative_to(REPO_ROOT)}")
    if v2_mode:
        _record_autoreport_event(
            identity=identity,
            stage="selection",
            state="completed",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            cache=[_selection_cache_observation(selection_artifact)],
            metrics={
                "selected_node_count": selection_artifact["selected_node_count"]
            },
            metadata={"stage_execution": "cache_reuse"},
            event_path=report_event_path,
        )
    _record_autoreport_event(
        identity=identity,
        stage="attack",
        state="started",
        producer="experiments/run.py",
        config_fingerprint=expected_fp,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        event_path=report_event_path,
    )
    rc = subprocess.run(cmd1, cwd=str(REPO_ROOT), env=child_env).returncode
    error = None
    if rc != 0:
        print(f"[FAIL] demo_attack rc={rc} for {out_dir}", file=sys.stderr)
        error = {
            "type": "SUBPROCESS_EXIT",
            "message": "demo_attack.py exited with rc={0}".format(rc),
            "returncode": rc,
            "retryable": True,
        }
    else:
        artifact_error = _check_attack_json(out_dir / "attack.json", strategy)
        if artifact_error is not None:
            print(
                f"[FAIL] invalid attack artifact for {out_dir}: {artifact_error}",
                file=sys.stderr,
            )
            error = {
                "type": "INVALID_ATTACK_ARTIFACT",
                "message": artifact_error,
                "retryable": True,
            }
    if error is not None:
        _record_autoreport_event(
            identity=identity,
            stage="attack",
            state="failed",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            error=error,
            retry=retry,
            event_path=report_event_path,
        )
        _record_autoreport_event(
            identity=identity,
            stage="run",
            state="failed",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            error=error,
            retry=retry,
            event_path=report_event_path,
        )
        return "failed_attack"
    _record_autoreport_event(
        identity=identity,
        stage="attack",
        state="completed",
        producer="experiments/run.py",
        config_fingerprint=expected_fp,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        cache=[cache_observation(
            cache_type="result",
            outcome="unknown",
            recipe={"strategy": strategy},
            lookup_policy="producer_not_observed",
            authoritative=False,
            write_outcome="saved" if (out_dir / "attack.json").exists() else "unknown",
        )],
        artifacts=[artifact_ref(path=str(out_dir / "attack.json"), artifact_type="evaluation")],
        event_path=report_event_path,
    )

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
            "--num_epochs", str(defaults.get("num_epochs", 100)),
            "--batch_size", str(defaults.get("batch_size", 64)),
            "--cuda", str(defaults.get("cuda", 0)),
            "--run_update_detection_auc", str(run_update_detection_auc),
        ]
        if defaults.get("save_predictions", True):
            cmd2.append("--save_predictions")
        if v2_mode:
            cmd2 += [
                "--cache_v2_store_root", str(selection_artifact["store_root"]),
                "--selection_artifact_id", str(selection_artifact["artifact_id"]),
            ]
        cmd2 += extra
        print(f"[run] eval_collateral {method}/{strategy}/seed{seed}")
        _record_autoreport_event(
            identity=identity,
            stage="collateral",
            state="started",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            event_path=report_event_path,
        )
        rc = subprocess.run(cmd2, cwd=str(REPO_ROOT), env=child_env).returncode
        if rc != 0:
            print(f"[FAIL] eval_collateral rc={rc} for {out_dir}", file=sys.stderr)
            error = {
                "type": "SUBPROCESS_EXIT",
                "message": "eval_collateral.py exited with rc={0}".format(rc),
                "returncode": rc,
                "retryable": True,
            }
            _record_autoreport_event(
                identity=identity,
                stage="collateral",
                state="failed",
                producer="experiments/run.py",
                config_fingerprint=expected_fp,
                git_sha=git_sha,
                cell_id=cell_id,
                run_id=run_id,
                attempt=attempt,
                error=error,
                retry=retry,
                event_path=report_event_path,
            )
            _record_autoreport_event(
                identity=identity,
                stage="run",
                state="failed",
                producer="experiments/run.py",
                config_fingerprint=expected_fp,
                git_sha=git_sha,
                cell_id=cell_id,
                run_id=run_id,
                attempt=attempt,
                error=error,
                retry=retry,
                event_path=report_event_path,
            )
            return "failed_collateral"
        _record_autoreport_event(
            identity=identity,
            stage="collateral",
            state="completed",
            producer="experiments/run.py",
            config_fingerprint=expected_fp,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            cache=(
                [_selection_cache_observation(selection_artifact)]
                if v2_mode
                else [cache_observation(
                    cache_type="result",
                    outcome="unknown",
                    recipe={"strategy": strategy},
                    lookup_policy="producer_not_observed",
                    authoritative=False,
                    write_outcome="reused",
                )]
            ),
            artifacts=[artifact_ref(path=str(out_dir / "collateral.json"), artifact_type="evaluation")],
            event_path=report_event_path,
        )

    # 3) _meta.json — audit trail + skip-decision fingerprint
    meta = {
        "config_name": cfg.get("name", "unnamed"),
        "config": {k: v for k, v in cfg.items() if k != "_source_path"},
        "method": method,
        "strategy": strategy,
        "seed": seed,
        "timestamp": datetime.now().isoformat(),
        "git_sha": git_sha,
        "hostname": socket.gethostname(),
        "python": py,
        "config_fingerprint": expected_fp,
        "fingerprint_version": _FINGERPRINT_VERSION,
        "selection_artifact": dict(selection_artifact) if v2_mode else None,
        "metric_policy": {
            "update_detection_auc": {
                "enabled": run_update_detection_auc,
                "status": "computed" if run_update_detection_auc else "disabled_by_config",
            }
        },
    }
    (out_dir / "_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    _record_autoreport_event(
        identity=identity,
        stage="run",
        state="completed",
        producer="experiments/run.py",
        config_fingerprint=expected_fp,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        artifacts=_existing_artifact_refs(out_dir),
        retry=retry,
        metadata={"expected_stages": expected_stages},
        event_path=report_event_path,
    )
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
    ap.add_argument(
        "--cache-v2-dataset-root",
        type=Path,
        default=None,
        help="machine-local processed dataset root for an explicit cache_v2 config",
    )
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.cache_v2_dataset_root is not None:
        if not isinstance(cfg.get("cache_v2"), dict):
            raise SystemExit("--cache-v2-dataset-root requires cache_v2.mode=selection")
        cfg["cache_v2"] = dict(cfg["cache_v2"])
        cfg["cache_v2"]["dataset_root"] = str(args.cache_v2_dataset_root)
    selection_map, selection_document = prepare_cache_v2_selection(
        cfg, dry_run=args.dry_run
    )
    print(f"=== Loaded {args.config.name} ===")
    print(f"  cell: {cfg['dataset']}_{cfg['base_model']}_r{cfg['ratio']}")
    print(f"  methods × strategies × seeds = {len(cfg['methods'])} × {len(cfg['strategies'])} × {len(cfg['seeds'])}")
    print(f"  total cells: {len(cfg['methods']) * len(cfg['strategies']) * len(cfg['seeds'])}")
    if cfg.get("model_overrides", {}).get(cfg["base_model"]):
        print(f"  model_overrides: {cfg['model_overrides'][cfg['base_model']]}")
    if cfg.get("cache_v2"):
        print(
            "  cache_v2: selection "
            f"({selection_document.get('mode')}, writes={len(selection_document.get('writes') or [])})"
        )

    counters: Dict[str, int] = {"completed": 0, "skipped": 0, "skipped_legacy": 0,
                                 "would_run": 0, "failed_attack": 0, "failed_collateral": 0}
    t0 = time.time()
    for idx, (method, strategy, seed) in enumerate(expand_matrix(cfg)):
        if args.limit is not None and idx >= args.limit:
            break
        status = run_cell(
            cfg,
            method,
            strategy,
            seed,
            force=args.force,
            dry_run=args.dry_run,
            selection_artifact=selection_map.get((str(strategy), int(seed))),
        )
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
