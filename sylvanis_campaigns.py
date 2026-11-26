"""MH-014: isolated recollections and a resolver-backed arena shutdown."""
import copy
import uuid

VERSION=1
CHAPTER_IDS=tuple(f'SY{i:02}' for i in range(1,17))
MEMORY_IDS=tuple(f'SY-M{i:02}' for i in range(1,11))
MEMORY_AT={i:MEMORY_IDS[i] for i in range(10)}
ROOM='glasshouse_lab__private_review_reunion_room'
ARENA='sylvanis_arena__ring'
TASKS={1:'roster',3:'provocation',6:'reserve',8:'access',9:'promise',10:'programme',11:'independent',12:'cancel',13:'exhibition',14:'finale'}
ROUTINE_TASKS=frozenset(('roster','reserve','access','promise','programme','independent','cancel'))

def read(s):return s.get('sylvanis_campaign',{})
def data(s):
    if s.get('player')!='sylvanis':raise ValueError('This is Sylvanis’s personal campaign.')
    d=s.setdefault('sylvanis_campaign',{})
    for k,v in dict(version=VERSION,chapter=0,phase='briefing',completed=[],memories=[],choices={},receipts=[],session=None,pending_return=None,condition=None,complete=False,arena_revealed=False,arena_closed=False,reserve=80,operating_costs=[],settlement=None,ending=None).items():d.setdefault(k,copy.deepcopy(v))
    return d
def chapter(s):return __import__('sylvanis_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),15)]]
def session(s):return read(s).get('session')
def room_target(s):
    d=read(s)
    if d.get('scene_resume'):return d['scene_resume']['beats'][d['scene_resume']['cursor']]['room']
    if d.get('arena_closed') and d.get('chapter')==14:return 'syndicate_hq__executive_meeting_room'
    return d.get('scene_room') or chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]
def required_cast(s,action=None,value=''):
    if action=='memory':return []
    d=read(s)
    lines=d['scene_resume']['beats'][d['scene_resume']['cursor']:] if d.get('scene_resume') else __import__('sylvanis_campaign_content').ending_pages(d) if d.get('chapter')==15 else chapter(s).get(d.get('phase','briefing'),[])
    if d.get('phase')=='tasks':return {8:['charles'],9:['takeo'],11:['charles'],12:['crow'],14:['crow']}.get(d.get('chapter'),[])
    return sorted({who for beat in lines if beat.get('room',chapter(s)['room'])==room_target(s) for who,_ in beat.get('speeches',[]) if who in ('crow','charles','takeo')})
def availability(s):
    custody=s.get('interpol',{}).get('custody',{})
    if custody.get('crow'):return 'Unavailable: the Crow is in saved Interpol custody. This route has no authored custody adaptation; the case is preserved.'
    if custody.get('sylvanis'):return 'Unavailable while Sylvanis is in saved custody.'
    return None
def meeting_access(s,who):
    d=read(s);event=d.get('appointment',{});now=s.get('world',{}).get('minute',0)
    return bool(s.get('player')=='sylvanis' and who in ('sylvanis','takeo') and not availability(s) and d.get('chapter') in (9,15) and event.get('sylvanis_appointment') and event.get('venue')=='site_01' and event.get('room')=='site_01__briefing_room' and 'takeo' in event.get('guests',[]) and event.get('start',1)<=now<event.get('end',0))
