import hashlib
from pathlib import Path

import pytest
import torch

from cache_v2 import (
    ArtifactConflictRecord,
    ProducerVersion,
    ScoreArtifactConflictError,
    ScoreArtifactStore,
    ScorePayload,
    ScoreProducerCalledError,
    ordered_ids_hash,
)
from cache_v2.store import CacheResolutionError
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import DatasetSelectionInputs, candidate_fingerprint
from experiments.tracin_v2.formal_recipe import (
    ALGORITHM_VERSION,
    SCORE_NAME,
    build_formal_recipe,
)
from experiments.tracin_v2.run_formal_selection_gate import (
    checkpoint_weight_schedule,
)


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _producer_version():
    return ProducerVersion(
        semantic_version=ALGORITHM_VERSION,
        source_fingerprint=_sha("proper-tracin-source"),
    )


def _recipe(**overrides):
    values = {
        "source_fingerprint": _sha("proper-tracin-source"),
        "data_identity": {
            "dataset_name": "fixture",
            "edge_index_hash": _sha("edges"),
            "features_hash": _sha("features"),
            "labels_hash": _sha("labels"),
            "split_hash": _sha("split"),
        },
        "candidate_ids_hash": ordered_ids_hash(tuple(range(20))),
        "target_ids_hash": ordered_ids_hash((20, 21, 22)),
        "target_profile": "attack_safe_holdout",
        "label_source": "validation_true_labels",
        "selector_model_input": {
            "architecture": "GCN",
            "initial_state_hash": _sha("initial-state"),
            "parameter_schema_hash": _sha("parameter-schema"),
        },
        "checkpoint_schedule": (
            {"global_step": 1, "weight": 0.01},
            {"global_step": 5, "weight": 0.01},
        ),
        "training": {"epochs": 5, "full_batch": True},
        "optimizer": {"name": "adam", "lr": 0.01, "weight_decay": 5e-4},
        "loss": {"name": "cross_entropy", "reduction": "mean"},
        "parameter_scope": "all_trainable",
        "seed_bundle": {"model_seed": 42, "selector_seed": 42},
        "numerics_profile_hash": _sha("cpu-numerics"),
    }
    values.update(overrides)
    return build_formal_recipe(**values)


def _payload(offset=0.0, provenance=None):
    candidates = tuple(range(20))
    return ScorePayload.build(
        score_name=SCORE_NAME,
        candidate_nodes=candidates,
        scores=[float(node) + float(offset) for node in candidates],
        output_provenance=(
            {
                "checkpoint_state_hashes": [_sha("checkpoint-1"), _sha("checkpoint-5")],
                "final_state_hash": _sha("final-state"),
            }
            if provenance is None
            else provenance
        ),
    )


