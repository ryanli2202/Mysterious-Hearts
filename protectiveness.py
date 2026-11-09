"""Protective reactions to romance, grounded in what each person has seen."""

PROTECTORS = {'yuriko': 'rei', 'emily': 'rei', 'april': 'garrett', 'valentina': 'ivan'}
DIRECTIONS = {
    'yuriko': 'Rei becomes more guarded with the player and protective of his younger sister Yuriko. He watches their intentions, asks direct questions and checks that she feels comfortable.',
    'emily': 'Rei becomes guarded and protective of his best friend Emily. He takes her feelings seriously, checks the player’s intentions and is wary of her being hurt.',
    'april': 'Garrett becomes protective of his childhood best friend April. His easy banter gains a watchful edge; he challenges careless intentions and checks how she is being treated.',
    'valentina': 'Ivan becomes protective of his adoptive sister Valentina and openly disapproves of the player pursuing her. Show cool scrutiny, pointed questions and restrained objections rather than immediate approval.',
}


def observe(s, target, activity, witnesses=(), *, physical=False):
    import town
    protector = PROTECTORS.get(target)
    if not protector or protector == s['player'] or not town.romanceable(s, target):
        return
    seen = protector in witnesses
    if physical:
        seen = seen or (town.present(s, target) and town.present(s, protector))
    if not seen:
        return
    records = s.setdefault('protectiveness', {})
    key = protector + ':' + target
    if key in records:
        return
    records[key] = dict(protector=protector, target=target, activity=activity,
                        minute=s['world']['minute'], source='witnessed firsthand',
                        approval=-25 if protector == 'ivan' else 0,
                        owners=list(set([s['player'], target, protector, *witnesses])))
    s['emotions'][protector] = 'guarded'
    town.relationship_notice(s, protector, protector.title() + ' has become protective of ' + target.title() + '.')


def context(s, who, listeners=None):
    """Conditional traits do not disclose an unwitnessed private relationship."""
    targets = [target for target, protector in PROTECTORS.items() if protector == who and who != s['player']]
    if not targets:
        return {}
    witnessed = []
    audience = set(listeners or [s['player']])
    for original in s.get('protectiveness', {}).values():
        if original['protector'] != who or not audience.issubset(original.get('owners', [s['player'], who, original['target']])):
            continue
        record = dict(original)
        if any(not audience.issubset(e.get('owners', [s['player'], who])) for e in record.get('evidence', [])):
            record.pop('approval', None)
            record.pop('evidence', None)
        witnessed.append(record)
    return dict(
        guidance=[DIRECTIONS[target] for target in targets],
        witnessed=witnessed,
        approval_direction='Approval grows through witnessed follow-through and respect, and falls through witnessed broken promises or crossed boundaries. Positive approval earns more ease; negative approval sharpens scrutiny. Ivan may respect the player while remaining reluctant about the romance. Do not infer approval from unseen private conduct.',
        rule='Apply these reactions when romance is witnessed, explicitly disclosed in the conversation, or already known from this speaker’s history. Do not infer romance from friendship, gifts or attraction scores, or invent knowledge of private dates. Protectiveness is concern, not automatic romantic jealousy. Respect her choices; do not veto her relationship, threaten the player or speak for her. Let trustworthy behaviour gradually ease guardedness without erasing the concern. Keep private knowledge private in groups.')
