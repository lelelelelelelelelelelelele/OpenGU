"""AAGU-113: class-prefix semantics and real native CPU/V2/GU consumers."""
import copy
from collections import Counter
import functools

import pytest
import torch

from test_modular_consumers import tables, run, write_yaml, identities
from experiments.c_target_v1.core import stable_ranking
from experiments.target_direct_v1.class_matching import class_prefix_matched_order, METHOD
from experiments.target_direct_v1.methods import resolve_parameters


def assert_all_prefixes(candidates, labels, source, matched):
    label = dict(zip(candidates, labels))
    assert sorted(matched) == list(candidates)
    for k in range(len(candidates) + 1):
        assert Counter(label[n] for n in source[:k]) == Counter(label[n] for n in matched[:k])


def test_all_prefixes_reproducibility_draws_gaps_ties_and_rng_isolation():
    candidates = list(range(18))
    labels = [0, 2, 5] * 6  # Missing class IDs are legitimate.
    source = stable_ranking(candidates, torch.zeros(18))
    before = torch.get_rng_state().clone()
    orders = [class_prefix_matched_order(candidates, labels, source, seed) for seed in (44, 55, 66)]
    assert len(set(orders)) == 3
    assert orders[0] == class_prefix_matched_order(candidates, labels, source, 44)
    assert torch.equal(before, torch.get_rng_state())
    for order in orders:
        assert_all_prefixes(candidates, labels, source, order)
    assert class_prefix_matched_order([9], [3], [9], 0) == (9,)


@pytest.mark.parametrize('field,value', [
    ('candidate_ids', []), ('candidate_ids', [1, 1]), ('candidate_ids', [2, 1]),
    ('candidate_ids', [True, 2]), ('candidate_labels', [0]),
    ('candidate_labels', [0, -1]), ('candidate_labels', [0, 1.0]),
    ('candidate_labels', [False, 1]), ('source_ranking', [1, 1]),
    ('source_ranking', [1, 3]), ('source_ranking', [1]),
    ('matching_seed', -1), ('matching_seed', True), ('matching_seed', 2**63),
])
def test_invalid_matching_inputs_fail_closed(field, value):
    options = dict(candidate_ids=[1, 2], candidate_labels=[0, 1], source_ranking=[2, 1], matching_seed=44)
    options[field] = value
    with pytest.raises(ValueError):
        class_prefix_matched_order(**options)


def test_non_candidate_labels_are_not_matching_inputs():
    candidates = [0, 2, 4, 6]
    full_labels = [0, 7, 1, 7, 0, 7, 1, 7]
    source = [6, 4, 2, 0]
    def match():
        return class_prefix_matched_order(candidates, [full_labels[n] for n in candidates], source, 44)
    before = match()
    for n in [1, 3, 5, 7]:
        full_labels[n] = 'not a usable label'
    assert match() == before


def test_score_transform_can_only_index_candidate_labels():
    from types import SimpleNamespace
    from experiments.target_direct_v1.class_matching import score_class_matched
    candidates = torch.tensor([0, 2, 4, 6])
    class CandidateOnlyLabels:
        def __getitem__(self, ids):
            assert torch.equal(ids, candidates), 'matching accessed noncandidate labels'
            return torch.tensor([0, 1, 0, 1])
    c = SimpleNamespace(candidates=candidates, data=SimpleNamespace(y=CandidateOnlyLabels()))
    scores = score_class_matched(c, {'matching_seed': 44}, source_ranking=[6, 4, 2, 0])
    ranking = stable_ranking(candidates.tolist(), scores)
    assert_all_prefixes(candidates.tolist(), [0, 1, 0, 1], [6, 4, 2, 0], ranking)


def test_matching_seed_is_explicit_and_has_no_global_axis_or_alias():
    for value in ({}, {'matching_seed': -1}, {'matching_seed': True}, {'seed': 44}):
        with pytest.raises(ValueError):
            resolve_parameters(METHOD, value)
    p = resolve_parameters(METHOD, {'matching_seed': 44})
    assert p['matching_seed'] == 44
    assert {k: v for k, v in p.items() if k != 'matching_seed'} == resolve_parameters('r_point')


