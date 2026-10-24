"""Real CPU MEGU regression: jointly optimized operator, fixed final, exact HIT."""
import copy
import functools
import json

import torch
from test_modular_consumers import tables, run, write_yaml


def test_megu_trains_both_groups_and_clears_gate_gradients(tables, monkeypatch, record_property):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance
    from experiments.unlearning_outputs import load_output, restore_model
    from experiments.modular_megu import megu_logits
    from task.MEGUTrainer import GATE, MEGUTrainer
    root, _, config = tables
    config = copy.deepcopy(config)
    config.update(method='MEGU', parameters=dict(unlearning_epochs=50, kappa=0.01,
        alpha1=0.8, alpha2=0.5, GNN_layer=3, unlearn_lr=0.05, unlearn_weight_decay=0.0001))
    write_yaml(root/'megu.yaml', config)
    operators, models, optimizers, steps, clears = [], [], [], [], []
    original_init, original_train = GATE.__init__, MEGUTrainer.megu_unlearning
    original_sgd = torch.optim.SGD

    @functools.wraps(original_init)
    def gate_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        operators.append((self, [p.detach().clone() for p in self.parameters()]))

    @functools.wraps(original_train)
    def train(self, nodes, neighbors):
        assert not self.data.train_mask[nodes].any()
        assert not torch.isin(self.data.edge_index_unlearn, torch.tensor(nodes)).any()
        self.model.eval()
        with torch.no_grad():
            pseudo = self.model(self.data.x, self.data.edge_index).argmax(dim=1)
        models.append((self.model, [p.detach().clone() for p in self.model.parameters()], pseudo))
        return original_train(self, nodes, neighbors)

    class ObservedSGD(original_sgd):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            optimizers.append(self)

        def zero_grad(self, *args, **kwargs):
            result = super().zero_grad(*args, **kwargs)
            clears.append(all(p.grad is None or torch.count_nonzero(p.grad).item() == 0
                              for p in operators[-1][0].parameters()))
            return result

        def step(self, *args, **kwargs):
            before = [[p.detach().clone() for p in g['params']] for g in self.param_groups]
            result = super().step(*args, **kwargs)
            delta = [sum(float((p.detach()-v).square().sum()) for p, v in zip(g['params'], old))
                     for g, old in zip(self.param_groups, before)]
            assert all(torch.isfinite(p).all() for g in self.param_groups for p in g['params'])
            steps.append(delta)
            return result

    monkeypatch.setattr(GATE, '__init__', gate_init)
    monkeypatch.setattr(MEGUTrainer, 'megu_unlearning', train)
    monkeypatch.setattr(torch.optim, 'SGD', ObservedSGD)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['megu.yaml'])
    cold = run(tables, 'gate_cold', **options)
    warm = run(tables, 'gate_warm', **options)
    assert len(operators) == len(models) == len(optimizers) == 1
    operator, initial_operator = operators[0]
    model, initial_model, pseudo = models[0]
    optimizer = optimizers[0]
    gate_delta = sum(float((p.detach()-v).square().sum()) for p, v in zip(operator.parameters(), initial_operator))
    model_delta = sum(float((p.detach()-v).square().sum()) for p, v in zip(model.parameters(), initial_model))
    observations = dict(groups=len(optimizer.param_groups), steps=len(steps), gate_delta_squared=gate_delta,
        model_delta_squared=model_delta, gate_gradients_cleared_each_step=all(clears),
        cold_hit=cold['unlearning'][0]['hit'], warm_hit=warm['unlearning'][0]['hit'],
        lr=[g['lr'] for g in optimizer.param_groups], weight_decay=[g['weight_decay'] for g in optimizer.param_groups])
    record_property('actual_megu_optimizer', json.dumps(observations))
    # This assertion fails on the original producer after its actual native run.
    assert gate_delta > 0, 'MEGU operator never stepped: the old optimizer omitted GATE parameters'
    assert model_delta > 0
    assert len(optimizer.param_groups) == 2
    assert set(map(id, optimizer.param_groups[0]['params'])) == set(map(id, model.parameters()))
    assert set(map(id, optimizer.param_groups[1]['params'])) == set(map(id, operator.parameters()))
    ids = [id(p) for group in optimizer.param_groups for p in group['params']]
    assert len(ids) == len(set(ids))
    assert all(g['lr'] == 0.05 and g['weight_decay'] == 0.0001 for g in optimizer.param_groups)
    assert len(steps) == len(clears) == 50 and all(clears)
    assert all(len(delta) == 2 and all(value > 0 for value in delta) for delta in steps)
    assert not cold['unlearning'][0]['hit'] and warm['unlearning'][0]['hit']
    assert torch.equal(model.megu_pseudo_labels, pseudo)
    data, _ = read_dataset(load_instance(root/'dataset.yaml', 'dataset_split'), root)
    payload = load_output(cold['unlearning'][0]['output'], root/'results/cache_v2', data=data, dataset_root=root)
    restored = restore_model(payload)
    with torch.no_grad():
        published = megu_logits(restored, data, torch.tensor(payload.arrays['retain_mask']), config['parameters'])
    torch.testing.assert_close(published, torch.tensor(payload.arrays['logits']))
    assert torch.isfinite(published).all()
    assert torch.equal(restored.megu_pseudo_labels, pseudo)
