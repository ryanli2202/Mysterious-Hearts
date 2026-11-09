"""Authored pre-game photo archive and persistent per-save engagement."""
import json
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EPOCH = datetime(2050, 1, 1)
ARCHIVE_VERSION = 30


@lru_cache(maxsize=1)
def catalog():
    return json.loads((ROOT / 'assets/grove/posts.json').read_text(encoding='utf-8'))


def ensure(data):
    if data.get('grove_archive_version') == ARCHIVE_VERSION:
        return
    from grove import FOLLOWERS
    archive = data.setdefault('grove_archive', [])
    existing = {p.get('archive_key') for p in archive}
    # Refresh authored Emily photos in place so existing reply targets and likes survive.
    replacements = {item['key']: item for item in catalog() if item['author'] == 'emily'}
    for post in archive:
        item = replacements.get(post.get('archive_key'))
        if item:
            post.update(image=item['image'], text=item['caption'])
            comments = [p for p in archive if p.get('parent') == post['id']]
            for comment, authored in zip(comments, item['comments']):
                comment.update(author=authored['author'], text=authored['text'],
                               minute=post['minute'] + authored['delay_minutes'])
    next_id = min([-1000, *(p['id'] - 1 for p in archive)])
    for item in catalog():
        if item['key'] in existing:
            continue
        minute = int((datetime.fromisoformat(item['published_at']) - EPOCH).total_seconds() // 60)
        parent = next_id
        archive.append(dict(id=parent, author=item['author'], text=item['caption'],
                            minute=minute, parent=None, image=item['image'],
                            archive_key=item['key'], historical=True,
                            likes=round(FOLLOWERS[item['author']] * item['engagement_basis_points'] / 10000)))
        next_id -= 1
        for comment in item['comments']:
            archive.append(dict(id=next_id, author=comment['author'], text=comment['text'],
                                minute=minute + comment['delay_minutes'], parent=parent,
                                historical=True))
            next_id -= 1
    data['grove_archive_version'] = ARCHIVE_VERSION


def timestamp(post):
    return (EPOCH + timedelta(minutes=post['minute'])).strftime('%d %b %Y Â· %H:%M')


def photos(s, who):
    import phone_apps as apps
    return sorted((p for p in apps.grove_posts(s) if p['author'] == who and p.get('image')),
                  key=lambda p: p['minute'], reverse=True)


def shows_character(post, who):
    """Require subject evidence; authorship or a caption alone is insufficient."""
    if post.get('archive_key'):
        # Consult the catalog so existing saves also receive reviewed metadata.
        return any(item['key'] == post['archive_key']
                   and item['image'] == post.get('image')
                   and who in item.get('visible_subjects', []) for item in catalog())
    context = post.get('photo_context', {})
    if 'subjects' in context:
        return any(subject.get('id') == who for subject in context['subjects'])
    # Grove's generated Selfie mode always depicts the posting character alone.
    return post.get('author') == who and context.get('mode') == 'Selfie'


def like_count(post, player):
    return post.get('likes', 0) + len(post.get('liked_by', []))


def update_likes(s):
    """Audience engagement grows over the first day of story time, never backwards."""
    for post in s.get('phone_apps', {}).get('posts', []):
        if 'likes_target' not in post:
            continue
        age = max(0, s['world']['minute'] - post['minute'])
        progress = min(1, age / 1440)
        earned = round(post['likes_target'] * (1 - (1 - progress) ** 3))
        post['likes'] = max(post.get('likes', 0), earned)


def unread_comments(s):
    return [n for n in s.get('phone_apps', {}).get('grove_notifications', []) if not n.get('read')]


def mark_read(s, post_id):
    for notification in unread_comments(s):
        if notification['post_id'] == post_id:
            notification['read'] = True


def toggle_like(s, post_id):
    import grove_accounts
    grove_accounts.require(s)
    import phone_apps as apps
    post = next((p for p in apps.grove_posts(s) if p['id'] == post_id and p.get('image')), None)
    if post is None:
        raise ValueError('This photo is no longer available.')
    liked = post.setdefault('liked_by', [])
    if s['player'] in liked:
        liked.remove(s['player'])
    else:
        liked.append(s['player'])


def publish(s, photo_id, caption):
    """Publish only a photo in this save's Gallery; persist its public scene context."""
    import copy
    import random
    import camera
    import grove
    import grove_accounts
    grove_accounts.require(s)
    import phone_apps as apps
    from PIL import Image
    caption = caption.strip()
    if not 1 <= len(caption) <= 280:
        raise ValueError('Write a caption between 1 and 280 characters.')
    record = next((p for p in camera.photos(s) if p['id'] == photo_id), None)
    if record is None:
        raise ValueError('Choose a photo from your Gallery.')
    with Image.open(camera.photo_path(record)) as source:
        source.verify()
    snapshot = record.get('snapshot', {})
    public = {key: copy.deepcopy(snapshot[key]) for key in
              ('mode', 'detail', 'subjects', 'group_pose') if key in snapshot}
    data = apps.ensure(s)
    post = apps._append(data, s['player'], caption, s['world']['minute'])
    rng = random.Random(f"grove-photo:{photo_id}:{post['id']}")
    post.update(image=record['path'], gallery_photo_id=photo_id, photo_context=public,
                likes=0, likes_target=round(grove.profile(s, s['player'])['followers'] * rng.uniform(.025, .15)))
    grove_accounts.record(s, post)
    contacts = apps.contacts(s)
    subjects = {p['id'] for p in public.get('subjects', [])}
    rng.shuffle(contacts)
    contacts.sort(key=lambda who: who not in subjects)
    for who in contacts[:3]:
        apps.queue_grove(s, who, post['id'])
    return post

