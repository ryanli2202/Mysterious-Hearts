"""Room-scoped faction access and stable guard-post assignments.

Perimeter victories permit passage only; they never confer command, research
clearance, private disclosures or membership. Original encounter IDs survive.
"""
POSTS = {
    'syndicate_hq': ('security_foyer', 'security_foyer', 'internal_corridor', 'internal_corridor',
                     'internal_corridor', 'internal_corridor'),
    'glasshouse_lab': ('cleared_entrance', 'cleared_entrance', 'internal_corridor', 'internal_corridor',
                      'internal_corridor', 'internal_corridor'),
}
ADDITIONS = {
    'syndicate_hq': (('executive-door', 'internal_corridor', 'clubs'),
                     ('executive-door', 'internal_corridor', 'spades'),
                     ('operations-door', 'internal_corridor', 'clubs'),
                     ('operations-door', 'internal_corridor', 'affiliate')),
    'glasshouse_lab': (('records-door', 'internal_corridor', 'clubs'),
                       ('records-door', 'internal_corridor', 'spades'),
                       ('workroom', 'laboratory_workroom', 'affiliate')),
}
# Original deployment order is untouched. Additional posts defend named rooms;
# campaign-required sets remain frozen separately from replenishing patrols.
for _number in range(1,9):
    _site='site_'+str(_number).zfill(2)
    _reception='reception_public_displays' if _number==7 else 'reception'
    _corridor='controlled_corridor' if _number==7 else 'secure_corridor'
    POSTS[_site]=('frontage','frontage',_reception,_reception,_corridor,_corridor)+((_corridor,)*3 if _number<=3 else ())
    _targets={1:('operations_office','guarded_service_room'),2:('dispatch_room','warehouse'),
              3:('research_office','restricted_laboratory'),4:('equipment_room','maintenance_bay'),
              5:('production_room','editing_room'),6:('accounts_office','restricted_records_room'),
              7:('data_wing','security_room'),8:('equipment_workshop','restricted_store')}[_number]
    _types=('yokai','tengu') if _number<=3 else ('clubs','affiliate')
    ADDITIONS[_site]=tuple((target+'-door',target,kind) for target in _targets for kind in _types)
for _venue,_key in (('blackstone_hq','reception_security'),('blackstone_loading','loading_compound'),
                    ('blackstone_records','research_records'),('blackstone_lab','experimental_wing'),('blackstone_command','executive_command')):
    POSTS[_venue]=(_key,)*3
    ADDITIONS[_venue]=((_key+'-support',_key,'pmc'),)
for _venue,_key in (('interpol_hq','public_lobby_verification_desk'),('interpol_briefing','awakened_operations_briefing_room'),
                    ('interpol_training','controlled_training_hall'),('interpol_containment','interview_containment_wing')):
    POSTS[_venue]=(_key,)*2
    ADDITIONS[_venue]=((_key+'-support','secure_corridor','interpol'),)
for _venue in ('lantern_house','saints_depot','purple_clubhouse','rojos_courtyard','consortium_house','syndicate'):
    POSTS[_venue]=('entrance',)*2
    _waiting='members_lounge' if _venue=='syndicate' else 'waiting_room'
    ADDITIONS[_venue]=(('meeting-door',_waiting,'lookout'),('meeting-door',_waiting,'crew_enforcer'))
for _venue in ('hamayashi_house','hamayashi_annex','hamayashi_store'):
    POSTS[_venue]=('entrance',)*2
    _post='reception_waiting_hall' if _venue=='hamayashi_house' else 'meeting_office_room' if _venue=='hamayashi_annex' else 'stock_hall'
    ADDITIONS[_venue]=(('inner-post',_post,'kai_guard'),)
for _venue in ('crew_lot_west','crew_lot_docks','crew_lot_north','crew_lot_south'):
    POSTS[_venue]=('reception' if _venue=='crew_lot_north' else 'entry',)
    ADDITIONS[_venue]=()


def post_room(venue,key):
    import interiors
    return interiors.building(venue)+'__'+key


def active(s, venue):
    import interiors
    return venue in POSTS and interiors.enabled(s, venue)


