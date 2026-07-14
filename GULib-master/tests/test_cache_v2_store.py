"""Isolated Selection payload-store tests for the Cache V2 canary."""

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
    semantic_version="cache-v2-canary-test-v1",
    source_fingerprint="test-source-fingerprint",
)


def _recipe(
    k=2,
    selector="pagerank",
    graph_hash=GRAPH_HASH,
    candidate_hash=CANDIDATE_HASH,
):
    return ArtifactRecipe(
        {
            "artifact_kind": "selection",
            "topology_fingerprint": graph_hash,
            "candidate_set_hash": candidate_hash,
            "node_id_space": "global",
            "selector": selector,
            "selector_algorithm_version": "test-v1",
            "selection_rule": "topk_desc",
            "k": k,
        }
    )


def _store(tmp_path):
    store = ArtifactStore(
        (tmp_path / "cache-v2-canary").absolute(),
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


def _row_count(database_path, table):
    with sqlite3.connect(str(database_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]


def _concurrent_worker(root, start_event, result_queue):
    store = ArtifactStore(Path(root), producer_version=PRODUCER_VERSION)
    start_event.wait(10)

    def producer():
        time.sleep(0.25)
        return [7, 2]

    try:
        result = store.get_or_compute(
            _recipe(),
            producer,
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


def test_selection_payload_is_versioned_canonical_and_validates_recipe_bounds():
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
    first.validate_against(recipe, num_nodes=8)

    with pytest.raises(ArtifactIntegrityError, match="outside"):
        first.validate_against(recipe, num_nodes=7)
    with pytest.raises(ArtifactIntegrityError, match="not canonical JSON"):
        SelectionPayload.from_bytes(first.canonical_bytes + b"\n")
    with pytest.raises(ContractValidationError, match="duplicates"):
        SelectionPayload.build([2, 2], GRAPH_HASH, CANDIDATE_HASH)
    with pytest.raises(ContractValidationError, match="not an integer"):
        SelectionPayload.build([2.0, 7], GRAPH_HASH, CANDIDATE_HASH)


def test_selection_payload_validates_candidate_hash_and_membership():
    candidates = [1, 2, 7]
    candidate_hash = _candidate_hash(candidates)
    recipe = _recipe(candidate_hash=candidate_hash)
    valid = SelectionPayload.build([7, 2], GRAPH_HASH, candidate_hash)
    valid.validate_against(recipe, num_nodes=10, candidate_nodes=candidates)

    with pytest.raises(ArtifactIntegrityError, match="candidate_set_hash"):
        valid.validate_against(recipe, num_nodes=10, candidate_nodes=[1, 2, 8])

    non_member = SelectionPayload.build([7, 3], GRAPH_HASH, candidate_hash)
    with pytest.raises(ArtifactIntegrityError, match="not members"):
        non_member.validate_against(
            recipe, num_nodes=10, candidate_nodes=candidates
        )


def test_store_apis_require_candidates_and_reject_mismatch_before_producer(
    tmp_path,
):
    store = _store(tmp_path)
    recipe = _recipe()

    with pytest.raises(TypeError, match="candidate_nodes"):
        store.load(recipe, num_nodes=10)
    with pytest.raises(TypeError, match="candidate_nodes"):
        store.get_or_compute(recipe, lambda: [7, 2], num_nodes=10)
    with pytest.raises(TypeError, match="candidate_nodes"):
        store.observe_recomputation(recipe, lambda: [7, 2], num_nodes=10)

    producer_calls = []

    def producer():
        producer_calls.append(True)
        return [7, 2]

    with pytest.raises(ContractValidationError, match="candidate_nodes is required"):
        store.get_or_compute(
            recipe, producer, num_nodes=10, candidate_nodes=None
        )
    with pytest.raises(
        ContractValidationError, match="candidate_set_hash"
    ):
        store.get_or_compute(
            recipe,
            producer,
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES[:-1],
        )
    assert producer_calls == []
    assert store.producer_call_count == 0


def test_cold_then_new_process_warm_hit_never_calls_producer_or_touches_payload(
    tmp_path,
):
    recipe = _recipe()
    cold_store = _store(tmp_path)
    cold = cold_store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
        request_envelope={
            "config_name": "phase-a",
            "yaml_path": "experiments/a.yaml",
            "experiment_id": "exp-a",
        },
    )
    payload_path = cold_store.root.joinpath(*Path(cold.semantic_path).parts)
    before = _snapshot(payload_path)

    assert cold.hit is False
    assert cold.outcome == "created"
    assert cold.producer_called is True
    assert cold_store.producer_call_count == 1
    assert _row_count(cold_store.index.database_path, "artifacts") == 1

    # Reconstruct the store to prove the warm hit is persistent, not in-memory.
    warm_store = ArtifactStore(cold_store.root, producer_version=PRODUCER_VERSION)
    warm_store.initialize()
    warm = warm_store.get_or_compute(
        recipe,
        lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
        request_envelope={
            "config_name": "renamed",
            "yaml_path": "elsewhere/renamed.yaml",
            "experiment_id": "different-experiment",
        },
        fail_if_called=True,
    )

    assert warm.hit is True
    assert warm.outcome == "hit"
    assert warm.producer_called is False
    assert warm.artifact_id == cold.artifact_id
    assert warm.content_hash == cold.content_hash
    assert warm.payload.selected_nodes_ordered == (7, 2)
    assert warm_store.producer_call_count == 1
    assert _snapshot(payload_path) == before
    assert _row_count(warm_store.index.database_path, "artifacts") == 1
    assert _row_count(warm_store.index.database_path, "artifact_conflicts") == 0


def test_two_processes_coordinate_one_recipe_and_publish_once(tmp_path):
    store = _store(tmp_path)
    context = multiprocessing.get_context("spawn")
    start_event = context.Event()
    result_queue = context.Queue()
    processes = [
        context.Process(
            target=_concurrent_worker,
            args=(str(store.root), start_event, result_queue),
        )
        for _ in range(2)
    ]
    for process in processes:
        process.start()
    start_event.set()
    results = [result_queue.get(timeout=30) for _ in processes]
    for process in processes:
        process.join(timeout=30)
        assert process.exitcode == 0

    assert all("error" not in result for result in results), results
    assert len({result["artifact_id"] for result in results}) == 1
    assert sorted(result["producer_called"] for result in results) == [False, True]
    assert sorted(result["outcome"] for result in results) == ["created", "hit"]
    assert store.producer_call_count == 1
    assert _row_count(store.index.database_path, "artifacts") == 1
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0


def test_recipe_parameter_change_is_a_miss_and_creates_a_second_artifact(tmp_path):
    store = _store(tmp_path)
    first = store.get_or_compute(
        _recipe(k=2),
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    second = store.get_or_compute(
        _recipe(k=1),
        lambda: [3],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )

    assert first.artifact_id != second.artifact_id
    assert second.hit is False
    assert second.miss_reasons == ("no_exact_candidate",)
    assert store.producer_call_count == 2
    assert _row_count(store.index.database_path, "artifacts") == 2


def test_identical_explicit_recomputation_is_idempotent(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    before = (_snapshot(payload_path), _snapshot(header_path))

    observed = store.observe_recomputation(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )

    assert observed.outcome == "identical"
    assert observed.artifact_id == original.artifact_id
    assert store.producer_call_count == 2
    assert (_snapshot(payload_path), _snapshot(header_path)) == before
    assert _row_count(store.index.database_path, "artifacts") == 1
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0


def test_different_explicit_recomputation_is_quarantined_without_overwrite(
    tmp_path,
):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    before = (_snapshot(payload_path), _snapshot(header_path))

    with pytest.raises(ArtifactConflictError) as caught:
        store.observe_recomputation(
            recipe,
            lambda: [7, 3],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )

    assert (_snapshot(payload_path), _snapshot(header_path)) == before
    assert _row_count(store.index.database_path, "artifacts") == 1
    assert _row_count(store.index.database_path, "artifact_conflicts") == 1
    formal = store.index.find_artifact(ArtifactType.SELECTION, recipe.recipe_hash)
    assert formal["artifact_id"] == original.artifact_id
    assert formal["content_hash"] == original.content_hash
    assert formal["status"] == ArtifactStatus.VALID.value
    conflict = store.index.conflicts(
        artifact_type=ArtifactType.SELECTION, recipe_hash=recipe.recipe_hash
    )[0]
    assert conflict["conflict_id"] == caught.value.conflict_id
    assert conflict["quarantine_path"] == caught.value.quarantine_path
    quarantine = store.root.joinpath(*Path(caught.value.quarantine_path).parts)
    assert quarantine.is_file()
    assert SelectionPayload.from_bytes(quarantine.read_bytes()).selected_nodes_ordered == (
        7,
        3,
    )

    with pytest.raises(ArtifactConflictError) as second_caught:
        store.observe_recomputation(
            recipe,
            lambda: [7, 4],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert second_caught.value.quarantine_path != caught.value.quarantine_path
    second_quarantine = store.root.joinpath(
        *Path(second_caught.value.quarantine_path).parts
    )
    assert second_quarantine.is_file()
    conflicts = store.index.conflicts(
        artifact_type=ArtifactType.SELECTION, recipe_hash=recipe.recipe_hash
    )
    assert len(conflicts) == 2
    assert {row["quarantine_path"] for row in conflicts} == {
        caught.value.quarantine_path,
        second_caught.value.quarantine_path,
    }

    # Once conflict exists, normal resolution stops before a producer call.
    calls_before = store.producer_call_count
    with pytest.raises(CacheResolutionError, match="conflict"):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == calls_before


def test_conflict_marker_survives_sqlite_failure_and_blocks_future_hit(
    tmp_path, monkeypatch
):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    before_payload = _snapshot(payload_path)

    def fail_conflict_registration(self, conflict):
        raise RuntimeError("injected conflict registration failure")

    monkeypatch.setattr(
        CacheIndexBatch, "record_conflict", fail_conflict_registration
    )
    with pytest.raises(RuntimeError, match="conflict registration failure"):
        store.observe_recomputation(
            recipe,
            lambda: [7, 3],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )

    assert _row_count(store.index.database_path, "artifact_conflicts") == 0
    marker_semantic, marker_path = store._conflict_marker_paths(recipe)
    assert recipe.recipe_hash in marker_semantic
    assert marker_path.is_file()
    marker_bytes = marker_path.read_bytes()
    marker_value = json.loads(marker_bytes.decode("utf-8"))
    assert marker_value["recipe_hash"] == recipe.recipe_hash
    assert marker_value["existing_artifact_id"] == original.artifact_id
    assert marker_value["existing_content_hash"] == original.content_hash
    assert marker_value["observed_content_hash"] != original.content_hash
    assert marker_bytes == json.dumps(
        marker_value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    calls_before = store.producer_call_count
    with pytest.raises(CacheResolutionError, match="durable conflict marker"):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == calls_before
    assert _snapshot(payload_path) == before_payload
    assert marker_path.read_bytes() == marker_bytes


def test_conflict_marker_survives_quarantine_failure(tmp_path, monkeypatch):
    store = _store(tmp_path)
    recipe = _recipe()
    store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )

    def fail_quarantine(recipe_arg, payload_arg, compute_seconds_arg):
        raise RuntimeError("injected quarantine failure")

    monkeypatch.setattr(store, "_quarantine_observation", fail_quarantine)
    with pytest.raises(RuntimeError, match="quarantine failure"):
        store.observe_recomputation(
            recipe,
            lambda: [7, 3],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )

    _, marker_path = store._conflict_marker_paths(recipe)
    marker_bytes = marker_path.read_bytes()
    assert _row_count(store.index.database_path, "artifact_conflicts") == 0
    calls_before = store.producer_call_count
    with pytest.raises(CacheResolutionError, match="durable conflict marker"):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == calls_before
    assert marker_path.read_bytes() == marker_bytes


def test_incomplete_conflict_marker_directory_blocks_hit_without_producer(
    tmp_path,
):
    store = _store(tmp_path)
    recipe = _recipe()
    store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    _, marker_path = store._conflict_marker_paths(recipe)
    marker_path.parent.mkdir(parents=True)

    calls_before = store.producer_call_count
    with pytest.raises(CacheResolutionError, match="incomplete or unexpected"):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == calls_before


@pytest.mark.parametrize("corruption", ["payload_hash", "header_size"])
def test_corruption_fails_closed_without_recompute(tmp_path, corruption):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
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
            json.dumps(
                sidecar,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
        expected = "size does not match"

    before_calls = store.producer_call_count
    with pytest.raises(ArtifactIntegrityError, match=expected):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == before_calls
    assert _row_count(store.index.database_path, "artifacts") == 1


def test_header_tamper_fails_closed_against_index_contract(tmp_path):
    store = _store(tmp_path)
    recipe = _recipe()
    original = store.get_or_compute(
        recipe,
        lambda: [7, 2],
        num_nodes=10,
        candidate_nodes=CANDIDATE_NODES,
    )
    payload_path = store.root.joinpath(*Path(original.semantic_path).parts)
    header_path = payload_path.with_name("header.json")
    sidecar = json.loads(header_path.read_text(encoding="utf-8"))
    sidecar["artifact_header"]["producer_version"][
        "source_fingerprint"
    ] = "tampered-source"
    header_path.write_text(
        json.dumps(
            sidecar,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    before_calls = store.producer_call_count
    with pytest.raises(ArtifactIntegrityError, match="producer_version.*index"):
        store.get_or_compute(
            recipe,
            lambda: (_ for _ in ()).throw(AssertionError("producer was called")),
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert store.producer_call_count == before_calls


def test_registration_failure_never_removes_preexisting_formal_files(
    tmp_path, monkeypatch
):
    store = _store(tmp_path)
    recipe = _recipe()
    payload = SelectionPayload.build([7, 2], GRAPH_HASH, CANDIDATE_HASH)
    artifact_id = build_artifact_id(
        ArtifactType.SELECTION, recipe.recipe_hash, payload.content_hash
    )
    semantic, payload_path, header_path = store._formal_paths(recipe, artifact_id)
    store._atomic_write_once(payload_path, payload.canonical_bytes)
    sentinel_path = payload_path.parent / "preexisting-sentinel.txt"
    sentinel_path.write_text("must survive", encoding="utf-8")
    before = _snapshot(payload_path)

    def fail_registration(self, artifact_header):
        raise RuntimeError("injected registration failure")

    monkeypatch.setattr(CacheIndexBatch, "register_artifact", fail_registration)
    with pytest.raises(RuntimeError, match="injected registration failure"):
        store.get_or_compute(
            recipe,
            lambda: [7, 2],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )

    assert _snapshot(payload_path) == before
    assert not header_path.exists()
    assert sentinel_path.read_text(encoding="utf-8") == "must survive"
    assert _row_count(store.index.database_path, "artifacts") == 0


def test_store_rejects_relative_or_external_paths(tmp_path):
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
        ArtifactStore(
            root / "child" / ".." / "escape",
            producer_version=PRODUCER_VERSION,
        )

    with pytest.raises(PathValidationError, match=r"must not contain '\.\.'"):
        ArtifactStore(
            root,
            producer_version=PRODUCER_VERSION,
            trace_path=root / "child" / ".." / "trace.jsonl",
        )


def test_existing_symlink_escape_is_rejected_before_payload_write(tmp_path):
    store = _store(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    link = store.root / "artifacts"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip("directory symlinks are unavailable: {0}".format(exc))

    with pytest.raises(PathValidationError, match="below ArtifactStore root"):
        store.get_or_compute(
            _recipe(),
            lambda: [7, 2],
            num_nodes=10,
            candidate_nodes=CANDIDATE_NODES,
        )
    assert list(outside.iterdir()) == []
    assert _row_count(store.index.database_path, "artifacts") == 0
