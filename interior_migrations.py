"""Authored restoration for already-active work, reviews, dates and operations.

Called inside the activation transaction. No clock, money, victories, dialogue
choices, attendance or completion records are changed by these repairs.
"""


def bind(s,record,venue,target,people,buildings,allowed=None,unplaced=None):
    import interiors,interior_compat
    if interiors.building(venue) not in buildings:return
    if target not in interiors.ROOMS or not interiors.same_building(venue,interiors.ROOMS[target].building):
        raise ValueError('An active activity needs its authored room repair; its progress is preserved.')
    saved=record.get('room')
    if saved and saved not in (allowed or (target,)):
        raise ValueError('An active activity has an invalid saved room; restore a compatible checkpoint.')
    record.setdefault('room',target)
    record.setdefault('room_schema',1)
    target=record['room']
    for who in people:
        actor=s['world']['cast'].get(who)
        if (unplaced is None or who in unplaced) and actor and not actor.get('journey') and interiors.building(actor['location'])==interiors.building(venue):
            interior_compat.assign(s,who,target)


def restore(s,buildings,unplaced=None):
    import interiors,interior_activities as activities
    for booking in s.get('careers',{}).get('bookings',[]):
        if booking['status'] not in ('booked','in_progress') or interiors.building(booking['venue']) not in buildings:continue
        targets=activities.career_targets(booking['track'],'finale' if booking['kind']=='finale' else 'work')
        if not targets:raise ValueError('An indoor career booking needs an authored repair; progress is preserved.')
        if booking.get('room') and booking['room'] not in targets:raise ValueError('The saved career booking room needs an authored repair.')
        booking.setdefault('room',targets[0]);booking.setdefault('rooms',list(targets));booking.setdefault('room_schema',1)
    active=s.get('careers',{}).get('active')
    if active and interiors.building(active['venue']) in buildings:
        targets=activities.CAREERS.get(active['track'])
        if not targets:raise ValueError('This active indoor career stage has no authored destination; progress is preserved.')
        bind(s,active,active['venue'],targets[0],(s['player'],),buildings,allowed=targets,unplaced=unplaced)
        granted=[]
        for target in targets:
            for ident in [*interiors.path_between(interiors.ARRIVALS[interiors.building(active['venue'])],target),target]:
                if interiors.ROOMS[ident].policy=='staff':
                    s['interiors']['grants'].setdefault(s['player'],{})[ident]=active['end']
                    granted.append(ident)
        s['interiors'].setdefault('career_visits',{})[s['player']]=dict(track=active['track'],start=active['start'],expires=active['end'],grants=list(dict.fromkeys(granted)))
        __import__('interior_work').career_roles(s,active['track'],active['end'],room=active['room'])
    for who,record in s.get('laboratory_missions',{}).get('people',{}).items():
        active=record.get('active')
        if active:
            bind(s,active,'glasshouse_lab','glasshouse_lab__private_review_reunion_room',(who,active['partner']),buildings,unplaced=unplaced)
    for who,data in s.get('crime_operations',{}).get('people',{}).items():
        active=data.get('active')
        if active:
            place=active['site'];area='reception' if active['kind']=='reception' else 'briefing'
            target=__import__('interior_compat').ROOMS[place+'_'+area]
            bind(s,active,place,target,(who,active.get('colleague')),buildings,unplaced=unplaced)
    date=s.get('date_session') or {}
    if date.get('started'):
        place=s['world']['location']
        if interiors.building(place) in buildings:
            target=date.get('room') or __import__('interior_public').casual(place)
            bind(s,date,place,target,(s['player'],date['partner']),buildings,unplaced=unplaced)
    encounter=s.get('interpol',{}).get('encounter')
    fight=s.get('combat',{}).get('active')
    if encounter and fight and fight.get('kind')=='interpol':
        step=__import__('interpol').objective(s)
        target=activities.interpol_room(step)
        if target:
            team=s['interpol']['active']
            bind(s,encounter,step['venue'],target,(s['player'],team['partner'],step.get('opponent')),buildings)
            fight.setdefault('room',target)
    if fight and fight.get('kind') not in ('guard','interpol') and interiors.building(fight['location']) in buildings:
        venue=fight['location']
        target=fight.get('room') or __import__('interior_compat').ROOMS.get(venue)
        if not target:
            target='iron_circle__ring_hall' if fight['kind']=='circle' else {
                'arena':'arena__training_hall','boxing_club':'boxing_club__training_hall',
                'track':'track__outdoor_track'}.get(venue) if fight['kind']=='spar' else None
        target=target or __import__('interior_public').casual(venue)
        bind(s,fight,venue,target,(s['player'],fight.get('opponent'),fight.get('ally')),buildings)
