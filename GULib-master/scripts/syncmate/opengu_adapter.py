from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import syncmate_core as core


OPENGU_SETUP_CONFIG_SHA256 = (
    "03fb31feae5edb3fde21b9eab2fcc892fecb764e05fafe44b38c753fdde9f8a1"
)


class OpenGUAdapter:
    adapter_id = "opengu"

    def __init__(self) -> None:
        smoke = core.Recipe(
            id="smoke",
            argv=(
                "{python}",
                "scripts/syncmate/syncmate.py",
                "smoke",
                "--json",
            ),
            config_path="scripts/syncmate/setup.example.yaml",
            config_sha256=OPENGU_SETUP_CONFIG_SHA256,
            timeout_seconds=180,
            expected_artifact_paths=(),
            requires_job_expected_git_sha=True,
            execution_validator="json-passed-v1",
        )
        self._recipes = MappingProxyType({smoke.id: smoke})

    def recipes(self) -> Mapping[str, core.Recipe]:
        return self._recipes

    def preflight(
        self,
        recipe: core.Recipe,
        project_root: Path,
    ) -> Mapping[str, Any]:
        config_path = core.resolve_repo_path(project_root, recipe.config_path)
        observed_sha = None
        if config_path.is_file():
            observed_sha = core.sha256_text(config_path.read_text(encoding="utf-8"))
        ready = observed_sha == recipe.config_sha256
        return {
            "ready": ready,
            "profile": "opengu-m1-local-smoke-v1",
            "expected": {
                "recipe": recipe.id,
                "config_path": recipe.config_path,
                "config_sha256": recipe.config_sha256,
            },
            "observed": {
                "config_exists": config_path.is_file(),
                "config_sha256": observed_sha,
            },
            "action": "continue" if ready else "restore the reviewed OpenGU setup example",
            "errors": [] if ready else ["OpenGU smoke config SHA-256 mismatch"],
        }

    def acceptance(
        self,
        receipt: Mapping[str, Any],
        manifest: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        del receipt, manifest
        return {
            "accepted": False,
            "status": "not_evaluated",
            "formal_evidence": False,
            "reason": "execution done is not OpenGU project acceptance",
        }


ADAPTER = OpenGUAdapter()
