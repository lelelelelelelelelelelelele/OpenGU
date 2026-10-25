"""Deliberately unisolated clients must fail before external process launch."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from local_transport_guard import ExternalTransportForbidden, local_only_transport


@pytest.mark.parametrize('program',['ssh','scp','sftp','curl','rsync'])
def test_unmapped_transport_is_rejected_before_launch(program):
    with pytest.raises(ExternalTransportForbidden,match='before launch'):
        subprocess.run([program,'never-execute.invalid'],check=True)
    records=[json.loads(x) for x in Path(os.environ['OPENGU_TEST_TRANSPORT_DENIALS']).read_text(encoding='utf-8').splitlines()]
    assert records[-1]['argv']==[program,'never-execute.invalid']


def test_child_python_inherits_transport_denial():
    result=subprocess.run([sys.executable,'-B','-c',
        "import subprocess; subprocess.Popen(['ssh','never-execute.invalid'])"],capture_output=True,text=True,encoding='utf-8')
    assert result.returncode!=0
    assert 'ExternalTransportForbidden' in result.stderr and 'before launch: ssh' in result.stderr
