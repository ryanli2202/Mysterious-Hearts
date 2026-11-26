"""Authored physical-stage destinations; unknown indoor work fails validation."""
CHARLES={
 0:'noodle_shop__dining_room',1:'noodle_shop__dining_room',2:'archive__reading_records_room',
 3:'interpol_hq__public_lobby_verification_desk',4:'noodle_shop__dining_room',5:'archive__reading_records_room',
 6:'site_08__frontage',7:'archive__reading_records_room',8:'noodle_shop__dining_room',
 9:'glasshouse_lab__private_review_reunion_room',10:'glasshouse_lab__private_review_reunion_room',
 11:'garrett_home__dining_room',12:'noodle_shop__dining_room',13:'archive__reading_records_room',
 14:None,15:'syndicate__council_meeting_room',16:'syndicate_office__guarded_access_passage',
 17:'glasshouse_lab__private_review_reunion_room',18:'syndicate__council_meeting_room',19:'noodle_shop__dining_room',
}
REI={0:'rei_home__art_space',1:'archive__reading_records_room',2:'rei_home__art_space',
     3:'blackstone_hq__reception_security',4:'archive__reading_records_room',5:'hamayashi_house__meeting_room'}
CAREERS={
 'restaurant':('noodle_shop__kitchen','noodle_shop__service_counter_view'),
 'modelling':('studio__photo_studio','studio__dressing_fitting_room'),
 'music':('studio__recording_booth','studio__choreography_room'),
 'study':('campus__lecture_room','campus__study_room'),
 'iron':('iron_circle__ring_hall',),'dragons':('syndicate__council_meeting_room',),
 'joker':('syndicate_hq__cross_branch_operations_room',),'taekwondo':('arena__training_hall',),
 'cast_emily':('flowers__shop_floor','flowers__arrangement_workroom'),
 'cast_sophie':('track__outdoor_track',), 'cast_amy':('campus__seminar_room',),
 'cast_samantha':('arena__training_hall',),'cast_april':('chess__playing_room','chess__lesson_alcove_view'),
 'cast_yuriko':('campus__theatre_workshop','campus__rehearsal_room'),
 'cast_valentina':('sailing_club__rigging_workshop',),'cast_neo':('makerspace__shared_workshop','makerspace__electronics_room'),
 'cast_alyssa':('archive__conservation_workshop',),'cast_tyler':('boxing_club__training_hall',),
 'cast_daniel':('cinema__auditorium','cinema__projection_room'),
 'cast_lena':('archive__conservation_workshop',),'cast_naomi':('cycle_shop__repair_room',),
 'cast_celeste':('planetarium__dome_theatre','planetarium__preparation_room'),
 'cast_dev':('makerspace__shared_workshop','makerspace__electronics_room'),
 'cast_rosa':('market__community_dining_room','market__staff_kitchen_store'),
 'cast_elliot':(),
 'cast_sylvanis':('syndicate_hq__cross_branch_operations_room',),'cast_martos':(),
 'cast_elias':('studio__review_room','studio__photo_studio'), 'cast_mavis':(),'cast_camila':(),
 'cast_fox':(),'cast_gordon':('interpol_hq__case_office',),
}
POST_STORY={
 'dragon_market':None,'dragon_freight':'syndicate_office__guarded_access_passage',
 'dragon_witness':'market__public_stalls','blackstone_transfer':None,
 'blackstone_records':'archive__forecourt','kai_remnants':'market__public_stalls',
 'kai_watch':None,'kai_charter':'market__public_stalls',
}
VISITS={
 'cafe':'cafe__counter_seating_room','marios_pizza':'marios_pizza__dining_counter_room',
 'cinema':'cinema__ticket_foyer','flowers':'flowers__shop_floor','sailing_club':'sailing_club__rigging_workshop',
 'bowling_alley':'bowling_alley__lane_hall','arcade':'arcade__cabinet_floor',
 'nightclub':'nightclub__dance_hall','bar':'bar__bar_seating_room','public_park':'public_park__garden_paths',
 'beach':'beach__shoreline_beach_scene','library':'library__reading_room','shopping_mall':'shopping_mall__concourse',
 'hill_tea_room':'hill_tea_room__tea_room','farm_shop':'farm_shop__produce_counter_hall',
 'pottery_studio':'pottery_studio__entrance_display_room','marine_centre':'marine_centre__exhibit_hall',
 'harbour_market':'harbour_market__stall_aisles','railway_museum':'railway_museum__collection_hall',
 'southbank_diner':'southbank_diner__dining_counter_room',
}
PROJECTS={
 'garrett':('noodle_shop__kitchen','noodle_shop__service_counter_view'),
 'rei':('studio__photo_studio',),'emily':('flowers__shop_floor','flowers__arrangement_workroom'),
 'sophie':('track__outdoor_track',),'minsu':('campus__study_room','campus__lecture_room'),
 'amy':(), 'yuriko':('campus__theatre_workshop',),'april':('chess__playing_room',),
 'samantha':('arena__training_hall',),
}
CLUBS={'Sketch club':'makerspace__shared_workshop','Reading circle':'library__reading_room','Running club':'track__outdoor_track'}
COLLECTIONS={'makerspace':'makerspace__welcome_room','library':'library__lobby_desk',
             'flowers':'flowers__shop_floor','planetarium':'planetarium__lobby_exhibits'}
