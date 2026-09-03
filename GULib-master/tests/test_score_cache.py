"""Unit tests for ScoreCache and the IF/IM caching paths in strategies."""

import json
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn as nn
from torch_geometric.data import Data

from attack.score_cache import ScoreCache, graph_fingerprint, model_fingerprint
from attack.attack_strategies.im_strategy import IMStrategy
from attack.attack_strategies.tracin_strategy import TracInStrategy
from attack.attack_strategies.hybrid_strategy import HybridStrategy


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def tiny_graph():
    """Deterministic 20-node graph so cache keys stay stable across runs."""
    torch.manual_seed(0)
    num_nodes = 20
    x = torch.randn(num_nodes, 8)
    # Deterministic ring + a few chords
    src = list(range(num_nodes)) + [0, 5, 10]
    dst = [(i + 1) % num_nodes for i in range(num_nodes)] + [10, 15, 0]
    edge_index = torch.tensor([src + dst, dst + src], dtype=torch.long)
    y = torch.randint(0, 3, (num_nodes,))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:15] = True
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, num_nodes=num_nodes)


@pytest.fixture
def tiny_model():
    class M(nn.Module):
        def __init__(self):
            super().__init__()
            self.lin = nn.Linear(8, 3)

        def forward(self, x, edge_index=None):
            return self.lin(x)

    torch.manual_seed(0)
    return M()


# ---------------------------------------------------------------------------
# ScoreCache primitives
# ---------------------------------------------------------------------------
# Fingerprint helpers
# ---------------------------------------------------------------------------
class TestFingerprints:
    def test_graph_fingerprint_deterministic(self, tiny_graph):
        cands = torch.arange(tiny_graph.num_nodes)
        a = graph_fingerprint(tiny_graph.edge_index, tiny_graph.num_nodes)
        b = graph_fingerprint(tiny_graph.edge_index, tiny_graph.num_nodes)
        assert a == b

    def test_graph_fingerprint_changes_with_edges(self, tiny_graph):
        cands = torch.arange(tiny_graph.num_nodes)
        ei2 = tiny_graph.edge_index.clone()
        ei2[0, 0] = (ei2[0, 0] + 1) % tiny_graph.num_nodes
        assert graph_fingerprint(tiny_graph.edge_index, tiny_graph.num_nodes) \
            != graph_fingerprint(ei2, tiny_graph.num_nodes)

    def test_model_fingerprint_changes_after_update(self, tiny_model):
        before = model_fingerprint(tiny_model)
        with torch.no_grad():
            tiny_model.lin.weight.add_(0.01)
        after = model_fingerprint(tiny_model)
        assert before != after


# ---------------------------------------------------------------------------
# Strategy integration
# ---------------------------------------------------------------------------
class TestIMScoreCacheIntegration:
    def test_im_cache_hit_on_second_call(self, tiny_graph, tmp_path, capsys):
        args = {
            'mc_rounds': 5,
            'propagation_prob': 0.1,
            'cache_v2_store_root': str(tmp_path),
        }
        s1 = IMStrategy(args)
        cands = list(range(15))
        s1.compute_initial_marginal_gains(
            tiny_graph.edge_index, tiny_graph.num_nodes, cands
        )
        out1 = capsys.readouterr().out
        assert "[ScoreCache] MISS im" in out1
        assert "[ScoreCache] SAVE im" in out1

        s2 = IMStrategy(args)
        scores2 = s2.compute_initial_marginal_gains(
            tiny_graph.edge_index, tiny_graph.num_nodes, cands
        )
        out2 = capsys.readouterr().out
        assert "[ScoreCache] HIT  im" in out2
        assert scores2.shape[0] == len(cands)

    def test_im_cache_disable_flag(self, tiny_graph, tmp_path, capsys):
        args = {
            'mc_rounds': 5,
            'enable_score_cache': False,
            'cache_v2_store_root': str(tmp_path),
        }
        s = IMStrategy(args)
        s.compute_initial_marginal_gains(
            tiny_graph.edge_index, tiny_graph.num_nodes, list(range(15))
        )
        out = capsys.readouterr().out
        assert "[ScoreCache]" not in out


