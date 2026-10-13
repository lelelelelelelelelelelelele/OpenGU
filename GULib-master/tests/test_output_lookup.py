"""Existing Output HITs must not execute model/checkpoint preparation."""
import copy
import functools
import json
from pathlib import Path

import pytest

from test_modular_consumers import tables, run, write_yaml


PARAMETERS = {
    'GNNDelete': {'unlearning_epochs': 2},
    'GIF': {'iteration': 2, 'scale': 1000, 'damp': .1},
    'IDEA': {'iteration': 2, 'scale': 1000, 'damp': .1, 'gaussian_mean': 0., 'gaussian_std': .001},
    'MEGU': {'unlearning_epochs': 2, 'unlearn_lr': .015, 'unlearn_weight_decay': .001},
    'GraphEraser': {'num_shards': 2, 'opt_num_epochs': 1, 'num_opt_samples': 1},
    'GraphRevoker': {'num_shards': 2, 'opt_num_epochs': 1, 'num_opt_samples': 1,
                     'gpa_epochs': 1, 'gpa_hidden_channels': 8, 'gpa_batch_size': 64},
    'Retrain': {},
}


def setup(tables, method):
    root, _, original = tables
    item = copy.deepcopy(original)
    item.update(method=method, parameters=PARAMETERS[method])
    write_yaml(root / 'method.yaml', item)
    return dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['method.yaml'])


def legacy_output(tables, monkeypatch, options):
    from experiments.output_lookup import OutputLookup
    # Populate the Store through the unchanged computation consumer. The warm
    # reader must consume these same artifacts, not a new format or alias.
    with monkeypatch.context() as patch:
        patch.setattr(OutputLookup, 'lookup', lambda *a, **k: (None, None))
        return run(tables, 'existing_producer', **options)['unlearning'][0]


def forbid(patch, module, name):
    original = getattr(module, name)
    @functools.wraps(original)
    def forbidden(*a, **k):
        pytest.fail('warm Output must not call ' + module.__name__ + '.' + name)
    patch.setattr(module, name, forbidden)


@pytest.mark.parametrize('method', PARAMETERS)
def test_seven_existing_outputs_hit_without_model_or_weight_loading(tables, monkeypatch, method):
    import experiments.modular_run as runner
    import experiments.modular_model as model
    import experiments.modular_shards as shards
    import experiments.modular_graphrevoker as revoker
    import utils.target_checkpoint as weights
    options = setup(tables, method)
    cold = legacy_output(tables, monkeypatch, options)
    assert not cold['hit']
    # All of these are real production entry points. wraps preserves source
    # identity so instrumentation cannot itself create a legitimate cache MISS.
    for module, name in ((runner,'prepare_model'), (model,'create_model'),
                         (weights,'load_weights'), (weights,'load_cached_weights'),
                         (shards,'prepare_ensemble'), (revoker,'prepare_graphrevoker_ensemble')):
        forbid(monkeypatch, module, name)
    warm = run(tables, 'warm_without_models', **options)['unlearning'][0]
    assert warm['hit'] and not warm['producer_called']
    for key in ('output','result','evaluation','target','generation_producer','consumption_producer'):
        if key in cold:
            assert warm[key] == cold[key]
    if method != 'Retrain':
        assert warm['checkpoint']['verification'] == 'metadata_only'
        assert warm['checkpoint']['state_hash'] == cold['checkpoint']['state_hash']
    if method in ('GraphEraser','GraphRevoker'):
        assert warm['ensemble_preparation']['state_hash'] == cold['ensemble_preparation']['state_hash']


