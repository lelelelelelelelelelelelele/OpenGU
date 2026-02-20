import random
import heapq
import numpy as np
import torch
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy

# Numba import guard
try:
    import numba
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False


# ---------------------------------------------------------------------------
# Numba-accelerated kernels (module-level for caching)
# ---------------------------------------------------------------------------
if HAS_NUMBA:
    @numba.njit(inline='always')
    def _splitmix64(state):
        """Deterministic splitmix64 RNG step."""
        state += np.uint64(0x9E3779B97F4A7C15)
        z = state
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
        return state, z

    @numba.njit(inline='always')
    def _rand_float(state):
        """Return (new_state, uniform float in [0, 1))."""
        state, z = _splitmix64(state)
        return state, (z >> np.uint64(11)) * np.float64(5.421010862427522e-20)

    @numba.njit(cache=True)
    def _simulate_spread_numba(indptr, indices, seed_array, prob, num_nodes,
                               round_seed, visited, stamp, frontier):
        """Single IC simulation using stamp-visited BFS.

        Args:
            indptr, indices: CSR adjacency (int32).
            seed_array: int32 array of seed node IDs.
            prob: propagation probability.
            num_nodes: total node count.
            round_seed: deterministic seed for this round's RNG.
            visited: int32 array (reused across rounds), marks visited with stamp.
            stamp: current stamp value (>0).
            frontier: int32 work buffer (pre-allocated, size num_nodes).

        Returns:
            Number of activated nodes (float64).
        """
        rng_state = np.uint64(round_seed)
        n_frontier = 0
        count = 0

        # Seed nodes
        for i in range(seed_array.shape[0]):
            node = seed_array[i]
            if visited[node] != stamp:
                visited[node] = stamp
                frontier[n_frontier] = node
                n_frontier += 1
                count += 1

        head = 0
        while head < n_frontier:
            node = frontier[head]
            head += 1
            start = indptr[node]
            end = indptr[node + 1]
            for j in range(start, end):
                neighbor = indices[j]
                if visited[neighbor] != stamp:
                    rng_state, r = _rand_float(rng_state)
                    if r < prob:
                        visited[neighbor] = stamp
                        frontier[n_frontier] = neighbor
                        n_frontier += 1
                        count += 1
                else:
                    # Still advance RNG for determinism
                    rng_state, _ = _rand_float(rng_state)

        return np.float64(count)

    @numba.njit(cache=True)
    def _estimate_spread_numba(indptr, indices, seed_array, prob, num_nodes,
                               mc_rounds, base_seed):
        """Estimate expected spread via MC simulations (numba fast path).

        Allocates visited/frontier once and reuses across rounds via stamp trick.
        """
        visited = np.zeros(num_nodes, dtype=np.int32)
        frontier = np.empty(num_nodes, dtype=np.int32)
        total = np.float64(0.0)
        stamp = np.int32(0)

        for r in range(mc_rounds):
            stamp += np.int32(1)
            # Overflow protection (defensive; mc_rounds << 2e9 in practice)
            if stamp >= np.int32(2_000_000_000):
                visited[:] = np.int32(0)
                stamp = np.int32(1)
            total += _simulate_spread_numba(indptr, indices, seed_array, prob,
                                            num_nodes, base_seed + r, visited,
                                            stamp, frontier)

        return total / np.float64(mc_rounds)


