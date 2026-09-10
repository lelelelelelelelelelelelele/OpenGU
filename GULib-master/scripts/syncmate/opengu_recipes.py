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
        'config_sha256': 'e0fb680d39efd67e6cdadab1ed45b4e87e52a963da02638c77ce0baf53584521',
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
'opengu-aagu011-gate-v1': {'config_path': 'experiments/configs/aagu011/gate.yaml',
                            'config_sha256': 'b1df26d4c473efa01e810e0f28bc43368f0bc98a763241ff2e957e6be64acf91',
                            'configuration_fingerprint': '4116feb355938c619de9252ef571d5e855a725bc5ab2821b788117ed8be4611c',
                            'run_identity': {'experiment_id': 'aagu011-table01-gate',
                                             'run_id': 'aagu011-gate-v1'},
                            'timeout_seconds': 21600,
                            'logical_cells': 18,
                            'stage': 'unlearning',
                            'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                                                  {'num_nodes': 3327, 'candidate_count': 2328},
                                                  {'num_nodes': 19717, 'candidate_count': 13801}]},
 'opengu-aagu011-references-v1': {'config_path': 'experiments/configs/aagu011/references.yaml',
                                  'config_sha256': '9967286dc86ba7b1da3e4a46b726153549008eb70baf73a427b25cf6600bc898',
                                  'configuration_fingerprint': 'b705d04376544616ab6f5d83bd69daea79034965b27c15365a5a0c45a1c956fc',
                                  'run_identity': {'experiment_id': 'aagu011-table01-retrain',
                                                   'run_id': 'aagu011-references-v1'},
                                  'timeout_seconds': 21600,
                                  'logical_cells': 45,
                                  'stage': 'unlearning',
                                  'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                                                        {'num_nodes': 3327, 'candidate_count': 2328},
                                                        {'num_nodes': 19717, 'candidate_count': 13801}]},
 'opengu-aagu011-table01-v1': {'config_path': 'experiments/configs/aagu011/table01.yaml',
                               'config_sha256': '65dd62ca4e0297765e36a7fc7ee81102dc5604a2686e3e50553fc5f7d7e51f33',
                               'configuration_fingerprint': '4b97e59cb8cf0462f16353d1c10b88d967a84e6efb117911fe5d3d2f5fcc7cdf',
                               'run_identity': {'experiment_id': 'aagu011-table01-gu',
                                                'run_id': 'aagu011-table01-v1'},
                               'timeout_seconds': 21600,
                               'logical_cells': 270,
                               'stage': 'unlearning',
                               'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                                                     {'num_nodes': 3327, 'candidate_count': 2328},
                                                     {'num_nodes': 19717, 'candidate_count': 13801}]},
}


EXPERIMENT_RECIPES['opengu-aagu047-shard-gate-v1'] = {
    'config_path': 'experiments/configs/aagu011/recovery_gate.yaml',
    'config_sha256': '2a8970e305e0c314b2e32cdcf0227fd7e7baad1857e55346ca056fa8e438f568',
    'configuration_fingerprint': 'cf3bc6e7083883d74ffbf88620df2d61d370864bfb85a792bc42f5c9b7550270',
    'run_identity': {'experiment_id': 'aagu047-shard-numerics', 'run_id': 'aagu047-shard-gate-v1'},
    'timeout_seconds': 21600, 'logical_cells': 12, 'stage': 'unlearning',
    'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                          {'num_nodes': 3327, 'candidate_count': 2328},
                          {'num_nodes': 19717, 'candidate_count': 13801}],
}
EXPERIMENT_RECIPES['opengu-aagu011-table01-v2'] = copy.deepcopy(EXPERIMENT_RECIPES['opengu-aagu011-table01-v1'])
EXPERIMENT_RECIPES['opengu-aagu011-table01-v2']['run_identity']['run_id'] = 'aagu011-table01-v2'


