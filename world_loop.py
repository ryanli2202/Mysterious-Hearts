"""Persistent minute-based cast schedules, journeys, social bonds and message timers."""
import custom_protagonist
import hidden_cast as hidden
import four_aces
import copy
import json
import story_calendar as dates
from functools import lru_cache

# Model, total seats, and the detail a bystander can actually see.
GARAGES = {
    'ivan': {'Bentley Flying Spur Mulliner': (5, 'the midnight-blue Bentley with a little sailboat hanging from the mirror')},
    'garrett': {
        'Bugatti Chiron': (2, 'the gold accents against the white bodywork'),
        'Lamborghini Aventador': (2, 'the gold trim on the pearl-white Aventador'),
        'Lamborghini Huracán': (2, 'the light catching the metallic-gold Huracán'),
        'Rolls-Royce Phantom Extended': (5, 'the long white Phantom with its fine gold trim'),
        'Bentley Continental GT': (4, 'the ivory finish on the Bentley'),
        'Ferrari 812 Superfast': (2, 'the long red bonnet of the Ferrari'),
        'Mercedes-Maybach S 680': (4, 'the gold pinstripes on the dark Maybach'),
    },
    'rei': {'Audi R8': (2, 'the all-black Audi R8')},
    'minsu': {'Nissan Skyline GT-R (R34)': (4, 'the food and taekwondo stickers just below the blue Skyline’s rear spoiler')},
}
GROUP_VAN = 'Mercedes-Benz Sprinter passenger van'
IVAN_CHAUFFEUR = 'Mina Cho'

def player_garage(s):
    import playable_cast
    return playable_cast.garage(s['player']) if playable_cast.is_new(s['player']) else GARAGES[s['player']]


def selected_car(s, who):
    garage = player_garage(s) if who == s['player'] else GARAGES[who]
    choice = s['world'].get('selected_car') if who == s['player'] else None
    return choice if choice in garage else next(iter(garage))

def trip_vehicle(s, who, passenger_count):
    import playable_cast
    if who not in GARAGES and not (who == s['player'] and playable_cast.is_new(who)):
        return 'motorcycle' if who == 'samantha' else 'town car'
    model = selected_car(s, who)
    occupants = 1 + passenger_count + (who == 'ivan')  # Reserve Mina's seat on Ivan's trips.
    garage = player_garage(s) if who == s['player'] else GARAGES[who]
    return model if occupants <= garage[model][0] else GROUP_VAN

