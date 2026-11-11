"""Reusable profiles. Enumeration is read-only; legacy recovery is explicit."""
import copy
import hashlib
import json
import re
import uuid
import custom_protagonist as custom
import save_system


def identity(profile):
    value = profile.get('profile_id')
    if value:
        if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{32,64}', value):
            raise ValueError('Invalid reusable character identity.')
        return value
    legacy = {k: v for k, v in profile.items() if k not in ('profile_id', 'profile_version')}
    return hashlib.sha256(json.dumps(legacy, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')).hexdigest()


def normalise(raw):
    profile = custom.validate(raw)
    profile['portrait'] = raw.get('portrait', '')
    custom.portrait_path(profile)
    profile['profile_id'] = identity(profile)
    profile['profile_version'] = 2
    return profile


def fingerprint(profile):
    return hashlib.sha256(json.dumps(normalise(profile), ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def save_profile(raw, save_root, *, separate=False, expected=None):
    profile = normalise(raw)
    if separate:
        profile['profile_id'] = uuid.uuid4().hex
    target = save_root.parent / 'custom_characters' / (profile['profile_id'] + '.json')
    if expected is not None and not separate:
        if not target.exists() or fingerprint(json.loads(target.read_text(encoding='utf-8'))) != expected:
            raise ValueError('This reusable character changed or was removed since editing began. Your draft is preserved. Reopen the latest profile or use Save as new character.')
    save_system.atomic(target, json.dumps(profile, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8'))
    return copy.deepcopy(profile)


def remember(state, save_root):
    if not custom.is_custom(state.get('player')):
        return
    profile = normalise(state.get('custom_protagonist'))
    target = save_root.parent / 'custom_characters' / (profile['profile_id'] + '.json')
    # Older playthroughs must never overwrite a subsequently edited profile.
    if not target.exists():
        save_profile(profile, save_root)


def recover(save_root):
    errors = []
    for path in save_system.entries(save_root):
        try:
            state = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(state, dict):
                remember(state, save_root)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{path.name}: {exc}')
    return errors


def enumerate_profiles(save_root):
    result, errors, seen = [], [], set()
    for path in sorted((save_root.parent / 'custom_characters').glob('*.json')):
        try:
            profile = normalise(json.loads(path.read_text(encoding='utf-8')))
            if profile['profile_id'] not in seen:
                result.append(profile)
                seen.add(profile['profile_id'])
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{path.name}: {exc}')
    return sorted(result, key=lambda p: (p['name'].casefold(), p['profile_id'])), errors


def profiles(save_root):
    """Compatibility entry point for explicit legacy library/recovery actions."""
    recover(save_root)
    return enumerate_profiles(save_root)[0]
