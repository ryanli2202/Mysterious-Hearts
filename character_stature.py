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


@lru_cache(maxsize=1)
def historical_records():
    return json.loads((ROOT / 'assets/portraits/stature.json').read_text(encoding='utf-8')).get('historical_characters', {})


def height_cm(who, path=None):
    # Child portraits must not inherit Camila's present 168 cm display height.
    historical={'neo-child10':138,'neo-home12':151,'neo-school16':174,'tyler-school16':178,'daniel-school16':175,'thirteen-child10':140,'neo-trainee10':136,'mariko-current':165,'mariko-home12':165,'mariko-home16':165,'mariko-raid':165,'neo-soren':180,'neo-tyler-father':184,'camila-child7':122,'camila-child11':143,'camila-teen16':165,'camila-pilar':120,'camila-elena':164,'camila-mara-young':169,'camila-mara-current':169,'camila-inez':171,'camila-ansel':180,'camila-contractor':183}
    # Authored display estimates for unspecified historical ages; these are not
    # canonical measurements or claims about birth dates.
    historical.update({'takeo-one-child':136,'takeo-thirteen-history':170,
                       'rei-child':139,'yuriko-child':120,'rei-escape':172,'yuriko-escape':148})
    if path is not None and Path(path).stem in historical:return historical[Path(path).stem]
    import custom_protagonist
    custom = custom_protagonist._profiles.get(who)
    if custom:
        return float(custom['height'])
    if who in ('sowon','kouji'):return {'sowon':167,'kouji':179}[who]
    key = slug(who)
    if key == 'shinzo-kazama' or (path is not None and Path(path).stem == 'takeo-kazama'):
        key = 'takeo-kazama'
    role = None
    if path is not None and Path(path).parent.name == 'guards':
        role = Path(path).stem
    elif key.startswith('guard_art_'):
        role = key[len('guard_art_'):]
    if role:
        key = 'joseph-richter' if role == 'richter_cybernetic' else 'guard-' + role
    return historical_records().get(key, records().get(key, {})).get('height_cm', 178)
