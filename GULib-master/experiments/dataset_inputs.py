"""Exact references to existing persisted inputs; no materialization or search."""
from pathlib import Path, PurePosixPath
import copy
import json
import pickle
import torch
from experiments.selection_inputs import make_dataset_selection_inputs
from utils.target_checkpoint import data_identity

from experiments.effective_config import ConfigurationError, fields
from utils.target_checkpoint import sha256_file


def input_path(root, relative):
    path = PurePosixPath(relative)
    if not path.parts or path.is_absolute() or '..' in path.parts or ':' in relative or '\\' in relative:
        raise ConfigurationError('unsafe Dataset/Split dependency path')
    root = Path(root).resolve()
    resolved = (root / relative).resolve()
    if root not in resolved.parents:
        raise ConfigurationError('Dataset/Split dependency escapes root')
    return resolved


def bind_input(instance, directory, root):
    manifest = (Path(directory) / instance['artifacts']['manifest']).resolve()
    relative = manifest.relative_to(Path(root).resolve()).as_posix()
    value = json.loads(manifest.read_text(encoding='utf-8'))
    graph = (manifest.parent / value['data_path']).resolve()
    return {'instance': copy.deepcopy(instance), 'manifest': relative,
            'graph': graph.relative_to(Path(root).resolve()).as_posix(),
            'graph_sha256': value['data_sha256']}


def resolve_input(reference, root):
    fields(reference, {'instance', 'manifest', 'graph', 'graph_sha256'},
           {'instance', 'manifest', 'graph', 'graph_sha256'}, 'Dataset/Split reference')
    manifest = input_path(root, reference['manifest'])
    graph = input_path(root, reference['graph'])
    instance = copy.deepcopy(reference['instance'])
    if sha256_file(manifest) != instance['artifacts']['manifest_sha256']:
        raise ConfigurationError('dataset manifest digest mismatch')
    value = json.loads(manifest.read_text(encoding='utf-8'))
    if (manifest.parent / value['data_path']).resolve() != graph:
        raise ConfigurationError('Dataset/Split graph path mismatch')
    if value['data_sha256'] != reference['graph_sha256']:
        raise ConfigurationError('Dataset/Split graph reference mismatch')
    instance['artifacts']['manifest'] = manifest.name
    data, _ = read_dataset(instance, manifest.parent)
    return data


def read_dataset(instance, directory):
    fields(instance['dataset'], {'name', 'family'}, {'name'}, 'dataset')
    fields(instance['artifacts'], {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'},
           {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'}, 'dataset artifacts')
    artifacts = instance['artifacts']
    if artifacts['node_id_space'] != 'pyg-global-node-index-v1':
        raise ConfigurationError('unsupported node ID space')
    if not artifacts['manifest'] or not artifacts['manifest_sha256'] or not artifacts['split_hash']:
        raise ConfigurationError('persisted Dataset/Split artifacts are required')
    manifest_path = (Path(directory) / artifacts['manifest']).resolve()
    if sha256_file(manifest_path) != artifacts['manifest_sha256']:
        raise ConfigurationError('dataset manifest digest mismatch')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    fields(manifest, {'schema', 'version', 'dataset', 'preprocessing', 'split', 'data_path', 'data_sha256', 'data_identity'},
                    {'schema', 'version', 'dataset', 'preprocessing', 'split', 'data_path', 'data_sha256', 'data_identity'}, 'dataset manifest')
    if manifest['schema'] != 'opengu.persisted_dataset_split' or manifest['version'] != 1:
        raise ConfigurationError('unknown persisted Dataset/Split manifest')
    for key in ('dataset', 'preprocessing', 'split'):
        if manifest[key] != instance[key]:
            raise ConfigurationError('dataset manifest ' + key + ' mismatch')
    data_path = (manifest_path.parent / manifest['data_path']).resolve()
    if sha256_file(data_path) != manifest['data_sha256']:
        raise ConfigurationError('persisted graph digest mismatch')
    with data_path.open('rb') as handle:
        data = pickle.load(handle)
    n = int(data.num_nodes)
    masks = [getattr(data, key + '_mask', None) for key in ('train', 'val', 'test')]
    if any(mask is None or mask.dtype != torch.bool or tuple(mask.shape) != (n,) or not mask.any() for mask in masks):
        raise ConfigurationError('three nonempty persisted boolean masks are required')
    if not torch.stack(masks).sum(0).eq(1).all():
        raise ConfigurationError('persisted split must partition the node space')
    identity = data_identity(data)
    if identity != manifest['data_identity'] or identity['split_hash'] != artifacts['split_hash']:
        raise ConfigurationError('actual Dataset/Split identity mismatch')
    if data.x.dtype != torch.float32 or not torch.isfinite(data.x).all():
        raise ConfigurationError('current consumers require finite float32 features')
    inputs = make_dataset_selection_inputs(data, dataset_name=instance['dataset']['name'].lower())
    return data, inputs


