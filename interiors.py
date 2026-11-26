"""Versioned room state, connected movement and room-local physical presence.

Building IDs remain the travel/save compatibility surface. Actor ``room`` is
authoritative; world.room mirrors the player's room. Unconverted buildings keep
one legacy scene. Reading state never advances time or rerolls a routine.
"""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    id: str
    building: str
    label: str
    neighbours: tuple
    art: str
    owners: tuple = ()
    private: bool = False
    bathroom: bool = False
    outdoor: bool = False
    capacity: int = 8
    safe_exit: str = ''
    physical_space: str = ''
    policy: str = 'shared'
    reservable: bool = False


def _penthouse():
    links = {
        'entrance': ('living_space',),
        'living_space': ('entrance', 'kitchen_and_dining', 'library', 'art_space', 'hallway'),
        'kitchen_and_dining': ('living_space',), 'library': ('living_space',),
        'art_space': ('living_space',),
        'hallway': ('living_space', 'rei_bedroom', 'yuriko_bedroom', 'bathroom'),
        'rei_bedroom': ('hallway',), 'yuriko_bedroom': ('hallway',),
        'bathroom': ('hallway',),
    }
    labels = {'kitchen_and_dining': 'Kitchen and dining', 'rei_bedroom': "Rei's bedroom",
              'yuriko_bedroom': "Yuriko's bedroom"}
    rooms = {}
    for key, edges in links.items():
        ident = 'rei_home__' + key
        owners = ('rei',) if key == 'rei_bedroom' else ('yuriko',) if key == 'yuriko_bedroom' else ()
        rooms[ident] = Room(ident, 'rei_home', labels.get(key, key.replace('_', ' ').capitalize()),
            tuple('rei_home__' + edge for edge in edges),
            'locations/rei_home' if key == 'living_space' else 'locations/interiors/rei_home/' + key,
            owners=owners, private=bool(owners), bathroom=key == 'bathroom',
            capacity=1 if key == 'bathroom' else 8, safe_exit='rei_home__entrance',
            physical_space='rei_home__shared_space' if key in ('living_space', 'kitchen_and_dining', 'art_space', 'library') else ident)
    return rooms


def _cafe():
    links = {
        'entrance': ('counter_seating_room',),
        'counter_seating_room': ('entrance', 'quiet_study_room', 'staff_kitchen', 'service_corridor', 'restroom'),
        'quiet_study_room': ('counter_seating_room',),
        'staff_kitchen': ('counter_seating_room', 'service_corridor'),
        'service_corridor': ('counter_seating_room', 'staff_kitchen', 'staff_office'),
        'staff_office': ('service_corridor',), 'restroom': ('counter_seating_room',),
    }
    result = {}
    for key, edges in links.items():
        ident = 'cafe__' + key
        result[ident] = Room(ident, 'cafe', key.replace('_', ' ').capitalize(),
            tuple('cafe__' + edge for edge in edges),
            'cafe-evening' if key == 'counter_seating_room' else 'locations/interiors/cafe/' + key,
            bathroom=key == 'restroom', capacity=1 if key == 'restroom' else 6 if key == 'quiet_study_room' else 10,
            safe_exit='cafe__entrance', physical_space=ident,
            policy='staff' if key in ('staff_kitchen', 'service_corridor', 'staff_office') else 'shared',
            reservable=key in ('quiet_study_room', 'staff_office'))
    return result


def _secure_pilots():
    result = {}
    layouts = {
        'syndicate_hq': ('security_foyer', 'council_chamber', ('council_chamber', 'executive_meeting_room', 'cross_branch_operations_room', 'members_lounge')),
        'glasshouse_lab': ('cleared_entrance', 'laboratory_workroom', ('laboratory_workroom', 'private_review_reunion_room', 'records_room', 'rest_room')),
    }
    for place, (entrance, original, branches) in layouts.items():
        links = {entrance: ('internal_corridor', 'restroom'),
                 'internal_corridor': (entrance, *branches), 'restroom': (entrance,)}
        links.update({key: ('internal_corridor',) for key in branches})
        for key, edges in links.items():
            ident = place + '__' + key
            capacity={'council_chamber':16,'executive_meeting_room':8,'cross_branch_operations_room':12,
                      'members_lounge':14,'private_review_reunion_room':6,'laboratory_workroom':10,
                      'records_room':6,'rest_room':8}.get(key,24)
            result[ident] = Room(ident, place, key.replace('_', ' ').capitalize(),
                tuple(place + '__' + edge for edge in edges),
                'locations/' + place if key == original else 'locations/interiors/' + place + '/' + key,
                bathroom=key == 'restroom', capacity=1 if key == 'restroom' else capacity,
                safe_exit=place + '__' + entrance, physical_space=ident, policy='security',
                reservable=key in ('council_chamber', 'executive_meeting_room', 'private_review_reunion_room'))
    return result


