from experiments.target_direct_v1.recipe import (
    ALGORITHM_VERSION,
    SCORE_FAMILY,
    build_recipe,
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
        graph_intervention={},
        hessian={},
        loss={},
        parameter_scope="last_layer",
        seed_bundle={},
        numerics={},
        target_checkpoint={"file_sha256": SHA, "state_hash": SHA},
    )
    fields = recipe.fields
    assert fields["algorithm_version"] == ALGORITHM_VERSION
    assert fields["score_family"] == SCORE_FAMILY
    assert fields["target_direct"]["white_box"] is True
    assert fields["target_direct"]["target_checkpoint"]["state_hash"] == SHA
