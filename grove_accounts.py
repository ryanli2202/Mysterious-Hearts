"""Save-scoped custom Grove accounts and activity-earned audience growth."""
import hashlib
import re
import custom_protagonist

DAY = 1440


def needed(s):
    return custom_protagonist.is_custom(s['player'])


def account(s):
    return s.get('grove_account') if needed(s) else None


def require(s):
    if s.get('player')=='fox': raise ValueError('Edward Fox has no Grove account.')
    if needed(s) and account(s) is None:
        raise ValueError('Create your Grove account before posting, replying or liking photos.')


def save(s, handle, bio):
    """Validate everything before creating/updating; never reset earned growth."""
    import grove
    if not needed(s):
        raise ValueError('Authored characters keep their established Grove accounts.')
    if not isinstance(handle, str) or not isinstance(bio, str):
        raise ValueError('Enter a handle and bio.')
    handle = handle.strip().removeprefix('@').lower()
    if not re.fullmatch(r'[a-z0-9][a-z0-9._]{2,23}', handle):
        raise ValueError('Use 3–24 letters, numbers, dots or underscores; begin with a letter or number.')
    if handle in {value.casefold() for value in grove.HANDLES.values()}:
        raise ValueError('That handle belongs to a Winterfield resident. Choose another.')
    bio = bio.strip()
    if not 1 <= len(bio) <= 280:
        raise ValueError('Write a bio between 1 and 280 characters.')
    data = account(s)
    if data is None:
        data = dict(created=s['world']['minute'], followers=0, events=[])
        s['grove_account'] = data
    data.update(handle=handle, bio=bio)
    return data


def update(s):
    data = account(s)
    if data is None:
        return
    now = s['world']['minute']
    for event in data['events']:
        earned = event['target'] * min(DAY, max(0, now-event['minute'])) // DAY
        previous = event['earned']
        if earned > previous:
            data['followers'] += earned - previous
            event['earned'] = earned


def record(s, post):
    """Credit up to three original posts/photos and five replies per story day."""
    data = account(s)
    if data is None or post['author'] != s['player']:
        return
    update(s)
    reply = post.get('parent') is not None
    if reply:
        posts = s.get('phone_apps', {})
        parent = next((p for p in [*posts.get('posts', []), *posts.get('grove_archive', [])]
                       if p['id'] == post['parent']), None)
        if not parent or parent['author'] == s['player']:
            return
    fingerprint = hashlib.sha256((post['text'].strip().casefold() + '\n' + post.get('image', '')).encode()).hexdigest()
    if any(e['post_id'] == post['id'] or e['fingerprint'] == fingerprint for e in data['events']):
        return
    day = post['minute']//DAY
    if sum(e['minute']//DAY == day and e['reply'] == reply for e in data['events']) >= (5 if reply else 3):
        return
    target = 1 if reply else (6 if post.get('image') else 4) + min(5, data['followers']//100)
    data['events'].append(dict(post_id=post['id'], minute=post['minute'], reply=reply,
                               fingerprint=fingerprint, target=target, earned=0))


def pending(s):
    update(s)
    return sum(e['target']-e['earned'] for e in (account(s) or {}).get('events', []))
