"""Work Plan facts. No Block enumeration, state writes, Git or execution side effects."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

STATES = {
    'preparation': {'draft': '待定义', 'preparing': '准备中', 'defined': '定义已固定'},
    'execution': {'unknown': '待核对', 'pending': '待运行', 'running': '运行中',
                  'partial': '部分完成', 'completed': '运行已完成', 'not_required': '无需新运行', 'failed': '运行失败'},
    'analysis': {'not_started': '待分析', 'working': '分析中', 'review': '待复核', 'complete': '分析已交付'},
    'decision': {'pending': '待科学决定', 'accepted': '已接受所述范围', 'rejected': '未接受', 'not_requested': '尚未提交决定'},
}
ID = re.compile(r'AAGU-\d{3}')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def load(root, canonical=None):
    source = root / 'self/research'
    frame = read_json(source / 'framework.json')
    states = read_records((canonical or root) / 'self/research/experiments')
    analyses = read_records(source / 'analyses')
    if not states or analyses.keys() - states.keys():
        raise ValueError('Missing local experiment state; restore self/research/experiments '
                         'from its maintained copy, not from historical analysis')
    records = []
    for key, state in states.items():
        if 'analysis' in state or 'decision' in state:
            raise ValueError('Analysis/decision belongs in analyses/: ' + key)
        published = analyses.get(key)
        record = dict(state)
        record['analysis'] = {'state': 'not_started', 'note': '尚无已保存分析。', 'evidence': []}
        record['decision'] = {'state': 'not_requested', 'note': '尚无已保存科学决定。', 'evidence': []}
        if published:
            if {'preparation', 'execution', 'next_step', 'blocks', 'dependencies'} & published.keys():
                raise ValueError('Live state belongs in experiments/: ' + key)
            for field in ('title', 'question', 'scope', 'recorded_at', 'configs', 'sources', 'attempts', 'history'):
                if field not in published:
                    raise ValueError('Missing analysis context: ' + field)
            record.update({stage: published[stage] for stage in ('analysis', 'decision')})
            record['published_analysis'] = published
        records.append(record)
    validate(records)
    return frame, records


def read_records(directory):
    records = {}
    for path in sorted(directory.glob('*.json')):
        record = read_json(path)
        if not ID.fullmatch(path.stem) or record.get('id') != path.stem:
            raise ValueError('Experiment filename/ID mismatch: ' + str(path))
        records[path.stem] = record
    return records


def validate(records):
    ids = {r['id'] for r in records}
    if len(ids) != len(records):
        raise ValueError('Duplicate experiment ID')
    for r in records:
        if not ID.fullmatch(r['id']):
            raise ValueError('Invalid experiment ID')
        for field in ('title', 'question', 'scope', 'next_step', 'reviewed_at', 'history', 'sources'):
            if not r.get(field):
                raise ValueError('Missing experiment field: ' + field)
        if r['category'] not in {'active', 'planned', 'history'}:
            raise ValueError('Invalid category')
        for stage in STATES:
            if r[stage]['state'] not in STATES[stage] or not r[stage].get('note'):
                raise ValueError('Invalid stage: ' + stage)
        if r['execution']['state'] in {'completed', 'partial', 'running', 'failed'} and not r['execution']['evidence']:
            raise ValueError('Observed execution requires evidence')
        if r['analysis']['state'] in {'review', 'complete'} and not r['analysis']['evidence']:
            raise ValueError('Analysis requires evidence')
        if r['decision']['state'] in {'accepted', 'rejected'} and not r['decision']['evidence']:
            raise ValueError('Decision requires evidence')
        for dep in r['dependencies']:
            if dep['experiment'] not in ids or dep['experiment'] == r['id']:
                raise ValueError('Unknown/self experiment dependency')
            if dep['stage'] not in {'preparation', 'execution', 'analysis'} or not dep['reason']:
                raise ValueError('Invalid experiment dependency')
            if dep['requirement'] not in {'evidence', 'analysis', 'accepted', 'successful_acceptance'}:
                raise ValueError('Invalid experiment requirement')
        for b in r['blocks']:
            if not ID.fullmatch(b['id']) or b['stage'] not in {'preparation', 'execution', 'analysis'} or not b['reason']:
                raise ValueError('Invalid Block dependency')
            if not b['delivery_note'] or type(b['delivery_confirmed']) is not bool:
                raise ValueError('Block delivery observation required')
        events = r['history']
        if len({e['id'] for e in events}) != len(events):
            raise ValueError('Duplicate event ID')
        for event in events:
            if not event['at'] or not event['note'] or not event['evidence']:
                raise ValueError('History needs dated evidence')
        for attempt in r['attempts']:
            if not attempt['run_id'] or not attempt['scope'] or not attempt['evidence']:
                raise ValueError('Run attempt requires identity, scope and evidence')
        for c in r['configs']:
            if c['role'] not in {'current', 'reference', 'historical', 'candidate'} or not c['path'].endswith(('.yaml', '.yml')):
                raise ValueError('Invalid config')
    lookup = {r['id']: r for r in records}
    def visit(key, trail):
        if key in trail:
            raise ValueError('Cyclic experiment dependency')
        for dep in lookup[key]['dependencies']:
            visit(dep['experiment'], trail | {key})
    for key in ids:
        visit(key, set())


def block_status(root, dependency):
    """Read ONLY the explicitly referenced Block. Unknown/absent never unblocks."""
    path = root / '.workblock/items' / dependency['id'] / 'WORKITEM.md'
    if not path.exists():
        return {'status': '记录缺失', 'resolved': False}
    content = path.read_text(encoding='utf-8')
    matches = re.findall(r'^当前状态:\s*`?([^`\n]+)`?\s*$', content, re.M)
    status = matches[0].strip() if len(matches) == 1 else '状态不明确'
    accepted = status.casefold() in {'accepted', 'accepted / closed'}
    return {'status': status, 'resolved': accepted and dependency['delivery_confirmed']}


def dependencies(record, records, canonical):
    result = []
    for b in record['blocks']:
        result.append(dict(b, kind='block', **block_status(canonical, b)))
    lookup = {r['id']: r for r in records}
    for d in record['dependencies']:
        parent = lookup[d['experiment']]
        requirement = d['requirement']
        resolved = (bool(parent['execution']['evidence']) and parent['execution']['state'] == 'completed'
                    if requirement == 'evidence' else
                    parent['analysis']['state'] == 'complete' if requirement == 'analysis' else
                    parent['decision']['state'] == 'accepted' and parent['decision'].get('success_confirmed') is True
                    if requirement == 'successful_acceptance' else
                    parent['decision']['state'] == 'accepted')
        if requirement != 'evidence':
            published = parent.get('published_analysis')
            resolved = resolved and bool(published) and all(
                published[field] == parent[field] for field in ('scope', 'configs'))
        result.append(dict(d, id=d['experiment'], kind='experiment', resolved=resolved,
                           status={'evidence': '需要匹配结果', 'analysis': '需要分析交付', 'accepted': '需要科学接受', 'successful_acceptance': '需要验证成功且科学接受'}[requirement]))
    return result


def refs(value):
    if isinstance(value, dict):
        if 'path' in value and 'label' in value:
            yield value
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def resolve(root, canonical, path):
    if path.startswith('../../OpenGU-DocMap/'):
        suffix = path[len('../../OpenGU-DocMap/'):]
        target = canonical.parent.parent / 'OpenGU-DocMap' / suffix
        if '..' in Path(suffix).parts or Path(suffix).anchor or ':' in suffix or '\\' in suffix:
            raise ValueError('Unsafe source path')
        return target
    p = Path(path)
    if p.anchor or '..' in p.parts or ':' in path or '\\' in path:
        raise ValueError('Unsafe source path: ' + path)
    base = canonical if path.startswith(('.workblock/', 'results/', '.syncmate/', 'self/research/experiments/')) else root
    return base / p


def check_links(frame, records, root, canonical):
    references = list(refs([frame, records]))
    missing = [r['path'] for r in references if not resolve(root, canonical, r['path']).exists()]
    if missing:
        raise ValueError('Missing sources: ' + ', '.join(sorted(set(missing))))
    return len(references)


def verify_manifests(records, root, canonical):
    """Explicit selected manifests only; does not turn local files into trusted evidence."""
    count = 0
    for record in records:
        if record.get('published_analysis'):
            count += verify_manifests([record['published_analysis']], root, canonical)
        for attempt in record['attempts']:
            bound = attempt.get('manifest')
            if not bound:
                continue
            path = resolve(root, canonical, bound['path'])
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != bound['sha256']:
                raise ValueError('Manifest changed: ' + attempt['run_id'])
            run = json.loads(raw)
            if run['run_id'] != attempt['run_id'] or run['experiment_id'] != bound['experiment_id'] or run['commit'] != bound['commit']:
                raise ValueError('Run identity mismatch')
            cells = run['cells']
            if len({c['cell_id'] for c in cells}) != len(cells):
                raise ValueError('Duplicate cell identity')
            if sum(c['status'] == 'completed' for c in cells) != bound['completed']:
                raise ValueError('Run count mismatch')
            for cell in cells:
                for name, info in cell['files'].items():
                    artifact = (path.parent / cell['path'] / name).resolve()
                    try:
                        artifact.relative_to(path.parent.resolve())
                    except ValueError as exc:
                        raise ValueError('Unsafe artifact path') from exc
                    if hashlib.sha256(artifact.read_bytes()).hexdigest() != info['sha256']:
                        raise ValueError('Artifact checksum mismatch: ' + str(artifact))
                    count += 1
            count += 1
    return count
