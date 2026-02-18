import random
import heapq
import torch
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy


class IMStrategy(BaseStrategy):
    """
    Influence Maximization strategy using CELF optimization.

    Selects nodes that maximize information spread under the Independent Cascade
    (IC) model. This is a pure topology-based method that does not use the GNN
    model. CELF (Cost-Effective Lazy Forward) exploits submodularity to avoid
    redundant spread estimations.

    Parameters (via args dict):
        propagation_prob: IC propagation probability per edge (default: 0.1)
        mc_rounds: Number of Monte Carlo simulations for spread estimation (default: 100)
    """

    def __init__(self, args: dict):
        super().__init__(args)
        self.propagation_prob = args.get('propagation_prob', 0.1)
        self.mc_rounds = args.get('mc_rounds', 100)

    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int,
    ) -> Tensor:
        """Select k nodes with highest influence spread via CELF."""
        # Limit candidates to training nodes
        if hasattr(data, 'train_mask') and data.train_mask is not None:
            candidate_set = data.train_mask.nonzero(as_tuple=False).squeeze(-1).tolist()
        else:
            candidate_set = list(range(data.num_nodes))

        selected, _ = self.compute_im_celf(
            data.edge_index, data.num_nodes, k, candidate_set
        )
        return torch.tensor(selected, dtype=torch.long)

    def compute_im_celf(self, edge_index, num_nodes, k, candidate_set):
        """
        CELF-optimized greedy Influence Maximization.

        Args:
            edge_index: [2, E] edge index tensor
            num_nodes: Total number of nodes in the graph
            k: Number of seed nodes to select
            candidate_set: List of candidate node indices

        Returns:
            (selected_nodes, scores): List of k selected node indices and their
                marginal gain scores as a tensor of length k.
        """
        random.seed(2024)
        adj = self._build_adjacency(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        # Step 1: Compute initial marginal gains for all candidates
        # Use a max-heap (negate values since heapq is a min-heap)
        heap = []
        for node in candidate_set:
            spread = self._estimate_spread(adj, {node}, prob, num_nodes, mc)
            heapq.heappush(heap, (-spread, 0, node))  # (neg_gain, last_updated, node)

        selected = []
        selected_set = set()
        scores = []
        current_spread = 0.0

        for i in range(k):
            while True:
                neg_gain, last_updated, node = heapq.heappop(heap)

                if last_updated == i:
                    # This node's marginal gain was computed in this round
                    selected.append(node)
                    selected_set.add(node)
                    scores.append(-neg_gain)
                    current_spread += (-neg_gain)
                    break
                else:
                    # Recompute marginal gain
                    new_spread = self._estimate_spread(
                        adj, selected_set | {node}, prob, num_nodes, mc
                    )
                    marginal = new_spread - current_spread
                    heapq.heappush(heap, (-marginal, i, node))

        return selected, torch.tensor(scores)

    def compute_initial_marginal_gains(self, edge_index, num_nodes, candidate_set):
        """
        Compute single-node spread for each candidate (CELF step 1 only).

        This is used by HybridStrategy to get IM scores without running full CELF.

        Args:
            edge_index: [2, E] edge index tensor
            num_nodes: Total number of nodes
            candidate_set: List of candidate node indices

        Returns:
            scores: [len(candidate_set)] tensor of spread scores
        """
        random.seed(2024)
        adj = self._build_adjacency(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        scores = []
        for node in candidate_set:
            spread = self._estimate_spread(adj, {node}, prob, num_nodes, mc)
            scores.append(spread)

        return torch.tensor(scores)

    def _build_adjacency(self, edge_index, num_nodes):
        """Build adjacency list from edge_index."""
        adj = [[] for _ in range(num_nodes)]
        src = edge_index[0].tolist()
        dst = edge_index[1].tolist()
        for s, d in zip(src, dst):
            adj[s].append(d)
        return adj

    def _simulate_spread(self, adj, seed_set, prob, num_nodes):
        """
        Single IC simulation from seed_set.

        Returns the number of activated nodes.
        """
        activated = set(seed_set)
        frontier = list(seed_set)

        while frontier:
            new_frontier = []
            for node in frontier:
                for neighbor in adj[node]:
                    if neighbor not in activated:
                        if random.random() < prob:
                            activated.add(neighbor)
                            new_frontier.append(neighbor)
            frontier = new_frontier

        return float(len(activated))

    def _estimate_spread(self, adj, seed_set, prob, num_nodes, mc_rounds):
        """
        Estimate expected spread via Monte Carlo simulations.

        Returns the average number of activated nodes over mc_rounds simulations.
        """
        total = 0.0
        for _ in range(mc_rounds):
            total += self._simulate_spread(adj, seed_set, prob, num_nodes)
        return total / mc_rounds
