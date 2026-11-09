"""Save-scoped phone identity; presentation preferences never become story facts."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFERENCES = ROOT / 'phone_preferences.json'
DEFAULTS = dict(device='Phone', scale=100, text_size=12, reduced_motion=False,
                confirm_send=False, preview='Sender only', reveal='Instant',
                typing_indicator=True, notification_volume=80, typing_volume=50,
                voicemail_volume=100)
_preferences = None
PROFILES = {
    'rei': dict(accent='#80c6ba', favourites=['emily', 'garrett', 'yuriko'],
                names={'emily': 'Em', 'garrett': 'Garrett', 'yuriko': 'Yuriko · Little sis',
                       'amy': 'Amy · Interview', 'samantha': 'Sam · Ring', 'minsu': 'Minsu · Sophie’s friend'},
                apps=['Messages', 'Gallery', 'Camera', 'Journal'],
                note='Sketch something for myself. Leave room for an unfinished idea.',
                messages=[('emily', 'I still have that little greenhouse. The white pane makes me smile.'),
                          ('garrett', 'There’s always a seat for you after closing.'),
                          ('yuriko', 'Ask before fixing my model this time, okay?')]),
    'garrett': dict(accent='#d5b371', favourites=['april', 'rei', 'emily'],
                    names={'april': 'April · Chess menace', 'rei': 'Rei', 'emily': 'Emily',
                           'amy': 'Amy · Interview', 'sophie': 'Sophie · Parties', 'ivan': 'Ivan · Business'},
                    apps=['Messages', 'Contacts', 'Maps', 'Doober Eats'],
                    note='Try another noodle recipe. Make time for a quiet meal after closing.',
                    messages=[('april', 'If you resign, you still have to tip your own king over.'),
                              ('rei', 'You kept the dumpling sketch, didn’t you?'),
                              ('emily', 'Saving your number here. Talk soon!')]),
    'minsu': dict(accent='#7bd7ce', favourites=['amy', 'sophie', 'emily'],
                  names={'amy': 'Amy · Next dorm', 'sophie': 'Sophie · Coach of chaos',
                         'emily': 'Emily · Café', 'samantha': 'Samantha · Gym', 'april': 'April · Library',
                         'rei': 'Rei · Party', 'garrett': 'Garrett · Party'},
                  apps=['Messages', 'Camera', 'Mini Games', 'Calendar'],
                  note='Study, train, eat. Review the food before sitting on it.',
                  messages=[('amy', 'Two intact buns next time. That’s my only request.'),
                            ('sophie', 'Ten seconds means ten seconds. No negotiating the last interval.'),
                            ('emily', 'It was nice meeting you at the café!')]),
    'ivan': dict(accent='#bda3e0', favourites=['valentina', 'rei', 'garrett'],
                 names={'valentina': 'Val · Sis', 'rei': 'Rei · Campaign', 'garrett': 'Garrett · Business',
                        'minsu': 'Minsu'},
                 apps=['Messages', 'Gallery', 'Contacts', 'Journal'],
                 note='Listen to the piano between sessions. Keep the table clear for dinner.',
                 messages=[('valentina', 'I’m taking the second verse at karaoke. You know the rules.'),
                           ('rei', 'Good working with you on the campaign.'),
                           ('garrett', 'You have my number. Keep in touch.')]),
}


def preferences():
    global _preferences
    if _preferences is None:
        try:
            saved = json.loads(PREFERENCES.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            saved = {}
        _preferences = dict(DEFAULTS)
        if isinstance(saved, dict):
            for key, value in saved.items():
                if key in DEFAULTS and type(value) is type(DEFAULTS[key]):
                    _preferences[key] = value
        for key, lo, hi in [('scale', 60, 120), ('text_size', 10, 20),
                            ('notification_volume', 0, 100), ('typing_volume', 0, 100), ('voicemail_volume', 0, 100)]:
            _preferences[key] = max(lo, min(hi, _preferences[key]))
    return _preferences


def save_preferences(values):
    preferences().update({k: v for k, v in values.items() if k in DEFAULTS})
    temp = PREFERENCES.with_suffix('.tmp')
    temp.write_text(json.dumps(preferences(), indent=2), encoding='utf-8')
    temp.replace(PREFERENCES)


def ensure(s):
    profile = PROFILES[s['player']]
    d = s.setdefault('phone_personalization', {})
    defaults = dict(names={**copy.deepcopy(profile['names']), **s.get('nicknames', {})}, favourites=profile['favourites'][:],
                    pinned_chats=[],
                    wallpaper='default', accent=profile['accent'], app_order=profile['apps'][:],
                    avatars={}, tones={}, notes='', story_note=profile['note'],
                    archived_messages=[dict(id=f'start:{s["player"]}:{i}', who=who, text=text)
                                       for i, (who, text) in enumerate(profile['messages'])])
    for key, value in defaults.items():
        d.setdefault(key, value)
    # Empty pins mean the player deliberately unpinned everything; never re-seed.
    d.setdefault('pins', [m['id'] for m in d['archived_messages']][:3])
    d['pins'] = list(dict.fromkeys(d['pins']))[:3]
    return d


def name(s, who):
    import game_core as core
    return ensure(s)['names'].get(who) or core.contact_name(s, who)


def rename(s, who, value):
    value = value.strip()
    if not 1 <= len(value) <= 40 or any(ord(c) < 32 for c in value):
        raise ValueError('Use a contact name of 1–40 characters on one line.')
    ensure(s)['names'][who] = value


def size(screen_width, screen_height, device=None, scale=None):
    p = preferences()
    a, b = (9, 16) if (device or p['device']) == 'Phone' else (3, 4)
    height = min(960, max(160, screen_height-90)) * (scale or p['scale']) / 100
    unit = max(1, int(min(height/b, (screen_height-90)/b, (screen_width-40)/a)))
    return a*unit, b*unit


def records(s):
    """Only delivered, visible texts, with stable IDs even after contact renames."""
    import phone_apps
    from messages_ui import text_messages
    known = set(phone_apps.contacts(s))
    rows = [dict(m, group=False, kind='in', earlier=True) for m in ensure(s)['archived_messages'] if m['who'] in known]
    for key, is_group in [(k, False) for k in known] + [(k, True) for k, g in s.get('groups', {}).items() if g.get('channel') == 'text']:
        view = dict(s, active=key)
        group = s['groups'][key] if is_group else None
        occurrences = {}
        for message in text_messages(view, group=group):
            if message[2] == 'status': continue
            digest = hashlib.sha256(json.dumps(message[1:5], ensure_ascii=False).encode()).hexdigest()[:24]
            count = occurrences.get(digest, 0)
            occurrences[digest] = count + 1
            rows.append(dict(id=f'{"group" if is_group else "route"}:{key}:{digest}:{count}',
                             who=key, text=message[1], kind=message[2], group=is_group, earlier=False,
                             minute=message[4] if len(message)>4 else None))
    return rows


def pin(s, ident):
    d = ensure(s)
    if ident not in {r['id'] for r in records(s)}:
        raise ValueError('Only an existing, visible message can be pinned.')
    if ident in d['pins']: return
    if len(d['pins']) >= 3:
        raise ValueError('All three pins are in use. Unpin a message first.')
    d['pins'].append(ident)


def unpin(s, ident):
    pins = ensure(s)['pins']
    if ident in pins: pins.remove(ident)


def photos(s):
    import camera
    return {f'photo:{r["id"]}': (r.get('title') or f'Photo · {r["minute"]}', camera.photo_path(r))
            for r in camera.photos(s) if camera.photo_path(r).is_file()}


def wallpaper_path(s, selection=None):
    selected = selection or ensure(s)['wallpaper']
    if selected == 'default':
        updated = ROOT / 'assets' / 'ui' / f'phone-wallpaper-{s["player"]}-v2.png'
        if updated.is_file(): return updated
        return ROOT / 'assets' / 'ui' / f'phone-wallpaper-{s["player"]}.png'
    return photos(s).get(selected, ('', ROOT / 'missing-wallpaper'))[1]


def reset(s):
    d = ensure(s)
    for key in ('names', 'favourites', 'wallpaper', 'accent', 'app_order', 'avatars', 'tones',
                'home_pages', 'home_dock', 'home_capacity', 'home_page'):
        d.pop(key, None)
    ensure(s)
