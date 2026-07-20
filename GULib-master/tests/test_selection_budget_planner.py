import hashlib
from pathlib import Path

import pytest
import torch

from cache_v2 import ProducerVersion
from cache_v2.errors import ContractValidationError
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import (
    DatasetSelectionInputs,
    candidate_fingerprint,
)
from experiments.selection_producer import UpstreamProducerCalledError


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _dataset():
    candidates = tuple(range(20))
    return DatasetSelectionInputs(
        dataset_name="fixture",
        edge_index=torch.tensor([[0, 1], [1, 0]], dtype=torch.long),
        num_nodes=20,
        candidate_nodes=candidates,
        dataset_fingerprint=_sha("dataset"),
        graph_fingerprint=_sha("graph"),
        candidate_set_hash=candidate_fingerprint(candidates, 20),
        legacy_graph_fingerprint="fixture-legacy",
    )


def _producer_version():
    return ProducerVersion(
        semantic_version="fixture-maxk-v1",
        source_fingerprint=_sha("producer"),
    )


def _materialize(root, budgets, producer, **overrides):
    arguments = {
        "store_root": Path(root).resolve(),
        "dataset": _dataset(),
        "strategy": "gt_full",
        "selector_seed": 42,
        "budgets": budgets,
        "producer_version": _producer_version(),
        "algorithm_version": "fixture-ranking-v1",
        "parameters": {
            "prefix_stable": True,
            "score_name": "gt_full",
            "ranking": "score_desc_node_id_asc",
        },
        "source_score_artifact_id": "score_11111111_22222222",
        "producer": producer,
    }
    arguments.update(overrides)
    return materialize_budget_selection(**arguments)


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


def test_cold_group_computes_max_once_and_fans_out_prefixes(tmp_path):
    calls = []

    def producer(k):
        calls.append(k)
        return tuple(range(19, 19 - k, -1))

    result = _materialize(tmp_path / "store", (3, 14, 7, 3), producer)

    assert calls == [14]
    assert result.budgets_descending == (14, 7, 3)
    assert result.request_max_k == result.artifact_k == 14
    assert result.cache_hit is False
    assert result.producer_called is True
    assert result.views["14"]["cache_outcome"] == "cache_miss_saved"
    assert result.views["14"]["prefix_reuse"] is False
    assert result.views["7"]["cache_outcome"] == "same_run_prefix_reuse"
    assert result.views["7"]["selected_nodes"] == list(range(19, 12, -1))


def test_warm_group_checks_max_once_and_is_zero_write(tmp_path):
    root = tmp_path / "store"
    cold = _materialize(root, (3, 7, 14), lambda k: tuple(range(k)))
    before = _file_state(root)

    warm = _materialize(
        root,
        (3, 7, 14),
        lambda _k: (_ for _ in ()).throw(AssertionError("producer called")),
        fail_if_producer_called=True,
    )

    assert warm.cache_hit is True
    assert warm.producer_called is False
    assert warm.artifact_k == 14
    assert warm.result.artifact_id == cold.result.artifact_id
    assert warm.views["14"]["cache_outcome"] == "cache_hit"
    assert warm.views["7"]["cache_outcome"] == "cache_hit_prefix_reuse"
    assert _file_state(root) == before


def test_smaller_future_request_reuses_smallest_covering_artifact(tmp_path):
    root = tmp_path / "store"
    k10 = _materialize(root, (10,), lambda k: tuple(range(k)))
    calls = []
    k14 = _materialize(
        root, (14,), lambda k: calls.append(k) or tuple(range(k))
    )
    assert calls == [14]
    assert k14.cache_hit is False

    covered = _materialize(
        root,
        (3, 7),
        lambda _k: (_ for _ in ()).throw(AssertionError("producer called")),
        fail_if_producer_called=True,
    )

    assert covered.cache_hit is True
    assert covered.request_max_k == 7
    assert covered.artifact_k == 10
    assert covered.result.artifact_id == k10.result.artifact_id
    assert covered.views["7"]["reuse_kind"] == "cache_artifact_prefix"


def test_exact_k_is_preferred_over_a_larger_covering_artifact(tmp_path):
    root = tmp_path / "store"
    exact = _materialize(root, (7,), lambda k: tuple(range(k)))
    _materialize(root, (14,), lambda k: tuple(range(k)))

    resolved = _materialize(
        root,
        (3, 7),
        lambda _k: (_ for _ in ()).throw(AssertionError("producer called")),
        fail_if_producer_called=True,
    )

    assert resolved.artifact_k == 7
    assert resolved.result.artifact_id == exact.result.artifact_id
    assert resolved.views["7"]["prefix_reuse"] is False


def test_identity_change_does_not_reuse_covering_artifact(tmp_path):
    root = tmp_path / "store"
    _materialize(root, (14,), lambda k: tuple(range(k)))
    calls = []
    changed = _materialize(
        root,
        (3, 7),
        lambda k: calls.append(k) or tuple(range(k)),
        selector_seed=43,
    )

    assert calls == [7]
    assert changed.cache_hit is False
    assert changed.artifact_k == 7


def test_prefix_reuse_requires_explicit_stability_contract(tmp_path):
    with pytest.raises(ContractValidationError, match="prefix_stable"):
        _materialize(
            tmp_path / "store",
            (3, 7),
            lambda k: tuple(range(k)),
            parameters={"prefix_stable": False, "score_name": "gt_full"},
        )


def test_fail_if_called_rejects_a_true_maxk_miss(tmp_path):
    with pytest.raises(UpstreamProducerCalledError, match="k=7"):
        _materialize(
            tmp_path / "store",
            (3, 7),
            lambda k: tuple(range(k)),
            fail_if_producer_called=True,
        )
