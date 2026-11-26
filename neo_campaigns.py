"""MH-020: explicit, save-local progression and evidence-backed encounters."""
import copy
import uuid
from neo_campaign_content import MEMORY_AT

CHAPTER_IDS=tuple(f'NE{i:02}' for i in range(1,15))
MEMORY_IDS=tuple(f'NE-M{i:02}' for i in range(1,7))
TEAM=('alyssa','tyler','daniel','april','garrett')
LOCAL=('mariko','tyler-father','soren','hachimura','thirteen')
FIGHTS={1:'club',2:'alfheim',3:'evacuation',5:'withdrawal',6:'blackhaven',7:'transport',8:'centre',10:'entry',11:'hachimura',12:'formation'}
CHOICES={9:('later_disclosure',('private','programme','parentage')),0:('ordinary',('repair','meal','evening')),4:('disclosure',('private','programme','parentage')),6:('approach',('meeting','observe')),7:('boarding',('lane','barrier')),10:('allocation',('tyler','daniel')),11:('response',('property','speak','silence')),12:('contact',('supervised','statement')),13:('remembrance',('invited','private','quiet'))}
STEPS={7:('open','account','handoff'),10:('annex_handoff',)}

def read(s):return s.get('neo_campaign',{})
def data(s):
    if s.get('player')!='neo':raise ValueError('This is Neo’s personal campaign.')
    d=s.setdefault('neo_campaign',{})
    defaults=dict(version=1,started=False,chapter=0,phase='briefing',completed=[],memories=[],choices={},disclosures={},evidence={},operations={},receipts=[],session=None,pending_return=None,condition=None,complete=False,mother_dead=False,custody={},captives={},appointments={})
    for k,v in defaults.items():d.setdefault(k,copy.deepcopy(v))
    return d
def chapter(s):return __import__('neo_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),13)]]
def session(s):return read(s).get('session')
def pending_memory(s):return next((key for key in MEMORY_AT.get(read(s).get('chapter',0),()) if key not in read(s).get('memories',[])),None)
def room_target(s):
    d=read(s)
    if d.get('chapter')==10 and d.get('operations',{}).get('entry'):return 'neo_annex__records'
    return chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]
def required_cast(s,action=None,value=''):
    if action=='disclose':return [value.split(':')[0]]
    if action in (None,'briefing') and read(s).get('chapter') in (1,4):return list(TEAM)
    if action=='objective':return ['tyler','daniel','april'] if read(s).get('chapter')==12 else []
    if action=='step':return ['alyssa']
    if action in ('start','memory'):return []
    import neo_campaign_content as content
    if action=='historical_return':
        lines=content.MEMORIES.get(read(s).get('pending_return'),{}).get('after_encounter',[])
    elif action=='aftermath':lines=chapter(s)['aftermath']
    elif action=='choice':
        if value not in CHOICES.get(read(s).get('chapter',0),('',()))[1]:return []
        lines=content.choice_scene(read(s).get('chapter',0),value)
    elif action is None:
        # Arrange everyone who actually speaks in this chapter, including the
        # return/aftermath, so the expanded scenes do not require absent actors.
        lines=chapter(s)['briefing']+chapter(s)['aftermath']
        for key in MEMORY_AT.get(read(s).get('chapter',0),()):lines+=content.MEMORIES[key]['after_encounter']
    else:lines=chapter(s)['briefing']
    return sorted({who for beat in lines for who,_ in beat['speeches'] if who in TEAM})
def unavailable(s):
    if s.get('interpol',{}).get('custody',{}).get('neo'):return 'Neo is unavailable in saved custody.'
    return ''