def knowledge(s,who,listeners=()):
    if not s or s.get('player')!='sylvanis' or who not in ('sylvanis','crow','charles','takeo'):return ''
    d=read(s);parts=[]
    if who=='sylvanis':
        parts.append('Sylvanis and the Crow knowingly manipulate and exploit each other: the Crow uses his feared reputation and abilities despite his volatility; Sylvanis uses the Crow’s ambitions as excuses and infrastructure for violence. He chooses freely and remains responsible, chaotic evil without remorse, redemption or hidden loyalty. Supreme strength and intelligence leave him chronically unfulfilled; he seeks chaos, thrill and the possibility of an opponent who can surprise him. Red and Blue Magic are temporary experiments towards that possibility, not proof he has created an equal. His Blisk civilisation prized dark magic, social Darwinism, violence and selfishness; he despises its predictable ambitions as boring. Species is not moral destiny or knowledge of another Blisk’s life.')
        if 'SY-M08' in d.get('memories',[]):parts.append('PRIVATE INTERNAL HISTORY, not an automatic spoken disclosure: he killed Garrett and Charles’s parents by choice. Garrett has learned nothing from this route; keep his investigation independent.')
        if 'SY-M09' in d.get('memories',[]):parts.append('PRIVATE INTERNAL KNOWLEDGE: he knowingly admitted Charles’s infiltration for amusement. Charles believes his cover holds. Do not confess this or invent Charles learning it; True Sight is not mind-reading.')
    if d.get('complete') and d.get('settlement'):
        if who in ('crow','sylvanis'):parts.append('The private arena exhibition is permanently closed; its equipment is decommissioned and shared discretionary backing withdrawn. Ledger disposition: '+d['settlement']['ledger']+'. His rank and the public venues remain. No new exhibition is authorised.')
        elif who=='takeo':parts.append('The failed demonstration order is closed. Wider supply is '+d['settlement']['wider_supply']+'. You remain at headquarters. The territorial betrayal is unresolved and unknown to you.')
        elif who=='charles':parts.append('Your bounded trial-discrepancy copy remains in a separate Glasshouse hold. You remain alive in the laboratory with cover intact. This is not completed revenge, a murder disclosure to Garrett, or knowledge that Sylvanis recognises your infiltration. Do not discuss your private purpose with uninformed listeners.')
    return ' '.join(parts)
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if availability(s):raise ValueError(availability(s))
    if d['complete']:raise ValueError('This campaign is complete.')
    if d['session'] or s.get('flashback_visit'):raise ValueError('Return from the recollection first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Go to the chapter objective through Maps first.')
    if room_target(s) in interiors.ROOMS:interior_activities.require(s,room_target(s))
    if s['world']['cast']['sylvanis'].get('journey'):raise ValueError('Wait for actual arrival first.')
    for who in required_cast(s,action,value):
        actor=s['world']['cast'].get(who,{})
        same=interiors.same_room(s,'sylvanis',who) if room_target(s) in interiors.ROOMS else actor.get('location')==destination(s)
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who) or actor.get('journey') or not same:raise ValueError('A required participant has not arrived or is unavailable: '+who)
    # Historical return pages reveal no history aloud. Present private scenes
    # never smuggle a secret to uninformed physical listeners.
    if destination(s) in ('glasshouse_lab','syndicate_hq') and action!='memory':
        present=set(interiors.occupants(s,room_target(s))) if room_target(s) in interiors.ROOMS else set()
        # A silent collaborator is still a permitted listener. Memories and
        # return narration are internal, not disclosures to the room. Keep this
        # room-scoped; an appointment alone never grants access to other scenes.
        listeners={ROOM:{'charles'},'syndicate_hq__executive_meeting_room':{'crow'}}.get(room_target(s),set())
        # SY07 uses Charles's normal workroom. Its present-day venue/account
        # business is not a private historical disclosure to the resident.
        if d['chapter']==6 and room_target(s)=='glasshouse_lab__laboratory_workroom':
            listeners=listeners|{'charles'}
        if present-{'sylvanis',*required_cast(s,action,value),*listeners}:raise ValueError('Use a private room without unrelated listeners.')
