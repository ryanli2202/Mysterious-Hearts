"""MH-021: transactional chapters, bounded historical records and fixed story fights."""
import copy
import uuid

VERSION=1
CHAPTER_IDS=tuple(f'IV{i:02}' for i in range(1,19))
FRIENDS=('april','garrett','neo','daniel','tyler')
MEMORY_AT={i:f'IV-M{i+1:02}' for i in range(2,10)}

def read(s):return s.get('ivan_campaign',{})
def data(s):
    if s.get('player')!='ivan':raise ValueError('This is Ivan’s personal campaign.')
    d=s.setdefault('ivan_campaign',{})
    for key,value in dict(version=VERSION,chapter=0,phase='briefing',completed=[],memories=[],choices={},receipts=[],complete=False,friends_defeated=[],friends_spared=False,small_wound=False,ivan_defeated=False,session=None,pending_return=None,appointment=None).items():d.setdefault(key,copy.deepcopy(value))
    return d
def chapter(s):return __import__('ivan_campaign_content').CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),17)]]
def session(s):return read(s).get('session')
def room_target(s):return chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]
def required_cast(s,action=None,value=''):
    if action=='memory':return []
    return list(chapter(s).get('cast',()))
def availability(s):
    custody=s.get('interpol',{}).get('custody',{})
    required={'ivan',*required_cast(s)}
    if any(custody.get(who) for who in required):return 'A required participant is in saved custody. This campaign preserves that case and has no custody adaptation.'
    return None
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    d=data(s)
    if availability(s):raise ValueError(availability(s))
    if d['complete']:raise ValueError('This campaign is complete.')
    if d['session'] or s.get('flashback_visit'):raise ValueError('Return from history first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current scene first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Travel to the chapter location through Maps first.')
    interior_activities.require(s,room_target(s))
    if s['world']['cast']['ivan'].get('journey'):raise ValueError('Wait for actual arrival.')
    for who in required_cast(s,action,value):
        actor=s['world']['cast'].get(who,{})
        if actor.get('journey') or combat.recovering(s,who) or not interiors.available(s,who) or not interiors.same_room(s,'ivan',who):raise ValueError('A required participant has not arrived or is unavailable: '+who)
    present=set(interiors.occupants(s,room_target(s)))
    if present-{'ivan',*chapter(s).get('cast',())}:raise ValueError('Use the private room without unrelated listeners.')

def request_appointment(s,recipient=''):
    import combat,interiors,scheduled_events,interior_bookings,world_loop
    d=data(s);guests=required_cast(s)
    if not guests:raise ValueError('No participant is needed here.')
    if d['complete'] or availability(s) or d['session'] or s.get('flashback_visit') or s.get('campaign_dialogue') or combat.active(s):raise ValueError('Finish the current activity or resolve participant availability first.')
    now=s['world']['minute'];venue=destination(s);target=room_target(s)
    for who in guests:
        event=scheduled_events.active(s,who)
        if event and not event.get('ivan_appointment'):raise ValueError('A participant has another commitment: '+who)
        if combat.recovering(s,who) or not interiors.available(s,who):raise ValueError('A participant is unavailable: '+who)
    if interior_bookings.participant_conflict(s,guests,now,now+240):raise ValueError('A participant has a conflicting obligation.')
    event=dict(id='ivan-'+uuid.uuid4().hex,title='Ivan campaign appointment',venue=venue,room=target,guests=guests,start=now,end=now+240,ivan_appointment=True)
    def travel(state):
        # A new private chapter replaces the previous meeting, not its privacy.
        # Move only the previous appointment's guests, using normal room access.
        old=read(state).get('appointment') or {}
        previous=set(old.get('guests',()))
        # Completing a chapter clears its appointment. Recover only its authored
        # same-room cast, including saves already blocked before this fix.
        completed=read(state).get('completed',[])
        if completed:
            prior=__import__('ivan_campaign_content').CHAPTERS.get(completed[-1],{})
            if prior.get('room')==target:previous.update(prior.get('cast',()))
        for who in previous-set(guests):
            if who in state['world']['cast'] and interiors.same_room(state,'ivan',who):
                exits=[key for key,room in interiors.ROOMS.items() if room.building==venue and key!=target]
                exit_room=next((key for key in exits if key.endswith('__entry')),exits[0] if exits else None)
                if not exit_room or not interiors.walk_actor(state,who,exit_room):
                    raise ValueError('The previous participant cannot leave the private meeting yet: '+who)
        data(state)['appointment']=copy.deepcopy(event)
        for who in guests:
            if not interiors.same_building(state['world']['cast'][who]['location'],venue):world_loop.start_trip(state,who,venue)
            else:interiors.walk_actor(state,who,target)
    projected=copy.deepcopy(s);travel(projected);travel(s)
    return 'Appointment requested. Travel and actual arrival are required.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None

