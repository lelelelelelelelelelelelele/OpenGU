"""Explicit saved Ret endpoints on the original graph; no model work or fake Output."""
import hashlib
import json
from pathlib import Path
import re

import numpy as np

from cache_v2 import canonical_sha256
from experiments.effective_config import ConfigurationError, fields
from experiments.response_diagnostics import prediction_triangle, prediction_by_label, request_composition
from experiments.ret_reference_policy import ARMS, DETERMINISTIC, OBSERVED

CASE = 'post_unlearning_ret_endpoint_sensitivity'
ENDPOINTS = ('final', 'best')
TRIANGLE_KEYS = tuple(prediction_triangle(np.zeros((0, 2)), np.zeros((0, 2)),
                                        np.zeros((0, 2)), np.array([], dtype=np.int64)))
METRICS = tuple(role + '_' + key for role in ENDPOINTS for key in TRIANGLE_KEYS)


def validate_inputs(values):
    required = {'run', 'sha256', 'cell_id', 'repeat', 'policy', 'arm', 'endpoints'}
    if not isinstance(values, list) or not values:
        raise ConfigurationError('Ret endpoint inputs must be a nonempty list')
    seen = set()
    for value in values:
        fields(value, required, required, 'Ret endpoint input')
        if (any(not isinstance(value[k], str) or not value[k] for k in required - {'endpoints'})
                or not re.fullmatch('[0-9a-f]{64}', value['sha256'])
                or value['repeat'] not in ('reference', 'on1', 'on2')
                or value['policy'] not in (DETERMINISTIC, OBSERVED) or value['arm'] not in ARMS
                or value['endpoints'] != list(ENDPOINTS)):
            raise ConfigurationError('Ret endpoint input requires exact run/cell, observed repeat, policy/arm and final+best')
        key = (value['run'], value['sha256'], value['cell_id'], value['repeat'])
        if key in seen:
            raise ConfigurationError('duplicate Ret endpoint input')
        seen.add(key)
    return values


def request_key(cell, selection):
    c = cell['conditions']
    return (cell['selection_id'], tuple(selection['selected_nodes']), c['seed'], c['model'],
            c['dataset_name'], c['dataset_fingerprint'])


def endpoint_sources(config):
    """Plan from checksum-bound light documents; do not load remote heavy assets."""
    from experiments.modular_artifacts import read_run
    result = []
    runs = {}
    for spec in validate_inputs(config['ret_endpoint_inputs']):
        path = Path(config['source_directory']) / spec['run']
        run_key = (path.resolve(), spec['sha256'])
        if run_key not in runs:
            runs[run_key] = read_run(path, spec['sha256'])
        run, documents = runs[run_key]
        matched = [(c, d) for c, d in zip(run['cells'], documents) if c['cell_id'] == spec['cell_id']]
        if len(matched) != 1 or matched[0][0]['conditions']['method'] != 'Retrain':
            raise ConfigurationError('Ret endpoint must identify exactly one Ret cell')
        cell, document = matched[0]
        saved = json.loads(document['observers/ret_reference_trace/result.json'])
        replays = [r for r in saved['diagnostics']['replays'] if r['repeat'] == spec['repeat']]
        if (len(replays) != 1 or any(replays[0]['identity'][k] != spec[k] for k in ('policy', 'arm'))
                or set(replays[0]['endpoints']) != set(ENDPOINTS)):
            raise ConfigurationError('Ret endpoint repeat/policy/arm mismatch or missing final/best')
        result.append(dict(input=spec, path=path, cell=cell, document=document, saved=saved,
                           replay=replays[0], key=request_key(cell, document['selection.json'])))
    return result


def planned_pairs(config):
    from experiments.modular_artifacts import read_run, metric_source_cells
    endpoints = endpoint_sources(config)
    used, pairs = set(), {}
    for source in config['output_inputs']:
        run, documents = read_run(Path(config['source_directory']) / source['run'], source['sha256'])
        for cell, document in metric_source_cells(run, source, documents):
            if cell['conditions']['method'] not in ('GIF', 'MEGU', 'GNNDelete'):
                raise ConfigurationError('Ret endpoint Metrics requires explicit GU Outputs only')
            matches = [i for i, endpoint in enumerate(endpoints)
                       if endpoint['key'] == request_key(cell, document['selection.json'])]
            if len(matches) != 1:
                raise ConfigurationError('each GU request requires exactly one explicit Ret endpoint input; duplicate arms are ambiguous')
            if cell['cell_id'] in pairs:
                raise ConfigurationError('duplicate GU cell in Ret endpoint inputs')
            index = matches[0]
            used.add(index)
            pairs[cell['cell_id']] = endpoints[index]
    if used != set(range(len(endpoints))):
        raise ConfigurationError('unused Ret endpoint inputs')
    return pairs


