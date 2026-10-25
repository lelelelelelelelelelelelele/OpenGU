"""Check source identity, links, table counts, and arithmetic output receipts."""
from pathlib import Path
import csv
import hashlib
import json
import re
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
markdown = (HERE / 'REPORT.md').read_text(encoding='utf-8')
html = (HERE / 'REPORT.html').read_text(encoding='utf-8')
digest = hashlib.sha256((HERE / 'REPORT.md').read_bytes()).hexdigest()
assert f'name="report-source-sha256" content="{digest}"' in html
assert '\ufffd' not in html and '\ufffd' not in markdown
targets = re.findall(r'\]\(([^)]+)\)', markdown)
local_targets = [unquote(t) for t in targets if not t.startswith(('https://', 'http://', '#'))]
for target in local_targets:
    assert (HERE / target).exists(), target
table_count = len(re.findall(r'^\|\s*---', markdown, flags=re.M))
assert html.count('<table>') == table_count == 6
for key in ['3.647', '2.263', '3.776', '3.057', '−0.541', '−0.111,0.581', '4.44']:
    assert key in html and key in markdown, key
for name, expected in [('GIF_SOURCE_EFFECTS.csv', 12), ('CLEAN_METHOD_SELECTOR_INTERACTIONS.csv', 72), ('FIG4_CLEAN_DESCRIPTIVE.csv', 140)]:
    with (HERE / name).open(encoding='utf-8', newline='') as handle:
        assert len(list(csv.DictReader(handle))) == expected
sources = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
assert len(sources['papers']) == 8
for source in sources['scalar_evidence']:
    assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
result = dict(status='pass', report_source_sha256=digest, primary_papers=8, tables=table_count, local_links_checked=len(local_targets), source_effect_rows=12, descriptive_interaction_rows=72, fig4_summary_rows=140, meaning='Document/receipt consistency only; not scientific acceptance')
(HERE / 'DOCUMENT_QA.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
