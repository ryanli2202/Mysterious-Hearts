"""Deterministic game-clock needs and persistent intentions; no background AI calls."""
import hashlib
import itertools

ACTIVITIES = {'emily':'flowers and quiet conversation', 'sophie':'post-training food',
              'april':'chess and thoughtful conversation', 'amy':'sketching together',
              'minsu':'food and a study break', 'rei':'painting and cooking',
              'garrett':'trying a new recipe', 'valentina':'sailing stories over tea',
              'samantha':'a break after training'}


def chance(*parts):
    return int(hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:8], 16) / 0xffffffff


def ensure(s):
    a = s.setdefault('autonomy', {'version': 1, 'people': {}, 'offers': [], 'encounters': {}, 'events': []})
    if a.get('seeded_bonds') and a['people'].keys() >= s['world']['cast'].keys(): return a
    for who in s['world']['cast']:
        # Authored gameplay schedules, editable independently of character canon.
        bed, wake = {'sophie': (22, 6), 'emily': (22, 7), 'samantha': (0, 9),
                     'rei': (0, 8), 'garrett': (0, 8), 'april': (0, 8),
                     'ivan': (1, 9)}.get(who, (23, 8))
        a['people'].setdefault(who, dict(energy=80., social=75., happiness=65.,
            bedtime=bed*60, wake=wake*60, plan=None, next_decision=s['world']['minute']+15,
            next_initiation=s['world']['minute']+60, unanswered=0, preferences={},
            relationships={}, sleep_until=None, last_event=None))
    if not a.get('seeded_bonds'):
        for key,bond in s.get('bond_details',{}).items():
            first,second=key.split(':')
            for who,other in ((first,second),(second,first)):
                a['people'][who]['relationships'].setdefault(other,dict(interest=bond['closeness'],closeness=bond['closeness'],trust=bond['trust'],tension=bond['tension']))
        a['seeded_bonds']=True
    # New authored colleagues also gain reciprocal peer recognition in older saves.
    import world_loop
    for key in world_loop.ACE_BONDS:
        first, second = key.split(':')
        bond = s.get('bond_details', {}).get(key)
        if bond:
            for who, other in ((first, second), (second, first)):
                a['people'][who]['relationships'].setdefault(other, dict(
                    interest=bond['closeness'], closeness=bond['closeness'],
                    trust=bond['trust'], tension=bond['tension']))
    return a


def person(s, who):
    if who in s.get('autonomy',{}).get('people',{}): return s['autonomy']['people'][who]
    return ensure(s)['people'][who]


def sleep_window(s, who):
    p = person(s, who); t = s['world']['minute'] % 1440
    return (t >= p['bedtime'] or t < p['wake']) if p['bedtime'] > p['wake'] else p['bedtime'] <= t < p['wake']


def status(s, who):
    if __import__('combat').recovering(s,who): return 'Recovering from knockout'
    import world_loop as loop
    p = person(s, who); actor = s['world']['cast'][who]; now = s['world']['minute']
    if actor['journey']: return 'Travelling'
    if p.get('sleep_until') and now < p['sleep_until']: return 'Asleep'
    if actor['activity'] == 'Sleep' and who!=s['player']: return 'Asleep'
    if actor['activity'] == 'Winding down': return 'Winding down'
    if who == s['player']:
        group=s.get('groups',{}).get(s.get('active_group'),{})
        if s['world']['party'] or group.get('open') and group.get('channel')!='text': return 'Socialising'
        return 'At home' if actor['location'] == loop.HOUSES[who][0] else 'Free time'
    if p.get('plan') and p['plan']['kind'] in ('visit', 'social', 'overnight') and p['plan'].get('accepted',True): return 'Socialising'
    if who in s['world']['party']: return 'Socialising'
    import faction_work
    shift=faction_work.appointment(who,now)
    if shift and actor['location']==shift[1] and actor['activity']==shift[2]: return 'At work / studying'
    if any(x in actor['activity'].lower() for x in ('shift','class','lecture','study','research','running','modelling','recording','business','rehearsal','workshop','training','practice','sparring','vocals','personal project','choosing opponents','reviewing fight reports')): return 'At work / studying'
    if actor['location'] == loop.HOUSES[who][0]: return 'At home'
    return 'Free time'


