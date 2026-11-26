"""Save-local Takeo campaign, bounded history and resolver-backed objectives."""
import copy
import uuid
import takeo_campaign_content as content

CHAPTER_IDS=tuple(content.CHAPTERS)
MEMORY_IDS=tuple(content.MEMORIES)
CONTACTS=('sylvanis','thirteen','Keisuke Hachimura')
MERIDIAN='takeo_meridian'
TRAVEL=frozenset(('site_01','site_02','site_01_briefing','site_02_briefing',MERIDIAN))

def read(s):return s.get('takeo_campaign',{})
def data(s):
    if s.get('player')!='takeo':raise ValueError('This is Takeo’s personal campaign.')
    d=s.setdefault('takeo_campaign',{})
    for key,value in dict(version=1,chapter=0,phase='briefing',memories=[],completed=[],choices={},receipts=[],session=None,pending_return=None,condition=None,operations={},complete=False).items():d.setdefault(key,copy.deepcopy(value))
    return d
def chapter(s):return content.CHAPTERS[CHAPTER_IDS[min(read(s).get('chapter',0),13)]]
def session(s):return read(s).get('session')
def pending_memory(s):return next((key for key in content.MEMORY_AT.get(read(s).get('chapter',0),()) if key not in read(s).get('memories',[])),None)
def room_target(s):
    d=read(s)
    if d.get('scene_resume'):return d['scene_resume']['beats'][d['scene_resume']['cursor']]['room']
    if d.get('scene_room'):return d['scene_room']
    if d.get('chapter')==12 and d.get('phase')=='tasks':return content.ARCHIVE if d.get('operations',{}).get('finale',{}).get('wave',0)>=2 else content.ENTRY
    if d.get('chapter')==13 and d.get('phase')=='aftermath':return content.HQ
    return chapter(s)['room']
def destination(s):return room_target(s).split('__')[0]
def travel_allowed(s,who,destination):return s.get('player')=='takeo' and who=='takeo' and destination in TRAVEL

def seed(s):
    """New games only; loading never recreates contacts, funds or progress."""
    for who,record in s['discoveries'].items():record.update(met=who in (*CONTACTS,'takeo'),contact=who in CONTACTS,home=who=='takeo')
    for who in CONTACTS:
        stats=s['friendships'].get(who,s['relationships'].get(who))
        if stats:stats.update(trust=45,closeness=10,status='command contact' if who!='sylvanis' else 'commercial counterpart')
    s['active']='thirteen';s.pop('grove_account',None);data(s)
    s.setdefault('npc_chats',{})['Keisuke Hachimura']=dict(history=[],connection=dict(status='command liaison',trust=45,closeness=10),shinokami_introduced=True)

def required_cast(s,action=None,value=''):
    if action not in (None,'briefing','aftermath','resume','task'):return []
    d=read(s);field=d.get('phase','briefing')
    if field=='tasks' and d.get('chapter') in TASK_TEXT and d.get('chapter')!=4:field='briefing'
    lines=d['scene_resume']['beats'][d['scene_resume']['cursor']:] if d.get('scene_resume') else chapter(s).get(field,[])[d.get('scene_cursor',0):]
    return sorted({who for beat in lines if beat.get('room',chapter(s)['room'])==room_target(s) for who,_ in beat.get('speeches',[]) if who in CONTACTS})

def local_here(s):
    event=read(s).get('local_appointment',{})
    return event.get('room')==room_target(s) and event.get('arrival',10**12)<=s['world']['minute']<event.get('end',0)

def permitted_cast(s):
    """Keep this chapter's same-room collaborators welcome when they fall silent."""
    spec=chapter(s);target=room_target(s)
    return {who for phase in ('briefing','aftermath') for beat in spec.get(phase,[])
            if beat.get('room',spec['room'])==target
            for who,_ in beat.get('speeches',[]) if who in CONTACTS}

def finish_local(s):
    if s.get('player')!='takeo' or s.get('campaign_dialogue') or session(s) or s.get('flashback_visit'):raise ValueError('Finish the current conversation first.')
    data(s).pop('local_appointment',None)
    return 'Keisuke leaves the completed command appointment.'

