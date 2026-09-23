"""Verified references to independently persisted method outputs."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import torch
from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, ProducerVersion
from cache_v2.runtime import _decode_exact_mapping
from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact
from experiments.effective_config import ConfigurationError, fields
from experiments.node_deletion import pairing_identity, retained_graph


def output_reference(result, recipe_hash):
    return {'artifact_id': result.artifact_id, 'recipe_hash': recipe_hash,
            'content_hash': result.content_hash}


def save_run_output(payload, path, dataset_root):
    """Same Output payload, run-owned storage, no computation-cache registration."""
    path = Path(path).resolve()
    relative = path.relative_to(Path(dataset_root).resolve()).as_posix()
    if not relative.startswith('results/runs/'):
        raise ConfigurationError('uncached output must belong to a run')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(payload.canonical_bytes)
    recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **payload.identity})
    return dict(storage='run', path=relative, recipe_hash=recipe.recipe_hash, content_hash=payload.content_hash)


def load_output(reference, store_root, *, data=None, dataset_root=None):
    if reference.get('storage') == 'run':
        fields(reference, {'storage', 'path', 'recipe_hash', 'content_hash'},
               {'storage', 'path', 'recipe_hash', 'content_hash'}, 'run output reference')
        if dataset_root is None:
            raise ConfigurationError('run output requires explicit Dataset/Split root')
        from experiments.modular_artifacts import safe_path
        path = safe_path(Path(dataset_root), reference['path'])
        if not reference['path'].startswith('results/runs/'):
            raise ConfigurationError('run output is outside results/runs')
        payload = UnlearningOutputPayload.from_bytes(path.read_bytes())
        recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **payload.identity})
        if payload.content_hash != reference['content_hash'] or recipe.recipe_hash != reference['recipe_hash']:
            raise ConfigurationError('run output digest mismatch')
        from experiments.modular_gu import gu_producer
        if ProducerVersion(**payload.identity['producer_version']) != gu_producer(
                payload.identity['target']['method'], payload.identity['pairing']['model']):
            raise ConfigurationError('run output producer changed')
        index = CacheIndex(Path(store_root) / 'index.sqlite')
        index.check_schema()
        selection = index.get_artifact(payload.identity['selection']['artifact_id'])
        if any(selection[k] != v for k, v in payload.identity['selection'].items()):
            raise ConfigurationError('run output Selection dependency mismatch')
        if data is not None and pairing_identity(payload.identity['pairing'], data,
                payload.arrays['selected_nodes']) != payload.identity['pairing']:
            raise ConfigurationError('run output Dataset/Split mismatch')
        return resolve_output(payload, dataset_root)
    fields(reference, {'artifact_id', 'recipe_hash', 'content_hash'},
           {'artifact_id', 'recipe_hash', 'content_hash'}, 'method output reference')
    root = Path(store_root)
    if not (root / 'index.sqlite').is_file():
        raise ConfigurationError('method output MISS: Store is absent')
    index = CacheIndex(root / 'index.sqlite')
    index.check_schema()
    record = index.get_artifact(reference['artifact_id'])
    if record['artifact_type'] != ArtifactType.PREDICTION.value:
        raise ConfigurationError('reference is not a method output')
    wrapper = _decode_exact_mapping(record['recipe'], 'output Recipe')
    recipe = ArtifactRecipe(wrapper['fields'], recipe_version=wrapper['recipe_version'])
    if recipe.fields.get('artifact_contract') != OUTPUT_CONTRACT:
        raise ConfigurationError('reference does not contain an independent method output')
    if any(record[key] != reference[key] for key in reference) or recipe.recipe_hash != reference['recipe_hash']:
        raise ConfigurationError('method output digest mismatch')
    identity = recipe.fields
    producer = ProducerVersion(**identity['producer_version'])
    from experiments.modular_gu import gu_producer
    current = gu_producer(identity['target']['method'], identity['pairing']['model'])
    if producer != current:
        raise ConfigurationError('method output producer changed; explicit new execution required')
    request = FormalArtifactRequest(ArtifactType.PREDICTION, recipe, producer)
    resolved = resolve_formal_artifact(root, request)
    if resolved is None:
        raise ConfigurationError('method output MISS; Metrics cannot execute producers')
    payload = resolved.payload
    if resolved.content_hash != reference['content_hash']:
        raise ConfigurationError('method output content digest mismatch')
    selection = index.get_artifact(identity['selection']['artifact_id'])
    if any(selection[key] != value for key, value in identity['selection'].items()):
        raise ConfigurationError('output Selection dependency digest mismatch')
    if data is not None:
        expected = pairing_identity(identity['pairing'], data, payload.arrays['selected_nodes'])
        if expected != identity['pairing']:
            raise ConfigurationError('method output Dataset/Split or deletion identity mismatch')
    if dataset_root is None:
        raise ConfigurationError('method output requires explicit Dataset/Split root')
    return resolve_output(payload, dataset_root)


class ResolvedOutput:
    """Verified in-memory inputs; only the underlying result is serialized."""
    def __init__(self, payload, data):
        self.payload = payload
        self.identity = payload.identity
        self.state = payload.state
        self.auxiliary = payload.auxiliary
        pairing = payload.identity['pairing']
        if pairing_identity(pairing, data, payload.arrays['selected_nodes']) != pairing:
            raise ConfigurationError('output Dataset/Split or deletion identity mismatch')
        if len(payload.arrays['logits']) != data.num_nodes:
            raise ConfigurationError('output logits differ from Dataset node count')
        retained = retained_graph(data, payload.arrays['selected_nodes'])
        evaluation = data if pairing['deletion']['evaluation_graph'] == 'original' else retained
        self.arrays = {key: getattr(data, key).detach().cpu().numpy() for key in
                      ('x', 'y', 'edge_index', 'train_mask', 'val_mask', 'test_mask')}
        self.arrays.update(payload.arrays)
        self.arrays.update(retain_mask=retained.train_mask.cpu().numpy(),
            training_edge_index=retained.edge_index.cpu().numpy(),
            evaluation_edge_index=evaluation.edge_index.cpu().numpy())

    @property
    def canonical_bytes(self):
        return self.payload.canonical_bytes

    @property
    def content_hash(self):
        return self.payload.content_hash


def resolve_output(payload, dataset_root):
    from experiments.dataset_inputs import resolve_input
    return ResolvedOutput(payload, resolve_input(payload.identity['dataset_input'], dataset_root))


def build_output(identity, model, logits, logits_before=None):
    def array(tensor):
        return tensor.detach().cpu().numpy()
    arrays = dict(logits=array(logits),
        selected_nodes=np.asarray(identity['pairing']['selected_nodes'], dtype=np.int64))
    if logits_before is not None:
        arrays['logits_before'] = array(logits_before)
    auxiliary = {}
    for name in ('deletion1', 'deletion2'):
        if hasattr(model, name):
            auxiliary[name + '_mask'] = array(getattr(model, name).mask)
    return UnlearningOutputPayload(identity, arrays,
        {key: array(value) for key, value in model.state_dict().items()}, auxiliary)


def utility(payload):
    a = payload.arrays
    mask = a['test_mask']
    after = float(np.mean(a['logits'][mask].argmax(1) == a['y'][mask]))
    before = (float(np.mean(a['logits_before'][mask].argmax(1) == a['y'][mask]))
              if 'logits_before' in a else None)
    drop = before - after if before is not None else None
    return {'f1_before': before, 'f1_after': after, 'f1_drop': drop,
            'f1_drop_ratio': (drop / before * 100 if before > 0 else 0.0) if before is not None else None}


def restore_model(payload):
    """Reconstruct the saved CPU model for independent forward verification."""
    if payload.identity['target']['method'] == 'GraphRevoker':
        from experiments.modular_graphrevoker import restore_graphrevoker
        return restore_graphrevoker(payload)
    from types import SimpleNamespace
    from experiments.modular_model import create_model, runtime_defaults
    arrays = payload.arrays
    config = payload.identity['pairing']['model']
    data = SimpleNamespace(x=torch.tensor(arrays['x']), y=torch.tensor(arrays['y']))
    if payload.identity['target']['method'] == 'GraphEraser':
        from experiments.modular_shards import ShardEnsemble
        assignment = torch.tensor(payload.state['assignment'])
        weights = torch.tensor(payload.state['weights'])
        models = [create_model(config, 'stored', data, torch.device('cpu')) for _ in weights]
        model = ShardEnsemble(models, assignment, weights)
    elif payload.identity['target']['method'] == 'GNNDelete':
        from model.base_gnn.deletion import GCNDelete
        args = runtime_defaults()
        args.update(gcn_num_layers=config['layers'], gcn_hidden=config['hidden_channels'],
                    out_dim=arrays['logits'].shape[1], base_model='GCN', dataset_name='stored',
                    downstream_task='node')
        model = GCNDelete(args, data.x.shape[1], arrays['logits'].shape[1],
            mask_1hop=torch.tensor(payload.auxiliary['deletion1_mask']),
            mask_2hop=torch.tensor(payload.auxiliary['deletion2_mask']))
    else:
        model = create_model(config, 'stored', data, torch.device('cpu'))
    model.load_state_dict({key: torch.tensor(value) for key, value in payload.state.items()}, strict=True)
    if payload.identity['target']['method'] == 'MEGU':
        model.megu_pseudo_labels = torch.tensor(payload.auxiliary['megu_pseudo_labels'])
    return model.eval()
