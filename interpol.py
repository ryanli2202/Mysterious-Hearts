"""Authoritative Interpol incidents, fines, evidence, operations and disclosure.

All physical mutations validate the current scene. Dialogue is never evidence.
The system is save-local; no external calls or retrospective criminal charges.
"""
import copy
import hashlib
import uuid
from interpol_cast import IDS, BOUNDARY
from interpol_cases import CASES, OPERATIONS

SECURE_ROOMS = ('interpol_briefing', 'interpol_training', 'interpol_containment')
BASE_INFLUENCE = {'civic': 80, 'blackhaven': 40, 'west': 35, 'waterfront': 30, 'central': 60}
OFFENCES = {
    'assault': ('Unprovoked assault', 800),
    'theft': ('Theft', 300),
    'intimidation': ('Witness intimidation', 600),
    'coercion': ('Approving a documented coercive request', 500),
    'reckless_commission': ('Reckless illicit commission', 450),
}


def ensure(s):
    d=s.setdefault('interpol', {})
    for k,v in dict(version=1, incidents=[], fines=[], files={}, knowledge={}, influence={},
                    disruption={}, custody={}, notifications=[], enrolled=[], active=None, encounter=None,
                    operations={}, history=[]).items():
        d.setdefault(k, copy.deepcopy(v))
    return d


def read(s):
    return s.get('interpol', {})


def district(location):
    if location in ('blackhaven','fox_home','fox_hideout'): return 'blackhaven'
    if location.startswith('interpol') or location.startswith('gordon'): return 'civic'
    if location.startswith(('site_01','site_02','site_03')) or location in ('saints_depot','archive'): return 'west'
    if location.startswith(('site_04','site_05','site_06','site_07','site_08','syndicate')): return 'waterfront'
    return 'central'


def influence(s, area=None):
    area=area or district(s['world']['location'])
    return read(s).get('influence',{}).get(area,BASE_INFLUENCE.get(area,50))


def clearance(s, who):
    if who==s.get('player') and 'interpol' in s.get('combat',{}).get('expelled',[]): return False
    return who in IDS or who in read(s).get('enrolled',[])


def case_access(s, who, location):
    a=read(s).get('active') or {}
    return (clearance(s,s.get('player')) and location=='syndicate_hq' and a.get('key')=='crow_operation'
            and who in (s.get('player'),a.get('partner')) and not a.get('repeatable'))


def check_trip(s, who, destination, passengers=()):
    if destination in SECURE_ROOMS and any(not clearance(s,p) for p in (who,*passengers)):
        raise ValueError('Each visitor needs Interpol case-assistance clearance. Register at the public desk first.')


def here(s, who):
    actor=s['world'].get('cast',{}).get(who,{})
    return actor.get('location')==s['world']['location'] and not actor.get('journey') and actor.get('activity')!='Sleep'


def guard(s, venue=None):
    import combat
    combat.guard(s)
    actor=s['world']['cast'][s['player']]
    if actor.get('activity')=='Sleep': raise ValueError('Wake up before a physical activity.')
    if venue and s['world']['location']!=venue: raise ValueError('Travel to the objective location first.')
    if s.get('careers',{}).get('active') or s.get('crime_operations',{}).get('people',{}).get(s['player'],{}).get('active'):
        raise ValueError('Finish your current work session first.')


def note(s, text):
    d=ensure(s); item=dict(minute=s['world']['minute'],text=text)
    d['history'].append(item)
    s['world'].setdefault('log',[]).append('Interpol: '+text)
    s['world']['log']=s['world']['log'][-120:]
    return text


def known_identity(s, observer, identity):
    return identity in read(s).get('knowledge',{}).get(observer,{}).get('identities',[])


def reveal(s, observers, identity, source):
    d=ensure(s)
    for observer in set(observers)-{None}:
        k=d['knowledge'].setdefault(observer,dict(identities=[],sources={}))
        if identity not in k['identities']: k['identities'].append(identity)
        k['sources'][identity]=dict(source=source,minute=s['world']['minute'])


