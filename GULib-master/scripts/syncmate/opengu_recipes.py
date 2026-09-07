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
    'opengu-aagu007-v2': {
        'config_path': 'experiments/configs/aagu007/experiment.yaml',
        'config_sha256': '1394ecdf82e64a79344a15f8191d1c7514034d9862bcff6a2d829ff6c02ca717',
        'configuration_fingerprint': '9f2913185bc357de0ce8a70e7adb6b70e498bc0552217fcc2e2ef9fd6e775eaf',
        'run_identity': {'experiment_id': 'aagu007-cora-degree-r001-v1', 'run_id': 'aagu007-v2'},
        'timeout_seconds': 1800,
        'logical_cells': 4,
        'stage': 'unlearning',
        'expected_dataset': {'num_nodes': 2708, 'candidate_count': 1895},
    },
    'opengu-aagu032-v1': {
        'config_path': 'experiments/configs/aagu032/experiment.yaml',
        'config_sha256': '35c24fe080ab546f4a8fea7bad5ee573eed6f04e8c4488cca2054d2956c730ca',
        'configuration_fingerprint': '3d80fc0e3d5447677565871c5dc06863f944ec4aeb80ae31e2533c72bdba42d9',
        'run_identity': {'experiment_id': 'aagu032-cora-gcn-retrain', 'run_id': 'aagu032-v1'},
        'timeout_seconds': 21600,
        'logical_cells': 42,
        'stage': 'unlearning',
        'expected_dataset': {'num_nodes': 2708, 'candidate_count': 1895},
    },
    'opengu-aagu032-extend-cora-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.yaml',
     'config_sha256': '77e7247283ec56b043523f0cf241e1fe3cbe83efc44210a12745e917c65bdb59',
     'configuration_fingerprint': 'fd6f561f5b798e2d412ffc43756427797edbdf4d61653a76aecb9f6aafc55766',
     'run_identity': {'experiment_id': 'aagu032-extended-cora-gcn-retrain', 'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_dataset': {'num_nodes': 2708, 'candidate_count': 1895}},
    'opengu-aagu032-extend-citeseer-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.citeseer.yaml',
     'config_sha256': 'bd0771203938d812851e29f6e34e049a6a9ce1a0139163dd50650bb49c2dd690',
     'configuration_fingerprint': '4fe267448d70ec9d2964f740489a3770e5bfadec7fc309a93f1c055c330c8cca',
     'run_identity': {'experiment_id': 'aagu032-extended-citeseer-gcn-retrain',
                      'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_dataset': {'num_nodes': 3327, 'candidate_count': 2328}},
    'opengu-aagu032-extend-pubmed-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.pubmed.yaml',
     'config_sha256': 'f4c2b91190310d226f41ed67032f3d594305644d854b090718027d051168fbc3',
     'configuration_fingerprint': '5c6344f295429cecab02bdcea91919aa3e1e875afbb116bf0c4fda3d5efb1d96',
     'run_identity': {'experiment_id': 'aagu032-extended-pubmed-gcn-retrain', 'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_dataset': {'num_nodes': 19717, 'candidate_count': 13801}},
}


def recipe_definitions():
    definitions = {
        "smoke": {
            "id": "smoke",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "smoke", "--json"),
            "config_path": "scripts/syncmate/setup.example.yaml",
            "config_sha256": "a04773028a9045c929f6ac3635dd3cea5b17de89184095d3e396aeb19baf77c5",
            "recipe_introduced_git_sha": RUNNER_RECIPE_INTRODUCED_SHA,
            "git_binding_policy": "job-exact-main-v1", "timeout_seconds": 180,
            "expected_artifact_paths": (), "success_predicate": "json.passed == true",
            "collector_acceptance": False,
        },
        "opengu-preflight-v1": {
            "id": "opengu-preflight-v1",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "runner-preflight", "--recipe", "opengu-preflight-v1", "--json"),
            "config_path": "scripts/syncmate/setup.example.yaml",
            "config_sha256": "a04773028a9045c929f6ac3635dd3cea5b17de89184095d3e396aeb19baf77c5",
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
        paths = (summary,) + (output_paths(summary, plan['logical_cells'])
                             if plan['stage'] == 'unlearning' else ())
        definitions[recipe_id] = {**copy.deepcopy(plan), 'id': recipe_id,
            'argv': ('{python}', 'experiments/run.py', plan['config_path'],
                     '--run-id', plan['run_identity']['run_id']),
            'git_binding_policy': 'job-exact-main-v1', 'requires_job_expected_git_sha': True,
            'timeout_seconds': plan['timeout_seconds'], 'expected_artifact_paths': paths,
            'collector_result_roots': (summary.rsplit('/', 1)[0],),
            'collector_artifact_names': ('summary.json',) + ARTIFACT_NAMES,
            'preflight_profile': 'modular-project-v1', 'collector_profile': 'modular-output-v1',
            'collector_acceptance': True, 'execution_validator': 'exact-artifacts-json-v1',
            'success_predicate': 'json.passed == true and all reviewed artifacts exist'}
    return definitions
