from __future__ import annotations

import argparse
import json
from importlib import metadata
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


EXPECTED_DISTRIBUTION = "syncmate"
EXPECTED_VERSION = "0.2.0"
EXPECTED_SOURCE_COMMIT = "4f0242306ba2707cbaadb9abce3c45d9ea4d0d51"


def verify_core_dependency(
    *,
    version_lookup: Callable[[str], str] = metadata.version,
    core_module: ModuleType | Any | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        distribution_version = version_lookup(EXPECTED_DISTRIBUTION)
    except metadata.PackageNotFoundError:
        return {
            "ready": False,
            "expected": {
                "distribution": EXPECTED_DISTRIBUTION,
                "version": EXPECTED_VERSION,
                "source_commit": EXPECTED_SOURCE_COMMIT,
            },
            "observed": {
                "distribution": None,
                "version": None,
                "source_commit": None,
                "module_file": None,
            },
            "errors": ["SyncMate Core distribution is not installed"],
        }

    if core_module is None:
        try:
            import syncmate_core as core_module
        except ImportError as exc:
            errors.append(f"SyncMate Core module import failed: {exc}")

    module_version = getattr(core_module, "__version__", None)
    source_commit = getattr(core_module, "__source_commit__", None)
    module_file = getattr(core_module, "__file__", None)
    if distribution_version != EXPECTED_VERSION or module_version != EXPECTED_VERSION:
        errors.append("SyncMate Core version mismatch")
    if source_commit != EXPECTED_SOURCE_COMMIT:
        errors.append("SyncMate Core source commit mismatch")
    if not module_file:
        errors.append("SyncMate Core module location is unavailable")
    return {
        "ready": not errors,
        "expected": {
            "distribution": EXPECTED_DISTRIBUTION,
            "version": EXPECTED_VERSION,
            "source_commit": EXPECTED_SOURCE_COMMIT,
        },
        "observed": {
            "distribution": EXPECTED_DISTRIBUTION,
            "distribution_version": distribution_version,
            "version": module_version,
            "source_commit": source_commit,
            "module_file": str(Path(module_file).resolve()) if module_file else None,
        },
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the exact independent SyncMate Core dependency"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = verify_core_dependency()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("SyncMate Core dependency: " + ("ready" if result["ready"] else "blocked"))
        for error in result["errors"]:
            print("  error: " + error)
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
