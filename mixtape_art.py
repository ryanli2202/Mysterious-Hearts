"""Local Mixtape artwork lookup and bounded image decoding cache."""
from functools import lru_cache
from pathlib import Path
from PIL import Image
import mixtape_catalog as music

ROOT = Path(__file__).resolve().parent / 'assets' / 'mixtape'
ARTIST_IDS = {a['id'] for a in music.ARTISTS}
SONG_ARTISTS = {s['id']: a['id'] for a in music.ARTISTS for s in a['songs']}


def artist_path(ident, kind='portrait'):
    if ident not in ARTIST_IDS or kind not in ('portrait', 'cover'):
        return None
    path = ROOT / f'{ident}-{kind}.png'
    return path if path.is_file() else None


def song_path(ident):
    return artist_path(SONG_ARTISTS.get(ident), 'cover')


@lru_cache(maxsize=128)
def thumbnail(path, size):
    """Cache small decoded images rather than all full-resolution sources."""
    with Image.open(path) as source:
        result = source.convert('RGB')
        result.thumbnail((size, size), Image.Resampling.LANCZOS)
        return result.copy()
