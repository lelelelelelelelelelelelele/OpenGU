"""Unit tests for IMStrategy, HybridStrategy, and registration."""

import json
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn as nn
from torch_geometric.data import Data

import attack.attack_strategies.im_strategy as im_strategy_module
from attack.attack_strategies.im_strategy import IMStrategy, HAS_NUMBA
from attack.attack_strategies.hybrid_strategy import HybridStrategy

# IMV4Strategy / HybridV4Strategy were merged into IMStrategy / HybridStrategy
# on 2026-05-05. The names below exist as aliases in attack_strategies/__init__.py
# (`IMV4Strategy = IMStrategy`, `HybridV4Strategy = HybridStrategy`) so old
# imports keep working. We import via that alias path here to assert the
# alias is wired correctly.
from attack.attack_strategies import IMV4Strategy, HybridV4Strategy


def _make_dummy_data(num_nodes=100, num_features=16, num_edges=300):
    """创建一个用于测试的 dummy PyG Data 对象。"""
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))
    y = torch.randint(0, 7, (num_nodes,))
    return Data(x=x, edge_index=edge_index, y=y)


def _make_dummy_model(num_features=16, num_classes=7):
    """创建一个简单的 GNN 模型用于测试。"""
    class DummyGNN(nn.Module):
        def __init__(self, in_channels, out_channels):
            super().__init__()
            self.lin = nn.Linear(in_channels, out_channels)

        def forward(self, x, edge_index=None):
            return self.lin(x)

    return DummyGNN(num_features, num_classes)