HOUSES = {
 'emily': ('emily_home', 'Emily’s garden apartment', 'A snug apartment above a quiet courtyard: pastel quilts, plushie shelves, a LEGO worktable and a balcony full of flowers.'),
 'sophie': ('sophie_home', 'Sophie’s trackside loft', 'A bright loft near campus with race bibs, a stretching corner, a meal-prep kitchen and a balcony overlooking the running paths.'),
 'amy': ('amy_home', 'Amy’s student dorm', 'An art-filled student dorm one dorm away from Minsu with a paint-splattered easel, philosophy books, thrifted armchairs and warm lamps by the window.'),
 'samantha': ('samantha_home', 'Samantha’s garage flat', 'A converted flat above a motorcycle garage: exposed brick, a heavy bag, a workbench and a surprisingly cosy kitchen.'),
 'april': ('april_home', 'April’s observatory townhouse', 'A quiet, orderly townhouse with a chess table, science books, a small lab desk and a rooftop telescope.'),
 'garrett': ('garrett_home', 'Garrett’s hillside estate', 'A lavish modern mansion with a noodle kitchen, gold accents, a terrace and a garage for his luxury car collection.'),
 'minsu': ('minsu_home', 'Minsu’s student dorm', 'One dorm away from Amy, with medical textbooks, study notes and space for his taekwondo kit.'),
 'rei': ('rei_home', 'Rei’s downtown penthouse', 'A gothic penthouse with a library, paintings, Yuriko’s scale models, a dedicated art space and an intimate kitchen high above the city.'),
}
HOUSES['yuriko'] = HOUSES['rei']
# Hour, place, activity. Travel takes real simulation minutes between appointments.
SCHEDULES = {
 'ivan': [(0,'valentina_home','Sleep'),(9,'studio','Vocals and choreography'),(14,'studio','Recording and publicity'),(18,'valentina_home','Dinner and martial arts practice'),(20,hidden.HQ,'Evening business meeting'),(23,'valentina_home','Writing songs')],
 'yuriko': [(0,'rei_home','Sleep'),(9,'campus','First-year theatre design lectures'),(12,'cafe','Lunch between classes'),(13,'campus','Scenic design workshop'),(16,'campus','Theatre crew rehearsal'),(18,'rei_home','Dinner and model building')],
 'minsu': [(0,'minsu_home','Sleep'),(9,'campus','Medical classes'),(13,'cafe','Study break'),(16,'track','Sports club and taekwondo training'),(19,'minsu_home','Medical study and downtime')],
 'emily': [(0,'emily_home','Sleep'),(8,'flowers','Flower-shop shift'),(17,'cafe','Tea break'),(19,'emily_home','LEGO and quiet evening')],
 'sophie': [(0,'sophie_home','Sleep'),(7,'track','Training'),(10,'campus','Classes'),(14,'track','Team practice'),(18,'cafe','Dinner'),(21,'sophie_home','Recovery')],
 'amy': [(0,'amy_home','Sleep'),(9,'campus','Philosophy seminars'),(13,'cafe','Interview and study time'),(17,'park','Sketching'),(20,'amy_home','Painting')],
 'samantha': [(0,'samantha_home','Sleep'),(10,'arena','Training'),(14,'arena','Sparring'),(18,'cafe','Dinner'),(20,'iron_circle','Fight night'),(23,'samantha_home','Rest')],
 'april': [(0,'april_home','Sleep'),(9,'campus','Independent research'),(14,'chess','Chess practice'),(18,'april_home','Science projects'),(22,'april_home','Stargazing')],
 'garrett': [(0,'garrett_home','Sleep'),(9,'noodle_shop','Running his noodle shop'),(18,'garrett_home','Dinner'),(20,'syndicate','Running the Red Dragons'),(23,'garrett_home','Evening at home')],
 'rei': [(0,'rei_home','Sleep'),(9,'studio','Modelling'),(14,'studio','Modelling'),(17,'rei_home','Painting and cooking'),(20,'iron_circle','Underground fighting'),(23,'rei_home','Reading')],
}
BONDS = {
 'alyssa:neo': ('Committed partners and housemates', 96, 94, 'Alyssa and Neo live together by choice. They cook dinner, trade co-op turns and ask before helping with each other’s work. Neither speaks for the other.'),
 'neo:tyler': ('Best friends since high school', 95, 92, 'Shared school years and the same after-school gym. Tyler saved Neo a place without demanding conversation; they still share controlled drills and dominoes.'),
 'neo:daniel': ('Best friends since high school', 95, 92, 'Daniel invited Neo to after-school films and let the quiet sit. They still argue gently about endings and play co-op games.'),
 'tyler:daniel': ('Best friends since high school', 92, 90, 'Tyler, Daniel and Neo stayed close after their overlapping school years; gym afternoons and cheap films became their standing rituals.'),
 'emily:sophie': ('High school friends', 78, 75, 'Shared school history; Sophie encourages Emily, whose gentleness balances Sophie’s self-pressure.'),
 'emily:amy': ('Quiet creative acquaintances', 48, 25, 'Flowers and painting offer common ground; both prefer patient conversation.'),
 'emily:samantha': ('Cautious acquaintances', 38, 18, 'Emily can find Samantha intense; Samantha respects direct boundaries.'),
 'emily:april': ('Reserved acquaintances', 45, 22, 'Both value thoughtful gestures, though April’s blunt precision can unsettle Emily.'),
 'sophie:amy': ('Campus acquaintances', 50, 32, 'Athletics and philosophy give them different campus circles and perspectives.'),
 'sophie:samantha': ('Competitive friends', 62, 48, 'Shared athletic drive creates mutual respect and spirited rivalry.'),
 'sophie:april': ('Friendly rivals', 48, 30, 'Instinct meets analysis; they disagree about preparation but respect effort.'),
 'amy:samantha': ('Curious acquaintances', 43, 20, 'Amy’s reflection and Samantha’s directness can complement or frustrate each other.'),
 'amy:april': ('Intellectual friends', 66, 45, 'Philosophy and science give them plenty to debate without always agreeing.'),
 'samantha:april': ('Wary respect', 42, 24, 'Action and analysis clash, but both appreciate competence and honesty.'),
}

