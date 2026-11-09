"""Criminal-world canon, faction baselines and compartmentalised knowledge."""
LAB = 'glasshouse_lab'
LAB_NAME = 'The Glasshouse · Sylvanis’s hidden laboratory'
INNER = frozenset(('crow', 'ivan', 'sylvanis', 'martos', 'elias', 'camila', 'mavis', 'charles'))
DOCTRINES = {
    'dragons': 'The Red Dragons are a Robin Hood-like gang: hear civilian grievances, defend residents against exploitation and return resources to the community. They refuse narcotics sales, including Blue Magic and Red Magic. Their hostility to both major factions comes from civilian exploitation, not a competing drug business.',
    'shinokami': 'The Shinokami operate militaristically: strict command, disciplined units, supply depots and territorial footholds. Their moderate working relationship with the Syndicate coexists with rivalry over territory and control of Winterfield. They regard expansion assistance as pragmatic cooperation and are unaware of any betrayal plan.',
    'syndicate': 'The Syndicate operates holistically across force, finance, intelligence, publicity, legitimate fronts and local gang relationships. Clubs, Hearts, Diamonds and Spades coordinate. Relations with Shinokami are moderately cooperative but contested over territory and control; relations with Red Dragons are hostile.',
}
DRUGS = ('Blue Magic is an underworld drug that temporarily awakens individuals for a few minutes, granting superhuman abilities before fading. It does not confer permanent Awakening or a guaranteed named Trait. Red Magic is more potent but causes more harmful side effects, including severe physical strain, disorientation and a dangerous crash. Blue Magic also carries strain and crash risks.')
SUPPLY = ('Sylvanis develops both drugs at the hidden Glasshouse laboratory and sells them to the Syndicate and local gangs. Red Dragons refuse narcotics and are excluded. Competition over supply and territory gives Sylvanis leverage while civilian harm fuels Red Dragons opposition. An individual gang member is not automatically a dealer or user.')
PLAN = ('The Crow plans to assist Shinokami expansion into Winterfield, build dependence on Syndicate support, then betray them for territory and control. This is a future plan, not a completed betrayal. Shinokami are unaware. The Crow directs strategy; Ivan coordinates cross-Suit support; Sylvanis develops both drugs, manages supply leverage and personally handles Syndicate relations with Takeo Mishima. The Crow sets strategy through Sylvanis rather than speaking to Mishima himself. Martos handles force and security, Elias publicity and influence, Camila financial dependencies, and Mavis intelligence and support. The Four Aces serve the Crow directly as specialists, not Suit commanders.')


def lab_access(who, state=None):
    import charles_quest
    return research_access(who,state) or charles_quest.guest(state,who)


def research_access(who, state=None):
    if state and who==state.get('player') and 'syndicate' in state.get('combat',{}).get('expelled',[]): return False
    if who in INNER: return True
    if not state or who != state.get('player'): return False
    member = state.get('job_apps', {}).get('membership') or {}
    return (member.get('faction') == 'Syndicate'
            and member.get('branch') in ('Clubs', 'Hearts', 'Diamonds', 'Spades')
            and member.get('rank', 0) >= 6 and member.get('strikes', 0) < 2)


def faction(who):
    if who in INNER or who == 'valentina': return 'syndicate'
    if who in ('takeo', 'thirteen', 'Keisuke Hachimura'): return 'shinokami'
    if who == 'garrett': return 'dragons'
    import gang_members, gang_leaders
    if who in gang_members.MEMBERS: return gang_members.MEMBERS[who]['gang']
    for key, spec in gang_leaders.LEADERS.items():
        if spec['name'] == who: return key
    return None


