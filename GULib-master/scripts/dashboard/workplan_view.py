"""Deterministic local Work Plan views from experiment records and explicit dependencies."""
from __future__ import annotations
import argparse
import html
import json
import os
from pathlib import Path
from urllib.parse import quote
import yaml
from scripts.dashboard import workplan_model as model

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'self/research'
STAGE_NAMES = {'preparation': '创建与准备', 'execution': '运行', 'analysis': '分析', 'decision': '科学决定'}
FAMILIES = {'main': 'GU 主实验', 'if': 'IF 与数值验证', 'im': 'IM', 'baseline': '共同参照', 'shared': '跨实验分析', 'training-diagnostic': '训练诊断'}


def esc(text):
    return html.escape(str(text), quote=True)


class Sources:
    def __init__(self, root, canonical):
        self.root, self.canonical = root.resolve(), canonical.resolve()

    def resolve(self, path):
        return model.resolve(self.root, self.canonical, path)

    def href(self, path, page):
        target = self.resolve(path)
        if target.anchor.casefold() != page.anchor.casefold():
            return target.as_uri()
        return quote(Path(os.path.relpath(target, page.parent)).as_posix(), safe='/.:')

    def anchor(self, ref, page):
        return f'<a href="{self.href(ref["path"], page)}">{esc(ref["label"])} ↗</a>'


def badge(stage, state):
    state = model.canonical_state(stage, state)
    return f'<span class="badge {esc(state)}">{esc(model.STATES[stage][state])}</span>'


def shell(title, body):
    style = Path(__file__).with_name('research.css').read_text(encoding='utf-8')
    script = Path(__file__).with_name('research.js').read_text(encoding='utf-8')
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{style}</style></head><body>{body}<script>{script}</script></body></html>\n'


def nav(prefix=''):
    return f'<nav class="top"><a class="brand" href="{prefix}index.html">OpenGU <span>/ Work Plan</span></a><div><a href="{prefix}index.html#experiments">实验总表</a><a href="{prefix}index.html#dependencies">依赖关系</a><a href="{prefix}runbook.html">运行流程</a><a href="{prefix}catalog.html">配置目录</a></div></nav>'


def references(refs, sources, page):
    return '<div class="sources">' + ''.join(sources.anchor(r, page) for r in {item['path']: item for item in refs}.values()) + '</div>'


def blocker_html(record, records, sources, page):
    deps = model.dependencies(record, records, sources.canonical)
    if not deps:
        return '<p class="muted">未登记实验或开发依赖。正式运行仍需执行准备检查。</p>'
    rows = []
    for dep in deps:
        label = 'Block' if dep['kind'] == 'block' else '实验'
        link = sources.anchor({'label': dep['id'], 'path': f'.workblock/items/{dep["id"]}/WORKITEM.md'}, page) if dep['kind'] == 'block' else f'<a href="{dep["id"]}.html">{dep["id"]}</a>'
        rows.append(f'<tr><td>{label} {link}</td><td>{STAGE_NAMES[dep["stage"]]}</td><td>{esc(dep["reason"])}</td><td>{esc(dep["status"])}</td><td class="{"good" if dep["resolved"] else "warn"}">{"已满足所述条件" if dep["resolved"] else "尚未满足"}</td></tr>')
    return '<div class="table-scroll"><table><thead><tr><th>依赖对象</th><th>约束阶段</th><th>原因</th><th>当前记录</th><th>判断</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'


def seconds_text(value):
    return '未记录' if value is None else f'{value:,.2f} 秒'


def cache_counts_text(counts):
    if not counts:
        return '未记录'
    return '；'.join(
        str(layer) + '：' + ' / '.join(f'{state} {count}' for state, count in values.items())
        for layer, values in counts.items())


