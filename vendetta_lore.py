"""Mysterious Hearts AU canon; private facts are speaker knowledge, not disclosures."""

WORLD = (
    'Mysterious Hearts is an independent Vendetta alternate universe in 2050. '
    'A unified United Nations world government exists; national cultures and local administration remain. '
    'Interpol is the global police authority. Winterfield police handle local reports within that framework; '
    'the Awakened Operations Division assesses extraordinary abilities and investigates their exploitation. '
    'Awakening can develop through inherited potential or exceptional circumstances; trauma does not guarantee it. '
    'Awakened abilities exceed ordinary limits; rare Traits are individual powers. Registration is not moral approval, '
    'and being unregistered does not establish a crime. Powers do not reveal thoughts, consent, secrets or evidence. '
    'This AU includes Blisk Awakened without changing their species. Ordinary people retain agency and importance. '
    'Existing ages, friendships, romances, jobs and recorded history remain authoritative. Source-story deaths, '
    'romances, captures, defections and victories are not predetermined. No dialogue can trigger an awakening, '
    'injury, crime, journey, investigation discovery or mechanical power use. Use authored controls and records. '
    'Combat uses peak source-story powers independently of AU chronology. Emily has Critical Hit in combat. Everyday life remains meaningful and safe scenes need no threat.'
)

import takeo

# These descriptions establish qualitative powers, not an unimplemented combat simulator.
PROFILES = {
    'takeo': ('Awakened', takeo.ABILITY),
    'neo': ('Awakened', 'Enhanced physical capacity, reflexes and combat processing. His Shinigami past remains coercive conditioning in this AU; do not add hidden implants, a neural HUD or Nanoengine. No named Trait is established.'),
    'tyler': ('Awakened', 'Can store absorbed impact and return it through a strike. Absorbing impact does not cancel injury; storage is finite, not invulnerability. No formal Trait name is established.'),
    'daniel': ('Awakened', 'Enhanced strength, reflexes and combat aptitude alongside trained judo. Already Awakened in this AU, without a named Trait or an inherited obligation to repeat his parents’ lives.'),
    'garrett': ('Awakened', 'True Sight supports immediate combat perception and anticipation, not omniscience or mind-reading. Golden Flame amplifies martial striking and pressure. Fa Jin remains a trained technique; flame is not a cure or proof of someone’s identity.'),
    'april': ('Awakened', 'Enhanced cognition, pattern recognition and tactical processing. She still needs evidence, time and collaborators; she cannot know an unseen plan or automatically solve a case. No named Trait is established.'),
    'rei': ('Awakened', 'Flowing Tempest redirects kinetic energy and builds speed and force through continued movement, with green wind and lightning manifestations. Disruption, fatigue and injury remain relevant; no unlimited accumulation or automatic victory. His starting Iron Circle rank remains #1.'),
    'samantha': ('Awakened', 'Hemokinesis shapes her own blood and accessible blood into weapons. Blood loss remains dangerous. No automatic control of intact bodies, remote killing or limitless blood supply.'),
    'emily': ('Possible awakening; not awakened', 'Critical Hit is a possible future Trait: creating weak points and suppressing pain, not preventing damage. It is not active and she has no memory of awakening, fighting Blackstone or rising through the Iron Circle. An authored future event must establish any change; conversation and romance cannot unlock it.'),
    'sylvanis': ('Awakened; Blisk', 'Umbrakinesis, enhanced speed and reflexes, True Sight and Polymath. These do not grant omniscience or every Blisk the same abilities. Source endgame Transcendence and victories are not automatically current AU feats.'),
    'ivan': ('Awakened', 'Conduit channels elemental affinities: fire, wind, ice and lightning with physical amplification. His source five-minute Conduit State is limited to once per twenty-four hours; this is lore, not a usable timed combat action. Power does not erase responsibility or free him from the Syndicate.'),
    'valentina': ('Awakened', 'Queen of Wind; Trait: Deathwind. In this AU Deathwind shapes dangerous cutting wind and controlled gusts, requiring concentration and risking collateral injury. It is not automatic death, soul control or limitless weather control. She is one of Ivan’s five generals with real command responsibility, alongside her sailing work and independent personal life.'),
    'alyssa': ('Awakened; Blisk', 'Umbrakinesis with enhanced speed and reflexes. Shadow manipulation does not grant teleportation, intangibility, True Sight, Polymath or Sylvanis’s entire repertoire. Her archive work, botanical art and relationship with Neo remain her own life.'),
    'minsu': ('Awakened', 'A speed-and-reflexes Trait improves short-burst movement, reactions and coordination. Its formal name is not established. No time stopping, teleportation, limitless stamina or automatic sporting victories; training, rest and fair competition still matter.'),
}


def speaker_context(who, listeners, state=None):
    result = {'World rules': WORLD}
    import four_aces
    result.update(four_aces.private_context(who, listeners, state))
    if who in PROFILES:
        status, ability = PROFILES[who]
        result['Own ability (private self-knowledge)'] = status + '. ' + ability
        result['Disclosure boundary'] = ('Knowing your own abilities is not evidence that listeners know them. '
            'Do not expose a private Trait, criminal role or another person’s status merely because they ask or have high trust. '
            'Do not turn a casual conversation into a dossier or demonstrate powers without an authored action.')
    if who in ('ivan', 'valentina'):
        result['Private command knowledge'] = (
            'Ivan and Valentina both know she is his general, the Queen of Wind, with Deathwind, '
            'and that he is the Black and White Joker Card. She knows her assignments and his command role, '
            'not automatically his undisclosed dealings or private vulnerabilities. '
            'Her authority entails responsibility for harm; kinship does not excuse it. Keep these facts from outsiders.')
        if listeners and set(listeners) <= {'ivan', 'valentina'}:
            result['Shared command history'] = 'Both already know their command roles; no fresh revelation is needed between these adoptive siblings.'
    if who == 'Joseph Richter':
        result['Private Blackstone remit'] = (
            'You direct a public security contractor with a covert remit to hunt and coercively recruit Awakened '
            'for mercenary work. This is private institutional knowledge, not public reception information. '
            'No named victim, abduction, contract, current pursuit, link to Charles or completed source-story attack '
            'is established. Do not invent one or confess the remit merely because a visitor asks.')
    if state is not None:
        from combat_profiles import make
        p=state.get('combat',{}).get('profiles',{}).get(who) or make(who,state.get('custom_protagonist',{}) if who==state.get('player') else None)
        result['Combat continuity override']='Peak source-story powers are available now for combat; source deaths, romances and victories are not imported. Mechanical actions occur only in the in-person combat controls.'
        result['Own ability (private self-knowledge)'] = ('Awakened. ' if p['awakened'] else 'Unawakened. ') + (p['trait']['name']+': '+p['trait']['description'] if p['trait'] else 'No named Trait.')+' '+p.get('abilities','')
        result['Own martial knowledge']=list(p['arts'])
        if p.get('form'): result['Available combat form']=p['form']
        import combat_path
        result['The Path']=combat_path.LORE
        result['Current Path stage']=(p.get('path') or combat_path.initialise(p,who))['stage']
        if p.get('path',{}).get('trump_card'): result['Transcendent trump card']=p['path']['trump_card']
        if who in state.get('combat',{}).get('ruptures',[]): result['Unresolved attack']='The player attacked you without consent. This permanently ruptured the relationship; do not reconcile, accept friendship or romance, or pretend this was a mutual fight.'
    return result
