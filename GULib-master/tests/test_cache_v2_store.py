"""Pure Recipe/Artifact store tests for Cache V2 Selection."""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import sqlite3
import time
from pathlib import Path

import pytest

from cache_v2 import (
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    ProducerVersion,
    build_artifact_id,
)
from cache_v2.errors import ContractValidationError, PathValidationError
from cache_v2.index import CacheIndexBatch
from cache_v2.store import (
    ArtifactConflictError,
    ArtifactIntegrityError,
    ArtifactStore,
    CacheResolutionError,
    SelectionPayload,
)


def _candidate_hash(nodes):
    payload = json.dumps(
        sorted(nodes),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


GRAPH_HASH = "a" * 64
CANDIDATE_NODES = tuple(range(10))
CANDIDATE_HASH = _candidate_hash(CANDIDATE_NODES)
PRODUCER_VERSION = ProducerVersion(
    semantic_version="cache-v2-store-test-v2",
    source_fingerprint="test-source-fingerprint",
)


def _recipe(k=2, selector="pagerank", graph_hash=GRAPH_HASH):
    return ArtifactRecipe(
        {
            "artifact_kind": "selection",
            "topology_fingerprint": graph_hash,
            "candidate_set_hash": CANDIDATE_HASH,
            "node_id_space": "global",
            "selector": selector,
            "selector_algorithm_version": "test-v1",
            "selection_rule": "topk_desc",
            "k": k,
        }
    )


def _store(tmp_path):
    store = ArtifactStore(
        (tmp_path / "cache-v2-store").absolute(),
        producer_version=PRODUCER_VERSION,
    )
    store.initialize()
    return store


def _snapshot(path):
    stat = path.stat()
    return (
        hashlib.sha256(path.read_bytes()).hexdigest(),
        stat.st_mtime_ns,
        stat.st_size,
    )


def _tree_state(root):
    return {
        path.relative_to(root).as_posix(): _snapshot(path)
        for path in root.rglob("*")
        if path.is_file()
    }


def _row_count(database_path, table):
    with sqlite3.connect(str(database_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]


def _concurrent_store_worker(root, start_event, result_queue):
    store = ArtifactStore(Path(root), producer_version=PRODUCER_VERSION)
    start_event.wait(10)
    time.sleep(0.2)
    try:
        result = store.store_selection(
            _recipe(),
            [7, 2],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
        result_queue.put(
            {
                "artifact_id": result.artifact_id,
                "producer_called": result.producer_called,
                "outcome": result.outcome,
            }
        )
    except Exception as exc:  # pragma: no cover - surfaced by parent assertion
        result_queue.put({"error": repr(exc)})


def test_selection_payload_is_versioned_canonical_and_validates_identity():
    recipe = _recipe()
    first = SelectionPayload.build(
        [7, 2], GRAPH_HASH, CANDIDATE_HASH, node_id_space="global"
    )
    second = SelectionPayload.from_bytes(first.canonical_bytes)

    assert first == second
    assert json.loads(first.canonical_bytes.decode("utf-8"))["payload_version"] == 1
    assert first.ordered_nodes_hash != SelectionPayload.build(
        [2, 7], GRAPH_HASH, CANDIDATE_HASH
    ).ordered_nodes_hash
    assert first.node_set_hash == SelectionPayload.build(
        [2, 7], GRAPH_HASH, CANDIDATE_HASH
    ).node_set_hash
    first.validate_against(recipe, num_nodes=10, candidate_nodes=CANDIDATE_NODES)

    with pytest.raises(ArtifactIntegrityError, match="outside"):
        first.validate_against(recipe, num_nodes=7)
    with pytest.raises(ArtifactIntegrityError, match="candidate_set_hash"):
        first.validate_against(recipe, num_nodes=10, candidate_nodes=(0, 1, 2))


def test_store_has_no_producer_callback_and_candidate_recheck_is_optional(tmp_path):
    store = _store(tmp_path)
    assert not hasattr(store, "get_or_compute")
    assert not hasattr(store, "observe_recomputation")

    stored = store.store_selection(_recipe(), [7, 2], num_nodes=10)
    assert stored.producer_called is False

    with pytest.raises(ContractValidationError, match="candidate_set_hash"):
        store.store_selection(
            _recipe(selector="degree"),
            [2],
            num_nodes=10,
            candidate_nodes=(0, 1, 2),
        )


def test_cold_store_then_read_only_hit_is_zero_write(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    cold = store.store_selection(
        recipe,
        [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
        compute_seconds=0.25,
    )
    before = _tree_state(store.root)

    warm_store = ArtifactStore(store.root, producer_version=PRODUCER_VERSION)
    warm = warm_store.load_read_only(
        recipe,
        10,
        candidate_nodes=CANDIDATE_NODES,
        artifact_id=cold.artifact_id,
    )

    assert cold.hit is False
    assert cold.outcome == "created"
    assert warm.hit is True
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id
    assert warm.payload.selected_nodes_ordered == (7, 2)
    assert _tree_state(store.root) == before


def test_concurrent_explicit_stores_publish_one_immutable_artifact(tmp_path):
    store = _store(tmp_path)
    context = multiprocessing.get_context("spawn")
    start_event = context.Event()
    result_queue = context.Queue()
    processes = [
        context.Process(
            target=_concurrent_store_worker,
            args=(str(store.root), start_event, result_queue),
        )
        for _ in range(2)
    ]
    for process in processes:
        process.start()
    start_event.set()
    results = [result_queue.get(timeout=20) for _ in processes]
    for process in processes:
        process.join(timeout=20)
        assert process.exitcode == 0

    assert all("error" not in result for result in results), results
    assert len({result["artifact_id"] for result in results}) == 1
    assert {result["outcome"] for result in results} == {"created", "identical"}
    assert all(result["producer_called"] is False for result in results)
    assert _row_count(store.index.database_path, "artifacts") == 1
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0


def test_recipe_change_creates_a_second_artifact(tmp_path):
    store = _store(tmp_path)
    first = store.store_selection(
        _recipe(k=2), [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    second = store.store_selection(
        _recipe(k=1), [3], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    assert first.artifact_id != second.artifact_id
    assert second.miss_reasons == ("no_exact_candidate",)
    assert _row_count(store.index.database_path, "artifacts") == 2


def test_identical_explicit_store_is_idempotent(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    before = (_snapshot(payload_path), _snapshot(header_path))

    observed = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    assert observed.hit is True
    assert observed.outcome == "identical"
    assert observed.artifact_id == original.artifact_id
    assert (_snapshot(payload_path), _snapshot(header_path)) == before
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0


def test_different_explicit_store_is_quarantined_and_blocks_resolution(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    before = (_snapshot(payload_path), _snapshot(header_path))

    with pytest.raises(ArtifactConflictError) as caught:
        store.store_selection(
            recipe, [7, 3], num_nodes=10, candidate_nodes=CANDIDATE_NODES
        )

    assert (_snapshot(payload_path), _snapshot(header_path)) == before
    assert _row_count(store.index.database_path, "artifacts") == 1
    assert _row_count(store.index.database_path, "artifact_conflicts") == 1
    formal = store.index.find_artifact(ArtifactType.SELECTION, recipe.recipe_hash)
    assert formal["artifact_id"] == original.artifact_id
    assert formal["status"] == ArtifactStatus.VALID.value
    quarantine = store.root.joinpath(*Path(caught.value.quarantine_path).parts)
    assert SelectionPayload.from_bytes(quarantine.read_bytes()).selected_nodes_ordered == (
        7,
        3,
    )
    with pytest.raises(CacheResolutionError, match="conflict"):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


def test_conflict_marker_survives_sqlite_failure_and_blocks_hit(tmp_path, monkeypatch):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )

    def fail_conflict_registration(self, conflict):
        raise RuntimeError("injected conflict registration failure")

    monkeypatch.setattr(CacheIndexBatch, "record_conflict", fail_conflict_registration)
    with pytest.raises(RuntimeError, match="conflict registration failure"):
        store.store_selection(
            recipe, [7, 3], num_nodes=10, candidate_nodes=CANDIDATE_NODES
        )

    _, marker_path = store._conflict_marker_paths(recipe)
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    assert marker["existing_artifact_id"] == original.artifact_id
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0
    with pytest.raises(CacheResolutionError, match="durable conflict marker"):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


def test_conflict_marker_survives_quarantine_failure(tmp_path, monkeypatch):
    store = _store(tmp_path)
    recipe = _recipe()
    store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )

    def fail_quarantine(recipe_arg, payload_arg, compute_seconds_arg):
        raise RuntimeError("injected quarantine failure")

    monkeypatch.setattr(store, "_quarantine_observation", fail_quarantine)
    with pytest.raises(RuntimeError, match="quarantine failure"):
        store.store_selection(
            recipe, [7, 3], num_nodes=10, candidate_nodes=CANDIDATE_NODES
        )
    _, marker_path = store._conflict_marker_paths(recipe)
    assert marker_path.is_file()
    with pytest.raises(CacheResolutionError, match="durable conflict marker"):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


def test_incomplete_conflict_marker_directory_blocks_hit(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    _, marker_path = store._conflict_marker_paths(recipe)
    marker_path.parent.mkdir(parents=True)
    with pytest.raises(CacheResolutionError, match="incomplete or unexpected"):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


@pytest.mark.parametrize("corruption", ["payload_hash", "header_size"])
def test_corruption_fails_closed(tmp_path, corruption):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")

    if corruption == "payload_hash":
        changed = bytearray(payload_path.read_bytes())
        changed[0] = ord("[")
        payload_path.write_bytes(bytes(changed))
        expected = "content hash mismatch"
    else:
        sidecar = json.loads(header_path.read_text(encoding="utf-8"))
        sidecar["payload_contract"]["size_bytes"] += 1
        header_path.write_text(
            json.dumps(sidecar, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        expected = "size does not match"

    with pytest.raises(ArtifactIntegrityError, match=expected):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


def test_header_tamper_fails_closed_against_index(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.store_selection(
        recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    sidecar = json.loads(header_path.read_text(encoding="utf-8"))
    sidecar["artifact_header"]["producer_version"]["source_fingerprint"] = "tampered"
    header_path.write_text(
        json.dumps(sidecar, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    with pytest.raises(ArtifactIntegrityError, match="producer_version.*index"):
        store.load_read_only(recipe, 10, candidate_nodes=CANDIDATE_NODES)


def test_registration_failure_preserves_preexisting_formal_file(tmp_path, monkeypatch):
    store = _store(tmp_path)
    recipe = _recipe()
    payload = SelectionPayload.build([7, 2], GRAPH_HASH, CANDIDATE_HASH)
    artifact_id = build_artifact_id(
        ArtifactType.SELECTION, recipe.recipe_hash, payload.content_hash
    )
    _, payload_path, header_path = store._formal_paths(recipe, artifact_id)
    store._atomic_write_once(payload_path, payload.canonical_bytes)
    sentinel_path = payload_path.parent / "sentinel.txt"
    sentinel_path.write_text("must survive", encoding="utf-8")
    before = _snapshot(payload_path)

    def fail_registration(self, artifact_header):
        raise RuntimeError("injected registration failure")

    monkeypatch.setattr(CacheIndexBatch, "register_artifact", fail_registration)
    with pytest.raises(RuntimeError, match="registration failure"):
        store.store_selection(
            recipe, [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
        )
    assert _snapshot(payload_path) == before
    assert not header_path.exists()
    assert sentinel_path.read_text(encoding="utf-8") == "must survive"
    assert _row_count(store.index.database_path, "artifacts") == 0


def test_store_rejects_relative_external_and_symlink_paths(tmp_path):
    with pytest.raises(PathValidationError, match="explicitly absolute"):
        ArtifactStore(Path("relative-store"), producer_version=PRODUCER_VERSION)

    root = (tmp_path / "store").absolute()
    with pytest.raises(PathValidationError, match="below ArtifactStore root"):
        ArtifactStore(
            root,
            producer_version=PRODUCER_VERSION,
            trace_path=(tmp_path / "outside.jsonl").absolute(),
        )
    with pytest.raises(PathValidationError, match=r"must not contain '\.\.'"):
        ArtifactStore(root / "child" / ".." / "escape", producer_version=PRODUCER_VERSION)

    store = _store(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    link = store.root / "artifacts"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip("directory symlinks are unavailable: {0}".format(exc))
    with pytest.raises(PathValidationError, match="below ArtifactStore root"):
        store.store_selection(
            _recipe(), [7, 2], num_nodes=10, candidate_nodes=CANDIDATE_NODES
        )
    assert list(outside.iterdir()) == []
