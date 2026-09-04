"""Batch-level inventory and retirement ledger for Legacy experiment evidence.

The tool is deliberately read-only with respect to ``results/``.  It hashes
declared batches, records live Legacy-cache consumers, and writes evidence only
to caller-selected, write-once output files.  Physical archive and deletion are
not commands in this tool: a batch must first reach the separately reviewed
``REPLACED`` state before another Block may authorize a move or deletion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cache_v2.archive_readiness import build_archive_readiness_manifest
from cache_v2.errors import ContractValidationError


PLAN_SCHEMA = "opengu.legacy_evidence_batch_plan"
PLAN_VERSION = 1
INVENTORY_SCHEMA = "opengu.legacy_evidence_inventory"
INVENTORY_VERSION = 1
LEDGER_SCHEMA = "opengu.legacy_evidence_retirement_ledger"
LEDGER_VERSION = 1
COMPARISON_SCHEMA = "opengu.legacy_evidence_inventory_comparison"
COMPARISON_VERSION = 1

LIFECYCLE_STATES = frozenset(
    {
        "INVALIDATED",
        "REGISTERED",
        "GATED",
        "RUNNING",
        "COLLECTED",
        "ACCEPTED",
        "PROJECTED",
        "REPLACED",
        "RETIRED",
    }
)
DISPOSITIONS = frozenset(
    {
        "active_rollback_source",
        "already_archived",
        "historical_engineering_evidence",
        "historical_projection",
        "transport_bundle",
    }
)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError("{0} must be non-empty text".format(label))
    return value.strip()


def _required_keys(value: Mapping[str, Any], keys: Iterable[str], label: str) -> None:
    expected = set(keys)
    actual = set(value)
    if actual != expected:
        raise ContractValidationError(
            "{0} keys mismatch: expected {1}, got {2}".format(
                label, sorted(expected), sorted(actual)
            )
        )


def _safe_relative_path(value: Any, label: str) -> str:
    text = _required_text(value, label).replace("\\", "/")
    path = Path(text)
    if path.is_absolute() or text.startswith("/") or ".." in path.parts:
        raise ContractValidationError("{0} must be a safe relative path".format(label))
    normalized = path.as_posix()
    if normalized == "." or not normalized.startswith("results/"):
        raise ContractValidationError("{0} must be below results/".format(label))
    if normalized == "results/cache_v2" or normalized.startswith("results/cache_v2/"):
        raise ContractValidationError(
            "{0} must not place Cache V2 in a retirement batch".format(label)
        )
    return normalized


def load_plan(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ContractValidationError("batch plan is not readable JSON") from exc
    if not isinstance(value, Mapping):
        raise ContractValidationError("batch plan root must be an object")
    _required_keys(
        value,
        {"schema", "version", "policy", "devices", "protected_paths", "batches"},
        "batch plan",
    )
    if value.get("schema") != PLAN_SCHEMA or value.get("version") != PLAN_VERSION:
        raise ContractValidationError("batch plan schema/version mismatch")

    policy = value.get("policy")
    if not isinstance(policy, Mapping):
        raise ContractValidationError("policy must be an object")
    _required_keys(
        policy,
        {
            "cutoff",
            "archive_requires_state",
            "delete_authorized",
            "legacy_cache_reuse",
        },
        "policy",
    )
    if policy.get("archive_requires_state") != "REPLACED":
        raise ContractValidationError("archive_requires_state must be REPLACED")
    if policy.get("delete_authorized") is not False:
        raise ContractValidationError("delete_authorized must be false")
    if policy.get("legacy_cache_reuse") != "forbidden_for_new_batches":
        raise ContractValidationError("legacy_cache_reuse policy mismatch")
    _required_text(policy.get("cutoff"), "policy.cutoff")

    devices = value.get("devices")
    if not isinstance(devices, list) or not devices:
        raise ContractValidationError("devices must be a non-empty list")
    normalized_devices: List[Dict[str, Any]] = []
    device_ids = set()
    for index, item in enumerate(devices):
        if not isinstance(item, Mapping):
            raise ContractValidationError("devices[{0}] must be an object".format(index))
        _required_keys(item, {"id", "role"}, "devices[{0}]".format(index))
        device_id = _required_text(item.get("id"), "devices[{0}].id".format(index))
        if device_id in device_ids:
            raise ContractValidationError("duplicate device id: {0}".format(device_id))
        device_ids.add(device_id)
        normalized_devices.append(
            {"id": device_id, "role": _required_text(item.get("role"), "device role")}
        )

    protected_paths = value.get("protected_paths")
    if protected_paths != ["results/cache_v2"]:
        raise ContractValidationError(
            "protected_paths must contain exactly results/cache_v2"
        )

    batches = value.get("batches")
    if not isinstance(batches, list) or not batches:
        raise ContractValidationError("batches must be a non-empty list")
    normalized_batches: List[Dict[str, Any]] = []
    batch_ids = set()
    for index, item in enumerate(batches):
        label = "batches[{0}]".format(index)
        if not isinstance(item, Mapping):
            raise ContractValidationError("{0} must be an object".format(label))
        _required_keys(
            item,
            {
                "id",
                "description",
                "evidence_class",
                "lifecycle_state",
                "invalidation_reason",
                "replacement_basis",
                "downstream_reference_basis",
                "locations",
            },
            label,
        )
        batch_id = _required_text(item.get("id"), label + ".id")
        if batch_id in batch_ids:
            raise ContractValidationError("duplicate batch id: {0}".format(batch_id))
        batch_ids.add(batch_id)
        state = _required_text(item.get("lifecycle_state"), label + ".lifecycle_state")
        if state not in LIFECYCLE_STATES:
            raise ContractValidationError("unsupported lifecycle state: {0}".format(state))
        locations = item.get("locations")
        if not isinstance(locations, Mapping) or not locations:
            raise ContractValidationError("{0}.locations must be an object".format(label))
        normalized_locations: Dict[str, List[Dict[str, str]]] = {}
        for device_id, records in locations.items():
            if device_id not in device_ids:
                raise ContractValidationError(
                    "{0} references unknown device {1}".format(label, device_id)
                )
            if not isinstance(records, list) or not records:
                raise ContractValidationError(
                    "{0}.locations.{1} must be non-empty".format(label, device_id)
                )
            normalized_records = []
            for record_index, record in enumerate(records):
                record_label = "{0}.locations.{1}[{2}]".format(
                    label, device_id, record_index
                )
                if not isinstance(record, Mapping):
                    raise ContractValidationError(record_label + " must be an object")
                _required_keys(record, {"path", "disposition"}, record_label)
                disposition = _required_text(
                    record.get("disposition"), record_label + ".disposition"
                )
                if disposition not in DISPOSITIONS:
                    raise ContractValidationError(
                        "unsupported disposition: {0}".format(disposition)
                    )
                normalized_records.append(
                    {
                        "path": _safe_relative_path(
                            record.get("path"), record_label + ".path"
                        ),
                        "disposition": disposition,
                    }
                )
            normalized_locations[device_id] = normalized_records
        normalized_batches.append(
            {
                "id": batch_id,
                "description": _required_text(item.get("description"), label + ".description"),
                "evidence_class": _required_text(
                    item.get("evidence_class"), label + ".evidence_class"
                ),
                "lifecycle_state": state,
                "invalidation_reason": _required_text(
                    item.get("invalidation_reason"), label + ".invalidation_reason"
                ),
                "replacement_basis": _required_text(
                    item.get("replacement_basis"), label + ".replacement_basis"
                ),
                "downstream_reference_basis": _required_text(
                    item.get("downstream_reference_basis"),
                    label + ".downstream_reference_basis",
                ),
                "locations": normalized_locations,
            }
        )
    return {
        "schema": PLAN_SCHEMA,
        "version": PLAN_VERSION,
        "policy": dict(policy),
        "devices": normalized_devices,
        "protected_paths": list(protected_paths),
        "batches": normalized_batches,
    }


def _git_file_states(repo: Path) -> Tuple[set[str], set[str], set[str]]:
    def paths(arguments: Sequence[str]) -> set[str]:
        process = subprocess.run(
            ["git", *arguments],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode:
            raise ContractValidationError(
                "git file-state query failed: {0}".format(
                    process.stderr.decode("utf-8", "replace").strip()
                )
            )
        return {
            item.decode("utf-8", "surrogateescape").replace("\\", "/")
            for item in process.stdout.split(b"\0")
            if item
        }

    tracked = paths(["ls-files", "-z", "--", "results"])
    ignored = paths(
        ["ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--", "results"]
    )
    untracked = paths(
        ["ls-files", "-z", "--others", "--exclude-standard", "--", "results"]
    )
    return tracked, ignored, untracked


def _file_record(
    path: Path,
    repo: Path,
    tracked: set[str],
    ignored: set[str],
    untracked: set[str],
) -> Dict[str, Any]:
    relative = path.relative_to(repo).as_posix()
    if relative in tracked:
        git_state = "tracked"
    elif relative in ignored:
        git_state = "ignored"
    elif relative in untracked:
        git_state = "untracked"
    else:
        git_state = "outside_observed_git_sets"
    stat = path.stat()
    return {
        "path": relative,
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": _sha256_file(path),
        "git_state": git_state,
    }


def _inventory_paths(
    repo: Path,
    path_records: Sequence[Mapping[str, str]],
    tracked: set[str],
    ignored: set[str],
    untracked: set[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    files: List[Dict[str, Any]] = []
    observed_locations: List[Dict[str, str]] = []
    seen = set()
    for record in path_records:
        relative = record["path"]
        root = (repo / relative).resolve(strict=False)
        try:
            root.relative_to(repo)
        except ValueError as exc:
            raise ContractValidationError("batch path escapes repository") from exc
        if not root.exists():
            observed_locations.append(
                {
                    "path": relative,
                    "disposition": record["disposition"],
                    "status": "absent",
                }
            )
            continue
        if root.is_file():
            candidates = [root]
        elif root.is_dir():
            candidates = sorted(item for item in root.rglob("*") if item.is_file())
        else:
            raise ContractValidationError("batch path is not a regular file or directory")
        observed_locations.append(
            {
                "path": relative,
                "disposition": record["disposition"],
                "status": "present",
            }
        )
        for candidate in candidates:
            resolved = candidate.resolve(strict=True)
            if resolved in seen:
                raise ContractValidationError(
                    "batch locations overlap at {0}".format(candidate)
                )
            seen.add(resolved)
            files.append(_file_record(candidate, repo, tracked, ignored, untracked))
    files.sort(key=lambda item: item["path"])
    return files, observed_locations


def _summary(files: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    states: MutableMapping[str, int] = {}
    for item in files:
        state = str(item["git_state"])
        states[state] = states.get(state, 0) + 1
    return {
        "file_count": len(files),
        "size_bytes": sum(int(item["size_bytes"]) for item in files),
        "aggregate_sha256": hashlib.sha256(_canonical_json(list(files))).hexdigest(),
        "git_states": dict(sorted(states.items())),
    }


def build_inventory(repo_root: Path, plan: Mapping[str, Any], device_id: str) -> Dict[str, Any]:
    repo = repo_root.expanduser().resolve(strict=True)
    if not (repo / ".git").exists():
        process = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if process.returncode:
            raise ContractValidationError("repo_root is not the Git worktree root")
        git_root = Path(process.stdout.strip()).resolve(strict=True)
        try:
            repo.relative_to(git_root)
        except ValueError as exc:
            raise ContractValidationError("repo_root is outside the Git worktree") from exc
    device_ids = {item["id"] for item in plan["devices"]}
    if device_id not in device_ids:
        raise ContractValidationError("unknown device id: {0}".format(device_id))

    tracked, ignored, untracked = _git_file_states(repo)
    batches = []
    assigned_files: Dict[str, str] = {}
    for batch in plan["batches"]:
        locations = batch["locations"].get(device_id)
        if not locations:
            continue
        files, observed_locations = _inventory_paths(
            repo, locations, tracked, ignored, untracked
        )
        for item in files:
            previous = assigned_files.get(item["path"])
            if previous is not None:
                raise ContractValidationError(
                    "file assigned to multiple batches: {0} ({1}, {2})".format(
                        item["path"], previous, batch["id"]
                    )
                )
            assigned_files[item["path"]] = batch["id"]
        batches.append(
            {
                "id": batch["id"],
                "description": batch["description"],
                "evidence_class": batch["evidence_class"],
                "lifecycle_state": batch["lifecycle_state"],
                "invalidation_reason": batch["invalidation_reason"],
                "replacement_basis": batch["replacement_basis"],
                "downstream_reference_basis": batch["downstream_reference_basis"],
                "locations": observed_locations,
                "summary": _summary(files),
                "files": files,
            }
        )

    protected = []
    for relative in plan["protected_paths"]:
        root = repo / relative
        files, locations = _inventory_paths(
            repo,
            [{"path": relative, "disposition": "active_rollback_source"}],
            tracked,
            ignored,
            untracked,
        )
        protected.append(
            {
                "path": relative,
                "status": locations[0]["status"],
                "summary": _summary(files),
                "files": files,
            }
        )

    readiness = build_archive_readiness_manifest(repo / "results", repo)
    consumer_items = readiness["consumer_refs"]["items"]
    result_files = sorted(
        item.relative_to(repo).as_posix()
        for item in (repo / "results").rglob("*")
        if item.is_file()
    )
    unassigned = [item for item in result_files if item not in assigned_files and not item.startswith("results/cache_v2/")]
    return {
        "schema": INVENTORY_SCHEMA,
        "version": INVENTORY_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "device_id": device_id,
        "repo_root": str(repo),
        "policy": dict(plan["policy"]),
        "batches": batches,
        "protected_paths": protected,
        "consumer_scan": {
            "count": len(consumer_items),
            "items": consumer_items,
        },
        "coverage": {
            "assigned_file_count": len(assigned_files),
            "unassigned_file_count": len(unassigned),
            "unassigned_paths": unassigned,
        },
        "actions": {
            "moves": [],
            "deletions": [],
            "cache_v2_writes": [],
        },
    }


def _load_inventory(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ContractValidationError("inventory is not readable JSON") from exc
    if not isinstance(value, Mapping):
        raise ContractValidationError("inventory root must be an object")
    if value.get("schema") != INVENTORY_SCHEMA or value.get("version") != INVENTORY_VERSION:
        raise ContractValidationError("inventory schema/version mismatch")
    return dict(value)


def compare_inventories(before: Mapping[str, Any], after: Mapping[str, Any]) -> Dict[str, Any]:
    if before.get("device_id") != after.get("device_id"):
        raise ContractValidationError("inventory device ids differ")
    before_batches = {item["id"]: item for item in before["batches"]}
    after_batches = {item["id"]: item for item in after["batches"]}
    if set(before_batches) != set(after_batches):
        raise ContractValidationError("inventory batch ids differ")
    changes = []
    for batch_id in sorted(before_batches):
        old = before_batches[batch_id]["summary"]
        new = after_batches[batch_id]["summary"]
        if old != new:
            changes.append({"batch_id": batch_id, "before": old, "after": new})
    before_protected = {item["path"]: item["summary"] for item in before["protected_paths"]}
    after_protected = {item["path"]: item["summary"] for item in after["protected_paths"]}
    protected_changes = []
    for path in sorted(set(before_protected) | set(after_protected)):
        if before_protected.get(path) != after_protected.get(path):
            protected_changes.append(
                {"path": path, "before": before_protected.get(path), "after": after_protected.get(path)}
            )
    return {
        "schema": COMPARISON_SCHEMA,
        "version": COMPARISON_VERSION,
        "device_id": before["device_id"],
        "before_generated_at": before["generated_at"],
        "after_generated_at": after["generated_at"],
        "batch_changes": changes,
        "protected_path_changes": protected_changes,
        "consumer_count_before": before["consumer_scan"]["count"],
        "consumer_count_after": after["consumer_scan"]["count"],
        "moves_observed": len(changes),
        "deletions_observed": 0 if not changes else None,
        "cache_v2_unchanged": not protected_changes,
        "pass": not changes and not protected_changes,
    }


def build_ledger(
    plan: Mapping[str, Any],
    inventories: Sequence[Mapping[str, Any]],
    unavailable: Mapping[str, str],
) -> Dict[str, Any]:
    inventory_by_device = {}
    for inventory in inventories:
        device_id = _required_text(inventory.get("device_id"), "inventory.device_id")
        if device_id in inventory_by_device:
            raise ContractValidationError("duplicate inventory for device: {0}".format(device_id))
        inventory_by_device[device_id] = inventory
    known_devices = {item["id"] for item in plan["devices"]}
    if set(inventory_by_device) | set(unavailable) != known_devices:
        raise ContractValidationError(
            "every plan device must have exactly one inventory or unavailable observation"
        )
    if set(inventory_by_device) & set(unavailable):
        raise ContractValidationError("a device cannot be observed and unavailable")

    entries = []
    for batch in plan["batches"]:
        devices: Dict[str, Any] = {}
        for device in plan["devices"]:
            device_id = device["id"]
            planned_locations = batch["locations"].get(device_id, [])
            if not planned_locations:
                devices[device_id] = {"status": "NOT_APPLICABLE", "locations": []}
                continue
            if device_id in unavailable:
                devices[device_id] = {
                    "status": "NOT_OBSERVED",
                    "reason": _required_text(
                        unavailable[device_id], "unavailable.{0}".format(device_id)
                    ),
                    "locations": planned_locations,
                }
                continue
            inventory_batches = {
                item["id"]: item for item in inventory_by_device[device_id]["batches"]
            }
            observed = inventory_batches.get(batch["id"])
            if observed is None:
                raise ContractValidationError(
                    "inventory missing planned batch {0} on {1}".format(batch["id"], device_id)
                )
            devices[device_id] = {
                "status": "OBSERVED",
                "locations": observed["locations"],
                "summary": observed["summary"],
            }
        entries.append(
            {
                "id": batch["id"],
                "description": batch["description"],
                "evidence_class": batch["evidence_class"],
                "lifecycle_state": batch["lifecycle_state"],
                "invalidation_reason": batch["invalidation_reason"],
                "replacement_basis": batch["replacement_basis"],
                "downstream_reference_basis": batch["downstream_reference_basis"],
                "devices": devices,
                "archive_eligible": batch["lifecycle_state"] == "REPLACED",
                "delete_authorized": False,
            }
        )

    parity_confirmed = not unavailable and len(inventory_by_device) == len(known_devices)
    protected = {
        device_id: inventory["protected_paths"]
        for device_id, inventory in sorted(inventory_by_device.items())
    }
    consumer_counts = {
        device_id: inventory["consumer_scan"]["count"]
        for device_id, inventory in sorted(inventory_by_device.items())
    }
    return {
        "schema": LEDGER_SCHEMA,
        "version": LEDGER_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "policy": dict(plan["policy"]),
        "entries": entries,
        "device_observation": {
            "observed": sorted(inventory_by_device),
            "unavailable": dict(sorted(unavailable.items())),
            "parity_confirmed": parity_confirmed,
        },
        "consumer_counts": consumer_counts,
        "protected_paths": protected,
        "actions": {
            "moves": [],
            "deletions": [],
            "cache_v2_writes": [],
        },
        "verdict": {
            "all_batches_registered": True,
            "device_parity_confirmed": parity_confirmed,
            "physical_archive_performed": False,
            "deletion_count": 0,
            "cache_v2_modified": False,
            "reason": (
                "all declared devices observed"
                if parity_confirmed
                else "one or more declared devices were not observed"
            ),
        },
    }


def write_once(path: Path, value: Mapping[str, Any]) -> Dict[str, Any]:
    output = path.expanduser().resolve(strict=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_json(value)
    descriptor = None
    try:
        descriptor = os.open(str(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    except FileExistsError as exc:
        raise ContractValidationError("output is write-once; choose a new path") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return {"path": str(output), "sha256": _sha256_file(output), "size_bytes": len(payload)}


def _parse_assignment(values: Sequence[str], label: str) -> Dict[str, str]:
    result = {}
    for value in values:
        if "=" not in value:
            raise ContractValidationError("{0} requires DEVICE=VALUE".format(label))
        device, item = value.split("=", 1)
        device = _required_text(device, label + " device")
        item = _required_text(item, label + " value")
        if device in result:
            raise ContractValidationError("duplicate {0} device: {1}".format(label, device))
        result[device] = item
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--repo", required=True)
    inventory.add_argument("--plan", required=True)
    inventory.add_argument("--device", required=True)
    inventory.add_argument("--output", required=True)

    compare = subparsers.add_parser("compare")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
    compare.add_argument("--output", required=True)

    ledger = subparsers.add_parser("ledger")
    ledger.add_argument("--plan", required=True)
    ledger.add_argument("--inventory", action="append", default=[])
    ledger.add_argument("--unavailable", action="append", default=[])
    ledger.add_argument("--output", required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "inventory":
        plan = load_plan(Path(args.plan))
        result = build_inventory(Path(args.repo), plan, args.device)
    elif args.command == "compare":
        result = compare_inventories(
            _load_inventory(Path(args.before)), _load_inventory(Path(args.after))
        )
    elif args.command == "ledger":
        plan = load_plan(Path(args.plan))
        inventory_paths = _parse_assignment(args.inventory, "--inventory")
        unavailable = _parse_assignment(args.unavailable, "--unavailable")
        inventories = [_load_inventory(Path(path)) for path in inventory_paths.values()]
        for expected_device, inventory in zip(inventory_paths, inventories):
            if inventory["device_id"] != expected_device:
                raise ContractValidationError(
                    "inventory assignment device does not match inventory content"
                )
        result = build_ledger(plan, inventories, unavailable)
    else:  # pragma: no cover
        raise AssertionError(args.command)
    write_result = write_once(Path(args.output), result)
    print(json.dumps({"ok": True, "output": write_result}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
