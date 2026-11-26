"""Authoritative Ace route operations and isolated, saved encounter sessions.

No historical world is copied from the player's present. The nested baseline is
disposable: only verified receipts and explicitly authored route facts return.
"""
import copy
import uuid

VERSION = 1
CHAPTER_IDS = tuple('MV-%02d' % n for n in range(1, 13))
MEMORY_IDS = tuple('MV-F%02d' % n for n in range(1, 7))
HISTORICAL_KIT_VERSION = 1
MEMORY_AT = {0:'MV-F01',1:'MV-F02',2:'MV-F03',3:'MV-F04',4:'MV-F05',7:'MV-F06'}
OPERATIONS = {0,3,6,7,10}
ROOMS = {'syndicate_hq':'syndicate_hq__cross_branch_operations_room',
         'glasshouse_lab':'glasshouse_lab__laboratory_workroom'}


def read(s):
    return s.get('ace_campaigns', {}).get('mavis', {})


def data(s):
    if s.get('player') != 'mavis': raise ValueError('This is Mavis’s personal campaign.')
    d = s.setdefault('ace_campaigns', {'version':VERSION}).setdefault('mavis', {})
    for k,v in dict(chapter=0,phase='briefing',memories=[],completed=[],operations={},
                    disclosures={},knowledge={},support={},receipts=[],session=None,
                    exposure=0,evidence=[],broker_removed=False,complete=False,pending_return=None,priority=None,appointments={}).items():
        d.setdefault(k,copy.deepcopy(v))
    return d


def chapter(s):
    from ace_campaign_content import CHAPTERS
    i = read(s).get('chapter',0)
    return CHAPTERS[CHAPTER_IDS[min(i,11)]]


def destination(s):
    d=read(s); phase=d.get('phase','briefing')
    if phase=='aftermath':return 'glasshouse_lab' if d.get('chapter')==4 else 'syndicate_hq'
    if phase=='briefing':
        speakers={who for b in chapter(s)['briefing'] for who,_ in b.get('speeches',[])}
        if 'crow' in speakers or speakers.intersection(('martos','elias','camila')):return 'syndicate_hq'
    place=chapter(s)['location']
    return 'mavis_dispatch_exchange' if place in ('warehouse','docks') else place


def room_target(s):
    d=read(s); venue=destination(s)
    if venue=='mavis_dispatch_exchange':
        op=d.get('operations',{}).get(CHAPTER_IDS[d.get('chapter',0)],{})
        part='receiving'
        if d.get('phase')=='operation' and op.get('approach'):
            part='inner_room' if d.get('chapter')==6 or op.get('contained') else 'exchange'
        return venue+'__'+part
    if venue=='syndicate_hq':
        phase=d.get('phase','briefing')
        speakers={who for b in chapter(s).get(phase,[]) for who,_ in b.get('speeches',[])} if phase in ('briefing','aftermath') else set()
        return venue+('__executive_meeting_room' if 'crow' in speakers else '__cross_branch_operations_room')
    return ROOMS.get(venue)


def required_cast(s,action=None,value=''):
    if action in ('memory','historical_return'):return []
    if action in ('disclose','support'):return [value.split(':')[0]]
    phase=read(s).get('phase','briefing')
    if phase not in ('briefing','aftermath'):return []
    return sorted({who for b in chapter(s)[phase] for who,_ in b.get('speeches',[])
                   if who!='mavis' and who in s['world'].get('cast',{})})


