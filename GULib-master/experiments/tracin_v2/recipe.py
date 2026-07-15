"""Recipe construction for isolated TracIn V2 experiments."""

from __future__ import annotations

import math
import re
from typing import Any, Dict, Mapping, Sequence

from cache_v2 import ArtifactRecipe


ALGORITHM_VERSION = "tracin-v2-unstable.0"
SCORE_FAMILY = "tracin_cp_node_loss_eval_set"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ValueError("{0} must be a lowercase full SHA-256 digest".format(label))
    return value


def build_unstable_recipe(
    *,
    source_fingerprint: str,
    data_identity: Mapping[str, Any],
    candidate_ids_hash: str,
    target_ids_hash: str,
    target_profile: str,
    label_source: str,
    diagnostic_only: bool,
    selector_model: Mapping[str, Any],
    checkpoints: Sequence[Mapping[str, Any]],
    weight_policy: str,
    optimizer: Mapping[str, Any],
    loss: Mapping[str, Any],
    parameter_scope: str,
    seed_bundle: Mapping[str, Any],
    numerics_profile_hash: str,
) -> ArtifactRecipe:
    source_fingerprint = _require_sha256(source_fingerprint, "source_fingerprint")
    candidate_ids_hash = _require_sha256(candidate_ids_hash, "candidate_ids_hash")
    target_ids_hash = _require_sha256(target_ids_hash, "target_ids_hash")
    numerics_profile_hash = _require_sha256(
        numerics_profile_hash, "numerics_profile_hash"
    )
    for field in ("edge_index_hash", "features_hash", "labels_hash", "split_hash"):
        _require_sha256(data_identity.get(field), "data_identity.{0}".format(field))
    for field in ("final_state_hash", "parameter_schema_hash"):
        _require_sha256(selector_model.get(field), "selector_model.{0}".format(field))
    if not checkpoints:
        raise ValueError("the TracIn V2 recipe requires at least one checkpoint")
    previous_step = None
    for index, checkpoint in enumerate(checkpoints):
        if not isinstance(checkpoint, Mapping):
            raise ValueError("each checkpoint manifest entry must be a mapping")
        step = checkpoint.get("global_step")
        weight = checkpoint.get("weight")
        state_hash = checkpoint.get("state_hash")
        if isinstance(step, bool) or not isinstance(step, int) or step < 0:
            raise ValueError("checkpoint global_step must be a non-negative integer")
        if previous_step is not None and step <= previous_step:
            raise ValueError("checkpoint global_step values must be strictly increasing")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(weight):
            raise ValueError("checkpoint weights must be finite numbers")
        if not isinstance(state_hash, str) or not state_hash.strip():
            raise ValueError("checkpoint state_hash must be a non-empty string")
        _require_sha256(state_hash, "checkpoint state_hash")
        previous_step = step
    fields: Dict[str, Any] = {
        "stability": "unstable",
        "score_family": SCORE_FAMILY,
        "algorithm_version": ALGORITHM_VERSION,
        "producer": {
            "semantic_version": ALGORITHM_VERSION,
            "source_fingerprint": str(source_fingerprint),
        },
        "data_identity": dict(data_identity),
        "candidate_set": {
            "ordered_ids_hash": str(candidate_ids_hash),
            "gradient_definition": "fixed_graph_node_cross_entropy",
            "node_id_space": "pyg-global-node-index-v1",
        },
        "target_set": {
            "ordered_ids_hash": str(target_ids_hash),
            "profile": str(target_profile),
            "label_source": str(label_source),
            "aggregation": "mean",
            "diagnostic_only": bool(diagnostic_only),
        },
        "selector_model": dict(selector_model),
        "trajectory": {
            "checkpoints": [dict(item) for item in checkpoints],
            "capture_policy": "post_epoch_state_dict",
            "weight_semantics": "learning_rate_of_preceding_optimizer_update",
            "weight_policy": str(weight_policy),
        },
        "optimizer": dict(optimizer),
        "loss": dict(loss),
        "aggregation": {
            "checkpoint": "weighted_sum",
            "orientation": "positive_proponent_harm_if_removed",
            "selection": "score_desc_node_id_asc",
        },
        "parameter_scope": str(parameter_scope),
        "seed_bundle": dict(seed_bundle),
        "numerics_profile_hash": str(numerics_profile_hash),
        "graph_semantics": {
            "graph_intervention_scope": "fixed_graph",
            "candidate_loss_scope": "single_supervised_node",
            "transductive_policy": "message_passing_over_full_graph",
        },
    }
    return ArtifactRecipe(fields)
