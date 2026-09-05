"""Execute one configured method and save its independent model/metric output."""
from __future__ import annotations

import json
from pathlib import Path
import torch

from experiments.modular_config import load_instance
from experiments.modular_gu import run_unlearning
from experiments.modular_model import create_model
from experiments.modular_run import verified_selection
from experiments.unlearning_outputs import load_output
from utils.target_checkpoint import data_identity, load_target_checkpoint


def execute_bound_method(*, instance, selection, data, dataset_name, checkpoint,
                         store_root, runtime_root):
    """One method only; Retrain neither requires nor loads a target checkpoint."""
    from attack.cache_identity import seeded_execution
    model = None
    if instance['method'] == 'Retrain':
        if checkpoint is not None:
            raise ValueError('Retrain does not consume a trained checkpoint')
    else:
        if checkpoint is None or checkpoint['metadata']['data_identity'] != data_identity(data):
            raise ValueError('checkpoint Dataset/Split differs from execution input')
        if checkpoint['metadata'].get('training') != instance['training']:
            raise ValueError('checkpoint has no matching explicit training conditions')
        with seeded_execution(instance['training']['seed']):
            model = create_model(instance['model'], dataset_name, data, data.x.device)
        model.load_state_dict(checkpoint['state_dict'], strict=True)
    return run_unlearning(instance, selection=selection, data=data, dataset_name=dataset_name,
        model=model, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root)


def cell_instance(cfg, method, seed):
    """Resolve the selected method table and the formal lane's shared model axes."""
    root = Path(cfg['_source_path']).resolve().parent
    from experiments.effective_config import fields, read_yaml
    instances = []
    for ref in cfg['unlearning_refs']:
        fields(read_yaml(root / ref), {'kind', 'schema_version', 'method', 'parameters'},
               {'kind', 'schema_version', 'method'}, 'formal method table')
        instances.append(load_instance(root / ref, 'unlearning'))
    matches = [item for item in instances if item['method'] == method]
    if len(matches) != 1:
        raise ValueError('cell needs exactly one matching Unlearning YAML')
    instance = matches[0]
    model = {'architecture': 'OpenGU.GCNNet', 'layers': cfg['model_overrides']['GCN']['gcn_num_layers'],
             'hidden_channels': cfg['model_overrides']['GCN']['gcn_hidden'], 'dropout': 0.5}
    training = {**instance['training'], 'epochs': cfg['defaults']['num_epochs'], 'seed': seed}
    return {**instance, 'model': model, 'training': training}


def save_method_result(row, *, store_root, output_dir, strategy, meta):
    """Export complete per-method state/predictions and a metrics receipt for collection."""
    payload = load_output(row['output'], store_root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {**row['result'], 'failed': False,
              'selected_nodes': payload.arrays['selected_nodes'].tolist(),
              'output': row['output'], 'evaluation': row['evaluation'],
              'producer_called': row['producer_called'], 'cache_hit': row['hit'],
              'compute_seconds': row['compute_seconds']}
    documents = {'attack.json': {'results': {strategy: result}},
                 'output-references.json': {'strategy': strategy, 'output': row['output']},
                 '_meta.json': {**meta, 'output_reference': row['output'],
                               'evaluation_receipt_id': row['evaluation']['evaluation_receipt_id']}}
    for name, value in documents.items():
        with (output_dir / name).open('x', encoding='utf-8') as handle:
            json.dump(value, handle, indent=2, allow_nan=False)
    with (output_dir / 'predictions.npz').open('xb') as handle:
        handle.write(payload.canonical_bytes)
    return result


def execute_cell(cfg, method, strategy, seed, selection_artifact, *, output_dir, fingerprint, git_sha):
    from experiments.processed_provider import processed_split_contract
    from experiments.target_direct_v1.split_profile import verify_profile
    if method not in ('GNNDelete', 'GIF', 'Retrain') or cfg['base_model'] != 'GCN':
        raise ValueError('persisted-output matrix consumer supports GCN GNNDelete/GIF/Retrain')
    if not selection_artifact:
        raise ValueError('method execution requires an existing Selection')
    if cfg.get('extra_args') != ['--num_threads', '1'] or cfg.get('method_overrides'):
        raise ValueError('target-direct output stage requires registered method tables, not extra argument overrides')
    if not torch.cuda.is_available():
        raise RuntimeError('formal target-direct output execution requires CUDA')
    torch.set_num_threads(1)
    instance = cell_instance(cfg, method, seed)
    repo = Path(__file__).resolve().parents[2]
    profile = verify_profile(repository_root=repo, processed_root=Path(cfg['processed_root']),
        dataset=cfg['dataset'], contract=processed_split_contract(cfg, require_explicit=True, require_profile=True))
    data, inputs = profile['data'].to('cuda'), profile['inputs']
    ref = {key: selection_artifact[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
    store_root = Path(selection_artifact['store_root'])
    selection = verified_selection(ref, store_root=store_root, data=data, inputs=inputs)
    checkpoint = None
    if method != 'Retrain':
        bound = selection_artifact['target_checkpoint']
        checkpoint = load_target_checkpoint(bound['path'], expected_file_sha256=bound['file_sha256'],
            expected_state_hash=bound['state_hash'], expected_metadata={'dataset_name': cfg['dataset'].lower(),
                'base_model': 'GCN', 'seed': seed, 'training': instance['training']})
    row = execute_bound_method(instance=instance, selection=selection, data=data,
        dataset_name=cfg['dataset'].lower(), checkpoint=checkpoint,
        store_root=store_root, runtime_root=Path(cfg['runtime_root']) / strategy / method / str(seed))
    save_method_result(row, store_root=store_root, output_dir=output_dir, strategy=strategy,
        meta={'config_fingerprint': fingerprint, 'fingerprint_version': 'v5-single-method-output',
              'method': method, 'strategy': strategy, 'seed': seed, 'git_sha': git_sha,
              'selection_artifact': selection_artifact, 'comparison_stage': 'deferred'})
    return 'completed'
