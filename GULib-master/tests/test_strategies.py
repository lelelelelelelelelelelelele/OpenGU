"""Unit tests for attack strategies (Steps 1-3)."""

import torch
from torch_geometric.data import Data

from attack.attack_strategies import RandomStrategy, DegreeStrategy, PageRankStrategy


def _make_dummy_data(num_nodes=100, num_features=16, num_edges=300):
    """创建一个用于测试的 dummy PyG Data 对象。"""
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))
    y = torch.randint(0, 7, (num_nodes,))
    return Data(x=x, edge_index=edge_index, y=y)


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
