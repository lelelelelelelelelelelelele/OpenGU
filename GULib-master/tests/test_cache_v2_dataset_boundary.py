"""Cache V2 must not own dataset loading, split construction, or Selection compute."""

from __future__ import annotations

import ast
import pickle
from dataclasses import replace
from pathlib import Path

import pytest
import torch
from torch_geometric.data import Data

from cache_v2 import ArtifactRecipe, ProducerVersion
from cache_v2.errors import ContractValidationError


def _canonical_cora_fixture() -> Data:
    num_nodes = 2708
    edge_count = 10556
    edge_ids = torch.arange(edge_count, dtype=torch.long)
    source = edge_ids // num_nodes
    target = edge_ids % num_nodes
    train_count = int(0.8 * num_nodes)
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:train_count] = True
    return Data(
        x=torch.arange(num_nodes * 4, dtype=torch.float32).reshape(num_nodes, 4),
        y=torch.arange(num_nodes, dtype=torch.long) % 7,
        edge_index=torch.stack((source, target)),
        train_mask=train_mask,
        train_indices=torch.arange(train_count, dtype=torch.long),
        num_nodes=num_nodes,
    )


def _producer_version(name: str = "fixture-selection-v2") -> ProducerVersion:
    return ProducerVersion(
        semantic_version=name,
        source_fingerprint="a" * 64,
    )


def _selection_inputs(*, strategy: str = "degree", seed: int = 42, k: int = 3):
    from experiments.selection_inputs import make_dataset_selection_inputs
    from experiments.selection_producer import SelectionInputs

    dataset_inputs = make_dataset_selection_inputs(
        _canonical_cora_fixture(), dataset_name="cora"
    )
    return SelectionInputs(
        dataset=dataset_inputs,
        strategy=strategy,
        seed=seed,
        k=k,
        producer_version=_producer_version(),
        algorithm_version="fixture-degree-v1",
        parameters={},
    )


