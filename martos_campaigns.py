"""Martos route authority: additive saves, isolated memories and real escort receipts."""
import copy
import hashlib
import json
import uuid
VERSION=1
CHAPTER_IDS=tuple('MT-%02d'%n for n in range(1,15))
MEMORY_IDS=tuple('MT-F%02d'%n for n in range(1,9))
MEMORY_AT={n:'MT-F%02d'%n for n in range(1,9)}
OPERATIONS={0,4,12}
HISTORICAL_FIGHTS={'MT-F01','MT-F02','MT-F04','MT-F05'}
ROLES={'mavis':'extraction','camila':'authentication','elias':'cover'}
ACCOUNT='Lena Varo: Martos served the forced-removal cordon and knowingly guarded the second abusive transfer. The record is preserved unaltered.'
ACCOUNT_HASH=hashlib.sha256(ACCOUNT.encode()).hexdigest()

def read(s):return s.get('ace_campaigns',{}).get('martos',{})
def data(s):
    if s.get('player')!='martos':raise ValueError('This is Martos’s personal campaign.')
    d=s.setdefault('ace_campaigns',{'version':1}).setdefault('martos',{})
    defaults=dict(version=VERSION,chapter=0,phase='briefing',memories=[],completed=[],operations={},agreement=None,evidence={},support={},disclosures={},knowledge={},receipts=[],session=None,pending_return=None,ending=None,complete=False,aftermath_read=[],strain_reports=0)
    for k,v in defaults.items():d.setdefault(k,copy.deepcopy(v))
    return d

def chapter(s):return __import__('martos_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),13)]]
def destination(s):
    d=read(s);i=d.get('chapter',0);phase=d.get('phase','briefing')
    if d.get('scene_resume'):return d['scene_resume']['beats'][d['scene_resume']['cursor']]['room'].split('__')[0]
    if d.get('scene_room'):return d['scene_room'].split('__')[0]
    if phase=='memory':return 'martos_transfer_house'
    if phase in ('briefing','aftermath'):
        lines=chapter(s).get(phase,[])
        if lines and lines[0].get('room'):return lines[0]['room'].split('__')[0]
        speakers={who for b in lines for who,_ in b.get('speeches',[])}
        if speakers.intersection(('crow','mavis','camila','elias','sylvanis')):return 'syndicate_hq'
    return 'martos_transfer_house'
def room_target(s):
    if read(s).get('scene_resume'):return read(s)['scene_resume']['beats'][read(s)['scene_resume']['cursor']]['room']
    if read(s).get('scene_room'):return read(s)['scene_room']
    phase=read(s).get('phase','briefing')
    if phase in ('briefing','aftermath'):
        lines=chapter(s).get(phase,[])
        if lines and lines[0].get('room'):return lines[0]['room']
    venue=destination(s)
    if venue=='syndicate_hq':
        phase=read(s).get('phase','briefing')
        crow=any(who=='crow' for b in chapter(s).get(phase,[]) for who,_ in b.get('speeches',[]))
        return venue+('__executive_meeting_room' if crow else '__cross_branch_operations_room')
    phase=read(s).get('phase')
    if phase=='handover':
        op=read(s).get('operations',{}).get('MT-13',{})
        return venue+('__departure' if op.get('delivered') or op.get('extraction_progress',0)<3 else '__receiving')
    return venue+('__departure' if phase in ('operation','escort_hold') else '__sitting')
def required_cast(s,action=None,value=''):
    if action=='objective' and read(s).get('chapter')==12:return list(ROLES)
    if action in ('memory','historical_return','agree','reject','recon','approach','objective','deliver','custody','release','control'):return []
    if action in ('support','disclose'):return [value.split(':')[0]] if value.split(':')[0] in ('mavis','camila','elias','sylvanis') else []
    pending=read(s).get('scene_resume')
    if pending:
        room=pending['beats'][pending['cursor']]['room']
        return sorted({who for b in pending['beats'][pending['cursor']:] if b.get('room')==room for who,_ in b.get('speeches',[]) if who!='martos' and who in s['world']['cast']})
    phase=read(s).get('phase','briefing')
    if phase not in ('briefing','aftermath'):return []
    return sorted({who for b in chapter(s).get(phase,[]) for who,_ in b.get('speeches',[]) if who!='martos' and who in s.get('world',{}).get('cast',{}) and (not b.get('room') or b['room']==room_target(s))})
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if d['complete']:raise ValueError('Martos’s campaign is complete.')
    if d['session']:raise ValueError('Return from the historical encounter first.')
    if s.get('flashback_visit'):raise ValueError('Return from the optional memory first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Go to the chapter objective in Maps first.')
    interior_activities.require(s,room_target(s))
    custody=s.get('interpol',{}).get('custody',{})
    if custody.get('martos') or custody.get('crow'):raise ValueError('The saved custody outcome prevents this operation.')
    if s['world']['cast']['martos'].get('journey'):raise ValueError('Arrive before starting the objective.')
    phase=d.get('phase','briefing')
    pending=d.get('scene_resume')
    lines=pending['beats'][pending['cursor']:] if pending else chapter(s).get(phase,[])
    if not isinstance(lines,list):lines=[]
    if action=='disclose' and value.split(':')[0]=='sera':needs_sera=True
    elif action not in ('briefing','aftermath','resume'):needs_sera=False
    else:needs_sera=any(who=='martos-sera' for b in lines if b.get('room',room_target(s))==room_target(s) for who,_ in b.get('speeches',[]))
    if needs_sera and not _sera_here(s):raise ValueError('Arrange Sera’s voluntary visit and wait for actual arrival.')
    if action=='disclose':
        person=value.split(':')[0]
        others=set(interiors.occupants(s,interiors.room(s)))-{'martos',person}
        if person!='sera' and _sera_here(s):others.add('martos-sera')
        if others:raise ValueError('Choose a private room without unrelated listeners before disclosing personal history.')
    for who in required_cast(s,action,value):
        if custody.get(who) or combat.recovering(s,who) or not interiors.available(s,who) or not __import__('interpol').here(s,who):raise ValueError('A required participant is unavailable or has not arrived: '+who+'.')
        if not interiors.same_room(s,'martos',who):raise ValueError('Meet the participant in the objective room: '+who+'.')

def support_available(s,who,room=False):
    import combat,interiors
    actor=s.get('world',{}).get('cast',{}).get(who,{})
    return bool(read(s).get('support',{}).get(who,{}).get('accepted') and actor and not actor.get('journey') and not s.get('interpol',{}).get('custody',{}).get(who) and not combat.recovering(s,who) and interiors.available(s,who) and (interiors.same_room(s,'martos',who) if room else interiors.same_building(s['world']['location'],actor.get('location',''))))

def condition(s):
    import combat,combat_profiles
    baseline=combat.resources(combat_profiles.profile(s,'martos'))
    saved=read(s).get('condition')
    if not saved:return baseline
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for field,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):
        result[field]=min(baseline[maximum] if maximum else 100,result[field]+int(elapsed*rate))
    return result

