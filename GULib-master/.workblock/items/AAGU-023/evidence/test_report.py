"""Static report checks; these do not claim browser visual acceptance."""
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('render_report', HERE / 'render_report.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])

    def handle_data(self, data):
        self.text.append(data)


class ReportTests(unittest.TestCase):
    def test_exact_generated_pair(self):
        md = (HERE.parent / 'REPORT.md').read_text(encoding='utf-8')
        self.assertEqual(renderer.render(md), (HERE.parent / 'REPORT.html').read_text(encoding='utf-8'))

    def test_links_and_decision(self):
        html = (HERE.parent / 'REPORT.html').read_text(encoding='utf-8')
        parsed = Links()
        parsed.feed(html)
        self.assertGreater(len(parsed.links), 10)
        for href in parsed.links:
            self.assertNotIn('://', href)
            self.assertTrue((HERE.parent / href).is_file(), href)
        self.assertEqual(html.count('data-workblock-human-result='), 1)
        self.assertEqual(html.count('data-workblock-decision="pending"'), 1)
        text = ''.join(parsed.text)
        for fact in ['1,115', '26,040,188', '建议接受', 'NOT OBSERVED', 'IndexNotFoundError']:
            self.assertIn(fact, text)

    def test_future_decision_projection_is_not_reset_by_renderer(self):
        md = (HERE.parent / 'REPORT.md').read_text(encoding='utf-8')
        accepted = md.replace('> 当前验收决定：`待决定`', '> 当前验收决定：`接受`')
        html = renderer.render(accepted)
        self.assertEqual(html.count('data-workblock-decision="accepted"'), 1)
        self.assertNotIn('data-workblock-decision="pending"', html)


if __name__ == '__main__':
    unittest.main()
