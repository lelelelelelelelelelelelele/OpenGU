from copy import deepcopy

import pytest
import torch

from cache_v2 import ArtifactRecipe
from experiments.tracin_v2.core import (
    deployed_cross_gradient_scores,
    stable_topk,
    tracin_cp_eval_scores,
    tracin_cp_self_scores,
)
from experiments.tracin_v2.recipe import build_unstable_recipe


def test_two_checkpoint_eval_and_self_scores_match_hand_calculation():
    candidate = [
        torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64),
        torch.tensor([[2.0, -1.0], [0.5, 3.0]], dtype=torch.float64),
    ]
    target = [
        torch.tensor([5.0, 6.0], dtype=torch.float64),
        torch.tensor([-2.0, 4.0], dtype=torch.float64),
    ]
    weights = [0.1, 0.25]

    expected_eval = 0.1 * torch.tensor([17.0, 39.0], dtype=torch.float64) + 0.25 * torch.tensor(
        [-8.0, 11.0], dtype=torch.float64
    )
    expected_self = 0.1 * torch.tensor([5.0, 25.0], dtype=torch.float64) + 0.25 * torch.tensor(
        [5.0, 9.25], dtype=torch.float64
    )

    assert torch.allclose(
        tracin_cp_eval_scores(candidate, target, weights), expected_eval
    )
    assert torch.allclose(tracin_cp_self_scores(candidate, weights), expected_self)


def test_single_checkpoint_collapse_and_legacy_sign_are_explicit():
    matrix = torch.tensor([[1.0, 0.0], [0.0, 2.0]])
    target = torch.tensor([3.0, 4.0])

    assert torch.equal(
        tracin_cp_eval_scores([matrix], [target], [1.0]), matrix.mv(target)
    )
    assert torch.equal(
        deployed_cross_gradient_scores(matrix),
        -matrix.mv(matrix.sum(dim=0)),
    )


def test_stable_topk_uses_node_id_for_ties():
    ids = [9, 2, 7, 4]
    scores = torch.tensor([1.0, 3.0, 3.0, -2.0])
    assert stable_topk(ids, scores, 3) == (2, 7, 9)


def _recipe():
    digest = "a" * 64
    return build_unstable_recipe(
        source_fingerprint=digest,
        data_identity={
            "edge_index_hash": digest,
            "features_hash": digest,
            "labels_hash": digest,
            "split_hash": digest,
        },
        candidate_ids_hash=digest,
        target_ids_hash=digest,
        target_profile="attack_safe_holdout",
        label_source="validation_true_labels",
        diagnostic_only=False,
        selector_model={
            "architecture": "GCN",
            "training_recipe_hash": "train",
            "final_state_hash": digest,
            "parameter_schema_hash": digest,
        },
        checkpoints=[
            {"epoch": 1, "global_step": 1, "state_hash": digest, "weight": 0.1}
        ],
        weight_policy="paper_lr",
        optimizer={"family": "sgd", "lr": 0.1},
        loss={"family": "cross_entropy", "candidate_reduction": "single"},
        parameter_scope="all_trainable",
        seed_bundle={"train": 2024},
        numerics_profile_hash=digest,
    )


@pytest.mark.parametrize(
    "path,value",
    [
        (("algorithm_version",), "tracin-v2-unstable.changed"),
        (("producer", "source_fingerprint"), "b" * 64),
        (("data_identity", "split_hash"), "b" * 64),
        (("candidate_set", "ordered_ids_hash"), "b" * 64),
        (("target_set", "ordered_ids_hash"), "b" * 64),
        (("target_set", "label_source"), "pseudo_labels"),
        (("selector_model", "final_state_hash"), "b" * 64),
        (("trajectory", "weight_policy"), "uniform_ablation"),
        (("optimizer", "lr"), 0.05),
        (("parameter_scope",), "last_layer"),
        (("seed_bundle", "train"), 7),
        (("numerics_profile_hash",), "b" * 64),
    ],
)
def test_semantic_recipe_mutations_are_cache_misses(path, value):
    base = _recipe()
    changed = deepcopy(base.fields)
    cursor = changed
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    assert ArtifactRecipe(changed).recipe_hash != base.recipe_hash


def test_invalid_inputs_fail_closed():
    matrix = torch.ones(2, 3)
    with pytest.raises(ValueError):
        tracin_cp_eval_scores([matrix], [], [1.0])
    with pytest.raises(ValueError):
        stable_topk([1, 1], torch.ones(2), 1)
    with pytest.raises(ValueError):
        stable_topk([1, 2], torch.tensor([1.0, float("nan")]), 1)
    with pytest.raises(ValueError):
        stable_topk([1.5, 2], torch.ones(2), 1)
    with pytest.raises(ValueError):
        tracin_cp_eval_scores([matrix], [torch.ones(3)], [-0.1])


def test_checkpoint_manifest_order_and_identity_are_semantic():
    base = _recipe()
    changed_state = deepcopy(base.fields)
    changed_state["trajectory"]["checkpoints"][0]["state_hash"] = "b" * 64
    assert ArtifactRecipe(changed_state).recipe_hash != base.recipe_hash

    changed_weight = deepcopy(base.fields)
    changed_weight["trajectory"]["checkpoints"][0]["weight"] = 0.2
    assert ArtifactRecipe(changed_weight).recipe_hash != base.recipe_hash

    with pytest.raises(ValueError, match="strictly increasing"):
        build_unstable_recipe(
            source_fingerprint="a" * 64,
            data_identity={
                "edge_index_hash": "a" * 64,
                "features_hash": "a" * 64,
                "labels_hash": "a" * 64,
                "split_hash": "a" * 64,
            },
            candidate_ids_hash="a" * 64,
            target_ids_hash="a" * 64,
            target_profile="attack_safe_holdout",
            label_source="validation_true_labels",
            diagnostic_only=False,
            selector_model={
                "architecture": "GCN",
                "final_state_hash": "a" * 64,
                "parameter_schema_hash": "a" * 64,
            },
            checkpoints=[
                {"global_step": 1, "state_hash": "a" * 64, "weight": 0.1},
                {"global_step": 1, "state_hash": "b" * 64, "weight": 0.1},
            ],
            weight_policy="paper_lr",
            optimizer={"family": "sgd"},
            loss={"family": "cross_entropy"},
            parameter_scope="all_trainable",
            seed_bundle={"train": 2024},
            numerics_profile_hash="a" * 64,
        )