def pay(s,stamina,minutes):
    resources=condition(s)
    if resources['stamina']<stamina:raise ValueError('Recover sufficient stamina before this action, or prioritise the protected delivery.')
    resources['stamina']-=stamina
    __import__('world_loop').advance(s,minutes)
    data(s)['condition']=dict(resources=resources,minute=s['world']['minute'])

def request_sera(s):
    d=data(s)
    if d['session'] or s.get('campaign_dialogue') or s.get('flashback_visit'):raise ValueError('Finish the active scene first.')
    import interiors
    venue=destination(s);target=room_target(s)
    for who in d.get('appointment',{}).get('guests',[]):
        if interiors.same_building(s['world']['cast'][who]['location'],venue) and interiors.enabled(s,venue):
            exit_room=('syndicate_hq__cross_branch_operations_room' if target=='syndicate_hq__members_lounge' else 'syndicate_hq__members_lounge') if venue=='syndicate_hq' else venue+'__departure' if target!=venue+'__departure' else venue+'__sitting'
            interiors.walk_actor(s,who,exit_room)
    d.pop('appointment',None)
    d['sera_visit']=dict(accepted=True,room=room_target(s),arrival=s['world']['minute']+10,end=s['world']['minute']+190,voluntary=True)
    return 'Sera accepts a voluntary private visit. Wait ten minutes for her arrival; she takes no combat or medical duty.'

def _sera_here(s):
    visit=read(s).get('sera_visit',{})
    return visit.get('accepted') and visit.get('room')==__import__('interiors').room(s) and visit.get('arrival',10**12)<=s['world']['minute']<visit.get('end',0)

