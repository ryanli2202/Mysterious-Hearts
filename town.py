"""Deterministic town, economy and social progression; no AI needed."""
import custom_protagonist
import public_venues
import vacant_homes
import crime_sites
import crime_operations
import hidden_cast as hidden
import character_memory
import social_world
import emotions
import dating
import random
import town_residents
import keisuke
import gang_leaders
import character_types
import sexuality
import romantic_types
import world_loop as loop
from itertools import combinations

GIRLS = ('emily', 'sophie', 'amy', 'samantha', 'april') + hidden.ROMANCE
MALE_ROUTES = ('garrett', 'rei', 'minsu', 'ivan', 'dev', 'elliot', 'tyler', 'daniel')
LOCAL_MEN = ('Theo', 'Noah', 'Leo')
POSITIVE_FLIRTS = ('welcomed_flirt', 'returned_flirt')
SOCIAL_EVENTS = ('none', 'flirt', *POSITIVE_FLIRTS, 'disclosed_flirt', 'mistreatment', 'agreed_breakup')
BOND_BONUSES = {'personal_detail': (2, 2), 'chemistry': (2, 2), 'support': (2, 1), 'shared_laugh': (0, 1)}
BOND_MOMENTS = ('none', 'setback', *BOND_BONUSES)
BOND_GUIDE = (
    'Return bond_moments by participant ID for this completed exchange with the player. '
    'personal_detail means one of them learned something new and personal about the other. '
    'Use chemistry for a personal discovery that also shows clear, mutual romantic interest. '
    'Use support when one offered concrete care or reassurance and the other accepted it, '
    'shared_laugh for humor that landed between them, and setback for a rebuff, disrespect or crossed boundary. '
    'Use none for routine talk, observers, repeated information or unsent choices. Classify each person independently.'
)
LOCATIONS = {
    'square': 'Winterfield town square', 'flowers': 'Petal & Stem',
    'track': 'University track', 'cafe': 'Campus café',
    'arena': 'Arena lounge', 'chess': 'Chess café', 'boutique': 'Gift boutique',
    'home': 'Private residence',
    'marios_pizza': "Mario's Pizza",
    'blackstone_hq': 'Blackstone Headquarters',
    'interpol_hq': 'Interpol Regional Headquarters',
    'syndicate_office': 'Waterfront executive offices',
    hidden.HQ: 'Syndicate underground headquarters',
}
LOCATIONS.update({key: v[0] for key, v in public_venues.VENUES.items()})
LOCATIONS.update({data[0]: data[1] for data in loop.HOUSES.values()})
LOCATIONS.update({key: data['name'] for key, data in vacant_homes.HOMES.items()})
LOCATIONS.update({'iron_circle': 'The Iron Circle · Underground fighting ring', 'noodle_shop': 'Golden Dragon · Garrett’s noodle shop', 'syndicate': 'Red Dragons private lounge'})
LOCATIONS.update({'campus': 'Winterfield University', 'park': 'Riverside park', 'studio': 'Downtown modelling studio'})
LOCATIONS.update(gang_leaders.LOCATIONS)
import organisation_guards
LOCATIONS.update(organisation_guards.LOCATIONS)
LOCATIONS.update({'car:'+who: 'In transit with '+who.title() for who in loop.HOUSES})
import criminal_dynamics
LOCATIONS[criminal_dynamics.LAB] = criminal_dynamics.LAB_NAME
LOCATIONS.update({p['area']: p['area_name'] for p in hidden.CAST.values()})
LOCATIONS.update({key: 'Unlabelled site '+key[-2:]+' · '+spec['district'] for key, spec in crime_sites.SITES.items()})
LOCATIONS.update({room: 'Site '+key[-2:]+' · '+area for room,(key,area) in crime_operations.ROOMS.items()})
OCCUPATIONS = dict(zip(GIRLS, ('flowers', 'track', 'cafe', 'arena', 'chess')))
import interpol_cast
LOCATIONS.update(interpol_cast.LOCATIONS)
HOMES = {who: data[0] for who, data in loop.HOUSES.items()}


def location_name(s, location):
    owned=s.get('organisation_guards',{}).get('properties',{}).get(location)
    if owned: return owned['owner']+' · '+owned['use']+' · '+organisation_guards.PROPERTIES[location][0].removeprefix('Vacant ')
    if location in crime_operations.ROOMS:
        key,area=crime_operations.ROOMS[location]
        return crime_sites.label(s,key)+' · '+area.title()
    if location in crime_sites.SITES:
        return crime_sites.label(s, location)
    if s.get('custom_protagonist', {}).get('home') == location:
        return loop.HOUSES[s['player']][1]
    return LOCATIONS[location]

JOBS = {'cafe': ('Café shift', 180), 'flowers': ('Flower delivery', 220),
        'track': ('Fitness coaching', 350), 'chess': ('Private tutoring', 400)}
GIFTS = {'bouquet': ('Seasonal bouquet', 120, 'emily'),
         'plush': ('Handmade plushie', 90, 'emily'),
         'sports': ('Training accessories', 160, 'sophie'),
         'paints': ('Artist paint set', 180, 'amy'),
         'gloves': ('Premium training gloves', 240, 'samantha'),
         'chess': ('Carved chess set', 320, 'april')}
NPCS = [('Maya', 'barista', 'The campus café is hiring for flexible shifts.'),
        ('Theo', 'bookseller', 'A thoughtful gift says more than an expensive one.'),
        ('June', 'gardener', 'Emily puts a lot of care into her arrangements.'),
        ('Noah', 'student', 'People talk in Winterfield. Honesty travels, too.'),
        ('Iris', 'musician', 'I like the square best when the evening crowds arrive.'),
        ('Leo', 'courier', 'Walking around town is how you find the good stories.')]
WANDERING_NPCS = tuple(NPCS)
NPCS += [town_residents.profile(name) for name in town_residents.RESIDENTS]
NPCS.append(keisuke.PROFILE)
NPCS.extend(gang_leaders.PROFILES)
import gang_members
NPCS.extend(gang_members.PROFILES)

