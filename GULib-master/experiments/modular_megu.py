"""Exact Selection adapter for the existing MEGU update and C&S prediction."""
from __future__ import annotations

import logging
from types import SimpleNamespace
import torch


def megu_node(args, model, data, nodes, runtime_root):
    from unlearning.unlearning_methods.MEGU.megu import megu
    from task.MEGUTrainer import MEGUTrainer
    from experiments.node_deletion import retained_graph
    from torch_geometric.utils import to_scipy_sparse_matrix
    from utils.utils import sparse_mx_to_torch_sparse_tensor, normalize_adj
    logger = logging.getLogger('modular.MEGU')
    retained = retained_graph(data, nodes)
    device = next(model.parameters()).device
    method = megu(args, logger, SimpleNamespace(data=data, model=model))
    method.device = device
    method.temp_node = list(nodes)
    method.unlearning_nodes = list(nodes)
    data.x_unlearn = data.x.clone()
    data.edge_index_unlearn = retained.edge_index
    # The correction anchors must also exclude the erased supervision.
    data.train_mask = retained.train_mask
    data.train_indices = retained.train_indices
    trainer = MEGUTrainer(args, logger, model, data)
    trainer.device = device
    method.target_model = trainer
    # The historical trainer takes its SGD settings from model.config.
    model.config.lr = args['instance']['training']['lr']
    model.config.decay = args['instance']['training']['weight_decay']
    method.adj = sparse_mx_to_torch_sparse_tensor(normalize_adj(
        to_scipy_sparse_matrix(data.edge_index, num_nodes=data.num_nodes))).to(device)
    neighbors = method.neighbor_select(data.x).to(device)
    seconds, _ = trainer.megu_unlearning(list(nodes), neighbors)
    return trainer.model, float(seconds)


def megu_logits(model, evaluation, retain_mask, parameters):
    """Encode true C&S probabilities as logits for the common metric consumer."""
    from task.MEGUTrainer import MEGUTrainer
    probabilities = torch.softmax(model(evaluation.x, evaluation.edge_index), dim=-1)
    context = SimpleNamespace(args=parameters, data=SimpleNamespace(
        train_mask=retain_mask, edge_index_unlearn=evaluation.edge_index))
    probabilities = MEGUTrainer.correct_and_smooth(context, probabilities, model.megu_pseudo_labels)
    if not torch.isfinite(probabilities).all() or (probabilities < 0).any():
        raise ValueError('MEGU C&S produced invalid probabilities')
    return probabilities.clamp_min(torch.finfo(probabilities.dtype).tiny).log().detach().clone()


def build_megu_output(identity, model, logits, logits_before):
    from experiments.unlearning_outputs import build_output
    from cache_v2.unlearning_output import UnlearningOutputPayload
    payload = build_output(identity, model, logits, logits_before)
    return UnlearningOutputPayload(payload.identity, payload.arrays, payload.state,
        {'megu_pseudo_labels': model.megu_pseudo_labels.detach().cpu().numpy()})


def run_megu_unlearning(instance, *, selection, model, data, dataset_name, checkpoint, store_root, runtime_root, dataset_input, dataset_root):
    if instance['method'] != 'MEGU':
        raise ValueError('MEGU consumer requires the MEGU instance')
    from pathlib import Path
    from experiments.modular_gu import gu_producer, GU_METHODS
    from experiments.modular_model import runtime_defaults
    from cache_v2 import ArtifactRecipe, ArtifactType
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact
    from experiments.unlearning_outputs import output_reference, utility
    from experiments.node_deletion import pairing_identity, retained_graph
    from attack.cache_identity import seeded_execution
    from experiments.selection_inputs import make_dataset_selection_inputs
    inputs = make_dataset_selection_inputs(data, dataset_name=dataset_name)
    target = {'method': instance['method'], 'parameters': instance['parameters']}
    if instance['method'] != 'Retrain':
        from utils.target_checkpoint import state_hash
        if state_hash(model.state_dict()) != checkpoint['state_hash']:
            raise ValueError('GU model differs from verified target checkpoint')
        target['checkpoint_state_hash'] = checkpoint['state_hash']
    producer = gu_producer(instance['method'], instance['model'])
    identity = {'dataset_input': dataset_input, 'target': target, 'pairing': pairing_identity(instance, data, selection.selected_nodes),
        'selection': {k: getattr(selection, k) for k in ('artifact_id', 'recipe_hash', 'content_hash')},
        'graph_fingerprint': inputs.graph_fingerprint, 'producer_version': producer.to_dict()}
    request = FormalArtifactRequest(ArtifactType.PREDICTION,
        ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity}), producer)
    stored = resolve_formal_artifact(Path(store_root), request)
    hit = stored is not None
    seconds = 0.0
    if not hit:
        args = runtime_defaults()
        args.update(instance['parameters'])
        args.update(instance=instance, dataset_name=dataset_name,
            base_model='GCN' if instance['model']['architecture'].endswith('GCNNet') else 'SGC',
            downstream_task='node', unlearn_task='node', unlearning_methods=instance['method'],
            num_epochs=instance['training']['epochs'], num_runs=1, run_update_detection_auc=False,
            random_seed=instance['training']['seed'], gcn_num_layers=instance['model']['layers'],
            gcn_hidden=instance['model']['hidden_channels'], formal_expected_k=len(selection.selected_nodes),
            num_unlearned_nodes=len(selection.selected_nodes), formal_fail_closed=True, test_freq=1,
            device=str(data.x.device))
        retained = retained_graph(data, selection.selected_nodes)
        evaluation = data if instance['deletion']['evaluation_graph'] == 'original' else retained
        before = None
        if model is not None:
            model.eval()
            with torch.no_grad():
                before = model(evaluation.x, evaluation.edge_index).detach().clone()
        working = data.clone()
        working.num_classes = int(data.y.max()) + 1
        for name in ('train', 'val', 'test'):
            setattr(working, name + '_indices', getattr(working, name + '_mask').nonzero().flatten().cpu().numpy())
        runtime_path = Path(runtime_root) / 'unlearning' / request.recipe.recipe_hash
        runtime_path.mkdir(parents=True, exist_ok=False)
        with seeded_execution(instance['training']['seed']):
            output_model, seconds = GU_METHODS[instance['method']](args, model, working, list(selection.selected_nodes), runtime_path)
        output_model.eval()
        with torch.no_grad():
            if instance['method'] == 'MEGU':
                logits = megu_logits(output_model, evaluation, retained.train_mask, instance['parameters'])
            else:
                logits = output_model(evaluation.x, evaluation.edge_index).detach().clone()
        payload = build_megu_output(identity, output_model, logits, before)
        stored = store_formal_artifact(store_root, request, payload, compute_seconds=seconds)
    reference = output_reference(stored, request.recipe.recipe_hash)
    from experiments.unlearning_outputs import load_output
    verified = load_output(reference, store_root, data=data, dataset_root=dataset_root)
    from experiments.output_metrics import evaluate_method
    return {**reference, 'output': reference, 'hit': hit, 'producer_called': not hit,
            'compute_seconds': seconds, 'result': utility(verified), 'target': target,
            'evaluation': evaluate_method(reference, verified)}