def _mavis_dispatch_exchange():
    """Neutral route venue: no ownership, faction membership or public unlock.

    Maps revelation and room access are enforced by the Ace route's explicit
    checks. This graph supplies ordinary arrival, walking and safe exit only.
    """
    place = 'mavis_dispatch_exchange'
    links = {'receiving': ('exchange',),
             'exchange': ('receiving', 'inner_room'),
             'inner_room': ('exchange',)}
    labels = {'receiving': 'Receiving passage', 'exchange': 'Dispatch exchange',
              'inner_room': 'Inner collection room'}
    art = {'receiving': 'locations/mavis-dispatch-receiving',
           'exchange': 'locations/mavis-dispatch-exchange',
           'inner_room': 'locations/mavis-dispatch-inner-room'}
    return {place + '__' + key: Room(
        place + '__' + key, place, labels[key],
        tuple(place + '__' + edge for edge in edges),
        art[key], capacity=12,
        safe_exit=place + '__receiving', physical_space=place + '__' + key,
        policy='security') for key, edges in links.items()}


def _martos_transfer_house():
    place='martos_transfer_house'
    links={'sitting':('departure','receiving'),'departure':('sitting','receiving'),'receiving':('sitting','departure')}
    return {place+'__'+key:Room(place+'__'+key,place,'Protected sitting room' if key=='sitting' else 'Witness records receiving room' if key=='receiving' else 'Covered departure court',tuple(place+'__'+edge for edge in edges),'locations/campaign/martos/'+('safe_stop' if key=='sitting' else 'receipt' if key=='receiving' else 'departure'),capacity=12,safe_exit=place+'__sitting',physical_space=place+'__'+key,policy='security') for key,edges in links.items()}


def _elias_theatre():
    place='elias_theatre'
    links={'stage':('dressing',),'dressing':('stage','receiving'),'receiving':('dressing','loading'),'loading':('receiving',)}
    labels={'stage':'Visiting production stage','dressing':'Private dressing room','receiving':'Booked affiliate receiving office','loading':'Secured service loading court'}
    return {place+'__'+key:Room(place+'__'+key,place,labels[key],tuple(place+'__'+edge for edge in edges),'locations/campaign/elias/'+({'stage':'stage_current','dressing':'dressing_current'}.get(key,key)),capacity=12,safe_exit=place+'__stage',physical_space=place+'__'+key,policy='security') for key,edges in links.items()}

def _camila_meridian():
    place='camila_meridian';links={'receiving':('sitting','loading'),'sitting':('receiving',),'loading':('receiving',)}
    labels={'receiving':'Booked Meridian receiving office','sitting':'Private household appointment room','loading':'Secured Meridian loading court'}
    return {place+'__'+key:Room(place+'__'+key,place,labels[key],tuple(place+'__'+edge for edge in edges),'locations/campaign/camila/'+key,capacity=12,safe_exit=place+'__receiving',physical_space=place+'__'+key,policy='security') for key,edges in links.items()}

def _sylvanis_arena():
    place='sylvanis_arena';links={'entry':('control','ring'),'control':('entry',),'ring':('entry',)}
    labels={'entry':'Private arena service entrance','control':'Exhibition control room','ring':'Underground testing arena'}
    art={'entry':'arena_entry','control':'arena_control','ring':'arena'}
    return {place+'__'+key:Room(place+'__'+key,place,labels[key],tuple(place+'__'+edge for edge in edges),'locations/campaign/sylvanis/'+art[key],capacity=12,safe_exit=place+'__entry',physical_space=place+'__'+key,policy='security') for key,edges in links.items()}

def _takeo_meridian():
    place='takeo_meridian';links={'entry':('command',),'command':('entry','research'),'research':('command','archive'),'archive':('research',)}
    return {place+'__'+key:Room(place+'__'+key,place,'Meridian '+key,tuple(place+'__'+edge for edge in edges),'locations/campaign/takeo/meridian_'+key,capacity=8,safe_exit=place+'__entry',physical_space=place+'__'+key,policy='security') for key,edges in links.items()}

def _ivan_network():
    labels={'receiving':'Network receiving desk','review':'Private network review room','practice':'Network practice room'}
    return {'ivan_network__'+key:Room('ivan_network__'+key,'ivan_network',label,tuple('ivan_network__'+other for other in labels if other!=key),'locations/campaign/ivan/'+key,capacity=12,safe_exit='ivan_network__receiving',physical_space='ivan_network__'+key,policy='security') for key,label in labels.items()}

def _neo_places():
    import neo_campaign_visuals as art
    groups={}
    for key in art.ROOM_ART:groups.setdefault(key.split('__')[0],[]).append(key)
    result={}
    for place,keys in groups.items():
        for index,key in enumerate(keys):
            edges=tuple(keys[j] for j in (index-1,index+1) if 0<=j<len(keys))
            result[key]=Room(key,place,key.split('__')[1].replace('_',' ').title(),edges,art.background(key),capacity=12,safe_exit=keys[0],physical_space=key)
    return result

ROOMS = _penthouse() | _cafe() | _secure_pilots() | _mavis_dispatch_exchange() | _martos_transfer_house() | _elias_theatre() | _camila_meridian() | _sylvanis_arena() | _neo_places() | _ivan_network() | _takeo_meridian()
ARRIVALS = {'rei_home': 'rei_home__entrance', 'cafe': 'cafe__entrance',
            'syndicate_hq': 'syndicate_hq__security_foyer', 'glasshouse_lab': 'glasshouse_lab__cleared_entrance'}
