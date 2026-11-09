"""Bundled fictional Mixtape artists and songs; no network or audio service."""
import json
from pathlib import Path

ARTISTS = json.loads((Path(__file__).resolve().parent / 'assets' / 'mixtape_catalog.json').read_text(encoding='utf-8'))['artists']
GENRES = tuple(dict.fromkeys(a['genre'] for a in ARTISTS))
SONGS = {s['id']: dict(s, artist=a['name']) for a in ARTISTS for s in a['songs']}


def track_label(ident):
    song = SONGS[ident]
    return f'{song["title"]} — {song["artist"]}'
