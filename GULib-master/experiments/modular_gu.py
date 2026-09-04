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
    return float(method.average_f1[0]), float(method.avg_unlearning_time[0])


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
    return float(method.average_f1[0]), float(method.avg_unlearning_time[0])


GU_METHODS = {'GNNDelete': gnndelete_node, 'GIF': gif_node}


def gu_producer(method, model):
    runtime_defaults()
    if method == 'GNNDelete':
        from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete
        from task.GNNDeleteTrainer import GNNDeleteTrainer
        from model.base_gnn.deletion import GCNDelete, DeletionLayer
        functions = [gnndelete, GNNDeleteTrainer, GCNDelete, DeletionLayer]
    else:
        from unlearning.unlearning_methods.GIF.gif import gif
        from task.GIFTrainer import GIFTrainer
        functions = [gif, GIFTrainer]
    if method == 'GIF':
        functions += [type(model).reason_once, type(model).reason_once_unlearn]
    return ProducerVersion('modular-opengu-node-gu-v1',
        implementation_fingerprint(GU_METHODS[method], *functions))


def run_unlearning(instance, *, selection, model, data, dataset_name, checkpoint, store_root, runtime_root):
    from attack.result_cache import ResultCache
    from attack.attack_result import AttackResult
    from attack.cache_identity import seeded_execution
    from experiments.selection_inputs import make_dataset_selection_inputs
    cache = ResultCache(store_root)
    inputs = make_dataset_selection_inputs(data, dataset_name=dataset_name)
    producer = gu_producer(instance['method'], model)
    target = {'method': instance['method'], 'model': instance['model'], 'training': instance['training'],
              'parameters': instance['parameters'], 'checkpoint_state_hash': checkpoint['state_hash'],
              'data_identity': data_identity(data)}
    request = cache.request(selection, inputs.graph_fingerprint, ordered_int_hash(selection.selected_nodes), target, producer)
    cached, provenance = cache.get_with_provenance(request)
    if cached is not None:
        return {'recipe_hash': request.recipe.recipe_hash, 'artifact_id': provenance['cache_key'],
                'hit': True, 'producer_called': False, 'result': cached.to_dict(), 'target': target}
    args = runtime_defaults()
    args.update(instance['parameters'])
    args.update(dataset_name=dataset_name, base_model='GCN' if instance['model']['architecture'].endswith('GCNNet') else 'SGC',
        downstream_task='node', unlearn_task='node', unlearning_methods=instance['method'],
        num_epochs=instance['training']['epochs'], num_runs=1, run_update_detection_auc=False,
        random_seed=instance['training']['seed'], gcn_num_layers=instance['model']['layers'],
        gcn_hidden=instance['model']['hidden_channels'], formal_expected_k=len(selection.selected_nodes),
        num_unlearned_nodes=len(selection.selected_nodes), formal_fail_closed=True, test_freq=1,
        device=str(data.x.device))
    model.eval()
    with torch.no_grad():
        before = float((model(data.x, data.edge_index)[data.test_mask].argmax(1) == data.y[data.test_mask]).float().mean())
    working = data.clone()
    working.num_classes = int(data.y.max()) + 1
    for name in ('train', 'val', 'test'):
        setattr(working, name + '_indices', getattr(working, name + '_mask').nonzero().flatten().cpu().numpy())
    runtime_path = Path(runtime_root) / 'unlearning' / request.recipe.recipe_hash
    runtime_path.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    with seeded_execution(instance['training']['seed']):
        after, seconds = GU_METHODS[instance['method']](args, model, working, list(selection.selected_nodes), runtime_path)
    if not torch.isfinite(torch.tensor([before, after, seconds])).all():
        raise ValueError('GU returned non-finite metrics')
    result = AttackResult(strategy_name=selection.selector, selected_nodes=list(selection.selected_nodes),
        f1_before=before, f1_after=after, unlearn_time=seconds, total_time=time.perf_counter()-started,
        selection_time=0.0, selection_artifact_id=selection.artifact_id, selection_recipe_hash=selection.recipe_hash,
        selection_content_hash=selection.content_hash, selection_authoritative=True, config=target)
    stored = cache.save(result, request)
    return {'recipe_hash': request.recipe.recipe_hash, 'artifact_id': stored.artifact_id, 'hit': False,
            'producer_called': True, 'result': result.to_dict(), 'target': target}