# Gameplay starting values: attraction is potential interest, not established romance.
STARTING_RELATIONSHIPS = {
    'minsu': {
        'emily': (0, 35, 0, 'strangers'),
        'sophie': (0, 85, 75, 'close sports-club friends'),
        'amy': (0, 85, 75, 'close friends and dorm neighbours'),
        'samantha': (0, 35, 0, 'strangers'),
        'april': (0, 35, 0, 'strangers'),
    },
    'garrett': {
        'emily': (8, 60, 30, 'friends'),
        'sophie': (22, 55, 35, 'party friends'),
        'amy': (24, 35, 5, 'interview contact'),
        'samantha': (38, 38, 8, 'new acquaintance'),
        'april': (8, 85, 75, 'childhood friends'),
    },
    'rei': {
        'emily': (58, 92, 88, 'close friends'),
        'sophie': (32, 72, 60, 'high school friends'),
        'amy': (28, 42, 7, 'interview contact'),
        'samantha': (42, 68, 45, 'fellow fighters'),
        'april': (6, 40, 10, 'new acquaintance'),
    },
}
for player in ('garrett', 'minsu'):
    STARTING_RELATIONSHIPS[player]['yuriko'] = (8, 45, 10, 'acquaintances')

RICHTER = 'Joseph Richter'
RICHTER_HISTORY = ('Joseph and Rei attended high school together in Winterfield after Rei arrived at fifteen. '
                   'Joseph helped lead a group that repeatedly bullied one of Rei’s closest friends. '
                   'That friend later died by suicide. Rei remembers what Joseph did. '
                   'Joseph minimises his own responsibility. Leave the friend unnamed and let the player decide what Rei says or feels.')

VENUE_STAFF = {
    'marios_pizza': ('Mario Romano', 'owner and pizza maker',
        'Mario runs the pizzeria. He marks orders on the boxes in pencil. Ask about the corner slice and he will turn the tray to show where the cheese browned against the pan.'),
    'blackstone_hq': ('Robin Vale', 'Blackstone reception clerk',
        'The visitor desk handles contractor badges and public appointments. Robin can explain how to replace a lost badge. Staff assignments and client files stay behind the access doors.'),
    'interpol_hq': ('Dana Lin', 'regional liaison desk officer',
        'Dana explains how to send a document to the right local investigator and why keeping the original matters. The public desk cannot confirm named subjects or share case files.'),
}
HQ_EXECUTIVE = (RICHTER, 'CEO of Blackstone',
    'Joseph is wealthy, mean and condescending. He talks over visitors, corrects trivial details and makes them justify taking up his time. '
    'He can answer a practical question while making the visitor feel small. He dismisses flirting and keeps private company business to himself.')

def sibling_route(s, who):
    return (s['player'], who) in (('rei', 'yuriko'), ('ivan', 'valentina'), ('yuriko', 'rei'), ('valentina', 'ivan'))

def romanceable(s, who):
    import playable_cast
    if playable_cast.is_new(s['player']):
        if s['player'] == 'sylvanis' or who in ('sylvanis', *playable_cast.EXCLUDED): return False
        if s['player'] in ('neo', 'alyssa') or who in ('neo', 'alyssa'):
            return {s['player'], who} == {'neo', 'alyssa'}
        return (character_types.is_major(who) and who != s['player'] and not sibling_route(s, who)
                and sexuality.compatible(s['player'], who))
    return (character_types.is_major(who) and who != s['player'] and not sibling_route(s, who)
            and who in (*GIRLS, 'yuriko', *MALE_ROUTES)
            and sexuality.compatible(s['player'], who))


def bond_schema(members):
    return {'type': 'object', 'properties': {who: {'type':'string', 'enum':list(BOND_MOMENTS)} for who in members},
            'required': list(members), 'additionalProperties': False}


def bond_moments(data, members, *, required=False):
    if not required and 'bond_moments' not in data:
        return {}
    moments = data.get('bond_moments')
    if (not isinstance(moments, dict) or set(moments) != set(members)
            or any(value not in BOND_MOMENTS for value in moments.values())):
        raise ValueError('Report one valid bond moment per conversation partner.')
    return moments

for roster in STARTING_RELATIONSHIPS.values():
    roster.update({who: (hidden.CAST[who]['attraction'], 35, 0, 'strangers') for who in hidden.ROMANCE})
STARTING_RELATIONSHIPS['ivan'] = {
    who: (0, 35, 0, 'strangers') for who in (*GIRLS, 'yuriko') if who != 'valentina'
}
ROMANTIC_STATUSES = ('dating', 'official', 'strained')

def starting_relationships(player):
    return {who: {'attraction': (romantic_types.initial_attraction(who, player, attraction)
                                   if status == 'strangers' else attraction),
                  'trust': trust, 'closeness': closeness,
                  'status': status, 'known_betrayals': []}
            for who, (attraction, trust, closeness, status)
            in STARTING_RELATIONSHIPS[player].items()}


