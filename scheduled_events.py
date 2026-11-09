"""Saved player appointments and game-clock reminders."""
from datetime import date
import uuid
import story_calendar as calendar


def create(s, title, day, time, venue, guests, duration=60, *, source=None):
    import town
    import hidden_cast
    day = date.fromisoformat(day)
    hour, minute = map(int, time.split(':'))
    if not 0 <= hour < 24 or not 0 <= minute < 60:
        raise ValueError('Enter a time from 00:00 to 23:59.')
    start = (day-calendar.START).days*1440 + hour*60 + minute
    guests = list(dict.fromkeys(guests))
    if not title.strip() or len(title.strip()) > 100:
        raise ValueError('Enter an event title of 1–100 characters.')
    if start <= s['world']['minute']:
        raise ValueError('Choose a future date and time.')
    if duration not in (30, 60, 90, 120, 180) or start%1440 + duration > 1439:
        raise ValueError('Choose a duration that ends before midnight.')
    if venue not in town.LOCATIONS or venue == 'home' or venue.startswith('car:') or not hidden_cast.visible_place(s, venue):
        raise ValueError('Choose a discovered venue.')
    if venue == 'iron_circle' and hour < 20:
        raise ValueError('The Iron Circle opens at 20:00.')
    import meet_cute
    app_invitation = source == 'meet_cute' and len(guests)==1 and meet_cute.can_schedule(s, guests[0])
    if app_invitation:
        proposal = meet_cute.ensure(s)['matches'][guests[0]]['proposal']
        app_invitation = proposal['start']==start and proposal['venue']==venue and duration==60
    if source is not None and not app_invitation:
        raise ValueError('This app invitation has not been mutually accepted.')
    if not guests or any(w == s['player'] or w not in s['world']['cast'] or not (hidden_cast.contact(s, w) or app_invitation) for w in guests):
        raise ValueError('Select at least one available contact.')
    import takeo
    import thirteen
    if 'thirteen' in guests and venue != thirteen.HQ:
        raise ValueError('Number Thirteen only meets in the depot command briefing room.')
    if 'takeo' in guests and venue != takeo.HQ:
        raise ValueError('Takeo only meets inside Shinokami headquarters.')
    if 'crow' in guests and venue != hidden_cast.HQ:
        raise ValueError('The Crow only meets inside Syndicate headquarters.')
    if venue == hidden_cast.HQ and any(not hidden_cast.hq_access(s, w) for w in [s['player'], *guests]):
        raise ValueError('Every guest needs access to this venue.')
    import careers
    if careers.conflict(s, start, start+duration):
        raise ValueError('You already have an event or career commitment at that time.')
    for e in s.get('scheduled_events', []):
        if not e.get('cancelled') and start < e['end'] and e['start'] < start+duration:
            raise ValueError('You already have an event at that time.')
    e = dict(id=uuid.uuid4().hex, title=title.strip(), venue=venue, guests=guests,
             start=start, end=start+duration, reminded=[], cancelled=False,
             created_minute=s['world']['minute'], memory_phase='planned', attendees=[])
    if app_invitation: e['source'] = 'meet_cute'
    s.setdefault('scheduled_events', []).append(e)
    import memory_store
    memory_store.event_record(s, e, 'planned')
    return e


def active(s, who, minute=None):
    now = s['world']['minute'] if minute is None else minute
    import syndicate_council
    council = syndicate_council.npc_event(s, who, now)
    if council:
        return council
    import crime_diplomacy
    if meeting := crime_diplomacy.npc_appointment(s, who, now):
        return meeting
    return next((e for e in s.get('scheduled_events', []) if not e.get('cancelled')
                 and who in e['guests'] and e['start'] <= now < e['end']), None)