def validate(s, session_ok=False,action=None,value=''):
    import combat, interiors, flashback_visits
    d=data(s)
    if d['complete']: raise ValueError('Mavis’s campaign is complete.')
    if d['session'] and not session_ok: raise ValueError('Finish or return from the isolated encounter first.')
    if s.get('flashback_visit'): raise ValueError('Return from the optional memory area first.')
    if combat.active(s) or combat.recovering(s): raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'): raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location']) != destination(s): raise ValueError('Go to the chapter objective in Maps first.')
    room=room_target(s)
    if room: __import__('interior_activities').require(s,room)
    actor=s['world'].get('cast',{}).get('mavis',{})
    if actor.get('journey'): raise ValueError('Arrive before starting the mission.')
    custody=s.get('interpol',{}).get('custody',{})
    if custody.get('mavis') or custody.get('crow'):
        raise ValueError('The saved custody outcome prevents this operation and its command briefing.')
    # Normal room access remains authoritative; a Story objective is no invitation.
    if room and interiors.enabled(s) and interiors.access(s,'mavis',room)!='allowed':
        raise ValueError('The chapter does not override this room’s access rules.')
    for who in required_cast(s,action,value):
        if custody.get(who) or combat.recovering(s,who) or not interiors.available(s,who):
            raise ValueError('A required participant is unavailable: '+who+'.')
        if not __import__('interpol').here(s,who):
            raise ValueError('Wait for the actual participant to arrive in the objective room: '+who+'.')
    if action=='disclose' and interiors.enabled(s):
        others=set(interiors.occupants(s,interiors.room(s)))-{'mavis',value.split(':')[0]}
        if others or __import__('interior_presence').count(s,interiors.room(s)):
            raise ValueError('Wait for a private room without unrelated listeners before personal disclosure.')


def perform_action(s, action, value=''):
    validate(s,action=action,value=value)
    d=data(s); i=d['chapter']; op=d['operations'].setdefault(CHAPTER_IDS[i],{})
    if action=='briefing':
        if d['phase']!='briefing': raise ValueError('This briefing has already been heard.')
        d['phase']='operation' if i in OPERATIONS else 'memory' if i in MEMORY_AT else 'aftermath'
    elif action=='recon':
        if d['phase']!='operation' or op.get('recon'): raise ValueError('Reconnaissance is unavailable.')
        op['recon']=True; op['observed']='Two patrol intervals; a monitored direct entrance and an unguarded service return.'
    elif action=='approach':
        if d['phase']!='operation' or not op.get('recon') or value not in ('service','direct'): raise ValueError('Observe the site and choose an available approach.')
        if op.get('approach'): raise ValueError('The approach is already committed.')
        op['approach']=value
        if value=='direct': d['exposure']+=1
        else: op['secondary_copy_lost']=True
    elif action=='objective':
        if d['phase']!='operation' or not op.get('approach') or op.get('objective'): raise ValueError('Commit an observed approach first.')
        op['objective']=True
        if i==10:
            op['authenticated']=True
            op['objective']=False
        elif i==6:
            start_session(s,CHAPTER_IDS[i],historical=False)
        else:
            op['extracted']=True
            d['evidence'].append(CHAPTER_IDS[i]+':authenticated-fragment')
            d['phase']='memory' if i in MEMORY_AT else 'aftermath'
    elif action=='contain':
        if i!=10 or not op.get('authenticated') or op.get('contained'):
            raise ValueError('Authenticate the transfer before containing it.')
        if set(d['support'])!={'martos','elias','camila'} or d['priority'] not in ('contain','retrieve'):
            raise ValueError('Agree specialist roles and the operational priority first.')
        op['contained']=True
        op['secondary_copy_lost']=d['priority']=='contain' or op.get('secondary_copy_lost',False)
        if d['priority']=='retrieve':d['exposure']+=1
    elif action=='confront':
        if i!=10 or not op.get('contained') or op.get('objective'):raise ValueError('Contain the authenticated transfer before confronting the Broker.')
        op['objective']=True;start_session(s,CHAPTER_IDS[i],False)
    elif action=='memory':
        key=MEMORY_AT.get(i)
        if d['phase']!='memory' or key in d['memories']: raise ValueError('This mandatory memory is unavailable.')
        if key in ('MV-F02','MV-F04'):
            start_session(s,key,historical=True)
        else:
            d['memories'].append(key); d['phase']='aftermath'
    elif action=='disclose':
        if i!=8 or d['phase']!='aftermath': raise ValueError('Personal disclosure belongs to the private debrief.')
        who,sep,topic=value.partition(':')
        if who not in ('martos','elias','camila') or topic not in ('private','contract'): raise ValueError('Choose a recipient and a supported disclosure.')
        d['disclosures'][who]=topic
    elif action=='support':
        if i!=9 or value not in ('martos','elias','camila'): raise ValueError('Agree the named specialist roles during preparation.')
        d['support'][value]={'martos':'extraction','elias':'cover','camila':'authentication'}[value]
    elif action=='priority':
        if i!=9 or value not in ('contain','retrieve'):raise ValueError('Set the operation priority during final preparation.')
        d['priority']=value
    elif action=='historical_return':
        if not d['pending_return']: raise ValueError('There is no unread historical encounter outcome.')
        d['pending_return']=None
    elif action=='aftermath':
        if d['phase']!='aftermath': raise ValueError('Resolve the chapter’s objectives and mandatory memory first.')
        if d['pending_return']:raise ValueError('Read the resolved historical return before the present debrief.')
        if i==9 and set(d['support'])!={'martos','elias','camila'}: raise ValueError('Agree all three specialist roles before the exchange.')
        if i==9 and d['priority'] not in ('contain','retrieve'):raise ValueError('Agree the operational priority before the exchange.')
        if i==10 and not d['broker_removed']: raise ValueError('Resolve the actual exchange confrontation first.')
        if i in (5,8,9):
            for who in ('martos','elias','camila'):
                facts=d['knowledge'].setdefault(who,[])
                fact={5:'archive-custodian',8:'broker-transfer-operation',9:'agreed-final-roles'}[i]
                if fact not in facts: facts.append(fact)
        d['completed'].append(CHAPTER_IDS[i]); d['chapter']+=1
        d['phase']='briefing'; d['complete']=d['chapter']==12
    else: raise ValueError('Unknown Ace campaign action.')
    return 'Mavis’s story continues.'


