"""Authored household rooms and independent dwell choices after building intent."""
PREFERENCES={
 'emily':('lego_workroom','living_room','kitchen','flower_balcony'),
 'sophie':('stretching_zone_view','open_living_kitchen','sleeping_loft'),
 'amy':('dorm_room',), 'minsu':('dorm_room',),
 'samantha':('garage_workbench','living_kitchen','bedroom'),
 'april':('study_lab_desk','sitting_chess_room','telescope_terrace'),
 'garrett':('noodle_kitchen','dining_room','living_room','garage','terrace'),
 'ivan':('kitchen_dining','piano_alcove_view','harbour_living_room','reading_mezzanine'),
 'valentina':('sail_workroom','kitchen_dining','reading_mezzanine'),
 'neo':('living_room','kitchen_dining','living_room','shared_bedroom'),
 'alyssa':('kitchen_dining','herb_balcony','living_room','shared_bedroom'),
 'tyler':('kitchen_dining','entry_living_room','accessible_porch'),
 'lena':('kitchen','photo_workroom','living_record_room'),
 'naomi':('kitchen','living_room','balcony'),
 'celeste':('kitchen_dining','piano_sitting_room'),
 'dev':('studio_room',), 'rosa':('kitchen','communal_dining_room','sitting_room','shared_courtyard'),
 'elliot':('kitchenette','living_workroom','covered_porch'),
 'daniel':('kitchen','living_drawing_room'),
 'fox':('equipment_workshop','living_kettle_room','private_evidence_room'),
 'gordon':('entrance_uniform_locker','kitchen','living_reading_room'),
 'sylvanis':('private_notes_room','bare_sitting_room'),
 'martos':('kitchen','watch_workroom','living_room'),
 'elias':('kitchen','script_study','sitting_rehearsal_room'),
 'mavis':('private_room',), 'camila':('kitchen','private_study','living_chess_room'),
}
SLEEP={who:'bedroom' for who in PREFERENCES}
SLEEP.update(sophie='sleeping_loft',amy='dorm_room',minsu='dorm_room',ivan='ivan_bedroom',
             valentina='valentina_bedroom',neo='shared_bedroom',alyssa='shared_bedroom',
             tyler='tyler_bedroom',dev='studio_room',mavis='private_room')
HOUSEHOLDS={'rei_home':('rei','yuriko'),'valentina_home':('ivan','valentina'),'neo_home':('neo','alyssa')}
for who in PREFERENCES:
    if who not in ('ivan','valentina','neo','alyssa'):
        HOUSEHOLDS[who+'_home']=(who,)


def owners(place,key):
    people=HOUSEHOLDS.get(place,())
    if not people:return ()
    if key=='father_bedroom':return ('Tyler’s father',)
    if key.endswith('_bedroom') and key not in ('shared_bedroom',):
        return tuple(who for who in people if key==who+'_bedroom')
    return people


def owners_for(s,target):
    import world_loop
    if target.building.startswith('vacant_') and world_loop.HOUSES.get(s['player'],('',))[0]==target.building:
        return (s['player'],)
    if target.private and not target.owners:
        import gang_leaders
        return tuple(person['name'] for person in gang_leaders.LEADERS.values() if person['base']==target.building)
    return target.owners


def sleep_rooms(s):
    import world_loop
    who=s['player'];place=world_loop.HOUSES.get(who,('',))[0]
    key='rei_bedroom' if who=='rei' else 'yuriko_bedroom' if who=='yuriko' else SLEEP.get(who,'bedroom_1' if place=='vacant_suburbs_home' else 'bedroom')
    return (place+'__'+key,)


def private(key):
    return ('bedroom' in key or key in ('private_evidence_room','private_notes_room','private_study','sleeping_loft'))