def tick(s):
    import town
    import syndicate_council
    syndicate_council.ensure(s)
    now = s['world']['minute']
    for e in s.get('scheduled_events', []):
        if e.get('cancelled'): continue
        for lead in (60, 15):
            if now == e['start']-lead and lead not in e['reminded']:
                e['reminded'].append(lead)
                text = f"{e['title']} in {lead} minutes at {town.LOCATIONS[e['venue']]}."
                s.setdefault('event_notifications', []).append(text)
                town.log(s, text)
        if now == e['start']:
            e['memory_phase'] = 'in_progress'
            text = f"{e['title']} is starting at {town.LOCATIONS[e['venue']]}. Your guests have arrived."
            s.setdefault('event_notifications', []).append(text)
            town.log(s, text)
        if e.get('source') == syndicate_council.SOURCE and now >= e['end'] and not e.get('council_resolved'):
            syndicate_council.finish(s, e)
            release(s, e)
            town.log(s, e['title'] + ' ended.')
        elif now == e['end'] and e.get('source') != syndicate_council.SOURCE:
            import memory_store
            e['memory_phase'] = 'completed' if s['player'] in e.get('attendees', []) else 'missed'
            memory_store.event_record(s,e,e['memory_phase'])
            release(s, e)
            town.log(s, e['title'] + ' ended.')


def describe(e):
    import town
    return (f"{calendar.story_date(e['start']):%Y-%m-%d} · {e['start']%1440//60:02}:{e['start']%60:02}"
            f" · {e['title']} · {town.LOCATIONS[e['venue']]}")


def join(s, event):
    import town
    import groups
    now = s['world']['minute']
    if event.get('cancelled') or not event['start'] <= now < event['end']:
        raise ValueError('Join during the scheduled event time.')
    if s['world']['location'] != event['venue'] or s['world']['cast'][s['player']]['journey']:
        raise ValueError('Travel to the event venue first.')
    if event.get('source') == 'syndicate_council':
        import syndicate_council
        syndicate_council.join(s, event)
    if event.get('source') == 'meet_cute':
        import hidden_cast, meet_cute
        for who in event['guests']:
            if town.loop.together(s, who):
                hidden_cast.mark_met(s,who)
                meet_cute.note_meeting(s,who)
    gid = groups.form(s, event['guests'])
    if event.get('source') == 'syndicate_council':
        event['council_joined'] = True
        s['groups'][gid]['history'].append(dict(speaker='Status update', text=
            'The Crow chairs the weekly Syndicate face-card council. Both Jokers and the four Aces attend '
            'alongside senior face-card members. Branch reports, inter-organisation affairs and outstanding '
            'duties are on the agenda. Identities remain private; the Crow’s identity is never revealed.'))
    event['joined_group'] = gid
    observe(s)
    return gid


def release(s, event):
    import groups
    if event.get('joined_group') and s.get('active_group') == event['joined_group']:
        groups.close_active(s, event['title'] + ' has ended.')
        s['world']['party'] = [w for w in s['world']['party'] if w not in event['guests']]


def cancel(s, event):
    if event.get('source') == 'syndicate_council':
        raise ValueError('Only the Crow can cancel a council meeting. Attendance is mandatory for Ivan.')
    event['cancelled'] = True
    event['memory_phase'] = 'cancelled'
    import memory_store
    memory_store.event_record(s,event,'cancelled')
    release(s, event)


def observe(s):
    """Record actual co-presence, not merely an invitation or an elapsed appointment."""
    import memory_store
    now=s['world']['minute']
    for e in s.get('scheduled_events', []):
        if e.get('cancelled') or not e['start'] <= now < e['end']: continue
        if e.get('source') == 'syndicate_council':
            import syndicate_council
            syndicate_council.observe(s, e)
            continue
        actual=[w for w in [s['player'],*e['guests']] if s['world']['cast'][w]['location']==e['venue']
                and not s['world']['cast'][w]['journey']]
        attendees=e.setdefault('attendees',[])
        added=[w for w in actual if w not in attendees]
        if added:
            attendees.extend(added)
            e.setdefault('attendance',[]).append(dict(minute=now, present=actual))
            e['memory_phase']='attended'
            memory_store.event_record(s,e,'attended')
