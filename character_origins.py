"""Versioned, deterministic custom starting choices; applied only at creation."""
import copy
import combat_balance
import combat_moves
import job_apps

EXPERIENCES = tuple(combat_balance.STARTING_EXPERIENCE)
# Maximum styles / advanced / master selections in the approved kit catalogue.
KITS = ((0,0,0), (1,0,0), (2,2,0), (2,4,1), (3,6,2), (3,8,3), (4,10,4))
ARTS = tuple(s['art'] for s in combat_moves.MARTIAL)
BACKGROUNDS = ('New arrival', 'First job', 'Career changer', 'Transferred professional', 'Returning to work',
               'Creative practitioner', 'Vocational specialist', 'Experienced supervisor', 'Student / recent graduate',
               'Former courier', 'Street survivor', 'Freelance fixer', 'Former crew member', 'Faction transfer',
               'Underground fighter', 'Numbers specialist', 'Small-crew founder', 'Former service professional', 'Prior Shinokami training')
BACKGROUND_EXPERIENCE = {'Former courier':1,'Street survivor':1,'Freelance fixer':2,'Former crew member':1,
                         'Faction transfer':2,'Underground fighter':3,'Former service professional':2,'Prior Shinokami training':2}
CRIME = {
    'Clean slate': (0,0,0), 'Former underworld worker': (20,0,0),
    'Independent operator': (20,5,2), 'Connected freelancer': (40,10,2),
    'Trusted crew member': (30,5,1), 'Crew lieutenant': (50,10,3), 'Crew captain': (65,15,4),
    'Established faction member': (40,5,2), 'Faction specialist': (50,10,3), 'Faction field leader': (60,15,4),
    'Small-crew founder': (25,5,2),
}
DEFAULT_ARTS = {
    'Clubs':['Military CQC','Judo','Boxing','Silat'],
    'Hearts':['Kickboxing','Taekwondo','Taido','Boxing'],
    'Diamonds':['Aikido','Judo','Wing Chun','Boxing'],
    'Spades':['Silat','Krav Maga','Military CQC','Systema'],
    'Shinokami':['Shinokami martial arts','Japanese Jujutsu','Kyokushin','Judo'],
    None:['Boxing','Judo','Military CQC','Silat'],
}


def validate(raw):
    if not isinstance(raw, dict) or raw.get('version', 1) != 1:
        raise ValueError('Unsupported starting-choice version.')
    p = dict(version=1, experience=raw.get('experience','Newcomer'), job=raw.get('job'),
             job_rank=raw.get('job_rank',0), crime=raw.get('crime','Clean slate'),
             organisation=raw.get('organisation'), arts=raw.get('arts',[]), moves=raw.get('moves',[]))
    p.update(background=raw.get('background','New arrival'), prior_job=raw.get('prior_job'),
             prior_rank=raw.get('prior_rank',0), crew_name=raw.get('crew_name','Independent crew'),career_interest=raw.get('career_interest'))
    if p['career_interest'] is not None and p['career_interest'] not in job_apps.JOBS: raise ValueError('Choose a supported career interest or none.')
    if p['background'] not in BACKGROUNDS: raise ValueError('Choose a supported narrative background.')
    if p['prior_job'] is not None and p['prior_job'] not in job_apps.JOBS: raise ValueError('Choose a supported previous career.')
    if type(p['prior_rank']) is not int or not 0<=p['prior_rank']<=3: raise ValueError('Prior career rank must be 0–3.')
    if not isinstance(p['crew_name'],str) or not 3<=len(p['crew_name'].strip())<=40: raise ValueError('Crew name must be 3–40 characters.')
    p['crew_name']=p['crew_name'].strip()
    if p['crime']=='Small-crew founder' and p['crew_name'].casefold() in ({v['name'].casefold() for v in job_apps.progression.GANGS.values()}|{'syndicate','shinokami'}):
        raise ValueError('Choose an original crew name, not a canonical organisation.')
    if p['experience'] not in EXPERIENCES: raise ValueError('Choose a recognised combat history.')
    if p['job'] is not None and p['job'] not in job_apps.JOBS: raise ValueError('Choose a supported job or Looking for work.')
    if type(p['job_rank']) is not int or not 0 <= p['job_rank'] <= 3: raise ValueError('Choose a career rank from 0 to 3.')
    if p['prior_job'] and p['prior_job']==p['job'] and p['prior_rank']>p['job_rank']:
        raise ValueError('Current rank must retain the selected prior rank in the same career; choose returning without employment for a separate re-entry.')
    if p['crime'] not in CRIME: raise ValueError('Choose a supported criminal background.')
    if p['crime'] in ('Trusted crew member','Crew lieutenant','Crew captain'):
        if p['organisation'] not in job_apps.progression.GANGS: raise ValueError('Choose a street crew for this role.')
    elif p['crime'] in ('Established faction member','Faction specialist','Faction field leader'):
        if p['organisation'] not in job_apps.BRANCHES: raise ValueError('Choose a faction branch for this role.')
    elif p['organisation'] is not None: raise ValueError('This background has no active organisation.')
    for field, choices in (('arts',ARTS), ('moves',combat_moves.MOVES)):
        if not isinstance(p[field], list) or any(not isinstance(v,str) or v not in choices for v in p[field]) or len(set(p[field])) != len(p[field]):
            raise ValueError('Choose distinct supported '+field+'.')
    return copy.deepcopy(p)