def test_cache_v2_has_no_dataset_or_selector_dependencies():
    from cache_v2.store import ArtifactStore

    cache_root = Path(__file__).resolve().parents[1] / "cache_v2"
    forbidden_roots = {
        "dataset",
        "experiments",
        "ogb",
        "torch",
        "torch_geometric",
        "yaml",
    }
    violations = []
    for path in sorted(cache_root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules = [node.module]
            for module in modules:
                if module.split(".", 1)[0] in forbidden_roots:
                    violations.append((path.name, module))
    assert violations == []

    materializer = (cache_root / "selection_materializer.py").read_text(
        encoding="utf-8"
    )
    assert "dataset_root" not in materializer
    assert "allow_download" not in materializer
    assert "Planetoid" not in materializer
    assert "PygNodePropPredDataset" not in materializer
    assert not hasattr(ArtifactStore, "get_or_compute")
    assert not hasattr(ArtifactStore, "observe_recomputation")


def test_processed_provider_uses_canonical_cora_pickle_without_rebuilding_split(
    tmp_path,
):
    from experiments.selection_inputs import load_processed_selection_inputs

    data = _canonical_cora_fixture()
    expected_candidates = tuple(data.train_indices.tolist())
    processed = tmp_path / "transductive" / "cora0.8_0_0.2.pkl"
    processed.parent.mkdir(parents=True)
    with processed.open("wb") as handle:
        pickle.dump(data, handle)

    loaded = load_processed_selection_inputs(
        processed_root=tmp_path,
        dataset_name="cora",
        train_ratio=0.8,
        val_ratio=0.0,
        test_ratio=0.2,
        is_transductive=True,
        is_balanced=False,
    )

    assert loaded.source_path == processed.resolve()
    assert loaded.num_nodes == 2708
    assert loaded.edge_index.shape == (2, 10556)
    assert loaded.candidate_nodes == expected_candidates
    assert loaded.edge_index.device.type == "cpu"
    assert len(loaded.dataset_fingerprint) == 64
    assert len(loaded.candidate_set_hash) == 64


def test_recipe_binds_dataset_candidates_strategy_seed_k_and_producer_version():
    from experiments.selection_producer import build_selection_job

    inputs = _selection_inputs()
    job = build_selection_job(inputs, producer=lambda: (0, 1, 2))
    fields = job.recipe.fields

    assert fields["selection_recipe_contract"] == "opengu-selection-recipe-v2"
    assert fields["dataset_fingerprint"] == inputs.dataset.dataset_fingerprint
    assert fields["candidate_set_hash"] == inputs.dataset.candidate_set_hash
    assert fields["selector"] == "degree"
    assert fields["selector_seed"] == 42
    assert fields["k"] == 3
    assert fields["producer_version"] == inputs.producer_version.to_dict()

    changed = replace(
        inputs,
        producer_version=_producer_version("fixture-selection-v3"),
    )
    changed_job = build_selection_job(changed, producer=lambda: (0, 1, 2))
    assert changed_job.recipe.recipe_hash != job.recipe.recipe_hash


def test_selection_recipe_can_bind_an_explicit_source_score_artifact():
    from cache_v2.selection_materializer import (
        SelectionArtifactRequest,
        build_selection_recipe,
    )

    inputs = _selection_inputs()
    common = {
        "dataset_fingerprint": inputs.dataset.dataset_fingerprint,
        "graph_fingerprint": inputs.dataset.graph_fingerprint,
        "candidate_set_hash": inputs.dataset.candidate_set_hash,
        "num_nodes": inputs.dataset.num_nodes,
        "candidate_count": inputs.dataset.candidate_count,
        "node_id_space": inputs.dataset.node_id_space,
        "strategy": inputs.strategy,
        "seed": inputs.seed,
        "k": inputs.k,
        "producer_version": inputs.producer_version,
        "algorithm_version": inputs.algorithm_version,
        "parameters": inputs.parameters,
    }
    recipe = build_selection_recipe(
        **common,
        source_score_artifact_id="score_11111111_22222222",
    )

    assert (
        recipe.fields["source_score_artifact_id"]
        == "score_11111111_22222222"
    )
    SelectionArtifactRequest.from_recipe(recipe, inputs.producer_version)

    with pytest.raises(ContractValidationError, match="Score Artifact"):
        build_selection_recipe(
            **common,
            source_score_artifact_id="sel_11111111_22222222",
        )


def test_cache_hit_does_not_call_dataset_provider_or_selection_producer(
    tmp_path, monkeypatch
):
    from cache_v2.selection_materializer import (
        SelectionArtifactRequest,
        resolve_selection_artifact,
        store_selection_artifact,
    )
    from experiments.selection_producer import build_selection_job

    calls = []

    def forbidden(*_args, **_kwargs):
        calls.append("forbidden")
        raise AssertionError("dataset/producer path was called during Cache HIT")

    import experiments.selection_inputs as input_module

    monkeypatch.setattr(input_module, "load_processed_selection_inputs", forbidden)
    inputs = _selection_inputs()
    job = build_selection_job(inputs, producer=forbidden)
    request = SelectionArtifactRequest.from_recipe(
        job.recipe, inputs.producer_version
    )
    store_root = tmp_path.resolve() / "store"
    stored = store_selection_artifact(
        store_root,
        request,
        selected_nodes=(0, 1, 2),
        compute_seconds=0.0,
    )
    assert stored.hit is False

    hit = resolve_selection_artifact(store_root, request)
    assert hit.hit is True
    assert hit.result is not None
    assert hit.result.payload.selected_nodes_ordered == (0, 1, 2)
    assert calls == []


def test_miss_is_computed_only_by_injected_experiment_producer(tmp_path):
    from experiments.selection_producer import (
        build_selection_job,
        resolve_or_produce_selection,
    )

    calls = []

    def producer():
        calls.append("producer")
        return (0, 1, 2)

    inputs = _selection_inputs()
    job = build_selection_job(inputs, producer=producer)
    store_root = tmp_path.resolve() / "store"

    cold = resolve_or_produce_selection(job, store_root)
    assert calls == ["producer"]
    assert cold.hit is False
    assert cold.producer_called is True

    warm_job = build_selection_job(
        inputs,
        producer=lambda: (_ for _ in ()).throw(
            AssertionError("producer called on warm hit")
        ),
    )
    warm = resolve_or_produce_selection(
        warm_job,
        store_root,
        fail_if_producer_called=True,
    )
    assert warm.hit is True
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id


def test_new_materializer_rejects_legacy_recipe_without_identity_boundary():
    from cache_v2.selection_materializer import SelectionArtifactRequest

    legacy = ArtifactRecipe(
        {
            "graph_fingerprint": "1" * 64,
            "candidate_set_hash": "2" * 64,
            "node_id_space": "pyg-global-node-index-v1",
            "selector": "degree",
            "selector_algorithm_version": "legacy-degree-v1",
            "k": 3,
        }
    )
    with pytest.raises(ContractValidationError, match="selection recipe contract"):
        SelectionArtifactRequest.from_recipe(legacy, _producer_version())


def test_runner_rejects_removed_cache_dataset_options(tmp_path):
    import experiments.run as runner

    base = {
        "strategies": ["degree"],
        "cache_v2": {"mode": "selection", "store_root": str(tmp_path / "store")},
    }
    settings = runner.cache_v2_settings(base)
    assert settings is not None
    assert "dataset_root" not in settings
    assert "allow_download" not in settings

    for key, value in (("dataset_root", "data/raw"), ("allow_download", True)):
        cfg = {"strategies": ["degree"], "cache_v2": dict(base["cache_v2"])}
        cfg["cache_v2"][key] = value
        with pytest.raises(ValueError, match=key):
            runner.cache_v2_settings(cfg)


def test_runner_target_direct_mode_requires_manifest_digest(tmp_path):
    import experiments.run as runner

    cfg = {
        "strategies": ["degree"],
        "cache_v2": {
            "mode": "target_direct_external_selection",
            "store_root": str(tmp_path / "store"),
            "manifest_path": str(tmp_path / "manifest.json"),
        },
    }
    with pytest.raises(ValueError, match="manifest_sha256"):
        runner.cache_v2_settings(cfg)
    cfg["cache_v2"]["manifest_sha256"] = "a" * 64
    settings = runner.cache_v2_settings(cfg)
    assert settings["mode"] == "target_direct_external_selection"
    assert settings["manifest_sha256"] == "a" * 64


def test_dataset_decoupling_markdown_and_html_agree_on_verdict_and_evidence():
    root = Path(__file__).resolve().parents[1]
    markdown = (
        root / "docs" / "cache_v2_dataset_decoupling_ACCEPTANCE_REPORT.md"
    ).read_text(encoding="utf-8")
    browser = (
        root / "report" / "cache_v2_dataset_decoupling_ACCEPTANCE_REPORT.html"
    ).read_text(encoding="utf-8")
    for expected in (
        "ACCEPTED",
        "2708",
        "10556",
        "2166",
        "sel_04fe0b95_82b98325",
        "118",
        "500",
        "3 deselected",
        "Server",
        "非阻塞 TODO",
    ):
        assert expected in markdown
        assert expected in browser
