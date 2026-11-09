"""Evidence-backed commitments, boundaries, repair, loyalties and invitations."""
import protectiveness

KINDS = ('promise', 'kept', 'broken', 'boundary', 'respected', 'crossed',
         'acknowledge', 'changed', 'forgive', 'loyalty', 'proposal', 'accept', 'decline', 'disclosure')


def ensure(s):
    return s.setdefault('relationship_dynamics', {'people': {}, 'next_id': 1})


def person(s, who):
    return ensure(s)['people'].setdefault(who, dict(promises=[], boundaries=[],
        repair={}, proposals=[], loyalties=[], evidence=[]))


def peek(s, who):
    return s.get('relationship_dynamics', {}).get('people', {}).get(who,
        dict(promises=[], boundaries=[], repair={}, proposals=[], loyalties=[], evidence=[]))


def stats(s, who):
    return (s.get('relationships', {}).get(who) or s.get('friendships', {}).get(who)
            or s.get('npc_chats', {}).get(who, {}).get('connection') or {})


def adjust(s, who, amount):
    r = stats(s, who)
    if r:
        r['trust'] = max(0, min(100, r.get('trust', 0) + amount))


def approval(s, who, amount, owners, reason):
    protector = protectiveness.PROTECTORS.get(who)
    record = s.get('protectiveness', {}).get(f'{protector}:{who}')
    if not record or protector not in owners or protector == s['player']:
        return
    record['approval'] = max(-100, min(100, record.get('approval', -25 if protector == 'ivan' else 0) + amount))
    record.setdefault('evidence', []).append(dict(reason=reason, minute=s['world']['minute'], owners=owners))
    record['evidence'] = record['evidence'][-12:]


def hurt(s, who, reason):
    p = person(s, who)
    p['repair'] = dict(harm=reason, since=s['world']['minute'], acknowledged=False, changed_days=[])
    r = stats(s, who)
    if r:
        r['unresolved_harm'] = reason
        if r.get('status') == 'official':
            r['status'] = 'strained'


def tick(s):
    for who, p in s.get('relationship_dynamics', {}).get('people', {}).items():
        for promise in p['promises']:
            if promise['status'] == 'open' and promise['due'] is not None and s['world']['minute'] > promise['due']:
                promise['status'] = 'overdue'
                # Time alone is not evidence that a third party learned anything.
                adjust(s, who, -4)
                hurt(s, who, 'Missed promise: ' + promise['detail'])


