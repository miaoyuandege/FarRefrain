import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from router import InboxRouter, load_config


class SharedRouteTests(unittest.TestCase):
    def test_all_configured_routes_support_canonical_and_single_alias(self):
        names = {"Example", "Profile", "Cards", "Demo", "Study", "Shared"}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            routes = {}
            for index, name in enumerate(sorted(names)):
                target = root / str(index)
                target.mkdir()
                routes[name] = str(target)
                (source / (name + "__canonical_probe.zip")).write_bytes(b"canonical")
                (source / (name + "_alias_probe.zip")).write_bytes(b"alias")
            config = root / "config.json"
            config.write_text(json.dumps({"source": str(source), "routes": routes,
                "poll_interval_seconds": 0.01, "stability_scans": 2,
                "log_file": str(root / "log")}), encoding="utf-8")
            shared = Path(routes["Shared"])
            (shared / "canonical_probe.zip").write_bytes(b"original")
            router = InboxRouter(load_config(config), event_sink=lambda event: None)
            try:
                router.scan_once()
                router.scan_once()
                self.assertEqual([], list(source.iterdir()))
                for name, target in routes.items():
                    canonical = (
                        "canonical_probe__001.zip"
                        if name == "Shared"
                        else "canonical_probe.zip"
                    )
                    self.assertEqual(b"canonical", (Path(target) / canonical).read_bytes())
                    self.assertEqual(b"alias", (Path(target) / "alias_probe.zip").read_bytes())
                self.assertEqual(b"original", (shared / "canonical_probe.zip").read_bytes())
                self.assertEqual(3, len(list(shared.iterdir())))
            finally:
                router.close()
