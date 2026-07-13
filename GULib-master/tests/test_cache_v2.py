"""Contract and read-only integration tests for Cache V2.1.

Every filesystem fixture in this module lives below ``tmp_path``.  In
particular, the LegacyIndexer tests never inspect or mutate the repository's
real ``results`` tree.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from enum import Enum
from pathlib import Path, PureWindowsPath

import numpy as np
import pytest

from cache_v2 import (
    ArtifactConflictRecord,
    ArtifactHeader,
    ArtifactNotFoundError,
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    CacheIndexError,
    ConsumerRef,
    ContractValidationError,
    ForbiddenRecipeFieldError,
    IndexNotFoundError,
    LegacySourceRecord,
    LegacySourceChangedError,
    PathKind,
    PathValidationError,
    ProducerVersion,
    RegisterOutcome,
    SchemaVersionError,
    VerificationStatus,
    normalize_absolute_source_path,
    normalize_relative_path,
    sha256_bytes,
)
from cache_v2.index import CacheIndex
from cache_v2.legacy import LegacyIndexer
from cache_v2.resolver import ArtifactResolver
from cache_v2.schema import (
    DDL_STATEMENTS,
    REQUIRED_TABLES,
    SCHEMA_FINGERPRINT,
    SCHEMA_FINGERPRINT_KEY,
    SCHEMA_VERSION,
    SCHEMA_VERSION_KEY,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CACHECTL = REPO_ROOT / "scripts" / "cachectl.py"


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    return path


def _file_snapshot(root):
    """Capture the exact content hash and mtime of every file below *root*."""

    snapshot = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        stat = path.stat()
        snapshot[path.relative_to(root).as_posix()] = (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            stat.st_mtime_ns,
            stat.st_size,
        )
    return snapshot


def _result_cache_payload(cache_key, selected_nodes=None):
    nodes = [1, 2] if selected_nodes is None else list(selected_nodes)
    return {
        "cache_key": cache_key,
        "cached_at": "2026-01-01T00:00:00Z",
        "config": {
            "dataset_name": "cora",
            "base_model": "GCN",
            "strategy_name": "degree",
            "k": len(nodes),
        },
        "result": {
            "strategy_name": "degree",
            "selected_nodes": nodes,
            "f1_before": 0.8,
            "f1_after": 0.7,
        },
    }


def _selection_cache_payload(cache_key, selected_nodes):
    return {
        "cache_key": cache_key,
        "cached_at": "2026-01-01T00:00:00Z",
        "config": {
            "dataset_name": "cora",
            "base_model": "GCN",
            "strategy_name": "degree",
            "k": len(selected_nodes),
            "graph_fingerprint": "1" * 32,
            "strategy_params_fingerprint": "2" * 32,
            "is_transductive": True,
            "is_balanced": False,
            "train_ratio": 0.8,
            "val_ratio": 0.1,
            "test_ratio": 0.1,
        },
        "selection_result": {
            "selection_key": cache_key,
            "strategy_name": "degree",
            "selected_nodes": list(selected_nodes),
        },
    }


def _artifact_header(artifact_type, recipe, content, status=ArtifactStatus.VALID):
    recipe_value = recipe if isinstance(recipe, ArtifactRecipe) else ArtifactRecipe(recipe)
    return ArtifactHeader(
        artifact_type=artifact_type,
        recipe=recipe_value,
        content_hash=sha256_bytes(content),
        producer_version=ProducerVersion(
            semantic_version="cache-v2.1-test",
            source_fingerprint="test-source-fingerprint",
        ),
        status=status,
        verification_status=(
            VerificationStatus.VERIFIED
            if status == ArtifactStatus.VALID
            else VerificationStatus.DEGRADED
        ),
        semantic_path="{0}/fixture".format(ArtifactType(artifact_type).value),
        compute_seconds=0.01,
        metadata={"fixture": True},
    )


def _initialized_index(tmp_path):
    database_path = (tmp_path / "cache_v2" / "index.sqlite").absolute()
    index = CacheIndex(database_path)
    index.initialize()
    return index


def _run_cachectl(arguments, cwd):
    env = os.environ.copy()
    return subprocess.run(
        [sys.executable, str(CACHECTL)] + list(arguments),
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
        check=False,
    )


class TestArtifactRecipe:
    def test_hash_is_stable_across_dict_key_order(self):
        first = ArtifactRecipe(
            {
                "graph_fingerprint": "graph-1",
                "selector": {"name": "degree", "version": 1},
                "k": 10,
            }
        )
        second = ArtifactRecipe(
            {
                "k": 10,
                "selector": {"version": 1, "name": "degree"},
                "graph_fingerprint": "graph-1",
            }
        )

        assert first.recipe_hash == second.recipe_hash
        assert first.canonical_json == second.canonical_json

    def test_float_path_enum_and_list_have_stable_typed_forms(self):
        first = ArtifactRecipe(
            {
                "threshold": 0.1,
                "source": PureWindowsPath(r"score_cache\if\entry.npz"),
                "type": ArtifactType.SCORE,
                "ordered_candidates": [3, 1, 2],
                "zero": -0.0,
            }
        )
        equivalent = ArtifactRecipe(
            {
                "ordered_candidates": [3, 1, 2],
                "type": ArtifactType.SCORE,
                "source": PureWindowsPath("score_cache/if/entry.npz"),
                "zero": 0.0,
                "threshold": 0.1,
            }
        )
        reordered_list = ArtifactRecipe(
            {
                "threshold": 0.1,
                "source": PureWindowsPath(r"score_cache\if\entry.npz"),
                "type": ArtifactType.SCORE,
                "ordered_candidates": [1, 3, 2],
                "zero": 0.0,
            }
        )

        assert first.recipe_hash == equivalent.recipe_hash
        assert first.recipe_hash != reordered_list.recipe_hash
        assert '"$cache_v2_type":"float"' in first.canonical_json
        assert '"$cache_v2_type":"path"' in first.canonical_json
        assert '"$cache_v2_type":"enum"' in first.canonical_json
        assert '"$cache_v2_type":"list"' in first.canonical_json

    def test_enum_identity_uses_qualified_type_not_only_class_name(self):
        left_mode = Enum("Mode", {"X": "x"}, module="producer_a")
        right_mode = Enum("Mode", {"X": "x"}, module="producer_b")

        left = ArtifactRecipe({"mode": left_mode.X})
        right = ArtifactRecipe({"mode": right_mode.X})

        assert left.recipe_hash != right.recipe_hash
        assert "producer_a.Mode" in left.canonical_json
        assert "producer_b.Mode" in right.canonical_json

    @pytest.mark.parametrize(
        "fields, forbidden_fragment",
        [
            ({"selector": {"config_name": "phase_b"}}, "config_name"),
            ({"inputs": [{"YAML-Path": "experiments/a.yaml"}]}, "YAML-Path"),
            ({"provenance": {"experiment_id": "exp-1"}}, "experiment_id"),
            ({"provenance": {"configName": "phase_b"}}, "configName"),
            ({"inputs": {"yamlPath": "experiments/a.yaml"}}, "yamlPath"),
            ({"provenance": {"experimentId": "exp-1"}}, "experimentId"),
            ({"nested": {"config": {"dataset_name": "cora"}}}, "config"),
        ],
    )
    def test_forbidden_experiment_fields_are_rejected_recursively(
        self, fields, forbidden_fragment
    ):
        with pytest.raises(ForbiddenRecipeFieldError) as caught:
            ArtifactRecipe(fields)

        assert forbidden_fragment in str(caught.value)

    def test_full_experiment_config_is_rejected_instead_of_hashed(self):
        complete_config = {
            "dataset_name": "cora",
            "base_model": "GCN",
            "unlearning_methods": "GIF",
            "unlearn_ratio": 0.05,
            "seed": 42,
            "num_epochs": 100,
            "root_path": "E:/project/OpenGU/GULib-master",
        }

        with pytest.raises(ForbiddenRecipeFieldError, match="root_path"):
            ArtifactRecipe({"request": complete_config})

    def test_true_prediction_dependencies_are_not_misclassified_as_ownership(self):
        recipe = ArtifactRecipe(
            {
                "dataset_name": "cora",
                "base_model": "GCN",
                "unlearning_methods": "GIF",
                "unlearn_ratio": 0.05,
                "seed": 42,
                "num_epochs": 100,
            }
        )

        assert len(recipe.recipe_hash) == 64


class TestCacheIndex:
    def test_same_recipe_and_content_registration_is_idempotent(self, tmp_path):
        index = _initialized_index(tmp_path)
        header = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "graph_fingerprint": "g1", "k": 2},
            b"[1,2]",
        )

        first = index.register_artifact(header)
        second = index.register_artifact(header)

        assert first.outcome == RegisterOutcome.CREATED
        assert second.outcome == RegisterOutcome.IDENTICAL
        assert first.artifact_id == second.artifact_id == header.artifact_id
        assert index.find_artifact(ArtifactType.SELECTION, header.recipe_hash)[
            "content_hash"
        ] == header.content_hash
        assert index.conflicts(
            artifact_type=ArtifactType.SELECTION, recipe_hash=header.recipe_hash
        ) == []
        with sqlite3.connect(str(index.database_path)) as connection:
            assert connection.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0] == 1

    def test_different_content_is_quarantined_as_conflict_without_overwrite(
        self, tmp_path
    ):
        index = _initialized_index(tmp_path)
        recipe = ArtifactRecipe(
            {"kind": "selection", "graph_fingerprint": "g1", "k": 2}
        )
        original = _artifact_header(
            ArtifactType.SELECTION, recipe, b"selected=[1,2]"
        )
        observed = _artifact_header(
            ArtifactType.SELECTION, recipe, b"selected=[1,3]"
        )

        assert index.register_artifact(original).outcome == RegisterOutcome.CREATED
        result = index.register_artifact(observed)

        assert result.outcome == RegisterOutcome.CONFLICT
        assert result.existing_artifact_id == original.artifact_id
        assert result.conflict_id is not None
        formal = index.find_artifact(ArtifactType.SELECTION, recipe.recipe_hash)
        assert formal["artifact_id"] == original.artifact_id
        assert formal["content_hash"] == original.content_hash
        assert index.get_status(original.artifact_id) == ArtifactStatus.VALID
        with pytest.raises(ArtifactNotFoundError):
            index.get_artifact(observed.artifact_id)
        conflicts = index.conflicts(
            artifact_type=ArtifactType.SELECTION, recipe_hash=recipe.recipe_hash
        )
        assert len(conflicts) == 1
        assert conflicts[0]["existing_artifact_id"] == original.artifact_id
        assert conflicts[0]["observed_content_hash"] == observed.content_hash

    def test_identical_content_cannot_be_recorded_as_a_conflict(self, tmp_path):
        index = _initialized_index(tmp_path)
        header = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "graph_fingerprint": "g1", "k": 2},
            b"[1,2]",
        )
        index.register_artifact(header)

        with pytest.raises(ContractValidationError, match="idempotent"):
            ArtifactConflictRecord(
                artifact_type=header.artifact_type,
                recipe_hash=header.recipe_hash,
                existing_artifact_id=header.artifact_id,
                existing_content_hash=header.content_hash,
                observed_content_hash=header.content_hash,
            )

        explanation = ArtifactResolver(index).explain_exact(
            header.artifact_type, header.recipe
        )
        assert explanation.hit is True
        assert explanation.conflicts == ()

    def test_conflict_requires_a_distinct_existing_content_baseline(self, tmp_path):
        header = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "graph_fingerprint": "g1", "k": 2},
            b"[1,2]",
        )

        with pytest.raises(ContractValidationError, match="baseline"):
            ArtifactConflictRecord(
                artifact_type=header.artifact_type,
                recipe_hash=header.recipe_hash,
                observed_content_hash=header.content_hash,
            )

    def test_tampered_artifact_row_fails_closed_before_exact_hit(self, tmp_path):
        index = _initialized_index(tmp_path)
        header = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "graph_fingerprint": "g1", "k": 2},
            b"[1,2]",
        )
        index.register_artifact(header)
        tampered_recipe = ArtifactRecipe(
            {"kind": "selection", "graph_fingerprint": "tampered", "k": 2}
        )
        with sqlite3.connect(str(index.database_path)) as connection:
            connection.execute(
                "UPDATE artifacts SET recipe_json = ? WHERE artifact_id = ?",
                (tampered_recipe.canonical_json, header.artifact_id),
            )
            connection.commit()

        with pytest.raises(CacheIndexError, match="does not match recipe_hash"):
            index.find_artifact(header.artifact_type, header.recipe_hash)
        with pytest.raises(CacheIndexError, match="does not match recipe_hash"):
            ArtifactResolver(index).explain_exact(header.artifact_type, header.recipe)

    def test_parent_child_and_consumer_queries(self, tmp_path):
        index = _initialized_index(tmp_path)
        score = _artifact_header(
            ArtifactType.SCORE, {"kind": "score", "case": "parent"}, b"scores"
        )
        selection = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "case": "middle"},
            b"selection",
        )
        prediction = _artifact_header(
            ArtifactType.PREDICTION,
            {"kind": "prediction", "case": "child"},
            b"prediction",
        )
        for header in (score, selection, prediction):
            index.register_artifact(header)

        index.add_dependency(score.artifact_id, selection.artifact_id, "source_score")
        index.add_dependency(
            selection.artifact_id, prediction.artifact_id, "selected_nodes"
        )
        index.add_consumer_ref(
            ConsumerRef(
                consumer_type="experiment",
                consumer_id="exp-a",
                artifact_id=selection.artifact_id,
                metadata={"role": "selection"},
            )
        )
        index.add_consumer_ref(
            "report", "report-a", selection.artifact_id, metadata={"table": 1}
        )

        assert index.parents(score.artifact_id) == []
        assert index.parents(selection.artifact_id) == [score.artifact_id]
        assert index.children(score.artifact_id) == [selection.artifact_id]
        assert index.children(selection.artifact_id) == [prediction.artifact_id]
        assert index.parents(prediction.artifact_id) == [selection.artifact_id]
        consumers = index.consumers(selection.artifact_id)
        assert [
            (item["consumer_type"], item["consumer_id"]) for item in consumers
        ] == [("experiment", "exp-a"), ("report", "report-a")]
        assert json.loads(consumers[0]["metadata_json"]) == consumers[0]["metadata"]
        assert "selection" in consumers[0]["metadata_json"]

    def test_exact_resolver_blocks_valid_child_with_invalid_parent(self, tmp_path):
        index = _initialized_index(tmp_path)
        parent = _artifact_header(
            ArtifactType.SCORE,
            {"kind": "score", "case": "invalid-parent"},
            b"scores",
            status=ArtifactStatus.INVALID,
        )
        child = _artifact_header(
            ArtifactType.SELECTION,
            {"kind": "selection", "case": "valid-child"},
            b"selection",
        )
        index.register_artifact(parent)
        index.register_artifact(child)
        index.add_dependency(parent.artifact_id, child.artifact_id, "source_score")

        explanation = ArtifactResolver(index).explain_exact(
            child.artifact_type, child.recipe
        )

        assert explanation.hit is False
        assert explanation.dependency_issues[0]["artifact_id"] == parent.artifact_id
        assert "status_invalid" in explanation.dependency_issues[0]["reasons"]
        assert any("dependency_" in reason for reason in explanation.miss_reasons)

    def test_schema_tables_version_and_metadata_are_created_together(self, tmp_path):
        index = _initialized_index(tmp_path)

        assert index.check_schema() == SCHEMA_VERSION
        assert not (index.database_path.parent / "index.jsonl").exists()
        with sqlite3.connect(str(index.database_path)) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            meta = dict(connection.execute("SELECT key, value FROM schema_meta"))
            pragma_version = connection.execute("PRAGMA user_version").fetchone()[0]

        assert REQUIRED_TABLES.issubset(tables)
        assert meta[SCHEMA_VERSION_KEY] == str(SCHEMA_VERSION)
        assert meta[SCHEMA_FINGERPRINT_KEY] == SCHEMA_FINGERPRINT
        assert pragma_version == SCHEMA_VERSION

    def test_same_version_schema_missing_recipe_unique_is_rejected(self, tmp_path):
        database_path = (tmp_path / "mutated" / "index.sqlite").absolute()
        database_path.parent.mkdir(parents=True)
        with sqlite3.connect(str(database_path)) as connection:
            for statement in DDL_STATEMENTS:
                if "CREATE TABLE artifacts" in statement:
                    statement = statement.replace(
                        ",\n        UNIQUE (artifact_type, recipe_hash)", ""
                    )
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
                ("created_at", "2026-01-01T00:00:00Z"),
            )
            connection.execute("PRAGMA user_version = {0}".format(SCHEMA_VERSION))
            connection.commit()

        with pytest.raises(SchemaVersionError, match="schema objects"):
            CacheIndex(database_path).check_schema()

    @pytest.mark.parametrize(
        "meta_version, pragma_version, message",
        [
            (SCHEMA_VERSION + 1, SCHEMA_VERSION, "disagrees"),
            (SCHEMA_VERSION + 1, SCHEMA_VERSION + 1, "unsupported"),
        ],
    )
    def test_schema_version_or_meta_mismatch_fails_closed(
        self, tmp_path, meta_version, pragma_version, message
    ):
        index = _initialized_index(tmp_path)
        with sqlite3.connect(str(index.database_path)) as connection:
            connection.execute(
                "UPDATE schema_meta SET value = ? WHERE key = ?",
                (str(meta_version), SCHEMA_VERSION_KEY),
            )
            connection.execute("PRAGMA user_version = {0}".format(pragma_version))
            connection.commit()

        with pytest.raises(SchemaVersionError, match=message):
            CacheIndex(index.database_path).check_schema()

    def test_missing_index_read_fails_without_creating_a_database(self, tmp_path):
        database_path = (tmp_path / "absent" / "index.sqlite").absolute()
        index = CacheIndex(database_path)

        with pytest.raises(IndexNotFoundError):
            index.check_schema()

        assert not database_path.exists()
        assert not database_path.parent.exists()


def test_windows_paths_are_normalized_without_cwd_dependence():
    absolute = normalize_absolute_source_path(
        r"e:\project\OpenGU\results\score_cache\if\..\if\abc.npz"
    )
    relative = normalize_relative_path(r"score_cache\if\.\abc.npz")
    record = LegacySourceRecord(
        legacy_kind="score_cache",
        legacy_path=r"score_cache\if\.\abc.npz",
        path_kind=PathKind.RELATIVE,
        source_root=r"e:\project\OpenGU\results",
        verification_status=VerificationStatus.UNKNOWN,
    )

    assert absolute == "E:/project/OpenGU/results/score_cache/if/abc.npz"
    assert relative == "score_cache/if/abc.npz"
    assert record.legacy_path == "score_cache/if/abc.npz"
    assert record.source_root == "E:/project/OpenGU/results"
    with pytest.raises(PathValidationError, match="explicitly absolute"):
        CacheIndex(Path("relative-index.sqlite"))
    with pytest.raises(PathValidationError, match="must not traverse"):
        normalize_relative_path(r"score_cache\..\outside.json")


class TestLegacyIndexer:
    def test_dry_run_is_zero_write_and_preserves_source_hash_and_mtime(
        self, tmp_path
    ):
        root = tmp_path / "results"
        key = "a" * 32
        _write_json(root / "cache" / (key + ".json"), _result_cache_payload(key))
        before = _file_snapshot(root)

        indexer = LegacyIndexer(root.absolute())
        report = indexer.scan()

        assert report.summary()["discovered_files"] == 1
        assert report.summary()["logical_sources"] == 1
        assert _file_snapshot(root) == before
        assert not indexer.index_path.exists()
        assert not (root / "cache_v2").exists()

    def test_corrupt_json_is_reported_and_other_files_continue(self, tmp_path):
        root = tmp_path / "results"
        good_key = "b" * 32
        bad_key = "c" * 32
        _write_json(
            root / "cache" / (good_key + ".json"),
            _result_cache_payload(good_key),
        )
        bad_path = root / "cache" / (bad_key + ".json")
        bad_path.parent.mkdir(parents=True, exist_ok=True)
        bad_path.write_text("{broken json", encoding="utf-8")

        report = LegacyIndexer(root.absolute()).scan()
        by_path = {record.source_path: record for record in report.records}

        assert len(report.records) == 2
        assert by_path["cache/{0}.json".format(good_key)].status == "unknown"
        assert by_path["cache/{0}.json".format(good_key)].content_hash is not None
        assert by_path["cache/{0}.json".format(bad_key)].status == "corrupt"
        assert report.anomaly_counts()["json_decode_error"] == 1

    def test_nonfinite_json_is_corrupt_and_does_not_block_apply(self, tmp_path):
        root = tmp_path / "results"
        good_key = "a" * 32
        bad_key = "b" * 32
        _write_json(
            root / "cache" / (good_key + ".json"),
            _result_cache_payload(good_key),
        )
        bad_path = root / "cache" / (bad_key + ".json")
        bad_path.parent.mkdir(parents=True, exist_ok=True)
        bad_path.write_text(
            '{"cache_key":"%s","config":{"unlearn_ratio":NaN}}' % bad_key,
            encoding="utf-8",
        )

        indexer = LegacyIndexer(root.absolute())
        report = indexer.scan()
        by_path = {record.source_path: record for record in report.records}

        assert by_path["cache/{0}.json".format(bad_key)].status == "corrupt"
        assert report.anomaly_counts()["json_decode_error"] == 1

        index = CacheIndex(indexer.index_path.absolute())
        index.initialize()
        outcome = indexer.apply(index, report)
        assert outcome["legacy_sources_written"] == 2
        assert len(index.legacy_sources()) == 2

    @pytest.mark.parametrize("strategy", ["random", "tracin", "hybrid"])
    def test_run_selection_missing_seed_is_never_complete(self, tmp_path, strategy):
        root = tmp_path / "results"
        root.mkdir(parents=True)
        config = {
            "strategy_name": strategy,
            "graph_fingerprint": "1" * 32,
            "k": 2,
            "is_transductive": True,
            "is_balanced": False,
            "train_ratio": 0.8,
            "val_ratio": 0.1,
            "test_ratio": 0.1,
            "base_model": "GCN",
            "loss": "cross_entropy",
            "fusion_method": "rank",
            "hybrid_alpha": 0.5,
            "propagation_prob": 0.1,
            "mc_rounds": 100,
            "candidate_fraction": 1.0,
            "im_batch_size": 5,
            "im_selector_seed": 2024,
        }
        indexer = LegacyIndexer(root.absolute())

        recipe, identity_complete = indexer._run_selection_recipe(
            config, root / "runs" / "fixture" / "attack.json"
        )

        assert recipe is not None
        assert recipe["selector"]["seed"] is None
        assert identity_complete is False
        assert indexer._anomalies[-1].code == "recipe_incomplete"
        assert "random_seed" in indexer._anomalies[-1].details["missing_fields"]

    def test_archive_deprecated_backup_and_cache_v2_are_excluded(self, tmp_path):
        root = tmp_path / "results"
        active_key = "d" * 32
        _write_json(
            root / "cache" / (active_key + ".json"),
            _result_cache_payload(active_key),
        )
        excluded_names = (
            "_archive_2025",
            "_archive2025",
            "deprecated_outputs",
            "backup",
            "backup-2025",
            "backup2025",
            "cache_v2",
        )
        for index, name in enumerate(excluded_names):
            hidden_key = str(index + 1) * 32
            _write_json(
                root / name / "cache" / (hidden_key + ".json"),
                _result_cache_payload(hidden_key),
            )

        report = LegacyIndexer(root.absolute()).scan()

        assert {state.path for state in report.file_states} == {
            "cache/{0}.json".format(active_key)
        }
        assert {record.source_path for record in report.records} == {
            "cache/{0}.json".format(active_key)
        }
        assert set(report.excluded_paths) == set(excluded_names)

    def test_npz_without_sidecar_is_reported_but_still_indexed_as_legacy(
        self, tmp_path
    ):
        root = tmp_path / "results"
        key = "e" * 32
        npz_path = root / "score_cache" / "if" / (key + ".npz")
        npz_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            str(npz_path),
            candidates=np.array([1, 2, 3], dtype=np.int64),
            scores=np.array([0.3, 0.2, 0.1], dtype=np.float32),
        )

        indexer = LegacyIndexer(root.absolute())
        report = indexer.scan()
        record = next(item for item in report.records if item.legacy_kind == "score_cache")
        sources, conflicts = indexer.to_contract_plan(report)

        assert report.anomaly_counts()["npz_sidecar_missing"] == 1
        assert record.source_paths == ("score_cache/if/{0}.npz".format(key),)
        assert record.artifact_type == "score"
        assert record.identity_complete is False
        assert record.status == "unknown"
        assert record.verification_status == "degraded"
        assert sources[0].artifact_id is None
        assert sources[0].observed_artifact_type == ArtifactType.SCORE
        assert conflicts == []

    def test_same_legacy_recipe_with_different_content_is_summarized_as_conflict(
        self, tmp_path
    ):
        root = tmp_path / "results"
        first_key = "f" * 32
        second_key = "0" * 32
        _write_json(
            root / "selection_cache" / (first_key + ".json"),
            _selection_cache_payload(first_key, [1, 2]),
        )
        _write_json(
            root / "selection_cache" / (second_key + ".json"),
            _selection_cache_payload(second_key, [1, 3]),
        )

        report = LegacyIndexer(root.absolute()).scan()

        assert len(report.conflicts) == 1
        assert report.conflicts[0].artifact_type == "selection"
        assert len(report.conflicts[0].content_hashes) == 2
        assert report.summary()["conflict_groups"] == 1
        assert report.anomaly_counts()["recipe_content_conflict"] == 1

    def test_result_cache_apply_remains_legacy_only(self, tmp_path):
        root = tmp_path / "results"
        key = "9" * 32
        source = _write_json(
            root / "cache" / (key + ".json"), _result_cache_payload(key)
        )
        source_before = _file_snapshot(source.parent)
        indexer = LegacyIndexer(root.absolute())
        report = indexer.scan()
        result_record = next(
            item for item in report.records if item.legacy_kind == "result_cache"
        )

        assert result_record.artifact_type is None
        assert result_record.recipe_hash is None
        index = CacheIndex(indexer.index_path.absolute())
        index.initialize()
        outcome = indexer.apply(index, report)

        assert outcome["formal_artifacts_written"] == 0
        assert len(index.legacy_sources()) == 1
        assert index.legacy_sources()[0]["artifact_id"] is None
        assert index.legacy_sources()[0]["observed_artifact_type"] is None
        assert _file_snapshot(source.parent) == source_before
        with sqlite3.connect(str(index.database_path)) as connection:
            assert connection.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0] == 0
        v2_files = sorted(
            path.relative_to(root).as_posix()
            for path in (root / "cache_v2").rglob("*")
            if path.is_file()
        )
        assert v2_files == ["cache_v2/index.sqlite"]

    def test_apply_rejects_a_stale_scan_report(self, tmp_path):
        root = tmp_path / "results"
        key = "7" * 32
        source = _write_json(
            root / "cache" / (key + ".json"), _result_cache_payload(key)
        )
        indexer = LegacyIndexer(root.absolute())
        report = indexer.scan()
        source.write_text("{\"changed\": true}", encoding="utf-8")
        index = CacheIndex(indexer.index_path.absolute())
        index.initialize()

        with pytest.raises(LegacySourceChangedError, match="changed after scan"):
            indexer.apply(index, report)

        assert index.legacy_sources() == []


def test_cachectl_real_argv_dry_run_imports_safely_and_writes_nothing(tmp_path):
    root = tmp_path / "results"
    key = "8" * 32
    _write_json(root / "cache" / (key + ".json"), _result_cache_payload(key))
    before = _file_snapshot(root)

    completed = _run_cachectl(
        ["legacy", "index", "--root", str(root.absolute()), "--dry-run"],
        cwd=tmp_path,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True
    assert payload["mode"] == "dry-run"
    assert payload["writes"] == []
    assert payload["report"]["summary"]["discovered_files"] == 1
    # Passing cachectl's real subcommand argv would make config.py's eager
    # argument parser fail if the CLI accidentally imported attack/config.
    assert _file_snapshot(root) == before
    assert not (root / "cache_v2").exists()


def test_exact_resolver_and_cli_explain_status_conflict_and_miss(tmp_path):
    index = _initialized_index(tmp_path)
    recipe = ArtifactRecipe(
        {"kind": "selection", "graph_fingerprint": "fixture-graph", "k": 2}
    )
    original = _artifact_header(ArtifactType.SELECTION, recipe, b"[1,2]")
    index.register_artifact(original)

    resolver = ArtifactResolver(index)
    clean = resolver.explain_exact(ArtifactType.SELECTION, recipe)
    assert clean.hit is True
    assert clean.status == ArtifactStatus.VALID
    assert clean.miss_reasons == ()

    recipe_path = _write_json(tmp_path / "recipe.json", recipe.fields)
    status = _run_cachectl(
        [
            "artifact",
            "status",
            original.artifact_id,
            "--db",
            str(index.database_path),
        ],
        cwd=tmp_path,
    )
    assert status.returncode == 0, status.stderr
    status_payload = json.loads(status.stdout)
    assert status_payload["status"] == "valid"
    assert status_payload["artifact"]["artifact_id"] == original.artifact_id

    exact = _run_cachectl(
        [
            "resolve",
            "explain",
            "--type",
            "selection",
            "--recipe",
            str(recipe_path),
            "--db",
            str(index.database_path),
        ],
        cwd=tmp_path,
    )
    assert exact.returncode == 0, exact.stderr
    exact_payload = json.loads(exact.stdout)
    assert exact_payload["explanation"]["hit"] is True
    assert exact_payload["execution_performed"] is False
    assert exact_payload["writes"] == []

    conflicting = _artifact_header(ArtifactType.SELECTION, recipe, b"[1,3]")
    assert index.register_artifact(conflicting).outcome == RegisterOutcome.CONFLICT
    blocked = resolver.explain_exact(ArtifactType.SELECTION, recipe)
    assert blocked.hit is False
    assert any("conflict" in reason for reason in blocked.miss_reasons)

    conflict_explain = _run_cachectl(
        [
            "resolve",
            "explain",
            "--type",
            "selection",
            "--recipe",
            str(recipe_path),
            "--db",
            str(index.database_path),
        ],
        cwd=tmp_path,
    )
    assert conflict_explain.returncode == 0, conflict_explain.stderr
    conflict_payload = json.loads(conflict_explain.stdout)
    assert conflict_payload["explanation"]["hit"] is False
    assert any(
        "conflict" in reason
        for reason in conflict_payload["explanation"]["miss_reasons"]
    )

    missing_recipe_path = _write_json(
        tmp_path / "missing_recipe.json",
        {"kind": "selection", "graph_fingerprint": "missing", "k": 99},
    )
    missing = _run_cachectl(
        [
            "resolve",
            "explain",
            "--type",
            "selection",
            "--recipe",
            str(missing_recipe_path),
            "--db",
            str(index.database_path),
        ],
        cwd=tmp_path,
    )
    assert missing.returncode == 0, missing.stderr
    missing_payload = json.loads(missing.stdout)
    assert missing_payload["explanation"]["hit"] is False
    assert missing_payload["explanation"]["miss_reasons"] == [
        "no_exact_candidate"
    ]
    assert missing_payload["execution_performed"] is False
    assert missing_payload["writes"] == []


def test_artifact_status_includes_legacy_only_recipe_conflicts(tmp_path):
    index = _initialized_index(tmp_path)
    recipe = ArtifactRecipe(
        {"kind": "selection", "graph_fingerprint": "fixture-graph", "k": 2}
    )
    header = _artifact_header(ArtifactType.SELECTION, recipe, b"[1,2]")
    index.register_artifact(header)
    conflict = ArtifactConflictRecord(
        artifact_type=header.artifact_type,
        recipe_hash=header.recipe_hash,
        existing_artifact_id=None,
        existing_content_hash="b" * 64,
        observed_content_hash="c" * 64,
        metadata={"legacy_only": True},
    )
    index.record_conflict(conflict)

    completed = _run_cachectl(
        [
            "artifact",
            "status",
            header.artifact_id,
            "--db",
            str(index.database_path),
        ],
        cwd=tmp_path,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert len(payload["conflicts"]) == 1
    assert payload["conflicts"][0]["existing_artifact_id"] is None


def test_resolve_explain_reports_legacy_exact_candidate_without_promoting_it(tmp_path):
    index = _initialized_index(tmp_path)
    recipe = ArtifactRecipe(
        {"kind": "selection", "graph_fingerprint": "legacy-graph", "k": 2}
    )
    source = LegacySourceRecord(
        legacy_kind="selection_cache",
        legacy_path="selection_cache/fixture.json",
        path_kind=PathKind.RELATIVE,
        source_root=str((tmp_path / "results").absolute()),
        observed_artifact_type=ArtifactType.SELECTION,
        observed_recipe_hash=recipe.recipe_hash,
        raw_content_hash="a" * 64,
        semantic_content_hash="b" * 64,
        verification_status=VerificationStatus.DEGRADED,
    )
    index.register_legacy_source(source)

    explanation = ArtifactResolver(index).explain_exact(
        ArtifactType.SELECTION, recipe
    )

    assert explanation.hit is False
    assert explanation.exact_candidate is None
    assert len(explanation.legacy_exact_candidates) == 1
    assert explanation.legacy_exact_candidates[0]["legacy_source_id"] == source.legacy_source_id
    assert "legacy_exact_candidate_not_authoritative" in explanation.miss_reasons
    assert "legacy_candidate_verification_degraded" in explanation.miss_reasons
    assert index.find_artifact(ArtifactType.SELECTION, recipe.recipe_hash) is None


def test_cachectl_distinguishes_plain_fields_key_from_recipe_wrapper(tmp_path):
    index = _initialized_index(tmp_path)
    recipe = ArtifactRecipe(
        {
            "kind": "selection",
            "fields": {"candidate_set_hash": "fixture"},
            "k": 2,
        }
    )
    header = _artifact_header(ArtifactType.SELECTION, recipe, b"[1,2]")
    index.register_artifact(header)
    plain_path = _write_json(tmp_path / "plain.json", recipe.fields)
    wrapped_path = _write_json(tmp_path / "wrapped.json", recipe.to_dict())

    for recipe_path in (plain_path, wrapped_path):
        completed = _run_cachectl(
            [
                "resolve",
                "explain",
                "--type",
                "selection",
                "--recipe",
                str(recipe_path),
                "--db",
                str(index.database_path),
            ],
            cwd=tmp_path,
        )
        assert completed.returncode == 0, completed.stderr
        payload = json.loads(completed.stdout)
        assert payload["explanation"]["recipe_hash"] == recipe.recipe_hash
        assert payload["explanation"]["hit"] is True
