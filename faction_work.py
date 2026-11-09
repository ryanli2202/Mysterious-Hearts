"""Private shift assignments; observable work never establishes secret rank."""

# Weekday cover work and rotating operational appointments. These are AU shifts,
# not new faction memberships or changes to the source characters' ranks.
def appointment(who, minute):
    import story_calendar as dates
    hour = minute % 1440 / 60
    day = minute // 1440
    if not dates.free_day(dates.story_date(minute)):
        if who in ('martos', 'camila') and 9 <= hour < 17:
            area = 'reception' if hour < 11 else 'briefing'
            return (9 if hour < 11 else 11, 'site_07_'+area,
                    'Security desk work' if who == 'martos' else 'Corporate account review')
        if who == 'elias' and 14 <= hour < 17:
            return (14, 'site_05_reception', 'Publicity appointment')
    if who in ('ivan', 'martos', 'elias', 'camila', 'mavis') and 17 <= hour < 18:
        return (17, 'glasshouse_lab', 'Private laboratory review')
    if who == 'valentina' and 10 <= hour < 13:
        return (10, 'site_04_briefing', 'Field operations review')
    if who == 'ivan' and 16 <= hour < 18:
        return (16, ('site_04','site_05','site_06','site_07','site_08')[day % 5]+'_briefing', 'Operations appointment')
    # Offsets preserve the existing staggered 20:00 headquarters appointments.
    sites = dict(martos='site_04', elias='site_05', camila='site_06', mavis='site_08')
    if who in sites and day % 4 == tuple(sites).index(who) and 18 <= hour < 20:
        return (18, sites[who]+'_briefing', 'Private appointment')
    return None


def next_stop(s, who, destination):
    """NPCs use the same frontage/reception/clearance path as visitors."""
    import crime_operations as ops
    if destination not in ops.ROOMS: return destination
    key, area = ops.ROOMS[destination]
    current = s['world']['cast'][who]['location']
    if ops.site_of(current) != key: return key
    if area == 'briefing' and not ops.permitted(s, who, key): return key+'_reception'
    if current == key: return key+'_reception'
    return destination


def colleagues(s, key):
    """Only physically present, on-duty people; no remote staff directory."""
    import crime_operations as ops
    result = []
    location = s['world']['location']
    for who, actor in s['world']['cast'].items():
        shift = appointment(who, s['world']['minute'])
        if who == s['player'] or not shift or shift[1] != location: continue
        if actor.get('journey') or actor['location'] != location: continue
        if ops.site_of(location) != key: continue
        if location.endswith('_briefing') and not ops.permitted(s,who,key): continue
        if actor.get('activity') != shift[2]: continue
        result.append(who)
    return result


def validate_colleague(s, key, who):
    if who not in colleagues(s,key):
        raise ValueError('Your colleague must be here, cleared and on duty. Wait for their shift or abandon this joint assignment.')


def disclosure(s):
    import four_aces
    listeners = {who for who, actor in s['world']['cast'].items()
                 if actor['location']==s['world']['location'] and not actor.get('journey')}
    return bool(listeners) and all(four_aces.knows_identities(s, who) for who in listeners)
