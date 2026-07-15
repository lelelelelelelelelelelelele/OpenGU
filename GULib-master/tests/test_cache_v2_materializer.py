import hashlib
import json
import pickle
from pathlib import Path

import pytest
import torch
from torch_geometric.data import Data

import experiments.selection_inputs as input_module
import experiments.selection_producer as producer_module
from scripts import cachectl


class FakeImStrategy:
    calls = 0

    def __init__(self, args):
        assert args["enable_score_cache"] is False
        self._score_cache = None
        self._celf_cache = None

    def compute_im_celf(self, edge_index, num_nodes, k, candidate_set):
        del edge_index, num_nodes
        type(self).calls += 1
        selected = list(candidate_set[:k])
        return selected, torch.ones(k, dtype=torch.float32)


class FakeRandomStrategy:
    def __init__(self, args):
        assert args == {}

    def select_nodes(self, data, model, k):
        del model
        candidates = data.train_indices
        return candidates[torch.randperm(candidates.numel())[:k]]


class FakeDegreeStrategy:
    def __init__(self, args):
        assert args == {}


class FakePageRankStrategy:
    def __init__(self, args):
        self.alpha = float(args["pagerank_alpha"])

    def select_nodes(self, data, model, k):
        del model
        candidates = data.train_indices
        return candidates[
            torch.argsort(candidates.float() * self.alpha, descending=True)[:k]
        ]