def time_budget_section(record, sources, page):
    summary = model.time_summary(record)
    state = summary['match_status']
    match_names = {
        'not_applicable': '无需 GPU 作业',
        'estimate_not_recorded': '估时未记录，暂不计算偏差',
        'estimate_scope_mismatch': '估时范围与当前实验不一致，暂不计算偏差',
        'estimate_basis_unconfirmed': '估算口径待确认，暂不计算偏差',
        'scope_incomplete': '范围未完成，暂不计算偏差',
        'actual_incomplete': (f'有 {summary["unstructured_attempts"]} 次历史尝试缺少 runtime 元数据，暂不计算偏差'
                              if summary['unstructured_attempts'] else
                              '暂无结构化已启动运行尝试，暂不计算偏差' if not summary['started_attempts'] else
                              f'有 {summary["missing_actual_attempts"]} 次已启动作业缺少实际耗时，暂不计算偏差'),
        'cache_incomplete': f'有 {summary["missing_cache_attempts"]} 次已启动作业缺少 Cache 统计，暂不计算偏差',
        'close': '接近估时（偏差在 ±20% 内）',
        'over': '超过估时',
        'under': '低于估时',
    }
    if summary['deviation_seconds'] is None:
        deviation = match_names[state]
    else:
        seconds = summary['deviation_seconds']
        ratio = summary['deviation_ratio']
        deviation = f'{match_names[state]}：{seconds:+,.2f} 秒（{ratio:+.1%}）'
    if summary['started_attempts'] or summary['unstructured_attempts']:
        actual = (f'{seconds_text(summary["actual_seconds"])}；记录中确认已启动 {summary["started_attempts"]} 次，'
                  f'其中 {summary["recorded_actual_attempts"]} 次有实际耗时')
        if summary['unstructured_attempts']:
            actual += f'；{summary["unstructured_attempts"]} 次历史尝试未记录 runtime'
    else:
        actual = '本页未登记可累计的作业时间；已有执行结果见实验分析。'
    scope_label = '完整' if summary['scope_complete'] else model.STATES['execution'][record['execution']['state']]
    body = '<details class="timing"><summary>时间记录 · 预估 ' + esc(seconds_text(summary['estimated_seconds'])) + ' · 实耗 ' + esc(seconds_text(summary['actual_seconds'])) + '</summary>'
    body += '<p>' + esc(actual) + '</p><p>' + esc(deviation) + '</p>'
    body += '<dl><dt>估算范围</dt><dd>' + esc(summary['estimate_scope']) + '</dd><dt>估算依据</dt><dd>' + esc(summary['estimate_basis']) + '</dd><dt>运行覆盖</dt><dd>' + esc(scope_label) + '</dd></dl>'
    body += '<p class="muted">实耗仅累计本页绑定且有起止耗时的作业，含失败和重跑；排队、回传单列。缺少时间不表示未执行。完整同范围且时间与 Cache 证据齐备时计算偏差，±20% 为接近。</p></details>'
    return body


def config_preview(config, sources, page, allow_unmaterialized_candidate=False):
    path = sources.resolve(config['path'])
    if not path.exists():
        if config['role'] == 'candidate' and allow_unmaterialized_candidate:
            return (f'<details class="yaml"><summary>{esc(path.name)} '
                    '<span>候选配置待创建</span></summary>'
                    f'<p class="path">{esc(config["path"])}</p>'
                    '<p class="muted">实验仍在草拟或准备阶段；配置文件创建后会自动出现在此处。</p></details>')
        raise ValueError('Missing experiment config: ' + config['path'])
    try:
        parsed = yaml.safe_load(path.read_text(encoding='utf-8'))
    except yaml.YAMLError as exc:
        raise ValueError('Invalid YAML: ' + config['path']) from exc
    if not isinstance(parsed, dict):
        raise ValueError('Experiment config must be a mapping: ' + config['path'])
    role = {'current': '现行文件', 'reference': '辅助配置', 'historical': '历史配置', 'candidate': '候选 / 不代表已执行'}[config['role']]
    return f'<details class="yaml"><summary>{esc(path.name)} <span>{role}</span></summary><p>{sources.anchor(config, page)}</p><p class="path">{esc(config["path"])}</p><pre>{esc(yaml.safe_dump(parsed, allow_unicode=True, sort_keys=False))}</pre></details>'


