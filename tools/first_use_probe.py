"""Prepare a fresh synthetic project and verify local Codex skill discovery only.

No model request, login, private history, account copy or remote operation.
The result is NOT end-to-end AI first-use or human acceptance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time


def prepare(candidate, workspace):
    candidate = Path(candidate).resolve(strict=True)
    workspace = Path(workspace).resolve()
    if workspace.exists() or workspace.is_relative_to(candidate) or candidate.is_relative_to(workspace):
        raise ValueError('workspace must be new and outside candidate')
    required = ['README.md', 'docs/QUICK_START.md', 'workflows/default/SKILL.md', 'core/MEMORY_CONTRACT.md']
    for rel in required:
        if not (candidate / rel).is_file():
            raise ValueError('required candidate file missing')
    workspace.mkdir(parents=True)
    for name in ['Inbox', 'Handoffs', 'docs', '.agents/skills']:
        (workspace / name).mkdir(parents=True, exist_ok=True)
    shutil.copytree(candidate / 'workflows/default', workspace / '.agents/skills/default', ignore=shutil.ignore_patterns('README.md'))
    (workspace / '.agents/core').mkdir()
    shutil.copyfile(candidate / 'core/MEMORY_CONTRACT.md', workspace / '.agents/core/MEMORY_CONTRACT.md')
    # Carry optional linked Core contracts with the copied memory contract.
    # Legacy candidates without these additions remain valid.
    for name in ['TRUTH_MODEL.md', 'CONTEXT_PROJECTION.md']:
        if (candidate / 'core' / name).is_file():
            shutil.copyfile(candidate / 'core' / name, workspace / '.agents/core' / name)
    helper = candidate / 'tools/context_projection.py'
    if helper.is_file():
        (workspace / '.agents/tools').mkdir(exist_ok=True)
        shutil.copyfile(helper, workspace / '.agents/tools/context_projection.py')
    (workspace / 'AGENTS.md').write_text('Use the local default Skill for execution. Start with PROJECT.md.\n', encoding='utf-8')
    (workspace / 'PROJECT.md').write_text('# Example project\nproject_key = first-use-example\nCore: .agents/core/MEMORY_CONTRACT.md\nProtocol: .agents/skills/default/references/WORKFLOW.md\nStage: FIRST_USE.md\nInbox: Inbox\nHandoffs: Handoffs\nRuntime: not configured; manual mode only.\n', encoding='utf-8')
    (workspace / 'FIRST_USE.md').write_text('# First use\nGoal: one synthetic documentation change. No completed tasks or acceptance yet.\n', encoding='utf-8')
    (workspace / 'docs/setup.md').write_text('# Setup\nRun the imaginary setup.\n', encoding='utf-8')
    (workspace / 'Inbox/FIRST-001_任务单.md').write_text('# FIRST-001\nRequired Skill: $default\nMode: manual_inbox / not_registered\nGoal: clarify synthetic setup.\nScope: docs/setup.md and Handoffs/FIRST-001_报告单.md; move this Source unchanged to Handoffs only after report.\nAcceptance: replace the setup sentence with exactly: This example requires no installation.\nPermission: local scoped edits only; no network, deletion, Runtime, background work or other projects.\nReport verification and keep Main AI Acceptance PENDING.\n', encoding='utf-8')
    return workspace


def probe(candidate, workspace, codex):
    workspace = prepare(candidate, workspace)
    profile = workspace / 'isolated-profile'
    for name in ['codex', 'roaming', 'local', 'temp']:
        (profile / name).mkdir(parents=True)
    # Only an OS bootstrap environment, never a copy of account/config/secret variables.
    env = {k: os.environ[k] for k in ['SystemRoot', 'WINDIR', 'COMSPEC', 'PATHEXT'] if k in os.environ}
    env.update(HOME=str(profile), USERPROFILE=str(profile), CODEX_HOME=str(profile / 'codex'),
               APPDATA=str(profile / 'roaming'), LOCALAPPDATA=str(profile / 'local'),
               TEMP=str(profile / 'temp'), TMP=str(profile / 'temp'),
               HTTP_PROXY='http://127.0.0.1:9', HTTPS_PROXY='http://127.0.0.1:9', ALL_PROXY='http://127.0.0.1:9')
    env['PATH'] = str(Path(env.get('SystemRoot', '')) / 'System32')
    version = subprocess.run([codex, '--version'], env=env, cwd=workspace, capture_output=True, text=True, timeout=15).stdout.strip()
    process = subprocess.Popen([codex, 'app-server', '--stdio', '-c', 'cli_auth_credentials_store="file"'],
                               env=env, cwd=workspace, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True, encoding='utf-8')
    responses = queue.Queue()
    def reader():
        for line in process.stdout:
            try: responses.put(json.loads(line))
            except ValueError: pass
    threading.Thread(target=reader, daemon=True).start()
    def send(value):
        process.stdin.write(json.dumps(value) + '\n'); process.stdin.flush()
    def request(ident, method, params):
        send({'id': ident, 'method': method, 'params': params})
        deadline = time.monotonic() + 20
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0: raise queue.Empty()
            value = responses.get(timeout=remaining)
            if value.get('id') == ident:
                if 'error' in value: raise RuntimeError('app-server request failed: ' + method)
                return value['result']
    try:
        request(0, 'initialize', {'clientInfo': {'name': 'mindos_local_probe', 'version': '0.1.0'}})
        send({'method': 'initialized', 'params': {}})
        listing = request(1, 'skills/list', {'cwds': [str(workspace)], 'forceReload': True})
        account = request(2, 'account/read', {'refreshToken': False})
        data = listing['data'][0]
        skill = [s for s in data['skills'] if s['name'] == 'default']
        expected = workspace / '.agents/skills/default/SKILL.md'
        local_skill = [s for s in skill if Path(s['path']).resolve() == expected.resolve() and s['enabled']]
        correct = len(local_skill) == 1
        foreign = [s for s in data['skills'] if not Path(s['path']).resolve().is_relative_to(workspace)]
        return {'client': version, 'skill_discovery': bool(correct), 'default_named_count': len(skill), 'discovery_errors': len(data.get('errors', [])),
                'foreign_skill_count': len(foreign), 'isolated_account_present': account.get('account') is not None,
                'skill_sha256': hashlib.sha256(expected.read_bytes()).hexdigest(),
                'protocol_sha256': hashlib.sha256((workspace/'.agents/skills/default/references/WORKFLOW.md').read_bytes()).hexdigest(),
                'local_installation_verified': bool(correct) and not data.get('errors'),
                'technical_setup_verified': bool(correct) and not data.get('errors') and not foreign,
                'model_request_made': False, 'ai_task_execution': 'NOT_RUN',
                'report_created': (workspace/'Handoffs/FIRST-001_报告单.md').exists(),
                'real_external_first_use': 'PENDING: requires user-authenticated isolated client and actual AI Task/Report',
                'private_config_or_auth_copied': False, 'git_remote_or_upload': False}
    finally:
        process.terminate()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.kill(); process.wait()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--codex', required=True, help='native Codex executable, not a shell wrapper')
    args = p.parse_args()
    try:
        result = probe(args.candidate, args.workspace, args.codex)
    except (OSError, ValueError, RuntimeError, queue.Empty, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'technical_setup_verified': False, 'error_type': type(exc).__name__, 'ai_task_execution': 'NOT_RUN'}))
        raise SystemExit(2)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['technical_setup_verified'] else 1)