class TestTracInScoreCacheIntegration:
    def test_tracin_cache_hit_on_second_call(self, tiny_graph, tiny_model, tmp_path, capsys):
        args = {
            'dataset_name': 'tiny',
            'base_model': 'GCN',
            'unlearn_ratio': 0.05,
            'seed': 2024,
            'device': torch.device('cpu'),
            'cache_v2_store_root': str(tmp_path),
        }
        s1 = TracInStrategy(args)
        cands = tiny_graph.train_mask.nonzero(as_tuple=False).squeeze(-1)
        scores1 = s1.compute_scores(tiny_model, tiny_graph.clone(), cands)
        out1 = capsys.readouterr().out
        assert "[ScoreCache] MISS if" in out1

        s2 = TracInStrategy(args)
        scores2 = s2.compute_scores(tiny_model, tiny_graph.clone(), cands)
        out2 = capsys.readouterr().out
        assert "[ScoreCache] HIT  if" in out2
        torch.testing.assert_close(scores1.detach(), scores2.detach())


    def test_tracin_cache_misses_on_different_dataset(self, tiny_graph, tiny_model, tmp_path, capsys):
        """Static config IS what isolates the cache — change dataset_name → miss."""
        cands = tiny_graph.train_mask.nonzero(as_tuple=False).squeeze(-1)

        s1 = TracInStrategy({
            'dataset_name': 'cora', 'base_model': 'GCN', 'seed': 0,
            'device': torch.device('cpu'), 'cache_v2_store_root': str(tmp_path),
        })
        s1.compute_scores(tiny_model, tiny_graph.clone(), cands)
        capsys.readouterr()

        s2 = TracInStrategy({
            'dataset_name': 'arxiv', 'base_model': 'GCN', 'seed': 0,
            'device': torch.device('cpu'), 'cache_v2_store_root': str(tmp_path),
        })
        s2.compute_scores(tiny_model, tiny_graph.clone(), cands)
        out = capsys.readouterr().out
        assert "[ScoreCache] MISS if" in out


class TestHybridUsesBothCaches:
    def test_hybrid_second_run_hits_both_caches(self, tiny_graph, tiny_model, tmp_path, capsys):
        args = {
            'dataset_name': 'tiny',
            'base_model': 'GCN',
            'seed': 2024,
            'mc_rounds': 5,
            'alpha': 0.5,
            'fusion_method': 'rank',
            'device': torch.device('cpu'),
            'cache_v2_store_root': str(tmp_path),
        }
        h1 = HybridStrategy(args)
        h1.select_nodes(tiny_graph.clone(), tiny_model, k=4)
        out1 = capsys.readouterr().out
        assert "[ScoreCache] MISS if" in out1
        assert "[ScoreCache] MISS im" in out1

        # New strategy instance — must hit purely through cache files
        h2 = HybridStrategy(args)
        h2.select_nodes(tiny_graph.clone(), tiny_model, k=4)
        out2 = capsys.readouterr().out
        assert "[ScoreCache] HIT  if" in out2
        assert "[ScoreCache] HIT  im" in out2
        assert "[ScoreCache] MISS" not in out2

    def test_hybrid_alpha_sweep_only_hits_cache(self, tiny_graph, tiny_model, tmp_path, capsys):
        """The whole point: changing alpha must not trigger recomputation."""
        base_args = {
            'dataset_name': 'tiny',
            'base_model': 'GCN',
            'seed': 2024,
            'mc_rounds': 5,
            'fusion_method': 'rank',
            'device': torch.device('cpu'),
            'cache_v2_store_root': str(tmp_path),
        }
        # Warm cache once
        HybridStrategy({**base_args, 'alpha': 0.5}).select_nodes(
            tiny_graph.clone(), tiny_model, k=4
        )
        capsys.readouterr()

        for alpha in [0.1, 0.3, 0.7, 0.9]:
            HybridStrategy({**base_args, 'alpha': alpha}).select_nodes(
                tiny_graph.clone(), tiny_model, k=4
            )
        out = capsys.readouterr().out
        # Across 4 alpha values, every score lookup should be a HIT
        assert out.count("[ScoreCache] HIT  if") == 4
        assert out.count("[ScoreCache] HIT  im") == 4
        assert "[ScoreCache] MISS" not in out