def test_output_miss_prepares_and_metadata_changes_do_not_reuse(tables, monkeypatch):
    from utils.target_checkpoint import TargetCheckpointError
    options = setup(tables, 'GNNDelete')
    first = legacy_output(tables, monkeypatch, options)
    sidecar = Path(first['checkpoint']['path']).with_suffix('.json')
    record = json.loads(sidecar.read_text(encoding='utf-8'))
    record['state_hash'] = '0' * 64
    sidecar.write_text(json.dumps(record), encoding='utf-8')
    # The changed reference cannot find the old Output. Its MISS then validates
    # actual checkpoint bytes and refuses the false state hash before computing.
    with pytest.raises(TargetCheckpointError, match='provenance'):
        run(tables, 'bad_state_reference', **options)


def test_metadata_corruption_is_not_a_clean_miss(tables, monkeypatch):
    from utils.target_checkpoint import TargetCheckpointError
    options = setup(tables, 'GNNDelete')
    first = legacy_output(tables, monkeypatch, options)
    path = Path(first['checkpoint']['path']).with_suffix('.json')
    record = json.loads(path.read_text(encoding='utf-8'))
    record['metadata']['training']['seed'] += 1
    path.write_text(json.dumps(record), encoding='utf-8')
    with pytest.raises(TargetCheckpointError, match='metadata mismatch'):
        run(tables, 'bad_metadata', **options)


def test_corrupt_output_is_not_recomputed_when_actually_consumed(tables, monkeypatch):
    from cache_v2 import CacheIndex
    from cache_v2.store import ArtifactIntegrityError
    import experiments.modular_run as runner
    options = setup(tables, 'GNNDelete')
    first = legacy_output(tables, monkeypatch, options)
    root = tables[0] / 'results/cache_v2'
    record = CacheIndex(root / 'index.sqlite').get_artifact(first['artifact_id'])
    (root / record['semantic_path']).write_bytes(b'corrupt output')
    forbid(monkeypatch, runner, 'prepare_model')
    warm = run(tables, 'cached_metrics_with_unused_output', **options)['unlearning'][0]
    assert warm['hit'] and warm['evaluation_cache']['hit'] and not warm['producer_called']
    write_yaml(tables[0] / 'new-metrics.yaml', {
        'kind': 'evaluation', 'schema_version': 1, 'case': 'post_method_metrics', 'metrics': ['f1']})
    with pytest.raises(ArtifactIntegrityError, match='hash|payload|digest'):
        run(tables, 'bad_output', **options, evaluation_refs=['new-metrics.yaml'])


@pytest.mark.parametrize('architecture', ['GCN','SGC','GAT','GIN'])
def test_metadata_reader_equals_model_preparation_identity(tables, architecture):
    from experiments.modular_config import model_training
    from experiments.modular_model import create_model, training_metadata
    from experiments.checkpoint_references import training_identity
    import pickle
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    model, training = model_training({'model': {'architecture':'OpenGU.' + architecture + 'Net'}})
    instance = dict(model=model, training=training)
    actual = create_model(model, 'fixture', data, 'cpu')
    assert training_identity(instance, data) == training_metadata(actual, instance, data)


def direct_lookup(tables, monkeypatch):
    """Use real saved Output identities, isolating catalogue selection from metrics."""
    from types import SimpleNamespace
    from cache_v2 import CacheIndex
    from cache_v2.source_compatibility import stored_recipe
    from experiments.output_lookup import OutputLookup
    import experiments.evaluation_cache as evaluation
    first = legacy_output(tables, monkeypatch, setup(tables, 'GNNDelete'))
    root = tables[0] / 'results/cache_v2'
    index = CacheIndex(root / 'index.sqlite')
    fields = stored_recipe(index.get_artifact(first['artifact_id'])).fields
    instance = {key: fields['pairing'][key] for key in ('model', 'training', 'deletion')}
    instance.update(method=fields['target']['method'], parameters=fields['target']['parameters'])
    lookup = OutputLookup(None, root, None)
    monkeypatch.setattr(lookup, 'checkpoint', lambda *a, **k: {'state_hash':fields['target']['checkpoint_state_hash']})
    monkeypatch.setattr(evaluation, 'evaluate_single', lambda *a, **k: (
        {key:first[key] for key in ('result', 'evaluation')}, {'hit': True}))
    monkeypatch.setattr(index.__class__, 'artifact_count', lambda *a: pytest.fail('global catalogue count'), raising=False)
    args = dict(selection=SimpleNamespace(**fields['selection'], selected_nodes=fields['pairing']['selected_nodes']),
        data=None, dataset_input=fields['dataset_input'], dataset_identity=fields['pairing']['data_identity'],
        dataset_root=None, inputs=SimpleNamespace(graph_fingerprint=fields['graph_fingerprint']))
    return lookup, instance, args, fields, first, index


