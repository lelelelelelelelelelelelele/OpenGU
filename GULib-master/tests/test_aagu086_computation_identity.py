import json
from dataclasses import replace
from pathlib import Path
import pytest
import torch
from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion, ArtifactResolver
from cache_v2.source_compatibility import source_candidates, checkpoint_candidates
from cache_v2 import canonical_sha256
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.errors import CacheResolutionError
from experiments.artifact_producer import FormalArtifactRequest, materialize_formal_artifact
from test_cache_v2_formal_artifacts import (_selection, _prediction_recipe, _prediction_payload, _tree_state, PREDICTION_VERSION)
from utils.target_checkpoint import save_cached_weights, load_cached_weights, resolve_cached_weights, TargetCheckpointError


def fail_producer():
    raise AssertionError('producer was called')


@pytest.mark.parametrize('source', ['comment-only', 'observer-disabled', 'unrelated-GAT-branch'])
def test_old_artifact_real_consumer_hit_without_rewrite(tmp_path, source, monkeypatch):
    selection = _selection(tmp_path)
    old = _prediction_recipe(selection)
    store = FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION)
    original = store.store_payload(old, _prediction_payload(selection))
    snapshot = _tree_state(tmp_path)
    producer = ProducerVersion(PREDICTION_VERSION.semantic_version, source)
    fields = old.fields
    fields['producer_version'] = producer.to_dict()
    request = FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(fields), producer)
    allow(monkeypatch, 'prediction', PREDICTION_VERSION.semantic_version,
          [{'source_fingerprint': PREDICTION_VERSION.source_fingerprint}, {'source_fingerprint': source}])
    monkeypatch.setattr(store.index.__class__, 'find_artifacts_by_type', lambda *a, **k: fail_producer())
    result = materialize_formal_artifact(tmp_path, request, fail_producer)
    assert result.artifact_id == original.artifact_id
    assert not result.producer_called
    assert result.result.recipe_hash == old.recipe_hash
    assert result.result.generation_producer == PREDICTION_VERSION.to_dict()
    assert result.result.consumption_producer == producer.to_dict()
    assert _tree_state(tmp_path) == snapshot


def test_new_cold_warm_and_effective_changes(tmp_path):
    selection = _selection(tmp_path)
    old = _prediction_recipe(selection)
    request = FormalArtifactRequest(ArtifactType.PREDICTION, old, PREDICTION_VERSION)
    result = materialize_formal_artifact(tmp_path, request, lambda: _prediction_payload(selection))
    assert result.producer_called
    assert request.recipe.fields['producer_version']['source_fingerprint'] == PREDICTION_VERSION.source_fingerprint
    assert not materialize_formal_artifact(tmp_path, request, fail_producer).producer_called
    for name, value in [('split_fingerprint', 'e' * 64), ('graph_fingerprint', 'f' * 64),
                        ('run_seed', 999), ('selection_artifact_id', 'sel_other'),
                        ('ensemble_state_hash', 'd' * 64)]:
        changed = request.recipe.fields
        changed[name] = value
        explanation = ArtifactResolver(FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION).index).explain_compatible(
            ArtifactType.PREDICTION, ArtifactRecipe(changed))
        assert not explanation.hit


def test_payload_corruption_still_rejected(tmp_path):
    selection = _selection(tmp_path)
    recipe = _prediction_recipe(selection)
    store = FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION)
    original = store.store_payload(recipe, _prediction_payload(selection))
    (tmp_path / original.semantic_path).write_bytes(b'corrupt')
    with pytest.raises(Exception, match='size|hash|payload'):
        materialize_formal_artifact(tmp_path, FormalArtifactRequest(ArtifactType.PREDICTION, recipe, PREDICTION_VERSION), fail_producer)


def allow(monkeypatch, scope, producer, members, conditions=None):
    import cache_v2.source_compatibility as compatibility
    group = dict(cache_scope=scope, producer=producer, applies_to=conditions or {},
        fingerprints=members, reason='test-reviewed equivalent sources', evidence=['test fixture'])
    monkeypatch.setattr(compatibility, 'registry', lambda: [group])