def ensure(s, *, start_minute=None):
    import custom_protagonist
    custom_protagonist.restore(s)
    character_types.migrate(s)
    s.setdefault('emotions', {})
    s.setdefault('world', {'location': 'square', 'money': 100000, 'inventory': {},
                           'job': None, 'last_shift_day': 0, 'npcs': [], 'log': []})
    w = s['world']
    if start_minute is not None:
        w.setdefault('minute', start_minute)
    if w['location'] == 'blackstone_hq' and RICHTER not in w['npcs']:
        w['npcs'].append(RICHTER)
    hidden.ensure(s)
    s.setdefault('relationships', starting_relationships(s['player']))
    for who, r in starting_relationships(s['player']).items(): s['relationships'].setdefault(who, r)
    for r in s['relationships'].values():
        r.setdefault('attraction', r.pop('affection', 0))
        r.setdefault('closeness', 0)
    s.setdefault('friendships', {})
    if sibling_route(s, 'yuriko'):
        s['friendships'].setdefault('yuriko', dict(attraction=0, trust=98, closeness=95, status='close siblings'))
    if sibling_route(s, 'valentina'):
        s['friendships'].setdefault('valentina', dict(attraction=0, trust=98, closeness=95, status='close siblings'))
    for who in ('garrett', 'rei', 'minsu', 'ivan'):
        if 'ivan' in (who, s['player']):
            s['friendships'].setdefault(who, dict(attraction=0, trust=45, closeness=18, status='acquaintances'))
            continue
        close = s['player'] in ('garrett', 'rei') and who in ('garrett', 'rei')
        s['friendships'].setdefault(who, {'trust': 95 if close else 35, 'closeness': 90 if close else 0, 'status': 'best friends' if close else 'strangers'})
    for who in hidden.CAST:
        if who == 'sylvanis':
            s['friendships'].setdefault(who, dict(attraction=0, trust=5, closeness=0,
                status='hostile coworkers' if s['player'] == 'ivan' else 'strangers'))
            continue
        if who not in hidden.ROMANCE:
            introduced = s['player'] == 'ivan' and who in hidden.IVAN_STARTING_CONTACTS
            s['friendships'].setdefault(who, {'attraction':0, 'trust':45 if introduced else 35, 'closeness':12 if introduced else 0, 'status':'acquaintances' if introduced else 'strangers'})
    sexuality.reconcile(s)
    s.setdefault('girl_bonds', {key: bond[0] for key, bond in loop.BONDS.items()})
    loop.ensure(s)
    keisuke.ensure(s)
    gang_leaders.ensure(s)
    town_residents.refresh(s)
    import living_world
    living_world.ensure(s)
    import autonomy, messaging
    autonomy.ensure(s)
    messaging.ensure(s)
    import mysterious_hearts, contact_profiles
    mysterious_hearts.ensure(s)
    contact_profiles.ensure(s)
    if custom_protagonist.is_custom(s['player']) and not s.get('custom_arrival_initialized'):
        for roster in (s['relationships'], s['friendships']):
            for record in roster.values():
                record.update(attraction=0, trust=35, closeness=0, status='strangers')
        s['custom_arrival_initialized'] = True
    if 'home_visitors' not in w:
        home = loop.HOUSES[s['player']][0]
        visitors = set()
        for trip in w['journeys']:
            if trip['destination'] == home and trip.get('status') == 'arrived':
                visitors.update([trip['driver'], *trip['passengers']])
        visitors.update(who for who, actor in w['cast'].items() if actor['location'] == home)
        w['home_visitors'] = sorted(visitors - {s['player']})
    return w

def log(s, text):
    w = ensure(s)
    w['log'].append(loop.clock(s) + ': ' + text)
    w['log'] = w['log'][-80:]
    return text

def set_channel(s, who, channel):
    route = s['routes'][who]
    previous = route.get('channel', 'text' if not route['history'] else 'in_person')
    if previous == channel: return
    route['channel'] = channel
    if channel == 'text':
        import groups
        active = s.get('groups', {}).get(s.get('active_group'), {})
        if active.get('solo') == who:
            groups.close_active(s, who.title() + ' headed out.')
    place = LOCATIONS[ensure(s)['location']]
    text = (f'Phone texts → In-person conversation · {who.title()} · {place}'
            if channel == 'in_person' else 'Hangout ended · Back to phone texts')
    if who=='charles' and channel=='text': text='In-person conversation ended · Charles’s number is private'
    route['history'].append({'role': 'status', 'content': text})
    route.update(choices=[], personal_choices=[], action_choices=[], dialogue='', scene='', awaiting_since=None, followup_sent=False)

def meet(s, who):
    import combat
    combat.check_pair(s,who)
    if who not in s['routes'] or who == s['player']:
        raise ValueError('That person is not available to meet.')
    ensure(s)
    if not loop.together(s, who):
        raise ValueError(who.title() + ' is currently at ' + loop.place_name(s, who) + '.')
    hidden.mark_met(s, who)
    import meet_cute
    meet_cute.note_meeting(s, who)
    s['active'] = who
    set_channel(s, who, 'in_person')
    dating.begin(s, who)
    import groups
    groups.open_solo(s, who)
    if s['world']['cast'][who].get('waiting_for_hangout'):
        accept_hangout(s, who)


def accept_hangout(s, who):
    if who == 'charles': raise ValueError('Charles remains inside the Glasshouse; no outings.')
    if who == 'thirteen': raise ValueError('Number Thirteen receives reports at Pacific Relay Depot; no outings.')
    if who == 'takeo': raise ValueError('Takeo receives visitors at headquarters and does not join outings.')
    if who == 'crow':
        raise ValueError('The Crow receives visitors at headquarters and does not join outings.')
    w = ensure(s)
    actor = w['cast'][who]
    if loop.together(s, who) and s['routes'][who].get('channel') == 'in_person':
        actor.pop('waiting_for_hangout', None)
        if who not in w['party']:
            w['party'].append(who)
        set_channel(s, who, 'in_person')
        actor['activity'] = 'Hanging out'
    else:
        actor['waiting_for_hangout'] = True
        if not actor['journey']:
            actor['activity'] = 'Waiting to meet ' + custom_protagonist.display_name(s["player"])

def end_hangouts(s):
    import groups
    groups.close_active(s, 'Everyone headed out.')
    s.pop('hangout_contact', None)
    s['world']['party'] = []
    for who in s['routes']: set_channel(s, who, 'text')

def summon(s, who):
    if who == 'charles': raise ValueError('Charles remains inside the Glasshouse; no outings.')
    if who == 'thirteen': raise ValueError('Number Thirteen receives reports at Pacific Relay Depot; no outings.')
    if who == 'takeo': raise ValueError('Takeo receives visitors at headquarters and does not join outings.')
    if who == 'crow':
        raise ValueError('Visit The Crow at Syndicate headquarters.')
    w = ensure(s)
    if who == s['player'] or who not in s['routes'] or not hidden.contact(s, who):
        raise ValueError('Choose someone from your contacts.')
    actor = w['cast'][who]
    if w['cast'][s['player']]['journey']:
        raise ValueError('Arrive at your destination before summoning someone.')
    if actor['journey']:
        raise ValueError('They are already travelling. Wait for them to arrive first.')
    if not loop.together(s, who):
        loop.start_trip(s, who, w['location'])
    meet(s, who)
    accept_hangout(s, who)
    import groups
    groups.reconcile(s)
    group = s['groups'].get(s.get('active_group'), {})
    context = group.setdefault('meeting_context', {}).setdefault(who, {})
    context.update(kind='visitor', visitor=who, host=s['player'], location=w['location'], minute=w['minute'])
    return log(s, who.title() + ' joined you at ' + loop.place_name(s) + '.')

def travel(s, place, companion=None):
    ensure(s)
    if place == 'home': place = loop.HOUSES[s['player']][0]
    if companion and (s['active'] != companion or s['routes'][companion].get('channel') != 'in_person'):
        raise ValueError('Meet your companion before offering a shared drive.')
    passengers = list(dict.fromkeys(who for who in ([companion] if companion else []) + s['world'].get('party', [])))
    loop.start_trip(s, s['player'], place, passengers)
    s['world']['party'] = passengers
    import groups
    groups.reconcile(s)
    s['turn'] += 1


