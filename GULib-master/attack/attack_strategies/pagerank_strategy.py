import torch
import networkx as nx
from torch import Tensor
from torch_geometric.data import Data
from torch_geometric.utils import to_networkx

from .base_strategy import BaseStrategy


class PageRankStrategy(BaseStrategy):
    """按 PageRank 值排序，选择 PageRank 最高的 k 个节点。

    适用于识别网络中“重要”的节点，作为攻击目标。
    """

    def __init__(self, args: dict):
        super().__init__(args)
        self.alpha = args.get("pagerank_alpha", 0.85)

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        # 转换为 NetworkX 图
        G = to_networkx(data, to_undirected=True)

        # 计算 PageRank
        pr_scores = nx.pagerank(G, alpha=self.alpha)

        # 转换为 tensor 并按分数排序
        scores = torch.tensor([pr_scores[i] for i in range(data.num_nodes)], dtype=torch.float)
        _, topk_indices = torch.topk(scores, k)

        return topk_indices
