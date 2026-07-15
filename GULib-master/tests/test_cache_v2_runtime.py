import hashlib
import json
from pathlib import Path

import pytest

from cache_v2 import ArtifactRecipe, ProducerVersion
from cache_v2.errors import ArtifactNotFoundError, CacheResolutionError
from cache_v2.runtime import load_selection_artifact
from cache_v2.store import ArtifactStore


CANDIDATES = (0, 1, 2, 3, 4)


def _candidate_hash(nodes):
    payload = json.dumps(
        sorted(nodes), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _fixture(tmp_path):
    root = (tmp_path / "store").resolve()
    producer = ProducerVersion(
        semantic_version="runtime-fixture-v1", source_fingerprint="a" * 64
    )
    store = ArtifactStore(root, producer_version=producer)
    store.initialize()
    recipe = ArtifactRecipe(
        {
            "graph_fingerprint": "b" * 64,
            "candidate_set_hash": _candidate_hash(CANDIDATES),
            "node_id_space": "global",
            "selector": "degree",
            "selector_algorithm_version": "fixture-v1",
            "k": 2,
        }
    )
    result = store.store_selection(
        recipe, [4, 2], num_nodes=5, candidate_nodes=CANDIDATES
    )
    return root, result


def _file_state(root):
    return {
        path.relative_to(root).as_posix(): (
            path.stat().st_size,
            path.stat().st_mtime_ns,
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in root.rglob("*")
        if path.is_file()
    }


def test_runtime_artifact_id_load_is_exact_verified_and_zero_write(tmp_path):
    root, stored = _fixture(tmp_path)
    before = _file_state(root)

    loaded = load_selection_artifact(
        root,
        stored.artifact_id,
        num_nodes=5,
        candidate_nodes=CANDIDATES,
        expected_selector="degree",
        expected_k=2,
    )

    assert loaded.selected_nodes == (4, 2)
    assert loaded.artifact_id == stored.artifact_id
    assert loaded.content_hash == stored.content_hash
    assert loaded.authoritative is True
    assert loaded.provenance(root)["hit_source"] == "cache_v2:" + stored.artifact_id
    assert _file_state(root) == before


def test_runtime_load_never_substitutes_artifact_or_candidate_set(tmp_path):
    root, stored = _fixture(tmp_path)
    with pytest.raises(ArtifactNotFoundError):
        load_selection_artifact(
            root,
            "sel_deadbeef_deadbeef",
            num_nodes=5,
            candidate_nodes=CANDIDATES,
        )
    with pytest.raises(CacheResolutionError, match="strategy"):
        load_selection_artifact(
            root,
            stored.artifact_id,
            num_nodes=5,
            candidate_nodes=CANDIDATES,
            expected_selector="random",
        )
    with pytest.raises(Exception, match="candidate_set_hash"):
        load_selection_artifact(
            root,
            stored.artifact_id,
            num_nodes=5,
            candidate_nodes=(0, 1, 2, 3),
        )