def finish_drive(s):
    loop.finish_drive(s)
    import groups
    groups.reconcile(s)

def select_car(s, model):
    w = ensure(s)
    if w['cast'][s['player']]['journey']:
        raise ValueError('Finish this drive before changing cars.')
    if model not in loop.player_garage(s):
        raise ValueError('Choose a car from your garage.')
    w['selected_car'] = model

def arrival_scene(s, arrivals):
    w = s['world']
    player = s['player']
    place = w['location']
    trip = arrivals.get(player)
    home = loop.HOUSES[player][0]
    scene = w.get('arrival_scene', {})
    if trip:
        scene = {'place': place, 'observations': {}}
        w['arrival_scene'] = scene
        w['npcs'] = [] if place.endswith('_home') or place in (hidden.HQ, criminal_dynamics.LAB) or place in crime_sites.SITES or place in crime_operations.ROOMS else [n[0] for n in random.sample(WANDERING_NPCS, random.randint(1, 3))]
        town_residents.refresh(s)
        date = s.get('date_session')
        if date and date.get('meeting_place') == place and date['partner'] not in w['npcs']:
            w['npcs'].append(date['partner'])
        if place in VENUE_STAFF:
            w['npcs'].append(VENUE_STAFF[place][0])
        if place == 'blackstone_hq':
            w['npcs'].append(RICHTER)
    elif place != home:
        return
    observations = scene.setdefault('observations', {})
    for who, actor in w['cast'].items():
        if who == player or actor['location'] != place or actor['activity'] == 'Sleep':
            continue
        if not trip and who not in arrivals:
            continue
        import autonomy
        plan=autonomy.person(s,who)['plan']
        if plan and plan['kind']=='visit' and not plan.get('accepted',True): continue
        route = s['routes'][who]
        familiar = sibling_route(s, who) or STARTING_RELATIONSHIPS[player].get(who, (0, 0, 0))[2] >= 30 or {who, player} == {'rei', 'garrett'}
        notes = []
        if trip and trip['vehicle'] not in route.setdefault('seen_vehicles', []):
            model = trip['vehicle']
            route['seen_vehicles'].append(model)
            detail = loop.player_garage(s).get(model, (0, model))[1]
            if who in trip['passengers']:
                notes.append(f'glances back at {detail} after getting out.')
            elif familiar:
                notes.append(f'spots {detail} and waves as you pull in.')
            else:
                notes.append(f'pauses to look at {detail}, then glances over to see who drove it.')
        if place == home and HOMES[who] != home and who not in w['home_visitors']:
            w['home_visitors'].append(who)
            if not familiar:
                notes.append({'minsu': 'steps around the taekwondo kit to read the titles on your stack of medical books.',
                              'rei': 'pauses beside the gothic statues before spotting the easel by the window.',
                              'ivan': 'leans over the piano to look at the pencilled harmony on the music stand.',
                              'garrett': 'walks to the terrace doors for a second look at the view from the estate.'}.get(player, 'looks around your new home.'))
        if notes:
            observations[who] = notes
            scene.setdefault('discussed', {}).pop(who, None)
        elif who in arrivals:
            observations.pop(who, None)
    if observations:
        scene['place'] = place
        w['arrival_scene'] = scene
    if trip and w['npcs']:
        witness = w['npcs'][0]
        detail = loop.player_garage(s).get(trip['vehicle'], (0, trip['vehicle']))[1]
        arrival = 'your chauffeur pulls up' if trip.get('chauffeur') else 'you park'
        observations[witness] = [f'turns for a closer look at {detail} as {arrival}.']

def arrival_notes(s, who):
    scene = s['world'].get('arrival_scene', {})
    if scene.get('place') == s['world']['location'] and who not in scene.get('discussed', {}):
        return scene['observations'].get(who, [])
    return []

def acknowledge_arrival(s, who):
    if arrival_notes(s, who):
        s['world']['arrival_scene'].setdefault('discussed', {})[who] = True


def wait(s, minutes=30):
    ensure(s); loop.advance(s, minutes)
    s['turn'] += 1
    return log(s, f'Waited {minutes} minutes.')


def npc_details(s, name):
    if name not in ensure(s)['npcs']: raise ValueError('That person has left this location.')
    if name.startswith('Post guard · '): return organisation_guards.npc_detail(s,name)
    if name == RICHTER and s['world']['location'] == 'blackstone_hq':
        return HQ_EXECUTIVE
    staff = VENUE_STAFF.get(s['world']['location'])
    if staff and staff[0] == name:
        return staff
    return next(n for n in NPCS if n[0] == name)