def _write_config(tmp_path, strategies=None, seeds=None, methods=None):
    path = tmp_path / "request.yaml"
    path.write_text(
        "\n".join(
            [
                "name: fixture_request",
                "dataset: cora",
                "base_model: GCN",
                "ratio: 0.5",
                "methods:",
                *["  - {0}".format(value) for value in (methods or ["GIF", "IDEA"])],
                "strategies:",
                *[
                    "  - {0}".format(value)
                    for value in (strategies or ["im", "tracin", "hybrid"])
                ],
                "seeds:",
                *["  - {0}".format(value) for value in (seeds or [42, 212, 722])],
                "extra_args:",
                "  - --candidate_fraction",
                "  - '0.5'",
                "  - --mc_rounds",
                "  - '7'",
                "  - --im_v4_batch_size",
                "  - '1'",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _fixture_inputs():
    edge_index = torch.tensor(
        [[0, 1, 1, 2, 2, 3, 3, 4], [1, 0, 2, 1, 3, 2, 4, 3]],
        dtype=torch.long,
    )
    data = Data(
        x=torch.arange(10, dtype=torch.float32).reshape(5, 2),
        y=torch.tensor([0, 1, 0, 1, 0]),
        edge_index=edge_index,
        num_nodes=5,
        train_mask=torch.tensor([True, True, True, True, False]),
        train_indices=torch.tensor([0, 1, 2, 3]),
    )
    return input_module.make_dataset_selection_inputs(data, dataset_name="cora")


def _prepare_roots(tmp_path):
    processed_root = (tmp_path / "processed").resolve()
    processed_root.mkdir()
    legacy_root = tmp_path / "legacy-results"
    for name in ("cache", "selection_cache", "score_cache"):
        (legacy_root / name).mkdir(parents=True)
    return processed_root, legacy_root.resolve()


@pytest.fixture
def fake_producer_layer(monkeypatch):
    inputs = _fixture_inputs()
    FakeImStrategy.calls = 0
    monkeypatch.setattr(
        producer_module,
        "load_im_strategy",
        lambda: (FakeImStrategy, True, Path(producer_module.__file__).resolve()),
    )
    simple_classes = {
        "random": FakeRandomStrategy,
        "degree": FakeDegreeStrategy,
        "pagerank": FakePageRankStrategy,
    }
    monkeypatch.setattr(
        producer_module,
        "load_simple_strategy",
        lambda strategy: (
            simple_classes[strategy],
            Path(producer_module.__file__).resolve(),
        ),
    )
    return inputs


def _file_state(path):
    stat = path.stat()
    return {
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def test_plan_deduplicates_im_and_structurally_skips_future_producers(
    tmp_path, fake_producer_layer
):
    config = _write_config(tmp_path)
    processed_root, _ = _prepare_roots(tmp_path)
    plan = producer_module.prepare_selection_plan(
        config, processed_root, dataset_inputs=fake_producer_layer
    )
    document = plan.to_dict()

    assert document["total_consumer_requests"] == 18
    assert document["supported_consumer_requests"] == 6
    assert document["unique_artifact_recipes"] == 1
    assert document["deduplicated_requests"] == 5
    assert {item["strategy"] for item in document["skipped"]} == {
        "tracin",
        "hybrid",
    }
    assert all(item["future_registry_extension"] for item in document["skipped"])
    fields = plan.jobs[0].recipe.fields
    assert fields["selector"] == "im"
    assert fields["k"] == 2
    assert fields["selector_parameters"]["candidate_fraction"] == 0.5
    assert fields["selector_parameters"]["mc_rounds"] == 7
    assert fields["selector_parameters"]["im_batch_size"] == 1
    assert fields["dataset_fingerprint"] == fake_producer_layer.dataset_fingerprint
    assert fields["producer_version"] == plan.jobs[0].producer_version.to_dict()
    serialized = json.dumps(plan.jobs[0].recipe.to_dict(), sort_keys=True)
    for forbidden in ("fixture_request", "request.yaml", "base_model", "GIF", "212"):
        assert forbidden not in serialized


def test_selection_plan_is_zero_write_for_store_and_legacy(
    tmp_path, fake_producer_layer
):
    config = _write_config(tmp_path, strategies=["im", "tracin"])
    processed_root, legacy_root = _prepare_roots(tmp_path)
    legacy_file = legacy_root / "selection_cache" / "sentinel.json"
    legacy_file.write_text('{"sentinel":true}', encoding="utf-8")
    legacy_before = _file_state(legacy_file)
    store_root = (tmp_path / "v2-store").resolve()

    document = producer_module.plan_selection(
        config,
        processed_root,
        store_root,
        legacy_root,
        dataset_inputs=fake_producer_layer,
    )

    assert document["execution_performed"] is False
    assert document["producer_calls"] == 0
    assert document["writes"] == []
    assert document["store_unchanged"] is True
    assert document["legacy_cache_unchanged"] is True
    assert document["split_reconstructed"] is False
    assert document["resolutions"][0]["miss_reasons"] == ["store_not_initialized"]
    assert not store_root.exists()
    assert _file_state(legacy_file) == legacy_before
    assert FakeImStrategy.calls == 0


def test_plan_registers_simple_producers_with_minimal_identity_and_seed_scope(
    tmp_path, fake_producer_layer
):
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42, 212],
    )
    processed_root, _ = _prepare_roots(tmp_path)
    plan = producer_module.prepare_selection_plan(
        config, processed_root, dataset_inputs=fake_producer_layer
    )
    document = plan.to_dict()

    assert document["registered_producers"] == ["degree", "im", "pagerank", "random"]
    assert document["total_consumer_requests"] == 12
    assert document["supported_consumer_requests"] == 12
    assert document["unique_artifact_recipes"] == 4
    assert document["deduplicated_requests"] == 8
    assert document["skipped"] == []

    random_jobs = [job for job in plan.jobs if job.strategy == "random"]
    degree_job = next(job for job in plan.jobs if job.strategy == "degree")
    pagerank_job = next(job for job in plan.jobs if job.strategy == "pagerank")
    assert {job.recipe.fields["selector_seed"] for job in random_jobs} == {42, 212}
    assert all(job.consumer_requests == 2 for job in random_jobs)
    assert degree_job.consumer_requests == 4
    assert pagerank_job.consumer_requests == 4
    assert degree_job.recipe.fields["selector_parameters"] == {}
    assert degree_job.recipe.fields["selector_algorithm_version"] == (
        producer_module.DEGREE_ALGORITHM_VERSION
    )
    assert pagerank_job.recipe.fields["selector_parameters"] == {
        "pagerank_alpha": 0.85
    }

    torch.manual_seed(991)
    rng_before = torch.get_rng_state().clone()
    first = random_jobs[0].producer()
    rng_after = torch.get_rng_state().clone()
    second = random_jobs[0].producer()
    assert first == second
    assert torch.equal(rng_before, rng_after)
    assert torch.equal(rng_before, torch.get_rng_state())
    assert random_jobs[0].recipe.recipe_hash != random_jobs[1].recipe.recipe_hash
    assert degree_job.recipe.recipe_hash != pagerank_job.recipe.recipe_hash


def test_degree_producer_has_explicit_portable_tie_break():
    inputs = _fixture_inputs()
    producer = producer_module.build_degree_producer(inputs, 2)
    assert producer() == (1, 2)
    assert producer() == (1, 2)
    assert producer_module.DEGREE_ALGORITHM_VERSION.endswith("node-id-asc-v2")


def test_simple_producers_cold_warm_and_read_only_legacy_comparison(
    tmp_path, fake_producer_layer
):
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42, 212],
        methods=["GIF"],
    )
    processed_root, legacy_root = _prepare_roots(tmp_path)
    store_root = (tmp_path / "v2-store").resolve()
    plan = producer_module.prepare_selection_plan(
        config, processed_root, dataset_inputs=fake_producer_layer
    )
    legacy_states = {}
    for position, job in enumerate(plan.jobs):
        selected_nodes = list(job.producer())
        legacy_file = legacy_root / "selection_cache" / "legacy-{0}.json".format(position)
        legacy_file.write_text(
            json.dumps(
                {
                    "cache_key": "legacy-{0}".format(position),
                    "config": {
                        "dataset_name": "cora",
                        "base_model": "GCN",
                        "unlearn_ratio": 0.5,
                        "seed": job.legacy_seed,
                        "strategy_name": job.strategy,
                        "k": job.k,
                        "graph_fingerprint": job.inputs.dataset.legacy_graph_fingerprint,
                        "strategy_params_fingerprint": producer_module._stable_hash32(
                            job.legacy_strategy_parameters
                        ),
                    },
                    "selection_result": {
                        "strategy_name": job.strategy,
                        "selected_nodes": selected_nodes,
                    },
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        legacy_states[legacy_file] = _file_state(legacy_file)

    cold = producer_module.materialize_selection(
        config,
        processed_root,
        store_root,
        legacy_root,
        verify=True,
        compare_legacy=True,
        dataset_inputs=fake_producer_layer,
    )
    assert len(cold["results"]) == 4
    assert all(not item["hit"] for item in cold["results"])
    assert all(item["producer_called"] for item in cold["results"])
    assert all(item["verification"]["hit"] for item in cold["results"])
    assert all(
        item["legacy_comparison"]["status"] == "exact_order_match"
        for item in cold["results"]
    )
    first_ids = {item["recipe_hash"]: item["artifact_id"] for item in cold["results"]}
    first_mtimes = {
        item["recipe_hash"]: Path(item["payload_path"]).stat().st_mtime_ns
        for item in cold["results"]
    }

    warm = producer_module.materialize_selection(
        config,
        processed_root,
        store_root,
        legacy_root,
        fail_if_producer_called=True,
        compare_legacy=True,
        dataset_inputs=fake_producer_layer,
    )
    assert all(item["hit"] and not item["producer_called"] for item in warm["results"])
    assert {item["recipe_hash"]: item["artifact_id"] for item in warm["results"]} == first_ids
    assert all(
        Path(item["payload_path"]).stat().st_mtime_ns
        == first_mtimes[item["recipe_hash"]]
        for item in warm["results"]
    )
    assert all(_file_state(path) == state for path, state in legacy_states.items())


def test_authoritative_simple_strategy_classes_materialize_fixture_graph(tmp_path):
    inputs = _fixture_inputs()
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42],
        methods=["GIF"],
    )
    processed_root, legacy_root = _prepare_roots(tmp_path)
    store_root = (tmp_path / "actual-strategy-store").resolve()
    cold = producer_module.materialize_selection(
        config,
        processed_root,
        store_root,
        legacy_root,
        verify=True,
        include_nodes=True,
        dataset_inputs=inputs,
    )
    assert {item["strategy"] for item in cold["results"]} == {
        "random",
        "degree",
        "pagerank",
    }
    assert all(item["selected_node_count"] == 2 for item in cold["results"])
    assert all(
        item["verification"]["producer_called"] is False
        for item in cold["results"]
    )
    warm = producer_module.materialize_selection(
        config,
        processed_root,
        store_root,
        legacy_root,
        fail_if_producer_called=True,
        dataset_inputs=inputs,
    )
    assert all(item["hit"] and not item["producer_called"] for item in warm["results"])


def test_processed_provider_reads_open_gu_pickle_without_split_construction(tmp_path):
    data = Data(
        x=torch.ones((3, 2)),
        y=torch.tensor([0, 1, 0]),
        edge_index=torch.tensor([[0, 1, 2], [1, 2, 0]], dtype=torch.long),
        num_nodes=3,
        train_mask=torch.tensor([True, False, True]),
        train_indices=torch.tensor([0, 2]),
    )
    marker = tmp_path / "transductive" / "cora0.8_0_0.2.pkl"
    marker.parent.mkdir(parents=True)
    with marker.open("wb") as handle:
        pickle.dump(data, handle)
    before = _file_state(marker)
    inputs = input_module.load_processed_selection_inputs(
        processed_root=tmp_path,
        dataset_name="cora",
        train_ratio=0.8,
        val_ratio=0.0,
        test_ratio=0.2,
        is_transductive=True,
        is_balanced=False,
    )
    assert inputs.num_nodes == 3
    assert inputs.candidate_nodes == (0, 2)
    assert _file_state(marker) == before


def test_cachectl_materialize_requires_explicit_apply(tmp_path, capsys):
    store_root = (tmp_path / "store").resolve()
    rc = cachectl.main(
        [
            "selection",
            "materialize",
            "--config",
            str(tmp_path / "missing.yaml"),
            "--store-root",
            str(store_root),
        ]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert "apply_required" in captured.err
    assert not store_root.exists()