def is_criminal_target(s, target):
    import criminal_dynamics
    return bool(criminal_dynamics.faction(target) or any(i['actor']==target and i['observed'] for i in read(s).get('incidents',[])))


def record_offence(s, kind, target=None, *, event_id=None, documented=False):
    """Called only by committed authored actions; deduplicate their stable event IDs."""
    if kind not in OFFENCES: raise ValueError('Unknown offence.')
    d=ensure(s); event_id=event_id or uuid.uuid4().hex
    prior=next((i for i in d['incidents'] if i['id']==event_id),None)
    if prior: return prior
    actor=s['player']; now=s['world']['minute']; location=s['world']['location']
    witnesses=[who for who in s['world']['cast'] if who!=actor and here(s,who)]
    witnesses.extend(s['world'].get('npcs',[]))
    # Patrol coverage is a disclosed game probability. It never fabricates Gordon's presence.
    public=not location.endswith('_home') and location not in ('glasshouse_lab','syndicate_hq') and not location.endswith('_briefing')
    roll=int(hashlib.sha256(event_id.encode()).hexdigest()[:8],16)%100
    patrol=public and roll<influence(s)
    if patrol: witnesses.append('Regional patrol')
    incident=dict(id=event_id,actor=actor,kind=kind,target=target,location=location,minute=now,
                  witnesses=list(dict.fromkeys(witnesses)),observed=bool(witnesses or documented),
                  evidence='Official work record' if documented else 'Witnessed act' if witnesses else 'No report or witness',
                  status='unreported',due=now+60)
    d['incidents'].append(incident)
    if actor=='fox' and kind=='assault' and is_criminal_target(s,target) and 'gordon' in witnesses:
        incident['status']='discretion'
        incident['reason']='Gordon witnessed Fox attacking a criminal target and declined to issue a fine.'
        note(s,incident['reason'])
    elif 'gordon' in witnesses:
        issue_fine(s,incident,'Jeremy Gordon · on the spot')
    elif incident['observed']:
        incident['status']='under investigation'
        note(s,OFFENCES[kind][0]+': a report was recorded. Regional review is due in 60 story minutes.')
    else:
        note(s,OFFENCES[kind][0]+': no witness or patrol recorded this incident.')
    jobs=s.get('job_apps')
    if jobs and incident['observed']: jobs['heat']=min(100,jobs.get('heat',0)+5)
    return incident


def issue_fine(s, incident, issuer):
    d=ensure(s)
    if incident['status'] in ('fined','discretion') or any(f['incident']==incident['id'] for f in d['fines']): return
    repeats=sum(f['actor']==incident['actor'] and f['kind']==incident['kind'] for f in d['fines'])
    amount=OFFENCES[incident['kind']][1]*(1+min(repeats,3)*.25)
    fine=dict(id='fine-'+incident['id'],incident=incident['id'],actor=incident['actor'],kind=incident['kind'],
              amount=int(amount),paid=0,issuer=issuer,minute=s['world']['minute'],location=incident['location'])
    d['fines'].append(fine); incident['status']='fined'
    text=f'{issuer}: ${int(amount)} fine for {OFFENCES[incident["kind"]][0].lower()}. Payment is available in the Interpol record or at the public desk.'
    d['notifications'].append(text); note(s,text)


def tick(s):
    if 'interpol' not in s: return
    for incident in s['interpol'].get('incidents',[]):
        if incident['status']=='under investigation' and s['world']['minute']>=incident['due']:
            issue_fine(s,incident,'Interpol regional review')


def debt(s):
    return sum(f['amount']-f['paid'] for f in read(s).get('fines',[]) if f['actor']==s['player'])


