import heapq
import numpy as np
import torch

from .im_strategy import IMStrategy, HAS_NUMBA, _estimate_spread_numba


class IMV4Strategy(IMStrategy):
    """
    IM V4: Batch-CELF approximation.

    Compared with baseline CELF, V4 accepts one validated best candidate and
    then greedily consumes the next B-1 heap candidates in the same round.
    This reduces recomputation at the cost of small spread degradation.
    """

    def __init__(self, args: dict):
        super().__init__(args)
        batch_size = args.get("im_v4_batch_size", 5)
        try:
            self.im_v4_batch_size = max(int(batch_size), 1)
        except (TypeError, ValueError):
            self.im_v4_batch_size = 5

    def compute_im_celf(self, edge_index, num_nodes, k, candidate_set):
        """
        Batch-CELF entrypoint with the same signature as IMStrategy.
        """
        if self.candidate_fraction < 1.0 and len(candidate_set) > k:
            candidate_set = self._prune_candidates_by_degree(
                edge_index, num_nodes, candidate_set, self.candidate_fraction, k
            )

        if HAS_NUMBA:
            return self._compute_im_celf_v4_numba(edge_index, num_nodes, k, candidate_set)
        return self._compute_im_celf_python(edge_index, num_nodes, k, candidate_set)

    def _compute_im_celf_v4_numba(self, edge_index, num_nodes, k, candidate_set):
        """
        Numba-backed Batch-CELF implementation.
        """
        indptr, indices = self._build_adjacency_csr(edge_index, num_nodes)
        prob = self.propagation_prob
        mc = self.mc_rounds
        batch = self.im_v4_batch_size

        heap = []
        for node in candidate_set:
            seed_arr = np.array([node], dtype=np.int32)
            base_seed = self.random_seed * 10000 + node % 10000
            spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
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
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, round_idx, node))

            round_idx += 1

        return selected, torch.tensor(scores)