ARRIVALS['martos_transfer_house']='martos_transfer_house__sitting'
ARRIVALS['elias_theatre']='elias_theatre__stage'
ARRIVALS['camila_meridian']='camila_meridian__receiving'
ARRIVALS['sylvanis_arena']='sylvanis_arena__entry'
for _neo_key in _neo_places():ARRIVALS.setdefault(_neo_key.split('__')[0],_neo_key)
ARRIVALS['ivan_network']='ivan_network__receiving'
ARRIVALS['takeo_meridian']='takeo_meridian__entry'
ARRIVALS['mavis_dispatch_exchange'] = 'mavis_dispatch_exchange__receiving'
_candidate_rooms, _candidate_arrivals = __import__('interior_catalog').load(Room)
ROOMS.update(_candidate_rooms)
ARRIVALS.update(_candidate_arrivals)
__import__('interior_dorms').link(ROOMS,Room)
ACTIVATABLE = set(ARRIVALS)
ALIASES = {'yuriko_home': 'rei_home', 'ivan_home': 'valentina_home', 'alyssa_home': 'neo_home'}
SCHEMA = 2
ACTIVITIES = {
    'home.sleep': ('rei_home__rei_bedroom',),
    'home.cook': ('rei_home__kitchen_and_dining',),
    'home.paint': ('rei_home__art_space',),
    'home.read': ('rei_home__library',),
    'home.journal': ('rei_home__library', 'rei_home__rei_bedroom'),
    'rei_story.0': ('rei_home__art_space',),
    'rei_story.2': ('rei_home__art_space',),
    'social.RD02': ('rei_home__art_space',),
    'social.RD06': ('rei_home__library',),
    'social.RD18': ('rei_home__living_space',),
    'social.RD33': ('rei_home__library',),
    'social.RD35': ('rei_home__living_space',),
    'job.barista.shift': ('cafe__counter_seating_room', 'cafe__staff_kitchen'),
    'job.barista.development': ('cafe__staff_office',),
    'cafe.tea': ('cafe__counter_seating_room',),
    'cafe.casual_shift': ('cafe__counter_seating_room',),
}


def enabled(s, location=None):
    """Only dependency-complete sites may be activated by the rollout registry.

    Candidate room data alone must never enable a half-converted building.
    The saved list also permits real pilot stories without altering other saves.
    """
    state = s.get('interiors')
    if not isinstance(state, dict):
        return False
    activated = state.get('enabled_buildings', [])
    place = building(location or s['world']['location'])
    return isinstance(activated, list) and place in ACTIVATABLE and place in activated


def activate(s, location):
    if location not in ARRIVALS:
        raise ValueError('This building has no reviewed room graph.')
    if location not in ACTIVATABLE:
        raise ValueError('This candidate graph still needs its workplace, event and presence integration checks.')
    if location in __import__('interior_dorms').PLACES:__import__('interior_dorms').register()
    # Activation/migration commits a validated copy. An error cannot leave a
    # mixture of old actor positions and new event/work references in the save.
    import copy
    candidate = copy.deepcopy(s)
    data = candidate.setdefault('interiors', {})
    if not isinstance(data, dict):
        raise ValueError('The saved interiors state is damaged.')
    active = data.setdefault('enabled_buildings', [])
    if not isinstance(active, list):
        raise ValueError('The saved building rollout list is invalid.')
    if location not in active:
        active.append(location)
    ensure(candidate)
    s.clear()
    s.update(candidate)
    return location


def rollout(s):
    """Atomically migrate an ordinary game into the complete room catalogue.

    Called at the play boundary after loading, never from a simulation iteration holding
    references into the old state. Failed migrations leave the input untouched.
    """
    data=s.get('interiors', {})
    if (isinstance(data,dict) and data.get('rollout_version')==SCHEMA
            and set(data.get('enabled_buildings',[]))==ACTIVATABLE):
        return
    import copy
    candidate=copy.deepcopy(s)
    data=candidate.setdefault('interiors',{})
    if not isinstance(data,dict):raise ValueError('The saved interiors state is damaged.')
    saved=data.get('enabled_buildings',[])
    if not isinstance(saved,list) or any(place not in ARRIVALS for place in saved):
        raise ValueError('The saved building rollout list is invalid.')
    data['enabled_buildings']=sorted(ACTIVATABLE)
    __import__('interior_dorms').register()
    ensure(candidate)
    data['rollout_version']=SCHEMA
    s.clear()
    s.update(candidate)


def building(location):
    legacy=__import__('interior_compat').ROOMS.get(location)
    if legacy:
        return legacy.split('__',1)[0]
    return ROOMS[location].building if location in ROOMS else ALIASES.get(location, location)


def same_building(a, b):
    first,second=building(a),building(b)
    return first==second or first in __import__('interior_dorms').PLACES and second in __import__('interior_dorms').PLACES


def public_building(location):
    place=building(location)
    return 'nest_dorm_corridor' if place in __import__('interior_dorms').PLACES else place


def available(s, who):
    if __import__('neo_campaigns').suppressed(s,who):return False
    actor = actor_record(s, who)
    asleep_until = s.get('autonomy', {}).get('people', {}).get(who, {}).get('sleep_until') or 0
    return (not actor.get('journey') and asleep_until <= s['world']['minute']
            and (who == s['player'] or actor.get('activity') != 'Sleep'))


