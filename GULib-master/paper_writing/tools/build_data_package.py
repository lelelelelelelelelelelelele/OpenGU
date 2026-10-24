"""Build/verify the dated, offline paper handover; never executes experiments.

Run with Python 3.12+ from any directory. `snapshot` copies evidence without
changing it; `seal` hashes the complete payload and writes the portable ZIP.
"""
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import re
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'paper_writing/data_package/2026-10-24'
DRAFT = ROOT / 'self/research/experiments/drafts/paper-data-package'
REPO_TARGET = Path('sources/OpenGU/GULib-master')
SKIP_DIRS = {'.git', '.obsidian', '.trash', '__pycache__', '.pytest_cache', 'node_modules'}
SKIP_SUFFIXES = {'.pyc', '.pyo', '.synctex', '.aux', '.fls', '.fdb_latexmk'}
READ_ERRORS = []

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def hash_file(path):
    h = sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def walk(folder):
    for base, dirs, files in os.walk(folder, followlinks=False, onerror=lambda e: READ_ERRORS.append({'path':str(e.filename),'error':str(e)})):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith('cpu-tmp')
                         and not (Path(base) / d).is_symlink()
                         and not (hasattr(Path(base) / d, 'is_junction') and (Path(base) / d).is_junction()))
        for name in sorted(files):
            p = Path(base) / name
            if p.suffix.lower() not in SKIP_SUFFIXES and not p.is_symlink():
                yield p

def snapshot():
    PACKAGE.mkdir(parents=True, exist_ok=True)
    records = {}
    def copy_file(source, target, scope):
        if not source.is_file():
            return
        key = target.as_posix()
        try:
            h = hash_file(source)
        except OSError as exc:
            READ_ERRORS.append({'path':str(source),'error':str(exc)})
            return
        dest = PACKAGE / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or hash_file(dest) != h:
            shutil.copyfile(str(source), str(dest))
        assert hash_file(dest) == h, str(dest)
        records[key] = {'path': key, 'source': str(source), 'source_relative': str(source.relative_to(ROOT)).replace('\\', '/') if source.is_relative_to(ROOT) else None,
                        'sha256': h, 'bytes': source.stat().st_size, 'scope': scope}
    roots = ['results', 'self', 'report', 'reports', 'experiments', 'scripts', 'attack', 'cache_v2',
             'model', 'dataset', 'task', 'pipeline', 'unlearning', 'utils', 'tests']
    for name in roots:
        count = 0
        for p in walk(ROOT / name):
            copy_file(p, REPO_TARGET / p.relative_to(ROOT), name)
            count += 1
        print(json.dumps({'copied_scope': name, 'files': count}), flush=True)
    for p in ROOT.iterdir():
        if p.is_file() and p.suffix.lower() in {'.py', '.md', '.json', '.toml', '.yaml', '.yml', '.txt', '.sh', '.lock'}:
            copy_file(p, REPO_TARGET / p.name, 'repository_context')
    # Avoid recursive inclusion of this package; preserve all earlier writing evidence.
    writing = ROOT / 'paper_writing'
    for child in writing.iterdir():
        if child.name == 'data_package':
            continue
        for p in walk(child) if child.is_dir() else [child]:
            copy_file(p, REPO_TARGET / p.relative_to(ROOT), 'paper_writing')
    for item in ['AAGU-101', 'AAGU-107', 'AAGU-108', 'AAGU-109', 'AAGU-110']:
        for p in walk(ROOT / '.workblock/items' / item):
            copy_file(p, REPO_TARGET / p.relative_to(ROOT), 'explicit_implementation_evidence')
    # Copy exact evidence references; never scan unrelated WorkItems or credentials.
    catalog = json.loads((DRAFT / 'catalog.json').read_text(encoding='utf-8'))
    unresolved = []
    for row in catalog['path_inventory']:
        if row['kind'] == 'remote_posix_locator':
            unresolved.append(row)
            continue
        p = ROOT / row['path']
        if p.is_file():
            copy_file(p, REPO_TARGET / p.relative_to(ROOT), 'explicit_experiment_reference')
        elif p.is_dir():
            for child in walk(p):
                copy_file(child, REPO_TARGET / child.relative_to(ROOT), 'explicit_experiment_reference_directory')
        else:
            unresolved.append(row)
    dump(PACKAGE / 'UNRESOLVED_REFERENCES.json', unresolved)
    historical = json.loads((DRAFT / 'HISTORICAL_SOURCES.json').read_text(encoding='utf-8'))
    for row in historical['sources']:
        p = Path(row['absolute_path'])
        if p.is_file() and p.is_relative_to(ROOT):
            copy_file(p, REPO_TARGET / p.relative_to(ROOT), 'explicit_historical_reference')
    # Materialize only the two known, owned result aliases as regular portable files.
    aliases = []
    for rel in ['results/runs/exp080-cc-base/e80r305', 'results/runs/exp084-gnndelete-checkpoint-audit/e84r1']:
        alias = ROOT / rel
        if not alias.exists():
            aliases.append({'alias': rel, 'state': 'missing'})
            continue
        actual = alias.resolve()
        if not actual.is_relative_to(ROOT / 'results'):
            raise RuntimeError('Result alias leaves owned results: ' + str(alias))
        count = 0
        for p in walk(actual):
            copy_file(p, REPO_TARGET / rel / p.relative_to(actual), 'materialized_result_alias')
            count += 1
        aliases.append({'alias': rel, 'actual': str(actual), 'files': count, 'state': 'materialized_as_regular_files'})
    docmap = ROOT.parents[1] / 'OpenGU-DocMap'
    for p in walk(docmap):
        copy_file(p, Path('sources/OpenGU-DocMap') / p.relative_to(docmap), 'research_and_writing_design')
    # Close file links of source reports. Missing historical links stay explicit.
    checked = set()
    link_gaps = []
    while True:
        todo = [(k, r) for k, r in records.items() if k not in checked and Path(k).suffix.lower() in {'.md', '.html'}]
        if not todo:
            break
        for key, row in todo:
            checked.add(key)
            original = Path(row['source'])
            try:
                content = original.read_text(encoding='utf-8')
            except (OSError, UnicodeError) as exc:
                READ_ERRORS.append({'path':str(original),'error':str(exc)})
                continue
            links = re.findall(r'(?:href|src)=[\"\x27]([^\"\x27]+)[\"\x27]', content)
            links += re.findall(r'\]\(([^\n()]+)\)', content)
            for raw in links:
                value = unquote(raw.strip('<>'))
                if value.startswith(('#', 'http:', 'https:', 'mailto:', 'data:', 'javascript:')):
                    continue
                value = value.removeprefix('file:///').split('#')[0].split('?')[0]
                if not value:
                    continue
                value = re.sub(r':\d+(?:[-–]\d+)?$', '', value)
                p = Path(value)
                if not p.is_absolute():
                    p = (original.parent / p).resolve()
                if p.is_relative_to(ROOT / 'paper_writing/data_package'):
                    continue
                if p.is_relative_to(ROOT):
                    target = REPO_TARGET / p.relative_to(ROOT)
                elif p.is_relative_to(docmap):
                    target = Path('sources/OpenGU-DocMap') / p.relative_to(docmap)
                else:
                    link_gaps.append({'source':key,'link':raw,'reason':'outside_owned_source_roots'})
                    continue
                if p.is_file():
                    copy_file(p, target, 'linked_report_evidence')
                elif not p.exists():
                    link_gaps.append({'source':key,'link':raw,'reason':'historical_target_not_found'})
    dump(PACKAGE / 'HISTORICAL_LINK_GAPS.json', link_gaps)
    for name in ['catalog.json', 'CATALOG_NOTES.md', 'DESIGN_METHODS.md', 'DATA_DICTIONARY.md', 'HISTORICAL_SYNTHESIS.md', 'HISTORICAL_SOURCES.json']:
        if not (DRAFT / name).is_file():
            raise RuntimeError('Required handover input missing: ' + name)
        copy_file(DRAFT / name, Path('handover') / name, 'current_handover_synthesis')
    dump(PACKAGE / 'READ_ERRORS.json', READ_ERRORS)
    dump(PACKAGE / 'SOURCE_MANIFEST.json', {
        'created_at': datetime.now(timezone.utc).isoformat(),
        'repository_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'snapshot_not_live_state': True,
        'copy_policy': 'Exact bytes. Local results and dated state included; raw model/dataset remote stores not fetched. Historical sources keep their original wording; use current adoption guide.',
        'excluded': ['.git/.obsidian/node_modules/__pycache__/.pytest_cache', 'CPU-test scratch directories cpu-tmp*', 'derived LaTeX compiler scratch', 'this data_package tree itself', 'non-result filesystem links'],
        'result_aliases': aliases, 'files': sorted(records.values(), key=lambda r: r['path'])})
    print(json.dumps({'snapshot_files': len(records), 'bytes': sum(r['bytes'] for r in records.values())}), flush=True)

