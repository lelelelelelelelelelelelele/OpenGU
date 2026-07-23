import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from experiments.target_direct_v1 import PROFILE
from experiments.target_direct_v1 import build_manifest as manifest_module
from experiments.target_direct_v1.recipe import ALGORITHM_VERSION, SCORE_NAMES


GIT_SHA = "a" * 40


def _summary(seed: int, *, parameter_scope: str = "last_layer"):
    return {
        "schema": "target_direct_v1.selection_summary",
        "version": 1,
        "status": {"state": "success"},
        "algorithm_version": ALGORITHM_VERSION,
        "dataset": "Cora",
        "seed": seed,
        "processed_profile": PROFILE,
        "candidate_count": 20,
        "parameter_scope": parameter_scope,
        "budget": {"requested_ratio": 0.05, "expected_k": 1},
        "git_provenance": {"head": GIT_SHA, "worktree_dirty": False},
        "target_checkpoint": {
            "path": "checkpoint.pt",
            "file_sha256": "b" * 64,
            "state_hash": "c" * 64,
        },
        "score_bundle": {
            "artifact_id": "score_bundle",
            "recipe_hash": "d" * 64,
        },
        "selection_artifacts": {
            strategy: {
                "artifact": {
                    "artifact_id": "selection_" + strategy,
                    "recipe_hash": "e" * 64,
                    "content_hash": "f" * 64,
                }
            }
            for strategy in SCORE_NAMES
        },
    }


@pytest.fixture
def manifest_fakes(tmp_path, monkeypatch):
    profile_manifest = tmp_path / "profile.manifest.json"
    profile_manifest.write_text("{}\n", encoding="utf-8")
    inputs = SimpleNamespace(
        candidate_count=20,
        num_nodes=30,
        candidate_nodes=tuple(range(20)),
    )
    monkeypatch.setattr(
        manifest_module,
        "verify_profile",
        lambda **_kwargs: {
            "inputs": inputs,
            "data": object(),
            "manifest": {"selection_identity": {"candidate_count": 20}},
            "manifest_path": str(profile_manifest),
        },
    )
    monkeypatch.setattr(
        manifest_module,
        "data_identity",
        lambda _data: {"dataset": "cora", "split": PROFILE},
    )
    monkeypatch.setattr(
        manifest_module,
        "load_target_checkpoint",
        lambda *_args, **_kwargs: {
            "path": str(tmp_path / "checkpoint.pt"),
            "file_sha256": "b" * 64,
            "state_hash": "c" * 64,
            "checkpoints": [{}, {}],
            "metadata": {
                "dataset_name": "cora",
                "seed": 42,
                "data_identity": {"dataset": "cora", "split": PROFILE},
            },
        },
    )

    def load_selection(_root, artifact_id, **_kwargs):
        strategy = artifact_id[len("selection_") :]
        return SimpleNamespace(
            artifact_id=artifact_id,
            recipe_hash="e" * 64,
            content_hash="f" * 64,
            selected_nodes=(0,),
            selector=strategy,
        )

    monkeypatch.setattr(
        manifest_module, "load_selection_artifact", load_selection
    )
    return tmp_path


def test_gate_manifest_accepts_one_seed_and_orders_degree_first(
    manifest_fakes,
):
    summary_path = manifest_fakes / "cold.json"
    summary_path.write_text(json.dumps(_summary(42)), encoding="utf-8")
    order = ("degree",) + tuple(
        strategy for strategy in SCORE_NAMES if strategy != "degree"
    )

    manifest = manifest_module.build_manifest(
        repository_root=manifest_fakes,
        processed_root=manifest_fakes / "data" / "processed",
        selection_store_root=manifest_fakes / "selection",
        dataset="Cora",
        summaries=[summary_path],
        expected_git_sha=GIT_SHA,
        ratio=0.05,
        required_seeds=(42,),
        strategy_order=order,
    )

    assert manifest["seeds"] == [42]
    assert manifest["strategies"] == list(order)
    assert manifest["parameter_scope"] == "last_layer"
    assert manifest["cells"][0]["strategy"] == "degree"
    assert len(manifest["cells"]) == 17


def test_formal_manifest_rejects_all_trainable_summary(manifest_fakes):
    summary_path = manifest_fakes / "all_trainable.json"
    summary_path.write_text(
        json.dumps(_summary(42, parameter_scope="all_trainable")),
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError, match="Selection summary identity mismatch"
    ):
        manifest_module.build_manifest(
            repository_root=manifest_fakes,
            processed_root=manifest_fakes / "data" / "processed",
            selection_store_root=manifest_fakes / "selection",
            dataset="Cora",
            summaries=[summary_path],
            expected_git_sha=GIT_SHA,
            ratio=0.05,
            required_seeds=(42,),
        )


def test_formal_manifest_rejects_unapproved_seed_request(manifest_fakes):
    with pytest.raises(ValueError, match="required_seeds"):
        manifest_module.build_manifest(
            repository_root=manifest_fakes,
            processed_root=manifest_fakes / "data" / "processed",
            selection_store_root=manifest_fakes / "selection",
            dataset="Cora",
            summaries=[],
            expected_git_sha=GIT_SHA,
            ratio=0.05,
            required_seeds=(7,),
        )
