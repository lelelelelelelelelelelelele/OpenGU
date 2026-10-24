"""Run-owned Ret endpoints and an explicit off/off/on/on reproducibility probe."""
import copy
import hashlib
import json
import random

import numpy as np
import torch

from experiments.effective_config import fields
from experiments.observers.retrain_validation import (
    classification, evaluation_observation, validate_masks, window_summary)
from utils.target_checkpoint import capture_state, state_hash, save_weights, sha256_file

AUDIT_EPOCHS = (1, 2, 10, 100, 1000, 3000)


def rng_identity(model):
    def digest(value):
        return hashlib.sha256(value).hexdigest()
    devices = sorted({p.device.index for p in model.parameters() if p.is_cuda})
    numpy_state = np.random.get_state()
    numpy_bytes = numpy_state[1].tobytes() + repr((numpy_state[0], *numpy_state[2:])).encode()
    return dict(cpu=digest(torch.get_rng_state().numpy().tobytes()),
        cuda={str(d): digest(torch.cuda.get_rng_state(d).cpu().numpy().tobytes()) for d in devices},
        python=digest(repr(random.getstate()).encode()),
        numpy=digest(numpy_bytes))


def prediction_difference(left, right, mask):
    changes = left.argmax(1) != right.argmax(1)
    return dict(all_node_prediction_changes=int(changes.sum()),
        test_prediction_changes=int(changes[mask].sum()),
        maximum_absolute_logit_error=float((left-right).abs().max()))


