"""CPU fixtures for the isolated real-data Selection V2 canary CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from cache_v2 import ProducerVersion
from cache_v2.errors import ContractValidationError, PathValidationError
from scripts import cache_v2_selection_canary as canary


def _inputs():
    # Deliberately unsorted with one duplicate edge. Canonicalization must make
    # this representation-independent before either hashing or production.
    edge_index = torch.tensor(
        [[3, 0, 1, 0, 2, 0], [0, 1, 2, 1, 3, 2]], dtype=torch.long
    )
    return canary.make_selection_inputs(edge_index, 4, [3, 1, 0, 2])


def _parameters():
    return canary.ImParameters(
        propagation_prob=0.1,
        mc_rounds=2,
        candidate_fraction=1.0,
        im_selector_seed=42,
        im_batch_size=1,
        parallel_mc=False,
    )


def test_recipe_uses_only_artifact_inputs_and_is_order_stable():
    first = _inputs()
    reordered = canary.make_selection_inputs(
        first.edge_index[:, torch.tensor([3, 1, 4, 0, 2])],
        first.num_nodes,
        list(reversed(first.candidate_nodes)),
    )

    assert reordered.graph_fingerprint == first.graph_fingerprint
    assert reordered.candidate_set_hash == first.candidate_set_hash

    recipe = canary.build_selection_recipe(first, 2, _parameters(), has_numba=True)
    changed_envelope = canary.build_request_envelope(
        "renamed-config", "elsewhere/renamed.yaml", "different-exp", 0.5
    )
    original_envelope = canary.build_request_envelope(
        "phase-a", "experiments/a.yaml", "exp-a", 0.5
    )

    assert recipe.fields.keys() == {
        "graph_fingerprint",
        "candidate_set_hash",
        "node_id_space",
        "selector",
        "selector_algorithm_version",
        "k",
        "im_parameters",
    }
    assert changed_envelope != original_envelope
    assert "config_name" not in recipe.fields
    assert "yaml_path" not in recipe.fields
    assert "experiment_id" not in recipe.fields
    assert "dataset" not in recipe.fields
    assert "model" not in recipe.fields

    # Request-envelope labels cannot change Artifact identity.
    rebuilt = canary.build_selection_recipe(first, 2, _parameters(), has_numba=True)
    assert rebuilt.recipe_hash == recipe.recipe_hash


def test_python_fallback_has_a_distinct_algorithm_and_ignores_unused_batch_size():
    inputs = _inputs()
    first = _parameters()
    second = canary.ImParameters(
        propagation_prob=first.propagation_prob,
        mc_rounds=first.mc_rounds,
        candidate_fraction=first.candidate_fraction,
        im_selector_seed=first.im_selector_seed,
        im_batch_size=99,
        parallel_mc=first.parallel_mc,
    )

    python_first = canary.build_selection_recipe(
        inputs, 2, first, has_numba=False
    )
    python_second = canary.build_selection_recipe(
        inputs, 2, second, has_numba=False
    )
    numba = canary.build_selection_recipe(inputs, 2, first, has_numba=True)

    assert python_first.recipe_hash == python_second.recipe_hash
    assert "im_batch_size" not in python_first.fields["im_parameters"]
    assert (
        python_first.fields["selector_algorithm_version"]
        == canary.PYTHON_SELECTOR_ALGORITHM_VERSION
    )
    assert numba.recipe_hash != python_first.recipe_hash
    assert (
        numba.fields["selector_algorithm_version"]
        == canary.NUMBA_SELECTOR_ALGORITHM_VERSION
    )


def test_seed42_split_matches_opengu_80_0_20_without_global_rng_side_effect():
    torch.manual_seed(999)
    before = torch.random.get_rng_state().clone()
    candidates = canary.opengu_train_candidates(10, split_seed=42)
    after = torch.random.get_rng_state()

    expected = torch.randperm(10, generator=torch.Generator().manual_seed(42))[:8]
    assert candidates == tuple(sorted(expected.tolist()))
    assert len(candidates) == 8
    assert torch.equal(before, after)


def test_im_producer_disables_both_legacy_score_cache_layers():
    captured = {}

    class FakeImStrategy:
        def __init__(self, args):
            captured.update(args)
            self._score_cache = None
            self._celf_cache = None

        def compute_im_celf(self, edge_index, num_nodes, k, candidates):
            assert edge_index.device.type == "cpu"
            assert candidates == sorted(candidates)
            return candidates[-k:], torch.ones(k)

    producer = canary.build_im_producer(
        _inputs(), 2, _parameters(), FakeImStrategy
    )

    assert list(producer()) == [2, 3]
    assert captured["enable_score_cache"] is False
    assert "score_cache_dir" not in captured


def test_cold_then_warm_use_independent_store_instances_and_preserve_payload(
    tmp_path,
):
    inputs = _inputs()
    parameters = _parameters()
    recipe = canary.build_selection_recipe(inputs, 2, parameters, has_numba=True)
    producer_version = ProducerVersion(
        semantic_version="fixture-v1", source_fingerprint="fixture-source"
    )
    store_root = (tmp_path / "store").absolute()
    cold_envelope = canary.build_request_envelope(
        "cold-config", "cold.yaml", "cold-exp", 0.5
    )
    warm_envelope = canary.build_request_envelope(
        "renamed-config", "warm.yaml", "warm-exp", 0.5
    )

    cold, _ = canary.run_store_phase(
        "cold",
        store_root,
        recipe,
        lambda: [3, 1],
        inputs,
        producer_version,
        cold_envelope,
    )
    payload_path = store_root.joinpath(*Path(cold.semantic_path).parts)
    before = (
        payload_path.read_bytes(),
        payload_path.stat().st_mtime_ns,
        payload_path.stat().st_size,
    )

    # run_store_phase constructs a new ArtifactStore, matching a second CLI
    # process. The warm sentinel would raise if resolution called this lambda.
    warm, _ = canary.run_store_phase(
        "warm",
        store_root,
        recipe,
        lambda: (_ for _ in ()).throw(AssertionError("producer called")),
        inputs,
        producer_version,
        warm_envelope,
    )
    after = (
        payload_path.read_bytes(),
        payload_path.stat().st_mtime_ns,
        payload_path.stat().st_size,
    )

    assert cold.hit is False
    assert cold.producer_called is True
    assert warm.hit is True
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id
    assert warm.content_hash == cold.content_hash
    assert warm.payload.selected_nodes_ordered == (3, 1)
    assert after == before

    with pytest.raises(RuntimeError, match="fresh store"):
        canary.run_store_phase(
            "cold",
            store_root,
            recipe,
            lambda: [3, 1],
            inputs,
            producer_version,
            cold_envelope,
        )


def test_legacy_snapshot_and_store_root_guard_are_fail_closed(tmp_path):
    legacy_roots = tuple(
        (tmp_path / name).absolute()
        for name in ("cache", "selection_cache", "score_cache")
    )
    for position, root in enumerate(legacy_roots):
        root.mkdir()
        (root / "sentinel.json").write_text(
            json.dumps({"position": position}), encoding="utf-8"
        )
    before, counts = canary.legacy_cache_state(legacy_roots)
    assert counts == {root.name: 1 for root in legacy_roots}
    assert canary.legacy_cache_state(legacy_roots)[0] == before

    with pytest.raises(PathValidationError, match="Legacy cache"):
        canary.validate_isolated_store_root(
            legacy_roots[0] / "nested", legacy_roots
        )
    isolated = canary.validate_isolated_store_root(
        (tmp_path / "isolated").absolute(), legacy_roots
    )
    assert isolated == (tmp_path / "isolated").absolute()


def test_execute_rejects_dataset_root_inside_legacy_results(tmp_path):
    parser = canary._parser()
    legacy_results = (tmp_path / "results").absolute()
    args = parser.parse_args(
        [
            "cold",
            "--store-root",
            str((tmp_path / "store").absolute()),
            "--dataset-root",
            str(legacy_results / "dataset"),
            "--legacy-results-root",
            str(legacy_results),
            "--allow-download",
        ]
    )

    with pytest.raises(PathValidationError, match="Legacy results"):
        canary.execute(args)


def test_dataset_validation_uses_the_same_lowercase_planetoid_path(tmp_path):
    dataset_root = (tmp_path / "raw").absolute()
    processed = dataset_root / canary.DATASET_NAME / "processed" / "data.pt"
    processed.parent.mkdir(parents=True)
    processed.write_bytes(b"fixture")

    assert canary.validate_dataset_root(dataset_root, allow_download=False) == dataset_root


@pytest.mark.parametrize("value", [[1.0], [True], [-1], [4]])
def test_candidate_contract_rejects_non_integer_or_out_of_range(value):
    with pytest.raises(ContractValidationError):
        canary.canonical_candidate_nodes(value, num_nodes=4)
