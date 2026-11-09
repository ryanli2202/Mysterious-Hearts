"""Authored adult character orientations, independent of affection and consent."""
import custom_protagonist

CANON = {
    'martos': ('Men', 'Straight'), 'elias': ('Men', 'Bisexual'),
    'mavis': ('Women', 'Bisexual'), 'camila': ('Women', 'Lesbian'),
    'rei': ('Men', 'Straight'), 'garrett': ('Men', 'Straight'),
    'ivan': ('Men', 'Bisexual'), 'minsu': ('Men', 'Straight'),
    'emily': ('Women', 'Straight'), 'sophie': ('Women', 'Bisexual'),
    'amy': ('Women', 'Bisexual'), 'samantha': ('Women', 'Bisexual'),
    'april': ('Women', 'Straight'), 'yuriko': ('Women', 'Straight'),
    'lena': ('Women', 'Straight'), 'naomi': ('Women', 'Lesbian'),
    'celeste': ('Women', 'Bisexual'), 'valentina': ('Women', 'Bisexual'),
    'dev': ('Men', 'Bisexual'), 'elliot': ('Men', 'Gay'),
    'tyler': ('Men', 'Bisexual'), 'daniel': ('Men', 'Gay'),
    'rosa': ('Women', 'Straight'), 'neo': ('Men', 'Straight'),
    'alyssa': ('Women', 'Bisexual'), 'sylvanis': ('Men', 'Straight'),
    'Theo': ('Men', 'Gay'), 'Noah': ('Men', 'Bisexual'), 'Leo': ('Men', 'Straight'),
}


def attracted_to(actor, other):
    if actor == other or actor not in CANON or other not in CANON:
        return False
    gender, orientation = CANON[actor]
    target_gender = CANON[other][0]
    return (orientation in ('Bisexual', 'Pansexual') or
            orientation == 'Straight' and {gender, target_gender} == {'Men', 'Women'} or
            orientation in ('Gay', 'Lesbian') and gender == target_gender)


def compatible(first, second):
    return attracted_to(first, second) and attracted_to(second, first)


def reason(player, who):
    if player not in CANON or who not in CANON: return ''
    if who in CANON and not attracted_to(who, player):
        return f'{who.title()} is {CANON[who][1].lower()} and is not attracted to your gender.'
    if player in CANON and not attracted_to(player, who):
        return f'{custom_protagonist.display_name(player)} is {CANON[player][1].lower()}; this pairing is outside their canonical attraction.'
    return ''


def direction(player, members):
    import romantic_types
    import romantic_voice
    people = list(dict.fromkeys([player, *members]))
    facts = '; '.join(f'{who}: {CANON[who][1].lower()}' for who in people if who in CANON)
    return ('Canonical sexual orientations: '+facts+'. These identities are fixed, not inferred from appearance, '
            'hobbies or personality. Attraction is not consent. Never change orientation because of persistence, '
            'gifts, trust, attraction scores or past generated dialogue. '
            'When an advance is outside the recipient’s attraction, decline clearly in their own voice; '
            'do not imply they can be persuaded or need more trust. Friendly affection and compliments remain possible. '
            'Public contact-profile sexuality is an explicit disclosure; do not invent additional private sexual history. '
            'Apply these orientations to every pair in a group, not only the speaker and player. '
            + ' '.join(reason(player, who) for who in members if who in CANON and not compatible(player, who))
            + romantic_types.direction(player, members)
            + romantic_voice.direction(player, members))


def reconcile(s):
    """Keep old conversations and bond history, retiring incompatible romance state."""
    if s.get('sexuality_canon_version') != 1:
        # Cached, unsent suggestions from old saves are not character history.
        chats = [(who, chat) for key in ('routes','npc_chats') for who, chat in s.get(key, {}).items()]
        chats += [(None, group) for group in s.get('groups', {}).values()
                  if not any(compatible(s['player'], who) for who in group.get('members', []))]
        for who, chat in chats:
            if who is None or who in CANON and not compatible(s['player'], who):
                for key in ('choices','personal_choices','action_choices'): chat[key] = []
                chat['suggestions_deferred'] = True
                chat['suggestions_requested'] = []
        s['sexuality_canon_version'] = 1
    for who, bond in s.get('relationships', {}).items():
        if who in CANON and not compatible(s['player'], who):
            bond['attraction'] = 0
            if bond.get('status') in ('dating', 'official', 'strained', 'mutual interest'):
                bond.setdefault('orientation_history', []).append(dict(status=bond['status'], reason=reason(s['player'], who)))
                bond['status'] = 'friends'
    for who, bond in s.get('friendships', {}).items():
        if 'attraction' in bond and who in CANON and not compatible(s['player'], who): bond['attraction'] = 0
    session = s.get('date_session')
    if session and session.get('partner') in CANON and not compatible(s['player'], session['partner']):
        s.setdefault('orientation_ended_dates', []).append(s.pop('date_session'))