def submission_facts(attempt, sources):
    """Read only explicitly linked controller receipts, never infer dates from run IDs."""
    submitted, recipe, ref = attempt.get('submitted_at'), attempt.get('recipe'), None
    for item in attempt['evidence']:
        if not item['path'].startswith('.syncmate/controller/'):
            continue
        path = sources.resolve(item['path'])
        if not path.exists():
            continue
        controller = json.loads(path.read_text(encoding='utf-8'))
        job = (controller.get('watch') or {}).get('job') or {}
        receipt = job.get('receipt') or {}
        submitted = submitted or receipt.get('submitted_at')
        recipe = recipe or job.get('recipe') or controller.get('recipe')
        ref = item
        break
    return submitted or '未记录', recipe or '未记录', ref


def attempt_rows(record, sources, page):
    if not record['attempts']:
        return '<p class="muted">本页未逐次登记运行；已交付结果见上方实验分析。提交时间与作业耗时未登记，不影响已有交付事实。</p>'
    body = '<div class="table-scroll"><table class="runs"><thead><tr><th>运行</th><th>提交时间</th><th>状态</th><th>作业起止 / 耗时</th><th>记录与证据</th></tr></thead><tbody>'
    for a in record['attempts']:
        rt = a.get('runtime') or {}
        submitted, recipe, ref = submission_facts(a, sources)
        state = a.get('state', a.get('status', 'unknown'))
        state = {'completed': '完成', 'verified': '已核验', 'running': '运行中', 'failed': '失败', 'pending': '待运行'}.get(state, state)
        elapsed = seconds_text(rt.get('actual_seconds'))
        if rt.get('actual_seconds') is not None:
            total = int(rt['actual_seconds']); elapsed = f'{total // 3600}小时{total % 3600 // 60}分{total % 60}秒' if total >= 3600 else f'{total // 60}分{total % 60}秒'
        if rt.get('job_started') is False:
            elapsed = '未启动'
        recipe_path = 'scripts/syncmate/recipes/' + recipe + '.yaml'
        recipe_link = sources.anchor({'label': recipe, 'path': recipe_path}, page) if recipe != '未记录' and sources.resolve(recipe_path).exists() else esc(recipe)
        timing = '<br><small>' + esc(rt.get('started_at', '起始未记录')) + '<br>→ ' + esc(rt.get('finished_at', '结束未记录')) + '</small>'
        body += '<tr><td class="run-name">' + esc(a['run_id']) + '<small>Recipe · ' + recipe_link + '</small>' + '</td><td>' + esc(submitted) + '</td><td>' + esc(state) + '</td><td>' + esc(elapsed) + timing + '</td><td><details><summary>详情与证据</summary><p>' + esc(a['scope']) + '</p>'
        body += '<p class="path">Recipe：' + esc(recipe) + '</p>'
        if ref:
            body += '<p>提交时间来源：' + sources.anchor(ref, page) + '（保留源记录时区）</p>'
        body += '<p>' + esc(rt.get('actual_basis', '此运行未登记作业起止耗时。')) + '</p>'
        body += '<p>排队 ' + esc(seconds_text(rt.get('queue_seconds'))) + ' · 回传 ' + esc(seconds_text(rt.get('return_seconds'))) + '</p>'
        cache = rt.get('cache') or {}
        body += '<p>Cache：' + esc(cache.get('summary', '未记录')) + '</p>'
        if cache.get('counts'):
            body += '<p>' + esc(cache_counts_text(cache['counts'])) + '</p>'
        refs = list({r['path']: r for r in a['evidence'] + rt.get('evidence', []) + cache.get('evidence', [])}.values())
        body += references(refs, sources, page)
        m = a.get('manifest', {})
        body += '<p class="path">代码版本：' + esc(a.get('commit') or m.get('commit', '未记录')) + '</p>'
        if m:
            body += '<p class="path">Manifest SHA-256：' + esc(m['sha256']) + ' · 完成条件 ' + esc(m['completed']) + '</p>'
        body += '</details></td></tr>'
    return body + '</tbody></table></div>'


