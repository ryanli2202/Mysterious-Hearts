"""Room positions for existing local rosters and temporary workplace roles.

The original roster providers still decide who is at a building. This adapter
preserves their complete current-visit roster, then exposes only the current
physical room to legacy consumers. It never creates a personal contact.
"""
import interiors


def state(s):
    data = s.setdefault('interiors', {})
    data.setdefault('local_actors', {})
    data.setdefault('local_rosters', {})
    data.setdefault('work_roles', {})
    return data


def default_room(place, name):
    if place == 'cafe':
        return 'cafe__counter_seating_room'
    return __import__('interior_public').casual(place) if place in __import__('interior_public').DEFAULTS else interiors.ARRIVALS.get(place,place)


def restore(s):
    place = interiors.building(s['world']['location'])
    if not interiors.enabled(s, place):
        return
    saved = state(s)['local_rosters'].get(place, [])
    s['world']['npcs'] = list(dict.fromkeys([*s['world']['npcs'], *saved]))


def staff_roster(s):
    """Maya's established barista role uses the existing café shift hours."""
    if not interiors.enabled(s, 'cafe'):
        return
    data = state(s)
    world = s['world']
    hour = world['minute'] % 1440 / 60
    if not 8 <= hour < 20:
        record = data['local_actors'].get('Maya')
        if record and record.get('source') == 'cafe_staff_shift':
            record['activity'] = 'Off duty'
            if record['room'] in interiors.ROOMS and interiors.ROOMS[record['room']].policy == 'staff':
                interiors.walk_actor(s, 'Maya', 'cafe__counter_seating_room')
        return
    group = s.get('groups', {}).get(s.get('active_group'), {})
    record = data['local_actors'].get('Maya')
    away=world['location']!='cafe' or record and record.get('room')!='cafe__counter_seating_room'
    if group.get('open') and group.get('local') == 'Maya' and away:
        if world['minute'] < group.get('journal_started', world['minute']) + 30:
            return
        __import__('groups').close_active(s, 'Maya wraps up the visit to return to the café shift.')
    record = data['local_actors'].get('Maya')
    if not record or record['location'] != 'cafe' or record.get('room') not in interiors.ROOMS:
        record = dict(location='cafe', room='cafe__counter_seating_room', journey=None)
        data['local_actors']['Maya'] = record
    record.update(source='cafe_staff_shift', activity='Café staff shift')
    if not (group.get('open') and group.get('local')=='Maya') and record.get('room')!='cafe__counter_seating_room':
        interiors.walk_actor(s,'Maya','cafe__counter_seating_room')
    for place, roster in data['local_rosters'].items():
        if place != 'cafe' and 'Maya' in roster:
            roster.remove('Maya')
    world['npcs'] = [name for name in world['npcs'] if name != 'Maya']
    if world['location'] == 'cafe':
        world['npcs'].append('Maya')


def filter_roster(s):
    place = interiors.building(s['world']['location'])
    if not interiors.enabled(s, place):
        return
    data = state(s)
    names = list(dict.fromkeys(s['world']['npcs']))
    data['local_rosters'][place] = names
    for name in names:
        if name.startswith('Post guard · '):
            row=__import__('organisation_guards').npc_rows(s).get(name)
            if row:
                data['local_actors'][name]=dict(location=place,room=row['room'],journey=None,
                    activity='On guard duty',source='guard_post',guard_id=row['id'],faction=row['faction'])
                continue
        record = data['local_actors'].get(name)
        if not record or interiors.building(record['location']) != place or record.get('room') not in interiors.ROOMS:
            data['local_actors'][name] = dict(location=place, room=default_room(place, name),
                journey=None, activity='At the current venue', source='existing_local_roster')
    local_intent(s,names,place)
    s['world']['npcs'] = [name for name in names if present(s, name)]


LEADER_PRIVATE={
 'lantern_house':('private_flat_living_repair_room','private_bedroom'),
 'saints_depot':('private_converted_office_living_sleeping_room','private_converted_office_living_sleeping_room'),
 'purple_clubhouse':('private_residence_living_room','private_bedroom'),
 'hamayashi_house':('rear_residence_living_room','private_bedroom'),
 'rojos_courtyard':('upstairs_living_guitar_room','private_bedroom'),
 'consortium_house':('upper_apartment_living_chart_room','private_bedroom'),
}