ACE_BONDS = {}
for ace in four_aces.IDS:
    for colleague in ('ivan', 'sylvanis'):
        key = ':'.join(sorted((ace, colleague)))
        ACE_BONDS[key] = ('Established professional acquaintances', 55, 30,
                         'They know one another through private work. The nature of that work is not public.')
for colleague in ('ivan', 'sylvanis', *four_aces.IDS):
    kind = 'Respect and mutual tolerance' if colleague == 'sylvanis' else 'Blind service to the Cardmaster' if colleague in four_aces.IDS else 'Trusted professional subordinate'
    ACE_BONDS[':'.join(sorted(('crow', colleague)))] = (kind, 70, 35, 'They work closely under The Crow. These dealings are private; his identity remains unknown.')
BONDS.update(ACE_BONDS)

for who, p in hidden.CAST.items():
    if who == 'charles':
        HOUSES[who] = (hidden.charles_han.LAB, p['home'], p['interior'])
        SCHEDULES[who] = [(0, hidden.charles_han.LAB, p['activity'])]
        continue
    if who == 'thirteen':
        HOUSES[who]=(hidden.thirteen.HQ,p['home'],p['interior'])
        SCHEDULES[who]=[(0,hidden.thirteen.HQ,p['activity'])]
        continue
    if who == 'takeo':
        HOUSES[who] = (hidden.takeo.HQ, p['home'], p['interior'])
        SCHEDULES[who] = [(0, hidden.takeo.HQ, p['activity'])]
        continue
    if who == 'crow':
        HOUSES[who] = (hidden.HQ, 'Syndicate headquarters', 'No private residence is known.')
        SCHEDULES[who] = [(0, hidden.HQ, p['activity'])]
        continue
    HOUSES[who] = (who+'_home', p['home'], p['interior'])
    SCHEDULES[who] = [(0, who+'_home', 'Sleep'), (9, p['area'], p['activity']), (17, 'park', 'Unwinding outdoors'), (19, who+'_home', 'Quiet evening')]

BONDS['fox:gordon'] = ('Established operational partners', 78, 45, 'Gordon trusts Fox’s effectiveness against criminals and usually exercises discretion. Fox respects Gordon’s competence; their methods differ. Private case discoveries are not shared automatically.')
SCHEDULES['fox'] = [(0,'fox_home','Sleep'),(10,'blackhaven','Checking witness leads'),(13,'interpol_hq','Liaison with regional investigators'),(16,'fox_home','Maintaining equipment'),(19,'blackhaven','Patrolling Blackhaven'),(23,'fox_home','Reviewing observations')]
SCHEDULES['gordon'] = [(0,'gordon_home','Sleep'),(8,'interpol_hq','Receiving reports'),(12,'interpol_training','Controlled Biocreation practice'),(14,'interpol_briefing','Reviewing investigations'),(17,'blackhaven','Field investigation and patrol'),(20,'gordon_home','Dinner and reading')]

HOUSES['ivan'] = HOUSES['valentina']
HOUSES['alyssa'] = HOUSES['neo']
SCHEDULES['alyssa'] = [(0, 'neo_home', 'Sleep'), (9, 'archive', 'Repairing books and binding notebooks'),
                       (16, 'market', 'Choosing herbs and groceries'), (17, 'park', 'Botanical sketching'),
                       (19, 'neo_home', 'Cooking and co-op games with Neo')]
SCHEDULES['neo'] = [(0, 'neo_home', 'Sleep'), (9, 'makerspace', 'Repairing radios and game controllers'),
                    (16, 'boxing_club', 'Controlled drills at Tyler’s club'),
                    (18, 'cinema', 'Browsing the Bijou programme and catching up with Daniel when free'),
                    (19, 'neo_home', 'Cooking and a quiet evening with Alyssa')]

def migrate_yeun_home(s):
    """Resolve the former apartment in saved locations, including mid-drive saves."""
    world = s.get('world', {})
    actors = world.get('cast', {}).values()
    trips = [*world.get('journeys', []), *(a['journey'] for a in actors if a.get('journey'))]
    records = [world, *actors, *trips, *s.get('groups', {}).values(), world.get('arrival_scene', {})]
    home = HOUSES['ivan'][0]
    for record in records:
        for field in ('location', 'place', 'origin', 'destination'):
            if record.get(field) == 'ivan_home':
                record[field] = home
    if s['player'] == 'ivan' and world.get('selected_car') == 'Graphite Genesis G80':
        world['selected_car'] = next(iter(GARAGES['ivan']))

