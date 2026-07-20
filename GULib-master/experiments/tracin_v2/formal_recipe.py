"""Pre-compute formal Recipe for ``proper-tracin-v1`` Score Artifacts."""

from __future__ import annotations

import math
from typing import Any, Dict, Mapping, Sequence

from cache_v2 import ArtifactRecipe, validate_sha256


ALGORITHM_VERSION = "proper-tracin-v1"
SCORE_NAME = "tracin_cp_eval_lr"


def _sha(value: Any, label: str) -> str:
    return validate_sha256(value, label)


def build_formal_recipe(
    *,
    source_fingerprint: str,
    data_identity: Mapping[str, Any],
    candidate_ids_hash: str,
    target_ids_hash: str,
    target_profile: str,
    label_source: str,
    selector_model_input: Mapping[str, Any],
    checkpoint_schedule: Sequence[Mapping[str, Any]],
    training: Mapping[str, Any],
    optimizer: Mapping[str, Any],
    loss: Mapping[str, Any],
    parameter_scope: str,
    seed_bundle: Mapping[str, Any],
    numerics_profile_hash: str,
) -> ArtifactRecipe:
    """Build an exact identity known before model training or score compute.

    Output checkpoint/final-state hashes deliberately do not belong here; they
    are producer evidence and are persisted in ``ScorePayload.output_provenance``.
    """

    _sha(source_fingerprint, "source_fingerprint")
    _sha(candidate_ids_hash, "candidate_ids_hash")
    _sha(target_ids_hash, "target_ids_hash")
    _sha(numerics_profile_hash, "numerics_profile_hash")
    for name in ("edge_index_hash", "features_hash", "labels_hash", "split_hash"):
        _sha(data_identity.get(name), "data_identity.{0}".format(name))
    for name in ("initial_state_hash", "parameter_schema_hash"):
        _sha(
            selector_model_input.get(name),
            "selector_model_input.{0}".format(name),
        )
    if not isinstance(target_profile, str) or not target_profile.strip():
        raise ValueError("target_profile must be non-empty")
    if not isinstance(label_source, str) or not label_source.strip():
        raise ValueError("label_source must be non-empty")
    if not isinstance(parameter_scope, str) or not parameter_scope.strip():
        raise ValueError("parameter_scope must be non-empty")
    if not checkpoint_schedule:
        raise ValueError("checkpoint_schedule must not be empty")

    schedule = []
    previous_step = None
    for item in checkpoint_schedule:
        if not isinstance(item, Mapping):
            raise ValueError("checkpoint schedule entries must be mappings")
        step = item.get("global_step")
        weight = item.get("weight")
        if (
            isinstance(step, bool)
            or not isinstance(step, int)
            or step <= 0
            or (previous_step is not None and step <= previous_step)
        ):
            raise ValueError(
                "checkpoint global_step values must be positive and strictly increasing"
            )
        if (
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not math.isfinite(float(weight))
            or float(weight) < 0
        ):
            raise ValueError("checkpoint weights must be finite and non-negative")
        schedule.append({"global_step": int(step), "weight": float(weight)})
        previous_step = int(step)

    fields: Dict[str, Any] = {
        "artifact_kind": "score",
        "stability": "candidate",
        "score_family": "tracin_cp_node_loss_eval_set",
        "score_name": SCORE_NAME,
        "algorithm_version": ALGORITHM_VERSION,
        "producer": {
            "semantic_version": ALGORITHM_VERSION,
            "source_fingerprint": source_fingerprint,
        },
        "data_identity": dict(data_identity),
        "candidate_set": {
            "ordered_ids_hash": candidate_ids_hash,
            "gradient_definition": "fixed_graph_node_cross_entropy",
            "node_id_space": "pyg-global-node-index-v1",
        },
        "target_set": {
            "ordered_ids_hash": target_ids_hash,
            "profile": target_profile.strip(),
            "label_source": label_source.strip(),
            "aggregation": "mean",
            "diagnostic_only": False,
        },
        "selector_model_input": dict(selector_model_input),
        "trajectory": {
            "checkpoint_schedule": schedule,
            "capture_policy": "post_epoch_state_dict",
            "weight_semantics": "learning_rate_of_preceding_optimizer_update",
            "aggregation": "weighted_sum",
        },
        "training": dict(training),
        "optimizer": dict(optimizer),
        "loss": dict(loss),
        "parameter_scope": parameter_scope.strip(),
        "seed_bundle": dict(seed_bundle),
        "numerics_profile_hash": numerics_profile_hash,
        "graph_semantics": {
            "graph_intervention_scope": "fixed_graph",
            "candidate_loss_scope": "single_supervised_node",
            "transductive_policy": "message_passing_over_full_graph",
        },
        "ranking": {
            "orientation": "positive_proponent_harm_if_removed",
            "ordering": "score_desc_node_id_asc",
            "prefix_stable": True,
        },
    }
    return ArtifactRecipe(fields)


__all__ = ["ALGORITHM_VERSION", "SCORE_NAME", "build_formal_recipe"]
