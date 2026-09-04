import hashlib
import json
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace
import pytest
from scripts.syncmate.verify_core_dependency import verify_core_dependency


@pytest.fixture
def installed(tmp_path):
    package = tmp_path / 'syncmate_core'
    package.mkdir()
    source = package / '__init__.py'
    source.write_text('__version__ = "0.3.0"\n', encoding='utf-8')
    pin = tmp_path / 'pin.json'
    pin.write_text(json.dumps({'distribution': 'syncmate', 'version': '0.3.0',
        'files': {'syncmate_core/__init__.py': hashlib.sha256(source.read_bytes()).hexdigest()}}))
    return {'distribution_lookup': lambda name: SimpleNamespace(version='0.3.0', locate_file=lambda p: tmp_path / p),
            'core_module': SimpleNamespace(__version__='0.3.0', __file__=str(source)), 'pin_path': pin}


def test_absent_distribution_fails_closed(installed):
    def missing(name):
        raise metadata.PackageNotFoundError(name)
    installed['distribution_lookup'] = missing
    result = verify_core_dependency(**installed)
    assert not result['ready']
    assert result['errors'] == ['SyncMate Core distribution is not installed']


def test_exact_payload_passes_without_self_declared_commit(installed):
    assert verify_core_dependency(**installed)['ready']


@pytest.mark.parametrize('change', ['corrupt', 'missing', 'shadow', 'version', 'residual'])
def test_installation_identity_failures(installed, change):
    path = Path(installed['core_module'].__file__)
    if change == 'corrupt':
        path.write_text('changed')
    elif change == 'missing':
        path.unlink()
    elif change == 'shadow':
        installed['core_module'].__file__ = str(path.parent.parent / '__init__.py')
    elif change == 'version':
        installed['core_module'].__version__ = '0.2.0'
    else:
        path.with_name('legacy.py').write_text('obsolete')
    assert not verify_core_dependency(**installed)['ready']
