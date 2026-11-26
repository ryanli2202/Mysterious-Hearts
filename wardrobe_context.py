"""Visit-scoped automatic appearance over the existing eligible wardrobe.

This resolver cannot move actors, unlock looks, change combat equipment or edit
captured photographs. Historical/required scene portraits retain final authority.
"""
import hashlib
from pathlib import Path


def category(path):
    return __import__('wardrobe_registry').category(path)


def context(s, who):
    import world_loop
    import interiors
    actor = s['world']['cast'][who]
    place = interiors.building(actor['location'])
    kind = 'baseline'
    if actor.get('journey') or str(actor['location']).startswith('car:'):
        return 'journey',kind,''
    if place == world_loop.HOUSES.get(who, ('',))[0] and (place in __import__('interior_residential').HOUSEHOLDS or place.startswith('vacant_')):
        asleep = actor.get('activity') == 'Sleep' or (s.get('autonomy', {}).get('people', {}).get(who, {}).get('sleep_until') or 0) > s['world']['minute']
        kind = 'sleep' if asleep else 'home'
    elif place == 'beach':
        kind = 'beach'
    elif place in ('track', 'boxing_club', 'gym'):
        kind = 'gym'
    ident=interiors.room(s,who)
    if interiors.enabled(s,place):
        if ident in ('arena__training_hall','iron_circle__ring_hall','iron_circle__fighter_preparation_room','boxing_club__training_hall'):
            kind='gym'
        if who=='emily' and place=='flowers':kind='florist'
        if who=='yuriko' and ident in ('campus__theatre_workshop','campus__rehearsal_room'):kind='theatre'
        if ident in ('nightclub__lounge','nightclub__dance_hall','bar__bar_seating_room') and s['world']['minute']%1440>=17*60:
            kind='formal'
    event = next((e for e in s.get('scheduled_events', [])
                  if not e.get('cancelled') and who in [s['player'], *e.get('guests', [])]
                  and e['start'] <= s['world']['minute'] < e['end']
                  and interiors.same_building(e['venue'],place) and e.get('dress_category')
                  and (not interiors.enabled(s,place) or interiors.room(s,who)==interiors.event_room(s,e))), None)
    if event:
        kind = event['dress_category']
    return place, kind, event['id'] if event else ''


def resolve(s, who):
    import camera
    import four_aces
    available = camera.outfits(s, who)
    root = s.setdefault('wardrobe_context', {'version': 1, 'actors': {}})
    records = root.setdefault('actors', {})
    baseline = s['world'].get('player_outfit') if who == s['player'] else None
    record = records.setdefault(who, dict(baseline=baseline if baseline in available else None,
                                         visit=0, place=None, manual=None))
    place, kind, event = context(s, who)
    if record['place'] != place:
        record.update(place=place, visit=record['visit'] + 1, manual=None)
        if who == s['player']:
            if record.get('baseline') in available:
                s['world']['player_outfit'] = record['baseline']
            else:
                s['world'].pop('player_outfit', None)
    identity = (place, record['visit'], kind, event)
    lock=(s.get('campaign_dialogue') or {}).get('wardrobe_snapshot',{}).get(who)
    scene=s.get('campaign_dialogue') or {}
    if not lock and scene.get('beats') and scene.get('cursor',0)<len(scene['beats']):
        lock=scene['beats'][scene.get('cursor',0)].get('wardrobe_snapshot',{}).get(who)
    if not lock:lock=(s.get('combat',{}).get('active') or {}).get('wardrobe_snapshot',{}).get(who)
    if 'Required combat appearance' in available:
        chosen='Required combat appearance'
    elif lock in available:
        chosen=lock
    elif four_aces.uniform_at(who, place) and 'Syndicate uniform' in available:
        chosen = 'Syndicate uniform'
    elif record.get('manual') in available:
        chosen = record['manual']
    else:
        # Gallery pictures remain photo staging references. Auto selection uses
        # actual portrait wardrobe assets only, with current availability checks.
        candidates = [label for label, path in available.items()
                      if Path(path).parent.name == 'portraits' and category(path) == kind]
        if kind == 'baseline' and record.get('baseline') in available:
            candidates = [record['baseline']]
        if not candidates and kind == 'sleep':
            candidates = [label for label, path in available.items()
                          if Path(path).parent.name == 'portraits' and category(path) == 'home']
        if candidates:
            old = record.get('effective')
            if record.get('context') == list(identity) and old in candidates:
                chosen = old
            else:
                seed = hashlib.sha256(f'{who}:{identity}'.encode()).digest()
                chosen = sorted(candidates)[int.from_bytes(seed[:4], 'big') % len(candidates)]
        else:
            chosen = record.get('baseline')
            if chosen not in available:
                chosen = next((label for label, path in available.items() if category(path) == 'baseline'),
                              next(iter(available), None))
    record.update(context=list(identity), effective=chosen)
    return chosen


def snapshot(s,people):
    return {who:resolve(s,who) for who in people if who in s['world']['cast']}


def path(s, who):
    import camera
    return camera.outfits(s, who).get(resolve(s, who))


def wear(s, label):
    import camera
    who = s['player']
    available = camera.outfits(s, who)
    if label != 'Automatic' and label not in available:
        raise ValueError('Choose an available outfit.')
    resolve(s, who)
    record = s['wardrobe_context']['actors'][who]
    record['manual'] = None if label == 'Automatic' else label
    # Preserve the old field as a compatibility mirror for existing consumers;
    # leaving a visit restores the saved baseline via the shared resolver.
    if label == 'Automatic':
        s['world'].pop('player_outfit', None)
    else:
        s['world']['player_outfit'] = label
    resolve(s, who)
