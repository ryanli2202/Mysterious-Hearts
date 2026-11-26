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
        'valentina', 'april', 'emily', 'alyssa', 'sowon', 'kouji', 'paul', 'somchai')


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
    path = scene_path(game,who)
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
        path = scene_path(game,who)
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


def scene_path(game,who):
    state=getattr(game,'state_data',None) or {}
    if not isinstance(state,dict):state={}
    fight=state.get('combat',{}).get('active') or {}
    # Authored encounter metadata is the contract. A second campaign-name list
    # silently dropped valid portraits whenever a new route was introduced.
    contextual=fight.get('contextual_portraits',{}).get(who)
    if contextual:
        path=ROOT.parent/(contextual+'.png')
        if path.is_file():return path
    historical=fight.get('historical_portraits',{}).get(who)
    if historical:
        path=ROOT.parent/(historical+'.png')
        if path.is_file():return path
    if who==fight.get('opponent'):
        path=ROOT.parent/(fight.get('opponent_profile',{}).get('portrait','')+'.png')
        if path.is_file():return path
    # The combat stage owns its dedicated artwork. Visit clothes and saved
    # wardrobe snapshots remain fallbacks, not replacements for combat art.
    dedicated = resolve(who)
    if dedicated is not None:
        return dedicated
    state=getattr(game,'state_data',None) or {}
    if not isinstance(state,dict):return None
    if state.get('interiors',{}).get('enabled_buildings') and who in state.get('world',{}).get('cast',{}):
        path=__import__('wardrobe_context').path(state,who)
        if path:return Path(path)
    return None
