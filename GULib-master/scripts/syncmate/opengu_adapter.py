from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

def _modular_preflight(definition, config_path):
    from experiments.syncmate_stage import preflight
    root = Path(config_path).resolve()
    for _ in Path(definition['config_path']).parts:
        root = root.parent
    return preflight(definition['id'], root=root)


_PREFLIGHT_HANDLERS = {'modular-project-v1': _modular_preflight}


class OpenGUProjectExtension:
    """OpenGU-owned policy surface consumed by the independent SyncMate Core."""

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