TRAINING={
 'arena':('arena__training_hall',),'boxing_club':('boxing_club__training_hall',),
 'iron_circle':('iron_circle__ring_hall','iron_circle__fighter_preparation_room'),
 'track':('track__outdoor_track',),'samantha_home':('samantha_home__heavy_bag_zone_view',),
 'garrett_home':('garrett_home__living_room',),'valentina_home':('valentina_home__harbour_living_room',),
 'daniel_home':('daniel_home__living_drawing_room',),'martos_home':('martos_home__living_room',),
 'fox_home':('fox_home__equipment_workshop',),
}


def require(s,targets):
    import interiors
    if not interiors.enabled(s):return
    if isinstance(targets,str):targets=(targets,)
    if not targets:raise ValueError('This indoor activity needs an authored room mapping before it can begin.')
    if any(target not in interiors.ROOMS for target in targets):
        raise ValueError('The authored activity room is unavailable; the saved activity is preserved.')
    if interiors.room(s) not in targets:
        raise ValueError('Go to '+' or '.join(interiors.ROOMS[target].label for target in targets)+' first.')


def campaign(s,source,index):
    table=CHARLES if source=='charles' else REI
    if index not in table:raise ValueError('This campaign stage has no reviewed destination.')
    target=table[index]
    if target is not None:require(s,target)


def career(s,key,phase='work'):
    require(s,career_targets(key,phase))


def career_targets(key,phase='work'):
    targets=CAREERS.get(key)
    if phase=='finale':
        targets={'modelling':('studio__review_room',),'music':('studio__review_room',),
                 'restaurant':('noodle_shop__staff_office_store',)}.get(key,targets)
    return targets


def interpol_room(step):
    venue=step['venue']
    legacy=__import__('interior_compat').ROOMS.get(venue)
    if legacy:return legacy
    if venue.startswith('site_'):return venue+'__frontage'
    if venue=='archive':return 'archive__reading_records_room'
    if venue=='interpol_hq':return 'interpol_hq__public_lobby_verification_desk'
    if venue=='syndicate_office':return 'syndicate_office__guarded_access_passage'
    if venue=='syndicate_hq':return 'syndicate_hq__security_foyer' if step['kind']=='inspect' else 'syndicate_hq__executive_meeting_room'
    if venue=='market':return 'market__public_stalls'
    return None  # Source-authored outdoor district objective.


def project_here(s,who):
    import interiors
    if not interiors.enabled(s,s['world']['cast'][who]['location']):return True
    return interiors.room(s,who) in PROJECTS.get(who,())


def training(s,discipline):
    import interiors
    if not interiors.enabled(s):return
    place=interiors.building(s['world']['location'])
    targets=TRAINING.get(place)
    if discipline=='Combat analysis':
        if place==__import__('world_loop').HOUSES[s['player']][0]:targets=(__import__('interior_public').casual(place),)
        elif place in ('library','campus'):targets=(place+'__reading_room',) if place=='library' else ('campus__study_room',)
    require(s,targets)
