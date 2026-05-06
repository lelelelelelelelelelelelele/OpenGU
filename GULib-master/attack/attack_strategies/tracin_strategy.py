import torch
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import Data

from .base_strategy import BaseStrategy
from ..score_cache import ScoreCache, graph_fingerprint


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

    requires_trained_model = True

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
        self.enable_score_cache = bool(args.get('enable_score_cache', True))
        self._score_cache = (
            ScoreCache(namespace='if', cache_dir=args.get('score_cache_dir', './results/score_cache'))
            if self.enable_score_cache else None
        )

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

        # Compute TracIn scores (cached if enabled)
        scores = self.compute_scores(model, data, candidates)

        # Select top-k nodes with highest scores
        _, topk_indices = torch.topk(scores, k)

        # Map indices back to actual node IDs
        selected_nodes = candidates[topk_indices]

        return selected_nodes.cpu()

    def compute_scores(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
    ) -> Tensor:
        """Public, cache-aware wrapper around _compute_tracin_scores.

        HybridStrategy calls this directly so the IF branch can be reused
        across alpha values without recomputing the gradient matrix.

        Returns scores in the same order as `candidates` (length M).
        """
        if self._score_cache is None:
            return self._compute_tracin_scores(model, data, candidates)

        cfg = self._build_cache_config(model, data, candidates)
        hit, key = self._score_cache.get(cfg)
        if hit is not None:
            cands_np = candidates.detach().cpu().numpy().astype('int64', copy=False)
            if hit.candidates.shape == cands_np.shape and (hit.candidates == cands_np).all():
                print(f"[ScoreCache] HIT  if  key={key} n={hit.scores.shape[0]} src={hit.source}")
                return torch.from_numpy(hit.scores).to(self.device)
            print(f"[ScoreCache] STALE if key={key} (candidate mismatch) — recomputing")

        print(f"[ScoreCache] MISS if  key={key} — computing TracIn scores...")
        scores = self._compute_tracin_scores(model, data, candidates)

        cands_np = candidates.detach().cpu().numpy().astype('int64', copy=False)
        scores_np = scores.detach().cpu().numpy().astype('float32', copy=False)
        path = self._score_cache.save(cands_np, scores_np, cfg)
        print(f"[ScoreCache] SAVE if  key={key} -> {path}")
        return scores

    def _build_cache_config(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
    ) -> dict:
        """Cache key for IF scores.

        Intentionally does NOT include the model state hash — empirically,
        re-training under the same (dataset, model, seed, ratio) config
        produces tiny weight drift due to non-deterministic CUDA/cuDNN ops,
        which would make the cache miss across every process invocation.
        Since the cache is used to share TracIn rankings (not bit-exact
        scores) between Hybrid alpha-sweeps and across cells with the same
        training config, the static config fields are the right key.

        If the user needs a fresh recompute, they can delete the cache file
        or pass enable_score_cache=False.
        """
        return {
            "namespace": "if",
            "dataset_name": str(self.args.get("dataset_name", "")),
            "base_model": str(self.args.get("base_model", "")),
            "unlearn_ratio": float(self.args.get("unlearn_ratio", 0.0)),
            "seed": int(self.args.get("seed", 0) or 0),
            "loss_type": self.loss_type,
            "is_transductive": bool(self.args.get("is_transductive", True)),
            "is_balanced": bool(self.args.get("is_balanced", False)),
            "unlearning_methods": str(self.args.get("unlearning_methods", "")),
            "graph_fingerprint": graph_fingerprint(
                data.edge_index, data.num_nodes, candidates
            ),
        }

    def _compute_tracin_scores(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
    ) -> Tensor:
        """Dispatcher: pick dense or chunked path based on estimated G size.

        For small graphs (cora/citeseer) the dense path is identical to the
        original implementation. For large graphs (ogbn-arxiv) the chunked
        path streams gradients to CPU memory to avoid materialising the full
        G matrix on GPU. Both paths produce the same top-k ranking; scores
        differ at most by ~1e-6 due to fp accumulation order.

        Threshold and chunk size are configurable via args:
            tracin_chunk_threshold_gb (default 4.0)
            tracin_chunk_size         (default 1000)
        """
        n_cand = int(candidates.shape[0])
        num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        g_matrix_gb = n_cand * num_params * 4 / 1e9

        threshold_gb = float(self.args.get('tracin_chunk_threshold_gb', 4.0))
        if g_matrix_gb < threshold_gb:
            print(f"[TracIn] G matrix ~{g_matrix_gb:.2f} GB < {threshold_gb} GB threshold → dense path")
            return self._compute_tracin_scores_dense(model, data, candidates)

        chunk_size = int(self.args.get('tracin_chunk_size', 1000))
        print(f"[TracIn] G matrix ~{g_matrix_gb:.1f} GB > {threshold_gb} GB threshold "
              f"→ chunked path (chunk_size={chunk_size}, CPU offload)")
        return self._compute_tracin_scores_chunked(model, data, candidates, chunk_size)

    def _compute_tracin_scores_dense(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
    ) -> Tensor:
        """
        Original dense TracIn implementation; materialises full G [N, d] on GPU.

        Use only when N × num_params × 4B fits in GPU memory with margin.
        For arxiv (N≈90K, d≈160K → ~55 GB) this OOMs even on H100 96GB
        because torch.stack temporarily doubles the footprint.
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

    def _compute_tracin_scores_chunked(
        self,
        model: torch.nn.Module,
        data: Data,
        candidates: Tensor,
        chunk_size: int = 1000,
    ) -> Tensor:
        """Chunked + CPU-offload TracIn: streams gradients to CPU pinned memory.

        Pass 1: forward once, then for each chunk of `chunk_size` candidates,
                stack their gradients into a small G_chunk on GPU, accumulate
                col_sum, offload G_chunk to CPU, free GPU memory.
        Pass 2: reload each G_chunk to GPU, compute scores = -(G_chunk @ col_sum),
                free again.

        Peak GPU memory: O(chunk_size × num_params); CPU memory: O(N × num_params).
        Result is numerically equivalent to the dense path within fp summation
        tolerance (~1e-6); top-k ranking is bit-identical for non-tied scores.
        """
        if hasattr(model, 'forward') and 'edge_index' in model.forward.__code__.co_varnames:
            out = model(data.x, data.edge_index)
        else:
            out = model(data.x)

        params = [p for p in model.parameters() if p.requires_grad]
        n_cand = int(candidates.shape[0])

        # Pass 1: build chunks, accumulate col_sum on GPU, offload G_chunk to CPU
        col_sum: Tensor | None = None
        G_cpu_chunks: list[Tensor] = []

        for chunk_start in range(0, n_cand, chunk_size):
            chunk_end = min(chunk_start + chunk_size, n_cand)
            chunk_grads = []
            for i in range(chunk_start, chunk_end):
                node = candidates[i]
                node_idx = node.item() if isinstance(node, Tensor) else int(node)
                loss = self._compute_node_loss(out, data.y, node_idx)
                # Retain the shared forward graph until the very last candidate.
                retain = (i < n_cand - 1)
                grad_tuple = torch.autograd.grad(
                    loss, params, retain_graph=retain, create_graph=False
                )
                chunk_grads.append(torch.cat([g.flatten() for g in grad_tuple]))

            G_chunk = torch.stack(chunk_grads)  # [B, d] on GPU
            chunk_col = G_chunk.sum(dim=0)
            col_sum = chunk_col if col_sum is None else col_sum + chunk_col
            G_cpu_chunks.append(G_chunk.detach().cpu())
            del G_chunk, chunk_grads, chunk_col
            if self.device.type == 'cuda':
                torch.cuda.empty_cache()

        assert col_sum is not None, "n_cand must be > 0"

        # Pass 2: reload each chunk and compute scores
        scores = torch.empty(n_cand, device=self.device)
        for k, G_chunk_cpu in enumerate(G_cpu_chunks):
            chunk_start = k * chunk_size
            G_chunk = G_chunk_cpu.to(self.device, non_blocking=True)
            chunk_end = chunk_start + G_chunk.shape[0]
            scores[chunk_start:chunk_end] = -(G_chunk @ col_sum)
            del G_chunk
            if self.device.type == 'cuda':
                torch.cuda.empty_cache()

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
