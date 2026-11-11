"""Atomic draft documents, meaningful revisions and isolated recovery copies."""
import copy
import datetime as dt
import json
import re
import uuid
import save_system

VERSION = 1
MAX_BYTES = 2_000_000
HISTORY_LIMIT = 40


def new():
    return dict(version=VERSION, id=uuid.uuid4().hex, generation=0, current={}, autosave=None,
                revisions=[], ideas=[], locks=[], updated='')


def path(root, ident):
    if not isinstance(ident, str) or not re.fullmatch(r'[0-9a-f]{32}', ident):
        raise ValueError('Invalid draft identity.')
    return root / (ident + '.json')


def validate(doc):
    if not isinstance(doc, dict) or doc.get('version') != VERSION:
        raise ValueError('Unsupported draft format; the original file has been preserved.')
    path(__import__('pathlib').Path('.'), doc.get('id'))
    if not isinstance(doc.get('current'), dict) or not isinstance(doc.get('revisions'), list):
        raise ValueError('Invalid draft data.')
    if type(doc.get('generation')) is not int or doc['generation'] < 0:
        raise ValueError('Invalid draft recovery generation.')
    for revision in doc['revisions']:
        if not isinstance(revision, dict) or not isinstance(revision.get('snapshot'), dict) or any(not isinstance(revision.get(k), str) for k in ('id','at','label')):
            raise ValueError('Invalid revision data; the original history has been preserved.')
    auto = doc.get('autosave')
    if auto is not None and (not isinstance(auto, dict) or not isinstance(auto.get('snapshot'), dict) or type(auto.get('generation')) is not int):
        raise ValueError('Invalid recovery copy; the original file has been preserved.')
    return copy.deepcopy(doc)


def write(root, doc, expected=None):
    data = json.dumps(validate(doc), ensure_ascii=False, indent=2).encode('utf-8')
    if len(data) > MAX_BYTES:
        raise ValueError('Draft exceeds the 2 MB limit. Remove unused unpinned revisions or long ideas.')
    target = path(root, doc['id'])
    if expected is not None and target.exists():
        # JSON normalisation accounts for in-memory signature tuples becoming
        # arrays on disk. Refuse stale autosaves as well as stale manual saves.
        current = read(root, doc['id'])
        if current != json.loads(json.dumps(expected)):
            raise ValueError('Draft changed in another editor. Changes remain open; use Save draft as copy or reopen the latest draft.')
    save_system.atomic(target, data)


def read(root, ident):
    file = path(root, ident)
    if file.stat().st_size > MAX_BYTES:
        raise ValueError('Draft exceeds the supported 2 MB limit.')
    return validate(json.loads(file.read_text(encoding='utf-8')))


def listing(root):
    drafts, errors = [], []
    for file in sorted(root.glob('*.json')):
        try:
            drafts.append(read(root, file.stem))
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f'{file.name}: {exc}')
    return drafts, errors


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def checkpoint(doc, snapshot, label, pinned=False):
    result = validate(doc)
    if not result['revisions'] or result['revisions'][-1]['snapshot'] != snapshot:
        result['revisions'].append(dict(id=uuid.uuid4().hex, at=stamp(), label=label,
                                        pinned=pinned, snapshot=copy.deepcopy(snapshot)))
    ordinary = [r['id'] for r in result['revisions'] if not r.get('pinned')]
    expired = set(ordinary[:-HISTORY_LIMIT])
    result['revisions'] = [r for r in result['revisions'] if r['id'] not in expired]
    return result


def save(root, doc, snapshot, label='Manual save', _expected=None):
    result = checkpoint(doc, snapshot, label)
    result.update(current=copy.deepcopy(snapshot), autosave=None, updated=stamp(), generation=doc['generation']+1)
    write(root, result, expected=doc if _expected is None else _expected)
    return result


def autosave(root, doc, snapshot):
    result = validate(doc)
    result['autosave'] = dict(snapshot=copy.deepcopy(snapshot), at=stamp(), generation=doc['generation'])
    result['updated'] = stamp()
    write(root, result, expected=doc)
    return result


def restore(root, doc, revision_id, current):
    # Resolve before adding a checkpoint: retention may evict the selected oldest
    # ordinary revision while preserving the pre-restore working snapshot.
    revision = next((r for r in doc['revisions'] if r['id'] == revision_id), None)
    if revision is None:
        raise ValueError('That revision is no longer available.')
    result = checkpoint(doc, current, 'Before restore')
    return save(root, result, revision['snapshot'], 'Restored ' + revision['label'], _expected=doc)


def pin(root, doc, revision_id, pinned):
    """Atomically change retention without changing working/recovery snapshots."""
    result = validate(doc)
    revision = next((r for r in result['revisions'] if r['id'] == revision_id), None)
    if revision is None:
        raise ValueError('That revision is no longer available.')
    revision['pinned'] = bool(pinned)
    result['updated'] = stamp()
    write(root, result, expected=doc)
    return result


def recovery(doc):
    auto = doc.get('autosave')
    if auto and auto.get('generation') == doc['generation'] and auto['snapshot'] != doc['current']:
        return copy.deepcopy(auto['snapshot'])
    return None


class Undo:
    def __init__(self):
        self.past, self.future = [], []

    def record(self, snapshot):
        if not self.past or self.past[-1] != snapshot:
            self.past.append(copy.deepcopy(snapshot))
            self.past = self.past[-80:]
            self.future.clear()

    def undo(self, current):
        while self.past and self.past[-1] == current:
            self.past.pop()
        if not self.past: return current
        self.future.append(copy.deepcopy(current))
        return copy.deepcopy(self.past.pop())

    def redo(self, current):
        if not self.future: return current
        self.past.append(copy.deepcopy(current))
        return copy.deepcopy(self.future.pop())
