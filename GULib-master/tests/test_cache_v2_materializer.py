import hashlib
import json
from pathlib import Path

import pytest
import torch
from torch_geometric.data import Data

import cache_v2.selection_materializer as materializer
from scripts import cachectl


class FakeImStrategy:
    calls = 0

    def __init__(self, args):
        assert args["enable_score_cache"] is False
        self._score_cache = None
        self._celf_cache = None

    def compute_im_celf(self, edge_index, num_nodes, k, candidate_set):
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

    def select_nodes(self, data, model, k):
        del model
        return data.train_indices.flip(0)[:k]


class FakePageRankStrategy:
    def __init__(self, args):
        self.alpha = float(args["pagerank_alpha"])

    def select_nodes(self, data, model, k):
        del model
        candidates = data.train_indices
        return candidates[torch.argsort(candidates.float() * self.alpha, descending=True)[:k]]


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
    return materializer.make_selection_inputs(edge_index, 5, [0, 1, 2, 3])


def _prepare_roots(tmp_path):
    dataset_root = tmp_path / "dataset"
    marker = dataset_root / "cora" / "processed" / "data.pt"
    marker.parent.mkdir(parents=True)
    marker.write_bytes(b"fixture")
    legacy_root = tmp_path / "legacy-results"
    for name in ("cache", "selection_cache", "score_cache"):
        (legacy_root / name).mkdir(parents=True)
    return dataset_root.resolve(), legacy_root.resolve()


@pytest.fixture
def fake_materializer(monkeypatch):
    inputs = _fixture_inputs()
    FakeImStrategy.calls = 0
    monkeypatch.setattr(
        materializer,
        "load_selection_inputs",
        lambda dataset_name, dataset_root, split_seed, train_ratio: inputs,
    )
    monkeypatch.setattr(
        materializer,
        "load_im_strategy",
        lambda: (FakeImStrategy, True, Path(materializer.__file__).resolve()),
    )
    simple_classes = {
        "random": FakeRandomStrategy,
        "degree": FakeDegreeStrategy,
        "pagerank": FakePageRankStrategy,
    }
    monkeypatch.setattr(
        materializer,
        "load_simple_strategy",
        lambda strategy: (
            simple_classes[strategy],
            Path(materializer.__file__).resolve(),
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
    tmp_path, fake_materializer
):
    config = _write_config(tmp_path)
    dataset_root, legacy_root = _prepare_roots(tmp_path)

    plan = materializer.prepare_selection_plan(
        config, dataset_root, legacy_root
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
    assert fields["im_parameters"]["candidate_fraction"] == 0.5
    assert fields["im_parameters"]["mc_rounds"] == 7
    assert fields["im_parameters"]["im_batch_size"] == 1
    serialized = json.dumps(plan.jobs[0].recipe.to_dict(), sort_keys=True)
    for forbidden in ("fixture_request", "request.yaml", "base_model", "GIF", "212"):
        assert forbidden not in serialized


def test_selection_plan_is_zero_write_for_store_and_legacy(
    tmp_path, fake_materializer
):
    config = _write_config(tmp_path, strategies=["im", "tracin"])
    dataset_root, legacy_root = _prepare_roots(tmp_path)
    legacy_file = legacy_root / "selection_cache" / "sentinel.json"
    legacy_file.write_text('{"sentinel":true}', encoding="utf-8")
    legacy_before = _file_state(legacy_file)
    store_root = (tmp_path / "v2-store").resolve()

    document = materializer.plan_selection(
        config, dataset_root, store_root, legacy_root
    )

    assert document["execution_performed"] is False
    assert document["producer_calls"] == 0
    assert document["writes"] == []
    assert document["store_unchanged"] is True
    assert document["legacy_cache_unchanged"] is True
    assert document["resolutions"][0]["miss_reasons"] == [
        "store_not_initialized"
    ]
    assert not store_root.exists()
    assert _file_state(legacy_file) == legacy_before
    assert FakeImStrategy.calls == 0


def test_plan_registers_simple_producers_with_minimal_identity_and_seed_scope(
    tmp_path, fake_materializer
):
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42, 212],
    )
    dataset_root, legacy_root = _prepare_roots(tmp_path)

    plan = materializer.prepare_selection_plan(config, dataset_root, legacy_root)
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
    assert {job.recipe.fields["random_parameters"]["seed"] for job in random_jobs} == {
        42,
        212,
    }
    assert all(job.consumer_requests == 2 for job in random_jobs)
    assert degree_job.consumer_requests == 4
    assert pagerank_job.consumer_requests == 4
    assert "random_parameters" not in degree_job.recipe.fields
    assert degree_job.recipe.fields["selector_algorithm_version"] == (
        materializer.DEGREE_ALGORITHM_VERSION
    )
    assert pagerank_job.recipe.fields["pagerank_parameters"] == {"alpha": 0.85}

    for job in plan.jobs:
        serialized = json.dumps(job.recipe.to_dict(), sort_keys=True)
        for forbidden in ("fixture_request", "request.yaml", "base_model", "GCN", "GIF", "IDEA"):
            assert forbidden not in serialized

    torch.manual_seed(991)
    rng_before = torch.get_rng_state().clone()
    first = random_jobs[0].producer()
    rng_after = torch.get_rng_state().clone()
    second = random_jobs[0].producer()
    assert first == second
    assert torch.equal(rng_before, rng_after)
    assert torch.equal(rng_before, torch.get_rng_state())
    assert random_jobs[0].recipe.recipe_hash != random_jobs[1].recipe.recipe_hash
    assert materializer.build_pagerank_recipe(
        fake_materializer, 2, 0.85
    ).recipe_hash != materializer.build_pagerank_recipe(
        fake_materializer, 2, 0.9
    ).recipe_hash


