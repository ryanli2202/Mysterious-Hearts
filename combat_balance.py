"""MH-001 initial arena calibration, separate from competitive rank rewards.

These are authored numeric targets, not a claim of measured win rates. The
named roster's full hierarchy and temporary states require later calibration.
"""

# rank endpoints, combat band, legacy capability category, start/end stats
ARENA_BANDS = (
    (450, 301, 'D', 'unawakened', (0, 0, 8, 10), (0, 0, 36, 36)),
    (300, 101, 'C', 'awakened', (1, 0, 36, 36), (59, 0, 62, 62)),
    (100, 11, 'B', 'trait', (60, 1, 62, 62), (74, 80, 82, 82)),
    (10, 2, 'Low A', 'contender', (75, 81, 83, 83), (78, 88, 88, 88)),
)


def arena_profile(rank):
    # Legacy rank-one saves retain their title; their ordinary generated bouts
    # remain contender-strength until the explicit championship flow is added.
    rank=max(2, min(450, int(rank)))
    for bottom, top, band, category, start, end in ARENA_BANDS:
        if top <= rank <= bottom:
            fraction=(bottom-rank)/(bottom-top)
            values=tuple(round(a+(b-a)*fraction) for a,b in zip(start,end))
            return band, category, values
    raise ValueError('Unrecognised arena rank.')
# Independent authored expression: force, functional endurance, initiative, accuracy.
# No win/lose test reads tiers. Physical Nanoengine exceeds Sylvanis's raw output.
EXPRESSIONS={
 'sylvanis':(1.95,2.45,24,.12), 'takeo':(2.15,2.15,8,.03), 'crow':(1.70,2.05,26,.13),
 'ivan':(1.32,1.40,12,.04), 'charles':(1.23,1.30,14,.07),
 'garrett':(1.15,1.20,10,.04), 'rei':(1.23,1.35,12,.05), 'neo':(1.12,1.20,12,.04),
 'thirteen':(1.20,1.25,8,.02), 'daniel':(1.22,1.30,5,.02),
 'martos':(1.35,1.40,0,0), 'mavis':(1.13,1.10,18,.08), 'elias':(1.22,1.45,14,.03),
 'camila':(1.05,1.15,18,.12), 'fox':(1.10,1.20,16,.08), 'gordon':(1.23,1.20,7,.04),
 'tyler':(.88,1.10,0,0), 'samantha':(.90,1.00,0,0), 'Keisuke Hachimura':(.92,1.02,0,0),
 'emily':(.86,.95,2,.03), 'alyssa':(.88,1.,5,.02), 'minsu':(.84,.95,20,.05),
 'valentina':(.94,1.,3,.02), 'april':(.60,.70,4,.02),
}


def expression(p):
    if p.get('origin_conditioning'):
        return tuple(p['origin_conditioning'])
    if p.get('boss')=='richter': return (1.30,1.55,0,.02)
    if p.get('guard_kind'):
        return (.85,1.8 if p['stats']['awakened_power']==0 else 1.,0,0) if p.get('combat_band')=='C' else (.8,1.,0,0)
    return EXPRESSIONS.get(p.get('combat_id'),(1.,1.,0,0))

def configure_arena(p):
    """Bounded style mechanics, independent of generated claims and competitive title."""
    import combat_moves as moves
    art=next(iter(p['arts']))
    style=('redirection' if art in ('Judo','Aikido','Japanese Jujutsu') else
           'interception' if art in ('Taekwondo','Taido','Jeet Kune Do') else
           'pressure' if art in ('Boxing','Muay Thai','Kyokushin','MMA') else 'control')
    role,tags={'redirection':('counter',['precision']), 'interception':('attack',['speed']),
               'pressure':('combo',[]), 'control':('control',['restrain'])}[style]
    p['arena_style']=style
    p['arena_preview']=dict(style=style,strength='Bounded '+style+' through '+art,
        counterplay='Manage distance and resources; bait commitment, use cover or contest the opening.',
        rules='Individual ring assessment. Street weapons, terrain and coordinated groups change the matchup.')
    # Do not gate a large force increase on a band label. Progression is continuous.
    moves.initialise(p)
    if p.get('trait'):
        m=moves.spec('unique:arena:'+style,p['trait']['name']+' · '+style,
            'A bounded '+style+' application; no automatic hits, immunity or invented powers.',role,'unique','unique',art=art,tags=tags)
        m.update(mana=12,stamina=12,force=.90+p['stats']['trait_refinement']*.003,range=1)
        p['moveset']['unique']=[m]
    return p

# Shared MH-002 handoff. Values are authored numeric baselines, not historical
# progression awards. Creator UI/kit allocation remains owned by MH-002.
STARTING_EXPERIENCE={
    'Newcomer':('D',(18,12,12,14),'Awakening'),
    'Trained':('D',(25,22,36,36),'Awakening'),
    'Practised':('C',(38,42,60,50),'Ascension'),
    'Veteran':('C',(58,65,80,67),'Ascension'),
    'Field leader':('B',(65,78,83,78),'Totality'),
    'Seasoned field leader':('B',(74,86,86,86),'Totality'),
    'Exceptional Veteran':('Low A',(78,90,88,89),'Totality'),
}

# Physical conditioning does not grant mana, Awakening, master moves or forms.
# This is an origin expression on the existing resolver, not a second stat scale.
UNAWAKENED_CONDITIONING = ((1.,1.,0,0), (1.25,1.3,1,.01), (1.8,1.8,3,.02),
                          (2.5,2.5,5,.03), (3.2,3.2,7,.04), (3.7,3.8,9,.05), (4.1,4.3,11,.06))
CAREER_FOCUS = {
    'photographer':(.25,1,.25,1), 'model':(.5,.5,1,.5), 'librarian':(.25,1,.25,1),
    'oculus':(.25,.5,.25,1), 'cinema':(.5,1,.5,.75), 'barista':(.5,.75,.5,.75),
    'florist':(.5,1,.5,.5), 'chef':(.75,1,.75,.75), 'retail':(.5,.5,.5,1),
    'arcade':(.5,1,.5,1), 'gardener':(1,.5,1,.5), 'bartender':(.5,.75,.75,1),
}


def starting_scale(experience,awakened=True,has_trait=True):
    """Return the shared scale without modifying a save, rank, Path or movebook."""
    from combat_profiles import STATS
    if experience not in STARTING_EXPERIENCE: raise ValueError('Choose an authored experience package.')
    band,values,stage=STARTING_EXPERIENCE[experience]; values=list(values)
    if not awakened: values[0]=0
    if not awakened or not has_trait: values[1]=0
    return dict(version=1,experience=experience,target=band,stats=dict(zip(STATS,values)),
                conditioning=((1.08,1.06,2,.01) if experience=='Exceptional Veteran' else (1.,1.,0,0)) if awakened else UNAWAKENED_CONDITIONING[list(STARTING_EXPERIENCE).index(experience)],
                stage=stage if awakened else 'Dormancy',
                assumptions='Combine with the approved starting kit and conditioning; no automatic Trait, form, title or historical progression. Unawakened packages require physical-conditioning calibration rather than pretending mana potency is physical strength.')