EXPERIMENT_RECIPES['opengu-aagu048-gpa-gate-v1'] = copy.deepcopy(EXPERIMENT_RECIPES['opengu-aagu047-shard-gate-v1'])
EXPERIMENT_RECIPES['opengu-aagu048-gpa-gate-v1'].update({
    'config_path': 'experiments/configs/aagu011/recovery_gate_v2.yaml',
    'config_sha256': '4424629c775f2e1d8274ab578a40ac51b1e377bf8ee84547783b8834e9b3a543',
    'configuration_fingerprint': '97277ec53f40c7a10eb7ad2384a5fffb3dc2683ca1e573d57925bded0d335c3e',
    'run_identity': {'experiment_id': 'aagu048-gpa-numerics', 'run_id': 'aagu048-gpa-gate-v1'},
})


EXPERIMENT_RECIPES['opengu-aagu051-gate-v1'] = {'config_path': 'experiments/configs/aagu051/gate.yaml',
 'config_sha256': '4a739195862329bab803ff11a4730e325e3ca3159810c387beaf08b28ff11e19',
 'configuration_fingerprint': '1cb3324c7d6deb81c5e0725e46c44443b6b6ba3de5a6f049f0a7cc1715335829',
 'run_identity': {'experiment_id': 'aagu051-random-gate',
                  'run_id': 'aagu051-gate-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 30,
 'stage': 'unlearning',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                       {'num_nodes': 3327, 'candidate_count': 2328},
                       {'num_nodes': 19717, 'candidate_count': 13801}]}
EXPERIMENT_RECIPES['opengu-aagu051-table-v1'] = {'config_path': 'experiments/configs/aagu051/table.yaml',
 'config_sha256': '84fbe2d3e753870ef1d55a128498d4206f346f9c0b783f242bd49502790cdfa1',
 'configuration_fingerprint': '34a2d4dd387f990a39daf4f4ed718428cce50ab84cce92b9f3586371cbc9d140',
 'run_identity': {'experiment_id': 'aagu051-random-response',
                  'run_id': 'aagu051-table-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 150,
 'stage': 'unlearning',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                       {'num_nodes': 3327, 'candidate_count': 2328},
                       {'num_nodes': 19717, 'candidate_count': 13801}]}


EXPERIMENT_RECIPES['opengu-aagu053-gate-v1'] = {'config_path': 'experiments/configs/im_group_discussion/gate_10.yaml',
 'config_sha256': '0264197ecb135798da8187c3250d6fbebbf68a7a97e3b8880c4bec9bec1f1f6c',
 'configuration_fingerprint': 'f40d0751d691f3892b8980ca56836ec72216ea13e098968e31120d7bbe452315',
 'run_identity': {'experiment_id': 'aagu053-im-group-gate10',
                  'run_id': 'aagu053-gate-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 36,
 'stage': 'unlearning',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                       {'num_nodes': 3327, 'candidate_count': 2328},
                       {'num_nodes': 19717, 'candidate_count': 13801}]}
EXPERIMENT_RECIPES['opengu-aagu053-table-v1'] = {'config_path': 'experiments/configs/im_group_discussion/Experiment.yaml',
 'config_sha256': 'b44d131927bf822e008ac86a448dc7c9c60c5acd4d44b6d0f6aa50da6d4eee8b',
 'configuration_fingerprint': 'd296c63caf0cae2950f3a4fb3f590c78f249911311883b8e25d3f68f67486a15',
 'run_identity': {'experiment_id': 'aagu053-im-group-budget10',
                  'run_id': 'aagu053-table-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 96,
 'stage': 'unlearning',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                       {'num_nodes': 3327, 'candidate_count': 2328},
                       {'num_nodes': 19717, 'candidate_count': 13801}]}
EXPERIMENT_RECIPES['opengu-aagu053-selection05-v1'] = {'config_path': 'experiments/configs/im_group_discussion/selection_05.yaml',
 'config_sha256': '0e295f1c655bf1a5c2a59f46fadb40bd25e29e7be5fe41c877d8d7c6141f1623',
 'configuration_fingerprint': '57c2384784f3e8d6660d69567f641f25f53a541e929e8ae44c041eab35bca2d4',
 'run_identity': {'experiment_id': 'aagu053-im-group-selection05',
                  'run_id': 'aagu053-selection05-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 48,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895},
                       {'num_nodes': 3327, 'candidate_count': 2328},
                       {'num_nodes': 19717, 'candidate_count': 13801}]}


EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-cora-s22-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_cora_s22.yaml',
 'config_sha256': '74238be764f8bbf0aaf03555952dd6ac3790f3596812dc987e82113d9321da44',
 'configuration_fingerprint': 'aa998ba3f7efac60ec7522c88949874e03d1b24d3faae675e104d886cbf2f882',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-cora-s22',
                  'run_id': 'aagu053-celf-warmup-cora-s22-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895}]}
EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-cora-s33-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_cora_s33.yaml',
 'config_sha256': '499699e065c40bed35ed74ab5ded7d42d4d86b6ddd55fd3e07a6b6174e706e6e',
 'configuration_fingerprint': '7250f94f63492c59f68146ea0f398270b5f6e95dcd2462f9e7b41baff74066c8',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-cora-s33',
                  'run_id': 'aagu053-celf-warmup-cora-s33-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 2708, 'candidate_count': 1895}]}
EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-citeseer-s22-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_citeseer_s22.yaml',
 'config_sha256': '55723b79038e23c7d4217d2aed09302828c4fe50d5f20a8d003e5b42a5f95c21',
 'configuration_fingerprint': '75f193e93b723c59a0021cd007488025e854ffbcbe6330a1f56bad33dba01d97',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-citeseer-s22',
                  'run_id': 'aagu053-celf-warmup-citeseer-s22-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 3327, 'candidate_count': 2328}]}
EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-citeseer-s33-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_citeseer_s33.yaml',
 'config_sha256': 'c2d36863f36fc2fccc62e48345ba1f0028a354ae1756c1152ecd7aa03afb3fbf',
 'configuration_fingerprint': 'f6ff71d740501dc77be3cb29b3f47378f81f14406bc7de57791bcd12c2088174',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-citeseer-s33',
                  'run_id': 'aagu053-celf-warmup-citeseer-s33-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 3327, 'candidate_count': 2328}]}
EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-pubmed-s22-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_pubmed_s22.yaml',
 'config_sha256': 'f7f2506510230b57df9a004013f787c085dd4313e955f88d9746f68a55d72e85',
 'configuration_fingerprint': 'a9fefe5333e8791e5b4aa23257326b5c93491e7793cdeb205bf79ec96b3d5114',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-pubmed-s22',
                  'run_id': 'aagu053-celf-warmup-pubmed-s22-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 19717, 'candidate_count': 13801}]}
EXPERIMENT_RECIPES['opengu-aagu053-celf-warmup-pubmed-s33-v1'] = {'config_path': 'experiments/configs/im_group_discussion/celf_warmup_pubmed_s33.yaml',
 'config_sha256': '91d473d01cb7c90598d77075899d0d09facd982c9b4a58e01ba3a346d1f920e2',
 'configuration_fingerprint': '542e600b038ea4c6a4c0a7b7a20c6cbc1983971bc959be749cfaca139c7acb94',
 'run_identity': {'experiment_id': 'aagu053-celf-warmup-pubmed-s33',
                  'run_id': 'aagu053-celf-warmup-pubmed-s33-v1'},
 'timeout_seconds': 21600,
 'logical_cells': 1,
 'stage': 'selector',
 'expected_datasets': [{'num_nodes': 19717, 'candidate_count': 13801}]}

EXPERIMENT_RECIPES['opengu-aagu056-rr1024-v1'] = {
    'config_path': 'experiments/configs/aagu056/rr_1024.yaml',
    'config_sha256': '0f7c7806c1e4ca168a713d682dbdbe8130c0e30c1eb8c9f86563f94bf8c7d55a',
    'configuration_fingerprint': '2094d1c119bd6c7170cdfe9ae40d6637f4b6a24a10e9abb8d8d8da3243e523ea',
    'run_identity': {'experiment_id': 'aagu056-arxiv-rr1024-budget05',
                     'run_id': 'aagu056-rr1024-v1'},
    'timeout_seconds': 21600,
    'logical_cells': 1,
    'stage': 'selector',
    'expected_datasets': [{'num_nodes': 169343, 'candidate_count': 118540}],
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