def test_degree_producer_has_explicit_portable_tie_break():
    inputs = _fixture_inputs()

    producer = materializer.build_degree_producer(inputs, 2)

    # Nodes 1, 2, and 3 all have degree 2.  The k-boundary is resolved by the
    # documented global node-id ascending order, independent of torch.topk.
    assert producer() == (1, 2)
    assert producer() == (1, 2)
    assert materializer.DEGREE_ALGORITHM_VERSION.endswith("node-id-asc-v2")
    assert materializer.DEGREE_PRODUCER_SEMANTIC_VERSION.endswith("selection-v2")


def test_simple_producers_cold_warm_and_read_only_legacy_comparison(
    tmp_path, fake_materializer
):
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42, 212],
        methods=["GIF"],
    )
    dataset_root, legacy_root = _prepare_roots(tmp_path)
    store_root = (tmp_path / "v2-store").resolve()
    plan = materializer.prepare_selection_plan(config, dataset_root, legacy_root)
    legacy_states = {}
    for position, job in enumerate(plan.jobs):
        selected_nodes = list(job.producer())
        legacy_file = legacy_root / "selection_cache" / "legacy-{0}.json".format(
            position
        )
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
                        "graph_fingerprint": job.inputs.legacy_graph_fingerprint,
                        "strategy_params_fingerprint": materializer._stable_hash32(
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

    cold = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        verify=True,
        compare_legacy=True,
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

    warm = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        fail_if_producer_called=True,
        compare_legacy=True,
    )
    assert len(warm["results"]) == 4
    assert all(item["hit"] for item in warm["results"])
    assert all(not item["producer_called"] for item in warm["results"])
    assert {
        item["recipe_hash"]: item["artifact_id"] for item in warm["results"]
    } == first_ids
    assert all(
        Path(item["payload_path"]).stat().st_mtime_ns
        == first_mtimes[item["recipe_hash"]]
        for item in warm["results"]
    )
    assert all(_file_state(path) == state for path, state in legacy_states.items())


