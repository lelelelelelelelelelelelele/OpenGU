"""Cache identity for white-box OpenGU target-direct score bundles."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cache_v2 import ArtifactRecipe
from experiments.bc_target_v2.recipe import (
    SCORE_NAMES,
    build_recipe as build_bc_recipe,
)


ALGORITHM_VERSION = "target-direct-opengu-gcn-score-bundle-v1"
SCORE_FAMILY = "target_direct_opengu_gcn_selection_score_bundle"


def build_recipe(
    *,
    source_fingerprint: str,
    data_identity: Mapping[str, Any],
    candidate_ids_hash: str,
    target_ids_hash: str,
    selector_model: Mapping[str, Any],
    training: Mapping[str, Any],
    checkpoints: Sequence[Mapping[str, Any]],
    checkpoint_views: Mapping[str, Sequence[int]],
    graph_intervention: Mapping[str, Any],
    hessian: Mapping[str, Any],
    loss: Mapping[str, Any],
    parameter_scope: str,
    seed_bundle: Mapping[str, Any],
    numerics: Mapping[str, Any],
    target_checkpoint: Mapping[str, Any],
) -> ArtifactRecipe:
    base = build_bc_recipe(
        source_fingerprint=source_fingerprint,
        data_identity=data_identity,
        candidate_ids_hash=candidate_ids_hash,
        target_ids_hash=target_ids_hash,
        selector_model=selector_model,
        training=training,
        checkpoints=checkpoints,
        checkpoint_views=checkpoint_views,
        graph_intervention=graph_intervention,
        hessian=hessian,
        loss=loss,
        parameter_scope=parameter_scope,
        seed_bundle=seed_bundle,
        numerics=numerics,
    )
    fields = base.fields
    fields["algorithm_version"] = ALGORITHM_VERSION
    fields["score_family"] = SCORE_FAMILY
    fields["producer"]["semantic_version"] = ALGORITHM_VERSION
    fields["target_direct"] = {
        "white_box": True,
        "selector_and_gu_share_exact_checkpoint": True,
        "target_checkpoint": dict(target_checkpoint),
    }
    return ArtifactRecipe(fields)