def generate_npc(s, name, reply):
    import guard_dialogue
    if guard_dialogue.is_guard(name): return guard_dialogue.generate(s, name, reply)
    import game_core as core
    import groups
    import json
    _, role, hook = npc_details(s, name)
    outcome=__import__('rei_story').context(s,name,[s['player']])
    if outcome: hook += ' SAVED OUTCOME OVERRIDES EARLIER BACKGROUND: '+outcome
    hook += ' ' + town_residents.context(name, s['world']['minute'])
    if name == RICHTER and reply is None and not s.get('npc_chats', {}).get(name) and not s.get('rei_story',{}).get('richter'):
        line = ('Takamura. I remember when you could walk past me without anybody asking for your picture. I preferred it.'
                if s['player'] == 'rei' else
                'Reception is right there. What made you think your question needed the chief executive?')
        return dict(narration='Richter checks his watch before the lift doors have finished closing.',
                    emotions={s['player']: emotions.current(s, s['player']), name: 'irritated'},
                    lines=[dict(speaker=name, text=line)],
                    choices=['I can speak to reception.', 'You could have just asked what I needed.',
                             'Do you bill by the second?', 'I’ll leave you to it.'])
    if name == RICHTER and s['player'] == 'rei':
        hook += ' ' + RICHTER_HISTORY + ' He recognises Takamura immediately. Their hostility is personal; Joseph resents being challenged about school.'
    player = core.PLAYERS[s['player']]
    styles = json.loads((core.ROOT/'dialogue_styles.json').read_text(encoding='utf-8'))
    system = (f'Write an in-person conversation between {name}, a local {role}, and {player} in Winterfield. '
              f'One detail {name} knows: {hook} Use it when relevant. Let the conversation move on. '
              'Use the recent exchange as context. Answer the latest player line in character. '
              'If opening the conversation, say something without inventing a greeting from the player. '
              'Give one brief observable narration, one spoken line from the local, and four distinct '
              'unsent spoken replies for the player. Respect familiarity and boundaries. Do not invent '
              'player actions, private knowledge or changes to world state.\n'
              + core.DIALOGUE_DIRECTION + '\nPlayer voice: ' + styles.get(s['player']+'_player', custom_protagonist.VOICE))
    history = s.get('npc_chats', {}).get(name, {}).get('history', [])
    if reply and reply.startswith(core.ACTION_PREFIX):
        system += '\nThe submitted player line is a physical action, not spoken dialogue. As Game Master, describe the action and its observable result in narration and respond naturally in dialogue. Never read the action aloud.'
    if arrival_notes(s, name) and reply is None:
        system += ' On opening, react in your own words to what you just noticed: ' + ' '.join(arrival_notes(s, name))
    import living_world
    return groups.generate_exchange([name], system, dict(living_world=living_world.context(s, [name]), location=loop.place_name(s), clock=loop.clock(s),
                                    calendar=loop.dates.context(s), relationship=character_stats(s,name),
                                    recent_exchange=history[-24:], player_reply=reply),
                                    state=s, members=[name], antagonist=name == RICHTER,
                                    kiss_targets=[name] if name in s['relationships'] and reply is not None and romanceable(s,name) else [],
                                    tones=core.REPLY_TONES if romanceable(s,name) else core.PLATONIC_TONES,
                                    submitted_tone=core.selected_tone(s, reply, npc=name), opening=reply is None)

def commit_npc(s, name, reply, result):
    import guard_dialogue
    if guard_dialogue.is_guard(name): return guard_dialogue.commit(s, name, reply, result)
    import combat
    combat.check_pair(s,name)
    if character_types.is_town(name):
        import town_npc_system
        return town_npc_system.commit(s, [name], reply, result)
    import game_core as core
    import groups
    import encounter_context
    encounter_context.validate(result, [name])
    npc_details(s, name)
    dating.check_conversation_step(s, name, result, reply is not None)
    groups.validate(result, [name])
    groups.validate_social(result,[name])
    groups.validate_spoken_exchange(result)
    goals = dating.check_progress(s, name, result, reply is not None)
    kiss = result.get('kissed_contact', 'none')
    if kiss != 'none' and (kiss != name or name not in s['relationships'] or reply is None or not present(s, name)):
        raise ValueError('Invalid kiss participant.')
    moment = bond_moments(result, [name]).get(name, 'none')
    tone = core.selected_tone(s, reply, npc=name)
    s['emotions'].update(emotions.turn_update(s, result, [name], tone=tone, player_acted=reply is not None))
    acknowledge_arrival(s, name)
    chat = s.setdefault('npc_chats', {}).setdefault(name, {'history': []})
    import memory_store
    memory_store.sync(s)
    if reply is not None:
        encounter_context.record(s, result, [name])
        chat.setdefault('connection', dict(status='acquaintances', trust=35, closeness=0))
        event = result.get('social_event','none')
        if event == 'none' and tone == 'Flirtatious':
            event = 'flirt'
        social_event(s, name, event, nearby_partners(s), setback=moment == 'setback')
        conversation_progress(s, name, moment, event)
        line = dict(speaker=core.PLAYERS[s['player']]+' (You)', text=reply, minute=s['world']['minute'])
        if reply.startswith(core.ACTION_PREFIX):
            line.update(kind='action', text=reply[len(core.ACTION_PREFIX):])
        chat['history'].append(line)
    chat['history'].append(dict(speaker='Narrator', text=result['narration']))
    chat['history'].extend({**line, 'minute': s['world']['minute']} for line in result['lines'])
    groups.sync_contacts(s)
    if name == RICHTER and s['player'] == 'rei':
        witnesses = [m for m in s['world']['party'] if loop.together(s, m)]
        if witnesses:
            exchange = ((f'Rei said “{reply}”. ' if reply else '') +
                        f'Joseph Richter said to Rei, “{result["lines"][0]["text"]}”')
            s.setdefault('shared_events', []).append(dict(minute=s['world']['minute'],
                text=exchange, witnesses=witnesses))
    social_world.record_notes(s, result, {name:result['lines'][0]['text']})
    import relationship_dynamics
    relationship_dynamics.commit(s, result, {name:result['lines'][0]['text']}, reply or '')
    chat['choices'] = result['choices']
    chat['personal_choices'] = result.get('personal_choices', [])
    chat['suggestions_requested'] = []
    chat['suggestions_deferred'] = result.get('suggestions_deferred', False)
    chat['ordered_tones'] = name != RICHTER
    if kiss == name and romanceable(s, name):
        betrayal(s, name, 'kiss')
        character_memory.record_first(s, name, 'kiss')
    if reply is not None:
        dating.advance(s, name, goals, kiss == name)
    dating.apply_conversation_step(s, name, result)
    s['turn'] += 1
    log(s, name + ': “' + result['lines'][0]['text'] + '”')
    memory_store.sync(s)

def work(s):
    import careers
    return careers.casual_work(s)

def buy(s, item):
    import phone_apps
    return phone_apps.order(s, 'Supafast', item)

def relationship_notice(s, who, note):
    if who in s['routes']:
        s['routes'][who]['history'].append({'role':'status','content':note})
    else:
        s['npc_chats'][who]['history'].append({'speaker':'Status update','text':note})


def present(s, who):
    if who in LOCAL_MEN: return who in s['world']['npcs']
    return loop.together(s,who)

def nearby_partners(s):
    return [key for key, rel in s['relationships'].items()
            if rel['status'] in ROMANTIC_STATUSES and present(s,key)]