def finish_supplier(s):
    """End the player's bounded appointment through ordinary NPC travel."""
    import combat, world_loop
    if (s.get('player')!='takeo' or s.get('campaign_dialogue') or session(s)
            or s.get('flashback_visit') or combat.active(s)):
        raise ValueError('Finish the current scene or encounter first.')
    if 'sylvanis' not in read(s).get('appointment',{}).get('guests',[]):
        raise ValueError('No supplier appointment is active.')
    projected=copy.deepcopy(s)
    data(projected).pop('appointment',None)
    world_loop.start_trip(projected,'sylvanis','glasshouse_lab')
    data(s).pop('appointment',None)
    world_loop.start_trip(s,'sylvanis','glasshouse_lab')
    return 'The supplier appointment ends. Sylvanis returns to Glasshouse through normal travel.'

def appointment_access(s,who,venue):
    event=read(s).get('appointment',{});now=s.get('world',{}).get('minute',0)
    return s.get('player')=='takeo' and who=='sylvanis' and venue=='site_01' and event.get('venue')==venue and who in event.get('guests',[]) and event.get('start',1)<=now<event.get('end',0) and not availability(s)

def availability(s):
    for who in ('takeo',*CONTACTS):
        if s.get('interpol',{}).get('custody',{}).get(who):return 'Saved custody prevents this command scene; no authored custody adaptation is available.'
    return ''

def knowledge(s,who,listeners):
    if not s or s.get('player')!='takeo' or not set(listeners)<={'takeo',who}:return ''
    d=read(s);parts=[]
    if who=='thirteen' and d.get('priority'):parts.append('Takeo gave one feasible order: preserve the regional force, not three incompatible positions. Thirteen retains existing US command and does not become a replacement One.')
    if who=='sylvanis' and d.get('dependency_verified'):parts.append('Takeo has examined the actual service dependencies. Your commercial bargain never made you subordinate. Do not disclose the Crow’s unobserved private planning.')
    if d.get('complete') and who in ('takeo','thirteen','sylvanis','Keisuke Hachimura'):
        parts.append('AUTHORITATIVE completed Takeo-save outcome, superseding baseline future-tense descriptions for this private conversation only: the local Meridian takeover is repelled; Takeo personally destroyed the unique experimental archive, without a complete backup. Pacific Relay and Thirteen’s regional command survive. The UN deputy withdrew alive with observations, without the programme archive. This resolves this site, not a worldwide war or other protagonist campaign.')
        if who in ('takeo','Keisuke Hachimura'):parts.append('Keisuke remains liaison/enforcer under countersigned reporting and narrower discretion. No retroactive recruit progression or new promotion.')
        if who=='sylvanis':parts.append('The failed agreement is closed; only separately priced, limited future business remains. You remain amused, autonomous and evil.')
    return ' '.join(parts)
def validate(s,action=None,value=''):
    import combat,interiors,interior_activities
    if s.get('player')!='takeo':raise ValueError('This is Takeo’s personal campaign.')
    d=read(s)
    if availability(s):raise ValueError(availability(s))
    if d.get('complete'):raise ValueError('Empire of One is complete.')
    if d.get('session') or s.get('flashback_visit'):raise ValueError('Return from history first.')
    if combat.active(s) or combat.recovering(s):raise ValueError('Finish combat and recover first.')
    if s.get('campaign_dialogue'):raise ValueError('Finish the current conversation first.')
    if interiors.building(s['world']['location'])!=destination(s):raise ValueError('Travel through Maps to the chapter objective first.')
    if room_target(s) in interiors.ROOMS:interior_activities.require(s,room_target(s))
    if s['world']['cast']['takeo'].get('journey'):raise ValueError('Wait for actual arrival first.')
    for who in required_cast(s,action,value):
        if who=='Keisuke Hachimura':
            if not local_here(s):raise ValueError('Arrange Keisuke’s bounded command appointment and wait for arrival.')
            continue
        actor=s['world']['cast'][who]
        same=interiors.same_room(s,'takeo',who) if room_target(s) in interiors.ROOMS else actor['location']==destination(s)
        if actor.get('journey') or not same or not interiors.available(s,who) or combat.recovering(s,who):raise ValueError('A required participant has not arrived or is unavailable: '+who)
    if action in (None,'briefing','aftermath','resume','task'):
        present=set(interiors.occupants(s,room_target(s))) if room_target(s) in interiors.ROOMS else {who for who,actor in s['world']['cast'].items() if actor['location']==destination(s) and not actor.get('journey')}
        if local_here(s):present.add('Keisuke Hachimura')
        if present-{'takeo',*required_cast(s,action,value),*permitted_cast(s)}:raise ValueError('Use the private command scene without unrelated listeners.')