def recommended(experience, arts, awakened=True):
    index = EXPERIENCES.index(experience)
    slots, advanced, masters = KITS[index]
    arts = list(dict.fromkeys(arts))[:slots]
    if not slots: arts = []
    moves = [m['id'] for m in combat_moves.MOVES.values() if m['art'] in arts and m['tier']=='basic']
    # Round-robin advanced moves gives qualified secondary styles before masters.
    advanced_arts = arts[:1] if index==2 else arts
    rows = [[m['id'] for m in combat_moves.MOVES.values() if m['art']==art and m['tier']=='advanced'] for art in advanced_arts]
    candidates = [row[i] for i in range(max(map(len,rows),default=0)) for row in rows if i<len(row)]
    moves += candidates[:advanced]
    if awakened:
        qualified = arts[:2] if index>=5 else arts[:1]
        qualified = [a for a in qualified if any(combat_moves.MOVES[m]['art']==a and combat_moves.MOVES[m]['tier']=='advanced' for m in moves)]
        rows = [[m['id'] for m in combat_moves.MOVES.values() if m['art']==a and m['tier']=='master'] for a in qualified]
        candidates = [row[i] for i in range(max(map(len,rows),default=0)) for row in rows if i<len(row)]
        moves += candidates[:masters]
    return arts, moves


def resolve(raw, awakened, has_trait=True):
    p = validate(raw)
    index = experience_index(p)
    experience = EXPERIENCES[index]
    if index and not p['arts'] and not p['moves']:
        p['arts'],p['moves']=recommended(experience,DEFAULT_ARTS.get(p['organisation'],['Streetfighting','Boxing','MMA','Muay Thai']),awakened)
    scale = combat_balance.starting_scale(experience, awakened, has_trait)
    slots, advanced, masters = KITS[index]
    if len(p['arts']) > slots: raise ValueError(f'{experience} permits at most {slots} martial arts.')
    if 'Shinokami martial arts' in p['arts'] and p['organisation']!='Shinokami' and p['background']!='Prior Shinokami training':
        raise ValueError('Shinokami martial arts require an active Shinokami role or explicitly selected prior Shinokami training.')
    selected = [combat_moves.MOVES[m] for m in p['moves']]
    if any(m['art'] not in p['arts'] for m in selected): raise ValueError('Every selected move needs a selected martial art.')
    if sum(m['tier']=='advanced' for m in selected)>advanced or sum(m['tier']=='master' for m in selected)>masters:
        raise ValueError('Selected techniques exceed the starting kit allocation.')
    if index==2 and any(m['tier']=='advanced' and m['art']!=p['arts'][0] for m in selected):
        raise ValueError('Practised advanced techniques belong to the primary art.')
    masters_arts = p['arts'][:2] if index>=5 else p['arts'][:1]
    for move in selected:
        if move['tier']=='master':
            if not awakened: raise ValueError('Unawakened characters cannot learn superhuman master techniques.')
            if move['art'] not in masters_arts or not any(m['tier']=='advanced' and m['art']==move['art'] for m in selected):
                raise ValueError('A master technique needs an advanced technique in a qualified primary/secondary art.')
    # Formal training grants basics; advanced/master moves are only those selected.
    learned = list(dict.fromkeys([m['id'] for m in combat_moves.MOVES.values() if m['tier']=='basic' and m['art'] in p['arts']] + p['moves']))
    contributions = [f'{experience}: shared MH-001 starting scale; strongest history counted once.']
    if p['organisation'] in job_apps.BRANCHES:
        stat={'Clubs':'martial_skill','Hearts':'awakened_power','Diamonds':'fight_iq','Spades':'trait_refinement','Shinokami':'martial_skill'}[p['organisation']]
        bonus=(CRIME[p['crime']][2]-1)*.5
        if (stat!='awakened_power' or awakened) and (stat!='trait_refinement' or awakened and has_trait):
            scale['stats'][stat]+=bonus
            contributions.append(p['organisation']+' branch experience: '+stat.replace('_',' ')+f' +{bonus:g}.')
    # Prior and current work are alternative evidence, never two stacked careers.
    career=max([(p[k],p[r]) for k,r in (('job','job_rank'),('prior_job','prior_rank')) if p[k]],key=lambda x:x[1],default=None)
    if career:
        job,rank=career
        bonuses=dict(zip(scale['stats'],[round(v*(rank+1),2) for v in combat_balance.CAREER_FOCUS[job]]))
        if not awakened: bonuses['awakened_power']=0
        if not awakened or not has_trait: bonuses['trait_refinement']=0
        for stat,bonus in bonuses.items(): scale['stats'][stat]+=bonus
        contributions.append(job_apps.JOBS[job]['ranks'][rank]+': '+', '.join(k.replace('_',' ')+f' +{v:g}' for k,v in bonuses.items())+'. Strongest prior/current career counted once.')
    contributions.append('Narrative background: '+p['background']+'. No invented local relationships or completed work.')
    target = ('Lower D','Upper D','Lower C','Upper C','Lower / mid B','Upper B','Low A')[index]
    if not awakened:
        contributions.append('Physical conditioning: force ×'+str(scale['conditioning'][0])+', endurance ×'+str(scale['conditioning'][1])+'. No mana, master techniques or automatic Awakening.')
    employment = None
    if p['job']:
        job = job_apps.JOBS[p['job']]
        employment = dict(key=p['job'], rank=p['job_rank'], title=job['ranks'][p['job_rank']],
                          venue=job['venue'], hours=list(job['hours']), pay=job['pay']+p['job_rank']*100)
    rep, heat, _ = CRIME[p['crime']]
    if p['organisation'] in job_apps.progression.GANGS:
        rep = max(rep, job_apps.progression.GANGS[p['organisation']]['rep'])
    return dict(version=1, choices=p, experience=experience, target=target, stats=scale['stats'],
                conditioning=scale['conditioning'],
                stage=scale['stage'], arts=p['arts'], learned=learned, employment=employment,
                reputation=rep, heat=heat, contributions=contributions)


