"""The paper's numerical table generator must preserve author-owned prose."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


class SelectorCostTests(unittest.TestCase):
    def test_table_rebuild_cannot_touch_manuscript_prose(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / 'report/paper/appendix/exp014-selector-cost-20261025'
        spec = importlib.util.spec_from_file_location('cost_build', folder / 'build.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        prose = root / 'report/paper/overleaf/sections/selector_cost.tex'
        original = prose.read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'rows.tex'
            module.build(folder / 'SUMMARY.json', output)
            self.assertEqual(original, prose.read_bytes())
            text = output.read_text(encoding='utf-8')
            self.assertIn('Timeout (2 h)', text)
            self.assertIn('6--8 h (est.)', text)


if __name__ == '__main__':
    unittest.main()
