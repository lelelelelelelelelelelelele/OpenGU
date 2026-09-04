"""Strict read-only Cache V2 Selection consumer contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

from .canonical import TYPE_TAG, canonicalize
from .contracts import ArtifactRecipe, ArtifactType, ProducerVersion
from .errors import CacheResolutionError, ContractValidationError
from .index import CacheIndex
from .store import ArtifactStore


def _decode_canonical(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, list):
        return [_decode_canonical(item) for item in value]
    if not isinstance(value, Mapping):
        raise ContractValidationError("indexed canonical value has an invalid type")
    tag = value.get(TYPE_TAG)
    if tag == "mapping" and set(value) == {TYPE_TAG, "items"}:
        items = value.get("items")
        if not isinstance(items, list):
            raise ContractValidationError("indexed canonical mapping is invalid")
        decoded = {}
        for item in items:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or not isinstance(item[0], str)
                or item[0] in decoded
            ):
                raise ContractValidationError("indexed canonical mapping item is invalid")
            decoded[item[0]] = _decode_canonical(item[1])
        return decoded
    if tag in {"list", "tuple"} and set(value) == {TYPE_TAG, "items"}:
        items = value.get("items")
        if not isinstance(items, list):
            raise ContractValidationError("indexed canonical sequence is invalid")
        decoded_items = [_decode_canonical(item) for item in items]
        return decoded_items if tag == "list" else tuple(decoded_items)
    if tag == "float" and set(value) == {TYPE_TAG, "hex"}:
        raw = value.get("hex")
        if not isinstance(raw, str):
            raise ContractValidationError("indexed canonical float is invalid")
        try:
            return float.fromhex(raw)
        except ValueError as exc:
            raise ContractValidationError("indexed canonical float is invalid") from exc
    raise ContractValidationError(
        "runtime Selection Recipe contains an unsupported canonical value"
    )


def _decode_exact_mapping(value: Any, label: str) -> Mapping[str, Any]:
    decoded = _decode_canonical(value)
    if not isinstance(decoded, Mapping) or canonicalize(decoded) != value:
        raise ContractValidationError("{0} does not round-trip canonically".format(label))
    return decoded


@dataclass(frozen=True)
class LoadedSelectionArtifact:
    artifact_id: str
    recipe_hash: str
    content_hash: str
    semantic_path: str
    selector: str
    k: int
    selected_nodes: Tuple[int, ...]
    producer_version: Mapping[str, Any]
    lookup_policy: str = "cache_v2_exact_artifact_id"
    authoritative: bool = True

    def provenance(self, store_root: Union[str, Path]) -> Mapping[str, Any]:
        return {
            "outcome": "hit",
            "artifact_id": self.artifact_id,
            "artifact_type": ArtifactType.SELECTION.value,
            "recipe_hash": self.recipe_hash,
            "content_hash": self.content_hash,
            "source_file": str(Path(store_root).resolve() / Path(self.semantic_path)),
            "hit_source": "cache_v2:{0}".format(self.artifact_id),
            "lookup_policy": self.lookup_policy,
            "authoritative": True,
            "write_outcome": "reused",
            "recipe": {"strategy": self.selector, "k": self.k},
        }


def load_selection_artifact(
    store_root: Union[str, Path],
    artifact_id: str,
    *,
    num_nodes: int,
    candidate_nodes: Sequence[int],
    expected_selector: Optional[str] = None,
    expected_k: Optional[int] = None,
    expected_dataset_fingerprint: Optional[str] = None,
    expected_graph_fingerprint: Optional[str] = None,
    expected_parameters: Optional[Mapping[str, Any]] = None,
) -> LoadedSelectionArtifact:
    root = Path(store_root).expanduser()
    if not root.is_absolute():
        raise ContractValidationError("Cache V2 store root must be absolute")
    root = root.resolve(strict=False)
    index = CacheIndex(root / "index.sqlite")
    index.check_schema()
    candidate = index.get_artifact(artifact_id)
    if candidate.get("artifact_type") != ArtifactType.SELECTION.value:
        raise CacheResolutionError("requested Artifact is not a Selection Artifact")

    recipe_wrapper = _decode_exact_mapping(candidate.get("recipe"), "indexed Recipe")
    if set(recipe_wrapper) != {"recipe_version", "fields"}:
        raise ContractValidationError("indexed Recipe wrapper is invalid")
    fields = recipe_wrapper.get("fields")
    if not isinstance(fields, Mapping):
        raise ContractValidationError("indexed Recipe fields are invalid")
    recipe = ArtifactRecipe(fields, recipe_version=recipe_wrapper["recipe_version"])
    if recipe.recipe_hash != candidate.get("recipe_hash"):
        raise CacheResolutionError("indexed Recipe does not match requested Artifact")
    for name, expected in (("dataset_fingerprint", expected_dataset_fingerprint),
                           ("graph_fingerprint", expected_graph_fingerprint)):
        if expected is not None and fields.get(name) != expected:
            raise CacheResolutionError("Selection " + name + " mismatch")
    for name, expected in dict(expected_parameters or {}).items():
        if (fields.get("selector_parameters") or {}).get(name) != expected:
            raise CacheResolutionError("Selection parameter " + name + " mismatch")

    producer_mapping = _decode_exact_mapping(
        candidate.get("producer_version"), "indexed producer version"
    )
    if set(producer_mapping) != {"semantic_version", "source_fingerprint"}:
        raise ContractValidationError("indexed producer version is invalid")
    producer = ProducerVersion(**dict(producer_mapping))
    store = ArtifactStore(root, producer_version=producer, index=index)
    result = store.load_read_only(
        recipe,
        num_nodes,
        candidate_nodes=candidate_nodes,
        artifact_id=artifact_id,
    )

    selector = fields.get("selector")
    k = fields.get("k")
    if not isinstance(selector, str) or not selector:
        raise ContractValidationError("Selection Recipe selector is invalid")
    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ContractValidationError("Selection Recipe k is invalid")
    if expected_selector is not None and selector != str(expected_selector):
        raise CacheResolutionError(
            "Selection Artifact selector does not match requested strategy"
        )
    if expected_k is not None and k != int(expected_k):
        raise CacheResolutionError("Selection Artifact k does not match requested k")
    selected = tuple(int(node) for node in result.payload.selected_nodes_ordered)
    if len(selected) != k:
        raise CacheResolutionError("Selection Artifact node count does not match Recipe k")
    return LoadedSelectionArtifact(
        artifact_id=result.artifact_id,
        recipe_hash=recipe.recipe_hash,
        content_hash=result.content_hash,
        semantic_path=result.semantic_path,
        selector=selector,
        k=k,
        selected_nodes=selected,
        producer_version=producer.to_dict(),
    )


__all__ = ["LoadedSelectionArtifact", "load_selection_artifact"]
