import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('public_scan', ROOT/'tools/prepublish_scan.py')
scanner = importlib.util.module_from_spec(spec); spec.loader.exec_module(scanner)


class PublicPretestTests(unittest.TestCase):
    def fixture(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name); (root/'.git').mkdir(); (root/'docs').mkdir()
        body = b'safe example\n'
        manifest = json.dumps({'assets':[{'path':'example.md','sha256':hashlib.sha256(body).hexdigest(),'origin':'SYNTHETIC','transformation':'test'}]}).encode()
        blobs = {'example.md':body, 'docs/asset-manifest.json':manifest}
        ids = {hashlib.sha256(v).hexdigest():v for v in blobs.values()}
        for name, value in blobs.items(): (root/name).write_bytes(value)
        def git(args, **kwargs):
            cmd = args[3:]
            if cmd[0] == 'rev-parse': return str(root).encode() + b'\n'
            if cmd[0] == 'ls-files': return b''.join(b'100644 '+hashlib.sha256(v).hexdigest().encode()+b' 0\t'+k.encode()+b'\0' for k,v in blobs.items())
            if cmd[0] == 'cat-file': return ids[cmd[2]]
            raise AssertionError('unexpected Git operation')
        return root, git

    def test_exact_staged_tree_and_metadata_exclusion(self):
        root, git = self.fixture()
        with patch.object(scanner.subprocess, 'check_output', side_effect=git):
            result = scanner.scan_tracked(root)
        self.assertTrue(result['passed']); self.assertEqual(result['tracked_files'],2)

    def test_untracked_even_ignored_file_blocks(self):
        root, git = self.fixture(); (root/'.env').write_text('synthetic private data')
        with patch.object(scanner.subprocess, 'check_output', side_effect=git):
            with self.assertRaises(ValueError): scanner.scan_tracked(root)

    def test_staged_working_tree_drift_blocks(self):
        root, git = self.fixture(); (root/'example.md').write_text('unreviewed change')
        with patch.object(scanner.subprocess, 'check_output', side_effect=git):
            with self.assertRaises(ValueError): scanner.scan_tracked(root)

    def test_ai_entry_and_unexecuted_synthetic_project(self):
        readme = (ROOT/'README.md').read_text(encoding='utf-8')
        self.assertLess(readme.index('assets/farrefrain-hero.svg'), readme.index('# FarRefrain'))
        for key in ['Move context out of the chat.', 'Keep thinking in the conversation.', '[Install with AI]', 'assets/farrefrain-workflow.svg']:
            self.assertIn(key, readme)
        self.assertLess(readme.index('New chats lose context'), readme.index('## Install with AI'))
        self.assertLess(readme.index('## Install with AI'), readme.index('## A 30-second example'))
        for key in ['Before:', 'With FarRefrain:', 'not a measured speed or success guarantee']:
            self.assertIn(key, readme)
        launch = (ROOT/'docs/LAUNCH_COPY.md').read_text(encoding='utf-8')
        for key in ['## One-liner', '## Short post', '## Story version', 'External Human First-use = NOT RUN', 'Prepared only']:
            self.assertIn(key, launch)
        entry = (ROOT/'START_HERE.md').read_text(encoding='utf-8')
        for key in ['A. Inspect','B. Install','C. Place','D. Verify','E. Tell','接管这个项目','执行任务','MIT LICENSED']:
            self.assertIn(key, entry)
        self.assertNotIn('LICENSE PENDING', entry)
        readme = (ROOT/'README.md').read_text(encoding='utf-8')
        self.assertIn('[LICENSE](LICENSE)', readme)
        self.assertIn('NOT v0.1 FINAL', readme)
        self.assertIn('External Human First-use = NOT RUN', readme)
        self.assertNotIn('LICENSE PENDING', readme)
        project = ROOT/'examples/external-first-use-project'
        self.assertEqual((project/'欢迎说明.md').read_text(encoding='utf-8').count('等待补充。'),1)
        self.assertTrue((project/'收件箱/EXT-FIRST-001_任务单.md').is_file())
        self.assertFalse((project/'任务交接记录/EXT-FIRST-001_报告单.md').exists())


if __name__ == '__main__': unittest.main()