def suppressed(s,who):
    key={'Keisuke Hachimura':'hachimura','Number Thirteen':'thirteen','keisuke':'hachimura','keisuke-hachimura':'hachimura'}.get(who,who)
    return bool(s.get('player')=='neo' and read(s).get('custody',{}).get(key))
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if unavailable(s):raise ValueError(unavailable(s))
    if d['complete']:raise ValueError('Neo’s campaign is complete.')
    if not d['started'] and action!='start':raise ValueError('Start the campaign explicitly first.')
    if s.get('flashback_visit') or d.get('session'):raise ValueError('Return from the historical visit first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if action=='start':return
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Go to the earned objective through Maps first.')
    interior_activities.require(s,room_target(s))
    if s['world']['cast']['neo'].get('journey'):raise ValueError('Wait for actual arrival first.')
    for who in required_cast(s,action,value):
        actor=s['world']['cast'].get(who,{})
        if not actor or actor.get('journey') or combat.recovering(s,who) or s.get('interpol',{}).get('custody',{}).get(who) or not interiors.available(s,who) or not interiors.same_room(s,'neo',who):raise ValueError('A required participant has not arrived or is unavailable: '+who)
    if action=='disclose':
        person=value.split(':')[0]
        if set(interiors.occupants(s,room_target(s)))-{'neo',person}:raise ValueError('Private disclosure requires only the named listener.')

def request_appointment(s,recipient=''):
    import combat,interiors,world_loop,scheduled_events,interior_bookings
    d=data(s)
    if not d['started'] or d['complete'] or d.get('session') or s.get('campaign_dialogue') or s.get('flashback_visit') or combat.active(s):raise ValueError('Finish the current scene or start the route first.')
    guests=[recipient] if recipient in TEAM else sorted(set(required_cast(s)) | ({'tyler','daniel','april'} if d['chapter']==12 else {'alyssa'} if d['chapter'] in (7,10) else set()))
    if not guests:raise ValueError('No remote participant is required for this scene.')
    now=s['world']['minute'];venue=destination(s);room=room_target(s)
    for who in guests:
        if s.get('interpol',{}).get('custody',{}).get(who) or combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A required participant is unavailable: '+who)
        current=scheduled_events.active(s,who)
        if current and not current.get('neo_appointment'):raise ValueError('A participant has another appointment: '+who)
    if interior_bookings.participant_conflict(s,guests,now,now+240):raise ValueError('A participant has a conflicting obligation.')
    event=dict(id='neo-'+uuid.uuid4().hex,title='Neo campaign meeting',venue=venue,room=room,guests=guests,start=now,end=now+240,neo_appointment=True)
    projected=copy.deepcopy(s)
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
        else:interiors.walk_actor(projected,who,room)
    # Do not leave removed listeners in a private meeting room.
    for who in set(d.get('appointment',{}).get('guests',[]))-set(guests):
        if interiors.same_room(s,'neo',who):interiors.walk_actor(s,who,venue+'__entry' if venue+'__entry' in interiors.ROOMS and room!=venue+'__entry' else next(k for k,r in interiors.ROOMS.items() if r.building==venue and k!=room))
    d['appointment']=event
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        else:interiors.walk_actor(s,who,room)
    return 'Meeting agreed. Normal travel and actual arrival are still required.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment',{})
    return event if who in event.get('guests',[]) and event['start']<=now<event['end'] else None

def condition(s):
    import combat,combat_profiles
    base=combat.resources(combat_profiles.profile(s,'neo'));saved=read(s).get('condition')
    if not saved:return base
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for field,rate,maximum in (('health',.4,'max_health'),('energy',.7,'max_energy'),('stamina',1,None)):result[field]=min(base[maximum] if maximum else 100,result[field]+int(elapsed*rate))
    return result
def phase_after_memory(s):
    d=data(s);d['phase']='memory' if pending_memory(s) else 'tasks'
def start_session(s,memory):
    validate(s,'memory');d=data(s)
    if d['phase']!='memory' or pending_memory(s)!=memory:raise ValueError('This is not the required memory.')
    d['session']=dict(token=uuid.uuid4().hex,mission=memory,cursor=0,events=[],era=__import__('neo_campaign_content').MEMORIES[memory]['era'])
    return 'Entered the exact-age recollection. Live time and resources are untouched.'
def memory_step(s,token,choice):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical token has expired.')
    tasks=__import__('neo_campaign_content').MEMORY_TASKS[item['mission']]
    if item['cursor']>=len(tasks):raise ValueError('This memory is already complete.')
    task=tasks[item['cursor']]
    if choice not in task['options']:raise ValueError('Choose an offered historical interaction.')
    text=task['options'][choice][1];item['events'].append(dict(choice=choice,text=text));item['cursor']+=1;return text
def return_session(s,token):
    d=data(s);item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical token has expired.')
    if item['cursor']!=len(__import__('neo_campaign_content').MEMORY_TASKS[item['mission']]):raise ValueError('Complete the supplied memory or return safely without completing it.')
    d['memories'].append(item['mission']);d['receipts'].append(dict(token=token,kind='history',mission=item['mission'],events=copy.deepcopy(item['events'])))
    d['pending_return']=item['mission'];d['session']=None;phase_after_memory(s);return 'Returned to the unchanged present.'
