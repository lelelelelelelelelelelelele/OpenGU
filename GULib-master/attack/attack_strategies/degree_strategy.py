import torch
from torch import Tensor
from torch_geometric.data import Data
from torch_geometric.utils import degree

from .base_strategy import BaseStrategy


class DegreeStrategy(BaseStrategy):
    """按节点度数排序，选择度数最高的 k 个节点。"""

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        edge_index = data.edge_index
        num_nodes = data.num_nodes

        # 计算每个节点的度数（无向图：计算入度即可，因为每条边会被存两次）
        deg = degree(edge_index[0], num_nodes=num_nodes)
        candidates = self.candidate_nodes(data, device=deg.device)
        k = self._validate_k(k, candidates)

        # 选度数最高的 k 个节点
        _, topk_indices = torch.topk(deg[candidates], k)
        return candidates[topk_indices].cpu()
