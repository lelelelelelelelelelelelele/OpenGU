"""Same-request Original/GU/Retrain response diagnostics on persisted predictions.

This module never trains or forwards a model. Request composition describes the
bound original graph; it is not a causal adjustment or a forgetting certificate.
"""
from __future__ import annotations

import hashlib
import itertools
import numpy as np

from experiments.effective_config import ConfigurationError
from experiments.flip_hop_metrics import exact_retrain, hop_groups
from experiments.implementation_identity import implementation_fingerprint


RELATIONS = ('all_equal', 'original_gu_equal', 'original_retrain_equal',
             'gu_retrain_equal', 'all_different')
CORRECTNESS = tuple(''.join(bits) for bits in itertools.product('01', repeat=3))
METRICS = ('node_count', 'original_accuracy', 'gu_accuracy', 'retrain_accuracy',
           'original_cross_entropy', 'gu_cross_entropy', 'retrain_cross_entropy',
           'original_gu_disagreement_count', 'original_retrain_disagreement_count',
           'gu_retrain_disagreement_count', 'original_gu_disagreement',
           'original_retrain_disagreement', 'gu_retrain_disagreement',
           'selected_node_count', 'original_train_count', 'retained_train_count',
           'original_edge_column_count', 'removed_edge_column_count',
           'original_unique_undirected_edge_count', 'removed_unique_undirected_edge_count',
           'test_1_hop_count', 'test_2_hop_count', 'test_3_hop_count', 'test_gt3_hop_count') + tuple(
               relation + '_count' for relation in RELATIONS) + tuple(
               relation + '_correct_' + bits + '_count'
               for relation in RELATIONS for bits in CORRECTNESS)


def cross_entropy(logits, labels):
    values = np.asarray(logits, dtype=np.float64)
    if not len(labels):
        return None
    shifted = values - values.max(axis=1, keepdims=True)
    return float(np.mean(np.log(np.exp(shifted).sum(axis=1)) - shifted[np.arange(len(labels)), labels]))


def prediction_triangle(original, gu, retrain, labels):
    """Five disjoint prediction relations crossed with O/G/R truth bits."""
    logits = [np.asarray(a) for a in (original, gu, retrain)]
    y = np.asarray(labels)
    if (any(a.ndim != 2 or a.shape != logits[0].shape or not np.isfinite(a).all() for a in logits)
            or logits[0].shape[0] != len(y) or logits[0].shape[1] < 2
            or y.ndim != 1 or not np.issubdtype(y.dtype, np.integer)
            or (y < 0).any() or (y >= logits[0].shape[1]).any()):
        raise ConfigurationError('response predictions/labels have invalid shape, values or classes')
    o,g,r = [a.argmax(axis=1) for a in logits]
    n = len(y)
    og,orr,gr = o==g,o==r,g==r
    relation_masks = (og&orr, og&~orr, orr&~og, gr&~og, ~og&~orr&~gr)
    correct = (o==y,g==y,r==y)
    result = {'node_count': n}
    for name,a,p in zip(('original','gu','retrain'),logits,correct):
        result[name+'_accuracy'] = float(p.mean()) if n else None
        result[name+'_cross_entropy'] = cross_entropy(a,y)
    for name,same in zip(('original_gu','original_retrain','gu_retrain'),(og,orr,gr)):
        count = int((~same).sum())
        result[name+'_disagreement_count'] = count
        result[name+'_disagreement'] = count/n if n else None
    for name,mask in zip(RELATIONS,relation_masks):
        result[name+'_count'] = int(mask.sum())
        for bits in CORRECTNESS:
            joint = mask.copy()
            for truth,bit in zip(correct,bits):
                joint &= truth if bit=='1' else ~truth
            result[name+'_correct_'+bits+'_count'] = int(joint.sum())
    if sum(result[name+'_count'] for name in RELATIONS) != n:
        raise ConfigurationError('response classes do not partition evaluation nodes')
    return result


def prediction_by_label(original, gu, retrain, labels):
    """Complete per-label triangles; empty classes retain zero counts/null rates."""
    arrays = [np.asarray(a) for a in (original, gu, retrain)]
    y = np.asarray(labels)
    total = prediction_triangle(*arrays, y)
    rows = [dict(class_id=c, **prediction_triangle(*(a[y == c] for a in arrays), y[y == c]))
            for c in range(arrays[0].shape[1])]
    for key, value in total.items():
        if key.endswith('_count') and sum(row[key] for row in rows) != value:
            raise ConfigurationError('per-label response counts do not recover global counts')
        if key.endswith(('_accuracy', '_cross_entropy', '_disagreement')) and total['node_count']:
            weighted = sum(row[key] * row['node_count'] for row in rows if row['node_count']) / total['node_count']
            if not np.isclose(weighted, value, rtol=1e-12, atol=1e-12):
                raise ConfigurationError('per-label response rates do not recover global values')
    return rows


