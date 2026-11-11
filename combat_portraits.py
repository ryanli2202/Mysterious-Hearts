"""Dedicated awakened artwork, requested only by the in-person combat view."""
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageTk
import character_stature
import portrait_framing

ROOT = Path(__file__).resolve().parent / 'assets' / 'portraits' / 'combat'
CAST = ('fox', 'gordon', 'sylvanis', 'takeo', 'crow', 'charles', 'garrett',
        'ivan', 'rei', 'neo', 'daniel', 'martos', 'elias', 'mavis', 'camila',
        'thirteen', 'Keisuke Hachimura', 'tyler', 'samantha', 'minsu',
        'valentina', 'april', 'emily', 'alyssa')


def resolve(who):
    """Whitelist canonical IDs; unknown/custom characters retain their own art."""
    if who not in CAST:
        return None
    slug = 'keisuke-hachimura' if who == 'Keisuke Hachimura' else who
    path = ROOT / (slug + '.png')
    return path if path.is_file() else None


@lru_cache(maxsize=48)
def _thumbnail(path, size, height, scale=None):
    return portrait_framing.fit(portrait_framing.load(path), size, height, scale)


def portrait(game, who, size, location, minute, *, scale=None):
    path = resolve(who)
    if path is not None:
        try:
            return ImageTk.PhotoImage(_thumbnail(str(path), size,
                character_stature.height_cm(who, path), scale), master=game)
        except (OSError, ValueError):
            # Missing/damaged optional art must not prevent playing a fight.
            pass
    if scale is None:
        return game.portrait(who, size, location, minute)
    return game.portrait(who, size, location, minute, scale=scale)


def group(game, sizes, location, minute):
    """Keep both sides at a common scale, including saved guard encounters."""
    entries = []
    for who, size in sizes.items():
        path = resolve(who)
        if path is None:
            _, path = game.portrait_path(who, location, minute)
        try:
            entries.append((portrait_framing.load(path), size,
                            character_stature.height_cm(who, path)))
        except (OSError, ValueError):
            pass
    scale = portrait_framing.shared_scale(entries) if entries else None
    photos = {}
    for who, size in sizes.items():
        try:
            photos[who] = portrait(game, who, size, location, minute, scale=scale)
        except (OSError, ValueError):
            photos[who] = ImageTk.PhotoImage(Image.new('RGBA', size), master=game)
    return photos
