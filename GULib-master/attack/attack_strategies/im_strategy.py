import random
import heapq
import numpy as np
import torch
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy
from ..score_cache import ScoreCache, graph_fingerprint

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
        # Use 53 random bits to match float64 mantissa precision.
        mantissa53 = z & np.uint64(0x1FFFFFFFFFFFFF)
        return state, np.float64(mantissa53) * np.float64(1.1102230246251565e-16)

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
        """Estimate expected spread via MC simulations (serial numba fast path).

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

    @numba.njit(parallel=True, cache=True)
    def _estimate_spread_numba_parallel(indptr, indices, seed_array, prob,
                                        num_nodes, mc_rounds, base_seed):
        """Parallel-MC variant of _estimate_spread_numba.

        Each MC round runs in its own thread via numba.prange. Per-round
        visited/frontier buffers are pre-allocated as 2D arrays OUTSIDE
        the prange loop (allocating inside numba.prange has unreliable
        semantics — buffers can be hoisted/shared, producing all-zero
        spreads). Each thread gets its own row by indexing visited[r],
        which numba treats as a true per-iteration view.

        On a 32-core CPU instance this gives ~25-30× speedup over the
        serial version. Result is numerically equivalent — each round
        receives a deterministic per-round seed (`base_seed + r`), the
        same simulation kernel, and integer counts summed in fp64
        (associative within fp64 noise ~1e-12). MC mean is identical.

        Memory: O(mc_rounds × num_nodes × 8B). For arxiv (170K nodes,
        50 MC) = ~68 MB — negligible vs. the GPU-side TracIn footprint.
        """
        # Pre-allocate per-round buffers so numba's parallel analysis
        # treats visited[r], frontier[r] as thread-local views.
        visited = np.zeros((mc_rounds, num_nodes), dtype=np.int32)
        frontier = np.empty((mc_rounds, num_nodes), dtype=np.int32)
        totals = np.zeros(mc_rounds, dtype=np.float64)
        for r in numba.prange(mc_rounds):
            totals[r] = _simulate_spread_numba(
                indptr, indices, seed_array, prob, num_nodes,
                base_seed + r, visited[r], np.int32(1), frontier[r]
            )
        return totals.sum() / np.float64(mc_rounds)


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
        # A.4: IM selector MC seed is decoupled from GU training seed.
        # Previously coupling caused Jaccard ~0.13 across 5 GU seeds (the
        # selector "wandered" with the seed, so +6.8 effect contained MC noise).
        # Default fixed value 2024; override only with `im_selector_seed`.
        seed_value = args.get('im_selector_seed', 2024)
        try:
            self.random_seed = int(seed_value)
        except (TypeError, ValueError):
            self.random_seed = 2024

        # Batch-CELF batch size (was IMV4Strategy's im_v4_batch_size; merged
        # into IMStrategy on 2026-05-05). The numba CELF path consumes
        # `self.im_batch_size` candidates per round (1 = classic CELF,
        # higher = batched approximation that trades some spread for speed).
        # Read both the new and legacy keys for backward compat with old yamls.
        batch_size = args.get('im_batch_size', args.get('im_v4_batch_size', 5))
        try:
            self.im_batch_size = max(int(batch_size), 1)
        except (TypeError, ValueError):
            self.im_batch_size = 5

        self.enable_score_cache = bool(args.get('enable_score_cache', True))
        self._score_cache = (
            ScoreCache(namespace='im', cache_dir=args.get('score_cache_dir', './results/score_cache'))
            if self.enable_score_cache else None
        )
        # Full-CELF cache (separate namespace from per-candidate spread cache).
        # Key intentionally omits unlearning_methods + GU seed — IM selection
        # is purely topological (edge_index + IM hyperparams + im_selector_seed),
        # so 1 successful run amortises across all (method × GU_seed) cells.
        self._celf_cache = (
            ScoreCache(namespace='im_celf', cache_dir=args.get('score_cache_dir', './results/score_cache'))
            if self.enable_score_cache else None
        )

        # Toggle MC parallelism. Default ON because numba.prange degrades
        # gracefully to serial when NUMBA_NUM_THREADS=1; on multi-core CPU
        # instances it gives ~25-30× speedup with bit-equivalent results.
        self.parallel_mc = bool(args.get('im_parallel_mc', True))
        if HAS_NUMBA:
            self._spread_fn = (
                _estimate_spread_numba_parallel if self.parallel_mc
                else _estimate_spread_numba
            )
        else:
            self._spread_fn = None

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

        Cache-aware: a successful run is persisted under a key that does NOT
        depend on the unlearning method or GU training seed (purely topology
        + IM hyperparams + im_selector_seed). One run on (dataset, IM
        hyperparams) covers all (method × GU_seed) cells.

        Args:
            edge_index: [2, E] edge index tensor
            num_nodes: Total number of nodes in the graph
            k: Number of seed nodes to select
            candidate_set: List of candidate node indices

        Returns:
            (selected_nodes, scores): List of k selected node indices and their
                marginal gain scores as a tensor of length k.
        """
        # Apply candidate_fraction pruning by degree (deterministic in inputs).
        # The post-pruning candidate set is what drives the actual CELF
        # computation, so the cache key fingerprints the post-pruning set.
        if self.candidate_fraction < 1.0 and len(candidate_set) > k:
            candidate_set = self._prune_candidates_by_degree(
                edge_index, num_nodes, candidate_set, self.candidate_fraction, k
            )

        cfg = None
        key = None
        if self._celf_cache is not None:
            cfg = self._build_celf_cache_config(edge_index, num_nodes, k, candidate_set)
            hit, key = self._celf_cache.get(cfg)
            if hit is not None:
                if hit.candidates.shape[0] == k and hit.scores.shape[0] == k:
                    print(f"[ScoreCache] HIT  im_celf  key={key} k={k} src={hit.source}")
                    selected = hit.candidates.astype(np.int64).tolist()
                    return selected, torch.from_numpy(hit.scores.astype(np.float32))
                print(f"[ScoreCache] STALE im_celf key={key} (k mismatch: {hit.candidates.shape[0]} vs {k}) — recomputing")
            else:
                print(f"[ScoreCache] MISS im_celf  key={key} — running full CELF on {len(candidate_set)} candidates...")

        if HAS_NUMBA:
            selected, scores = self._compute_im_celf_numba(edge_index, num_nodes, k, candidate_set)
        else:
            selected, scores = self._compute_im_celf_python(edge_index, num_nodes, k, candidate_set)

        if self._celf_cache is not None and cfg is not None:
            selected_arr = np.asarray(selected, dtype=np.int64)
            scores_arr = scores.detach().cpu().numpy().astype(np.float32, copy=False)
            path = self._celf_cache.save(selected_arr, scores_arr, cfg)
            print(f"[ScoreCache] SAVE im_celf  key={key} -> {path}")

        return selected, scores

    def _build_celf_cache_config(self, edge_index, num_nodes, k, candidate_set):
        """Cache key for full-CELF results.

        Intentionally omits unlearning_methods and GU training seed: CELF
        is pure topology + IM hyperparams. Including them would force
        N_methods × N_seeds redundant 2-4h runs. With the canonical default
        `im_selector_seed=2024` (Phase A.4), one cache entry covers all
        18 (method × GU_seed × IM strategy) cells in B.2.
        """
        return {
            "namespace": "im_celf",
            "propagation_prob": float(self.propagation_prob),
            "mc_rounds": int(self.mc_rounds),
            "candidate_fraction": float(self.candidate_fraction),
            "im_selector_seed": int(self.random_seed),
            "im_batch_size": int(self.im_batch_size),
            "k": int(k),
            "graph_fingerprint": graph_fingerprint(edge_index, num_nodes, candidate_set),
        }

    def _compute_im_celf_python(self, edge_index, num_nodes, k, candidate_set):
        """Pure Python CELF implementation (fallback).

        Step 1 (initial spreads) is computed inline rather than via
        compute_initial_marginal_gains so the global random.random() state
        flows continuously into step 2+, preserving the bit-exact original
        RNG behavior captured by the golden fixtures.
        """
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
        """Numba-accelerated batch-CELF implementation.

        Merged from former IMV4Strategy on 2026-05-05. Batch-CELF accepts the
        validated best candidate per round, then greedily consumes the next
        ``self.im_batch_size - 1`` heap candidates in the same round. With
        ``im_batch_size=1`` this reduces to classical CELF; higher values
        trade a small amount of spread for fewer recomputations.
        """
        indptr, indices = self._build_adjacency_csr(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds
        batch = self.im_batch_size

        # Step 1: Compute initial marginal gains for all candidates.
        # Inlined (rather than via compute_initial_marginal_gains) to avoid
        # cache-induced divergence — the numba step 2+ has its own deterministic
        # seeding so this is purely a "don't disturb golden fixtures" call.
        heap = []
        for node in candidate_set:
            seed_arr = np.array([node], dtype=np.int32)
            base_seed = self.random_seed * 10000 + node % 10000
            spread = self._spread_fn(indptr, indices, seed_arr, prob,
                                     num_nodes, mc, base_seed)
            heapq.heappush(heap, (-spread, 0, node))

        selected = []
        selected_set_list = []
        scores = []
        current_spread = 0.0
        round_idx = 0

        while len(selected) < k and heap:
            batch_size = min(batch, k - len(selected))

            while True:
                neg_gain, last_updated, node = heapq.heappop(heap)

                if last_updated == round_idx:
                    gain = float(-neg_gain)
                    selected.append(node)
                    selected_set_list.append(node)
                    scores.append(gain)
                    current_spread += gain

                    popped_count = 1
                    while popped_count < batch_size and heap:
                        next_neg_gain, _, next_node = heapq.heappop(heap)
                        next_gain = float(-next_neg_gain)
                        selected.append(next_node)
                        selected_set_list.append(next_node)
                        scores.append(next_gain)
                        current_spread += next_gain
                        popped_count += 1
                    break

                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                # Deterministic cheap hash for seed synthesis (avoid Python hash randomization).
                pseudo_hash = int(np.sum(seed_arr)) * 131 + int(seed_arr.shape[0])
                base_seed = self.random_seed * 10000 + (pseudo_hash % 10000)
                new_spread = self._spread_fn(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, round_idx, node))

            round_idx += 1

        return selected, torch.tensor(scores)

    def compute_initial_marginal_gains(self, edge_index, num_nodes, candidate_set):
        """
        Compute single-node spread for each candidate (CELF step 1 only).

        This is used by HybridStrategy to get IM scores without running full CELF,
        and by full-CELF as the first step. Cached via ScoreCache (NPZ) when
        enabled — pure topology, so cache is shared across methods, seeds, and k.

        Args:
            edge_index: [2, E] edge index tensor
            num_nodes: Total number of nodes
            candidate_set: List of candidate node indices

        Returns:
            scores: [len(candidate_set)] tensor of spread scores, in the same
                    order as candidate_set
        """
        if self._score_cache is not None:
            cfg = self._build_cache_config(edge_index, num_nodes, candidate_set)
            hit, key = self._score_cache.get(cfg)
            if hit is not None:
                cand_np = np.asarray(candidate_set, dtype=np.int64)
                if hit.candidates.shape == cand_np.shape and (hit.candidates == cand_np).all():
                    print(f"[ScoreCache] HIT  im  key={key} n={hit.scores.shape[0]} src={hit.source}")
                    return torch.from_numpy(hit.scores)
                print(f"[ScoreCache] STALE im key={key} (candidate mismatch) — recomputing")
            print(f"[ScoreCache] MISS im  key={key} — computing spread for {len(candidate_set)} candidates...")

        if HAS_NUMBA:
            scores = self._compute_initial_gains_numba(edge_index, num_nodes, candidate_set)
        else:
            scores = self._compute_initial_gains_python(edge_index, num_nodes, candidate_set)

        if self._score_cache is not None:
            cand_np = np.asarray(candidate_set, dtype=np.int64)
            scores_np = scores.detach().cpu().numpy().astype(np.float32, copy=False)
            path = self._score_cache.save(cand_np, scores_np, cfg)
            print(f"[ScoreCache] SAVE im  key={key} -> {path}")

        return scores

    def _build_cache_config(self, edge_index, num_nodes, candidate_set):
        """IM cache key — pure topology, no model state. Shared across methods/seeds."""
        return {
            "namespace": "im",
            "propagation_prob": float(self.propagation_prob),
            "mc_rounds": int(self.mc_rounds),
            "candidate_fraction": float(self.candidate_fraction),
            "im_selector_seed": int(self.random_seed),
            "graph_fingerprint": graph_fingerprint(edge_index, num_nodes, candidate_set),
        }

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
            spread = self._spread_fn(indptr, indices, seed_arr, prob,
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
