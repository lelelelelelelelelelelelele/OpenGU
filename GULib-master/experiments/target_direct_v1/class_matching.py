"""Transform a verified full R-point order without reading noncandidate labels."""
from __future__ import annotations

import hashlib
import torch

METHOD = 'class_matched_r_point'
MATCHING_VERSION = 'class-prefix-torch-randperm-v1'


def class_prefix_matched_order(candidate_ids, candidate_labels, source_ranking, matching_seed):
    candidates, labels, ranking = tuple(candidate_ids), tuple(candidate_labels), tuple(source_ranking)
    if (not candidates or any(type(v) is not int or v < 0 for v in candidates)
            or candidates != tuple(sorted(set(candidates)))):
        raise ValueError('matching candidates must be nonempty unique increasing nonnegative integers')
    if (len(labels) != len(candidates)
            or any(type(v) is not int or v < 0 for v in labels)):
        raise ValueError('matching labels must be candidate-aligned nonnegative integers')
    if (len(ranking) != len(candidates) or any(type(v) is not int for v in ranking)
            or set(ranking) != set(candidates)):
        raise ValueError('source R-point ranking must contain exactly all candidates once')
    if type(matching_seed) is not int or not 0 <= matching_seed < 2**63:
        raise ValueError('matching_seed must be an explicit integer in [0, 2**63)')
    label_by_id = dict(zip(candidates, labels))
    classes = {}
    for node, label in zip(candidates, labels):
        classes.setdefault(label, []).append(node)
    shuffled = {}
    for label, nodes in sorted(classes.items()):
        # Class streams are independent of class enumeration and global torch RNG.
        domain = ('%s:%d:%d' % (MATCHING_VERSION, matching_seed, label)).encode('ascii')
        seed = int.from_bytes(hashlib.sha256(domain).digest()[:8], 'big') % 2**63
        generator = torch.Generator(device='cpu').manual_seed(seed)
        order = torch.randperm(len(nodes), generator=generator).tolist()
        shuffled[label] = iter([nodes[i] for i in order])
    return tuple(next(shuffled[label_by_id[node]]) for node in ranking)


def ordinal_scores(candidate_ids, ranking):
    """Encode order for the existing ScoreBundle; values are not IF magnitudes."""
    positions = {node: len(ranking) - i for i, node in enumerate(ranking)}
    return torch.tensor([positions[node] for node in candidate_ids], dtype=torch.float64)


def score_class_matched(computations, parameters, *, source_ranking):
    candidates = computations.candidates.detach().cpu().tolist()
    labels = computations.data.y[computations.candidates].detach().cpu().tolist()
    ranking = class_prefix_matched_order(candidates, labels, source_ranking, parameters['matching_seed'])
    return ordinal_scores(candidates, ranking)


def source_parameters(parameters):
    return {key: value for key, value in parameters.items() if key != 'matching_seed'}
