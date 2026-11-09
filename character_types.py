"""The two playable character systems; romance is a separate capability."""
import hidden_cast

MAJOR = 'major character'
TOWN = 'town NPC'
MAJOR_CHARACTERS = frozenset(('garrett', 'rei', 'minsu', 'ivan', 'yuriko',
    'emily', 'sophie', 'amy', 'samantha', 'april', *hidden_cast.CAST))


def is_major(who):
    import custom_protagonist
    return who in MAJOR_CHARACTERS or who in custom_protagonist._profiles


def is_town(who):
    import town
    return who in {p[0] for p in (*town.NPCS, *town.VENUE_STAFF.values(), town.HQ_EXECUTIVE)}


def kind(who):
    return MAJOR if is_major(who) else TOWN if is_town(who) else None


def migrate(state):
    """Retain obsolete progression as history without retaining active romance."""
    dynamics = state.get('relationship_dynamics', {})
    for who in list(dynamics.get('people', {})):
        if is_town(who):
            dynamics.setdefault('legacy_town_people', {})[who] = dynamics['people'].pop(who)
    for bucket in ('relationships', 'friendships'):
        for who in list(state.get(bucket, {})):
            if not is_town(who):
                continue
            old = state[bucket].pop(who)
            chat = state.setdefault('npc_chats', {}).setdefault(who, {'history': []})
            chat.setdefault('legacy_progression', {}).setdefault(bucket, old)
            chat.setdefault('connection', dict(status='acquaintances', trust=35, closeness=0))
    for who, chat in state.get('npc_chats', {}).items():
        if not is_town(who):
            continue
        connection = chat.get('connection')
        if connection is None: continue
        obsolete = {k: v for k, v in connection.items()
                    if k not in ('status', 'trust', 'closeness', 'visit_days', 'conversation_day')}
        if obsolete or connection.get('status') not in ('strangers', 'acquaintances', 'familiar face', 'established colleagues'):
            chat.setdefault('legacy_progression', {}).setdefault('connection', dict(connection))
            connection.clear()
            connection.update(status='acquaintances', trust=35, closeness=0)
    date = state.get('date_session')
    if isinstance(date, dict) and is_town(date.get('partner')):
        state.setdefault('legacy_town_dates', []).append(state.pop('date_session'))
    app = state.get('meet_cute', {})
    for who in list(app.get('matches', {})):
        if not is_town(who):
            continue
        match = app['matches'].pop(who)
        app.setdefault('legacy_town_matches', {})[who] = match
        for event in state.get('scheduled_events', []):
            if event.get('id') in match.get('dates', []): event['cancelled'] = True
        if app.get('exclusive_with') == who: app['exclusive_with'] = None
    likes = app.get('likes', [])
    removed = [item for item in likes if is_town(item.get('who'))]
    if removed:
        app.setdefault('legacy_town_likes', []).extend(removed)
        app['likes'] = [item for item in likes if not is_town(item.get('who'))]