def room(s, who=None):
    who = who or s['player']
    actor = actor_record(s, who)
    place = building(actor['location'])
    if not enabled(s,place):
        return place
    candidate = actor.get('room')
    legacy=__import__('interior_compat').ROOMS.get(actor['location'])
    if legacy and actor.get('room_location')!=actor['location']:
        return legacy
    if candidate in ROOMS and ROOMS[candidate].building == place:
        return candidate
    return ARRIVALS.get(place, place)


def same_room(s, first, second):
    a, b = (actor_record(s, who) for who in (first, second))
    return (not a.get('journey') and not b.get('journey')
            and not str(a['location']).startswith('car:')
            and same_building(a['location'], b['location'])
            and physical_room(s, first) == physical_room(s, second))


def audible(s,first,second):
    """Only authored shared physical spaces expose live speech to listeners."""
    return same_room(s,first,second) and available(s,first) and available(s,second)


def actor_record(s, who):
    if who in s['world']['cast']:
        return s['world']['cast'][who]
    record = __import__('interior_presence').actor(s, who)
    if record is None:
        raise ValueError('This person is not present in a supported room.')
    return record


def occupancy(s, ident):
    return len(occupants(s, ident)) + __import__('interior_presence').count(s, ident)


def physical_room(s, who=None):
    ident = room(s, who)
    return (ROOMS[ident].physical_space or ident) if ident in ROOMS else ident


def occupants(s, ident):
    target = (ROOMS[ident].physical_space or ident) if ident in ROOMS else ident
    return [who for who, actor in s['world']['cast'].items()
            if not actor.get('journey') and physical_room(s, who) == target]


def ensure(s):
    """Additive migration, including only already-joined legacy participants.

    Never reconstruct old transcripts or move a merely co-located bystander into
    an active conversation. Invalid active rooms remain visibly repairable.
    """
    w = s['world']
    old = s.get('interiors')
    if old is not None and not isinstance(old, dict):
        raise ValueError('The saved interiors state is damaged; restore a compatible checkpoint.')
    if old:
        if any(not isinstance(old.get(key, {}), dict) for key in ('grants', 'visited')):
            raise ValueError('The saved room permissions are damaged; restore a compatible checkpoint.')
        if type(old.get('version', SCHEMA)) is not int:
            raise ValueError('The saved interiors version is invalid.')
        if not isinstance(old.get('enabled_buildings', []), list):
            raise ValueError('The saved building rollout list is invalid.')
        for grants in old.get('grants', {}).values():
            if not isinstance(grants, dict) or any(type(expiry) is not int for expiry in grants.values()):
                raise ValueError('The saved room permissions are damaged; restore a compatible checkpoint.')
    # Do not discard a malformed in-progress scene's exact saved position. The
    # original story remains intact for an authored repair/recovery mapping.
    if s.get('campaign_dialogue'):
        for who in (s['player'], *s.get('groups', {}).get(s.get('active_group'), {}).get('members', [])):
            actor = w['cast'].get(who, {})
            saved = actor.get('room')
            if saved is not None and saved not in ROOMS and building(actor.get('location')) in ARRIVALS:
                raise ValueError('This active scene has an unknown saved room; restore a compatible checkpoint before continuing.')
    state = s.setdefault('interiors', {'version': SCHEMA, 'grants': {}, 'visited': {}})
    if state.get('version', SCHEMA) > SCHEMA:
        raise ValueError('This story uses a newer interiors format.')
    state.setdefault('grants', {})
    state.setdefault('visited', {})
    migrated_buildings = state.setdefault('migrated_buildings', {})
    if not isinstance(migrated_buildings,dict) or any(type(version) is not int for version in migrated_buildings.values()):
        raise ValueError('The saved building migration versions are invalid.')
    if any(place not in ARRIVALS for place in state.get('enabled_buildings',[])):
        raise ValueError('The saved rollout references an unknown building.')
    pending_buildings={place for place in state.get('enabled_buildings',[]) if migrated_buildings.get(place,0)<SCHEMA}
    unplaced={who for who,actor in w['cast'].items() if actor.get('room') not in ROOMS
              or ROOMS[actor['room']].building!=building(actor['location'])}
    for event in s.get('scheduled_events', []):
        if (not event.get('cancelled') and event['end'] > w['minute']
                and enabled(s, event['venue'])):
            event.setdefault('room', event_room(s, event))
    first = 'version' not in state or not state.get('migrated')
    # Keep the player mirror in sync before validating legacy actor records.
    w['location'] = ALIASES.get(w['location'],w['location'])
    w['cast'][s['player']]['location'] = w['location']
    for who, actor in w['cast'].items():
        place = building(actor['location'])
        actor['location'] = ALIASES.get(actor['location'],actor['location'])
        legacy=__import__('interior_compat').ROOMS.get(actor['location'])
        if legacy and enabled(s,place) and actor.get('room_location')!=actor['location']:
            actor['room']=legacy
            actor['room_location']=actor['location']
        ident = actor.get('room')
        valid = ident in ROOMS and ROOMS[ident].building == place
        if enabled(s,place):
            if not valid:
                actor['room'] = ARRIVALS[place]
                actor['room_since'] = w['minute']
                actor['room_until'] = w['minute']
                actor.pop('zone', None)
                actor.pop('room_route', None)
        else:
            actor.pop('room', None)
            actor.pop('zone', None)
    if first or w['location'] in pending_buildings:
        __import__('interior_migrations').restore(s,pending_buildings,unplaced)
        __import__('interior_security').migrate(s, pending_buildings)
        __import__('interior_meetings').migrate(s,pending_buildings)
        for event in s.get('scheduled_events', []):
            if ((event.get('joined_group') or event.get('council_joined')) and event.get('room') in ROOMS
                    and event['start'] <= w['minute'] < event['end']
                    and event['venue'] == w['location'] and not event.get('cancelled')):
                w['cast'][s['player']]['room'] = event['room']
        active_scene = s.get('campaign_dialogue', {}) or {}
        action=active_scene.get('action')
        destination=None
        if action=='charles_quest.advance':
            destination=__import__('interior_activities').CHARLES.get(__import__('charles_quest').read(s)['step'])
        elif action=='rei_story.advance':
            destination=__import__('interior_activities').REI.get(s.get('rei_story',{}).get('stage',0))
        elif active_scene.get('social_id'):
            key=active_scene['social_id']
            destination=ACTIVITIES.get('social.'+key,(None,))[0]
            spec=__import__('campaign_prose').SOCIAL.get(key,{})
            if not destination and spec.get('venue')=='noodle_shop':destination='noodle_shop__dining_room'
        if destination in ROOMS and same_building(w['location'],ROOMS[destination].building):
            __import__('interior_compat').assign(s,s['player'],destination)
            active_scene.setdefault('room',destination)
            if action=='charles_quest.advance' and __import__('charles_quest').read(s)['step'] in (9,10,17):
                actor=w['cast'].get('charles',{})
                if building(actor.get('location'))=='glasshouse_lab' and not actor.get('journey'):
                    __import__('interior_compat').assign(s,'charles',destination)
        if active_scene.get('action') == 'rei_story.advance' and w['location'] == 'rei_home':
            stage = s.get('rei_story', {}).get('stage', 0)
            destination = ACTIVITIES.get('rei_story.' + str(stage))
            if destination:
                w['cast'][s['player']]['room'] = destination[0]
        player_room = room(s)
        participants = set(w.get('party', []))
        participants.update(active_scene.get('social_cast',[]))
        group = s.get('groups', {}).get(s.get('active_group'), {})
        if group.get('open') and group.get('channel', 'in_person') != 'text':
            participants.update(group.get('members', []))
        participants.update(who for who, route in s.get('routes', {}).items()
                            if route.get('channel') == 'in_person')
        for who in participants - {s['player']}:
            actor = w['cast'].get(who)
            if who in unplaced and actor and not actor.get('journey') and building(actor['location'])==building(w['location']):
                if player_room in ROOMS:
                    if room(s,who)==player_room or access(s,who,player_room)=='allowed':
                        __import__('interior_compat').assign(s,who,player_room)
                        actor['room_until'] = w['minute'] + 30
        state.update(version=SCHEMA, migrated=True)
    if pending_buildings:
        __import__('interior_work').migrate(s)
        __import__('interior_contracts').migrate(s,pending_buildings)
    for place in pending_buildings:
        migrated_buildings[place] = SCHEMA
    sync_player(s)
    return state