def _after_memory(d):d['phase']='operation' if d['chapter'] in OPERATIONS else 'aftermath'
def perform_action(s,action,value=''):
    validate(s,action,value)
    d=data(s);i=d['chapter'];key=CHAPTER_IDS[i];op=d['operations'].get(key,{})
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This briefing has already been heard.')
        d['phase']='agreement' if i==0 and not d['agreement'] else 'memory' if i in MEMORY_AT else 'operation' if i in OPERATIONS else 'aftermath'
    elif action=='reject':
        if d['phase']!='agreement':raise ValueError('The agreement is not open.')
        d['rejected_terms']=True
    elif action=='agree':
        if d['phase']!='agreement' or value not in ('archive','revised'):raise ValueError('Choose a viable agreed arrangement.')
        d['agreement']=dict(recipient='independent witness archive liaison',route='covered departure',fallback='protected return to the transfer house',records_owner='Lena Varo',disclosures=['operational route','unaltered witness account'],personal_disclosure=False,accepted=True,revised=value=='revised')
        d['evidence']=dict(account=ACCOUNT,sha256=ACCOUNT_HASH,authenticated_source='Lena Varo · original signed account',holder='Lena Varo',recipient=d['agreement']['recipient'],receipt=None)
        d['phase']='operation'
    elif action=='memory':
        memory=MEMORY_AT.get(i)
        if d['phase']!='memory' or memory in d['memories']:raise ValueError('This mandatory memory is unavailable.')
        if memory in HISTORICAL_FIGHTS:start_session(s,memory,True)
        else:d['memories'].append(memory);_after_memory(d)
    elif action=='recon':
        if d['phase']!='operation' or op.get('recon'):raise ValueError('Reconnaissance is unavailable.')
        op['recon']=True;op['observed']='Northline pursuers cover the direct gate. The sheltered return requires a longer hold. This observation concerns present pursuit, not the historical testimony.'
    elif action=='approach':
        if d['phase']!='operation' or not op.get('recon') or op.get('approach') or value not in ('covered','direct'):raise ValueError('Observe the route and choose an uncommitted approach.')
        pay(s,8 if value=='covered' else 3,2 if value=='covered' else 1)
        op['approach']=value
        op['pressure_limit']=4 if value=='covered' else 3
        op['approach_cost']=dict(stamina=8 if value=='covered' else 3,minutes=2 if value=='covered' else 1)
    elif action=='control':
        if i not in (4,11,12) or value not in ('communicate','hold'):raise ValueError('Choose a supported control commitment.')
        d['control_commitment']=value
    elif action=='objective':
        if d['phase']!='operation' or not op.get('approach') or op.get('attack_stopped'):raise ValueError('Commit an observed approach first.')
        if i==12 and (set(d['support'])!=set(ROLES) or not d.get('preparation')):raise ValueError('Agree the extraction, authentication, cover and transfer conditions first.')
        start_session(s,key,False)
    elif action=='support':
        if i not in (2,9,11) or value not in ROLES:raise ValueError('Agree the named specialist roles during preparation.')
        d['support'][value]=dict(role=ROLES[value],accepted=True)
    elif action=='disclose':
        who,_,topic=value.partition(':')
        if i not in (5,9,13) or who not in ('mavis','camila','elias','sera') or topic not in ('account','private'):raise ValueError('Choose a supported private disclosure.')
        d['disclosures'][who]=topic
        if topic=='account':
            facts=d['knowledge'].setdefault(who,[])
            if 'Martos selected personal account' not in facts:facts.append('Martos selected personal account')
    elif action=='prepare':
        if i!=11 or d['phase']!='aftermath' or set(d['support'])!=set(ROLES):raise ValueError('Agree all specialist roles before confirming transfer conditions.')
        d['preparation']=dict(account_hash=hashlib.sha256(d['evidence']['account'].encode()).hexdigest(),authentication='Camila checks original account hash',custody_receiver='regional custody receiving team',custody_conditions=['Voss disarmed','active attack stopped','safe route verified'],fallback=d['agreement']['fallback'],records_unaltered=True)
    elif action=='secure_departure':
        if d['phase'] not in ('handover','escort_hold') or not op.get('attack_stopped') or op.get('extraction_progress',0)>=3:raise ValueError('No remaining protected departure leg.')
        pay(s,5,1)
        op['extraction_progress']=op.get('extraction_progress',0)+1
        op.setdefault('departure_minutes',[]).append(s['world']['minute'])
        if op['extraction_progress']>=3:d['phase']='handover' if i==12 else 'aftermath'
    elif action=='deliver':
        if i!=12 or not op.get('attack_stopped') or op.get('extraction_progress',0)<3:raise ValueError('Stop the attack and complete the protected extraction first.')
        if not support_available(s,'camila',True) or not support_available(s,'elias'):raise ValueError('The agreed authentication and cover colleagues must be present and available for delivery.')
        if d['evidence'].get('sha256')!=hashlib.sha256(d['evidence'].get('account','').encode()).hexdigest() or d['evidence']['sha256']!=ACCOUNT_HASH:raise ValueError('The original account must arrive unaltered.')
        if not d.get('support',{}).get('camila',{}).get('accepted') or d.get('preparation',{}).get('account_hash')!=ACCOUNT_HASH:raise ValueError('The agreed authentication conditions are incomplete.')
        if d['evidence'].get('receipt'):raise ValueError('The recipient has already received these records.')
        token=uuid.uuid4().hex
        d['evidence'].update(holder=d['agreement']['recipient'],receipt=dict(id=token,recipient=d['agreement']['recipient'],minute=s['world']['minute'],sha256=ACCOUNT_HASH,intact=True))
        op['lena_safe']=True;op['delivered']=True
        op['authentication_used']=d['support']['camila']['role'];op['cover_used']=d['support']['elias']['role']
    elif action=='disarm':
        if i!=12 or not op.get('attack_stopped') or op.get('disarmed'):raise ValueError('Defeat the actual commander before disarming him once.')
        pay(s,5,1);op['disarmed']=True;op['disarm_token']=op['encounter_token']
    elif action=='perimeter':
        if i!=12 or not op.get('disarmed') or op.get('receiver_eta'):raise ValueError('Disarm the commander before securing a custody route once.')
        if not support_available(s,'elias'):raise ValueError('The agreed cover colleague must be available to secure the perimeter.')
        pay(s,15,1)
        op['secured_route']=support_available(s,'elias')
        op['receiver_eta']=s['world']['minute']+5
        op['receiver_authorised']=True
    elif action in ('custody','prioritise_delivery'):
        if i!=12 or not op.get('delivered') or op.get('custody'):raise ValueError('Deliver Lena and her records before resolving the commander.')
        secured=bool(op.get('disarmed') and op.get('secured_route') and op.get('receiver_authorised') and s['world']['minute']>=op.get('receiver_eta',10**12) and support_available(s,'elias'))
        if action=='custody' and not secured:raise ValueError('Disarm Voss, secure the route with available cover and wait for the authorised receiving team.')
        if action=='prioritise_delivery':pay(s,0,1)
        captured=action=='custody' and secured
        op['custody']=dict(receiver='regional custody receiving team' if captured else None,conditions=dict(disarmed=bool(op.get('disarmed')),secured_route=bool(op.get('secured_route')),receiver_arrived=secured),minute=s['world']['minute'],result='received disarmed' if captured else 'escaped while protection took priority over the unguarded secondary perimeter',token=op['encounter_token'])
        d['ending']='promise_kept' if captured and not op.get('extraction_cost') else 'delivered_at_cost'
        d['phase']='aftermath'
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('There is no unread historical return.')
        d['pending_return']=None
    elif action=='aftermath':
        if d['phase']!='aftermath' or d['pending_return']:raise ValueError('Resolve the chapter objectives and historical return first.')
        if i==11 and not d.get('preparation'):raise ValueError('Confirm the transfer conditions first.')
        if i==12 and not (op.get('delivered') and op.get('custody')):raise ValueError('The handover remains incomplete.')
        if i==13 and (not d.get('ending') or len(d['memories'])!=8):raise ValueError('Resolve the protection objective and every mandatory memory first.')
        d['completed'].append(key);d['chapter']+=1;d['phase']='briefing';d['complete']=d['chapter']==14
        if i==13:d['aftermath_read']=['Lena','Sera','colleague','Crow']
    else:raise ValueError('Unknown Martos campaign action.')
    if op:d['operations'].setdefault(key,op)
    d.pop('scene_room',None)
    return 'Martos’s campaign record updated.'

