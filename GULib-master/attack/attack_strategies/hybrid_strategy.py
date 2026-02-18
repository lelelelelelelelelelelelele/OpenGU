import torch
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy
from .tracin_strategy import TracInStrategy
from .im_strategy import IMStrategy


class HybridStrategy(BaseStrategy):
    """
    Hybrid strategy combining TracIn (proxy-IF) and Influence Maximization scores.

    Fuses IF scores (gradient-based node importance) with IM scores (topological
    spread influence) to select nodes that are both individually influential and
    well-positioned for cascading impact.

    Parameters (via args dict):
        fusion_method: 'rank' (default) or 'linear'
        alpha: Weight for IF scores; (1-alpha) for IM scores (default: 0.5)
        + all TracIn and IM parameters
    """

    def __init__(self, args: dict):
        super().__init__(args)
        self.fusion_method = args.get('fusion_method', 'rank')
        self.alpha = args.get('alpha', 0.5)
        self.tracin = TracInStrategy(args)
        self.im = IMStrategy(args)

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        """Select k nodes using fused IF + IM scores."""
        model.eval()
        device = self.tracin.device
        model.to(device)
        data = data.to(device)

        # Determine candidates (same logic as TracIn)
        if hasattr(data, 'train_mask') and data.train_mask is not None:
            candidates = data.train_mask.nonzero(as_tuple=False).squeeze(-1).to(device)
        else:
            candidates = torch.arange(data.num_nodes, device=device)

        candidate_list = candidates.tolist()

        # Compute IF scores via TracIn
        if_scores = self.tracin._compute_tracin_scores(model, data, candidates)

        # Compute IM scores (initial marginal gains)
        im_scores = self.im.compute_initial_marginal_gains(
            data.edge_index, data.num_nodes, candidate_list
        )
        im_scores = im_scores.to(device)

        # Fuse scores
        fused = self.fuse_scores(if_scores, im_scores, self.fusion_method, self.alpha)

        # Select top-k
        _, topk_indices = torch.topk(fused, k)
        selected = candidates[topk_indices]

        return selected.cpu()

    @staticmethod
    def fuse_scores(if_scores, im_scores, method='rank', alpha=0.5):
        """
        Fuse IF and IM scores.

        Args:
            if_scores: [N] tensor of IF scores
            im_scores: [N] tensor of IM scores
            method: 'rank' or 'linear'
            alpha: Weight for IF; (1-alpha) for IM

        Returns:
            fused: [N] tensor of fused scores
        """
        # Clean NaN/Inf
        if_scores = torch.nan_to_num(if_scores, nan=0.0, posinf=0.0, neginf=0.0)
        im_scores = torch.nan_to_num(im_scores, nan=0.0, posinf=0.0, neginf=0.0)

        if method == 'linear':
            if_norm = HybridStrategy._min_max_normalize(if_scores)
            im_norm = HybridStrategy._min_max_normalize(im_scores)
            return alpha * if_norm + (1 - alpha) * im_norm
        elif method == 'rank':
            if_rank = HybridStrategy._rank_normalize(if_scores)
            im_rank = HybridStrategy._rank_normalize(im_scores)
            return alpha * if_rank + (1 - alpha) * im_rank
        else:
            raise ValueError(f"Unknown fusion method: {method}")

    @staticmethod
    def _min_max_normalize(scores):
        """Min-max normalize scores to [0, 1]. Returns zeros if all scores are equal."""
        smin = scores.min()
        smax = scores.max()
        denom = smax - smin
        if denom == 0:
            return torch.zeros_like(scores)
        return (scores - smin) / denom

    @staticmethod
    def _rank_normalize(scores):
        """Rank-percentile normalize. Returns [1.0] for single element."""
        n = scores.numel()
        if n <= 1:
            return torch.ones_like(scores)
        ranks = scores.argsort().argsort().float()
        return ranks / (n - 1)
