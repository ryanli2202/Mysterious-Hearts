"""Room reservations share event identity, time and participants with their source."""
import interiors


MEETING_ROOMS = {
    'rei_home': ('rei_home__living_space',),
    'cafe': ('cafe__counter_seating_room', 'cafe__quiet_study_room'),
    'syndicate_hq': ('syndicate_hq__members_lounge',),
    'glasshouse_lab': ('glasshouse_lab__rest_room',),
}
for _place in __import__('interior_public').DEFAULTS:
    MEETING_ROOMS.setdefault(_place,(__import__('interior_public').casual(_place),))


def participants(s, event):
    return tuple(dict.fromkeys([event.get('organizer', s['player']), *event.get('guests', [])]))


def records(s):
    for event in s.get('scheduled_events', []):
        if event.get('cancelled') or event.get('room') not in interiors.ROOMS:
            continue
        yield dict(id=event['id'], room=event['room'], start=event['start'], end=event['end'],
                   people=participants(s, event))
    for meeting in __import__('crime_diplomacy').commitments(s):
        target=meeting.get('room') or __import__('interior_meetings').ROOMS.get(meeting.get('target'))
        if target in interiors.ROOMS:
            yield dict(id=meeting['id'],room=target,start=meeting['start'],end=meeting['end'],
                       people=(s['player'],meeting.get('attendee') or __import__('crime_diplomacy').ATTENDEES[meeting['target']]))
    for who, visit in s.get('interiors', {}).get('work_visits', {}).items():
        if visit['purpose'] == 'development' and visit['rooms'] and not visit.get('cancelled'):
            yield dict(id=who+':work:'+visit['job'], room=visit['rooms'][0], start=visit.get('start', 0),
                       end=visit['expires'], people=(who, visit['job']+':supervisor'))


def validate(s, event, ident):
    if ident not in MEETING_ROOMS.get(interiors.building(event['venue']), ()):
        raise ValueError('Choose a public/shared meeting room at this venue.')
    target = interiors.ROOMS[ident]
    conflict=participant_conflict(s,participants(s,event),event['start'],event['end'],event['id'])
    if conflict:raise ValueError('A required participant already has a commitment during this appointment.')
    if len(participants(s, event)) > target.capacity:
        raise ValueError('This room does not have enough places for the participants.')
    if target.reservable:
        for record in records(s):
            if (record['id'] != event['id'] and record['room'] == ident
                    and event['start'] < record['end'] and record['start'] < event['end']):
                raise ValueError('This room is reserved. Choose another time or shared room.')


def participant_conflict(s,people,start,end,exclude=None):
    """Central hard-obligation conflicts; normal leisure/work remains lower priority."""
    people=set(people)
    import syndicate_council as council
    if people.intersection(council.ROSTER):
        week=council.week_start(start)
        for boundary in (week,week+council.WEEK):
            if start<boundary+60 and boundary<end:
                return dict(id='syndicate-council:'+str(boundary),start=boundary,end=boundary+60)
    for event in s.get('scheduled_events',[]):
        if event.get('cancelled') or event['id']==exclude:continue
        if start<event['end'] and event['start']<end and people.intersection(participants(s,event)):return event
    for meeting in __import__('crime_diplomacy').commitments(s):
        if meeting['id']==exclude:continue
        attendee=meeting.get('attendee') or __import__('crime_diplomacy').ATTENDEES[meeting['target']]
        if start<meeting['end'] and meeting['start']<end and people.intersection((s['player'],attendee)):return meeting
    for booking in s.get('careers',{}).get('bookings',[]):
        if s['player'] in people and booking['id']!=exclude and booking['status']=='booked' and start<booking['end'] and booking['start']<end:return booking
    pending=s.get('job_apps',{}).get('pending') or {}
    if s['player'] in people and pending.get('kind')=='shift' and start<pending['deadline'] and pending['started']<end:return pending
    active=s.get('careers',{}).get('active')
    if active and s['player'] in people and start<active['end'] and active['start']<end:return active
    return None


def access(s, who, ident):
    if not interiors.ROOMS[ident].reservable:
        return True
    now = s['world']['minute']
    return all(who in record['people'] for record in records(s)
               if record['room'] == ident and record['start'] <= now < record['end'])


def label(event):
    room = interiors.ROOMS.get(event.get('room'))
    return room.label if room else ''
