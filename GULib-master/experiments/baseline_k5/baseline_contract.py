"""Versioned contracts for the method-specific k=5 noise anchor."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping, Tuple


SCHEMA = "opengu.k5_noise_anchor"
SCHEMA_VERSION = 2
RESULT_ROOT_NAME = "k5_random"
LEGACY_ARCHIVE_ROOT_NAME = "k5_random_OLD_20260227"
SHARD_METHODS = frozenset({"GraphEraser", "GraphRevoker"})


def default_result_root(repo_root: Path) -> Path:
    """Return the canonical K5 path after the pre-v2 evidence is archived."""
    return Path(repo_root) / "results" / "baseline" / RESULT_ROOT_NAME


def legacy_archive_root(repo_root: Path) -> Path:
    """Return the immutable location of the 2026-02-26/27 legacy artifacts."""
    return Path(repo_root) / "results" / "baseline" / LEGACY_ARCHIVE_ROOT_NAME


def finite_f1(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{label} must be finite and within [0, 1]")
    return result


def measure_method_perf_before(pipeline: Any, method_name: str) -> Tuple[float, str]:
    """Train once and return the method-native pre-unlearning test F1.

    Partition methods expose their real shard/SISA evaluation through
    ``aggregate_f1_score``.  Evaluating ``model_zoo.model`` would instead read
    one ordinary module and is not an equivalent aggregate.
    """
    pipeline._ensure_base_model_trained()
    if str(method_name) in SHARD_METHODS:
        value = getattr(pipeline.method, "aggregate_f1_score", None)
        return finite_f1(value, f"{method_name}.aggregate_f1_score"), "shard_aggregate_f1"

    trained_model = pipeline._get_trained_model()
    value = pipeline._evaluate_model(trained_model)
    return finite_f1(value, f"{method_name}.trained_model_f1"), "trained_model_test_f1"


def validate_run_result(result: Mapping[str, Any], expected_k: int) -> float:
    if bool(result.get("failed")):
        reason = result.get("failure_reason") or "unlearning reported failure"
        raise RuntimeError(str(reason))
    selected = result.get("selected_nodes")
    if selected is None or len(selected) != int(expected_k):
        raise ValueError(
            f"selected_nodes must contain exactly {int(expected_k)} nodes"
        )
    return finite_f1(result.get("f1_after"), "f1_after")


def expected_config(
    *, dataset: str, model: str, method: str, seed: int, k: int
) -> Mapping[str, Any]:
    return {
        "dataset_name": str(dataset),
        "base_model": str(model),
        "unlearning_methods": str(method),
        "seed": int(seed),
        "k": int(k),
        "strategy": "random",
    }


def validate_record(
    record: Mapping[str, Any], expected: Mapping[str, Any]
) -> Mapping[str, Any]:
    if record.get("schema") != SCHEMA or record.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("record is not a k5 noise-anchor v2 artifact")
    config = record.get("config")
    if not isinstance(config, dict):
        raise ValueError("record config is missing")
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(
                f"record config mismatch for {key}: {config.get(key)!r} != {value!r}"
            )
    f1_after = finite_f1(record.get("f1_after"), "record.f1_after")
    method_before = finite_f1(
        record.get("method_perf_before"), "record.method_perf_before"
    )
    noise_drop = record.get("method_noise_drop")
    if isinstance(noise_drop, bool) or not isinstance(noise_drop, (int, float)):
        raise ValueError("record.method_noise_drop must be numeric")
    if not math.isfinite(float(noise_drop)):
        raise ValueError("record.method_noise_drop must be finite")
    if not math.isclose(
        float(noise_drop), method_before - f1_after, rel_tol=0.0, abs_tol=1e-12
    ):
        raise ValueError("record.method_noise_drop is inconsistent")
    return record


def load_valid_record(path: Path, expected: Mapping[str, Any]) -> Mapping[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("record root must be an object")
    return validate_record(value, expected)