def context(who, listeners=(), state=None):
    affiliation = faction(who)
    if not affiliation: return {}
    result = {'Criminal-world theme': DRUGS,
              'Faction operations': DOCTRINES.get(affiliation, 'Local gangs negotiate supply and territory between larger powers. Sylvanis sells Blue Magic and Red Magic to local gangs; this does not establish a particular member as a dealer or user.'),
              'Rivalries': 'Red Dragons oppose Syndicate and Shinokami. Syndicate–Shinokami cooperation is moderate and fragile, with rivalry over territory and control.',
              'Simulation boundary': 'Qualitative story effects only; no inventory items or combat buffs. Never invent player consumption, activation, injury or manufacturing instructions. Preserve existing personalities and loyalties.',
              'Disclosure': 'Private criminal knowledge is not public proof. Do not volunteer it to civilians, invent completed operations or infer secrets from player allegations.'}
    if affiliation not in ('syndicate', 'shinokami'):
        result['Larger powers'] = 'Local gangs fear the Shinokami’s military strength and the Syndicate’s reach across force, finance and intelligence. Show guarded negotiation, caution over territory and reluctance to provoke either organisation. Fear does not mean automatic submission, membership or admiration; preserve Red Dragons civilian protection and refusal of narcotics. Do not force the player to feel fear or invent atrocities.'
    if affiliation in ('syndicate', 'shinokami'):
        result['Diplomatic liaison'] = 'Sylvanis manages Syndicate relations with Takeo Mishima directly. The Crow sets internal Syndicate strategy but does not talk to Mishima himself. Do not invent a completed meeting or agreement. This liaison reveals no confidential future strategy.'
    if who == 'sylvanis':
        result['Working routine'] = 'Spend most working hours developing Blue Magic and Red Magic in his private laboratory or coordinating at Syndicate headquarters. Handle Takeo relations personally; retain the established volatile, violent temperament.'
    if who in INNER:
        if listeners and all(research_access(person, state) for person in listeners):
            result['Private supply knowledge'] = SUPPLY
            result['Charles working cover'] = 'Charles Han is Sylvanis’s trusted laboratory associate and right-hand man. You know the working cover only, not his real motives or family history. Do not invent a discovered infiltration or inform Garrett of his location.'
        if listeners and all(person in INNER for person in listeners) and private_audience(state):
            result['Confidential strategy'] = PLAN
        else:
            result['Compartmentalisation'] = 'Defer confidential strategy until alone with authorised inner-circle colleagues. Laboratory supply details may be discussed only with personally cleared visitors or Syndicate Jacks in good standing.'
        if state and state.get('world', {}).get('location') == LAB:
            result['Current laboratory'] = 'Sylvanis runs this concealed research space, with locked research rooms and a private review desk for Blue Magic and Red Magic. No public reception or walk-in sales.'
    if state and private_audience(state):
        import laboratory_missions
        if record := laboratory_missions.context(state, who, listeners):
            result['Laboratory reviews'] = record
    return result


def baseline(source, target):
    import bubblegram_roles
    if source in {r['key'] for r in bubblegram_roles.ROLES.values()}: source = 'syndicate'
    source = 'syndicate' if source == 'joker' else source
    target = 'syndicate' if target == 'joker' else target
    pair = frozenset((source, target))
    if pair in (frozenset(('dragons', 'syndicate')), frozenset(('dragons', 'shinokami'))): return 15
    if pair == frozenset(('syndicate', 'shinokami')): return 55
    return 35


def laboratory_briefing(s):
    actor = s['world']['cast'][s['player']]
    if (not research_access(s['player'], s) or s['world']['location'] != LAB
            or actor['location'] != LAB or actor.get('journey')):
        raise ValueError('Review these records in person at the Glasshouse with Jack-rank or personal clearance.')
    if any(not lab_access(who, s) for who, person in s['world']['cast'].items()
           if person['location'] == LAB and not person.get('journey')):
        raise ValueError('Defer this private briefing while an uncleared listener is present.')
    text = DRUGS + '\n\n' + SUPPLY
    present = [who for who, person in s['world']['cast'].items()
               if person['location'] == LAB and not person.get('journey')]
    if s['player'] in INNER and private_audience(s):
        text += '\n\n' + PLAN
    return text


def reconcile_lab_access(s):
    world = s.get('world', {})
    for who, actor in world.get('cast', {}).items():
        if lab_access(who, s): continue
        if actor.get('location') == LAB or (actor.get('journey') or {}).get('destination') == LAB:
            actor.update(location='syndicate_office', journey=None, activity='At the public waterfront offices')
            if who == s['player']: world['location'] = actor['location']


def private_audience(state):
    if not state or state.get('world', {}).get('location') != LAB: return True
    world = state['world']
    return not world.get('npcs') and all(who in INNER for who, actor in world['cast'].items()
        if actor['location'] == LAB and not actor.get('journey'))