# ---------------------------------------------------------------------------
# TestIMStrategy
# ---------------------------------------------------------------------------
class TestIMStrategy:
    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data()
        strategy = IMStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复节点"""
        data = _make_dummy_data()
        strategy = IMStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """索引 ∈ [0, N)"""
        data = _make_dummy_data(num_nodes=80)
        strategy = IMStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert (result >= 0).all() and (result < 80).all()

    def test_ratio_interface(self):
        """select_nodes_by_ratio 正常工作"""
        data = _make_dummy_data(num_nodes=200)
        strategy = IMStrategy(args={'mc_rounds': 10})
        ratio = 0.02  # 4 nodes
        result = strategy.select_nodes_by_ratio(data, model=None, ratio=ratio)
        expected_k = int(200 * ratio)
        assert result.shape == (expected_k,)

    def test_star_graph_center(self):
        """星图（节点0连接1-5），k=1 应选中中心节点0"""
        # Star graph: 0->1, 0->2, 0->3, 0->4, 0->5
        src = [0, 0, 0, 0, 0]
        dst = [1, 2, 3, 4, 5]
        edge_index = torch.tensor([src, dst], dtype=torch.long)
        data = Data(
            x=torch.randn(6, 16),
            edge_index=edge_index,
            y=torch.randint(0, 7, (6,)),
        )
        strategy = IMStrategy(args={'propagation_prob': 0.5, 'mc_rounds': 200})
        result = strategy.select_nodes(data, model=None, k=1)
        assert result.item() == 0

    def test_initial_marginal_gains_shape(self):
        """compute_initial_marginal_gains 返回 [N_cand] tensor"""
        data = _make_dummy_data(num_nodes=50)
        strategy = IMStrategy(args={'mc_rounds': 10})
        candidates = list(range(50))
        scores = strategy.compute_initial_marginal_gains(
            data.edge_index, data.num_nodes, candidates
        )
        assert scores.shape == (50,)

    def test_celf_matches_naive_top1(self):
        """CELF 选出的第一个节点与 naive（取 initial gain 最大者）一致"""
        data = _make_dummy_data(num_nodes=30, num_edges=60)
        strategy = IMStrategy(args={'mc_rounds': 50})
        candidates = list(range(30))

        # CELF result
        selected, _ = strategy.compute_im_celf(
            data.edge_index, data.num_nodes, 1, candidates
        )

        # Naive: compute all initial gains, pick argmax
        scores = strategy.compute_initial_marginal_gains(
            data.edge_index, data.num_nodes, candidates
        )
        naive_top1 = candidates[scores.argmax().item()]

        assert selected[0] == naive_top1

    def test_im_v4_output_shape(self):
        """IMV4Strategy alias resolves to IMStrategy and produces k nodes.

        Post-merge (2026-05-05) IMV4Strategy is an alias for IMStrategy.
        Both `im_v4_batch_size` (legacy) and `im_batch_size` should work.
        """
        data = _make_dummy_data()
        # Legacy kwarg name still accepted for backward compat.
        strategy = IMV4Strategy(args={'mc_rounds': 10, 'im_v4_batch_size': 3})
        assert strategy.im_batch_size == 3, "legacy im_v4_batch_size should map to im_batch_size"
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)
        assert len(result.unique()) == k

        # New kwarg name also works.
        strategy2 = IMStrategy(args={'mc_rounds': 10, 'im_batch_size': 3})
        assert strategy2.im_batch_size == 3


# ---------------------------------------------------------------------------
# TestHybridFusion (pure function tests, no model needed)
# ---------------------------------------------------------------------------
class TestHybridFusion:
    def test_alpha_one_follows_if(self):
        """α=1.0 时 argmax 与 IF scores argmax 一致"""
        if_scores = torch.tensor([1.0, 5.0, 3.0, 2.0])
        im_scores = torch.tensor([4.0, 1.0, 2.0, 3.0])
        fused = HybridStrategy.fuse_scores(if_scores, im_scores, method='rank', alpha=1.0)
        assert fused.argmax() == if_scores.argmax()

    def test_alpha_zero_follows_im(self):
        """α=0.0 时 argmax 与 IM scores argmax 一致"""
        if_scores = torch.tensor([1.0, 5.0, 3.0, 2.0])
        im_scores = torch.tensor([4.0, 1.0, 2.0, 3.0])
        fused = HybridStrategy.fuse_scores(if_scores, im_scores, method='rank', alpha=0.0)
        assert fused.argmax() == im_scores.argmax()

    def test_rank_scale_invariant(self):
        """rank 融合：将 IF scores 乘以 100，排序结果不变"""
        if_scores = torch.tensor([1.0, 5.0, 3.0, 2.0])
        im_scores = torch.tensor([4.0, 1.0, 2.0, 3.0])

        fused1 = HybridStrategy.fuse_scores(if_scores, im_scores, method='rank', alpha=0.5)
        fused2 = HybridStrategy.fuse_scores(if_scores * 100, im_scores, method='rank', alpha=0.5)

        order1 = fused1.argsort(descending=True)
        order2 = fused2.argsort(descending=True)
        assert torch.equal(order1, order2)

    def test_linear_scale_sensitive(self):
        """linear 融合：乘以常数可能改变排序"""
        if_scores = torch.tensor([1.0, 3.0, 2.0])
        im_scores = torch.tensor([3.0, 1.0, 2.0])

        fused1 = HybridStrategy.fuse_scores(if_scores, im_scores, method='linear', alpha=0.5)
        fused2 = HybridStrategy.fuse_scores(if_scores * 100, im_scores, method='linear', alpha=0.5)

        order1 = fused1.argsort(descending=True)
        order2 = fused2.argsort(descending=True)
        # linear with different scales produces different min-max normalization
        # This test just verifies it doesn't crash; scale sensitivity is expected
        assert fused1.shape == fused2.shape

    def test_nan_handling(self):
        """含 NaN 的输入不 crash"""
        if_scores = torch.tensor([1.0, float('nan'), 3.0])
        im_scores = torch.tensor([2.0, 4.0, float('nan')])
        fused = HybridStrategy.fuse_scores(if_scores, im_scores, method='rank', alpha=0.5)
        assert not torch.isnan(fused).any()

    def test_identical_scores(self):
        """全相同分数不 crash（min_max 分母为 0 的边界）"""
        if_scores = torch.tensor([3.0, 3.0, 3.0])
        im_scores = torch.tensor([3.0, 3.0, 3.0])
        fused = HybridStrategy.fuse_scores(if_scores, im_scores, method='linear', alpha=0.5)
        assert not torch.isnan(fused).any()
        assert (fused == 0).all()  # min_max returns zeros when all equal


# ---------------------------------------------------------------------------
# TestHybridStrategy (end-to-end with DummyGNN)
# ---------------------------------------------------------------------------
class TestHybridStrategy:
    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data(num_nodes=50, num_features=16)
        model = _make_dummy_model(num_features=16, num_classes=7)
        strategy = HybridStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=model, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复"""
        data = _make_dummy_data(num_nodes=50, num_features=16)
        model = _make_dummy_model(num_features=16, num_classes=7)
        strategy = HybridStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=model, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """索引合法"""
        data = _make_dummy_data(num_nodes=50, num_features=16)
        model = _make_dummy_model(num_features=16, num_classes=7)
        strategy = HybridStrategy(args={'mc_rounds': 10})
        k = 5
        result = strategy.select_nodes(data, model=model, k=k)
        assert (result >= 0).all() and (result < 50).all()

    def test_hybrid_v4_output_shape(self):
        """HybridV4Strategy alias resolves to HybridStrategy and produces k nodes.

        Post-merge (2026-05-05) HybridV4Strategy is an alias for HybridStrategy.
        """
        data = _make_dummy_data(num_nodes=50, num_features=16)
        model = _make_dummy_model(num_features=16, num_classes=7)
        strategy = HybridV4Strategy(args={'mc_rounds': 10, 'im_v4_batch_size': 3})
        k = 5
        result = strategy.select_nodes(data, model=model, k=k)
        assert result.shape == (k,)
        assert len(result.unique()) == k


