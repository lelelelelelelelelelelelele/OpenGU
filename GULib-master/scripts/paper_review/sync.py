"""Cloud snapshots are inspected before packaging; checks never upload or overwrite."""
import io
import json
from pathlib import Path, PurePosixPath
import zipfile
import subprocess
import tempfile

from .model import digest, now

PROJECT = 'https://www.overleaf.com/project/6ab3c34131990d0250f3d05d'


def read_zip(data):
    result = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if sum(info.file_size for info in archive.infolist()) > 100_000_000:
            raise ValueError('源码包超过 100 MB。')
        for info in archive.infolist():
            if info.is_dir():
                continue
            name = info.orig_filename
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or chr(92) in name or ':' in name or any(
                    part.startswith('.') and part != '.gitattributes' for part in path.parts):
                raise ValueError('源码包包含不安全的文件路径。')
            if name in result:
                raise ValueError('源码包包含重复文件。')
            result[name] = archive.read(info)
    if 'main.tex' not in result:
        raise ValueError('请选择既有 Overleaf 项目根目录的源码 ZIP。')
    return result


def local_files(paper):
    return {p.relative_to(paper).as_posix(): p.read_bytes() for p in paper.rglob('*')
            if p.is_file() and p.suffix in {'.tex', '.bib', '.pdf', '.png', '.jpg', '.cls', '.sty', '.bst'}}


def manifest(files):
    return {n: digest(b) for n, b in files.items()}


class Cloud:
    def __init__(self, desk):
        self.desk = desk
        self.state = desk.state / 'cloud.json'

    def status(self):
        state = json.loads(self.state.read_text(encoding='utf-8')) if self.state.exists() else {}
        state['project'] = PROJECT
        current = manifest(local_files(self.desk.paper))
        if state.get('local') != current:
            state.update(status='未验证', detail='本地源码已变化或尚未检查云端。')
        elif state.get('status') == '已同步':
            state['detail'] = '已核对记录所列时刻的云端源码与编译；后续云端修改须重新检查。'
        return state

    def check(self, data):
        remote = read_zip(data)
        local = local_files(self.desk.paper)
        old = json.loads(self.state.read_text(encoding='utf-8')) if self.state.exists() else {}
        remote_manifest = manifest(remote)
        baseline = old.get('baseline', remote_manifest)
        cloud_changed = sorted(n for n in set(baseline) | set(remote_manifest)
                               if baseline.get(n) != remote_manifest.get(n))
        # Remote-only assets are retained. Deletion is never inferred from their local absence.
        differences = sorted(n for n in local if remote.get(n) != local[n])
        state = dict(status='源码一致，编译未验证' if not differences else '有待同步差异',
                     checkedAt=now(), baseline=baseline, remote=remote_manifest, local=manifest(local),
                     differences=differences, cloudChanged=cloud_changed,
                     cloudOnly=sorted(set(remote) - set(local)),
                     detail='云端自上次检查后发生变化，请先取回并核对；差异包已禁用。' if cloud_changed else
                            '已检查下载快照；上传前须再次下载检查，上传后须重新编译并核对源码。')
        (self.desk.state / 'cloud-latest.zip').write_bytes(data)
        if not (self.desk.state / 'cloud-baseline.zip').exists():
            (self.desk.state / 'cloud-baseline.zip').write_bytes(data)
        self.state.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        return self.status()

    def package(self):
        state = self.status()
        if state.get('status') == '未验证' or state.get('cloudChanged') or 'remote' not in state:
            raise ValueError('请先取回并核对最新云端差异，不能覆盖未取回修改。')
        files = local_files(self.desk.paper)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in state['differences']:
                archive.writestr(name, files[name])
        return buffer.getvalue()

    def pull(self):
        """Merge all upstream edits first; conflicts leave every source untouched."""
        state = self.status()
        if state.get('status') == '未验证':
            raise ValueError('本地已变化，请先重新检查云端 ZIP。')
        remote = read_zip((self.desk.state / 'cloud-latest.zip').read_bytes())
        base = read_zip((self.desk.state / 'cloud-baseline.zip').read_bytes())
        local = local_files(self.desk.paper)
        changes = {}
        for name in state['cloudChanged']:
            target = (self.desk.paper / name).resolve()
            if not target.is_relative_to(self.desk.paper) or target.suffix not in {
                    '.tex', '.bib', '.pdf', '.png', '.jpg', '.cls', '.sty', '.bst'}:
                raise ValueError('云端文件不在支持的论文输入范围内：' + name)
            before, current, incoming = base.get(name), local.get(name), remote.get(name)
            if current == incoming:
                continue
            if current == before:
                changes[name] = incoming
            elif incoming == before:
                continue
            elif before is not None and incoming is not None and current is not None and name.endswith(('.tex', '.bib')):
                with tempfile.TemporaryDirectory(dir=self.desk.state) as temp:
                    paths = [Path(temp) / n for n in ('local', 'base', 'remote')]
                    for path, data in zip(paths, (current, before, incoming)):
                        path.write_bytes(data.replace(b'\r\n', b'\n'))
                    result = subprocess.run(['git', 'merge-file', '-p', *map(str, paths)], capture_output=True)
                    if result.returncode:
                        raise ValueError('云端与本地有冲突，未写入任何源码：' + name)
                    changes[name] = result.stdout
            else:
                raise ValueError('云端与本地有冲突，未写入任何源码：' + name)
        for name, data in changes.items():
            path = self.desk.paper / name
            self.desk.record(dict(block='cloud', kind='pull', reason='取回已检查的云端修改',
                                  path=name, beforeSha=digest(local[name]) if name in local else None,
                                  afterSha=digest(data) if data is not None else None))
            if data is None:
                path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        state.update(baseline=state['remote'])
        self.state.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        (self.desk.state / 'cloud-baseline.zip').write_bytes((self.desk.state / 'cloud-latest.zip').read_bytes())
        return self.check((self.desk.state / 'cloud-latest.zip').read_bytes())

    def verify(self, data, compile_url, observation):
        state = self.check(data)
        if state['differences']:
            raise ValueError('云端源码仍有差异，不能标为已同步。')
        if not compile_url.startswith('https://www.overleaf.com/download/project/6ab3c34131990d0250f3d05d/build/'):
            raise ValueError('需要本项目实际编译结果的下载地址。')
        if not observation.strip():
            raise ValueError('需要实际核对编译结果的观察记录。')
        # This is an explicit human/agent verification receipt, not inferred compiler success.
        state.update(status='已同步', verifiedAt=now(), compileUrl=compile_url,
                     compileObservation=observation, baseline=state['remote'], cloudChanged=[])
        self.state.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        (self.desk.state / 'cloud-baseline.zip').write_bytes(data)
        return self.status()