def request_appointment(s,recipient=''):
    # Proven professional invitation logic with route-local state, no teleport.
    import scheduled_events,interior_bookings,hidden_cast,world_loop,interiors,combat
    d=data(s);guests=list(ROLES) if recipient=='team' else [recipient] if recipient in ROLES else required_cast(s)
    if not guests:raise ValueError('This objective needs no remote appointment.')
    if d['session'] or combat.active(s) or s.get('campaign_dialogue'):raise ValueError('Finish the current encounter first.')
    now=s['world']['minute'];venue=destination(s);target=room_target(s)
    for who in guests:
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A required participant is unavailable: '+who)
        current=scheduled_events.active(s,who)
        if current and not current.get('martos_appointment'):raise ValueError('A required participant has another commitment: '+who)
        if venue=='syndicate_hq' and not hidden_cast.hq_access(s,who):raise ValueError('Existing headquarters authorisation is required.')
    if interior_bookings.participant_conflict(s,guests,now,now+180):raise ValueError('A participant has a conflicting obligation.')
    projected=copy.deepcopy(s)
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
    old=d.get('appointment',{})
    for who in set(old.get('guests',[]))-set(guests):
        if interiors.same_building(s['world']['cast'][who]['location'],venue) and interiors.enabled(s,venue):
            exit_room=('syndicate_hq__cross_branch_operations_room' if target=='syndicate_hq__members_lounge' else 'syndicate_hq__members_lounge') if venue=='syndicate_hq' else venue+'__departure' if target!=venue+'__departure' else venue+'__sitting'
            interiors.walk_actor(s,who,exit_room)
    if recipient in ROLES and d.get('sera_visit'):d['sera_visit']['end']=now
    d['appointment']=dict(id='martos-'+uuid.uuid4().hex,title='Martos campaign appointment',venue=venue,room=target,guests=guests,start=now,end=now+180,martos_appointment=True)
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        elif interiors.enabled(s,venue):interiors.walk_actor(s,who,target)
    return 'Appointment requested. Wait for normal travel and authorised room arrival.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None

