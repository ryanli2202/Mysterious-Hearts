"""Casual meeting destinations and ordinary public-room intent.

These defaults are only for unspecified social visits. Campaign/work providers
must use their authored stage destination rather than borrowing a casual table.
"""
DEFAULTS={
 'rei_home':'living_space','emily_home':'living_room','sophie_home':'open_living_kitchen',
 'amy_home':'dorm_room','minsu_home':'dorm_room','nest_dorm_corridor':'public_dorm_corridor',
 'samantha_home':'living_kitchen','april_home':'sitting_chess_room','garrett_home':'living_room',
 'valentina_home':'harbour_living_room','neo_home':'living_room','tyler_home':'entry_living_room',
 'lena_home':'living_record_room','naomi_home':'living_room','celeste_home':'piano_sitting_room',
 'dev_home':'studio_room','rosa_home':'sitting_room','elliot_home':'living_workroom',
 'daniel_home':'living_drawing_room','fox_home':'living_kettle_room','gordon_home':'living_reading_room',
 'sylvanis_home':'bare_sitting_room','martos_home':'living_room','elias_home':'sitting_rehearsal_room',
 'mavis_home':'private_room','camila_home':'living_chess_room',
 'vacant_downtown_home':'open_living_kitchen','vacant_suburbs_home':'living_room',
 'vacant_beach_home':'living_room','vacant_university_home':'living_study_kitchenette',
 'cafe':'counter_seating_room','noodle_shop':'dining_room','marios_pizza':'dining_counter_room',
 'chess':'caf_room','flowers':'shop_floor','boutique':'display_counter_room',
 'shopping_mall':'food_seating_view','campus':'study_room','track':'outdoor_track',
 'studio':'reception','arena':'lounge','boxing_club':'reception_lounge','iron_circle':'spectator_lounge',
 'library':'reading_room','archive':'reading_records_room','makerspace':'shared_workshop',
 'cycle_shop':'customer_counter_room','planetarium':'lobby_exhibits','cinema':'ticket_foyer',
 'sailing_club':'reception','market':'public_stalls','bowling_alley':'lounge','arcade':'cabinet_floor',
 'nightclub':'lounge','bar':'bar_seating_room','public_park':'garden_paths','beach':'shoreline_beach_scene',
 'hill_tea_room':'tea_room','farm_shop':'produce_counter_hall','pottery_studio':'pottery_workshop',
 'marine_centre':'exhibit_hall','harbour_market':'public_seating','railway_museum':'collection_hall',
 'southbank_diner':'dining_counter_room','syndicate_office':'appointment_room',
 'syndicate_hq':'members_lounge','syndicate':'members_lounge','glasshouse_lab':'rest_room',
 'interpol_hq':'public_lobby_verification_desk','blackstone_hq':'reception_security',
 'lantern_house':'waiting_room','saints_depot':'waiting_room','purple_clubhouse':'waiting_room',
 'hamayashi_house':'reception_waiting_hall','rojos_courtyard':'waiting_room','consortium_house':'waiting_room',
 'hamayashi_annex':'meeting_office_room','hamayashi_store':'stock_hall','crew_lot_west':'workshop',
 'crew_lot_docks':'warehouse','crew_lot_north':'meeting_room','crew_lot_south':'garage',
 'mavis_dispatch_exchange':'receiving',
 'martos_transfer_house':'sitting',
 'elias_theatre':'stage',
}
for number in range(1,9):
    DEFAULTS['site_'+str(number).zfill(2)]='reception_public_displays' if number==7 else 'reception'

CAST_DESTINATIONS={
 ('emily','flowers'):'arrangement_workroom',('sophie','track'):'outdoor_track',
 ('amy','campus'):'seminar_room',('minsu','campus'):'lecture_room',('april','campus'):'study_room',
 ('samantha','arena'):'training_hall',('tyler','boxing_club'):'training_hall',
 ('neo','makerspace'):'electronics_room',('alyssa','archive'):'conservation_workshop',
 ('lena','archive'):'conservation_workshop',('naomi','cycle_shop'):'repair_room',
 ('celeste','planetarium'):'dome_theatre',('dev','makerspace'):'electronics_room',
 ('rosa','market'):'community_dining_room',('daniel','cinema'):'projection_room',
 ('elias','studio'):'review_room',
 ('garrett','noodle_shop'):'kitchen',
}


def casual(place):
    import interiors
    place=interiors.building(place)
    key=DEFAULTS.get(place)
    if not key:raise ValueError('This venue needs an authored social meeting room.')
    return place+'__'+key


def intent(s,who):
    import interiors
    actor=s['world']['cast'][who]
    place=interiors.building(actor['location'])
    legacy=__import__('interior_compat').ROOMS.get(actor['location'])
    if legacy:return legacy
    if place in __import__('interior_residential').HOUSEHOLDS or place.startswith('vacant_'):
        return None
    activity=actor.get('activity','').lower()
    if who=='yuriko' and place=='campus':
        # Theatre-design teaching uses its own workshop classroom. Minsu's
        # simultaneous medical lecture retains the distinct lecture room.
        key='rehearsal_room' if 'rehearsal' in activity else 'theatre_workshop'
    elif who=='rei' and place=='studio':key='photo_studio'
    elif who=='ivan' and place=='studio':key='choreography_room' if 'choreograph' in activity else 'recording_booth'
    elif place=='chess' and who=='april':key='playing_room'
    elif who=='emily' and place=='flowers':key='arrangement_workroom' if s['world']['minute']//40%2 else 'shop_floor'
    elif who=='garrett' and place=='noodle_shop':key='kitchen' if s['world']['minute']//40%2 else 'service_counter_view'
    elif place=='library' and any(word in activity for word in ('study','research','reading')):key='reading_room'
    elif (who,place) in CAST_DESTINATIONS:key=CAST_DESTINATIONS[who,place]
    else:return casual(place)
    return place+'__'+key
