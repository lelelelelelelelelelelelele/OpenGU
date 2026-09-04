"""Independent target-direct methods sharing only computations they consume."""
from __future__ import annotations

from functools import partial
import torch

from experiments.effective_config import effective, choice, ConfigurationError
from experiments.c_target_v1.core import (
    checkpoint_point_gradients, inverse_hessian_target, graph_source_scores,
    deployed_cross_gradient_scores,
)
from experiments.target_direct_v1.scoring import (
    degree_scores, deterministic_random_scores, inverse_hessian_vectors,
    hutchinson_parameter_change_scores, weighted_checkpoint_scores,
)


SCORE_NAMES = (
    'a_grad_norm', 'b_param_hutch', 'degree', 'gt_full', 'gt_simple', 'legacy',
    'p_graph', 'p_point', 'p_simple', 'r_point', 'random',
    'tracin_cp_graph_3', 'tracin_cp_graph_6', 'tracin_cp_point_3',
    'tracin_cp_point_6', 'tracin_cp_simple_3', 'tracin_cp_simple_6',
)
LISSA_DEFAULTS = {'iterations': 20, 'scale': 25.0, 'damp': 0.01}
HESSIAN_LOSS = {'type': 'cross_entropy', 'source': 'train_mask', 'reduction': 'mean'}
TARGET_LOSS = {'type': 'cross_entropy', 'source': 'validation_mask', 'reduction': 'mean'}
GRAPH_METHODS = frozenset({'p_graph', 'p_simple', 'gt_full', 'gt_simple'})
IHVP_METHODS = frozenset({'b_param_hutch', 'r_point', 'gt_full', 'gt_simple'})


def uses_model(name):
    return name not in {'degree', 'random'}


def uses_target(name):
    return uses_model(name) and name not in {'a_grad_norm', 'b_param_hutch', 'legacy'}


def uses_graph_source(name):
    return name in GRAPH_METHODS or name.startswith(('tracin_cp_graph_', 'tracin_cp_simple_'))


def parameter_defaults(name):
    choice(name, SCORE_NAMES, 'selector method')
    value = {}
    if uses_model(name):
        value['parameter_scope'] = 'last_layer'
    if uses_target(name):
        value['target_loss'] = TARGET_LOSS
    if name in IHVP_METHODS:
        value.update(hessian_loss=HESSIAN_LOSS, lissa=LISSA_DEFAULTS)
    if uses_graph_source(name):
        value['affected_hops'] = 2
    if name == 'b_param_hutch':
        value['hutchinson'] = {'probes': 32, 'seed': 1729}
    if name == 'random':
        value['seed'] = 104245
    if name.startswith('tracin_cp_'):
        value['checkpoint_view'] = 'cp3' if name.endswith('_3') else 'cp_all'
        value['checkpoint_steps'] = []
    return value


def resolve_parameters(name, supplied=None):
    params = effective({} if supplied is None else supplied, parameter_defaults(name))
    if 'parameter_scope' in params:
        choice(params['parameter_scope'], ('last_layer', 'all_trainable'), 'parameter_scope')
    for loss in ('target_loss', 'hessian_loss'):
        if loss in params and params[loss] != (TARGET_LOSS if loss == 'target_loss' else HESSIAN_LOSS):
            raise ConfigurationError(f'{name} has a fixed {loss} definition')
    if 'lissa' in params:
        p = params['lissa']
        if p['iterations'] <= 0 or p['scale'] <= 0 or not 0 <= p['damp'] < 1:
            raise ConfigurationError('invalid LiSSA settings')
    if 'hutchinson' in params and (params['hutchinson']['probes'] <= 0 or params['hutchinson']['seed'] < 0):
        raise ConfigurationError('invalid Hutchinson settings')
    if params.get('affected_hops', 1) <= 0 or params.get('seed', 0) < 0:
        raise ConfigurationError('invalid hops/seed')
    if 'checkpoint_view' in params:
        choice(params['checkpoint_view'], ('cp3', 'cp_all'), 'checkpoint_view')
        steps = params['checkpoint_steps']
        if steps and (len(steps) < 3 or any(type(step) is not int or step <= 0 for step in steps)
                      or steps != sorted(set(steps))):
            raise ConfigurationError('checkpoint_steps must be unique increasing positive integers, at least three')
    return params