def matched_tables(tables, k=3):
    root = tables[0]
    source = {'kind': 'selector', 'schema_version': 1, 'method': 'r_point',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': k},
        'model': {'architecture': 'OpenGU.GCNNet', 'hidden_channels': 4},
        'training': {'epochs': 3},
        'parameters': {'lissa': {'iterations': 2, 'scale': 25.0, 'damp': 0.01}}}
    write_yaml(root / 'source.yaml', source)
    refs = ['source.yaml']
    for seed in (44, 55, 66):
        value = copy.deepcopy(source)
        value['method'] = METHOD
        value['parameters']['matching_seed'] = seed
        name = 'matched_%d.yaml' % seed
        write_yaml(root / name, value)
        refs.append(name)
    return refs


def test_native_three_draws_real_rpoint_v2_cold_warm_and_gu(tables, monkeypatch, record_property):
    refs = matched_tables(tables)
    cold = run(tables, 'matched_cold', selector_refs=refs, stage='unlearning',
               unlearning_refs=['gu.yaml'], return_scores=True)
    source, *matched = cold['selectors']
    labels = [n % 2 for n in range(10)]
    for row in matched:
        assert_all_prefixes(list(range(10)), labels, source['ranking'], row['ranking'])
        binding = row['score']['recipe']['fields']['source_r_point']
        assert binding == {k: source['score'][k] for k in ('artifact_id', 'recipe_hash', 'content_hash')}
        assert row['score']['recipe']['fields']['score_names'] == [METHOD]
        assert row['selection']['artifact']['source_score_artifact_id'] == row['score']['artifact_id']
    assert len({tuple(s['ranking']) for s in matched}) == 3
    assert len({s['score']['recipe_hash'] for s in cold['selectors']}) == 4
    assert len(cold['unlearning']) == 4 and all(not u['hit'] for u in cold['unlearning'])
    from experiments.target_direct_v1 import methods
    for name in ('r_point', METHOD):
        original = methods.METHODS[name]
        @functools.wraps(original)
        def forbidden(*args, **kwargs):
            raise AssertionError('warm native consumer recomputed a Score')
        monkeypatch.setitem(methods.METHODS, name, forbidden)
    warm = run(tables, 'matched_warm', selector_refs=refs, stage='unlearning',
               unlearning_refs=['gu.yaml'], return_scores=True)
    assert identities(cold) == identities(warm)
    assert all(s['score']['hit'] and s['selection']['cache']['hit'] for s in warm['selectors'])
    assert all(u['hit'] for u in warm['unlearning'])
    record_property('matched_native_cold', __import__('json').dumps(cold))
    record_property('matched_native_warm', __import__('json').dumps(warm))


def test_full_candidate_budget_and_lower_prefix_reuse(tables):
    refs = matched_tables(tables, k=10)
    large = run(tables, 'matched_all', selector_refs=refs, return_scores=True)
    refs = matched_tables(tables, k=2)
    small = run(tables, 'matched_prefix', selector_refs=refs, return_scores=True)
    assert identities(large) == identities(small)
    assert all(s['selection']['cache']['hit'] for s in small['selectors'])
    assert all(s['score']['hit'] for s in small['selectors'])
    for a, b in zip(large['selectors'], small['selectors']):
        assert a['ranking'] == b['ranking']
        assert b['requested_k'] == 2


def test_wrong_rpoint_source_identity_rejected(tables):
    from experiments.target_direct_v1.recipe import build_recipe
    from experiments.target_direct_v1.methods import Computations
    from experiments.c_target_v1.core import GateGCN
    import pickle
    refs = matched_tables(tables)
    cold = run(tables, 'source_identity', selector_refs=refs, return_scores=True)
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    c = Computations(GateGCN(3, 4, 2, .5), data, [])
    p = resolve_parameters(METHOD, {'matching_seed': 44})
    source = copy.deepcopy(cold['selectors'][0]['score'])
    for wrong in (None, source, {**source, 'recipe_hash': '0' * 64}):
        with pytest.raises(ValueError, match='exact verified R-point'):
            build_recipe(name=METHOD, computations=c, parameters=p, source_score=wrong)


def test_missing_upstream_payload_is_not_repaired_from_matched_hit(tables):
    from cache_v2.index import CacheIndex
    from experiments.c_target_v1.score_store import ScoreBundleIntegrityError
    refs = matched_tables(tables)
    cold = run(tables, 'missing_source_cold', selector_refs=refs, return_scores=True)
    root = tables[0] / 'results/cache_v2'
    index = CacheIndex(root / 'index.sqlite')
    source = index.get_artifact(cold['selectors'][0]['score']['artifact_id'])
    (root / source['semantic_path']).unlink()  # Only this test's disposable Store.
    with pytest.raises(ScoreBundleIntegrityError, match='missing'):
        run(tables, 'missing_source_warm', selector_refs=['matched_44.yaml'])