def test_authoritative_simple_strategy_classes_materialize_fixture_graph(
    tmp_path, monkeypatch
):
    inputs = _fixture_inputs()
    monkeypatch.setattr(
        materializer,
        "load_selection_inputs",
        lambda dataset_name, dataset_root, split_seed, train_ratio: inputs,
    )
    config = _write_config(
        tmp_path,
        strategies=["random", "degree", "pagerank"],
        seeds=[42],
        methods=["GIF"],
    )
    dataset_root, legacy_root = _prepare_roots(tmp_path)
    store_root = (tmp_path / "actual-strategy-store").resolve()

    cold = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        verify=True,
        include_nodes=True,
    )
    assert {item["strategy"] for item in cold["results"]} == {
        "random",
        "degree",
        "pagerank",
    }
    assert all(item["selected_node_count"] == 2 for item in cold["results"])
    assert all(item["verification"]["producer_called"] is False for item in cold["results"])

    warm = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        fail_if_producer_called=True,
    )
    assert all(item["hit"] and not item["producer_called"] for item in warm["results"])


def test_processed_planetoid_loader_is_read_only_and_does_not_nest_root(tmp_path):
    dataset_root = (tmp_path / "dataset").resolve()
    marker = dataset_root / "cora" / "processed" / "data.pt"
    marker.parent.mkdir(parents=True)
    data = Data(
        edge_index=torch.tensor([[0, 1, 2], [1, 2, 0]], dtype=torch.long),
        num_nodes=3,
    )
    torch.save((data, None), marker)
    before = materializer._tree_metadata_snapshot(dataset_root / "cora")

    inputs = materializer.load_selection_inputs("cora", dataset_root, 42, 2.0 / 3.0)

    after = materializer._tree_metadata_snapshot(dataset_root / "cora")
    assert inputs.num_nodes == 3
    assert len(inputs.candidate_nodes) == 2
    assert before == after
    assert not (dataset_root / "cora" / "cora").exists()


def test_materialize_cold_warm_verify_and_legacy_exact_comparison(
    tmp_path, fake_materializer
):
    config = _write_config(tmp_path, strategies=["im", "tracin"], seeds=[42, 212])
    dataset_root, legacy_root = _prepare_roots(tmp_path)
    store_root = (tmp_path / "v2-store").resolve()
    prepared = materializer.prepare_selection_plan(
        config, dataset_root, legacy_root
    )
    job = prepared.jobs[0]
    legacy_file = legacy_root / "selection_cache" / "legacy-im.json"
    legacy_file.write_text(
        json.dumps(
            {
                "cache_key": "legacy-im",
                "config": {
                    "dataset_name": "cora",
                    "base_model": "GCN",
                    "unlearn_ratio": 0.5,
                    "seed": 2024,
                    "strategy_name": "im",
                    "k": 2,
                    "graph_fingerprint": job.inputs.legacy_graph_fingerprint,
                    "strategy_params_fingerprint": materializer._legacy_im_parameter_fingerprint(
                        job.parameters
                    ),
                },
                "selection_result": {
                    "strategy_name": "im",
                    "selected_nodes": [0, 1],
                },
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    legacy_before = _file_state(legacy_file)

    cold = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        verify=True,
        compare_legacy=True,
    )
    first = cold["results"][0]
    payload_path = Path(first["payload_path"])
    payload_mtime = payload_path.stat().st_mtime_ns

    assert first["hit"] is False
    assert first["producer_called"] is True
    assert first["verification"]["hit"] is True
    assert first["verification"]["producer_called"] is False
    assert first["verification"]["payload_mtime_unchanged"] is True
    assert first["legacy_comparison"]["status"] == "exact_order_match"
    assert first["legacy_comparison"]["authoritative"] is False
    assert first["legacy_comparison"]["used_for_resolution"] is False
    assert cold["legacy_cache_unchanged"] is True
    assert _file_state(legacy_file) == legacy_before
    assert FakeImStrategy.calls == 1

    warm = materializer.materialize_selection(
        config,
        dataset_root,
        store_root,
        legacy_root,
        fail_if_producer_called=True,
        compare_legacy=True,
    )
    second = warm["results"][0]
    assert second["hit"] is True
    assert second["producer_called"] is False
    assert second["artifact_id"] == first["artifact_id"]
    assert second["content_hash"] == first["content_hash"]
    assert payload_path.stat().st_mtime_ns == payload_mtime
    assert FakeImStrategy.calls == 1
    assert _file_state(legacy_file) == legacy_before


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
