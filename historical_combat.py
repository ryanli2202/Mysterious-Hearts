"""Isolated adult flashback kits, with current canonical combat capability.

Gameplay parity does not import present knowledge, earned Path history, equipment
or temporary forms, and does not establish an Awakening date in narrative canon.
"""
import copy

VERSION = 1
CONTEXTS = {
    'mavis': ('mavis-age20', {'MV-F02', 'MV-F04'}, 'mist'),
    'martos': ('martos-era-operative', {'MT-F01', 'MT-F02', 'MT-F04', 'MT-F05'}, 'rage'),
    'elias': ('elias-historical', {'EL-F03', 'EL-F04', 'EL-F05'}, 'flow'),
}


def strengthen(profile, who):
    """Install only canonical combat stats/abilities; retain the era identity."""
    import combat_profiles, combat_moves
    if profile.get('historical_capability_version', 0) >= VERSION:
        return False
    canonical = combat_profiles.make(who)
    from combat_balance import expression
    profile['historical_expression'] = list(expression(canonical))
    profile['awakened'] = True
    profile['trait'] = copy.deepcopy(canonical['trait'])
    # A playable awakened kit must not still display the old dormant baseline.
    # This is a gameplay floor, not present-day Path progress or a dated grant.
    import combat_path
    if profile.get('path', {}).get('stage') == combat_path.DORMANCY:
        profile['path']['stage'] = combat_path.AWAKENING
    for key, value in canonical['stats'].items():
        profile['stats'][key] = max(value, profile['stats'].get(key, 0))
    for art, value in canonical['arts'].items():
        profile.setdefault('arts', {})[art] = max(value, profile.get('arts', {}).get(art, 0))
    # Previously authored era disciplines remain usable at master proficiency.
    for art in profile['arts']:
        profile['arts'][art] = max(profile['arts'][art], canonical['stats']['martial_skill'])
    book = combat_moves.initialise(profile)
    for move in combat_moves.MOVES.values():
        if move['art'] in profile['arts'] and combat_moves.eligible(profile, move['tier']):
            if move['id'] not in book['learned']:
                book['learned'].append(move['id'])
    for field in ('unique', 'amplifications'):
        present = {entry['id'] for entry in book[field]}
        for entry in canonical['moveset'][field]:
            if entry['id'] not in present:
                book[field].append(copy.deepcopy(entry))
    profile['historical_capability_version'] = VERSION
    profile['basis'] = 'Adult historical combat kit: canonical capability; era identity and fixed history retained.'
    return True


def repair(s):
    """Upgrade a supported active session once, preserving damage and spending."""
    who = s.get('player')
    if who not in CONTEXTS:
        return False
    identity, missions, effect = CONTEXTS[who]
    item = s.get('ace_campaigns', {}).get(who, {}).get('session')
    if not isinstance(item, dict) or not item.get('historical') or item.get('mission') not in missions:
        return False
    nested = item.get('state', {})
    if nested.get('player') != who or not nested.get('ace_historical_context'):
        return False
    root = nested.get('combat', {})
    profile = root.get('profiles', {}).get(who)
    fight = root.get('active')
    if not profile or profile.get('combat_id') != identity:
        return False
    trait = profile.get('trait')
    if trait and trait.get('effect') != effect:
        return False
    if not trait and who != 'martos':
        return False
    if fight and (fight.get('status') != 'active' or not fight.get({'mavis':'ace_historical', 'martos':'martos_historical', 'elias':'elias_historical'}[who])):
        return False
    if not strengthen(profile, who):
        return False
    if fight:
        import combat
        capacities = combat.resources(profile)
        resources = fight['player']
        for value, maximum in (('health', 'max_health'), ('energy', 'max_energy')):
            spent = max(0, resources[maximum] - resources[value])
            old_value = resources[value]
            resources[maximum] = max(resources[maximum], capacities[maximum])
            resources[value] = (0 if value == 'health' and old_value <= 0
                                else max(0, resources[maximum] - spent))
    return True
