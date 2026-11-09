"""Retrieve witnessed exchanges from saved transcripts and keep permanent relationship firsts."""
import re
import json
import conversation_lore as lore
import story_calendar

FIRSTS = {'date':'First date', 'kiss':'First kiss', 'official':'Became official',
          'gift':'First gift', 'breakup':'First breakup'}


def heard_about(state, who, subject, counterpart):
    """Actual words available to this listener, including in pre-reference saves."""
    heard = []
    player = state['player']

    def remember(label, line, between_pair=False):
        if isinstance(line, str) and (between_pair or lore.names_person(line, subject)):
            heard.append(f'{label}: {line[:400]}')

    for partner, route in state['routes'].items():
        if who not in (player, partner):
            continue
        discussed = 0
        for msg in route['history']:
            if msg['role'] == 'user':
                label, line = player, msg['content']
            elif msg['role'] == 'assistant':
                try:
                    scene = json.loads(msg['content'])
                except ValueError:
                    continue
                label, line = partner, scene.get('dialogue') if isinstance(scene, dict) else None
            else:
                continue
            if not isinstance(line, str):
                continue
            discussed = 3 if lore.names_person(line, subject) else max(0, discussed - 1)
            remember(label, line, discussed > 0)
    for partner, chat in state.get('npc_chats', {}).items():
        if who in (player, partner):
            for msg in chat.get('history', []):
                remember(msg['speaker'], msg.get('text'))
    for group in state.get('groups', {}).values():
        if who == player or who in group['members']:
            present = {player, *group['members']}
            pair_present = {subject.lower(), counterpart.lower()} <= present
            for msg in group['history']:
                if msg['speaker'] != 'Status update':
                    pair_spoke = pair_present and any(lore.names_person(msg['speaker'], n) for n in (subject, counterpart))
                    remember(msg['speaker'], msg.get('text'), pair_spoke)
    for event in state.get('shared_events', []):
        if who in event['witnesses']:
            remember('Witnessed', event['text'])
    return list(dict.fromkeys(heard))[-3:]


def record_first(state, who, kind):
    import town
    firsts = state['relationships'][who].setdefault('firsts', {})
    if kind not in firsts:
        firsts[kind] = town.loop.clock(state)
        if town.present(state, who):
            firsts[kind] += ' · ' + town.loop.place_name(state)


def restore_firsts(state):
    for who, relationship in state['relationships'].items():
        if 'firsts' in relationship: continue
        firsts = {}
        for entry in relationship.get('milestones', []):
            stamp, _, text = entry.partition(': ')
            if text.startswith('Spent a mutually agreed date with '): kind = 'date'
            elif text.endswith('agreed to be exclusive. All romance contacts know.'): kind = 'official'
            elif text.endswith(' as a friendly gift.'): kind = 'gift'
            elif text.startswith('Honestly ended the relationship with '): kind = 'breakup'
            else: continue
            firsts.setdefault(kind, stamp + ' (earliest saved record)')
        if firsts: relationship['firsts'] = firsts


def legacy_recall(state, who, cue='', limit=5):
    """Prefer matching older moments while keeping room for the latest exchange."""
    words = {w for w in re.findall(r'\w+', cue.casefold()) if len(w) > 3}
    moments = []
    route = state['routes'].get(who, {})
    for line in route.get('history', []):
        text = line.get('content', '')
        if line['role'] == 'assistant':
            try:
                text = json.loads(text).get('dialogue', '')
            except (ValueError, AttributeError):
                continue
        if line['role'] in ('user', 'assistant') and text:
            moments.append((line.get('minute', -1), 'Private conversation with player — ' + text[:700]))
    for line in state.get('npc_chats', {}).get(who, {}).get('history', []):
        if line.get('speaker') not in ('Narrator', 'Status update'):
            moments.append((line.get('minute', -1), 'In-person conversation — ' + line['speaker'] + ': ' + line['text']))
    for group in state.get('groups', {}).values():
        if who not in group['members']: continue
        source = 'Group text: ' + group['name'] if group.get('channel') == 'text' else 'Group hangout'
        lines = []
        stamp = -1
        def finish():
            if lines:
                moments.append((stamp, source + ' — ' + ' | '.join(lines)))
        for line in group['history']:
            speaker = line['speaker']
            if speaker.endswith(' (You)') or speaker == 'Status update':
                finish()
                lines = []
                stamp = line.get('minute', -1)
            if speaker != 'Status update':
                lines.append(f"{speaker}: {line['text'][:400]}")
        finish()
    for event in state.get('shared_events', []):
        if who in event['witnesses']:
            moments.append((event['minute'], event['text']))
    import town
    for trip in state['world']['journeys']:
        party = [trip['driver'], *trip['passengers']]
        if who in party and state['player'] in party and trip.get('status') == 'arrived':
            moments.append((trip['arrives'], f"Shared a drive to {town.LOCATIONS[trip['destination']]} with " +
                            ', '.join(p.title() for p in party if p != who) + '.'))
    # Old birthday celebrations already live in the honoree's personal history.
    for line in route.get('history', []):
        if line['role'] == 'status' and ' celebrated ' in line['content']:
            if not any(line['content'] == text for _, text in moments):
                moments.append((-1, line['content']))
    if not moments: return []
    moments.sort(key=lambda m:m[0])
    recent = moments[-1:]
    others = sorted(reversed(moments[:-1]), key=lambda m:len(words.intersection(
        re.findall(r'\w+', m[1].casefold()))), reverse=True)
    return [(f'{story_calendar.story_date(stamp):%b %d, %Y} · ' if stamp >= 0 else '') + text[:1800]
            for stamp, text in recent + others[:limit-1]]


def recall(state, who, cue='', limit=8):
    import memory_store
    return memory_store.packet(state, who, cue, limit)
