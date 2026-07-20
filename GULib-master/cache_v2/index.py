"""Fail-closed SQLite access for the Cache V2.1 metadata index."""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Optional, Union

from .canonical import TYPE_TAG, canonical_json
from .contracts import (
    HEADER_VERSION,
    RECIPE_VERSION,
    ArtifactConflictRecord,
    ArtifactHeader,
    ArtifactStatus,
    ArtifactType,
    ConsumerRef,
    DependencyRecord,
    LegacySourceRecord,
    RegisterOutcome,
    RegistrationResult,
    VerificationStatus,
    build_artifact_id,
    validate_sha256,
)
from .errors import (
    ArtifactNotFoundError,
    CacheIndexError,
    DependencyCycleError,
    IndexNotFoundError,
    PathValidationError,
    SchemaVersionError,
)
from .paths import normalize_semantic_path
from .schema import (
    REQUIRED_TABLES,
    SCHEMA_FINGERPRINT,
    SCHEMA_FINGERPRINT_KEY,
    SCHEMA_VERSION,
    SCHEMA_VERSION_KEY,
    create_schema,
    current_schema_fingerprint,
    utc_now_iso,
)


MAX_RECIPE_JSON_BYTES = 262144
MAX_SMALL_JSON_BYTES = 65536


def _enum_value(value: Any) -> Any:
    return getattr(value, "value", value)


def _bounded_json(text: str, label: str, limit: int) -> str:
    if not isinstance(text, str):
        raise CacheIndexError("{0} must be JSON text".format(label))
    try:
        json.loads(text)
    except (TypeError, ValueError) as exc:
        raise CacheIndexError("{0} is not valid JSON: {1}".format(label, exc))
    if len(text.encode("utf-8")) > limit:
        raise CacheIndexError(
            "{0} exceeds the metadata-only limit of {1} bytes".format(label, limit)
        )
    return text


def _parse_canonical_json(text: str, label: str) -> Any:
    if not isinstance(text, str):
        raise CacheIndexError("{0} must be JSON text".format(label))
    try:
        parsed = json.loads(text)
    except (TypeError, ValueError) as exc:
        raise CacheIndexError("index contains invalid {0}: {1}".format(label, exc))
    normalized = json.dumps(
        parsed,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    if normalized != text:
        raise CacheIndexError("index contains non-canonical {0}".format(label))
    return parsed


def _tagged_mapping(value: Any, label: str) -> Dict[str, Any]:
    if not isinstance(value, dict) or value.get(TYPE_TAG) != "mapping":
        raise CacheIndexError("{0} must be a canonical tagged mapping".format(label))
    if set(value) != {TYPE_TAG, "items"} or not isinstance(value.get("items"), list):
        raise CacheIndexError("{0} has an invalid canonical mapping shape".format(label))
    decoded: Dict[str, Any] = {}
    for item in value["items"]:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
            or item[0] in decoded
        ):
            raise CacheIndexError("{0} has invalid canonical mapping items".format(label))
        decoded[item[0]] = item[1]
    return decoded


