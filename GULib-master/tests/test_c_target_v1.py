import hashlib

import pytest
import torch

from cache_v2 import ProducerVersion
from experiments.c_target_v1.core import (
    affected_nodes,
    build_undirected_adjacency,
    pair_metrics,
    remove_incident_edges,
    stable_ranking,
)
from experiments.c_target_v1.recipe import SCORE_NAMES, build_recipe
from experiments.c_target_v1.score_store import (
    ProducerCalledError,
    ScoreBundlePayload,
    ScoreBundleStore,
)


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _recipe(candidate_hash, seed=2024):
    return build_recipe(
        source_fingerprint=_sha("source"),
        data_identity={
            "dataset": "Cora",
            "edge_index_hash": _sha("edges"),
            "features_hash": _sha("features"),
            "labels_hash": _sha("labels"),
            "split_hash": _sha("split"),
        },
        candidate_ids_hash=candidate_hash,
        target_ids_hash=_sha("targets"),
        selector_model={
            "architecture": "GateGCN",
            "final_state_hash": _sha("state"),
            "parameter_schema_hash": _sha("parameters"),
        },
        training={"epochs": 30, "optimizer": "SGD"},
        checkpoints=(
            {"global_step": 1, "state_hash": _sha("state-1"), "weight": 0.1},
            {"global_step": 30, "state_hash": _sha("state-30"), "weight": 0.1},
        ),
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "affected_hops": 2,
            "exact_retrain": False,
        },
        hessian={"method": "LiSSA", "iterations": 20},
        loss={"type": "cross_entropy", "target_set": "validation_mask"},
        parameter_scope="all_trainable",
        seed_bundle={"python_numpy_torch": seed},
        numerics={"torch_dtype": "torch.float32", "deterministic_algorithms": True},
    )


def _payload(candidates):
    base = {
        name: [float(index + offset) for index in range(len(candidates))]
        for offset, name in enumerate(SCORE_NAMES)
    }
    rankings = {
        name: list(stable_ranking(candidates, torch.tensor(values)))
        for name, values in base.items()
    }
    return ScoreBundlePayload.build(
        candidates,
        base,
        rankings,
        {"exact_retrain_performed": False},
    )


def test_score_bundle_store_cold_warm_and_recipe_mismatch(tmp_path):
    candidates = (3, 8, 10)
    payload = _payload(candidates)
    recipe = _recipe(payload.candidate_ids_hash)
    store = ScoreBundleStore(
        tmp_path.resolve(),
        producer_version=ProducerVersion(
            semantic_version="test-v1", source_fingerprint=_sha("producer")
        ),
    )

    cold = store.get_or_compute(recipe, lambda: payload)
    assert cold.hit is False
    assert cold.producer_called is True
    assert cold.payload == payload
    assert (tmp_path / cold.semantic_path).is_file()

    warm = store.get_or_compute(
        recipe,
        lambda: pytest.fail("producer must not run on an exact warm hit"),
        fail_if_called=True,
    )
    assert warm.hit is True
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id
    assert warm.content_hash == cold.content_hash

    mismatched_recipe = _recipe(payload.candidate_ids_hash, seed=2025)
    with pytest.raises(ProducerCalledError):
        store.get_or_compute(
            mismatched_recipe,
            lambda: pytest.fail("mismatched recipe must not reuse the old payload"),
            fail_if_called=True,
        )


def test_score_bundle_rejects_ranking_not_derived_from_scores():
    candidates = (1, 2, 3)
    scores = {name: (1.0, 2.0, 3.0) for name in SCORE_NAMES}
    rankings = {name: (3, 2, 1) for name in SCORE_NAMES}
    rankings["gt_full"] = (1, 2, 3)
    with pytest.raises(Exception, match="inconsistent with scores"):
        ScoreBundlePayload.build(candidates, scores, rankings)


def test_graph_affected_set_and_incident_edge_removal():
    edge_index = torch.tensor(
        [[0, 1, 1, 2, 2, 3], [1, 0, 2, 1, 3, 2]], dtype=torch.long
    )
    adjacency = build_undirected_adjacency(edge_index, num_nodes=4)
    assert affected_nodes(adjacency, node_id=0, hops=0) == (0,)
    assert affected_nodes(adjacency, node_id=0, hops=1) == (0, 1)
    assert affected_nodes(adjacency, node_id=0, hops=2) == (0, 1, 2)

    deleted = remove_incident_edges(edge_index, node_id=1)
    assert deleted.tolist() == [[2, 3], [3, 2]]


def test_stable_ranking_and_pair_metrics_are_deterministic():
    candidates = (9, 2, 5)
    reference = torch.tensor([1.0, 1.0, 0.0])
    proxy = torch.tensor([0.0, 2.0, 1.0])
    reference_ranking = stable_ranking(candidates, reference)
    proxy_ranking = stable_ranking(candidates, proxy)
    assert reference_ranking == (2, 9, 5)
    assert proxy_ranking == (2, 5, 9)
    metrics = pair_metrics(
        reference.tolist(),
        proxy.tolist(),
        reference_ranking,
        proxy_ranking,
        k=2,
    )
    assert metrics["intersection"] == 1
    assert metrics["union"] == 3
    assert metrics["jaccard"] == pytest.approx(1.0 / 3.0)
    assert metrics["common_fraction"] == pytest.approx(0.5)
