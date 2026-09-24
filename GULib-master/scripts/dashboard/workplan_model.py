"""Work Plan facts. No Block enumeration, state writes, Git or execution side effects."""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

STATES = {
    'preparation': {'draft': '待定义', 'preparing': '准备中', 'ready': '准备就绪', 'ongoing': '进行中', 'defined': '定义已固定'},
    'execution': {'unknown': '待核对', 'pending': '待运行', 'running': '运行中',
                  'partial': '部分完成', 'completed': '运行已完成', 'not_required': '无需新运行', 'failed': '运行失败'},
    'analysis': {'not_started': '待分析', 'working': '分析中', 'review': '待复核', 'complete': '分析已交付'},
    'decision': {'pending': '待科学决定', 'accepted': '已接受所述范围', 'rejected': '未接受', 'not_requested': '尚未提交决定'},
}
STATE_ALIASES = {'preparation': {'partially_verified': 'ongoing'}}
ESTIMATE_STATUSES = {'estimated', 'not_recorded', 'not_applicable'}
ACTUAL_STATUSES = {'recorded', 'not_recorded', 'not_applicable'}
CACHE_STATUSES = {'observed', 'not_recorded', 'not_applicable'}
ATTEMPT_ESTIMATE_STATUSES = {'recorded_before_start', 'not_recorded_before_start', 'not_applicable'}
MATCH_TOLERANCE = 0.20
EXPERIMENT_ID = re.compile(r'EXP-\d{3}')
BLOCK_ID = re.compile(r'AAGU-\d{3}')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def canonical_state(stage, state):
    return STATE_ALIASES.get(stage, {}).get(state, state)


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
            for field in ('title', 'question', 'scope', 'recorded_at', 'configs', 'sources', 'attempts'):
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
        if not EXPERIMENT_ID.fullmatch(path.stem) or record.get('id') != path.stem:
            raise ValueError('Experiment filename/ID mismatch: ' + str(path))
        records[path.stem] = record
    return records


def validate(records):
    ids = {r['id'] for r in records}
    if len(ids) != len(records):
        raise ValueError('Duplicate experiment ID')
    for r in records:
        if not EXPERIMENT_ID.fullmatch(r['id']):
            raise ValueError('Invalid experiment ID')
        for field in ('title', 'question', 'scope', 'next_step', 'reviewed_at', 'sources'):
            if not r.get(field):
                raise ValueError('Missing experiment field: ' + field)
        if r['category'] not in {'active', 'planned', 'history'}:
            raise ValueError('Invalid category')
        for stage in STATES:
            state = canonical_state(stage, r[stage]['state'])
            if state not in STATES[stage] or not r[stage].get('note'):
                raise ValueError('Invalid stage: ' + stage)
        if r['execution']['state'] in {'completed', 'partial', 'running', 'failed'} and not r['execution']['evidence']:
            raise ValueError('Observed execution requires evidence')
        if r['analysis']['state'] in {'review', 'complete'} and not r['analysis']['evidence']:
            raise ValueError('Analysis requires evidence')
        if r['decision']['state'] in {'accepted', 'rejected'} and not r['decision']['evidence']:
            raise ValueError('Decision requires evidence')
        validate_time_budget(r)
        for dep in r['dependencies']:
            if dep['experiment'] not in ids or dep['experiment'] == r['id']:
                raise ValueError('Unknown/self experiment dependency')
            if dep['stage'] not in {'preparation', 'execution', 'analysis'} or not dep['reason']:
                raise ValueError('Invalid experiment dependency')
            if dep['requirement'] not in {'evidence', 'analysis', 'accepted', 'successful_acceptance'}:
                raise ValueError('Invalid experiment requirement')
        for b in r['blocks']:
            if not BLOCK_ID.fullmatch(b['id']) or b['stage'] not in {'preparation', 'execution', 'analysis'} or not b['reason']:
                raise ValueError('Invalid Block dependency')
            if not b['delivery_note'] or type(b['delivery_confirmed']) is not bool:
                raise ValueError('Block delivery observation required')
        budget = r.get('time_budget')
        legacy_runtime = budget is None or (
            isinstance(budget, dict) and budget.get('legacy_unrecorded') is True)
        for attempt in r['attempts']:
            if not attempt['run_id'] or not attempt['scope'] or not attempt['evidence']:
                raise ValueError('Run attempt requires identity, scope and evidence')
            validate_attempt_runtime(attempt, legacy_record=legacy_runtime)
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


def _finite_seconds(value, label, *, positive=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0 or (positive and value == 0)):
        raise ValueError('Invalid ' + label)


def _evidence_list(value, label):
    if not isinstance(value, list):
        raise ValueError('Invalid ' + label + ' evidence')
    for ref in value:
        if not isinstance(ref, dict) or not ref.get('label') or not ref.get('path'):
            raise ValueError('Invalid ' + label + ' evidence')