# Sociable contacts check in after one day; reserved contacts allow two.
SCHEDULES['sylvanis'] = [(0,'sylvanis_home','Sleep'), (8,hidden.HQ,'Coordinating Syndicate relations with Takeo Mishima'),
                         (10,'glasshouse_lab','Developing Blue Magic and Red Magic'),
                         (18,hidden.HQ,'Reviewing research supply and Syndicate business'), (23,'sylvanis_home','Reviewing research notes')]



@lru_cache(maxsize=4096)
def appointment(who, minute):
    if who in ('crow', 'takeo', 'thirteen', 'charles'): return SCHEDULES[who][0]
    import custom_protagonist
    if custom_protagonist.is_custom(who):
        return (0, HOUSES[who][0], 'Sleep' if minute % 1440 < 8*60 or minute % 1440 >= 23*60 else 'Settling into Winterfield')
    import leisure as outings
    hour = minute % 1440 / 60
    import faction_work
    shift = faction_work.appointment(who, minute)
    if shift: return shift
    if who in four_aces.IDS:
        # Stagger visits across a four-day rotation; retain ordinary cover schedules.
        if minute // 1440 % 4 == four_aces.IDS.index(who) and 20 <= hour < 22:
            return (20, hidden.HQ, 'Private evening appointment')
        return next(item for item in reversed(SCHEDULES[who]) if item[0] <= hour)
    # Keep these residents' slow mornings and quiet-home evenings, varying outings.
    if who in ('lena','naomi','celeste','dev','rosa','elliot'):
        free = dates.free_day(dates.story_date(minute))
        slot=11 if hour<14 else 14 if hour<17 else 17
        venue=outings.choose(who,minute//1440*1440+slot*60)
        activity=outings.ACTIVITIES[venue]
        if hour < 8: return (0, HOUSES[who][0], 'Sleep')
        if free:
            if hour < 11: return (8, HOUSES[who][0], 'An unhurried morning at home')
            if hour < 19: return (slot, venue, activity)
            return (19, HOUSES[who][0], 'A quiet evening at home')
        if 17 <= hour < 19:
            if minute//1440 % 3 == 0: return (17, HOUSES[who][0], 'A quiet evening after work')
            return (17, venue, activity)
    if who != 'sylvanis' and dates.free_day(dates.story_date(minute)):
        if hour < 8: return (0, HOUSES[who][0], 'Sleep')
        if hour < 11:
            place = next(item[1] for item in reversed(SCHEDULES[who]) if item[0] <= 14)
            return (8, place, 'Free time')
        if 20 <= hour < 22 and who in ('sophie', 'samantha', 'garrett', 'ivan', 'tyler'):
            place = outings.choose(who, minute//1440*1440+20*60, preferred=('nightclub', 'bar', 'bowling_alley', 'arcade'))
            return (20, place, outings.ACTIVITIES[place])
        if hour>=20: return (22 if who in ('sophie', 'samantha', 'garrett', 'ivan', 'tyler') else 20,HOUSES[who][0],'A quiet evening at home')
        slot=11 if hour<14 else 14 if hour<17 else 17
        place=outings.choose(who,minute//1440*1440+slot*60)
        return (slot,place,outings.ACTIVITIES[place])
    slot,place,activity=next(item for item in reversed(SCHEDULES[who]) if item[0] <= hour)
    if who!='sylvanis' and (place=='cafe' or activity=='Unwinding outdoors'):
        place=outings.choose(who,minute//1440*1440+slot*60,meals=place=='cafe')
        activity=outings.ACTIVITIES[place]
    return slot,place,activity

def ensure(s):
    w = s['world']
    w.setdefault('minute', (s['turn']//3)*1440 + (14,18,23)[s['turn']%3]*60)
    if w['location'] == 'home': w['location'] = HOUSES[s['player']][0]
    if 'cast' not in w:
        w['cast'] = {who: {'location': appointment(who,w['minute'])[1], 'journey': None,
                          'activity': appointment(who,w['minute'])[2]} for who in HOUSES}
        w['cast'].setdefault(s['player'], dict(location=w['location'], journey=None, activity='Settling into Winterfield'))
        w['cast'][s['player']]['location'] = w['location']
        # Preserve existing face-to-face saves without separating the pair on load.
        for who, route in s['routes'].items():
            if route.get('channel', 'in_person' if route.get('history') else 'text') == 'in_person': w['cast'][who]['location'] = w['location']
    for who in HOUSES:
        if who not in w['cast']:
            _, place, activity = appointment(who, w['minute'])
            w['cast'][who] = dict(location=place, journey=None, activity=activity)
    w['cast']['thirteen'].update(location=hidden.thirteen.HQ,journey=None,activity=hidden.CAST['thirteen']['activity'])
    w['cast']['takeo'].update(location=hidden.takeo.HQ, journey=None, activity=hidden.CAST['takeo']['activity'])
    w['cast']['crow'].update(location=hidden.HQ, journey=None, activity=hidden.CAST['crow']['activity'])
    w['cast']['charles'].update(location=hidden.charles_han.LAB, journey=None, activity=hidden.CAST['charles']['activity'])
    w.setdefault('journeys', [])
    w.setdefault('party', [])
    s.setdefault('groups', {})
    s.setdefault('active_group', None)
    w.setdefault('social_day', w['minute']//1440)
    if 'bond_details' not in s:
        s['bond_details'] = {key: {'type': v[0], 'trust': v[1], 'closeness': v[2],
                                  'tension': 0, 'key_points': [v[3]], 'events': []}
                             for key,v in BONDS.items()}
        for key, old in s.get('girl_bonds', {}).items():
            if key in s['bond_details'] and old not in ('neutral', BONDS[key][0]):
                s['bond_details'][key]['events'].append(old)
                s['bond_details'][key]['tension'] = 30
    for key in ('neo:tyler', 'neo:daniel', 'tyler:daniel', 'alyssa:neo', *ACE_BONDS):
        kind, trust, close, memory = BONDS[key]
        s['bond_details'].setdefault(key, dict(type=kind, trust=trust, closeness=close,
                                             tension=0, key_points=[memory], events=[]))
    # Correct the authored school history in existing saves without resetting bonds.
    bond = s['bond_details']['neo:tyler']
    bond['key_points'] = [point.replace('Different school years, same after-school gym.',
                                      'Shared school years and the same after-school gym.')
                          for point in bond.get('key_points', [])]
    for who, route in s['routes'].items():
        route.setdefault('unread', 0)
        if route.get('channel','text') == 'text' and route.get('dialogue'):
            route.setdefault('awaiting_since', w['minute'])
            route.setdefault('followup_sent', False)
    import crime_operations
    hidden.reconcile_hq_access(s)
    crime_operations.reconcile(s)
    import criminal_dynamics
    criminal_dynamics.reconcile_lab_access(s)
    import syndicate_council
    syndicate_council.ensure(s)
    return w

def clock(s):
    m=ensure(s)['minute']
    return f'{dates.story_date(m):%a, %b %d} · {m%1440//60:02d}:{m%60:02d}'

def together(s, who):
    import combat
    if combat.recovering(s,who) or combat.recovering(s): return False
    w=ensure(s)
    plan=s.get('autonomy',{}).get('people',{}).get(who,{}).get('plan')
    if plan and plan['kind']=='visit' and not plan.get('accepted',True): return False
    return w['cast'][who]['location'] == w['location']

def place_name(s, who=None):
    import town
    w=ensure(s); c=w['cast'][who or s['player']]
    j=c['journey']
    if not hidden.visible_place(s,c['location']) or (j and not all(hidden.visible_place(s,p) for p in (j['origin'],j['destination']))):
        return 'Private location'
    service = f" · Driven by {j['chauffeur']}" if j and j.get('chauffeur') else ''
    return (f"In {j['vehicle']}{service} · {town.LOCATIONS[j['origin']]} → {town.LOCATIONS[j['destination']]} · {max(0,j['arrives']-w['minute'])} min"
            if j else town.location_name(s, c['location']))

def event(s, text):
    import town
    import crime_operations
    if any(town.LOCATIONS[room] in text and s['world']['location'] != room for room in crime_operations.ROOMS): return
    import criminal_dynamics
    if criminal_dynamics.LAB_NAME in text and not criminal_dynamics.lab_access(s['player'], s): return
    if town.LOCATIONS[hidden.HQ] in text and not hidden.hq_access(s, s['player']): return
    if any((not hidden.known(s,who) and custom_protagonist.display_name(who) in text) or (not hidden.visible_place(s,who+'_home') and p['home'] in text) for who,p in hidden.CAST.items()): return
    w=s['world']; w['log'].append(clock(s)+': '+text); w['log']=w['log'][-120:]

def start_trip(s, who, destination, passengers=()):
    import combat
    fight=combat.active(s)
    for traveller in (who,*passengers):
        if traveller==s['player'] or (fight and traveller==fight['opponent']): combat.guard(s,traveller)
        elif combat.recovering(s,traveller): raise ValueError('This person is recovering from a knockout.')
    import town
    import crime_operations
    if 'charles' in (who, *passengers) and destination != hidden.charles_han.LAB:
        raise ValueError('Charles stays inside the Glasshouse.')
    if 'thirteen' in (who, *passengers) and destination != hidden.thirteen.HQ:
        raise ValueError('Number Thirteen receives reports at the depot command room.')
    if 'takeo' in (who, *passengers) and destination != hidden.takeo.HQ:
        raise ValueError('Takeo remains inside Shinokami headquarters.')
    if 'crow' in (who, *passengers) and destination != hidden.HQ:
        raise ValueError('The Crow remains inside Syndicate headquarters.')
    import criminal_dynamics
    if destination == criminal_dynamics.LAB and any(not criminal_dynamics.lab_access(p, s) for p in (who, *passengers)):
        raise ValueError('The Glasshouse requires personal clearance or Syndicate Jack rank in good standing for every traveller.')
    import interpol
    interpol.check_trip(s,who,destination,passengers)
    if s.get('campaign_dialogue') and who==s['player']:
        raise ValueError('Finish the scripted conversation before travelling.')
    import organisation_guards
    organisation_guards.check_trip(s,who,destination,passengers)
    crime_operations.check_trip(s,who,destination,passengers)
    w=ensure(s); actor=w['cast'][who]
    if destination == hidden.HQ and any(not hidden.hq_access(s, person) for person in (who, *passengers)):
        raise ValueError('Each traveller needs established Syndicate headquarters authorisation.')
    if who == s['player'] and not hidden.visible_place(s, destination): raise ValueError('Discover this home address first.')
    if destination not in town.LOCATIONS or destination == 'home' or destination.startswith('car:'): raise ValueError('Choose a destination.')
    if actor['journey']: raise ValueError('Finish the current journey first.')
    if actor['location'] == destination: raise ValueError('Already at that destination.')
    for person in passengers:
        if w['cast'][person]['location'] != actor['location'] or w['cast'][person]['journey']:
            raise ValueError('Your passenger must be here before departure.')
    if destination == 'iron_circle' and not 20*60 <= w['minute']%1440 < 1440:
        raise ValueError('The Iron Circle opens at 20:00. Wait until night.')
    vehicle = trip_vehicle(s, who, len(passengers))
    trip={'driver':who,'origin':actor['location'],'destination':destination,'departed':w['minute'],
          'arrives':w['minute'],'vehicle':vehicle,'passengers':list(passengers), 'status':'arrived'}
    if who == 'ivan':
        # The driver key identifies the cast member whose journey advances the car.
        trip['chauffeur'] = IVAN_CHAUFFEUR
    for person in (who,*passengers):
        w['cast'][person].update(location=destination,journey=None,activity='Arrived')
        import leisure
        needs=s.get('autonomy',{}).get('people',{}).get(person)
        if needs is not None and destination in leisure.ACTIVITIES:
            recent=needs.setdefault('recent_venues',[])
            if not recent or recent[-1]!=destination: recent.append(destination)
            needs['recent_venues']=recent[-6:]
    if s['player'] in (who,*passengers): w['location']=destination
    if who == s['player']: w.pop('arrival_scene', None)
    w['journeys'].append(copy.deepcopy(trip)); w['journeys']=w['journeys'][-100:]
    if trip.get('chauffeur'):
        event(s, f'{IVAN_CHAUFFEUR} drove Ivan to {town.LOCATIONS[destination]} in the {vehicle}.')
    else:
        event(s, f'{custom_protagonist.display_name(who)} arrived at {town.LOCATIONS[destination]} in {vehicle}.')
    town.arrival_scene(s, {person:trip for person in (who,*passengers)})
    reconcile(s)

def reconcile(s):
    import town
    for who,route in s['routes'].items():
        if route.get('channel') == 'in_person' and not together(s,who):
            town.set_channel(s,who,'text')
            route['history'].append({'role':'status','content':custom_protagonist.display_name(who)+' left the shared location.'})

def followups(s):
    """Evaluate saved messaging intentions; wording is generated asynchronously."""
    import messaging
    messaging.tick(s)


def advance(s, minutes, *, finish_day=False, combat_turn=False):
    __import__('flashback_visits').require_present(s)
    import combat
    if combat.active(s) and not combat_turn: raise ValueError('Finish the fight before advancing time elsewhere.')
    if combat.active(s) and combat_turn:
        if type(minutes) is not int or not 0<=minutes<=1: raise ValueError('Combat advances at most one minute per exchange.')
        s['world']['minute']+=minutes
        return
    combat.enforce(s)
    import town
    w=ensure(s)
    if not isinstance(minutes,int) or not 0 <= minutes <= 2880: raise ValueError('Invalid time interval.')
    import phone_apps
    phone_apps.sync(s)
    for _ in range(minutes):
        w['minute']+=1
        import relationship_dynamics
        relationship_dynamics.tick(s)
        if w['minute']%1440==8*60:
            import emotions
            for who, feeling in s['emotions'].items():
                s['emotions'][who]=emotions.NEXT_MORNING.get(feeling,feeling)
        import scheduled_events
        scheduled_events.tick(s)
        import crime_operations
        crime_operations.reconcile(s)
        import criminal_dynamics
        criminal_dynamics.reconcile_lab_access(s)
        import careers
        careers.tick(s)
        import crime_diplomacy
        crime_diplomacy.tick(s)
        import interpol
        interpol.tick(s)
        arrivals = {}
        if w['minute'] % 1440 == 0:
            day = dates.story_date(w['minute'])
            for title, _, who in dates.events(s, day):
                event(s, 'Today is ' + title + '.')
                if who and who != s['player']:
                    s['routes'][who]['history'].append({'role':'status', 'content':'Today is ' + title + '.'})
        for who, actor in w['cast'].items():
            if combat.recovering(s,who):
                actor.update(journey=None,activity='Recovering from knockout')
                continue
            fight=combat.active(s)
            if fight and who in (s['player'],fight['opponent']):
                actor.update(journey=None,activity='In a combat encounter')
                continue
            custody=s.get('interpol',{}).get('custody',{}).get(who)
            if custody:
                actor.update(location=custody['location'],journey=None,activity='In regional custody after the Interpol operation')
                continue
            task=s.get('interpol',{}).get('active')
            if task and who==task.get('partner') and actor['location']==w['location'] and not actor.get('journey'):
                actor['activity']='Interpol field team'
                continue
            if who == 'charles':
                actor.update(location=hidden.charles_han.LAB, journey=None, activity=hidden.CAST['charles']['activity'])
                continue
            if who == 'thirteen':
                actor.update(location=hidden.thirteen.HQ,journey=None,activity=hidden.CAST['thirteen']['activity'])
                continue
            if who == 'takeo':
                actor.update(location=hidden.takeo.HQ, journey=None, activity=hidden.CAST['takeo']['activity'])
                continue
            if who == 'crow':
                actor.update(location=hidden.HQ, journey=None, activity=hidden.CAST['crow']['activity'])
                continue
            if who == 'garrett' and s['player']!='garrett' and __import__('charles_disclosure').hold(s): continue
            invitation = scheduled_events.active(s, who)
            if invitation and who != s['player']:
                actor.update(location=invitation['venue'], journey=None, activity=invitation['title'])
                if who in w['party'] and w['location'] != invitation['venue']:
                    w['party'].remove(who)
                continue
            j=actor['journey']
            if j:
                if w['minute'] >= j['arrives']:
                    arrivals[who] = j
                    actor.update(location=j['destination'],journey=None,activity='Arrived')
                    if who==s['player']: w['location']=actor['location']
                    if who == j['driver']:
                        for recorded in reversed(w['journeys']):
                            if recorded['driver'] == who and recorded['departed'] == j['departed']:
                                recorded['status'] = 'arrived'
                                break
                    event(s,custom_protagonist.display_name(who)+' arrived at '+town.LOCATIONS[actor['location']]+'.')
                continue
            if who==s['player']: continue
            import autonomy
            if autonomy.control(s, who): continue
            if (who in w['party'] and together(s, who)) or town.dating.in_hangout(s, who):
                actor['activity'] = 'Hanging out'
                continue
            planned_date = town.dating.session(s, who)
            if actor.get('waiting_for_hangout') or (planned_date and not planned_date['started']):
                actor['activity'] = 'Waiting to meet ' + custom_protagonist.display_name(s["player"])
                continue
            hour,dest,activity=appointment(who,w['minute'])
            import faction_work
            dest=faction_work.next_stop(s,who,dest)
            if activity == 'Sleep' and not autonomy.sleep_window(s, who):
                actor['activity'] = 'Morning routine'
                continue
            # A shared hangout persists until the next scheduled appointment.
            boundary=w['minute']%1440 == hour*60
            if actor['location']!=dest and (boundary or s['routes'][who].get('channel')!='in_person'):
                start_trip(s,who,dest)
                actor['activity']=activity
            else: actor['activity']=activity
        if arrivals:
            town.arrival_scene(s, arrivals)
        town.town_residents.refresh(s)
        scheduled_events.observe(s)
        reconcile(s)
        for key,bond in s['bond_details'].items():
            a,b = key.split(':'); first,second=w['cast'][a],w['cast'][b]
            sharing = (first['location']==second['location'] and not first['journey']
                       and first['activity']!='Sleep' and second['activity']!='Sleep'
                       and not combat.recovering(s,a) and not combat.recovering(s,b))
            bond['shared_minutes'] = bond.get('shared_minutes',0)+1 if sharing else 0
            day=w['minute']//1440
            if bond['shared_minutes'] >= 15 and bond.get('last_shared_day') != day:
                bond['last_shared_day']=day
                if not bond['tension']:
                    bond['closeness']=min(100,bond['closeness']+1)
                    bond['trust']=min(100,bond['trust']+1)
                point = 'Crossed paths at '+town.LOCATIONS[first['location']]+('. Existing tension remains.' if bond['tension'] else '. Familiarity grew.')
                bond['events'].append(clock(s)+': '+point)
                bond['events']=bond['events'][-12:]
        import autonomy
        autonomy.tick(s)
        import mysterious_hearts, contact_profiles
        mysterious_hearts.tick(s)
        import meet_cute
        meet_cute.tick(s)
        if w['minute'] % 60 == 0: contact_profiles.tick(s)
        followups(s)
        import groups
        groups.reconcile(s)
        # Phone intentions and reactions observe the same clock boundaries whether
        # time advances in one long wait or many small steps. No AI runs here.
        phone_apps.sync(s)

def finish_drive(s):
    w=ensure(s); j=w['cast'][s['player']]['journey']
    if j: settle_journeys(s)


def settle_journeys(s):
    """Complete saved legacy journeys without charging time on load."""
    import town
    w=s['world']; arrivals={}
    for who, actor in w['cast'].items():
        trip=actor.get('journey')
        if not trip: continue
        arrivals[who]=trip
        actor.update(location=trip['destination'],journey=None,activity='Arrived')
        if who==s['player']: w['location']=actor['location']
    for trip in w.get('journeys',[]):
        if trip.get('status')=='in transit': trip.update(status='arrived',arrives=w['minute'])
    if arrivals:
        town.arrival_scene(s,arrivals)
        reconcile(s)

def bond_event(s, a, b, text, tension=0):
    ensure(s); key=next((k for k in s['bond_details'] if set(k.split(':'))=={a,b}), ':'.join(sorted((a,b))))
    s['bond_details'].setdefault(key, {'type':'New acquaintances', 'trust':35, 'closeness':0, 'tension':0, 'key_points':[], 'events':[]})
    bond=s['bond_details'][key]; bond['tension']=min(100,bond['tension']+tension)
    bond['trust']=max(0,bond['trust']-tension//2)
    bond['events'].append(clock(s)+': '+text); bond['events']=bond['events'][-12:]


def idle_messages(s):
    """Check elapsed game time only; real-world idling cannot trigger early texts."""
    followups(s)


def conversation_time(s, action, dialogue=''):
    """Dialogue and physical actions never charge time; the active-play clock does."""
    return
