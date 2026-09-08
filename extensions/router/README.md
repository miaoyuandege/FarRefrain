# Inbox Router — SHIPPED, optional transport

Python 3.10+ standard library, no Runtime, network, MCP, bot or AI dependency. Windows / Python 3.12 is the exercised platform. Other OSes are unverified. This transports files only; it does not interpret, authorize or execute their contents.

Copy `router.py` and [config.example.json](config.example.json) into a new dedicated local directory. Review the config and name it `config.json`. Create its `outbox`, `project/inbox`, and `notes/inbox` directories (or set your own existing targets). Relative paths resolve against the config directory, not the shell working directory. Keep input and targets distinct, same-filesystem, trusted local directories; run only one router per source. Never point this at an unreviewed Downloads folder.

```text
python -B router.py --config config.json --check-config
python -B router.py --config config.json --max-scans 2
```

The bounded command exits after two scans; omit `--max-scans` only when you intend foreground polling. Ctrl-C stops it. No service installation or autostart occurs. Change the configuration to add a route; no code edit is needed. `--check-config` does not transport files.

- `Example__note_part__02.md` → `note_part__02.md` (canonical output naming).
- `Example_note_part__02.md` → same target (human input alias only).
- `[Example]note.md` remains accepted (legacy).
- Configured names match exactly; unknown routes and ordinary files stay untouched.
- Coexisting canonical/alias input for one target produces `ALIAS_COLLISION`; both stay, no numbered copy. Resolve the intended source manually.
- An ordinary existing target stays intact; the newcomer uses `__001`, then `__002`, etc.
- Two unchanged size/mtime scans are required; `.tmp`, `.part`, `.crdownload`, directories and symlinks are ignored. Stability is not a writer lock: producers must finish/close files before handing them off.

Windows uses no-overwrite rename. The portable branch uses atomic hard-link creation followed by source unlink to avoid POSIX rename overwrites; unsupported/cross-filesystem operations fail with the source retained. A crash between link and unlink can leave both names: stop and reconcile them before restarting, never assume exactly-once delivery. The portable branch is unit-tested on Windows via explicit injection, not OS-certified.

Logs contain filenames and transport metadata, never file bodies; optional `route_event_spool` produces local JSON events including actual destination path, size and time. Paths/names can themselves be sensitive: leave the spool disabled unless needed, keep output private, and never upload operational logs/config. Event persistence failure does not undo a completed transport; reconcile from the destination and error record.

Run `python -B -m unittest discover -s tests -v` in this module. Tests use fresh temporary files and generic route names. Repository integration tests demonstrate adding/removing the module without changing boot/current/history bytes. Removal means stop it and remove your installed module/config only; leave transported memory and unprocessed sources in place.