def abandon_session(s,token):
    if not session(s) or session(s)['token']!=token:raise ValueError('This historical token has expired.')
    data(s)['session']=None;return 'Returned safely. The memory remains incomplete.'

def finish_memory_reading(s):
    """Called only at the reader's commit boundary; retain legacy session APIs."""
    memory=pending_memory(s)
    start_session(s,memory)
    d=data(s);item=d['session']
    d['memories'].append(memory)
    d['receipts'].append(dict(token=item['token'],kind='history',mission=memory,
                              mode='authored_reading',events=[]))
    d['pending_return']=memory;d['session']=None;phase_after_memory(s)
    return 'The recollection ends. Return to the present.'

def tasks_done(s):
    d=read(s);i=d.get('chapter',0)
    if i in CHOICES and CHOICES[i][0] not in d.get('choices',{}):return False
    if i in FIGHTS and not d.get('operations',{}).get(FIGHTS[i]):return False
    if i==10 and not d.get('operations',{}).get('records'):return False
    return all(step in d.get('operations',{}) for step in STEPS.get(i,()))
def perform_action(s,action,value=''):
    validate(s,action,value);d=data(s);i=d['chapter']
    if d.get('pending_return') and action!='historical_return':raise ValueError('Read the historical return first.')
    if action=='start':
        if d['started']:raise ValueError('This campaign has already started.')
        d['started']=True;return 'Neo’s campaign has started explicitly. School visits are available.'
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This scene is already complete.')
        d['phase']='memory' if pending_memory(s) else 'tasks'
    elif action=='memory':return finish_memory_reading(s)
    elif action=='historical_return':
        if not d.get('pending_return'):raise ValueError('No historical return is pending.')
        d['pending_return']=None
    elif action=='choice':
        key,options=CHOICES.get(i,('',()))
        if d['phase']!='tasks' or value not in options or key in d['choices']:raise ValueError('Choose an available unresolved decision.')
        if i in (11,12) and not d['operations'].get('hachimura' if i==11 else 'formation'):raise ValueError('Resolve the actual encounter before choosing its aftermath.')
        d['choices'][key]=value
        if key=='disclosure':
            # Decision itself is not a disclosure. Named private meetings own that.
            d['disclosure_policy']=value
        if key=='boarding':d['boarding_plan']=dict(method=value,stationary=True,cost=4 if value=='lane' else 7)
        if key=='approach':d['entry_position']='observed side lane' if value=='observe' else 'agreed front meeting'
        if key=='allocation':d['supported_first']=value
        if key=='contact':d['later_contact']='supervised offer' if value=='supervised' else 'necessary statement only'
    elif action=='disclose':
        parts=value.split(':');person=parts[0];topic=parts[1] if len(parts)==2 else ''
        if i not in (4,9) or d['phase']!='tasks' or person not in TEAM or topic not in ('programme','parentage'):raise ValueError('This private disclosure is unavailable.')
        policy=d['choices'].get('later_disclosure' if i==9 else 'disclosure')
        if topic=='parentage' and policy!='parentage':raise ValueError('Parentage has not been selected for disclosure.')
        if policy=='private':raise ValueError('Neo chose to keep the deeper history private.')
        topics=d['disclosures'].setdefault(person,[])
        if topic in topics:raise ValueError('This listener already received that fact.')
        topics.append(topic)
    elif action=='objective':
        if d['phase']!='tasks':raise ValueError('Read the scene and memories first.')
        mission='records' if i==10 and d['operations'].get('entry') else FIGHTS.get(i)
        if not mission or d['operations'].get(mission):raise ValueError('This encounter is unavailable or already resolved.')
        if i in (6,7,10) and CHOICES[i][0] not in d['choices']:raise ValueError('Choose the actual approach first.')
        f=encounter(s,mission);__import__('combat_engine').ensure_arena(f);apply_approach(s,f);d['encounter_token']=f['id'];__import__('combat').ensure(s)['active']=f;return 'Actual nonlethal objective encounter started.'
    elif action=='step':
        allowed=STEPS.get(i,())
        if d['phase']!='tasks' or value not in allowed or value in d['operations']:raise ValueError('This physical objective is unavailable or already complete.')
        if not d['operations'].get('transport' if i==7 else 'records'):raise ValueError('Resolve the real encounter before handling captives or records.')
        index=allowed.index(value)
        if index and allowed[index-1] not in d['operations']:raise ValueError('Complete the previous accounted handoff step first.')
        d['operations'][value]=dict(token=uuid.uuid4().hex,observed=True)
        if value=='account':d['captives']['transport']=dict(expected=6,accounted=6,received=0)
        if value=='handoff':
            d['captives']['transport']['received']=6;d['evidence']['manifest']=dict(origin='stationary transport compartment',verified=True,commander_photo=True)
        if value=='annex_handoff':
            d['captives']['annex']=dict(expected=4,accounted=4,received=4);d['evidence']['orders']=dict(origin='cleared annex records room',verified=True)
    elif action=='aftermath':
        if d['phase']!='tasks' or not tasks_done(s):raise ValueError('Complete this chapter’s actual objectives first.')
        if i==3 and not d['mother_dead']:
            d['mother_dead']=True;d['death_event']=dict(id='NE-MARIKO-FIXED',responsible='hachimura',other_present_deaths=0)
        if i==5:d['evidence']['blackhaven_lead']=dict(origin='Garrett’s bounded warehouse note and Alyssa’s first-hand witness accounts',verified=True)
        if i==4:
            for _ in range(3):__import__('world_loop').advance(s,24*60)
        if i==9 and 'manifest' not in d['evidence']:raise ValueError('The actual photograph manifest is required.')
        if i==13:
            if set(d['memories'])!=set(MEMORY_IDS) or set(d['custody'])!={'hachimura','thirteen'} or sum(v.get('received',0) for v in d['captives'].values())!=10:raise ValueError('All memories, living custody and ten captive handoffs are required.')
            d['complete']=True;d['ending']='a_life_of_his_own'
        d['completed'].append(CHAPTER_IDS[i]);d['chapter']+=1;d['phase']='briefing'
    else:raise ValueError('Unknown Neo campaign action.')
    return 'Neo’s campaign record updated.'

