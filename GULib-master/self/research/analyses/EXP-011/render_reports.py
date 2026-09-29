"""Render the Markdown analysis and full tables without changing their content."""
from pathlib import Path
from markdown_it import MarkdownIt

base = Path(__file__).resolve().parent
md = MarkdownIt('commonmark', {'html': False}).enable('table')
style = '''body{max-width:1120px;margin:40px auto;padding:0 24px;font:16px/1.8 system-ui,sans-serif;color:#192638;background:#fafbfd}h1,h2{line-height:1.35}h2{margin-top:2em}table{border-collapse:collapse;width:100%;font-size:14px;background:white}td,th{border:1px solid #dbe2ea;padding:8px;text-align:left}th{background:#eaf0f7}blockquote{border-left:4px solid #3876b0;margin-left:0;padding:8px 20px;background:#eef5fb}a{color:#165d9b}code{overflow-wrap:anywhere}@media print{body{max-width:none;margin:0}table{font-size:10px}}'''
for stem in ('table02-v2-analysis', 'table02-v2-tables'):
    source = (base / (stem + '.md')).read_text(encoding='utf-8')
    content = md.render(source)
    page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EXP-011 Table02</title><style>' + style + '</style><main>' + content + '</main></html>'
    (base / (stem + '.html')).write_text(page, encoding='utf-8')
    assert '<table>' in page and '\ufffd' not in page
    print(stem + '.html: rendered from Markdown')