def validate_time_budget(record):
    budget = record.get('time_budget')
    if budget is None:
        return
    if not isinstance(budget, dict):
        raise ValueError('Missing experiment time budget: ' + record['id'])
    status = budget.get('estimate_status')
    seconds = budget.get('estimated_seconds')
    if status not in ESTIMATE_STATUSES or not budget.get('scope') or not budget.get('basis'):
        raise ValueError('Invalid experiment time estimate: ' + record['id'])
    if status == 'estimated':
        _finite_seconds(seconds, 'estimated seconds', positive=True)
        if budget.get('calculation') not in (None, 'cache_miss_serial'):
            raise ValueError('Estimate must use cache-miss serial calculation: ' + record['id'])
    elif seconds is not None:
        raise ValueError('Unrecorded or non-applicable estimate must not contain seconds: ' + record['id'])
    if status == 'not_recorded' and budget.get('legacy_unrecorded') is not True:
        raise ValueError('Only a pre-existing estimate may be unrecorded: ' + record['id'])
    if status != 'not_recorded' and budget.get('legacy_unrecorded') is True:
        raise ValueError('Legacy estimate marker requires not_recorded status: ' + record['id'])
    if status == 'not_applicable' and record['execution']['state'] != 'not_required':
        raise ValueError('Non-applicable estimate requires no GPU run: ' + record['id'])


def validate_attempt_runtime(attempt, legacy_record=False):
    runtime = attempt.get('runtime')
    if not isinstance(runtime, dict):
        if runtime is None:
            return
        raise ValueError('Run attempt requires runtime and cache status: ' + attempt['run_id'])
    if type(runtime.get('job_started')) is not bool:
        raise ValueError('Run attempt requires job_started: ' + attempt['run_id'])
    estimate_status = runtime.get('estimate_status')
    estimate_seconds = runtime.get('estimated_seconds')
    if estimate_status not in ATTEMPT_ESTIMATE_STATUSES:
        raise ValueError('Invalid run estimate status: ' + attempt['run_id'])
    if estimate_status == 'recorded_before_start':
        _finite_seconds(estimate_seconds, 'run estimated seconds', positive=True)
        if not runtime.get('estimate_basis') or not runtime.get('estimate_scope'):
            raise ValueError('Run estimate needs basis and scope: ' + attempt['run_id'])
    elif estimate_seconds is not None:
        raise ValueError('Unrecorded run estimate must not contain seconds: ' + attempt['run_id'])
    if (estimate_status == 'not_recorded_before_start'
            and runtime.get('legacy_unrecorded') is not True and not legacy_record):
        raise ValueError('Only a pre-existing run may lack a frozen estimate: ' + attempt['run_id'])
    if estimate_status != 'not_recorded_before_start' and runtime.get('legacy_unrecorded') is True:
        raise ValueError('Legacy runtime marker requires an unrecorded estimate: ' + attempt['run_id'])
    actual_status = runtime.get('actual_status')
    actual_seconds = runtime.get('actual_seconds')
    if actual_status not in ACTUAL_STATUSES:
        raise ValueError('Invalid actual runtime status: ' + attempt['run_id'])
    if actual_status == 'recorded':
        _finite_seconds(actual_seconds, 'actual seconds')
        if not runtime.get('actual_basis') or not runtime.get('actual_scope'):
            raise ValueError('Recorded runtime needs basis and scope: ' + attempt['run_id'])
        runtime_evidence = runtime.get('evidence')
        if legacy_record and not runtime_evidence:
            runtime_evidence = attempt.get('evidence')
        _evidence_list(runtime_evidence, 'runtime')
        if not runtime_evidence:
            raise ValueError('Recorded runtime needs evidence: ' + attempt['run_id'])
        if not runtime['job_started']:
            raise ValueError('Recorded runtime requires a started job: ' + attempt['run_id'])
    elif actual_seconds is not None:
        raise ValueError('Unrecorded runtime must not contain seconds: ' + attempt['run_id'])
    elif not runtime.get('actual_basis') or not runtime.get('actual_scope'):
        raise ValueError('Unrecorded runtime needs an explanation and scope: ' + attempt['run_id'])
    if actual_status == 'not_recorded' and not runtime['job_started']:
        raise ValueError('Unstarted job cannot have missing actual runtime: ' + attempt['run_id'])
    if not runtime['job_started'] and actual_status != 'not_applicable':
        raise ValueError('Unstarted job must have non-applicable runtime: ' + attempt['run_id'])
    if actual_status == 'not_applicable' and runtime['job_started']:
        raise ValueError('Started job cannot have non-applicable runtime: ' + attempt['run_id'])
    for field in ('queue_seconds', 'return_seconds'):
        value = runtime.get(field)
        if value is not None:
            _finite_seconds(value, field)

    cache = runtime.get('cache')
    if cache is None and legacy_record:
        return
    if not isinstance(cache, dict) or cache.get('status') not in CACHE_STATUSES or not cache.get('summary'):
        raise ValueError('Run attempt requires cache observation status: ' + attempt['run_id'])
    counts = cache.get('counts')
    if not isinstance(counts, dict):
        raise ValueError('Invalid cache counts: ' + attempt['run_id'])
    if cache['status'] == 'observed':
        _evidence_list(cache.get('evidence'), 'cache')
        if not runtime['job_started'] or not cache['evidence'] or not counts:
            raise ValueError('Observed cache statistics need counts and evidence: ' + attempt['run_id'])
        for layer, values in counts.items():
            if not layer or not isinstance(values, dict) or not values:
                raise ValueError('Invalid cache layer counts: ' + attempt['run_id'])
            for state, count in values.items():
                if state not in {'hit', 'miss', 'not_applicable', 'disabled'}:
                    raise ValueError('Invalid cache state: ' + attempt['run_id'])
                if type(count) is not int or count < 0:
                    raise ValueError('Invalid cache count: ' + attempt['run_id'])
    elif counts:
        raise ValueError('Unavailable cache statistics must not contain counts: ' + attempt['run_id'])
    if cache['status'] == 'not_applicable' and runtime['job_started']:
        raise ValueError('Started job cannot have non-applicable cache: ' + attempt['run_id'])
    if cache['status'] == 'not_recorded' and not runtime['job_started']:
        raise ValueError('Unstarted job cannot have missing cache statistics: ' + attempt['run_id'])


