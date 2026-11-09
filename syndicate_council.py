"""Weekly, private face-card council, driven exclusively by the story clock."""
import story_calendar as calendar

SOURCE = 'syndicate_council'
ROSTER = ('crow', 'ivan', 'sylvanis', 'valentina', 'martos', 'elias', 'camila', 'mavis')
ROLES = 'The Crow (chair), both Jokers, the four Aces, and senior face-card members'
WEEK = 7 * 1440


def eligible(s):
    if s['player'] in ROSTER:
        return True
    m = s.get('job_apps', {}).get('membership') or {}
    return (m.get('faction') == 'Syndicate' and m.get('branch') in
            ('Clubs', 'Hearts', 'Diamonds', 'Spades') and m.get('rank', 0) >= 6)


def week_start(minute):
    day = calendar.story_date(minute)
    return minute//1440*1440 + (6-day.weekday())*1440 + 20*60


def npc_event(s, who, minute):
    start = week_start(minute)
    if who in ROSTER and who != s['player'] and start <= minute < start+60:
        return dict(venue='syndicate_hq', title='Syndicate face-card council · chaired by the Crow')


def ensure(s, through=None):
    events = s.setdefault('scheduled_events', [])
    now = s['world']['minute']
    if not eligible(s):
        for e in events:
            if e.get('source') == SOURCE and e['end'] > now:
                e['cancelled'] = True
        return
    first = week_start(now)
    # New/old saves and newly promoted Jacks start with the next full meeting.
    if first < now:
        first += WEEK
    # Restore upcoming invitations after regained eligibility or stale cancellation.
    for e in events:
        if e.get('source') == SOURCE and e['end'] > now:
            e['cancelled'] = False
            e['mandatory'] = s['player'] == 'ivan'
    ids = {e['id'] for e in events}
    stop = max(first+9*WEEK, (through+1) if through is not None else 0)
    for start in range(first, stop, WEEK):
        ident = f'syndicate-council:{start}'
        if ident in ids:
            continue
        events.append(dict(id=ident, source=SOURCE, title='Syndicate face-card council',
            venue='syndicate_hq', guests=[w for w in ROSTER if w != s['player']],
            start=start, end=start+60, reminded=[], cancelled=False,
            created_minute=now, memory_phase='planned', attendees=[],
            mandatory=s['player']=='ivan', attendance_minutes=0))


def join(s, e):
    if not eligible(s) or e not in s.get('scheduled_events', []):
        raise ValueError('The council is restricted to Syndicate face-card members: Jack and above.')
    import crime_operations
    if s.get('careers', {}).get('active') or crime_operations.read(s).get('active'):
        raise ValueError('Finish your current work or operation before attending council.')


def observe(s, e):
    now = s['world']['minute']
    actor = s['world']['cast'][s['player']]
    if (e.get('council_joined') and eligible(s) and actor['location'] == e['venue']
            and s['world']['location'] == e['venue'] and not actor.get('journey')
            and actor.get('activity') != 'Sleep' and e.get('last_attendance_minute') != now):
        e['last_attendance_minute'] = now
        e['attendance_minutes'] += 1
        if s['player'] not in e['attendees']:
            e['attendees'].append(s['player'])


def finish(s, e):
    if e.get('council_resolved'):
        return
    e['council_resolved'] = True
    attended = e.get('attendance_minutes', 0) >= 45
    e['memory_phase'] = 'completed' if attended else 'missed'
    if e.get('mandatory') and s['player'] == 'ivan':
        import careers
        d = careers.get(s, 'joker')
        if not attended:
            d['reliability'] = careers.clamp(d['reliability']-5)
            d['pressure'] = careers.clamp(d['pressure']+10)
        careers.record(s, 'joker', 'The Crow’s weekly face-card council: ' +
            ('mandatory attendance fulfilled.' if attended else
             'mandatory attendance missed or incomplete; reliability -5, pressure +10.'))
    s.setdefault('event_notifications', []).append(
        'Syndicate council: ' + ('attendance fulfilled.' if attended else 'attendance missed or incomplete.'))


def details(e):
    return ('Every Sunday, 20:00–21:00 · chaired by the Crow.\n' + ROLES +
            '.\n' + ('Mandatory for Ivan. ' if e.get('mandatory') else '') +
            'Travel to headquarters, join through Calendar, and remain for at least 45 game minutes. '
            f"Attendance: {e.get('attendance_minutes', 0)}/45 minutes · {e['memory_phase']}.")
