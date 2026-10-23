"""Render REPORT.md to the matching static HTML and verify local report links."""
from pathlib import Path
from html import escape
from urllib.parse import unquote, urlsplit
import re
import sys
from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
source = HERE / (sys.argv[1] if len(sys.argv) > 1 else 'REPORT.md')
md = source.read_text(encoding='utf-8')
body = MarkdownIt('commonmark', {'html': False}).enable('table').render(md)
missing = []
for href in re.findall(r'(?:href|src)="([^"]+)"', body):
    url = urlsplit(href)
    if url.scheme or not url.path:
        continue
    target = (HERE / unquote(url.path)).resolve()
    if not target.exists():
        missing.append(str(target))
if missing:
    raise SystemExit('Missing links:\n' + '\n'.join(sorted(set(missing))))
body = re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll">\1</div>', body, flags=re.S)
css = '''
:root { color-scheme: light; --ink:#182a37; --muted:#60717b; --line:#dce5e9; --accent:#12665b; }
* { box-sizing:border-box; }
body { margin:0; background:#f3f6f5; color:var(--ink); font:16px/1.8 "Segoe UI","Microsoft YaHei",sans-serif; }
main { max-width:1240px; margin:42px auto; padding:46px 56px; background:white; border-top:6px solid var(--accent); box-shadow:0 12px 48px #18382c0a; }
h1 { font-size:36px; line-height:1.35; letter-spacing:.02em; margin:0 0 20px; }
h2 { font-size:25px; margin-top:52px; padding-top:20px; border-top:1px solid var(--line); }
h3 { font-size:19px; margin-top:30px; }
h1 + p { color:var(--muted); font-size:14px; }
a { color:var(--accent); text-decoration:underline; text-underline-offset:3px; overflow-wrap:anywhere; }
p,li,td { overflow-wrap:anywhere; }
strong { color:#104d46; }
code { background:#edf3f3; border-radius:4px; padding:2px 5px; font-size:.88em; overflow-wrap:anywhere; }
.table-scroll { overflow-x:auto; margin:20px 0; }
table { width:100%; border-collapse:collapse; font-size:14px; line-height:1.65; min-width:740px; }
th,td { padding:12px 14px; border:1px solid var(--line); text-align:left; vertical-align:top; }
th { background:#eaf2ef; color:#194a41; }
tr:nth-child(even) { background:#fafcfb; }
li { margin:9px 0; }
footer { color:var(--muted); font-size:13px; margin-top:40px; }
@media(max-width:760px) { main { margin:0; padding:26px 20px; } h1 { font-size:27px; } h2 { font-size:22px; } }
@media print { main { margin:0; padding:0; box-shadow:none; } body { background:white; } table { min-width:0; font-size:10px; } h2 { break-after:avoid; } }
'''
title = md.splitlines()[0].lstrip('# ')
html = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + escape(title) + '</title><style>' + css + '</style></head><body><main>' + body + '<footer>由 ' + escape(source.name) + ' 生成；实验状态以相应 EXP 记录为准。</footer></main></body></html>'
source.with_suffix('.html').write_text(html, encoding='utf-8')
print(f'Rendered {source.name}; local links verified; {len(md)} source characters.')
