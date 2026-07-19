"""Immutable typed storage for formal Score, Prediction, and Evaluation Artifacts.

The store accepts only already-produced typed payloads.  Dataset/GU/evaluator
execution remains an experiment-layer responsibility.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Mapping, Optional, Tuple, Union

from .canonical import canonicalize, sha256_bytes
from .conflict_resolution import ConflictResolutionLedger
from .contracts import (
    ARTIFACT_ID_PREFIXES,
    ArtifactConflictRecord,
    ArtifactHeader,
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    ProducerVersion,
    RegisterOutcome,
    VerificationStatus,
    build_artifact_id,
    validate_artifact_id,
    validate_sha256,
)
from .errors import (
    ArtifactNotFoundError,
    ArtifactStoreError,
    CacheResolutionError,
    CacheV2Error,
    ContractValidationError,
    PathValidationError,
)
from .formal_artifacts import payload_type_for
from .paths import normalize_semantic_path
from .resolver import ArtifactResolver
from .store import (
    CONFLICT_MARKER_VERSION,
    SELECTION_PAYLOAD_SCHEMA,
    SELECTION_PAYLOAD_VERSION,
    ArtifactConflictError,
    ArtifactIntegrityError,
    ArtifactStore,
    SelectionPayload,
    _CreatedFile,
    _parse_canonical_plain_json,
    _plain_json_bytes,
)


@dataclass(frozen=True)
class FormalStoreResult:
    hit: bool
    outcome: str
    artifact_id: str
    content_hash: str
    semantic_path: str
    payload: Any
    producer_called: bool = False
    miss_reasons: Tuple[str, ...] = ()


class FormalArtifactStore(ArtifactStore):
    """Typed exact-only store layered on the accepted Selection primitives."""

    @staticmethod
    def _formal_type(value: Union[ArtifactType, str]) -> ArtifactType:
        try:
            artifact_type = ArtifactType(value)
        except (TypeError, ValueError):
            raise ContractValidationError("unsupported formal Artifact type")
        if artifact_type is ArtifactType.SELECTION:
            raise ContractValidationError(
                "Selection must use the accepted Selection Artifact store API"
            )
        payload_type_for(artifact_type)
        return artifact_type

    def _validate_recipe_producer(self, recipe: ArtifactRecipe) -> None:
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        if recipe.fields.get("producer_version") != self.producer_version.to_dict():
            raise ContractValidationError(
                "Recipe producer_version does not match ArtifactStore producer_version"
            )

    def _typed_recipe_lock(self, artifact_type: ArtifactType, recipe: ArtifactRecipe) -> Any:
        return self._exclusive_lock(
            "{0}-{1}".format(artifact_type.value, recipe.recipe_hash)
        )

    def _typed_conflict_marker_paths(
        self, artifact_type: ArtifactType, recipe_hash: str
    ) -> Tuple[str, Path]:
        type_value = ArtifactType(artifact_type)
        recipe_value = validate_sha256(recipe_hash, "recipe_hash")
        semantic = normalize_semantic_path(
            "conflict_markers/{0}/{1}/marker.json".format(
                type_value.value, recipe_value
            )
        )
        marker_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts), "conflict marker"
        )
        return semantic, marker_path

    def _inspect_typed_conflict_marker(
        self, artifact_type: ArtifactType, recipe_hash: str
    ) -> Optional[Dict[str, Any]]:
        type_value = ArtifactType(artifact_type)
        recipe_value = validate_sha256(recipe_hash, "recipe_hash")
        raw_directories = (
            self.root / "conflict_markers",
            self.root / "conflict_markers" / type_value.value,
            self.root / "conflict_markers" / type_value.value / recipe_value,
        )
        for position, raw_directory in enumerate(raw_directories):
            if raw_directory.is_symlink():
                raise CacheResolutionError(
                    "conflict marker directory is a symlink: {0}".format(raw_directory)
                )
            try:
                directory = self._safe_output_path(
                    raw_directory, "conflict marker directory"
                )
            except PathValidationError as exc:
                raise CacheResolutionError(
                    "conflict marker directory escapes ArtifactStore root: {0}".format(
                        exc
                    )
                )
            if not directory.exists():
                return None
            if not directory.is_dir():
                raise CacheResolutionError(
                    "conflict marker directory is not a directory: {0}".format(
                        directory
                    )
                )
            if position < 2:
                continue
            entries = list(directory.iterdir())
            if len(entries) != 1 or entries[0].name != "marker.json":
                raise CacheResolutionError(
                    "conflict marker recipe directory is incomplete or unexpected"
                )
            if entries[0].is_symlink():
                raise CacheResolutionError("conflict marker must not be a symlink")

        semantic, marker_path = self._typed_conflict_marker_paths(
            type_value, recipe_value
        )
        if marker_path.is_symlink() or not marker_path.is_file():
            raise CacheResolutionError(
                "conflict marker is not a regular file: {0}".format(semantic)
            )
        try:
            value = _parse_canonical_plain_json(
                marker_path.read_bytes(), "conflict marker"
            )
        except ArtifactIntegrityError as exc:
            raise CacheResolutionError("conflict marker is corrupt: {0}".format(exc))
        expected = {
            "artifact_type",
            "existing_artifact_id",
            "existing_content_hash",
            "marker_version",
            "observed_content_hash",
            "reason",
            "recipe_hash",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise CacheResolutionError("conflict marker schema is invalid")
        try:
            existing_id = validate_artifact_id(
                value["existing_artifact_id"], "existing_artifact_id"
            )
            existing_hash = validate_sha256(
                value["existing_content_hash"], "existing_content_hash"
            )
            observed_hash = validate_sha256(
                value["observed_content_hash"], "observed_content_hash"
            )
        except CacheV2Error as exc:
            raise CacheResolutionError(
                "conflict marker contract is invalid: {0}".format(exc)
            )
        prefix = ARTIFACT_ID_PREFIXES[type_value] + "_"
        if (
            value["marker_version"] != CONFLICT_MARKER_VERSION
            or value["artifact_type"] != type_value.value
            or value["recipe_hash"] != recipe_value
            or value["reason"] != "content_conflict"
            or not existing_id.startswith(prefix)
            or existing_hash == observed_hash
        ):
            raise CacheResolutionError("conflict marker identity is invalid")
        return value

    def _write_typed_conflict_marker(
        self,
        artifact_type: ArtifactType,
        recipe: ArtifactRecipe,
        existing_artifact_id: str,
        existing_content_hash: str,
        observed_content_hash: str,
    ) -> str:
        type_value = self._formal_type(artifact_type)
        existing = self._inspect_typed_conflict_marker(
            type_value, recipe.recipe_hash
        )
        semantic, marker_path = self._typed_conflict_marker_paths(
            type_value, recipe.recipe_hash
        )
        if existing is not None:
            return semantic
        marker = {
            "artifact_type": type_value.value,
            "existing_artifact_id": validate_artifact_id(
                existing_artifact_id, "existing_artifact_id"
            ),
            "existing_content_hash": validate_sha256(
                existing_content_hash, "existing_content_hash"
            ),
            "marker_version": CONFLICT_MARKER_VERSION,
            "observed_content_hash": validate_sha256(
                observed_content_hash, "observed_content_hash"
            ),
            "reason": "content_conflict",
            "recipe_hash": recipe.recipe_hash,
        }
        if marker["existing_content_hash"] == marker["observed_content_hash"]:
            raise ContractValidationError(
                "identical content must not create a conflict marker"
            )
        marker_path.parent.mkdir(parents=True, exist_ok=False)
        marker_path = self._safe_output_path(marker_path, "conflict marker")
        created = self._atomic_write_once(marker_path, _plain_json_bytes(marker))
        if created is not None:
            self._sync_directory(marker_path.parent)
        validated = self._inspect_typed_conflict_marker(
            type_value, recipe.recipe_hash
        )
        if validated is None:
            raise CacheResolutionError("conflict marker was not durably published")
        return semantic

    def _assert_typed_no_conflict_marker(
        self, artifact_type: ArtifactType, recipe_hash: str
    ) -> None:
        type_value = ArtifactType(artifact_type)
        marker = self._inspect_typed_conflict_marker(type_value, recipe_hash)
        if marker is None:
            return
        conflicts = self.index.conflicts(
            artifact_type=type_value, recipe_hash=recipe_hash
        )
        if not conflicts:
            raise CacheResolutionError(
                "durable conflict marker has no indexed conflict and blocks exact hit"
            )
        resolved, unresolved = ConflictResolutionLedger(self.index).classify(conflicts)
        marker_match = any(
            item["conflict"].get("existing_artifact_id")
            == marker["existing_artifact_id"]
            and item["conflict"].get("existing_content_hash")
            == marker["existing_content_hash"]
            and item["conflict"].get("observed_content_hash")
            == marker["observed_content_hash"]
            for item in resolved
        )
        if unresolved or not marker_match:
            raise CacheResolutionError(
                "durable conflict marker blocks exact {0} hit for Recipe {1}".format(
                    type_value.value, recipe_hash
                )
            )

    def _typed_formal_paths(
        self, artifact_type: ArtifactType, artifact_id: str, extension: str
    ) -> Tuple[str, Path, Path]:
        type_value = self._formal_type(artifact_type)
        extension_value = extension.strip().lower()
        if extension_value not in ("json", "npz"):
            raise ContractValidationError("unsupported formal payload extension")
        semantic = normalize_semantic_path(
            "artifacts/{0}/{1}/payload.{2}".format(
                type_value.value, artifact_id, extension_value
            )
        )
        payload_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts), "formal payload"
        )
        return semantic, payload_path, payload_path.with_name("header.json")

    def _typed_sidecar_bytes(
        self, header: ArtifactHeader, payload_schema: str, payload_version: int, payload_size: int
    ) -> bytes:
        return _plain_json_bytes(
            {
                "artifact_header": header.to_dict(),
                "payload_contract": {
                    "schema": payload_schema,
                    "version": payload_version,
                    "size_bytes": payload_size,
                },
            }
        )

    def _typed_header_for_payload(
        self,
        recipe: ArtifactRecipe,
        payload: Any,
        semantic_path: str,
        compute_seconds: float,
        status: ArtifactStatus = ArtifactStatus.VALID,
    ) -> ArtifactHeader:
        payload_bytes = payload.canonical_bytes
        return ArtifactHeader(
            artifact_type=payload.artifact_type,
            recipe=recipe,
            content_hash=sha256_bytes(payload_bytes),
            producer_version=self.producer_version,
            status=status,
            verification_status=VerificationStatus.VERIFIED,
            semantic_path=semantic_path,
            compute_seconds=compute_seconds,
            metadata={
                "payload_schema": payload.payload_schema,
                "payload_version": payload.payload_version,
                "payload_size_bytes": len(payload_bytes),
            },
        )

    @staticmethod
    def _expected_parent_type(relation: str) -> ArtifactType:
        mapping = {
            "selection_input": ArtifactType.SELECTION,
            "prediction_input": ArtifactType.PREDICTION,
        }
        try:
            return mapping[relation]
        except KeyError:
            raise ContractValidationError(
                "unsupported formal Artifact dependency relation: {0}".format(relation)
            )

    def _load_verified_dependency_payload(
        self, parent: Mapping[str, Any], expected_type: ArtifactType
    ) -> Any:
        """Verify dependency bytes/header without requiring its producer callback."""

        type_value = ArtifactType(expected_type)
        semantic = parent.get("semantic_path")
        if not isinstance(semantic, str):
            raise ArtifactIntegrityError("dependency has no semantic_path")
        semantic = normalize_semantic_path(semantic)
        try:
            payload_path = self._safe_output_path(
                self.root.joinpath(*PurePosixPath(semantic).parts),
                "dependency payload",
            )
            header_path = self._safe_output_path(
                payload_path.with_name("header.json"),
                "dependency Artifact header",
            )
        except PathValidationError as exc:
            raise ArtifactIntegrityError(
                "dependency path escapes ArtifactStore root: {0}".format(exc)
            )
        if not payload_path.is_file() or not header_path.is_file():
            raise ArtifactIntegrityError(
                "dependency payload or header is missing: {0}".format(
                    parent.get("artifact_id")
                )
            )

        header_value = _parse_canonical_plain_json(
            header_path.read_bytes(), "dependency Artifact header sidecar"
        )
        if not isinstance(header_value, dict) or set(header_value) != {
            "artifact_header",
            "payload_contract",
        }:
            raise ArtifactIntegrityError(
                "dependency Artifact header sidecar schema is invalid"
            )
        artifact_header = header_value["artifact_header"]
        payload_contract = header_value["payload_contract"]
        if not isinstance(artifact_header, dict) or not isinstance(
            payload_contract, dict
        ):
            raise ArtifactIntegrityError(
                "dependency Artifact header sidecar sections are invalid"
            )
        expected_artifact_header_keys = {
            "header_version",
            "artifact_id",
            "artifact_type",
            "recipe",
            "recipe_hash",
            "content_hash",
            "producer_version",
            "status",
            "verification_status",
            "semantic_path",
            "compute_seconds",
            "created_at",
            "metadata",
        }
        if set(artifact_header) != expected_artifact_header_keys:
            raise ArtifactIntegrityError(
                "dependency Artifact header fields are invalid"
            )

        if type_value is ArtifactType.SELECTION:
            payload_class = SelectionPayload
            expected_schema = SELECTION_PAYLOAD_SCHEMA
            expected_version = SELECTION_PAYLOAD_VERSION
            expected_extension = ".json"
        else:
            payload_class = payload_type_for(type_value)
            expected_schema = payload_class.payload_schema
            expected_version = payload_class.contract_version
            expected_extension = "." + payload_class.file_extension
        if payload_path.suffix != expected_extension:
            raise ArtifactIntegrityError("dependency payload extension is invalid")
        if (
            set(payload_contract) != {"schema", "version", "size_bytes"}
            or payload_contract.get("schema") != expected_schema
            or payload_contract.get("version") != expected_version
            or isinstance(payload_contract.get("size_bytes"), bool)
            or not isinstance(payload_contract.get("size_bytes"), int)
            or payload_contract["size_bytes"] < 0
        ):
            raise ArtifactIntegrityError(
                "dependency payload size/schema contract is invalid"
            )
        expected_metadata = canonicalize(
            {
                "payload_schema": expected_schema,
                "payload_version": expected_version,
                "payload_size_bytes": payload_contract["size_bytes"],
            }
        )
        if artifact_header.get("metadata") != expected_metadata:
            raise ArtifactIntegrityError(
                "dependency payload contract does not match header metadata"
            )

        expected_header_fields = {
            "artifact_id": parent.get("artifact_id"),
            "artifact_type": type_value.value,
            "recipe": parent.get("recipe"),
            "recipe_hash": parent.get("recipe_hash"),
            "content_hash": parent.get("content_hash"),
            "status": parent.get("status"),
            "verification_status": parent.get("verification_status"),
            "semantic_path": semantic,
            "compute_seconds": parent.get("compute_seconds"),
            "created_at": parent.get("created_at"),
            "header_version": parent.get("header_version"),
            "metadata": parent.get("metadata"),
        }
        for name, expected in expected_header_fields.items():
            if artifact_header.get(name) != expected:
                raise ArtifactIntegrityError(
                    "dependency Artifact header {0} does not match index".format(
                        name
                    )
                )
        producer_value = artifact_header.get("producer_version")
        if not isinstance(producer_value, dict) or canonicalize(
            producer_value
        ) != parent.get("producer_version"):
            raise ArtifactIntegrityError(
                "dependency Artifact producer_version does not match index"
            )

        before = payload_path.stat()
        payload_bytes = payload_path.read_bytes()
        after = payload_path.stat()
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise ArtifactIntegrityError("dependency payload changed while being read")
        if len(payload_bytes) != after.st_size:
            raise ArtifactIntegrityError("dependency payload size changed while being read")
        if len(payload_bytes) != payload_contract["size_bytes"]:
            raise ArtifactIntegrityError("dependency payload size does not match header")
        if sha256_bytes(payload_bytes) != parent.get("content_hash"):
            raise ArtifactIntegrityError("dependency payload content hash mismatch")
        payload = payload_class.from_bytes(payload_bytes)

        dependencies = tuple(getattr(payload, "dependencies", ()))
        expected_parents = sorted(parent_id for _, parent_id in dependencies)
        if self.index.parents(parent["artifact_id"]) != expected_parents:
            raise ArtifactIntegrityError(
                "indexed dependencies do not match dependency payload"
            )
        if dependencies:
            self._validate_dependencies(payload)
        return payload

    def _validate_dependencies(self, payload: Any) -> Tuple[Tuple[str, str], ...]:
        pairs = tuple(payload.dependencies)
        if len(set(pairs)) != len(pairs):
            raise ContractValidationError("formal Artifact dependencies contain duplicates")
        parent_ids = [parent_id for _, parent_id in pairs]
        if len(set(parent_ids)) != len(parent_ids):
            raise ContractValidationError(
                "formal Artifact dependencies repeat a parent Artifact"
            )
        resolver = ArtifactResolver(self.index)
        ledger = ConflictResolutionLedger(self.index)
        for relation, parent_id in pairs:
            expected_type = self._expected_parent_type(relation)
            try:
                parent = self.index.get_artifact(parent_id)
            except ArtifactNotFoundError as exc:
                raise CacheResolutionError(
                    "dependency Artifact is missing: {0}".format(parent_id)
                ) from exc
            if parent.get("artifact_type") != expected_type.value:
                raise CacheResolutionError(
                    "dependency {0} has wrong Artifact type".format(parent_id)
                )
            if (
                parent.get("status") != ArtifactStatus.VALID.value
                or parent.get("verification_status")
                != VerificationStatus.VERIFIED.value
            ):
                raise CacheResolutionError(
                    "dependency {0} is not valid and verified".format(parent_id)
                )
            conflicts = self.index.conflicts(
                artifact_type=expected_type, recipe_hash=parent["recipe_hash"]
            )
            _, unresolved = ledger.classify(conflicts)
            if unresolved:
                raise CacheResolutionError(
                    "dependency {0} has an unresolved conflict".format(parent_id)
                )
            self._assert_typed_no_conflict_marker(
                expected_type, parent["recipe_hash"]
            )
            issues = resolver._dependency_issues(parent_id)
            if issues:
                raise CacheResolutionError(
                    "dependency {0} has unhealthy ancestors".format(parent_id)
                )
            parent_payload = self._load_verified_dependency_payload(
                parent, expected_type
            )
            if relation == "selection_input":
                if (
                    parent_payload.ordered_nodes_hash
                    != payload.metadata["selected_nodes_hash"]
                    or parent_payload.graph_fingerprint
                    != payload.graph_fingerprint
                    or parent_payload.node_id_space != payload.node_id_space
                ):
                    raise ArtifactIntegrityError(
                        "Prediction payload identity does not match Selection dependency"
                    )
            elif relation == "prediction_input":
                if parent_payload.graph_fingerprint != payload.graph_fingerprint:
                    raise ArtifactIntegrityError(
                        "Evaluation graph identity does not match Prediction dependency"
                    )
        return pairs

    def _quarantine_typed_observation(
        self, recipe: ArtifactRecipe, payload: Any, compute_seconds: float
    ) -> Tuple[str, ArtifactHeader]:
        artifact_type = self._formal_type(payload.artifact_type)
        content_hash = payload.content_hash
        semantic = normalize_semantic_path(
            "quarantine/{0}/{1}/{2}-{3}/payload.{4}".format(
                artifact_type.value,
                recipe.recipe_hash[:16],
                content_hash[:16],
                uuid.uuid4().hex,
                payload.file_extension,
            )
        )
        payload_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts),
            "quarantine payload",
        )
        header = self._typed_header_for_payload(
            recipe,
            payload,
            semantic,
            compute_seconds,
            status=ArtifactStatus.CONFLICT,
        )
        created_payload: Optional[_CreatedFile] = None
        created_header: Optional[_CreatedFile] = None
        try:
            created_payload = self._atomic_write_once(
                payload_path, payload.canonical_bytes
            )
            created_header = self._atomic_write_once(
                payload_path.with_name("header.json"),
                self._typed_sidecar_bytes(
                    header,
                    payload.payload_schema,
                    payload.payload_version,
                    len(payload.canonical_bytes),
                ),
            )
        except Exception:
            self._cleanup_created_file(created_header)
            self._cleanup_created_file(created_payload)
            raise
        return semantic, header

    def _load_typed_candidate(
        self,
        candidate: Mapping[str, Any],
        recipe: ArtifactRecipe,
        artifact_type: ArtifactType,
        miss_reasons: Tuple[str, ...] = (),
    ) -> FormalStoreResult:
        type_value = self._formal_type(artifact_type)
        payload_class = payload_type_for(type_value)
        if candidate.get("artifact_type") != type_value.value:
            raise ArtifactIntegrityError("indexed candidate has wrong Artifact type")
        if candidate.get("recipe_hash") != recipe.recipe_hash:
            raise ArtifactIntegrityError("indexed candidate Recipe hash changed")
        if candidate.get("status") != ArtifactStatus.VALID.value:
            raise ArtifactIntegrityError("indexed candidate is not valid")
        if candidate.get("verification_status") != VerificationStatus.VERIFIED.value:
            raise ArtifactIntegrityError("indexed candidate is not verified")
        semantic = candidate.get("semantic_path")
        if not isinstance(semantic, str):
            raise ArtifactIntegrityError("indexed candidate has no semantic_path")
        semantic = normalize_semantic_path(semantic)
        try:
            payload_path = self._safe_output_path(
                self.root.joinpath(*PurePosixPath(semantic).parts),
                "indexed formal payload",
            )
            header_path = self._safe_output_path(
                payload_path.with_name("header.json"), "indexed Artifact header"
            )
        except PathValidationError as exc:
            raise ArtifactIntegrityError(
                "indexed formal path escapes ArtifactStore root: {0}".format(exc)
            )
        if payload_path.suffix != "." + payload_class.file_extension:
            raise ArtifactIntegrityError("indexed formal payload extension is invalid")
        if not payload_path.is_file() or not header_path.is_file():
            raise ArtifactIntegrityError("indexed formal payload or header is missing")

        header_value = _parse_canonical_plain_json(
            header_path.read_bytes(), "Artifact header sidecar"
        )
        if not isinstance(header_value, dict) or set(header_value) != {
            "artifact_header",
            "payload_contract",
        }:
            raise ArtifactIntegrityError("Artifact header sidecar schema is invalid")
        artifact_header = header_value["artifact_header"]
        payload_contract = header_value["payload_contract"]
        if not isinstance(artifact_header, dict) or not isinstance(payload_contract, dict):
            raise ArtifactIntegrityError("Artifact header sidecar sections are invalid")
        if (
            set(payload_contract) != {"schema", "version", "size_bytes"}
            or payload_contract.get("schema") != payload_class.payload_schema
            or payload_contract.get("version") != payload_class.contract_version
            or isinstance(payload_contract.get("size_bytes"), bool)
            or not isinstance(payload_contract.get("size_bytes"), int)
            or payload_contract["size_bytes"] < 0
        ):
            raise ArtifactIntegrityError("payload size/schema contract is invalid")
        producer_value = artifact_header.get("producer_version")
        if not isinstance(producer_value, dict) or set(producer_value) != {
            "semantic_version",
            "source_fingerprint",
        }:
            raise ArtifactIntegrityError(
                "Artifact header producer_version contract is invalid"
            )
        expected_metadata = {
            "payload_schema": payload_class.payload_schema,
            "payload_version": payload_class.contract_version,
            "payload_size_bytes": payload_contract["size_bytes"],
        }
        if artifact_header.get("metadata") != canonicalize(expected_metadata):
            raise ArtifactIntegrityError(
                "payload size does not match Artifact header metadata"
            )
        try:
            producer_version = ProducerVersion(**producer_value)
            versioned_header = ArtifactHeader(
                header_version=artifact_header["header_version"],
                artifact_id=artifact_header["artifact_id"],
                artifact_type=artifact_header["artifact_type"],
                recipe=recipe,
                content_hash=artifact_header["content_hash"],
                producer_version=producer_version,
                status=artifact_header["status"],
                verification_status=artifact_header["verification_status"],
                semantic_path=artifact_header["semantic_path"],
                compute_seconds=artifact_header["compute_seconds"],
                created_at=artifact_header["created_at"],
                metadata=expected_metadata,
            )
        except (CacheV2Error, KeyError, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError(
                "Artifact header sidecar violates versioned contract: {0}".format(exc)
            )
        if versioned_header.to_dict() != artifact_header:
            raise ArtifactIntegrityError(
                "Artifact header sidecar fields are not self-consistent"
            )
        index_expectations = {
            "artifact_id": versioned_header.artifact_id,
            "artifact_type": versioned_header.artifact_type.value,
            "recipe_hash": versioned_header.recipe_hash,
            "content_hash": versioned_header.content_hash,
            "semantic_path": versioned_header.semantic_path,
            "status": versioned_header.status.value,
            "verification_status": versioned_header.verification_status.value,
            "compute_seconds": versioned_header.compute_seconds,
            "created_at": versioned_header.created_at,
            "header_version": versioned_header.header_version,
        }
        for key, expected in index_expectations.items():
            if candidate.get(key) != expected:
                raise ArtifactIntegrityError(
                    "Artifact header sidecar {0} does not match index".format(key)
                )
        if candidate.get("recipe") != recipe.canonical_form:
            raise ArtifactIntegrityError(
                "Artifact header Recipe does not match indexed recipe_json"
            )
        if candidate.get("producer_version") != canonicalize(
            producer_version.to_dict()
        ):
            raise ArtifactIntegrityError(
                "Artifact header producer_version does not match index"
            )
        if candidate.get("metadata") != canonicalize(expected_metadata):
            raise ArtifactIntegrityError("Artifact header metadata does not match index")

        before = payload_path.stat()
        payload_bytes = payload_path.read_bytes()
        after = payload_path.stat()
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise ArtifactIntegrityError("formal payload changed while being read")
        if len(payload_bytes) != after.st_size:
            raise ArtifactIntegrityError("formal payload size changed while being read")
        if len(payload_bytes) != payload_contract["size_bytes"]:
            raise ArtifactIntegrityError("formal payload size does not match header")
        observed_hash = sha256_bytes(payload_bytes)
        if observed_hash != candidate.get("content_hash"):
            raise ArtifactIntegrityError("formal payload content hash mismatch")
        payload = payload_class.from_bytes(payload_bytes)
        payload.validate_against(recipe)
        dependencies = self._validate_dependencies(payload)
        expected_parents = sorted(parent_id for _, parent_id in dependencies)
        if self.index.parents(candidate["artifact_id"]) != expected_parents:
            raise ArtifactIntegrityError(
                "indexed dependencies do not match formal payload dependencies"
            )
        return FormalStoreResult(
            hit=True,
            outcome="hit",
            artifact_id=candidate["artifact_id"],
            content_hash=observed_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def _write_typed_formal(
        self,
        recipe: ArtifactRecipe,
        payload: Any,
        compute_seconds: float,
        miss_reasons: Tuple[str, ...],
    ) -> FormalStoreResult:
        artifact_type = self._formal_type(payload.artifact_type)
        dependencies = self._validate_dependencies(payload)
        artifact_id = build_artifact_id(
            artifact_type, recipe.recipe_hash, payload.content_hash
        )
        semantic, payload_path, header_path = self._typed_formal_paths(
            artifact_type, artifact_id, payload.file_extension
        )
        header = self._typed_header_for_payload(
            recipe, payload, semantic, compute_seconds
        )
        payload_bytes = payload.canonical_bytes
        created_payload: Optional[_CreatedFile] = None
        created_header: Optional[_CreatedFile] = None
        identical_artifact_id: Optional[str] = None
        conflict_error: Optional[ArtifactConflictError] = None
        try:
            with self.index.transaction() as writer:
                existing = writer.connection.execute(
                    """
                    SELECT artifact_id, content_hash FROM artifacts
                    WHERE artifact_type = ? AND recipe_hash = ?
                    """,
                    (artifact_type.value, recipe.recipe_hash),
                ).fetchone()
                if existing is not None:
                    existing_id = str(existing["artifact_id"])
                    existing_hash = str(existing["content_hash"])
                    if existing_hash == header.content_hash:
                        identical_artifact_id = existing_id
                    else:
                        self._write_typed_conflict_marker(
                            artifact_type,
                            recipe,
                            existing_id,
                            existing_hash,
                            header.content_hash,
                        )
                        quarantine_path, observed_header = (
                            self._quarantine_typed_observation(
                                recipe, payload, compute_seconds
                            )
                        )
                        conflict = ArtifactConflictRecord(
                            artifact_type=artifact_type,
                            recipe_hash=recipe.recipe_hash,
                            existing_artifact_id=existing_id,
                            existing_content_hash=existing_hash,
                            observed_content_hash=observed_header.content_hash,
                            quarantine_path=quarantine_path,
                            metadata={
                                "observed_artifact_id": observed_header.artifact_id
                            },
                        )
                        writer.record_conflict(conflict)
                        conflict_error = ArtifactConflictError(
                            conflict.conflict_id, quarantine_path
                        )
                else:
                    created_payload = self._atomic_write_once(
                        payload_path, payload_bytes
                    )
                    created_header = self._atomic_write_once(
                        header_path,
                        self._typed_sidecar_bytes(
                            header,
                            payload.payload_schema,
                            payload.payload_version,
                            len(payload_bytes),
                        ),
                    )
                    registration = writer.register_artifact(header)
                    if registration.outcome != RegisterOutcome.CREATED:
                        raise ArtifactStoreError(
                            "unexpected registration outcome under write lock: {0}".format(
                                registration.outcome.value
                            )
                        )
                    for relation, parent_id in dependencies:
                        writer.add_dependency(
                            parent_id,
                            header.artifact_id,
                            relation=relation,
                        )
        except Exception:
            self._cleanup_created_file(created_header)
            self._cleanup_created_file(created_payload)
            raise

        if conflict_error is not None:
            self._trace(
                "artifact_conflict",
                artifact_type=artifact_type.value,
                recipe_hash=recipe.recipe_hash,
                conflict_id=conflict_error.conflict_id,
                quarantine_path=conflict_error.quarantine_path,
            )
            raise conflict_error
        if identical_artifact_id is not None:
            candidate = self.index.get_artifact(identical_artifact_id)
            loaded = self._load_typed_candidate(
                candidate, recipe, artifact_type, miss_reasons=miss_reasons
            )
            return FormalStoreResult(
                hit=True,
                outcome=RegisterOutcome.IDENTICAL.value,
                artifact_id=loaded.artifact_id,
                content_hash=loaded.content_hash,
                semantic_path=loaded.semantic_path,
                payload=loaded.payload,
                producer_called=False,
                miss_reasons=miss_reasons,
            )
        self._trace(
            "artifact_registered",
            artifact_type=artifact_type.value,
            recipe_hash=recipe.recipe_hash,
            artifact_id=header.artifact_id,
            outcome=RegisterOutcome.CREATED.value,
            semantic_path=semantic,
        )
        return FormalStoreResult(
            hit=False,
            outcome=RegisterOutcome.CREATED.value,
            artifact_id=header.artifact_id,
            content_hash=header.content_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def store_payload(
        self,
        recipe: ArtifactRecipe,
        payload: Any,
        *,
        compute_seconds: float = 0.0,
    ) -> FormalStoreResult:
        self._ensure_initialized()
        artifact_type = self._formal_type(getattr(payload, "artifact_type", None))
        payload_class = payload_type_for(artifact_type)
        if not isinstance(payload, payload_class):
            raise ContractValidationError("payload class does not match Artifact type")
        self._validate_recipe_producer(recipe)
        payload.validate_against(recipe)
        with self._typed_recipe_lock(artifact_type, recipe):
            self._assert_typed_no_conflict_marker(
                artifact_type, recipe.recipe_hash
            )
            explanation = ArtifactResolver(self.index).explain_exact(
                artifact_type, recipe
            )
            if (
                not explanation.hit
                and (
                    explanation.exact_candidate is not None
                    or explanation.miss_reasons != ("no_exact_candidate",)
                )
            ):
                raise CacheResolutionError(
                    "exact {0} lookup failed closed: {1}".format(
                        artifact_type.value, ",".join(explanation.miss_reasons)
                    )
                )
            result = self._write_typed_formal(
                recipe,
                payload,
                compute_seconds,
                explanation.miss_reasons,
            )
            self._trace(
                "upstream_formal_artifact_stored",
                artifact_type=artifact_type.value,
                recipe_hash=recipe.recipe_hash,
                artifact_id=result.artifact_id,
                content_hash=result.content_hash,
                outcome=result.outcome,
            )
            return result

    def load_payload_read_only(
        self,
        artifact_type: Union[ArtifactType, str],
        recipe: ArtifactRecipe,
        *,
        artifact_id: Optional[str] = None,
    ) -> FormalStoreResult:
        self._ensure_initialized()
        type_value = self._formal_type(artifact_type)
        self._validate_recipe_producer(recipe)
        self._assert_typed_no_conflict_marker(type_value, recipe.recipe_hash)
        before = ArtifactResolver(self.index).explain_exact(type_value, recipe)
        if not before.hit or before.exact_candidate is None:
            raise CacheResolutionError(
                "exact {0} Artifact is not resolvable: {1}".format(
                    type_value.value, ",".join(before.miss_reasons)
                )
            )
        if artifact_id is not None and before.exact_candidate.get("artifact_id") != artifact_id:
            raise CacheResolutionError(
                "exact {0} Artifact ID does not match requested Artifact".format(
                    type_value.value
                )
            )
        result = self._load_typed_candidate(
            before.exact_candidate,
            recipe,
            type_value,
            miss_reasons=before.miss_reasons,
        )
        self._assert_typed_no_conflict_marker(type_value, recipe.recipe_hash)
        after = ArtifactResolver(self.index).explain_exact(type_value, recipe)
        if (
            not after.hit
            or after.exact_candidate is None
            or after.exact_candidate.get("artifact_id") != result.artifact_id
        ):
            raise CacheResolutionError(
                "exact {0} resolution changed during read".format(type_value.value)
            )
        return result


__all__ = ["FormalArtifactStore", "FormalStoreResult"]
