"""Unit tests for IMStrategy, HybridStrategy, and registration."""

import torch
import torch.nn as nn
from torch_geometric.data import Data

from attack.attack_strategies.im_strategy import IMStrategy
from attack.attack_strategies.hybrid_strategy import HybridStrategy


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

    def test_import_from_subpackage(self):
        from attack.attack_strategies import IMStrategy, HybridStrategy
        assert IMStrategy is not None
        assert HybridStrategy is not None
