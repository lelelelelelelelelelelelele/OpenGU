"""Regression checks for source ownership, lost edits and honest sync state."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts.paper_review.model import BLOCKS, Desk
from scripts.paper_review.sync import Cloud, read_zip


def archive(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as z:
        for name, value in files.items():
            z.writestr(name, value)
    return buffer.getvalue()


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.paper = self.root / 'paper'
        (self.paper / 'sections').mkdir(parents=True)
        (self.paper / 'main.tex').write_text('main\n', encoding='utf-8')
        source = '\n'.join('\\subsection{' + value[2] + '}\n原文\n' for value in BLOCKS.values() if value[2])
        (self.paper / 'sections/results.tex').write_text(source+'\n\\subsection{Other}\nkeep\n', encoding='utf-8')
        (self.paper / 'sections/selector_cost.tex').write_text('author text\n', encoding='utf-8')
        self.desk = Desk(self.paper, self.root / 'state')
        self.cloud = Cloud(self.desk)

    def files(self):
        return {p.relative_to(self.paper).as_posix(): p.read_bytes() for p in self.paper.rglob('*') if p.is_file()}

    def test_edit_keeps_other_blocks_and_audits_reason(self):
        original = self.desk.block('fig4')['source']
        block = self.desk.block('fig3')
        self.desk.save('fig3', block['version'], block['source'].replace('原文', '修改'), '核对说明')
        self.assertEqual(original, self.desk.block('fig4')['source'])
        event = self.desk.events('fig3')[-1]
        self.assertIn('+修改', event['diff'])
        self.assertEqual(event['reason'], '核对说明')

    def test_external_edit_rejects_stale_save(self):
        block = self.desk.block('fig3')
        path = self.paper / 'sections/results.tex'
        path.write_text(path.read_text(encoding='utf-8')+'external', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '其他编辑'):
            self.desk.save('fig3', block['version'], 'changed', 'why')
        self.assertTrue(path.read_text(encoding='utf-8').endswith('external'))

    def test_comment_binds_exact_source(self):
        block = self.desk.block('exp014')
        self.desk.comment('exp014', block['version'], '<script>意见</script>')
        self.assertEqual(block['source'], self.desk.events('exp014')[0]['source'])

    def test_browser_newlines_do_not_make_unchanged_source_dirty(self):
        block = self.desk.block('fig3')
        self.assertNotIn('\r', block['source'])
        with self.assertRaisesRegex(ValueError, '没有变化'):
            self.desk.save('fig3', block['version'], block['source'], 'unchanged')

    def test_empty_reason_rejected(self):
        block = self.desk.block('fig3')
        with self.assertRaises(ValueError):
            self.desk.save('fig3', block['version'], block['source']+'x', '')

    def test_zip_cannot_traverse_or_write_git(self):
        for path in ('../main.tex', '/main.tex', '.git/config', 'sections\\main.tex', 'C:/main.tex'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                data = archive({'main.tex': 'x', path: 'y'})
                if chr(92) in path:
                    # ZipFile normalizes native separators while writing on Windows.
                    data = data.replace(b'sections/main.tex', b'sections'+bytes([92])+b'main.tex')
                read_zip(data)

    def test_matching_zip_does_not_imply_compile_or_sync(self):
        state = self.cloud.check(archive(self.files()))
        self.assertEqual(state['status'], '源码一致，编译未验证')

    def test_cloud_change_blocks_export_and_conflict_preserves_every_source(self):
        base = self.files()
        self.cloud.check(archive(base))
        (self.paper / 'main.tex').write_text('local\n', encoding='utf-8')
        preserved = (self.paper / 'main.tex').read_bytes()
        remote = dict(base, **{'main.tex': b'remote\n', 'sections/new.tex': b'new'})
        self.cloud.check(archive(remote))
        with self.assertRaises(ValueError):
            self.cloud.package()
        with self.assertRaisesRegex(ValueError, '冲突'):
            self.cloud.pull()
        self.assertEqual(preserved, (self.paper / 'main.tex').read_bytes())
        self.assertFalse((self.paper / 'sections/new.tex').exists())

    def test_pull_merges_disjoint_changes(self):
        (self.paper / 'main.tex').write_text('a\nb\nc\nd\ne\n', encoding='utf-8')
        base = self.files()
        self.cloud.check(archive(base))
        (self.paper / 'main.tex').write_text('local\nb\nc\nd\ne\n', encoding='utf-8')
        remote = dict(base, **{'main.tex': b'a\nb\nc\nd\nremote\n'})
        self.cloud.check(archive(remote))
        self.cloud.pull()
        self.assertEqual('local\nb\nc\nd\nremote\n', (self.paper / 'main.tex').read_text(encoding='utf-8'))
        self.assertIn('main.tex', read_zip(self.cloud.package()))

    def test_remote_only_asset_is_preserved(self):
        self.cloud.check(archive(dict(self.files(), **{'teaser.pdf': b'asset'})))
        self.assertIn('teaser.pdf', self.cloud.status()['cloudOnly'])
        self.assertEqual([], self.cloud.status()['differences'])

    def test_source_change_invalidates_verified_receipt(self):
        self.cloud.verify(archive(self.files()),
                          'https://www.overleaf.com/download/project/6ab3c34131990d0250f3d05d/build/test/output.pdf',
                          'Explicit test fixture observation, not a real cloud compilation')
        self.assertEqual('已同步', self.cloud.status()['status'])
        self.assertEqual([], self.cloud.status()['cloudChanged'])
        (self.paper / 'main.tex').write_text('changed', encoding='utf-8')
        self.assertEqual('未验证', self.cloud.status()['status'])

    def test_verify_rejects_mismatch(self):
        with self.assertRaises(ValueError):
            self.cloud.verify(archive({'main.tex':'other'}), 'x', 'x')

    def test_table_rebuild_cannot_touch_manuscript_prose(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / 'report/paper/appendix/exp014-selector-cost-20261025'
        spec = importlib.util.spec_from_file_location('cost_build', folder / 'build.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = self.root / 'rows.tex'
        original = (self.paper / 'sections/selector_cost.tex').read_bytes()
        module.build(folder / 'SUMMARY.json', output)
        self.assertEqual(original, (self.paper / 'sections/selector_cost.tex').read_bytes())
        self.assertIn('Timeout (2 h)', output.read_text(encoding='utf-8'))
        self.assertIn('6--8 h (est.)', output.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