def experience_index(p):
    return max(EXPERIENCES.index(p['experience']),CRIME[p['crime']][2],BACKGROUND_EXPERIENCE.get(p.get('background'),0))


def apply(state):
    """Called by custom.create only. Existing stories never reseed origin state."""
    if state.get('character_origin') or 'origin' not in state['custom_protagonist']: return
    p = state['custom_protagonist']
    origin = resolve(p['origin'], p['awakened'], bool(p.get('awakening_trait')))
    state['character_origin'] = copy.deepcopy(origin)
    d = job_apps.ensure(state)
    job = origin['employment']
    if job:
        role = job_apps.profile(state,job['key'])
        _, craft, reliability = job_apps.LADDER[job['rank']]
        role.update(rank=job['rank'],craft=craft,reliability=max(50,reliability),
                    leadership=job['rank']*4, origin_experience=job_apps.LADDER[job['rank']][0])
        d['employment']=job['key']; state['world']['job']=job['title']
    choices=origin['choices']
    if choices['career_interest']:
        d['saved_jobs']=list(dict.fromkeys(d.get('saved_jobs',[])+[choices['career_interest']]))
    if choices['prior_job']:
        previous=job_apps.profile(state,choices['prior_job'])
        rank=choices['prior_rank']; _,craft,reliability=job_apps.LADDER[rank]
        previous.update(rank=max(previous['rank'],rank),craft=max(previous['craft'],craft),
                        reliability=max(previous['reliability'],reliability),
                        origin_experience=max(previous.get('origin_experience',0),job_apps.LADDER[rank][0]))
    for key in {choices['job'],choices['prior_job']}-{None}:
        role=job_apps.profile(state,key)
        rank=role['rank']
        # Recognised prior credentials are distinct from local paid project history.
        if rank>=2: role['certificates']=list(dict.fromkeys(role.get('certificates',[])+['craft']))
        if rank>=3:
            role['certificates']=list(dict.fromkeys(role['certificates']+['leadership']))
            role['origin_portfolio']=[dict(title='Recognised prior professional project',quality=3,origin=True)]
    d['reputation']=origin['reputation']; d['heat']=origin['heat']
    choices=origin['choices']; crime=choices['crime']; organisation=choices['organisation']
    if crime=='Small-crew founder':
        d['gang']=dict(name=choices['crew_name'],role='Founder',rank=0,standing=0,
                       members={},charter='Independent crew',assimilation={},origin=True)
    if crime in ('Trusted crew member','Crew lieutenant','Crew captain'):
        rank=('Trusted crew member','Crew lieutenant','Crew captain').index(crime)+1
        spec=job_apps.progression.GANGS[organisation]
        d['gang']=dict(id=organisation,name=spec['name'],role='Member',rank=rank,
                       standing=job_apps.progression.GANG_REVIEWS[rank][0],origin=True)
    if crime in ('Established faction member','Faction specialist','Faction field leader'):
        rank=('Established faction member','Faction specialist','Faction field leader').index(crime)+1
        faction,site,ranks=job_apps.BRANCHES[organisation]
        d['membership']=dict(faction=faction,branch=organisation,sponsor='@'+organisation.lower()+'-liaison',
                            rank=rank,assignments=0,strikes=0,origin=True,
                            origin_experience=job_apps.progression.REVIEWS[rank][0])
        d['invitations'][faction]=dict(status='accepted',minute=state['world']['minute'],origin=True)
    # Actual onboarding/recognition helpers see only the selected role.
    job_apps.ensure(state)
    # Fix the stage-entry clock and optional learned signature at story creation,
    # not at the first later visit to combat. Existing stories never enter here.
    profile=__import__('combat_profiles').profile(state,state['player'])
    if profile.get('origin_signature'):
        state['character_origin']['signature_id']=profile['origin_signature']