def repair_ready(s, who):
    if who in s.get('combat',{}).get('ruptures',[]): return False
    repair = peek(s, who)['repair']
    return bool('resolved' not in repair and stats(s, who).get('unresolved_harm') == repair.get('harm')
                and repair.get('acknowledged') and repair.get('changed_days')
                and max(repair['changed_days']) > repair.get('acknowledged_day', s['world']['minute']//1440))


def proposal_allowed(s, who):
    import town
    r = stats(s, who)
    p = peek(s, who)
    return bool(town.romanceable(s, who) and r and r.get('trust', 0) >= 60
                and r.get('closeness', 0) >= 45 and not r.get('unresolved_harm')
                and not s.get('date_session') and not any(v['status'] == 'open' for v in p['proposals'])
                and (not p['proposals'] or s['world']['minute'] - p['proposals'][-1]['minute'] >= 4320))


def add_schema(schema, s, members):
    props = {
        'kind': {'type': 'string', 'enum': list(KINDS)},
        'who': {'type': 'string', 'enum': list(members)},
        'source': {'type': 'string', 'enum': [s['player'], *members]},
        'quote': {'type': 'string'}, 'detail': {'type': 'string'},
        'ref': {'type': 'integer'}, 'due_minutes': {'type': 'integer', 'minimum': -1, 'maximum': 43200},
        'proposal_type': {'type': 'string', 'enum': ['none', 'date', 'introduction', 'relationship_talk']},
    }
    schema['properties']['relationship_events'] = {'type': 'array', 'maxItems': 3, 'items': {
        'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}}
    schema['required'].append('relationship_events')
    return (' Return relationship_events (or []) only for explicit events in this delivered exchange. '
            'who is the affected present contact; source is the actual speaker; quote is an exact substring of '
            'their delivered words or submitted player action. Never use narration, unsent choices, hypotheticals or guesses. '
            'promise records a concrete player commitment, detail its terms, due_minutes the explicitly agreed delay '
            'from the current minute (-1 when no exact deadline is agreed). Do not invent deadlines. '
            'kept/broken refer to an existing promise ID, with evidence of actual follow-through/failure, not a new promise. '
            'boundary records the contact’s explicit personal preference about affection, teasing, gifts or questions; '
            'respected/crossed refer to an existing boundary ID and actual player conduct. '
            'acknowledge means the player owns the specific recorded harm; changed means concrete corrective conduct; '
            'forgive means the contact freely forgives after repair_ready is true. An apology alone is not changed behaviour. '
            'loyalty records a contact explicitly addressing tension between friendship/family and the player, without '
            'dictating anyone’s decision. proposal means the contact initiates a date, introduction or relationship talk '
            'when proposal_allowed is true; detail is the concrete proposal and proposal_type is date, introduction '
            'or relationship_talk (none for other event kinds). accept/decline refer to a proposal ID '
            'and an explicit player response. Accepting records willingness only; use existing date/exclusivity steps '
            'to arrange an actual date or commitment. '
            'disclosure means the player explicitly tells a protector about their own romance with one of the protected '
            'people; detail must be that person’s exact character key. Otherwise ref is 0 and due_minutes is -1. '
            'Use individual preferences and voices, never universal boundaries or automatic consent.')


def commit(s, data, spoken, player_text='', owners=None):
    tick(s)
    owners = list(dict.fromkeys(owners or [s['player'], *spoken]))
    lines = {**spoken, s['player']: player_text or ''}
    events = data.get('relationship_events', [])
    if not isinstance(events, list):
        return
    for event in events[:3]:
        if not isinstance(event, dict):
            continue
        kind, who, source, quote, detail = (event.get(k) for k in ('kind', 'who', 'source', 'quote', 'detail'))
        import character_types
        if not character_types.is_major(who): continue
        ref, due = event.get('ref', 0), event.get('due_minutes', -1)
        if not all(isinstance(v, str) for v in (kind, who, source, quote, detail)):
            continue
        if (kind not in KINDS or who not in spoken or source not in (s['player'], who)
                or not isinstance(quote, str) or not 3 <= len(quote) <= 600 or quote not in lines[source]
                or not isinstance(detail, str) or not 1 <= len(detail) <= 350
                or type(ref) is not int or type(due) is not int or not -1 <= due <= 43200):
            continue
        if kind in ('boundary', 'proposal', 'loyalty', 'forgive') and source != who:
            continue
        if kind in ('promise', 'acknowledge', 'disclosure', 'accept', 'decline') and source != s['player']:
            continue
        p = person(s, who)
        fingerprint = [kind, source, quote, ref]
        if fingerprint in p['evidence']:
            continue
        now = s['world']['minute']
        collection = p['promises'] if kind in ('kept', 'broken') else p['boundaries'] if kind in ('respected', 'crossed') else p['proposals']
        item = next((v for v in collection if v['id'] == ref), None)
        amount = 0
        if kind in ('promise', 'boundary', 'proposal', 'loyalty'):
            key = {'promise': 'promises', 'boundary': 'boundaries', 'proposal': 'proposals', 'loyalty': 'loyalties'}[kind]
            if kind == 'proposal' and not proposal_allowed(s, who):
                continue
            if kind == 'proposal' and event.get('proposal_type', 'relationship_talk') not in ('date', 'introduction', 'relationship_talk'):
                continue
            if any(v['detail'].casefold() == detail.casefold() for v in p[key]):
                continue
            ident = ensure(s)['next_id']
            ensure(s)['next_id'] += 1
            p[key].append(dict(id=ident, detail=detail, quote=quote, minute=now, owners=owners,
                               status='open', due=now + due if kind == 'promise' and due >= 0 else None))
            if kind == 'proposal':
                p[key][-1]['proposal_type'] = event.get('proposal_type', 'relationship_talk')
        elif kind in ('kept', 'broken'):
            if not item or item['status'] not in ('open', 'overdue'):
                continue
            item['status'] = kind
            item['owners'] = [owner for owner in item['owners'] if owner in owners]
            amount = 5 if kind == 'kept' else -8
            if kind == 'broken':
                hurt(s, who, 'Broken promise: ' + item['detail'])
            elif p['repair'].get('acknowledged'):
                p['repair']['changed_days'] = sorted(set([*p['repair']['changed_days'], now//1440]))
        elif kind in ('respected', 'crossed'):
            if not item or item.get('response_days', {}).get(kind) == now//1440:
                continue
            item.setdefault('response_days', {})[kind] = now//1440
            item['last_day'] = now//1440
            item['last_response'] = kind
            item['response_owners'] = owners
            amount = 2 if kind == 'respected' else -8
            if kind == 'crossed':
                hurt(s, who, 'Crossed boundary: ' + item['detail'])
        elif kind == 'acknowledge':
            harm = stats(s, who).get('unresolved_harm')
            if not harm:
                continue
            if not p['repair'] or p['repair'].get('harm') != harm or 'resolved' in p['repair']:
                hurt(s, who, harm)
            if not p['repair'].get('acknowledged'):
                p['repair'].update(acknowledged=True, acknowledged_day=now//1440, acknowledgment=quote)
        elif kind == 'changed':
            if not p['repair'].get('acknowledged'):
                continue
            p['repair']['changed_days'] = sorted(set([*p['repair']['changed_days'], now//1440]))
        elif kind == 'forgive':
            if not repair_ready(s, who):
                continue
            r = stats(s, who)
            r.pop('unresolved_harm', None)
            r['jealousy'] = 0
            if r.get('status') == 'strained':
                r['status'] = 'official'
            p['repair']['resolved'] = now
            amount = 5
        elif kind in ('accept', 'decline'):
            if not item or item['status'] != 'open':
                continue
            item.update(status='accepted' if kind == 'accept' else 'declined', minute=now)
            item['owners'] = [owner for owner in item['owners'] if owner in owners]
        elif kind == 'disclosure':
            if protectiveness.PROTECTORS.get(detail) != who:
                continue
            protectiveness.observe(s, detail, 'romance disclosed by player', [who])
            s.get('protectiveness', {}).get(f'{who}:{detail}', {})['source'] = 'player disclosure'
        adjust(s, who, amount)
        approval(s, who, amount, owners, detail)
        p['evidence'].append(fingerprint)


def context(s, who, listeners):
    p = peek(s, who)
    # Private records inform a speaker privately; do not reveal them to a group.
    def visible(rows):
        result = []
        for row in rows:
            if not set(listeners).issubset(row['owners']):
                continue
            row = dict(row)
            if not set(listeners).issubset(row.get('response_owners', row['owners'])):
                for key in ('last_response', 'last_day', 'response_owners', 'response_days'):
                    row.pop(key, None)
            result.append(row)
        return result
    private = listeners == [s['player']]
    return dict(promises=visible(p['promises']), boundaries=visible(p['boundaries']),
        proposals=visible(p['proposals']), loyalties=visible(p['loyalties']),
        repair=p['repair'] if private else {}, repair_ready=repair_ready(s, who) if private else False,
        unresolved_harm=stats(s, who).get('unresolved_harm') if private else None,
        proposal_allowed=proposal_allowed(s, who) if private else False,
        direction='Remember concrete commitments and individually expressed boundaries. Ask about overdue promises without inventing excuses. '
        'Repair requires specific accountability, corrective action on a later day and freely offered forgiveness. '
        'When eligible, occasionally initiate a personal date, introduction or relationship conversation in your own voice; '
        'a proposal is not acceptance or an official status change. Respect a declined proposal and do not repeatedly press. '
        'Rei may feel torn between friendship with the player and concern for Emily or Yuriko; Garrett between friendship '
        'and concern for April; Ivan between affection for Valentina and disapproval. When this is known and relevant, '
        'let the protected person challenge intrusive behaviour and state their own wishes. Do not manufacture conflict every turn.')


def notebook(s, who):
    p = s.get('relationship_dynamics', {}).get('people', {}).get(who, {})
    lines = []
    for key, title in (('promises', 'Promise'), ('boundaries', 'Boundary'), ('proposals', 'Their invitation'), ('loyalties', 'Loyalty')):
        for r in p.get(key, []):
            lines.append(f"{title} · {r['detail']}" + (f" — {r['status']}" if key in ('promises', 'proposals') else ''))
    if p.get('repair') and 'resolved' not in p['repair']:
        lines.append('Making amends · ' + p['repair']['harm'])
    return lines
