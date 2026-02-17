import torch
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy


class RandomStrategy(BaseStrategy):
    """随机采样 k 个节点。"""

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        return torch.randperm(data.num_nodes)[:k]
