"""Reviewed project recipes; scientific configuration has one ordinary YAML schema."""
from __future__ import annotations
import copy
from experiments.modular_artifacts import ARTIFACT_NAMES, output_paths
from scripts.syncmate.opengu_layout import modular_output_path

RUNNER_AGENT_MAX_TIMEOUT_SECONDS = 21600
RUNNER_RECIPE_INTRODUCED_SHA = "3331c641ce16d0d7a3def66b0e302dd4a39a919c"
RUNNER_RECIPE_ALLOWED_TOOL_DELTA = ("GULib-master/scripts/syncmate/", "GULib-master/tests/test_syncmate.py")

# These fingerprints are reviewed constants, not recomputed expected values.
# Changing any referenced table requires a new review and updated registration.
EXPERIMENT_RECIPES = {
    'opengu-aagu007-v1': {
        'config_path': 'experiments/configs/aagu007/experiment.yaml',
        'config_sha256': '7c6778824e8a67d920d7388e31565ce14e94a51422a57b851eadf34c81749b2a',
        'configuration_fingerprint': '91f35a95df6fba1ac825498af997800b20949e58a22fbce53001e7083ff0ed87',
        'run_identity': {'experiment_id': 'aagu007-cora-degree-r001-v1', 'run_id': 'aagu007-v1'},
        'logical_cells': 4,
        'expected_dataset': {'num_nodes': 2708, 'candidate_count': 1895},
    },
}


def recipe_definitions():
    definitions = {
        "smoke": {
            "id": "smoke",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "smoke", "--json"),
            "config_path": "scripts/syncmate/setup.example.yaml",
            "config_sha256": "9d48bbb04532151eec2cd5868a89821500440e288f65a48fbf09b152bd0660fa",
            "recipe_introduced_git_sha": RUNNER_RECIPE_INTRODUCED_SHA,
            "git_binding_policy": "job-exact-main-v1", "timeout_seconds": 180,
            "expected_artifact_paths": (), "success_predicate": "json.passed == true",
            "collector_acceptance": False,
        },
        "opengu-preflight-v1": {
            "id": "opengu-preflight-v1",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "runner-preflight", "--recipe", "opengu-preflight-v1", "--json"),
            "config_path": "scripts/syncmate/setup.example.yaml",
            "config_sha256": "9d48bbb04532151eec2cd5868a89821500440e288f65a48fbf09b152bd0660fa",
            "recipe_introduced_git_sha": RUNNER_RECIPE_INTRODUCED_SHA,
            "git_binding_policy": "job-exact-main-v1", "timeout_seconds": 180,
            "expected_artifact_paths": (
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/attack.json",
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/collateral.json",
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/_meta.json",
            ),
            "success_predicate": "json.passed == true and generated_artifacts == expected_artifact_paths",
            "collector_acceptance": True,
        },
    }
    for recipe_id, plan in EXPERIMENT_RECIPES.items():
        summary = modular_output_path(**plan['run_identity'])
        paths = (summary,) + output_paths(summary, plan['logical_cells'])
        definitions[recipe_id] = {**copy.deepcopy(plan), 'id': recipe_id,
            'argv': ('{python}', 'experiments/run.py', '--recipe', recipe_id),
            'git_binding_policy': 'job-exact-main-v1', 'requires_job_expected_git_sha': True,
            'timeout_seconds': 1800, 'expected_artifact_paths': paths,
            'collector_result_roots': (summary.rsplit('/', 1)[0],),
            'collector_artifact_names': ('summary.json',) + ARTIFACT_NAMES,
            'preflight_profile': 'modular-project-v1', 'collector_profile': 'modular-output-v1',
            'collector_acceptance': True, 'execution_validator': 'exact-artifacts-json-v1',
            'success_predicate': 'json.passed == true and all reviewed artifacts exist'}
    return definitions
