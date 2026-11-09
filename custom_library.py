"""Reusable protagonist profiles, stored outside disposable story saves."""
import hashlib
import json
import custom_protagonist as custom
import save_system


def remember(state, save_root):
    if not custom.is_custom(state.get('player')):
        return
    profile = custom.validate(state.get('custom_protagonist'))
    profile['portrait'] = state['custom_protagonist'].get('portrait', '')
    custom.portrait_path(profile)
    data = json.dumps(profile, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')
    key = hashlib.sha256(data).hexdigest()
    target = save_root.parent / 'custom_characters' / (key + '.json')
    if not target.exists():
        save_system.atomic(target, data)


def profiles(save_root):
    # Recover legacy profiles, including those in checkpoints and named saves.
    for path in save_system.entries(save_root):
        try:
            state = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(state, dict):
                remember(state, save_root)
        except (ValueError, KeyError, TypeError):
            continue
    result = []
    for path in sorted((save_root.parent / 'custom_characters').glob('*.json')):
        try:
            raw = json.loads(path.read_text(encoding='utf-8'))
            profile = custom.validate(raw)
            profile['portrait'] = raw.get('portrait', '')
            custom.portrait_path(profile)
            result.append(profile)
        except (ValueError, KeyError, TypeError):
            continue
    return sorted(result, key=lambda p: p['name'].casefold())
