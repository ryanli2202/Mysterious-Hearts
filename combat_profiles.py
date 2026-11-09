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
    'rei': (79,94,94,93), 'neo': (93,0,98,97), 'daniel': (87,0,97,94),
    'martos': (85,88,93,89), 'elias': (77,91,92,93), 'mavis': (75,95,95,96),
    'camila': (68,96,89,99), 'thirteen': (83,0,95,90),
    'Keisuke Hachimura': (72,0,91,87), 'tyler': (80,89,94,92),
    'samantha': (68,86,85,83), 'minsu': (61,79,91,82), 'valentina': (74,91,89,89),
    'april': (35,0,38,99), 'emily': (64,86,75,85), 'alyssa': (66,83,78,83),
}
# Each trait has an actual cost, complexity gate and tactical identity in combat.py.
TRAITS = {
    'fox': ('Eight Senses', 'Track sound, scent, heartbeat, vibration and air displacement; fight in darkness and counter ambushes. Physical perception, not mind-reading or automatic identity proof.', 'senses'),
    'gordon': ('Biocreation', 'Grow biological handguns, rifle-like constructs, high-impact rounds and adaptive components. Powerful fire uses finite mana; no external ammunition dependency or guaranteed hit.', 'biocreation'),
    'garrett': ('True Sight / Golden Flame', 'Predict immediate movement; golden fire reinforces striking, defence and mobility. No mind-reading.', 'flame'),
    'rei': ('Flowing Tempest', 'Redirect kinetic force; sustained motion builds momentum. Interruptions and exhaustion break accumulation.', 'flow'),
    'sylvanis': ('True Sight / Polymath / Umbrakinesis', 'Predictive perception and rapid analysis; shape shadows. Second-stage Transcendence creates corrosive, burning, explosive or piercing shadows even in absolute light.', 'shadow'),
    'takeo': ('Nanoengine', 'Internal nanomachines reinforce strength and armour and form adaptive weapons. No limitless energy or invulnerability.', 'armour'),
    'crow': ('Polymath', 'Exceptional analysis, learning and tactical prediction from available evidence; no omniscience.', 'analysis'),
    'ivan': ('Conduit', 'Fire, wind, ice and red/blue lightning with physical amplification. Full Conduit State: five minutes once per 24 hours.', 'elemental'),
    'charles': ('White Flame Tiger', 'Transcendent white-flame tiger manifestation reinforces highly refined martial pressure.', 'flame'),
    'martos': ('Rage', 'Pressure increases force and durability; overmutation sacrifices control and precision.', 'rage'),
    'elias': ('Pyromovement', 'Movement accumulates heat for strikes and trails; restraint breaks accumulation.', 'flow'),
    'mavis': ('Mist', 'Dark-vapour evasion and infiltration; bright light and finite energy constrain dispersal.', 'mist'),
    'camila': ('Analysis', 'Read observed patterns and anticipate likely choices; requires evidence.', 'analysis'),
    'samantha': ('Hemokinesis', 'Shape accessible blood into weapons; own blood costs health. No automatic control of intact bodies.', 'blood'),
    'tyler': ('Impact storage', 'Absorb and return finite impact; taking damage still causes injury.', 'impact'),
    'minsu': ('Speed and reflexes', 'Short movement and reaction bursts; no time stop or teleportation.', 'speed'),
    'valentina': ('Deathwind', 'Concentrated cutting wind and gusts; not automatic death or limitless weather.', 'wind'),
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
    abilities={'neo':'Peak Shinigami Protocol: neural combat optimisation, elite instincts and AI-assisted movement. Does not grant Nanoengine.',
               'garrett':'Fa Jin internal-force striking, True Sight, Golden Flame and peak Transcendence.',
               'thirteen':'Shinigami experimental conditioning and specialised martial arts.',
               'daniel':'Peak awakened physical potential and instinctive battle aptitude.',
               'april':'Enhanced cognition, pattern recognition and tactical processing.'}
    result=dict(name=custom.get('name', who), awakened=awakened, stats=dict(zip(STATS, values)),
                arts=styles, trait=dict(zip(('name','description','effect'), trait)) if trait else None,
                form=FORMS.get(who), abilities=abilities.get(who,''), basis='Peak source strength; numerical game balance')
    result['mana_potential']=custom.get('mana_potential',True)
    combat_path.initialise(result,who)
    return result

def profile(s, who):
    root = s.setdefault('combat', {})
    root.setdefault('path_epoch',s['world']['minute'])
    profiles = root.setdefault('profiles', {})
    if who not in profiles:
        custom = s.get('custom_protagonist', {}) if who == s.get('player') else {}
        profiles[who] = make(who, custom)
        import game_core
        profiles[who]['name']=custom.get('name') or game_core.CONTACTS.get(who,(who,))[0]
    combat_path.initialise(profiles[who],who,root['path_epoch'])
    return profiles[who]
