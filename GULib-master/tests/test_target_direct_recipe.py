from experiments.target_direct_v1.recipe import (
    ALGORITHM_VERSION,
    SCORE_FAMILY,
    build_recipe,
)
from experiments.target_direct_v1.run_selection import (
    selection_recipe_parameters,
)


SHA = "a" * 64


def test_target_direct_recipe_binds_checkpoint_identity():
    recipe = build_recipe(
        source_fingerprint=SHA,
        data_identity={
            "edge_index_hash": SHA,
            "features_hash": SHA,
            "labels_hash": SHA,
            "split_hash": SHA,
        },
        candidate_ids_hash=SHA,
        target_ids_hash=SHA,
        selector_model={"final_state_hash": SHA, "parameter_schema_hash": SHA},
        training={"epochs": 100},
        checkpoints=({"global_step": 100, "state_hash": SHA, "weight": 0.01},),
        checkpoint_views={"single": (0,)},
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "source_scope": "affected_intersection_train_mask",
        },
        hessian={},
        loss={"graph_source_set": "affected_intersection_train_mask"},
        parameter_scope="last_layer",
        seed_bundle={},
        numerics={},
        target_checkpoint={"file_sha256": SHA, "state_hash": SHA},
    )
    fields = recipe.fields
    assert fields["algorithm_version"] == ALGORITHM_VERSION
    assert ALGORITHM_VERSION == "target-direct-opengu-gcn-score-bundle-v3"
    assert fields["score_family"] == SCORE_FAMILY
    assert (
        fields["graph_intervention"]["source_scope"]
        == "affected_intersection_train_mask"
    )
    assert (
        fields["loss"]["graph_source_set"]
        == "affected_intersection_train_mask"
    )
    assert fields["target_direct"]["white_box"] is True
    assert fields["target_direct"]["target_checkpoint"]["state_hash"] == SHA
    projection = fields["target_direct"]["budget_projection"]
    assert projection["semantics"] == "prefix_stable_budget_independent"
    assert projection["supported_ratios"] == [0.01, 0.05]
    assert projection["budget_conditioned_strategies"] == []


def test_ratio_specific_selection_recipes_share_scores_but_not_budget_identity():
    one = selection_recipe_parameters(
        name="degree",
        ratio=0.01,
        expected_k=18,
        target_checkpoint_state_hash=SHA,
    )
    five = selection_recipe_parameters(
        name="degree",
        ratio=0.05,
        expected_k=94,
        target_checkpoint_state_hash=SHA,
    )

    assert one["score_family"] == five["score_family"]
    assert one["target_checkpoint_state_hash"] == five[
        "target_checkpoint_state_hash"
    ]
    assert one["requested_ratio"] == 0.01
    assert five["requested_ratio"] == 0.05
    assert one["expected_k"] == 18
    assert five["expected_k"] == 94
    assert one != five