def request_appointment(s,recipient=''):
    """A scoped professional invitation; ordinary travel and door checks apply."""
    import interiors,combat,scheduled_events,interior_bookings,hidden_cast,world_loop
    d=data(s)
    if d['session'] or combat.active(s) or s.get('campaign_dialogue'):
        raise ValueError('Finish the current encounter or conversation first.')
    guests=[recipient] if recipient in ('martos','elias','camila') else required_cast(s)
    if not guests:raise ValueError('This objective requires no remote appointment.')
    venue=destination(s); target=room_target(s); now=s['world']['minute']
    for who in guests:
        if s.get('interpol',{}).get('custody',{}).get(who):raise ValueError('A required participant is in custody: '+who+'.')
        if combat.recovering(s,who) or not interiors.available(s,who):
            raise ValueError('The required participant cannot attend now: '+who+'.')
        current=scheduled_events.active(s,who)
        if current and current.get('ace_appointment') is not True:raise ValueError('This participant has another active commitment: '+who+'.')
        if venue=='syndicate_hq' and not hidden_cast.hq_access(s,who):raise ValueError('Every attendee needs existing headquarters authorisation.')
    if interior_bookings.participant_conflict(s,guests,now,now+180):
        raise ValueError('A required participant has a conflicting obligation.')
    old=d.get('appointment') or {}
    # Release the preceding professional meeting by normal authorised walking.
    for who in set(old.get('guests',[]))-set(guests):
        if interiors.same_building(s['world']['cast'][who]['location'],'syndicate_hq') and interiors.enabled(s,'syndicate_hq'):
            interiors.walk_actor(s,who,'syndicate_hq__members_lounge')
    event=dict(id='ace-'+uuid.uuid4().hex,title='Mavis campaign appointment',venue=venue,room=target,
               guests=guests,start=now,end=now+180,ace_appointment=True)
    # Validate all travel on a copy before committing the appointment.
    projected=copy.deepcopy(s)
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
    d['appointment']=event
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        elif interiors.enabled(s,venue):interiors.walk_actor(s,who,target)
    return 'Appointment requested. Wait for normal travel and authorised room arrival; no clearance or custody rule is changed.'


def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    if event and who in event['guests'] and event['start']<=now<event['end']:return event
    return None


def exchange_visible(s):
    return s.get('player')=='mavis' and not s.get('interpol',{}).get('custody',{}).get('mavis')


