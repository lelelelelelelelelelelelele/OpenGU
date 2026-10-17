"""Reviewed registry entries, real consumers, and immutable temporary caches."""
from copy import deepcopy
from functools import wraps
import importlib

import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, ProducerVersion
from cache_v2.source_compatibility import source_candidates, stored_recipe
from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact
from experiments.modular_gu import gu_producer
from experiments.unlearning_outputs import load_output_payload
from test_cache_v2_formal_artifacts import _tree_state
from test_gnndelete_mask_equivalence import old_mask, evidence
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
def test_actual_gcns_match_reviewed_new_source(model):
    assert gu_producer('GNNDelete', model).source_fingerprint == NEW
    assert OLD in candidates(NEW, model)
    assert NEW in candidates(OLD, model)


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
@pytest.mark.parametrize('generation,consumption', [(OLD, NEW), (NEW, OLD)], ids=['old-to-new', 'new-to-old'])
def test_real_modular_output_reuses_other_source_without_writes(tables, monkeypatch, model, generation, consumption):
    import experiments.modular_gu as gu
    import experiments.target_direct_v1.methods as selectors
    mask_module = importlib.import_module('unlearning.unlearning_methods.GNNDelete.gnndelete')
    root, _, instance = tables
    instance['model'] = model
    write_yaml(root / 'gu.yaml', instance)
    # Run the real training consumer to create a bounded old/new Output. For
    # the old checkpoint use its exact old mask expression and measured source;
    # the prior AST/equivalence audit proves the rest of the class is unchanged.
    with monkeypatch.context() as patch:
        if generation == OLD:
            patch.setattr(mask_module, '_incident_edge_mask', old_mask)
            patch.setattr(gu, 'gu_producer', lambda *a, **kw: ProducerVersion(VERSION, OLD))
        cold = run(tables, 'cache_cold', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    original = cold['unlearning'][0]
    assert original['producer_called'] and not original['hit']
    assert original['generation_producer']['source_fingerprint'] == generation
    store = root / 'results/cache_v2'
    snapshot = _tree_state(store)
    with monkeypatch.context() as patch:
        patch.setitem(gu.GU_METHODS, 'GNNDelete', forbid(gu.GU_METHODS['GNNDelete']))
        patch.setitem(selectors.METHODS, 'degree', forbid(selectors.METHODS['degree']))
        if consumption == OLD:
            patch.setattr(gu, 'gu_producer', lambda *a, **kw: ProducerVersion(VERSION, OLD))
        warm = run(tables, 'cache_cross_source', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    observed = warm['unlearning'][0]
    assert observed['hit'] and not observed['producer_called']
    assert observed['output'] == original['output']
    assert observed['generation_producer'] == original['generation_producer']
    assert observed['consumption_producer']['source_fingerprint'] == consumption
    assert not warm['selectors'][0]['score']['producer_called']
    assert not warm['selectors'][0]['selection']['cache']['producer_called']
    assert _tree_state(store) == snapshot

    index = CacheIndex(store / 'index.sqlite')
    fields = stored_recipe(index.get_artifact(original['output']['artifact_id'])).fields
    def request(values):
        return FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(values),
                                     ProducerVersion(**values['producer_version']))
    current_fields = deepcopy(fields)
    current_fields['producer_version']['source_fingerprint'] = consumption
    assert resolve_formal_artifact(store, request(current_fields)).artifact_id == original['output']['artifact_id']
    # No source substitution may erase any actual scientific input difference.
    for mutate in (
        lambda f: f['target']['parameters'].update(unlearn_lr=0.123),
        lambda f: f['target'].update(checkpoint_state_hash='f' * 64),
        lambda f: f['pairing']['training'].update(seed=765),
        lambda f: f['pairing']['model'].update(hidden_channels=512),
        lambda f: f.update(graph_fingerprint='e' * 64),
        lambda f: f['pairing']['data_identity'].update(split_hash='d' * 64),
        lambda f: f['selection'].update(content_hash='a' * 64),
    ):
        changed = deepcopy(current_fields)
        mutate(changed)
        assert resolve_formal_artifact(store, request(changed)) is None
    assert _tree_state(store) == snapshot

    # Materialize a second source-specific fixture through the normal store
    # API. Both now exist: each exact source must win over cross-source reuse.
    payload = load_output_payload(original['output'], store)
    identity = {k: v for k, v in current_fields.items() if k != 'artifact_contract'}
    second = UnlearningOutputPayload(identity, payload.arrays, payload.state, payload.auxiliary)
    stored = store_formal_artifact(store, request(current_fields), second)
    assert stored.artifact_id != original['output']['artifact_id']
    both_snapshot = _tree_state(store)
    assert resolve_formal_artifact(store, request(current_fields)).artifact_id == stored.artifact_id
    assert resolve_formal_artifact(store, request(fields)).artifact_id == original['output']['artifact_id']
    assert _tree_state(store) == both_snapshot
    evidence('cache_' + str(model['layers']) + '_' + str(model['hidden_channels']) + '_' + generation[:8] + '_to_' + consumption[:8],
             dict(status='PASS', model=model, generation_source=generation, consumption_source=consumption,
                  cache_files_and_index_unchanged=True, compared_cache_files=len(snapshot),
                  output_reference=original['output'], producer_called=False, selector_producer_called=False,
                  generation_provenance_preserved=True, non_source_changes_rejected=7,
                  exact_current_source_preferred=True,
                  scope='local temporary real-consumer cache; not a cloud historical inventory'))
