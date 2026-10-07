"""Resolve checkpoint identities without constructing models or reading weights.

These are readers of the existing checkpoint metadata contract, not producers.
Weights are validated by the normal preparation path only when consumed on MISS.
"""
import json
import re
from pathlib import Path

from cache_v2 import canonical_sha256
from experiments.implementation_identity import implementation_fingerprint
from experiments.modular_model import numerical_environment
from utils.target_checkpoint import data_identity, TargetCheckpointError


def model_class(model_config):
    from importlib import import_module
    name = model_config['architecture'].split('.')[-1]
    modules = {'GCNNet':'gcn', 'SGCNet':'sgc', 'GATNet':'gat', 'GINNet':'gin'}
    return getattr(import_module('model.base_gnn.' + modules[name]), name)


def training_identity(instance, data):
    from experiments.modular_model import train_supervised
    cls = model_class(instance['model'])
    functions = [cls.__init__, cls.forward]
    if hasattr(cls, 'load_config'):
        functions.append(cls.load_config)
    return {'format': 'pure-state-dict-v1', 'data_identity': data_identity(data),
        'model': instance['model'], 'training': instance['training'],
        'numerics': numerical_environment(data),
        'implementation': implementation_fingerprint(*functions, train_supervised)}


def ensemble_identity(instance, data):
    from experiments.modular_model import train_supervised
    from experiments.modular_shards import (
        initial_ensemble, partition_nodes, ShardEnsemble, train_shard, aggregate_weights)
    metadata = {'format':'ensemble-state-dict-v1', 'method':instance['method'],
        'data_identity':data_identity(data), 'model':instance['model'],
        'training':instance['training'], 'parameters':instance['parameters']}
    if instance['method'] == 'GraphEraser':
        from unlearning.unlearning_methods.GraphEraser.partition.constrained_lpa_base import ConstrainedLPABase
        from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator
        from model.base_gnn.gcn import GCNNet
        metadata.update(numerics=str(data.x.dtype), implementation=implementation_fingerprint(
            initial_ensemble, partition_nodes, ConstrainedLPABase, ShardEnsemble,
            train_shard, train_supervised, GCNNet, aggregate_weights, OptimalAggregator))
    elif instance['method'] == 'GraphRevoker':
        from experiments.modular_graphrevoker import initial_graphrevoker_ensemble, graphrevoker_implementation_functions
        from experiments.implementation_identity import model_factory_fingerprint
        cls = model_class(instance['model'])
        functions = [cls.__init__, cls.forward]
        if hasattr(cls, 'load_config'):
            functions.append(cls.load_config)
        metadata.update(numerics=numerical_environment(data), implementation=canonical_sha256({
            'factory':model_factory_fingerprint(instance['model']),
            'computation':implementation_fingerprint(initial_graphrevoker_ensemble,
                *graphrevoker_implementation_functions(), ShardEnsemble, train_shard,
                train_supervised, *functions)}))
    else:
        raise ValueError('unsupported ensemble checkpoint')
    return metadata


def read_checkpoint_reference(root, metadata, prefix=''):
    from cache_v2.source_compatibility import checkpoint_candidates
    scope = 'ensemble_checkpoint' if 'method' in metadata else 'training_checkpoint'
    for candidate in checkpoint_candidates(metadata, scope):
        path = Path(root) / (prefix + canonical_sha256(candidate) + '.pt')
        sidecar = path.with_suffix('.json')
        if not path.exists() and not sidecar.exists():
            continue
        if not path.is_file() or not sidecar.is_file():
            raise TargetCheckpointError('incomplete checkpoint reference: ' + str(path))
        record = json.loads(sidecar.read_text(encoding='utf-8'))
        if (not isinstance(record, dict) or set(record) != {'metadata','file_sha256','state_hash'}
                or record['metadata'] != candidate
                or any(not isinstance(record[k], str) or not re.fullmatch('[0-9a-f]{64}', record[k])
                       for k in ('file_sha256','state_hash'))):
            raise TargetCheckpointError('checkpoint reference metadata mismatch: ' + str(sidecar))
        return dict(path=str(path.resolve()), file_sha256=record['file_sha256'],
            state_hash=record['state_hash'], hit=True, source='training_cache',
            verification='metadata_only', effective_identity=metadata,
            generation_metadata=record['metadata'], consumption_metadata=metadata)
    return None
