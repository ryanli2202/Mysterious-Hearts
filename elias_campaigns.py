"""Elias authority: additive saves, isolated history and independently secured objectives."""
import copy
import hashlib
import uuid
VERSION=1
CHAPTER_IDS=tuple('EL-%02d'%i for i in range(1,15))
MEMORY_IDS=tuple('EL-F%02d'%i for i in range(1,9))
MEMORY_AT={i:'EL-F%02d'%i for i in range(1,9)}
ROLES={'mavis':'civilian cover','martos':'perimeter and handover','camila':'records authentication'}
LOCAL=('elias-johanna','elias-konrad','elias-lotte')
FORMATIONS={'EL-F03':('entry/security assault','loading approach'),'EL-F04':('courtyard reserve','final breaching team')}
LEDGER='Braun reserve ledger: Konrad Braun pledged reserve funds and the service-route security team to an independent breakaway compact without administrator Johanna Braun’s authority.'
LEDGER_HASH=hashlib.sha256(LEDGER.encode()).hexdigest()

def read(s):return s.get('ace_campaigns',{}).get('elias',{})
def data(s):
    if s.get('player')!='elias':raise ValueError('This is Elias’s personal campaign.')
    d=s.setdefault('ace_campaigns',{'version':1}).setdefault('elias',{})
    defaults=dict(version=VERSION,chapter=0,phase='briefing',completed=[],memories=[],choices={},evidence={},support={},disclosures={},knowledge={},operations={},receipts=[],session=None,pending_return=None,historical_affiliate=None,present_affiliate=None,condition=None,ending=None,aftermath_read=[],complete=False,local_visits={})
    for key,value in defaults.items():d.setdefault(key,copy.deepcopy(value))
    return d
def chapter(s):return __import__('elias_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),13)]]
def room_target(s):
    d=read(s)
    if d.get('scene_resume'):return d['scene_resume']['beats'][d['scene_resume']['cursor']]['room']
    if d.get('scene_room'):return d['scene_room']
    if d.get('phase')=='handover':return 'elias_theatre__loading'
    if d.get('phase')=='tasks' and d.get('chapter') in (0,11):return 'elias_theatre__receiving'
    if d.get('phase')=='tasks' and d.get('chapter')==12:return 'elias_theatre__loading'
    if d.get('phase','briefing') in ('briefing','aftermath'):
        lines=chapter(s).get(d.get('phase','briefing'),[])
        if lines and lines[0].get('room'):return lines[0]['room']
    return chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]
def session(s):return read(s).get('session')
def required_cast(s,action=None,value=''):
    if action in ('support','disclose'):return [value.split(':')[0]] if value.split(':')[0] in ROLES else []
    if action in ('separate','seal','perimeter','custody'):return [{'separate':'mavis','seal':'camila','perimeter':'martos','custody':'martos'}[action]]
    if action not in (None,'briefing','aftermath','resume'):return []
    d=read(s);pending=d.get('scene_resume');lines=pending['beats'][pending['cursor']:] if pending else chapter(s).get(d.get('phase','briefing'),[])
    return sorted({who for beat in lines if beat.get('room',room_target(s))==room_target(s) for who,_ in beat.get('speeches',[]) if who!='elias' and (who in LOCAL or who in s.get('world',{}).get('cast',{}))})
def local_here(s,who):
    visit=read(s).get('local_visits',{}).get(who,{})
    return bool(visit.get('accepted') and visit.get('room')==__import__('interiors').room(s) and visit.get('arrival',10**12)<=s['world']['minute']<visit.get('end',0))
