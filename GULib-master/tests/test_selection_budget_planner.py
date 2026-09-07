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

@pytest.mark.parametrize('mode,large,small', [('ratio', .7, .36), ('k', 14, 7)])
def test_resolved_budget_coverage_is_read_only(tmp_path, mode, large, small):
    from experiments.modular_config import resolve_budget
    root = tmp_path / 'store'
    def params(value):
        return {'prefix_stable': True, 'budget': resolve_budget({'mode': mode, 'value': value}, 20)}
    cold = _materialize(root, (14,), lambda k: tuple(range(k)), parameters=params(large))
    before = _file_state(root)
    warm = _materialize(root, (7,), lambda k: pytest.fail('producer called'),
                        parameters=params(small), fail_if_producer_called=True)
    manifest = warm.to_manifest(root)
    assert warm.result.artifact_id == cold.result.artifact_id
    assert warm.artifact_recipe_hash == cold.artifact_recipe_hash
    assert warm.result.content_hash == cold.result.content_hash
    assert manifest['request_budget'] == params(small)['budget']
    assert manifest['artifact_budget'] == params(large)['budget']
    assert manifest['views']['7']['selected_nodes'] == list(range(7))
    assert _file_state(root) == before


@pytest.mark.parametrize('change', ['mode', 'denominator', 'rounding', 'extra', 'value', 'k',
                                    'dataset', 'candidates', 'score', 'ranking', 'producer'])
def test_budget_coverage_preserves_non_size_identity(tmp_path, change):
    from dataclasses import replace
    from experiments.modular_config import resolve_budget
    root = tmp_path / 'store'
    params = {'prefix_stable': True, 'budget': resolve_budget({'mode': 'ratio', 'value': .7}, 20),
              'ranking': 'descending'}
    _materialize(root, (14,), lambda k: tuple(range(k)), parameters=params)
    params['budget'] = resolve_budget({'mode': 'ratio', 'value': .35}, 20)
    overrides = {'parameters': params}
    if change == 'mode': params['budget'] = resolve_budget({'mode': 'k', 'value': 7}, 20)
    elif change in ('denominator', 'rounding'): params['budget'][change] = 'different'
    elif change == 'extra': params['budget']['other_semantics'] = 'different'
    elif change == 'value': params['budget']['value'] = .5
    elif change == 'k': params['budget']['k'] = 6
    elif change == 'dataset': overrides['dataset'] = replace(_dataset(), dataset_fingerprint=_sha('other'))
    elif change == 'candidates':
        candidates = tuple(range(1, 20))
        overrides['dataset'] = replace(_dataset(), candidate_nodes=candidates,
            candidate_set_hash=candidate_fingerprint(candidates, 20))
    elif change == 'score': overrides['source_score_artifact_id'] = 'score_33333333_44444444'
    elif change == 'ranking': params['ranking'] = 'ascending'
    elif change == 'producer': overrides['producer_version'] = ProducerVersion('other', _sha('other'))
    with pytest.raises(UpstreamProducerCalledError):
        _materialize(root, (7,), lambda k: tuple(range(k)), fail_if_producer_called=True, **overrides)


def test_budget_smallest_covering_and_exact_priority(tmp_path):
    from experiments.modular_config import resolve_budget
    root = tmp_path / 'store'
    def request(k, fail=False):
        return _materialize(root, (k,), lambda n: tuple(range(n)),
            parameters={'prefix_stable': True, 'budget': resolve_budget({'mode': 'k', 'value': k}, 20)},
            fail_if_producer_called=fail)
    ten, fourteen = request(10), request(14)
    assert not fourteen.cache_hit  # Small cannot cover large.
    assert request(7, True).result.artifact_id == ten.result.artifact_id
    assert request(10, True).lookup_policy == 'cache_v2_exact_recipe'


def test_ratio_floor_minimum_one_and_typed_budget_semantics(tmp_path):
    from experiments.modular_config import resolve_budget
    def params(ratio, extra):
        return {'prefix_stable': True, 'budget': {
            **resolve_budget({'mode': 'ratio', 'value': ratio}, 20), 'extra': extra}}
    root = tmp_path / 'store'
    _materialize(root, (7,), lambda k: tuple(range(k)), parameters=params(.39, 1))
    smallest = _materialize(root, (1,), lambda k: pytest.fail('producer called'),
        parameters=params(.001, 1), fail_if_producer_called=True)
    assert smallest.artifact_k == 7 and smallest.views['1']['selected_nodes'] == [0]
    with pytest.raises(UpstreamProducerCalledError):
        _materialize(root, (1,), lambda k: [0], parameters=params(.001, True), fail_if_producer_called=True)
