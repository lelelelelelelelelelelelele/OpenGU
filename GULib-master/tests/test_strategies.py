"""Unit tests for attack strategies (Steps 1-5)."""

import torch
from torch_geometric.data import Data

from attack.attack_strategies import RandomStrategy, DegreeStrategy, PageRankStrategy, TracInStrategy


def _make_dummy_data(num_nodes=100, num_features=16, num_edges=300):
    """创建一个用于测试的 dummy PyG Data 对象。"""
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))
    y = torch.randint(0, 7, (num_nodes,))
    return Data(x=x, edge_index=edge_index, y=y)


def _make_train_masked_star():
    """A tiny graph where node 9 is important but not in train_mask."""
    x = torch.randn(10, 16)
    y = torch.randint(0, 7, (10,))
    train_mask = torch.zeros(10, dtype=torch.bool)
    train_mask[:5] = True
    edge_index = torch.tensor([
        [9, 9, 9, 9, 9, 0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4, 1, 2, 3, 4, 0],
    ])
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)


def _assert_selected_from_train_mask(data, result):
    train_nodes = set(data.train_mask.nonzero(as_tuple=False).view(-1).tolist())
    assert set(result.tolist()).issubset(train_nodes)


class TestRandomStrategy:
    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data()
        strategy = RandomStrategy(args={})
        k = 20
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复节点"""
        data = _make_dummy_data()
        strategy = RandomStrategy(args={})
        k = 50
        result = strategy.select_nodes(data, model=None, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """所有索引 ∈ [0, N)"""
        data = _make_dummy_data(num_nodes=80)
        strategy = RandomStrategy(args={})
        k = 30
        result = strategy.select_nodes(data, model=None, k=k)
        assert (result >= 0).all() and (result < 80).all()

    def test_ratio_interface(self):
        """select_nodes_by_ratio 与手动算 k 结果长度一致"""
        data = _make_dummy_data(num_nodes=200)
        strategy = RandomStrategy(args={})
        ratio = 0.1
        result = strategy.select_nodes_by_ratio(data, model=None, ratio=ratio)
        expected_k = int(200 * ratio)
        assert result.shape == (expected_k,)

    def test_selects_only_train_nodes_when_train_mask_present(self):
        """Random baseline should match unlearning request semantics: train nodes only."""
        data = _make_train_masked_star()
        strategy = RandomStrategy(args={})
        torch.manual_seed(0)

        result = strategy.select_nodes(data, model=None, k=5)

        _assert_selected_from_train_mask(data, result)

    def test_ratio_uses_train_mask_count_when_present(self):
        data = _make_train_masked_star()
        strategy = RandomStrategy(args={})

        result = strategy.select_nodes_by_ratio(data, model=None, ratio=0.4)

        assert result.shape == (2,)


class TestDegreeStrategy:
    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data()
        strategy = DegreeStrategy(args={})
        k = 20
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复节点"""
        data = _make_dummy_data()
        strategy = DegreeStrategy(args={})
        k = 50
        result = strategy.select_nodes(data, model=None, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """所有索引 ∈ [0, N)"""
        data = _make_dummy_data(num_nodes=80)
        strategy = DegreeStrategy(args={})
        k = 30
        result = strategy.select_nodes(data, model=None, k=k)
        assert (result >= 0).all() and (result < 80).all()

    def test_ratio_interface(self):
        """select_nodes_by_ratio 与手动算 k 结果一致"""
        data = _make_dummy_data(num_nodes=200)
        strategy = DegreeStrategy(args={})
        ratio = 0.1
        result = strategy.select_nodes_by_ratio(data, model=None, ratio=ratio)
        expected_k = int(200 * ratio)
        assert result.shape == (expected_k,)

    def test_deterministic(self):
        """DegreeStrategy 是确定性的：两次调用结果相同"""
        data = _make_dummy_data()
        strategy = DegreeStrategy(args={})
        k = 20
        result1 = strategy.select_nodes(data, model=None, k=k)
        result2 = strategy.select_nodes(data, model=None, k=k)
        assert torch.equal(result1, result2)

    def test_highest_degree_selected(self):
        """验证选中的确实是度数最高的节点"""
        # 构造一个简单图：节点0有3条边，节点1有2条边，其余1条
        edge_index = torch.tensor([
            [0, 0, 0, 1, 1, 2, 3, 4],  # source
            [1, 2, 3, 2, 4, 5, 6, 5]   # target
        ])
        data = Data(x=torch.randn(7, 16), edge_index=edge_index, y=torch.randint(0, 7, (7,)))

        strategy = DegreeStrategy(args={})
        k = 2
        result = strategy.select_nodes(data, model=None, k=k)

        # 度数：0=3, 1=2, 2=2, 3=1, 4=1, 5=1, 6=1
        # top-2 应该是节点 0 和 (1 或 2)
        assert 0 in result
        assert all(r in [0, 1, 2] for r in result.tolist())

    def test_selects_only_train_nodes_when_train_mask_present(self):
        data = _make_train_masked_star()
        strategy = DegreeStrategy(args={})

        result = strategy.select_nodes(data, model=None, k=3)

        _assert_selected_from_train_mask(data, result)


class TestPageRankStrategy:
    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data()
        strategy = PageRankStrategy(args={})
        k = 20
        result = strategy.select_nodes(data, model=None, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复节点"""
        data = _make_dummy_data()
        strategy = PageRankStrategy(args={})
        k = 50
        result = strategy.select_nodes(data, model=None, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """所有索引 ∈ [0, N)"""
        data = _make_dummy_data(num_nodes=80)
        strategy = PageRankStrategy(args={})
        k = 30
        result = strategy.select_nodes(data, model=None, k=k)
        assert (result >= 0).all() and (result < 80).all()

    def test_ratio_interface(self):
        """select_nodes_by_ratio 与手动算 k 结果一致"""
        data = _make_dummy_data(num_nodes=200)
        strategy = PageRankStrategy(args={})
        ratio = 0.1
        result = strategy.select_nodes_by_ratio(data, model=None, ratio=ratio)
        expected_k = int(200 * ratio)
        assert result.shape == (expected_k,)

    def test_deterministic(self):
        """PageRankStrategy 是确定性的：两次调用结果相同"""
        data = _make_dummy_data()
        strategy = PageRankStrategy(args={})
        k = 20
        result1 = strategy.select_nodes(data, model=None, k=k)
        result2 = strategy.select_nodes(data, model=None, k=k)
        assert torch.equal(result1, result2)

    def test_selects_only_train_nodes_when_train_mask_present(self):
        data = _make_train_masked_star()
        strategy = PageRankStrategy(args={})

        result = strategy.select_nodes(data, model=None, k=3)

        _assert_selected_from_train_mask(data, result)


class TestTracInStrategy:
    """Tests for TracInStrategy (Step 5)."""

    def _make_dummy_model(self, num_features=16, num_classes=7):
        """创建一个简单的 GNN 模型用于测试。"""
        import torch.nn as nn
        import torch.nn.functional as F

        class DummyGNN(nn.Module):
            def __init__(self, in_channels, out_channels):
                super().__init__()
                self.lin = nn.Linear(in_channels, out_channels)

            def forward(self, x, edge_index=None):
                return self.lin(x)

        return DummyGNN(num_features, num_classes)

    def test_output_shape(self):
        """返回恰好 k 个节点"""
        data = _make_dummy_data(num_nodes=100, num_features=16)
        model = self._make_dummy_model(num_features=16, num_classes=7)
        strategy = TracInStrategy(args={})
        k = 20
        result = strategy.select_nodes(data, model=model, k=k)
        assert result.shape == (k,)

    def test_no_duplicates(self):
        """无重复节点"""
        data = _make_dummy_data(num_nodes=100, num_features=16)
        model = self._make_dummy_model(num_features=16, num_classes=7)
        strategy = TracInStrategy(args={})
        k = 50
        result = strategy.select_nodes(data, model=model, k=k)
        assert len(result.unique()) == k

    def test_valid_indices(self):
        """所有索引 ∈ [0, N)"""
        data = _make_dummy_data(num_nodes=80, num_features=16)
        model = self._make_dummy_model(num_features=16, num_classes=7)
        strategy = TracInStrategy(args={})
        k = 30
        result = strategy.select_nodes(data, model=model, k=k)
        assert (result >= 0).all() and (result < 80).all()

    def test_ratio_interface(self):
        """select_nodes_by_ratio 与手动算 k 结果长度一致"""
        data = _make_dummy_data(num_nodes=200, num_features=16)
        model = self._make_dummy_model(num_features=16, num_classes=7)
        strategy = TracInStrategy(args={})
        ratio = 0.1
        result = strategy.select_nodes_by_ratio(data, model=model, ratio=ratio)
        expected_k = int(200 * ratio)
        assert result.shape == (expected_k,)

    def test_deterministic(self):
        """TracInStrategy 是确定性的：两次调用结果相同"""
        data = _make_dummy_data(num_nodes=100, num_features=16)
        model = self._make_dummy_model(num_features=16, num_classes=7)
        strategy = TracInStrategy(args={})
        k = 20
        result1 = strategy.select_nodes(data, model=model, k=k)
        result2 = strategy.select_nodes(data, model=model, k=k)
        assert torch.equal(result1, result2)
