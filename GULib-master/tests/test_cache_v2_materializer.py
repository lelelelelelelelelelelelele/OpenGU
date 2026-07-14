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