def end_relationship(s, who):
    dating.cancel(s, who)
    r = s['relationships'][who]
    volatile = bool(r.get('unresolved_harm') or r['status'] == 'strained')
    kind = 'volatile' if volatile else 'amicable'
    r['status'] = 'exes' if volatile else 'friends'
    s['emotions'][who] = 'angry' if volatile else 'sad'
    r['attraction'] = max(0, r['attraction'] - (25 if volatile else 10))
    r['closeness'] = max(0, r['closeness'] - (20 if volatile else 2))
    cause = r.pop('unresolved_harm', None) or ('broken trust' if volatile else 'mutual agreement')
    r['jealousy'] = 0
    note = f'{kind.title()} breakup with {who.title()} · {cause}.'
    r.setdefault('breakups', []).append(dict(date=loop.clock(s), kind=kind, reason=cause))
    character_memory.record_first(s, who, 'breakup')
    relationship_notice(s,who,note)
    return note


def social_event(s, who, event, witnesses=(), *, setback=False):
    if character_types.is_town(who): return
    if event == 'none' or sibling_route(s, who) or who == 'sylvanis': return
    if event in POSITIVE_FLIRTS and not romanceable(s, who):
        event = 'flirt'  # An attempted advance never becomes reciprocal attraction.
    r = character_stats(s, who)
    if who in LOCAL_MEN and not r and event in POSITIVE_FLIRTS and not setback:
        chat = s.setdefault('npc_chats', {}).setdefault(who, {'history': []})
        r = chat.setdefault('connection', dict(status='acquaintances', attraction=0, trust=35, closeness=0))
    if event in ('flirt', *POSITIVE_FLIRTS):
        import protectiveness
        protectiveness.observe(s, who, event, witnesses,
                               physical=s['routes'].get(who, {}).get('channel') == 'in_person')
        for partner in set(witnesses) - {who}:
            rel = s['relationships'].get(partner)
            if rel and rel['status'] in ROMANTIC_STATUSES:
                rel['jealousy'] = min(100, rel.get('jealousy', 0) + (20 if rel['status']=='dating' else 30))
                s['emotions'][partner] = 'jealous'
                notice = f'{partner.title()} saw {custom_protagonist.display_name(s["player"])} flirting with {who.title()}.'
                rel.setdefault('milestones', []).append(loop.clock(s)+': '+notice)
                relationship_notice(s,partner,notice)
        if (r and event in POSITIVE_FLIRTS and romanceable(s, who) and not setback
                and r['status'] != 'strained' and not r.get('unresolved_harm')):
            gain = 2 if event == 'welcomed_flirt' else 3
            if event == 'returned_flirt' and who in (*MALE_ROUTES, *LOCAL_MEN):
                gain = 10  # Existing friendship-first romance routes unlock at 30.
            r['attraction'] = min(100, r.get('attraction', 0) + gain)
            if event == 'returned_flirt' and r['attraction'] >= 30 and who not in s['relationships']:
                s['relationships'][who] = dict(r, status='mutual interest', known_betrayals=[])
                note = 'The flirting between you and '+who.title()+' has become mutual interest.'
                relationship_notice(s,who,note)
                log(s,note)
    elif r and r['status'] in ROMANTIC_STATUSES:
        if event == 'disclosed_flirt':
            r['jealousy'] = min(100, r.get('jealousy', 0)+20)
            s['emotions'][who] = 'jealous'
            note = f'{custom_protagonist.display_name(s["player"])} told {who.title()} about flirting with someone else.'
            r.setdefault('milestones', []).append(loop.clock(s)+': '+note)
        elif event == 'agreed_breakup':
            log(s, end_relationship(s, who))
        elif event == 'mistreatment':
            repeated = bool(r.get('unresolved_harm'))
            s['emotions'][who] = 'angry' if repeated else 'disappointed'
            r['trust'] = max(0, r['trust']-15)
            r['unresolved_harm'] = 'mistreatment'
            r.setdefault('milestones', []).append(loop.clock(s)+': Hurt by mistreatment during the conversation.')
            if repeated: log(s, end_relationship(s, who))


def bond_key(s, a, b):
    return next((k for k in s['girl_bonds'] if set(k.split(':')) == {a,b}), ':'.join(sorted((a,b))))


def betrayal(s, target, activity):
    import consequences
    import protectiveness
    protectiveness.observe(s, target, activity, physical=(
        activity == 'a date' or s['routes'].get(target, {}).get('channel') == 'in_person'))
    consequences.observe(s, target, activity)


PIZZA_MENU = {
    'Cheese corner slice': (5, 'Mario cuts the browned edge loose from the pan with his spatula.'),
    'Pepperoni square': (6, 'Mario slides the square onto folded paper, catching a crisp curl of pepperoni before it rolls off.'),
    'Roasted pepper and mushroom slice': (6, 'Mario tears a basil leaf over the peppers just before serving.'),
}


def date_progress(s, who):
    r = s['relationships'][who]
    r['attraction'] = min(100, r['attraction'] + 15)
    r['closeness'] = min(100, r['closeness'] + 10)
    if r['status'] not in ROMANTIC_STATUSES:
        r['status'] = 'dating'
    s['emotions'][who] = 'happy'


def order_pizza(s, item, guests=(), date=False):
    w = ensure(s)
    if w['location'] != 'marios_pizza' or item not in PIZZA_MENU:
        raise ValueError("Choose a slice at Mario's Pizza.")
    guests = list(dict.fromkeys(guests))
    eligible = pizza_companions(s)
    if any(who not in eligible or not present(s, who) for who in guests):
        raise ValueError('Bring your friends or partner to the pizzeria before ordering.')
    if date:
        if len(guests) != 1 or not dating.in_hangout(s, guests[0]):
            raise ValueError('Ask them on a date first, then order together during your date.')
    price, serving = PIZZA_MENU[item]
    total = price * (1 + len(guests))
    if total > w['money']:
        raise ValueError(f'This order costs ${total}.')
    names = ', '.join(s.get('nicknames', {}).get(who) or who.title() for who in guests)
    company = ' on a date with ' + names if date else (' with ' + names if guests else '')
    note = f"{custom_protagonist.display_name(s["player"])} ordered {item.lower()} at Mario's Pizza{company} (${total}). {serving}"
    w['money'] -= total
    for who in guests:
        if not date:
            stats = character_stats(s, who)
            stats['closeness'] = min(100, stats['closeness'] + 2)
        relationship_notice(s, who, note)
    if guests:
        s.setdefault('shared_events', []).append(dict(minute=w['minute'], text=note, witnesses=guests))
    s['turn'] += 1
    w['camera_activity'] = dict(text=item + ': ' + serving, location=w['location'], minute=w['minute'])
    return log(s, note)