def request_appointment(s,recipient=''):
    import scheduled_events,interior_bookings,world_loop,interiors,combat
    d=data(s);guests=[recipient] if recipient in ('crow','charles','takeo') else required_cast(s)
    if not guests:raise ValueError('No remote participant is needed here.')
    if availability(s):raise ValueError(availability(s))
    if d['session'] or combat.active(s) or s.get('campaign_dialogue') or s.get('flashback_visit'):raise ValueError('Finish the current scene first.')
    venue=destination(s);target=room_target(s);now=s['world']['minute']
    for who in guests:
        if who=='charles' and venue!='glasshouse_lab':raise ValueError('Charles stays at the Glasshouse.')
        if who=='takeo' and venue!='site_01':raise ValueError('Takeo receives this meeting at his headquarters.')
        if who=='crow' and venue not in ('syndicate_hq','sylvanis_arena'):raise ValueError('This chapter grants no Crow appearance at this venue.')
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A required participant is unavailable: '+who)
        current=scheduled_events.active(s,who)
        if current and not current.get('sylvanis_appointment'):raise ValueError('A participant has another commitment: '+who)
    if interior_bookings.participant_conflict(s,guests,now,now+240):raise ValueError('A participant has a conflicting obligation.')
    event=dict(id='sylvanis-'+uuid.uuid4().hex,title='Sylvanis authored campaign appointment',venue=venue,room=target,guests=guests,start=now,end=now+240,sylvanis_appointment=True)
    # Plan on a copy first; travel errors must not leave a partial appointment.
    projected=copy.deepcopy(s);data(projected)['appointment']=copy.deepcopy(event)
    def travel(state):
        for who in guests:
            if not interiors.same_building(state['world']['cast'][who]['location'],venue):world_loop.start_trip(state,who,venue)
            elif target in interiors.ROOMS:interiors.walk_actor(state,who,target)
    travel(projected);d['appointment']=event;travel(s)
    return 'Appointment requested. Travel and actual arrival remain necessary.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None
def condition(s):
    import combat,combat_profiles
    base=combat.resources(combat_profiles.profile(s,'sylvanis'));saved=read(s).get('condition')
    if not saved:return base
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for field,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):result[field]=min(base[maximum] if maximum else 100,result[field]+int(elapsed*rate))
    return result
def start_session(s,memory):
    validate(s,'memory');d=data(s)
    if d['phase']!='memory' or MEMORY_AT.get(d['chapter'])!=memory:raise ValueError('This is not the current mandatory memory.')
    spec=__import__('sylvanis_campaign_content').MEMORIES[memory]
    # Sandbox owns only local observations. It never copies live world state.
    d['session']=dict(token=uuid.uuid4().hex,mission=memory,era=spec['era'],cursor=0,events=[])
    return 'Entered an isolated fixed recollection.'
def memory_step(s,token,choice):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical token has expired.')
    tasks=__import__('sylvanis_campaign_content').MEMORY_TASKS[item['mission']]
    if item['cursor']>=len(tasks):raise ValueError('This interaction is already complete.')
    task=tasks[item['cursor']]
    if choice not in task['options']:raise ValueError('Choose an offered historical action.')
    text=task['options'][choice][1];item['events'].append(dict(choice=choice,text=text));item['cursor']+=1;return text
def return_session(s,token):
    d=data(s);item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical token has expired.')
    if item['cursor']!=len(__import__('sylvanis_campaign_content').MEMORY_TASKS[item['mission']]):raise ValueError('Complete the remembered interaction or return safely.')
    d['memories'].append(item['mission']);d['receipts'].append(dict(token=token,kind='history',mission=item['mission'],events=copy.deepcopy(item['events'])))
    d['pending_return']=item['mission'];d['session']=None;d['phase']='tasks' if d['chapter'] in TASKS else 'aftermath'
    return 'Returned to the untouched present.'
def abandon_session(s,token):
    d=data(s)
    if not session(s) or session(s)['token']!=token:raise ValueError('This historical token has expired.')
    d['session']=None;return 'Returned safely; mandatory history remains incomplete.'

def complete_read_history(s):
    """Finish an already-read history; also accepts legacy half-journalled saves."""
    item=session(s)
    if not item:raise ValueError('No completed reading is waiting.')
    token=item['token']
    while item['cursor']<len(__import__('sylvanis_campaign_content').MEMORY_TASKS[item['mission']]):
        memory_step(s,token,'observe' if item['cursor']==0 else 'remember')
    return return_session(s,token)