def parameter_preview(config, sources):
    path = sources.resolve(config['path'])
    if not path.exists():
        return ''
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    labels = {'dataset_refs': '数据集', 'selector_refs': '选择策略', 'unlearning_refs': '遗忘 / 重训练', 'seeds': '训练 seed', 'random_selector_seeds': 'Random seed', 'im_selector_seeds': 'IM seed', 'budget_ratios': '删除比例'}
    rows = []
    for key, label in labels.items():
        value = data.get(key)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        text = '、'.join(Path(str(x)).stem if key.endswith('_refs') else str(x) for x in values)
        value_html = esc(text) if len(text) < 150 else '<details><summary>' + str(len(values)) + ' 项配置 · 展开</summary>' + esc(text) + '</details>'
        rows.append('<dt>' + esc(label) + '</dt><dd>' + value_html + '</dd>')
    return '<dl class="parameters">' + ''.join(rows) + '</dl>' if rows else ''


def experiment_groups(record, sources):
    """Group by explicit config/run identities; filenames never establish execution."""
    documents = {}
    for config in record['configs']:
        path = sources.resolve(config['path'])
        documents[config['path']] = yaml.safe_load(path.read_text(encoding='utf-8')) if path.exists() else {}
    groups = []
    used = set()
    for config in record['configs']:
        data = documents[config['path']] or {}
        if data.get('kind') != 'experiment' or config['role'] not in {'current', 'candidate'}:
            continue
        recipes = [c for c in record['configs'] if (documents[c['path']] or {}).get('config_path') == config['path']]
        recipe_ids = {(documents[c['path']] or {}).get('id') for c in recipes} - {None}
        runs = {(documents[c['path']] or {}).get('run_identity', {}).get('run_id') for c in recipes} - {None}
        attempts = []
        for attempt in record['attempts']:
            _, recipe, _ = submission_facts(attempt, sources)
            match = recipe in recipe_ids or attempt['run_id'] in runs or attempt.get('config_path') == config['path']
            manifest = attempt.get('manifest')
            if not match and manifest:
                path = sources.resolve(manifest['path'])
                if path.exists():
                    match = json.loads(path.read_text(encoding='utf-8')).get('config_path') == config['path']
            if match:
                attempts.append(attempt)
        if config['role'] == 'candidate' and not attempts:
            continue
        results = []
        for ref in {item['path']: item for item in record['analysis']['evidence']}.values():
            if not ref['path'].startswith('self/research/analyses/') or not ref['path'].endswith('.json'):
                continue
            path = sources.resolve(ref['path'])
            if not path.exists():
                continue
            result = json.loads(path.read_text(encoding='utf-8'))
            if result.get('config_path') == config['path'] or result.get('run_id') in {a['run_id'] for a in attempts}:
                results.append((ref, result))
            for case in result.get('cases', []):
                identity = case.get('run', {})
                if identity.get('config_path') == config['path'] or identity.get('run_id') in {a['run_id'] for a in attempts}:
                    results.append((ref, case))
        groups.append(dict(config=config, recipes=recipes, attempts=attempts, results=results,
                           cells=[documents[c['path']]['logical_cells'] for c in recipes if 'logical_cells' in documents[c['path']]]))
        used.update([config['path'], *[c['path'] for c in recipes]])
    return groups, [c for c in record['configs'] if c['path'] not in used]


def group_title(config):
    stem = Path(config['path']).stem
    if stem.startswith('validation_'):
        return stem.removeprefix('validation_').upper() + ' 固定参数验证'
    if stem.startswith('observer_candidates_'):
        return stem.removeprefix('observer_candidates_').upper() + ' 参数校准'
    return config['label'].removesuffix('.yaml')