def intent(s,who):
    import interiors,world_loop,weather
    actor=s['world']['cast'][who]
    place=interiors.building(actor['location'])
    if place!=world_loop.HOUSES.get(who,('',))[0] or who not in PREFERENCES:
        return None
    if actor.get('activity')=='Sleep':
        key=SLEEP[who]
    else:
        choices=PREFERENCES[who]
        # Stable phase per person, independent housemates and meaningful dwell.
        phase=sum(map(ord,who))%len(choices)
        key=choices[(s['world']['minute']//40+phase)%len(choices)]
        if who=='april' and s['world']['minute']%1440>=22*60:
            key='telescope_terrace'
        if who=='sylvanis' and s['world']['minute']%1440>=23*60:
            key='private_notes_room'
        target=interiors.ROOMS.get(place+'__'+key)
        if target and target.outdoor and (weather.shelter(s['world']['minute']) or (who!='april' and weather.at(s['world']['minute'])['light']=='night')):
            key=choices[0]
    target=place+'__'+key
    return target if target in interiors.ROOMS else None


HOME_ACTIONS={
 'Record a harmony at the piano':('valentina_home__piano_alcove_view',),
 'Practise martial arts footwork':('valentina_home__harbour_living_room',),
 'Make seaweed soup for Valentina':('valentina_home__kitchen_dining',),
 'Work on a song you own outright':('valentina_home__piano_alcove_view','valentina_home__reading_mezzanine'),
 'Review medical lecture notes':('minsu_home__dorm_room',),
 'Stretch after taekwondo training':('minsu_home__dorm_room',),
 'Prepare a study snack':('minsu_home__dorm_room',),
 'Unwind with music':('minsu_home__dorm_room',),
 'Paint at the easel':('rei_home__art_space',),
 'Write in your journal':('rei_home__library','rei_home__rei_bedroom'),
 'Cook a comforting meal':('rei_home__kitchen_and_dining',),
 'Read and reflect in the library':('rei_home__library',),
 'Experiment with a noodle recipe':('garrett_home__noodle_kitchen',),
 # Existing abstract cleared-floor practice remains within the living room;
 # the layout does not invent a dedicated gym room.
 'Train in the home gym':('garrett_home__living_room',),
 'Relax on the terrace':('garrett_home__terrace',),
 'Review personal business':('garrett_home__living_room',),
}
KITCHENS={
 'rei_home':'kitchen_and_dining','emily_home':'kitchen','sophie_home':'open_living_kitchen',
 'samantha_home':'living_kitchen','april_home':'kitchen','garrett_home':'noodle_kitchen',
 'valentina_home':'kitchen_dining','neo_home':'kitchen_dining','tyler_home':'kitchen_dining',
 'lena_home':'kitchen','naomi_home':'kitchen','celeste_home':'kitchen_dining','dev_home':'studio_room',
 'rosa_home':'kitchen','elliot_home':'kitchenette','daniel_home':'kitchen','fox_home':'living_kettle_room',
 'gordon_home':'kitchen','sylvanis_home':'kitchen','martos_home':'kitchen','elias_home':'kitchen',
 'camila_home':'kitchen','vacant_downtown_home':'open_living_kitchen','vacant_suburbs_home':'kitchen',
 'vacant_beach_home':'kitchen','vacant_university_home':'living_study_kitchenette',
}
NAMED_HOME_ACTIONS={
 'Build a miniature set':'rei_home__art_space','Sketch a costume concept':'rei_home__art_space','Read a play':'rei_home__library',
 'Tend the balcony flowers':'emily_home__flower_balcony','Build a LEGO arrangement':'emily_home__lego_workroom','Sew a small plushie':'emily_home__living_room',
 'Stretch and review split times':'sophie_home__stretching_zone_view',"Prepare tomorrow's training meals":'sophie_home__open_living_kitchen','Plan a recovery evening':'sophie_home__open_living_kitchen',
 'Paint a small canvas':'amy_home__dorm_room','Read philosophy notes':'amy_home__dorm_room','Sketch in your dorm':'amy_home__dorm_room',
 'Maintain your motorcycle':'samantha_home__garage_workbench','Practise controlled footwork':'samantha_home__heavy_bag_zone_view','Check your training equipment':'samantha_home__garage_workbench',
 'Analyse a chess position':'april_home__sitting_chess_room','Read a scientific paper':'april_home__study_lab_desk','Observe the night sky':'april_home__telescope_terrace',
 'Sort your film photographs':'lena_home__photo_workroom','Read local history':'lena_home__living_record_room','Practise salsa steps':'lena_home__living_record_room',
 'Shape a ceramic mug':'naomi_home__kitchen','Plan a climbing practice':'naomi_home__living_room','Read a mystery novel':'naomi_home__living_room',
 'Practise jazz piano':'celeste_home__piano_sitting_room','Bake a loaf of bread':'celeste_home__kitchen_dining','Update your birdwatching notebook':'celeste_home__piano_sitting_room',
 'Repair a small electronic device':'dev_home__studio_room','Arrange a tabletop game':'dev_home__studio_room','Sort night photographs':'dev_home__studio_room',
 'Test a shared recipe':'rosa_home__kitchen','Tend courtyard plants':'rosa_home__shared_courtyard','Maintain your roller skates':'rosa_home__sitting_room',
 'Carve a small wooden bird':'elliot_home__living_workroom','Review field recordings':'elliot_home__living_workroom','Inspect kayaking equipment':'elliot_home__covered_porch',
 'Repair the loaner gloves':'tyler_home__entry_living_room','Set out a domino game':'tyler_home__entry_living_room','Listen to a baseball broadcast':'tyler_home__accessible_porch',
 'Mend a sail':'valentina_home__sail_workroom','Review the tide notebook':'valentina_home__reading_mezzanine','Practise a karaoke verse':'valentina_home__harbour_living_room',
 'Draw a lobby card':'daniel_home__living_drawing_room','Review a film programme':'daniel_home__living_drawing_room','Practise judo footwork':'daniel_home__living_drawing_room',
 'Repair an old controller':'neo_home__living_room','Cook ginger pork rice bowls':'neo_home__kitchen_dining','Set up a co-op game':'neo_home__living_room',
 'Bind a small notebook':'neo_home__living_room','Sketch a balcony herb':'neo_home__herb_balcony','Prepare jasmine tea':'neo_home__kitchen_dining',
 'Review private research notes':'sylvanis_home__private_notes_room',"Examine an opponent's recorded technique":'sylvanis_home__private_notes_room','Reconsider a patronage proposal':'sylvanis_home__bare_sitting_room',
 'Restore a watch':'martos_home__watch_workroom','Complete controlled strength training':'martos_home__living_room','Cook a rice dish':'martos_home__kitchen',
 'Rehearse a performance':'elias_home__sitting_rehearsal_room','Review your recordings':'elias_home__script_study','Plan a quiet evening':'elias_home__sitting_rehearsal_room',
 'Repair a small object':'mavis_home__private_room','Sort ambient recordings':'mavis_home__private_room','Listen to the rain':'mavis_home__private_room',
 'Solve a chess problem':'camila_home__living_chess_room','Read an architecture study':'camila_home__private_study','Review a personal budget':'camila_home__private_study',
 'Maintain your field equipment':'fox_home__equipment_workshop','Review your private notebook':'fox_home__private_evidence_room','Practise controlled close combat':'fox_home__equipment_workshop',
 'Read a book off duty':'gordon_home__living_reading_room','Maintain your uniform and equipment':'gordon_home__entrance_uniform_locker','Prepare a quiet dinner':'gordon_home__kitchen',
}
HOME_ACTIONS.update({action:(room,) for action,room in NAMED_HOME_ACTIONS.items()})


def kitchen_rooms(s):
    import interiors
    place=interiors.building(s['world']['location'])
    key=KITCHENS.get(place)
    return (place+'__'+key,) if key else ()


def require_action(s,action):
    import interiors
    place=interiors.building(s['world']['location'])
    targets=HOME_ACTIONS.get(action.replace('\u2019',"'"))
    if place.startswith('vacant_'):
        living=__import__('interior_public').casual(place)
        targets={'Unpack a moving box':(interiors.ARRIVALS[place],living),
                 'Prepare a simple meal':kitchen_rooms(s),'Write in your journal':(living,),
                 'Relax and settle in':(living,)}.get(action)
    if targets and interiors.room(s) not in targets:
        raise ValueError('Go to '+' or '.join(interiors.ROOMS[target].label for target in targets)+' first.')