def test_checkpoint_current_first_then_exact_historical_path(tmp_path, monkeypatch):
    metadata = {'model': 'GCN', 'training': {'seed': 42}, 'implementation': 'old'}
    path = tmp_path / (canonical_sha256(metadata) + '.pt')
    save_cached_weights(path, {'w': torch.tensor([1.0])}, metadata)
    current = dict(metadata, implementation='new')
    allow(monkeypatch, 'training_checkpoint', 'supervised_training',
          [{'implementation': 'old'}, {'implementation': 'new'}])
    monkeypatch.setattr(Path, 'glob', lambda *a, **k: fail_producer())
    assert resolve_cached_weights(tmp_path, current) == path
    assert load_cached_weights(path, current)['generation_metadata'] == metadata
    assert resolve_cached_weights(tmp_path, dict(current, training={'seed': 43})) != path
    new_path = tmp_path / (canonical_sha256(current) + '.pt')
    save_cached_weights(new_path, {'w': torch.tensor([2.0])}, current)
    assert resolve_cached_weights(tmp_path, current) == new_path
    new_path.write_bytes(b'corrupt')
    with pytest.raises(Exception):
        resolve_cached_weights(tmp_path, current)


def test_multiple_groups_order_without_unique_match_or_transitive_expansion(monkeypatch):
    import cache_v2.source_compatibility as compatibility
    groups = [dict(cache_scope='score', producer='selector', applies_to={},
        fingerprints=[{'source_fingerprint': f} for f in members])
        for members in [('A', 'B'), ('B', 'C'), ('A', 'D')]]
    monkeypatch.setattr(compatibility, 'registry', lambda: groups)
    actual = list(source_candidates('score', 'selector', {}, {'source_fingerprint': 'A'}))
    assert actual == [{'source_fingerprint': f} for f in ('A', 'B', 'D')]
    assert list(source_candidates('score', 'selector', {}, {'source_fingerprint': 'unknown'})) == [{'source_fingerprint': 'unknown'}]
    assert list(source_candidates('selection', 'selector', {}, {'source_fingerprint': 'A'})) == [{'source_fingerprint': 'A'}]


def test_multifield_members_are_not_cross_combined(monkeypatch):
    old = {'implementation': 'A', 'trajectory_implementation': 'B'}
    new = {'implementation': 'C', 'trajectory_implementation': 'D'}
    allow(monkeypatch, 'selector_trajectory', 'supervised_training', [old, new])
    metadata = dict(new, model='GCN', training={'seed': 1})
    candidates = list(checkpoint_candidates(metadata, 'selector_trajectory'))
    assert candidates == [metadata, dict(metadata, **old)]
    assert metadata['implementation'] == 'C'


def test_distinct_cross_source_content_does_not_block_current(tmp_path, monkeypatch):
    from cache_v2 import ArtifactHeader
    selection = _selection(tmp_path)
    recipe = _prediction_recipe(selection)
    store = FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION)
    original = store.store_payload(recipe, _prediction_payload(selection))
    fields = recipe.fields
    newer = ProducerVersion(PREDICTION_VERSION.semantic_version, 'new-source')
    fields['producer_version'] = newer.to_dict()
    other = ArtifactRecipe(fields)
    store.index.register_artifact(ArtifactHeader(artifact_type=ArtifactType.PREDICTION,
        recipe=other, content_hash='d' * 64, producer_version=newer, status='valid', verification_status='verified'))
    allow(monkeypatch, 'prediction', PREDICTION_VERSION.semantic_version,
          [{'source_fingerprint': PREDICTION_VERSION.source_fingerprint}, {'source_fingerprint': 'new-source'}])
    find = store.index.find_artifact
    def current_only(kind, digest):
        assert digest == recipe.recipe_hash
        return find(kind, digest)
    monkeypatch.setattr(store.index, 'find_artifact', current_only)
    assert ArtifactResolver(store.index).explain_compatible(ArtifactType.PREDICTION, recipe).hit


def test_unknown_source_does_not_reuse(tmp_path):
    from experiments.artifact_producer import resolve_formal_artifact
    selection = _selection(tmp_path)
    recipe = _prediction_recipe(selection)
    FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION).store_payload(recipe, _prediction_payload(selection))
    producer = ProducerVersion(PREDICTION_VERSION.semantic_version, 'unknown')
    fields = recipe.fields
    fields['producer_version'] = producer.to_dict()
    assert resolve_formal_artifact(tmp_path, FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(fields), producer)) is None


