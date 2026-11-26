"""The Inheritance: finite authority, observed evidence and isolated childhood."""
import copy
import hashlib
import uuid

VERSION=1
CHAPTER_IDS=tuple('CA-%02d'%i for i in range(1,15))
MEMORY_IDS=tuple('CA-F%02d'%i for i in range(1,9))
MEMORY_AT={i:'CA-F%02d'%i for i in range(1,9)}
ROLES={'mavis':'records route','martos':'personnel escort','elias':'negotiation cover'}
LOCAL=('camila-mara','camila-inez','camila-ansel')
ROOM='camila_meridian__receiving'
RECORDS={
 'schedule':'Meridian original: Inez Salcedo reserves the East depot for the network payroll dispatch. The reserve available for this resolution is seventy allocation units.',
 'pledge':'Vey signed undertaking: Ansel promises the same East depot exclusively to a separate compact. The depot cannot satisfy both exclusive commitments.'}
HASHES={key:hashlib.sha256(text.encode()).hexdigest() for key,text in RECORDS.items()}
TASKS={0:'mandate',3:'schedule',4:'correction',5:'testimony',6:'pledge',7:'corroborate',8:'plan',9:'roles',10:'agreement',11:'prepare',12:'allocate'}
PLANS={'release':dict(cost=20,asset='East depot concession relinquished',reserve=40),
       'retain':dict(cost=45,asset='East depot retained',reserve=15)}

def read(s):return s.get('ace_campaigns',{}).get('camila',{})

def data(s):
    if s.get('player')!='camila':raise ValueError('This is Camila’s personal campaign.')
    d=s.setdefault('ace_campaigns',{'version':1}).setdefault('camila',{})
    defaults=dict(version=VERSION,chapter=0,phase='briefing',completed=[],memories=[],choices={},evidence={},agreements={},support={},disclosures={},operations={},receipts=[],session=None,pending_return=None,condition=None,ending=None,complete=False,local_visits={},reserve=70,allocations=[],mandate=None)
    for key,value in defaults.items():d.setdefault(key,copy.deepcopy(value))
    return d

def chapter(s):return __import__('camila_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),13)]]
def session(s):return read(s).get('session')
def room_target(s):
    d=read(s)
    if d.get('scene_resume'):return d['scene_resume']['beats'][d['scene_resume']['cursor']]['room']
    if d.get('scene_room'):return d['scene_room']
    if d.get('phase')=='tasks':return 'camila_meridian__loading' if d.get('chapter')==12 else ROOM
    lines=chapter(s).get(d.get('phase','briefing'),[])
    return lines[0].get('room',chapter(s)['room']) if lines else chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]

def required_cast(s,action=None,value=''):
    if action in ('support','disclose'):return [value.split(':')[0]] if value.split(':')[0] in ROLES else []
    if action=='task':return {'mandate':['crow'],'schedule':['camila-inez'],'testimony':['camila-inez'],'pledge':['camila-ansel'],'agreement':['camila-inez','camila-ansel'],'prepare':['crow']}.get(value,[])
    if action in ('seal','escort','cover','allocate'):return {'seal':['mavis'],'escort':['martos','camila-inez'],'cover':['elias'],'allocate':['camila-inez']}[action]
    if action not in (None,'briefing','aftermath','resume'):return []
    d=read(s);pending=d.get('scene_resume');lines=pending['beats'][pending['cursor']:] if pending else __import__('camila_campaign_content').ending_pages(d) if d.get('chapter')==13 and d.get('phase')=='aftermath' else chapter(s).get(d.get('phase','briefing'),[])
    return sorted({who for beat in lines if beat.get('room',room_target(s))==room_target(s) for who,_ in beat.get('speeches',[]) if who!='camila' and (who in LOCAL or who in s.get('world',{}).get('cast',{}))})

def local_here(s,who):
    visit=read(s).get('local_visits',{}).get(who,{})
    return bool(visit.get('accepted') and visit.get('room')==__import__('interiors').room(s) and visit.get('arrival',10**12)<=s['world']['minute']<visit.get('end',0))

