"""Save-local protection work after the authored endings; no defeated HQ respawns."""
import organisation_guards as guards


def mission(title,venue,enemies,brief,outcome,route=None):
    return dict(title=title,venue=venue,enemies=enemies,brief=brief,outcome=outcome,route=route)


MISSIONS = {
 'dragon_market': mission('Red Dragons · market escort','blackhaven',('tengu','yokai'),
    'Residents request an escort after a new Shinokami collection threat. The Dragons secure a voluntary exit route; Garrett confronts the armed collectors.',
    'The residents and their takings reach safety. Red Dragons escorts collect no protection fee and recruit nobody.'),
 'dragon_freight': mission('Red Dragons · release the drivers','syndicate_office',('affiliate','clubs'),
    'Drivers report a fresh Syndicate attempt to seize people as collateral. The Dragons arrange transport while Garrett opens the loading exit.',
    'The drivers leave freely with their documented property. The Dragons take no cut; the Syndicate remains active.'),
 'dragon_witness': mission('Red Dragons · protect a complainant','market',('spades','affiliate'),
    'A resident who refused a Syndicate demand asks for help reaching a safe meeting. Dragons volunteers guard the destination while Garrett intercepts the pursuit.',
    'The complainant reaches the chosen meeting safely. Their identity stays out of public crew reports.'),
 'blackstone_transfer': mission('Awakened protection · intercept a transfer','blackhaven',('pmc','seeker'),
    'An Awakened adult supplies a coercive transfer notice from a remaining Blackstone contractor cell. Richter’s closed programme has not reopened. Confirm consent before blocking this new transfer.',
    'The Awakened adult leaves voluntarily. This transfer is stopped and its notice preserved; the original laboratory remains closed.'),
 'blackstone_records': mission('Awakened protection · secure withdrawal records','archive',('pmc','headhunter'),
    'A willing witness brings their own withdrawal records. A surviving Blackstone retrieval detail tries to seize them outside the archive.',
    'The witness retains their records and reaches a safe contact. No patient names are published and Richter is not returned to command.'),
 'kai_remnants': mission('Hamayashi remnants · stop a new recruitment cell','market',('kai_guard','kai_sentinel'),
    'After the successor’s dissolution, a breakaway cell is using its old name to pressure adults into service. A consenting complainant identifies the detail; this is not the original clan returning.',
    'The identified cell’s coercive effort is stopped. The dissolved successor’s bases stay closed; this victory does not erase Rei’s past.', 'destroyed'),
 'kai_watch': mission('Hamayashi watch · defend the right to leave','blackhaven',('kai_guard','kai_sentinel'),
    'Rei left the successor alone. Now a specific rogue detail has obstructed an adult’s voluntary departure, in breach of its charter. Their complaint warrants intervention without declaring every member guilty.',
    'The departing adult reaches safety and the documented breach is recorded. Rei has not joined or destroyed the successor.', 'leave'),
 'kai_charter': mission('Hamayashi leadership · enforce the charter','market',('kai_guard','kai_sentinel'),
    'An adult member asks to leave. A disobedient detail has ignored the voluntary-membership charter. As leader, Rei must secure the departure rather than demand loyalty.',
    'The member leaves safely; the offending detail is removed from duty. The adult-only, voluntary charter remains binding on Rei’s organisation.', 'lead'),
}


def read(s):
    return s.get('post_story',{})


def data(s):
    return s.setdefault('post_story',dict(version=1,active=None,serial=0,completed={},history=[],
        protected=0,management=dict(budget=450,last_day=-1,actions={},shelter=0)))


def complete(s):
    if s['player']=='garrett':
        import charles_quest
        return charles_quest.read(s)['step']>=len(charles_quest.STEPS)
    return s['player']=='rei' and bool(s.get('rei_story',{}).get('complete'))


def leader(s):
    gang=s.get('job_apps',{}).get('gang') or {}
    return complete(s) and s['player']=='rei' and s['rei_story']['hamayashi']=='lead' and gang.get('id')=='hamayashi' and gang.get('role')=='Leader'


def available(s):
    if not complete(s):return {}
    if s['player']=='garrett':return {k:v for k,v in MISSIONS.items() if k.startswith('dragon_')}
    route=s['rei_story']['hamayashi']
    return {k:v for k,v in MISSIONS.items() if k.startswith('blackstone_') or
            (v['route']==route and (route!='lead' or leader(s)))}


def base(s):
    return 'syndicate' if s['player']=='garrett' else 'rei_home'