def exchange_access(s,who,destination):
    if who!=s.get('player') or not exchange_visible(s):return False
    d=read(s); index=d.get('chapter',0)
    if index not in OPERATIONS:return False
    part=destination.split('__',1)[-1]
    op=d.get('operations',{}).get(CHAPTER_IDS[index],{})
    if part=='receiving':return True
    if part=='exchange':return bool(op.get('approach'))
    if part=='inner_room':return bool(op.get('contained') if index==10 else op.get('approach'))
    return False


def start_session(s, mission, historical):
    import game_core, combat, combat_profiles, combat_engine
    d=data(s)
    if d['session']: raise ValueError('An encounter is already active.')
    if mission=='MV-F02' and mission in d['memories']: raise ValueError('The predecessor’s death is fixed; this mission cannot reopen.')
    if historical:
        if d['phase']!='memory' or MEMORY_AT.get(d['chapter'])!=mission:
            raise ValueError('This historical mission is not the current mandatory memory.')
    elif d['phase']!='operation' or CHAPTER_IDS[d['chapter']]!=mission or not d['operations'].get(mission,{}).get('objective'):
        raise ValueError('Complete the current operation approach and objective first.')
    if not historical:
        combat.guard(s)
        f=encounter(s,mission,False)
        f['ace_mission']=mission
        d['operations'][mission]['encounter_token']=f['id']
        s['combat']['active']=f
        return
    nested=game_core.fresh('mavis')
    # Fresh mechanics, explicitly bounded cast and no present routes or social history.
    nested['routes']={}; nested['world']['cast']={}; nested['world']['npcs']=[]
    nested['world'].update(location='mavis_dispatch_exchange',minute=480)
    # Exact-era checkpoint kit, built without the present canonical Totality
    # seed, earned profile, role or public epithet. The authorised historical
    # kit uses supported Mist skills without importing present progression.
    p=combat_profiles.make('mavis-age20',dict(awakened=True))
    p.update(name='Mavis · age 20',portrait='mavis-age20',
             trait=dict(zip(('name','description','effect'),combat_profiles.TRAITS['mavis'])),
             basis='Authored age-twenty encounter baseline; numeric balance does not establish historical Path progression.')
    p['stats'].update(awakened_power=55,trait_refinement=60,martial_skill=80,fight_iq=78)
    p['arts']={'Silat':80};p.pop('moveset',None)
    __import__('combat_moves').initialise(p,'mavis')
    p['historical_kit_version']=HISTORICAL_KIT_VERSION
    __import__('historical_combat').strengthen(p,'mavis')
    nested['combat']['profiles']['mavis']=p
    nested['ace_historical_context']=dict(age=20,title='Independent contract operative' if mission=='MV-F02' else 'Provisional Syndicate service')
    f=encounter(nested,mission,historical)
    nested['combat']['active']=f
    token=f['id']
    d['session']=dict(token=token,mission=mission,historical=historical,
                     checkpoint='reconnaissance' if historical else 'confrontation',state=nested,receipt=None)


