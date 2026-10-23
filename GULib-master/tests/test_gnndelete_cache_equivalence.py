"""Historical mask-equivalence registry and corrected-output cache isolation."""
from copy import deepcopy
from functools import wraps

import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, ProducerVersion
from cache_v2.source_compatibility import source_candidates, stored_recipe
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact
from experiments.modular_gu import gu_producer
from experiments.unlearning_outputs import load_output_payload
from test_cache_v2_formal_artifacts import _tree_state
from test_modular_consumers import tables, run, write_yaml


OLD = '8902822640d7ce40b0fe669ff487b802836430ccf8c72cec88ba269b80f11cb2'
NEW = '630aaddacd35481f3a1e71062de95eef904dea34b74babf0cab83776fee24a74'
EARLIER = ['05197336573d7298a1df86ab51697c997a9501c9e2ad8336e40747a565ba637b',
           'b7eecaea7a0f76a6a25d39aed8e923234bf7ffa53a74bc5fb9eee8928aa7ece8']
VERSION = 'opengu-independent-node-output-v1'
DEFAULT = dict(architecture='OpenGU.GCNNet', dropout=0.5, hidden_channels=64, layers=2)
ARXIV_MODEL = dict(DEFAULT, hidden_channels=256, layers=3)


def candidates(source, model=DEFAULT, producer='GNNDelete', version=VERSION):
    return [v['source_fingerprint'] for v in source_candidates(
        'prediction', producer, dict(model=model, semantic_version=version), dict(source_fingerprint=source))]


@pytest.mark.parametrize('model', [DEFAULT, ARXIV_MODEL, dict(DEFAULT, hidden_channels=4)])
def test_corrected_gcns_cannot_reuse_test_selected_sources(model):
    current = gu_producer('GNNDelete', model).source_fingerprint
    assert current not in {OLD, NEW, *EARLIER}
    assert candidates(current, model) == [current]
    assert all(current not in candidates(old, model) for old in (OLD, NEW, *EARLIER))


@pytest.mark.parametrize('current', [OLD, NEW] + EARLIER)
def test_default_model_all_reviewed_members_are_direct_candidates(current):
    actual = candidates(current)
    assert actual[0] == current
    assert len(actual) == len(set(actual)) == 4
    assert set(actual) == {OLD, NEW, *EARLIER}


def test_scope_and_unknown_sources_are_not_broadened():
    for source in EARLIER:
        assert candidates(source, ARXIV_MODEL) == [source]
    assert candidates('unreviewed') == ['unreviewed']
    assert candidates(NEW, producer='GIF') == [NEW]
    assert candidates(NEW, version='different-semantic-version') == [NEW]


def forbid(function):
    @wraps(function)
    def prohibited(*args, **kwargs):
        raise AssertionError('cache HIT invoked a producer')
    return prohibited


@pytest.mark.parametrize('model', [DEFAULT, dict(DEFAULT, hidden_channels=256)], ids=['gcn2-64', 'gcn2-256'])
@pytest.mark.parametrize('historical', [OLD, NEW])
def test_corrected_consumer_recomputes_historical_output_and_then_reuses_exact(tables, monkeypatch, model, historical):
    import experiments.modular_gu as gu
    import experiments.target_direct_v1.methods as selectors
    root, _, instance = tables
    instance['model'] = model
    write_yaml(root / 'gu.yaml', instance)
    current = gu_producer('GNNDelete', model)
    # This temporary fixture exercises historical identity lookup only. Its
    # payload is not represented as an execution of the old algorithm.
    with monkeypatch.context() as patch:
        patch.setattr(gu, 'gu_producer', lambda *a, **kw: ProducerVersion(VERSION, historical))
        historical_run = run(tables, 'historical_identity', stage='unlearning',
                             selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    original = historical_run['unlearning'][0]
    store = root / 'results/cache_v2'
    snapshot = _tree_state(store)
    index = CacheIndex(store / 'index.sqlite')
    fields = stored_recipe(index.get_artifact(original['output']['artifact_id'])).fields
    corrected_fields = deepcopy(fields)
    corrected_fields['producer_version']['source_fingerprint'] = current.source_fingerprint
    request = FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(corrected_fields), current)
    assert resolve_formal_artifact(store, request) is None
    assert _tree_state(store) == snapshot
    with monkeypatch.context() as patch:
        patch.setitem(selectors.METHODS, 'degree', forbid(selectors.METHODS['degree']))
        corrected = run(tables, 'corrected', stage='unlearning',
                        selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    observed = corrected['unlearning'][0]
    assert not observed['hit'] and observed['producer_called']
    assert observed['generation_producer']['source_fingerprint'] == current.source_fingerprint
    assert observed['output'] != original['output']
    assert observed['checkpoint']['state_hash'] == original['checkpoint']['state_hash']
    assert corrected['selectors'][0]['selection']['artifact'] == historical_run['selectors'][0]['selection']['artifact']
    assert load_output_payload(original['output'], store) is not None
    both_snapshot = _tree_state(store)
    with monkeypatch.context() as patch:
        patch.setitem(gu.GU_METHODS, 'GNNDelete', forbid(gu.GU_METHODS['GNNDelete']))
        patch.setitem(selectors.METHODS, 'degree', forbid(selectors.METHODS['degree']))
        warm = run(tables, 'corrected_warm', stage='unlearning',
                   selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    assert warm['unlearning'][0]['hit']
    assert warm['unlearning'][0]['output'] == observed['output']
    assert _tree_state(store) == both_snapshot
    # Source isolation must not weaken any other scientific input identity.
    for mutate in (
        lambda f: f['target']['parameters'].update(unlearn_lr=0.123),
        lambda f: f['target'].update(checkpoint_state_hash='f' * 64),
        lambda f: f['pairing']['training'].update(seed=765),
        lambda f: f['pairing']['model'].update(hidden_channels=512),
        lambda f: f.update(graph_fingerprint='e' * 64),
        lambda f: f['pairing']['data_identity'].update(split_hash='d' * 64),
        lambda f: f['selection'].update(content_hash='a' * 64),
    ):
        changed = deepcopy(corrected_fields)
        mutate(changed)
        changed_request = FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(changed), current)
        assert resolve_formal_artifact(store, changed_request) is None
    assert _tree_state(store) == both_snapshot
