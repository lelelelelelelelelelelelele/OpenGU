"""Paired prediction disagreement on retained test nodes of the bound graph."""
from __future__ import annotations

import hashlib
import numpy as np

from experiments.effective_config import ConfigurationError
from experiments.implementation_identity import implementation_fingerprint


def exact_retrain(output, candidates):
    """Reject missing/ambiguous pairs, including repeated identical references."""
    matches = [(ref, payload) for ref, payload in candidates
               if payload.identity['target']['method'] == 'Retrain'
               and all(payload.identity[key] == output.identity[key]
                       for key in ('selection', 'pairing', 'dataset_input', 'graph_fingerprint'))]
    if len(matches) != 1:
        raise ConfigurationError('flip-hop needs exactly one verified Retrain with the same request, Dataset/Split, training and evaluation graph')
    reference, retrain = matches[0]
    for name in ('selected_nodes', 'y', 'test_mask', 'edge_index', 'evaluation_edge_index'):
        if not np.array_equal(output.arrays[name], retrain.arrays[name]):
            raise ConfigurationError('paired output evaluation inputs differ: ' + name)
    if output.arrays['logits'].shape != retrain.arrays['logits'].shape:
        raise ConfigurationError('paired prediction shapes differ')
    return reference, retrain


def hop_groups(edge_index, selected_nodes, num_nodes):
    """Undirected multi-source distances capped after three hops; 4 means far."""
    distance = np.full(num_nodes, 4, dtype=np.int8)
    distance[selected_nodes] = 0
    source, target = edge_index
    # Three vectorized edge scans bound memory to O(V+E), without Python adjacency lists.
    for hop in (1, 2, 3):
        frontier = distance == hop - 1
        neighbors = np.concatenate((target[frontier[source]], source[frontier[target]]))
        distance[neighbors[distance[neighbors] == 4]] = hop
    return distance


def flip_hop(output, retrain):
    """Return counts/rates and the full versioned measurement protocol."""
    a = output.arrays
    mask = a['test_mask'].copy()
    mask[a['selected_nodes']] = False
    flipped = a['logits'].argmax(axis=1) != retrain.arrays['logits'].argmax(axis=1)
    distance = hop_groups(a['edge_index'], a['selected_nodes'], len(mask))
    count = int(mask.sum())
    disagreements = int(flipped[mask].sum())
    metrics = {'node_count': count, 'flipped_count': disagreements,
               'fraction_flipped': disagreements / count if count else None}
    for hop, label in ((1, '1'), (2, '2'), (3, '3'), (4, 'gt3')):
        group = mask & (distance == hop)
        size, changed = int(group.sum()), int(flipped[group].sum())
        metrics.update({label + '_hop_count': size, label + '_hop_flipped_count': changed,
                        label + '_hop_flip_rate': changed / size if size else None})
    protocol = {
        'version': 'retained-test-gu-retrain-flip-hop-v1',
        'comparison': 'argmax_gu_vs_same_request_retrain_first_index_ties',
        'evaluation_mask': 'test_mask_excluding_selected_nodes',
        'evaluation_mask_sha256': hashlib.sha256(np.asarray(mask, dtype=np.uint8).tobytes()).hexdigest(),
        'node_count': len(mask),
        'hop_graph': 'bound_pre_deletion_edge_index',
        'graph_fingerprint': output.identity['graph_fingerprint'],
        'dataset_input': output.identity['dataset_input'],
        'prediction_graph': output.identity['pairing']['evaluation_graph_identity'],
        'grouping': 'undirected_multi_source_shortest_distance_1_2_3_gt3_or_unreachable',
        'empty_rate': None,
        'implementation': implementation_fingerprint(flip_hop, exact_retrain, hop_groups),
        'numpy_version': np.__version__,
    }
    return metrics, protocol