def decorate(s, venue, rows):
    """Save the authored expansion once, keeping original campaign requirements."""
    if not active(s, venue):
        return rows
    data = s.setdefault('organisation_guards', {})
    manifests = data.setdefault('interior_posts', {})
    if venue not in manifests:
        old_ids = [row['id'] for row in rows]
        day = s['world']['minute'] // 1440
        wins = data.get('victories', {}).get('patrol:' + str(day), [])
        manifests[venue] = dict(version=1, original_ids=old_ids,original_rows=[dict(row) for row in rows],
            legacy_clear_day=day if old_ids and all(ident in wins for ident in old_ids) else None,
            additions=[dict(id=venue + ':interior:' + post + ':' + str(index),
                room=post_room(venue,room), post=post, type=kind, faction=rows[0]['faction'] if rows else 'syndicate', venue=venue,
                duty_start=0, duty_end=1440)
                for index, (post, room, kind) in enumerate(ADDITIONS[venue])])
    result = []
    for row in rows:
        row = dict(row)
        try:
            index = int(row['id'].removeprefix(venue + ':'))
        except ValueError:
            index = -1
        if 0 <= index < len(POSTS[venue]):
            row.update(room=post_room(venue,POSTS[venue][index]),
                       post='perimeter-' + str(index), duty_start=0, duty_end=1440)
        else:
            row.setdefault('room', post_room(venue,POSTS[venue][0]))
        result.append(row)
    return result + [dict(row) for row in manifests[venue]['additions']]


def mission_rows(s, venue, rows, scope):
    if not active(s, venue) or scope == 'patrol':
        return rows
    # Existing authored missions retain their original opponents. New research
    # security is real, but is not silently added to the brothers' critical path.
    original = s['organisation_guards']['interior_posts'][venue]['original_ids']
    required = s['organisation_guards'].setdefault('interior_required', {}).setdefault(scope + ':' + venue, list(original))
    return [row for row in rows if row['id'] in required]


def legacy_passage(s, venue):
    manifest = s.get('organisation_guards', {}).get('interior_posts', {}).get(venue, {})
    return manifest.get('legacy_clear_day') == s['world']['minute'] // 1440


