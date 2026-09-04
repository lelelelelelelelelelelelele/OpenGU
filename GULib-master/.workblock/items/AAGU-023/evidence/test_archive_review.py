import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('archive_review', Path(__file__).with_name('archive_review.py'))
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ArchiveReviewTests(unittest.TestCase):
    def test_original_bundle_and_totals(self):
        self.assertEqual(review.check_bundle()['files'], 1115)
        self.assertEqual(review.check_bundle()['old_v2_artifacts'], 16)

    def test_exact_device_population(self):
        local, ssh = review.request('local'), review.request('ssh')
        self.assertEqual(sum(len(g['files']) for g in local['groups']), 75)
        self.assertEqual(sum(len(g['files']) for g in ssh['groups']), 1040)
        self.assertEqual(len(ssh['active_v2_files']), 1)
        self.assertEqual(local['active_v2_files'], [])
        self.assertNotIn('results/cache_v2', local['absent'])
        self.assertIn('results/_archive_aagu023_20260904/ledger-final.json', [f['path'] for f in local['ledgers']])

    def test_portable_probe_source_compiles(self):
        code = Path(review.__file__).read_text(encoding='utf-8').rsplit("\nif __name__ == '__main__':", 1)[0]
        compile(code, '<remote-probe>', 'exec')

    def test_scope_rejects_escape(self):
        for p in ['../outside', 'results/../../outside', 'attack/test.py', '/results/x']:
            with self.assertRaises(ValueError):
                review.safe_path(Path.cwd(), p)

    def test_probe_detects_corruption_extra_files_and_active_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / 'results/archive'
            dest.mkdir(parents=True)
            (root / 'results/cache_v2').mkdir()
            (dest / 'a').write_bytes(b'original')
            req = {'device': 'fixture', 'groups': [{'path': 'results/archive', 'files': [
                {'path': 'a', 'bytes': 8, 'sha256': review.sha(b'original')}]}],
                'active_v2_files': [], 'ledgers': [], 'absent': ['results/cache']}
            with patch.object(subprocess, 'check_output', return_value='fixture-head'):
                self.assertEqual(review.probe(root, req)['status'], 'PASS')
                (dest / 'a').write_bytes(b'changed!')
                (dest / 'extra').write_bytes(b'x')
                (root / 'results/cache').mkdir()
                result = review.probe(root, req)
            self.assertEqual(result['status'], 'FAIL')
            self.assertEqual(len(result['problems']), 3)


if __name__ == '__main__':
    unittest.main()
