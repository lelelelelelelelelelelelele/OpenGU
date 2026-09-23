"""Deterministic local Work Plan views from experiment records and explicit dependencies."""
from __future__ import annotations
import argparse
import html
import os
from pathlib import Path
from urllib.parse import quote
import yaml
from scripts.dashboard import workplan_model as model

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'self/research'
STAGE_NAMES = {'preparation': '创建与准备', 'execution': '运行', 'analysis': '分析', 'decision': '科学决定'}
FAMILIES = {'main': 'GU 主实验', 'if': 'IF 与数值验证', 'im': 'IM', 'baseline': '共同参照', 'shared': '跨实验分析'}


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
    return '<div class="sources">' + ''.join(sources.anchor(r, page) for r in refs) + '</div>'


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
        'scope_incomplete': '范围未完成，暂不计算偏差',
        'actual_incomplete': ('暂无结构化已启动运行尝试，暂不计算偏差' if not summary['started_attempts']
                              else f'有 {summary["missing_actual_attempts"]} 次已启动作业缺少实际耗时，暂不计算偏差'),
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
    if summary['started_attempts']:
        actual = (f'{seconds_text(summary["actual_seconds"])}；已启动 {summary["started_attempts"]} 次，'
                  f'其中 {summary["recorded_actual_attempts"]} 次有实际耗时')
    else:
        actual = '暂无已启动 GPU 作业'
    scope_label = '完整' if summary['scope_complete'] else model.STATES['execution'][record['execution']['state']]
    rows = [
        ('预估耗时', seconds_text(summary['estimated_seconds']), summary['estimate_scope']),
        ('估算依据', 'Cache 未命中、按作业串行累计' if summary['estimate_status'] == 'estimated' else '未记录' if summary['estimate_status'] == 'not_recorded' else '不适用', summary['estimate_basis']),
        ('累计实际耗时', actual, '只累计已启动 GPU 作业；排队与回传时间单列，不计入实际耗时。'),
        ('范围完成状态', scope_label, '只有完整范围、完整实际耗时和 Cache 统计齐备时才计算偏差。'),
        ('估时偏差', deviation, '接近阈值为 ±20%；偏差 = 累计实际耗时 − 预估耗时。'),
    ]
    body = '<section class="time-budget"><h2>时间预算与实际耗时</h2><div class="table-scroll"><table><thead><tr><th>指标</th><th>结果</th><th>范围与口径</th></tr></thead><tbody>'
    body += ''.join(f'<tr><th>{esc(label)}</th><td>{esc(value)}</td><td>{esc(detail)}</td></tr>' for label, value, detail in rows)
    body += '</tbody></table></div>'
    if record['attempts']:
        body += '<h3>运行尝试</h3><div class="table-scroll"><table><thead><tr><th>Run</th><th>GPU 作业耗时</th><th>排队</th><th>回传</th><th>Cache 情况</th><th>证据</th></tr></thead><tbody>'
        for attempt in record['attempts']:
            runtime = attempt['runtime']
            if runtime['actual_status'] == 'recorded':
                elapsed = seconds_text(runtime['actual_seconds'])
            elif not runtime['job_started']:
                elapsed = '未启动'
            else:
                elapsed = '未记录'
            cache = runtime['cache']
            counts = cache_counts_text(cache['counts'])
            cache_text = esc(cache['summary'])
            if cache['status'] == 'observed':
                cache_text += '<br><small>' + esc(counts) + '</small>'
            refs = list({ref['path']: ref for ref in runtime.get('evidence', []) + cache.get('evidence', [])}.values())
            if not refs:
                refs = attempt['evidence']
            body += ('<tr><td>' + esc(attempt['run_id']) + '</td><td>' + esc(elapsed)
                     + '<br><small>' + esc(runtime['actual_basis']) + '</small></td><td>'
                     + esc(seconds_text(runtime.get('queue_seconds'))) + '</td><td>'
                     + esc(seconds_text(runtime.get('return_seconds'))) + '</td><td>'
                     + cache_text + '</td><td>' + references(refs, sources, page) + '</td></tr>')
        body += '</tbody></table></div>'
    return body + '</section>'


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
    role = {'current': '现行入口', 'reference': '辅助配置', 'historical': '历史配置', 'candidate': '候选 / 不代表已执行'}[config['role']]
    return f'<details class="yaml"><summary>{esc(path.name)} <span>{role}</span></summary><p>{sources.anchor(config, page)}</p><p class="path">{esc(config["path"])}</p><pre>{esc(yaml.safe_dump(parsed, allow_unicode=True, sort_keys=False))}</pre></details>'


