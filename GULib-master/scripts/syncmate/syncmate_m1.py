from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Optional

import syncmate_core as core
from syncmate_core import cli as core_cli

import opengu_adapter as adapter_module


ADAPTER = adapter_module.ADAPTER
core_module_file = str(Path(core.__file__).resolve())


def contract_payload() -> dict[str, Any]:
    return {
        "adapter": ADAPTER.adapter_id,
        "recipe_ids": sorted(ADAPTER.recipes()),
        "core_module": core_module_file,
        "core_contract": core_cli.contract_payload(),
        "compatibility_candidate": "scripts/syncmate/syncmate_m1.py",
        "physical_replacement_approved": False,
    }


def smoke_payload() -> dict[str, Any]:
    payload = core_cli.smoke_payload()
    payload.update(
        {
            "adapter": ADAPTER.adapter_id,
            "core_module": core_module_file,
            "formal_evidence": False,
            "project_acceptance": "not_evaluated",
        }
    )
    return payload


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "git {0} failed: {1}".format(" ".join(args), completed.stderr.strip())
        )
    return completed.stdout.strip()


def runner_smoke_payload() -> dict[str, Any]:
    temp = tempfile.TemporaryDirectory(prefix="opengu-syncmate-m1-runner-")
    root = Path(temp.name)
    payload: dict[str, Any] = {
        "mode": "opengu-m1-runner-smoke",
        "passed": False,
        "temporary": True,
        "cleaned": False,
        "workdir": str(root),
        "formal_evidence": False,
        "errors": [],
    }
    try:
        sync_dir = root / "scripts" / "syncmate"
        sync_dir.mkdir(parents=True)
        compatibility_path = sync_dir / "syncmate.py"
        shutil.copy2(Path(__file__).resolve(), compatibility_path)
        shutil.copy2(Path(adapter_module.__file__).resolve(), sync_dir / "opengu_adapter.py")
        shutil.copy2(
            Path(adapter_module.__file__).resolve().with_name("setup.example.yaml"),
            sync_dir / "setup.example.yaml",
        )
        (root / ".gitignore").write_text(".syncmate/\n", encoding="utf-8")

        _git(root, "init")
        _git(root, "config", "user.email", "syncmate-m1@example.invalid")
        _git(root, "config", "user.name", "SyncMate M1 Smoke")
        _git(root, "add", "--", ".")
        _git(root, "commit", "-m", "fixture: reviewed OpenGU SyncMate smoke")
        git_sha = _git(root, "rev-parse", "HEAD")
        tracked_status = _git(root, "status", "--porcelain", "--untracked-files=no")
        tracked_clean = tracked_status == ""

        recipe = ADAPTER.recipes()["smoke"]
        job = core.build_job_envelope(
            recipe,
            root,
            job_id="opengu-m1-smoke",
            git_state={"clean": tracked_clean, "sha": git_sha},
            created_at="2026-08-03T00:00:00Z",
            requested_by="syncmate-m1-local-gate2",
        )
        runtime_root = root / ".syncmate" / "m1"
        receipt = core.run_job(
            job,
            ADAPTER,
            root,
            observed_git_sha=git_sha,
            runtime_root=runtime_root,
        )
        receipt_path = runtime_root / "receipts" / "opengu-m1-smoke.json"
        manifest_path = runtime_root / "manifests" / "opengu-m1-smoke.json"
        execution_output: dict[str, Any] = {}
        try:
            parsed = json.loads(receipt.get("stdout") or "")
            if isinstance(parsed, dict):
                execution_output = parsed
        except json.JSONDecodeError:
            pass
        acceptance = ADAPTER.acceptance(receipt, receipt.get("manifest") or {})
        passed = (
            receipt.get("status") == "done"
            and (receipt.get("manifest") or {}).get("status") == "verified"
            and (receipt.get("project_acceptance") or {}).get("status")
            == "not_evaluated"
            and execution_output.get("passed") is True
            and acceptance.get("accepted") is False
            and receipt_path.is_file()
            and manifest_path.is_file()
        )
        payload.update(
            {
                "passed": passed,
                "fixture": {
                    "compatibility_path": compatibility_path.relative_to(root).as_posix(),
                    "tracked_tree_clean_at_dispatch": tracked_clean,
                    "git_sha": git_sha,
                },
                "job": dict(job),
                "receipt": receipt,
                "execution_output": execution_output,
                "adapter_acceptance": dict(acceptance),
                "runtime_evidence": {
                    "receipt": receipt_path.relative_to(root).as_posix(),
                    "receipt_sha256": core.sha256_file(receipt_path),
                    "manifest": manifest_path.relative_to(root).as_posix(),
                    "manifest_sha256": core.sha256_file(manifest_path),
                },
            }
        )
    except Exception as exc:
        payload["errors"].append(f"{type(exc).__name__}: {exc}")
    finally:
        temp.cleanup()
        payload["cleaned"] = not root.exists()
    payload["passed"] = bool(payload["passed"] and payload["cleaned"])
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OpenGU-owned adapter over the independent SyncMate Core M1 slice"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("contract", "smoke", "runner-smoke"):
        command = commands.add_parser(name)
        command.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "contract":
        payload = contract_payload()
    elif args.command == "smoke":
        payload = smoke_payload()
    else:
        payload = runner_smoke_payload()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            "{0}: {1}".format(
                args.command,
                "passed" if payload.get("passed", True) else "failed",
            )
        )
    return 0 if payload.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