def _validate_utc_timestamp(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise CacheIndexError("{0} must be an ISO-8601 UTC string".format(label))
    parse_value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(parse_value)
    except ValueError as exc:
        raise CacheIndexError("{0} is invalid: {1}".format(label, exc))
    if (
        parsed.tzinfo is None
        or parsed.utcoffset() is None
        or parsed.utcoffset().total_seconds() != 0
    ):
        raise CacheIndexError("{0} must be normalized to UTC".format(label))


def _validate_artifact_record(
    record: Dict[str, Any],
    recipe_value: Any,
    producer_value: Any,
    metadata_value: Any,
) -> None:
    """Revalidate DB rows before they can participate in an exact hit."""

    try:
        artifact_type = ArtifactType(record["artifact_type"])
        status = ArtifactStatus(record["status"])
        verification = VerificationStatus(record["verification_status"])
        recipe_hash = validate_sha256(record["recipe_hash"], "recipe_hash")
        content_hash = validate_sha256(record["content_hash"], "content_hash")
    except (KeyError, TypeError, ValueError) as exc:
        raise CacheIndexError("invalid Artifact row contract: {0}".format(exc))

    computed_recipe_hash = hashlib.sha256(
        record["recipe_json"].encode("utf-8")
    ).hexdigest()
    if computed_recipe_hash != recipe_hash:
        raise CacheIndexError("Artifact recipe_json does not match recipe_hash")

    recipe_mapping = _tagged_mapping(recipe_value, "recipe_json")
    if recipe_mapping.get("recipe_version") != RECIPE_VERSION:
        raise CacheIndexError("Artifact recipe_json has an unsupported recipe_version")
    _tagged_mapping(recipe_mapping.get("fields"), "recipe_json.fields")
    producer_mapping = _tagged_mapping(producer_value, "producer_version_json")
    _tagged_mapping(metadata_value, "metadata_json")

    semantic_version = producer_mapping.get("semantic_version")
    source_fingerprint = producer_mapping.get("source_fingerprint")
    for label, value in (
        ("semantic_version", semantic_version),
        ("source_fingerprint", source_fingerprint),
    ):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise CacheIndexError("producer {0} must be a non-empty string or null".format(label))

    expected_id = build_artifact_id(artifact_type, recipe_hash, content_hash)
    if record.get("artifact_id") != expected_id:
        raise CacheIndexError("Artifact artifact_id does not match type/Recipe/content hashes")
    if record.get("header_version") != HEADER_VERSION:
        raise CacheIndexError("Artifact header_version is unsupported")

    semantic_path = record.get("semantic_path")
    if semantic_path is not None:
        try:
            normalized_path = normalize_semantic_path(semantic_path)
        except Exception as exc:
            raise CacheIndexError("Artifact semantic_path is invalid: {0}".format(exc))
        if normalized_path != semantic_path:
            raise CacheIndexError("Artifact semantic_path is not canonical")

    compute_seconds = record.get("compute_seconds")
    if compute_seconds is not None:
        if (
            not isinstance(compute_seconds, (int, float))
            or not math.isfinite(float(compute_seconds))
            or float(compute_seconds) < 0
        ):
            raise CacheIndexError("Artifact compute_seconds is invalid")
    _validate_utc_timestamp(record.get("created_at"), "Artifact created_at")

    if status == ArtifactStatus.VALID:
        if verification != VerificationStatus.VERIFIED:
            raise CacheIndexError("valid Artifact row is not verified")
        if semantic_version is None and source_fingerprint is None:
            raise CacheIndexError("valid Artifact row has no producer identity")


def _json_record(row: sqlite3.Row) -> Dict[str, Any]:
    record = dict(row)
    parsed_values: Dict[str, Any] = {}
    for column, decoded_name in (
        ("recipe_json", "recipe"),
        ("producer_version_json", "producer_version"),
        ("metadata_json", "metadata"),
    ):
        if column in record:
            parsed = _parse_canonical_json(record[column], column)
            parsed_values[column] = parsed
            record[decoded_name] = parsed
    if "recipe_json" in record:
        _validate_artifact_record(
            record,
            parsed_values["recipe_json"],
            parsed_values["producer_version_json"],
            parsed_values["metadata_json"],
        )
    return record


class CacheIndex:
    """Metadata-only CacheIndex.

    Construction performs no I/O and creates nothing. ``initialize`` is the
    only operation allowed to create the database and its parent directory.
    All ordinary reads use SQLite ``mode=ro`` plus ``query_only``.
    """

    def __init__(self, database_path: Union[str, Path]):
        supplied = Path(database_path).expanduser()
        if not supplied.is_absolute():
            raise PathValidationError(
                "CacheIndex database_path must be explicitly absolute: {0!r}".format(
                    str(database_path)
                )
            )
        self.path = Path(str(supplied))

    @property
    def database_path(self) -> Path:
        return self.path

    def _uri(self, mode: str) -> str:
        absolute = self.path.absolute()
        return absolute.as_uri() + "?mode=" + mode

    def _configure(self, connection: sqlite3.Connection, read_only: bool) -> None:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        if read_only:
            connection.execute("PRAGMA query_only = ON")

    def _connect_read(self) -> sqlite3.Connection:
        if not self.path.is_file():
            raise IndexNotFoundError("CacheIndex not found: {0}".format(self.path))
        connection: Optional[sqlite3.Connection] = None
        try:
            connection = sqlite3.connect(
                self._uri("ro"), uri=True, timeout=30.0, isolation_level=None
            )
            self._configure(connection, read_only=True)
            self._validate_schema(connection)
            return connection
        except (IndexNotFoundError, SchemaVersionError):
            if connection is not None:
                connection.close()
            raise
        except sqlite3.Error as exc:
            if connection is not None:
                connection.close()
            raise CacheIndexError(
                "failed to open CacheIndex read-only: {0}".format(exc)
            ) from exc

    def _connect_write_existing(self) -> sqlite3.Connection:
        if not self.path.is_file():
            raise IndexNotFoundError("CacheIndex not found: {0}".format(self.path))
        connection: Optional[sqlite3.Connection] = None
        try:
            connection = sqlite3.connect(
                self._uri("rw"), uri=True, timeout=30.0, isolation_level=None
            )
            self._configure(connection, read_only=False)
            self._validate_schema(connection)
            return connection
        except (IndexNotFoundError, SchemaVersionError):
            if connection is not None:
                connection.close()
            raise
        except sqlite3.Error as exc:
            if connection is not None:
                connection.close()
            raise CacheIndexError("failed to open CacheIndex: {0}".format(exc)) from exc

    def _validate_schema(self, connection: sqlite3.Connection) -> None:
        try:
            user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
            table_rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
            tables = {str(row[0]) for row in table_rows}
            missing = sorted(REQUIRED_TABLES.difference(tables))
            if missing:
                raise SchemaVersionError(
                    "CacheIndex is missing required table(s): {0}".format(
                        ", ".join(missing)
                    )
                )
            row = connection.execute(
                "SELECT value FROM schema_meta WHERE key = ?",
                (SCHEMA_VERSION_KEY,),
            ).fetchone()
            if row is None:
                raise SchemaVersionError("schema_meta has no schema_version")
            try:
                meta_version = int(row[0])
            except (TypeError, ValueError):
                raise SchemaVersionError("schema_meta schema_version is not an integer")
            if user_version != meta_version:
                raise SchemaVersionError(
                    "PRAGMA user_version {0} disagrees with schema_meta {1}".format(
                        user_version, meta_version
                    )
                )
            if user_version != SCHEMA_VERSION:
                raise SchemaVersionError(
                    "unsupported CacheIndex schema {0}; expected {1}".format(
                        user_version, SCHEMA_VERSION
                    )
                )
            fingerprint_row = connection.execute(
                "SELECT value FROM schema_meta WHERE key = ?",
                (SCHEMA_FINGERPRINT_KEY,),
            ).fetchone()
            if fingerprint_row is None:
                raise SchemaVersionError("schema_meta has no schema_fingerprint")
            if str(fingerprint_row[0]) != SCHEMA_FINGERPRINT:
                raise SchemaVersionError("schema_meta schema_fingerprint is unsupported")
            if current_schema_fingerprint(connection) != SCHEMA_FINGERPRINT:
                raise SchemaVersionError(
                    "CacheIndex schema objects do not match schema v{0}".format(
                        SCHEMA_VERSION
                    )
                )
        except SchemaVersionError:
            raise
        except sqlite3.Error as exc:
            raise SchemaVersionError(
                "failed to validate CacheIndex schema: {0}".format(exc)
            ) from exc

    def initialize(self) -> None:
        """Explicitly create schema v1, or validate an existing index."""

        if self.path.exists():
            connection = self._connect_write_existing()
            connection.close()
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection: Optional[sqlite3.Connection] = None
        try:
            connection = sqlite3.connect(
                str(self.path), timeout=30.0, isolation_level=None
            )
            self._configure(connection, read_only=False)
            connection.execute("BEGIN IMMEDIATE")
            create_schema(connection)
            self._validate_schema(connection)
            connection.commit()
        except (SchemaVersionError, CacheIndexError):
            if connection is not None:
                connection.rollback()
            raise
        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()
            raise CacheIndexError(
                "failed to initialize CacheIndex: {0}".format(exc)
            ) from exc
        finally:
            if connection is not None:
                connection.close()

    def check_schema(self) -> int:
        with self._read_connection() as connection:
            return int(connection.execute("PRAGMA user_version").fetchone()[0])

    @contextmanager
    def _read_connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect_read()
        try:
            yield connection
        except sqlite3.Error as exc:
            raise CacheIndexError("CacheIndex read failed: {0}".format(exc)) from exc
        finally:
            connection.close()

    @contextmanager
    def batch(self) -> Iterator["CacheIndexBatch"]:
        """Run several writes atomically under ``BEGIN IMMEDIATE``."""

        connection = self._connect_write_existing()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield CacheIndexBatch(self, connection)
            connection.commit()
        except sqlite3.Error as exc:
            connection.rollback()
            raise CacheIndexError("CacheIndex transaction failed: {0}".format(exc)) from exc
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def transaction(self) -> Iterator["CacheIndexBatch"]:
        """Alias for :meth:`batch`, kept explicit for callers and tests."""

        return self.batch()

    def register_artifact(self, header: ArtifactHeader) -> RegistrationResult:
        with self.batch() as writer:
            return writer.register_artifact(header)

    def register_legacy_source(self, record: LegacySourceRecord) -> str:
        with self.batch() as writer:
            return writer.register_legacy_source(record)

    def record_conflict(self, record: ArtifactConflictRecord) -> str:
        with self.batch() as writer:
            return writer.record_conflict(record)

    def add_dependency(
        self,
        record_or_parent: Union[DependencyRecord, str],
        child_artifact_id: Optional[str] = None,
        relation: str = "input",
    ) -> None:
        with self.batch() as writer:
            writer.add_dependency(record_or_parent, child_artifact_id, relation)

    def add_consumer_ref(
        self,
        record_or_type: Union[ConsumerRef, str],
        consumer_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        with self.batch() as writer:
            writer.add_consumer_ref(
                record_or_type, consumer_id, artifact_id, metadata=metadata
            )

    def get_artifact(self, artifact_id: str) -> Dict[str, Any]:
        with self._read_connection() as connection:
            row = connection.execute(
                "SELECT * FROM artifacts WHERE artifact_id = ?", (artifact_id,)
            ).fetchone()
        if row is None:
            raise ArtifactNotFoundError("Artifact not found: {0}".format(artifact_id))
        return _json_record(row)

    def get(self, artifact_id: str) -> Dict[str, Any]:
        return self.get_artifact(artifact_id)

    def find_artifact(
        self, artifact_type: Union[ArtifactType, str], recipe_hash: str
    ) -> Optional[Dict[str, Any]]:
        type_value = ArtifactType(artifact_type).value
        with self._read_connection() as connection:
            row = connection.execute(
                """
                SELECT * FROM artifacts
                WHERE artifact_type = ? AND recipe_hash = ?
                """,
                (type_value, recipe_hash),
            ).fetchone()
        return None if row is None else _json_record(row)

    def find_artifacts_by_type(
        self, artifact_type: Union[ArtifactType, str]
    ) -> List[Dict[str, Any]]:
        """Return validated Artifact rows of one type in deterministic order."""

        type_value = ArtifactType(artifact_type).value
        with self._read_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM artifacts
                WHERE artifact_type = ?
                ORDER BY recipe_hash, artifact_id
                """,
                (type_value,),
            ).fetchall()
        return [_json_record(row) for row in rows]

    def lookup_exact(
        self, artifact_type: Union[ArtifactType, str], recipe_hash: str
    ) -> Optional[Dict[str, Any]]:
        return self.find_artifact(artifact_type, recipe_hash)

    def get_status(self, artifact_id: str) -> ArtifactStatus:
        artifact = self.get_artifact(artifact_id)
        return ArtifactStatus(artifact["status"])

    def status(self, artifact_id: str) -> ArtifactStatus:
        return self.get_status(artifact_id)

    def parents(self, artifact_id: str) -> List[str]:
        self.get_artifact(artifact_id)
        with self._read_connection() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT parent_artifact_id FROM dependencies
                WHERE child_artifact_id = ?
                ORDER BY parent_artifact_id
                """,
                (artifact_id,),
            ).fetchall()
        return [str(row[0]) for row in rows]

    def get_parents(self, artifact_id: str) -> List[str]:
        return self.parents(artifact_id)

    def children(self, artifact_id: str) -> List[str]:
        self.get_artifact(artifact_id)
        with self._read_connection() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT child_artifact_id FROM dependencies
                WHERE parent_artifact_id = ?
                ORDER BY child_artifact_id
                """,
                (artifact_id,),
            ).fetchall()
        return [str(row[0]) for row in rows]

    def get_children(self, artifact_id: str) -> List[str]:
        return self.children(artifact_id)

    def consumers(self, artifact_id: str) -> List[Dict[str, Any]]:
        self.get_artifact(artifact_id)
        with self._read_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM consumer_refs
                WHERE artifact_id = ?
                ORDER BY consumer_type, consumer_id
                """,
                (artifact_id,),
            ).fetchall()
        return [_json_record(row) for row in rows]

    def get_consumers(self, artifact_id: str) -> List[Dict[str, Any]]:
        return self.consumers(artifact_id)

    def conflicts(
        self,
        artifact_type: Optional[Union[ArtifactType, str]] = None,
        recipe_hash: Optional[str] = None,
        artifact_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        clauses: List[str] = []
        parameters: List[Any] = []
        if artifact_type is not None:
            clauses.append("artifact_type = ?")
            parameters.append(ArtifactType(artifact_type).value)
        if recipe_hash is not None:
            clauses.append("recipe_hash = ?")
            parameters.append(recipe_hash)
        if artifact_id is not None:
            clauses.append("existing_artifact_id = ?")
            parameters.append(artifact_id)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._read_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM artifact_conflicts"
                + where
                + " ORDER BY detected_at, conflict_id",
                parameters,
            ).fetchall()
        return [_json_record(row) for row in rows]

    def get_conflicts(
        self,
        artifact_type: Optional[Union[ArtifactType, str]] = None,
        recipe_hash: Optional[str] = None,
        artifact_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self.conflicts(artifact_type, recipe_hash, artifact_id)

    def get_conflict(self, conflict_id: str) -> Dict[str, Any]:
        with self._read_connection() as connection:
            row = connection.execute(
                "SELECT * FROM artifact_conflicts WHERE conflict_id = ?",
                (conflict_id,),
            ).fetchone()
        if row is None:
            raise ArtifactNotFoundError(
                "Artifact conflict not found: {0}".format(conflict_id)
            )
        return _json_record(row)

    def explain_exact(
        self,
        artifact_type: Union[ArtifactType, str],
        recipe: Any,
    ) -> Any:
        # Local import avoids an index -> resolver -> index import cycle.
        from .resolver import explain_exact

        return explain_exact(self, artifact_type, recipe)

    def legacy_sources(
        self,
        artifact_type: Optional[Union[ArtifactType, str]] = None,
        recipe_hash: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        clauses: List[str] = []
        parameters: List[Any] = []
        if artifact_type is not None:
            clauses.append("observed_artifact_type = ?")
            parameters.append(ArtifactType(artifact_type).value)
        if recipe_hash is not None:
            clauses.append("observed_recipe_hash = ?")
            parameters.append(validate_sha256(recipe_hash, "recipe_hash"))
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._read_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM legacy_sources"
                + where
                + " ORDER BY source_root, legacy_path",
                parameters,
            ).fetchall()
        return [_json_record(row) for row in rows]


class CacheIndexBatch:
    """Writer bound to one explicit CacheIndex transaction."""

    def __init__(self, index: CacheIndex, connection: sqlite3.Connection):
        self.index = index
        self.connection = connection

    def _require_artifact(self, artifact_id: str) -> None:
        row = self.connection.execute(
            "SELECT 1 FROM artifacts WHERE artifact_id = ?", (artifact_id,)
        ).fetchone()
        if row is None:
            raise ArtifactNotFoundError("Artifact not found: {0}".format(artifact_id))

    def register_artifact(self, header: ArtifactHeader) -> RegistrationResult:
        if not isinstance(header, ArtifactHeader):
            raise CacheIndexError("register_artifact requires ArtifactHeader")

        existing = self.connection.execute(
            """
            SELECT artifact_id, content_hash FROM artifacts
            WHERE artifact_type = ? AND recipe_hash = ?
            """,
            (header.artifact_type.value, header.recipe_hash),
        ).fetchone()
        if existing is not None:
            existing_id = str(existing["artifact_id"])
            existing_hash = str(existing["content_hash"])
            if existing_hash == header.content_hash:
                return RegistrationResult(
                    outcome=RegisterOutcome.IDENTICAL,
                    artifact_id=existing_id,
                    existing_artifact_id=existing_id,
                )
            conflict = ArtifactConflictRecord(
                artifact_type=header.artifact_type,
                recipe_hash=header.recipe_hash,
                observed_content_hash=header.content_hash,
                existing_artifact_id=existing_id,
                existing_content_hash=existing_hash,
                metadata={"observed_artifact_id": header.artifact_id},
            )
            self.record_conflict(conflict)
            return RegistrationResult(
                outcome=RegisterOutcome.CONFLICT,
                artifact_id=header.artifact_id,
                existing_artifact_id=existing_id,
                conflict_id=conflict.conflict_id,
            )

        recipe_json = _bounded_json(
            header.recipe.canonical_json, "recipe_json", MAX_RECIPE_JSON_BYTES
        )
        producer_json = _bounded_json(
            header.producer_version_json,
            "producer_version_json",
            MAX_SMALL_JSON_BYTES,
        )
        metadata_json = _bounded_json(
            header.metadata_json, "metadata_json", MAX_SMALL_JSON_BYTES
        )
        self.connection.execute(
            """
            INSERT INTO artifacts(
                artifact_id, artifact_type, recipe_hash, content_hash,
                recipe_json, semantic_path, producer_version_json, status,
                verification_status, compute_seconds, created_at,
                header_version, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                header.artifact_id,
                header.artifact_type.value,
                header.recipe_hash,
                header.content_hash,
                recipe_json,
                header.semantic_path,
                producer_json,
                header.status.value,
                header.verification_status.value,
                header.compute_seconds,
                header.created_at,
                header.header_version,
                metadata_json,
            ),
        )
        return RegistrationResult(
            outcome=RegisterOutcome.CREATED, artifact_id=header.artifact_id
        )

    def register_legacy_source(self, record: LegacySourceRecord) -> str:
        if not isinstance(record, LegacySourceRecord):
            raise CacheIndexError("register_legacy_source requires LegacySourceRecord")
        if record.artifact_id is not None:
            self._require_artifact(record.artifact_id)

        metadata_json = _bounded_json(
            canonical_json(record.metadata),
            "metadata_json",
            MAX_SMALL_JSON_BYTES,
        )
        source_root = record.source_root or ""
        values = (
            record.legacy_source_id,
            record.artifact_id,
            record.legacy_kind,
            record.legacy_path,
            record.path_kind.value,
            source_root,
            None
            if record.observed_artifact_type is None
            else record.observed_artifact_type.value,
            record.observed_recipe_hash,
            record.raw_content_hash,
            record.semantic_content_hash,
            record.verification_status.value,
            record.size_bytes,
            record.mtime_ns,
            record.imported_at,
            metadata_json,
        )
        self.connection.execute(
            """
            INSERT INTO legacy_sources(
                legacy_source_id, artifact_id, legacy_kind, legacy_path,
                path_kind, source_root, observed_artifact_type,
                observed_recipe_hash, raw_content_hash, semantic_content_hash,
                verification_status, size_bytes, mtime_ns, imported_at,
                metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(legacy_source_id) DO UPDATE SET
                artifact_id = excluded.artifact_id,
                observed_artifact_type = excluded.observed_artifact_type,
                observed_recipe_hash = excluded.observed_recipe_hash,
                raw_content_hash = excluded.raw_content_hash,
                semantic_content_hash = excluded.semantic_content_hash,
                verification_status = excluded.verification_status,
                size_bytes = excluded.size_bytes,
                mtime_ns = excluded.mtime_ns,
                imported_at = excluded.imported_at,
                metadata_json = excluded.metadata_json
            """,
            values,
        )
        return record.legacy_source_id

    def record_conflict(self, record: ArtifactConflictRecord) -> str:
        if not isinstance(record, ArtifactConflictRecord):
            raise CacheIndexError("record_conflict requires ArtifactConflictRecord")
        if record.existing_artifact_id is not None:
            artifact = self.connection.execute(
                "SELECT * FROM artifacts WHERE artifact_id = ?",
                (record.existing_artifact_id,),
            ).fetchone()
            if artifact is None:
                raise ArtifactNotFoundError(
                    "Artifact not found: {0}".format(record.existing_artifact_id)
                )
            artifact = _json_record(artifact)
            if (
                artifact["artifact_type"] != record.artifact_type.value
                or artifact["recipe_hash"] != record.recipe_hash
            ):
                raise CacheIndexError(
                    "conflict existing Artifact does not match artifact_type/recipe_hash"
                )
            if (
                record.existing_content_hash is not None
                and artifact["content_hash"] != record.existing_content_hash
            ):
                raise CacheIndexError(
                    "conflict existing_content_hash does not match indexed Artifact"
                )
        if record.legacy_source_id is not None:
            source = self.connection.execute(
                "SELECT 1 FROM legacy_sources WHERE legacy_source_id = ?",
                (record.legacy_source_id,),
            ).fetchone()
            if source is None:
                raise CacheIndexError(
                    "Legacy source not found: {0}".format(record.legacy_source_id)
                )
        metadata_json = _bounded_json(
            canonical_json(record.metadata),
            "metadata_json",
            MAX_SMALL_JSON_BYTES,
        )
        existing = self.connection.execute(
            "SELECT * FROM artifact_conflicts WHERE conflict_id = ?",
            (record.conflict_id,),
        ).fetchone()
        if existing is not None:
            stable_values = (
                existing["artifact_type"],
                existing["recipe_hash"],
                existing["existing_artifact_id"],
                existing["existing_content_hash"],
                existing["observed_content_hash"],
                existing["legacy_source_id"],
                existing["quarantine_path"],
            )
            requested_values = (
                record.artifact_type.value,
                record.recipe_hash,
                record.existing_artifact_id,
                record.existing_content_hash,
                record.observed_content_hash,
                record.legacy_source_id,
                record.quarantine_path,
            )
            if stable_values != requested_values:
                raise CacheIndexError(
                    "conflict_id collision with different conflict identity"
                )
            return record.conflict_id
        self.connection.execute(
            """
            INSERT INTO artifact_conflicts(
                conflict_id, artifact_type, recipe_hash,
                existing_artifact_id, existing_content_hash,
                observed_content_hash, legacy_source_id, quarantine_path,
                detected_at, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.conflict_id,
                record.artifact_type.value,
                record.recipe_hash,
                record.existing_artifact_id,
                record.existing_content_hash,
                record.observed_content_hash,
                record.legacy_source_id,
                record.quarantine_path,
                record.detected_at,
                metadata_json,
            ),
        )
        return record.conflict_id

    def add_dependency(
        self,
        record_or_parent: Union[DependencyRecord, str],
        child_artifact_id: Optional[str] = None,
        relation: str = "input",
    ) -> None:
        if isinstance(record_or_parent, DependencyRecord):
            record = record_or_parent
        else:
            if child_artifact_id is None:
                raise CacheIndexError("child_artifact_id is required")
            record = DependencyRecord(
                parent_artifact_id=record_or_parent,
                child_artifact_id=child_artifact_id,
                relation=relation,
            )
        self._require_artifact(record.parent_artifact_id)
        self._require_artifact(record.child_artifact_id)
        cycle = self.connection.execute(
            """
            WITH RECURSIVE descendants(artifact_id) AS (
                SELECT child_artifact_id FROM dependencies
                WHERE parent_artifact_id = ?
                UNION
                SELECT d.child_artifact_id
                FROM dependencies AS d
                JOIN descendants AS seen
                  ON d.parent_artifact_id = seen.artifact_id
            )
            SELECT 1 FROM descendants WHERE artifact_id = ? LIMIT 1
            """,
            (record.child_artifact_id, record.parent_artifact_id),
        ).fetchone()
        if cycle is not None:
            raise DependencyCycleError(
                "dependency {0} -> {1} would create a cycle".format(
                    record.parent_artifact_id, record.child_artifact_id
                )
            )
        self.connection.execute(
            """
            INSERT OR IGNORE INTO dependencies(
                parent_artifact_id, child_artifact_id, relation, created_at
            ) VALUES (?, ?, ?, ?)
            """,
            (
                record.parent_artifact_id,
                record.child_artifact_id,
                record.relation,
                utc_now_iso(),
            ),
        )

    def add_consumer_ref(
        self,
        record_or_type: Union[ConsumerRef, str],
        consumer_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if isinstance(record_or_type, ConsumerRef):
            record = record_or_type
        else:
            if consumer_id is None or artifact_id is None:
                raise CacheIndexError("consumer_id and artifact_id are required")
            record = ConsumerRef(
                consumer_type=record_or_type,
                consumer_id=consumer_id,
                artifact_id=artifact_id,
                metadata={} if metadata is None else metadata,
            )
        self._require_artifact(record.artifact_id)
        metadata_json = _bounded_json(
            record.metadata_json, "metadata_json", MAX_SMALL_JSON_BYTES
        )
        self.connection.execute(
            """
            INSERT INTO consumer_refs(
                consumer_type, consumer_id, artifact_id, created_at,
                metadata_json
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(consumer_type, consumer_id, artifact_id) DO UPDATE SET
                created_at = excluded.created_at,
                metadata_json = excluded.metadata_json
            """,
            (
                record.consumer_type,
                record.consumer_id,
                record.artifact_id,
                record.created_at,
                metadata_json,
            ),
        )