READING_ACTIONS = ('scene', 'respond', 'recollection', 'return_scene')

def reading_actions(s, action, value=''):
    """Compose existing transactions; old phase/action IDs remain resumable."""
    d=read(s);i=d.get('chapter',0);phase=d.get('phase','briefing')
    tail=not chapter(s).get('choices') and i not in (15,16)
    if action=='scene' and phase=='briefing' and not d.get('pending_return'):
        steps=[('briefing','')]
        if i in MEMORY_AT:steps += [('memory',''),('historical_return','')]
        if tail:steps.append(('aftermath',''))
        return steps
    if action=='respond' and phase=='choice' and not d.get('pending_return'):
        if value not in chapter(s).get('choices',{}):raise ValueError('Choose an offered response.')
        return [('choice',value),('aftermath','')]
    if action=='recollection' and phase=='memory' and not d.get('pending_return'):
        return [('memory',''),('historical_return','')]+([('aftermath','')] if tail else [])
    if action=='return_scene' and d.get('pending_return'):
        return [('historical_return','')]+([('aftermath','')] if phase=='aftermath' else [])
    raise ValueError('This chapter passage is unavailable or was already read.')

def perform_action(s,action,value=''):
    if action in READING_ACTIONS:
        validate(s,action,value)
        projected=copy.deepcopy(s)
        for step,option in reading_actions(s,action,value):perform_action(projected,step,option)
        # The composed steps only change this record. Commit all or none, once,
        # after the reader's final page. World/relationships/old snapshots stay put.
        s['ivan_campaign']=projected['ivan_campaign']
        return 'Chapter passage complete.'
    validate(s,action,value);d=data(s);i=d['chapter'];key=CHAPTER_IDS[i]
    if d['pending_return'] and action!='historical_return':raise ValueError('Read the return to the present first.')
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This scene was already read.')
        d['phase']='memory' if i in MEMORY_AT else 'choice' if chapter(s).get('choices') else 'combat' if i in (15,16) else 'aftermath'
        if i==5 and d['choices'].get('IV03',{}).get('value')=='excerpt':d['origin_excerpt_shared_with']=['valentina']
    elif action=='memory':
        if d['phase']!='memory':raise ValueError('This history is unavailable.')
        memory=MEMORY_AT[i]
        # Archival material and scripted recollections never issue grants or mutate live state.
        if memory not in d['memories']:d['memories'].append(memory)
        d['pending_return']=memory;d['phase']='choice' if chapter(s).get('choices') else 'aftermath'
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('No historical return is waiting.')
        d['pending_return']=None
    elif action=='choice':
        if d['phase']!='choice' or value not in chapter(s).get('choices',{}):raise ValueError('Choose an offered response.')
        d['choices'][key]=dict(value=value,audience=required_cast(s),text=chapter(s)['choices'][value][1])
        d['phase']='aftermath'
    elif action=='combat':
        if d['phase']!='combat' or i not in (15,16):raise ValueError('This confrontation is unavailable.')
        if i==16 and not d['friends_spared']:raise ValueError('The friends must be defeated and deliberately spared first.')
        import combat,combat_engine
        f=encounter(s);combat_engine.ensure_arena(f);combat.ensure(s)['active']=f;d['encounter_token']=f['id']
        return 'Fixed-story confrontation started. Tactical exchanges affect the resistance record, not the canonical ending.'
    elif action=='spare':
        if i!=15 or d['phase']!='spare' or set(d['friends_defeated'])!=set(FRIENDS):raise ValueError('All five friends must be defeated before the sparing decision.')
        d['friends_spared']=True;d['phase']='aftermath'
    elif action=='aftermath':
        if d['phase']!='aftermath':raise ValueError('Resolve the chapter objective first.')
        if i==17 and not (d['friends_spared'] and d['small_wound'] and d['ivan_defeated']):raise ValueError('The protected confrontations must be resolved first.')
        d['completed'].append(key);d['chapter']+=1;d['phase']='briefing';d['appointment']=None;d['complete']=d['chapter']==18
        if d['complete']:d['ending']=dict(captive=True,syndicate_member=True,secret_training=True,friends_support=True,coercive_operation_cancelled=True,absolution=False)
    else:raise ValueError('Unknown Ivan campaign action.')
    return 'Ivan campaign record updated.'

