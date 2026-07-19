"""Pure Cache V2 Selection Recipe, resolution, and Artifact materialization.

Dataset access and Selection compute deliberately do not exist in this module.
The experiment/GU layer supplies a complete Recipe and, on a clean miss, an
already-produced ordered node list.  Cache V2 only validates identity,
resolves exact hits, writes immutable Artifacts, and enforces integrity.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence, Tuple, Union

from .contracts import (
    ArtifactRecipe,
    ArtifactType,
    ProducerVersion,
    validate_artifact_id,
    validate_sha256,
)
from .errors import CacheResolutionError, ContractValidationError
from .index import CacheIndex
from .resolver import ArtifactResolver
from .store import ArtifactStore, StoreResult


SELECTION_RECIPE_CONTRACT = "opengu-selection-recipe-v2"


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ContractValidationError("{0} must be a non-empty string".format(label))
    return value.strip()


def _required_integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ContractValidationError(
            "{0} must be an integer >= {1}".format(label, minimum)
        )
    return value


def _producer_mapping(version: ProducerVersion) -> Mapping[str, Any]:
    if not isinstance(version, ProducerVersion) or not version.is_identified:
        raise ContractValidationError("producer_version must identify its producer")
    return version.to_dict()


def build_selection_recipe(
    *,
    dataset_fingerprint: str,
    graph_fingerprint: str,
    candidate_set_hash: str,
    num_nodes: int,
    candidate_count: int,
    node_id_space: str,
    strategy: str,
    seed: int,
    k: int,
    producer_version: ProducerVersion,
    algorithm_version: str,
    parameters: Mapping[str, Any],
    source_score_artifact_id: Optional[str] = None,
) -> ArtifactRecipe:
    """Build the V2 boundary Recipe from upstream SelectionInputs identity."""

    num_nodes = _required_integer(num_nodes, "num_nodes")
    candidate_count = _required_integer(candidate_count, "candidate_count", minimum=1)
    k = _required_integer(k, "k", minimum=1)
    seed = _required_integer(seed, "selector_seed")
    if candidate_count > num_nodes:
        raise ContractValidationError("candidate_count exceeds num_nodes")
    if k > candidate_count:
        raise ContractValidationError("k exceeds candidate_count")
    if not isinstance(parameters, Mapping):
        raise ContractValidationError("selector_parameters must be a mapping")
    fields = {
        "selection_recipe_contract": SELECTION_RECIPE_CONTRACT,
        "dataset_fingerprint": validate_sha256(
            dataset_fingerprint, "dataset_fingerprint"
        ),
        "graph_fingerprint": validate_sha256(
            graph_fingerprint, "graph_fingerprint"
        ),
        "candidate_set_hash": validate_sha256(
            candidate_set_hash, "candidate_set_hash"
        ),
        "num_nodes": num_nodes,
        "candidate_count": candidate_count,
        "node_id_space": _required_text(node_id_space, "node_id_space"),
        "selector": _required_text(strategy, "strategy").lower(),
        "selector_seed": seed,
        "selector_algorithm_version": _required_text(
            algorithm_version, "algorithm_version"
        ),
        "producer_version": dict(_producer_mapping(producer_version)),
        "k": k,
        "selector_parameters": dict(parameters),
    }
    if source_score_artifact_id is not None:
        source_score = validate_artifact_id(
            source_score_artifact_id, "source_score_artifact_id"
        )
        if not source_score.startswith("score_"):
            raise ContractValidationError(
                "source_score_artifact_id must identify a Score Artifact"
            )
        fields["source_score_artifact_id"] = source_score
    return ArtifactRecipe(fields)


@dataclass(frozen=True)
class SelectionArtifactRequest:
    """Dataset-free identity required by Cache V2 for one Selection Artifact."""

    recipe: ArtifactRecipe
    producer_version: ProducerVersion
    num_nodes: int

    def __post_init__(self) -> None:
        if not isinstance(self.recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        producer = _producer_mapping(self.producer_version)
        fields = self.recipe.fields
        if fields.get("selection_recipe_contract") != SELECTION_RECIPE_CONTRACT:
            raise ContractValidationError(
                "unsupported selection recipe contract; Legacy Selection Recipes "
                "remain addressable by explicit Artifact ID but are not eligible "
                "for V2 producer resolution"
            )
        required = {
            "selection_recipe_contract",
            "dataset_fingerprint",
            "graph_fingerprint",
            "candidate_set_hash",
            "num_nodes",
            "candidate_count",
            "node_id_space",
            "selector",
            "selector_seed",
            "selector_algorithm_version",
            "producer_version",
            "k",
            "selector_parameters",
        }
        missing = sorted(required.difference(fields))
        if missing:
            raise ContractValidationError(
                "Selection Recipe identity is incomplete: {0}".format(",".join(missing))
            )
        for name in (
            "dataset_fingerprint",
            "graph_fingerprint",
            "candidate_set_hash",
        ):
            validate_sha256(fields.get(name), "Recipe {0}".format(name))
        recipe_num_nodes = _required_integer(fields.get("num_nodes"), "Recipe num_nodes")
        candidate_count = _required_integer(
            fields.get("candidate_count"), "Recipe candidate_count", minimum=1
        )
        k = _required_integer(fields.get("k"), "Recipe k", minimum=1)
        _required_integer(fields.get("selector_seed"), "Recipe selector_seed")
        _required_text(fields.get("node_id_space"), "Recipe node_id_space")
        _required_text(fields.get("selector"), "Recipe selector")
        _required_text(
            fields.get("selector_algorithm_version"),
            "Recipe selector_algorithm_version",
        )
        if not isinstance(fields.get("selector_parameters"), Mapping):
            raise ContractValidationError("Recipe selector_parameters must be a mapping")
        if fields.get("producer_version") != producer:
            raise ContractValidationError(
                "Recipe producer_version does not match Artifact producer_version"
            )
        source_score = fields.get("source_score_artifact_id")
        if source_score is not None:
            source_score = validate_artifact_id(
                source_score, "Recipe source_score_artifact_id"
            )
            if not source_score.startswith("score_"):
                raise ContractValidationError(
                    "Recipe source_score_artifact_id must identify a Score Artifact"
                )
        if recipe_num_nodes != self.num_nodes:
            raise ContractValidationError(
                "Selection request num_nodes does not match Recipe num_nodes"
            )
        if candidate_count > recipe_num_nodes:
            raise ContractValidationError("Recipe candidate_count exceeds num_nodes")
        if k > candidate_count:
            raise ContractValidationError("Recipe k exceeds candidate_count")

    @classmethod
    def from_recipe(
        cls, recipe: ArtifactRecipe, producer_version: ProducerVersion
    ) -> "SelectionArtifactRequest":
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        num_nodes = recipe.fields.get("num_nodes")
        return cls(
            recipe=recipe,
            producer_version=producer_version,
            num_nodes=num_nodes,
        )


@dataclass(frozen=True)
class SelectionResolution:
    hit: bool
    result: Optional[StoreResult]
    miss_reasons: Tuple[str, ...]


def _absolute_store_root(store_root: Union[str, Path]) -> Path:
    supplied = Path(store_root).expanduser()
    if not supplied.is_absolute():
        raise ContractValidationError("Cache V2 store root must be absolute")
    if ".." in supplied.parts:
        raise ContractValidationError("Cache V2 store root must not contain '..'")
    return supplied.resolve(strict=False)


def resolve_selection_artifact(
    store_root: Union[str, Path], request: SelectionArtifactRequest
) -> SelectionResolution:
    """Resolve and verify an exact hit without dataset access or any write."""

    if not isinstance(request, SelectionArtifactRequest):
        raise ContractValidationError("request must be SelectionArtifactRequest")
    root = _absolute_store_root(store_root)
    index_path = root / "index.sqlite"
    if not index_path.is_file():
        return SelectionResolution(False, None, ("store_not_initialized",))
    index = CacheIndex(index_path)
    index.check_schema()
    explanation = ArtifactResolver(index).explain_exact(
        ArtifactType.SELECTION, request.recipe
    )
    if explanation.hit and explanation.exact_candidate is not None:
        store = ArtifactStore(
            root,
            producer_version=request.producer_version,
            index=index,
        )
        result = store.load_read_only(
            request.recipe,
            request.num_nodes,
            candidate_nodes=None,
            artifact_id=explanation.exact_candidate["artifact_id"],
        )
        return SelectionResolution(True, result, explanation.miss_reasons)
    if (
        explanation.exact_candidate is None
        and explanation.miss_reasons == ("no_exact_candidate",)
    ):
        return SelectionResolution(False, None, explanation.miss_reasons)
    raise CacheResolutionError(
        "exact Selection lookup failed closed: {0}".format(
            ",".join(explanation.miss_reasons)
        )
    )


def store_selection_artifact(
    store_root: Union[str, Path],
    request: SelectionArtifactRequest,
    *,
    selected_nodes: Sequence[int],
    compute_seconds: float,
) -> StoreResult:
    """Store upstream-produced nodes; this function never invokes a producer."""

    if not isinstance(request, SelectionArtifactRequest):
        raise ContractValidationError("request must be SelectionArtifactRequest")
    root = _absolute_store_root(store_root)
    store = ArtifactStore(root, producer_version=request.producer_version)
    if not store.index.database_path.is_file():
        store.initialize()
    else:
        store.index.check_schema()
    return store.store_selection(
        request.recipe,
        selected_nodes,
        num_nodes=request.num_nodes,
        candidate_nodes=None,
        compute_seconds=compute_seconds,
    )


__all__ = [
    "SELECTION_RECIPE_CONTRACT",
    "SelectionArtifactRequest",
    "SelectionResolution",
    "build_selection_recipe",
    "resolve_selection_artifact",
    "store_selection_artifact",
]