def pizza_companions(s):
    guests = list(loop.dates.outing_companions(s))
    date = s.get('date_session')
    if date and dating.in_hangout(s, date['partner']) and date['partner'] not in guests:
        guests.append(date['partner'])
    return guests


def relationship(s, who, action, item=None):
    __import__('combat').guard(s)
    if who in s.get('combat',{}).get('ruptures',[]): raise ValueError('Your attack permanently ruptured this relationship.')
    w = ensure(s)
    if who in sexuality.CANON and not sexuality.compatible(s['player'],who):
        raise ValueError(sexuality.reason(s['player'],who))
    if not romanceable(s, who) or who not in s['relationships']: raise ValueError('There is no mutual romantic interest yet.')
    if not hidden.known(s, who): raise ValueError('Meet this person first.')
    r = s['relationships'][who]
    if action in dating.ASK:
        reply = dating.generate_invitation(s, who, action)
        return dating.commit_invitation(s, who, action, reply)
    if action == 'gift' and not present(s, who):
        raise ValueError('Meet ' + who.title() + ' in town to spend time together.')
    if action == 'gift':
        import phone_apps
        gifts = phone_apps.gift_options(s)
        if item not in gifts or w['inventory'].get(item, 0) < 1: raise ValueError('Buy or collect this gift first.')
        if r['status'] == 'strained': raise ValueError('She needs accountability, not gifts. Talk and repair trust first.')
        w['inventory'][item] -= 1
        r['attraction'] = min(100, r['attraction'] + (12 if gifts[item][2] == who else 5))
        r['closeness'] = min(100, r['closeness'] + 5)
        s['emotions'][who] = 'grateful'
        text = f'{who.title()} received {gifts[item][0]} as a friendly gift.'
    elif action == 'breakup':
        if r['status'] not in ROMANTIC_STATUSES: raise ValueError('You are not in a romantic relationship.')
        text = end_relationship(s, who)
    elif action == 'repair':
        import relationship_dynamics
        if r.get('unresolved_harm'):
            raise ValueError('Talk about the specific hurt, take responsibility and follow through over time. Let them decide when to forgive.')
        if r['trust'] >= 100 and not r.get('jealousy') and not r.get('unresolved_harm'): raise ValueError('Trust is already full.')
        if r.get('repair_day') == s['world']['minute']//1440+1: raise ValueError('Give her time. You can make amends once per day.')
        r['repair_day'] = s['world']['minute']//1440+1
        r['trust'] = min(100, r['trust'] + 10)
        r['closeness'] = min(100, r['closeness'] + 3)
        r['jealousy'] = max(0, r.get('jealousy',0)-20)
        if r['trust'] >= 50 and not r['jealousy']: r.pop('unresolved_harm',None)
        if r['status'] == 'strained' and r['trust'] >= 50: r['status'] = 'official'
        s['emotions'][who] = 'guarded' if r.get('unresolved_harm') or r.get('jealousy') else 'relieved'
        text = f'Listened and made amends with {who.title()}. Trust improves gradually; past betrayals remain known.'
    else: raise ValueError('Unknown relationship action.')
    if action in character_memory.FIRSTS:
        character_memory.record_first(s, who, action)
    s['turn'] += 1
    if action == 'gift' and who in s['routes']: meet(s, who)
    s['relationships'][who].setdefault('milestones', []).append(loop.clock(s)+': '+text)
    s['relationships'][who]['milestones'] = s['relationships'][who]['milestones'][-30:]
    return log(s, text)


def become_official(s, who):
    if not romanceable(s, who): raise ValueError('This pairing is not romantically compatible.')
    r = s['relationships'][who]
    betrayal(s, who, 'an official relationship')
    r['status'] = 'official'
    r['closeness'] = min(100, r['closeness'] + 10)
    text = f'{who.title()} and {custom_protagonist.display_name(s["player"])} agreed to be exclusive.'
    for other, bond in s['relationships'].items():
        if other != who and bond['status'] == 'dating':
            s['girl_bonds'][bond_key(s, who, other)] = 'awkward about a former dating overlap'
            if who in s['routes'] and other in s['routes']:
                loop.bond_event(s, who, other, text, tension=15)
    character_memory.record_first(s, who, 'official')
    r.setdefault('milestones', []).append(loop.clock(s) + ': ' + text)
    log(s, text)

def finish_day(s):
    """Compatibility for old controls: rest without skipping the calendar."""
    return rest(s)


def rest(s):
    w=ensure(s)
    if w['location'] != loop.HOUSES[s['player']][0]: raise ValueError('Drive home before resting.')
    import autonomy
    autonomy.advance_player(s,'sleep')
    return log(s,'Resting at home. Time continues naturally.')