def local_intent(s,names,place):
    """Existing source rosters establish attendance; this only selects rooms."""
    import gang_leaders,crime_diplomacy
    now=s['world']['minute'];group=s.get('groups',{}).get(s.get('active_group'),{})
    for name in names:
        record=actor(s,name)
        if not record or record.get('source')=='guard_post':continue
        if group.get('open') and group.get('local')==name and group.get('channel')!='text':continue
        if (place=='hamayashi_house' and s['player']=='rei' and s.get('rei_story',{}).get('stage')==5
                and name in ('Emi Suda','Ren Aoki','Daichi Kurose')):
            if interiors.walk_actor(s,name,'hamayashi_house__meeting_room'):
                record.update(activity='Answering the charter enquiry',room_until=now+40)
            continue
        assignment=s.get('job_apps',{}).get('pending') or {}
        if (name in assignment.get('coworkers',[]) and assignment.get('room') in interiors.ROOMS
                and now<assignment['deadline'] and interiors.same_building(place,assignment['venue'])):
            if interiors.walk_actor(s,name,assignment['room']):record['activity']='Assigned crew commission'
            continue
        meeting=next((m for m in crime_diplomacy.commitments(s) if m.get('attendee')==name and m['start']<=now<m['end']),None)
        if meeting:
            target=__import__('interior_meetings').assign(s,meeting)
            if target and interiors.walk_actor(s,name,target):record.update(activity='Leadership appointment',room_until=meeting['end'])
            continue
        if name in gang_leaders.BY_NAME and place in LEADER_PRIVATE:
            if record.get('room_until',-1)>now:continue
            hour=now%1440/60
            room=LEADER_PRIVATE[place][1] if hour>=23 or hour<7 else LEADER_PRIVATE[place][0] if hour>=20 else 'office' if place in ('lantern_house','rojos_courtyard','consortium_house') else __import__('interior_public').DEFAULTS[place]
            if interiors.walk_actor(s,name,place+'__'+room):
                record.update(activity='Sleep' if hour>=23 or hour<7 else 'Private downtime' if hour>=20 else 'Receiving visitors',room_until=now+40)


def actor(s, name):
    return s.get('interiors', {}).get('local_actors', {}).get(name)


def present(s, name):
    record = actor(s, name)
    if not record:
        return name in s['world'].get('npcs', [])
    if not interiors.same_building(record['location'], s['world']['location']):
        return False
    place = interiors.building(record['location'])
    roster = s.get('interiors', {}).get('local_rosters', {}).get(place, [])
    if name not in roster:
        return False
    return interiors.physical_room(s, name) == interiors.physical_room(s)


def count(s, ident):
    target = interiors.ROOMS[ident]
    physical = target.physical_space or ident
    data = s.get('interiors', {})
    names = data.get('local_rosters', {}).get(target.building, [])
    locals_here = sum(1 for name in names if not name.startswith('Post guard · ') and actor(s, name)
                      and interiors.same_building(actor(s, name)['location'], target.building)
                      and interiors.physical_room(s, name) == physical)
    roles = sum(1 for role in data.get('work_roles', {}).values()
                if role['expires'] > s['world']['minute'] and role['room'] in interiors.ROOMS
                and (interiors.ROOMS[role['room']].physical_space or role['room']) == physical)
    guards=len(__import__('organisation_guards').room_rows(s,ident))
    untracked=0
    if physical==interiors.physical_room(s):
        untracked=sum(1 for name in set(s['world'].get('npcs',[])) if not actor(s,name) and not name.startswith('Post guard · '))
    return locals_here + roles + guards + untracked


def depart(s, place):
    data = s.get('interiors', {})
    data.get('local_rosters', {}).pop(place, None)


def work_role(s, job, ident, expires):
    state(s)['work_roles'][job + ':supervisor'] = dict(id=job + ':supervisor',
        label='Workplace supervisor', room=ident, expires=expires, kind='workplace_role')


def visible_roles(s):
    return [role for role in s.get('interiors', {}).get('work_roles', {}).values()
            if role['expires'] > s['world']['minute'] and role['room'] == interiors.room(s)]
