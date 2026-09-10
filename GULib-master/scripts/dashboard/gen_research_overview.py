"""Build research phases, independent experiment sheets and a shared SVG map.

Only explicit sheet sources own preparation/run/analysis snapshots. WorkItems
are provenance links; their lifecycle is never used as experiment progress.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
import re
import yaml
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'self/research'
STYLE=Path(__file__).with_name('research.css')
SCRIPT=Path(__file__).with_name('research.js')
PREP={'draft':'配置待形成','defined':'配置已定','review':'范围待复核','preparing':'运行准备中','waiting':'等待输入'}
RUN={'unknown':'运行待核对','unbound':'未绑定运行','pending':'待运行','running':'运行中','partial':'部分完成','failed':'运行失败','completed':'运行完成','not_required':'无需新运行'}
ANALYSIS={'not_started':'未开始','working':'分析中','review':'待科学复核','complete':'分析完成'}


def esc(value):return html.escape(str(value),quote=True)


def load(root=ROOT):
    directory=root/'self/research'
    frame=json.loads((directory/'framework.json').read_text(encoding='utf-8'))
    sheets=[]
    for id in frame['sheets']:
        if not re.fullmatch('[a-z][a-z0-9-]+',id):raise ValueError('Invalid sheet ID')
        sheet=json.loads((directory/'experiments'/f'{id}.json').read_text(encoding='utf-8'))
        if sheet['id']!=id:raise ValueError('Sheet ID differs from filename')
        sheets.append(sheet)
    validate(frame,sheets)
    return frame,sheets


def validate(frame,sheets):
    if frame['schema_version']!=1:raise ValueError('Unsupported framework schema')
    phases={p['id'] for p in frame['phases']};topics={t['id'] for t in frame['topics']};ids={s['id'] for s in sheets}
    if len(ids)!=len(sheets) or len(frame['sheets'])!=len(ids):raise ValueError('Duplicate sheet ID')
    if len(phases)!=len(frame['phases']) or len(topics)!=len(frame['topics']):raise ValueError('Duplicate phase/topic')
    for s in sheets:
        if s['phase'] not in phases or s['family'] not in frame['families'] or not set(s['topics']).issubset(topics):raise ValueError('Invalid phase/family/topic')
        for key in ['title','question','comparison','narrative','metrics','outputs','limits','sources']:
            if not s.get(key):raise ValueError('Incomplete experiment definition: '+key)
        if s['preparation']['state'] not in PREP or s['execution']['state'] not in RUN or s['analysis']['state'] not in ANALYSIS:raise ValueError('Unknown progress state')
        if s['kind'] not in {'experiment','analysis'}:raise ValueError('Unknown sheet kind')
        if s['kind']=='experiment' and s['preparation']['state']=='defined' and not s['configs']:raise ValueError('Defined experiment needs executable config')
        if s['kind']=='analysis' and (s['execution']['state']!='not_required' or not s['analysis']['inputs']):raise ValueError('Analysis sheet requires inputs and no new execution')
        for c in s['configs']:
            if not c['path'].startswith('experiments/configs/') or not c['path'].endswith(('.yaml','.yml')):raise ValueError('Executable config must be YAML, not a WorkItem')
        run=s['execution'];done,total=run['completed'],run['total']
        if total is not None and (type(total) is not int or total<=0):raise ValueError('Invalid expected count')
        if done is not None and (type(done) is not int or done<0 or total is None or done>total):raise ValueError('Invalid completed count')
        if run['state']=='completed' and (total is None or done!=total or not run['runs']):raise ValueError('Completion needs explicit runs and matching counts')
        if (run['state'] in {'running','partial','failed'} or (done or 0)>0) and not run['runs']:raise ValueError('Observed execution needs run evidence')
        if run['state']=='pending' and (not s['configs'] or done!=0):raise ValueError('Pending requires bound config and explicit zero')
        for r in run['runs']:
            if not all(r.get(k) for k in ['experiment_id','run_id','commit','sha256','path']):raise ValueError('Run identity missing')
        if not set(s['analysis']['inputs']).issubset(ids) or s['id'] in s['analysis']['inputs']:raise ValueError('Invalid analysis input')
        if s['analysis']['state'] in {'complete','review'} and not s['analysis']['links']:raise ValueError('Analysis progress needs sources')
    # Existing input chains may not form a cycle; these are evidence inputs, not Block dependencies.
    lookup={s['id']:s for s in sheets}
    def visit(id,trail):
        if id in trail:raise ValueError('Cyclic analysis inputs')
        for parent in lookup[id]['analysis']['inputs']:visit(parent,trail|{id})
    for id in ids:visit(id,set())


def links(obj):
    if isinstance(obj,dict):
        if 'label' in obj and 'path' in obj:yield obj
        for v in obj.values():yield from links(v)
    elif isinstance(obj,list):
        for v in obj:yield from links(v)


class Sources:
    def __init__(self,root,canonical):self.root=root.resolve();self.canonical=canonical.resolve()
    def resolve(self,path):
        if path.startswith('../../OpenGU-DocMap/'):
            return self.canonical.parent.parent/'OpenGU-DocMap'/path[len('../../OpenGU-DocMap/'):]
        p=Path(path)
        if p.is_absolute() or '..' in p.parts or ':' in path or '\\' in path:raise ValueError('Invalid source path: '+path)
        base=self.canonical if path.startswith(('.workblock/','results/')) else self.root
        return base/p
    def href(self,path,page):
        target=self.resolve(path)
        if target.anchor.lower()!=page.anchor.lower():return target.as_uri()
        return quote(Path(os.path.relpath(target,page.parent)).as_posix(),safe='/.:')
    def anchor(self,link,page):return f'<a href="{self.href(link["path"],page)}">{esc(link["label"])} ↗</a>'


def check_sources(frame,sheets,sources):
    refs=list(links([frame,sheets]))
    missing=[r['path'] for r in refs if not sources.resolve(r['path']).exists()]
    if missing:raise ValueError('Missing sources: '+', '.join(sorted(set(missing))))
    return len(refs)


def verify_runs(sheets,sources):
    checked=0
    for s in sheets:
        observed=set()
        for bound in s['execution']['runs']:
            path=sources.resolve(bound['path']);raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=bound['sha256']:raise ValueError('Run manifest changed')
            run=json.loads(raw)
            if any(run[k]!=bound[k] for k in ['experiment_id','run_id','commit']):raise ValueError('Run identity mismatch')
            if run['config_path'] not in [c['path'] for c in s['configs']]:raise ValueError('Run config mismatch')
            for cell in run['cells']:
                if cell['status']=='completed':observed.add((run['experiment_id'],cell['cell_id']))
                for name,info in cell['files'].items():
                    artifact=(path.parent/cell['path']/name).resolve()
                    try:artifact.relative_to(path.parent.resolve())
                    except ValueError as exc:raise ValueError('Artifact outside run') from exc
                    if hashlib.sha256(artifact.read_bytes()).hexdigest()!=info['sha256']:raise ValueError('Artifact checksum mismatch')
                    checked+=1
            checked+=1
        if s['execution']['runs'] and len(observed)!=s['execution']['completed']:raise ValueError('Run count mismatch')
    return checked


def badge(state,labels):return f'<span class="badge {esc(state)}">{esc(labels[state])}</span>'


def shell(title,body,script=''):
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+STYLE.read_text(encoding='utf-8')+'</style></head><body>'+body+('<script>'+script+'</script>' if script else '')+'</body></html>\n'


def diagram(frame,sheets,prefix):
    family=frame['families'];byphase={p['id']:[s for s in sheets if s['phase']==p['id']] for p in frame['phases']}
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 590" role="img" aria-labelledby="map-title map-desc">','<title id="map-title">研究阶段与实验配置单</title><desc id="map-desc">Phase 1和Phase 2中的IF研究与共同参照，以及独立IM研究线。点击每张配置单查看准备、运行和分析。</desc>', '<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#223138" stroke-width=".5"/></pattern><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#82b6b6"/></marker></defs>', '<style>text{font-family:"Microsoft YaHei","Noto Sans SC",sans-serif}a rect{transition:stroke .15s}a:hover rect,a:focus rect{stroke:#f4e6c3;stroke-width:2}a:focus{outline:none}</style>', '<rect width="1440" height="590" rx="12" fill="#111e26"/><rect width="1440" height="590" fill="url(#grid)"/>','<text x="30" y="38" fill="#b9cbd0" font-size="16">研究阶段 × 方法分组</text>','<path d="M462 286 H498" stroke="#82b6b6" fill="none" stroke-width="2" marker-end="url(#arrow)"/>']
    colors={'if':'#80d4c1','im':'#e3ba79','baseline':'#9bbde9','shared':'#bdb4da','main':'#a7c8ed'}
    for i,phase in enumerate(frame['phases']):
        x=30+i*480;w=420
        svg.append(f'<rect x="{x}" y="68" width="{w}" height="410" rx="10" fill="#14232b" stroke="#3b535d"/>')
        svg.append(f'<text x="{x+22}" y="103" fill="#f1e9d7" font-size="22" font-weight="600">{esc(phase["name"])}</text><text x="{x+22}" y="129" fill="#9fb4bc" font-size="15">{esc(phase["subtitle"])}</text>')
        for j,s in enumerate(byphase[phase['id']]):
            y=152+j*98;color=colors[s['family']]
            svg.append(f'<a href="{prefix}{s["id"]}.html" tabindex="0" aria-label="{esc(s["title"])}"><rect x="{x+18}" y="{y}" width="384" height="80" rx="6" fill="#1a2e37" stroke="{color}"/><text x="{x+34}" y="{y+25}" fill="{color}" font-size="12">{esc(family[s["family"]])} · {esc(PREP[s["preparation"]["state"]])}</text><text x="{x+34}" y="{y+52}" fill="#edf0e9" font-size="18">{esc(s["title"])}</text></a>')
        if phase['id']=='im-track':svg.append(f'<text x="{x+22}" y="400" fill="#aebfc4" font-size="14">组内删除效果与选集稳定性</text><text x="{x+22}" y="427" fill="#aebfc4" font-size="14">不以IF阶段完成作为前置</text>')
    svg.append('<text x="30" y="526" fill="#b9cbd0" font-size="16">先理解选点，再比较遗忘结果；各部分的研究问题与当前进度见下方展开说明。</text>')
    svg.append('<text x="30" y="562" fill="#9ab0b8" font-size="13">点击实验名称查看配置、结果与分析。连线表示研究衔接，不代表运行必须串行。</text></svg>')
    return ''.join(svg)


def config_preview(config,sources,page):
    path=sources.resolve(config['path'])
    try:
        parsed=yaml.safe_load(path.read_text(encoding='utf-8'))
    except yaml.YAMLError as exc:
        raise ValueError('Invalid YAML: '+config['path']) from exc
    if not isinstance(parsed,dict):raise ValueError('Experiment config must be a mapping: '+config['path'])
    content=yaml.safe_dump(parsed,allow_unicode=True,sort_keys=False,width=100)
    return '<section class="yaml-file"><h3>'+sources.anchor({'label':path.name,'path':config['path']},page)+'</h3><p class="config-path">'+esc(config['path'])+'</p><pre class="yaml-content"><code>'+esc(content)+'</code></pre></section>'


def question_links(s,frame,prefix):
    return '<div class="question-links">'+''.join(f'<a href="{prefix}#question-{t["id"]}">{esc(t["question"])}</a>' for t in frame['topics'] if t['id'] in s['topics'])+'</div>'


def sheet_page(s,frame,sources,page):
    a=lambda r:sources.anchor(r,page)
    phase=next(p for p in frame['phases'] if p['id']==s['phase'])
    run=s['execution'];analysis=s['analysis'];count='未核对覆盖' if run['completed'] is None else f'{run["completed"]} / {run["total"]} 条件'
    if run['state']=='not_required':count='复用既有结果'
    def table(rows):return '<dl class="definition">'+''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in rows)+'</dl>'
    body=f'<div class="shell sheet"><nav class="top"><a href="../index.html#cluster-{s["family"]}">← {esc(frame["families"][s["family"]])} · 研究总览</a><span>实验配置单 · {esc(s["id"])}</span></nav><header class="sheet-hero"><div class="eyebrow">{esc(phase["name"])} / {esc(frame["families"][s["family"]])}</div><h1>{esc(s["title"])}</h1><p class="question">{esc(s["question"])}</p></header><div class="status-grid"><div><label>准备</label>{badge(s["preparation"]["state"],PREP)}</div><div><label>运行</label>{badge(run["state"],RUN)}<small>{esc(count)}</small></div><div><label>分析</label>{badge(analysis["state"],ANALYSIS)}</div></div><nav class="section-nav"><a href="#design">实验设计</a><a href="#preparation">配置与准备</a><a href="#results">运行与结果</a><a href="#analysis">结果分析</a></nav>'
    body+='<section id="design" class="panel"><h2>实验设计</h2>'+''.join('<p class="experiment-story">'+esc(paragraph)+'</p>' for paragraph in s['narrative'])+'<h3>这项实验对应的研究问题</h3>'+question_links(s,frame,'../index.html')+'<p>'+esc(s['metrics'])+'</p><p class="boundary">'+esc(s['limits'])+'</p></section>'
    body+='<section id="preparation" class="panel"><h2>配置与准备</h2>'
    if s['configs']:
        body+='<p class="muted">以下内容在生成页面时直接读取并解析所链接的YAML文件。文件改动后重新生成页面即可更新；引用的文件名保持原样。</p>'
        body+=''.join(config_preview(c,sources,page) for c in s['configs'])
    else:
        body+='<p class="muted">离线分析无需新执行表。</p>' if s['kind']=='analysis' else '<p class="muted">尚未形成独立执行表，研究问题已保留。</p>'
    body+=('<ul>'+''.join('<li>'+esc(g)+'</li>' for g in s['preparation']['gaps'])+'</ul>' if s['preparation']['gaps'] else '<p class="muted">已有关联的执行定义；重新运行仍需核对对应版本、数据身份和运行前置。</p>')+'</section>'
    body+='<section id="results" class="panel"><div class="section-head"><span>03</span><h2>运行与结果</h2></div>'+badge(run['state'],RUN)
    for r in run['runs']:
        body+='<div class="run">'+a(r)+table([['Experiment',r['experiment_id']],['Run',r['run_id']],['代码版本',r['commit']]])+'</div>'
    if not run['runs']:body+='<p class="muted">尚未关联本配置单的完整运行结果；已有准备记录与完成结果分别查看。</p>' if s['kind']=='experiment' else '<p>直接消费下方关联的实验结果，不启动新运行。</p>'
    body+='<div class="source-list">'+''.join(a(r) for r in run['links'])+'</div></section>'
    body+='<section id="analysis" class="panel"><div class="section-head"><span>04</span><h2>结果分析</h2></div>'+badge(analysis['state'],ANALYSIS)
    if analysis['inputs']:body+='<h3>关联输入配置单</h3><div class="source-list">'+''.join(f'<a href="{id}.html">{esc(next(x["title"] for x in frame["loaded_sheets"] if x["id"]==id))} →</a>' for id in analysis['inputs'])+'</div>'
    body+='<div class="source-list">'+(''.join(a(r) for r in analysis['links']) or '<p class="muted">尚未关联分析成果。可在获得部分可用结果后开始分析，完成状态另行记录。</p>')+'</div></section>'
    body+='<footer><h3>定义与历史来源</h3><div class="source-list">'+''.join(a(r) for r in s['sources'])+f'</div><p>来源整理：{s["reviewed_at"]}。配置单独立承接研究准备；来源记录的Block状态不决定这里的实验进度。本页不自动提交实验或刷新运行。</p></footer></div>'
    return shell(s['title']+' · 实验配置单',body)


def index_page(frame,sheets,sources,page):
    a=lambda r:sources.anchor(r,page)
    phase_names={p['id']:p['name'] for p in frame['phases']}
    body='<div class="shell"><nav class="top"><span class="brand">OPENGU / EXPERIMENTS</span><div>'+a(frame['sources'][0])+a(frame['sources'][2])+'</div></nav><header class="hero"><div><div class="eyebrow">研究框架与实验配置单</div><h1>实验研究总览</h1><p>策略性删除会怎样影响图遗忘？<br>从选点机制到结果解释，逐部分查看研究设计与当前证据。</p></div><div class="hero-aside"><strong>'+str(len(sheets))+'</strong> 张配置与分析单<br><span>IF 簇 / IM 簇</span></div></header><section class="map-panel" aria-label="研究框图"><div class="map-heading"><h2>研究框架</h2><a href="diagram/research-framework.svg">打开完整 SVG ↗</a></div><p class="muted">点击框内配置单查看详情；窄屏可横向滚动框图。</p><div class="map-scroll" tabindex="0">'+diagram(frame,sheets,'experiments/')+'</div></section>'
    map_start=body.index('<section class="map-panel"')
    overview_map=body[map_start:]
    header=body[:map_start]
    body=''
    body+='<section id="research-questions" class="topics" aria-label="研究问题与当前进度"><h2>我们要回答什么，目前做到哪里</h2><p class="research-intro">我们想知道：刻意选择删除节点，能否改变图遗忘的结果？如果改变了，原因是什么，又在哪些条件下成立？下面逐部分展开研究思路；点击问题可以展开或收起说明。</p><div class="topic-grid">'
    for i,t in enumerate(frame['topics']):
        related=[s for s in sheets if t['id'] in s['topics']]
        ready=sum((s['execution']['completed'] or 0)>0 for s in related)
        progress=f'{len(related)}项相关实验或分析 · {ready}项已有核对结果' if related else '尚未形成实验配置'
        body+=f'<details class="topic" id="question-{t["id"]}" {"open" if i==0 else ""}><summary><span class="topic-heading">{esc(t["question"])}</span><span class="topic-progress">{esc(progress)}</span></summary><div class="topic-body">'
        body+=''.join('<p>'+esc(paragraph)+'</p>' for paragraph in t['narrative'])
        if related:
            body+='<div class="research-progress"><h3>对应实验的当前进度</h3><p class="muted">以下是已核对的实验记录；单项完成不代表本部分的全部问题已解决。</p>'
            for sheet in related:
                ex=sheet['execution'];an=sheet['analysis'];prep=sheet['preparation']
                observation=(f'已核对 {ex["completed"]} / {ex["total"]} 个运行条件。' if ex['completed'] is not None else '运行覆盖尚未核对。')
                if sheet['kind']=='analysis':observation='复用已有实验结果做离线分析，无需新运行。'
                if prep['state']=='draft':observation='研究设计已保留，尚未形成独立执行配置。'
                body+=f'<p class="research-experiment"><a href="experiments/{sheet["id"]}.html">{esc(sheet["title"])} ↗</a><span>{esc(observation)}准备：{esc(PREP[prep["state"]])}；分析：{esc(ANALYSIS[an["state"]])}。</span></p>'
            body+=f'<button class="topic-filter" data-topic="{t["id"]}" data-label="{esc(t["question"])}" aria-pressed="false">在下方查看这些实验的完整状态</button></div>'
        else:
            body+='<p class="research-empty">这里目前只有研究方向，尚未关联执行配置或结果。需要先明确比较条件，再建立实验配置单。</p>'
        body+='</div></details>'
    body+='</div></section>'
    questions=body
    body=header
    body+='<nav class="cluster-nav" aria-label="研究入口"><a href="#cluster-if">IF 簇</a><a href="#cluster-im">IM 簇</a><a href="#cluster-main">GU 主实验</a><a href="#research-questions">按问题找实验</a><a href="#stage-map">阶段框图</a></nav>'
    body+='<section class="sheet-list" id="sheets"><div class="list-heading"><h2>按研究簇查看实验</h2><span id="count" role="status" aria-live="polite"></span></div><div class="filters"><label>阶段<select id="phase"><option value="all">全部阶段 / 研究线</option>'+''.join(f'<option value="{p["id"]}">{esc(p["name"])}</option>' for p in frame['phases'])+'</select></label><label>方法组<select id="family"><option value="all">全部分组</option>'+''.join(f'<option value="{id}">{esc(name)}</option>' for id,name in frame['families'].items())+'</select></label><label>工作视图<select id="view"><option value="all">全部配置单</option><option value="prepare">准备实验</option><option value="run">待运行 / 运行中</option><option value="analysis">待分析 / 待复核</option></select></label><label class="search">搜索<input id="search" type="search" placeholder="研究问题、配置单…"></label><button id="clear">清除筛选</button></div><p id="filter-note" class="muted">准备、运行、分析是独立状态。配置已定不等于已运行；缺失结果不自动计为零。</p><div class="cluster-list">'
    current_family=None
    for s in sorted(sheets,key=lambda item:list(frame['families']).index(item['family'])):
        if s['family']!=current_family:
            if current_family is not None:body+='</div></section>'
            current_family=s['family']
            body+=f'<section class="cluster" id="cluster-{current_family}"><h2>{esc(frame["families"][current_family])}</h2><p class="cluster-story">{esc(frame["family_stories"][current_family])}</p><div class="cards">'
        ex=s['execution'];an=s['analysis'];prep=s['preparation']['state']
        # Analysis-only sheets enter the queue when at least one explicitly linked input has usable results.
        has_results=(ex['completed'] or 0)>0 or (s['kind']=='analysis' and any((x['execution']['completed'] or 0)>0 for x in sheets if x['id'] in an['inputs']))
        scopes=[]
        if prep!='defined':scopes.append('prepare')
        if ex['state'] in {'pending','running','partial','failed'}:scopes.append('run')
        if has_results and an['state']!='complete':scopes.append('analysis')
        story_html=''.join('<p>'+esc(paragraph)+'</p>' for paragraph in s['narrative'])
        related_questions=question_links(s,frame,'')
        body+=f'<article class="card family-{s["family"]}" data-phase="{s["phase"]}" data-family="{s["family"]}" data-topics="{" ".join(s["topics"])}" data-views="{" ".join(scopes)}"><div class="card-meta">{esc(phase_names[s["phase"]])} · {esc(frame["families"][s["family"]])}</div><h3><a href="experiments/{s["id"]}.html">{esc(s["title"])} <span aria-hidden="true">↗</span></a></h3><p>{esc(s["question"])}</p><details class="experiment-explanation"><summary>这项实验为什么做，怎样回答问题</summary>{story_html}<h4>对应研究问题</h4>{related_questions}</details><div class="card-status"><div><small>准备</small>{badge(prep,PREP)}</div><div><small>运行</small>{badge(ex["state"],RUN)}</div><div><small>分析</small>{badge(an["state"],ANALYSIS)}</div></div></article>'
    body+='</div></section></div><p id="empty" class="empty" hidden>当前筛选没有配置单。该研究问题仍保留；可清除筛选查看已有设计。</p></section>'+questions+'<details id="stage-map" class="stage-map"><summary>查看 Phase 1 / Phase 2 阶段框图</summary>'+overview_map+'</details><footer><div class="source-list">'+''.join(a(r) for r in frame['sources'][1:])+'</div><p>来源整理：'+frame['reviewed_at']+'。大框图表达研究结构，不生成Block任务状态或调度队列。旧覆盖CSV仅作为历史链接，不驱动本页。</p></footer></div>'
    return shell(frame['title'],body,SCRIPT.read_text(encoding='utf-8'))


def outputs(frame,sheets,sources,directory):
    frame=dict(frame,loaded_sheets=sheets)
    result={directory/'index.html':index_page(frame,sheets,sources,directory/'index.html'),directory/'diagram/research-framework.svg':diagram(frame,sheets,'../experiments/')}
    for s in sheets:
        path=directory/'experiments'/f'{s["id"]}.html';result[path]=sheet_page(s,frame,sources,path)
    return result


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--canonical-root',type=Path,default=ROOT);ap.add_argument('--output-dir',type=Path,default=SOURCE);ap.add_argument('--check',action='store_true');ap.add_argument('--check-links',action='store_true');ap.add_argument('--verify-evidence',action='store_true');args=ap.parse_args(argv)
    try:
        frame,sheets=load();sources=Sources(ROOT,args.canonical_root)
        if args.check_links:print('Linked sources:',check_sources(frame,sheets,sources),'PASS')
        if args.verify_evidence:print('Run/artifact checksums:',verify_runs(sheets,sources),'PASS')
        built=outputs(frame,sheets,sources,args.output_dir.resolve())
        for path,content in built.items():
            if args.check:
                if not path.exists() or path.read_text(encoding='utf-8')!=content:raise ValueError('Stale generated output: '+str(path))
            else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
        print(('Checked' if args.check else 'Generated'),len(built),'pages / SVG; no task or execution writes')
    except (ValueError,OSError,KeyError) as exc:ap.exit(1,str(exc)+'\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
