"""Target-direct execution of independent GU/Retrain followed by output Metrics."""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import torch

from experiments.modular_config import load_instance, unlearning
from experiments.modular_gu import run_unlearning
from experiments.modular_model import create_model
from experiments.modular_run import verified_selection
from experiments.unlearning_outputs import load_output
from utils.target_checkpoint import data_identity, load_target_checkpoint


def update_detection_auc(payload):
    """Existing GNNDelete posterior-change AUC, evaluated from persisted logits."""
    from sklearn.metrics import roc_auc_score
    a = payload.arrays
    members = a['selected_nodes']
    nonmembers = np.flatnonzero(a['test_mask'])
    n = min(len(members), len(nonmembers))
    if n < 2:
        return None
    rows = np.concatenate((members[:n], nonmembers[:n]))
    before = torch.softmax(torch.tensor(a['logits_before']), dim=1).numpy()
    after = torch.softmax(torch.tensor(a['logits']), dim=1).numpy()
    change = np.linalg.norm(before[rows] - after[rows], axis=1)
    return float(roc_auc_score(np.r_[np.ones(n), np.zeros(n)], change))


def execute_bound_outputs(*, gu, retrain, selection, data, dataset_name, checkpoint,
                          store_root, runtime_root):
    """Shared CPU-testable execution seam; caller owns verified input binding."""
    from attack.cache_identity import seeded_execution
    if gu['model'] != retrain['model'] or gu['training'] != retrain['training'] or gu['deletion'] != retrain['deletion']:
        raise ValueError('GU and independent Retrain training/deletion contracts differ')
    if checkpoint['metadata']['data_identity'] != data_identity(data):
        raise ValueError('checkpoint Dataset/Split differs from execution input')
    if checkpoint['metadata'].get('training') != gu['training']:
        raise ValueError('checkpoint has no matching explicit training conditions')
    with seeded_execution(gu['training']['seed']):
        model = create_model(gu['model'], dataset_name, data, data.x.device)
    model.load_state_dict(checkpoint['state_dict'], strict=True)
    common = dict(selection=selection, data=data, dataset_name=dataset_name,
                  store_root=store_root, runtime_root=runtime_root)
    gu_row = run_unlearning(gu, model=model, checkpoint=checkpoint, **common)
    retrain_row = run_unlearning(retrain, model=None, checkpoint=None, **common)
    return gu_row, retrain_row


def execute_cell(cfg, method, strategy, seed, selection_artifact, *, output_dir, fingerprint, git_sha):
    from experiments.processed_provider import processed_split_contract
    from experiments.target_direct_v1.split_profile import verify_profile
    from eval_collateral import evaluate_outputs
    if method not in ('GNNDelete', 'GIF') or cfg['base_model'] != 'GCN':
        raise ValueError('persisted-output matrix consumer supports GCN GNNDelete/GIF')
    if not selection_artifact or not selection_artifact.get('target_checkpoint'):
        raise ValueError('output execution requires existing Selection and exact target checkpoint')
    if not cfg.get('retrain_ref') or not cfg.get('evaluation_ref'):
        raise ValueError('output execution requires explicit retrain_ref and evaluation_ref')
    if cfg.get('extra_args') != ['--num_threads', '1'] or cfg.get('method_overrides'):
        raise ValueError('target-direct output stage requires registered method tables, not extra argument overrides')
    device = torch.device('cuda')
    if not torch.cuda.is_available():
        raise RuntimeError('formal target-direct output execution requires CUDA')
    torch.set_num_threads(1)
    repo = Path(__file__).resolve().parents[2]
    profile = verify_profile(repository_root=repo, processed_root=Path(cfg['processed_root']),
        dataset=cfg['dataset'], contract=processed_split_contract(cfg, require_explicit=True, require_profile=True))
    data, inputs = profile['data'].to(device), profile['inputs']
    root = Path(cfg['_source_path']).resolve().parent
    from experiments.effective_config import read_yaml, fields
    declaration = read_yaml(root / cfg['retrain_ref'])
    fields(declaration, {'kind', 'schema_version', 'method'}, {'kind', 'schema_version', 'method'}, 'formal Retrain table')
    retrain_table = load_instance(root / cfg['retrain_ref'], 'unlearning')
    if retrain_table['method'] != 'Retrain':
        raise ValueError('retrain_ref must select Retrain')
    # The registered target-direct lane binds model seed/epochs/shape on its shared axes.
    model = {'architecture': 'OpenGU.GCNNet', 'layers': cfg['model_overrides']['GCN']['gcn_num_layers'],
             'hidden_channels': cfg['model_overrides']['GCN']['gcn_hidden'], 'dropout': 0.5}
    training = {**retrain_table['training'], 'epochs': cfg['defaults']['num_epochs'], 'seed': seed}
    retrain = {**retrain_table, 'model': model, 'training': training}
    gu = unlearning({'kind': 'unlearning', 'schema_version': 1, 'method': method,
                     'model': model, 'training': training, 'deletion': retrain['deletion']})
    ref = {key: selection_artifact[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
    store_root = Path(selection_artifact['store_root'])
    selection = verified_selection(ref, store_root=store_root, data=data, inputs=inputs)
    bound = selection_artifact['target_checkpoint']
    checkpoint = load_target_checkpoint(bound['path'], expected_file_sha256=bound['file_sha256'],
        expected_state_hash=bound['state_hash'], expected_metadata={'dataset_name': cfg['dataset'].lower(),
            'base_model': 'GCN', 'seed': seed, 'training': training})
    gu_row, retrain_row = execute_bound_outputs(gu=gu, retrain=retrain, selection=selection,
        data=data, dataset_name=cfg['dataset'].lower(), checkpoint=checkpoint,
        store_root=store_root, runtime_root=Path(cfg['runtime_root']) / strategy / method / str(seed))
    pairs = [{'strategy': strategy, 'unlearning': gu_row['output'], 'retrain': retrain_row['output']}]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / 'output-references.json').open('x', encoding='utf-8') as handle:
        json.dump(pairs, handle, indent=2)
    payload = load_output(gu_row['output'], store_root)
    auc = update_detection_auc(payload) if cfg['defaults']['run_update_detection_auc'] else None
    result = {**gu_row['result'], 'failed': False, 'selected_nodes': list(selection.selected_nodes),
              'mia_auc': auc, 'output': gu_row['output'], 'retrain_output': retrain_row['output']}
    with (output_dir / 'attack.json').open('x', encoding='utf-8') as handle:
        json.dump({'results': {strategy: result}, 'producer_observations': {
            'GU': gu_row['producer_called'], 'Retrain': retrain_row['producer_called']}}, handle, indent=2)
    evaluate_outputs(load_instance(root / cfg['evaluation_ref'], 'evaluation'), pairs,
                     store_root=store_root, output_dir=output_dir)
    meta = {'config_fingerprint': fingerprint, 'fingerprint_version': 'v4-independent-outputs',
            'method': method, 'strategy': strategy, 'seed': seed, 'git_sha': git_sha,
            'selection_artifact': selection_artifact, 'output_references': pairs,
            'training_producer_called_by_metrics': False,
            'metric_policy': {'update_detection_auc': {'enabled': cfg['defaults']['run_update_detection_auc'],
                'status': 'computed' if auc is not None else ('insufficient_samples' if cfg['defaults']['run_update_detection_auc'] else 'disabled_by_config')}}}
    with (output_dir / '_meta.json').open('x', encoding='utf-8') as handle:
        json.dump(meta, handle, indent=2)
    return 'completed'
