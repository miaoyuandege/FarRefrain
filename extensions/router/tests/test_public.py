import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from router import ConfigError, load_config, move_exclusive


class PublicRouterTests(unittest.TestCase):
    def test_example_relative_paths_resolve_against_config_not_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ['outbox', 'project/inbox', 'notes/inbox']:
                (root/name).mkdir(parents=True)
            config = root/'config.json'
            config.write_bytes((ROOT/'config.example.json').read_bytes())
            loaded = load_config(config)
            self.assertEqual(root/'outbox', loaded.source)
            self.assertEqual(root/'project/inbox', loaded.routes['Example'])

    def test_source_equal_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root/'config.json'
            config.write_text(json.dumps({'source': '.', 'routes': {'Example': '.'}}))
            with self.assertRaises(ConfigError): load_config(config)

    def test_portable_exclusive_move_preserves_race_winner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = root/'source', root/'target'
            source.write_bytes(b'new'); target.write_bytes(b'race-winner')
            with self.assertRaises(FileExistsError): move_exclusive(source, target, platform='posix')
            self.assertEqual(b'race-winner', target.read_bytes())
            self.assertEqual(b'new', source.read_bytes())
            target.unlink()
            move_exclusive(source, target, platform='posix')
            self.assertFalse(source.exists())
            self.assertEqual(b'new', target.read_bytes())


if __name__ == '__main__': unittest.main()
