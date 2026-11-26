"""Snapshot existing Bubblegram destinations without revealing another venue."""
MEETING={
 'syndicate':'syndicate__council_meeting_room','lantern_house':'lantern_house__meeting_room',
 'saints_depot':'saints_depot__meeting_room','purple_clubhouse':'purple_clubhouse__meeting_room',
 'hamayashi_house':'hamayashi_house__meeting_room','rojos_courtyard':'rojos_courtyard__meeting_room',
 'consortium_house':'consortium_house__boardroom','syndicate_hq':'syndicate_hq__cross_branch_operations_room',
 'syndicate_office':'syndicate_office__appointment_room','market':'market__public_stalls',
}


def assign(s,pending):
    import interiors
    if pending.get('kind')=='shift':return
    venue=pending['venue']
    if not interiors.enabled(s,venue):
        pending.setdefault('destination_kind','outdoor_district' if venue in ('downtown','blackhaven','market') else 'legacy_venue')
        return
    target=__import__('interior_compat').ROOMS.get(venue) or MEETING.get(venue)
    if target not in interiors.ROOMS:
        raise ValueError('This indoor contract needs an authored destination; the assignment is preserved.')
    if pending.get('room') and pending['room']!=target:
        raise ValueError('The saved contract destination needs an authored repair; progress is preserved.')
    pending.setdefault('room',target)
    pending['destination_kind']='outdoor_room' if interiors.ROOMS[target].outdoor else 'indoor_room'
    pending.setdefault('room_schema',1)


def require(s,pending):
    import interiors
    assign(s,pending)
    if not interiors.enabled(s,pending['venue']):return
    __import__('interior_activities').require(s,pending['room'])
    for who in pending.get('coworkers',[]):
        actor=__import__('interior_presence').actor(s,who)
        if not actor or not __import__('interior_presence').present(s,who) or not interiors.available(s,who):
            raise ValueError('Wait for the actual assigned coworkers in the contract room before resolving it.')


def migrate(s,buildings):
    pending=s.get('job_apps',{}).get('pending')
    if not pending or pending.get('kind')=='shift':return
    if __import__('interiors').building(pending['venue']) in buildings:assign(s,pending)