def pay(s, fine_id):
    fine=next((f for f in ensure(s)['fines'] if f['id']==fine_id and f['actor']==s['player']),None)
    if not fine: raise ValueError('That fine is not payable by this protagonist.')
    owed=fine['amount']-fine['paid']
    if owed<=0: raise ValueError('This fine is already paid.')
    amount=min(owed,max(0,int(s['world']['money'])))
    if amount<=0: raise ValueError('No funds available. The unpaid balance remains on the record.')
    s['world']['money']-=amount; fine['paid']+=amount
    s.setdefault('interpol',{}).setdefault('payments',[]).append(dict(fine=fine_id,amount=amount,minute=s['world']['minute']))
    return note(s,f'Paid ${amount}. Remaining on this fine: ${fine["amount"]-fine["paid"]}. Incident history retained.')


def street_action(s, kind):
    guard(s)
    if s['world']['location'] not in ('blackhaven','downtown','market','syndicate_office'):
        raise ValueError('These street actions are available in Blackhaven, downtown, the market and the waterfront frontage.')
    if kind not in ('theft','intimidation'): raise ValueError('Choose an available street action.')
    record_offence(s,kind)
    if kind=='theft': s['world']['money']+=90
    import world_loop
    world_loop.advance(s,10)
    return 'The theft added $90; any observed offence carries a separate fine.' if kind=='theft' else 'The intimidation was recorded as an actual offence; witnesses and patrols determine enforcement.'


def enrol(s):
    guard(s,'interpol_hq'); d=ensure(s)
    if 'interpol' in s.get('combat',{}).get('expelled',[]): raise ValueError('Re-registering cannot erase your expulsion from Interpol.')
    if s['player'] in d['enrolled'] or s['player'] in IDS: return 'Your Interpol role already grants case access.'
    d['enrolled'].append(s['player'])
    return note(s,'Registered as a civilian case assistant. Briefing access granted; no police rank, general warrant or confidential identity knowledge.')


def available(s, key):
    return all(req in read(s).get('files',{}) and read(s)['files'][req].get('complete') for req in CASES[key]['requires'])


def begin(s, key, repeatable=False):
    guard(s,'interpol_hq'); d=ensure(s)
    if not clearance(s,s['player']): raise ValueError('Register for case assistance at this desk first.')
    if d['active']: raise ValueError('Finish or suspend the current operation first.')
    if repeatable:
        if key not in OPERATIONS: raise ValueError('Unknown operation.')
        if not d['files'].get('blackhaven',{}).get('complete'): raise ValueError('Complete the first case before independent operations.')
        if d['operations'].get(key,-1)==s['world']['minute']//1440: raise ValueError('This operation was completed today; return tomorrow.')
    else:
        if key not in CASES or not available(s,key): raise ValueError('Complete the prerequisite case files first.')
        if d['files'].get(key,{}).get('complete'): raise ValueError('This case is already complete.')
        if CASES[key].get('reveal')==s['player']: raise ValueError('You cannot join the investigation of your own concealed role.')
    partner='fox' if s['player']=='gordon' else 'gordon'
    import combat
    if partner in combat.ensure(s)['ruptures']: raise ValueError('Your attack permanently ruptured this partnership. They will not assemble a field team with you.')
    if not here(s,partner) or combat.recovering(s,partner):
        raise ValueError('Meet '+('Fox (normally 13:00–16:00)' if partner=='fox' else 'Gordon (normally 08:00–12:00)')+' at the public desk before assembling the team.')
    file=d['files'].setdefault(key,dict(step=0,evidence=[],attempts=0,complete=False)) if not repeatable else {}
    party=s['world'].setdefault('party',[])
    d['active']=dict(key=key,partner=partner,repeatable=repeatable,party_added=partner not in party,
                     participants=[s['player'],partner],started=s['world']['minute'])
    if partner not in party: party.append(partner)
    import hidden_cast
    hidden_cast.mark_met(s,partner)
    s['world']['cast'][partner]['activity']='Interpol field team'
    return note(s,'Team assembled for '+(OPERATIONS if repeatable else CASES)[key]['title']+'. Travel to the objective together.')