def _file_state(root):
    return {
        path.relative_to(root).as_posix(): (
            path.stat().st_size,
            path.stat().st_mtime_ns,
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in Path(root).rglob("*")
        if path.is_file()
    }


def _dataset():
    candidates = tuple(range(20))
    return DatasetSelectionInputs(
        dataset_name="fixture",
        edge_index=torch.tensor([[0, 1], [1, 0]], dtype=torch.long),
        num_nodes=23,
        candidate_nodes=candidates,
        dataset_fingerprint=_sha("dataset"),
        graph_fingerprint=_sha("graph"),
        candidate_set_hash=candidate_fingerprint(candidates, 23),
        legacy_graph_fingerprint="fixture-legacy",
    )


def test_formal_recipe_is_precompute_only_and_mutations_miss():
    recipe = _recipe()
    encoded = recipe.canonical_json
    assert recipe.fields["algorithm_version"] == "proper-tracin-v1"
    assert "initial_state_hash" in encoded
    assert "final_state_hash" not in encoded
    assert "state_hash" not in encoded.replace("initial_state_hash", "")

    changed = _recipe(
        checkpoint_schedule=(
            {"global_step": 1, "weight": 0.01},
            {"global_step": 4, "weight": 0.01},
        )
    )
    assert changed.recipe_hash != recipe.recipe_hash


def test_checkpoint_weights_are_known_before_training():
    assert checkpoint_weight_schedule(
        (1, 5, 10, 20, 30),
        initial_lr=0.01,
        milestones=(10, 20),
        gamma=0.5,
    ) == (
        {"global_step": 1, "weight": 0.01},
        {"global_step": 5, "weight": 0.01},
        {"global_step": 10, "weight": 0.01},
        {"global_step": 20, "weight": 0.005},
        {"global_step": 30, "weight": 0.0025},
    )


def test_score_store_cold_warm_exact_hit_is_zero_compute_and_zero_write(tmp_path):
    root = (tmp_path / "score-store").resolve()
    store = ScoreArtifactStore(root, producer_version=_producer_version())
    calls = []
    cold = store.get_or_compute(
        _recipe(), lambda: calls.append("cold") or _payload()
    )
    assert calls == ["cold"]
    assert cold.hit is False
    assert cold.producer_called is True
    assert cold.artifact_id.startswith("score_")
    before = _file_state(root)

    warm = store.get_or_compute(
        _recipe(),
        lambda: pytest.fail("producer must not run on a warm exact hit"),
        fail_if_producer_called=True,
    )
    assert warm.hit is True
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id
    assert warm.payload.output_provenance["final_state_hash"] == _sha("final-state")
    assert _file_state(root) == before


def test_score_store_fail_if_called_rejects_real_miss(tmp_path):
    store = ScoreArtifactStore(
        (tmp_path / "score-store").resolve(),
        producer_version=_producer_version(),
    )
    with pytest.raises(ScoreProducerCalledError):
        store.get_or_compute(
            _recipe(), lambda: _payload(), fail_if_producer_called=True
        )


def test_same_recipe_different_score_payload_is_quarantined_and_blocks_hits(tmp_path):
    root = (tmp_path / "score-store").resolve()
    store = ScoreArtifactStore(root, producer_version=_producer_version())
    recipe = _recipe()
    accepted = store.store_score(recipe, _payload())

    changed_scores = list(_payload().scores)
    changed_scores[0] = 100.0
    conflicting = ScorePayload.build(
        score_name=SCORE_NAME,
        candidate_nodes=tuple(range(20)),
        scores=changed_scores,
        output_provenance={"final_state_hash": _sha("different-final-state")},
    )
    with pytest.raises(ScoreArtifactConflictError) as captured:
        store.store_score(recipe, conflicting)

    conflict = captured.value
    assert (root / conflict.quarantine_path).is_file()
    assert store.index.conflicts(
        artifact_type="score", recipe_hash=recipe.recipe_hash
    )
    assert accepted.artifact_id != ""
    with pytest.raises(CacheResolutionError, match="conflict marker"):
        store.load(recipe)


def test_index_conflict_without_marker_still_blocks_store(tmp_path):
    root = (tmp_path / "score-store").resolve()
    store = ScoreArtifactStore(root, producer_version=_producer_version())
    recipe = _recipe()
    accepted = store.store_score(recipe, _payload())
    store.index.record_conflict(
        ArtifactConflictRecord(
            artifact_type="score",
            recipe_hash=recipe.recipe_hash,
            existing_artifact_id=accepted.artifact_id,
            existing_content_hash=accepted.content_hash,
            observed_content_hash=_sha("unpublished-conflicting-payload"),
            quarantine_path="quarantine/score/external/payload.json",
        )
    )

    with pytest.raises(CacheResolutionError, match="recipe_conflict_present"):
        store.store_score(recipe, _payload())


def test_formal_score_parents_maxk_selection_and_warm_prefix_reuse(tmp_path):
    root = tmp_path.resolve()
    score_store = ScoreArtifactStore(
        (root / "score").resolve(), producer_version=_producer_version()
    )
    score = score_store.get_or_compute(_recipe(), lambda: _payload())
    selection_version = ProducerVersion(
        semantic_version="proper-tracin-selection-v1",
        source_fingerprint=_sha("selection-source"),
    )
    selection_root = (root / "selection").resolve()
    cold = materialize_budget_selection(
        store_root=selection_root,
        dataset=_dataset(),
        strategy="proper_tracin",
        selector_seed=42,
        budgets=(3, 14, 7),
        producer_version=selection_version,
        algorithm_version="proper-tracin-v1-topk",
        parameters={
            "prefix_stable": True,
            "score_name": SCORE_NAME,
            "ranking": "score_desc_node_id_asc",
        },
        source_score_artifact_id=score.artifact_id,
        producer=lambda k: score.payload.ranking[:k],
    )
    assert cold.producer_called is True
    assert cold.result.payload.source_score_artifact_id == score.artifact_id
    assert cold.views["7"]["selected_nodes"] == list(score.payload.ranking[:7])

    warm = materialize_budget_selection(
        store_root=selection_root,
        dataset=_dataset(),
        strategy="proper_tracin",
        selector_seed=42,
        budgets=(3, 7),
        producer_version=selection_version,
        algorithm_version="proper-tracin-v1-topk",
        parameters={
            "prefix_stable": True,
            "score_name": SCORE_NAME,
            "ranking": "score_desc_node_id_asc",
        },
        source_score_artifact_id=score.artifact_id,
        producer=lambda _k: pytest.fail("selection producer must not run"),
        fail_if_producer_called=True,
    )
    assert warm.cache_hit is True
    assert warm.producer_called is False
    assert warm.artifact_k == 14
    assert warm.views["7"]["reuse_kind"] == "cache_artifact_prefix"
