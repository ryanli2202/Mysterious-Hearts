"""Peak-source combat canon. Numeric ratings except the top three are game balance."""
import combat_path

STATS = ('awakened_power', 'trait_refinement', 'martial_skill', 'fight_iq')
ARTS = {
    'Taekwondo': 'Distance, fast kicks, angle changes; vulnerable during committed kicks.',
    'Judo': 'Clinch, balance breaking and throws; requires contact and leverage.',
    'Kyokushin': 'Conditioned body strikes and low kicks; closing distance risks counters.',
    'MMA': 'Transitions between strikes, takedowns and ground control.',
    'Muay Thai': 'Elbows, knees, kicks and clinch control; manage range.',
    'Boxing': 'Jabs, combinations, slips and footwork; no automatic answer to grappling.',
    'Streetfighting': 'Improvised angles and rough close-range exchanges; less efficient technique.',
    'Sanda': 'Mobile striking, catches and throws.',
    'Jeet Kune Do': 'Interception, economy of motion and adaptable counters.',
    'Military CQC': 'Close control, disarming and efficient takedowns; requires position.',
    'Kickboxing': 'Punch-kick combinations and distance management.',
    'Silat': 'Off-angle entries, sweeps and joint control.',
    'Aikido': 'Redirection and balance manipulation; needs a committed attack.',
    'Taido': 'Changing body axes, evasive footwork and acrobatic attacks; costs stamina.',
    'Lethwei': 'Close striking including headbutts; risky exchanges.',
    'Japanese Jujutsu': 'Joint control, throws and submission positioning.',
    'Wing Chun': 'Centre-line control, short strikes and trapping in close range.',
    'Shinokami martial arts': 'Specialised conditioned interception and suppression techniques.',
    'Krav Maga': 'Direct defensive responses, close control and disengagement.',
    'Systema': 'Adaptive movement, breathing and close-range control.',
    'Kudo': 'Integrated striking, clinching and throws.',
}
TEACHERS = {
    'fox': ['Military CQC','Streetfighting','Krav Maga'],
    'gordon': ['Military CQC','MMA','Combat analysis'],
    'minsu': ['Taekwondo'], 'rei': ['Judo', 'Kyokushin'],
    'daniel': ['MMA', 'Muay Thai'], 'tyler': ['Boxing'], 'samantha': ['Streetfighting'],
    'garrett': ['Sanda', 'Jeet Kune Do'], 'neo': ['Military CQC'], 'martos': ['Military CQC'],
    'elias': ['Kickboxing'], 'mavis': ['Silat'], 'camila': ['Aikido'],
    'ivan': ['Judo', 'Kickboxing', 'Taekwondo', 'Taido', 'Lethwei'],
    'valentina': ['Taido'], 'april': ['Combat analysis'],
    'Keisuke Hachimura': ['Kyokushin', 'Japanese Jujutsu'],
    'charles': ['Sanda', 'Jeet Kune Do', 'Wing Chun'],
    'thirteen': ['Shinokami martial arts'], 'sylvanis': list(ARTS),
}
RATINGS = {
    'fox': (80,97,97,97), 'gordon': (85,97,95,98),
    'sylvanis': (90,100,100,100), 'takeo': (100,80,95,90), 'crow': (80,100,100,100),
    'charles': (85,94,97,96), 'garrett': (84,96,96,96), 'ivan': (86,94,96,95),
    'rei': (79,94,94,93), 'neo': (93,94,98,97), 'daniel': (87,90,97,94),
    'martos': (85,88,93,89), 'elias': (77,91,92,93), 'mavis': (75,95,95,96),
    'camila': (68,96,89,99), 'thirteen': (83,90,95,90),
    'Keisuke Hachimura': (72,0,91,87), 'tyler': (80,89,94,92),
    'samantha': (68,86,85,83), 'minsu': (61,79,91,82), 'valentina': (74,91,89,89),
    'april': (35,85,38,99), 'emily': (64,86,75,85), 'alyssa': (66,83,78,83),
}
# Learned Traits have resource costs and tactical identities, never stat unlock gates.
TRAITS = {
    'neo': ('Shinigami Protocol', 'Reactive combat processing, adaptation and informed tactical choices within physical and resource limits. No hidden implants, neural HUD or Nanoengine.', 'analysis'),
    'thirteen': ('Shinigami Protocol', 'Reactive combat processing and adaptation paired with specialised martial training. Available information and feasible movement limit responses.', 'analysis'),
    'daniel': ('War God', 'Coordinated physical pressure, instinctive transitions and contact reading; not mind-reading or automatic takedowns. Shares his father’s Trait, not an assumed full repertoire.', 'physical'),
    'april': ('Polymath', 'Enhanced cognition, pattern recognition and tactical synthesis from observed evidence. Requires information and preparation; does not grant physical mastery or omniscience.', 'analysis'),
    'fox': ('Eight Senses', 'Track sound, scent, heartbeat, vibration and air displacement; fight in darkness and counter ambushes. Physical perception, not mind-reading or automatic identity proof.', 'senses'),
    'gordon': ('Biocreation', 'Grow biological handguns, rifle-like constructs, high-impact rounds and adaptive components. Powerful fire uses finite mana; no external ammunition dependency or guaranteed hit.', 'biocreation'),
    'garrett': ('True Sight / Golden Flame', 'See pure mana and magical flow with near-perfect application efficiency; precognition, reflexes, speed and strength reinforcement remain physically bounded. Golden Flame reinforces martial pressure; no mind-reading or infinite energy.', 'flame'),
    'rei': ('Flowing Tempest', 'Redirect kinetic force; sustained motion builds momentum. Interruptions and exhaustion break accumulation.', 'flow'),
    'sylvanis': ('True Sight / Polymath / Umbrakinesis', 'Pure-mana perception and efficient Awakened application with precognition; Polymath synthesises observed evidence; shape shadows. Second-stage Transcendence creates corrosive, burning, explosive or piercing shadows even in absolute light.', 'shadow'),
    'takeo': ('Nanoengine', 'Internal nanomachines reinforce strength and armour and form adaptive weapons. No limitless energy or invulnerability.', 'armour'),
    'crow': ('Polymath', 'Exceptional analysis, learning and tactical prediction from available evidence; no omniscience.', 'analysis'),
    'ivan': ('Conduit', 'Red lightning amplifies attack power; blue lightning movement speed; fire physical strength; ice reaction and Tranquility; wind soul injury and Misanthropy continued-function endurance. Instant reaction does not remove travel time. Full Conduit State: five minutes once per 24 hours.', 'elemental'),
    'charles': ('True Sight / White Flame Tiger', 'Pure-mana perception grants precognition, efficient Awakened application and heightened reflexes; white-flame tiger manifestation reinforces refined martial pressure. Finite energy and physical travel time remain.', 'flame'),
    'martos': ('Rage', 'Pressure increases force and durability; overmutation sacrifices control and precision.', 'rage'),
    'elias': ('Pyromovement', 'Movement accumulates heat for strikes and trails; restraint breaks accumulation.', 'flow'),
    'mavis': ('Mist', 'Dark-vapour evasion and infiltration; bright light and finite energy constrain dispersal.', 'mist'),
    'camila': ('Analysis', 'Perceive minuscule and microscopic changes and visualise branching possibilities from observations. Branches are not guaranteed futures or mind-reading.', 'analysis'),
    'samantha': ('Hemokinesis', 'Shape accessible blood into weapons; own blood costs health. No automatic control of intact bodies.', 'blood'),
    'tyler': ('Impact storage', 'Absorb and return finite impact; taking damage still causes injury.', 'impact'),
    'minsu': ('Speed and reflexes', 'Short movement and reaction bursts; no time stop or teleportation.', 'speed'),
    'valentina': ('Deathwind', 'Deathwind was provided by Ivan as an extension of his wind, inheriting soul injury and Misanthropy continued-function endurance. Cutting gusts require resources; no automatic death, regeneration, other elements or limitless weather.', 'wind'),
    'emily': ('Critical Hit', 'Create weak points; pain immunity never prevents damage or knockout.', 'critical'),
    'alyssa': ('Umbrakinesis', 'Shadow manipulation and heightened reflexes; no inherited access to Sylvanis’s other powers.', 'shadow'),
}
FORMS = {'garrett': 'Transcendence', 'charles': 'Transcendence',
         'sylvanis': 'Second-stage Transcendence', 'ivan': 'Conduit State'}