def finish_reading(s,action):
    """Reader-only continuation: no travel, choices, fights or unavailable cast skipped.

    perform_action stays compatible with old callers and saves. Routine effects
    occur only after their authored scene has been read, never on opening it.
    """
    d=data(s)
    if action=='memory' and session(s):complete_read_history(s)
    if not d.get('pending_return') and d.get('phase')=='tasks' and TASKS.get(d['chapter']) in ROUTINE_TASKS:
        perform_action(s,'task',TASKS[d['chapter']])
    if d.get('complete') or d.get('scene_resume') or session(s):return
    next_action=('historical_return' if d.get('pending_return') else
                 {'briefing':'briefing','memory':'memory','aftermath':'aftermath'}.get(d.get('phase')))
    if not next_action:return
    # A changed room, missing speaker, custody or an unrelated listener is a real
    # stop, not permission to move anyone or to disclose private material.
    try:validate(s,next_action)
    except ValueError:return
    __import__('campaign_dialogue').begin(s,'sylvanis_campaigns.perform_action',(next_action,''))
def perform_action(s,action,value=''):
    validate(s,action,value);d=data(s);i=d['chapter'];key=CHAPTER_IDS[i]
    if d.get('pending_return') and action!='historical_return':raise ValueError('Read the pending historical return first.')
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This briefing is already complete.')
        d['phase']='memory' if i in MEMORY_AT else 'tasks' if i in TASKS else 'aftermath'
    elif action=='memory':return start_session(s,MEMORY_AT.get(i))
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('No historical return is waiting.')
        d['pending_return']=None
    elif action=='task':
        if d['phase']!='tasks' or TASKS.get(i)!=value:raise ValueError('This chapter objective is unavailable or already complete.')
        if value=='provocation':raise ValueError('Choose the provocation explicitly.')
        if value=='reserve':
            if d['reserve']!=80:raise ValueError('The operating account is not ready.')
            d['reserve']-=20;d['operating_costs'].append(dict(id='venue',units=20));d['arena_revealed']=True
        elif value=='access':d['archive_window']=dict(granted=True,bounded=True,disclosure=False)
        elif value=='promise':d['delegation']=dict(authorised='controlled demonstration',extra_promise='unsanctioned exhibition',takeo_at_hq=True)
        elif value=='programme':
            if not d.get('delegation'):raise ValueError('Agree the actual delegation before changing the programme.')
            d['programmes']={'buyer':'controlled comparison','fighters':'unsanctioned exhibition','signed_by':'sylvanis'}
        elif value=='independent':
            if not d.get('archive_window'):raise ValueError('The bounded archive opportunity is required.')
            d['charles_event']=dict(id=uuid.uuid4().hex,evidence='sealed trial-discrepancy copy',storage='separate Glasshouse hold',reserve_case_withheld=True,garrett_disclosure=False,charles_knows_sylvanis_knows=False)
        elif value=='cancel':
            if not d.get('programmes') or not d.get('charles_event'):raise ValueError('The actual discrepancies must precede containment.')
            d['shutdown_order']=dict(declared=True,cancelled=True,shared_support_withdrawn=True,voluntary_breach=True)
        elif value in ('exhibition','finale'):
            if not d.get('shutdown_order'):raise ValueError('The declared cancellation must precede the event.')
            if value=='finale' and not d.get('exhibition_result'):raise ValueError('Resolve the actual exhibition first.')
            import combat_engine
            f=encounter(s,value);combat_engine.ensure_arena(f);d['encounter_token']=f['id'];s.setdefault('combat',__import__('combat').ensure(s))['active']=f
            return 'Actual campaign encounter started.'
        d.setdefault('objectives',{})[key]=value;d['phase']='aftermath'
    elif action=='provocation':
        if i!=3 or d['phase']!='tasks' or value not in ('buyer','supervisors','crow'):raise ValueError('Choose an available provocation.')
        d['choices']['provocation']=value;d['phase']='aftermath'
    elif action=='aftermath':
        if d['phase']!='aftermath':raise ValueError('Resolve the actual chapter objective first.')
        if i==15 and (set(d['memories'])!=set(MEMORY_IDS) or not d.get('settlement')):raise ValueError('All ten histories and actual shutdown settlement are required.')
        d['completed'].append(key);d['chapter']+=1;d['phase']='briefing';d['complete']=d['chapter']==16
    else:raise ValueError('Unknown Sylvanis campaign action.')
    d.pop('scene_room',None);return 'Sylvanis campaign record updated.'
