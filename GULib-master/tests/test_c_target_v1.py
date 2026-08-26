import hashlib
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from cache_v2 import ProducerVersion
from cache_v2.errors import PathValidationError, SchemaVersionError
from cache_v2.index import CacheIndex
from cache_v2.selection_materializer import (
    SelectionArtifactRequest,
    build_selection_recipe,
    store_selection_artifact,
)
from experiments.c_target_v1.core import (
    affected_nodes,
    build_undirected_adjacency,
    graph_source_scores,
    pair_metrics,
    remove_incident_edges,
    stable_ranking,
)
from experiments.c_target_v1.recipe import SCORE_NAMES, build_recipe
from experiments.c_target_v1.run_cora_gcn import DEFAULT_DATA_ROOT
from experiments.c_target_v1.score_store import (
    ProducerCalledError,
    ScoreBundlePayload,
    ScoreBundleStore,
)


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def test_c_target_default_dataset_root_is_repository_canonical_raw():
    repository_root = Path(__file__).resolve().parents[1]
    assert DEFAULT_DATA_ROOT == (repository_root / "data" / "raw").resolve()


def _recipe(candidate_hash, seed=2024, *, include_source_contract=True):
    graph_intervention = {
        "operation": "remove_candidate_incident_edges",
        "affected_hops": 2,
        "exact_retrain": False,
    }
    loss = {"type": "cross_entropy", "target_set": "validation_mask"}
    if include_source_contract:
        graph_intervention["source_scope"] = (
            "affected_intersection_train_mask"
        )
        loss["graph_source_set"] = "affected_intersection_train_mask"
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
        graph_intervention=graph_intervention,
        hessian={"method": "LiSSA", "iterations": 20},
        loss=loss,
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


def test_score_bundle_store_can_share_canonical_index_with_selection_store(
    tmp_path,
):
    root = tmp_path.resolve()
    candidates = (3, 8, 10)
    payload = _payload(candidates)
    recipe = _recipe(payload.candidate_ids_hash)
    producer = ProducerVersion(
        semantic_version="test-v1", source_fingerprint=_sha("producer")
    )
    canonical_index = CacheIndex(root / "index.sqlite")

    cold = ScoreBundleStore(
        root, producer_version=producer, index=canonical_index
    ).get_or_compute(recipe, lambda: payload)
    assert cold.hit is False
    assert canonical_index.database_path == root / "index.sqlite"

    selection_producer = ProducerVersion(
        semantic_version="selection-v1", source_fingerprint=_sha("selection")
    )
    selection_recipe = build_selection_recipe(
        dataset_fingerprint=_sha("dataset"),
        graph_fingerprint=_sha("graph"),
        candidate_set_hash=payload.candidate_ids_hash,
        num_nodes=11,
        candidate_count=len(candidates),
        node_id_space="global",
        strategy="degree",
        seed=2024,
        k=2,
        producer_version=selection_producer,
        algorithm_version="selection-v1",
        parameters={"fixture": True},
        source_score_artifact_id=cold.artifact_id,
    )
    selection = store_selection_artifact(
        root,
        SelectionArtifactRequest.from_recipe(
            selection_recipe, selection_producer
        ),
        selected_nodes=(3, 8),
        compute_seconds=0.01,
    )
    assert selection.artifact_id.startswith("sel_")
    assert canonical_index.check_schema() == 1

    warm = ScoreBundleStore(
        root,
        producer_version=producer,
        index=CacheIndex(root / "index.sqlite"),
    ).get_or_compute(
        recipe,
        lambda: pytest.fail("canonical index warm hit must not call producer"),
        fail_if_called=True,
    )
    assert warm.hit is True
    assert warm.artifact_id == cold.artifact_id


def test_score_bundle_store_rejects_injected_index_outside_root(tmp_path):
    root = (tmp_path / "cache").resolve()
    external = CacheIndex((tmp_path / "other" / "index.sqlite").resolve())

    with pytest.raises(PathValidationError, match="injected CacheIndex"):
        ScoreBundleStore(
            root,
            producer_version=ProducerVersion(
                semantic_version="test-v1", source_fingerprint=_sha("producer")
            ),
            index=external,
        )


def test_score_bundle_store_rejects_injected_index_with_wrong_schema(tmp_path):
    root = tmp_path.resolve()
    index_path = root / "index.sqlite"
    with sqlite3.connect(index_path) as connection:
        connection.execute("CREATE TABLE wrong_schema (id INTEGER PRIMARY KEY)")
    store = ScoreBundleStore(
        root,
        producer_version=ProducerVersion(
            semantic_version="test-v1", source_fingerprint=_sha("producer")
        ),
        index=CacheIndex(index_path),
    )

    with pytest.raises(SchemaVersionError):
        store.initialize()


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


