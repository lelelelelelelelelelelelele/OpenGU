"""Export paired training configurations through the shared pure-weight pipeline."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_plan(path):
    from experiments.effective_config import read_yaml, fields, ConfigurationError
    from experiments.modular_config import model_training, resolve_reference, load_instance
    value = read_yaml(path)
    fields(value, {'kind', 'schema_version', 'experiment_id', 'dataset_ref', 'models', 'groups', 'seeds'},
           {'kind', 'schema_version', 'experiment_id', 'dataset_ref', 'models', 'groups', 'seeds'}, 'checkpoint training')
    if value['kind'] != 'checkpoint_training' or (type(value['schema_version']) is not int or value['schema_version'] != 1):
        raise ConfigurationError('expected checkpoint_training schema_version 1')
    if not value['models'] or not value['groups'] or not value['seeds']:
        raise ConfigurationError('models, groups and seeds must be nonempty')
    if any(type(seed) is not int or seed < 0 for seed in value['seeds']) or len(set(value['seeds'])) != len(value['seeds']):
        raise ConfigurationError('training seeds must be unique nonnegative integers')
    from experiments.modular_execution import _SAFE_ID
    for name in [value['experiment_id']] + list(value['groups']):
        if not isinstance(name, str) or _SAFE_ID.fullmatch(name) is None:
            raise ConfigurationError('unsafe experiment/group identifier')
    dataset_path = resolve_reference('dataset_refs', value['dataset_ref'], Path(path).resolve().parent)
    instances = []
    for group, training in value['groups'].items():
        for model in value['models']:
            for seed in value['seeds']:
                resolved_model, resolved_training = model_training({'model': model, 'training': {**training, 'seed': seed}})
                instances.append({'group': group, 'kind': 'checkpoint_training',
                    'model': resolved_model, 'training': resolved_training})
    from cache_v2 import canonical_sha256
    if len({canonical_sha256(x) for x in instances}) != len(instances):
        raise ConfigurationError('duplicate training cells')
    from utils.target_checkpoint import sha256_file
    return {**value, 'config_path': str(Path(path).resolve()), 'config_sha256': sha256_file(path), 'dataset': load_instance(dataset_path, 'dataset_split'),
            'dataset_directory': str(dataset_path.parent), 'instances': instances}


def train_matrix(plan, data, context):
    """Data is already resolved and verified by the caller's execution boundary."""
    import torch
    from sklearn.metrics import f1_score
    from experiments.modular_model import prepare_model, create_model
    from utils.target_checkpoint import save_weights, capture_state, load_weights, data_identity
    output_root = context.output.parent
    output_root.mkdir(parents=True, exist_ok=False)
    result = {'schema': 'opengu.paired_checkpoints.v1', 'experiment_id': plan['experiment_id'],
              'config_path': plan['config_path'], 'config_sha256': plan['config_sha256'],
              'execution': context.receipt(), 'data_identity': data_identity(data), 'cells': [], 'status': 'running'}
    def persist():
        context.output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    persist()
    try:
        for index, instance in enumerate(plan['instances']):
            model, _, observation = prepare_model(instance, data=data,
                dataset_name=plan['dataset']['dataset']['name'], checkpoint_root=context.checkpoint_root,
                device=context.request_device, reference_directory=plan['dataset_directory'])
            name = '{}-h{}-seed{}'.format(instance['group'], instance['model']['hidden_channels'], instance['training']['seed'])
            path = output_root / '{}-{}.pt'.format(index, name)
            exported = save_weights(path, capture_state(model))
            restored = create_model(instance['model'], plan['dataset']['dataset']['name'], data, context.request_device)
            load_weights(path, restored)
            model.eval()
            with torch.no_grad():
                logits = model(data.x, data.edge_index)
                restored_logits = restored(data.x, data.edge_index)
                if not torch.isfinite(logits).all() or not torch.equal(logits, restored_logits):
                    raise ValueError('nonfinite logits or export changed fixed-input predictions')
                metrics = {}
                for split in ('train', 'val', 'test'):
                    mask = getattr(data, split + '_mask')
                    labels = data.y[mask].cpu().numpy()
                    predicted = logits[mask].argmax(1).cpu().numpy()
                    metrics[split] = {'loss': float(torch.nn.functional.cross_entropy(logits[mask], data.y[mask])),
                        'accuracy': float((labels == predicted).mean()),
                        'macro_f1': float(f1_score(labels, predicted, average='macro'))}
            result['cells'].append({'group': instance['group'], 'model': instance['model'],
                'training': instance['training'], 'preparation': observation,
                'output': {k: exported[k] for k in ('path', 'file_sha256', 'state_hash')},
                'logits_max_abs_error': 0., 'metrics': metrics})
            persist()
        result['status'] = 'completed'
        persist()
    except BaseException as exc:
        result.update(status='failed', error=type(exc).__name__ + ': ' + str(exc))
        persist()
        raise
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--run-id')
    parser.add_argument('--device-config', type=Path, default=ROOT / '.syncmate/device.yaml')
    args = parser.parse_args()
    sys.argv[:] = sys.argv[:1]
    plan = load_plan(args.config)
    if args.dry_run:
        if args.run_id:
            raise ValueError('dry-run has no execution run ID')
        print(json.dumps(plan, indent=2))
        return
    if not args.run_id:
        raise ValueError('execution requires --run-id')
    from experiments.modular_execution import device_context
    from experiments.modular_run import read_dataset
    context = device_context(plan['experiment_id'], run_id=args.run_id, device_file=args.device_config)
    from experiments.dataset_inputs import bind_input
    reference = bind_input(plan['dataset'], plan['dataset_directory'], ROOT)
    if any(not reference[key].startswith('data/processed/') for key in ('manifest', 'graph')):
        raise ValueError('formal training inputs must stay in data/processed')
    data, _ = read_dataset(plan['dataset'], Path(plan['dataset_directory']))
    train_matrix(plan, data.to(context.request_device), context)


if __name__ == '__main__':
    main()
