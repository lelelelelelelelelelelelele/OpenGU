"""One explicit Ret reference or a bounded four-repetition probe."""
import time
from cache_v2.canonical import canonical_sha256

from attack.cache_identity import seeded_execution
from experiments.modular_model import create_model, train_supervised
from experiments.ret_reference_policy import training_graph, environment
from utils.target_checkpoint import data_identity, state_hash

METRICS = {'final_accuracy', 'final_cross_entropy', 'repetitions'}


def reference_identity(instance, data, nodes):
    spec = instance['reference']
    trained, validation = training_graph(data, nodes, spec['arm'])
    return dict(policy=spec['policy'], arm=spec['arm'],
        role='node_deletion_reference' if spec['arm']=='joint' else 'undeleted_baseline' if spec['arm']=='none' else 'diagnostic_control',
        training_graph_identity=data_identity(trained), validation_graph_identity=data_identity(validation),
        training=instance['training'], numerical_environment_hash=canonical_sha256(environment(spec['policy'],data.x.device,data.x.dtype)),
        primary_endpoint='final3000', auxiliary_endpoint='validation_best',
        selection_rule='maximum_validation_accuracy_earliest_tie', validation_mask='original_val_mask')


def train_reference(instance, data, nodes, dataset_name, *, observer, asset_root, dataset_root, prior=None, mode='reference'):
    if observer is None or instance['training']['epochs'] != 3000 or instance['model']['architecture']!='OpenGU.GCNNet':
        raise ValueError('Ret references require Observer, GCN and fixed 3000 epochs')
    graph, validation = training_graph(data, nodes, instance['reference']['arm'])
    identity = reference_identity(instance, data, nodes)
    if mode not in ('reference','probe'):
        raise ValueError('unknown Ret reference mode')
    repeats = [('reference',True)] if mode=='reference' else [('off1',False),('off2',False),('on1',True),('on2',True)]
    started = time.perf_counter()
    statistics = []
    for repeat, observe in repeats:
        seed = instance['training']['seed']
        with seeded_execution(seed):
            model = create_model(instance['model'],dataset_name,graph,data.x.device)
        initial = state_hash(model.state_dict())
        with seeded_execution(seed):
            from experiments.observers.ret_reference import rng_identity
            execution = {**identity, 'environment':environment(instance['reference']['policy'],data.x.device,data.x.dtype),
                'initial_state_hash':initial,'training_start_rng':rng_identity(model)}
            observer({'phase':'reference_start','step':0,'values':dict(model=model, validation=validation,
                identity=execution,repeat=repeat,observe=observe)})
            _, stats = train_supervised(model,graph,instance['training'],(),epoch_end=observer)
            observer({'phase':'training_complete','step':3000,'values':dict(model=model,original=data,
                validation=validation,prior=prior,asset_root=asset_root,dataset_root=dataset_root)})
        statistics.append(stats)
    observer.identity['reference_execution'] = [r['identity'] for r in observer.items[0][1].replays]
    return model, time.perf_counter()-started, statistics