def require_activity(s, key):
    if not enabled(s):
        return
    targets = __import__('interior_residential').sleep_rooms(s) if key=='home.sleep' else ACTIVITIES.get(key)
    if key=='home.cook':targets=__import__('interior_residential').kitchen_rooms(s)
    if not targets:
        raise ValueError('This indoor activity has no authored room mapping.')
    if room(s) not in targets:
        raise ValueError('Go to ' + ' or '.join(ROOMS[target].label for target in targets) + ' first.')


def event_room(s, event):
    if event.get('sylvanis_appointment') and event.get('room') in ROOMS and enabled(s,event['venue']):return event['room']
    if enabled(s,event['venue']) and event['venue'] in __import__('interior_compat').ROOMS:
        return __import__('interior_compat').ROOMS[event['venue']]
    if enabled(s, event['venue']) and event['venue'] in ('syndicate_hq', 'glasshouse_lab'):
        if event.get('room'):
            return event['room']
        if event.get('source') == __import__('syndicate_council').SOURCE:
            return 'syndicate_hq__council_chamber'
        return event['venue'] + ('__members_lounge' if event['venue'] == 'syndicate_hq' else '__rest_room')
    if enabled(s, event['venue']) and event['venue'] == 'rei_home':
        return event.get('room', 'rei_home__living_space')
    if enabled(s, event['venue']) and event['venue'] == 'cafe':
        return event.get('room', 'cafe__counter_seating_room')
    if enabled(s,event['venue']):
        return event.get('room') or __import__('interior_public').casual(event['venue'])
    return event['venue']


def sync_player(s):
    w = s['world']
    actor = w['cast'][s['player']]
    # Legacy consumers still own building travel, never a second room position.
    if actor['location'] != w['location']:
        actor['location'] = w['location']
        actor.pop('room', None)
    if enabled(s,w['location']):
        actor['room'] = room(s)
        w['room'] = actor['room']
    else:
        w.pop('room', None)