def support_available(s,who):
    import combat,interiors
    actor=s.get('world',{}).get('cast',{}).get(who,{})
    return bool(read(s).get('support',{}).get(who,{}).get('accepted') and actor and not actor.get('journey') and not combat.recovering(s,who) and not s.get('interpol',{}).get('custody',{}).get(who) and interiors.available(s,who) and interiors.same_room(s,'camila',who))

def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if d['complete']:raise ValueError('Camila’s campaign is complete.')
    if d['session']:raise ValueError('Return from the mandatory memory first.')
    if s.get('flashback_visit'):raise ValueError('Return from the optional memory first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Go to the chapter objective through Maps first.')
    interior_activities.require(s,room_target(s))
    custody=s.get('interpol',{}).get('custody',{})
    if custody.get('camila') or custody.get('crow'):raise ValueError('The saved custody outcome prevents this operation.')
    if s['world']['cast']['camila'].get('journey'):raise ValueError('Arrive before starting the objective.')
    for who in required_cast(s,action,value):
        if who in LOCAL:
            if not local_here(s,who):raise ValueError('Arrange the voluntary appointment and wait for actual arrival: '+who)
        elif custody.get(who) or combat.recovering(s,who) or not interiors.available(s,who) or not interiors.same_room(s,'camila',who) or s['world']['cast'][who].get('journey'):raise ValueError('A required participant is unavailable or has not arrived: '+who)
    private_crow=(d['chapter'] in (0,11,13) and 'crow' in required_cast(s,action,value))
    if private_crow:
        others=set(interiors.occupants(s,interiors.room(s)))-{'camila','crow'}
        others.update(who for who in LOCAL if local_here(s,who))
        if others:raise ValueError('The private family and mandate meeting needs a room without unrelated listeners.')
    if action=='disclose':
        person=value.split(':')[0];others=set(interiors.occupants(s,interiors.room(s)))-{'camila',person}
        others.update(who for who in LOCAL if local_here(s,who))
        if others:raise ValueError('Private family disclosure needs a room without unrelated listeners.')

def request_local(s,who):
    d=data(s)
    if who not in LOCAL:raise ValueError('Choose a named local participant.')
    if d['session'] or s.get('campaign_dialogue') or s.get('flashback_visit'):raise ValueError('Finish the current scene first.')
    if destination(s)!='camila_meridian':raise ValueError('Local appointments belong at the Meridian receiving house.')
    d['local_visits'][who]=dict(accepted=True,room=room_target(s),arrival=s['world']['minute']+10,end=s['world']['minute']+190,voluntary=True)
    return 'The participant accepts a bounded appointment. Wait ten minutes for actual arrival.'

def finish_local(s,who):
    if who not in LOCAL:raise ValueError('Choose a named local participant.')
    d=data(s)
    if s.get('campaign_dialogue') or s.get('flashback_visit') or d.get('session'):raise ValueError('Finish the current scene first.')
    d['local_visits'].pop(who,None)
    return 'The voluntary local appointment has ended; the participant leaves the private meeting.'

def request_appointment(s,recipient=''):
    import scheduled_events,interior_bookings,hidden_cast,world_loop,interiors,combat
    d=data(s);guests=list(ROLES) if recipient=='team' else [recipient] if recipient in (*ROLES,'crow') else [who for who in required_cast(s) if who not in LOCAL]
    if not guests:raise ValueError('No remote colleague is needed here.')
    if d['session'] or combat.active(s) or s.get('campaign_dialogue') or s.get('flashback_visit'):raise ValueError('Finish the current scene first.')
    now=s['world']['minute'];venue=destination(s);target=room_target(s)
    for who in guests:
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A required participant is unavailable: '+who)
        current=scheduled_events.active(s,who)
        if current and not current.get('camila_appointment'):raise ValueError('A participant has another commitment: '+who)
        if venue=='syndicate_hq' and not hidden_cast.hq_access(s,who):raise ValueError('Existing headquarters authorisation is required.')
    if interior_bookings.participant_conflict(s,guests,now,now+180):raise ValueError('A participant has a conflicting obligation.')
    event=dict(id='camila-'+uuid.uuid4().hex,title='Camila campaign appointment',venue=venue,room=target,guests=guests,start=now,end=now+180,camila_appointment=True)
    projected=copy.deepcopy(s);data(projected)['appointment']=copy.deepcopy(event)
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
        else:interiors.walk_actor(projected,who,target)
    old=d.get('appointment',{})
    for who in set(old.get('guests',[]))-set(guests):
        if interiors.same_building(s['world']['cast'][who]['location'],venue):
            other=('syndicate_hq__members_lounge' if target!='syndicate_hq__members_lounge' else 'syndicate_hq__cross_branch_operations_room') if venue=='syndicate_hq' else 'camila_meridian__receiving' if target!='camila_meridian__receiving' else 'camila_meridian__sitting'
            interiors.walk_actor(s,who,other)
    d['appointment']=event
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        else:interiors.walk_actor(s,who,target)
    return 'Appointment requested. Normal travel and authorised arrival remain necessary.'

