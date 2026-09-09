"""Explicit IM configurations and incremental selection; no training runs."""
from pathlib import Path

import numpy as np
import pytest
import yaml

from experiments.modular_config import selector
from experiments.im_score_benchmark.rr_core import RRBundle
from experiments.im_score_benchmark.selectors import maximum_coverage_greedy


ROOT = Path(__file__).resolve().parents[1] / 'experiments/configs'


def test_public_im_instances_resolve_explicit_algorithms():
    rr = selector(yaml.safe_load((ROOT / 'selectors/im_rr_greedy.yaml').read_text()))
    assert rr['method'] == 'im_rr_greedy'
    assert rr['parameters']['rr_count'] == 4096
    celf = selector(yaml.safe_load((ROOT / 'selectors/im_celf.yaml').read_text()))
    assert celf['method'] == 'im'
    assert celf['parameters']['im_batch_size'] == 1
    for name in ('single_seed', 'multi_seed', 'candidates'):
        table = yaml.safe_load((ROOT / f'aagu040/{name}.yaml').read_text())
        for ref in table['selector_refs']:
            selector(yaml.safe_load((ROOT / 'selectors' / ref).read_text()))


@pytest.mark.parametrize('seed', range(8))
def test_incremental_greedy_matches_full_recount_at_every_step(seed):
    rng = np.random.default_rng(seed)
    candidates = [1, 3, 5, 7, 9, 11]
    rows = [[node for node in candidates if rng.random() < .35] for _ in range(31)]
    # Include an empty RR row and strong overlap explicitly.
    rows += [[], [1, 3, 5], [1, 3, 5]]
    bundle = RRBundle.from_rr_sets(num_nodes=12, candidate_nodes=candidates,
        rr_sets=rows, roots=[0] * len(rows), propagation_probability=.1, rr_seed=seed)
    result = maximum_coverage_greedy(bundle, len(candidates))
    selected, covered, trace, gains = [], set(), [], []
    for _ in candidates:
        remaining = [node for node in candidates if node not in selected]
        hits = {node: {i for i, row in enumerate(rows) if node in row} - covered
                for node in remaining}
        node = min(remaining, key=lambda v: (-len(hits[v]), v))
        selected.append(node)
        gains.append(len(hits[node]))
        covered |= hits[node]
        trace.append(len(covered))
    assert result.selected_nodes.tolist() == selected
    assert result.accepted_gains.tolist() == gains
    assert result.metadata['coverage_trace'] == trace
    assert result.metadata['covered_rr_count'] == len(covered)
    assert result.metadata['estimated_spread'] == pytest.approx(12 * len(covered) / len(rows))
