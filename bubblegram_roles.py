"""Established playable Syndicate desks, separate from newcomer sponsorship.

Aces are mission specialists, never the commanders of their namesake Suits.
Budgets are one-time game operating reserves, not personal funds or canon wealth.
"""
ROLES = {
    'sylvanis': dict(key='coloured_joker', name='Coloured Joker network', role='Coloured Joker · second-in-command',
        authority='Senior command · cross-Suit authority', budget=60000, venue='syndicate_hq',
        title='Cross-Suit obligation review', brief='Contradictory branch reports require your decision. Challenge the accounts without treating a report as proof of a completed operation.'),
    'valentina': dict(key='wind_general', name='Queen of Wind field command', role='Queen of Wind · Ivan’s general',
        authority='Clubs field command at Breakwater; no cross-Suit command', budget=30000, venue='site_04_briefing',
        title='Breakwater field review', brief='Two field teams dispute their responsibilities. Review the handover within your Clubs command; other Suits retain their own leadership.'),
    'martos': dict(key='ace_clubs', name='Ace of Clubs mission desk', role='Ace of Clubs · mission specialist',
        authority='Cardmaster-assigned mission specialist, not Clubs commander', budget=20000, venue='site_04_briefing',
        title='Protection mandate review', brief='A protection assignment has conflicting responsibility records. Verify the assigned scope; being an Ace does not make you the Clubs commander.'),
    'elias': dict(key='ace_hearts', name='Ace of Hearts mission desk', role='Ace of Hearts · mission specialist',
        authority='Cardmaster-assigned mission specialist, not Hearts commander', budget=18000, venue='site_05_briefing',
        title='Influence mandate review', brief='A private campaign brief exceeds its agreed mandate. Decide how to resolve the dispute without assuming command of Hearts.'),
    'camila': dict(key='ace_diamonds', name='Ace of Diamonds mission desk', role='Ace of Diamonds · mission specialist',
        authority='Cardmaster-assigned mission specialist, not Diamonds commander', budget=25000, venue='site_06_briefing',
        title='Financial mandate review', brief='An assigned financial review contains contradictory figures. Resolve the commission within the documented mandate; Diamonds leadership remains separate.'),
    'mavis': dict(key='ace_spades', name='Ace of Spades mission desk', role='Ace of Spades · mission specialist',
        authority='Cardmaster-assigned mission specialist, not Spades commander', budget=18000, venue='site_08_briefing',
        title='Information mandate review', brief='Two sources disagree about the scope of a private assignment. Preserve uncertainty and clarify the authorised task without claiming command of Spades.'),
}


def sync(s, d):
    if 'syndicate' in s.get('combat',{}).get('expelled',[]):
        d['affiliations']=[]; d.pop('story_membership',None); d.pop('syndicate_role',None)
        d.pop('leadership',None)
        return
    spec = ROLES.get(s['player'])
    if not spec: return
    d['affiliations'] = ['Syndicate', spec['name']]
    d['syndicate_role'] = spec['role']
    d['story_membership'] = dict(faction='Syndicate', role=spec['role'], authority=spec['authority'])
    if not d.get('playable_syndicate_role_v1'):
        if d.get('membership'):
            d.setdefault('prior_sponsorships', []).append(d['membership'])
            d['membership'] = None
            if (d.get('pending') or {}).get('kind') == 'faction':
                d.setdefault('prior_assignments', []).append(d['pending'])
                d['pending'] = None
        if d.get('gang'):
            d.setdefault('gang_archive', []).append(d['gang'])
        desk = dict(id=spec['key'], name=spec['name'], role=spec['role'], standing=40,
                    rank=3, established=True, mission_desk=True)
        d['leadership'] = dict(desk)
        d['gang'] = dict(desk)
        d['playable_syndicate_role_v1'] = True


def mandate(who):
    spec = ROLES.get(who)
    return (spec['key'], spec['name'], spec['role'], spec['budget']) if spec else None


def contract(s, key, original):
    spec = ROLES.get(s['player'])
    if not spec or key not in ('crew', 'network', 'leadership'): return original
    return {**original, 'title': spec['title'] if key == 'leadership' else spec['role'] + ' · ' + original['title'],
            'alias': '@' + spec['key'].replace('_', '-'), 'venue': spec['venue'], 'brief': spec['brief']}