def seal():
    payload = []
    for p in walk(PACKAGE):
        if p.name in ['MANIFEST.json', 'VALIDATION.json'] and p.parent == PACKAGE:
            continue
        payload.append({'path': p.relative_to(PACKAGE).as_posix(), 'bytes': p.stat().st_size, 'sha256': hash_file(p)})
    dump(PACKAGE / 'MANIFEST.json', {'schema': 1, 'sealed_at': datetime.now(timezone.utc).isoformat(),
         'purpose': 'Complete local writing evidence handover, not full remote training reproduction',
         'files': payload})
    verify()
    target = PACKAGE.parent / 'WWW27-paper-data-2026-10-24.zip'
    with zipfile.ZipFile(str(target), 'w', zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for p in walk(PACKAGE):
            z.write(str(p), '2026-10-24/' + p.relative_to(PACKAGE).as_posix())
    # Independently check CRC for every compressed member before delivery.
    with zipfile.ZipFile(str(target)) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError('ZIP CRC mismatch: ' + bad)
        members = len(z.infolist())
    dump(PACKAGE.parent / 'WWW27-paper-data-2026-10-24.zip.sha256.json',
         {'path': target.name, 'bytes': target.stat().st_size, 'sha256': hash_file(target), 'members': members, 'crc_test': 'passed'})
    print(json.dumps({'zip': str(target), 'bytes': target.stat().st_size, 'members': members}), flush=True)

def verify():
    errors = []
    manifest = json.loads((PACKAGE / 'MANIFEST.json').read_text(encoding='utf-8'))
    for r in manifest['files']:
        p = PACKAGE / r['path']
        if not p.is_file() or p.stat().st_size != r['bytes'] or hash_file(p) != r['sha256']:
            errors.append(r['path'])
    dump(PACKAGE / 'VALIDATION.json', {'passed': not errors, 'files_checked': len(manifest['files']), 'errors': errors,
          'meaning': 'Byte integrity only; scientific adoption is governed by claim guide and experiment decisions.'})
    if errors:
        raise RuntimeError('Package failed integrity: ' + repr(errors[:10]))
    print(json.dumps({'verified_payload_files': len(manifest['files']), 'passed': True}), flush=True)

if __name__ == '__main__':
    {'snapshot': snapshot, 'seal': seal, 'verify': verify}[sys.argv[1]]()