def arrived(s, who):
    actor = s['world']['cast'][who]
    previous = ROOMS.get(actor.get('room'))
    if who == s['player'] and previous and previous.building != building(actor['location']):
        __import__('interior_presence').depart(s, previous.building)
    actor.pop('room', None)
    actor.pop('zone', None)
    actor.pop('room_route', None)
    actor['room_since'] = s['world']['minute']
    actor['room_until'] = s['world']['minute']
    place = building(actor['location'])
    if enabled(s,place):
        actor['room'] = ARRIVALS[place]
    grants = s.get('interiors', {}).get('grants', {})
    grants.pop(who, None)
    if who == s['player']:
        sync_player(s)


def access(s, who, destination):
    target = ROOMS[destination]
    current = room(s, who)
    if current == destination:
        return 'allowed'
    # Leaving a restricted room follows the authored outward route even after
    # expiry. It cannot grant a sideways shortcut into another restricted room.
    if current in ROOMS and ROOMS[current].policy != 'shared':
        exit_path = route(s, ROOMS[current].safe_exit, who)
        if exit_path and destination == exit_path[0]:
            return 'allowed'
    if who in __import__('interior_residential').owners_for(s,target):
        return 'allowed'
    if not __import__('interior_bookings').access(s, who, destination):
        return 'wait'
    others = [p for p in occupants(s, destination) if p != who]
    extra = __import__('interior_presence').count(s, destination)
    if target.bathroom and (others or extra):
        return 'wait'
    if len(others) + extra >= target.capacity:
        return 'wait'
    if target.private:
        expires = s.get('interiors', {}).get('grants', {}).get(who, {}).get(destination, -1)
        return 'allowed' if expires > s['world']['minute'] else 'knock'
    if target.policy == 'staff':
        return 'allowed' if __import__('interior_work').permitted(s, who, destination) else 'denied'
    if target.policy == 'security':
        return 'allowed' if __import__('interior_security').permitted(s, who, destination) else 'denied'
    if target.policy != 'shared':
        return 'denied'
    return 'allowed'


def request_work_access(s, purpose='shift'):
    """Minimum, expiring workplace access; never a faction credential."""
    if not enabled(s, 'cafe'):
        raise ValueError('The café workplace rollout is not ready.')
    _guard_action(s)
    ensure(s)
    import job_apps
    if s['world']['location'] != 'cafe' or job_apps.ensure(s).get('employment') != 'barista':
        raise ValueError('Only the employed café team can request this work access.')
    if purpose not in ('shift', 'development'):
        raise ValueError('Choose a supported workplace task.')
    duration = 60 if purpose == 'shift' else 30
    job_apps.guard(s, 'cafe', duration)
    now = s['world']['minute']
    start, end = job_apps.JOBS['barista']['hours']
    if not start * 60 <= now % 1440 <= end * 60 - duration:
        raise ValueError('The whole task must fit within workplace hours.')
    targets = ('cafe__staff_kitchen', 'cafe__service_corridor')
    if purpose == 'development':
        targets = ('cafe__service_corridor', 'cafe__staff_office')
    grants = s['interiors']['grants'].setdefault(s['player'], {})
    for target in targets:
        grants[target] = now + duration
    return 'Work access granted for this task; it expires within workplace hours.'


def _guard_action(s):
    import combat
    import flashback_visits
    flashback_visits.require_present(s)
    combat.guard(s, s['player'])
    if not available(s, s['player']):
        raise ValueError('Wake up before changing rooms.')
    if s.get('campaign_dialogue') or s.get('campaign_prose', {}).get('active'):
        raise ValueError('Finish the active story scene before changing rooms.')


def move(s, destination, *, companions=True):
    _guard_action(s)
    ensure(s)
    who = s['player']
    current = room(s)
    if current not in ROOMS or destination not in ROOMS[current].neighbours:
        raise ValueError('Choose an adjacent door.')
    outcome = access(s, who, destination)
    if outcome != 'allowed':
        raise ValueError('Knock and wait for permission.' if outcome == 'knock' else
                         'This door requires room-specific security clearance.' if outcome == 'denied' and ROOMS[destination].policy == 'security' else
                         'Request scoped work access before entering.' if outcome == 'denied' else
                         'This room is occupied. Wait outside.')
    w = s['world']
    following = [p for p in w.get('party', []) if same_room(s, who, p)] if companions else []
    group = s.get('groups', {}).get(s.get('active_group'), {})
    talking = ([p for p in group.get('members', []) if p in w['cast'] and p != who and same_room(s, who, p)]
               if group.get('open') and group.get('channel') != 'text' else [])
    if companions:
        following = list(dict.fromkeys([*following, *talking]))
    local = s.get('groups', {}).get(s.get('active_group'), {}).get('local')
    if (companions and local and not group.get('guard_session') and not str(local).startswith('Post guard · ')
            and __import__('interior_presence').actor(s, local)
            and __import__('interior_presence').present(s, local)):
        following.append(local)
    if any(not available(s, person) for person in following):
        raise ValueError('A companion is unavailable. Enter alone or wait for them.')
    if any(access(s, p, destination) != 'allowed' for p in following):
        raise ValueError('A companion cannot enter. Enter alone or choose another door.')
    target_space = ROOMS[destination].physical_space or destination
    additions = sum(physical_room(s, person) != target_space for person in set([who, *following]))
    if occupancy(s, destination) + additions > ROOMS[destination].capacity:
        raise ValueError('There is not enough room for the party. Enter alone or wait.')
    if not companions:
        w['party'] = list(dict.fromkeys([*w.get('party', []), *talking]))
    for person in (who, *following):
        actor = actor_record(s, person)
        __import__('interior_compat').assign(s,person,destination)
        actor.update(room_since=w['minute'], room_until=w['minute'] + 30)
        actor.pop('zone', None)
        actor.pop('room_route', None)
        s['interiors']['visited'].setdefault(person, [])
        if destination not in s['interiors']['visited'][person]:
            s['interiors']['visited'][person].append(destination)
    sync_player(s)
    __import__('town_residents').refresh(s)
    import world_loop
    world_loop.reconcile(s)
    import groups
    groups.reconcile(s)
    return destination


