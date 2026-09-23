"""Observe parameter and same-graph prediction changes across unlearning."""
import json

import torch

from experiments.effective_config import ConfigurationError, fields


def norm(value):
    return float(torch.linalg.vector_norm(value.detach().double()))


class SameGraphChange:
    version = 'same-graph-change-v1'
    requires = {'unlearning_start': {'model', 'graphs'}, 'unlearning_end': {'model', 'graphs'}}
    files = ('result.json',)

    def __init__(self, parameters):
        defaults = dict(graphs=['original', 'retained'], node_scope='all', utility_mask='test_mask',
            f1_average='micro', record=['parameter_delta_l2', 'parameter_delta_relative_l2',
            'logits_delta_l2', 'logits_delta_max_abs', 'prediction_flip_rate', 'accuracy', 'f1'])
        fields(parameters, set(defaults), (), 'same_graph_change')
        self.parameters = {**defaults, **parameters}
        if self.parameters != defaults:
            raise ConfigurationError('unsupported same_graph_change parameters')
        self.before = None
        self.result = {}

    def snapshot(self, model, graphs):
        # Restore every submodule's mode, including mixed train/eval models.
        modes = [(module, module.training) for module in model.modules()]
        try:
            model.eval()
            with torch.no_grad():
                return (torch.cat([p.detach().flatten() for p in model.parameters()]).clone(),
                        {name: model(g.x, g.edge_index).detach().clone() for name, g in graphs.items()})
        finally:
            for module, mode in modes:
                module.training = mode

    def __call__(self, event):
        if event['phase'] not in self.requires:
            return
        v = event['values']
        state, logits = self.snapshot(v['model'], v['graphs'])
        if event['phase'] == 'unlearning_start':
            self.before = state, logits
            return
        if self.before is None:
            raise ValueError('same_graph_change missing start')
        baseline, before = self.before
        size = norm(baseline)
        self.result = dict(parameter_delta_l2=norm(state-baseline),
            parameter_delta_relative_l2=norm(state-baseline)/size if size else None, graphs={})
        for name, graph in v['graphs'].items():
            old, new = before[name], logits[name]
            mask = graph.test_mask
            if not bool(mask.any()):
                raise ValueError('same_graph_change requires nonempty test_mask')
            accuracy = float((new[mask].argmax(1) == graph.y[mask]).float().mean())
            baseline_accuracy = float((old[mask].argmax(1) == graph.y[mask]).float().mean())
            self.result['graphs'][name] = dict(logits_delta_l2=norm(new-old),
                logits_delta_max_abs=float((new-old).abs().max()),
                prediction_flip_rate=float((new.argmax(1) != old.argmax(1)).float().mean()),
                accuracy=accuracy, f1=accuracy, baseline_accuracy=baseline_accuracy, baseline_f1=baseline_accuracy)

    def save(self, folder, metadata):
        if metadata['status'] == 'completed' and not self.result:
            raise ValueError('same_graph_change missing end coverage')
        (folder/'result.json').write_text(json.dumps({**metadata, 'measurements': self.result,
            'coverage': ['unlearning_start', 'unlearning_end'] if self.result else ['unlearning_start'] if self.before else [],
            'comparison': 'GU(graph) versus PT(same graph); all-node logits; test-mask single-label micro F1'},
            indent=2, allow_nan=False), encoding='utf-8')


