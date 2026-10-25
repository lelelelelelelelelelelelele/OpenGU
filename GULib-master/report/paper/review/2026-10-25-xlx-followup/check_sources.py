from pathlib import Path
import csv
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
W = Path('C:/Users/ADMIN/.codex/worktrees/paper-reentry-v1/OpenGU/GULib-master')
D = Path('C:/Users/ADMIN/.codex/worktrees/dual-ssh-runners/OpenGU/GULib-master')
review = W / 'paper_writing/review/2026-10-25-reentry'
paths = [review / name for name in ['POST_REVIEW.md', 'RESULTS_ARGUMENTS.md', 'CHANNEL_PRECISION.md', 'CHANNEL_PRECISION_INPUTS.json', 'CHANNEL_EXPLORATORY_INTERVALS.csv', 'REVIEW_INPUTS.json']]
paths += [ROOT / 'self/research/experiments/EXP-089.json', ROOT / 'self/research/experiments/drafts/round4-execution/method-sensitivity-prep/PROTOCOL.md', ROOT / '.workblock/items/AAGU-121/WORKITEM.md', ROOT / '.workblock/runtime/AAGU-121/pytest-final-guarded.xml', Path('E:/project/SyncMate/.workblock/items/SM-027/WORKITEM.md')]
records = [dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size) for p in paths]
manifest = json.loads((review / 'REVIEW_INPUTS.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    p = review / item['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256'], p
interval_inputs = json.loads((review / 'CHANNEL_PRECISION_INPUTS.json').read_text(encoding='utf-8'))
for path, digest in interval_inputs['files'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
with (review / 'CHANNEL_EXPLORATORY_INTERVALS.csv').open(encoding='utf-8-sig', newline='') as handle:
    intervals = list(csv.DictReader(handle))
assert len(intervals) == 672 and all(int(r['n']) == 10 for r in intervals)
tests = ET.parse(ROOT / '.workblock/runtime/AAGU-121/pytest-final-guarded.xml').getroot()
suites = [{k: s.attrib[k] for k in ('tests', 'errors', 'failures', 'skipped', 'timestamp')} for s in tests.iter('testsuite')]
assert sum(int(s['tests']) for s in suites) == 89
assert all(int(s['errors']) == int(s['failures']) == int(s['skipped']) == 0 for s in suites)
def head(path):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + path.parent.as_posix(), '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
result = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(), thread_id='01a16ada-da3c-7521-87d8-b47f4f1823fb', sources=records, frozen_inputs_verified=len(manifest['files']), channel_groups=672, tests=suites, paper_head=head(W), integration_head=head(D), scope='Read-only current evidence audit; no experiment/installation/acceptance or new scientific inference')
(HERE / 'AUDIT_RECEIPT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'sources'}, ensure_ascii=False))
