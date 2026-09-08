from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from router import FileRouteEventSink, InboxRouter, load_config  # noqa: E402


class InboxRouterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="router-test-")
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        self.source.mkdir()
        self.target.mkdir()
        self.log_file = self.root / "router.log"
        self.config_path = self.root / "config.json"
        self.config_path.write_text(
            json.dumps({
                "source": str(self.source),
                "poll_interval_seconds": 0.01,
                "stability_scans": 2,
                "routes": {"Cards": str(self.target)},
                "log_file": str(self.log_file),
                "max_log_bytes": 1024,
                "log_backup_count": 1,
            }, ensure_ascii=False),
            encoding="utf-8",
        )
        self.config = load_config(self.config_path)
        self.router = InboxRouter(self.config)

    def tearDown(self):
        self.router.close()
        self.temporary.cleanup()

    def scan(self, count: int = 1):
        for _ in range(count):
            self.router.scan_once()

    def test_normal_route_removes_prefix_after_two_stable_scans(self):
        source = self.source / "Cards__Task.md"
        source.write_text("payload", encoding="utf-8")

        self.scan()
        self.assertTrue(source.exists())
        self.scan()

        self.assertFalse(source.exists())
        self.assertEqual("payload", (self.target / "Task.md").read_text(encoding="utf-8"))

    def test_legacy_bracket_route_remains_compatible(self):
        source = self.source / "[Cards]Legacy.md"
        source.write_text("legacy", encoding="utf-8")

        self.scan(2)

        self.assertFalse(source.exists())
        self.assertEqual("legacy", (self.target / "Legacy.md").read_text(encoding="utf-8"))

    def test_single_underscore_alias_preserves_internal_underscores(self):
        source = self.source / "Cards_Task_part__02.md"
        source.write_text("alias", encoding="utf-8")

        self.scan(2)

        self.assertFalse(source.exists())
        self.assertEqual(
            "alias",
            (self.target / "Task_part__02.md").read_text(encoding="utf-8"),
        )

    def test_ordinary_and_unknown_single_underscore_files_are_untouched(self):
        ordinary = self.source / "notes_file.md"
        unknown = self.source / "Unknown_Task.md"
        ordinary.write_text("ordinary", encoding="utf-8")
        unknown.write_text("unknown", encoding="utf-8")

        self.scan(3)

        self.assertTrue(ordinary.exists())
        self.assertTrue(unknown.exists())
        self.assertEqual([], list(self.target.iterdir()))

    def test_canonical_and_alias_collision_fails_closed(self):
        canonical = self.source / "Cards__Same.md"
        compatibility = self.source / "Cards_Same.md"
        canonical.write_text("canonical", encoding="utf-8")
        compatibility.write_text("compatibility", encoding="utf-8")

        self.scan(4)

        self.assertTrue(canonical.exists())
        self.assertTrue(compatibility.exists())
        self.assertEqual([], list(self.target.iterdir()))
        log = self.log_file.read_text(encoding="utf-8")
        self.assertEqual(1, log.count('"event":"ALIAS_COLLISION"'))
        self.assertNotIn("Same__001.md", log)

    def test_plain_files_and_directories_are_untouched(self):
        plain = self.source / "history.md"
        directory = self.source / "history-dir"
        plain.write_text("history", encoding="utf-8")
        directory.mkdir()

        self.scan(3)

        self.assertEqual("history", plain.read_text(encoding="utf-8"))
        self.assertTrue(directory.is_dir())
        self.assertEqual([], list(self.target.iterdir()))

    def test_unknown_project_stays_and_warns_once(self):
        unknown = self.source / "Unknown__Task.md"
        unknown.write_text("unknown", encoding="utf-8")

        self.scan(4)

        self.assertTrue(unknown.exists())
        log = self.log_file.read_text(encoding="utf-8")
        self.assertEqual(1, log.count('"event":"UNKNOWN_PROJECT"'))
        self.assertEqual([], list(self.target.iterdir()))

    def test_meaningful_events_rotate_without_moving_unknown_sources(self):
        unknown_sources = []
        for index in range(20):
            path = self.source / f"Unknown{index:02d}__{'x' * 70}.md"
            path.write_text("unknown", encoding="utf-8")
            unknown_sources.append(path)

        self.scan()

        self.assertTrue(self.log_file.with_name(self.log_file.name + ".1").is_file())
        self.assertTrue(all(path.is_file() for path in unknown_sources))
        self.assertEqual([], list(self.target.iterdir()))

    def test_collision_never_overwrites_existing_file(self):
        existing = self.target / "Task.md"
        source = self.source / "Cards__Task.md"
        existing.write_text("old", encoding="utf-8")
        source.write_text("new", encoding="utf-8")

        self.scan(2)

        self.assertEqual("old", existing.read_text(encoding="utf-8"))
        self.assertEqual("new", (self.target / "Task__001.md").read_text(encoding="utf-8"))
        log = self.log_file.read_text(encoding="utf-8")
        self.assertIn('"event":"COLLISION_RENAMED"', log)

    def test_incomplete_files_and_changing_files_are_not_moved_early(self):
        temporary_files = [
            self.source / "Cards__download.crdownload",
            self.source / "Cards__download.part",
            self.source / "Cards__download.tmp",
        ]
        for path in temporary_files:
            path.write_text("partial", encoding="utf-8")

        changing = self.source / "Cards__Changing.md"
        changing.write_text("a", encoding="utf-8")
        self.scan()
        self.assertTrue(changing.exists())

        changing.write_text("longer", encoding="utf-8")
        self.scan()
        self.assertTrue(changing.exists())

        self.scan()
        self.assertFalse(changing.exists())
        self.assertEqual("longer", (self.target / "Changing.md").read_text(encoding="utf-8"))
        self.scan(2)
        self.assertTrue(all(path.exists() for path in temporary_files))

    def test_restart_processes_a_valid_file_already_in_source(self):
        self.router.close()
        waiting = self.source / "Cards__Waiting.md"
        waiting.write_text("waiting", encoding="utf-8")

        restarted = InboxRouter(self.config)
        self.router = restarted
        self.scan(2)

        self.assertFalse(waiting.exists())
        self.assertEqual("waiting", (self.target / "Waiting.md").read_text(encoding="utf-8"))

    def test_new_project_requires_config_only(self):
        second_target = self.root / "second-target"
        second_target.mkdir()
        raw = json.loads(self.config_path.read_text(encoding="utf-8"))
        raw["routes"]["Extra"] = str(second_target)
        self.config_path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")

        self.router.close()
        self.config = load_config(self.config_path)
        self.router = InboxRouter(self.config)
        source = self.source / "Extra_Task.txt"
        source.write_text("second", encoding="utf-8")
        self.scan(2)

        self.assertEqual("second", (second_target / "Task.txt").read_text(encoding="utf-8"))

    def test_idle_scans_do_not_create_polling_log_noise(self):
        self.scan(5)
        self.assertTrue(self.log_file.exists())
        self.assertEqual("", self.log_file.read_text(encoding="utf-8"))

    def test_successful_route_emits_content_free_collision_resolved_event(self):
        spool = self.root / "spool"
        existing = self.target / "Task.md"
        existing.write_text("old", encoding="utf-8")
        source = self.source / "Cards__Task.md"
        source.write_text("secret-like-body-must-not-enter-event", encoding="utf-8")
        self.router.close()
        self.router = InboxRouter(self.config, event_sink=FileRouteEventSink(spool))

        self.scan(2)

        events = list(spool.glob("*.json"))
        self.assertEqual(1, len(events))
        payload_text = events[0].read_text(encoding="utf-8")
        payload = json.loads(payload_text)
        self.assertEqual("Cards", payload["route_name"])
        self.assertEqual("Task.md", payload["requested_target_name"])
        self.assertTrue(payload["actual_target_path"].endswith("Task__001.md"))
        self.assertTrue(payload["collision_renamed"])
        self.assertNotIn("secret-like-body", payload_text)

    def test_canonical_and_alias_emit_equal_normalized_route_facts(self):
        events = []
        self.router.close()
        self.router = InboxRouter(self.config, event_sink=events.append)

        canonical = self.source / "Cards__Equal_name.md"
        canonical.write_text("canonical", encoding="utf-8")
        self.scan(2)
        (self.target / "Equal_name.md").unlink()

        compatibility = self.source / "Cards_Equal_name.md"
        compatibility.write_text("compatibility", encoding="utf-8")
        self.scan(2)

        self.assertEqual(2, len(events))
        normalized = [
            (event.route_name, event.requested_target_name, event.collision_renamed)
            for event in events
        ]
        self.assertEqual([("Cards", "Equal_name.md", False)] * 2, normalized)

    def test_cli_routes_alias_in_real_temporary_filesystem(self):
        source = self.source / "Cards_CLI_probe.md"
        source.write_text("cli", encoding="utf-8")
        self.router.close()

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "router.py"),
                "--config",
                str(self.config_path),
                "--max-scans",
                "2",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.router = InboxRouter(self.config)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertFalse(source.exists())
        self.assertEqual("cli", (self.target / "CLI_probe.md").read_text(encoding="utf-8"))

    def test_event_failure_keeps_successful_move_for_reconciliation(self):
        source = self.source / "Cards__CrashGap.md"
        source.write_text("payload", encoding="utf-8")

        def fail_event(_result):
            raise OSError("forced event sink failure")

        self.router.close()
        self.router = InboxRouter(self.config, event_sink=fail_event)
        self.scan(2)

        self.assertFalse(source.exists())
        self.assertEqual("payload", (self.target / "CrashGap.md").read_text(encoding="utf-8"))
        self.assertIn(
            '"event":"EVENT_PERSIST_FAILED"',
            self.log_file.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
