"""Passive validation of one fixed 3000-epoch retained-graph training run."""
from contextlib import contextmanager
import copy
import json
import math
import random

import numpy as np
import torch
import torch.nn.functional as F

from experiments.effective_config import fields
from utils.target_checkpoint import capture_state, state_hash, save_weights, sha256_file


@contextmanager
def evaluation_observation(model):
    """Evaluation cannot consume the next training dropout draw or change modes."""
    modes = [(module, module.training) for module in model.modules()]
    python_rng, numpy_rng = random.getstate(), np.random.get_state()
    devices = sorted({p.device.index for p in model.parameters() if p.is_cuda})
    try:
        with torch.random.fork_rng(devices=devices), torch.no_grad():
            model.eval()
            yield
    finally:
        for module, mode in modes:
            module.training = mode
        random.setstate(python_rng)
        np.random.set_state(numpy_rng)


def validate_masks(data):
    masks = [getattr(data, name + '_mask') for name in ('train', 'val', 'test')]
    if any(m.dtype != torch.bool or m.ndim != 1 or m.numel() != data.num_nodes or not m.any() for m in masks):
        raise ValueError('Ret diagnostics require nonempty boolean train/val/test masks')
    if any(bool((masks[i] & masks[j]).any()) for i, j in ((0, 1), (0, 2), (1, 2))):
        raise ValueError('Ret diagnostics require disjoint train/val/test masks')


def classification(logits, labels, mask):
    values, truth = logits[mask], labels[mask]
    if not torch.isfinite(values).all():
        raise ValueError('nonfinite Ret diagnostic logits')
    return {'accuracy': float((values.argmax(1) == truth).double().mean()),
            'cross_entropy': float(F.cross_entropy(values, truth))}


def window_summary(rows, best):
    if [r['epoch'] for r in rows] != list(range(1, 3001)):
        raise ValueError('Ret validation trace must cover exactly epochs 1..3000')
    for row in rows:
        if any(not math.isfinite(row[k]) for k in ('train_loss', 'validation_cross_entropy', 'validation_accuracy', 'update_lr')):
            raise ValueError('nonfinite Ret validation trace')
    before = sum(r['validation_cross_entropy'] for r in rows[2000:2500]) / 500
    after = sum(r['validation_cross_entropy'] for r in rows[2500:3000]) / 500
    increase = (after - before) / before if before else None
    ce_trigger = after > 0 if before == 0 else after >= before * 1.10
    accuracy_gap = best['accuracy'] - rows[-1]['validation_accuracy']
    return {'validation_accuracy_gap': accuracy_gap,
            'ce_2001_2500': before, 'ce_2501_3000': after,
            'ce_relative_increase': increase,
            'ce_relative_increase_status': 'finite' if before else 'zero_to_positive' if after else 'both_zero',
            'accuracy_trigger': accuracy_gap >= 0.01, 'ce_trigger': ce_trigger,
            'optimization_sensitive': accuracy_gap >= 0.01 or ce_trigger}


