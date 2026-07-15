import json
import hashlib
from pathlib import Path

import pytest

from cache_v2 import ArtifactRecipe, ArtifactResolver, ArtifactType, ProducerVersion
from cache_v2.conflict_resolution import ConflictResolutionLedger
from cache_v2.contracts import (
    ArtifactConflictRecord,
    LegacySourceRecord,
    PathKind,
    VerificationStatus,
)
from cache_v2.errors import CacheResolutionError, ContractValidationError
from cache_v2.index import CacheIndex
from cache_v2.store import ArtifactConflictError, ArtifactStore
from scripts import cachectl


CANDIDATES = (0, 1, 2, 3, 4)


def _candidate_hash(nodes):
    payload = json.dumps(
        sorted(nodes),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _recipe():
    return ArtifactRecipe(
        {
            "artifact_type": "selection",
            "graph_fingerprint": "f" * 64,
            "candidate_set_hash": _candidate_hash(CANDIDATES),
            "node_id_space": "global",
            "selector": "fixture",
            "selector_algorithm_version": "fixture-v1",
            "k": 2,
        }
    )


def _store(tmp_path):
    store = ArtifactStore(
        (tmp_path / "store").absolute(),
        producer_version=ProducerVersion(
            semantic_version="fixture-selection-v1",
            source_fingerprint="a" * 64,
        ),
    )
    store.initialize()
    return store


def _create_formal_conflict(store, recipe):
    original = store.store_selection(
        recipe,
        [1, 2],
        num_nodes=5,
        candidate_nodes=CANDIDATES,
    )
    with pytest.raises(ArtifactConflictError) as caught:
        store.store_selection(
            recipe,
            [1, 3],
            num_nodes=5,
            candidate_nodes=CANDIDATES,
        )
    conflict = store.index.conflicts(
        artifact_type=ArtifactType.SELECTION,
        recipe_hash=recipe.recipe_hash,
    )[0]
    assert conflict["conflict_id"] == caught.value.conflict_id
    return original, conflict


def test_keep_existing_resolution_is_dry_run_then_write_once_and_reenables_hit(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original, conflict = _create_formal_conflict(store, recipe)
    marker_semantic, marker_path = store._conflict_marker_paths(recipe)
    quarantine = store.root.joinpath(*Path(conflict["quarantine_path"]).parts)
    marker_before = marker_path.read_bytes()
    quarantine_before = quarantine.read_bytes()

    blocked = ArtifactResolver(store.index).explain_exact(
        ArtifactType.SELECTION, recipe
    )
    assert blocked.hit is False
    assert blocked.conflict_count == 1
    assert blocked.resolved_conflict_count == 0

    ledger = ConflictResolutionLedger(store.index)
    planned = ledger.keep_existing(
        conflict["conflict_id"],
        actor="cache-maintainer",
        reason="fixture producer v1 is the declared baseline",
        apply=False,
    )
    assert planned["mode"] == "dry-run"
    assert planned["writes"] == []
    assert not Path(planned["resolution_path"]).exists()
    assert ArtifactResolver(store.index).explain_exact(
        ArtifactType.SELECTION, recipe
    ).hit is False

    applied = ledger.keep_existing(
        conflict["conflict_id"],
        actor="cache-maintainer",
        reason="fixture producer v1 is the declared baseline",
        apply=True,
    )
    resolution_path = Path(applied["resolution_path"])
    assert applied["mode"] == "apply"
    assert applied["outcome"] == "created"
    assert applied["writes"] == [str(resolution_path)]
    raw = resolution_path.read_bytes()
    assert raw == json.dumps(
        json.loads(raw.decode("utf-8")),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    resolved = ArtifactResolver(store.index).explain_exact(
        ArtifactType.SELECTION, recipe
    )
    assert resolved.hit is True
    assert resolved.conflict_count == 0
    assert resolved.resolved_conflict_count == 1
    assert resolved.resolved_conflicts[0]["resolution"]["action"] == "keep_existing"

    hit = store.load_read_only(
        recipe, 5, candidate_nodes=CANDIDATES, artifact_id=original.artifact_id
    )
    assert hit.hit is True
    assert hit.artifact_id == original.artifact_id
    assert store.index.conflicts(recipe_hash=recipe.recipe_hash) == [conflict]
    assert marker_path.read_bytes() == marker_before
    assert quarantine.read_bytes() == quarantine_before
    assert marker_semantic in marker_path.as_posix()

    repeated = ledger.keep_existing(
        conflict["conflict_id"],
        actor="cache-maintainer",
        reason="fixture producer v1 is the declared baseline",
        apply=True,
    )
    assert repeated["outcome"] == "identical"
    assert repeated["writes"] == []

    with pytest.raises(ContractValidationError, match="write-once"):
        ledger.keep_existing(
            conflict["conflict_id"],
            actor="different-actor",
            reason="attempt to replace the audit decision",
            apply=True,
        )


def test_new_conflict_after_resolution_blocks_again(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    _, first = _create_formal_conflict(store, recipe)
    ledger = ConflictResolutionLedger(store.index)
    ledger.keep_existing(
        first["conflict_id"], actor="maintainer", reason="keep baseline", apply=True
    )
    assert ArtifactResolver(store.index).explain_exact(
        ArtifactType.SELECTION, recipe
    ).hit is True

    with pytest.raises(ArtifactConflictError) as caught:
        store.store_selection(
            recipe,
            [2, 3],
            num_nodes=5,
            candidate_nodes=CANDIDATES,
        )
    assert caught.value.conflict_id != first["conflict_id"]
    blocked = ArtifactResolver(store.index).explain_exact(
        ArtifactType.SELECTION, recipe
    )
    assert blocked.hit is False
    assert blocked.conflict_count == 1
    assert blocked.resolved_conflict_count == 1


def test_legacy_only_conflict_cannot_be_resolved_as_keep_existing(tmp_path):
    index = CacheIndex((tmp_path / "index.sqlite").absolute())
    index.initialize()
    source = LegacySourceRecord(
        legacy_kind="selection_cache",
        legacy_path="selection_cache/legacy.json",
        path_kind=PathKind.RELATIVE,
        source_root=str(tmp_path.absolute()),
        raw_content_hash="1" * 64,
        semantic_content_hash="2" * 64,
        verification_status=VerificationStatus.DEGRADED,
    )
    index.register_legacy_source(source)
    conflict = ArtifactConflictRecord(
        artifact_type=ArtifactType.SELECTION,
        recipe_hash="3" * 64,
        existing_content_hash="4" * 64,
        observed_content_hash="5" * 64,
        legacy_source_id=source.legacy_source_id,
    )
    index.record_conflict(conflict)

    with pytest.raises(ContractValidationError, match="formal existing Artifact"):
        ConflictResolutionLedger(index).keep_existing(
            conflict.conflict_id,
            actor="maintainer",
            reason="legacy rows cannot establish authority",
            apply=False,
        )
    assert index.conflicts()[0]["conflict_id"] == conflict.conflict_id


def test_corrupt_resolution_record_fails_closed(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    _, conflict = _create_formal_conflict(store, recipe)
    ledger = ConflictResolutionLedger(store.index)
    path = Path(ledger.resolution_path(conflict["conflict_id"]))
    path.parent.mkdir(parents=True)
    path.write_text('{"action":"keep_existing"}', encoding="utf-8")

    with pytest.raises(CacheResolutionError, match="resolution record"):
        ArtifactResolver(store.index).explain_exact(ArtifactType.SELECTION, recipe)


def test_cachectl_conflict_dry_run_apply_and_status(tmp_path, capsys):
    store = _store(tmp_path)
    recipe = _recipe()
    _, conflict = _create_formal_conflict(store, recipe)
    common = [
        conflict["conflict_id"],
        "--db",
        str(store.index.database_path),
    ]

    assert cachectl.main(["conflict", "status", *common]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["state"] == "unresolved"
    assert status["writes"] == []

    resolve_args = [
        "conflict",
        "resolve",
        *common,
        "--actor",
        "cache-maintainer",
        "--reason",
        "fixture baseline is authoritative",
    ]
    assert cachectl.main(resolve_args) == 0
    planned = json.loads(capsys.readouterr().out)
    assert planned["mode"] == "dry-run"
    assert planned["writes"] == []

    assert cachectl.main([*resolve_args, "--apply"]) == 0
    applied = json.loads(capsys.readouterr().out)
    assert applied["outcome"] == "created"
    assert len(applied["writes"]) == 1

    assert cachectl.main(["conflict", "status", *common]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["state"] == "resolved"
    assert status["resolution"]["action"] == "keep_existing"
