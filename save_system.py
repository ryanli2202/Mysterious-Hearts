"""Story storage, recovery checkpoints and portable story bundles."""
import contextlib
import datetime as dt
import json
import os
from pathlib import Path
import re
import tempfile
import threading
import time
import uuid
import zipfile

_MUTEX = threading.RLock()

@contextlib.contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True)
    with _MUTEX, (root / '.save.lock').open('a+b') as stream:
        if os.fstat(stream.fileno()).st_size == 0:
            stream.write(b'0'); stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX)
        try: yield
        finally:
            stream.seek(0)
            if os.name == 'nt': msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else: fcntl.flock(stream, fcntl.LOCK_UN)

def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.stem+'-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)

def identity(state):
    value = state.get('story_id')
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{32}', value):
        value = state['story_id'] = uuid.uuid4().hex
    return value

def checkpoints(path):
    if not path.exists(): return
    try:
        data = path.read_bytes()
        state = json.loads(data)
        if not isinstance(state, dict) or 'routes' not in state: return
    except (ValueError, OSError): return
    recent = path.parent / 'recent'
    daily = path.parent / 'daily'
    now = time.time()
    previous = sorted(recent.glob('*.json')) if recent.exists() else []
    if not previous or now - previous[-1].stat().st_mtime >= 300:
        atomic(recent / (str(time.time_ns())+'.json'), data)
    day = dt.datetime.now().strftime('%Y-%m-%d')
    if not (daily / (day+'.json')).exists(): atomic(daily / (day+'.json'), data)
    for folder, count in ((recent, 12), (daily, 14)):
        for old in sorted(folder.glob('*.json'))[:-count]: old.unlink()

def write(state, path, active):
    import qol
    if state is None: return
    if path.is_relative_to(active.parent):
        from custom_library import remember
        remember(state, active.parent)
    with locked(active.parent if path.is_relative_to(active.parent) else path.parent):
        sid = identity(state)
        state['saved_at'] = dt.datetime.now(dt.timezone.utc).isoformat()
        data = json.dumps(state, ensure_ascii=False, indent=2).encode('utf-8')
        if path == active:
            target = active.parent / 'stories' / sid / 'autosave.json'
            checkpoints(target)
            atomic(target, data)
            atomic(active, data)
        else:
            try: qol.backup(path)
            except ValueError: pass
            atomic(path, data)

def entries(root):
    return sorted(root.rglob('*.json'), key=lambda p:p.stat().st_mtime, reverse=True)

def delete(root, selected=None):
    """Delete JSON saves only, including all snapshots of a selected story."""
    with locked(root):
        sid = None
        if selected:
            selected = selected.resolve()
            if not selected.is_relative_to(root.resolve()): raise ValueError('Invalid save location.')
            try: sid = json.loads(selected.read_text(encoding='utf-8')).get('story_id')
            except ValueError: pass
            relative = selected.relative_to(root.resolve())
            if len(relative.parts) >= 3 and relative.parts[0] == 'stories':
                sid = relative.parts[1]
        targets = []
        for path in entries(root):
            remove = selected is None or path.resolve() == selected
            if sid:
                remove |= path.is_relative_to(root / 'stories' / sid)
                try: remove |= json.loads(path.read_text(encoding='utf-8')).get('story_id') == sid
                except ValueError: pass
            if remove: targets.append(path)
        # Preserve reusable characters before deleting any story or checkpoint.
        from custom_library import remember
        for path in targets:
            try:
                state = json.loads(path.read_text(encoding='utf-8'))
                if isinstance(state, dict): remember(state, root)
            except (ValueError, KeyError, TypeError): pass
        for path in targets: path.unlink()

def recovery(root):
    active = root / 'story.json'
    sid = None
    try: sid = json.loads(active.read_text(encoding='utf-8')).get('story_id')
    except (OSError, ValueError): pass
    return [p for p in entries(root) if p != active and (not sid or sid in p.parts)]

def export_story(state, destination, root):
    files = set()
    generated = (root / 'assets' / 'generated').resolve()
    def scan(value):
        if isinstance(value, dict):
            for child in value.values(): scan(child)
        elif isinstance(value, list):
            for child in value: scan(child)
        elif isinstance(value, str) and value.replace('\\', '/').startswith('assets/generated/'):
            path = (root / value).resolve()
            if path.is_relative_to(generated) and path.is_file(): files.add(path)
    scan(state)
    album = state.get('camera', {}).get('album', '')
    if re.fullmatch('[0-9a-f]{32}', album):
        folder = generated / 'camera-albums' / album
        for path in folder.rglob('*'):
            if path.is_file() and path.resolve().is_relative_to(generated):
                files.add(path)
                if path.suffix == '.json': scan(json.loads(path.read_text(encoding='utf-8')))
    destination = Path(destination)
    fd, temp = tempfile.mkstemp(suffix='.zip', dir=destination.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as bundle:
            bundle.writestr('story.json', json.dumps(state, ensure_ascii=False))
            for path in sorted(files): bundle.write(path, path.relative_to(root).as_posix())
        os.replace(temp, destination)
    finally: Path(temp).unlink(missing_ok=True)

def import_story(source, root, save_root):
    import game_core as core
    with zipfile.ZipFile(source) as bundle:
        infos = bundle.infolist()
        if len(infos) > 10000 or sum(i.file_size for i in infos) > 1024**3:
            raise ValueError('Story bundle is too large.')
        names = [i.filename for i in infos]
        if len(set(names)) != len(names): raise ValueError('Duplicate bundle entries.')
        generated = (root / 'assets' / 'generated').resolve()
        assets = []
        for info in infos:
            if info.filename == 'story.json': continue
            path = (root / info.filename).resolve()
            if not info.filename.startswith('assets/generated/') or not path.is_relative_to(generated):
                raise ValueError('Invalid bundle asset path.')
            if info.is_dir(): continue
            data = bundle.read(info)
            if path.exists() and path.read_bytes() != data:
                raise ValueError('An existing photo conflicts with this bundle. No files were imported.')
            assets.append((path, data))
        # Run the normal compatibility checks before installing anything.
        with tempfile.TemporaryDirectory() as folder:
            check = Path(folder) / 'story.json'
            check.write_bytes(bundle.read('story.json'))
            state = core.load(check)
        state['story_id'] = uuid.uuid4().hex
        state['save_name'] = state.get('save_name', state['player'].title()) + ' (imported)'
        with locked(save_root):
            for path, data in assets:
                if not path.exists(): atomic(path, data)
            target = save_root / 'stories' / state['story_id'] / 'autosave.json'
            atomic(target, json.dumps(state, ensure_ascii=False, indent=2).encode('utf-8'))
        return target
