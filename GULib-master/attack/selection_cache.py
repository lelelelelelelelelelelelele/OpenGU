"""Generic Selection consumer of the existing Cache V2 contract."""
from dataclasses import dataclass
from pathlib import Path
from attack.cache_identity import resolve_store_root
from cache_v2 import CacheIndex
from cache_v2.selection_materializer import resolve_selection_artifact, store_selection_artifact

@dataclass
class SelectionResult:
    selected_nodes: list
    artifact_id: str
    recipe_hash: str
    content_hash: str
    source: str
    selection_time: float

class SelectionCache:
    def __init__(self, cache_dir="./results/cache_v2"):
        self.root = resolve_store_root(cache_dir)

    def _result(self, result, request):
        return SelectionResult(list(result.payload.selected_nodes_ordered),
            result.artifact_id, request.recipe.recipe_hash, result.content_hash,
            str(self.root / result.semantic_path),
            float(CacheIndex(self.root / "index.sqlite").get_artifact(result.artifact_id)["compute_seconds"] or 0.0))

    def get(self, request):
        resolution = resolve_selection_artifact(self.root, request)
        return self._result(resolution.result, request) if resolution.hit else None

    def save(self, selected_nodes, request, selection_time):
        result = store_selection_artifact(self.root, request, selected_nodes=selected_nodes,
                                         compute_seconds=selection_time)
        return self._result(result, request)