def make(who, custom=None):
    custom = custom or {}
    awakened = who in RATINGS or bool(custom.get('awakened'))
    values = RATINGS.get(who, (18,12,12,14) if awakened else (0,0,8,10))
    trait = TRAITS.get(who)
    if custom.get('awakened') and custom.get('awakening_trait'):
        trait = (custom['awakening_trait'], custom.get('awakening_description',''), 'custom')
    styles = {art: values[2] for art in TEACHERS.get(who, []) if art in ARTS}
    extras = {'rei': ['Aikido'], 'garrett': ['Wing Chun'], 'daniel': ['Judo','Krav Maga','Systema','Military CQC'],
              'ivan': ['Muay Thai','Kudo'],
              'takeo': ['Military CQC'], 'crow': list(ARTS)}
    styles.update({art: values[2] for art in extras.get(who, [])})
    abilities={'neo':'Shinigami Protocol: reactive combat processing and elite instincts. Does not grant Nanoengine or hidden implants.',
               'garrett':'Fa Jin internal-force striking, True Sight, Golden Flame and peak Transcendence.',
               'thirteen':'Shinigami Protocol, experimental conditioning and specialised martial arts.',
               'daniel':'War God: coordinated physical pressure and instinctive battle aptitude.',
               'april':'Polymath: enhanced cognition, pattern recognition and tactical processing.'}
    result=dict(name=custom.get('name', who), awakened=awakened, stats=dict(zip(STATS, values)),
                arts=styles, trait=dict(zip(('name','description','effect'), trait)) if trait else None,
                form=FORMS.get(who), abilities=abilities.get(who,''), basis='Peak source strength; numerical game balance')
    result['lore_revision']=2
    result['identity_version']=1
    result['combat_id']=who
    result['mana_potential']=custom.get('mana_potential',True)
    if custom.get('origin'):
        import character_origins
        origin = character_origins.resolve(custom['origin'], awakened, bool(trait))
        result['stats'] = origin['stats']
        result['origin_conditioning'] = origin['conditioning']
        result['arts'] = {art: origin['stats']['martial_skill'] for art in origin['arts']}
        result['basis'] = 'Reviewed starting choices · shared MH-001 scale'
        combat_path.initialise(result, who, stage=origin['stage'])
        result['moveset'] = dict(version=1, learned=list(origin['learned']), arts=list(origin['arts']),
                                 amplifications=__import__('copy').deepcopy(custom.get('trait_amplifications', [])), unique=[], origin_version=1)
    combat_path.initialise(result,who)
    import combat_moves
    combat_moves.initialise(result,who,custom)
    if custom.get('specialisation'):
        __import__('creator_combat').specialise(result,custom['specialisation'])
    if custom.get('starting_signature'):
        skill=__import__('creator_combat').validate_signature(custom,custom['starting_signature'],result)
        result['moveset']['unique'].append(skill)
        result['origin_signature']=skill['id']
    return result


