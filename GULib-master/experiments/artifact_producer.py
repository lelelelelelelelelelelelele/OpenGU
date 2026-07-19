"""Experiment-owned production seam for formal Cache V2 Artifacts.

Cache V2 resolves and stores immutable payloads.  This module is deliberately
outside ``cache_v2`` because only the experiment/GU layer may invoke Score,
Prediction, or Evaluation producers after a clean exact miss.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Union

from cache_v2 import (
    ArtifactRecipe,
    ArtifactResolver,
    ArtifactType,
    CacheIndex,
    ProducerVersion,
)
from cache_v2.errors import CacheResolutionError, ContractValidationError
from cache_v2.formal_artifacts import payload_type_for
from cache_v2.formal_store import FormalArtifactStore, FormalStoreResult


FORMAL_ARTIFACT_TYPES = frozenset(
    (ArtifactType.SCORE, ArtifactType.PREDICTION, ArtifactType.EVALUATION)
)


def _absolute_store_root(store_root: Union[str, Path]) -> Path:
    supplied = Path(store_root).expanduser()
    if not supplied.is_absolute():
        raise ContractValidationError("Cache V2 store root must be absolute")
    if ".." in supplied.parts:
        raise ContractValidationError("Cache V2 store root must not contain '..'")
    return supplied.resolve(strict=False)


@dataclass(frozen=True)
class FormalArtifactRequest:
    """Complete dataset-free identity for one formal Artifact request."""

    artifact_type: ArtifactType
    recipe: ArtifactRecipe
    producer_version: ProducerVersion

    def __post_init__(self) -> None:
        try:
            artifact_type = ArtifactType(self.artifact_type)
        except (TypeError, ValueError):
            raise ContractValidationError("unsupported formal Artifact type")
        if artifact_type not in FORMAL_ARTIFACT_TYPES:
            raise ContractValidationError(
                "formal producer request must be Score, Prediction, or Evaluation"
            )
        if not isinstance(self.recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        if (
            not isinstance(self.producer_version, ProducerVersion)
            or not self.producer_version.is_identified
        ):
            raise ContractValidationError(
                "producer_version must identify its producer"
            )
        if self.recipe.fields.get("producer_version") != self.producer_version.to_dict():
            raise ContractValidationError(
                "Recipe producer_version does not match Artifact producer_version"
            )
        payload_type_for(artifact_type)
        object.__setattr__(self, "artifact_type", artifact_type)


@dataclass(frozen=True)
class MaterializedFormalArtifact:
    """Result of exact resolution or one upstream producer invocation."""

    producer_called: bool
    result: FormalStoreResult
    producer_seconds: float

    @property
    def artifact_id(self) -> str:
        return self.result.artifact_id

    @property
    def content_hash(self) -> str:
        return self.result.content_hash


def _resolve_formal_artifact(
    root: Path, request: FormalArtifactRequest
) -> FormalStoreResult | None:
    """Return a verified exact hit, a clean miss, or raise fail-closed."""

    index_path = root / "index.sqlite"
    if not index_path.is_file():
        return None
    index = CacheIndex(index_path)
    index.check_schema()
    explanation = ArtifactResolver(index).explain_exact(
        request.artifact_type, request.recipe
    )
    if explanation.hit and explanation.exact_candidate is not None:
        return FormalArtifactStore(
            root,
            producer_version=request.producer_version,
            index=index,
        ).load_payload_read_only(
            request.artifact_type,
            request.recipe,
            artifact_id=explanation.exact_candidate["artifact_id"],
        )
    if (
        explanation.exact_candidate is None
        and explanation.miss_reasons == ("no_exact_candidate",)
    ):
        return None
    raise CacheResolutionError(
        "exact {0} lookup failed closed: {1}".format(
            request.artifact_type.value, ",".join(explanation.miss_reasons)
        )
    )


def materialize_formal_artifact(
    store_root: Union[str, Path],
    request: FormalArtifactRequest,
    producer: Callable[[], Any],
) -> MaterializedFormalArtifact:
    """Resolve first and invoke the experiment-owned producer only on MISS."""

    if not isinstance(request, FormalArtifactRequest):
        raise ContractValidationError("request must be FormalArtifactRequest")
    if not callable(producer):
        raise ContractValidationError("producer must be callable")
    root = _absolute_store_root(store_root)
    resolved = _resolve_formal_artifact(root, request)
    if resolved is not None:
        return MaterializedFormalArtifact(False, resolved, 0.0)

    started = time.perf_counter()
    payload = producer()
    elapsed = time.perf_counter() - started
    expected_payload_type = payload_type_for(request.artifact_type)
    if not isinstance(payload, expected_payload_type):
        raise ContractValidationError(
            "producer returned the wrong payload class for {0}".format(
                request.artifact_type.value
            )
        )

    store = FormalArtifactStore(root, producer_version=request.producer_version)
    if not store.index.database_path.is_file():
        store.initialize()
    else:
        store.index.check_schema()
    result = store.store_payload(
        request.recipe,
        payload,
        compute_seconds=elapsed,
    )
    return MaterializedFormalArtifact(True, result, elapsed)


__all__ = [
    "FORMAL_ARTIFACT_TYPES",
    "FormalArtifactRequest",
    "MaterializedFormalArtifact",
    "materialize_formal_artifact",
]
