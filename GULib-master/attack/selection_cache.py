"""
SelectionCache - Caching mechanism for strategy-selected nodes.

This cache is intentionally decoupled from attack result cache so that
selection can be reused across GU methods when safe.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SelectionResult:
    """Serializable selection cache payload."""

    strategy_name: str
    selected_nodes: List[int]
    selection_time: float
    selection_key: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SelectionResult":
        nodes = data.get("selected_nodes", [])
        if nodes is None:
            nodes = []
        return SelectionResult(
            strategy_name=str(data.get("strategy_name", "")),
            selected_nodes=[int(x) for x in nodes],
            selection_time=float(data.get("selection_time", 0.0)),
            selection_key=str(data.get("selection_key", "")),
            created_at=str(data.get("created_at", datetime.now().isoformat())),
            metadata=dict(data.get("metadata", {})),
        )


class SelectionCache:
    """
    Cache selected nodes by a strategy-specific cross-method key.

    Cache file format:
    {
      "cache_key": "<hash>",
      "cached_at": "<iso-time>",
      "config": {...},
      "selection_result": {...}
    }
    """

    def __init__(self, cache_dir: str = "./results/selection_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _stable_json(config: Dict[str, Any]) -> str:
        return json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def build_selection_key(self, config: Dict[str, Any]) -> str:
        key_string = self._stable_json(config)
        digest = hashlib.sha256(key_string.encode("utf-8")).hexdigest()
        return digest[:32]

    def _cache_path(self, cache_key: str) -> Path:
        return self.cache_dir / f"{cache_key}.json"

    def get(self, config: Dict[str, Any]) -> Tuple[Optional[SelectionResult], Optional[str], Optional[str]]:
        """
        Return (selection_result, cache_key, source_file) if hit, else (None, key, None).

        Corrupted entries are ignored and treated as cache miss.
        """
        cache_key = self.build_selection_key(config)
        cache_path = self._cache_path(cache_key)
        if not cache_path.exists():
            return None, cache_key, None

        try:
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            result_data = payload.get("selection_result")
            if not isinstance(result_data, dict):
                return None, cache_key, None
            result = SelectionResult.from_dict(result_data)
            return result, cache_key, str(cache_path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None, cache_key, None

    def save(self, result: SelectionResult, config: Dict[str, Any]) -> str:
        cache_key = self.build_selection_key(config)
        cache_path = self._cache_path(cache_key)
        payload = {
            "cache_key": cache_key,
            "cached_at": datetime.now().isoformat(),
            "config": config,
            "selection_result": result.to_dict(),
        }
        cache_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
        return str(cache_path)