def encounter(s):
    import combat,combat_profiles
    d=data(s);mission='friends' if d['chapter']==15 else 'sylvanis'
    who=next((who for who in FRIENDS if who not in d['friends_defeated']),None) if mission=='friends' else 'sylvanis'
    if not who:raise ValueError('All five friends have already been defeated.')
    p=combat_profiles.profile(s,'ivan');q=copy.deepcopy(combat_profiles.profile(s,who));token=uuid.uuid4().hex
    resources=combat.resources(p)
    previous=d.get('condition')
    if previous:resources=copy.deepcopy(previous)
    if resources['health']<=0:raise ValueError('Recover before continuing the confrontation.')
    return dict(id=token,kind='ivan_campaign',display_kind='IVAN · FIXED STORY CONFRONTATION',opponent=who,opponent_profile=q,location=s['world']['location'],location_label='Network practice room',room=room_target(s),player=resources,enemy=combat.resources(q),elapsed=0,turn=0,log=['Fixed authored outcome: Ivan defeats each friend and deliberately spares them, then draws a little blood before losing to Sylvanis. Exchanges record his tactics and strain; they cannot unlock an escape ending.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,campaign_objective=True,ivan_mission=mission,contextual_portraits={who:who+'-selection','ivan':'ivan-selection'})

def fixed_result(s,f,result):
    """One explicit scenario boundary shared by concession, knockout and turn limit."""
    if not f.get('ivan_mission'):return result
    if not f.get('exchanges'):return result
    return 'Story result — Ivan defeats '+f['opponent']+'; deliberate sparing remains a separate choice.' if f['ivan_mission']=='friends' else 'Story result — a little blood, then Sylvanis defeats Ivan. Captivity continues.'
def finish_boundary(s,f):
    if f.get('ivan_mission') and f.get('turn',0)>=3 and f.get('status')=='active':
        __import__('combat').finish(s,fixed_result(s,f,''));return True
    return False
def after_combat_close(s,f):
    if not f.get('ivan_mission'):return
    d=data(s)
    if any(row['token']==f['id'] for row in d['receipts']):return
    if d.get('encounter_token')!=f['id'] or f['status']!='finished':raise ValueError('Expired or unfinished Ivan encounter.')
    if not f.get('exchanges'):
        # A zero-exchange concession is cancellation, not an authored victory.
        d.pop('encounter_token',None);return
    d['receipts'].append(dict(token=f['id'],mission=f['ivan_mission'],opponent=f['opponent'],exchanges=[row['id'] for row in f['exchanges']],physical_result=f['result']))
    d['condition']=copy.deepcopy(f['player'])
    if f['ivan_mission']=='friends':
        if f['opponent'] not in FRIENDS:raise ValueError('Wrong participant for the fixed confrontation.')
        if f['opponent'] not in d['friends_defeated']:d['friends_defeated'].append(f['opponent'])
        d['phase']='spare' if set(d['friends_defeated'])==set(FRIENDS) else 'combat'
    else:d['small_wound']=True;d['ivan_defeated']=True;d['phase']='aftermath'
    d.pop('encounter_token',None)

def action_pages(s,args):
    import ivan_campaign_content as content
    action=args[0];value=args[1] if len(args)>1 else '';d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),17)]
    if action in READING_ACTIONS:
        projected=copy.deepcopy(s);lines=[]
        for step,option in reading_actions(s,action,value):
            lines.extend(action_pages(projected,(step,option)))
            perform_action(projected,step,option)
        return lines
    if action in ('briefing','aftermath'):lines=copy.deepcopy(chapter(s)[action])
    elif action=='memory':lines=copy.deepcopy(content.MEMORIES[MEMORY_AT[d['chapter']]]['text'])
    elif action=='historical_return':lines=copy.deepcopy(content.RETURNS[d.get('pending_return') or MEMORY_AT[d['chapter']]])
    elif action=='choice':lines=copy.deepcopy(content.CHOICES[key][value])
    elif action=='spare':lines=copy.deepcopy(content.SPARING)
    elif action=='combat':lines=[content.p('This is a fixed-outcome story confrontation using the shared combat resolver. Complete exchanges to record tactics and strain, or cancel before the first exchange. The friends’ defeat, their deliberate sparing, the small wound and Ivan’s defeat are protected story events.')]
    else:raise ValueError('No authored Ivan page for this action.')
    if action=='aftermath':lines+=content.callbacks(d)
    if action=='briefing' and d.get('chapter')==5 and d.get('choices',{}).get('IV03',{}).get('value')=='excerpt':
        lines=[content.p('Before they turn to the route, Ivan puts the engineering-and-sale excerpt in front of Valentina. He keeps the rest of the file closed. She reads slowly, without reaching for the pages he has not offered.'),content.b('valentina','I can read this with you. You do not have to give me the rest.')]+lines
    return content.stage(lines,key,action,room_target(s),memory=action=='memory')