def check(s,key=None):
    import combat
    combat.guard(s)
    if not complete(s):raise ValueError('Finish this protagonist’s authored story first.')
    if key is not None and key not in available(s):raise ValueError('This mission does not match your current story ending or leadership.')
    if s.get('interpol',{}).get('active') or s.get('careers',{}).get('active') or s.get('job_apps',{}).get('pending'):
        raise ValueError('Finish the active case or assignment before protection work.')


def begin(s,key):
    check(s,key);guards.here(s,base(s));d=data(s)
    if d['active']:raise ValueError('Finish the saved protection mission first. Its progress is retained.')
    if d['completed'].get(key,-1)==s['world']['minute']//1440:raise ValueError('This mission was completed today. Return next story day.')
    d['serial']+=1
    d['active']=dict(key=key,scope='post-story:'+str(d['serial']),verified=False,started=s['world']['minute'])
    return MISSIONS[key]['brief']+' Travel to the objective and verify the request in person.'


def current(s):
    a=read(s).get('active')
    if not a:raise ValueError('Select a post-story protection mission first.')
    check(s,a['key']);spec=MISSIONS[a['key']];guards.here(s,spec['venue'])
    return a,spec


def verify(s):
    a,spec=current(s)
    if a['verified']:raise ValueError('This request is already verified.')
    a['verified']=True
    return 'The willing complainant confirms the specific threat and their chosen safe destination. No bystander is treated as an enemy. '+spec['brief']


def remaining(s):
    a=read(s).get('active')
    if not a:return []
    won=s.get('organisation_guards',{}).get('victories',{}).get(a['scope'],[])
    return [(a['scope']+':'+str(i),kind) for i,kind in enumerate(MISSIONS[a['key']]['enemies']) if a['scope']+':'+str(i) not in won]


def fight(s):
    a,spec=current(s)
    if not a['verified']:raise ValueError('Verify the civilian’s request first.')
    rows=remaining(s)
    if not rows:raise ValueError('The detail is defeated. Secure the civilian’s departure.')
    ident,kind=rows[0]
    return guards.start(s,ident,guards.profile(s,kind),a['scope'])


def finish(s):
    a,spec=current(s)
    if not a['verified'] or remaining(s):raise ValueError('Verify the request and defeat the entire detail first.')
    d=data(s);text=spec['outcome'];day=s['world']['minute']//1440
    if leader(s):
        m=d['management'];m['budget']+=100
        if m['shelter']:
            m['shelter']-=1;text+=' A funded shelter placement supports the person’s onward recovery.'
        text+=' The organisation receives $100 in earmarked protection funding.'
    d['completed'][a['key']]=day;d['protected']+=1
    d['history'].append(dict(key=a['key'],minute=s['world']['minute'],text=text,scope=a['scope']))
    d['active']=None
    return text+' One protection request resolved; new requests become available next story day.'


def withdraw(s):
    import combat
    combat.guard(s)
    if not read(s).get('active'):raise ValueError('No active protection mission.')
    data(s)['active']=None
    return 'Mission withdrawn without a rescue, funding or completion reward. A fresh briefing is required to try again.'


DIRECTIVES = {
 'shelter': ('Fund a voluntary shelter placement',100),
 'departures': ('Audit voluntary departures with Ren',75),
 'recruitment': ('Review adult-only recruitment with Emi',75),
}


def manage(s,key):
    import combat
    combat.guard(s)
    if not leader(s):raise ValueError('Complete Rei’s leadership ending and retain Hamayashi-kai leadership to use this desk.')
    if key not in DIRECTIVES:raise ValueError('Choose a current management directive.')
    d=data(s);m=d['management'];day=s['world']['minute']//1440;title,cost=DIRECTIVES[key]
    if m['last_day']==day:raise ValueError('One management directive per story day. Return tomorrow.')
    if m['budget']<cost:raise ValueError('Insufficient organisation funds. Completed protection missions replenish this budget.')
    m['budget']-=cost;m['last_day']=day;m['actions'][key]=m['actions'].get(key,0)+1
    if key=='shelter':m['shelter']+=1
    text=title+f' — ${cost} allocated from the organisation budget. '
    text+=('One shelter placement is reserved for the next completed protection mission.' if key=='shelter' else
           'Ren verifies exit requests and records that no member owes service for receiving aid.' if key=='departures' else
           'Emi checks adult consent and excludes coercive recruiters from intake duty.')
    d['history'].append(dict(key='management:'+key,minute=s['world']['minute'],text=text))
    return text