def request_appointment(s,recipient=''):
    import combat,scheduled_events,world_loop,interiors,interior_bookings
    d=data(s);guests=[recipient] if recipient in ('sylvanis','Keisuke Hachimura') else required_cast(s)
    guests=[who for who in guests if who!='thirteen']
    if not guests:raise ValueError('Thirteen remains at Pacific Relay; travel there for his command meeting.')
    if availability(s):raise ValueError(availability(s))
    if d['session'] or s.get('campaign_dialogue') or s.get('flashback_visit') or combat.active(s):raise ValueError('Finish the current scene first.')
    venue=destination(s);now=s['world']['minute'];target=room_target(s)
    local='Keisuke Hachimura' in guests
    guests=[who for who in guests if who!='Keisuke Hachimura']
    if local and not guests:
        d['local_appointment']=dict(room=target,arrival=now+20,end=now+200)
        return 'Keisuke acknowledges the bounded command appointment. Allow twenty minutes for arrival.'
    if venue!='site_01':raise ValueError('These private appointments are at Kestrel only.')
    for who in guests:
        other=scheduled_events.active(s,who)
        if combat.recovering(s,who) or not interiors.available(s,who) or other and not other.get('takeo_appointment'):raise ValueError('A participant has another commitment: '+who)
    if interior_bookings.participant_conflict(s,guests,now,now+180):raise ValueError('A participant has another obligation.')
    event=dict(id='takeo-'+uuid.uuid4().hex,title='Takeo command appointment',venue=venue,room=target,guests=guests,start=now,end=now+180,takeo_appointment=True)
    projected=copy.deepcopy(s);data(projected)['appointment']=event
    for who in guests:
        if projected['world']['cast'][who]['location']!=venue:world_loop.start_trip(projected,who,venue)
    d['appointment']=event
    if local:d['local_appointment']=dict(room=target,arrival=now+20,end=now+200)
    for who in guests:
        if s['world']['cast'][who]['location']!=venue:world_loop.start_trip(s,who,venue)
        elif target in interiors.ROOMS:interiors.walk_actor(s,who,target)
    return 'Accepted bounded command appointment. Wait for normal travel and actual arrival.'
def npc_appointment(s,who,now):
    event=read(s).get('appointment')
    return event if event and who in event['guests'] and event['start']<=now<event['end'] else None

def condition(s):
    import combat,combat_profiles
    base=combat.resources(combat_profiles.profile(s,'takeo'));saved=read(s).get('condition')
    if not saved:return base
    result=copy.deepcopy(saved['resources']);elapsed=max(0,s['world']['minute']-saved['minute'])
    for key,rate,maximum in (('health',.25,'max_health'),('energy',.5,'max_energy'),('stamina',1,None)):result[key]=min(base[maximum] if maximum else 100,result[key]+int(elapsed*rate))
    return result

def start_session(s,memory):
    validate(s,'memory');d=data(s)
    if d['phase']!='memory' or pending_memory(s)!=memory:raise ValueError('This is not the current mandatory memory.')
    d['session']=dict(token=uuid.uuid4().hex,mission=memory,cursor=0,events=[])
    return 'Entered an isolated historical recollection. The present is paused.'
def memory_step(s,token,choice):
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if choice not in ('observe','context') or item['cursor']!=0:raise ValueError('Choose an offered observation once.')
    item['events'].append('Observed the remembered consequence.' if choice=='observe' else 'Kept the period’s limited knowledge distinct from the present.');item['cursor']=1
    return item['events'][-1]
def return_session(s,token):
    d=data(s);item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if item['cursor']!=1:raise ValueError('Complete the remembered observation or return safely.')
    d['memories'].append(item['mission']);d['receipts'].append(dict(token=token,kind='memory',mission=item['mission'],events=copy.deepcopy(item['events'])))
    d['pending_return']=item['mission'];d['session']=None;d['phase']='memory' if pending_memory(s) else 'tasks'
    return 'Returned without changing present time, resources, cast or social knowledge.'
def abandon_session(s,token):
    d=data(s)
    if not d['session'] or d['session']['token']!=token:raise ValueError('This historical session has expired.')
    d['session']=None;return 'Returned safely; the recollection remains incomplete.'

