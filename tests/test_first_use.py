import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('first_use', ROOT/'tools/first_use_probe.py')
first_use = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first_use)


class SetupTests(unittest.TestCase):
    def test_prepare_matches_candidate_and_does_not_forge_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = first_use.prepare(ROOT, Path(tmp)/'fresh')
            for source, target in [('workflows/default/SKILL.md', '.agents/skills/default/SKILL.md'), ('core/MEMORY_CONTRACT.md', '.agents/core/MEMORY_CONTRACT.md')]:
                self.assertEqual(hashlib.sha256((ROOT/source).read_bytes()).digest(), hashlib.sha256((work/target).read_bytes()).digest())
            self.assertEqual(len(list((work/'.agents/skills/default/templates').glob('*.md'))), 6)
            self.assertTrue((work/'Inbox/FIRST-001_任务单.md').exists())
            self.assertEqual(list((work/'Handoffs').iterdir()), [])
            self.assertFalse((work/'.git').exists())

    def test_existing_workspace_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            keep = Path(tmp)/'keep.md'; keep.write_text('user asset')
            with self.assertRaises(ValueError): first_use.prepare(ROOT, Path(tmp))
            self.assertEqual(keep.read_text(), 'user asset')

    def test_candidate_overlap_rejected(self):
        with self.assertRaises(ValueError): first_use.prepare(ROOT, ROOT/'probe-output')

    def test_missing_candidate_rejected_before_workspace_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); candidate = base/'empty'; candidate.mkdir()
            with self.assertRaises(ValueError): first_use.prepare(candidate, base/'out')
            self.assertFalse((base/'out').exists())


if __name__ == '__main__': unittest.main()
