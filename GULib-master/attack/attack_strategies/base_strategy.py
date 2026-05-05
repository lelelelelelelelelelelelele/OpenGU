from abc import ABC, abstractmethod
import torch
from torch import Tensor
from torch_geometric.data import Data


class BaseStrategy(ABC):
    # Whether select_nodes needs the `model` argument to be a trained GNN
    # rather than a random-init one. AttackPipeline reads this to decide
    # whether to run base-model training before calling select_nodes.
    # Subclasses that derive scores from gradients/logits override to True.
    requires_trained_model = False

    def __init__(self, args: dict):
        self.args = args

    def candidate_nodes(self, data: Data, device=None) -> Tensor:
        """Return nodes eligible for unlearning; train_mask wins when present."""
        train_mask = getattr(data, "train_mask", None)
        if train_mask is not None:
            if train_mask.dim() > 1:
                train_mask = train_mask.squeeze(-1)
            candidates = train_mask.nonzero(as_tuple=False).view(-1).long()
            if candidates.numel() > 0:
                return candidates.to(device) if device is not None else candidates

        train_indices = getattr(data, "train_indices", None)
        if train_indices is not None:
            candidates = torch.as_tensor(train_indices, dtype=torch.long)
            if candidates.numel() > 0:
                return candidates.to(device) if device is not None else candidates

        return torch.arange(data.num_nodes, dtype=torch.long, device=device)

    @staticmethod
    def _validate_k(k: int, candidates: Tensor) -> int:
        k = int(k)
        if k < 0:
            raise ValueError(f"k must be non-negative, got {k}")
        if k > int(candidates.numel()):
            raise ValueError(
                f"k={k} exceeds available candidate nodes ({int(candidates.numel())})"
            )
        return k

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
        k = int(self.candidate_nodes(data).numel() * ratio)
        return self.select_nodes(data, model, k)