def context(s, viewer=None):
    import json
    import copy
    ensure(s)
    # Full histories remain in the save and UI; send a bounded recent snapshot to the AI.
    data = copy.deepcopy({k: s[k] for k in ('world', 'relationships', 'girl_bonds', 'bond_details', 'friendships')})
    data['calendar'] = loop.dates.context(s)
    import encounter_context
    import phone_apps
    members = (s.get('groups', {}).get(s.get('active_group'), {}).get('members', [])
               if viewer == 'group' else [viewer] if viewer else [s['active']])
    import living_world
    data['living_world'] = living_world.context(s, members)
    data['social_apps'] = phone_apps.conversation_context(s, members)
    data['meeting'] = encounter_context.for_participants(s, members)
    data['calendar']['celebrated_today'] = [key.split('/', 1)[1] for key in s.get('celebrations', [])
        if key.startswith(loop.dates.story_date(s['world']['minute']).isoformat() + '/')]
    for who in hidden.ensure(s):
        if not hidden.known(s,who):
            data['world']['cast'].pop(who, None)
            data['relationships'].pop(who, None)
            data['friendships'].pop(who, None)
    for who, actor in data['world']['cast'].items():
        if not hidden.visible_place(s, actor['location']):
            actor['location'] = 'private location'
            actor['activity'] = 'Busy'
        journey = actor.get('journey')
        if ((who in hidden.CAST and not hidden.ensure(s)[who]['home']) or
                (journey and not all(hidden.visible_place(s, p) for p in (journey['origin'], journey['destination'])))):
            actor['journey'] = None
    data['world']['journeys'] = [j for j in data['world']['journeys'] if hidden.known(s,j['driver']) and all(hidden.visible_place(s,p) for p in (j['origin'],j['destination']))]
    for field in ('girl_bonds', 'bond_details'):
        data[field] = {k:v for k,v in data[field].items() if all(hidden.known(s,who) for who in k.split(':'))}
    for roster in (data['friendships'], data['relationships']):
        for who, record in roster.items():
            record['friendship'] = social_world.friendship(s, who)
            record['romance'] = social_world.romance(s, who) or 'None'
            record['status'] = (record['friendship'] if record['romance'] == 'None' else record['romance']).lower()
        roster.pop(s['player'], None)
    data['world']['log'] = data['world']['log'][-10:]
    data['world'].pop('arrival_scene', None)
    data['world'].pop('home_visitors', None)
    data['world']['journeys'] = data['world']['journeys'][-5:]
    for bond in data['bond_details'].values(): bond['events'] = bond['events'][-3:]
    for relation in data['relationships'].values():
        relation['milestones'] = relation.get('milestones', [])[-4:]
        relation['known_betrayals'] = relation['known_betrayals'][-3:]
    if viewer:
        data['world'].pop('log', None)
        if data['world'].get('job') in ('Joker Card responsibilities','Red Dragons leadership','Iron Circle champion'):
            data['world']['job']='Private work'
        data['world'].pop('home_journal', None)
        data['calendar'].pop('celebrated_today', None)
        for who, relation in data['relationships'].items():
            if who != viewer:
                relation.pop('firsts', None)
                relation.pop('last_date', None)
                relation.pop('milestones', None)
                relation.pop('unresolved_harm', None)
                relation.pop('jealousy', None)
                relation.pop('breakups', None)
                relation.pop('confessed_at', None)
        if dating.session(s, viewer):
            data['your_date_with_player'] = dating.describe(s, viewer)
    if viewer:
        import consequences
        consequences.filter_context(s, data, members)
    if s['world']['location'] in vacant_homes.HOMES:
        data['current_residence'] = dict(vacant_homes.HOMES[s['world']['location']], status=vacant_homes.status(s, s['world']['location']))
    return json.dumps(data, ensure_ascii=False)


def character_stats(s, who):
    ensure(s)
    return s['relationships'].get(who) or s['friendships'].get(who) or s.get('npc_chats', {}).get(who, {}).get('connection')


def conversation_progress(s, who, moment='none', event='none'):
    """Daily familiarity plus up to three meaningful exchanges per person per day."""
    if character_types.is_town(who):
        import town_npc_system
        town_npc_system.familiarity(s, who)
        return
    r = character_stats(s, who)
    if (not r or r.get('status') == 'strained' or r.get('unresolved_harm') or moment == 'setback'
            or event in ('mistreatment', 'disclosed_flirt', 'agreed_breakup')):
        return
    day = s['world']['minute']//1440+1
    familiarizing = who in hidden.VENDETTA_CAST and r['status'] in ('acquaintances', 'friends')
    trust = closeness = 0
    if r.get('conversation_day') != day:
        r.update(conversation_day=day, bond_bonus_count=0)
        trust, closeness = (3 if familiarizing else 1), 2
    bonus = BOND_BONUSES.get(moment)
    if bonus is None and event in POSITIVE_FLIRTS and romanceable(s, who):
        bonus = (0, 1)
    if bonus and r.get('bond_bonus_count', 0) < 3:
        extra_trust, extra_closeness = bonus
        trust += extra_trust
        closeness += extra_closeness
        r['bond_bonus_count'] = r.get('bond_bonus_count', 0) + 1
        if moment == 'chemistry' and romanceable(s, who) and event not in POSITIVE_FLIRTS:
            r['attraction'] = min(100, r.get('attraction', 0) + 1)
    r['trust'] = min(100, r['trust'] + trust)
    r['closeness'] = min(100, r['closeness'] + closeness)
    if familiarizing and r['closeness'] >= 6:
        r['status'] = 'friends'


CAREERS = {
 'ivan': [('studio','Record vocals for an idol session',4500,9,18), (hidden.HQ,'Handle Joker Card executive business',6000,20,24)],
 'minsu': [],  # Medical study is not a licensed medical career or paid booking.
 'rei': [('studio','Modelling booking',4000,9,18), ('iron_circle','Iron Circle prize fight',8000,20,24)],
 'garrett': [('noodle_shop','Run the noodle shop',1500,9,18), ('syndicate','Handle Red Dragons business',5000,20,24)],
}
HOME_ACTIONS = {
 'ivan': ['Record a harmony at the piano', 'Practise martial arts footwork', 'Make seaweed soup for Valentina', 'Work on a song you own outright'],
 'minsu': ['Review medical lecture notes', 'Stretch after taekwondo training', 'Prepare a study snack', 'Unwind with music'],
 'rei': ['Paint at the easel', 'Write in your journal', 'Cook a comforting meal', 'Read and reflect in the library'],
 'garrett': ['Experiment with a noodle recipe', 'Train in the home gym', 'Relax on the terrace', 'Review personal business'],
}

def career_work(s, index):
    import careers
    import playable_cast
    if playable_cast.is_new(s['player']):
        if type(index) is not int or index != 0: raise ValueError('Choose an available career.')
        return careers.quick(s, 'cast_' + s['player'])
    keys={'rei': ('modelling','iron'), 'garrett': ('restaurant','dragons'), 'ivan': ('music','joker'), 'minsu': ()}
    if not isinstance(index,int) or not 0 <= index < len(keys[s['player']]):
        raise ValueError('Choose an available career.')
    return careers.quick(s,keys[s['player']][index])

def home_action(s, action):
    __import__('combat').guard(s)
    w=ensure(s)
    if w['location']!=HOMES[s['player']]: raise ValueError('Self actions are available at your own home.')
    if not isinstance(action,str) or not action.strip() or len(action)>2000: raise ValueError('Enter an action under 2,000 characters.')
    s['turn']+=1
    import autonomy
    needs=autonomy.person(s,s['player'])
    needs['social']=min(100,needs['social']+5)
    needs['happiness']=min(100,needs['happiness']+2)
    text=log(s,custom_protagonist.display_name(s["player"])+' · '+action.strip())
    w['camera_activity'] = dict(text=action.strip(), location=w['location'], minute=w['minute'])
    w.setdefault('home_journal',[]).append(text); w['home_journal']=w['home_journal'][-80:]
    return text