def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None

def condition(s):
    import combat,combat_profiles
    base=combat.resources(combat_profiles.profile(s,'camila'));saved=read(s).get('condition')
    if not saved:return base
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for field,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):result[field]=min(base[maximum] if maximum else 100,result[field]+int(elapsed*rate))
    return result

def pay(s,stamina,minutes):
    resources=condition(s)
    if resources['stamina']<stamina:raise ValueError('Recover sufficient stamina before this action.')
    resources['stamina']-=stamina;__import__('world_loop').advance(s,minutes);data(s)['condition']=dict(resources=resources,minute=s['world']['minute'])

def start_session(s,memory):
    validate(s,'memory');d=data(s)
    if d['phase']!='memory' or MEMORY_AT.get(d['chapter'])!=memory:raise ValueError('This is not the current mandatory memory.')
    spec=__import__('camila_campaign_content').MEMORIES[memory]
    # A purpose-built sandbox has no live world, combat profile, time or resources.
    d['session']=dict(token=uuid.uuid4().hex,mission=memory,age=spec['age'],cursor=0,events=[],state=dict(observations=[],choice=None),narrative=True)
    return 'The recollection is ready to return to the present.'

def memory_step(s,token,choice):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if item.get('narrative'):raise ValueError('This recollection has been read; return to the present.')
    from camila_campaign_content import MEMORY_TASKS
    tasks=MEMORY_TASKS[item['mission']]
    if item['cursor']>=len(tasks):raise ValueError('This memory interaction is already complete.')
    task=tasks[item['cursor']]
    if choice not in task['options']:raise ValueError('Choose an offered historical action.')
    text=task['options'][choice][1];item['events'].append(dict(step=item['cursor'],choice=choice,text=text));item['state']['observations'].append(text);item['cursor']+=1
    return text

def return_session(s,token):
    d=data(s);item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical return token has expired.')
    tasks=__import__('camila_campaign_content').MEMORY_TASKS[item['mission']]
    if not item.get('narrative') and item['cursor']!=len(tasks):raise ValueError('Complete the remembered interaction or abandon it safely.')
    memory=item['mission'];d['memories'].append(memory);d['receipts'].append(dict(token=token,mission=memory,kind='authored_recollection',events=copy.deepcopy(item['events'])))
    d['pending_return']=memory;d['session']=None;d['phase']='tasks' if d['chapter'] in TASKS else 'aftermath'
    return 'Returned to the present; only the completed recollection is recorded.'

def abandon_session(s,token):
    d=data(s)
    if not d['session'] or d['session']['token']!=token:raise ValueError('This historical return token has expired.')
    d['session']=None;return 'Returned safely; the mandatory memory remains incomplete.'

def verified(d):
    return all(d.get('evidence',{}).get(key,{}).get('text')==text and d['evidence'][key].get('sha256')==HASHES[key] for key,text in RECORDS.items()) and d.get('corroborated') is True

def _mark(d,key):
    d.setdefault('tasks_done',{})[CHAPTER_IDS[d['chapter']]]=key;d['phase']='aftermath'

