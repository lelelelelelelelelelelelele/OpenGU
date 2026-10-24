"""Validate portable navigation, inventory coverage and frozen input identity."""
from hashlib import sha256
from html.parser import HTMLParser
import csv
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'paper_writing/data_package/2026-10-24'
S = P / 'sources/OpenGU/GULib-master'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.source_hash=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='meta' and a.get('name')=='source-sha256':self.source_hash=a['content']

errors=[]; links=0; sources=[]
for p in sorted(P.glob('*.md')):
    html=p.with_suffix('.html')
    if not html.exists():errors.append('missing HTML '+p.name);continue
    page=Page();page.feed(html.read_text(encoding='utf-8'))
    if page.source_hash != sha256(p.read_bytes()).hexdigest():errors.append('stale HTML '+p.name)
    if '\ufffd' in p.read_text(encoding='utf-8'):errors.append('encoding '+p.name)
    for href in page.links:
        if href.startswith(('#','https:','http:','mailto:')):continue
        path=unquote(href.split('#')[0]).removeprefix('file:///')
        path=re.sub(r':\d+(?:[-–]\d+)?$','',path)
        target=Path(path)
        if target.is_absolute():errors.append('nonportable core link '+p.name+': '+href);continue
        links+=1
        if not (p.parent/target).exists():errors.append('missing core link '+p.name+': '+href)
    sources.append(p.name)
cat=json.loads((P/'handover/catalog.json').read_text(encoding='utf-8'))
state_ids={p.stem for p in (S/'self/research/experiments').glob('EXP-*.json')}
catalog_ids={x['id'] for x in cat['experiments']}
if state_ids != catalog_ids or len(state_ids)!=33:errors.append('experiment catalog coverage')
for r in cat['yaml_reference_closure']:
    p=S/r['path']
    if not p.is_file() or sha256(p.read_bytes()).hexdigest()!=r['sha256']:errors.append('YAML closure '+r['path'])
for e in cat['experiments']:
    r=e['source_snapshot']
    for label in ('experiment','analysis'):
        if r.get(label+'_path'):
            p=S/r[label+'_path']
            if sha256(p.read_bytes()).hexdigest()!=r[label+'_sha256']:errors.append('catalog source changed '+str(p))
with (P/'RUNS.csv').open(encoding='utf-8',newline='') as f:runs=list(csv.DictReader(f))
if len(runs)!=75:errors.append('attempt coverage')
review=S/'paper_writing/review/2026-10-24-round3/REVIEW_INPUTS.json'
for r in json.loads(review.read_text(encoding='utf-8'))['sources']:
    p=S/r['path']
    if not p.is_file() or sha256(p.read_bytes()).hexdigest()!=r['sha256']:errors.append('frozen input changed '+r['path'])
v8=(P/'OUTLINE.v8.md').read_text(encoding='utf-8')
if [v8.count(x) for x in ['**核心目标（要说什么）：**','**准备怎么说：**','**注意点／强调：**']] != [102]*3:
    errors.append('outline writing-unit fields')
result={'passed':not errors,'core_documents':sources,'local_core_links_checked':links,
        'experiment_records':len(state_ids),'registered_attempts':len(runs),'yaml_files_checked':len(cat['yaml_reference_closure']),
        'frozen_review_sources_checked':153,'errors':errors,
        'limits':'Navigation, inventory and byte identity; not scientific acceptance or model re-forward verification.'}
(P/'DOCUMENT_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
