"""Semantic Cache V2 recipe for the C-target score bundle."""

from __future__ import annotations

import math
import re
from typing import Any, Mapping, Sequence

from cache_v2 import ArtifactRecipe


ALGORITHM_VERSION = "c-target-gif-tracin-v1.0"
SCORE_FAMILY = "c_target_gif_tracin_score_bundle"
SCORE_NAMES = (
    "gt_full",
    "gt_simple",
    "legacy",
    "p_graph",
    "p_point",
    "p_simple",
    "r_point",
    "tracin_cp_point",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ValueError("{0} must be a full lowercase SHA-256".format(label))
    return value


def build_recipe(
    *,
    source_fingerprint: str,
    data_identity: Mapping[str, Any],
    candidate_ids_hash: str,
    target_ids_hash: str,
    selector_model: Mapping[str, Any],
    training: Mapping[str, Any],
    checkpoints: Sequence[Mapping[str, Any]],
    graph_intervention: Mapping[str, Any],
    hessian: Mapping[str, Any],
    loss: Mapping[str, Any],
    parameter_scope: str,
    seed_bundle: Mapping[str, Any],
    numerics: Mapping[str, Any],
) -> ArtifactRecipe:
    _sha(source_fingerprint, "source_fingerprint")
    _sha(candidate_ids_hash, "candidate_ids_hash")
    _sha(target_ids_hash, "target_ids_hash")
    for name in (
        "edge_index_hash",
        "features_hash",
        "labels_hash",
        "split_hash",
    ):
        _sha(data_identity.get(name), "data_identity.{0}".format(name))
    for name in ("final_state_hash", "parameter_schema_hash"):
        _sha(selector_model.get(name), "selector_model.{0}".format(name))
    if not checkpoints:
        raise ValueError("at least one checkpoint is required")
    previous = None
    for item in checkpoints:
        step = item.get("global_step")
        state = item.get("state_hash")
        weight = item.get("weight")
        if (
            isinstance(step, bool)
            or not isinstance(step, int)
            or step < 0
            or (previous is not None and step <= previous)
        ):
            raise ValueError("checkpoint steps must be strictly increasing")
        _sha(state, "checkpoint state_hash")
        if (
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not math.isfinite(float(weight))
            or float(weight) < 0
        ):
            raise ValueError("checkpoint weight must be finite and non-negative")
        previous = step

    fields = {
        "artifact_kind": "score_bundle",
        "score_family": SCORE_FAMILY,
        "score_names": list(SCORE_NAMES),
        "algorithm_version": ALGORITHM_VERSION,
        "producer": {
            "semantic_version": ALGORITHM_VERSION,
            "source_fingerprint": source_fingerprint,
        },
        "data_identity": dict(data_identity),
        "candidate_set": {
            "ordered_ids_hash": candidate_ids_hash,
            "node_id_space": "pyg-global-node-index-v1",
        },
        "target_set": {
            "ordered_ids_hash": target_ids_hash,
            "profile": "attack_safe_validation",
            "label_source": "validation_true_labels",
            "aggregation": "mean",
            "diagnostic_only": False,
        },
        "selector_model": dict(selector_model),
        "training": dict(training),
        "trajectory": {
            "checkpoints": [dict(item) for item in checkpoints],
            "capture_policy": "post_epoch_state_dict",
            "weight_policy": "preceding_optimizer_update_lr",
        },
        "graph_intervention": dict(graph_intervention),
        "hessian": dict(hessian),
        "loss": dict(loss),
        "parameter_scope": str(parameter_scope),
        "seed_bundle": dict(seed_bundle),
        "numerics": dict(numerics),
        "aggregation": {
            "orientation": "score_desc_more_harm_if_removed",
            "ranking": "score_desc_node_id_asc",
        },
    }
    return ArtifactRecipe(fields)