def encounter(s,mission,historical):
    import combat,combat_profiles,combat_engine
    p=combat_profiles.profile(s,'martos');q=combat_profiles.make('martos-route-operative',dict(awakened=False))
    q.update(name='Adrien Voss' if mission=='MT-13' else 'Northline interceptor' if not historical else 'Historical armed obstacle',combat_id='martos-route-operative',portrait='martos-historical-opposition' if historical else 'voss-current' if mission=='MT-13' else 'northline-interceptor',trait=None,awakened=False)
    q['stats'].update(awakened_power=0,trait_refinement=0,martial_skill=64 if mission=='MT-13' else 48,fight_iq=65 if mission=='MT-13' else 46);q['arts']={'Boxing':q['stats']['martial_skill']};q.pop('moveset',None)
    token=uuid.uuid4().hex
    f=dict(id=token,kind='martos_campaign',opponent=q['name'],opponent_profile=q,location=s['world']['location'],player=combat.resources(p),enemy=combat.resources(q),elapsed=0,turn=0,log=['Protect the leg while holding the attacker. Three completed exchanges advance extraction. Report strain and agree a handover before overextending.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,martos_mission=mission,martos_historical=historical)
    if mission=='MT-13':
        f['enemy']['health']=f['enemy']['max_health']=320
        q['basis']='Authored encounter durability: layered armour and fortified cover; no invented Trait or Awakening history.'
    f['martos_pressure_limit']=read(s).get('operations',{}).get(mission,{}).get('pressure_limit',4)
    f['martos_objective']=dict(extraction_progress=0,protected=True,strain_reported=False,handover=False,extraction_cost=False,exchanges=[])
    if historical:f['location_label']='School evacuation hall' if mission=='MT-F01' else 'Field extraction court'
    if historical:f['historical_portraits']={'martos':'martos-service-early' if mission=='MT-F01' else 'martos-special-forces',q['name']:'martos-historical-opposition'}
    else:
        f['contextual_portraits']={'martos':'martos-selection',q['name']:q['portrait']}
        if __import__('interiors').enabled(s):f['room']=__import__('interiors').room(s)
    if not historical and read(s).get('condition'):
        saved=read(s)['condition'];elapsed=max(0,s['world']['minute']-saved['minute'])
        for field,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):
            cap=f['player'][maximum] if maximum else 100
            f['player'][field]=min(cap,saved['resources'][field]+int(elapsed*rate))
        if f['player']['health']<=0:raise ValueError('Recover before retrying the protection objective.')
    combat_engine.ensure_arena(f);return f

def start_session(s,mission,historical):
    import game_core,combat,combat_profiles
    d=data(s)
    if d['session'] or combat.active(s):raise ValueError('An encounter is already active.')
    validate(s,action='memory' if historical else 'objective')
    if historical:
        if d['phase']!='memory' or MEMORY_AT.get(d['chapter'])!=mission:raise ValueError('This is not the current mandatory memory.')
        nested=game_core.fresh('martos');nested['routes']={};nested['world']['cast']={};nested['world']['npcs']=[];nested['world'].update(location='martos_transfer_house',minute=480)
        p=combat_profiles.make('martos-era-operative',dict(awakened=mission in ('MT-F04','MT-F05')));p.update(name='Martos · historical checkpoint',portrait='martos-service-early' if mission=='MT-F01' else 'martos-special-forces',trait=dict(name='Rage',description='Historical extraction pressure. Coordination risk persists.',effect='rage') if mission in ('MT-F04','MT-F05') else None,basis='Exact-era authored checkpoint. No present signature, Path, equipment or social knowledge.')
        p['stats'].update(awakened_power=55 if mission in ('MT-F04','MT-F05') else 0,trait_refinement=35,martial_skill=72,fight_iq=72);p['arts']={'Boxing':72};p.pop('moveset',None);__import__('combat_moves').initialise(p,'martos-era-operative')
        __import__('historical_combat').strengthen(p,'martos')
        age=__import__('martos_campaign_content').MEMORIES[mission]['age'];p['name']='Martos · age '+str(age)
        nested['ace_historical_context']=dict(age=age,title='Conventional service member' if mission=='MT-F01' else 'Special-forces operator · historical checkpoint')
        nested['combat']['profiles']['martos']=p;f=encounter(nested,mission,True);nested['combat']['active']=f
        d['session']=dict(token=f['id'],mission=mission,historical=True,checkpoint='reconnaissance',state=nested,receipt=None)
    else:
        if d['phase']!='operation' or CHAPTER_IDS[d['chapter']]!=mission:raise ValueError('This is not the current operation.')
        operation=d['operations'].get(mission,{})
        if not operation.get('recon') or not operation.get('approach'):raise ValueError('Complete the observed operation approach first.')
        if mission=='MT-13' and (set(d['support'])!=set(ROLES) or not d.get('preparation')):raise ValueError('Agree all final roles and transfer conditions first.')
        combat.guard(s);f=encounter(s,mission,False);s['combat']['active']=f;d['operations'][mission]['encounter_token']=f['id']

def session(s):return read(s).get('session')
def historical_approach(s,token,action):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if item['checkpoint']=='reconnaissance' and action=='observe':item['checkpoint']='approach'
    elif item['checkpoint']=='approach' and action in ('covered','direct'):
        f=__import__('combat').active(item['state'])
        if action=='covered':
            if f['player']['stamina']<15:raise ValueError('The covered historical route requires fifteen stamina.')
            f['player']['stamina']-=15
        else:f['player']['health']*=.9
        item['checkpoint']='confrontation';item['approach']=action
    else:raise ValueError('Observe and choose the historical approach first.')
    return 'Historical approach recorded. Present resources are unchanged.'

def combat_control(s,action):
    f=__import__('combat').active(s)
    if not f or not f.get('martos_mission') or f['status']!='active':raise ValueError('No active Martos encounter.')
    ledger=f['martos_objective']
    if action=='report':
        if ledger['strain_reported']:raise ValueError('Strain is already reported.')
        ledger['strain_reported']=True
        if not f.get('martos_historical'):data(s)['strain_reports']+=1
        f['log'].append('Martos reports his actual strain. No resources are restored.')
    elif action=='handover':
        if not ledger.get('strain_eligible'):raise ValueError('Handover requires recorded pressure from a paid Trait action, injury or sustained actual hold.')
        if not ledger['strain_reported']:raise ValueError('Communicate strain before handing over the protected leg.')
        if f.get('martos_historical'):allowed=True
        else:allowed=support_available(s,'mavis') and read(s).get('control_commitment')=='communicate'
        if not allowed:raise ValueError('An agreed, available extraction colleague is required.')
        if ledger['handover']:raise ValueError('The protected leg is already handed over.')
        ledger['handover']=True;f['log'].append('The agreed colleague takes the precision extraction leg while Martos holds the attacker.')
    else:raise ValueError('Unknown control action.')
    return 'Control commitment recorded.'

def on_exchange(s,f):
    if not f.get('martos_mission'):return
    ledger=f['martos_objective'];exchanges=f.get('exchanges',[])
    if not exchanges or exchanges[-1]['id'] in ledger['exchanges']:return
    ledger['exchanges'].append(exchanges[-1]['id'])
    records=exchanges[-1]['records']
    player=next((row for row in records if row.get('side')=='player'),records[0])
    profile=__import__('combat_profiles').profile(s,'martos')
    try:action=__import__('combat_moves').selection(profile,player['move_id'])
    except (ValueError,KeyError):action={}
    survived=f['player']['health']>0
    enemy=next((row for row in records if row.get('side')=='enemy'),{})
    meaningful_guard=action.get('role')=='defence' and player.get('outcome')=='guarded' and enemy.get('role') in ('attack','combo','break','throw','control') and abs(f['arena']['positions']['player']-f['arena']['positions']['enemy'])<=2
    hold=survived and (player.get('damage',0)>0 or meaningful_guard or (action.get('role')=='control' and player.get('hits',0)>0))
    ratio=f['player']['health']/max(1,f['player']['max_health'])
    ledger['strain_eligible']=ledger.get('strain_eligible',False) or bool(player.get('mana',0)>0 or ratio<.85 or len(ledger['exchanges'])>=2)
    if hold or (ledger['handover'] and survived):ledger['extraction_progress']=min(3,ledger['extraction_progress']+1)
    if ledger['strain_eligible'] and not ledger['handover'] and (len(ledger['exchanges'])>=f.get('martos_pressure_limit',4) or ratio<.5):
        ledger['extraction_cost']=True
        ledger['protected']=False
        f['log'].append('Overextension loses the secondary sheltered route. Lena falls back to the protected holding point; the original account stays intact.')

def _receipt(f):
    ledger=f.get('martos_objective',{});real=bool(f.get('exchanges')) and f.get('status')=='finished'
    won=real and f.get('result','').startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    return dict(token=f['id'],mission=f['martos_mission'],won=won,result=f.get('result'),turns=f['turn'],ledger=copy.deepcopy(ledger),consumed=True)
def after_combat_close(s,f):
    if not f.get('martos_mission') or f.get('martos_historical'):return
    d=data(s);mission=f['martos_mission'];op=d['operations'].get(mission,{})
    if any(r['token']==f['id'] for r in d['receipts']):return
    if CHAPTER_IDS[min(d['chapter'],13)]!=mission or op.get('encounter_token')!=f['id']:raise ValueError('This encounter token belongs to an expired operation.')
    receipt=_receipt(f);d['receipts'].append(receipt)
    d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    if receipt['won']:
        op.update(receipt['ledger']);op['attack_stopped']=True
        # A quick defeat still requires the independently protected departure leg.
        if op['extraction_progress']<3:op['needs_hold']=True
        d['phase']='escort_hold' if op['extraction_progress']<3 and mission!='MT-13' else 'handover' if mission=='MT-13' else 'aftermath'
    else:d['ending']='withdrawal_recovery';op['failed_attempts']=op.get('failed_attempts',0)+1

def finish_session(s,token):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This result belongs to a closed encounter or another save.')
    f=__import__('combat').active(item['state'])
    if item['checkpoint']!='confrontation' or not f or f['status']!='finished' or f['id']!=token:raise ValueError('Resolve or concede the actual encounter first.')
    item['receipt']=_receipt(f);return item['receipt']
def return_session(s,token):
    d=data(s);item=session(s);receipt=finish_session(s,token)
    if receipt['won'] and receipt['ledger']['extraction_progress']>=3:
        if item['mission'] not in d['memories']:d['memories'].append(item['mission'])
        d['pending_return']=item['mission'];d['receipts'].append(copy.deepcopy(receipt));_after_memory(d)
        if item['mission']=='MT-F04':d['fixed_history_injury']='Sera injured during Martos’s age-23 overmutation extraction; local success does not erase it.'
    d['session']=None
    return 'Returned to the present. '+('The bounded objective is recorded.' if d['pending_return'] else 'The memory remains incomplete; retry its checkpoint.')
def retry_session(s):
    d=data(s);item=session(s)
    if not item or not item.get('receipt') or (item['receipt']['won'] and item['receipt']['ledger']['extraction_progress']>=3):raise ValueError('Retry follows an unsuccessful historical encounter.')
    mission=item['mission'];d['session']=None;start_session(s,mission,True)
    return 'Historical checkpoint restarted; present resources are unchanged.'
def abandon_session(s,token):
    d=data(s)
    if not d['session'] or d['session']['token']!=token:raise ValueError('This return token has expired.')
    d['session']=None;return 'Returned safely. The memory remains incomplete.'

def action_pages(s,args):
    from campaign_prose import page
    import martos_campaign_content as content
    action=args[0];value=args[1] if len(args)>1 else '';d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),13)];spec=chapter(s)
    if action in ('briefing','aftermath'):
        lines=copy.deepcopy(spec[action])
        if action=='aftermath' and d.get('chapter')==13:
            final=d['operations'].get('MT-13',{})
            cost='The secondary sheltered route was lost under overextension; Lena used the protected fallback.' if final.get('extraction_cost') else 'The agreed extraction leg was preserved.'
            if final.get('custody',{}).get('result','').startswith('escaped'):cost+=' Voss escaped when protection took priority over the secondary perimeter.'
            lines=content.aftermath_scene(d['ending'],{'cost_description':cost})+lines
    elif action in ('reject','agree'):lines=content.agreement_scene('refused' if action=='reject' else 'revised' if value=='revised' else 'accepted')
    elif action=='support':
        lines=content.support_scene('accepted',value)
        room=__import__('interiors').room(s)
        for beat in lines:
            beat.update(room=room,background=__import__('interiors').ROOMS[room].art)
            if room.startswith('syndicate_hq__'):beat.setdefault('portraits',{})['martos']='martos-syndicate'
            for segment in beat.get('stage_segments',[]):segment.update(background=beat['background'],portraits=copy.deepcopy(beat.get('portraits',{})))
    elif action=='memory':lines=copy.deepcopy(content.MEMORIES[MEMORY_AT[d['chapter']]]['text'])
    elif action=='historical_return':lines=copy.deepcopy(content.MEMORIES[d['pending_return']]['after_encounter'])
    elif action=='disclose':
        lines=copy.deepcopy(content.DISCLOSURES[value.split(':')[0]]) if value.endswith(':account') else content.private_disclosure_scene(value.split(':')[0])
        room=__import__('interiors').room(s)
        for beat in lines:
            beat.update(room=room,background=__import__('interiors').ROOMS[room].art)
            if room.startswith('syndicate_hq__'):beat.setdefault('portraits',{})['martos']='martos-syndicate'
            for segment in beat.get('stage_segments',[]):segment.update(background=beat['background'],portraits=copy.deepcopy(beat.get('portraits',{})))
    elif action=='recon':lines=copy.deepcopy(spec.get('operation_intro',[]))+[page('Observe the present pursuers before committing an approach. Historical wrongdoing and present pursuit remain separate records.',title=spec['title'])]
    else:
        texts={'secure_departure':'Martos secures another departure leg. One real minute passes and five stamina are spent; the account remains intact.','reject':'Lena rejects these terms. She remains at the protected negotiation stop; a revised arrangement is still available.','agree':'Lena accepts an independent recipient, covered route and protected-return fallback. Her original account remains hers and will be carried unaltered.','approach':'Martos commits to the '+value+' route. Actual opposition and extraction remain unresolved.','objective':'The protected leg must continue while Martos holds the attacker. Three real combat exchanges advance departure. Report strain and hand over precision work to an agreed, available colleague; overextension has a recorded cost.','support':'The colleague accepts the defined '+ROLES.get(value,'support')+' responsibility. Attendance and availability remain necessary at execution.','control':'Martos records a control commitment; it neither heals him nor erases an injury.','prepare':'They confirm the original account, independent recipient, fallback, agreed roles and separate disarmed-custody conditions.','deliver':'The independent witness archive liaison receives Lena safely and her authenticated account intact. Receipt preserves evidence; it grants no conviction or forgiveness.','disarm':'Martos secures the defeated commander’s weapon. Five stamina and one real minute are spent; this alone is not a custody transfer.','perimeter':'The agreed cover colleague secures a route for the separately authorised receiving team. Fifteen stamina and one real minute are spent. Arrival takes five more minutes.','prioritise_delivery':'Martos commits the remaining attention to the protected delivery rather than guard the secondary perimeter. Voss escapes; that residual risk is recorded.','custody':'The regional custody receiving team accepts the defeated, disarmed Voss after the attack has stopped and the transfer route is secure.','release':'The secondary perimeter fails. Voss escapes. Lena and the original records are safe; the residual risk is recorded.'}
        lines=[page(texts[action],title=spec['title'])]
    if action=='aftermath' and d.get('chapter')==13:
        for beat in lines:
            if beat.get('room')=='syndicate_hq__members_lounge':
                beat['martos_closing_variants']={'mavis':content.closing_scene('mavis'),'alone':content.closing_scene(None)}
                break
    for n,b in enumerate(lines):b.setdefault('scene_id',key+'-'+action+'-%02d'%n)
    return lines