def support_available(s,who):
    import combat,interiors
    actor=s.get('world',{}).get('cast',{}).get(who,{})
    return bool(read(s).get('support',{}).get(who,{}).get('accepted') and actor and not actor.get('journey') and not combat.recovering(s,who) and not s.get('interpol',{}).get('custody',{}).get(who) and interiors.available(s,who) and interiors.same_room(s,'elias',who))
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if d['complete']:raise ValueError('Elias’s campaign is complete.')
    if d['session']:raise ValueError('Return from the historical encounter first.')
    if s.get('flashback_visit'):raise ValueError('Return from the optional memory first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Go to the chapter objective through Maps first.')
    interior_activities.require(s,room_target(s))
    custody=s.get('interpol',{}).get('custody',{})
    if custody.get('elias') or custody.get('crow'):raise ValueError('The saved custody outcome prevents this operation.')
    if s['world']['cast']['elias'].get('journey'):raise ValueError('Arrive before starting the objective.')
    for who in required_cast(s,action,value):
        if who in LOCAL:
            if not local_here(s,who):raise ValueError('Arrange the voluntary appointment and wait for actual arrival: '+who)
        elif custody.get(who) or combat.recovering(s,who) or not interiors.available(s,who) or not interiors.same_room(s,'elias',who) or s['world']['cast'][who].get('journey'):raise ValueError('A required participant is unavailable or has not arrived: '+who)
    if action=='disclose':
        person=value.split(':')[0]
        others=set(interiors.occupants(s,interiors.room(s)))-{'elias',person}
        others.update(who for who in LOCAL if local_here(s,who))
        if others:raise ValueError('A private disclosure needs a room without unrelated listeners.')

def request_local(s,who):
    d=data(s)
    if who not in LOCAL:raise ValueError('Choose a named production or affiliate participant.')
    if d['session'] or s.get('campaign_dialogue') or s.get('flashback_visit'):raise ValueError('Finish the current scene first.')
    room=room_target(s)
    if who=='elias-lotte' and room not in ('elias_theatre__stage','elias_theatre__dressing'):raise ValueError('Lotte’s appointment concerns the production, in the theatre only.')
    if who!='elias-lotte' and room=='elias_theatre__stage':raise ValueError('Affiliate business needs a private receiving appointment.')
    d['local_visits'][who]=dict(accepted=True,room=room,arrival=s['world']['minute']+10,end=s['world']['minute']+190,voluntary=True)
    return 'The participant accepts the bounded appointment. Wait ten minutes for actual arrival.'

def request_appointment(s,recipient=''):
    import scheduled_events,interior_bookings,hidden_cast,world_loop,interiors,combat
    d=data(s);guests=list(ROLES) if recipient=='team' else [recipient] if recipient in (*ROLES,'crow','sylvanis') else [who for who in required_cast(s) if who not in LOCAL]
    if not guests:raise ValueError('No remote colleague is needed here.')
    if d['session'] or combat.active(s) or s.get('campaign_dialogue'):raise ValueError('Finish the current scene first.')
    now=s['world']['minute'];venue=destination(s);target=room_target(s)
    for who in guests:
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A required participant is unavailable: '+who)
        current=scheduled_events.active(s,who)
        if current and not current.get('elias_appointment'):raise ValueError('A participant has another commitment: '+who)
        if venue=='syndicate_hq' and not hidden_cast.hq_access(s,who):raise ValueError('Existing headquarters authorisation is required.')
    if interior_bookings.participant_conflict(s,guests,now,now+180):raise ValueError('A participant has a conflicting obligation.')
    projected=copy.deepcopy(s)
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
    old=d.get('appointment',{})
    for who in set(old.get('guests',[]))-set(guests):
        if interiors.same_building(s['world']['cast'][who]['location'],venue):
            other='syndicate_hq__members_lounge' if target!='syndicate_hq__members_lounge' else 'syndicate_hq__cross_branch_operations_room'
            if venue=='elias_theatre':other=venue+'__receiving' if target!=venue+'__receiving' else venue+'__dressing'
            interiors.walk_actor(s,who,other)
    d['appointment']=dict(id='elias-'+uuid.uuid4().hex,title='Elias campaign appointment',venue=venue,room=target,guests=guests,start=now,end=now+180,elias_appointment=True)
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        else:interiors.walk_actor(s,who,target)
    return 'Appointment requested. Normal travel and authorised room arrival remain necessary.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None