def validate_pair(gu, endpoint, loaded):
    """Compare shared request fields; intervention training graphs remain explicit."""
    import torch
    from torch_geometric.data import Data
    from experiments.ret_reference_policy import training_graph
    from utils.target_checkpoint import data_identity
    ret = loaded['output']
    left, right = gu.identity, ret.identity
    if any(left[k] != right[k] for k in ('selection', 'dataset_input', 'graph_fingerprint')):
        raise ConfigurationError('Ret endpoint Selection/Dataset/Split identity differs from GU')
    lp, rp = left['pairing'], right['pairing']
    for key in ('data_identity', 'selected_nodes', 'model', 'deletion', 'evaluation_graph_identity'):
        if lp[key] != rp[key]:
            raise ConfigurationError('Ret endpoint request identity differs: ' + key)
    if lp['deletion']['evaluation_graph'] != 'original':
        raise ConfigurationError('saved endpoint Metrics requires original graph predictions')
    omitted = ('epochs', 'optimizer', 'lr', 'weight_decay', 'scheduler')
    external = bool(left['target'].get('checkpoint_state_hash')) and all(lp['training'].get(k) is None for k in omitted)
    lt = {k: v for k, v in lp['training'].items() if not (external and k in omitted)}
    rt = {k: v for k, v in rp['training'].items() if not (external and k in omitted)}
    if lt != rt:
        raise ConfigurationError('Ret endpoint training/seed differs from GU')
    a, b = gu.arrays, ret.arrays
    for key in ('selected_nodes', 'y', 'train_mask', 'test_mask', 'edge_index', 'evaluation_edge_index'):
        if not np.array_equal(a[key], b[key]):
            raise ConfigurationError('Ret endpoint bound arrays differ: ' + key)
    # The light GU view binds features/validation mask by data_identity; the
    # resolved Ret view carries those same verified arrays for graph checking.
    data = Data(**{k: torch.tensor(b[k]) for k in ('x', 'y', 'edge_index', 'train_mask', 'val_mask', 'test_mask')})
    trained, validation = training_graph(data, a['selected_nodes'], endpoint['input']['arm'])
    execution = endpoint['replay']['identity']
    if (execution['training_graph_identity'] != data_identity(trained)
            or execution['validation_graph_identity'] != data_identity(validation)
            or execution['training'] != rp['training']):
        raise ConfigurationError('Ret endpoint intervention graph/training identity differs')
    if 'logits_before' not in a or a['logits_before'].shape != a['logits'].shape:
        raise ConfigurationError('Ret endpoint Metrics requires persisted Original predictions')


def evaluate(instance, rows, *, config, store_root, dataset_root):
    from experiments.ret_reference_reading import load_endpoints
    from experiments.unlearning_outputs import load_metric_output
    from experiments.implementation_identity import implementation_fingerprint
    pairs = planned_pairs(config)
    loaded_by_spec, results = {}, []
    for row in rows:
        conditions = row['conditions']
        endpoint = pairs[row['cell_id']]
        key = canonical_sha256(endpoint['input'])
        if key not in loaded_by_spec:
            loaded_by_spec[key] = load_endpoints(endpoint['path'], endpoint['input']['sha256'],
                endpoint['input']['cell_id'], dataset_root=dataset_root, store_root=store_root)
        loaded = loaded_by_spec[key]
        gu = load_metric_output(row['output'], store_root, dataset_root=dataset_root)
        validate_pair(gu, endpoint, loaded)
        a = gu.arrays
        mask = a['test_mask'].copy()
        mask[a['selected_nodes']] = False
        composition = request_composition(a, mask)
        request_labels = dict(labels_hash=gu.identity['pairing']['data_identity']['labels_hash'],
            ordered_nodes_hash=canonical_sha256(a['selected_nodes'].tolist()), k=len(a['selected_nodes']),
            selected_label_sequence_sha256=canonical_sha256(a['y'][a['selected_nodes']].tolist()),
            deleted_class_counts=composition['deleted_class_counts'],
            retained_class_counts=composition['retained_class_counts'],
            count_basis='original_train_mask_not_reference_arm_supervision')
        metrics, by_label = {}, {}
        for role in ENDPOINTS:
            logits = loaded['endpoints'][endpoint['input']['repeat']][role]['logits']['original']
            arrays = (a['logits_before'][mask], a['logits'][mask], logits[mask], a['y'][mask])
            metrics.update({role + '_' + k: v for k, v in prediction_triangle(*arrays).items()})
            by_label[role] = prediction_by_label(*arrays)
        identity = dict(case=CASE, metrics=sorted(instance['metrics']), producer_version=instance['producer_version'],
            implementation=implementation_fingerprint(evaluate, validate_pair, planned_pairs, endpoint_sources,
                load_endpoints, prediction_triangle, prediction_by_label, request_composition), unlearning_output=row['output'],
            ret_endpoints=dict(input=endpoint['input'], observer=next(r for r in endpoint['cell']['observers'] if r['name']=='ret_reference_trace'),
                source_output=endpoint['cell'].get('output', endpoint['cell'].get('source', {}).get('output')),
                execution=endpoint['replay']['identity'], endpoints=endpoint['replay']['endpoints']),
            protocol=dict(version='saved-original-ret-endpoints-v1', prediction_graph='original', forward_calls=0,
                original_prediction='persisted_raw_pre_update_logits',
                gu_prediction='MEGU_updated_C&S' if gu.identity['target']['method']=='MEGU' else 'persisted_updated_logits',
                original_checkpoint_state_hash=gu.identity['target'].get('checkpoint_state_hash'),
                evaluation_mask='test_mask_excluding_selected_nodes',
                evaluation_mask_sha256=hashlib.sha256(np.asarray(mask, dtype=np.uint8).tobytes()).hexdigest(),
                correctness_order=['Original', 'GU', 'Retrain'], class_order='zero_based_label_id', by_label=by_label, request_labels=request_labels))
        results.append(dict(evaluation_receipt_id='evalr_'+canonical_sha256(identity)[:32], identity=identity,
            metrics={k: metrics[k] for k in instance['metrics']}, cache=None, execution_conditions=conditions))
    return dict(effective_config=instance, rows=results, not_applicable=[])