def permitted(s, who, destination):
    import interiors, organisation_guards as guards
    target = interiors.ROOMS[destination]
    venue, key = target.building, destination.split('__', 1)[1]
    if venue=='ivan_network':
        event=__import__('ivan_campaigns').read(s).get('appointment') or {};now=s['world']['minute']
        return s.get('player')=='ivan' and not __import__('ivan_campaigns').availability(s) and (who=='ivan' or who in event.get('guests',[]) and event.get('start',1)<=now<event.get('end',0))
    if venue=='sylvanis_arena':
        d=__import__('sylvanis_campaigns').read(s)
        if who==s.get('player')=='sylvanis' and interiors.same_building(s['world']['location'],venue) and key=='entry':return True
        return s.get('player')=='sylvanis' and d.get('arena_revealed',False) and not d.get('arena_closed') and not __import__('sylvanis_campaigns').availability(s) and (who=='sylvanis' or who=='crow' and __import__('the_crow').campaign_venue(s,venue))
    if venue=='takeo_meridian':return who==s.get('player')=='takeo' and not __import__('takeo_campaigns').availability(s)
    if s.get('player')=='takeo' and who=='takeo' and venue in ('site_01','site_02'):return True
    if venue=='camila_meridian':
        return s.get('player')=='camila' and (who=='camila' or who in __import__('camila_campaigns').ROLES or who=='crow' and __import__('the_crow').campaign_venue(s,venue)) and not s.get('interpol',{}).get('custody',{}).get(who)
    if venue=='elias_theatre':
        return s.get('player')=='elias' and (who=='elias' or who in __import__('elias_campaigns').ROLES) and not s.get('interpol',{}).get('custody',{}).get(who)
    if venue=='martos_transfer_house':
        return s.get('player')=='martos' and (who=='martos' or who in __import__('martos_campaigns').ROLES) and not s.get('interpol',{}).get('custody',{}).get(who)
    if venue=='mavis_dispatch_exchange':return __import__('ace_campaigns').exchange_access(s,who,destination)
    if destination == interiors.ARRIVALS[venue] or key == 'restroom':
        return True
    if venue=='syndicate_office':
        if __import__('hidden_cast').hq_access(s,who):return True
        operation=s.get('interpol',{}).get('active') or {}
        if operation.get('key') in ('crow_trail','protect','syndicate_supply') and who in (s['player'],operation.get('partner')):return True
        if who==s['player']:
            if who=='garrett' and __import__('charles_quest').read(s)['step']==16:return True
            if (s.get('post_story',{}).get('active') or {}).get('key')=='dragon_freight':return True
            if (s.get('interpol',{}).get('active') or {}).get('key') in ('crow_trail','protect','syndicate_supply'):return True
        return False
    if venue in ('syndicate','lantern_house','saints_depot','purple_clubhouse','hamayashi_house','rojos_courtyard','consortium_house','hamayashi_annex','hamayashi_store'):
        if key in ('waiting_room','reception_waiting_hall','visitor_restroom'):return True
        import gang_members,gang_leaders
        if who in gang_members.MEMBERS and gang_members.MEMBERS[who]['base']==venue:return True
        if who in gang_leaders.BY_NAME and gang_leaders.BY_NAME[who]['base']==venue:return True
        if who==s['player']:
            faction=guards.DEPLOYMENTS.get(venue,(None,))[0]
            if faction and guards.member(s,faction):return True
            if venue=='hamayashi_house' and who=='rei' and s.get('rei_story',{}).get('stage')==5 and key=='meeting_room':return True
            pending=s.get('job_apps',{}).get('pending') or {}
            if pending.get('room')==destination and s['world']['minute']<pending['deadline']:return True
        for meeting in __import__('crime_diplomacy').commitments(s):
            if (meeting.get('room')==destination and meeting['start']-15<=s['world']['minute']<meeting['end']
                    and who in (s['player'],meeting.get('attendee'))):return True
        return False
    if venue.startswith('site_'):
        if key in ('reception','reception_public_displays'):
            if who==s['player']=='garrett' and __import__('charles_quest').read(s)['step']==6 and venue=='site_08':
                return not any(row.get('room')==venue+'__frontage' for row in guards.remaining(s,venue,'charles:search'))
            return True
        if who==s['player']=='garrett' and __import__('charles_quest').read(s)['step']==6 and venue=='site_08' and key=='secure_corridor':
            return not any(row.get('room') in (venue+'__frontage',venue+'__reception') for row in guards.remaining(s,venue,'charles:search'))
        import crime_operations
        return crime_operations.permitted(s,who,venue)
    if venue=='interpol_hq':
        return __import__('interpol').clearance(s,who)
    if venue=='blackstone_hq':
        if key=='controlled_corridor':
            return who==s['player']=='rei' and s.get('rei_story',{}).get('stage',0)>=6 and not s['world'].get('party')
        legacy=__import__('interior_compat').LOCATIONS.get(destination)
        if not legacy:
            return False
        try:
            guards.check_trip(s,who,legacy,tuple(s['world'].get('party',[])) if who==s['player'] else ())
        except ValueError:
            return False
        return who==s['player']=='rei'
    if venue == 'syndicate_hq':
        if not __import__('hidden_cast').hq_access(s, who):
            return who == s['player'] and key in ('internal_corridor', 'members_lounge') and guards.breach(s, venue)
        if key == 'council_chamber':
            return who in __import__('syndicate_council').ROSTER or (who == s['player'] and __import__('syndicate_council').eligible(s))
        return True
    import criminal_dynamics as crime
    if crime.research_access(who, s):
        return True
    if not __import__('charles_quest').guest(s, who):
        return False
    if key in ('laboratory_workroom', 'records_room'):
        return False
    if who == s['player'] == 'garrett' and __import__('charles_quest').read(s).get('step') == 9:
        remaining = guards.remaining(s, venue, 'charles:search')
        if key == 'internal_corridor':
            return not any(row.get('room') == interiors.ARRIVALS[venue] for row in remaining)
        if key == 'private_review_reunion_room' and remaining:
            return False
    return key != 'private_review_reunion_room' or 19 <= s['world']['minute'] % 1440 / 60 < 23


