from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import syncmate_core as core

OPENGU_SETUP_CONFIG_SHA256 = (
    "9d48bbb04532151eec2cd5868a89821500440e288f65a48fbf09b152bd0660fa"
)


def _target_selection_preflight(definition: Mapping[str, Any], config_path: Path) -> Mapping[str, Any]:
    from experiments.target_direct_v1.syncmate_stage import preflight_selection

    stage = str((definition.get("selection_matrix") or {}).get("stage") or "")
    return preflight_selection(stage, config_path)


def _target_gu_preflight(definition: Mapping[str, Any], config_path: Path) -> Mapping[str, Any]:
    from experiments.target_direct_v1.syncmate_stage import preflight_gu

    contract = definition.get("gu_gate") or definition.get("gu_stage") or {}
    return preflight_gu(
        str(contract.get("stage") or ""), ratio=contract["ratio"],
        config_path=config_path, gate_only="gu_gate" in definition,
    )


def _atomic_preflight(definition, config_path):
    from experiments.syncmate_atomic_stage import preflight
    return preflight(definition['id'])


_PREFLIGHT_HANDLERS = {
    "sm005-atomic-gpu-v1": _atomic_preflight,
    "target-direct-selection-4090-v1": _target_selection_preflight,
    "target-direct-gu-4090-v1": _target_gu_preflight,
}


class OpenGUProjectExtension:
    """OpenGU-owned policy surface consumed by the generic compatibility Core."""

    extension_id = "opengu"

    def result_roots(self) -> tuple[str, ...]:
        return ("results/runs",)

    def recipes(self, project_root: Path) -> Mapping[str, Mapping[str, Any]]:
        import opengu_recipes as recipes_module
        del project_root
        return recipes_module.recipe_definitions()

    def artifact_names(
        self,
        device: Mapping[str, Any] | None,
        peer: Mapping[str, Any] | None,
    ) -> tuple[str, ...]:
        policy = (peer or {}).get("artifact_policy") or (device or {}).get("artifact_policy") or {}
        included = policy.get("include") if isinstance(policy, Mapping) else None
        if included:
            return tuple(str(name) for name in included)
        return ("attack.json", "collateral.json", "_meta.json")

    def preflight(
        self,
        profile: str,
        definition: Mapping[str, Any],
        config_path: Path,
    ) -> Mapping[str, Any]:
        handler = _PREFLIGHT_HANDLERS.get(profile)
        if handler is None:
            return {
                "ready": False,
                "owner": self.extension_id,
                "profile": profile,
                "expected": {"profile": "reviewed OpenGU preflight profile"},
                "observed": {"profile": profile},
                "action": "select a reviewed OpenGU recipe",
                "errors": ["OpenGU preflight profile is not reviewed"],
            }
        try:
            result = dict(handler(definition, config_path))
        except Exception as exc:
            return {
                "ready": False,
                "owner": self.extension_id,
                "profile": profile,
                "expected": {"handler": "successful Project preflight"},
                "observed": {"error": f"{type(exc).__name__}: {exc}"},
                "action": "repair the OpenGU Project preflight dependency",
                "errors": [f"OpenGU Project preflight failed: {type(exc).__name__}: {exc}"],
            }
        result["owner"] = self.extension_id
        result["profile"] = profile
        return result

    def accept(
        self,
        profile: str,
        definition: Mapping[str, Any],
        context: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        import opengu_acceptance as acceptance_module
        return acceptance_module.acceptance_payload(profile, definition, context)

    def results(
        self,
        index: Mapping[str, Any],
        options: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        import opengu_results as results_module
        return results_module.results_payload(index, options)


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
