"""Validate this round's editable sources and generated reading copies."""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WRITING = HERE.parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.source_hash = [], [], None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.hrefs.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name') == 'source-sha256':
            self.source_hash = attrs['content']

sources = [WRITING / x for x in (
    'outline/OUTLINE.md', 'outline/OUTLINE.v4.md', 'outline/OUTLINE.v5.md',
    'protocol/ROUND3_EXECUTION_PROTOCOL.md', 'README.md',
    'review/2026-10-24-round3/REPORT.md')]
errors, checked = [], []
links = 0
for source in sources:
    md = source.read_text(encoding='utf-8')
    page = Page()
    html = source.with_suffix('.html').read_text(encoding='utf-8')
    page.feed(html)
    digest = sha256(source.read_bytes()).hexdigest()
    if page.source_hash != digest:
        errors.append(f'stale HTML: {source}')
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'duplicate anchors: {source}')
    if '\ufffd' in md + html:
        errors.append(f'encoding replacement: {source}')
    for href in page.hrefs:
        if not href or re.match(r'^(https?://|mailto:)', href):
            continue
        if href.startswith('#'):
            if unquote(href[1:]) not in page.ids:
                errors.append(f'missing anchor: {source}: {href}')
            continue
        path = re.sub(r':\d+(?:[-–]\d+)?$', '', unquote(href.split('#')[0]).strip('<>'))
        target = Path(path)
        if not target.is_absolute():
            target = source.parent / target
        links += 1
        if not target.exists():
            errors.append(f'missing local link: {source}: {href}')
    checked.append({'source': str(source.relative_to(WRITING)), 'sha256': digest})
outline = sources[0].read_text(encoding='utf-8')
counts = {s: outline.count(s) for s in (
    '**核心目标（要说什么）：**', '**准备怎么说：**', '**注意点／强调：**')}
if len(set(counts.values())) != 1 or '详细提纲 v6' not in outline:
    errors.append('outline version or per-paragraph fields do not agree')
freeze = json.loads((WRITING / 'protocol/PROTOCOL_FREEZE.json').read_text(encoding='utf-8-sig'))
if freeze['sha256'] != sha256((WRITING / 'protocol/ROUND3_EXECUTION_PROTOCOL.md').read_bytes()).hexdigest():
    errors.append('frozen protocol hash mismatch')
result = {'passed': not errors, 'sources': checked, 'local_links_checked': links,
          'outline_writing_units': counts, 'errors': errors,
          'visual_check': 'not performed; structural checks only'}
(HERE / 'DOCUMENT_VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 1)
