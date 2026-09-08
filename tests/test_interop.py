"""Files-only adoption checks; these do not claim a fresh external runtime probe."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InteropExampleTests(unittest.TestCase):
    def test_result_is_not_adoption_or_a_package(self):
        example = ROOT/'examples/interop'
        self.assertEqual({'README.md','external-result.md'}, {p.name for p in example.iterdir()})
        self.assertIn('NOT ADOPTED', (example/'README.md').read_text(encoding='utf-8'))
        result = (example/'external-result.md').read_text(encoding='utf-8').splitlines()
        self.assertEqual(4, len(result))
        for line, prefix in zip(result[1:], ['Progress:','Plans:','Problems:']):
            self.assertTrue(line.startswith(prefix))
        notebook = ROOT/'examples/kernel-only'
        self.assertIn('limit = 12', (notebook/'current-memory/general/limit.md').read_text(encoding='utf-8'))
        self.assertIn('NOT adopted', (notebook/'current-memory/planning/ideas.md').read_text(encoding='utf-8'))
        self.assertTrue((notebook/'history/limit-8.md').is_file())

    def test_dated_evidence_keeps_discovery_and_removal_limits(self):
        doc = (ROOT/'docs/ECOSYSTEM_INTEROP.md').read_text(encoding='utf-8')
        for term in ['NOT PROVEN', 'not permanent erasure', 'no-universal-manifest',
                     '2026.8.31', 'lychee 0.24.2', 'Node', 'two denied reads']:
            self.assertIn(term, doc)


if __name__ == '__main__':
    unittest.main()
