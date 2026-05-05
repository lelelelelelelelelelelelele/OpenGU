import torch
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy


class TracInStrategy(BaseStrategy):
    """
    TracIn (Tracing Influence) strategy for node selection.

    TracIn approximates influence functions using gradient similarity, providing
    a computationally efficient alternative to full Hessian-based IF calculation.

    The TracIn score for a node is computed as the sum of negative gradient dot
    products with all other nodes. Higher scores indicate more influential nodes
    that, when unlearned, have greater impact on model performance.

    Reference: "Estimating Training Data Influence by Tracing Gradient Descent"
    (Pruthi et al., NeurIPS 2020)
    """

    def __init__(self, args: dict):
        """
        Initialize TracIn strategy.

        Args:
            args: Configuration dictionary containing:
                - loss: Loss function type ('cross_entropy' or 'mse'), default 'cross_entropy'
                - device: torch device (auto-detected if not provided)
        """
        super().__init__(args)
        self.loss_type = args.get('loss', 'cross_entropy')
        self.device = args.get('device', torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        """
        Select k nodes with highest TracIn influence scores.

        Args:
            data: PyG Data object with edge_index, x, y
            model: Trained GNN model
            k: Number of nodes to select

        Returns:
            node_indices: [k] tensor of selected node indices
        """
        model.eval()
        model.to(self.device)
        data = data.to(self.device)

        # Limit candidates to training nodes (unlearning only selects from train set)
        if hasattr(data, 'train_mask') and data.train_mask is not None:
            candidates = data.train_mask.nonzero(as_tuple=False).squeeze(-1).to(self.device)
        else:
            candidates = torch.arange(data.num_nodes, device=self.device)

        # Compute TracIn scores
        scores = self._compute_tracin_scores(model, data, candidates)

        # Select top-k nodes with highest scores
        _, topk_indices = torch.topk(scores, k)

        # Map indices back to actual node IDs
        selected_nodes = candidates[topk_indices]

        return selected_nodes.cpu()

    def _compute_tracin_scores(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
    ) -> Tensor:
        """
        Compute TracIn scores for all candidate nodes.

        The TracIn score for node i is:
            score_i = -sum_j (grad_i · grad_j)

        Higher scores indicate more influential nodes.

        Args:
            model: Trained GNN model
            data: PyG Data object
            candidates: Tensor of candidate node indices

        Returns:
            scores: [num_candidates] tensor of TracIn scores
        """
        # Single full-graph forward; reused across every per-candidate backward
        # via retain_graph=True. Previously the forward was repeated inside the
        # candidate loop (90K times on arxiv), which dominated runtime.
        if hasattr(model, 'forward') and 'edge_index' in model.forward.__code__.co_varnames:
            out = model(data.x, data.edge_index)
        else:
            out = model(data.x)

        params = [p for p in model.parameters() if p.requires_grad]
        n_cand = candidates.shape[0]

        grads = []
        for i, node in enumerate(candidates):
            node_idx = node.item() if isinstance(node, Tensor) else node
            loss = self._compute_node_loss(out, data.y, node_idx)
            # Final iteration releases the graph; earlier iterations retain it
            retain = (i < n_cand - 1)
            grad_tuple = torch.autograd.grad(
                loss, params, retain_graph=retain, create_graph=False
            )
            grads.append(torch.cat([g.flatten() for g in grad_tuple]))

        # G: [N, d] matrix of per-node gradients
        G = torch.stack(grads)  # [num_candidates, num_params]

        # TracIn score_i = -sum_j (grad_i · grad_j) = -(G @ G^T).sum(dim=1)[i]
        # Equivalent: scores = -(G @ G^T @ 1) = -(G @ (G^T @ 1)) for memory efficiency
        col_sum = G.sum(dim=0)  # [d]
        scores = -(G @ col_sum)  # [num_candidates]

        return scores

    def _compute_node_loss(
        self,
        out: Tensor,
        y: Tensor,
        node_idx: int,
    ) -> Tensor:
        """
        Compute loss for a single node.

        Args:
            out: Model output logits [num_nodes, num_classes]
            y: Ground truth labels [num_nodes]
            node_idx: Index of the node

        Returns:
            loss: Scalar loss tensor
        """
        if self.loss_type == 'cross_entropy':
            return F.cross_entropy(out[node_idx:node_idx+1], y[node_idx:node_idx+1])
        elif self.loss_type == 'mse':
            return F.mse_loss(out[node_idx], y[node_idx].float())
        else:
            raise ValueError(f"Unsupported loss type: {self.loss_type}")