def encounter(s,mission,wave=0):
    import combat,combat_profiles
    token=uuid.uuid4().hex
    names={'breach':'Meridian barricade squad','supply':'Syndicate service interception','finale':('Meridian entry resistance','Syndicate local seizure team','UN archive perimeter team')[wave]}
    q=combat_profiles.make('takeo-opposition',dict(awakened=False));q.update(name=names[mission],combat_id='takeo-opposition',portrait='takeo-opposition',trait=None,awakened=False,basis='Trained tactical resistance; objectives and routes matter. No invented equal to Takeo or Nanoengine counter.')
    q['stats'].update(awakened_power=0,trait_refinement=0,martial_skill=65,fight_iq=72);q['arts']={'Military CQC':65};q.pop('moveset',None)
    resources=condition(s)
    if resources['health']<=0:raise ValueError('Recover before retrying the checkpoint.')
    return dict(id=token,kind='takeo_campaign',display_kind='TAKEO · EMPIRE OF ONE',opponent=q['name'],opponent_profile=q,location=s['world']['location'],room=room_target(s),location_label='Meridian complex',player=resources,enemy=combat.resources(q),elapsed=0,turn=0,log=['Clear real resistance; strength alone does not preserve an absent command or deny an archive.'],status='active',result=None,score=[0,0],seed=int(token[:8],16),path_form_rules=True,takeo_mission=mission,takeo_wave=wave,contextual_portraits={'takeo':'combat/takeo',q['name']:'takeo-opposition'})

def after_combat_close(s,f):
    if not f.get('takeo_mission'):return
    d=data(s)
    if any(row['token']==f['id'] for row in d['receipts']):return
    mission=f['takeo_mission'];op=d['operations'].get(mission,{})
    if op.get('encounter_token')!=f['id'] or d['chapter']!={'breach':1,'supply':10,'finale':12}[mission]:raise ValueError('This encounter belongs to an expired operation.')
    won=bool(f.get('exchanges')) and f.get('status')=='finished' and (f.get('result') or '').startswith('Victory') and f['enemy']['health']<=0 and f['player']['health']>0
    d['receipts'].append(dict(token=f['id'],kind='combat',mission=mission,wave=f['takeo_wave'],won=won,exchanges=[row['id'] for row in f.get('exchanges',[])]));d['condition']=dict(resources=copy.deepcopy(f['player']),minute=s['world']['minute'])
    if won:
        if mission=='finale':op['wave']=op.get('wave',0)+1
        else:op['secured']=True
    else:op['failed_attempts']=op.get('failed_attempts',0)+1
    op.pop('encounter_token',None)

TASK_TEXT={0:'The Meridian objective is entered against an existing Pacific Relay foothold.',2:'The delivery terms are bounded commercial obligations, not command over Sylvanis.',3:'The observed research forecast replaces the unsupported replication promise. The unique archive has no complete backup.',4:'Transport priority is entered against the available capacity.',5:'The private designation index is closed without a name or address for One.',6:'The corrected withdrawal report preserves the functioning unit and records the earlier deception.',7:'The independently checked service ledger identifies the outside dependencies.',8:'Arakawa’s authenticated UN demand is retained separately from the Syndicate instructions.',9:'Keisuke’s discretion is restricted; adverse reports must reach command under countersignature.',11:'Thirteen receives one feasible order: preserve the regional force. Takeo will deny the archive.'}

def commit_command(d,i,value=''):
    """Commit a narrated decision once; the transport branch stays player-chosen."""
    if i==4 and value not in ('personnel','equipment'):
        raise ValueError('Choose an offered transport priority.')
    if i==11 and (not d.get('archive_unique') or not d.get('dependency_verified') or not d['operations'].get('supply',{}).get('secured')):
        raise ValueError('Establish the archive constraint, dependency and actual supply result first.')
    if i==4:
        d['choices']['transport']=value
        d['choices']['transfer_cost']='laboratory equipment left behind' if value=='personnel' else 'two vehicle sections abandoned during withdrawal'
    if i==3:d['archive_unique']=True
    if i==7:d['dependency_verified']=True
    if i==9:d['keisuke_supervised']=True
    if i==11:d.update(priority='regional_command',replication_transfer_cancelled=True)
    d['receipts'].append(dict(token=uuid.uuid4().hex,kind='command',chapter=CHAPTER_IDS[i],value=value))
    d['phase']='aftermath'

