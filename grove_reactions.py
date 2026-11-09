"""Save-scoped, delayed reactions from a photo author's social circle."""
import random


def schedule_reply(s, data, comment, by_id):
    """One possible follow-up per new AI comment, with a finite conversation budget."""
    import phone_apps as apps
    parent = by_id.get(comment.get('parent'))
    if parent is None:
        return
    chain, seen = [], set()
    node = comment
    while node and node['id'] not in seen:
        seen.add(node['id'])
        chain.append(node)
        node = by_id.get(node.get('parent'))
    root = chain[-1]
    depth = comment.get('auto_reply_depth', 0)
    if depth >= 4:
        return
    used = sum(p.get('auto_reply_root') == root['id'] for p in data['posts'])
    reserved = sum(j.get('auto_reply_root') == root['id'] for j in data['grove_pending'])
    reserved += sum(r.get('root') == root['id'] for r in data.setdefault('grove_reactions', []))
    if used + reserved >= 12:
        return
    eligible = (set(apps.contacts(s)) - {'crow', 'takeo', 'thirteen', 'charles', 'fox'}) - {comment['author'], s['player']}
    # Address the person being replied to first, then another participant in this branch.
    candidates = list(dict.fromkeys(p['author'] for p in chain[1:] if p['author'] in eligible))
    if not candidates:
        return
    rng = random.Random(f"grove-conversation:{comment['id']}:{comment['minute']}")
    if rng.random() > (.85 if depth == 0 else .55):
        return
    who = candidates[0]
    data['grove_reactions'].append(dict(post=comment['id'], author=who, kind='reply',
        root=root['id'], depth=depth+1,
        due=s['world']['minute']+rng.randint(3, max(15, apps.frequency(who)//3))))


def sync(s, data):
    import grove
    import phone_apps as apps
    import social_world
    now = s['world']['minute']
    known = (set(apps.contacts(s)) - {'crow', 'takeo', 'thirteen', 'charles', 'fox'})
    pending = data.setdefault('grove_reactions', [])
    for post in data['posts']:
        if not post.get('image') or post['author'] == s['player'] or post.get('reactions_scheduled'):
            continue
        post['reactions_scheduled'] = True
        rng = random.Random(f"grove-reactions:{post['author']}:{post['id']}:{post['minute']}")
        candidates = [who for who in sorted(known - {post['author']})
                      if post['author'] in social_world.speaker_ties(s, who)
                      or s.get('bond_details', {}).get(f"{who}:{post['author']}")
                      or s.get('bond_details', {}).get(f"{post['author']}:{who}")]
        rng.shuffle(candidates)
        # Active personalities are more likely to show up early in the thread.
        candidates.sort(key=lambda who: apps.frequency(who) * rng.uniform(.5, 1.5))
        for index, who in enumerate(candidates[:5]):
            start = max(now, post['minute'])
            pending.append(dict(post=post['id'], author=who, kind='like', due=start+rng.randint(2, 120)))
            if index < 3:
                pending.append(dict(post=post['id'], author=who, kind='comment',
                                    due=start+rng.randint(5, max(30, apps.frequency(who)))))
    by_id = {post['id']: post for post in apps.grove_posts(s)}
    for reaction in list(pending):
        if reaction['due'] > now:
            continue
        pending.remove(reaction)
        post = by_id.get(reaction['post'])
        who = reaction['author']
        if post is None or who not in known or who == s['player']:
            continue
        stats = grove.relationship(s, who, post['author'])['current_state']
        if reaction['kind'] == 'like':
            if stats.get('unresolved_harm') or stats.get('tension', 0) >= 60:
                continue
            liked = post.setdefault('liked_by', [])
            if who not in liked:
                liked.append(who)
        else:
            # The normal AI writer receives the photo, full ancestry and current ties.
            if not any(p.get('parent') == post['id'] and p['author'] == who for p in data['posts']) \
                    and not any(j.get('parent') == post['id'] and j['author'] == who for j in data['grove_pending']):
                job = apps.queue_grove(s, who, post['id'])
                if reaction['kind'] == 'reply':
                    job.update(auto_reply_depth=reaction['depth'], auto_reply_root=reaction['root'])
