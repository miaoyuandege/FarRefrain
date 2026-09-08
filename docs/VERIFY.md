# Local candidate verification

Use an already available Python 3.10+ interpreter. No dependency installation or network access is required for the included tests.

From the candidate root:

```text
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s extensions/router/tests -v
python -B -m unittest discover -s tools/history-distiller -p test_distill.py -v
python -B tools/prepublish_scan.py
```

In a Git checkout, stage only the explicit reviewed manifest inventory and use `python -B tools/prepublish_scan.py --tracked`. This scans actual staged blobs, checks byte-for-byte equality with working files and rejects untracked files (including ignored files) outside root `.git` metadata. Submodules/symlinks/unmerged entries are not accepted. The manifest still excludes only itself from content hashing. Never stage a parent workspace, private evidence or an unreviewed file to make a check pass. The default filesystem scan continues to reject Git metadata; it is for a pre-init source tree or clean exported snapshot.

The preflight checks the entire candidate, including ignored files; manifest coverage/content hashes; known secret/private/path risks; unexpected generated/binary data; and links in tests. It prints rule categories and locations, never matched secret values. Confirmed or unresolved suspicious findings block success. Synthetic examples and keyword-only references are classified separately. It cannot recognize all possible private prose; maintainer allowlist review is still essential.

Only the manifest itself is excluded from recursive content hashing. After an intentional reviewed change, explicitly regenerate `docs/asset-manifest.json` with per-file origin/transformation and public SHA256; review the difference. There is no automatic source sync or manifest updater that silently blesses unknown files.

Skill schema validation is an additional maintainer check using the existing skill-creator validator when available. Passing these local checks does not grant a license or authorize publishing.

The modular suite exercises files-only authorized update/fresh recovery, installed Skill/contract hashes and every installed resource link, synthetic lifecycle truth boundaries, and adding/removing a real Router copy without changing Core or workflow memory. Only temporary fixtures are mutated. Native discovery, authenticated AI execution and external human acceptance remain separate from these deterministic checks.

## Native local-discovery probe (optional, not first-use PASS)

`tools/first_use_probe.py --workspace NEW_OUTSIDE_DIRECTORY --codex NATIVE_EXECUTABLE` prepares a synthetic Task and project, copies only reviewed protocol/Skill/templates, then invokes a short-lived native app-server over stdio. Run it with Python and an explicit native Codex executable path, not a PowerShell wrapper. No daemon, account copy, login or model request is made. Generated workspaces stay outside the candidate and are retained for inspection; existing paths are refused.

The child receives an allowlisted OS environment, empty profile/config locations and loopback proxy endpoints. OS-level user resources may still be discovered on Windows: this is detected and fails the clean setup check. The probe reports local Skill loading separately from isolation and account state. Exit 0 means setup/discovery only, not AI understanding, Task execution, Report generation or human acceptance. Any outside Skill metadata or setup failure returns nonzero.

To complete real first-use later, use an actually isolated authorized user/client, authenticate directly without copying account files, inspect `/skills`, say “接管这个项目”, then “执行任务” for the synthetic Task. Verify the exact setup sentence, real single report, raw Source hash preservation, absence of unrelated changes and user acceptance. Keep that evidence private. No release freeze until this gate is resolved.