def request_composition(arrays, mask):
    y = np.asarray(arrays['y'])
    train = np.asarray(arrays['train_mask'], dtype=bool)
    selected = np.asarray(arrays['selected_nodes'], dtype=np.int64)
    edges = np.asarray(arrays['edge_index'], dtype=np.int64)
    if (train.shape != y.shape or len(set(selected.tolist())) != len(selected)
            or not len(selected) or (selected<0).any() or (selected>=len(y)).any()
            or not train[selected].all()):
        raise ConfigurationError('response request must contain unique bound training nodes')
    removed = np.zeros(len(y),dtype=bool)
    removed[selected]=True
    incident = removed[edges[0]] | removed[edges[1]]
    # Canonical unordered pairs count reciprocal/duplicate storage only once.
    unique = np.unique(np.sort(edges,axis=0).T,axis=0)
    unique_incident = removed[unique[:,0]] | removed[unique[:,1]]
    classes = int(y.max())+1
    retained = train & ~removed
    if not retained.any():
        raise ConfigurationError('response request leaves no retained supervision')
    distance = hop_groups(edges, selected, len(y))
    result = dict(selected_node_count=len(selected),original_train_count=int(train.sum()),
        retained_train_count=int(retained.sum()),original_edge_column_count=edges.shape[1],
        removed_edge_column_count=int(incident.sum()),
        original_unique_undirected_edge_count=len(unique),
        removed_unique_undirected_edge_count=int(unique_incident.sum()),
        deleted_class_counts=np.bincount(y[selected],minlength=classes).tolist(),
        retained_class_counts=np.bincount(y[retained],minlength=classes).tolist())
    for hop,name in ((1,'1'),(2,'2'),(3,'3'),(4,'gt3')):
        result['test_'+name+'_hop_count'] = int((mask & (distance==hop)).sum())
    return result


def response_diagnostics(output, retrain):
    exact_retrain(output, [(None,retrain)])
    a,b = output.arrays,retrain.arrays
    if 'logits_before' not in a:
        raise ConfigurationError('response diagnostics requires persisted Original predictions; no training fallback')
    if ('train_mask' not in a or 'train_mask' not in b
            or not np.array_equal(a['train_mask'],b['train_mask'])):
        raise ConfigurationError('response inputs require the same original training mask')
    if np.asarray(a['logits_before']).shape != np.asarray(a['logits']).shape:
        raise ConfigurationError('response Original predictions have incompatible shape')
    mask = a['test_mask'].copy()
    mask[a['selected_nodes']]=False
    metrics = prediction_triangle(a['logits_before'][mask],a['logits'][mask],b['logits'][mask],a['y'][mask])
    composition = request_composition(a,mask)
    class_counts = {key: composition.pop(key) for key in ('deleted_class_counts','retained_class_counts')}
    metrics.update(composition)
    protocol = dict(version='same-request-response-diagnostics-v1',
        comparison='argmax_first_index_ties',correctness_order=['Original','GU','Retrain'],
        original_prediction='persisted_raw_pre_update_logits',
        gu_prediction='MEGU_updated_C&S' if output.identity['target']['method']=='MEGU' else 'persisted_updated_logits',
        original_checkpoint_state_hash=output.identity['target'].get('checkpoint_state_hash'),
        evaluation_mask='test_mask_excluding_selected_nodes',
        evaluation_mask_sha256=hashlib.sha256(np.asarray(mask,dtype=np.uint8).tobytes()).hexdigest(),
        prediction_graph=output.identity['pairing']['evaluation_graph_identity'],
        request_graph='bound_pre_deletion_edge_index',
        unique_edge_definition='unordered_endpoint_pairs_including_self_loops',
        class_count_order='zero_based_label_id',class_supervision_counts=class_counts,
        graph_fingerprint=output.identity['graph_fingerprint'],
        dataset_input=output.identity['dataset_input'],numpy_version=np.__version__,
        implementation=implementation_fingerprint(response_diagnostics,prediction_triangle,cross_entropy,request_composition,exact_retrain,hop_groups))
    return metrics,protocol
