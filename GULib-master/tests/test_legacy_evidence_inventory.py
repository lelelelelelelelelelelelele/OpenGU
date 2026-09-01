from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from cache_v2.errors import ContractValidationError
from scripts.legacy_evidence_inventory import (
    build_inventory,
    build_ledger,
    compare_inventories,
    load_plan,
    write_once,
)


ROOT = Path(__file__).resolve().parents[1]


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("results/cache_v2/\nresults/cache/*.json\n", encoding="utf-8")
    (repo / "consumer.py").write_text(
        'cache = ResultCache("./results/cache")\n', encoding="utf-8"
    )
    (repo / "results" / "cache").mkdir(parents=True)
    (repo / "results" / "cache" / "legacy.json").write_text("{}", encoding="utf-8")
    (repo / "results" / "_archive_old").mkdir()
    (repo / "results" / "_archive_old" / "payload.json").write_text("{}", encoding="utf-8")
    (repo / "results" / "cache_v2").mkdir()
    (repo / "results" / "cache_v2" / "artifact.bin").write_bytes(b"v2")
    subprocess.run(["git", "add", ".gitignore", "consumer.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
    return repo


def _plan(path: Path) -> Path:
    value = {
        "schema": "opengu.legacy_evidence_batch_plan",
        "version": 1,
        "policy": {
            "cutoff": "2026-05-31T23:59:59+08:00",
            "archive_requires_state": "REPLACED",
            "delete_authorized": False,
            "legacy_cache_reuse": "forbidden_for_new_batches",
        },
        "devices": [
            {"id": "local", "role": "local review checkout"},
            {"id": "ssh", "role": "AutoDL active checkout"},
        ],
        "protected_paths": ["results/cache_v2"],
        "batches": [
            {
                "id": "legacy-result-cache",
                "description": "Legacy ResultCache",
                "evidence_class": "legacy_cache",
                "lifecycle_state": "INVALIDATED",
                "invalidation_reason": "not an authoritative formal cache",
                "replacement_basis": "Cache V2 only for exact current identities",
                "downstream_reference_basis": "consumer scan remains non-zero",
                "locations": {
                    "local": [
                        {
                            "path": "results/cache",
                            "disposition": "active_rollback_source",
                        }
                    ],
                    "ssh": [
                        {
                            "path": "results/cache",
                            "disposition": "active_rollback_source",
                        }
                    ],
                },
            },
            {
                "id": "already-archived-old",
                "description": "Existing archive",
                "evidence_class": "legacy_payload",
                "lifecycle_state": "INVALIDATED",
                "invalidation_reason": "predates cutoff",
                "replacement_basis": "not yet replaced",
                "downstream_reference_basis": "kept for audit",
                "locations": {
                    "local": [
                        {
                            "path": "results/_archive_old",
                            "disposition": "already_archived",
                        }
                    ]
                },
            },
        ],
    }
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_inventory_is_read_only_and_separates_cache_v2(tmp_path):
    repo = _repo(tmp_path)
    plan = load_plan(_plan(tmp_path / "plan.json"))
    before = (repo / "results" / "cache_v2" / "artifact.bin").read_bytes()
    inventory = build_inventory(repo, plan, "local")
    assert inventory["coverage"] == {
        "assigned_file_count": 2,
        "unassigned_file_count": 0,
        "unassigned_paths": [],
    }
    assert inventory["consumer_scan"]["count"] == 1
    assert inventory["actions"] == {
        "moves": [],
        "deletions": [],
        "cache_v2_writes": [],
    }
    assert inventory["protected_paths"][0]["summary"]["file_count"] == 1
    assert (repo / "results" / "cache_v2" / "artifact.bin").read_bytes() == before


def test_plan_rejects_cache_v2_as_retirement_batch(tmp_path):
    plan_path = _plan(tmp_path / "plan.json")
    value = json.loads(plan_path.read_text(encoding="utf-8"))
    value["batches"][0]["locations"]["local"][0]["path"] = "results/cache_v2"
    plan_path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ContractValidationError, match="Cache V2"):
        load_plan(plan_path)


def test_compare_proves_zero_change_and_detects_mutation(tmp_path):
    repo = _repo(tmp_path)
    plan = load_plan(_plan(tmp_path / "plan.json"))
    before = build_inventory(repo, plan, "local")
    unchanged = build_inventory(repo, plan, "local")
    assert compare_inventories(before, unchanged)["pass"] is True

    (repo / "results" / "cache" / "legacy.json").write_text('{"changed":true}', encoding="utf-8")
    changed = build_inventory(repo, plan, "local")
    comparison = compare_inventories(before, changed)
    assert comparison["pass"] is False
    assert comparison["batch_changes"][0]["batch_id"] == "legacy-result-cache"
    assert comparison["cache_v2_unchanged"] is True


def test_ledger_keeps_unreachable_ssh_explicit(tmp_path):
    repo = _repo(tmp_path)
    plan = load_plan(_plan(tmp_path / "plan.json"))
    local = build_inventory(repo, plan, "local")
    ledger = build_ledger(
        plan,
        [local],
        {"ssh": "SSH banner exchange refused on all configured OpenGU aliases"},
    )
    assert ledger["device_observation"]["parity_confirmed"] is False
    assert ledger["verdict"]["device_parity_confirmed"] is False
    assert ledger["verdict"]["deletion_count"] == 0
    assert ledger["entries"][0]["devices"]["ssh"]["status"] == "NOT_OBSERVED"
    assert ledger["entries"][1]["devices"]["ssh"]["status"] == "NOT_APPLICABLE"


def test_outputs_are_write_once(tmp_path):
    output = tmp_path / "evidence.json"
    write_once(output, {"ok": True})
    with pytest.raises(ContractValidationError, match="write-once"):
        write_once(output, {"ok": True})


def test_aagu023_plan_keeps_archive_and_delete_gates_closed():
    plan = load_plan(
        ROOT / ".workblock" / "items" / "AAGU-023" / "evidence" / "batch-plan.json"
    )
    assert len(plan["batches"]) == 20
    assert not [item for item in plan["batches"] if item["lifecycle_state"] == "REPLACED"]
    assert plan["policy"]["archive_requires_state"] == "REPLACED"
    assert plan["policy"]["delete_authorized"] is False
    assert plan["protected_paths"] == ["results/cache_v2"]