class Computations:
    """One invocation can reuse equal point/graph/IHVP intermediates on MISS."""
    def __init__(self, model, data, checkpoints):
        self.model, self.data, self.checkpoints = model, data, checkpoints
        self.candidates = torch.where(data.train_mask)[0].sort().values
        self.targets = torch.where(data.val_mask)[0].sort().values
        self.memo = {}

    def point(self, index, scope):
        key = ('point', index, scope)
        if key not in self.memo:
            self.memo[key] = checkpoint_point_gradients(
                self.model, self.data, state=self.checkpoints[index]['state'],
                candidate_ids=self.candidates, target_ids=self.targets, parameter_scope=scope)
        return self.memo[key]

    def inverse(self, p):
        key = ('inverse', p['parameter_scope'], tuple(sorted(p['lissa'].items())))
        if key not in self.memo:
            self.memo[key] = inverse_hessian_target(
                self.model, self.data, state=self.checkpoints[-1]['state'],
                hessian_train_ids=self.candidates, target_ids=self.targets,
                parameter_scope=p['parameter_scope'], **p['lissa'])[1]
        return self.memo[key]

    def graph(self, index, p, inverse=False):
        key = ('graph', index, p['parameter_scope'], p['affected_hops'],
               tuple(sorted(p['lissa'].items())) if inverse else None)
        if key not in self.memo:
            target = self.point(index, p['parameter_scope'])[1]
            self.memo[key] = graph_source_scores(
                self.model, self.data, state=self.checkpoints[index]['state'],
                candidate_ids=self.candidates, source_ids=self.candidates,
                parameter_scope=p['parameter_scope'], affected_hops=p['affected_hops'],
                target_gradient=target, inverse_target=self.inverse(p) if inverse else target)[0]
        return self.memo[key]


def score_degree(c, p):
    return degree_scores(c.data.edge_index, c.candidates, int(c.data.num_nodes))


def score_random(c, p):
    return deterministic_random_scores(len(c.candidates), p['seed'])


def score_a(c, p):
    return c.point(len(c.checkpoints)-1, p['parameter_scope'])[0].norm(dim=1)


def score_legacy(c, p):
    return deployed_cross_gradient_scores(c.point(len(c.checkpoints)-1, p['parameter_scope'])[0])


def score_b(c, p):
    matrix = c.point(len(c.checkpoints)-1, p['parameter_scope'])[0]
    generator = torch.Generator(device='cpu').manual_seed(p['hutchinson']['seed'])
    probes = torch.randint(0, 2, (p['hutchinson']['probes'], matrix.shape[1]), generator=generator)
    probes = probes.to(dtype=matrix.dtype).mul(2).sub(1)
    inverse, _ = inverse_hessian_vectors(
        c.model, c.data, state=c.checkpoints[-1]['state'], hessian_train_ids=c.candidates,
        parameter_scope=p['parameter_scope'], vectors=probes, **p['lissa'])
    return hutchinson_parameter_change_scores(matrix, inverse.to(matrix.device))


def score_r(c, p):
    return c.point(len(c.checkpoints)-1, p['parameter_scope'])[0].mv(c.inverse(p))


def score_point(c, p):
    matrix, target = c.point(len(c.checkpoints)-1, p['parameter_scope'])
    return matrix.mv(target)


def score_graph(c, p, *, name):
    return c.graph(len(c.checkpoints)-1, p, name.startswith('gt_'))[name]


def checkpoint_indices(count, view):
    if count < 3:
        raise ConfigurationError('TracIn requires at least three checkpoints')
    return (0, count // 2, count-1) if view == 'cp3' else tuple(range(count))


def selected_checkpoint_indices(checkpoints, p):
    steps = p.get('checkpoint_steps', [])
    available = {item['global_step']: i for i, item in enumerate(checkpoints)}
    if any(step not in available for step in steps):
        raise ConfigurationError('requested checkpoint step is absent from the verified trajectory')
    indices = [available[step] for step in steps] if steps else list(range(len(checkpoints)))
    return tuple(indices[i] for i in checkpoint_indices(len(indices), p['checkpoint_view']))


def score_trajectory(c, p, *, source):
    indices = selected_checkpoint_indices(c.checkpoints, p)
    vectors, weights = [], []
    for index in indices:
        if source == 'point':
            matrix, target = c.point(index, p['parameter_scope'])
            vectors.append(matrix.mv(target).to(torch.float64))
        else:
            vectors.append(c.graph(index, p)['p_' + source].to(torch.float64))
        weights.append(float(c.checkpoints[index]['update_lr']))
    return weighted_checkpoint_scores(vectors, weights, range(len(indices)))


METHODS = {'degree': score_degree, 'random': score_random, 'a_grad_norm': score_a,
           'b_param_hutch': score_b, 'legacy': score_legacy, 'r_point': score_r, 'p_point': score_point}
METHODS.update({name: partial(score_graph, name=name) for name in GRAPH_METHODS})
METHODS.update({name: partial(score_trajectory, source=name.split('_')[2])
                for name in SCORE_NAMES if name.startswith('tracin_cp_')})


def implementation_functions(name):
    function = METHODS[name]
    functions = [function.func if isinstance(function, partial) else function]
    if uses_model(name):
        functions += [Computations.point]
    if uses_graph_source(name):
        functions += [Computations.graph]
    if name in {'r_point', 'gt_simple', 'gt_full'}:
        functions += [Computations.inverse]
    return functions