def knock(s, destination):
    _guard_action(s)
    ensure(s)
    current = room(s)
    if current not in ROOMS or destination not in ROOMS[current].neighbours:
        raise ValueError('Approach the door before knocking.')
    target = ROOMS[destination]
    if not target.private or target.bathroom:
        raise ValueError('This door does not accept social visits.')
    minute = s['world']['minute']
    for owner in __import__('interior_residential').owners_for(s,target):
        actor = s['world']['cast'].get(owner) or __import__('interior_presence').actor(s,owner)
        if not actor or actor.get('journey') or room(s, owner) != destination:
            continue
        if actor.get('activity') == 'Sleep' or 'sleep' in actor.get('room_activity', '').lower():
            continue
        rel = s.get('relationships', {}).get(owner, s.get('friendships', {}).get(owner, {}))
        household=__import__('interior_residential').HOUSEHOLDS.get(target.building,())
        if s['player'] not in household and rel.get('trust', 0) < 45:
            continue
        s['interiors']['grants'].setdefault(s['player'], {})[destination] = minute + 30
        return 'You are invited in for a short visit.'
    # No name or current private activity leaks through an unanswered door.
    return 'No invitation to enter. You can wait outside or leave.'


def route(s, destination, who=None):
    """Find a connected path; move() still checks every edge when traversing."""
    return path_between(room(s,who),destination)


def path_between(start,destination):
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        ident, path = queue.popleft()
        if ident == destination:
            return path
        for neighbour in ROOMS.get(ident, Room('', '', '', (), '')).neighbours:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append((neighbour, path + [neighbour]))
    raise ValueError('There is no connected route to that room.')


def walk_actor(s, who, destination):
    """Traverse every authorised edge; persist the remainder at a blocked door."""
    actor = actor_record(s, who)
    if destination not in ROOMS or not same_building(actor['location'],ROOMS[destination].building):
        return False
    if actor.get('journey'):
        raise ValueError('Arrive before changing rooms.')
    if __import__('combat').recovering(s, who):
        raise ValueError('A recovering person cannot change rooms.')
    if who == s['player'] or who in (s.get('campaign_dialogue') or {}).get('social_cast', []):
        __import__('combat').guard(s, who)
    steps = route(s, destination, who)
    if not steps and room(s,who)!=destination:
        return False
    for index, step in enumerate(steps):
        if access(s, who, step) != 'allowed':
            actor['room_route'] = steps[index:]
            return False
        __import__('interior_compat').assign(s,who,step)
        actor['room_since'] = s['world']['minute']
    actor.pop('room_route', None)
    return True


def evacuate(s, who, destination=None):
    """Follow the authored outward path after a permit ends; never grant entry."""
    actor = actor_record(s, who)
    current = room(s, who)
    if current not in ROOMS:
        return
    destination = destination or ROOMS[current].safe_exit
    for step in route(s, destination, who):
        __import__('interior_compat').assign(s,who,step)
        actor['room_since'] = s['world']['minute']
    actor.pop('room_route', None)
    actor.pop('zone', None)
    if who == s['player']:
        sync_player(s)
        __import__('town_residents').refresh(s)


def reunite(s, who):
    _guard_action(s)
    ensure(s)
    w = s['world']
    if who not in w.get('party', []) or not same_building(w['cast'][who]['location'], w['location']):
        raise ValueError('This companion is not waiting in this building.')
    if w['cast'][who].get('journey'):
        raise ValueError('This companion is still travelling.')
    if not available(s, who):
        raise ValueError('This companion is unavailable. Wait for them.')
    if not walk_actor(s, who, room(s)):
        return 'Your companion is waiting at a door they cannot enter.'
    return 'Your companion has rejoined you.'


