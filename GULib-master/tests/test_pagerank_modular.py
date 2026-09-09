"""PageRank YAML uses the existing graph algorithm and exact immutable cache lane."""
import copy
import networkx as nx
import pytest
import torch
from torch_geometric.data import Data
from torch_geometric.utils import to_networkx
from attack.attack_strategies.pagerank_strategy import PageRankStrategy
from experiments.target_direct_v1.methods import Computations, METHODS, resolve_parameters
from experiments.c_target_v1.core import stable_ranking
from experiments.modular_config import selector, load_experiment
from experiments.effective_config import ConfigurationError
from test_modular_consumers import tables, run, write_yaml


def test_full_scores_existing_graph_semantics_and_nondefault_alpha():
    data = Data(num_nodes=6, edge_index=torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 4, 4]]),
                train_mask=torch.tensor([True, False, True, True, True, True]),
                val_mask=torch.tensor([False, True, False, False, False, False]))
    c = Computations(None, data, [])
    outputs = []
    for alpha in (.85, .25):
        p = resolve_parameters('pagerank', {'pagerank_alpha': alpha})
        scores = METHODS['pagerank'](c, p)
        expected = nx.pagerank(to_networkx(data, to_undirected=True), alpha=alpha)
        assert torch.equal(scores, torch.tensor([expected[i] for i in c.candidates.tolist()], dtype=torch.float32))
        assert torch.equal(scores, PageRankStrategy(p).score_nodes(data)[c.candidates])
        outputs.append(scores)
    assert not torch.equal(*outputs)
    # Isolated nodes are retained; a tied graph uses node IDs, never torch.topk ties.
    tied = data.clone()
    tied.edge_index = torch.empty((2, 0), dtype=torch.long)
    tc = Computations(None, tied, [])
    assert stable_ranking(tc.candidates.tolist(), METHODS['pagerank'](tc, resolve_parameters('pagerank'))) == tuple(tc.candidates.tolist())


@pytest.mark.parametrize('alpha', [-.1, 1.1, float('nan'), float('inf'), True])
def test_invalid_damping_rejected(alpha):
    with pytest.raises(ConfigurationError):
        resolve_parameters('pagerank', {'pagerank_alpha': alpha})


def test_real_yaml_cold_warm_changed_parameter_and_ten_percent(tables):
    root = tables[0]
    value = {'kind': 'selector', 'schema_version': 1, 'method': 'pagerank',
             'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'ratio', 'value': .1},
             'parameters': {'pagerank_alpha': .85}}
    write_yaml(root / 'pagerank.yaml', value)
    cold = run(tables, 'pagerank-cold', selector_refs=['pagerank.yaml'])['selectors'][0]
    warm = run(tables, 'pagerank-warm', selector_refs=['pagerank.yaml'])['selectors'][0]
    assert not cold['score']['hit'] and not cold['selection']['cache']['hit']
    assert warm['score']['hit'] and warm['selection']['cache']['hit']
    assert cold['score']['recipe_hash'] == warm['score']['recipe_hash']
    assert cold['selection']['artifact']['artifact_id'] == warm['selection']['artifact']['artifact_id']
    assert cold['selection']['request_max_k'] == cold['selection']['artifact_k'] == 1
    assert len(cold['scores']) == len(cold['ranking']) == 10
    assert all(node < 10 for node in cold['ranking'])
    value['parameters']['pagerank_alpha'] = .25
    write_yaml(root / 'pagerank.yaml', value)
    changed = run(tables, 'pagerank-changed', selector_refs=['pagerank.yaml'])['selectors'][0]
    assert not changed['score']['hit'] and not changed['selection']['cache']['hit']
    assert changed['score']['recipe_hash'] != cold['score']['recipe_hash']
    assert changed['selection']['artifact']['artifact_id'] != cold['selection']['artifact']['artifact_id']
    assert 'selector_model' not in changed['score']['recipe']['fields']


def test_three_public_datasets_expand_without_producers(tmp_path):
    from experiments.modular_run import execute
    value = {'kind': 'experiment', 'schema_version': 1, 'experiment_id': 'aagu042-dry',
             'stage': 'unlearning', 'unlearning_refs': ['gif.yaml'], 'dataset_refs': ['cora.yaml', 'citeseer.yaml', 'pubmed.yaml'],
             'selector_refs': ['pagerank.yaml'], 'seeds': [42, 212, 2024],
             'budget_ratios': [.1], 'matrix': 'cartesian_product'}
    import yaml
    path = tmp_path / 'experiment.yaml'
    path.write_text(yaml.safe_dump(value), encoding='utf-8')
    plan = execute(path, dry_run=True)
    assert plan['logical_cells'] == 9
    assert plan['producer_called'] is False
