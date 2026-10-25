"""Three manuscript slices, optimistic editing, and durable review history."""
import difflib
import hashlib
import json
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

BLOCKS = {
    'fig3': ('Fig. 3 · PubMed 请求响应', 'results.tex', 'Family-like response patterns reveal GU limitations'),
    'fig4': ('Fig. 4 · CiteSeer 预算响应', 'results.tex', 'Selector effects persist with method-dependent GU responses'),
    'exp014': ('EXP-014 · 请求生成成本', 'selector_cost.tex', None),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


class Desk:
    def __init__(self, paper, state):
        self.paper = Path(paper).resolve()
        self.state = Path(state).resolve()
        self.state.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()

    def slice(self, key):
        _, filename, title = BLOCKS[key]
        path = self.paper / 'sections' / filename
        text = path.read_bytes().decode('utf-8')
        start, end = 0, len(text)
        if title:
            start = text.index('\\subsection{' + title + '}')
            next_section = text.find('\\subsection{', start + 1)
            if next_section >= 0:
                end = next_section
        return path, text, start, end

    def block(self, key):
        path, text, start, end = self.slice(key)
        return dict(id=key, title=BLOCKS[key][0], path=str(path),
                    line=text[:start].count('\n') + 1, source=text[start:end].replace('\r\n', '\n'),
                    version=digest(text.encode('utf-8')))

    def events(self, key):
        path = self.state / 'reviews.jsonl'
        if not path.exists():
            return []
        return [row for line in path.read_text(encoding='utf-8').splitlines()
                if (row := json.loads(line))['block'] == key]

    def record(self, event):
        event['time'] = now()
        with (self.state / 'reviews.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + '\n')

    def save(self, key, version, source, reason):
        if not reason.strip():
            raise ValueError('请填写修改原因。')
        with self.lock:
            path, text, start, end = self.slice(key)
            if digest(text.encode('utf-8')) != version:
                raise ValueError('源码已被其他编辑更新，请刷新后重新核对。')
            before = text[start:end]
            source = source.replace('\r\n', '\n')
            if '\r\n' in before:
                source = source.replace('\n', '\r\n')
            if source == before:
                raise ValueError('源码没有变化；意见请单独保存。')
            if BLOCKS[key][2] and not source.startswith('\\subsection{' + BLOCKS[key][2] + '}'):
                raise ValueError('请保留本块的 subsection 标题，以便稳定定位。')
            event = dict(block=key, kind='edit', reason=reason, before=before, after=source,
                         version=version, diff=''.join(difflib.unified_diff(
                             before.splitlines(True), source.splitlines(True), fromfile='before', tofile='after')))
            # Record the intended before/after first; a failed write is explicitly marked.
            self.record(dict(event, kind='edit-intent'))
            try:
                with path.open('w', encoding='utf-8', newline='') as stream:
                    stream.write(text[:start] + source + text[end:])
            except OSError:
                self.record(dict(block=key, kind='edit-failed', reason=reason))
                raise
            self.record(event)
            return self.block(key)

    def comment(self, key, version, text):
        if not text.strip():
            raise ValueError('请先填写意见。')
        with self.lock:
            block = self.block(key)
            if version != block['version']:
                raise ValueError('源码已变化，请刷新后再提交意见。')
            self.record(dict(block=key, kind='comment', reason=text, version=version,
                             source=block['source']))

    def git_diff(self):
        result = subprocess.run(['git', 'diff', 'HEAD', '--', str(self.paper)],
                                cwd=self.paper, capture_output=True, encoding='utf-8', check=True)
        return result.stdout
