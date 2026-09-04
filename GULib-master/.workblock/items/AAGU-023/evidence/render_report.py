"""Render AAGU-023 Markdown authority into paired HTML with installed Mistune 3."""
import argparse
from html import escape
from pathlib import Path
import re
import mistune

ITEM = Path(__file__).resolve().parent.parent
CSS = '''
:root{color-scheme:light;--ink:#193039;--muted:#536c74;--accent:#126b63;--line:#ccd9d6}
*{box-sizing:border-box}body{margin:0;background:#f3f6f3;color:var(--ink);font:16px/1.7 system-ui,"Microsoft YaHei",sans-serif}
main{max-width:1200px;margin:24px auto 60px;padding:0 24px}h1{font-size:26px;line-height:1.3;margin:0 0 8px}
.meta{color:var(--muted);font-size:14px;margin-bottom:18px}section{background:#fff;border:1px solid var(--line);border-radius:10px;padding:24px;margin:18px 0}
h2{font-size:21px;margin:0 0 14px}h3{font-size:17px;margin:0 0 12px;color:var(--accent)}p{margin:0 0 14px}
ul,ol{padding-left:22px}li{margin-bottom:10px}a{color:#006b78;text-underline-offset:3px}code{font-size:.88em;overflow-wrap:anywhere;background:#edf2ef;padding:1px 4px;border-radius:3px}
.human{border-top:5px solid var(--accent)}.human-grid{display:grid;grid-template-columns:1fr 1.25fr .85fr;gap:24px}.human-grid>div{min-width:0}
.human-grid ul{margin-top:0}.human-grid p,.human-grid li{font-size:15px;line-height:1.65}.human-grid>div+div{border-left:1px solid var(--line);padding-left:24px}
[data-workblock-decision]{display:inline-block;background:#fff0ba;color:#604b00;font-weight:700;padding:5px 15px;border-radius:20px;margin-bottom:8px}
blockquote{margin:8px 0 14px;border-left:3px solid var(--line);padding-left:15px}.table-wrap{overflow-x:auto;margin:18px 0}table{border-collapse:collapse;width:100%;font-size:14px}
td,th{border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}th{background:#eef3ef}td code{font-size:13px}section:last-child{font-size:14px;color:var(--muted)}
@media(max-width:800px){main{padding:0 12px;margin-top:16px}h1{font-size:22px}.human-grid{display:block}.human-grid>div+div{border-left:0;border-top:1px solid var(--line);padding:18px 0 0;margin-top:18px}section{padding:18px}}
'''


def render(text):
    md = mistune.create_markdown(escape=True, plugins=['table'])
    title, body = text.split('\n', 1)
    sections = re.split(r'^## ', body, flags=re.M)[1:]
    if not sections or not sections[0].startswith('Human Result\n'):
        raise ValueError('Human Result must be first')
    human = sections[0].split('\n', 1)[1]
    parts = re.split(r'^### ', human, flags=re.M)[1:]
    columns = []
    for part in parts:
        name, content = part.split('\n', 1)
        html = md(content)
        if name == '当前决定':
            for value, state in [('待决定', 'pending'), ('接受', 'accepted')]:
                html = html.replace('<code>' + value + '</code>', '<span data-workblock-decision="' + state + '">' + value + '</span>', 1)
        columns.append('<div><h3>' + escape(name) + '</h3>' + html + '</div>')
    html = '<section class="human" data-workblock-human-result="2.1"><h2>Human Result</h2><div class="human-grid">' + ''.join(columns) + '</div></section>'
    for section in sections[1:]:
        heading, content = section.split('\n', 1)
        html += '<section><h2>' + escape(heading) + '</h2>' + md(content) + '</section>'
    html = html.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    return '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + escape(title[2:]) + '</title><style>' + CSS + '</style></head><body><main><h1>' + escape(title[2:]) + '</h1><div class="meta">Formal · data / lifecycle / integration · 原始证据可追溯 · 零删除</div>' + html + '</main></body></html>\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    html = render((ITEM / 'REPORT.md').read_text(encoding='utf-8'))
    target = ITEM / 'REPORT.html'
    if args.check:
        if target.read_text(encoding='utf-8') != html:
            raise SystemExit('REPORT.html differs from Markdown renderer')
        print('Report pair rendering: PASS')
    else:
        with target.open('w', encoding='utf-8', newline='\n') as out:
            out.write(html)