def encounter(s,mission,historical):
    import combat,combat_profiles,combat_engine
    p=combat_profiles.profile(s,'mavis')
    opponent=combat_profiles.make('ace-authored-operative')
    opponent.update(name={'MV-F02':'Unnamed prior Spade','MV-F04':'Venn','MV-07':'Rusk','MV-11':'Broker'}[mission],
                    combat_id='ace-authored-operative',portrait={'MV-F02':'mavis-previous-spade','MV-F04':'mavis-venn','MV-07':'mavis-rusk','MV-11':'mavis-broker'}[mission],trait=None,awakened=False)
    if historical:
        opponent['historical_reference']='mavis-previous-spade' if mission=='MV-F02' else 'mavis-venn'
        opponent['era']=__import__('ace_campaign_content').MEMORIES[mission]['era']
    opponent['arts']={'Boxing':68}; opponent['stats'].update(martial_skill=68,fight_iq=72)
    if mission=='MV-F02':
        # New encounter baseline only. Never rewrite an active saved fight.
        # Trait=None means unspecified/unmodelled, not canonical absence.
        opponent.update(combat_id='mavis-previous-spade',awakened=True,
                        trait_status='Unspecified; not modelled in this encounter.',
                        basis='Authored prior-Ace encounter balance: Exceptional Veteran power/skill/IQ, supported Totality. Identity and Trait remain unspecified.',
                        encounter_balance_version=2)
        opponent['stats']=dict(awakened_power=78,trait_refinement=0,martial_skill=88,fight_iq=89)
        opponent['arts']={'Boxing':88}
        opponent.pop('path',None)
        __import__('combat_path').initialise(opponent,opponent['combat_id'],stage='Totality')
    opponent.pop('moveset',None)
    token=uuid.uuid4().hex
    f=dict(id=token,kind='ace',opponent=opponent['name'],opponent_profile=opponent,
           location=s['world']['location'],player=combat.resources(p),enemy=combat.resources(opponent),
           elapsed=0,turn=0,log=['Isolated historical checkpoint.' if historical else 'Authored campaign encounter.'],status='active',result=None,
           score=[0,0],seed=int(token[:8],16),path_form_rules=True)
    import interiors
    if historical:
        f['ace_historical']=True
        f['historical_portraits']={'mavis':'mavis-age20',opponent['name']:opponent['portrait']}
    elif interiors.enabled(s):f['room']=interiors.room(s)
    combat_engine.ensure_arena(f)
    return f


def after_combat_close(s,f):
    """Consume an actual live present encounter once, after normal combat costs."""
    mission=f.get('ace_mission')
    if not mission:return
    d=data(s)
    if any(r['token']==f['id'] for r in d['receipts']):return
    if CHAPTER_IDS[min(d['chapter'],11)]!=mission:raise ValueError('This campaign encounter belongs to a different chapter.')
    if d['operations'].get(mission,{}).get('encounter_token')!=f['id']:
        raise ValueError('This result belongs to an expired campaign encounter.')
    won=f['result'].startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    d['receipts'].append(dict(token=f['id'],mission=mission,won=won,result=f['result'],turns=f['turn'],consumed=True))
    op=d['operations'][mission]
    if won:
        op['extracted']=True;op['target_fate']='dead'
        d['evidence'].append(mission+':authenticated-transfer')
        if mission=='MV-11':
            d['broker_removed']=True
            d['archive_outcome']='Authenticated transfer contained; '+('secondary working material lost.' if op.get('secondary_copy_lost') else 'secondary working material recovered, other historical copies remain outside our control.')
        d['phase']='aftermath'
    else:op['objective']=False


def session(s): return read(s).get('session')


def repair_historical_kit(s):
    """Add the authorised age20 abilities to an active saved player kit only.

    Resources, opponent and resolved/pending exchange payloads are untouched.
    Existing entries retain their IDs/data, including a legacy selected amp.
    """
    import combat_moves as moves
    item=session(s)
    if (s.get('player')!='mavis' or not isinstance(item,dict) or not item.get('historical')
            or item.get('mission') not in ('MV-F02','MV-F04')):return False
    nested=item.get('state') or {}
    if nested.get('player')!='mavis' or nested.get('ace_historical_context',{}).get('age')!=20:return False
    root=nested.get('combat') or {};fight=root.get('active') or {};p=root.get('profiles',{}).get('mavis')
    if not p or fight.get('status')!='active' or not fight.get('ace_historical'):return False
    if p.get('combat_id')!='mavis-age20' or (p.get('trait') or {}).get('effect')!='mist':return False
    if p.get('historical_kit_version',0)>=HISTORICAL_KIT_VERSION:return False
    p['stats']['martial_skill']=max(80,p['stats']['martial_skill'])
    p.setdefault('arts',{})['Silat']=max(80,p.get('arts',{}).get('Silat',0))
    book=moves.initialise(p)
    for move in moves.MOVES.values():
        if move['art']=='Silat' and moves.eligible(p,move['tier']) and move['id'] not in book['learned']:
            book['learned'].append(move['id'])
    for field,source in (('unique',moves.UNIQUES['mavis']),('amplifications',moves.AMPLIFICATIONS['mavis'])):
        present={entry['id'] for entry in book[field]}
        for entry in source:
            if entry['id'] not in present:book[field].append(copy.deepcopy(entry));present.add(entry['id'])
    p['historical_kit_version']=HISTORICAL_KIT_VERSION
    return True