def invite(s, who, destination):
    """Ask a present contact to continue together through an adjacent door."""
    _guard_action(s)
    if who==s['player'] or who not in s['world']['cast'] or not same_room(s,s['player'],who):
        raise ValueError('Invite someone who is here with you.')
    current=ROOMS.get(room(s))
    if not current or destination not in current.neighbours:
        raise ValueError('Choose an adjacent room for the invitation.')
    if not available(s,who):return 'They are unavailable. Try again later.'
    now=s['world']['minute']
    if __import__('interior_bookings').participant_conflict(s,[who],now,now+30):
        return 'They have a commitment. They suggest another time.'
    relation=s.get('relationships',{}).get(who,{})
    household=who in __import__('interior_residential').HOUSEHOLDS.get(building(s['world']['location']),()) and s['player'] in __import__('interior_residential').HOUSEHOLDS.get(building(s['world']['location']),())
    if (relation.get('unresolved_harm') or not household and relation.get('status') not in ('friends','dating','official')
            and relation.get('trust',0)<45):
        return 'They decline the invitation for now.'
    if access(s,who,destination)!='allowed':return 'They cannot enter that room. Choose another place together.'
    # Commit only after both people, the route and capacity have been validated.
    import copy
    candidate=copy.deepcopy(s)
    party=candidate['world'].setdefault('party',[])
    if who not in party:party.append(who)
    move(candidate,destination)
    s.clear();s.update(candidate)
    return 'They accept. You continue together in '+ROOMS[destination].label+'.'


def tick(s):
    ensure(s)
    w = s['world']
    minute = w['minute']
    for who, actor in w['cast'].items():
        if who == s['player'] or actor.get('journey') or not enabled(s, actor['location']):
            continue
        if who in (s.get('campaign_dialogue') or {}).get('social_cast', []):
            continue
        import scheduled_events
        if scheduled_events.active(s, who):
            continue
        # The existing building scheduler, obligations and conversations win.
        if s.get('routes', {}).get(who, {}).get('channel') == 'in_person' and same_room(s, who, s['player']):
            continue
        if who in w.get('party', []) and same_room(s, who, s['player']):
            continue
        if actor.get('room_until', -1) > minute:
            continue
        home_target=__import__('interior_residential').intent(s,who)
        if home_target:
            if walk_actor(s,who,home_target):
                actor.update(room_activity=actor.get('activity','At home'),room_until=minute+40)
            continue
        if actor['location'] in ('syndicate_hq', 'glasshouse_lab'):
            target = __import__('interior_security').intent(s, who)
            if target and walk_actor(s, who, target):
                actor['room_until'] = minute + 10
            continue
        if actor['location'] == 'cafe':
            intent = actor.get('activity', '').lower()
            target = 'cafe__quiet_study_room' if any(word in intent for word in ('study', 'reading')) else 'cafe__counter_seating_room'
            if walk_actor(s, who, target):
                actor.update(room_activity=actor.get('activity', 'Visiting the café'), room_until=minute + 40)
            continue
        if actor['location'] != 'rei_home' or who not in ('rei', 'yuriko'):
            target=__import__('interior_public').intent(s,who)
            if target and walk_actor(s,who,target):actor['room_until']=minute+40
            continue
        hour = minute % 1440 / 60
        if actor.get('activity') == 'Sleep':
            key, activity = who + '_bedroom', 'Sleeping'
        elif who == 'rei':
            key, activity = ('library', 'Reading') if hour >= 23 else ('art_space', 'Painting') if int(minute // 40) % 2 else ('kitchen_and_dining', 'Cooking')
        elif 18 <= hour < 19:
            key, activity = 'kitchen_and_dining', 'Dinner'
        else:
            choices = [('yuriko_bedroom', 'Private study and downtime'), ('living_space', 'Relaxing'),
                       ('art_space', 'Model building'), ('library', 'Reading')]
            key, activity = choices[int(minute // 40) % len(choices)]
        destination = 'rei_home__' + key
        # Routines use the same authored graph and never cross locked bedrooms.
        if destination != room(s, who):
            walk_actor(s, who, destination)
        actor.update(room_activity=activity, room_until=minute + 40)
    # Access expiry permits outward movement; no trapping anyone in a bedroom.
    for who, permissions in list(s['interiors']['grants'].items()):
        for ident, expiry in list(permissions.items()):
            if expiry <= minute:
                actor = w['cast'].get(who)
                if actor and ident in ROOMS and room(s, who) == ident and who not in ROOMS[ident].owners:
                    import combat
                    if combat.active(s):
                        continue  # Expired access is not extended; finish combat first.
                    if ROOMS[ident].policy == 'staff':
                        evacuate(s, who)
                    else:
                        __import__('interior_compat').assign(s,who,ROOMS[ident].neighbours[0])
                    if who == s['player']:
                        w.setdefault('log', []).append('The visit ended. You returned to a permitted waiting area.')
                del permissions[ident]
        if not permissions:
            s['interiors']['grants'].pop(who, None)
    reconcile_security(s)
    sync_player(s)


def reconcile_security(s):
    """A revoked internal permit returns each person along the outward route."""
    if __import__('combat').active(s):return
    for who,actor in s['world']['cast'].items():
        place=building(actor['location'])
        if not place.startswith('site_') or not enabled(s,place):continue
        ident=room(s,who)
        if ident not in ROOMS or ROOMS[ident].policy!='security':continue
        if __import__('interior_security').permitted(s,who,ident):continue
        destination=place+('__reception_public_displays' if place=='site_07' else '__reception')
        evacuate(s,who,destination)
        actor['activity']='Clearance expired · reception'


def label(s, who=None):
    ident = room(s, who)
    return ROOMS[ident].label if ident in ROOMS else ''


def art(s):
    target = ROOMS.get(room(s))
    if target and target.outdoor:
        current=__import__('weather').at(s['world']['minute'])
        return target.art,current['light'],current['condition']
    return target.art if target else None
