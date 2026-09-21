"""Real run.py subprocess and generic SyncMate local transport, no GPU claims."""
import json
from pathlib import Path

import yaml

from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, cli, commit, declaration
from test_syncmate_gu_outputs import collect
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context


def test_observer_cli_collect_verify_and_accept(workspace, record_property):
    runner, path, config = workspace
    gu = yaml.safe_load((runner/'gu.yaml').read_text())
    gu.update(method='GIF', parameters={'iteration': 2, 'scale': 100, 'damp': .1})
    write_yaml(runner/'gif.yaml', gu)
    idea = {**gu, 'method': 'IDEA', 'parameters': {**gu['parameters'], 'gaussian_mean': 0., 'gaussian_std': 0.}}
    write_yaml(runner/'idea.yaml', idea)
    config.update(stage='unlearning', unlearning_refs=['gif.yaml', 'idea.yaml', 'retrain.yaml'],
        seeds=[42], budget_ratios=[.1], execution={'gu_cache': {'GIF': 'disabled', 'IDEA': 'disabled', 'Retrain': 'reuse'}},
        observers=[dict(name=name, methods=['GIF', 'IDEA']) for name in ('linear_solver_trace', 'same_graph_change')] +
        [dict(name='hessian_calibration', methods=['GIF', 'IDEA'], parameters={'lanczos_steps': 3})])
    write_yaml(path, config)
    sha = commit(runner)
    definition = declaration(runner, path, 'unlearning')
    definition['collector_artifact_names'] = tuple(sorted({Path(p).name for p in definition['expected_artifact_paths']}))
    command = cli(runner, path, 'registered')
    assert command.returncode == 0, command.stdout + command.stderr
    execution = json.loads(command.stdout)
    assert set(execution['generated_artifacts']) == set(definition['expected_artifact_paths'])
    collector = runner/'collector'
    collector.mkdir()
    for source in runner.glob('*.yaml'):
        (collector/source.name).write_bytes(source.read_bytes())
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        collected, _, _ = collect((runner, collector, sha, definition))
        checked = extension.accept('modular-output-v1', definition, collected)
        assert checked['passed'], checked
        assert checked['accepted_cells'] == 3
        rows = extension.results(collected['artifact_index'], {'project_root': collector})
        assert len(rows['rows']) == 3 and not rows['parse_errors'], rows
    assert not list(collector.rglob('output.npz'))
    assert not (collector/'results/cache_v2').exists()
    record_property('observer_collection', json.dumps(dict(checked=checked, files=len(definition['expected_artifact_paths']),
        source_sha=sha, transport='local', cli='experiments/run.py --verification-root', formal_gpu=False)))