def historical_approach(s, token, action):
    item=session(s)
    if not item or token!=item['token']: raise ValueError('This historical session has expired.')
    if item['checkpoint']=='reconnaissance' and action=='observe':
        item['checkpoint']='approach'
        item['observation']='A guarded stair faces the landing. A service passage reaches the same door, but a timed light sweep exposes anyone who waits.'
    elif item['checkpoint']=='approach' and action in ('service','stair'):
        item['approach']=action; item['checkpoint']='authority_case' if item['mission']=='MV-F04' else 'confrontation'
        f=__import__('combat').active(item['state'])
        if action=='stair':
            f['player']['health']=round(f['player']['health']*.85)
            f['log'].append('The guarded stair costs health before the confrontation.')
        else:
            f['player']['energy']=max(0,f['player']['energy']-20)
            f['log'].append('The service passage and timed light sweep cost twenty mana.')
    elif item['checkpoint']=='authority_case' and action=='secure_case':
        item['authority_case_secured']=True;item['checkpoint']='confrontation'
        __import__('combat').active(item['state'])['log'].append('The separate route-authority case is secured before confronting Venn.')
    else: raise ValueError('Complete the saved historical reconnaissance before choosing an approach.')
    return 'Historical objective updated; present resources are unchanged.'


def finish_session(s, token):
    import combat
    d=data(s); item=d['session']
    if not item or item['token']!=token: raise ValueError('This result belongs to a closed encounter or another save.')
    if item['checkpoint']!='confrontation': raise ValueError('Resolve the historical infiltration before the confrontation.')
    if not item.get('historical'):raise ValueError('Present encounters must resolve through normal combat.')
    if item['mission']=='MV-F04' and not item.get('authority_case_secured'):
        raise ValueError('Recover the separate route-authority case before resolving this historical mission.')
    f=combat.active(item['state'])
    if not f or f['id']!=token or f['status']!='finished': raise ValueError('Resolve or concede the actual encounter first.')
    won=f['result'].startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    receipt=dict(token=token,mission=item['mission'],won=won,result=f['result'],turns=f['turn'],consumed=False)
    item['receipt']=receipt
    return receipt


def return_session(s, token):
    d=data(s); item=d['session']
    if not item or token!=item['token']: raise ValueError('This return token has expired.')
    receipt=finish_session(s,token)
    if receipt['won']:
        mission=item['mission']
        if item['historical']:
            if mission not in d['memories']: d['memories'].append(mission)
            if mission=='MV-F02': d['predecessor_dead']=True
            d['pending_return']=mission
        else:
            op=d['operations'][mission]; op['extracted']=True
            d['evidence'].append(mission+':authenticated-transfer')
            if mission=='MV-11':
                d['broker_removed']=True
                d['archive_outcome']='Authenticated transfer contained; secondary copies remain outside our control.'
        receipt['consumed']=True; d['receipts'].append(copy.deepcopy(receipt)); d['phase']='aftermath'
    if not receipt['won'] and not item['historical']:
        d['operations'][item['mission']]['objective']=False
    d['session']=None
    return 'Returned to the present. '+('The resolved outcome is recorded.' if receipt['won'] else 'The mission remains incomplete. Retry the checkpoint from Story.')


def retry_session(s):
    d=data(s); item=d['session']
    if not item or not item.get('receipt') or item['receipt']['won']: raise ValueError('Retry is available after an unsuccessful encounter.')
    mission,historical=item['mission'],item['historical']; d['session']=None
    start_session(s,mission,historical)
    return 'Checkpoint restarted; present resources are unchanged.'


def abandon_session(s, token):
    d=data(s); item=d['session']
    if not item or item['token']!=token: raise ValueError('This return token has expired.')
    if not item['historical']: d['operations'][item['mission']]['objective']=False
    d['session']=None
    return 'Returned safely. The unresolved mission remains available from its checkpoint.'