class IMStrategy(BaseStrategy):
    """
    Influence Maximization strategy using CELF optimization.

    Selects nodes that maximize information spread under the Independent Cascade
    (IC) model. This is a pure topology-based method that does not use the GNN
    model. CELF (Cost-Effective Lazy Forward) exploits submodularity to avoid
    redundant spread estimations.

    When numba is available, MC simulations are JIT-compiled for 10-50x speedup.
    Falls back to pure Python automatically if numba is not installed.

    Parameters (via args dict):
        propagation_prob: IC propagation probability per edge (default: 0.1)
        mc_rounds: Number of Monte Carlo simulations for spread estimation (default: 100)
        candidate_fraction: Fraction of candidates to keep (by degree), for large graphs (default: 1.0)
    """

    def __init__(self, args: dict):
        super().__init__(args)
        self.propagation_prob = args.get('propagation_prob', 0.1)
        self.mc_rounds = args.get('mc_rounds', 100)
        self.candidate_fraction = args.get('candidate_fraction', 1.0)
        seed_value = args.get('random_seed', args.get('seed', 2024))
        try:
            self.random_seed = int(seed_value)
        except (TypeError, ValueError):
            self.random_seed = 2024

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
        # Apply candidate_fraction pruning by degree
        if self.candidate_fraction < 1.0 and len(candidate_set) > k:
            candidate_set = self._prune_candidates_by_degree(
                edge_index, num_nodes, candidate_set, self.candidate_fraction, k
            )

        if HAS_NUMBA:
            return self._compute_im_celf_numba(edge_index, num_nodes, k, candidate_set)
        else:
            return self._compute_im_celf_python(edge_index, num_nodes, k, candidate_set)

    def _compute_im_celf_python(self, edge_index, num_nodes, k, candidate_set):
        """Pure Python CELF implementation (fallback)."""
        random.seed(self.random_seed)
        adj = self._build_adjacency_python(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        # Step 1: Compute initial marginal gains for all candidates
        heap = []
        for node in candidate_set:
            spread = self._estimate_spread_python(adj, {node}, prob, num_nodes, mc)
            heapq.heappush(heap, (-spread, 0, node))

        selected = []
        selected_set = set()
        scores = []
        current_spread = 0.0

        for i in range(k):
            while True:
                neg_gain, last_updated, node = heapq.heappop(heap)

                if last_updated == i:
                    selected.append(node)
                    selected_set.add(node)
                    scores.append(-neg_gain)
                    current_spread += (-neg_gain)
                    break
                else:
                    new_spread = self._estimate_spread_python(
                        adj, selected_set | {node}, prob, num_nodes, mc
                    )
                    marginal = new_spread - current_spread
                    heapq.heappush(heap, (-marginal, i, node))

        return selected, torch.tensor(scores)

    def _compute_im_celf_numba(self, edge_index, num_nodes, k, candidate_set):
        """Numba-accelerated CELF implementation."""
        indptr, indices = self._build_adjacency_csr(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        # Step 1: Compute initial marginal gains for all candidates
        heap = []
        for node in candidate_set:
            seed_arr = np.array([node], dtype=np.int32)
            base_seed = self.random_seed * 10000 + node % 10000
            spread = _estimate_spread_numba(indptr, indices, seed_arr, prob,
                                            num_nodes, mc, base_seed)
            heapq.heappush(heap, (-spread, 0, node))

        selected = []
        selected_set_list = []
        scores = []
        current_spread = 0.0

        for i in range(k):
            while True:
                neg_gain, last_updated, node = heapq.heappop(heap)

                if last_updated == i:
                    selected.append(node)
                    selected_set_list.append(node)
                    scores.append(-neg_gain)
                    current_spread += (-neg_gain)
                    break
                else:
                    seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                    base_seed = self.random_seed * 10000 + int(np.sum(np.sort(seed_arr))) % 10000
                    new_spread = _estimate_spread_numba(
                        indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
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
        if HAS_NUMBA:
            return self._compute_initial_gains_numba(edge_index, num_nodes, candidate_set)
        else:
            return self._compute_initial_gains_python(edge_index, num_nodes, candidate_set)

    def _compute_initial_gains_python(self, edge_index, num_nodes, candidate_set):
        """Pure Python initial gains computation (fallback)."""
        random.seed(self.random_seed)
        adj = self._build_adjacency_python(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        scores = []
        for node in candidate_set:
            spread = self._estimate_spread_python(adj, {node}, prob, num_nodes, mc)
            scores.append(spread)

        return torch.tensor(scores)

    def _compute_initial_gains_numba(self, edge_index, num_nodes, candidate_set):
        """Numba-accelerated initial gains computation."""
        indptr, indices = self._build_adjacency_csr(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds

        scores = []
        for node in candidate_set:
            seed_arr = np.array([node], dtype=np.int32)
            base_seed = self.random_seed * 10000 + node % 10000
            spread = _estimate_spread_numba(indptr, indices, seed_arr, prob,
                                            num_nodes, mc, base_seed)
            scores.append(spread)

        return torch.tensor(scores)

    # -------------------------------------------------------------------
    # Adjacency builders
    # -------------------------------------------------------------------
    def _build_adjacency_python(self, edge_index, num_nodes):
        """Build adjacency list from edge_index (pure Python)."""
        adj = [[] for _ in range(num_nodes)]
        src = edge_index[0].tolist()
        dst = edge_index[1].tolist()
        for s, d in zip(src, dst):
            adj[s].append(d)
        return adj

    def _build_adjacency_csr(self, edge_index, num_nodes):
        """Build sorted, deduplicated CSR adjacency from edge_index.

        Returns:
            (indptr, indices): numpy int32 arrays in CSR format.
        """
        src = edge_index[0].cpu().numpy().astype(np.int64)
        dst = edge_index[1].cpu().numpy().astype(np.int64)

        # Sort by (src, dst) for deterministic traversal order
        order = np.lexsort((dst, src))
        src = src[order]
        dst = dst[order]

        # Deduplicate (coalesce)
        if len(src) > 0:
            mask = np.ones(len(src), dtype=np.bool_)
            mask[1:] = (src[1:] != src[:-1]) | (dst[1:] != dst[:-1])
            src = src[mask]
            dst = dst[mask]

        # Build CSR
        indptr = np.zeros(num_nodes + 1, dtype=np.int32)
        for s in src:
            indptr[s + 1] += 1
        np.cumsum(indptr, out=indptr)
        indices = dst.astype(np.int32)

        return indptr, indices

    # -------------------------------------------------------------------
    # Pure Python MC simulation (fallback)
    # -------------------------------------------------------------------
    def _simulate_spread(self, adj, seed_set, prob, num_nodes):
        """Single IC simulation from seed_set (pure Python)."""
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

    def _estimate_spread_python(self, adj, seed_set, prob, num_nodes, mc_rounds):
        """Estimate expected spread via MC simulations (pure Python)."""
        total = 0.0
        for _ in range(mc_rounds):
            total += self._simulate_spread(adj, seed_set, prob, num_nodes)
        return total / mc_rounds

    # Keep old names as aliases for backward compatibility in tests
    _build_adjacency = _build_adjacency_python
    _estimate_spread = _estimate_spread_python

    # -------------------------------------------------------------------
    # Candidate pruning
    # -------------------------------------------------------------------
    def _prune_candidates_by_degree(self, edge_index, num_nodes, candidate_set,
                                    fraction, min_k):
        """Prune candidate set to top-degree fraction, keeping at least min_k."""
        src = edge_index[0]
        device = src.device
        # Compute degree for candidates only
        degrees = torch.zeros(num_nodes, dtype=torch.long, device=device)
        degrees.scatter_add_(0, src, torch.ones_like(src))

        cand_tensor = torch.tensor(candidate_set, dtype=torch.long, device=device)
        cand_degrees = degrees[cand_tensor]

        n_keep = max(int(len(candidate_set) * fraction), min_k)
        n_keep = min(n_keep, len(candidate_set))

        _, top_idx = cand_degrees.topk(n_keep)
        return cand_tensor[top_idx].tolist()
