"""Selection-to-GU adapter using OpenGU's existing node deletion consumers."""
from __future__ import annotations

import logging
import time
from pathlib import Path
import torch
from cache_v2 import ProducerVersion
from cache_v2.formal_artifacts import ordered_int_hash
from experiments.implementation_identity import implementation_fingerprint
from experiments.modular_model import runtime_defaults
from utils.target_checkpoint import data_identity


def gnndelete_node(args, model, data, nodes, runtime_root):
    from model.model_zoo import model_zoo
    from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete
    from task.GNNDeleteTrainer import GNNDeleteTrainer
    logger = logging.getLogger('modular.GNNDelete')
    zoo = model_zoo(args, data)
    zoo.model = model
    method = gnndelete(args, logger, zoo)
    method.device = next(model.parameters()).device
    args['checkpoint_dir'] = str(runtime_root)
    args['unlearning_model'] = 'gnndelete_nodeemb'
    method.target_model = GNNDeleteTrainer(args, logger, model, data)
    method.target_model.device = method.device
    method.delete_node(nodes)
    return method.target_model.model, float(method.avg_unlearning_time[0])


def gif_node(args, model, data, nodes, runtime_root):
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    from task.GIFTrainer import GIFTrainer
    logger = logging.getLogger('modular.GIF')
    method = gif(args, logger, SimpleNamespace(data=data, model=model))
    method.device = next(model.parameters()).device
    method.target_model = GIFTrainer(args, logger, model, data)
    method.target_model.device = method.device
    method.target_model_name = args['base_model']
    model.eval()
    method.unlearning_request(nodes)
    method.unlearn()
    return method.target_model.model, float(method.avg_unlearning_time[0])


def retrain_node(args, model, data, nodes, runtime_root):
    from unlearning.unlearning_methods.Retrain.retrain import run_retrain
    return run_retrain(args['instance'], data, nodes, args['dataset_name'])


GU_METHODS = {'GNNDelete': gnndelete_node, 'GIF': gif_node, 'Retrain': retrain_node}


def gu_producer(method, model_config):
    runtime_defaults()
    from experiments.modular_model import train_supervised
    from experiments.implementation_identity import model_functions
    from experiments.node_deletion import retained_graph, pairing_identity
    from experiments.unlearning_outputs import build_output
    from unlearning.unlearning_methods.Retrain.retrain import run_retrain
    from model.base_gnn.gcn import GCNNet
    from model.base_gnn.sgc import SGCNet
    model_class = GCNNet if model_config['architecture'] == 'OpenGU.GCNNet' else SGCNet
    functions = [model_class.__init__, model_class.forward, model_class.load_config,
                 retained_graph, pairing_identity, build_output, GU_METHODS[method]]
    if method == 'GNNDelete':
        from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete
        from task.GNNDeleteTrainer import GNNDeleteTrainer
        from model.base_gnn.deletion import GCNDelete, DeletionLayer
        functions += [gnndelete, GNNDeleteTrainer, GCNDelete, DeletionLayer, gnndelete_node]
    elif method == 'GIF':
        from unlearning.unlearning_methods.GIF.gif import gif
        from task.GIFTrainer import GIFTrainer
        functions += [gif, GIFTrainer, gif_node, model_class.reason_once, model_class.reason_once_unlearn]
    elif method == 'Retrain':
        functions += [run_retrain, train_supervised]
    else:
        raise ValueError('unsupported independent method: ' + method)
    import inspect
    from cache_v2 import canonical_sha256
    return ProducerVersion('opengu-independent-node-output-v1', canonical_sha256({
        'method_implementation': implementation_fingerprint(*functions),
        'execution_implementation': inspect.getsource(run_unlearning),
    }))


def run_unlearning(instance, *, selection, model, data, dataset_name, checkpoint, store_root, runtime_root):
    from cache_v2 import ArtifactRecipe, ArtifactType
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact
    from experiments.unlearning_outputs import build_output, output_reference, utility
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
    identity = {'target': target, 'pairing': pairing_identity(instance, data, selection.selected_nodes),
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
            logits = output_model(evaluation.x, evaluation.edge_index).detach().clone()
        payload = build_output(identity, data, output_model, logits, before)
        stored = store_formal_artifact(store_root, request, payload, compute_seconds=seconds)
    reference = output_reference(stored, request.recipe.recipe_hash)
    from experiments.unlearning_outputs import load_output
    verified = load_output(reference, store_root, data=data)
    from experiments.output_metrics import evaluate_method
    return {**reference, 'output': reference, 'hit': hit, 'producer_called': not hit,
            'compute_seconds': seconds, 'result': utility(verified), 'target': target,
            'evaluation': evaluate_method(reference, verified)}