def time_summary(record):
    """Summarize the full registered estimate scope and every started attempt."""
    budget = record.get('time_budget') or {}
    estimate_status = budget.get('estimate_status', 'not_recorded')
    attempts = [a.get('runtime') for a in record['attempts']]
    missing_runtime = sum(not isinstance(a, dict) for a in attempts)
    started = [a for a in attempts if isinstance(a, dict) and a.get('job_started') is True]
    recorded = [a for a in started if a.get('actual_status') == 'recorded']
    actual_seconds = sum(a['actual_seconds'] for a in recorded)
    missing_actual = len(started) - len(recorded) + missing_runtime
    missing_cache = sum(not isinstance(a.get('cache'), dict)
                        or a['cache'].get('status') != 'observed' for a in started) + missing_runtime
    scope_complete = record['execution']['state'] == 'completed'
    deviation_seconds = deviation_ratio = None
    if estimate_status == 'not_applicable':
        match_status = 'not_applicable'
    elif estimate_status != 'estimated':
        match_status = 'estimate_not_recorded'
    elif budget.get('scope') != record['scope']:
        match_status = 'estimate_scope_mismatch'
    elif budget.get('calculation') != 'cache_miss_serial':
        match_status = 'estimate_basis_unconfirmed'
    elif not scope_complete:
        match_status = 'scope_incomplete'
    elif not started and not missing_runtime:
        match_status = 'actual_incomplete'
    elif missing_actual:
        match_status = 'actual_incomplete'
    elif missing_cache:
        match_status = 'cache_incomplete'
    else:
        deviation_seconds = actual_seconds - budget['estimated_seconds']
        deviation_ratio = deviation_seconds / budget['estimated_seconds']
        if abs(deviation_ratio) <= MATCH_TOLERANCE:
            match_status = 'close'
        elif deviation_ratio > 0:
            match_status = 'over'
        else:
            match_status = 'under'
    return {
        'estimate_status': estimate_status,
        'estimated_seconds': budget.get('estimated_seconds'),
        'estimate_scope': budget.get('scope') or '未记录',
        'estimate_basis': budget.get('basis') or '未记录',
        'estimate_calculation_confirmed': budget.get('calculation') == 'cache_miss_serial',
        'scope_complete': scope_complete,
        'started_attempts': len(started),
        'unstructured_attempts': missing_runtime,
        'recorded_actual_attempts': len(recorded),
        'missing_actual_attempts': missing_actual,
        'missing_cache_attempts': missing_cache,
        'actual_seconds': actual_seconds if recorded else None,
        'match_status': match_status,
        'deviation_seconds': deviation_seconds,
        'deviation_ratio': deviation_ratio,
    }


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
    pending_candidates = {
        config['path']
        for record in records
        if canonical_state('preparation', record.get('preparation', {}).get('state')) in {
                'draft', 'preparing', 'ongoing'}
        for config in record.get('configs', [])
        if config['role'] == 'candidate' and not resolve(root, canonical, config['path']).exists()
    }
    missing = [r['path'] for r in references
               if r['path'] not in pending_candidates
               and not resolve(root, canonical, r['path']).exists()]
    if missing:
        raise ValueError('Missing sources: ' + ', '.join(sorted(set(missing))))
    return sum(r['path'] not in pending_candidates for r in references)


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