def objective(s):
    a=read(s).get('active')
    if not a: return None
    if a['repeatable']:
        spec=OPERATIONS[a['key']]
        return dict(title=spec['title'],venue=spec['venue'],kind='combat',finding='Witness and consignment safety secured.',enemy=spec['enemy'],power=spec['power'])
    return CASES[a['key']]['steps'][read(s)['files'][a['key']]['step']]


def travel_objective(s):
    guard(s); a=read(s).get('active'); step=objective(s)
    if not a or not step: raise ValueError('Assemble a team first.')
    if not clearance(s,s['player']): raise ValueError('Your Interpol clearance has been revoked. Suspend the operation.')
    if not here(s,a['partner']): raise ValueError('Reunite with your field partner before travelling.')
    import town
    town.travel(s,step['venue'])  # The assembled field partner is already in the saved party.
    return 'The field team arrived at the objective.'


def team_guard(s):
    a=read(s).get('active'); step=objective(s)
    if not a or not step: raise ValueError('No active investigation.')
    guard(s,step['venue'])
    import combat
    if not clearance(s,s['player']) or a['partner'] in combat.ensure(s)['ruptures']:
        raise ValueError('This field partnership no longer has valid clearance or trust. Suspend the operation.')
    if not here(s,a['partner']) or combat.recovering(s,a['partner']): raise ValueError('Your field partner must be here and fit for duty.')
    if read(s).get('encounter'): raise ValueError('Resolve and close the operation’s combat encounter first.')
    if (read(s).get('files',{}).get(a['key'],{}).get('retry_after',0)>s['world']['minute']):
        raise ValueError('The suspect escaped this attempt. Regroup for two story hours before returning.')
    return a,step


def advance(s):
    a,step=team_guard(s)
    if step['kind']=='combat': return start_encounter(s)
    finding=step['finding']
    if step.get('sensory') and 'fox' in a['participants']:
        finding+=' '+step['sensory']
    record_evidence(s,step,finding)
    import world_loop
    world_loop.advance(s,20)
    return finding


def record_evidence(s, step, finding):
    d=ensure(s); a=d['active']; key=a['key']; spec=CASES[key]; file=d['files'][key]
    entry=dict(title=step['title'],finding=finding,minute=s['world']['minute'],venue=step['venue'],participants=a['participants'][:])
    file['evidence'].append(entry); file['step']+=1
    if step['kind']=='reveal':
        import four_aces
        who=spec['reveal']; reveal(s,a['participants'],who,key)
        finding=four_aces.CAST[who]['name']+' is the Ace of '+four_aces.CAST[who]['suit']+'. '+finding
        entry['finding']=finding
    if step['kind']=='locate': reveal(s,a['participants'],'crow_location',key)
    if step['kind']=='close':
        d['custody']['crow']=dict(location='interpol_containment',case=key,minute=s['world']['minute'])
        if 'crow' in s['world']['cast']:
            s['world']['cast']['crow'].update(location='interpol_containment',journey=None,activity='In regional custody after Operation Night Ledger')
    # Link already discovered site notebooks; case work does not disclose unrelated fronts.
    if step['venue'].startswith('site_'):
        s.setdefault('interpol_site_evidence',{}).setdefault(step['venue'],[]).append(dict(case=key,title=step['title'],minute=s['world']['minute']))
    note(s,finding)
    if file['step']>=len(spec['steps']):
        file['complete']=True; file['completed_at']=s['world']['minute']
        reward(s,spec)
        release_team(s)


def reward(s,spec):
    d=ensure(s); area=spec['district']; d['influence'][area]=min(95,influence(s,area)+8)
    d['disruption'][spec['faction']]=max(d['disruption'].get(spec['faction'],0),s['world']['minute']+2*1440)
    s['world']['money']+=250
    note(s,'Case outcome recorded. $250 field allowance; regional influence increased. Related criminal commissions are disrupted for two story days.')