def encounter(s,mission):
    import combat,combat_profiles
    d=data(s);resources=condition(s)
    if resources['health']<=0:raise ValueError('Recover before attempting the checkpoint.')
    boss=mission in ('hachimura','evacuation','formation')
    q=combat_profiles.profile(s,'thirteen') if mission=='formation' else combat_profiles.make('neo-'+mission,dict(awakened=False))
    if mission in ('hachimura','evacuation'):
        # Authored enforcer baseline, without inventing a supernatural power.
        q.update(name='Keisuke Hachimura',combat_id='keisuke-hachimura',stats=dict(awakened_power=48,trait_refinement=0,martial_skill=80,fight_iq=80),arts={'Military CQC':80},trait=None,awakened=False,basis='Experienced coercive enforcer; prepared rematch, no new named ability.')
    elif not boss:q.update(name={'club':'House fighters','alfheim':'Collection crew','withdrawal':'Retrieval squad','blackhaven':'Retrieval lieutenant','transport':'Transport escort','centre':'Punitive assault squad','entry':'Annex entry guard','records':'Annex records guard'}[mission],stats=dict(awakened_power=30,trait_refinement=0,martial_skill=62,fight_iq=60),arts={'Military CQC':62})
    if not boss:q['portrait']='crew_enforcer' if mission=='club' else 'tengu'
    token=uuid.uuid4().hex
    return dict(id=token,kind='neo_campaign',display_kind='NEO · A LIFE OF HIS OWN',opponent=q['name'],opponent_profile=q,location=s['world']['location'],location_label=chapter(s)['title'],room=room_target(s),player=resources,enemy=combat.resources(q),elapsed=0,turn=0,log=['Nonlethal checkpoint. Evacuation: survive three actual exchanges. Formation: earn three supported openings. Other encounters require actual victory. Failure awards no deaths or story success.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,campaign_objective=True,neo_mission=mission,openings=0,support_pending=False,contextual_portraits={'neo':'neo-scene',q['name']:'thirteen-selection' if mission=='formation' else 'keisuke-hachimura-selection' if boss else 'guards/crew_enforcer' if mission=='club' else 'guards/tengu'})
def apply_approach(s,f):
    d=read(s);mission=f['neo_mission'];choices=d.get('choices',{});cost=0
    if mission=='blackhaven':
        f['arena']['positions'].update(player=0 if choices.get('approach')=='observe' else 2,enemy=4 if choices.get('approach')=='observe' else 3)
    if mission=='transport':
        cost=4 if choices.get('boarding')=='lane' else 7
        f['arena']['positions'].update(player=1 if choices.get('boarding')=='lane' else 2,enemy=3)
    if mission=='entry':
        cost=4 if choices.get('allocation')=='tyler' else 8
        f['arena']['positions'].update(player=1 if choices.get('allocation')=='tyler' else 2,enemy=3)
    if f['player']['stamina']<cost:raise ValueError('Recover enough stamina for the selected approach.')
    f['player']['stamina']-=cost;f['approach_cost']=cost;f['approach']=choices.get({'blackhaven':'approach','transport':'boarding','entry':'allocation'}.get(mission,''))

def support_opening(s):
    f=__import__('combat').active(s)
    if not f or f.get('neo_mission')!='formation' or f['status']!='active':raise ValueError('The trio formation objective is unavailable.')
    f['support_pending']=True
    __import__('combat_engine').resolve(s,__import__('combat_engine').request(s,'utility:guard'))
    return 'A real guarded exchange contests one supported opening.'
def on_exchange(s,f):
    if f.get('neo_mission')!='formation' or not f.get('exchanges'):return
    latest=f['exchanges'][-1]
    if latest.get('neo_counted'):return
    latest['neo_counted']=True
    in_range=abs(f['arena']['positions']['player']-f['arena']['positions']['enemy'])<=2
    pressured=any(row['side']=='enemy' and row['role'] in ('attack','combo','break','throw','control','counter') for row in latest['records'])
    if f.pop('support_pending',False) and f['player']['health']>0 and in_range and pressured:
        f['openings']=f.get('openings',0)+1;latest['neo_opening']=f['openings']
def finish_boundary(s,f):
    mission=f.get('neo_mission')
    met=(mission=='evacuation' and f.get('turn',0)>=3) or (mission=='formation' and f.get('openings',0)>=3)
    if met and f['player']['health']>0 and f['enemy']['health']>0:
        f.update(status='finished',result='Objective complete — evacuation covered.' if mission=='evacuation' else 'Objective complete — formation broken; medical extraction.')
        return True
    return False
def after_combat_close(s,f):
    mission=f.get('neo_mission')
    if not mission:return
    d=data(s)
    if any(r.get('token')==f['id'] for r in d['receipts']):return
    conceded=f.get('status')=='finished' and str(f.get('result','')).startswith('Defeat — conceded.')
    if d.get('encounter_token')!=f['id'] or f.get('status')!='finished' or not (f.get('exchanges') or conceded):raise ValueError('An actual resolved encounter receipt is required.')
    objective=mission=='evacuation' and len(f['exchanges'])>=3 or mission=='formation' and f.get('openings',0)>=3
    won=f['player']['health']>0 and (objective or f['enemy']['health']<=0 and str(f['result']).startswith('Victory'))
    if mission=='formation':won=f['player']['health']>0 and f.get('openings',0)>=3
    d['receipts'].append(dict(token=f['id'],kind='combat',mission=mission,won=won,exchanges=[r['id'] for r in f['exchanges']],openings=f.get('openings',0)))
    d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    if won:
        d['operations'][mission]=dict(receipt=f['id'],nonlethal=True)
        if mission in ('hachimura','formation'):
            who='hachimura' if mission=='hachimura' else 'thirteen'
            d['custody'][who]=dict(alive=True,medical=mission=='formation',receipt=f['id'])
            __import__('interpol').ensure(s)['custody'][who]=dict(location='interpol_containment',case='neo-retrieval',minute=s['world']['minute'],alive=True,medical=mission=='formation')
            if who in s['world']['cast']:s['world']['cast'][who].update(location='interpol_containment',journey=None,activity='Receiving care in secure Neo-campaign custody')
    d['last_attempt']=dict(mission=mission,won=won,retry=not won)

def finish_reading(s,reading):
    """Record only aftermath actually present in the completed reader snapshot.

    An old save may have a one-page choice open, without the expanded outcome.
    Completing that old page must not skip an aftermath it never contained.
    """
    if not reading.get('args') or reading['args'][0]!='choice':return
    d=data(s);index=d['chapter']
    if index not in (11,12):return
    key=CHAPTER_IDS[index]
    if any(beat.get('source_id','').startswith(key+':aftermath:') for beat in reading['beats']):
        seen=d.setdefault('read_outcomes',[])
        if key not in seen:seen.append(key)


def action_pages(s,args):
    import neo_campaign_content as content,neo_campaign_visuals as visuals
    d=read(s);action=args[0];value=args[1] if len(args)>1 else '';key=CHAPTER_IDS[min(d.get('chapter',0),13)]
    if action in ('briefing','aftermath'):
        # The post-combat decision scene already includes its earned outcome.
        # Legacy saves without that marker still receive the full aftermath.
        if action=='aftermath' and key in d.get('read_outcomes',[]):
            lines=[content.p('With the handoff complete, Neo leaves the response team to its work. The people beside him are waiting.')]
        else:lines=content.copy_scene(key,action)
    elif action=='memory':
        memory=pending_memory(s);lines=content.copy_scene(memory,'text');return visuals.bind(lines,memory,'text',content.MEMORIES[memory]['background'],visuals.HISTORICAL[memory],memory=True)
    elif action=='historical_return':lines=content.copy_scene(d['pending_return'],'after_encounter')
    elif action=='start':lines=[content.p('Neo already has a home, a partner and a life. Start A Life of His Own. No loss has happened merely because this page was opened.')]
    elif action=='choice':
        lines=content.choice_scene(d.get('chapter',0),value)
        if d.get('chapter') in (11,12):
            outcome=visuals.bind(content.copy_scene(key,'aftermath'),key,'aftermath',visuals.background(room_target(s)),visuals.CURRENT,room=room_target(s))
            lines=outcome+lines
    elif action=='disclose':lines=content.disclosure_scene(*value.split(':'))
    elif action=='objective':lines=[content.p('Neo checks the route out once more, then takes his place beside the others.')]
    elif action=='step':
        lines={
            'open':[content.p('Neo opens the stationary compartment from the cleared side. He steps back so the people inside can see the lane beyond him.'),content.b('neo','The way out is here. Take your time. We are staying.')],
            'account':[content.b('alyssa','I have six names. Tell me if I say yours wrong.'),content.p('She waits for each answer, checks the person in front of her, then asks who is missing. Neo keeps the doorway clear while the list becomes six people they can account for.')],
            'handoff':[content.p('All six passengers reach the receiving team alive. Alyssa checks the final handoff; Neo secures the transfer manifest and the commander photograph found with it. The door stays open behind them.')],
            'annex_handoff':[content.p('The four remaining captives reach the medical corridor. Neo waits for the receiving team to acknowledge the last person before carrying the current retrieval orders out of the cleared records room.'),content.b('neo','Four through. Keep this route open.')],
        }[value]
    else:raise ValueError('No authored page for this action.')
    if action=='briefing' and d.get('chapter') in (4,13):
        ordinary=d.get('choices',{}).get('ordinary','evening');lines.insert(0,content.p({'repair':'The unfinished radio from the repair afternoon remains on the shelf.','meal':'Neo remembers the meal he actually chose to share.','evening':'The ordinary evening they chose matters without needing an object as proof.'}[ordinary]))
    bg='locations/campaign/neo/alfheim_damaged' if key=='NE03' and action=='aftermath' else visuals.background(room_target(s))
    return visuals.bind(lines,key,action,bg,visuals.CURRENT,room=room_target(s))

def knowledge(s,who,listeners=()):
    if s.get('player')!='neo' or not read(s).get('started'):return ''
    who={'Keisuke Hachimura':'hachimura','Number Thirteen':'thirteen'}.get(who,who)
    d=read(s);facts=[]
    if d.get('mother_dead') and who=='hachimura':facts.append('The saved home attack has happened: Hachimura killed Mariko, Neo escaped, and Tyler’s father survived. Saved events override the old future-only source description. Do not volunteer private retrieval or family history to uninformed listeners.')
    if who in TEAM and d.get('chapter',0)>=5:facts.append('The retrieval team targets Neo alive; Hachimura answers to a larger command. This is safety information, not automatic knowledge of parentage or childhood scenes.')
    for topic in d.get('disclosures',{}).get(who,[]):facts.append('Neo privately disclosed '+topic+' to this recipient; do not relay it to other listeners.')
    if d.get('mother_dead') and who in ('neo',*TEAM):facts.append('Mariko died in the authored home attack; every other present-day participant survives. Historical visits are memories, not resurrection.')
    if suppressed(s,who):facts.append('This person is alive in earned secure custody and cannot resume ordinary recruitment, command appointments or meetings.')
    return ' '.join(facts)


