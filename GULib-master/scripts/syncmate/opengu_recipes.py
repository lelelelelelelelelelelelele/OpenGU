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
    'opengu-aagu031-stage-s-v2': {
        'config_path': 'experiments/configs/aagu031/stage_s.yaml',
        'config_sha256': 'b996e5f654ce14e3924cf384931336568ccb5957e615be9dcddf68fd2d6767f3',
        'configuration_fingerprint': '5ee2ab0b879f20e6b0eb24b37a6cbe351fee641c4b501fdbff7955fa5498ad44',
        'run_identity': {'experiment_id': 'aagu031-selector-stage-s-v2', 'run_id': 'aagu031-stage-s-v2'},
        'timeout_seconds': 21600, 'logical_cells': 72, 'stage': 'selector',
        'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                              {'num_nodes': 3327, 'candidate_count': 2328},
                              {'num_nodes': 19717, 'candidate_count': 13801}],
    },
    'opengu-aagu007-v2': {
        'config_path': 'experiments/configs/aagu007/experiment.yaml',
        'config_sha256': '19208034fb94760b546f811af73673f97ca0cb9f12619ce41f194f807f5e8848',
        'configuration_fingerprint': '18a5bcc0a8fdfe7e8293d4a32800af3c0c5bf1281025d31ede88980dd274f97a',
        'run_identity': {'experiment_id': 'aagu007-cora-degree-r001-v1', 'run_id': 'aagu007-v2'},
        'timeout_seconds': 1800,
        'logical_cells': 4,
        'stage': 'unlearning',
        'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895}],
    },
    'opengu-aagu032-v1': {
        'config_path': 'experiments/configs/aagu032/experiment.yaml',
        'config_sha256': '772458db81fc6dd64bcbe69d450de0c43228e8943fdf70b108059f6f1e0bec97',
        'configuration_fingerprint': '45d89594f8e4b644714ab8a7ff26da6b99980d6cfa93259d378685f6b6381108',
        'run_identity': {'experiment_id': 'aagu032-cora-gcn-retrain', 'run_id': 'aagu032-v1'},
        'timeout_seconds': 21600,
        'logical_cells': 42,
        'stage': 'unlearning',
        'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895}],
    },
    'opengu-aagu032-extend-cora-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.yaml',
     'config_sha256': '5090c06dccf5f734ba4b6433e86e01bae402cbdd10da8686555af6a9b5fcd6a4',
     'configuration_fingerprint': '7075a0ba26f01fc1fef8ab4d86e28f65f5032203755c0a8c65a2ef6c9c6d2150',
     'run_identity': {'experiment_id': 'aagu032-extended-cora-gcn-retrain', 'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895}]},
    'opengu-aagu032-extend-citeseer-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.citeseer.yaml',
     'config_sha256': '3f329e347363283fd9bb00a695435be8070179ac7d77b71eb8b0251b3404035f',
     'configuration_fingerprint': 'b21fa4aa5e4a8795ad1d0232ca607b0c6cc894a90e3ae8174ddfb702a63ce2d6',
     'run_identity': {'experiment_id': 'aagu032-extended-citeseer-gcn-retrain',
                      'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_datasets': [{'num_nodes': 3327, 'candidate_count': 2328}]},
    'opengu-aagu032-extend-pubmed-v1': {'config_path': 'experiments/configs/aagu032_extend/experiment.pubmed.yaml',
     'config_sha256': '59f323e0c1f07dbfcd43243c6d194094130636b1bc324a5b36394baf99439a76',
     'configuration_fingerprint': '6499d4cba056700c7895db6db3b29a63daf09922d8b0f4e8a6bfd13f65845a28',
     'run_identity': {'experiment_id': 'aagu032-extended-pubmed-gcn-retrain', 'run_id': 'aagu032-extend-v1'},
     'timeout_seconds': 21600,
     'logical_cells': 96,
     'stage': 'unlearning',
     'expected_datasets': [{'num_nodes': 19717, 'candidate_count': 13801}]},
    'opengu-aagu032-extend-v2': {
        'config_path': 'experiments/configs/aagu032_extend_v2/experiment.yaml',
        'config_sha256': 'c6032e4d5ed8a9d3ac02b5366eb42a018bfa09b16a08e1f671a6810005f62aa8',
        'configuration_fingerprint': 'a98b63a0bf2ee0377edc031e21b9db992d45123243fbe32d2b68330a21354842',
        'run_identity': {'experiment_id': 'aagu032-extended-v2-multi-gcn-retrain', 'run_id': 'aagu032-extend-v2'},
        'timeout_seconds': 21600, 'logical_cells': 360, 'stage': 'unlearning',
        'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                              {'num_nodes': 3327, 'candidate_count': 2328},
                              {'num_nodes': 19717, 'candidate_count': 13801}],
    },
}


def recipe_definitions():
    from pathlib import Path
    from experiments.modular_config import load_experiment
    root = Path(__file__).resolve().parents[2]
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
        paths = (summary,) + output_paths(summary, load_experiment(root / plan['config_path']))
        definitions[recipe_id] = {**copy.deepcopy(plan), 'id': recipe_id,
            'argv': ('{python}', 'experiments/run.py', plan['config_path'],
                     '--run-id', plan['run_identity']['run_id']),
            'git_binding_policy': 'job-exact-main-v1', 'requires_job_expected_git_sha': True,
            'timeout_seconds': plan['timeout_seconds'], 'expected_artifact_paths': paths,
            'collector_result_roots': (summary.rsplit('/', 1)[0],),
            'collector_artifact_names': ('run.json',) + ARTIFACT_NAMES,
            'preflight_profile': 'modular-project-v1', 'collector_profile': 'modular-output-v1',
            'collector_acceptance': True, 'execution_validator': 'exact-artifacts-json-v1',
            'success_predicate': 'json.passed == true and all reviewed artifacts exist'}
    return definitions