def enter_story_phase(d,phase):
    # A non-choice decision is already spoken in the scene. Reading its final
    # page commits it; there is no second report/confirmation action to click.
    i=d['chapter']
    if phase=='tasks' and i in TASK_TEXT and i!=4:commit_command(d,i)
    else:d['phase']=phase

def finish_legacy_memory(s,token):
    """Resume old saved observation sessions without another filler choice."""
    item=session(s)
    if not item or item['token']!=token:raise ValueError('This historical session has expired.')
    if item['cursor']==0:memory_step(s,token,'observe')
    return return_session(s,token)

def perform_action(s,action,value=''):
    validate(s,action,value);d=data(s);i=d['chapter']
    if d['pending_return'] and action!='historical_return':raise ValueError('Read the historical return first.')
    if action=='briefing':
        if d['phase']!='briefing':raise ValueError('This briefing is already recorded.')
        enter_story_phase(d,'memory' if pending_memory(s) else 'tasks' if i!=13 else 'aftermath')
    elif action=='memory':return start_session(s,pending_memory(s))
    elif action=='recollection':
        memory=pending_memory(s)
        if d['phase']!='memory' or not memory:raise ValueError('This is not the current mandatory memory.')
        # The reader commits only after its final historical/return page. No
        # live-world state changes, observation minigame or journal checkbox.
        d['memories'].append(memory)
        d['receipts'].append(dict(token=uuid.uuid4().hex,kind='memory',mission=memory,events=['Read the complete recollection.']))
        enter_story_phase(d,'memory' if pending_memory(s) else 'tasks')
    elif action=='historical_return':
        if not d['pending_return']:raise ValueError('No historical return is waiting.')
        enter_story_phase(d,'memory' if pending_memory(s) else 'tasks')
        d['pending_return']=None
    elif action=='task':
        if d['phase']!='tasks' or i not in TASK_TEXT:raise ValueError('This command objective is unavailable.')
        commit_command(d,i,value)
    elif action=='objective':
        import combat
        if d['phase']!='tasks' or i not in (1,10,12):raise ValueError('This encounter is unavailable.')
        mission={1:'breach',10:'supply',12:'finale'}[i];op=d['operations'].setdefault(mission,{})
        if op.get('secured') or mission=='finale' and op.get('wave',0)>=3:raise ValueError('This checkpoint is already secured.')
        if mission=='finale' and op.get('wave',0)==2 and not op.get('preserved'):raise ValueError('Commit the cleared preservation route before entering the archive perimeter.')
        f=encounter(s,mission,op.get('wave',0));__import__('combat_engine').ensure_arena(f);op['encounter_token']=f['id'];combat.ensure(s)['active']=f
        return 'Actual resistance started; loss preserves the checkpoint for retry.'
    elif action=='confirm_objective':
        if d['phase']!='tasks' or i not in (1,10) or not d['operations'].get({1:'breach',10:'supply'}[i],{}).get('secured'):raise ValueError('Win the actual encounter first.')
        d['phase']='aftermath'
    elif action=='preserve':
        op=d['operations'].get('finale',{})
        if i!=12 or d['phase']!='tasks' or op.get('wave')!=2 or op.get('preserved') or d.get('priority')!='regional_command' or not d.get('replication_transfer_cancelled'):raise ValueError('Clear the first two checkpoints and commit the feasible preservation order first.')
        op['preserved']=dict(token=uuid.uuid4().hex,bridgehead=True,commander='thirteen',cost=d['choices'].get('transfer_cost'))
    elif action=='destroy':
        op=d['operations'].get('finale',{})
        if i!=12 or d['phase']!='tasks' or op.get('wave')!=3 or not op.get('preserved') or op.get('archive_destroyed') or not d.get('archive_unique'):raise ValueError('Preserve the command and clear the real archive perimeter first.')
        op['archive_destroyed']=dict(token=uuid.uuid4().hex,actor='takeo',custody='destroyed',backup=False);op['local_takeover']='repelled';op['un_outcome']='deputy withdrew alive with observations, without programme archive';d['phase']='aftermath'
    elif action=='aftermath':
        if d['phase']!='aftermath':raise ValueError('Complete the actual chapter objectives first.')
        if i==13 and (set(d['memories'])!=set(MEMORY_IDS) or not d['operations'].get('finale',{}).get('archive_destroyed') or not d['operations']['finale'].get('preserved')):raise ValueError('All eight memories, preserved command and personal archive destruction are required.')
        d['completed'].append(CHAPTER_IDS[i]);d['chapter']+=1;d['phase']='briefing';d['complete']=d['chapter']==14
        if d['complete']:d['ending']='empire_of_one'
    else:raise ValueError('Unknown Takeo action.')
    d.pop('scene_room',None)
    d.pop('scene_cursor',None)
    return 'Takeo’s campaign record updated.'