def group_view(group, sources, page, index):
    config = group['config']
    attempts = group['attempts']
    states = [a.get('state', a.get('status')) for a in attempts]
    status = '已完成' if states and all(x in {'completed', 'verified'} for x in states) else '有运行记录' if states else '未关联运行记录'
    count = ' · ' + str(group['cells'][0]) + ' 格' if group['cells'] and len(set(group['cells'])) == 1 else ''
    body = '<article class="experiment-group" id="group-' + str(index) + '"><h3>' + esc(group_title(config)) + '<span class="group-status">' + esc(count + ' · ' + status) + '</span></h3>'
    if attempts:
        body += '<p>' + esc(attempts[-1]['scope']) + '</p>'
    else:
        body += '<p class="muted">已登记实验配置；本页尚未关联到具体运行。</p>'
    body += '<h4>分析结果</h4>'
    if not group['results']:
        body += '<p class="muted">本组暂无单独关联的结构化分析，已有结论见页面下方总体分析与证据。</p>'
    for ref, result in group['results']:
        if result.get('numerical_gate'):
            body += '<p>数值检查：' + esc({'passed': '通过', 'failed': '未通过'}.get(result['numerical_gate'], result['numerical_gate'])) + '</p>'
        if result.get('methods') and isinstance(result['methods'], dict):
            for method, finding in result['methods'].items():
                frozen = finding.get('frozen_parameters')
                if frozen:
                    body += '<p>' + esc(method) + ' · ' + esc({'stable': '数值稳定'}.get(finding.get('status'), finding.get('status', '未记录'))) + ' · 固定参数 ' + esc(', '.join(str(k) + '=' + str(v) for k, v in frozen.items())) + '</p>'
        utility = result.get('utility', {})
        if utility:
            body += '<div class="table-scroll"><table><caption>原图评价 · F1（0–1）</caption><thead><tr><th>请求</th><th>GIF</th><th>IDEA</th><th>Retrain</th><th>GIF−Retrain</th></tr></thead><tbody>'
            for seed, values in utility.items():
                nums = [values.get('GIF', {}).get('f1'), values.get('IDEA', {}).get('f1'), values.get('retrain_f1'), values.get('GIF', {}).get('f1_minus_retrain')]
                body += '<tr><td>' + esc(seed) + '</td>' + ''.join('<td>' + ('未记录' if v is None else f'{v:.6f}') + '</td>' for v in nums) + '</tr>'
            body += '</tbody></table></div>'
        body += references([ref], sources, page)
    body += '<h4>运行记录</h4>' + attempt_rows({'attempts': attempts}, sources, page)
    body += '<details class="group-files"><summary>实验参数与技术文件</summary>' + parameter_preview(config, sources)
    body += '<h4>实验配置</h4>' + config_preview(config, sources, page)
    if group['recipes']:
        body += '<h4>提交 Recipe · 启动上面的实验配置</h4>' + ''.join(config_preview(c, sources, page) for c in group['recipes'])
    return body + '</details></article>'