# ---------------------------------------------------------------------------
# TestRegistration
# ---------------------------------------------------------------------------
class TestRegistration:
    def test_im_in_builtin(self):
        from attack.attack_manager import AttackManager
        assert "im" in AttackManager.BUILTIN_STRATEGIES

    def test_hybrid_in_builtin(self):
        from attack.attack_manager import AttackManager
        assert "hybrid" in AttackManager.BUILTIN_STRATEGIES

    def test_im_resolves_to_canonical_implementation(self):
        # 2026-05-05: V4 merged into IMStrategy. Registry now points to
        # IMStrategy directly (which contains the batch-CELF numba path).
        from attack.attack_manager import AttackManager
        assert AttackManager.BUILTIN_STRATEGIES["im"] is IMStrategy
        # Backward-compat alias still resolves to the same class.
        assert IMV4Strategy is IMStrategy

    def test_hybrid_resolves_to_canonical_implementation(self):
        from attack.attack_manager import AttackManager
        assert AttackManager.BUILTIN_STRATEGIES["hybrid"] is HybridStrategy
        assert HybridV4Strategy is HybridStrategy

    def test_v4_alias_no_longer_registered(self):
        # Old aliases removed; runs/cache are clean of the suffix going forward.
        from attack.attack_manager import AttackManager
        assert "im_v4" not in AttackManager.BUILTIN_STRATEGIES
        assert "hybrid_v4" not in AttackManager.BUILTIN_STRATEGIES

    def test_import_from_subpackage(self):
        from attack.attack_strategies import IMStrategy, HybridStrategy, IMV4Strategy, HybridV4Strategy
        assert IMStrategy is not None
        assert HybridStrategy is not None
        assert IMV4Strategy is not None
        assert HybridV4Strategy is not None


# ---------------------------------------------------------------------------
# TestIMAcceleration
# ---------------------------------------------------------------------------
requires_numba = pytest.mark.skipif(not HAS_NUMBA, reason="numba not installed")


