"""Explicit Jobseek room stages, expiring work access and local role attendance."""
import interiors


from interior_workplaces import STAGES, STAFF_ROOMS, CAST_ROOMS


def targets(s, purpose):
    key = s.get('job_apps', {}).get('employment')
    return STAGES.get(key, {}).get(purpose, ())


def active(s):
    import job_apps
    key = s.get('job_apps', {}).get('employment')
    return (key in STAGES and interiors.enabled(s, job_apps.JOBS[key]['venue'])
            and interiors.same_building(s['world']['location'], job_apps.JOBS[key]['venue']))


def permitted(s, who, destination):
    if who!=s['player'] and who in CAST_ROOMS and destination in CAST_ROOMS[who]:
        import world_loop
        actor=s['world']['cast'].get(who,{})
        _,place,_=world_loop.appointment(who,s['world']['minute'])
        if interiors.same_building(place,interiors.ROOMS[destination].building) and not actor.get('journey'):
            return True
    career=s.get('interiors',{}).get('career_visits',{}).get(who)
    if who==s['player'] and career and career['expires']>s['world']['minute'] and destination in career['grants']:
        return True
    if who == 'Maya' and interiors.ROOMS[destination].building == 'cafe':
        record = __import__('interior_presence').actor(s, who)
        return bool(record and record['location'] == 'cafe' and 8 <= s['world']['minute'] % 1440 / 60 < 20
                    and destination in ('cafe__staff_kitchen', 'cafe__service_corridor'))
    visit = s.get('interiors', {}).get('work_visits', {}).get(who)
    return bool(who == s['player'] and visit and visit['expires'] > s['world']['minute']
                and visit['job'] == s.get('job_apps', {}).get('employment')
                and s['interiors']['grants'].get(who, {}).get(destination, -1) > s['world']['minute'])


def _grant(s, key, purpose, expires):
    rooms = STAGES[key][purpose]
    grants = s['interiors']['grants'].setdefault(s['player'], {})
    # Only actual staff rooms on the authored public-to-task route are granted.
    # A job can never turn a faction corridor or a bedroom into a work permit.
    for target in rooms:
        for ident in [*interiors.route(s, target), target]:
            room = interiors.ROOMS[ident]
            if room.policy == 'staff':
                grants[ident] = expires
    s['interiors'].setdefault('work_visits', {})[s['player']] = dict(
        job=key, purpose=purpose, rooms=list(rooms), start=s['world']['minute'], expires=expires)
    if purpose == 'development':
        __import__('interior_presence').work_role(s, key, rooms[0], expires)


def prepare(s, purpose='shift'):
    interiors._guard_action(s)
    if not active(s):
        raise ValueError('Travel to your supported workplace first.')
    import job_apps
    key = s['job_apps']['employment']
    if purpose not in STAGES[key]:
        raise ValueError('Choose a supported workplace task.')
    duration = 60 if purpose == 'shift' else 30
    data = job_apps.ensure(s)
    pending = data.get('pending')
    if pending and (purpose != 'shift' or pending.get('kind') != 'shift' or pending.get('key') != key):
        raise ValueError('Finish or withdraw the current assignment first.')
    now = s['world']['minute']
    start, end = job_apps.JOBS[key]['hours']
    deadline = pending['deadline'] if pending else now + duration
    if deadline <= now or not start * 60 <= now % 1440 < end * 60 or deadline > now // 1440 * 1440 + end * 60:
        raise ValueError('The whole task must fit within workplace hours.')
    job_apps.guard(s, job_apps.JOBS[key]['venue'], deadline - now)
    _grant(s, key, purpose, deadline)
    return 'Work access is ready. Go to ' + ' or '.join(interiors.ROOMS[r].label for r in STAGES[key][purpose]) + '.'


def require(s, purpose, pending=None, minutes=0):
    if not active(s):
        return
    key = s['job_apps']['employment']
    rooms = tuple(pending.get('rooms', ())) if pending else ()
    rooms = rooms or STAGES[key][purpose]
    if interiors.room(s) not in rooms:
        raise ValueError('Go to ' + ' or '.join(interiors.ROOMS[r].label for r in rooms) + ' before starting this task.')
    if interiors.ROOMS[interiors.room(s)].policy == 'staff':
        expiry = s['interiors']['grants'].get(s['player'], {}).get(interiors.room(s), -1)
        if expiry <= s['world']['minute'] or expiry < s['world']['minute'] + minutes:
            raise ValueError('Request fresh work access before continuing this task.')
    if purpose == 'development':
        role = s['interiors'].get('work_roles', {}).get(key + ':supervisor')
        if not role or role['room'] != interiors.room(s) or role['expires'] <= s['world']['minute'] or role['expires'] < s['world']['minute'] + minutes:
            raise ValueError('Arrange work access so the workplace supervisor can meet you here.')


def begin(s, pending):
    if not active(s):
        return
    key = pending['key']
    pending.update(room=interiors.room(s), rooms=list(STAGES[key]['shift']), room_schema=1)
    _grant(s, key, 'shift', pending['deadline'])