def reconcile_identity(p, who):
    """Add confirmed Traits once, preserving earned refinement and learned moves.

    No resource refill, Path reset or signature replacement. Only the former
    traitless canonical defaults are migrated; custom Traits remain authoritative.
    """
    p.setdefault('combat_id',who)
    if p.get('lore_revision',0)<2:
        canonical=TRAITS.get(who)
        existing=p.get('trait')
        if canonical and existing and existing.get('effect')!='custom':
            existing.update(name=canonical[0],description=canonical[1])
        p['lore_revision']=2
    if p.get('identity_version', 0) >= 1:
        return
    if who in ('neo', 'thirteen', 'daniel', 'april') and not p.get('trait'):
        p['trait']=dict(zip(('name','description','effect'), TRAITS[who]))
        p['stats']['trait_refinement']=max(p['stats'].get('trait_refinement',0), RATINGS[who][1])
        p['abilities']={
            'neo':'Shinigami Protocol: reactive combat processing and elite instincts. No hidden implants or Nanoengine.',
            'thirteen':'Shinigami Protocol, experimental conditioning and specialised martial arts.',
            'daniel':'War God: coordinated physical pressure and instinctive battle aptitude.',
            'april':'Polymath: enhanced cognition, pattern recognition and tactical processing.',
        }[who]
        book=p.get('moveset')
        if book is not None and not book.get('amplifications'):
            import combat_moves
            book['amplifications']=[dict(id='amp:established',name=p['trait']['name'],
                description=p['trait']['description'],aspect=p['trait']['name'],role='Trait reinforcement',
                tags=['precision'],compatible=list(combat_moves.ROLES),mana=8,
                environment='Contact force against arena objects.')]
    p['identity_version']=1

def profile(s, who):
    root = s.setdefault('combat', {})
    root.setdefault('path_epoch',s['world']['minute'])
    profiles = root.setdefault('profiles', {})
    if who not in profiles:
        custom = s.get('custom_protagonist', {}) if who == s.get('player') else {}
        profiles[who] = make(who, custom)
        import game_core
        profiles[who]['name']=custom.get('name') or game_core.CONTACTS.get(who,(who,))[0]
    reconcile_identity(profiles[who],who)
    combat_path.initialise(profiles[who],who,root['path_epoch'])
    import combat_moves
    combat_moves.initialise(profiles[who],who,s.get('custom_protagonist') if who==s.get('player') else None)
    return profiles[who]
