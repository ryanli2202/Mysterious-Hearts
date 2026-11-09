"""Validated, offline update catalogue; reader preferences never touch story saves."""
from pathlib import Path
from datetime import date
import argparse
import hashlib
import json
import os
import tempfile

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / 'patch_notes' / 'catalog.json'
PREFERENCES = ROOT / 'patch_notes_preferences.json'
NOTICE = ('Historical entries reconstruct recoverable development, not numbered releases. '
          'Unknown release dates stay unknown. Topic order is not a verified chronology. '
          'Original reports may describe superseded behavior; their test claims are historical. '
          'The 17 oversized chats were recovered from local logs; interrupted work is labelled. '
          'No complete commit history exists.')


def validate(data):
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Unsupported patch notes schema')
    if not isinstance(data.get('releases'), list) or not data['releases']:
        raise ValueError('Patch notes require at least one entry')
    ids = set()
    for item in data['releases']:
        if not isinstance(item, dict):
            raise ValueError('Each patch note must be an object')
        for key in ('id', 'title', 'category', 'kind', 'summary', 'body', 'provenance', 'save_impact'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'Missing or invalid {key}')
        if item['id'] in ids:
            raise ValueError('Duplicate entry ID: '+item['id'])
        ids.add(item['id'])
        if item['kind'] not in ('Release', 'Retrospective', 'Development report'):
            raise ValueError('Unknown entry kind')
        if item.get('date') is not None:
            if not isinstance(item['date'], str):
                raise ValueError('Dates must be ISO date strings or null')
            date.fromisoformat(item['date'])
        if item['kind'] == 'Release' and not item.get('date'):
            raise ValueError('Published releases require an actual date')
        if not isinstance(item.get('sources'), list) or not item['sources'] or not all(isinstance(x, str) and x for x in item['sources']):
            raise ValueError('Each entry needs sources')
    return data


def load(path=CATALOG):
    return validate(json.loads(Path(path).read_text(encoding='utf-8')))['releases']


def revision(item):
    return hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def preferences(path=PREFERENCES):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        if not isinstance(data, dict) or not isinstance(data.get('read', {}), dict) or not isinstance(data.get('bookmarks', []), list):
            raise ValueError('Invalid reader preferences')
        return {'read': {k:v for k,v in data.get('read', {}).items() if isinstance(k,str) and isinstance(v,str)},
                'bookmarks': [x for x in data.get('bookmarks', []) if isinstance(x,str)]}
    except (OSError, ValueError, AttributeError, TypeError):
        return {'read': {}, 'bookmarks': []}


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name+'.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)


def save_preferences(data, path=PREFERENCES):
    atomic_write(path, json.dumps(data, indent=2))


def unread(item, prefs):
    return prefs['read'].get(item['id']) != revision(item)


def select(entries, query='', category='All categories', kind='All types', status='All entries', prefs=None, reports=False, order='Catalogue order'):
    prefs = prefs or {'read': {}, 'bookmarks': []}
    words = query.casefold().split()
    result = [r for r in entries if
              (reports or r['kind'] != 'Development report') and
              (category == 'All categories' or r['category'] == category) and
              (kind == 'All types' or r['kind'] == kind) and
              (status != 'Unread' or unread(r, prefs)) and
              (status != 'Bookmarked' or r['id'] in prefs['bookmarks']) and
              all(w in '\n'.join([r['title'], r['summary'], r['body'], *r['sources']]).casefold() for w in words)]
    if order == 'Title': result.sort(key=lambda r:r['title'].casefold())
    if order == 'Dated first': result.sort(key=lambda r:r.get('date') or '', reverse=True)
    return result


def render(item):
    date_label = item.get('date') or 'Unknown — reconstructed history'
    return (f"# {item['title']}\n\n{item['id']} | {item['kind']} | {item['category']}\n"
            f"Date: {date_label}\n\n{item['summary']}\n\n"
            f"## Details\n\n{item['body']}\n\n## Save compatibility\n\n{item['save_impact']}\n\n"
            f"## Evidence and historical limits\n\n{item['provenance']}\n\n"
            + '\n'.join('- '+s for s in item['sources'])+'\n')


def export(entries, path):
    atomic_write(path, '# Mysterious Hearts — Patch notes\n\n'+NOTICE+'\n\n'+
                 '\n\n---\n\n'.join(render(item) for item in entries))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'export', 'search'))
    parser.add_argument('--query', default='')
    parser.add_argument('--reports', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'patch_notes'/'PATCH_NOTES.md')
    args = parser.parse_args()
    entries = load()
    if args.command == 'validate': print(f'Valid catalogue: {len(entries)} entries'); return
    entries = select(entries, query=args.query, reports=args.reports)
    if args.command == 'export': export(entries, args.output); print(args.output)
    else:
        for item in entries: print(item['id']+'  '+item['title'])


if __name__ == '__main__': main()
