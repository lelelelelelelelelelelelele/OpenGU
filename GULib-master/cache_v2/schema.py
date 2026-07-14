"""SQLite schema for the Cache V2.1 metadata index.

The database is intentionally metadata-only. Artifact payloads stay in the
artifact store planned for a later phase, and legacy payloads remain read-only
at their original paths.
"""

from __future__ import annotations

import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from typing import FrozenSet, Tuple


SCHEMA_VERSION = 1
SCHEMA_VERSION_KEY = "schema_version"
SCHEMA_FINGERPRINT_KEY = "schema_fingerprint"

ARTIFACT_TYPE_VALUES: Tuple[str, ...] = (
    "score",
    "selection",
    "prediction",
    "evaluation",
)

ARTIFACT_STATUS_VALUES: Tuple[str, ...] = (
    "valid",
    "degraded",
    "invalid",
    "corrupt",
    "missing",
    "retired",
    "unknown",
    "conflict",
)

VERIFICATION_STATUS_VALUES: Tuple[str, ...] = (
    "verified",
    "degraded",
    "invalid",
    "corrupt",
    "missing",
    "unknown",
)

REQUIRED_TABLES: FrozenSet[str] = frozenset(
    {
        "schema_meta",
        "artifacts",
        "dependencies",
        "consumer_refs",
        "legacy_sources",
        "artifact_conflicts",
    }
)


def _sql_values(values: Tuple[str, ...]) -> str:
    return ", ".join("'%s'" % value for value in values)


DDL_STATEMENTS: Tuple[str, ...] = (
    """
    CREATE TABLE schema_meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE artifacts (
        artifact_id TEXT PRIMARY KEY,
        artifact_type TEXT NOT NULL
            CHECK (artifact_type IN (%s)),
        recipe_hash TEXT NOT NULL
            CHECK (length(recipe_hash) = 64 AND recipe_hash NOT GLOB '*[^0-9a-f]*'),
        content_hash TEXT NOT NULL
            CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
        recipe_json TEXT NOT NULL
            CHECK (json_valid(recipe_json) AND length(recipe_json) <= 262144),
        semantic_path TEXT,
        producer_version_json TEXT NOT NULL
            CHECK (json_valid(producer_version_json) AND length(producer_version_json) <= 65536),
        status TEXT NOT NULL
            CHECK (status IN (%s)),
        verification_status TEXT NOT NULL
            CHECK (verification_status IN (%s)),
        compute_seconds REAL
            CHECK (compute_seconds IS NULL OR compute_seconds >= 0),
        created_at TEXT NOT NULL,
        header_version INTEGER NOT NULL CHECK (header_version = 1),
        metadata_json TEXT NOT NULL DEFAULT '{}'
            CHECK (json_valid(metadata_json) AND length(metadata_json) <= 65536),
        UNIQUE (artifact_type, recipe_hash)
    )
    """ % (
        _sql_values(ARTIFACT_TYPE_VALUES),
        _sql_values(ARTIFACT_STATUS_VALUES),
        _sql_values(VERIFICATION_STATUS_VALUES),
    ),
    """
    CREATE TABLE dependencies (
        parent_artifact_id TEXT NOT NULL,
        child_artifact_id TEXT NOT NULL,
        relation TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY (parent_artifact_id, child_artifact_id, relation),
        CHECK (parent_artifact_id <> child_artifact_id),
        FOREIGN KEY (parent_artifact_id)
            REFERENCES artifacts(artifact_id) ON DELETE RESTRICT,
        FOREIGN KEY (child_artifact_id)
            REFERENCES artifacts(artifact_id) ON DELETE RESTRICT
    )
    """,
    """
    CREATE INDEX idx_dependencies_parent
        ON dependencies(parent_artifact_id)
    """,
    """
    CREATE INDEX idx_dependencies_child
        ON dependencies(child_artifact_id)
    """,
    """
    CREATE TABLE consumer_refs (
        consumer_type TEXT NOT NULL,
        consumer_id TEXT NOT NULL,
        artifact_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}'
            CHECK (json_valid(metadata_json) AND length(metadata_json) <= 65536),
        PRIMARY KEY (consumer_type, consumer_id, artifact_id),
        FOREIGN KEY (artifact_id)
            REFERENCES artifacts(artifact_id) ON DELETE RESTRICT
    )
    """,
    """
    CREATE INDEX idx_consumer_refs_artifact
        ON consumer_refs(artifact_id)
    """,
    """
    CREATE INDEX idx_consumer_refs_consumer
        ON consumer_refs(consumer_type, consumer_id)
    """,
    """
    CREATE TABLE legacy_sources (
        legacy_source_id TEXT PRIMARY KEY,
        artifact_id TEXT,
        legacy_kind TEXT NOT NULL,
        legacy_path TEXT NOT NULL,
        path_kind TEXT NOT NULL CHECK (path_kind IN ('relative', 'absolute')),
        source_root TEXT NOT NULL DEFAULT '',
        observed_artifact_type TEXT
            CHECK (observed_artifact_type IS NULL OR observed_artifact_type IN (%s)),
        observed_recipe_hash TEXT
            CHECK (observed_recipe_hash IS NULL OR
                   (length(observed_recipe_hash) = 64 AND observed_recipe_hash NOT GLOB '*[^0-9a-f]*')),
        raw_content_hash TEXT
            CHECK (raw_content_hash IS NULL OR
                   (length(raw_content_hash) = 64 AND raw_content_hash NOT GLOB '*[^0-9a-f]*')),
        semantic_content_hash TEXT
            CHECK (semantic_content_hash IS NULL OR
                   (length(semantic_content_hash) = 64 AND semantic_content_hash NOT GLOB '*[^0-9a-f]*')),
        verification_status TEXT NOT NULL
            CHECK (verification_status IN (%s)),
        size_bytes INTEGER CHECK (size_bytes IS NULL OR size_bytes >= 0),
        mtime_ns INTEGER CHECK (mtime_ns IS NULL OR mtime_ns >= 0),
        imported_at TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}'
            CHECK (json_valid(metadata_json) AND length(metadata_json) <= 65536),
        UNIQUE (source_root, legacy_path),
        FOREIGN KEY (artifact_id)
            REFERENCES artifacts(artifact_id) ON DELETE SET NULL
    )
    """ % (
        _sql_values(ARTIFACT_TYPE_VALUES),
        _sql_values(VERIFICATION_STATUS_VALUES),
    ),
    """
    CREATE INDEX idx_legacy_sources_artifact
        ON legacy_sources(artifact_id)
    """,
    """
    CREATE INDEX idx_legacy_sources_recipe
        ON legacy_sources(observed_artifact_type, observed_recipe_hash)
    """,
    """
    CREATE TABLE artifact_conflicts (
        conflict_id TEXT PRIMARY KEY,
        artifact_type TEXT NOT NULL
            CHECK (artifact_type IN (%s)),
        recipe_hash TEXT NOT NULL
            CHECK (length(recipe_hash) = 64 AND recipe_hash NOT GLOB '*[^0-9a-f]*'),
        existing_artifact_id TEXT,
        existing_content_hash TEXT NOT NULL
            CHECK (length(existing_content_hash) = 64 AND existing_content_hash NOT GLOB '*[^0-9a-f]*'),
        observed_content_hash TEXT NOT NULL
            CHECK (length(observed_content_hash) = 64 AND observed_content_hash NOT GLOB '*[^0-9a-f]*'),
        legacy_source_id TEXT,
        quarantine_path TEXT,
        detected_at TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}'
            CHECK (json_valid(metadata_json) AND length(metadata_json) <= 65536),
        FOREIGN KEY (existing_artifact_id)
            REFERENCES artifacts(artifact_id) ON DELETE SET NULL,
        FOREIGN KEY (legacy_source_id)
            REFERENCES legacy_sources(legacy_source_id) ON DELETE SET NULL
    )
    """ % _sql_values(ARTIFACT_TYPE_VALUES),
    """
    CREATE INDEX idx_artifact_conflicts_recipe
        ON artifact_conflicts(artifact_type, recipe_hash)
    """,
    """
    CREATE INDEX idx_artifact_conflicts_existing
        ON artifact_conflicts(existing_artifact_id)
    """,
    """
    CREATE INDEX idx_artifact_conflicts_legacy_source
        ON artifact_conflicts(legacy_source_id)
    """,
)


