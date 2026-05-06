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
        hybrid_alpha: Weight for IF scores in fusion; (1-α) for IM scores
            (default: 0.5). Falls back to legacy `alpha` only if `hybrid_alpha`
            is not set, but `alpha` is also used by GNNDelete/CGU as a loss
            coefficient — sweeping fusion α with the legacy field would also
            sweep the unlearning loss, so use `hybrid_alpha` for new runs.
        candidate_fraction: shared with IM. If <1.0, the candidate pool is
            pruned by degree before computing IF/IM scores, so the fusion
            uses the SAME pruned set IM-only would use.
    """

    requires_trained_model = True

    def __init__(self, args: dict):
        super().__init__(args)
        self.fusion_method = args.get('fusion_method', 'rank')
        # `hybrid_alpha` overrides legacy `alpha`. We only fall through to
        # `alpha` (default 0.5) when `hybrid_alpha` is missing, to avoid
        # silent collision with GNNDelete/CGU loss-alpha sweeps.
        hybrid_alpha = args.get('hybrid_alpha')
        if hybrid_alpha is None:
            hybrid_alpha = args.get('alpha', 0.5)
        self.alpha = float(hybrid_alpha)
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

        # Shared candidate set so IF and IM scores have aligned shapes.
        candidates = self.candidate_nodes(data, device=device)
        k = self._validate_k(k, candidates)

        # Apply IM's degree-based pruning to the shared candidate set when
        # candidate_fraction < 1.0. Both IF and IM then operate on the
        # pruned set, keeping fusion well-defined.
        candidate_list = candidates.tolist()
        if self.im.candidate_fraction < 1.0 and len(candidate_list) > k:
            candidate_list = self.im._prune_candidates_by_degree(
                data.edge_index, data.num_nodes, candidate_list,
                self.im.candidate_fraction, k,
            )
            candidates = torch.tensor(candidate_list, dtype=torch.long, device=device)

        # Compute IF scores via TracIn (cache-aware: re-runs only on miss).
        if_scores = self.tracin.compute_scores(model, data, candidates)

        # Compute IM scores via initial marginal gains (cache-aware: pure topology).
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
