from abc import ABC, abstractmethod
import torch
from torch import Tensor
from torch_geometric.data import Data


class BaseStrategy(ABC):
    def __init__(self, args: dict):
        self.args = args

    @abstractmethod
    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        """
        选择 k 个节点用于遗忘。

        Args:
            data: PyG Data 对象（含 edge_index, x, y, masks）
            model: 已训练的 GNN 模型（部分策略不使用）
            k: 选择节点数

        Returns:
            node_indices: [k] 选中的节点索引
        """
        pass

    def select_nodes_by_ratio(
        self,
        data: Data,
        model: torch.nn.Module,
        ratio: float,
    ) -> Tensor:
        """按比例选择节点。ratio ∈ (0, 1)。"""
        k = int(data.num_nodes * ratio)
        return self.select_nodes(data, model, k)