def sheet_page(r, records, sources, page):
    body = '<main class="shell experiment-sheet">' + nav('../')
    body += f'<header><p class="eyebrow">{r["id"]} / {FAMILIES[r["family"]]}</p><h1>{esc(r["title"])}</h1><div class="status-line">' + ''.join('<span>' + name + ' ' + badge(key, r[key]['state']) + '</span>' for key, name in STAGE_NAMES.items()) + '</div></header>'
    groups, supporting = experiment_groups(r, sources)
    grouped_runs = {a['run_id'] for g in groups for a in g['attempts']}
    body += '<nav class="sheet-nav"><a href="#definition">研究问题</a><a href="#groups">实验组</a><a href="#analysis">总体分析</a><a href="#archive">历史与依赖</a></nav>'
    body += '<section id="definition"><h2>实验定义</h2><p class="question-text">' + esc(r['question']) + '</p>'
    body += '<p class="execution-note">' + esc(r['execution']['note']) + '</p></section>'
    body += '<section id="groups"><h2>实验组</h2>'
    if groups:
        body += ''.join(group_view(g, sources, page, i) for i, g in enumerate(groups, 1))
    else:
        body += '<p class="muted">本页没有现行实验配置组；已有分析及历史来源保留在下方。</p>'
    if supporting:
        body += '<details><summary>准备、候选与历史文件（不计作已运行实验）</summary>'
        body += ''.join(config_preview(c, sources, page, model.canonical_state('preparation', r['preparation']['state']) in {'draft','preparing','ongoing'}) for c in supporting)
        body += '</details>'
    body += '</section>'
    body += '<section id="analysis"><h2>总体分析与决定</h2><p>' + esc(r['analysis']['note']) + '</p>'
    published = r.get('published_analysis') or {}
    for point in published.get('analysis', {}).get('highlights', []):
        body += '<p class="finding">' + esc(point) + '</p>'
    for table in ([] if any(g['results'] for g in groups) else published.get('analysis', {}).get('tables', [])):
        body += '<div class="table-scroll"><table><caption>' + esc(table['caption']) + '</caption><thead><tr>' + ''.join('<th>' + esc(x) + '</th>' for x in table['columns']) + '</tr></thead><tbody>'
        body += ''.join('<tr>' + ''.join('<td>' + esc(x) + '</td>' for x in row) + '</tr>' for row in table['rows']) + '</tbody></table></div>'
    body += references(r['analysis']['evidence'], sources, page)
    body += '<p class="decision-line"><strong>科学决定</strong> · ' + badge('decision', r['decision']['state']) + ' ' + esc(r['decision']['note']) + '</p>'
    body += references(r['decision']['evidence'], sources, page)
    body += '<p class="next-inline"><strong>下一步</strong> · ' + esc(r['next_step']) + '</p>'
    if published:
        body += '<details><summary>分析范围与来源</summary><p>' + esc(published['scope']) + '</p><p>记录日期 ' + esc(published['recorded_at']) + '</p>'
        body += sources.anchor({'label': '版本化分析记录', 'path': f'self/research/analyses/{r["id"]}.json'}, page)
        for a in published['attempts']:
            body += '<p class="path">' + esc(a['run_id']) + ' · ' + esc(a.get('commit') or a.get('manifest', {}).get('commit', '版本见原始证据')) + '</p>'
        body += '</details>'
    body += '</section><section id="runs">'
    remaining = [a for a in r['attempts'] if a['run_id'] not in grouped_runs]
    if remaining:
        body += '<details><summary>其他历史运行（尚未关联到上方实验组）</summary>' + attempt_rows({'attempts': remaining}, sources, page) + '</details>'
    body += time_budget_section(r, sources, page) + '</section>'
    body += '<section id="archive"><details><summary>历史、依赖与来源</summary>' + blocker_html(r, records, sources, page)
    body += '<ol class="timeline">'
    for event in reversed(r['history']):
        body += '<li><time>' + esc(event['at']) + '</time><p>' + esc(event['note']) + '</p>' + references(event['evidence'], sources, page) + '</li>'
    body += '</ol>' + references(r['sources'], sources, page) + '</details></section>'
    body += '<footer>记录核对日期 ' + esc(r['reviewed_at']) + '</footer></main>'
    return shell(r['id'] + ' · ' + r['title'], body)