def condition(s):
    import combat,combat_profiles
    base=combat.resources(combat_profiles.profile(s,'elias'));saved=read(s).get('condition')
    if not saved:return base
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for field,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):result[field]=min(base[maximum] if maximum else 100,result[field]+int(elapsed*rate))
    return result
def pay(s,stamina,minutes):
    resources=condition(s)
    if resources['stamina']<stamina:raise ValueError('Recover sufficient stamina before this action.')
    resources['stamina']-=stamina;__import__('world_loop').advance(s,minutes)
    data(s)['condition']=dict(resources=resources,minute=s['world']['minute'])

def _profile():
    import combat_profiles,combat_moves,combat_path
    p=combat_profiles.make('elias-historical',dict(awakened=True))
    p.update(name='Elias · age 23',combat_id='elias-historical',trait=dict(name='Pyromovement',description='Movement accumulates heat; stopping or restraint limits accumulation. Heated strikes require delivery.',effect='flow'),form=None,basis='Exact-era family defence; trained adult disciplines, no present signature or Path history.')
    p['stats'].update(awakened_power=76,trait_refinement=82,martial_skill=88,fight_iq=86);p['arts']={art:88 for art in ('Judo','Japanese Jujutsu','Aikido','Kickboxing')}
    p.pop('moveset',None);p.pop('path',None);combat_path.initialise(p,'elias-historical');combat_moves.initialise(p,'elias-historical');p['moveset']['unique']=[]
    __import__('historical_combat').strengthen(p,'elias')
    return p