def release_team(s):
    d=ensure(s); a=d['active']
    if a and a.get('party_added') and a['partner'] in s['world'].get('party',[]): s['world']['party'].remove(a['partner'])
    d['active']=None; d['encounter']=None
    # A scoped warrant cannot become permanent criminal headquarters membership.
    import hidden_cast
    hidden_cast.reconcile_hq_access(s)


def suspend(s):
    guard(s)
    if read(s).get('encounter'): raise ValueError('Finish the encounter before suspending.')
    release_team(s)
    return note(s,'Field team released. Collected evidence is retained; resume at the public desk.')


def regroup_delay(s):
    import combat
    a=read(s).get('active')
    if not a: return 0
    return max(0, read(s).get('files',{}).get(a['key'],{}).get('retry_after',0)-s['world']['minute'],
               combat.recovering(s),combat.recovering(s,a['partner']))


def regroup(s):
    import combat, world_loop
    if combat.active(s): raise ValueError('Close the combat encounter before regrouping.')
    if s['world']['cast'][s['player']].get('journey'): raise ValueError('Finish travelling before regrouping.')
    delay=regroup_delay(s)
    if not delay: raise ValueError('The team does not need a recovery wait.')
    world_loop.advance(s,delay)
    return note(s,'Regrouping and any knockout recovery are complete. Return to the objective with your partner.')


def encounter_profile(s):
    from combat_profiles import make,profile
    step=objective(s)
    if not step or step['kind']!='combat': raise ValueError('No authorised combat objective.')
    if step.get('opponent'):
        result=copy.deepcopy(profile(s,step['opponent'])); result['name']=step['enemy']
    else:
        result=make('interpol_suspect',dict(name=step['enemy'],awakened=True))
        power=step['power']; result['stats'].update(awakened_power=power,trait_refinement=0,martial_skill=min(90,power+15),fight_iq=min(90,power+12))
        result['arts']={'Military CQC':result['stats']['martial_skill']}
    return result


def start_encounter(s):
    a,step=team_guard(s)
    if step.get('opponent')==s['player']: raise ValueError('You cannot be both sides of an operation.')
    import combat
    if step.get('opponent') and combat.recovering(s,step['opponent']): raise ValueError('The target is recovering; return after their recovery period.')
    token=uuid.uuid4().hex; ensure(s)['encounter']=dict(token=token,key=a['key'],step=read(s)['files'].get(a['key'],{}).get('step',0))
    # This authored interception places the actual suspect at the scene. The
    # encounter profile uses a mask/role label until later corroboration.
    actor=s['world']['cast'].get(step.get('opponent'))
    previous=copy.deepcopy(actor) if actor is not None else None
    if actor is not None: actor.update(location=step['venue'],journey=None,activity='Intercepted during an Interpol operation')
    try:
        f=combat.start(s,step.get('opponent') or 'interpol:'+a['key'],'interpol')
    except Exception:
        if actor is not None: actor.clear(); actor.update(previous)
        ensure(s)['encounter']=None
        raise
    f['operation_token']=token; f['ally']=a['partner']
    f['ally_profile']=copy.deepcopy(combat.profile(s,a['partner']))
    f['ally_resources']=combat.resources(f['ally_profile'])
    f['log'].append(a['partner'].title()+' joins the authorised operation. Its combat results determine the next evidence step.')
    return 'Operation combat started. Open Combat to resolve the encounter.'


def validate_encounter(s, who):
    d=read(s); a=d.get('active'); e=d.get('encounter'); step=objective(s)
    if not a or not e or not step or step['kind']!='combat' or s['world']['location']!=step['venue'] or not here(s,a['partner']):
        raise ValueError('An authorised, assembled Interpol operation is required.')
    if who!=(step.get('opponent') or 'interpol:'+a['key']): raise ValueError('Wrong operation opponent.')
    return encounter_profile(s)