def record(s, text, owners, kind='experience'):
    import memory_store
    a=ensure(s); now=s['world']['minute']
    a['events'].append(dict(minute=now, text=text, owners=list(owners)))
    a['serial']=a.get('serial',0)+1
    a['events']=a['events'][-150:]
    memory_store.add(s, source='autonomy:'+str(a['serial']),
                     text=text, owners=list(owners), minute=now, importance=3)


def social_encounter(s, first, second, location):
    """Small disagreements can be repaired; serious existing harm never decays here."""
    now=s['world']['minute']; people=[person(s,w) for w in (first,second)]
    ties=[p['relationships'].setdefault(other,dict(interest=15.,trust=10.,closeness=0.,tension=0.))
          for p,other in zip(people,(second,first))]
    prior=next((b for pair,b in s['bond_details'].items() if set(pair.split(':'))=={first,second}),None)
    for tie in ties:
        if prior: tie['tension']=max(tie['tension'],prior['tension'])
    if any(t['tension'] for t in ties):
        text=f'{first} and {second} crossed paths at {location}. Their existing tension remains unresolved.'
    elif any(t.get('minor_tension',0) for t in ties) and chance(first,second,now//1440,'repair')<.5:
        for p,t in zip(people,ties):
            t['minor_tension']=0; t['trust']=min(100,t['trust']+1); p['happiness']=min(100,p['happiness']+2)
        text=f'{first} and {second} talked through a small disagreement about their outing plans at {location}.'
    elif min(t['closeness'] for t in ties)>=6 and min(p['social'] for p in people)<35 and chance(first,second,now//1440,'disagreement')<.10:
        for p,t in zip(people,ties):
            t['minor_tension']=min(6,t.get('minor_tension',0)+2); t['trust']=max(0,t['trust']-1); p['happiness']=max(0,p['happiness']-2)
        text=f'{first} and {second} disagreed over how much time to spend together at {location}; they need a quieter conversation later.'
    else:
        for who,t in zip((first,second),ties):
            t['interest']=min(100,t['interest']+1+chance(who,now,'interest')*3)
            t['closeness']=min(100,t['closeness']+2); t['trust']=min(100,t['trust']+1)
        text=f'{first} and {second} talked at {location} and became better acquainted.'
    record(s,text,[first,second])


def request(s, who, kind, reason, venue=None):
    import world_loop as loop
    a=ensure(s); now=s['world']['minute']
    if any(o['who']==who and o['state']=='pending' for o in a['offers']): return
    offer=dict(id=max([o['id'] for o in a['offers']], default=0)+1, who=who, kind=kind,
               reason=reason, venue=venue or s['world']['location'], minute=now,
               expires=now+90, state='pending')
    if kind=='hangout' and chance(who,now,'bring_friend')<.2:
        peers=[other for other,tie in person(s,who)['relationships'].items() if other!=s['player'] and tie['closeness']>=15 and status(s,other) in ('Free time','At home') and not person(s,other)['plan']]
        if peers:
            offer['guests']=[max(peers,key=lambda other:person(s,who)['relationships'][other]['interest'])]
            reason+=' Ask whether your friend '+offer['guests'][0]+' can join; their attendance requires the player accepting this group invitation.'
            offer['reason']=reason
    a['offers'].append(offer)
    a['offers']=a['offers'][-80:]
    import messaging
    messaging.initiate(s, who, reason, offer=offer['id'])
    loop.event(s, who.title()+' has a '+kind+' invitation. Open Life & availability to respond.')
    return offer


def respond(s, identifier, decision):
    import world_loop as loop
    import town
    offer=next(o for o in ensure(s)['offers'] if o['id']==identifier)
    if offer['state']!='pending' or offer['expires'] < s['world']['minute']: raise ValueError('This invitation has expired.')
    who=offer['who']; p=person(s, who); now=s['world']['minute']
    if decision not in ('accept','decline','later'): raise ValueError('Choose accept, decline or later.')
    if decision=='later':
        offer['state']='rescheduled'; p['next_initiation']=now+180
        record(s, 'The player asked '+who+' to check back later; no meeting was promised.', [s['player'],who]); return
    if decision=='decline':
        offer['state']='declined'; p['next_initiation']=now+240
        if p.get('plan',{} ) and p['plan']['kind']=='visit': p['plan']['until']=now
        record(s, 'The player declined this invitation from '+who+' without ending their friendship.', [s['player'],who]); return
    if offer['kind']=='overnight':
        if not loop.together(s,who) or s['world']['location']!=loop.HOUSES[s['player']][0]: raise ValueError('You must both be at your home to agree a stay.')
        until=now+(p['wake']-now%1440)%1440+60
        p['plan']=dict(kind='overnight', venue=s['world']['location'], until=until, target=s['player'])
        record(s, who+' accepted a separate sleeping place at the player’s home. This is a platonic overnight stay, not consent to intimacy.',[who,s['player']])
    else:
        if sleep_window(s,who) or status(s,who) in ('Asleep','At work / studying'): raise ValueError('They are no longer available. Ask again later.')
        p['plan']=dict(kind='visit', venue=offer['venue'], until=now+120, target=s['player'], accepted=True)
        for guest in offer.get('guests',[]):
            if status(s,guest) in ('Free time','At home') and not person(s,guest)['plan']:
                person(s,guest)['plan']=dict(kind='social',venue=offer['venue'],until=now+120,target=who,activity='an agreed group introduction',introduce_to_player=True)
        if not s['world']['cast'][who]['journey'] and s['world']['cast'][who]['location']!=offer['venue']:
            loop.start_trip(s,who,offer['venue'])
        if loop.together(s,who): town.meet(s,who)
        record(s, 'Agreed to meet '+who+' at '+town.LOCATIONS[offer['venue']]+'. Attendance is not yet established.',[s['player'],who])
    offer['state']='accepted'


def control(s, who):
    """Called each game minute before ordinary routines. True reserves this actor."""
    import world_loop as loop
    import dating
    p=person(s,who); actor=s['world']['cast'][who]; now=s['world']['minute']; plan=p['plan']
    if who==s['player']: return False
    if actor['journey']: return False
    hour,destination,activity=loop.appointment(who,now)
    if plan and now%1440==hour*60 and destination!=loop.HOUSES[who][0] and any(word in activity.lower() for word in ('shift','class','lecture','modelling','recording','business','rehearsal','training','running','vocals','choosing opponents','reviewing fight reports')):
        p['plan']=None
        if who in s['world']['party']: s['world']['party'].remove(who)
        actor.pop('waiting_for_hangout',None)
        return False
    managed_visit=bool(plan and plan['kind'] in ('visit','overnight') and plan.get('accepted',True))
    if not managed_visit and not sleep_window(s,who) and (dating.in_hangout(s,who) or who in s['world']['party'] or actor.get('waiting_for_hangout')):
        p['plan']=None
        return False
    if not managed_visit and not sleep_window(s,who) and s['routes'][who].get('channel')=='in_person':
        p['plan']=None
        return False
    if plan and now>=plan['until']:
        if plan['kind']=='overnight':
            record(s,who+' finished an overnight visit and is preparing to leave.',[who,s['player']])
        if plan['kind'] in ('visit','overnight'):
            if who in s['world']['party']: s['world']['party'].remove(who)
            p['plan']=None
            destination=loop.appointment(who,now)[1]
            if destination==actor['location']: destination=loop.HOUSES[who][0]
            if destination!=actor['location']: loop.start_trip(s,who,destination)
            actor['activity']=activity if destination==loop.appointment(who,now)[1] else 'Quiet recovery'
            return True
        p['plan']=None; plan=None
        p['next_decision']=now+30
    if plan:
        import weather
        import leisure
        if plan['venue'] in leisure.OUTDOORS and weather.shelter(now):
            shelter=leisure.social_destination(s,who,plan.get('target'),indoor=True)
            if plan['kind'] in ('social','project'):
                plan['venue']=shelter
                plan['activity']=leisure.ACTIVITIES[shelter]
                other=person(s,plan['target']).get('plan')
                if other and other.get('target')==who:
                    other.update(venue=shelter,activity=leisure.ACTIVITIES[shelter])
                record(s,who+' moved their planned outdoor activity indoors to '+shelter.replace('_',' ')+'.',[who])
            elif plan['kind']=='visit' and plan.get('accepted') and not plan.get('weather_proposal'):
                plan['weather_proposal']=True
                request(s,who,'hangout','Propose moving this outdoor outing indoors because of rain; keep the existing plan unless the player accepts.',shelter)
        if actor['location'] != plan['venue']:
            loop.start_trip(s,who,plan['venue'])
        if plan['kind']=='overnight':
            actor['activity']='Sleep' if sleep_window(s,who) else 'Breakfast and preparing to leave'
            return True
        if plan['kind']=='rest':
            actor['activity']='Quiet recovery'
            return True
        if plan['kind']=='project':
            actor['activity']='Working on a personal project'
            return True
        if plan['kind']=='visit' and not plan.get('accepted',True):
            actor['activity']='Waiting outside'
            if not any(o['who']==who and o['state']=='pending' for o in ensure(s)['offers']):
                p['plan']=None
                if actor['location']!=loop.HOUSES[who][0]: loop.start_trip(s,who,loop.HOUSES[who][0])
            return True
        if not sleep_window(s,who):
            actor['activity']='Quiet company' if p['social']<35 else 'Hanging out'
            target=plan['target']; other=s['world']['cast'].get(target,{})
            shared=(loop.together(s,who) if target==s['player'] else other.get('location')==actor['location'] and not other.get('journey'))
            shared=shared and status(s,target)!='Asleep'
            if not plan.get('recorded') and shared:
                plan['recorded']=True
                record(s, who+' met '+plan['target']+' for '+plan.get('activity','a relaxed visit')+'.',[who,plan['target']])
                activity=plan.get('activity','quiet conversation')
                p['preferences'][activity]=p['preferences'].get(activity,0)+1
                p['happiness']=min(100,p['happiness']+2)
            if plan.get('introduce_to_player') and loop.together(s,who) and loop.together(s,plan['target']):
                import hidden_cast
                hidden_cast.mark_met(s,who)
                record(s,plan['target']+' introduced '+who+' to the player during their agreed outing.',[who,plan['target'],s['player']])
                plan['introduce_to_player']=False
            return True
    if sleep_window(s,who):
        home=loop.HOUSES[who][0]
        together=loop.together(s,who) and (who in s['world']['party'] or dating.in_hangout(s,who) or plan)
        # Late starts can flex, but only by a bounded amount and never all night.
        late=(now%1440-p['bedtime'])%1440
        grace=60 if together and p['energy']>25 and p['happiness']>55 else 15
        if together and late<grace:
            actor['activity']='Winding down'
            if not p.get('bed_notice') or now-p['bed_notice']>600:
                p['bed_notice']=now
                record(s, who+' is getting tired and needs to leave or settle down soon.',[who,s['player']])
                if actor['location']==loop.HOUSES[s['player']][0] and s['relationships'].get(who,s.get('friendships',{}).get(who,{})).get('closeness',0)>=35:
                    request(s,who,'overnight','Ask whether a separate sleeping place is available tonight; no intimacy is implied.')
            return True
        p['plan']=None
        if who in s['world']['party']: s['world']['party'].remove(who)
        actor.pop('waiting_for_hangout',None)
        if actor['location']!=home:
            loop.start_trip(s,who,home)
        actor['activity']='Sleep'
        return True
    if actor['activity']=='Sleep': actor['activity']='Morning routine'
    return False


def tick(s):
    import world_loop as loop
    import hidden_cast
    import living_world
    import scheduled_events
    a=ensure(s); now=s['world']['minute']
    if now%5: return
    for o in a['offers']:
        if o['state']=='pending' and now>o['expires']: o['state']='expired'
    for who,p in a['people'].items():
        if __import__('combat').recovering(s,who): continue
        if who == 'crow': continue
        state=status(s,who); actor=s['world']['cast'][who]
        sleeping=state=='Asleep'; social=state=='Socialising' or actor['activity'] in ('Hanging out','Quiet company')
        p['energy']=max(0,min(100,p['energy']+(1.05 if sleeping else -.40)))
        companions=[other for other,c in s['world']['cast'].items() if other!=who and c['location']==actor['location'] and not c['journey'] and status(s,other)!='Asleep'] if social else []
        def familiarity(other):
            if s['player'] in (who,other):
                friend=other if who==s['player'] else who
                return s.get('relationships',{}).get(friend,s.get('friendships',{}).get(friend,{})).get('closeness',0)
            return p['relationships'].get(other,{}).get('closeness',0)
        comfort=bool(companions and len(companions)<=2 and max(map(familiarity,companions))>=55)
        p['social']=max(0,min(100,p['social']+(.45 if sleeping or state=='At home' or actor['activity']=='Quiet recovery' else .15 if comfort else -.28 if social else -.08)))
        p['happiness']=max(0,min(100,p['happiness']+(.12 if social and p['social']>15 else -.12 if p['energy']<15 else (60-p['happiness'])*.0005)))
        if p['sleep_until'] and now>=p['sleep_until']: p['sleep_until']=None
        cause=p.get('emotion_cause')
        if who!=s['player'] and cause and now-cause['minute']>=180 and s['emotions'].get(who)==cause['feeling']:
            import emotions
            s['emotions'][who]=emotions.NEXT_MORNING.get(cause['feeling'],cause['feeling'])
            p.pop('emotion_cause',None)
        if who==s['player'] or sleeping: continue
        # Small, owned life events influence mood without rewriting biography.
        if state=='At work / studying' and p.get('event_day')!=now//1440 and now%1440>=15*60:
            p['event_day']=now//1440
            good=chance(who,now//1440,'day')>.35
            p['happiness']=max(0,min(100,p['happiness']+(3 if good else -3)))
            record(s,who+(' made satisfying progress during their usual work or study.' if good else ' found today’s work or study tiring and wants some quiet recovery.'),[who])
        project_plan=p.get('plan') or {}
        if who in living_world.PROJECTS and not actor['journey'] and (actor['location']==living_world.PROJECTS[who][1] or project_plan.get('kind')=='project' and actor['location']==project_plan['venue']):
            progress=living_world.ensure(s)['projects'].setdefault(who,{})
            if 'work_minutes' not in progress: living_world.project(s,who)
            progress['work_minutes']=progress.get('work_minutes',0)+5
            if progress['work_minutes']>=360 and not progress.get('completion_recorded'):
                progress['completion_recorded']=True
                record(s,who+' finished their project: '+living_world.PROJECTS[who][0]+'.',[who])
                p['happiness']=min(100,p['happiness']+5)
        if now<p['next_decision']: continue
        p['next_decision']=now+15+int(chance(who,now,'decision')*16)
        import dating
        if p['plan'] or actor['journey'] or scheduled_events.active(s,who) or who in s['world']['party'] or dating.in_hangout(s,who) or s['routes'][who].get('channel')=='in_person': continue
        if state=='At work / studying': continue
        if p['energy']<25 or p['social']<15:
            p['plan']=dict(kind='rest',venue=loop.HOUSES[who][0],until=now+60,target=who,activity='quiet recovery')
            continue
        if who in living_world.PROJECTS and living_world.project(s,who)['stage']<3 and chance(who,now,'project')<.10:
            p['plan']=dict(kind='project',venue=living_world.PROJECTS[who][1],until=now+90,target=who)
            continue
        daily_offers=sum(o['minute']//1440==now//1440 for o in a['offers'])
        if daily_offers<4 and now>=p['next_initiation'] and hidden_cast.contact(s,who) and state in ('Free time','At home'):
            bond=s.get('relationships',{}).get(who,s.get('friendships',{}).get(who,{}))
            interest=bond.get('closeness',0)
            import messaging
            attention=messaging.affinity(s,who)
            if chance(who,now,'invite') < .04+attention/800 and p['unanswered']<2:
                p['next_initiation']=now+round(120+(100-attention)*4)
                if interest>=55 and s['world']['location']==loop.HOUSES[s['player']][0] and status(s,s['player'])!='Asleep':
                    # Familiar visitors can travel to the door, never enter automatically.
                    p['plan']=dict(kind='visit',venue=s['world']['location'],until=now+75,target=s['player'],accepted=False)
                    request(s,who,'visit','Ask to drop by for a quiet visit; wait for permission to enter.',s['world']['location'])
                else:
                    activity=ACTIVITIES.get(who,'a relaxed conversation')
                    rituals=[venue for key,days in living_world.ensure(s)['rituals'].items() for friend,venue in [key.split(':')] if friend==who and len(days)>=3]
                    import leisure
                    venue=leisure.social_destination(s,who,s['player'],preferred=rituals)
                    activity=leisure.ACTIVITIES[venue]
                    motivation='Suggest returning to your established shared ritual.' if venue in rituals else 'Suggest '+activity+'; offer a shorter or quieter alternative if needed.'
                    import memory_store
                    commitments=memory_store.open_commitments(s,[who,s['player']])
                    if commitments and chance(who,now,'promise')<.35:
                        motivation='Gently revisit this actual unresolved proposal or promise without claiming it was agreed or completed: '+commitments[-1]['text']
                    request(s,who,'hangout',motivation,venue)
                p['unanswered']+=1
        # Deliberate peer company: choose an established acquaintance and a public venue.
        if not p['plan'] and p['social']>40 and chance(who,now,'peer')<.12:
            peers=[b for b in p['relationships'] if b!=s['player'] and p['relationships'][b]['tension']<15 and status(s,b) in ('Free time','At home') and not person(s,b)['plan']]
            if peers:
                other=max(peers,key=lambda b:p['relationships'][b]['interest']+chance(who,b,now)*15)
                import leisure
                venue=leisure.social_destination(s,who,other)
                for first,second in ((who,other),(other,who)):
                    person(s,first)['plan']=dict(kind='social',venue=venue,until=now+90,target=second,activity=leisure.ACTIVITIES[venue])
    # Introductions require sustained public co-presence; private homes never introduce strangers.
    for first,second in itertools.combinations(a['people'],2):
        if s['player'] in (first,second): continue
        x=s['world']['cast'][first]; y=s['world']['cast'][second]
        key=':'.join(sorted((first,second))); encounter=a['encounters'].setdefault(key,dict(minutes=0,day=-1))
        if x['location']!=y['location'] or x['journey'] or y['journey'] or x['location'].endswith('_home') or any(status(s,w)=='Asleep' for w in (first,second)):
            encounter['minutes']=0
            continue
        encounter['minutes']+=5
        if encounter['minutes']<20 or encounter['day']==now//1440: continue
        encounter['day']=now//1440
        social_encounter(s,first,second,x['location'])


def advance_player(s, action):
    import world_loop as loop
    import town
    now=s['world']['minute']; p=person(s,s['player'])
    if action=='wake':
        p['sleep_until']=None
        s['world']['sleep_speed']=1
        return 0
    if action in ('sleep_normal','sleep_fast','sleep_faster','sleep_skip'):
        until=p.get('sleep_until')
        if until is None or until<=now: raise ValueError('Start sleeping before changing sleep time.')
        if action=='sleep_skip':
            remaining=until-now
            while remaining:
                step=min(remaining,2880)
                loop.advance(s,step)
                remaining-=step
            p['sleep_until']=None
            s['world'].update(sleep_speed=1,clock_fraction=0.)
            return until-now
        s['world']['sleep_speed']={'sleep_normal':1,'sleep_fast':4,'sleep_faster':12}[action]
        return 0
    if action not in ('nap','sleep'): raise ValueError('Time passes automatically while you play.')
    duration={'nap':60,'sleep':480}[action]
    if action in ('nap','sleep'):
        if s['world']['location']!=loop.HOUSES[s['player']][0]: raise ValueError('Go home before sleeping.')
        town.end_hangouts(s)
        p['sleep_until']=now+duration
        s['world']['sleep_speed']=1
    return duration


def context(s,who):
    p=person(s,who)
    return dict(status=status(s,who), needs={k:round(p[k]) for k in ('energy','social','happiness')},
                sleep_schedule={'bedtime':p['bedtime'],'wake':p['wake']}, intention=p['plan'],
                personal_relationships=p['relationships'], enjoyed_activities=p['preferences'],emotion_cause=p.get('emotion_cause'),
                pending_requests=[dict(kind=o['kind'],venue=o['venue'],expires=o['expires']) for o in ensure(s)['offers'] if o['who']==who and o['state']=='pending'],
                recent_events=[e for e in ensure(s)['events'] if who in e['owners']][-6:])