def knowledge(s,who,listeners=()):
    if s.get('player')!='ivan':return ''
    d=read(s)
    if who=='ivan':return 'Ivan was engineered before birth, sold at birth and traded at eighteen; idol work is real permitted daytime work, not free exit. These are private reflections, not automatic disclosure. The signed order remains private. '+('He remains captive after defeat and is trying restraint with friends’ support, without absolution.' if d.get('complete') else '')
    if who in FRIENDS and d.get('friends_spared'):return 'You personally confronted Ivan over the coercive operation; he defeated and deliberately spared you. No signed-order, origin dossier or general identity was automatically disclosed.'
    if who=='valentina' and who in d.get('origin_excerpt_shared_with',[]) and not set(listeners)-{'ivan','valentina'}:return 'Ivan privately showed you the limited engineering-and-birth-sale excerpt. This gives no signed-order, parent identity or other-general history. Keep it private around outsiders.'
    return __import__('ivan_generals').knowledge(s,who,listeners)


def reread_pages(s, key):
    """Read latest completed-chapter prose with saved choices, without actions.

    This separate reader leaves old verbatim archives and live state untouched.
    Only explicitly completed chapter IDs are available; no future disclosures.
    """
    if s.get('player')!='ivan' or key not in CHAPTER_IDS or key not in read(s).get('completed',[]):
        raise ValueError('Complete this Ivan chapter before rereading it.')
    shadow=copy.deepcopy(s);d=shadow['ivan_campaign'];d['chapter']=CHAPTER_IDS.index(key)
    lines=action_pages(shadow,('briefing',''))
    if d['chapter'] in MEMORY_AT:
        lines+=action_pages(shadow,('memory',''))
        d['pending_return']=MEMORY_AT[d['chapter']]
        lines+=action_pages(shadow,('historical_return',''))
        d['pending_return']=None
    selected=d.get('choices',{}).get(key,{}).get('value')
    if selected in chapter(shadow).get('choices',{}):lines+=action_pages(shadow,('choice',selected))
    if key=='IV16' and d.get('friends_spared'):lines+=action_pages(shadow,('spare',''))
    lines+=action_pages(shadow,('aftermath',''))
    for beat in lines:beat['title']=key+' · '+chapter(shadow)['title']
    return __import__('campaign_presentation').archive(dict(player='ivan',beats=lines))