def support_turn(s,f,rng):
    if f['kind']!='interpol' or not f.get('ally_resources'): return
    import combat
    r=f['ally_resources']; p=f['ally_profile']; q=f['opponent_profile']
    if r['health']<=0 or f['enemy']['health']<=0 or f['player']['health']<=0: return
    cost=19 if (p.get('trait') or {}).get('effect')=='biocreation' else 14
    mode='Trait' if p.get('trait') and r['energy']>=cost and r['stamina']>=8 else 'Recover'
    damage,text=combat.strike(p,q,r,f['enemy'],mode,next(iter(p['arts']),'Untrained'),40,0,rng,f['elapsed'],False)
    f['log'].append(p['name']+' supports the operation: '+text+'.'); f['score'][0]+=damage
    if f['enemy']['health']>0 and f['turn']%2==0:
        _,reply=combat.strike(q,p,f['enemy'],r,'Martial',next(iter(q['arts']),'Untrained'),0,0,rng,f['elapsed'],False)
        f['log'].append(q['name']+' counters the field partner: '+reply+'.')
        if r['health']<=0:
            combat.ensure(s)['recovery'][f['ally']]=s['world']['minute']+1440
            f['log'].append(p['name']+' is incapacitated and needs a day of recovery.')


def resolve_fight(s,f):
    if f.get('kind')!='interpol': return
    d=ensure(s); e=d.get('encounter'); a=d.get('active')
    if not e or not a or e['token']!=f.get('operation_token'): return
    d['encounter']=None
    if not f.get('result','').startswith('Victory'):
        file=d['files'].setdefault(a['key'],dict(step=0,evidence=[],attempts=0,complete=False))
        file['attempts']+=1; file['retry_after']=s['world']['minute']+120
        note(s,'The operation failed to secure its objective. Evidence retained; regroup before retrying.')
        return
    if a['repeatable']:
        spec=OPERATIONS[a['key']]; d['operations'][a['key']]=s['world']['minute']//1440
        reward(s,spec); release_team(s)
    else:
        step=objective(s); record_evidence(s,step,step['finding'])


def share_identity(s, target, identity):
    guard(s)
    if target==s['player'] or not here(s,target): raise ValueError('Meet the intended recipient in person.')
    if not known_identity(s,s['player'],identity): raise ValueError('Your case file has not established that identity.')
    reveal(s,[target],identity,'Explicit briefing by '+s['player'])
    return note(s,'Shared this established finding with '+target+'. No other private case records were disclosed.')


def context(s, who, listeners=()):
    if not s: return {}
    result={}
    if who in IDS: result['Interpol conduct']=BOUNDARY
    own=read(s).get('knowledge',{}).get(who,{}).get('identities',[])
    shared=[ident for ident in own if all(known_identity(s,p,ident) for p in listeners)]
    if shared:
        import four_aces
        result['Established case discoveries']=[four_aces.CAST[x]['name']+' is the Ace of '+four_aces.CAST[x]['suit'] if x in four_aces.IDS else 'The Crow’s command site was located by the saved case.' for x in shared]
    if who in IDS or shared:
        result['Disclosure']='Only the supplied discoveries may be acknowledged to this audience. Do not reveal unlisted Aces or invent the Crow’s real name.'
    if read(s).get('custody',{}).get('crow') and (who=='crow' or who in IDS):
        result['Current custody']='The saved operation placed the Crow in the regional containment wing. Do not invent an escape or keep describing him as still at headquarters. His birth identity remains unverified.'
    a=read(s).get('active')
    if a and who in a['participants'] and all(p in a['participants'] for p in listeners):
        result['Current objective']=objective(s)['title']
    relevant=[i for i in read(s).get('incidents',[]) if who==i['actor'] or who in i['witnesses']]
    if relevant: result['Personally known incidents']=[{k:i.get(k) for k in ('kind','actor','target','status','reason')} for i in relevant[-4:]]
    return result