def intent(s, who):
    actor = s['world']['cast'][who]
    venue = actor['location']
    if venue == 'syndicate_hq':
        council = __import__('syndicate_council').npc_event(s, who, s['world']['minute'])
        if council:
            return venue + '__council_chamber'
        key = 'executive_meeting_room' if who == 'crow' or who in ('martos','elias','camila','mavis') and 'appointment' in actor.get('activity','').lower() else 'cross_branch_operations_room' if who in ('ivan','sylvanis') else 'members_lounge'
    elif venue == 'glasshouse_lab':
        family = __import__('charles_quest').guest(s, 'garrett') and 19 <= s['world']['minute'] % 1440 / 60 < 23
        family = family and s['world']['cast'].get('garrett', {}).get('location') == venue
        review='laboratory review' in actor.get('activity','').lower()
        key = 'private_review_reunion_room' if review or family and who in ('garrett', 'charles') else 'laboratory_workroom' if who in ('charles', 'sylvanis') else 'rest_room'
    else:
        return None
    return venue + '__' + key


def private_review(s, required=(), observer=None):
    import interiors
    target = 'glasshouse_lab__private_review_reunion_room'
    observer = observer or s['player']
    if interiors.room(s, observer) != target:
        return False
    present = interiors.occupants(s, target)
    return all(who in present and interiors.available(s, who) for who in required) and not any(
        who not in (observer, *required) for who in present) and not __import__('interior_presence').count(s, target)


def migrate(s, buildings):
    import interiors, organisation_guards as guards
    for venue in POSTS:
        if interiors.building(venue) in buildings:
            guards.slots(s, venue)
    group=s.get('groups',{}).get(s.get('active_group'),{})
    saved=group.get('guard_row') or {}
    if group.get('open') and group.get('guard_session') and interiors.building(saved.get('venue')) in buildings:
        row=next((row for row in guards.slots(s,saved['venue']) if row['id']==saved.get('id')),None)
        if not row:raise ValueError('The saved guard conversation needs an authored post repair.')
        __import__('interior_compat').assign(s,s['player'],row['room'])
        name=next((name for name,actual in guards.npc_rows(s).items() if actual['id']==row['id']),None)
        if not name:raise ValueError('The saved guard is unavailable; its conversation is preserved.')
        old=group.get('local');group.update(local=name,guard_row=dict(row),guard_session=__import__('guard_dialogue').session_key(s,row))
        group['members']=[name if person==old else person for person in group.get('members',[])]
    encounter = s.get('organisation_guards', {}).get('encounter')
    if not encounter or interiors.building(encounter['venue']) not in buildings or encounter['venue'] not in POSTS:
        return
    venue = encounter['venue']
    target = encounter.get('room')
    if not target:
        if encounter.get('slot'):
            row = next((row for row in guards.slots(s, venue) if row['id'] == encounter['slot']['id']), None)
            if not row:
                raise ValueError('The saved guard post needs an authored repair before continuing.')
            target = row['room']
            encounter['slot'] = dict(row)
        elif encounter.get('who') == 'charles':
            target = 'glasshouse_lab__private_review_reunion_room'
        else:
            target = interiors.ARRIVALS[interiors.building(venue)]
    if target not in interiors.ROOMS or interiors.ROOMS[target].building != interiors.building(venue):
        raise ValueError('The saved encounter has an invalid room; restore a compatible checkpoint.')
    encounter['room'] = target
    __import__('interior_compat').assign(s,s['player'],target)
    # Restore only real saved combat participants. Never recruit bystanders.
    if encounter.get('who') in s['world']['cast']:
        s['world']['cast'][encounter['who']]['room'] = target
    fight = s.get('combat', {}).get('active') or {}
    ally = fight.get('ally')
    if ally in s['world']['cast']:
        s['world']['cast'][ally]['room'] = target