def action_pages(s, args):
    from ace_campaign_content import (MEMORIES, DISCLOSURES, OUTCOME_VARIANTS,
                                      SUPPORT_SCENES, PRIORITY_SCENES,
                                      APPROACH_SCENES, OBJECTIVE_SCENES, b)
    from campaign_prose import page
    action=args[0]; spec=chapter(s); value=args[1] if len(args)>1 else ''
    chapter_id=CHAPTER_IDS[read(s).get('chapter',0)]
    if action=='historical_return':
        key=read(s)['pending_return']
        return stamp(copy.deepcopy(MEMORIES[key]['after_encounter']),key+'-resolved')
    if action=='confront' and spec.get('confrontation'):
        return stamp(copy.deepcopy(spec['confrontation']),CHAPTER_IDS[read(s)['chapter']]+'-confrontation')
    if action in ('briefing','aftermath'):
        lines=copy.deepcopy(spec[action])
        if action=='aftermath' and read(s).get('chapter')==11:
            variants=['secondary_lost' if any(o.get('secondary_copy_lost') for o in read(s)['operations'].values()) else 'contained']
            if read(s)['exposure']:variants.append('exposed')
            lines=[copy.deepcopy(b) for k in variants for b in OUTCOME_VARIANTS[k]]+lines
        return stamp(lines,CHAPTER_IDS[read(s).get('chapter',0)]+'-'+action)
    if action=='memory':
        key=MEMORY_AT[read(s).get('chapter',0)]
        return stamp(copy.deepcopy(MEMORIES[key]['text']),key)
    if action=='recon' and spec.get('operation_intro'):
        return stamp(copy.deepcopy(spec['operation_intro']),chapter_id+'-recon')
    if action=='approach' and chapter_id in APPROACH_SCENES:
        from ace_campaign_visuals import bind, EXCHANGE, CURRENT
        lines=[b(narration=APPROACH_SCENES[chapter_id][value])]
        bind(lines,chapter_id+':approach:'+value,EXCHANGE,CURRENT|{'mavis':'mavis-syndicate'})
        return stamp(lines,chapter_id+'-approach-'+value)
    if action=='objective' and chapter_id in OBJECTIVE_SCENES:
        return stamp(copy.deepcopy(OBJECTIVE_SCENES[chapter_id]),chapter_id+'-objective')
    if action=='support':
        return stamp(copy.deepcopy(SUPPORT_SCENES[value]),'MV-10-support-'+value)
    if action=='priority':
        return stamp(copy.deepcopy(PRIORITY_SCENES[value]),'MV-10-priority-'+value)
    if action=='disclose':
        who,_,topic=value.partition(':')
        lines=copy.deepcopy(DISCLOSURES[who if topic=='contract' else who+'_private'])
        return stamp(lines,'MV-09-disclose-'+who+'-'+topic)
    text={'recon':'Mavis observes two patrol intervals before committing herself. The direct entrance is monitored; the service route costs time and leaves a secondary copy beyond reach.',
          'approach':'Mavis commits to the '+value+' approach. The recorded exposure and evidence costs will survive extraction.',
          'objective':'The approach reaches the objective. Any protected confrontation must now be resolved in combat before the evidence can be carried out.',
          'disclose':'Mavis chooses what to tell this colleague privately. Required operational facts remain part of the team’s debrief.',
          'support':'The specialist confirms a bounded task. Agreement supplies neither command authority nor a guaranteed rescue.',
          'priority':'Mavis chooses '+value+' as the operation priority. Containment risks secondary working material; retrieval exposes the entry route.',
          'contain':'Camila checks the authenticated chain, Elias holds the cover and Martos confirms the agreed extraction signal. Mavis secures the transfer itself. The Broker and his protection remain unresolved.',
          'confront':'The authenticated transfer is contained. Mavis enters the inner room to confront the Broker. The actual encounter determines whether she can finish this operation.'}[action]
    return [page(text,title=spec['title'])]


def stamp(lines,key):
    for index,b in enumerate(lines):b.setdefault('scene_id',key+'-%02d'%index)
    return lines
