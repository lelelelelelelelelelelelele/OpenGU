"""Match a prepared M ranking's membership in two prepared S prefixes."""
from cache_v2 import canonical_sha256
from experiments.target_direct_v1.class_matching import class_prefix_matched_order, ordinal_scores

METHOD = 'overlap_profile_r_point'
VERSION = 'two-prefix-membership-permutation-v1'


def validate_profile_counts(counts, candidate_count=None):
    if (not isinstance(counts, (list, tuple)) or len(counts) != 2
            or any(type(k) is not int for k in counts) or not 0 < counts[0] < counts[1]
            or (candidate_count is not None and counts[1] >= candidate_count)):
        raise ValueError('profile_counts must be two increasing positive counts below the candidate count')
    return tuple(counts)


def source_parameters(parameters):
    return {k: v for k, v in parameters.items() if k not in ('overlap_seed', 'profile_counts')}


def draw_seed(parameters, source_identity, matched_identity):
    seed = parameters['overlap_seed']
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError('overlap_seed must be explicitly supplied in [0, 2**63)')
    return int(canonical_sha256(dict(algorithm=VERSION, overlap_seed=seed,
        profile_counts=list(validate_profile_counts(parameters['profile_counts'])),
        source_r_point=source_identity, source_class_matched=matched_identity))[:16], 16) % 2**63


def overlap_profile_order(candidate_ids, source_ranking, matched_ranking, parameters,
                          source_identity, matched_identity):
    candidates, source = tuple(candidate_ids), tuple(source_ranking)
    lo, hi = validate_profile_counts(parameters['profile_counts'], len(candidates))
    if (len(source) != len(candidates) or any(type(n) is not int for n in source)
            or set(source) != set(candidates)):
        raise ValueError('overlap profile requires a complete S ranking of the same candidates')
    first, second = set(source[:lo]), set(source[lo:hi])
    # These integers are S-prefix membership, never the Dataset's class labels.
    layers = [0 if n in first else 1 if n in second else 2 for n in candidates]
    return class_prefix_matched_order(candidates, layers, matched_ranking,
        draw_seed(parameters, source_identity, matched_identity))


def score_overlap(computations, parameters, *, source_ranking, matched_ranking,
                  source_identity, matched_identity):
    candidates = computations.candidates.detach().cpu().tolist()
    ranking = overlap_profile_order(candidates, source_ranking, matched_ranking, parameters,
                                    source_identity, matched_identity)
    return ordinal_scores(candidates, ranking)
