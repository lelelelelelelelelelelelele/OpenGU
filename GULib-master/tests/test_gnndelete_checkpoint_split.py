"""Counterfactual labels, real updates, checkpoint export and split validation."""
import copy

import pytest
import torch
import torch.nn.functional as F
from torch_geometric import seed_everything

from task.GNNDeleteTrainer import GNNDeleteTrainer
from experiments.modular_gu import gnndelete_node
from model.base_gnn.gcn import GCNNet
from test_gnndelete_mask_equivalence import arguments, graph, exact


class FixedLogits(torch.nn.Module):
    def __init__(self, logits):
        super().__init__()
        self.register_buffer('logits', logits)

    def forward(self, *args):
        return self.logits


@pytest.mark.parametrize('architecture', ['GCN', 'SGC', 'S2GC', 'SIGN'])
def test_stage_selects_its_own_metrics(architecture):
    data = graph()
    data.features_pre = data.x
    logits = F.one_hot(data.y, 2).float() * 4
    logits[data.test_mask] = logits[data.test_mask].flip(1)
    trainer = GNNDeleteTrainer.__new__(GNNDeleteTrainer)
    trainer.data, trainer.model = data, FixedLogits(logits)
    trainer.args, trainer.device = {'base_model': architecture}, torch.device('cpu')
    val = trainer.eval_node_fullbatch_del('val')
    test = trainer.eval_node_fullbatch_del('test')
    assert val[1:4] == (1.0, 1.0, 1.0)
    assert test[1:4] == (0.0, 0.0, 0.0)
    assert val[0] == pytest.approx(F.cross_entropy(logits[data.val_mask], data.y[data.val_mask]).item())
    assert test[0] == pytest.approx(F.cross_entropy(logits[data.test_mask], data.y[data.test_mask]).item())
    assert set(val[4]) == {'val_loss', 'val_dt_acc', 'val_dt_f1'}
    assert set(test[4]) == {'test_loss', 'test_dt_acc', 'test_dt_f1'}
    data.y[data.test_mask] = 1 - data.y[data.test_mask]
    assert trainer.eval_node_fullbatch_del('val') == val
    assert trainer.eval_node_fullbatch_del('test')[1] == 1.0
    with pytest.raises(ValueError, match='stage'):
        trainer.eval_node_fullbatch_del('train')


def train(monkeypatch, directory, *, seed=42, test_flip=False, validation_label=None,
          controlled=False, always_zero=False, epochs=3, frequency=1, invalid=None):
    """Freeze initial weights; perturb labels only after creating the model."""
    directory.mkdir(parents=True)
    data, args = graph(), arguments(seed=seed)
    seed_everything(seed)
    initial = GCNNet(args, 4, 2)
    if test_flip:
        data.y[data.test_mask] = 1 - data.y[data.test_mask]
    if validation_label is not None:
        data.y[data.val_mask] = validation_label
    if invalid == 'empty':
        data.val_mask[:] = False
    elif invalid == 'overlap':
        data.val_mask[data.test_mask] = True
    elif invalid == 'integer':
        data.val_mask = data.val_mask.long()
    args.update(checkpoint_dir=str(directory), unlearning_epochs=epochs, test_freq=frequency)
    observed = {}
    actual_train = GNNDeleteTrainer.train_node_fullbatch_del
    actual_eval = GNNDeleteTrainer.eval_node_fullbatch_del

    def capture(trainer, *a, **kw):
        observed['trainer'] = trainer
        return actual_train(trainer, *a, **kw)

    def evaluate(trainer, stage='val', pred_all=False):
        # Controlled logits make the best epoch counterfactual identifiable;
        # optimization, split evaluation, serialization and export stay real.
        count = observed.get('validation_calls', 0)
        if stage == 'val':
            observed['validation_calls'] = count + 1
        label = 0 if always_zero or count == 0 else 1
        logits = torch.zeros(data.num_nodes, 2)
        logits[:, label] = 5
        actual_forward = trainer.model.forward
        try:
            trainer.model.forward = lambda *a, **kw: logits
            return actual_eval(trainer, stage, pred_all)
        finally:
            trainer.model.forward = actual_forward

    with monkeypatch.context() as patch:
        patch.setattr(GNNDeleteTrainer, 'train_node_fullbatch_del', capture)
        if controlled:
            patch.setattr(GNNDeleteTrainer, 'eval_node_fullbatch_del', evaluate)
        model, _ = gnndelete_node(args, initial, data, [2], directory)
    best = torch.load(directory / 'model_best.pt', map_location='cpu')
    final = torch.load(directory / 'model_final.pt', map_location='cpu')
    exported = copy.deepcopy(model.state_dict())
    exact(exported, best['model_state'])
    return observed['trainer'], best, final, exported


