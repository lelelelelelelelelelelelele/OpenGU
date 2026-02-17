"""Unit tests for attack strategies (Step 1: RandomStrategy)."""

import torch
from torch_geometric.data import Data

from attack.attack_strategies import RandomStrategy


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