class RetReferenceTrace:
    version = 'ret-reference-trace-v1'
    files = ('result.json', 'trace.jsonl')
    requires = {
        'reference_start': {'model', 'validation', 'identity', 'repeat', 'observe'},
        'epoch_end': {'model', 'data', 'train_loss', 'update_lr'},
        'training_complete': {'model', 'original', 'validation', 'prior', 'asset_root', 'dataset_root'},
    }

    def __init__(self, parameters):
        fields(parameters, set(), (), 'ret_reference_trace')
        self.parameters = {}
        self.rows, self.replays, self.test_logits = [], [], []
        self.active = None
        self.result = None

    def __call__(self, event):
        v = event['values']
        if event['phase'] == 'reference_start':
            if self.active is not None:
                raise ValueError('Ret reference overlap')
            validate_masks(v['validation'])
            if v['repeat'] not in ('reference', 'off1', 'off2', 'on1', 'on2'):
                raise ValueError('unknown Ret repetition')
            self.active = dict(repeat=v['repeat'], observe=v['observe'], identity=v['identity'],
                initial_state_hash=state_hash(v['model'].state_dict()),
                initial_rng=rng_identity(v['model']), rows=[], best=None, best_state=None,
                validation=v['validation'], snapshots=[])
            return
        if self.active is None:
            raise ValueError('Ret reference event before start')
        if event['phase'] == 'training_complete':
            self.complete(v)
            return
        epoch, model, a = event['step'], v['model'], self.active
        if epoch != len(a['rows'])+1 or epoch > 3000:
            raise ValueError('Ret reference epoch order mismatch')
        row = dict(repeat=a['repeat'], epoch=epoch, train_loss=float(v['train_loss']),
                   update_lr=float(v['update_lr']))
        if a['observe']:
            data = a['validation']
            with evaluation_observation(model):
                measured = classification(model(data.x, data.edge_index), data.y, data.val_mask)
            row.update(validation_accuracy=measured['accuracy'], validation_cross_entropy=measured['cross_entropy'])
            if a['best'] is None or measured['accuracy'] > a['best']['accuracy']:
                a['best'], a['best_state'] = dict(epoch=epoch, **measured), capture_state(model)
        if epoch in AUDIT_EPOCHS:
            a['snapshots'].append(dict(epoch=epoch, state_hash=state_hash(model.state_dict()), rng=rng_identity(model)))
        a['rows'].append(row)
        self.rows.append(row)

    def complete(self, v):
        model = v['model']
        state, rng = state_hash(model.state_dict()), rng_identity(model)
        with evaluation_observation(model):
            self._complete(v)
        if state_hash(model.state_dict()) != state or rng_identity(model) != rng:
            raise ValueError('Ret endpoint observation changed final state/RNG')

    def _complete(self, v):
        a = self.active
        if len(a['rows']) != 3000:
            raise ValueError('Ret reference requires exactly 3000 epochs')
        original, retained, final_model = v['original'], v['validation'], v['model']
        final_state = capture_state(final_model)
        final_rng = rng_identity(final_model)
        assets = v['asset_root']/a['repeat']
        assets.mkdir(parents=True, exist_ok=False)
        model = copy.deepcopy(final_model)
        endpoints, final_logits = {}, None
        selected = [('final', final_state, 3000)]
        if a['observe']:
            selected.append(('best', a['best_state'], a['best']['epoch']))
        for role, state, epoch in selected:
            model.load_state_dict(state, strict=True)
            exported = save_weights(assets/(role+'.pt'), state)
            predictions = {}
            for graph_name, graph in (('original', original), ('retained', retained)):
                with evaluation_observation(model):
                    logits = model(graph.x, graph.edge_index)
                    measured = classification(logits, original.y, original.test_mask)
                path = assets/(role+'-'+graph_name+'.npz')
                with path.open('xb') as handle:
                    np.savez_compressed(handle, logits=logits.detach().cpu().numpy())
                predictions[graph_name] = dict(test=measured, path=path.relative_to(v['dataset_root']).as_posix(),
                                              sha256=sha256_file(path))
                if role == 'final' and graph_name == 'original':
                    final_logits = logits.detach().cpu().clone()
            endpoints[role] = dict(epoch=epoch, checkpoint_role=role, state_hash=exported['state_hash'],
                weights=dict(path=(assets/(role+'.pt')).relative_to(v['dataset_root']).as_posix(),
                             sha256=exported['file_sha256']), probes=predictions)
        prior = None
        if v['prior'] is not None:
            old = torch.as_tensor(np.array(v['prior']['logits'], copy=True))
            if old.shape != final_logits.shape or not torch.isfinite(old).all():
                raise ValueError('Ret prior logits invalid')
            prior = dict(reference=v['prior']['reference'], state_hash_equal=state_hash(final_state)==v['prior']['state_hash'],
                **prediction_difference(old, final_logits, original.test_mask.cpu()))
        replay = {k:a[k] for k in ('repeat', 'observe', 'identity', 'initial_state_hash', 'initial_rng', 'snapshots')}
        replay.update(endpoints=endpoints, final_rng=final_rng, prior_comparison=prior,
            validation_best=a['best'], windows=window_summary(a['rows'], a['best']) if a['observe'] else None)
        self.replays.append(replay)
        self.test_logits.append(final_logits)
        self.active = None
        self.result = dict(replays=self.replays, validation_graph='retained(S)',
            validation_mask='original_val_mask', selection_rule='maximum_validation_accuracy_earliest_tie',
            primary_endpoint='final3000', auxiliary_endpoint='validation_best',
            primary_probe='original', secondary_probe='retained(S)',
            probe_scope='fixed test endpoints; not deployment compliance certification',
            repetitions_are_independent_samples=False)
        repeats = [r['repeat'] for r in self.replays]
        if repeats == ['off1','off2','on1','on2']:
            first = self.replays[0]
            self.result['probe_comparisons'] = [dict(repeat=r['repeat'],
                initial_state_equal=r['initial_state_hash']==first['initial_state_hash'],
                initial_rng_equal=r['initial_rng']==first['initial_rng'],
                final_state_equal=r['endpoints']['final']['state_hash']==first['endpoints']['final']['state_hash'],
                final_rng_equal=r['final_rng']==first['final_rng'],
                **prediction_difference(self.test_logits[0], self.test_logits[i], original.test_mask.cpu()))
                for i,r in enumerate(self.replays[1:],1)]

    def save(self, folder, metadata):
        repeats = [r['repeat'] for r in self.replays]
        if metadata['status'] == 'completed' and (self.active is not None or repeats not in (
                ['reference'], ['off1','off2','on1','on2'])):
            raise ValueError('Ret reference incomplete repetition sequence')
        (folder/'result.json').write_text(json.dumps({**metadata,'diagnostics':self.result},indent=2,allow_nan=False),encoding='utf-8')
        (folder/'trace.jsonl').write_text(''.join(json.dumps(r,allow_nan=False)+'\n' for r in self.rows),encoding='utf-8')