def test_factory_ignores_unselected_branch_but_keeps_initialization(monkeypatch):
    import experiments.implementation_identity as identity
    from experiments.modular_model import create_model
    source = identity.computation_source
    model = {'architecture': 'OpenGU.GCNNet'}
    before = identity.model_factory_fingerprint(model)
    monkeypatch.setattr(identity, 'computation_source', lambda f:
        source(f).replace("args['base_model'] = 'GAT'", "args['base_model'] = 'UNUSED'") if f is create_model else source(f))
    assert identity.model_factory_fingerprint(model) == before
    monkeypatch.setattr(identity, 'computation_source', lambda f:
        source(f).replace("args['base_model'] = 'GCN'", "args['base_model'] = 'CHANGED'") if f is create_model else source(f))
    assert identity.model_factory_fingerprint(model) != before


def test_graphrevoker_old_checkpoint_path_skips_training(tmp_path, monkeypatch):
    from test_graphrevoker_modular import inputs, settings
    from experiments.modular_config import model_training
    from experiments.modular_model import runtime_defaults
    from experiments.modular_graphrevoker import prepare_graphrevoker_ensemble
    import experiments.modular_graphrevoker as revoker
    data = inputs()
    model, training = model_training({'model': {'architecture': 'OpenGU.GCNNet', 'hidden_channels': 4},
        'training': {'epochs': 1, 'seed': 42}})
    instance = dict(model=model, training=training, parameters=settings())
    # Produce one genuine disposable ensemble; retain its state under a reviewed historical source.
    ensemble, cold = prepare_graphrevoker_ensemble(instance, data, tmp_path / 'cold')
    current = cold['generation_metadata']
    old = dict(current, implementation='reviewed-old-implementation')
    old_path = tmp_path / ('graphrevoker-' + canonical_sha256(old) + '.pt')
    from utils.target_checkpoint import capture_state
    save_cached_weights(old_path, capture_state(ensemble), old)
    allow(monkeypatch, 'ensemble_checkpoint', 'GraphRevoker',
          [{'implementation': current['implementation']}, {'implementation': old['implementation']}])
    # Preserve the original source identity while making any training call fail.
    from functools import wraps
    @wraps(revoker.initial_graphrevoker_ensemble)
    def forbidden(*args, **kwargs):
        raise AssertionError('ensemble training was called')
    monkeypatch.setattr(revoker, 'initial_graphrevoker_ensemble', forbidden)
    restored, warm = prepare_graphrevoker_ensemble(instance, data, tmp_path)
    assert warm['hit'] and warm['state_hash'] == cold['state_hash']
    assert warm['generation_metadata'] == old
    assert warm['consumption_metadata'] == current


def test_invalid_current_candidate_does_not_fall_through_to_valid_history(tmp_path, monkeypatch):
    from cache_v2 import ArtifactHeader
    selection = _selection(tmp_path)
    recipe = _prediction_recipe(selection)
    store = FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION)
    store.store_payload(recipe, _prediction_payload(selection))
    current = ProducerVersion(PREDICTION_VERSION.semantic_version, 'invalid-current')
    fields = recipe.fields
    fields['producer_version'] = current.to_dict()
    request = ArtifactRecipe(fields)
    store.index.register_artifact(ArtifactHeader(artifact_type=ArtifactType.PREDICTION,
        recipe=request, content_hash='c'*64, producer_version=current, status='invalid', verification_status='verified'))
    allow(monkeypatch, 'prediction', PREDICTION_VERSION.semantic_version,
        [{'source_fingerprint': PREDICTION_VERSION.source_fingerprint}, {'source_fingerprint': current.source_fingerprint}])
    with pytest.raises(CacheResolutionError, match='status_invalid'):
        materialize_formal_artifact(tmp_path, FormalArtifactRequest(ArtifactType.PREDICTION, request, current), fail_producer)


def test_factory_fingerprint_ignores_optional_ast_representation(monkeypatch):
    import ast
    import experiments.implementation_identity as identity
    model = {'architecture': 'OpenGU.GCNNet'}
    original_parse = ast.parse
    expected = identity.model_factory_fingerprint(model)
    def omit_optional(*args, **kwargs):
        tree = original_parse(*args, **kwargs)
        for node in ast.walk(tree):
            node._fields = tuple(name for name in node._fields
                if getattr(node, name, None) is not None or name == 'value')
            if isinstance(node, ast.FunctionDef):
                node._fields += ('type_params',)
                node.type_params = []
        return tree
    monkeypatch.setattr(ast, 'parse', omit_optional)
    assert identity.model_factory_fingerprint(model) == expected