def _require_final(d):
    if d['chapter']!=12 or d['phase']!='tasks':raise ValueError('This final objective is unavailable.')
    if not d.get('prepared') or not d.get('mandate',{}).get('active') or not verified(d):raise ValueError('A live finite mandate and verified original records are required.')

def perform_action(s,action,value=''):
    validate(s,action,value);d=data(s);i=d['chapter'];key=CHAPTER_IDS[i]
    if d.get('pending_return') and action!='historical_return':raise ValueError('Read the pending historical return first.')
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This briefing has already been heard.')
        d['phase']='memory' if i in MEMORY_AT else 'tasks' if i in TASKS else 'aftermath'
    elif action=='memory':return start_session(s,MEMORY_AT.get(i))
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('No historical return is waiting.')
        d['pending_return']=None
    elif action=='task':
        if d['phase']!='tasks' or TASKS.get(i)!=value:raise ValueError('This chapter task is unavailable or already recorded.')
        if value=='mandate':
            # Private briefing is in HQ; subsequent tasks move to Meridian.
            d['mandate']=dict(active=True,objective='Preserve Meridian payroll and core network; resolve the competing depot commitments',family_disclosure_allowed=True,current_cardmaster='crow',suit_command=False)
        elif value=='schedule':d['evidence']['schedule']=dict(text=RECORDS['schedule'],sha256=HASHES['schedule'],observed=True,source='Inez original')
        elif value=='correction':
            if 'schedule' not in d['evidence']:raise ValueError('Observe the original schedule before correcting the hypothesis.')
            d['choices']['hypothesis']='incompatible promises, not imaginary missing money'
        elif value=='testimony':d['agreements']['impact']=dict(witness='Inez Salcedo',payroll_due=True,outsider_cost='Service interruption already cost two independent shifts; no recovery can erase them.')
        elif value=='pledge':d['evidence']['pledge']=dict(text=RECORDS['pledge'],sha256=HASHES['pledge'],observed=True,source='Ansel signed undertaking')
        elif value=='corroborate':
            if not all(d['evidence'].get(k,{}).get('text')==v and d['evidence'][k].get('sha256')==HASHES[k] for k,v in RECORDS.items()):raise ValueError('Both unaltered observed originals are required; Analysis cannot supply unseen evidence.')
            pay(s,6,3);d['corroborated']=True
        elif value=='roles':
            if set(d['support'])!=set(ROLES):raise ValueError('Agree all three voluntary specialist roles first.')
        elif value=='agreement':
            if not verified(d) or d['choices'].get('plan') not in PLANS:raise ValueError('A verified trail and a chosen viable allocation plan are required.')
            d['agreements']['inez']=dict(signed=True,plan=d['choices']['plan'],conditions='Payroll funded, actual personnel recovered, signed allocation before depot disposition')
            d['agreements']['ansel']=dict(acknowledged=True,release=False,refusal='Ansel refuses release and calls his armed depot contractors. Refusal is recorded, not treated as consent.')
        elif value=='prepare':
            if not verified(d) or not d['agreements'].get('inez',{}).get('signed') or set(d['support'])!=set(ROLES):raise ValueError('Verified records, signed operating terms and accepted roles are required.')
            d['prepared']=True
        else:raise ValueError('Use the plan or allocation controls for this objective.')
        _mark(d,value)
    elif action=='plan':
        if i!=8 or d['phase']!='tasks' or value not in PLANS or d['choices'].get('plan'):raise ValueError('Choose one available allocation plan at this checkpoint.')
        if not verified(d) or d['reserve']!=70:raise ValueError('Verify the originals and the seventy-unit reserve before committing the bridge.')
        d['reserve']-=10;d['allocations'].append(dict(id='bridge',units=10,purpose='Keep the payroll operation open pending recovery'));d['choices']['plan']=value;_mark(d,'plan')
    elif action=='support':
        if i!=9 or d['phase']!='tasks' or value not in ROLES or value in d['support']:raise ValueError('This specialist agreement is unavailable or already recorded.')
        d['support'][value]=dict(role=ROLES[value],accepted=True,limited=True)
    elif action=='disclose':
        who,_,topic=value.partition(':')
        if i!=9 or d['phase']!='tasks' or who not in ROLES or topic not in ('family','private'):raise ValueError('Choose a permitted recipient and disclosure.')
        if not d.get('mandate',{}).get('family_disclosure_allowed'):raise ValueError('No family disclosure has been authorised.')
        if who in d['disclosures']:raise ValueError('This recipient choice has already been recorded.')
        d['disclosures'][who]=topic
        if topic=='family':d.setdefault('recipient_knowledge',{})[who]=['Crow adopted and raised Camila']
    elif action in ('cover','objective','seal','escort','allocate'):
        _require_final(d);op=d['operations'].setdefault('CA-13',{})
        if op.get(action):raise ValueError('This objective is already recorded.')
        if action=='cover':
            if not support_available(s,'elias'):raise ValueError('The agreed negotiation-cover specialist must actually attend.')
            op['cover']=dict(specialist='elias',public_route_separate=True)
        elif action=='objective':
            if not op.get('cover') or not all(support_available(s,who) for who in ROLES):raise ValueError('Separate the public route and assemble the agreed specialists first.')
            if op.get('attack_stopped'):raise ValueError('The actual armed obstruction has already ended.')
            import combat_engine
            f=encounter(s);combat_engine.ensure_arena(f);op['encounter_token']=f['id'];s['combat']['active']=f
        elif action=='seal':
            if not op.get('attack_stopped') or not support_available(s,'mavis'):raise ValueError('Stop the actual obstruction and bring the records specialist before sealing.')
            op['seal']=dict(hashes=copy.deepcopy(HASHES),originals=True,specialist='mavis')
        elif action=='escort':
            if not op.get('attack_stopped') or not support_available(s,'martos') or not local_here(s,'camila-inez'):raise ValueError('Stop the obstruction and bring the escort and Inez to recover the personnel.')
            pay(s,8,2);op['escort']=dict(specialist='martos',receiver='Inez Salcedo',personnel=['Meridian dispatch team'],arrived=True)
        else:
            plan=PLANS.get(d['choices'].get('plan'))
            if not plan or not all(op.get(k) for k in ('cover','attack_stopped','seal','escort')) or not d['agreements'].get('inez',{}).get('signed'):raise ValueError('Complete the actual cover, resistance, original-record and personnel objectives before allocation.')
            if d['agreements']['inez']['plan']!=d['choices']['plan'] or d['reserve']<plan['cost']:raise ValueError('The signed plan and sufficient remaining reserve must match.')
            d['reserve']-=plan['cost'];d['allocations'].append(dict(id='final',units=plan['cost'],purpose=plan['asset']));op['allocate']=dict(id=uuid.uuid4().hex,plan=d['choices']['plan'],units=plan['cost'],reserve=d['reserve'],payroll_funded=True,asset=plan['asset'])
            d['mandate']['active']=False;d['mandate']['expired_by']='completed allocation';d['ending']='inheritance_with_cost' if d['choices']['plan']=='release' else 'decision_she_can_own';_mark(d,'allocate')
    elif action=='aftermath':
        if d['phase']!='aftermath':raise ValueError('Complete this chapter’s actual tasks first.')
        if i==13 and (set(d['memories'])!=set(MEMORY_IDS) or not d['operations'].get('CA-13',{}).get('allocate') or d['mandate']['active']):raise ValueError('All eight memories, final allocation and expired mandate are required.')
        d['completed'].append(key);d['chapter']+=1;d['phase']='briefing';d['complete']=d['chapter']==14
    else:raise ValueError('Unknown Camila campaign action.')
    d.pop('scene_room',None)
    return 'Camila’s campaign record updated.'