def encounter(s,kind):
    import combat,combat_profiles
    if condition(s)['health']<=0:raise ValueError('Recover before entering combat.')
    if kind=='finale':q=combat_profiles.profile(s,'crow')
    else:
        q=combat_profiles.make('sylvanis-exhibition-fighter',dict(awakened=False));q.update(name='Contracted exhibition fighter',combat_id='sylvanis-exhibition-fighter',portrait='sylvanis-fighter',trait=None,awakened=False,basis='An experienced contracted fighter, not an invented Sylvanis equal.')
        q['stats'].update(awakened_power=0,trait_refinement=0,martial_skill=76,fight_iq=72);q['arts']={'Military CQC':76};q.pop('moveset',None)
    token=uuid.uuid4().hex
    return dict(id=token,kind='sylvanis_campaign',display_kind='SYLVANIS · THE CROW’S PATIENCE',opponent=q['name'],opponent_profile=q,location=s['world']['location'],location_label='Sylvanis’s private testing arena',room=ARENA,player=condition(s),enemy=combat.resources(q),elapsed=0,turn=0,log=['Shutdown is declared. Four exchanges before service-route withdrawal; two successful ledger interceptions retain the asset. Direct combat does not halt the separate shutdown.' if kind=='finale' else 'Resolve the actual exhibition fight. The shutdown continues separately.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,campaign_objective=True,sylvanis_mission=kind,ledger_progress=0,contextual_portraits={'sylvanis':'sylvanis-syndicate',q['name']:'crow-selection' if kind=='finale' else 'sylvanis-fighter'})
def attempt_ledger(s):
    import combat,combat_engine
    f=combat.active(s)
    if not f or f.get('sylvanis_mission')!='finale' or f['status']!='active':raise ValueError('The declared ledger interception is unavailable.')
    if f.get('ledger_progress',0)>=2:raise ValueError('The ledger has already been retained.')
    # This consumes a real defensive exchange, including the Crow's response.
    request=combat_engine.request(s,'utility:guard');f['ledger_attempt_turn']=f['turn'];return combat_engine.resolve(s,request)
def on_exchange(s,f):
    if f.get('sylvanis_mission')!='finale' or not f.get('exchanges'):return
    latest=f['exchanges'][-1]
    if f.get('ledger_checked')==latest['id']:return
    f['ledger_checked']=latest['id']
    if f.pop('ledger_attempt_turn',None)==f['turn']:
        records={row['side']:row for row in latest['records']}
        clear=(f['player']['health']>0 and not f['player'].get('restrained') and not f['player'].get('staggered') and abs(f['arena']['positions']['player']-f['arena']['positions']['enemy'])<=2 and records['enemy']['damage']<f['player']['max_health']*.15)
        if clear:f['ledger_progress']+=1
        latest['sylvanis_objective']=dict(attempt=True,secured=clear,progress=f['ledger_progress'],enemy_damage=records['enemy']['damage'])
        f['log'].append('Ledger interception '+('secured an opening' if clear else 'was contested successfully by the Crow')+f" ({f['ledger_progress']}/2).")
def finish_boundary(s,f):
    if f.get('sylvanis_mission')=='finale' and f['turn']>=4 and min(f['player']['health'],f['enemy']['health'])>0:
        __import__('combat').finish(s,'Objective window closed — the arena shuts down; '+('ledger retained.' if f['ledger_progress']>=2 else 'Crow’s team withdraws with ledger.'))
        return True
    return False
def after_combat_close(s,f):
    if not f.get('sylvanis_mission'):return
    d=data(s)
    if any(r['token']==f['id'] for r in d['receipts']):return
    if d.get('encounter_token')!=f['id']:raise ValueError('This encounter belongs to an expired objective.')
    conceded=f['status']=='finished' and f.get('result')=='Defeat — conceded. Opponent is the clear victor.' and f['enemy']['health']>0
    real=(bool(f.get('exchanges')) or conceded) and f['status']=='finished'
    if not real:raise ValueError('Actual resolved exchanges are required; a fabricated result cannot advance the campaign.')
    d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    receipt=dict(token=f['id'],kind='combat',mission=f['sylvanis_mission'],result=f['result'],exchanges=[r['id'] for r in f['exchanges']],ledger_progress=f.get('ledger_progress',0),player_health=f['player']['health'],enemy_health=f['enemy']['health'])
    d['receipts'].append(receipt)
    if f['sylvanis_mission']=='exhibition':
        won=f['player']['health']>0 and f['enemy']['health']<=0 and f['result'].startswith('Victory')
        d['exhibition_result']=dict(won=won,receipt=f['id']);d['phase']='aftermath'
    else:
        retained=f.get('ledger_progress',0)>=2 and f['player']['health']>0 and not conceded
        success=retained and d.get('exhibition_result',{}).get('won',False)
        d['settlement']=dict(receipt=f['id'],ledger='sylvanis' if retained else 'crow_team',stock='crow_team',equipment='decommissioned',arena='permanently closed',physical_result=f['result'],charles_copy='separate Glasshouse hold',shared_support=False,takeo_order='closed',wider_supply='limited revised terms' if success else 'paused')
        units=30 if success else 60;d['reserve']-=units;d['operating_costs'].append(dict(id='shutdown',units=units));d['arena_closed']=True;d['ending']='an_expensive_evening' if success else 'a_spoiled_performance';d['phase']='aftermath'
def action_pages(s,args):
    import sylvanis_campaign_content as content,sylvanis_campaign_visuals as visuals
    action=args[0];value=args[1] if len(args)>1 else '';d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),15)]
    if action in ('briefing','aftermath'):
        lines=content.ending_pages(d) if d.get('chapter')==15 and action=='aftermath' else content.copy_scene(key,action)
    elif action=='memory':lines=content.copy_scene(MEMORY_AT[d['chapter']],'text')
    elif action=='historical_return':
        lines=content.copy_scene(d['pending_return'],'after_encounter')
        for beat in lines:beat['room']=room_target(s);beat.pop('stage_segments',None);beat['background']=visuals.background(room_target(s))
        visuals.bind(lines,d['pending_return'],'after_encounter',visuals.background(room_target(s)),visuals.CURRENT,room=room_target(s))
    elif action=='provocation':lines=[content.p({'buyer':'He wants the buyer to abandon the careful commercial language.','supervisors':'He wants the supervisors to lose their rehearsed composure.','crow':'He wants the Crow to come in person.'}[value]),content.b('sylvanis','Yes. That would entertain me.')]
    elif action=='task':lines=[content.p(content.ACTION_TEXT[value])]
    else:raise ValueError('No authored page for this action.')
    if action=='briefing' and d.get('chapter')==12:
        response={'buyer':'The delegation has lodged a written objection to the substituted programme. Its observer will attend only to establish the breach.','supervisors':'The supervisors have countersigned their refusal to certify the altered programme. They have sent both copies to the Crow.','crow':'Sylvanis sent both programmes directly to the Crow under his own signature. The reply addresses him personally.'}[d.get('choices',{}).get('provocation','crow')]
        lines.insert(0,content.p(response))
    if action not in ('memory','historical_return'):visuals.bind(lines,key,action,visuals.background(room_target(s)),visuals.CURRENT,room=room_target(s))
    if d.get('chapter')==14 and d.get('arena_closed'):
        for beat in lines:beat['room']=room_target(s)
    return lines
def pause_for_room(s,dialogue,next_cursor):
    beat=dialogue['beats'][next_cursor]
    if beat.get('mode')=='memory' or not beat.get('room') or (beat['room']==__import__('interiors').room(s) if beat['room'] in __import__('interiors').ROOMS else beat['room']==s['world']['location']):return False
    pending=copy.deepcopy(dialogue);pending['cursor']=next_cursor;pending.pop('presentation',None);data(s)['scene_resume']=pending;data(s)['scene_room']=beat['room'];s['campaign_dialogue']=None;return True
def resume_scene(s):
    d=data(s);pending=d.get('scene_resume')
    if not pending:raise ValueError('No saved scene is waiting.')
    validate(s,'resume');pending['venue']=s['world']['location'];s['campaign_dialogue']=pending;d.pop('scene_resume',None);return 'Resumed the exact saved reading position.'