def test_output_source_rank_rechecks_new_preferred_and_ambiguous_candidates(tables, monkeypatch):
    from cache_v2 import ArtifactRecipe, ProducerVersion
    from cache_v2.formal_store import FormalArtifactStore
    from cache_v2.unlearning_output import UnlearningOutputPayload
    import cache_v2.source_compatibility as compatibility
    import experiments.modular_gu as gu
    lookup, instance, args, fields, first, index = direct_lookup(tables, monkeypatch)
    previous = ProducerVersion(**fields['producer_version'])
    current = ProducerVersion(previous.semantic_version, 'new-output-source')
    monkeypatch.setattr(gu, 'gu_producer', lambda *a: current)
    monkeypatch.setattr(compatibility, 'registry', lambda: [dict(cache_scope='prediction',producer='GNNDelete',
        applies_to={'semantic_version':current.semantic_version, 'model':instance['model']},
        fingerprints=[{'source_fingerprint':current.source_fingerprint},
                      {'source_fingerprint':previous.source_fingerprint}])])
    assert lookup.lookup(instance, **args)[0]['output'] == first['output']
    original = FormalArtifactStore(lookup.store_root, producer_version=previous).load_payload_read_only(
        'prediction', ArtifactRecipe(fields)).payload
    def publish(new_fields):
        identity = {key:value for key,value in new_fields.items() if key != 'artifact_contract'}
        payload = UnlearningOutputPayload(identity, original.arrays, original.state, original.auxiliary)
        return FormalArtifactStore(lookup.store_root, producer_version=current).store_payload(
            ArtifactRecipe(new_fields), payload)
    new_fields = {**fields, 'producer_version':current.to_dict()}
    preferred = publish(new_fields)
    assert lookup.lookup(instance, **args)[0]['artifact_id'] == preferred.artifact_id
    alternative = copy.deepcopy(new_fields)
    alternative['pairing']['extra_scientific_identity'] = 'second-admitted-candidate'
    publish(alternative)
    with pytest.raises(ValueError, match='ambiguous registered Output'):
        lookup.lookup(instance, **args)


@pytest.mark.parametrize('fault', ['invalid', 'conflict', 'foreign_source'])
def test_parent_local_output_lookup_preserves_fail_closed_and_clean_miss(tables, monkeypatch, fault):
    from cache_v2 import ArtifactConflictRecord, ArtifactType, ProducerVersion
    import experiments.modular_gu as gu
    lookup, instance, args, fields, first, index = direct_lookup(tables, monkeypatch)
    if fault == 'foreign_source':
        monkeypatch.setattr(gu, 'gu_producer', lambda *a: ProducerVersion('foreign-protocol','foreign-source'))
        assert lookup.lookup(instance, **args) == (None, None)
        return
    if fault == 'invalid':
        with index.transaction() as writer:
            writer.connection.execute("UPDATE artifacts SET status='invalid' WHERE artifact_id=?", (first['artifact_id'],))
    else:
        index.record_conflict(ArtifactConflictRecord(artifact_type=ArtifactType.PREDICTION,
            recipe_hash=first['recipe_hash'], existing_artifact_id=first['artifact_id'],
            existing_content_hash=first['content_hash'], observed_content_hash='0'*64))
    with pytest.raises(ValueError, match='Output lookup failed closed'):
        lookup.lookup(instance, **args)