class TestIMAcceleration:
    """Tests for numba acceleration, CSR building, and candidate pruning."""

    @requires_numba
    def test_numba_rand_float_spans_unit_interval(self):
        """Numba RNG helper should produce values across [0, 1), not a tiny subrange."""
        from attack.attack_strategies.im_strategy import _rand_float

        state = np.uint64(123456789)
        values = []
        for _ in range(4096):
            state, r = _rand_float(state)
            values.append(float(r))

        assert all(0.0 <= v < 1.0 for v in values)
        assert min(values) < 0.1
        assert max(values) > 0.9

    def test_csr_structure(self):
        """CSR indptr/indices have correct shapes and values."""
        # Simple graph: 0->1, 0->2, 1->2
        edge_index = torch.tensor([[0, 0, 1], [1, 2, 2]], dtype=torch.long)
        strategy = IMStrategy(args={'mc_rounds': 5})
        indptr, indices = strategy._build_adjacency_csr(edge_index, num_nodes=3)

        assert indptr.dtype == np.int32
        assert indices.dtype == np.int32
        assert len(indptr) == 4  # num_nodes + 1
        # Node 0 has neighbors [1, 2], node 1 has [2], node 2 has []
        assert indptr[0] == 0
        assert indptr[1] == 2  # node 0: 2 edges
        assert indptr[2] == 3  # node 1: 1 edge
        assert indptr[3] == 3  # node 2: 0 edges
        assert list(indices) == [1, 2, 2]

    def test_csr_deduplication(self):
        """CSR builder deduplicates repeated edges."""
        # Duplicate edge: 0->1 appears twice
        edge_index = torch.tensor([[0, 0, 0], [1, 1, 2]], dtype=torch.long)
        strategy = IMStrategy(args={'mc_rounds': 5})
        indptr, indices = strategy._build_adjacency_csr(edge_index, num_nodes=3)

        # After dedup: 0->1, 0->2
        assert indptr[1] - indptr[0] == 2
        assert sorted(indices[indptr[0]:indptr[1]]) == [1, 2]

    def test_csr_sorted_order(self):
        """CSR indices within each node are sorted by dst."""
        edge_index = torch.tensor([[0, 0, 0], [3, 1, 2]], dtype=torch.long)
        strategy = IMStrategy(args={'mc_rounds': 5})
        indptr, indices = strategy._build_adjacency_csr(edge_index, num_nodes=4)

        neighbors = list(indices[indptr[0]:indptr[1]])
        assert neighbors == sorted(neighbors)

    @requires_numba
    def test_numba_vs_python_consistency(self):
        """Numba and Python paths produce similar spread on a directed star graph.

        Uses a directed star (hub 0 -> leaves) where the hub clearly
        has the highest spread, so both paths should agree on the top node.
        """
        # Directed star: 0->1, 0->2, ..., 0->9 (no reverse edges)
        # Plus a short chain: 1->2, 2->3
        src = list(range(10)) * 0  # empty
        src = [0] * 9 + [1, 2]
        dst = list(range(1, 10)) + [2, 3]
        edge_index = torch.tensor([src, dst], dtype=torch.long)
        num_nodes = 10

        strategy = IMStrategy(args={'mc_rounds': 500, 'propagation_prob': 0.5})
        candidates = list(range(num_nodes))

        scores_numba = strategy._compute_initial_gains_numba(
            edge_index, num_nodes, candidates
        )
        scores_python = strategy._compute_initial_gains_python(
            edge_index, num_nodes, candidates
        )

        # Both paths should agree that node 0 (the hub) has the highest spread
        assert scores_numba.argmax().item() == 0
        assert scores_python.argmax().item() == 0

        # Hub spread should be much higher than isolated leaf nodes (4..9)
        hub_numba = scores_numba[0].item()
        leaf_numba = scores_numba[4:].mean().item()
        assert hub_numba > leaf_numba + 0.5

    @requires_numba
    def test_numba_deterministic(self):
        """Numba path produces identical results across calls."""
        torch.manual_seed(42)
        data = _make_dummy_data(num_nodes=20, num_edges=50)
        strategy = IMStrategy(args={'mc_rounds': 50})
        candidates = list(range(20))

        scores1 = strategy._compute_initial_gains_numba(
            data.edge_index, data.num_nodes, candidates
        )
        scores2 = strategy._compute_initial_gains_numba(
            data.edge_index, data.num_nodes, candidates
        )
        assert torch.equal(scores1, scores2)

    @requires_numba
    def test_numba_matches_python_on_im_fixture(self):
        """Numba and Python paths should agree on the im_basic_k3 fixture."""
        fixture_path = Path(__file__).parent / "fixtures" / "strategies" / "im_basic_k3.json"
        spec = json.loads(fixture_path.read_text(encoding="utf-8"))
        graph = spec["graph"]
        data = Data(
            num_nodes=int(graph["num_nodes"]),
            x=torch.tensor(graph["x"], dtype=torch.float),
            edge_index=torch.tensor(graph["edge_index"], dtype=torch.long),
            y=torch.tensor(graph["y"], dtype=torch.long),
            train_mask=torch.tensor(graph["train_mask"], dtype=torch.bool),
        )

        original_has_numba = im_strategy_module.HAS_NUMBA
        try:
            im_strategy_module.HAS_NUMBA = False
            selected_python = IMStrategy(spec["args"]).select_nodes(data, model=None, k=int(spec["k"]))

            im_strategy_module.HAS_NUMBA = True
            selected_numba = IMStrategy(spec["args"]).select_nodes(data, model=None, k=int(spec["k"]))
        finally:
            im_strategy_module.HAS_NUMBA = original_has_numba

        assert selected_numba.tolist() == selected_python.tolist()

    @requires_numba
    def test_numba_celf_output_shape(self):
        """Numba CELF returns correct number of nodes."""
        torch.manual_seed(42)
        data = _make_dummy_data(num_nodes=30, num_edges=60)
        strategy = IMStrategy(args={'mc_rounds': 20})
        candidates = list(range(30))

        selected, scores = strategy._compute_im_celf_numba(
            data.edge_index, data.num_nodes, 5, candidates
        )
        assert len(selected) == 5
        assert scores.shape == (5,)
        assert len(set(selected)) == 5  # no duplicates

    def test_candidate_fraction(self):
        """candidate_fraction prunes candidate set."""
        torch.manual_seed(42)
        data = _make_dummy_data(num_nodes=100, num_edges=300)
        strategy = IMStrategy(args={'mc_rounds': 5, 'candidate_fraction': 0.3})
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)
        assert len(result.unique()) == k

    def test_candidate_fraction_preserves_min_k(self):
        """candidate_fraction never prunes below k candidates."""
        torch.manual_seed(42)
        data = _make_dummy_data(num_nodes=50, num_edges=100)
        # fraction=0.05 would give 2.5 -> 2 candidates, but k=5 should force 5
        strategy = IMStrategy(args={'mc_rounds': 5, 'candidate_fraction': 0.05})
        k = 5
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)

    @requires_numba
    def test_splitmix64_deterministic(self):
        """splitmix64 RNG produces identical sequences for same seed."""
        from attack.attack_strategies.im_strategy import _splitmix64

        state1 = np.uint64(12345)
        state2 = np.uint64(12345)

        results1 = []
        results2 = []
        for _ in range(10):
            state1, z1 = _splitmix64(state1)
            state2, z2 = _splitmix64(state2)
            results1.append(z1)
            results2.append(z2)

        assert results1 == results2

    def test_has_numba_flag(self):
        """HAS_NUMBA is a boolean."""
        assert isinstance(HAS_NUMBA, bool)