def diagram(records, canonical, prefix='experiments/'):
    rows = [(r, model.dependencies(r, records, canonical)) for r in records]
    rows = [(r, deps) for r, deps in rows if deps]
    height = 100 + sum(len(deps) * 56 + 30 for _, deps in rows)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 {height}" role="img" aria-labelledby="map-title"><title id="map-title">实验单向引用依赖；橙色为尚未满足</title>', '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#82919a"/></marker></defs><rect width="1040" height="100%" fill="#10191e"/><style>text{font-family:Microsoft YaHei,sans-serif}a:hover rect{stroke:#fff}</style><text x="24" y="36" fill="#d6e6e5" font-size="18">实验 → 所依赖的实验结果或开发 Block</text>']
    y = 66
    for r, deps in rows:
        svg.append(f'<a href="{prefix}{r["id"]}.html"><rect x="24" y="{y}" width="290" height="42" rx="5" fill="#1e333a" stroke="#739e9f"/><text x="36" y="{y+26}" fill="#edf4ef" font-size="14">{r["id"]} · {esc(r["title"][:16])}</text></a>')
        for i, d in enumerate(deps):
            dy = y + i * 56
            color = '#7fc7b0' if d['resolved'] else '#edb76b'
            svg.append(f'<path d="M314 {y+21} H340 V{dy+21} H410" stroke="#82919a" fill="none" marker-end="url(#arrow)"/><rect x="416" y="{dy}" width="596" height="42" rx="5" fill="#18272e" stroke="{color}"/><text x="429" y="{dy+17}" fill="{color}" font-size="13">{"Block" if d["kind"]=="block" else "实验"} {d["id"]} · {STAGE_NAMES[d["stage"]]} · {"已满足" if d["resolved"] else "未满足"}</text><text x="429" y="{dy+34}" fill="#c4d0d2" font-size="12">{esc(d["reason"][:44])}</text>')
        y += len(deps) * 56 + 30
    return ''.join(svg) + '</svg>'


def index_page(frame, records, sources, page):
    body = '<main class="shell">' + nav() + '<header class="hero"><div><p class="eyebrow">实验过程与研究进度</p><h1>Work Plan</h1><p class="lead">创建、运行、分析。<br>从实验问题进入，查看当前证据与下一步。</p></div><div class="numbers">'
    body += ''.join(f'<div><strong>{sum(r["category"]==k for r in records)}</strong><span>{label}</span></div>' for k, label in [('active', '当前维护'), ('planned', '待准备'), ('history', '历史与已交付')])
    body += f'</div></header><p class="snapshot">来源核对 {frame["reviewed_at"]} · 页面为本地生成快照，运行实时监控见 SyncMate。</p><section id="experiments"><h2>实验总表</h2><div class="filters"><label>范围<select id="category"><option value="current">当前与待准备</option><option value="all">全部实验</option><option value="active">当前维护</option><option value="planned">待准备</option><option value="history">历史与已交付</option></select></label><label>研究组<select id="family"><option value="all">全部研究组</option>'
    body += ''.join(f'<option value="{k}">{v}</option>' for k, v in FAMILIES.items())
    body += '</select></label><label>工作视图<select id="view"><option value="all">全部进度</option><option value="blocked">存在未满足依赖</option><option value="run">待运行 / 待核对</option><option value="analysis">待分析 / 待决定</option></select></label><label class="search">搜索<input id="search" type="search" placeholder="EXP-032、YAML、研究问题"></label><button id="clear">重置</button></div><p id="count" role="status" aria-live="polite"></p><div class="table-scroll"><table class="experiment-table"><thead><tr><th>实验 / 定义</th><th>准备</th><th>运行</th><th>分析</th><th>依赖与下一步</th></tr></thead><tbody>'
    for r in sorted(records, key=lambda item: ({'active': 0, 'planned': 1, 'history': 2}[item['category']], item['id'])):
        unmet = [d for d in model.dependencies(r, records, sources.canonical) if not d['resolved']]
        views = ['blocked'] if unmet else []
        if r['execution']['state'] in {'pending', 'unknown', 'partial', 'failed', 'running'}:
            views.append('run')
        if r['execution']['state'] in {'completed', 'not_required'} and (r['analysis']['state'] != 'complete' or r['decision']['state'] == 'pending'):
            views.append('analysis')
        search = ' '.join([r['id'], r['title'], r['scope'], *[c['path'] for c in r['configs']]])
        body += f'<tr class="experiment" data-category="{r["category"]}" data-family="{r["family"]}" data-views="{" ".join(views)}" data-search="{esc(search)}"><td><a class="experiment-name" href="experiments/{r["id"]}.html"><small>{r["id"]}</small>{esc(r["title"])}</a><p>{esc(r["scope"])}</p></td>'
        for key in ['preparation', 'execution', 'analysis']:
            body += f'<td>{badge(key,r[key]["state"])}<p>{esc(r[key]["note"])}</p></td>'
        body += '<td>' + ''.join(f'<span class="dependency">{d["id"]} · {STAGE_NAMES[d["stage"]]}待满足</span>' for d in unmet) + f'<p>{esc(r["next_step"])}</p></td></tr>'
    body += '</tbody></table></div><p id="empty" hidden>没有匹配实验。请更换筛选条件。</p></section><section id="dependencies"><h2>实验依赖图</h2><p>从实验指向所需结果或开发交付。橙色表示尚未满足；点击左侧实验查看完整原因。</p><div class="map-scroll">' + diagram(records, sources.canonical) + '</div></section>'
    body += '<section><h2>研究问题</h2>' + ''.join('<details class="question"><summary>' + esc(t['question']) + '</summary>' + ''.join('<p>' + esc(p) + '</p>' for p in t['narrative']) + '</details>' for t in frame['topics']) + '</section><footer><p>Work Plan 拥有实验过程；Block 拥有开发变更。只读取实验明确引用的 Block，不枚举、同步或更新全体 Block。</p><a href="migration.html">查看实验归属整理与尚待交接项 →</a></footer></main>'
    return shell(frame['title'], body)


def catalog(root, records):
    groups = model.read_json(root / 'self/research/config_groups.json')
    roles = {c['path']: c['role'] for r in records for c in r['configs']}
    result = []
    for name, group in groups.items():
        folder = root / 'experiments/configs' / name
        if not folder.is_dir():
            raise ValueError('Missing config group: ' + name)
        for path in sorted(folder.rglob('*.yaml')):
            relative = path.relative_to(root).as_posix()
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
            result.append(dict(group, path=relative, label=path.name, role=roles.get(relative, '辅助 / 未单列为现行入口'), config_kind=data.get('kind', '专题定义') if isinstance(data, dict) else '未知'))
    unclassified = [p.name for p in (root / 'experiments/configs').iterdir() if p.is_dir() and p.name.startswith(('aagu', 'exp')) and p.name not in groups]
    if unclassified:
        raise ValueError('Unclassified experiment configuration groups: ' + ', '.join(unclassified))
    return result


def catalog_page(records, sources, page):
    rows = catalog(sources.root, records)
    body = '<main class="shell">' + nav() + f'<header><h1>配置目录</h1><p>{len(rows)} 份编号实验目录及 IM 目录中的 YAML。参数直接读取原文件；文件数量不是实验数量。</p></header><div class="table-scroll"><table><thead><tr><th>归属</th><th>文件</th><th>类型</th><th>用途</th></tr></thead><tbody>'
    for r in rows:
        body += '<tr><td>' + (f'<a href="experiments/{r["owner"]}.html">{r["owner"]}</a>' if r['kind'] == 'experiment' else esc(r['owner']) + ' 开发验证') + '</td><td>' + sources.anchor(r, page) + f'<p class="path">{esc(r["path"])}</p></td><td>{esc(r["config_kind"])}</td><td>{esc(r["role"])}</td></tr>'
    return shell('Work Plan · 配置目录', body + '</tbody></table></div></main>')


def document_page(title, filename):
    text = (SOURCE / filename).read_text(encoding='utf-8')
    body = '<main class="shell prose">' + nav() + f'<header><h1>{esc(title)}</h1></header>'
    in_code = False
    for line in text.splitlines():
        if line.startswith('```'):
            body += '</code></pre>' if in_code else '<pre><code>'
            in_code = not in_code
        elif in_code:
            body += esc(line) + '\n'
        elif line.startswith('## '):
            body += '<h2>' + esc(line[3:]) + '</h2>'
        elif line.startswith('# '):
            continue
        elif line.strip():
            body += '<p>' + esc(line) + '</p>'
    return shell(title, body + '</main>')


def outputs(frame, records, sources, directory):
    result = {directory / 'index.html': index_page(frame, records, sources, directory / 'index.html'),
              directory / 'diagram/experiment-dependencies.svg': diagram(records, sources.canonical, '../experiments/'),
              directory / 'catalog.html': catalog_page(records, sources, directory / 'catalog.html'),
              directory / 'runbook.html': document_page('实验运行流程', 'RUNBOOK.md'),
              directory / 'migration.html': document_page('实验归属整理', 'MIGRATION.md')}
    for r in records:
        path = directory / 'experiments' / f'{r["id"]}.html'
        result[path] = sheet_page(r, records, sources, path)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical-root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path, default=SOURCE)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--check-links', action='store_true')
    parser.add_argument('--verify-evidence', action='store_true')
    args = parser.parse_args(argv)
    try:
        frame, records = model.load(ROOT, args.canonical_root)
        sources = Sources(ROOT, args.canonical_root)
        if args.check_links:
            print('Source references:', model.check_links(frame, records, ROOT, sources.canonical))
        if args.verify_evidence:
            print('Explicit manifest / file hashes:', model.verify_manifests(records, ROOT, sources.canonical))
        generated = outputs(frame, records, sources, args.output_dir.resolve())
        for path, content in generated.items():
            if args.check:
                if not path.exists() or path.read_text(encoding='utf-8') != content:
                    raise ValueError('Stale generated output: ' + str(path))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
        print(('Checked' if args.check else 'Generated'), len(generated), 'Work Plan pages / SVG; no Block or execution writes')
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')
    return 0