@pytest.mark.parametrize('seed', [42, 212, 2024])
def test_real_training_and_export_are_invariant_to_test_labels(monkeypatch, tmp_path, seed):
    left = train(monkeypatch, tmp_path / 'left', seed=seed)
    right = train(monkeypatch, tmp_path / 'right', seed=seed, test_flip=True)
    exact(left[1], right[1])
    exact(left[2], right[2])
    exact(left[3], right[3])
    left_val = [x for x in left[0].trainer_log['log'] if 'val_loss' in x]
    right_val = [x for x in right[0].trainer_log['log'] if 'val_loss' in x]
    exact(left_val, right_val)
    assert len(left_val) == 3
    assert left[1]['selection_stage'] == 'val'
    assert left[1]['selection_metric'] == 'accuracy+micro_f1'


def test_validation_changes_selected_epoch_test_does_not_and_best_is_exported(monkeypatch, tmp_path):
    first = train(monkeypatch, tmp_path / 'first', controlled=True, validation_label=0)
    second = train(monkeypatch, tmp_path / 'second', controlled=True, validation_label=1)
    test_changed = train(monkeypatch, tmp_path / 'test_changed', controlled=True, validation_label=0, test_flip=True)
    assert first[1]['epoch'] == 0
    assert second[1]['epoch'] == 1  # Equal epoch-2 score keeps the earlier checkpoint.
    assert first[1]['selection_score'] == second[1]['selection_score'] == 2.0
    exact(first[1], test_changed[1])
    exact(first[3], test_changed[3])
    assert any(not torch.equal(first[3][k], second[3][k]) for k in first[3])
    assert any(not torch.equal(first[3][k], first[2]['model_state'][k]) for k in first[3])
    trainer = first[0]
    trainer.test_node_fullbatch_del(ckpt='final')
    exact(trainer.model.state_dict(), first[2]['model_state'])
    trainer.test_node_fullbatch_del(ckpt='best')
    exact(trainer.model.state_dict(), first[1]['model_state'])
    with pytest.raises(ValueError, match='checkpoint'):
        trainer.test_node_fullbatch_del(ckpt='unknown')


def test_all_zero_validation_saves_first_and_frequency_beyond_epochs_evaluates_final(monkeypatch, tmp_path):
    zero = train(monkeypatch, tmp_path / 'zero', controlled=True, always_zero=True, validation_label=1)
    assert zero[1]['epoch'] == 0 and zero[1]['selection_score'] == 0.0
    assert zero[0].trainer_log['best_epoch'] == 0
    sparse = train(monkeypatch, tmp_path / 'sparse', epochs=1, frequency=2)
    assert sparse[1]['epoch'] == 0


@pytest.mark.parametrize('invalid', ['empty', 'overlap', 'integer'])
def test_invalid_validation_fails_before_optimizer_or_checkpoint(monkeypatch, tmp_path, invalid):
    def forbidden(*args, **kwargs):
        raise AssertionError('invalid split reached optimizer')
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    with pytest.raises(ValueError, match='mask'):
        train(monkeypatch, tmp_path / invalid, invalid=invalid)
    assert not list(tmp_path.rglob('model_*.pt'))


@pytest.mark.parametrize('epochs,frequency', [(0, 1), (3, 0), (-1, 1)])
def test_invalid_training_schedule_is_rejected(monkeypatch, tmp_path, epochs, frequency):
    with pytest.raises(ValueError, match='positive'):
        train(monkeypatch, tmp_path / 'bad', epochs=epochs, frequency=frequency)
    assert not list(tmp_path.rglob('model_*.pt'))