def sheet_page(r, records, sources, page):
    body = '<main class="shell">' + nav('../') + f'<header><p class="eyebrow">{r["id"]} / {FAMILIES[r["family"]]}</p><h1>{esc(r["title"])}</h1><p class="lead">{esc(r["question"])}</p><p class="muted">核对日期 {r["reviewed_at"]} · 实验状态独立维护</p></header>'
    body += '<div class="stages">' + ''.join(f'<div><label>{name}</label>{badge(key, r[key]["state"])}<p>{esc(r[key]["note"])}</p></div>' for key, name in STAGE_NAMES.items()) + '</div>'
    body += '<section class="next"><h2>下一步</h2><p>' + esc(r['next_step']) + '</p></section>'
    body += time_budget_section(r, sources, page)
    body += '<section><h2>依赖与阻塞</h2>' + blocker_html(r, records, sources, page) + '<p class="muted">Block 状态是生成页面时的只读观察。交付状态与本实验所需能力同时确认后，才解除对应依赖；不会自动启动。</p></section>'
    body += '<section><h2>实验定义与 YAML</h2><p>' + esc(r['scope']) + '</p>'
    body += ''.join(config_preview(c, sources, page, model.canonical_state(
        'preparation', r['preparation']['state']) in {'draft', 'preparing', 'ongoing'})
                    for c in r['configs']) if r['configs'] else '<p class="muted">没有主线执行 YAML 绑定。分析项直接消费结果；待准备项先完成定义或软件交付。</p>'
    body += '</section><section><h2>运行尝试</h2>'
    if not r['attempts']:
        body += '<p class="muted">尚未在此逐次绑定 run_id。已有交付按下方来源报告阅读，不编造运行身份或重复计数。</p>'
    for attempt in r['attempts']:
        body += f'<article class="attempt"><h3>{esc(attempt["run_id"])}</h3><p>{esc(attempt["scope"])}</p>' + references(attempt['evidence'], sources, page)
        if attempt.get('manifest'):
            m = attempt['manifest']
            body += f'<details><summary>运行身份</summary><dl><dt>experiment_id</dt><dd>{esc(m["experiment_id"])}</dd><dt>代码版本</dt><dd>{esc(m["commit"])}</dd><dt>manifest SHA-256</dt><dd>{m["sha256"]}</dd><dt>完成条件</dt><dd>{m["completed"]}</dd></dl></details>'
        body += '</article>'
    body += references(r['execution']['evidence'], sources, page) + '</section>'
    for key in ['analysis', 'decision']:
        body += f'<section><h2>{STAGE_NAMES[key]}与证据</h2>{badge(key,r[key]["state"])}<p>{esc(r[key]["note"])}</p>' + references(r[key]['evidence'], sources, page) + '</section>'
    if r.get('published_analysis'):
        published = r['published_analysis']
        body += '<section><h2>已保存分析的范围与运行依据</h2><p>' + esc(published['scope']) + '</p>'
        body += '<p>记录日期 ' + esc(published['recorded_at']) + '；该范围与当前计划分别维护，历史结论不自动覆盖新增范围。</p>'
        body += sources.anchor({'label': '版本化分析记录', 'path': f'self/research/analyses/{r["id"]}.json'}, page)
        for attempt in published['attempts']:
            commit = attempt.get('commit') or attempt.get('manifest', {}).get('commit', '未记录；需查原始证据')
            body += '<p>' + esc(attempt['run_id']) + ' · SHA ' + esc(commit) + '</p>' + references(attempt['evidence'], sources, page)
        body += references(published['sources'], sources, page) + '</section>'
    body += '<section><h2>过程记录</h2><ol class="timeline">'
    for event in reversed(r['history']):
        body += f'<li><time>{esc(event["at"])}</time><p>{esc(event["note"])}</p>' + references(event['evidence'], sources, page) + '</li>'
    body += '</ol></section><footer><h2>定义与历史来源</h2>' + references(r['sources'], sources, page) + '<p>历史 WorkItem 保留原始定义、证据和开发交付；实验创建、运行与分析以本记录为入口。</p></footer></main>'
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
    body += '</select></label><label>工作视图<select id="view"><option value="all">全部进度</option><option value="blocked">存在未满足依赖</option><option value="run">待运行 / 待核对</option><option value="analysis">待分析 / 待决定</option></select></label><label class="search">搜索<input id="search" type="search" placeholder="AAGU-032、YAML、研究问题"></label><button id="clear">重置</button></div><p id="count" role="status" aria-live="polite"></p><div class="table-scroll"><table class="experiment-table"><thead><tr><th>实验 / 定义</th><th>准备</th><th>运行</th><th>分析</th><th>依赖与下一步</th></tr></thead><tbody>'
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
    unclassified = [p.name for p in (root / 'experiments/configs').iterdir() if p.is_dir() and p.name.startswith('aagu') and p.name not in groups]
    if unclassified:
        raise ValueError('Unclassified AAGU configuration groups: ' + ', '.join(unclassified))
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
