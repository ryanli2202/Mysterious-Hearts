"""Existing diplomatic appointments acquire one exact, persisted destination."""
ROOMS={
 'dragons':'syndicate__council_meeting_room','joker':'syndicate_office__appointment_room',
 'syndicate':'syndicate_hq__executive_meeting_room','shinokami':'site_01__briefing_room',
 'lantern':'lantern_house__meeting_room','rail':'saints_depot__meeting_room',
 'purple':'purple_clubhouse__meeting_room','hamayashi':'hamayashi_house__meeting_room',
 'rojos':'rojos_courtyard__meeting_room','waterfront':'consortium_house__boardroom',
}


def assign(s,meeting):
    import interiors
    if interiors.enabled(s,meeting['venue']) and meeting['status'] in ('booked','in_progress'):
        meeting.setdefault('room',ROOMS[meeting['target']])
    return meeting.get('room')


def require(s,meeting,attendee=True):
    import interiors
    if not interiors.enabled(s,meeting['venue']):return
    target=assign(s,meeting)
    __import__('interior_activities').require(s,target)
    who=meeting['attendee']
    if attendee and (not interiors.same_room(s,s['player'],who) or not interiors.available(s,who)):
        raise ValueError('The actual attendee must arrive in the assigned meeting room first.')
    others=set(interiors.occupants(s,target))-{s['player'],who}
    data=__import__('interior_presence').state(s)
    others.update(name for name,actor in data['local_actors'].items()
                  if name!=who and __import__('interior_presence').present(s,name) and actor.get('room')==target)
    if others:raise ValueError('Wait until the reserved meeting room has no unrelated listeners.')


def migrate(s,buildings):
    import interiors,crime_diplomacy
    for meeting in crime_diplomacy.commitments(s):
        crime_diplomacy.migrate_meeting(meeting)
        if interiors.building(meeting['venue']) not in buildings:continue
        target=assign(s,meeting)
        if meeting['status']!='in_progress':continue
        group=s.get('groups',{}).get(meeting.get('group'),{})
        if group.get('open') and interiors.same_building(s['world']['location'],meeting['venue']):
            __import__('interior_compat').assign(s,s['player'],target)
            actor=s['world']['cast'].get(meeting['attendee'])
            if actor and interiors.same_building(actor['location'],meeting['venue']) and not actor.get('journey'):
                __import__('interior_compat').assign(s,meeting['attendee'],target)