def encounter(s):
    import combat,combat_profiles
    p=combat_profiles.profile(s,'camila');q=combat_profiles.make('meridian-obstruction',dict(awakened=False))
    q.update(name='Meridian armed contractor',combat_id='meridian-obstruction',portrait='camila-contractor',trait=None,awakened=False,basis='Ansel’s hired armed obstruction; no invented Trait or rank.')
    q['stats'].update(awakened_power=0,trait_refinement=0,martial_skill=69,fight_iq=67);q['arts']={'Military CQC':69};q.pop('moveset',None)
    token=uuid.uuid4().hex;resources=condition(s)
    if resources['health']<=0:raise ValueError('Recover before retrying the obstruction.')
    return dict(id=token,kind='camila_campaign',display_kind='CAMILA · THE INHERITANCE',opponent=q['name'],opponent_profile=q,location=s['world']['location'],location_label='Meridian loading court',room='camila_meridian__loading',player=resources,enemy=combat.resources(q),elapsed=0,turn=0,log=['Recover the dispatch personnel and original records. Analysis is observation, never an automatic victory.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,camila_mission='CA-13',contextual_portraits={'camila':'camila-syndicate',q['name']:'camila-contractor'})

def after_combat_close(s,f):
    if not f.get('camila_mission'):return
    d=data(s);op=d['operations'].get('CA-13',{})
    if any(row['token']==f['id'] for row in d['receipts']):return
    if d['chapter']!=12 or op.get('encounter_token')!=f['id']:raise ValueError('This encounter belongs to an expired operation.')
    real=bool(f.get('exchanges')) and f['status']=='finished'
    won=real and (f.get('result') or '').startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    d['receipts'].append(dict(token=f['id'],mission='CA-13',kind='combat',won=won,exchanges=[row['id'] for row in f.get('exchanges',[])]));d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    if won:op['attack_stopped']=True;d['ending']=None
    else:d['ending']='account_remains_open';op['failed_attempts']=op.get('failed_attempts',0)+1

def action_pages(s,args):
    import camila_campaign_content as content,camila_campaign_visuals as visuals
    action=args[0];value=args[1] if len(args)>1 else '';d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),13)]
    if action in ('briefing','aftermath'):lines=content.copy_scene(key,action)
    elif action=='memory':lines=content.copy_scene(MEMORY_AT[d['chapter']],'text')
    elif action=='historical_return':lines=content.copy_scene(d['pending_return'],'after_encounter')
    elif action=='disclose':
        who,_,topic=value.partition(':');lines=[content.b('camila','He adopted me. He raised me himself. I am telling you what this means to me, not awarding myself your obedience.' if topic=='family' else 'The mandate is the whole operational account. My family history remains private.'),content.b(who,{'mavis':'Then we have the terms we need. The rest stays in this room.','martos':'Your history stays yours. I agreed to bring the people back.','elias':'I can respect a confidence without mistaking it for an instruction.'}[who])]
    elif action=='support':lines=__import__('camila_campaign_expansion').support(value,content.b,content.p)
    else:
        text=content.ACTION_TEXT.get(action)
        if isinstance(text,dict):text=text.get(value)
        if not text:raise ValueError('No authored Camila action page is available.')
        lines=[content.p(text)]
    if action=='aftermath' and d.get('chapter')==13:lines=content.ending_pages(d)
    if not lines:raise ValueError('The authored scene is empty.')
    if action not in ('memory','historical_return'):visuals.bind(lines,key+':'+action,'text',visuals.BACKGROUNDS[room_target(s)],visuals.CURRENT,room=room_target(s))
    return lines

def pause_for_room(s,dialogue,next_cursor):
    beat=dialogue['beats'][next_cursor]
    if beat.get('mode')=='memory' or not beat.get('room') or __import__('interiors').room(s)==beat['room']:return False
    pending=copy.deepcopy(dialogue);pending['cursor']=next_cursor;pending.pop('presentation',None);data(s)['scene_resume']=pending;data(s)['scene_room']=beat['room'];s['campaign_dialogue']=None
    return True

def resume_scene(s):
    d=data(s);pending=d.get('scene_resume')
    if not pending:raise ValueError('No saved scene is waiting.')
    validate(s,'resume');pending['venue']=s['world']['location'];s['campaign_dialogue']=pending;d.pop('scene_resume',None)
    return 'Resumed the exact saved reading position in the actual room.'
