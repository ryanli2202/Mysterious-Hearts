"""Portrait stature, including explicit MH-013 display defaults.

Display defaults and explicit stature do not change dialogue disclosure rules.
Custom profiles always retain the height supplied by their owner.
"""
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def slug(who):
    return str(who).strip().lower().replace(' ', '-')


@lru_cache(maxsize=1)
def records():
    return json.loads((ROOT / 'assets/portraits/stature.json').read_text(encoding='utf-8'))['characters']


def height_cm(who, path=None):
    import custom_protagonist
    custom = custom_protagonist._profiles.get(who)
    if custom:
        return float(custom['height'])
    key = slug(who)
    role = None
    if path is not None and Path(path).parent.name == 'guards':
        role = Path(path).stem
    elif key.startswith('guard_art_'):
        role = key[len('guard_art_'):]
    if role:
        key = 'joseph-richter' if role == 'richter_cybernetic' else 'guard-' + role
    return records().get(key, {}).get('height_cm', 178)