def pause_for_room(s,dialogue,next_cursor):
    beat=dialogue['beats'][next_cursor]
    if beat.get('mode')=='memory' or not beat.get('room'):return False
    import interiors
    if interiors.room(s)==beat['room']:return False
    snapshot=copy.deepcopy(dialogue);snapshot['cursor']=next_cursor
    snapshot.pop('presentation',None)
    data(s)['scene_resume']=snapshot
    data(s)['scene_room']=beat['room']
    s['campaign_dialogue']=None
    return True

def resume_scene(s):
    d=data(s);pending=d.get('scene_resume')
    if not pending:raise ValueError('No saved scene is waiting.')
    validate(s,action='resume')
    beat=pending['beats'][pending['cursor']]
    variants=beat.get('martos_closing_variants')
    if variants:
        import combat,interiors
        appointment=d.get('appointment',{})
        available=bool('mavis' in appointment.get('guests',[]) and appointment.get('room')==interiors.room(s) and appointment.get('start',0)<=s['world']['minute']<appointment.get('end',0) and interiors.same_room(s,'martos','mavis') and interiors.available(s,'mavis') and not combat.recovering(s,'mavis') and not s.get('interpol',{}).get('custody',{}).get('mavis'))
        if available and set(interiors.occupants(s,interiors.room(s)))-{'martos','mavis'}:raise ValueError('Wait for a private lounge audience without unrelated listeners, or continue the repair alone.')
        chosen=copy.deepcopy(variants['mavis' if available else 'alone'])
        __import__('campaign_dialogue').stamp_pages(s,chosen)
        pending['beats'][pending['cursor']:]=chosen
        d['closing_colleague']='mavis' if available else None
    pending['venue']=s['world']['location']
    s['campaign_dialogue']=pending
    d.pop('scene_resume',None)
    return 'Resumed the saved scene at the actual room.'


def dismiss_closing_colleague(s):
    import interiors
    d=data(s);pending=d.get('scene_resume')
    if not pending or not pending['beats'][pending['cursor']].get('martos_closing_variants'):raise ValueError('No quiet closing scene is waiting.')
    event=d.get('appointment',{})
    if 'mavis' in event.get('guests',[]):
        if interiors.same_building(s['world']['cast']['mavis']['location'],'syndicate_hq'):interiors.walk_actor(s,'mavis','syndicate_hq__cross_branch_operations_room')
        event['guests']=[who for who in event['guests'] if who!='mavis']
    return 'Continuing the watch repair alone.'
