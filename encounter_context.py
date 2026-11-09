"""Meeting provenance and agreed plans, independent of dialogue channel changes."""

DIRECTION = (
    'Use meeting_context to frame this encounter. A spontaneous visit was not arranged: react '
    'with recognition, surprise, warmth, irritation or distraction as appropriate to your relationship '
    'and activity, without claiming you expected the player. A planned meeting was agreed beforehand; '
    'remember the supplied arrangement. Compare its stated place/time with the current scene: an early '
    'or off-location encounter is still an unexpected drop-in, not proof the planned outing happened. '
    'A visitor came to the player: on the opening invent a modest, '
    'plausible personal reason for dropping by, grounded in their interests, relationship and circumstances. '
    'Never mention a summon command or assume the player called them. Do not invent an emergency, '
    'purchase, gift, intimate history or prior invitation. Keep that reason consistent with the recorded '
    'conversation on later turns, rather than inventing a new reason every reply. These are adult peers '
    'with independent wishes; an unexpected visit is not automatically welcomed or romantic. '
    'New arrivals react to the current gathering without making everyone greet again.')

PLAN_DIRECTION = (
    'Return meeting_plans for explicit agreements or cancellations made in this exchange, otherwise []. '
    'Each entry has who, status (agreed or cancelled), and details (a short factual summary of the '
    'agreed place/time/purpose, only as actually stated). Include only participants who explicitly '
    'agree with the player. A suggestion, invitation without acceptance, hypothetical, or an unsent '
    'suggested player reply is NOT an agreement. Do not schedule travel or change location. '
    'Record only meetings that have not begun, not the hangout currently in progress. '
    'A future agreement is remembered but does not make anyone join a party now.')


def add_schema(schema, members):
    schema['properties']['meeting_plans'] = {'type': 'array', 'items': {
        'type': 'object', 'properties': {'who': {'type': 'string', 'enum': list(members)},
        'status': {'type': 'string', 'enum': ['agreed', 'cancelled']},
        'details': {'type': 'string', 'maxLength': 400}},
        'required': ['who', 'status', 'details'], 'additionalProperties': False}, 'maxItems': len(members)}
    schema['required'].append('meeting_plans')


def validate(data, members=None):
    if not isinstance(data, dict): raise ValueError('Invalid meeting response.')
    plans = data.get('meeting_plans', [])
    if not isinstance(plans, list): raise ValueError('Invalid meeting agreements.')
    seen = set()
    for plan in plans:
        if (not isinstance(plan, dict) or not isinstance(plan.get('who'), str)
                or plan['who'] in seen or (members is not None and plan['who'] not in members)
                or plan.get('status') not in ('agreed', 'cancelled')
                or not isinstance(plan.get('details'), str) or not 1 <= len(plan['details'].strip()) <= 400):
            raise ValueError('Invalid meeting agreement.')
        seen.add(plan['who'])


def record(s, data, members):
    validate(data, members)
    for plan in data.get('meeting_plans', []):
        plans = s.setdefault('meeting_plans', {})
        import memory_store
        previous=plans.get(plan['who'])
        prior=memory_store.plan_record(s,plan['who'],previous,'agreed') if previous else None
        memory_store.plan_record(s,plan['who'],dict(details=plan['details'].strip(),agreed_at=s['world']['minute']),
                                 plan['status'],prior,owners=[s['player'],*members])
        if plan['status'] == 'cancelled': plans.pop(plan['who'], None)
        else: plans[plan['who']] = {'details': plan['details'].strip(), 'agreed_at': s['world']['minute']}


def begin(s, group):
    contexts = {}
    for who in group['members']:
        plan = s.get('meeting_plans', {}).pop(who, None)
        if plan:
            import memory_store
            prior=memory_store.plan_record(s,who,plan,'agreed')
            memory_store.plan_record(s,who,plan,'met; planned activity completion unconfirmed',prior)
        actor = s['world']['cast'].get(who, {})
        date = s.get('date_session', {})
        planned = bool(plan or actor.get('waiting_for_hangout') or date.get('partner') == who)
        contexts[who] = {'kind': 'planned' if planned else 'spontaneous',
                         'minute': s['world']['minute'], 'location': s['world']['location'],
                         'activity_before_meeting': actor.get('activity'),
                         'arrangement': plan or ('Accepted date' if date.get('partner') == who else
                                                  'Accepted invitation to hang out' if planned else None)}
    group['meeting_context'] = contexts


def for_participants(s, members):
    active = s.get('groups', {}).get(s.get('active_group'), {})
    return {'direction': DIRECTION,
            'meeting_context': {who: active.get('meeting_context', {}).get(who) for who in members},
            'current_meeting_exchange': active.get('history', [])[active.get('journal_offset', 0):][-12:]
                if active.get('open') and set(active.get('members', [])).intersection(members) else [],
            'agreed_future_plans': {who: s.get('meeting_plans', {}).get(who) for who in members}}