def action_pages(s,args):
    action=args[0];d=read(s);key=CHAPTER_IDS[min(d.get('chapter',0),13)]
    if action in ('briefing','aftermath'):lines=content.copy_scene(key,action)
    elif action in ('memory','recollection'):
        key=pending_memory(s);lines=content.copy_scene(key,'text')
    elif action=='historical_return':lines=copy.deepcopy(content.RETURNS[d['pending_return']])
    elif action=='task':
        if d['chapter']==4:
            lines=[content.p({'personnel':'Takeo gives the personnel priority. Men climb into the vehicles while laboratory equipment remains beneath its covers. The programme will have less to work with; the regional force will have more people available to carry out its orders. He watches the first load leave without describing the decision as mercy.', 'equipment':'Takeo assigns the heavy transport to equipment. The revised movement leaves two vehicle sections without a place in the later withdrawal. He reads the consequence before signing. The equipment is valuable to the programme he intends to build, and he is willing to spend part of his force’s transport capacity to carry it.'}[args[1]])]
        else:
            # Old saves can stop on the former task phase. Give them the same
            # authored decision, without an empty journal/recording page.
            lines=content.copy_scene(key,'briefing')
    elif action=='confirm_objective':lines=[content.p('The road is open. Takeo waits until the first vehicle has crossed the cleared approach before accepting the report. The men following it now have somewhere to go; a declaration of victory would not have given them that.')]
    elif action=='preserve':lines=[content.p('Takeo confirms the independent route. Thirteen brings his surviving command through it. The cancelled replication transfer cannot be restored without undoing the movement now under way.')]
    elif action=='destroy':lines=[content.b('takeo-deputy','The men on that route are leaving because you gave up the transfer. You could have named that objective earlier.'),content.b('takeo','You came for the programme. You will leave without it.'),content.p('Arakawa watches from the cleared exit. His team cannot take the cabinet without crossing Mishima; its evacuation order is already running. Takeo drives nanomachine-hardened fingers through the archive housing and tears the storage assembly apart. The bridgehead and Thirteen’s command survive. The immediate replication project does not.')]
    else:raise ValueError('No reading page for this action.')
    if action=='aftermath' and d.get('chapter')==13:
        lines.insert(0,content.p('The final withdrawal ledger records the material cost: '+d['choices'].get('transfer_cost','the cancelled replication transfer')+'.'))
    visuals=__import__('takeo_campaign_visuals')
    lines=visuals.bind(lines,key,action,room_target(s),memory=action in ('memory','recollection'))
    if action=='recollection':
        lines+=visuals.bind(copy.deepcopy(content.RETURNS[key]),CHAPTER_IDS[d['chapter']],'historical_return',room_target(s))
    return lines
def pause_for_room(s,dialogue,next_cursor):
    target=dialogue['beats'][next_cursor].get('room')
    if not target or dialogue['beats'][next_cursor].get('mode')=='memory' or __import__('interiors').same_building(target,s['world']['location']) and (target not in __import__('interiors').ROOMS or target==__import__('interiors').room(s)):return False
    d=data(s);d['scene_room']=target;d['scene_cursor']=next_cursor;d['scene_resume']=copy.deepcopy(dialogue);d['scene_resume']['cursor']=next_cursor;s['campaign_dialogue']=None;return True
def resume_scene(s):
    validate(s,'resume');d=data(s)
    if not d.get('scene_resume'):raise ValueError('No saved scene is waiting.')
    people=required_cast(s);s['campaign_dialogue']=d.pop('scene_resume');s['campaign_dialogue'].update(venue=s['world']['location'],social_cast=people);return 'Resumed the saved in-person scene.'