def cancel(s):
    visit = s.get('interiors', {}).get('work_visits', {}).get(s['player'])
    if not visit:
        return
    visit['expires'] = min(visit['expires'], s['world']['minute'])
    visit['cancelled'] = True
    role = s['interiors'].get('work_roles', {}).get(visit['job'] + ':supervisor')
    if role:
        role['expires'] = min(role['expires'], s['world']['minute'])
    current = interiors.room(s)
    if current in interiors.ROOMS and interiors.ROOMS[current].policy == 'staff' and not __import__('combat').active(s):
        interiors.evacuate(s, s['player'])
    __import__('world_loop').reconcile(s)


def migrate(s):
    pending = s.get('job_apps', {}).get('pending')
    if not pending or pending.get('kind') != 'shift' or pending.get('key') not in STAGES:
        return
    if not interiors.enabled(s, pending['venue']):
        return
    key = pending['key']
    authored=STAGES[key]['shift']
    if pending.get('room') and pending['room'] not in authored:
        raise ValueError('The saved work room needs an authored repair; the assignment has been preserved.')
    if pending.get('rooms') and any(room not in authored for room in pending['rooms']):
        raise ValueError('The saved work route needs an authored repair; the assignment has been preserved.')
    pending.setdefault('room', STAGES[key]['shift'][0])
    pending.setdefault('rooms', list(STAGES[key]['shift']))
    pending.setdefault('room_schema', 1)
    # Restore only a player whose saved active shift already places them here.
    # No attendees, time, payout, rank or deadline is manufactured.
    if interiors.same_building(s['world']['location'],pending['venue']):
        actor = s['world']['cast'][s['player']]
        if actor.get('room') == interiors.ARRIVALS[interiors.building(pending['venue'])]:
            __import__('interior_compat').assign(s,s['player'],pending['room'])
        _grant(s, key, 'shift', pending['deadline'])


def prepare_career(s,key,duration=60):
    interiors._guard_action(s)
    import careers
    spec=careers.TRACKS.get(key)
    if not spec or key not in careers.available(s):raise ValueError('Choose your own authored career.')
    if not interiors.enabled(s,spec['venue']) or not interiors.same_building(s['world']['location'],spec['venue']):
        raise ValueError('Visit the career workplace first.')
    now=s['world']['minute']
    booking=next((b for b in s.get('careers',{}).get('bookings',[]) if b['track']==key and b['status']=='booked' and b['start']<=now<b['end']),None)
    if booking:
        if now-booking['start']>15:raise ValueError('The 15-minute arrival window has passed. Cancel and rebook.')
        duration=booking['end']-now
    active=s.get('careers',{}).get('active')
    if active:
        if active['track']!=key:raise ValueError('Finish or abandon the other active career session first.')
        # Resume the existing stage; its deadline, choices and eventual payout
        # are retained. A short closing visit grants no second work session.
        duration=min(120,max(15,active['end']-s['world']['minute']))
    else:careers.guard(s,key,duration,booking=booking['id'] if booking else None,venue=spec['venue'])
    if (not active and not booking and duration not in (60,120)) or not spec['hours'][0]*60<=now%1440 or now%1440+duration>spec['hours'][1]*60:
        raise ValueError('The whole career visit must fit within workplace hours.')
    targets=__import__('interior_activities').career_targets(key,'finale' if booking and booking['kind']=='finale' else 'work')
    if not targets:raise ValueError('This indoor career needs an authored room mapping.')
    granted=[]
    for target in targets:
        for ident in [*interiors.route(s,target),target]:
            if interiors.ROOMS[ident].policy=='staff':
                s['interiors']['grants'].setdefault(s['player'],{})[ident]=now+duration
                granted.append(ident)
    s['interiors'].setdefault('career_visits',{})[s['player']]=dict(track=key,start=now,expires=now+duration,grants=list(dict.fromkeys(granted)))
    if active:career_roles(s,key,now+duration,room=active.get('room') or targets[0])
    elif booking and booking['kind']=='finale':career_roles(s,key,now+duration,room=targets[0])
    return 'Career access is ready. Go to '+' or '.join(interiors.ROOMS[target].label for target in targets)+'.'


def career_roles(s,key,end,room=None):
    room=room or interiors.room(s)
    if room not in interiors.ROOMS or not interiors.enabled(s,interiors.ROOMS[room].building):return
    import careers
    for index,label in enumerate(careers.TRACKS[key]['contacts']):
        s['interiors'].setdefault('work_roles',{})['career:'+key+':'+str(index)]=dict(
            id='career:'+key+':'+str(index),label=label,room=room,expires=end,source='authored_career_role')


def require_career_roles(s,key):
    if not interiors.enabled(s):return
    import careers
    for index,_ in enumerate(careers.TRACKS[key]['contacts']):
        role=s['interiors'].get('work_roles',{}).get('career:'+key+':'+str(index))
        if not role or role['room']!=interiors.room(s) or role['expires']<=s['world']['minute']:
            raise ValueError('Arrange career access so the actual review partners can meet you here.')
