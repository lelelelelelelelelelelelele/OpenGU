from __future__ import annotations

import importlib.util
import sys
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = PROJECT_ROOT / "scripts" / "syncmate" / "verify_core_dependency.py"
EXPECTED_VERSION = "0.2.0"
EXPECTED_SOURCE_COMMIT = "4f0242306ba2707cbaadb9abce3c45d9ea4d0d51"


def _load_verifier():
    spec = importlib.util.spec_from_file_location("verify_core_dependency_test", VERIFY_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_missing_core_distribution_fails_closed():
    verifier = _load_verifier()

    def missing(_name: str) -> str:
        raise metadata.PackageNotFoundError("syncmate")

    result = verifier.verify_core_dependency(
        version_lookup=missing,
        core_module=None,
    )

    assert result["ready"] is False
    assert result["errors"] == ["SyncMate Core distribution is not installed"]


@pytest.mark.parametrize(
    "version,commit,error",
    [
        ("9.9.9", EXPECTED_SOURCE_COMMIT, "SyncMate Core version mismatch"),
        (EXPECTED_VERSION, "0" * 40, "SyncMate Core source commit mismatch"),
    ],
)
def test_wrong_core_identity_fails_closed(version: str, commit: str, error: str):
    verifier = _load_verifier()
    core = SimpleNamespace(
        __version__=version,
        __source_commit__=commit,
        __file__="C:/disposable/site-packages/syncmate_core/__init__.py",
    )

    result = verifier.verify_core_dependency(
        version_lookup=lambda _name: version,
        core_module=core,
    )

    assert result["ready"] is False
    assert error in result["errors"]


def test_exact_installed_core_identity_passes():
    verifier = _load_verifier()
    core = SimpleNamespace(
        __version__=EXPECTED_VERSION,
        __source_commit__=EXPECTED_SOURCE_COMMIT,
        __file__="C:/disposable/site-packages/syncmate_core/__init__.py",
    )

    result = verifier.verify_core_dependency(
        version_lookup=lambda _name: EXPECTED_VERSION,
        core_module=core,
    )

    assert result["ready"] is True
    assert result["errors"] == []
    assert result["observed"]["version"] == EXPECTED_VERSION
    assert result["observed"]["source_commit"] == EXPECTED_SOURCE_COMMIT
