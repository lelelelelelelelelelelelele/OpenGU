"""Historical configuration references used by the offline calibration analyzer."""
import subprocess

import pytest

from experiments.analyze_observer_calibration import read_git_yaml, resolve_config_ref


@pytest.mark.parametrize('reference, expected', [
    ('citeseer.yaml', 'experiments/configs/datasets/citeseer.yaml'),
    ('./citeseer.yaml', 'experiments/configs/aagu067/citeseer.yaml'),
    ('../datasets/citeseer.yaml', 'experiments/configs/datasets/citeseer.yaml'),
])
def test_dataset_reference_forms(reference, expected):
    assert resolve_config_ref('experiments/configs/aagu067', reference, 'dataset_refs') == expected


@pytest.mark.parametrize('reference', ['/tmp/data.yaml', '../../../../escape.yaml', 'C:graph.yaml', 'x\\graph.yaml', '', 'graph.json'])
def test_invalid_references_fail_closed(reference):
    with pytest.raises(ValueError):
        resolve_config_ref('experiments/configs/aagu067', reference, 'dataset_refs')


def test_public_method_reference():
    assert resolve_config_ref('experiments/configs/aagu067', 'gif.yaml', 'unlearning_refs') == 'experiments/configs/unlearning/gif.yaml'


def test_configuration_read_is_pinned_to_run_commit(tmp_path):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args], text=True).strip()

    git('init', '-q')
    relative = resolve_config_ref('experiments/configs/aagu067', 'citeseer.yaml', 'dataset_refs')
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_text('dataset:\n  name: CiteSeer\n', encoding='utf-8')
    git('add', relative)
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'dataset at run time')
    commit = git('rev-parse', 'HEAD')
    path.unlink()
    value, _ = read_git_yaml(tmp_path, commit, relative, 'dataset')
    assert value['dataset']['name'] == 'CiteSeer'
    with pytest.raises(ValueError, match='absent from run commit'):
        read_git_yaml(tmp_path, commit, 'experiments/configs/datasets/missing.yaml', 'dataset')