def encounter(s,mission,historical=False,formation=None):
    import combat,combat_profiles,combat_engine
    p=combat_profiles.profile(s,'elias');q=combat_profiles.make('elias-route-opposition',dict(awakened=False))
    name=('Formation leader · '+formation) if historical else 'Konrad Braun · armed breakaway command'
    skill=65 if historical else 73
    q.update(name=name,combat_id='elias-route-opposition',portrait='elias-historical-opposition' if historical else 'konrad-current',trait=None,awakened=False,basis='Competent organised armed opposition; no invented Trait, Awakening or rank.')
    q['stats'].update(awakened_power=0,trait_refinement=0,martial_skill=skill,fight_iq=skill);q['arts']={'Military CQC':skill};q.pop('moveset',None)
    token=uuid.uuid4().hex
    f=dict(id=token,kind='elias_campaign',opponent=name,opponent_profile=q,location=s['world']['location'],player=combat.resources(p),enemy=combat.resources(q),elapsed=0,turn=0,log=['Historical formation encounter: actual victory required.' if historical else 'Stop the armed resistance. Records, civilians, authority and custody require separate actions.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,elias_mission=mission,elias_historical=historical,elias_formation=formation)
    combat_engine.ensure_arena(f)
    if historical:
        f['location_label']='Braun estate outside Hamburg · '+formation
        f['historical_portraits']={'elias':'elias-actor',name:'elias-historical-opposition'}
    else:
        f['contextual_portraits']={'elias':'elias-selection',name:'konrad-current'};f['room']='elias_theatre__loading';f['player']=condition(s)
        if f['player']['health']<=0:raise ValueError('Recover before retrying armed containment.')
    return f

def start_session(s,memory):
    import game_core
    validate(s,'memory');d=data(s)
    if d['phase']!='memory' or MEMORY_AT.get(d['chapter'])!=memory:raise ValueError('This is not the current mandatory memory.')
    if memory not in (*FORMATIONS,'EL-F05'):raise ValueError('This memory has no encounter.')
    nested=game_core.fresh('elias');nested['routes']={};nested['world']['cast']={};nested['world']['npcs']=[];nested['world'].update(location='elias_german_estate',minute=480,time_mode='paused');nested['combat']['profiles']['elias']=_profile()
    nested['ace_historical_context']=dict(age=23,title='Independent Braun family defender')
    token=uuid.uuid4().hex
    d['session']=dict(token=token,mission=memory,historical=True,state=nested,checkpoint='duel' if memory=='EL-F05' else 'reconnaissance',formation_index=0,formation_receipts=[],receipt=None,duel_cursor=0,duel_methods=[],duel_events=[])
    return 'Historical checkpoint opened; present state is untouched.'
def historical_approach(s,token,action):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if item['mission'] not in FORMATIONS:raise ValueError('Use the authored duel controls.')
    if item['checkpoint']=='reconnaissance' and action=='observe':item['checkpoint']='approach'
    elif item['checkpoint']=='approach' and action in ('angle','pressure'):
        n=item['state'];formation=FORMATIONS[item['mission']][item['formation_index']];f=encounter(n,item['mission'],True,formation)
        f['player']['stamina']-=8 if action=='angle' else 3
        n['combat']['active']=f;item.update(checkpoint='confrontation',approach=action,receipt=None)
    else:raise ValueError('Observe and choose a historical approach first.')
    return 'Historical movement committed; heat still requires actual movement in the encounter.'
def _receipt(f):
    exchanges=f.get('exchanges',[]);real=bool(exchanges) and f.get('status')=='finished'
    won=real and f.get('result','').startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    return dict(token=f['id'],mission=f['elias_mission'],formation=f.get('elias_formation'),won=won,result=f.get('result'),turns=f['turn'],exchanges=[r['id'] for r in exchanges],consumed=True)
def finish_session(s,token):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This result belongs to a closed encounter or another save.')
    if item['mission']=='EL-F05':
        if item['duel_cursor']!=3 or not item.get('receipt'):raise ValueError('Complete the three committed historical exchanges first.')
        return item['receipt']
    f=__import__('combat').active(item['state'])
    if item['checkpoint']!='confrontation' or not f or f['status']!='finished':raise ValueError('Resolve or concede the actual encounter first.')
    if item.get('receipt') and item['receipt']['token']==f['id']:return item['receipt']
    receipt=_receipt(f);item['receipt']=receipt
    if receipt['won']:item['formation_receipts'].append(copy.deepcopy(receipt))
    return receipt
def next_formation(s,token):
    item=session(s);receipt=finish_session(s,token)
    if not receipt.get('won') or item['formation_index']!=0:raise ValueError('A genuine first formation victory is required.')
    item['formation_index']=1;item.update(checkpoint='reconnaissance',receipt=None);item['state']['combat']['active']=None
    return 'First formation routed and disarmed by Elias. The second remains unresolved.'
def duel_step(s,token,method):
    item=session(s)
    if not item or item['token']!=token or item['mission']!='EL-F05':raise ValueError('This authored duel token has expired.')
    if item['duel_cursor']>=3 or method not in ('rhythm','leverage','distance'):raise ValueError('Choose a supported uncompleted duel exchange.')
    from elias_campaign_content import DUEL_COUNTERS
    cursor=item['duel_cursor'];text=DUEL_COUNTERS[method][0 if method not in item['duel_methods'] else 1]
    if cursor==2:text+=' The decisive counter takes Elias’s balance. The Crow fixes his shoulder and turns the attempt to rise into physical impossibility. Elias cannot continue. This is his first personal defeat.'
    item['duel_methods'].append(method);item['duel_events'].append(dict(exchange=cursor+1,method=method,witnessed_counter=text));item['duel_cursor']+=1
    if item['duel_cursor']==3:item['receipt']=dict(token=token,mission='EL-F05',kind='authored_fixed_history',result='Crow personally defeated healthy Elias at family headquarters',first_defeat=True,healthy_start=True,methods=list(item['duel_methods']),events=copy.deepcopy(item['duel_events']),consumed=True)
    return text
def return_session(s,token):
    d=data(s);item=session(s);receipt=finish_session(s,token)
    complete=item['mission']=='EL-F05' or len(item['formation_receipts'])==2
    if complete:
        memory=item['mission']
        if memory not in d['memories']:d['memories'].append(memory)
        additions=[receipt] if memory=='EL-F05' else item['formation_receipts']
        for r in additions:
            if not any(row['token']==r['token'] for row in d['receipts']):d['receipts'].append(copy.deepcopy(r))
        d['pending_return']=memory;d['phase']='tasks' if d['chapter'] in TASKS else 'aftermath'
    d['session']=None
    return 'Returned to the present. '+('The remembered result is recorded.' if complete else 'The memory remains incomplete.')
def retry_session(s):
    item=session(s)
    if not item or item['mission']=='EL-F05' or not item.get('receipt') or item['receipt']['won']:raise ValueError('Retry follows an unsuccessful formation attempt.')
    item['state']['combat']['active']=None;item.update(checkpoint='reconnaissance',receipt=None)
    return 'Historical formation restarted; earlier accepted formation receipts remain.'
def abandon_session(s,token):
    d=data(s)
    if not d['session'] or d['session']['token']!=token:raise ValueError('This return token has expired.')
    d['session']=None;return 'Returned safely. The mandatory memory remains incomplete.'

# Exact mandatory actions for chapter progression; narration cannot satisfy them.
TASKS={0:{'assignment'},1:{'rehearsal'},3:{'commitment'},4:{'dispatch'},6:{'obligation'},7:{'corroborate'},8:{'rehearsal_choice'},9:{'roles'},10:{'method'},11:{'prepare'},12:{'containment'}}
def _done(d,key):return key in d.setdefault('tasks_done',{}).get(CHAPTER_IDS[d['chapter']],[])
def _mark(d,key):
    rows=d.setdefault('tasks_done',{}).setdefault(CHAPTER_IDS[d['chapter']],[])
    if key not in rows:rows.append(key)
    if TASKS.get(d['chapter'],set()).issubset(rows):d['phase']='aftermath'
def perform_action(s,action,value=''):
    validate(s,action,value);d=data(s);i=d['chapter'];key=CHAPTER_IDS[i];op=d['operations'].setdefault(key,{})
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This briefing has already been heard.')
        d['phase']='memory' if i in MEMORY_AT else 'tasks' if i in TASKS else 'aftermath'
        if i==0:
            # Acceptance is part of finishing the actual assignment scene. Keep
            # the legacy task handler for saves paused at its former extra click.
            d['assignment']=dict(objective='Preserve useful affiliate operations and contain unauthorised independence',audience=['elias','crow'])
            _mark(d,'assignment')
    elif action=='memory':
        memory=MEMORY_AT.get(i)
        if d['phase']!='memory' or memory in d['memories']:raise ValueError('This mandatory memory is unavailable.')
        if memory in (*FORMATIONS,'EL-F05'):return start_session(s,memory)
        d['memories'].append(memory);d['pending_return']=memory;d['phase']='tasks' if i in TASKS else 'aftermath'
        if memory=='EL-F06':d['historical_affiliate']=dict(administrator='Johanna Braun',independence=False,direct_service='Elias',suit_command=False)
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('No historical reflection is waiting.')
        d['pending_return']=None
    elif action=='task':
        if d['phase']!='tasks' or value not in TASKS.get(i,set()) or _done(d,value):raise ValueError('This chapter task is unavailable or already recorded.')
        if value=='assignment':d['assignment']=dict(objective='Preserve useful affiliate operations and contain unauthorised independence',audience=['elias','crow'])
        elif value=='rehearsal':
            if not local_here(s,'elias-lotte'):raise ValueError('Lotte must attend the actual scheduled rehearsal.')
            d['choices']['first_rehearsal']='completed with Lotte'
        elif value=='commitment':
            if not local_here(s,'elias-johanna'):raise ValueError('Johanna must arrive with the original signed commitment.')
            d['evidence']['commitment']=dict(source='Johanna’s original signed Konrad pledge',verified=True,recipient='Elias',unaltered=True)
        elif value=='dispatch':
            pay(s,6,3);d['evidence']['dispatch']=dict(source='loading office dispatch carbon and separate duty log',verified=True,recipient='Elias',unaltered=True)
        elif value=='obligation':
            if not local_here(s,'elias-johanna'):raise ValueError('Johanna must attend the obligation review.')
            d['obligations']=dict(reporting=True,revenue=True,independent_force=False,administrator='Johanna Braun')
        elif value=='corroborate':
            if not all(d['evidence'].get(k,{}).get('verified') for k in ('commitment','dispatch')):raise ValueError('Inspect the original commitment and independent dispatch first.')
            if not local_here(s,'elias-johanna'):raise ValueError('Arrange Johanna’s bounded corroboration interview first.')
            d['evidence']['ledger']=dict(text=LEDGER,sha256=LEDGER_HASH,source='Johanna’s original reserve ledger',verified=True,holder='Johanna Braun',sealed=False)
        elif value=='roles':
            if set(d['support'])!=set(ROLES):raise ValueError('Each specialist must accept their own bounded role.')
        elif value=='prepare':
            if not all(d['evidence'].get(k,{}).get('verified') for k in ('commitment','dispatch','ledger')) or not d['choices'].get('method') or set(d['support'])!=set(ROLES):raise ValueError('Verify the complete trail, select a method and agree all support roles first.')
            if not local_here(s,'elias-johanna'):raise ValueError('Johanna must attend to sign the limited receiving instruction.')
            d['preparation']=dict(custodian='Johanna Braun',receiver='authorised Braun affiliate security receiving team',authority='Johanna’s signed limited detention and revocation instruction',records_hash=LEDGER_HASH)
        elif value in ('method','rehearsal_choice','containment'):raise ValueError('Resolve this task through its explicit choice or actual objective controls.')
        _mark(d,value)
    elif action=='rehearsal_choice':
        if i!=8 or d['phase']!='tasks' or value not in ('keep','renegotiate','extra') or _done(d,'rehearsal_choice'):raise ValueError('Choose a supported production commitment once.')
        if not local_here(s,'elias-lotte'):raise ValueError('Lotte must attend the professional scheduling decision.')
        d['choices']['rehearsal']=value
        if value=='extra':pay(s,10,20);d['choices']['missed_rehearsal']=True
        elif value=='renegotiate':pay(s,0,5)
        _mark(d,'rehearsal_choice')
    elif action=='method':
        if i!=10 or d['phase']!='tasks' or value not in ('quiet','bold') or _done(d,'method'):raise ValueError('Select one viable final method.')
        if value=='bold':pay(s,18,15);d['choices']['reserve_cost']=dict(stamina=18,minutes=15,reason='private demonstration draws the reserve security allocation and delays the production reset')
        d['choices']['method']=value;_mark(d,'method')
    elif action=='support':
        if i!=9 or d['phase']!='tasks' or value not in ROLES:raise ValueError('Agree specialist roles during the private preparation chapter.')
        d['support'][value]=dict(role=ROLES[value],accepted=True)
        if set(d['support'])==set(ROLES):_mark(d,'roles')
    elif action=='disclose':
        who,_,topic=value.partition(':')
        if i not in (9,13) or who not in ROLES or topic not in ('account','private'):raise ValueError('Select a supported private disclosure recipient.')
        d['disclosures'][who]=topic
        if topic=='account':
            facts=d['knowledge'].setdefault(who,[]);fact='Elias voluntarily described his first inferiority and need for acknowledgement'
            if fact not in facts:facts.append(fact)
    elif action=='separate':
        if i!=12 or d['phase']!='tasks' or not d.get('preparation'):raise ValueError('Confirm final authority before separating the civilian route.')
        if op.get('civilians_separated'):raise ValueError('The civilian route is already separated.')
        if not support_available(s,'mavis'):raise ValueError('The agreed cover specialist must be present and available.')
        pay(s,5,2);op['civilians_separated']=True;op['cover_preserved']=True;op['audience_knowledge']=['public production only']
    elif action=='objective':
        if i!=12 or d['phase']!='tasks' or not op.get('civilians_separated') or not d.get('preparation') or op.get('attack_stopped'):raise ValueError('Separate civilians and confirm authority before the unresolved armed confrontation.')
        __import__('combat').guard(s);f=encounter(s,key);s['combat']['active']=f;op['encounter_token']=f['id']
    elif action=='seal':
        if i!=12 or not op.get('attack_stopped') or op.get('records_sealed'):raise ValueError('Defeat the actual armed resistance before sealing the original records once.')
        if not support_available(s,'camila'):raise ValueError('The agreed records specialist must be present and available.')
        ledger=d['evidence'].get('ledger',{})
        if ledger.get('text')!=LEDGER or ledger.get('sha256')!=LEDGER_HASH or d['preparation']['records_hash']!=LEDGER_HASH:raise ValueError('The original ledger must remain unaltered and authenticated.')
        op['records_sealed']=dict(sha256=LEDGER_HASH,recipient='Johanna’s secured affiliate archive',authenticator='Camila',minute=s['world']['minute']);ledger['sealed']=True
    elif action=='disarm':
        if i!=12 or not op.get('attack_stopped') or op.get('disarmed'):raise ValueError('Defeat Konrad’s actual armed resistance before disarming him once.')
        pay(s,5,1);op['disarmed']=dict(token=op['encounter_token'],weapon_secured=True)
    elif action=='revoke':
        if i!=12 or not op.get('disarmed') or not op.get('records_sealed') or op.get('revoked'):raise ValueError('Disarm the resistance and authenticate the records before revocation once.')
        if not local_here(s,'elias-johanna'):raise ValueError('Johanna must actually attend to sign the removal of authority.')
        op['revoked']=dict(signer='Johanna Braun',signing_authority=False,security_authority=False,commitments_cancelled=True,minute=s['world']['minute'])
    elif action=='perimeter':
        if i!=12 or not op.get('revoked') or op.get('receiver_eta'):raise ValueError('Revoke unauthorised control before securing the receiving route once.')
        if not support_available(s,'martos'):raise ValueError('The agreed perimeter specialist must be present and available.')
        pay(s,8,2);op['perimeter']=dict(specialist='Martos',secured=True);op['receiver_eta']=s['world']['minute']+5
    elif action=='custody':
        if i!=12 or op.get('custody'):raise ValueError('No unresolved final custody handover is available.')
        if not all(op.get(k) for k in ('civilians_separated','attack_stopped','records_sealed','disarmed','revoked','perimeter')):raise ValueError('Complete the civilian, armed, records, disarm, authority and perimeter objectives first.')
        if not support_available(s,'martos') or not local_here(s,'elias-johanna') or s['world']['minute']<op.get('receiver_eta',10**12):raise ValueError('Wait for the authorised receiver, with Johanna and agreed perimeter support present.')
        op['custody']=dict(id=uuid.uuid4().hex,token=op['encounter_token'],custodian='Johanna Braun',receiver=d['preparation']['receiver'],arrived=True,minute=s['world']['minute'],result='disarmed Konrad received into supervised private detention')
        d['present_affiliate']=dict(administrator='Johanna Braun',retained=True,obligations=copy.deepcopy(d['obligations']),konrad_authority=False,suit_command=False)
        d['ending']='expensive_performance' if d['choices'].get('reserve_cost') or d['choices'].get('missed_rehearsal') else 'work_completed';_mark(d,'containment')
    elif action=='aftermath':
        if d['phase']!='aftermath' or d['pending_return']:raise ValueError('Resolve the chapter tasks and historical reflection first.')
        if i==13 and (not d['ending'] or len(d['memories'])!=8 or not d['operations'].get('EL-13',{}).get('custody')):raise ValueError('Complete every mandatory memory and actual containment objective first.')
        if i==13:d['aftermath_read']=['Johanna','Lotte','Crow','stage']
        d['completed'].append(key);d['chapter']+=1;d['phase']='briefing';d['complete']=d['chapter']==14
    else:raise ValueError('Unknown Elias campaign action.')
    d.pop('scene_room',None)
    return 'Elias’s campaign record updated.'

def after_combat_close(s,f):
    if not f.get('elias_mission') or f.get('elias_historical'):return
    d=data(s);op=d['operations'].get(f['elias_mission'],{})
    if any(row['token']==f['id'] for row in d['receipts']):return
    if d['chapter']!=12 or op.get('encounter_token')!=f['id']:raise ValueError('This encounter token belongs to an expired operation.')
    receipt=_receipt(f);d['receipts'].append(receipt);d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    if receipt['won']:op['attack_stopped']=True;d['phase']='handover'
    else:d['ending']='unfinished_business';op['failed_attempts']=op.get('failed_attempts',0)+1

def action_pages(s,args):
    from campaign_prose import page
    import elias_campaign_content as content,elias_campaign_visuals as visuals
    action=args[0];value=args[1] if len(args)>1 else '';d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),13)]
    if action in ('briefing','aftermath'):lines=content.copy_scene(key,action)
    elif action=='memory':lines=content.copy_scene(MEMORY_AT[d['chapter']],'text')
    elif action=='historical_return':lines=content.copy_scene(d['pending_return'],'after_encounter')
    else:
        lines=__import__('elias_campaign_manuscript').action_scene(action,value,content.b,content.p)
        if not lines:
            text=content.ACTION_TEXT.get(action,{}).get(value) if isinstance(content.ACTION_TEXT.get(action),dict) else content.ACTION_TEXT.get(action)
            if not text:raise ValueError('No authored Elias action page is available.')
            lines=[page(text,title=chapter(s)['title'])]
    if action=='briefing' and d['chapter']==13 and d['choices'].get('reserve_cost'):
        lines.insert(-1,content.b('elias-johanna','The demonstration consumed the reserve allocation and delayed the production reset. It does not reappear because the plan worked.'))
    if action=='aftermath' and d['chapter']==13:lines=content.ending_pages(d)
    if not lines:raise ValueError('The authored scene is empty.')
    if action not in ('memory','historical_return'):
        visuals.bind(lines,key+':'+action,'text',visuals.BACKGROUNDS[room_target(s)],visuals.CURRENT,room=room_target(s))
    for index,beat in enumerate(lines):beat.setdefault('scene_id',key+'-'+action+'-%03d'%index)
    return lines
def pause_for_room(s,dialogue,next_cursor):
    beat=dialogue['beats'][next_cursor]
    if beat.get('mode')=='memory' or not beat.get('room') or __import__('interiors').room(s)==beat['room']:return False
    pending=copy.deepcopy(dialogue);pending['cursor']=next_cursor;pending.pop('presentation',None)
    data(s)['scene_resume']=pending;data(s)['scene_room']=beat['room'];s['campaign_dialogue']=None
    return True
def resume_scene(s):
    d=data(s);pending=d.get('scene_resume')
    if not pending:raise ValueError('No saved scene is waiting.')
    validate(s,'resume');pending['venue']=s['world']['location'];s['campaign_dialogue']=pending;d.pop('scene_resume',None)
    return 'Resumed the exact saved reading position in the actual room.'
