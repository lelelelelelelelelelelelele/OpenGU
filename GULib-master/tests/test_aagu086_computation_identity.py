import json
from dataclasses import replace
from pathlib import Path
import pytest
import torch
from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion, ArtifactResolver
from cache_v2.computation_identity import computation_recipe, checkpoint_inputs
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.errors import CacheResolutionError
from experiments.artifact_producer import FormalArtifactRequest, materialize_formal_artifact
from test_cache_v2_formal_artifacts import (_selection, _prediction_recipe, _prediction_payload, _tree_state, PREDICTION_VERSION)
from utils.target_checkpoint import save_cached_weights, load_cached_weights, resolve_cached_weights, TargetCheckpointError


def fail_producer():
    raise AssertionError('producer was called')


@pytest.mark.parametrize('source', ['comment-only', 'observer-disabled', 'unrelated-GAT-branch'])
def test_old_artifact_real_consumer_hit_without_rewrite(tmp_path, source):
    selection = _selection(tmp_path)
    old = _prediction_recipe(selection)
    store = FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION)
    original = store.store_payload(old, _prediction_payload(selection))
    snapshot = _tree_state(tmp_path)
    producer = ProducerVersion(PREDICTION_VERSION.semantic_version, source)
    fields = old.fields
    fields['producer_version'] = producer.to_dict()
    request = FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(fields), producer)
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
    assert request.recipe.fields['producer_version']['source_fingerprint'] is None
    assert not materialize_formal_artifact(tmp_path, request, fail_producer).producer_called
    for name, value in [('split_fingerprint', 'e' * 64), ('graph_fingerprint', 'f' * 64),
                        ('run_seed', 999), ('selection_artifact_id', 'sel_other'),
                        ('ensemble_state_hash', 'd' * 64)]:
        changed = request.recipe.fields
        changed[name] = value
        explanation = ArtifactResolver(FormalArtifactStore(tmp_path, producer_version=PREDICTION_VERSION).index).explain_exact(
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


def test_checkpoint_source_changes_keep_weights_but_state_conflicts_block(tmp_path):
    metadata = {'model': 'GCN', 'training': {'seed': 42}, 'implementation': 'old'}
    path = tmp_path / 'old.pt'
    save_cached_weights(path, {'w': torch.tensor([1.0])}, metadata)
    snapshot = _tree_state(tmp_path)
    current = dict(metadata, implementation='GAT-branch-added')
    assert resolve_cached_weights(tmp_path, current) == path
    assert load_cached_weights(path, current)['state_hash']
    assert _tree_state(tmp_path) == snapshot
    assert resolve_cached_weights(tmp_path, dict(current, training={'seed': 43})) != path
    save_cached_weights(tmp_path / 'second.pt', {'w': torch.tensor([2.0])}, current)
    with pytest.raises(TargetCheckpointError, match='conflicting states'):
        resolve_cached_weights(tmp_path, current)


def test_only_explicit_source_fields_are_ignored():
    fields = {'producer_version': {'semantic_version': 'v1', 'source_fingerprint': 'code'},
              'dataset_source_fingerprint': 'data', 'parameters': {'source_fingerprint': 'parameter'},
              'target': {'checkpoint_state_hash': 'weights', 'ensemble_state_hash': 'ensemble'}}
    effective = computation_recipe(ArtifactRecipe(fields)).fields
    assert effective['dataset_source_fingerprint'] == 'data'
    assert effective['parameters'] == fields['parameters']
    assert effective['target'] == fields['target']


def test_distinct_content_blocks_even_exact_old_recipe_and_producer(tmp_path):
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
    explanation = ArtifactResolver(store.index).explain_exact(ArtifactType.PREDICTION, recipe)
    assert not explanation.hit
    assert 'effective_input_content_conflict' in explanation.miss_reasons
    with pytest.raises(CacheResolutionError, match='effective_input_content_conflict'):
        materialize_formal_artifact(tmp_path, FormalArtifactRequest(ArtifactType.PREDICTION, other, newer), fail_producer)
