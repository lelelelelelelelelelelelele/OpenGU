"""
ScoreCache - Per-candidate score arrays for fusion-based strategies.

Complements SelectionCache:
- SelectionCache (json): top-k node lists, used for fast same-k reuse.
- ScoreCache    (npz):  full per-candidate score vectors, used by HybridStrategy
                        to fuse IF + IM under arbitrary alpha without recompute.

Layout:
    {cache_dir}/{namespace}/{key}.npz   # candidates: int64[M], scores: float32[M]
    {cache_dir}/{namespace}/{key}.json  # sidecar with config, for debugging

Cache key is a SHA-256 hash of the namespace-specific config dict (k is
NOT included so any k can reuse one score vector).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np


@dataclass
class ScoreResult:
    candidates: np.ndarray  # int64[M]
    scores: np.ndarray      # float32[M]
    key: str
    source: str


class ScoreCache:
    """NPZ-backed cache for per-candidate score arrays.

    One instance per namespace ('if', 'im', ...). Stateless beyond the
    namespace + cache directory.
    """

    def __init__(self, namespace: str, cache_dir: str = "./results/score_cache"):
        self.namespace = namespace
        self.dir = Path(cache_dir) / namespace
        self.dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _stable_json(config: Dict[str, Any]) -> str:
        return json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def build_key(self, config: Dict[str, Any]) -> str:
        digest = hashlib.sha256(self._stable_json(config).encode("utf-8")).hexdigest()
        return digest[:32]

    def _path(self, key: str) -> Path:
        return self.dir / f"{key}.npz"

    def _meta_path(self, key: str) -> Path:
        return self.dir / f"{key}.json"

    def get(self, config: Dict[str, Any]) -> Tuple[Optional[ScoreResult], str]:
        """Return (ScoreResult, key) on hit, (None, key) on miss / corruption."""
        key = self.build_key(config)
        path = self._path(key)
        if not path.exists():
            return None, key
        try:
            with np.load(path, allow_pickle=False) as payload:
                candidates = np.asarray(payload["candidates"], dtype=np.int64)
                scores = np.asarray(payload["scores"], dtype=np.float32)
        except (OSError, ValueError, KeyError, EOFError):
            return None, key
        if candidates.shape != scores.shape or candidates.ndim != 1:
            return None, key
        return ScoreResult(candidates=candidates, scores=scores, key=key, source=str(path)), key

    def save(
        self,
        candidates: np.ndarray,
        scores: np.ndarray,
        config: Dict[str, Any],
    ) -> str:
        """Persist scores. Returns path."""
        key = self.build_key(config)
        path = self._path(key)
        meta_path = self._meta_path(key)

        candidates_arr = np.asarray(candidates, dtype=np.int64).reshape(-1)
        scores_arr = np.asarray(scores, dtype=np.float32).reshape(-1)
        if candidates_arr.shape != scores_arr.shape:
            raise ValueError(
                f"ScoreCache.save: candidates {candidates_arr.shape} vs "
                f"scores {scores_arr.shape} mismatch"
            )

        np.savez(path, candidates=candidates_arr, scores=scores_arr)
        meta_path.write_text(
            json.dumps(
                {
                    "key": key,
                    "namespace": self.namespace,
                    "config": config,
                    "saved_at": datetime.now().isoformat(),
                    "n_candidates": int(candidates_arr.shape[0]),
                },
                indent=2,
                ensure_ascii=True,
            ),
            encoding="utf-8",
        )
        return str(path)


# ---------------------------------------------------------------------------
# Helpers for building cache configs from strategy state
# ---------------------------------------------------------------------------

def graph_fingerprint(edge_index, num_nodes: int, candidates) -> str:
    """SHA-256 fingerprint of (num_nodes, edge_index, candidate set).

    Mirrors AttackManager._compute_graph_fingerprint so both caches can stay
    consistent if a future commit unifies them.
    """
    import torch
    if isinstance(edge_index, torch.Tensor):
        ei = edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    else:
        ei = np.asarray(edge_index, dtype=np.int64)
    if isinstance(candidates, torch.Tensor):
        cands = candidates.detach().cpu().numpy().astype(np.int64, copy=False)
    else:
        cands = np.asarray(candidates, dtype=np.int64)
    digest = hashlib.sha256()
    digest.update(np.int64(num_nodes).tobytes())
    digest.update(ei.tobytes())
    digest.update(cands.tobytes())
    return digest.hexdigest()[:32]


def model_fingerprint(model) -> str:
    """SHA-256 over flattened state_dict tensors.

    Two trained models with identical weights (e.g. same dataset + arch + seed
    + training data) produce the same fingerprint, so TracIn scores can be
    shared across GU methods that all start from the same pre-unlearn base.
    """
    import torch
    digest = hashlib.sha256()
    state = model.state_dict() if hasattr(model, "state_dict") else {}
    for name in sorted(state.keys()):
        tensor = state[name]
        if not isinstance(tensor, torch.Tensor):
            continue
        digest.update(name.encode("utf-8"))
        digest.update(np.asarray(tensor.shape, dtype=np.int64).tobytes())
        digest.update(tensor.detach().cpu().numpy().tobytes())
    return digest.hexdigest()[:32]