def _normalize_schema_sql(sql: str) -> str:
    return " ".join(sql.strip().rstrip(";").split())


def _ddl_object_name(sql: str) -> str:
    match = re.match(
        r"^CREATE\s+(?:UNIQUE\s+)?(?:TABLE|INDEX)\s+([A-Za-z_][A-Za-z0-9_]*)",
        _normalize_schema_sql(sql),
        flags=re.IGNORECASE,
    )
    if match is None:
        raise ValueError("DDL statement has no supported schema object name")
    return match.group(1)


def _fingerprint_schema_objects(objects: Tuple[Tuple[str, str], ...]) -> str:
    payload = "\n".join(
        "{0}\0{1}".format(name, _normalize_schema_sql(sql))
        for name, sql in sorted(objects)
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


EXPECTED_SCHEMA_OBJECTS: Tuple[Tuple[str, str], ...] = tuple(
    (_ddl_object_name(statement), statement) for statement in DDL_STATEMENTS
)
SCHEMA_FINGERPRINT = _fingerprint_schema_objects(EXPECTED_SCHEMA_OBJECTS)


def current_schema_fingerprint(connection: sqlite3.Connection) -> str:
    """Fingerprint all explicit tables/indexes, including constraints in SQL."""

    rows = connection.execute(
        """
        SELECT name, sql FROM sqlite_master
        WHERE type IN ('table', 'index')
          AND sql IS NOT NULL
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()
    objects = tuple((str(row[0]), str(row[1])) for row in rows)
    return _fingerprint_schema_objects(objects)


def utc_now_iso() -> str:
    """Return a stable UTC timestamp suitable for SQLite metadata."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_schema(connection: sqlite3.Connection) -> None:
    """Create schema v1 on an open connection inside the caller transaction."""

    for statement in DDL_STATEMENTS:
        connection.execute(statement)
    connection.execute(
        "INSERT INTO schema_meta(key, value) VALUES (?, ?)",
        (SCHEMA_VERSION_KEY, str(SCHEMA_VERSION)),
    )
    connection.execute(
        "INSERT INTO schema_meta(key, value) VALUES (?, ?)",
        (SCHEMA_FINGERPRINT_KEY, SCHEMA_FINGERPRINT),
    )
    connection.execute(
        "INSERT INTO schema_meta(key, value) VALUES (?, ?)",
        ("created_at", utc_now_iso()),
    )
    connection.execute("PRAGMA user_version = %d" % SCHEMA_VERSION)
