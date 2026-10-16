"""Render the editable main report and appendix into self-contained HTML.

Run in an environment with markdown-it-py and beautifulsoup4.
This script reads the report and evidence; it never changes experiment state.
"""
from pathlib import Path
import base64
import hashlib
import json
import re
from html import escape
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

OUT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(stem, sidebar_title, evidence_label, receipt_name, updated_date):
    source = OUT / (stem + '.md')
    raw = source.read_text(encoding='utf-8')
    assert '@@' not in raw, 'Unfilled report data'
    md = MarkdownIt('commonmark', {'html': False}).enable('table')
    body = md.render(raw)
    soup = BeautifulSoup(body, 'html.parser')
    before = soup.get_text(' ', strip=True)
    links = []
    for element in soup.select('a[href], img[src]'):
        attr = 'src' if element.name == 'img' else 'href'
        href = element[attr]
        parsed = urlsplit(href)
        if parsed.scheme in ('http', 'https', 'mailto') or href.startswith('#'):
            continue
        path = (OUT / unquote(parsed.path)).resolve()
        if path.parent == OUT and path.name in ('REPORT.html', 'FIXED_BUDGET_APPENDIX.html'):
            # Both pages are generated below. Hash the editable peer source to
            # avoid circular receipts whose HTML hashes become stale on rebuild.
            peer_source = path.with_suffix('.md')
            assert peer_source.is_file(), f'Missing report source: {href}'
            links.append({'link': href, 'source_sha256': digest(peer_source)})
        else:
            assert path.is_file(), f'Missing report link: {href}'
            links.append({'link': href, 'sha256': digest(path)})
        if element.name == 'img':
            mime = {'png': 'image/png', 'svg': 'image/svg+xml'}[path.suffix[1:]]
            element['src'] = f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
            element['loading'] = 'eager'
            element['decoding'] = 'sync'
        else:
            element['href'] = parsed.path + (('#' + parsed.fragment) if parsed.fragment else '')
    nav = []
    for index, heading in enumerate(soup.find_all('h2'), 1):
        heading['id'] = f'section-{index}'
        nav.append(f'<a href="#section-{index}">{heading.get_text()}</a>')
    for table in soup.find_all('table'):
        wrapper = soup.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0'})
        table.wrap(wrapper)
    assert before == soup.get_text(' ', strip=True)
    css = '''
    :root{color-scheme:light;--ink:#173143;--muted:#516576;--paper:#f4f6f5;--line:#d7e1e3;--accent:#126b61;--nav:#102b3b}
    *{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:32px}
    body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 'Segoe UI','Microsoft YaHei',sans-serif}
    .shell{display:grid;grid-template-columns:250px minmax(0,1040px);max-width:1370px;margin:auto;gap:34px;padding:32px 24px 72px}
    aside{position:sticky;top:28px;align-self:start;background:var(--nav);color:white;border-radius:16px;padding:24px 20px}
    .eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#9dc9c5;margin-bottom:8px}
    aside strong{display:block;font-size:19px;line-height:1.45;margin-bottom:20px}
    nav a{display:block;color:#d6e5e9;text-decoration:none;font-size:13px;line-height:1.5;margin:13px 0}
    nav a:hover{color:#85dfce}aside small{display:block;border-top:1px solid #365361;padding-top:16px;color:#afc2ca;font-size:12px;line-height:1.7}
    main{min-width:0;background:white;border:1px solid var(--line);border-radius:18px;padding:42px 46px;box-shadow:0 10px 40px #12304406}
    h1{font-size:34px;line-height:1.35;letter-spacing:-.03em;margin:0 0 22px;font-weight:750}
    h2{font-size:24px;line-height:1.4;margin:52px 0 20px;padding-top:24px;border-top:2px solid var(--line)}
    h3{font-size:18px;margin:30px 0 14px;color:#125e59}p{margin:15px 0}strong{font-weight:700}
    blockquote{margin:24px 0;padding:18px 23px;background:#eef7f4;border-left:4px solid var(--accent);border-radius:0 10px 10px 0}
    blockquote p{margin:4px 0}a{color:#096d8c;text-underline-offset:3px;overflow-wrap:anywhere}
    ul,ol{padding-left:24px}li{padding-left:3px;margin:8px 0}code{font:13px/1.6 Consolas,monospace;background:#edf2f4;border-radius:4px;padding:2px 5px;overflow-wrap:anywhere}
    pre{white-space:pre-wrap;background:#edf2f4;padding:17px;border-radius:8px;overflow-wrap:anywhere}
    .table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:9px;margin:22px 0}
    table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.6}th{background:#173c50;color:white;font-weight:600;text-align:left}
    th,td{padding:11px 12px;vertical-align:top;border-bottom:1px solid #e0e7e9;min-width:92px}td:first-child,th:first-child{min-width:110px}tr:nth-child(even) td{background:#f4f7f8}
    img{display:block;max-width:100%;height:auto;margin:24px auto 10px;border:1px solid #dce5e8;border-radius:8px}
    hr{border:0;border-top:1px solid var(--line);margin:30px 0}footer{margin-top:38px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:16px}
    @media(max-width:1000px){.shell{grid-template-columns:minmax(0,1fr);padding:16px;gap:16px}aside{position:static;padding:18px 22px}nav{display:flex;flex-wrap:wrap;gap:6px 18px}nav a{margin:3px 0}aside small{margin-top:12px}main{padding:28px}h1{font-size:29px}}
    @media(max-width:520px){body{font-size:15px}.shell{padding:8px}main{padding:23px 17px;border-radius:12px}h1{font-size:25px}h2{font-size:21px}aside strong{font-size:17px}th,td{padding:9px}blockquote{padding:13px 16px}}
    @media print{body{background:white}.shell{display:block;padding:0}aside{display:none}main{border:0;box-shadow:none;padding:0}h2{break-after:avoid}img,tr{break-inside:avoid}a{color:inherit}}
    '''
    title = escape(soup.h1.get_text())
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + title + '</title><style>' + css + '</style></head><body><div class="shell"><aside><div class="eyebrow">OpenGU · Research note</div><strong>' + sidebar_title + '</strong><nav>' + ''.join(nav) + '</nav><small>' + evidence_label + '<br>既有结果重分析 · ' + updated_date + '</small></aside><main>' + str(soup) + '<footer>由同目录 ' + source.name + ' 生成。实验事实、解释和拟议实验分别标注；图像已嵌入，阅读不依赖外部资源。</footer></main></div></body></html>'
    target = OUT / (stem + '.html')
    target.write_text(page, encoding='utf-8')
    receipt = {
        'markdown_sha256': digest(source), 'html_sha256': digest(target),
        'body_text_agreement': True, 'local_link_count': len(links),
        'local_links': links, 'embedded_figures': len(soup.find_all('img')),
        'sections': len(nav), 'unfilled_markers': False,
        'new_gpu_experiments': 0, 'scientific_acceptance_changed': False,
        'browser_render': 'NOT OBSERVED',
    }
    (OUT / receipt_name).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'local_links'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build('FIXED_BUDGET_APPENDIX', '固定 10%<br>的补充证据',
          'EXP-079 / e79r5 · 十 seed', 'appendix_report_verification.json', '2026-10-16')
    build('REPORT', '删除预算<br>与重训练对齐',
          'EXP-032 · 三 seed · 四个 ratio', 'report_verification.json', '2026-10-17')
