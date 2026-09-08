"""Read-only, bounded candidate preflight. Never print matched secret values."""
import argparse
from collections import Counter
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

SECRET = re.compile(r'\b(?:sk[-_]|ghp_|github_pat_)[A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
ASSIGNMENT = re.compile(r'''(?i)(?:api[_-]?key|password|app[_-]?secret|authorization|cookie)\s*[:=]\s*["']([^"'\r\n]{8,})["']''')
BEARER = re.compile(r'(?i)\bBearer\s+[A-Za-z0-9._~+/-]{16,}')
WINDOWS = re.compile(r'\b[A-Za-z]:[\\/]')
UUID = re.compile(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b', re.I)
IP = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
URL = re.compile(r'''https?://([^/\s)'"<>]+)''', re.I)
KEYWORDS = re.compile(r'(?i)\b(?:secret|token|cookie|authorization|bearer|api[_-]?key|openid|session_meta)\b')
FORBIDDEN_DIRS = {'.git', '.codex', 'sessions', 'archived_sessions', 'private', 'logs', 'evidence', '__pycache__', '.venv'}
FORBIDDEN_SUFFIXES = {'.db', '.sqlite', '.sqlite3', '.jsonl', '.log', '.pyc', '.pem', '.key', '.png', '.jpg', '.zip'}
PUBLIC_BINARY_ASSETS = {'assets/social-preview.png'}
GENERATED = {'observations.json', 'observations.md', 'readiness.json'}
TEXT_SUFFIXES = {'.md', '.py', '.json', '.txt', '.yaml', '.yml', '.toml', '.svg'}
MANIFEST = 'docs/asset-manifest.json'
PUBLIC_REFERENCE_HOSTS = {'learn.chatgpt.com', 'developers.openai.com', 'docs.github.com', 'choosealicense.com', 'www.apache.org', 'www.w3.org', 'github.com', 'agentskills.io'}


def scan(root, require_manifest=True):
    root = Path(root).resolve(strict=True)
    findings = []
    files = {}
    def add(path, category, rule, line=None):
        findings.append({'path': path, 'category': category, 'rule': rule, 'line': line})
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        # Never dereference outside the candidate, including linked directories.
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            add(rel, 'confirmed secret/private', 'linked_path'); continue
        if path.is_dir():
            if path.name in FORBIDDEN_DIRS:
                add(rel, 'confirmed secret/private', 'private_or_generated_directory')
            continue
        if not path.is_file():
            add(rel, 'suspicious', 'non_regular_file'); continue
        files[rel] = path
        if (path.name.startswith('.env') or path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name in GENERATED) and rel not in PUBLIC_BINARY_ASSETS:
            add(rel, 'confirmed secret/private', 'private_or_generated_file'); continue
        if any(part in FORBIDDEN_DIRS for part in path.relative_to(root).parts):
            continue
        if path.stat().st_size > 4 * 1024 * 1024:
            add(rel, 'suspicious', 'oversized_unreviewed_file'); continue
        if rel in PUBLIC_BINARY_ASSETS:
            data = path.read_bytes()
            valid_png = (
                len(data) >= 24
                and data[:8] == b'\x89PNG\r\n\x1a\n'
                and data[12:16] == b'IHDR'
                and struct.unpack('>II', data[16:24]) == (1280, 640)
            )
            if not valid_png:
                add(rel, 'suspicious', 'invalid_public_binary')
            else:
                add(rel, 'safe', 'allowlisted_original_public_binary')
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and rel not in {'.gitignore', 'LICENSE'}:
            add(rel, 'suspicious', 'unknown_file_type'); continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError):
            add(rel, 'suspicious', 'unreadable_or_binary'); continue
        had_finding = False
        for number, line in enumerate(text.splitlines(), 1):
            if SECRET.search(line) or BEARER.search(line):
                add(rel, 'confirmed secret/private', 'credential_shape', number); had_finding = True
            if ASSIGNMENT.search(line):
                add(rel, 'suspicious', 'credential_assignment', number); had_finding = True
            if WINDOWS.search(line) or UUID.search(line):
                add(rel, 'suspicious', 'absolute_path_or_real_identity', number); had_finding = True
            for value in IP.findall(line):
                try: address = ipaddress.ip_address(value)
                except ValueError: continue
                documented = any(address in ipaddress.ip_network(net) for net in ('192.0.2.0/24','198.51.100.0/24','203.0.113.0/24','127.0.0.0/8'))
                add(rel, 'expected synthetic/example' if documented else 'suspicious', 'ip_reference', number); had_finding = True
            for host in URL.findall(line):
                host = host.rstrip('.,')
                expected = host in {'example.com','example.org','localhost'} or host.endswith('.example') or bool(re.fullmatch(r'(?:localhost|127\.0\.0\.1)(?::\d+)?', host))
                public_reference = host in PUBLIC_REFERENCE_HOSTS
                category = 'safe' if public_reference else ('expected synthetic/example' if expected else 'suspicious')
                add(rel, category, 'reviewed_public_reference' if public_reference else 'hostname_reference', number); had_finding = True
        if not had_finding:
            add(rel, 'expected synthetic/example' if KEYWORDS.search(text) else 'safe', 'keyword_only_reference' if KEYWORDS.search(text) else 'no_pattern_hit')
    if require_manifest:
        try:
            manifest = json.loads((root / MANIFEST).read_text(encoding='utf-8'))
            entries = manifest['assets']
            declared = {item['path']: item for item in entries}
            if len(declared) != len(entries): raise ValueError('duplicate')
            actual = set(files) - {MANIFEST}
            if set(declared) != actual:
                add(MANIFEST, 'suspicious', 'unmapped_or_missing_assets')
            for rel, item in declared.items():
                path = files.get(rel)
                if not path or path.is_symlink() or not path.resolve().is_relative_to(root): continue
                if not item.get('origin') or not item.get('transformation'):
                    add(rel, 'suspicious', 'missing_provenance')
                if path.stat().st_size > 4 * 1024 * 1024: continue
                if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                    add(rel, 'suspicious', 'manifest_hash_mismatch')
        except (OSError, ValueError, TypeError, KeyError):
            add(MANIFEST, 'suspicious', 'invalid_or_missing_manifest')
    counts = dict(Counter(item['category'] for item in findings))
    return {'files': len(files), 'categories': counts, 'findings': findings,
            'passed': not any(item['category'] in ('confirmed secret/private','suspicious') for item in findings)}


def scan_tracked(root):
    """Scan actual index blobs; only root Git metadata is outside the push tree."""
    root = Path(root).resolve(strict=True)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL)
    if Path(git('rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
        raise ValueError('not exact repository root')
    if (root/'.git').is_symlink() or not (root/'.git').is_dir():
        raise ValueError('unexpected Git metadata')
    entries = {}
    for record in git('ls-files', '--stage', '-z').split(b'\0'):
        if not record: continue
        meta, raw = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        rel = raw.decode('utf-8')
        if mode not in {'100644','100755'} or stage != '0' or rel in entries:
            raise ValueError('unsupported index entry')
        target = root/rel
        if target.is_symlink() or not target.resolve().is_relative_to(root):
            raise ValueError('unsafe tracked path')
        blob = git('cat-file', 'blob', oid)
        if not target.is_file() or target.read_bytes() != blob:
            raise ValueError('working tree differs from staged bytes')
        entries[rel] = blob
    actual = set()
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if rel.parts[0] == '.git': continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('linked working tree asset')
        if path.is_file(): actual.add(rel.as_posix())
    if actual != set(entries): raise ValueError('untracked or missing files outside Git metadata')
    with tempfile.TemporaryDirectory(prefix='public-index-scan-') as temp:
        clean = Path(temp)
        for rel, blob in entries.items():
            target = clean/rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(blob)
        result = scan(clean)
    result['scope'] = 'exact staged blobs; working tree byte equality; root Git metadata excluded'
    result['tracked_files'] = len(entries)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--tracked', action='store_true', help='Require an exact Git index/worktree and scan the staged public tree')
    args = parser.parse_args()
    try:
        result = scan_tracked(args.root) if args.tracked else scan(args.root)
    except (OSError, ValueError, subprocess.SubprocessError):
        print(json.dumps({'passed': False, 'error': 'candidate_unreadable'})); raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
