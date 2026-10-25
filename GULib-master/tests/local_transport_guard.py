"""Test fixtures for the standard-library transport boundary."""
import json
import os
from pathlib import Path
import pytest
from transport_boundary import ExternalTransportForbidden, install_guard


@pytest.fixture(autouse=True)
def local_only_transport(monkeypatch,tmp_path):
    """Default for deployment/UI tests; -p enables it for the whole selected run."""
    folder=tmp_path/'local-transport-guard'
    folder.mkdir()
    (folder/'sitecustomize.py').write_text('from local_transport_guard import install_guard\ninstall_guard()\n',encoding='utf-8')
    monkeypatch.setenv('PYTHONPATH',str(folder)+os.pathsep+str(Path(__file__).parent)+os.pathsep+os.environ.get('PYTHONPATH',''))
    monkeypatch.setenv('OPENGU_TEST_TRANSPORT_DENIALS',str(tmp_path/'transport-denied.jsonl'))
    install_guard(monkeypatch.setattr)


if os.environ.get('OPENGU_CPU_TESTS_ONLY') == '1':
    install_guard()