class _ToyMessagePassing(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = torch.nn.Parameter(
            torch.tensor([[0.7, -0.4], [0.2, 0.9]], dtype=torch.float32)
        )

    def forward(self, x, edge_index):
        messages = torch.zeros_like(x)
        messages.index_add_(0, edge_index[1], x[edge_index[0]])
        return (x + 0.5 * messages).matmul(self.weight)


def test_c_target_recipe_requires_affected_training_source_contract():
    recipe = _recipe(_sha("candidates"))
    assert recipe.fields["algorithm_version"] == "c-target-gif-tracin-v1.1"
    assert (
        recipe.fields["graph_intervention"]["source_scope"]
        == "affected_intersection_train_mask"
    )
    assert (
        recipe.fields["loss"]["graph_source_set"]
        == "affected_intersection_train_mask"
    )

    with pytest.raises(ValueError, match="affected training-source contract"):
        _recipe(
            _sha("obsolete-candidates"),
            include_source_contract=False,
        )


def _toy_graph_source_scores(*, labels=None, features=None, edge_index=None):
    model = _ToyMessagePassing()
    if edge_index is None:
        edge_index = torch.tensor(
            [[0, 1, 0, 2, 0, 3], [1, 0, 2, 0, 3, 0]], dtype=torch.long
        )
    if features is None:
        features = torch.tensor(
            [[1.0, 0.2], [0.3, 1.4], [1.1, -0.7], [-0.4, 0.8]],
            dtype=torch.float32,
        )
    if labels is None:
        labels = torch.tensor([0, 1, 0, 1], dtype=torch.long)
    data = SimpleNamespace(
        x=features,
        y=labels,
        edge_index=edge_index,
        num_nodes=4,
    )
    direction = torch.tensor([0.4, -0.6, 0.3, 0.8], dtype=torch.float32)
    scores, _ = graph_source_scores(
        model,
        data,
        state=model.state_dict(),
        candidate_ids=torch.tensor([0]),
        source_ids=torch.tensor([0, 3]),
        parameter_scope="all_trainable",
        affected_hops=1,
        target_gradient=direction,
        inverse_target=direction,
    )
    return scores


def test_graph_source_scores_use_only_affected_training_labels():
    baseline = _toy_graph_source_scores()
    nontraining_labels = torch.tensor([0, 0, 1, 1], dtype=torch.long)
    assert all(
        torch.equal(
            baseline[name],
            _toy_graph_source_scores(labels=nontraining_labels)[name],
        )
        for name in baseline
    )

    training_labels = torch.tensor([0, 1, 0, 0], dtype=torch.long)
    changed = _toy_graph_source_scores(labels=training_labels)
    assert not torch.equal(baseline["p_graph"], changed["p_graph"])


def test_graph_source_scores_keep_nontraining_features_in_message_passing():
    features = torch.tensor(
        [[1.0, 0.2], [0.3, 1.4], [1.1, -0.7], [-0.4, 0.8]],
        dtype=torch.float32,
    )
    baseline = _toy_graph_source_scores(features=features)
    changed_features = features.clone()
    changed_features[1] = torch.tensor([1.7, -0.2])
    changed_features[2] = torch.tensor([-0.8, 1.5])
    changed = _toy_graph_source_scores(features=changed_features)
    assert not torch.equal(baseline["p_graph"], changed["p_graph"])


def test_graph_source_scores_keep_nontraining_structure_in_message_passing():
    baseline_edges = torch.tensor(
        [[0, 1, 0, 2, 0, 3], [1, 0, 2, 0, 3, 0]], dtype=torch.long
    )
    changed_edges = torch.cat(
        (
            baseline_edges,
            torch.tensor([[1, 3], [3, 1]], dtype=torch.long),
        ),
        dim=1,
    )
    baseline = _toy_graph_source_scores(edge_index=baseline_edges)
    changed = _toy_graph_source_scores(edge_index=changed_edges)
    assert not torch.equal(baseline["p_graph"], changed["p_graph"])


def test_graph_source_scores_match_explicit_incident_edge_deletion():
    model = _ToyMessagePassing()
    edge_index = torch.tensor(
        [[0, 1, 0, 2, 0, 3], [1, 0, 2, 0, 3, 0]], dtype=torch.long
    )
    data = SimpleNamespace(
        x=torch.tensor(
            [[1.0, 0.2], [0.3, 1.4], [1.1, -0.7], [-0.4, 0.8]],
            dtype=torch.float32,
        ),
        y=torch.tensor([0, 1, 0, 1], dtype=torch.long),
        edge_index=edge_index,
        num_nodes=4,
    )
    direction = torch.tensor([0.4, -0.6, 0.3, 0.8], dtype=torch.float32)
    scores, _ = graph_source_scores(
        model,
        data,
        state=model.state_dict(),
        candidate_ids=torch.tensor([0]),
        source_ids=torch.tensor([0, 3]),
        parameter_scope="all_trainable",
        affected_hops=1,
        target_gradient=direction,
        inverse_target=direction,
    )

    original_logits = model(data.x, data.edge_index)
    loss1 = torch.nn.functional.cross_entropy(
        original_logits[torch.tensor([0, 3])],
        data.y[torch.tensor([0, 3])],
        reduction="sum",
    )
    grad1 = torch.autograd.grad(loss1, model.weight)[0].reshape(-1)
    deleted_edge_index = remove_incident_edges(data.edge_index, node_id=0)
    deleted_logits = model(data.x, deleted_edge_index)
    loss2 = torch.nn.functional.cross_entropy(
        deleted_logits[torch.tensor([3])],
        data.y[torch.tensor([3])],
        reduction="sum",
    )
    grad2 = torch.autograd.grad(loss2, model.weight)[0].reshape(-1)
    expected = torch.dot(grad1 - grad2, direction)
    assert scores["p_graph"].item() == pytest.approx(expected.item())


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
