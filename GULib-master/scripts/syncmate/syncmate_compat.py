#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Optional


COMPATIBILITY_ENTRY = Path(__file__).resolve()
PROJECT_ROOT = COMPATIBILITY_ENTRY.parents[2]
REPO_ROOT = PROJECT_ROOT
if str(COMPATIBILITY_ENTRY.parent) not in sys.path:
    sys.path.insert(0, str(COMPATIBILITY_ENTRY.parent))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from syncmate_core import legacy as _core
from syncmate_core.project import install_project_extension

import opengu_acceptance as _acceptance
import opengu_recipes as _recipes
from opengu_adapter import OpenGUProjectExtension


PROJECT_EXTENSION = OpenGUProjectExtension()
install_project_extension(PROJECT_EXTENSION)
_core.set_runtime_repo_root(PROJECT_ROOT)


def _acceptance_context(
    node_id: str,
    expected_git_sha: Optional[str],
) -> dict[str, Any]:
    return {
        "artifact_index": _core.load_artifact_index(),
        "node_id": node_id,
        "expected_git_sha": expected_git_sha,
        "project_root": _core.REPO_ROOT,
    }


def target_direct_selection_acceptance_payload(
    definition: Mapping[str, Any],
    *,
    node_id: str,
    expected_git_sha: Optional[str],
) -> dict[str, Any]:
    return _acceptance.acceptance_payload(
        "target-direct-selection-v2",
        definition,
        _acceptance_context(node_id, expected_git_sha),
    )


def target_direct_gu_acceptance_payload(
    definition: Mapping[str, Any],
    *,
    node_id: str,
    expected_git_sha: Optional[str],
) -> dict[str, Any]:
    return _acceptance.acceptance_payload(
        "target-direct-gu-v2",
        definition,
        _acceptance_context(node_id, expected_git_sha),
    )


def target_direct_gu_stage_acceptance_payload(
    definition: Mapping[str, Any],
    *,
    node_id: str,
    expected_git_sha: Optional[str],
) -> dict[str, Any]:
    return _acceptance.acceptance_payload(
        "target-direct-gu-stage-v2",
        definition,
        _acceptance_context(node_id, expected_git_sha),
    )


def _install_project_compatibility_surface() -> None:
    definitions = _recipes.recipe_definitions()
    _core.RUNNER_RECIPE_DEFINITIONS = definitions
    _core.QUEUE_ALLOWED_RECIPES = tuple(definitions)
    _core.ARTIFACT_NAMES = ("attack.json", "collateral.json", "_meta.json")
    _core.target_direct_selection_acceptance_payload = target_direct_selection_acceptance_payload
    _core.target_direct_gu_acceptance_payload = target_direct_gu_acceptance_payload
    _core.target_direct_gu_stage_acceptance_payload = target_direct_gu_stage_acceptance_payload
    generic_contract_payload = _core.runner_queue_contract_payload

    def project_contract_payload() -> dict[str, Any]:
        payload = generic_contract_payload()
        integration = payload.setdefault("integration", {})
        integration["opengu"] = integration.get("project", "")
        return payload

    _core.runner_queue_contract_payload = project_contract_payload
    for name in dir(_recipes):
        if name.startswith("__"):
            continue
        if name.isupper() or name.startswith("_target_direct"):
            setattr(_core, name, getattr(_recipes, name))


_install_project_compatibility_surface()
_core.implementation_module = _core
_core.implementation_file = str(Path(_core.__file__).resolve())
_core.compatibility_entry_file = str(COMPATIBILITY_ENTRY)


if __name__ == "__main__":
    raise SystemExit(_core.main())

_core.__file__ = str(COMPATIBILITY_ENTRY)
sys.modules[__name__] = _core
