"""Executable synthetic witnesses; no human acceptance or live workspace writes."""
import hashlib
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote
import json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('setup_probe', ROOT/'tools/first_use_probe.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


class ModularTests(unittest.TestCase):
    def test_files_only_update_and_fresh_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)/'project'
            shutil.copytree(ROOT/'examples/kernel-only', project)
            overview = (project/'project-overview.md').read_bytes()
            current = project/'current-memory/general/limit.md'
            original = current.read_bytes()
            self.assertIn(b'limit = 12', original)
            self.assertIn('example-notebook', overview.decode())
            history = project/'history/limit-12.md'
            history.write_bytes(original)
            current.write_text('# Current limit\n\nlimit = 16\n\nAdopted synthetic D-03, 2026-09-08; exercise authorization. Previous: [12](../../history/limit-12.md).\n', encoding='utf-8')
            (project/'project-current-stage.md').write_text('# Current position\n\nAdopted limit 16; see [current](current-memory/general/limit.md). Synthetic D-03, 2026-09-08.\n', encoding='utf-8')
            # Recover from disk again, without cached conversation state or workflow.
            self.assertEqual(overview, (project/'project-overview.md').read_bytes())
            self.assertEqual(original, history.read_bytes())
            self.assertIn('limit = 16', current.read_text(encoding='utf-8'))
            self.assertIn('NOT adopted', (project/'current-memory/planning/ideas.md').read_text(encoding='utf-8'))
            self.assertFalse((project/'.agents').exists())

    def test_installed_skill_hashes_and_all_resource_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = setup.prepare(ROOT, Path(tmp)/'fresh')
            installed = work/'.agents/skills/default'
            for relative in ['SKILL.md', 'references/WORKFLOW.md', 'references/main-ai.md', 'templates/task.md', 'templates/report.md']:
                self.assertEqual((ROOT/'workflows/default'/relative).read_bytes(), (installed/relative).read_bytes())
            for path in (work/'.agents').rglob('*.md'):
                for raw in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                    rel = unquote(raw.strip('<>').split('#')[0])
                    if rel and '://' not in rel:
                        self.assertTrue((path.parent/rel).is_file(), f'{path.name}: {rel}')
            self.assertIn('Main AI Acceptance PENDING', (work/'Inbox/FIRST-001_任务单.md').read_text(encoding='utf-8'))
            self.assertEqual([], list((work/'Handoffs').iterdir()))

    def test_workflow_fixture_lifecycle_is_not_human_evidence(self):
        root = ROOT/'examples/default-workflow'
        self.assertIn('This example requires no installation.', (root/'current-memory/general/setup.md').read_text(encoding='utf-8'))
        self.assertEqual(1, len(list((root/'handoffs').glob('*_report.md'))))
        self.assertIn('Main AI Acceptance = PENDING', (root/'handoffs/EXAMPLE-001_report.md').read_text(encoding='utf-8'))
        self.assertEqual(['README.md'], [p.name for p in (root/'inbox').iterdir()])

    def test_add_route_remove_without_core_or_workflow_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for example in ['kernel-only', 'default-workflow']:
                project = root/example
                shutil.copytree(ROOT/'examples'/example, project)
                before = snapshot(project)
                outbox, inbox = root/(example+'-out'), project/'inbox'
                outbox.mkdir(); inbox.mkdir(exist_ok=True)
                module = root/(example+'-router')
                module.mkdir()
                shutil.copyfile(ROOT/'extensions/router/router.py', module/'router.py')
                config = module/'config.json'
                config.write_text(json.dumps({'source': str(outbox), 'routes': {'Example': str(inbox)}, 'stability_scans': 2, 'poll_interval_seconds': 0.01, 'log_file': str(module/'transport.log')}))
                source = outbox/'Example__proposal.md'
                source.write_bytes(b'Synthetic proposal; not current truth.\n')
                result = subprocess.run([sys.executable, '-B', str(module/'router.py'), '--config', str(config), '--max-scans', '2'], capture_output=True, timeout=15)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertFalse(source.exists())
                self.assertEqual(b'Synthetic proposal; not current truth.\n', (inbox/'proposal.md').read_bytes())
                shutil.rmtree(module)  # only the new, temporary installation owned by this test
                after = snapshot(project)
                self.assertEqual(before, {k: after[k] for k in before})
                self.assertIn('project-overview.md', after)

    def test_policy_ownership_and_handoff_cases(self):
        core = (ROOT/'core/MEMORY_CONTRACT.md').read_text(encoding='utf-8')
        policy = (ROOT/'workflows/default/references/WORKFLOW.md').read_text(encoding='utf-8')
        self.assertNotIn('## Worklist', core)
        self.assertNotIn('Research / Reuse Gate', core)
        self.assertIn('If Codex still needs action', policy)
        self.assertIn('no further Codex action remains', policy)
        for case in ['Rework', 'continuation', 'blocker recovery', 'governance writeback']:
            self.assertIn(case, policy)
        self.assertLess(len((ROOT/'core/MindOS.md').read_bytes()), 600)
        self.assertLess(len((ROOT/'workflows/default/SKILL.md').read_text(encoding='utf-8')), 2200)


if __name__ == '__main__':
    unittest.main()