class RetrainValidationTrace:
    version = 'retrain-validation-trace-v1'
    requires = {
        'epoch_end': {'model', 'data', 'train_loss', 'update_lr'},
        'training_complete': {'model', 'original', 'old_logits', 'old_state_hash', 'asset_root', 'dataset_root'},
    }
    files = ('result.json', 'trace.jsonl')

    def __init__(self, parameters):
        fields(parameters, set(), (), 'retrain_validation_trace')
        self.parameters = {}
        self.rows, self.best_state, self.best, self.result = [], None, None, None

    def __call__(self, event):
        values = event['values']
        if event['phase'] == 'training_complete':
            self.complete(values)
            return
        epoch, model, data = event['step'], values['model'], values['data']
        if epoch != len(self.rows) + 1 or epoch > 3000:
            raise ValueError('Ret validation epoch order/coverage mismatch')
        if not self.rows:
            validate_masks(data)
        with evaluation_observation(model):
            measured = classification(model(data.x, data.edge_index), data.y, data.val_mask)
        row = dict(epoch=epoch, train_loss=float(values['train_loss']), update_lr=float(values['update_lr']),
                   validation_accuracy=measured['accuracy'], validation_cross_entropy=measured['cross_entropy'])
        if any(not math.isfinite(v) for v in row.values()):
            raise ValueError('nonfinite Ret validation observation')
        self.rows.append(row)
        if self.best is None or measured['accuracy'] > self.best['accuracy']:
            self.best = dict(epoch=epoch, **measured)
            self.best_state = capture_state(model)

    def complete(self, values):
        summary = window_summary(self.rows, self.best)
        original, final_model = values['original'], values['model']
        validate_masks(original)
        final_state = capture_state(final_model)
        assets = values['asset_root']
        assets.mkdir(parents=True, exist_ok=False)
        endpoints = {}
        model = copy.deepcopy(final_model)
        for role, state, epoch in (('best', self.best_state, self.best['epoch']), ('final', final_state, 3000)):
            model.load_state_dict(state, strict=True)
            with evaluation_observation(model):
                logits = model(original.x, original.edge_index)
                measured = classification(logits, original.y, original.test_mask)
            exported = save_weights(assets / (role + '.pt'), state)
            predictions = assets / (role + '.npz')
            with predictions.open('xb') as handle:
                np.savez_compressed(handle, logits=logits.detach().cpu().numpy())
            endpoints[role] = {'checkpoint_role': role, 'epoch': epoch,
                'state_hash': exported['state_hash'], 'test': measured,
                'weights': {'path': str((assets / (role + '.pt')).relative_to(values['dataset_root']).as_posix()),
                            'sha256': exported['file_sha256']},
                'predictions': {'path': str(predictions.relative_to(values['dataset_root']).as_posix()),
                                'sha256': sha256_file(predictions)}}
            if role == 'final':
                old = torch.tensor(values['old_logits'], device=logits.device, dtype=logits.dtype)
                if old.shape != logits.shape or not torch.isfinite(old).all():
                    raise ValueError('old Ret predictions invalid')
                mismatch = logits.argmax(1) != old.argmax(1)
                comparison = {'state_hash_equal': exported['state_hash'] == values['old_state_hash'],
                    'all_node_prediction_changes': int(mismatch.sum()),
                    'test_prediction_changes': int(mismatch[original.test_mask].sum()),
                    'maximum_absolute_logit_error': float((logits - old).abs().max()),
                    'old_test': classification(old, original.y, original.test_mask)}
        if state_hash(final_model.state_dict()) != state_hash(final_state):
            raise ValueError('endpoint evaluation changed final training state')
        self.result = {'epochs': 3000, 'best': {**endpoints['best'], 'validation': self.best},
            'final': {**endpoints['final'], 'validation': {
                'accuracy': self.rows[-1]['validation_accuracy'],
                'cross_entropy': self.rows[-1]['validation_cross_entropy']}},
            'windows': summary, 'old_final_comparison': comparison,
            'validation_graph': 'retained', 'validation_mask': 'original_split_val_mask',
            'selection_rule': 'maximum_validation_accuracy_earliest_tie',
            'test_graph': 'original', 'test_policy': 'fixed_best_and_final_only',
            'train_loss_semantics': 'pre_update_train_mode_cross_entropy',
            'validation_semantics': 'post_update_eval_mode_cross_entropy_and_accuracy'}

    def save(self, folder, metadata):
        if metadata['status'] == 'completed' and self.result is None:
            raise ValueError('Ret diagnostics have no completed fixed endpoints')
        (folder / 'trace.jsonl').write_text(''.join(json.dumps(row, allow_nan=False) + '\n' for row in self.rows), encoding='utf-8')
        (folder / 'result.json').write_text(json.dumps({**metadata, 'diagnostics': self.result}, indent=2, allow_nan=False), encoding='utf-8')
