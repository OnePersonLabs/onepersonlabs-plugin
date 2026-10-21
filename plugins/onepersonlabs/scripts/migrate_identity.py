#!/usr/bin/env python3
"""Explicit, one-time migration of the previous plugin's local owned state.

Run after pause-for-refresh and before uninstalling the previous package. This
does not provide a runtime alias or change unrelated profiles and preferences.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
import tomllib


def atomic(path: Path, data: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix='.identity-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def map_path(value: str, mappings: list[tuple[Path, Path]]) -> str:
    for old, new in mappings:
        for before, after in [(str(old), str(new)), (old.as_posix(), new.as_posix())]:
            compared = value.casefold() if os.name == 'nt' else value
            prefix = before.casefold() if os.name == 'nt' else before
            if compared == prefix or compared.startswith(prefix + '/') or compared.startswith(prefix + '\\'):
                return after + value[len(before):]
    return value


def map_json(value, mappings):
    if isinstance(value, str):
        return map_path(value, mappings)
    if isinstance(value, list):
        return [map_json(item, mappings) for item in value]
    if isinstance(value, dict):
        return {key: map_json(item, mappings) for key, item in value.items()}
    return value


def legacy_roles(config: dict) -> list[str]:
    owned = []
    for name, entry in config.get('agents', {}).items():
        if not name.startswith('opl-') or not isinstance(entry, dict):
            continue
        filename = entry.get('config_file')
        if not isinstance(filename, str):
            continue
        path = Path(filename)
        manifest = path.parent.parent / '.codex-plugin/plugin.json'
        if (not path.is_absolute() or path.suffix != '.toml' or path.stem != name
                or path.parent.name != 'agents' or path.is_symlink() or path.parent.is_symlink()
                or not manifest.is_file() or manifest.is_symlink()):
            continue
        if json.loads(manifest.read_text(encoding='utf-8-sig')).get('name') == 'opl':
            owned.append(name)
    return owned


def migrated_config(data: bytes, home: Path, version: str, owned: list[str], root_mappings=()) -> bytes:
    text = data.decode('utf-8-sig')
    headers = list(re.finditer(r'(?m)^\[[^\n]+\][ \t]*\r?$', text))
    for index in reversed(range(len(headers))):
        header = headers[index]
        for name in owned:
            if header.group().strip() in (f'[agents.{name}]', f'[agents."{name}"]', f"[agents.'{name}']"):
                end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
                text = text[:header.start()] + text[end:]
                break
    old_config = tomllib.loads(data.decode('utf-8-sig'))
    for previous in old_config.get('projects', {}):
        current = map_path(previous, list(root_mappings))
        if current != previous:
            if current in old_config['projects']:
                raise ValueError('renamed project already has a configuration entry')
            for before, after in [(json.dumps(previous), json.dumps(current)),
                                  ("'" + previous + "'", "'" + current + "'")]:
                text = text.replace('[projects.' + before + ']', '[projects.' + after + ']')
    # Preserve disabled-skill intent across the identity/version replacement.
    for entry in old_config.get('skills', {}).get('config', []):
        if not isinstance(entry, dict) or not isinstance(entry.get('path'), str):
            continue
        previous = entry['path']
        path = Path(previous)
        old_cache = home / 'plugins/cache/opl/opl'
        try:
            relative = path.relative_to(old_cache)
        except ValueError:
            continue
        if len(relative.parts) < 2:
            raise ValueError('invalid previous plugin skill path')
        current = home / 'plugins/cache/onepersonlabs/onepersonlabs' / version / Path(*relative.parts[1:])
        # Replace only the exact TOML string representing this owned path.
        for before, after in [(json.dumps(previous), json.dumps(str(current))),
                              ("'" + previous + "'", "'" + str(current) + "'")]:
            text = text.replace(before, after)
    new_config = tomllib.loads(text)
    expected = json.loads(json.dumps(old_config))
    if 'projects' in expected:
        expected['projects'] = {map_path(key, list(root_mappings)): value for key, value in expected['projects'].items()}
    for name in owned:
        expected['agents'].pop(name)
    for entry in expected.get('skills', {}).get('config', []):
        if isinstance(entry, dict) and isinstance(entry.get('path'), str):
            try:
                relative = Path(entry['path']).relative_to(home / 'plugins/cache/opl/opl')
            except ValueError:
                continue
            entry['path'] = str(home / 'plugins/cache/onepersonlabs/onepersonlabs' / version / Path(*relative.parts[1:]))
    if expected != new_config:
        raise ValueError('configuration migration would change unrelated preferences')
    destinations = set()
    for entry in new_config.get('skills', {}).get('config', []):
        if not isinstance(entry, dict) or not isinstance(entry.get('path'), str):
            continue
        destination = Path(entry['path'])
        if destination in destinations:
            raise ValueError(f'conflicting skills.config destination requires explicit resolution: {destination}')
        destinations.add(destination)
    return text.encode('utf-8')


def runtime_paths(home: Path) -> tuple[Path, Path]:
    if os.name == 'nt':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local'))
        old, new = base / 'OPL/human-inbox', base / 'OnePersonLabs/human-inbox'
    else:
        base = Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state'))
        old, new = base / 'opl/human-inbox', base / 'onepersonlabs/human-inbox'
    return (Path(os.environ.get('OPL_HUMAN_RUNTIME', old)).expanduser().resolve(),
            Path(os.environ.get('ONEPERSONLABS_HUMAN_RUNTIME', new)).expanduser().resolve())


def migrate_home(home: Path, backups: Path, root_mappings=()) -> dict:
    home = home.resolve()
    backups = backups.resolve()
    backups.mkdir(parents=True, exist_ok=True)
    moves = [(home / 'opl', home / 'onepersonlabs'), runtime_paths(home)]
    prepared_json = {}
    for old, new in moves:
        if old.exists() and (old.is_symlink() or (new != old and new.exists())):
            raise ValueError(f'migration source is linked or destination already exists: {old} -> {new}')
        if backups.is_relative_to(old) or backups.is_relative_to(new):
            raise ValueError('backup directory must be outside state migration targets')
        if old.exists():
            for filename in old.rglob('*'):
                if filename.is_symlink() or getattr(filename, 'is_junction', lambda: False)():
                    raise ValueError(f'linked migration state requires explicit resolution: {filename}')
                if filename.is_file() and filename.suffix == '.json':
                    prepared_json[filename] = json.loads(filename.read_text(encoding='utf-8-sig'))
    old_runtime, _ = runtime_paths(home)
    if old_runtime.exists():
        record = old_runtime / 'refresh-state.json'
        if not record.is_file():
            raise ValueError('pause-for-refresh must record service state before migration')
        state = json.loads(record.read_text())
        receipt = old_runtime / 'service.json'
        if state.get('was_running') and receipt.exists():
            # pause-for-refresh has already proved shutdown. Its retained record
            # is required by resume-after-refresh, and must travel with the catalog.
            if not isinstance(state.get('workspace'), str):
                raise ValueError('invalid refresh lifecycle record')
    config = home / 'config.toml'
    original = config.read_bytes()
    owned = legacy_roles(tomllib.loads(original.decode('utf-8-sig')))
    manifest = Path(__file__).resolve().parents[1] / '.codex-plugin/plugin.json'
    version = json.loads(manifest.read_text())['version']
    replacement = migrated_config(original, home, version, owned, root_mappings)
    backup_config = backups / 'config.before-identity.toml'
    if backup_config.exists():
        raise ValueError('migration recovery already exists; reconcile before retry')
    backup_config.write_bytes(original)
    journal = backups / 'progress.json'
    progress = {'state': 'prepared', 'moves': [], 'config': str(config)}
    atomic(journal, (json.dumps(progress, indent=2) + '\n').encode())
    mappings = [*moves, *root_mappings]
    moved = []
    for index, (old, new) in enumerate(moves):
        if not old.exists():
            continue
        shutil.copytree(old, backups / f'state-{index}', symlinks=True)
        new.parent.mkdir(parents=True, exist_ok=True)
        if old != new:
            old.rename(new)
        moved.append(str(new))
        progress['moves'].append({'from': str(old), 'to': str(new)})
        atomic(journal, (json.dumps(progress, indent=2) + '\n').encode())
        for previous, value in prepared_json.items():
            if not previous.is_relative_to(old):
                continue
            filename = new / previous.relative_to(old)
            updated = map_json(value, mappings)
            if updated != value:
                atomic(filename, (json.dumps(updated, indent=2) + '\n').encode())
    _, runtime = runtime_paths(home)
    catalog = runtime / 'catalog.sqlite3'
    if catalog.exists():
        with closing(sqlite3.connect(catalog)) as database:
            for identifier, previous in database.execute('SELECT id,path FROM workspaces').fetchall():
                current = map_path(previous, list(root_mappings))
                if current != previous:
                    database.execute('UPDATE workspaces SET path=? WHERE id=?', (current, identifier))
            database.commit()
    # Compare-and-swap: concurrent configuration edits must not be overwritten.
    if config.read_bytes() != original:
        raise ValueError('configuration changed during migration; retain recovery and reconcile')
    if replacement != original:
        atomic(config, replacement)
    result = {'home': str(home), 'moved': moved, 'retired_owned_roles': owned,
              'config_sha256': hashlib.sha256(config.read_bytes()).hexdigest(),
              'backup': str(backups)}
    (backups / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    progress['state'] = 'complete'
    atomic(journal, (json.dumps(progress, indent=2) + '\n').encode())
    return result


def migrate_project(root: Path, backups: Path) -> dict:
    root = root.resolve(); backups = backups.resolve()
    pending = [(root / '.opl', root / '.onepersonlabs'), (root / '.borg', root / '.all-your-base')]
    for old, new in pending:
        if old.exists() and (old.is_symlink() or new.exists()):
            raise ValueError(f'project migration collision or linked source: {old}')
        if backups.is_relative_to(old) or backups.is_relative_to(new):
            raise ValueError('backup must be outside project state')
    moved = []
    for old, new in pending:
        if not old.exists():
            continue
        backups.mkdir(parents=True, exist_ok=True)
        target = backups / old.name.lstrip('.')
        if target.exists():
            raise ValueError('project recovery exists; reconcile before retry')
        shutil.copytree(old, target, symlinks=True)
        old.rename(new)
        moved.append(str(new))
        ignore = root / '.gitignore'
        if ignore.exists():
            text = ignore.read_text()
            updated = text.replace('/.opl/', '/.onepersonlabs/').replace('/.borg/', '/.all-your-base/')
            if updated != text:
                atomic(ignore, updated.encode())
    return {'project': str(root), 'moved': moved}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path)
    parser.add_argument('--project', type=Path)
    parser.add_argument('--backup-root', type=Path, required=True)
    parser.add_argument('--rename-root', action='append', default=[], metavar='OLD=NEW')
    args = parser.parse_args()
    if bool(args.home) == bool(args.project):
        parser.error('select exactly one of --home or --project')
    mappings = [tuple(Path(value) for value in item.split('=', 1)) for item in args.rename_root]
    if any(len(item) != 2 for item in mappings):
        parser.error('each --rename-root needs OLD=NEW')
    result = migrate_home(args.home, args.backup_root, mappings) if args.home else migrate_project(args.project, args.backup_root)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
